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

EIGEN AANPASSINGEN (updated 4-4-2022):
- Cellen
- Convert object naar float
- Input file selection function
- params/output file selection handmatig ingevoerd
- determine_segments: line 20, 21: segment.quit(), segment.destroy()

FUTURE AANPASSINGEN (updated 4-4-2022):
- GUI lay-out
- Keuze mixed/wave mode
"""

""" Import modules and functions """
# Import python functions
import math
from pathlib import PurePath
import matplotlib.pyplot as plt
import matplotlib
#matplotlib.use('wxAgg')
import os
import sys
my_dir = r'C:\Users\fwhiemstra\Documents\Python-projects\mechanical_ventilation_params\code-anne-meester_versie-floor'
os.chdir(my_dir)
sys.path.append(my_dir)

# Import modules
from constants import FS, PRESSURE_TYPE
from graphical_user_interface import graphical_user_interface
from import_data import import_data
from pressure_type_detection import pressure_type_detection
from graphs_raw_data import graphs_raw_data
from determine_segment import determine_segment
from trim_recording import trim_recording
from respiratory_rate_fft import respiratory_rate_fft
from inspiration_detection import inspiration_detection
from tidal_volume_calculator import tidal_volume_calculator
from peep_calculator import peep_calculator
from ptp_calculator import ptp_calculator
from tp_parameter_calculator import tp_parameter_calculator
from energy_calculator import energy_calculator
from pv_energy_calculator import pv_energy_calculator
from sd_se_statistics import sd_se_statistics
from graphs import graphs
from summary import summary
from select_output_file import select_output_file
from hysteresis_area import hysteresis_area
import pandas as pd

#%%
plt.close('all')
""" Import and name data """
# Start and get entries from graphical user interface
#[params, input_txt_file, output_xlsx_file] = graphical_user_interface()

from graphical_user_interface_input_file import graphical_user_interface_input_file
input_txt_file = graphical_user_interface_input_file()
#input_txt_file = [r'C:\Users\fwhiemstra\Documents\Python-projects\mechanical_ventilation_params\test-data\MV-spontaneous-breathing-data/1__211006132800_Waves_001.txt']
#input_txt_file = [r'C:\Users\fwhiemstra\Documents\Python-projects\mechanical_ventilation_params\test-data\Additional artefact data\001\W_Hamilton-C6__220321153431_Waves_001.txt']

output_xlsx_file = r'C:\Users\fwhiemstra\Documents\Python-projects\mechanical_ventilation_params\test-data\MV-spontaneous-breathing-data/output_test.xlsx'
params = ['123', 2, 'test']

# Import data from chosen input file
input_file = input_txt_file[0]
[p_air, p_es, flow, volume] = import_data(input_file)

""" Set variables"""
# Calculate length of the measured signal
length = flow.shape[0]
# Calculate the total time measured [minutes]
t_dur = math.floor(len(flow)/FS/60)
# Patient number
patient_id = params[0]

""" Convert objects to float64 (in case of mixed mode setting) """
for i in range(length-1):
    if flow[i] == '--':
        flow[i] = 0
    else:
        flow[i] = float(flow[i])
flow = pd.to_numeric(flow)

""" Determine the correct start time and segment length based on the graphs of the raw data """
# Graph of the raw data: p_es, p_air, volume and flow over time
graphs_raw_data(p_es, p_air, volume, flow, FS, length)

#%%
# Determine correct start time and segment length
determine_segment(params)

# Variable segment length
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

""" input file name """
input_filename = PurePath(input_file).stem + PurePath(input_file).suffix

""" General code """
# Cut recording based on specified segment length and start time
[volume_trim, flow_trim, p_air_trim, p_es_trim, segment_time_sec, data_length] = trim_recording(
    rec_delay, FS, p_es, segment_len, volume, flow, p_air, length)

# Calculate respiratory rate - based on median frequency
rr = respiratory_rate_fft(volume_trim)

# Detecting the start- and end points of inspiration
[start_insp, start_insp_values, end_insp, end_insp_values] = inspiration_detection(
    volume_trim, p_es_trim, flow_trim, rr)

# Calculating tidal volume
[tidal_volume, mean_tidal_volume] = tidal_volume_calculator(start_insp, end_insp, volume_trim)

# Calculating PEEP
[peep, mean_peep] = peep_calculator(start_insp, p_air_trim)

#%%
""" Calculate the energy of the airway pressures (Pair) using the energy calculator """
[e_breath, mean_e_breath, p_breath, air_power] = energy_calculator(
    'p_air', start_insp, end_insp, p_air_trim, volume_trim, peep)

""" Plot the three PV loops in one figure """
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, sharex='all', sharey='all')
fig.suptitle('Pressure volume loops')

""" Define the PV-loops and calculate the Hysteresis Area (HA) for the airway pressure """
# Calculate Hysteresis Area (HA)
[aw_e_breath, mean_aw_e_breath] = pv_energy_calculator(start_insp, end_insp, p_air_trim, volume_trim, 'Airway pressure', ax1)
[aw_p_breath, aw_loop_power] = hysteresis_area(start_insp, aw_e_breath)

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
    [tp_e_breath, tp_mean_e_breath, p_tp_breath, p_tp_mean] = energy_calculator(
    'p_tp', start_insp, end_insp, p_tp_trim, volume_trim, peep)
    # Calculate esophageal work and power
    [es_e_breath, es_mean_e_breath, p_es_breath, p_es_mean] = energy_calculator(
    'p_es', start_insp, end_insp, p_es_trim, volume_trim, peep)

    """ Calculate the hysteresis using the pv energy calculator"""
    [tp_e_breath, mean_tp_e_breath] = pv_energy_calculator(
        start_insp, end_insp, p_tp_trim, volume_trim, 'Transpulmonary pressure', ax3)
    [tp_p_breath, tp_loop_power] = hysteresis_area(start_insp, tp_e_breath)

    [es_e_breath, mean_es_e_breath] = pv_energy_calculator(
        start_insp, end_insp, p_es_trim, volume_trim, 'Esophageal pressure', ax2)
    [es_p_breath, es_loop_power] = hysteresis_area(start_insp, es_e_breath)

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
    tp_p_breath = None
    tp_loop_power = None
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
[standard_deviations, standard_errors] = sd_se_statistics(p_breath, aw_p_breath, es_p_breath, tp_p_breath,
                                                    p_es_breath, p_tp_breath, ptp_es, ptp_tp,
                                                    tp_peak, tp_swing, pressure_type)

#%%
""" Display of the results """
# Show graphs
graphs(
    p_air_trim, p_es_trim, p_tp_trim, volume_trim, flow_trim, end_insp, start_insp,
    end_insp_values, start_insp_values, segment_time_sec, pressure_type)

# Show summary of the results

summary( 
    patient_id, pressure_type, rr, mean_tidal_volume, mean_peep,
    air_power, p_tp_mean, p_es_mean, aw_loop_power, tp_loop_power, ptp_es_mean,
    ptp_tp_mean, tp_peak_mean, tp_swing_mean)

# Export results to output file
output_option = params[1]  # 1 = use existing output file, 2 = create new output file
new_output_name = params[2]  # name for new .xlsx file, if new-file-option is chosen

[output_file, output_filename] = select_output_file(output_option, new_output_name, output_xlsx_file, input_filename,
    patient_id, pressure_type, data_length, rr, mean_tidal_volume, air_power,
    mean_peep, ptp_es_mean, ptp_tp_mean, p_es_mean, p_tp_mean, es_loop_power, aw_loop_power, tp_loop_power, tp_peak_mean,
    tp_swing_mean, standard_deviations, standard_errors)