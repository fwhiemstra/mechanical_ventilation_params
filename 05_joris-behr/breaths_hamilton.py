"""
Script to detect inpsiration and expiration based on hamilton data

Author: Joris Behr
Date: October 2022
"""
import numpy as np
import math

from import_and_process_data import import_data
from coughdetection import coughdetection
from graphs_raw_data import graphs_raw_data
from constants import FS, ADJ_HAM
from import_and_process_data import convert_to_numpy_data
from matplotlib import pyplot as plt
from respiratory_rate_fft import respiratory_rate_fft
from inspiration_detection import inspiration_detection
from trim_recording import trim_recording
from determine_segment import determine_segment



def breaths_hamilton(flow,breath_no):
    #parameters
    time_sec = [i / FS for i in range(0, len(flow))] # Time in seconds for plot
    
    if type(breath_no) == list:
        breath_no = np.array(breath_no)
        flow = np.array(flow)
    else:
        breath_no = breath_no.to_numpy().flatten()       # Changing type to numpy array for calculation purposes
        flow = flow.to_numpy().flatten()                 # Idem,  MIGHT CHANGE WITH IMPORT MODULE

    #Finding start inspiratory indices and transforming to time [s] 
    start_insp = np.where(np.diff(breath_no)== 1)
    start_insp_time = [i / FS for i in start_insp]

    # figures
    fig = plt.figure()
    ax1 = fig.add_subplot(2,1,1)
    end_exp_scatter = ax1.scatter(start_insp_time, flow[start_insp], c='r')
    ax1.plot(time_sec, flow, 'k')
    # ax1.legend(end_exp_scatter,'End of inspiration', loc='upper right', shadow=True)
    ax1.set_title(r'flow')
    ax1.set_ylabel(r'Pressure [cmH2O]')
    ax1.set_xlabel(r'Time [s]')
    plt.show()
    
    return start_insp


if __name__ == '__main__':
    input_file = r'C:\Users\joris\OneDrive\Documenten\Studie\TM jaar 2&3\Q1\data\wave_mode\10\Waves_010.txt'
    [p_air, p_es, flow, volume, breath_no] = import_data(input_file)
    length = len(p_air)
    params = ['234', 2, 'test']

    # Graph of full raw data
    graphs_raw_data(p_es, p_air, volume, flow, FS)

    #Selecting part of data
    t_dur = math.floor(len(flow)/FS/60)
    print(f'The length of the signal is {t_dur}')
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
    
    #Trimming data to segment length
    [volume_trim, flow_trim, p_air_trim, p_es_trim,breath_no_trim, segment_time_sec, data_length] = trim_recording(
    rec_delay, FS, p_es, segment_len, volume, flow, p_air,breath_no, length)

    #Determining respiratory rate for inpiration_detection
    rr = respiratory_rate_fft(volume_trim)
    # [start_insp, start_insp_values, end_insp, end_insp_values] = inspiration_detection(
    # volume, p_es, flow, rr)
    #Calculating start indices by using hamilton data vs own script
    [start_insp_ham] = breaths_hamilton(flow_trim,breath_no_trim) 




    