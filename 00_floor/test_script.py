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
import numpy as np
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

""" Determine the correct start time and segment length based on the graphs of the raw data """
# Graph of the raw data: p_es, p_air, volume and flow over time
graphs_raw_data(p_es, p_air, volume, flow, FS, length)

#%%
""" Import and name data """
# Start and get entries from graphical user interface
#[params, input_txt_file, output_xlsx_file] = graphical_user_interface()

from graphical_user_interface_input_file import graphical_user_interface_input_file
input_txt_file_w = graphical_user_interface_input_file()
#input_txt_file = [r'C:\Users\fwhiemstra\Documents\Python-projects\mechanical_ventilation_params\test-data\MV-spontaneous-breathing-data/1__211006132800_Waves_001.txt']
#input_txt_file = [r'C:\Users\fwhiemstra\Documents\Python-projects\mechanical_ventilation_params\test-data\Additional artefact data\001\W_Hamilton-C6__220321153431_Waves_001.txt']

output_xlsx_file = r'C:\Users\fwhiemstra\Documents\Python-projects\mechanical_ventilation_params\test-data\MV-spontaneous-breathing-data/output_test.xlsx'
params = ['123', 2, 'test']

# Import data from chosen input file
input_file_w = input_txt_file_w[0]
[p_air_w, p_es_w, flow_w, volume_w] = import_data(input_file_w)


""" Set variables"""
# Calculate length of the measured signal
length_w = flow_w.shape[0]
for i in range(length_w-1):
    if flow_w[i] == '--':
        flow_w[i] = 0
    else:
        flow_w[i] = float(flow_w[i])
flow_w = pd.to_numeric(flow_w)

# Calculate the total time measured [minutes]
t_dur_w = math.floor(len(flow_w)/FS/60)
# Patient number
patient_id = params[0]

""" Determine the correct start time and segment length based on the graphs of the raw data """
# Graph of the raw data: p_es, p_air, volume and flow over time
graphs_raw_data(p_es_w, p_air_w, volume_w, flow_w, FS, length_w)