"""
Inspiration detection

Author: Sanne van Deelen
Date: February 2021

Modified by Bart Keulen
Date: October 2021
"""
import pandas as pd
import numpy as np

from constants import FS, RR_SEP_FRAC

def inspiration_detection(volume_trim, p_air_trim, flow_trim, rr_):
    """
    Returns indices and corresponding pressure values of start and end of each inspiration
    """
    min_separation = 0.8 * (1/rr_) * 60 * FS  # No. of indices that must separate the peaks
    max_separation = 1.2 * (1/rr_) * 60 * FS  # No. of indices that must separate the peaks

    # Find starts as all derivatives higher than/equal to 0.5 (value chosen on data)
    p_air_trim_series = pd.Series(p_air_trim)
    p_air_diff = np.diff(p_air_trim_series)  # Derivative of airway pressure
    df_p_min = pd.DataFrame(data=p_air_diff, columns=['Pair-diff'])
    inspiration = df_p_min[df_p_min['Pair-diff'] >= 0.5].index.values
    start_insp = inspiration.tolist()

    # Find all start points with a minimal and maximal separation to exclude other fluctuations
    i = 1
    while i < len(start_insp):
        if min_separation < start_insp[i] - start_insp[i - 1]:
            i += 1           
        else:
            del start_insp[i]

    # Find ends of inspiration as peak volume between two starts or
    # Between the last start and end of signal.
    end_insp = []
    i = 0
    while i < len(start_insp)-1:
        vol_max = max(volume_trim[start_insp[i]:start_insp[i+1]])
        vol_max_idx = volume_trim[start_insp[i]:start_insp[i+1]].index(vol_max) + start_insp[i]

        if vol_max_idx - start_insp[i] < max_separation:
            end_insp.append(vol_max_idx)
            i += 1
        else:
            del start_insp[i]
 
    # Find end of last inspiration
    vol_max = max(volume_trim[start_insp[-1]:])
    vol_max_idx = volume_trim[start_insp[-1]:].index(vol_max) + start_insp[-1]
    end_insp.append(vol_max_idx)

    # Exclude starts or ends without corresponding starts or ends
    if start_insp[0] > end_insp[0]:
        del end_insp[0]
    if start_insp[-1] > end_insp[-1]:
        del start_insp[-1]

    # Exclude incomplete inspirations
    if end_insp[-1] == len(volume_trim)-1:
        del end_insp[-1], start_insp[-1]
    if end_insp[-1] - start_insp[-1] < min_separation:
        del end_insp[-1], start_insp[-1]
    
    # Exclude detected breaths when the indices of start and end are equal,
    # when the maximum flow is below 500 mL/s or the minimum volume is below -50mL.
    i = 0
    while i < len(start_insp):
        if start_insp[i] == end_insp[i]:
            del start_insp[i], end_insp[i]
        elif max(flow_trim[start_insp[i]:end_insp[i]]) <= 500:
            del start_insp[i], end_insp[i]
        elif min(volume_trim[start_insp[i]:end_insp[i]]) <= -50:
            del start_insp[i], end_insp[i]
        else:
            i += 1

    # Collect inspiration pressure values
    start_insp_values = []
    end_insp_values = []

    for i in start_insp:
        start_pressure_values = p_air_trim[i]
        start_insp_values.append(start_pressure_values)
    
    for i in end_insp:
        end_pressure_values = p_air_trim[i]
        end_insp_values.append(end_pressure_values)

    return start_insp, start_insp_values, end_insp, end_insp_values
