"""
Script to detect inpsiration and expiration based on hamilton data

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

def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return idx

def breaths_hamilton(flow,breath_no,rr):
    #parameters
    time_sec = [i / FS for i in range(0, len(flow))] # Time in seconds for plot
    separation = round(0.3 * (1/rr) * 60 * FS)
    dist = round(0.2*FS)

    if type(breath_no) == list:
        breath_no = np.array(breath_no)
        flow = np.array(flow)
    else:
        breath_no = breath_no.to_numpy().flatten()       # Changing type to numpy array for calculation purposes
        flow = flow.to_numpy().flatten()                 # Idem,  MIGHT CHANGE WITH IMPORT MODULE

    #Finding start inspiratory indices and transforming to time [s] 
    start_insp = np.where(np.diff(breath_no) > 0)

    # Attempt to improve start finding
    start_insp_improved = np.asarray(start_insp).flatten()
    start_insp_improved = start_insp_improved - ADJ_HAM
    start_insp_improved = [i for i in start_insp_improved if flow[i]<250 and flow[i] > -250] # hier morgelijk nog iets doen met de median?

    # Remove values that are too close to eachother or arent followed by positive flow
    
    val_del = list()
    for idx,val in enumerate(start_insp_improved):
        if (separation < start_insp_improved[idx] - start_insp_improved[idx-1]) and (flow[val+dist] > 100):
            pass
        else:
            val_del.append(val)

    start_insp_improved = [ i for i in start_insp_improved if i not in val_del]



    # Search for nearby flow values that are closer to 0
    near = 20
    start_insp_improved_2 = np.zeros(np.shape(start_insp_improved))
    for idx, val in enumerate(start_insp_improved):
        if val - near < 0:
            start_insp_improved_2.append = find_nearest(flow[0:val+near],0) - near
        elif val + near > start_insp_improved[-1]:
            start_insp_improved_2[idx] = find_nearest(flow[val-near:-1],0) +val-near
        else:
            a = find_nearest(flow[val-near:val],0)+val-near
            b = find_nearest(flow[val:val+near],0)+val
            if abs(flow[a]) < abs(flow[b]):
                start_insp_improved_2[idx] = a
            else:
                start_insp_improved_2[idx] = b

    start_insp_improved_2 = start_insp_improved_2.astype(int)
    

    # Calculating end inspiratory 
    t_insp_est = (0.6*np.diff(start_insp_improved_2)).astype(int)
    t_blank = 50
    end_insp_ham = np.zeros(np.shape(t_insp_est))
    
    for idx,val in enumerate(start_insp_improved_2[0:-2]):
        for i in range(val+t_blank, val+t_insp_est[idx]):
            if flow[i] >0 and flow[i+2] <0 and flow[i+dist] <-100:
                end_insp_ham[idx] = i+1 
                # idx+=1
                # i = 0
            else:
                pass
    end_insp_ham = end_insp_ham.astype(int)
    id_0 = np.asarray(np.where(end_insp_ham==0))
    end_insp_ham = np.asarray([v for i,v in enumerate(end_insp_ham) if i not in id_0])
    start_insp_improved_2 = np.asarray([v for i,v in enumerate(start_insp_improved_2) if i not in id_0])
    end_insp_ham = end_insp_ham.astype(int) 

    print(len(end_insp_ham),len(start_insp_improved_2))


    #remove last insp value for equal array lengths
    start_insp_improved_2 = start_insp_improved_2[0:-1]

    #computing time from start indices
    start_insp_time = [i / FS for i in start_insp]
    start_insp_time_improved = [i / FS for i in start_insp_improved]
    start_insp_time_improved_2= [i / FS for i in start_insp_improved_2]
    end_insp_time = [i / FS for i in end_insp_ham]

    #Computing flow values
    start_insp_values = flow[start_insp_improved_2]
    end_insp_values = flow[end_insp_ham]

    # figures
    fig = plt.figure()
    ax1 = fig.add_subplot(1,1,1)
    # ax2 = fig.add_subplot(2,1,2,sharex= ax1)
    # ham_insp = ax1.scatter(start_insp_time, flow[start_insp], c='r')
    ham_insp_impr = ax1.scatter(start_insp_time_improved, flow[start_insp_improved], c='g')
    ham_insp_impr2 = ax1.scatter(start_insp_time_improved_2, flow[start_insp_improved_2], c='y')
    ham_exp = ax1.scatter(end_insp_time,flow[end_insp_ham], marker="x", c='y')
    ax1.plot(time_sec, flow, 'k')
    # ax1.legend(end_exp_scatter,'End of inspiration', loc='upper right', shadow=True)
    # ax2.plot(time_sec,flow,'k')
    # ax2.scatter(start_insp_time_improved_2, flow[start_insp_improved_2], c='y')
    ax1.set_title(r'flow')
    ax1.set_ylabel(r'Pressure [cmH2O]')
    ax1.set_xlabel(r'Time [s]')
    plt.tight_layout()
    plt.show()
    
    return start_insp_improved_2, end_insp_ham, start_insp_values, end_insp_values


if __name__ == '__main__':
    input_file = r'C:\Users\joris\OneDrive\Documenten\Studie\TM jaar 2&3\Q1\data\wave_mode\5\Waves_005.txt'
    [p_air, p_es, flow, volume, breath_no] = import_data(input_file)
    length = len(p_air)
    params = ['234', 2, 'test']

    p_es,p_air,flow,volume,breath_no, artefact_detection, cough_time_total, cough_time_percentage, number_coughs, mean_cough_power, mean_cough_amplitude, mean_cough_length, mean_cough_inbetweentime, mean_cough_peak_flow,max_cough_peak_flow,  percentage_hard_coughs = coughdetection(p_es, p_air, volume, flow,breath_no)

    # Graph of full (raw) data
    graphs_raw_data(p_es, p_air, volume, flow, FS)

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
    start_insp_ham, end_insp_ham= breaths_hamilton(flow,breath_no,rr) 
    # print(len(start_insp_ham))




    