"""
Inspiration detection

Author: Anne Meester
Date: February 2022

"""

import numpy as np
from constants import FS
import pandas as pd


def inspiration_detection(volume_trim, p_es_trim, flow_trim, rr_):
    """
    Returns indices and corresponding flow values of start and end of each inspiration
    """

    # Variables
    # separation = round(0.3 * (1/rr_) * 60 * FS)
    # dist = 40
    # close_dist = 30
    # amplitude = 100
    # end_insp_sep = 50
    # inspirationerror = 0

    # Variables depending on sampling frequency
    separation = round(0.3 * (1/rr_) * 60 * FS)
    dist = round(0.4*FS)
    close_dist = 0.3*FS
    amplitude = 100
    end_insp_sep = round(0.5*FS)
    inspirationerror = 0

    """ Find where flow == 0 """
    # Since the flow data never becomes exactly zero. Find the transition:
    # - From negative to positive --> estimate start inspiration
    # - From positive to negative --> estimate end inspiration
    start_insp_flow = []
    end_insp_flow = []
    a = 0
    i = 0
    while i < len(flow_trim)-dist:
        if flow_trim[i] <= a and flow_trim[i+1] > a and flow_trim[i+dist] > 100:
            start_insp_flow.append(i)
            i += 1
        elif flow_trim[i] >= a and flow_trim[i+1] < a and flow_trim[i+dist] < -100:
            end_insp_flow.append(i)
            i += 1
        else:
            i += 1

    """ Find all estimated start and end points with a minimal separation """
    # Estimated start point
    i = 1
    while i < len(start_insp_flow):
        if separation < start_insp_flow[i] - start_insp_flow[i-1]:
            i += 1
        else:
            del start_insp_flow[i]

    # Estimated end point
    i = 1
    while i < len(end_insp_flow):
        if separation < end_insp_flow[i] - end_insp_flow[i-1]:
            i += 1
        else:
            del end_insp_flow[i]

    # Exclude starts or ends without corresponding starts or ends
    i = -5
    while i < 0:
        if start_insp_flow[-1] > end_insp_flow[i]:
            i += 1
        else:
            del end_insp_flow[i]

    if start_insp_flow[0] > end_insp_flow[0]:
        del end_insp_flow[0]

    if start_insp_flow[-1] > end_insp_flow[-1]:
        del start_insp_flow[-1]

    # Make sure start inspiration and end inspiration alternate
    while len(start_insp_flow) != len(end_insp_flow):
        if len(start_insp_flow) > len(end_insp_flow):
            # print(len(end_insp_flow))
            # print(len(start_insp_flow))
            i = 1
            while i < len(end_insp_flow):
                if start_insp_flow[i] < end_insp_flow[i] and start_insp_flow[i] > end_insp_flow[i-1]:
                    i += 1
                else:
                    del start_insp_flow[i]


        if len(end_insp_flow) > len(start_insp_flow):
            i = 0
            while i < len(start_insp_flow):
                if start_insp_flow[i] < end_insp_flow[i] and end_insp_sep < end_insp_flow[i] - start_insp_flow[i]:
                    i += 1
                else:
                    del end_insp_flow[i]
                    

            

    """ Calculate end inspiration based on flow and volume data """
    # The volume is maximum at the end of inspiration AND the flow = 0
    # - Determine where volume is maximum
    # - If the index of max volume is almost equal to the index where flow = 0 --> append value to array with end inspiration values
    end_insp = []
    i = 0
    while i < len(end_insp_flow):
        if end_insp_flow[i] - dist < 0:
            vol_max = max(volume_trim[0:(end_insp_flow[i] + dist)])
            vol_max_idx = volume_trim[0:(end_insp_flow[i] + dist)].index(vol_max)
        elif end_insp_flow[i] + dist > len(flow_trim):
            vol_max = max(volume_trim[(end_insp_flow[i] - dist):len(flow_trim)])
            vol_max_idx = volume_trim[(end_insp_flow[i] - dist):len(flow_trim)].index(vol_max) + (end_insp_flow[i] - dist)
        else:
            vol_max = max(volume_trim[(end_insp_flow[i] - dist):(end_insp_flow[i] + dist)])
            vol_max_idx = volume_trim[(end_insp_flow[i] - dist):(end_insp_flow[i] + dist)].index(vol_max) + (end_insp_flow[i] - dist)

        if vol_max_idx < (end_insp_flow[i] + close_dist) and vol_max_idx > (end_insp_flow[i] - close_dist):
            end_insp.append(vol_max_idx)
            i += 1
        else:
            end_insp.append(end_insp_flow[i])
            i += 1
        

    """ Calculate start inspiration based on flow and P_es data """
    # Calculate derivatives
    flow_diff = np.diff(flow_trim)                    # Derivative of the flow
    p_es_diff = np.diff(p_es_trim)                    # Derivative of the pressure

    # The derivative of the flow is maximum at start of inspiration AND the derivative of Pes is minimum
    # Search within an area of 40 samples before the estimated start of inspiration and 40 samples after, the smaller
    # area where the flow is between -100 mL/s and 100 mL/s. Here it is then checked which points meet the requirements:
    # - Determine where derivative of flow is maximum
    # - Determine where derivative Pes is minimum
    # - If these indices are really close --> start inspiration
    start_insp = []
    i = 0

    while i < len(start_insp_flow):
        if start_insp_flow[i] - dist < 0:
            arr = flow_trim[0:(start_insp_flow[i] + dist)]
            arr_search = np.where((np.asarray(arr) > (-1*amplitude)) & (np.asarray(arr) < amplitude))[0]

            diff_flow_max = max(flow_diff[arr_search])
            diff_flow_max_idx = np.where(flow_diff[0:(start_insp_flow[i] + dist)] == diff_flow_max)[0][0]
            diff_p_es_min = min(p_es_diff[arr_search])
            diff_p_es_min_idx = np.where(p_es_diff[0:(start_insp_flow[i] + dist)] == diff_p_es_min)[0][0]

        elif start_insp_flow[i] + dist > len(flow_diff):
            arr = flow_trim[(start_insp_flow[i] - dist):len(flow_diff)]
            arr_search = np.where((np.asarray(arr) > (-1 * amplitude)) & (np.asarray(arr) < amplitude))[0] + (
                        start_insp_flow[i] - dist)

            diff_flow_max = max(flow_diff[arr_search])
            diff_flow_max_idx = np.where(flow_diff[(start_insp_flow[i] - dist):len(flow_diff)] == diff_flow_max)[0][0] + (start_insp_flow[i] - dist)
            diff_p_es_min = min(p_es_diff[arr_search])
            diff_p_es_min_idx = np.where(p_es_diff[(start_insp_flow[i] - dist):len(p_es_diff)] == diff_p_es_min)[0][0] + (start_insp_flow[i] - dist)

        else:
            try:
                arr = flow_trim[(start_insp_flow[i] - dist):(start_insp_flow[i] + dist)]
                arr_search = np.where((np.asarray(arr) > -100) & (np.asarray(arr) < 100))[0] + (start_insp_flow[i] - dist)
                diff_flow_max = max(flow_diff[arr_search])
                diff_flow_max_idx = np.where(flow_diff[(start_insp_flow[i] - dist):(start_insp_flow[i] + dist)] == diff_flow_max)[0][0] + (start_insp_flow[i] - dist)
                diff_p_es_min = min(p_es_diff[arr_search])
                diff_p_es_min_idx = np.where(p_es_diff[(start_insp_flow[i] - dist):(start_insp_flow[i] + dist)] == diff_p_es_min)[0][0] + (start_insp_flow[i] - dist)
            except:
                inspirationerror += 1


        if diff_flow_max_idx < (diff_p_es_min_idx + close_dist) and diff_flow_max_idx > (diff_p_es_min_idx - close_dist):
            start_insp.append(diff_flow_max_idx)
            i += 1
        elif diff_flow_max_idx < (start_insp_flow[i] + close_dist) and diff_flow_max_idx > (start_insp_flow[i] - close_dist):
            start_insp.append(diff_flow_max_idx)
            i += 1
        elif diff_p_es_min_idx < (start_insp_flow[i] + close_dist) and diff_p_es_min_idx > (start_insp_flow[i] - close_dist):
            start_insp.append(diff_p_es_min_idx)
            i += 1
        else:
            start_insp.append(start_insp_flow[i])
            i += 1


    # Collect inspiration flow values
    start_insp_values = []
    end_insp_values = []

    for i in start_insp:
        try:
            start_flow_values = flow_trim[i]
            start_insp_values.append(start_flow_values)
        except:
            inspirationerror += 1
            
    
    for i in end_insp:
        try:
            end_flow_values = flow_trim[i]
            end_insp_values.append(end_flow_values)
        except:
            inspirationerror += 1
            
    print("number of errors in inspiration is {}". format(inspirationerror))
    return start_insp, start_insp_values, end_insp, end_insp_values


