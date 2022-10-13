"""
Script to firstly detect the start of inspiration based on flow data. Subsequently find begin expiratory data.

Author: Joris Behr
Date: October 2022
"""
from tracemalloc import start
import numpy as np
from numpy import *

from import_and_process_data import import_data
from coughdetection import coughdetection
from graphs_raw_data import graphs_raw_data
from constants import FS
from import_and_process_data import convert_to_numpy_data
from matplotlib import pyplot as plt
from respiratory_rate_fft import respiratory_rate_fft
from inspiration_detection import inspiration_detection
from trim_recording import trim_recording
from determine_segment import determine_segment
from scipy.signal import find_peaks

def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return idx

def inspiration_detection_2(flow,rr):
    # Parameters
    separation = round(0.3 * (1/rr) * 60 * FS)
    dist = round(0.4*FS)

    # Data transformation
    if type(flow) == list:
        flow = np.array(flow)
    else:
        flow = flow.to_numpy().flatten()

    # Trying to find start insp based on flow acceleration, as described by M. Ligtenberg en F. Hiemstra            
    flow_diff = np.diff(flow)
    _, properties= find_peaks(flow_diff,height=10,distance=separation)
    min_peak_height = 0.7*median(properties['peak_heights'])
    idx_peak, _ = find_peaks(flow_diff,height=min_peak_height,distance=separation)
    
    # Copying peaks to enable plotting them
    xpeak = idx_peak.copy()
    
    
    # Flow acceleration peak data are not very precise, thus
    # flow data is used to find places where flow flips pos/neg or other way around.

    idx_remove = list() # List to add values that should be deleted 
    for i, idx in enumerate(idx_peak):
        if flow[idx]>40:
        # If flow is very positive, find the point where it flips to negative by "looking back"
            if idx - 400 <0:
                id_0 = np.where(np.diff(np.sign(flow[0:idx])))[0]
                try:
                    idx_peak[i] = id_0[-1]
                except:
                    idx_remove.append(idx) # if no flip is found, value should be removed
            else:
                id_0 = np.where(np.diff(np.sign(flow[idx-400:idx])))[0]
                try:
                    idx_peak[i] = id_0[-1]+idx-400
                except:
                    idx_remove.append(idx) # if no flip is found, value should be removed
        elif flow[idx]<-40:
        # If flow is very negative, find point where it flips to positive by "looking forward"
            if idx + 400 >len(flow):
                id_0 = np.where(np.diff(np.sign(flow[idx:-1])))[0]
                try:
                    idx_peak[i] = id_0[0]
                except:
                    idx_remove.append(idx) # if no flip is found, value should be removed
            else:
                id_0 = np.where(np.diff(np.sign(flow[idx:idx+200])))[0]
                try:
                    idx_peak[i] = id_0[0]+idx
                except:
                    
                    idx_remove.append(idx) # if no flip is found, value should be removed
        else:
        # if the value is within bounds, keep it.
            idx_peak[i] = idx 

    # Start of inspiration is defined as points:
    # 1. Where flow shifts neg/pos (not in idx_remove)
    # 2. Flow acceleration is not smaller than -10 ml/s^2
    # 3. Flow is >100 after 20 steps.
    # 4. that are at least seperation distance from previous
    start_insp = np.asarray([v for i,v in enumerate(idx_peak[0:-1]) if (v not in idx_remove and flow_diff[v] >-10 and flow[v+20]>100 and diff(idx_peak)[i] >separation)])
    


    # Finding end inspiration by using flow acceleration:
    # 1. Determining highest negative peak between two inspirations
    # 2. Finding nearest point where flow switches neg-pos(2a) or pos-neg(2b)
    # 3. Set end inspiration at last positive value before switch
    # 4. Remove start insp values that can't meet requirement of step 2.
    end_insp = list()
    end_insp_peak = list()
    val_start_remove = list()
    for val1, val2 in zip(start_insp[0:-1], start_insp[1:]):
        # Step 1
        peak, _ = find_peaks(-flow_diff[val1:val2],distance=separation, height=100)
        end_insp_peak.append(peak[0]+val1)
        if len(peak)>0:
            exp_peak_loc = peak[0]+val1 

            # Step 2a
            if flow[exp_peak_loc] <0:
                new_peak = np.where((np.flip(flow[exp_peak_loc-10:exp_peak_loc]))>0)[0]
                # Step 3
                if len(new_peak) >0:
                    end_insp.append(exp_peak_loc-new_peak[0]-1)
                else:
                    val_start_remove.append(val1)
            # Step 2b
            elif flow[exp_peak_loc] >0:
                new_peak = np.where((flow[exp_peak_loc:exp_peak_loc+10])<=0)[0]
                if len(new_peak) >0:
                    end_insp.append(exp_peak_loc+new_peak[0]-1)
                else:
                    val_start_remove.append(val1)
            else:
                end_insp.append(exp_peak_loc)
        else: 
            val_start_remove.append(val1)
    
    #Step 4
    start_insp = [v for v in start_insp if v not in val_start_remove]

    #defining times
    start_insp_time = [i / FS for i in start_insp]
    end_insp_time = [i / FS for i in end_insp]
    time_sec = [i / FS for i in range(0, len(flow))] # Time in seconds for plot
    
    # # figures
    # fig = plt.figure()
    # ax1 = fig.add_subplot(2,1,1)
    # ax1.plot(time_sec, flow, 'k')
    # start_insp_scat = ax1.scatter(start_insp_time, flow[start_insp], c='g')
    # end_insp_scat  = ax1.scatter(end_insp_time,flow[end_insp], c='y')
    # ax1.legend((start_insp_scat,end_insp_scat,),
    #     ('Start inspiration using peaks', 'End inspiration'), loc='upper right', shadow=True)

    # ax2 = fig.add_subplot(2,1,2,sharex = ax1)
    # ax2.plot(time_sec[0:-1],flow_diff)
    # insp_peak_scat = ax2.scatter(np.array(time_sec)[xpeak],flow_diff[xpeak], c='g')
    # exp_peak_scat = ax2.scatter(np.array(time_sec)[end_insp_peak],flow_diff[end_insp_peak], c= 'y')
    # ax2.legend((insp_peak_scat, exp_peak_scat),('Start inspiration peak', 'End inspiration peak'), loc='upper right', shadow=True)

    # ax1.set_title(r'Flow')
    # ax2.set_title(r'Flow acceleration')
    # ax1.set_ylabel(r'Pressure [cmH2O]')
    # ax1.set_xlabel(r'Time [s]')
    # plt.tight_layout()
    # plt.show()

    start_insp = start_insp[0:-1]

    #defining start and end values
    start_insp_val = flow[start_insp]
    end_insp_val = flow[end_insp]

    return start_insp, start_insp_val, end_insp, end_insp_val


