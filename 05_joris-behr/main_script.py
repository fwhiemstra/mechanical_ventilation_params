"""
Power calculator in patients ventilated in spontaneous mode with pressure support if needed
(Main script)

Assignment for Technical Medicine
Commissioned by the Intensive Care Unit of Leiden University Medical Center
Code is designed to handle decrypted files 'W-files' from Hamilton C6 Mechanical Ventilator

Based on a MATLAB script made by: Marloes van der Werf, Jeroen Roest,
Floor Hiemstra & Max Ligtenberg

Author: Sanne van Deelen
Date: February 2021

Modified by Bart Keulen
Date: October 2021

Modified by Anne Meester
Date: February 2022

Modified by Jill Oudshoorn
Date: July 2022

"""

""" Import modules and functions """
# Import python functions
import math
from pathlib import PurePath
import matplotlib.pyplot as plt
import os
import sys
import pandas as pd

from hamilton_vs_script import ham_vs_script
my_dir = r'C:\Users\joris\OneDrive\Documenten\Studie\TM jaar 2&3\Q1\mechanical_ventilation_params\05_joris-behr'
#my_dir = r'C:\Users\jiddl\Desktop\stage 4\python codes\code-Jill-Oudshoorn'
os.chdir(my_dir)
sys.path.append(my_dir)

# Import modules
from constants import FS, PRESSURE_TYPE
from graphical_user_interface import graphical_user_interface
from import_and_process_data import import_data
from pressure_type_detection import pressure_type_detection
from graphs_raw_data import graphs_raw_data
from determine_segment import determine_segment
from trim_recording import trim_recording
from respiratory_rate_fft import respiratory_rate_fft
from inspiration_detection import inspiration_detection
from inspiration_detection_2 import inspiration_detection_2
from tidal_volume_calculator import tidal_volume_calculator
from peep_calculator import peep_calculator
from ptp_calculator import ptp_calculator
from tp_parameter_calculator import tp_parameter_calculator
from energy_calculator import energy_calculator
from pv_energy_calculator import pv_energy_calculator
from statistics_calculator import sd_se_statistics, correlations
from graphs import graphs
from graphs_ham_vs_script import graphs_vs
from summary import summary
from select_output_file import select_output_file
from hysteresis_area import hysteresis_area
from export_csv import export_csv
from annotate_import import annotate_import
from artefact_scoring import artefact_scoring
from coughdetection import coughdetection
from print_results import print_results
from inspiration_hamilton import breaths_hamilton
from inspiration_detection_2 import inspiration_detection_2
from export_params import export_params, param_to_df
from pes_pcw_correction import pes_pcw_correction

#%%
"choises of skipping parts of the script"
# Next to calculating the mechanical power this script is capable of 
# 1. cough detection and filtering, 
# 2. calculating the sensitivity of artefact detection when given an annotated script from trainset.nl
# 3. creating a csv file that can be uploaded on trainset.nl to annotate the data
# 4. graphs can be put on and off.
# 0 = off
# 1 = on
# 5. Different inspiration detection algoritms can be compared: 
# Select script2, script1 or hamilton


# Settings
artefactdetection = 1
exportCSV = 0
graph = 0
annotation = 0
params = ['234', 2, 'test']
insp_detection = 'script2'
insp_comp = ''
input_file = r'C:\Users\joris\OneDrive\Documenten\Studie\TM jaar 2&3\Q1\data\wave_mode\9\Waves_009.txt'
output_xlsx_file = []
#

""" Annotate, Import and name data """
if annotation == 1:
    [p_air, p_es, flow, volume, artefact_timestamp, artefact_timestamp_compressed ] = annotate_import(input_file, input_annotation, FS)
else:
    [p_air, p_es, flow, volume,breath_no] = import_data(input_file)

#%%
""" Set variables"""
# Calculate length of the measured signal
length = flow.shape[0]
# Calculate the total time measured [minutes]
t_dur = math.floor(len(flow)/FS/60)

# Patient number
patient_id = params[0]

"""export CSV"""
#writes the import data into a csv file applicable for the annotation programm trainset
if exportCSV ==1:
    export_csv(p_es, p_air, volume, flow, FS, length, patient_id, t_dur)

p_es,pcw = pes_pcw_correction(p_es)
print(pcw)

"""Artefact detection"""
# detects coughs, filters the coughs and returns a list with cough parameters
if artefactdetection == 1:
    p_es,p_air,flow,volume,breath_no, artefact_detection, cough_time_total, cough_time_percentage, number_coughs, mean_cough_power, mean_cough_amplitude, mean_cough_length, mean_cough_inbetweentime, mean_cough_peak_flow,max_cough_peak_flow,  percentage_hard_coughs = coughdetection(p_es, p_air, volume, flow,breath_no)
    #if number_coughs != 0 :
        # returns the cough parameters in a table
        # print_results(patient_id, cough_time_total, cough_time_percentage, number_coughs, mean_cough_power, mean_cough_amplitude, mean_cough_length, mean_cough_inbetweentime, mean_cough_peak_flow, max_cough_peak_flow, percentage_hard_coughs )

