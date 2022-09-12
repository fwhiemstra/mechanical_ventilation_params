"""
Function for calculating the peak and swing
of the transpulmonary pressure

Author: Bart Keulen
Date: October 2021
"""

import numpy as np


def tp_parameter_calculator(p_tp, start_insp, end_insp):
    '''
    Calculating the peak and swing of the transpulmonary pressure.
    
    INPUT: p_tp, start_insp, end_insp
    OUTPUT: tp_peak, tp_peak_mean, tp_swing, tp_swing_mean
    '''
    tp_peak = []    # Empty list for peak values
    tp_swing = []   # Empty list for swing values

    # Check if lengths are the same, otherwise delete last start_insp value
    if len(start_insp) > len(end_insp):
        start_insp.remove(start_insp[-1])

    for start, end in zip(start_insp, end_insp):
        # Take pressure values per inspiration
        p_single_breath = p_tp[start:end]

        # Calculate peak pressure of one breath
        peak = max(p_single_breath)
        tp_peak.append(peak)

        # Calculate swing as peak - minimum pressure
        swing = peak - min(p_single_breath)
        tp_swing.append(swing)

    # Calculate mean of peak and swing values
    tp_peak_mean = round(np.mean(tp_peak),2)
    tp_swing_mean = round(np.mean(tp_swing),2)
           
    return tp_peak, tp_peak_mean, tp_swing, tp_swing_mean