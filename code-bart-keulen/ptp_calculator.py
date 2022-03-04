"""
Function for calculating the pressure-time product (PTP)

Author: Bart Keulen
Date: October 2021
"""

import numpy as np
from constants import FS


def ptp_calculator(pressure, start_insp, end_insp):
    '''
    Calculating the pressure-time product (PTP).

    INPUT: pressure, start_insp, end_insp
    OUTPUT: ptp_minute, ptp_mean
    '''
    ptp = []        # Empty list for PTP values
    dt = 1/FS       # Time step
    
    for start, end in zip(start_insp, end_insp):
            p_single_breath = pressure[start:end]  # Take pressure values per inspiration
            ptp_single_breath = np.trapz(p_single_breath, dx=dt)  # Numerical integration of pressure over time
            ptp.append(ptp_single_breath)

    # Calculate PTP/min per breath [cmH20.s/min]
    ptp_minute = []
    for i in range(len(start_insp)-1):
        dur_min = (start_insp[i+1]-start_insp[i])/FS/60   # Duration of breath
        ptp_breath_minute = ptp[i] / dur_min              # PTP/min
        ptp_minute.append(ptp_breath_minute)

    ptp_mean = round(np.mean(ptp_minute),2)  # Mean value of PTP over chosen segment

    return ptp_minute, ptp_mean