""" Artefact scoring"""
# determines the accuracy of the cough detection, based on annotated data
if annotation == 1 and number_coughs != 0:
    artefact_scoring(artefact_detection, artefact_timestamp, artefact_timestamp_compressed)

#%%
""" Determine the correct start time and segment length based on the graphs of the raw data without coughs"""
# Graph of the raw data: p_es, p_air, volume and flow over time
if graph ==1:
    graphs_raw_data(p_es, p_air, volume, flow, FS)
# Determine correct start time and segment length
t_dur = math.floor(len(flow)/FS/60)

# print(f'The length of the signal is {t_dur}')
# determine_segment(params,t_dur)

# Code to run full script.
params.append(t_dur)
params.append(0)


# # Variable segment length
if params[3] == '':
    segment_len = 0  # No segment length is defined
else:
    segment_len = int(params[3]) * FS * 60  # Segment length is defined
# Delay to start segment of interest [seconds]
if params[4] == '':
    rec_delay = 0  # Delay is zero when no starting time is defined
else:
    rec_delay = int(params[4]) * FS  # Starting time is defined

#%%
""" Determine pressure type """
# 1=airway pressure OR 2=transpulmonal + airway pressure
pressure_type = pressure_type_detection(p_es)

#%%
""" input file name """
input_filename = PurePath(input_file).stem + PurePath(input_file).suffix

#%%
""" General code """
# # Cut recording based on specified segment length and start time
[volume_trim, flow_trim, p_air_trim, p_es_trim,breath_no_trim, segment_time_sec, data_length] = trim_recording(
    rec_delay, FS, p_es, segment_len, volume, flow, p_air,breath_no, length)

#%%
# Calculate respiratory rate - based on median frequency
rr = respiratory_rate_fft(volume_trim)

#%%
# Detecting the start- and end points of inspiration using one of the created versions
if insp_detection == 'script1':
    [start_insp, start_insp_values, end_insp, end_insp_values] = inspiration_detection(
         volume_trim, p_es_trim, flow_trim, rr)
elif insp_detection == 'script2':
    start_insp, start_insp_values, end_insp, end_insp_values = inspiration_detection_2(flow_trim, rr)
elif insp_detection == 'hamilton':
# Detecting the start- and endpoints of inspiration using the breath numbers from the hamilton device
    start_insp, end_insp, start_insp_values, end_insp_values = breaths_hamilton(flow_trim,breath_no_trim, rr)

if insp_comp == 'script1':
    [start_insp_2, start_insp_values_2, end_insp_2, end_insp_values_2] = inspiration_detection(
         volume_trim, p_es_trim, flow_trim, rr)
elif insp_comp == 'script2':
    start_insp_2, start_insp_values2, end_insp_2, end_insp_values_2 = inspiration_detection_2(flow_trim, rr)
elif insp_comp == 'hamilton':
    start_insp_2, end_insp_2, start_insp_values_2, end_insp_values_2 = breaths_hamilton(flow_trim,breath_no_trim, rr)


#%%
# Calculating tidal volume
[tidal_volume, mean_tidal_volume] = tidal_volume_calculator(end_insp, volume_trim)
#%%
# Calculating PEEP
[peep, mean_peep] = peep_calculator(start_insp, p_air_trim)
#%%
""" Calculate the energy of the airway pressures (Pair) using the energy calculator """
[e_aw, e_aw_mean, pow_aw, pow_air_mean] = energy_calculator(
    'p_air', start_insp, end_insp, p_air_trim, volume_trim)
#%%
""" Plot the three PV loops in one figure """
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, sharex = 'all', sharey = 'all')
fig.suptitle('Pressure volume loops')
#%%
""" Define the PV-loops and calculate the dynamic energy and power for the airway pressure """
# Calculate Hysteresis Area (HA)
[e_hys_aw, e_hys_aw_mean,hys_aw, hys_aw_mean] = pv_energy_calculator(start_insp, end_insp, p_air_trim, volume_trim, 'Airway pressure', ax1)


