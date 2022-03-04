"""
Mechanical power calculator for transpulmonary and total mechanical power.
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
"""

# Set path settings
import os
import sys
my_dir = r'C:\Users\fwhiemstra\Documents\Python code\ICU_Circadian_Rhythms\scripts\mechanical_ventilation\code-bart-keulen'
os.chdir(my_dir)
sys.path.append(my_dir)

# Import python functions
import math
from pathlib import PurePath
from constants import VENTILATION_MODE, INSP_HOLD, FS, PRESSURE_TYPE

# Import modules
from graphical_user_interface import graphical_user_interface
from import_data import import_data
from pressure_type_detection import pressure_type_detection
from trim_recording import trim_recording
from respiratory_rate_fft import respiratory_rate_fft
from inspiration_detection import inspiration_detection
from tidal_volume_calculator import tidal_volume_calculator
from peep_calculator import peep_calculator
from ptp_calculator import ptp_calculator
from tp_parameter_calculator import tp_parameter_calculator
from energy_calculator import energy_calculator
from pv_loop_definition import pv_loop_definition
from pv_energy_calculator import pv_energy_calculator
from sd_se_statistics import sd_se_statistics
from graphs import graphs
from summary import summary
from select_output_file import select_output_file

# Start and get entries from graphical user interface
[params, input_txt_file, output_xlsx_file] = graphical_user_interface()

#%%
params = ['123', 2, '1', '10', 1, 1, 1, '', 0]
input_txt_file = ['C:/Users/fwhiemstra/Documents/Python code/ICU_Circadian_Rhythms/scripts/mechanical-ventilation/test-data/W_Hamilton__211022142318_Waves_001.txt']
output_xlsx_file = ['C:/Users/fwhiemstra/Documents/Python code/ICU_Circadian_Rhythms/scripts/mechanical-ventilation/code-bart-keulen/output_test.xlsx']

# Import data from chosen input file
input_file = input_txt_file[0]
[p_air, p_es, flow, volume] = import_data(input_file)

# Set variables
""" length of measured signal """
length = flow.shape[0]

""" total time measured [minutes] """
t_dur = math.floor(len(flow)/FS/60)

""" patient number """
patient_id = params[0]

""" inspiratory hold [percentage] (only relevant in VCV recordings) """
ventilation_mode = params[1]
if ventilation_mode == VENTILATION_MODE.VCV:
    insp_hold = params[8]  # 1=0%, 2=10%
elif ventilation_mode == VENTILATION_MODE.PCV:
    insp_hold = INSP_HOLD.NONE

""" 1=airway pressure OR 2=transpulmonal + airway pressure"""
pressure_type = pressure_type_detection(p_es)

""" segment length """
if params[2] == '':
    segment_len = 0  # No segment length is defined
else:
    segment_len = int(params[2]) * FS * 60  # Segment length is defined

""" delay to start segment of interest [seconds] """
if params[3] == '':
    rec_delay = 0  # Delay is zero when no starting time is defined
else:
    rec_delay = int(params[3]) * FS  # Starting time is defined

""" show plots, 1=true/0=false """
show_plots = params[4]

""" display summary table, 1=true/0=false """
summary_ = params[5]

""" input file name """
input_filename = PurePath(input_file).stem + PurePath(input_file).suffix

# General code
[volume_trim, flow_trim, p_air_trim, p_es_trim, segment_time_sec, data_length] = trim_recording(
    rec_delay, FS, p_es, segment_len, volume, flow, p_air, length)
rr = respiratory_rate_fft(volume_trim)
[start_insp, start_insp_values, end_insp, end_insp_values] = inspiration_detection(
    volume_trim, p_air_trim, flow_trim, rr)
[tidal_volume, mean_tidal_volume] = tidal_volume_calculator(start_insp, end_insp, volume_trim)
[peep, mean_peep] = peep_calculator(start_insp, p_air_trim)

