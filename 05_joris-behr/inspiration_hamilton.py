"""
Script to detect inpsiration and expiration based on hamilton breath number data

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
    """Function to find value in an array that is nearest to a given value"""
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return idx

def breaths_hamilton(flow,breath_no,rr):
    """Function to find the start and end inspiration by using the hamilton breath number data. """
    # Parameters
    separation = round(0.3 * (1/rr) * 60 * FS) # Minimal seperation between to inspirations
    dist = round(0.2*FS)                       # Distance between start inspiration and flow threshold

    # Data transformation
    if type(breath_no) == list:
        breath_no = np.array(breath_no)
        flow = np.array(flow)
    else:
        breath_no = breath_no.to_numpy().flatten()
        flow = flow.to_numpy().flatten()

       
    #Finding start inspiratory indices based on change in breath number
    start_insp = np.where(np.diff(breath_no) > 0)

    # Improving inspiration by: 1) Shifting time of start and 2) too high/low values
    start_insp_improved = np.asarray(start_insp).flatten()
    start_insp_improved = start_insp_improved - ADJ_HAM
    start_insp_improved = [i for i in start_insp_improved if flow[i]<250 and flow[i] > -250]

    # Remove values that are too close to eachother or arent followed by positive flow
    val_del = list()
    for idx,val in enumerate(start_insp_improved):
        if (separation < start_insp_improved[idx] - start_insp_improved[idx-1]) and (flow[val+dist] > 100 or flow[val+100] >100):
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

    #Changing datatype so it can be used as index
    start_insp_improved_2 = start_insp_improved_2.astype(int)
    

    # Calculating end inspiratory time by searching for point where
    # flow shifts from positive to negative and is followed by -100ml/s flow.
    
    # region of interest to search for inspiration after inspiration
    exp_roi = (0.6*np.diff(start_insp_improved_2)).astype(int) 
    # Defining blanking period to prevent finding inspiration
    t_blank = 50
    end_insp_ham = np.zeros(np.shape(exp_roi))

    for idx,val in enumerate(start_insp_improved_2[0:-1]):
        for i in range(val+t_blank, val+exp_roi[idx]):
            if flow[i] >0 and flow[i+1] <0 and flow[i+dist] <-100:
                end_insp_ham[idx] = i
            else:
                pass
    
    #Changing datatype so it can be used as index
    end_insp_ham = end_insp_ham.astype(int)

    # Zeros have to be removed, corresponding start values as well
    id_0 = np.asarray(np.where(end_insp_ham==0))
    end_insp_ham = np.asarray([v for i,v in enumerate(end_insp_ham) if i not in id_0])
    start_insp_improved_2 = np.asarray([v for i,v in enumerate(start_insp_improved_2) if i not in id_0])
    end_insp_ham = end_insp_ham.astype(int) 

    #remove last insp value for equal array lengths
    start_insp_improved_2 = start_insp_improved_2[0:-1]

    #computing time from start indices
    time_sec = [i / FS for i in range(0, len(flow))] # Time in seconds for plot
    start_insp_time_improved = [i / FS for i in start_insp_improved]
    start_insp_time_improved_2= [i / FS for i in start_insp_improved_2]
    end_insp_time = [i / FS for i in end_insp_ham]

    #Computing flow values
    start_insp_values = flow[start_insp_improved_2]
    end_insp_values = flow[end_insp_ham]

    # figures
    fig = plt.figure()
    ax1 = fig.add_subplot(1,1,1)
    ham_insp_impr = ax1.scatter(start_insp_time_improved, flow[start_insp_improved], c='g')
    ham_insp_impr2 = ax1.scatter(start_insp_time_improved_2, flow[start_insp_improved_2], c='y')
    ham_exp = ax1.scatter(end_insp_time,flow[end_insp_ham], marker="x", c='y')
    ax1.legend((ham_insp_impr,ham_insp_impr2,ham_exp),
            ('Hamilton inspiration + time shift', 'Hamilton inspiration improved', 'Hamilton expiration'), loc='upper right', shadow=True)
    ax1.plot(time_sec, flow, 'b')
    ax1.set_title(r'flow')
    ax1.set_ylabel(r'Pressure [cmH2O]')
    ax1.set_xlabel(r'Time [s]')
    plt.tight_layout()
    plt.show()
    
    return start_insp_improved_2, end_insp_ham, start_insp_values, end_insp_values


if __name__ == '__main__':
    """If script is run as main script, the following will be done
    1. file is imported
    2. coughs are filtered
    3. data is showed in graph
    4. data can be trimmed
    5. respiratory rate is determined
    6. inspiration is determined based on hamilton"""

    input_file = r'C:\Users\joris\OneDrive\Documenten\Studie\TM jaar 2&3\Q1\data\wave_mode\1\Waves_001.txt'
    [p_air, p_es, flow, volume, breath_no] = import_data(input_file)
    length = len(p_air)
    params = ['234', 2, 'test']

    p_es,p_air,flow,volume,breath_no, artefact_detection, cough_time_total, cough_time_percentage, number_coughs, mean_cough_power, mean_cough_amplitude, mean_cough_length, mean_cough_inbetweentime, mean_cough_peak_flow,max_cough_peak_flow,  percentage_hard_coughs = coughdetection(p_es, p_air, volume, flow,breath_no)

    # Graph of full data
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

    #Calculating start indices by using hamilton data vs own script
    start_insp_ham, end_insp_ham, start_insp_values, end_insp_values= breaths_hamilton(flow,breath_no,rr) 





    