#%%
""" Calculations for transpulmonary pressure if Pes is not zero (Ptransp = Paw-Pes) """
if pressure_type == PRESSURE_TYPE.TRANSPULMONARY:
    # Calculate the transpulmonary pressure
    p_tp_trim = []
    for elem_air, elem_es in zip(p_air_trim, p_es_trim):
        p_tp_elem = elem_air - elem_es
        p_tp_trim.append(p_tp_elem)

    """ Calculate dynamic energy using the energy calculator """
    # Calculate transpulmonary work and power
    [e_tp, e_tp_mean, pow_tp, pow_tp_mean] = energy_calculator(
    'p_tp', start_insp, end_insp, p_tp_trim, volume_trim)
    
    # Calculate esophageal work and power
    [e_es, e_es_mean, pow_es, pow_es_mean] = energy_calculator(
    'p_es', start_insp, end_insp, p_es_trim, volume_trim)

    """ Calculate the hysteresis using the pv energy calculator"""
    [e_hys_tp, e_hys_tp_mean,hys_tp, hys_tp_mean] = pv_energy_calculator(
        start_insp, end_insp, p_tp_trim, volume_trim, 'Transpulmonary pressure', ax3)

    [e_hys_es, e_hys_es_mean,hys_es, es_loop_power] = pv_energy_calculator(
        start_insp, end_insp, p_es_trim, volume_trim, 'Esophageal pressure', ax2)

    """ Calculate pressure time product (PTP) """
    [ptp_es, ptp_es_mean] = ptp_calculator('p_es', p_es_trim, start_insp, end_insp)
    [ptp_tp, ptp_tp_mean] = ptp_calculator('p_tp', p_tp_trim, start_insp, end_insp)

    """ Calculate different parameters: pressure peak and pressure swing """
    [tp_peak, tp_peak_mean, tp_swing, tp_swing_mean] = tp_parameter_calculator(p_tp_trim, start_insp, end_insp)

    """ If Pes = 0 --> parameters are 'None' """
elif pressure_type == PRESSURE_TYPE.AIRWAY:
    # Set all tp and es output variables to None
    p_tp_trim = None
    wob_tp_breath = None
    wob_tp_mean = None
    wob_es_breath = None
    wob_es_mean = None
    hys_tp = None
    hys_tp_mean = None
    ptp_es = None
    ptp_es_mean = None
    ptp_tp = None
    ptp_tp_mean = None
    tp_peak = None
    tp_peak_mean = None
    tp_swing = None
    tp_swing_mean = None

#%%
""" Statistics """
[standard_deviations, standard_errors] = sd_se_statistics(pow_aw, hys_aw, hys_es, hys_tp,
                                                    pow_es, pow_tp, ptp_es, ptp_tp,
                                                    tp_peak, tp_swing, pressure_type)

# correlation = correlations(pow_aw, hys_aw, hys_es, hys_tp,
#                                                     pow_es, pow_tp, ptp_es, ptp_tp,
#                                                     tp_peak, tp_swing)

#%%
""" Display of the results """
# Compare inspiration detection resulsts
if insp_comp != "":
    ham_vs_script(start_insp,start_insp_2,flow_trim,insp_detection,insp_comp)
    if graph == 1:
        graphs_vs( 
        p_air_trim, p_es_trim, p_tp_trim, volume_trim, flow_trim, end_insp,end_insp_2, start_insp,start_insp_2,
                end_insp_values, start_insp_values,segment_time_sec, pressure_type, insp_detection, insp_comp)
# Show graphs
if graph == 1:
    graphs(
        p_air_trim, p_es_trim, p_tp_trim, volume_trim, flow_trim, end_insp, start_insp,end_insp_values, start_insp_values,
        segment_time_sec, pressure_type)

# Show summary of the results
# summary( 
#     patient_id, pressure_type, rr, mean_tidal_volume, mean_peep,
#     pow_air_mean, pow_tp_mean, pow_es_mean, hys_aw_mean, hys_tp_mean, ptp_es_mean,
#     ptp_tp_mean, tp_peak_mean, tp_swing_mean)


# transform parameters to one single dataframe
param = param_to_df(e_aw, e_es, e_tp, pow_aw, pow_es, pow_tp,e_hys_aw, e_hys_es, e_hys_tp, hys_aw, hys_es, hys_tp, ptp_es, ptp_tp, tp_peak, tp_swing)

# Create excel file from parameter values
# export_params(e_aw, e_es, e_tp, pow_aw, pow_es, pow_tp,e_hys_aw, e_hys_es, e_hys_tp, hys_aw, hys_es, hys_tp, ptp_es, ptp_tp, tp_peak, tp_swing)

# Export results to output file
output_option = params[1]  # 1 = use existing output file, 2 = create new output file
new_output_name = params[2]  # name for new .xlsx file, if new-file-option is chosen

# [output_file, output_filename] = select_output_file(output_option, new_output_name, output_xlsx_file, input_filename,
#     patient_id, pressure_type, data_length, rr, mean_tidal_volume, pow_air_mean,
#     mean_peep, ptp_es_mean, ptp_tp_mean, pow_es_mean, pow_tp_mean, es_loop_power, hys_aw_mean, hys_tp_mean, tp_peak_mean,
#     tp_swing_mean, standard_deviations, standard_errors)