if __name__ == '__main__':
    input_file = r'C:\Users\joris\OneDrive\Documenten\Studie\TM jaar 2&3\Q1\data\wave_mode\3\Waves_003.txt'
    [p_air, p_es, flow, volume, breath_no] = import_data(input_file)
    length = len(p_air)
    params = ['234', 2, 'test']

    p_es,p_air,flow,volume,breath_no, artefact_detection, cough_time_total, cough_time_percentage, number_coughs, mean_cough_power, mean_cough_amplitude, mean_cough_length, mean_cough_inbetweentime, mean_cough_peak_flow,max_cough_peak_flow,  percentage_hard_coughs = coughdetection(p_es, p_air, volume, flow,breath_no)

    # Graph of full (raw) data
    # graphs_raw_data(p_es, p_air, volume, flow, FS)

    # #Selecting part of data
    # t_dur = math.floor(len(flow)/FS/60)
    # print(f'The length of the signal is {t_dur}')
    # determine_segment(params)

    # # Variable segment length
    # if params[3] == '':
    #     segment_len = 0  # No segment length is defined
    # else:
    #     segment_len = int(params[3]) * FS * 60  # Segment length is defined
    # # Delay to start segment of interest [seconds]
    # if params[4] == '':
    #     rec_delay = 0  # Delay is zero when no starting time is defined
    # else:
    #     rec_delay = int(params[4]) * FS  # Starting time is defined
    
    # #Trimming data to segment length
    # [volume_trim, flow_trim, p_air_trim, p_es_trim,breath_no_trim, segment_time_sec, data_length] = trim_recording(
    # rec_delay, FS, p_es, segment_len, volume, flow, p_air,breath_no, length)

    #Determining respiratory rate for inpiration_detection
    rr = respiratory_rate_fft(volume)
    # [start_insp, start_insp_values, end_insp, end_insp_values] = inspiration_detection(
    # volume, p_es, flow, rr)

    #Calculating start indices by using hamilton data vs own script
    start_insp= inspiration_detection_2(flow,rr) 
    # print(len(start_insp_ham))




    