#%%
# Calculate mechanical power for airway pressures
[e_breath, mean_e_breath, p_breath, mech_power] = energy_calculator(
    start_insp, end_insp, p_air_trim, volume_trim, rr, peep, dynamic=0)
[dyn_e_breath, dyn_mean_e_breath, dyn_p_breath, dyn_mech_power] = energy_calculator(
    start_insp, end_insp, p_air_trim, volume_trim, rr, peep, dynamic=1)

#%%
# Define the PV-loops and calculate the loop-energy of the airway pressure
[pv_ends, pv_ends_values, pv_starts, pv_starts_values] = pv_loop_definition(
    rr, start_insp, volume_trim)
[aw_e_breath, mean_aw_e_breath, aw_p_breath, aw_loop_power] = pv_energy_calculator(
    pv_starts, pv_ends, p_air_trim, volume_trim)

if pressure_type == PRESSURE_TYPE.TRANSPULMONARY:
    # Calculate the transpulmonary pressure
    p_tp_trim = []
    for elem_air, elem_es in zip(p_air_trim, p_es_trim):
        p_tp_elem = elem_air - elem_es
        p_tp_trim.append(p_tp_elem)

    # Calculate WOB of the esophageal and transpulmonary pressure
    [tp_e_breath, tp_mean_e_breath, wob_tp_breath, wob_tp_mean] = energy_calculator(
    start_insp, end_insp, p_tp_trim, volume_trim, rr, peep, dynamic=0)
    [es_e_breath, es_mean_e_breath, wob_es_breath, wob_es_mean] = energy_calculator(
    start_insp, end_insp, p_es_trim, volume_trim, rr, peep, dynamic=0)

    # Calculate the loop-energy of the transpulmonary pressure
    [tp_e_breath, mean_tp_e_breath, tp_p_breath, tp_loop_power] = pv_energy_calculator(
        pv_starts, pv_ends, p_tp_trim, volume_trim)

    # Calculate parameters for monitoring spontaneous breathing
    [ptp_es, ptp_es_mean] = ptp_calculator(p_es_trim, start_insp, end_insp)
    [ptp_tp, ptp_tp_mean] = ptp_calculator(p_tp_trim, start_insp, end_insp)

    [tp_peak, tp_peak_mean, tp_swing, tp_swing_mean] = tp_parameter_calculator(p_tp_trim, start_insp, end_insp)

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
# Statistics
[standard_deviations, standard_errors] = sd_se_statistics(p_breath, dyn_p_breath, aw_p_breath, tp_p_breath,
                                                    wob_es_breath, wob_tp_breath, ptp_es, ptp_tp,
                                                    tp_peak, tp_swing, pressure_type)

# Show graphs
graphs(
    show_plots, p_air_trim, p_es_trim, p_tp_trim, volume_trim, flow_trim, end_insp, start_insp,
    end_insp_values, start_insp_values, pv_starts, pv_ends, segment_time_sec, pressure_type)

# Show summary of the results
summary( 
    summary_, patient_id, ventilation_mode, pressure_type, rr, mean_tidal_volume, mean_peep,
    mech_power, dyn_mech_power, wob_tp_mean, wob_es_mean, aw_loop_power, tp_loop_power, ptp_es_mean,
    ptp_tp_mean, tp_peak_mean, tp_swing_mean)

# Export results to output file
output_option = params[6]  # 1 = use existing output file, 2 = create new output file
new_output_name = params[7]  # name for new .xlsx file, if new-file-option is chosen

[output_file, output_filename] = select_output_file(output_option, new_output_name, output_xlsx_file, input_filename,
    patient_id, ventilation_mode, pressure_type, data_length, rr, mean_tidal_volume, mech_power, dyn_mech_power,
    insp_hold, mean_peep, ptp_es_mean, ptp_tp_mean, wob_es_mean, wob_tp_mean, aw_loop_power, tp_loop_power, tp_peak_mean,
    tp_swing_mean, standard_deviations, standard_errors)
