"""
Script to detect inpsiration and expiration based on hamilton data

Author: Joris Behr
Date: October 2022
"""
import numpy as np

from import_data import import_data
from coughdetection import coughdetection
from graphs_raw_data import graphs_raw_data
from constants import FS
from import_and_process_data import convert_to_numpy_data
from matplotlib import pyplot as plt
from respiratory_rate_fft import respiratory_rate_fft
from inspiration_detection import inspiration_detection


def breaths_hamilton(flow,breath_no):
    #parameters
    time_sec = [i / FS for i in range(0, len(flow))] # Time in seconds for plot
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
    input_file = r'C:\Users\joris\OneDrive\Documenten\Studie\TM jaar 2&3\Q1\data\wave_mode\2\2__211110111828_Waves_001.txt'
    [p_air, p_es, flow, volume, breath_no] = import_data(input_file)
    #p_es,p_air,flow,volume,artefact_detection, cough_time_total, cough_time_percentage, number_coughs, mean_cough_power, mean_cough_amplitude, mean_cough_length, mean_cough_inbetweentime, mean_cough_peak_flow,max_cough_peak_flow,  percentage_hard_coughs = coughdetection(p_es, p_air, volume, flow,breath_no)
    graphs_raw_data(p_es, p_air, volume, flow, FS)
    [start_insp] = breaths_hamilton(flow,breath_no)
    rr = respiratory_rate_fft(volume)
    #[start_insp, start_insp_values, end_insp, end_insp_values] = inspiration_detection(
    #volume, p_es, flow, rr)

    