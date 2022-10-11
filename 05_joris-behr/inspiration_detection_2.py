"""
Script to firstly detect the start of inspiration based on flow data. Subsequently find begin expiratory data.

Author: Joris Behr
Date: October 2022
"""
from tracemalloc import start
import numpy as np
import math

from import_and_process_data import import_data
from coughdetection import coughdetection
from graphs_raw_data import graphs_raw_data
from constants import ADJ_HAM, FS
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

    # Finding start inspiration based on flow and flow threshold
    start_insp = list()
    for idx,_ in enumerate(flow):
        if idx+dist < len(flow):
            if flow[idx] <= 0 and flow[idx+1] >= 0 and flow[idx+dist] > 100:
                if len(start_insp) >0:
                    if start_insp[-1] +separation < idx:
                        start_insp.append(idx)
                else:
                    start_insp.append(idx)
            else:
                pass

    # Trying to find start insp based on flow acceleration, as described by M. Ligtenberg en F. Hiemstra            
    flow_diff = np.diff(flow)
    idx_peak, _= find_peaks(flow_diff, height=60,distance=separation)
    idx_peak = idx_peak[flow[idx_peak]>-100]
    
    # Flow acceleration data are not very precise, thus y
    # flow data is used to find places where flow flips pos/neg or other way around.

    for i, idx in enumerate(idx_peak):
        if flow[idx]>20:
            if idx - 400 <0:
                id_0 = np.where(np.diff(np.sign(flow[0:idx])))[0]
                try:
                    idx_peak[i] = id_0[-1]
                except:
                    print(idx)
            else:
                id_0 = np.where(np.diff(np.sign(flow[idx-400:idx])))[0]
                try:
                    idx_peak[i] = id_0[-1]+idx-400
                except:
                    print(idx)
        if flow[idx]<-20:
            if idx + 400 >len(flow):
                id_0 = np.where(np.diff(np.sign(flow[idx:-1])))[0]
                try:
                    idx_peak[i] = id_0[0]
                except:
                    print(idx)
            else:
                id_0 = np.where(np.diff(np.sign(flow[idx:idx+400])))[0]
                try:
                    idx_peak[i] = id_0[-1]+idx
                except:
                    print(idx)
    
    # Calculating end inspiratory time by searching for point where
    # flow shifts from positive to negative and is followed by -100ml/s flow.
    
    # region of interest to search for inspiration after inspiration
    exp_roi = (0.5*np.diff(start_insp)).astype(int) 
    t_blank = 20
    end_insp = list()
    

    # for idx,val in enumerate(start_insp[0:-1]):
    #     for i in range(val+t_blank, val+exp_roi[idx]):
    #         if flow[i] >0 and flow[i+1] <0 and flow[i+dist] <-100:
    #             # end_insp_ham[idx] = i
    #             end_insp.append(i)
    #         else:
    #             pass

    # for idx,val in enumerate(start_insp[0:-1]):
    #     a = find_nearest(flow[val+t_blank:val+exp_roi[idx]],0)+val+t_blank
    #     # if flow[a]+50 < -100:
    #     end_insp.append(a)
    #     # else:
    #     #     end_insp.append(find_nearest(flow[a+1:a+exp_roi[idx]],0)+a)

    for idx, val in enumerate(start_insp[0:-1]):
        for i in range(val+t_blank,val+exp_roi[idx]):
            if flow[i] >= 0 and flow[i+1]< 0 and flow[i+50] <=-100:
                end_insp.append(i)
        
    

        

    print(f'length insp: {len(start_insp)} \nlength exp: {len(end_insp)}\nlength insp peaks {len(idx_peak)}' )

    #defining times
    start_insp_time = [i / FS for i in start_insp]
    end_insp_time = [i / FS for i in end_insp]
    time_sec = [i / FS for i in range(0, len(flow))] # Time in seconds for plot

    #defining start and end values
    start_insp_val = flow[start_insp]
    end_insp_val = flow[end_insp]

    # figures
    fig = plt.figure()
    ax1 = fig.add_subplot(2,1,1)
    start_insp_scat = ax1.scatter(start_insp_time, flow[start_insp], c='g')
    end_insp_scat  = ax1.scatter(end_insp_time,flow[end_insp], marker="x", c='y')
    ax2 = fig.add_subplot(2,1,2,sharex = ax1)
    ax2.plot(time_sec[0:-1],flow_diff)
    peak_scatter = ax1.scatter(np.asarray(time_sec)[idx_peak],flow[idx_peak], c='r')
    ax2.scatter(np.array(time_sec)[idx_peak],flow_diff[idx_peak], c='r')
    ax1.plot(time_sec, flow, 'k')
    ax1.legend((start_insp_scat,end_insp_scat, peak_scatter),
        ('Start inspiration', 'End inspiration', 'Start inspiration using peaks'), loc='upper right', shadow=True)
    ax1.set_title(r'Flow')
    ax2.set_title(r'Flow acceleration')
    ax1.set_ylabel(r'Pressure [cmH2O]')
    ax1.set_xlabel(r'Time [s]')
    plt.tight_layout()
    plt.show()

    start_insp = start_insp[0:-1]

    return start_insp, start_insp_val, end_insp, end_insp_val


if __name__ == '__main__':
    input_file = r'C:\Users\joris\OneDrive\Documenten\Studie\TM jaar 2&3\Q1\data\wave_mode\10\Waves_010.txt'
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




    