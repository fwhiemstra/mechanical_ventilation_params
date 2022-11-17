"""
Function for calculating the pressure-time product (PTP)

Author: Bart Keulen
Date: October 2021

Modified by Anne Meester
Date: February 2022
"""

import numpy as np
from numpy import NaN
from constants import FS


def ptp_calculator(name, pressure, start_insp, end_insp):
    '''
    Calculating the pressure-time product (PTP).

    INPUT: pressure, start_insp, end_insp
    OUTPUT: ptp_minute, ptp_mean
    '''
    ptp = []        # Empty list for PTP values
    dt = 1/FS       # Time step
    ptperror = 0

    for start, end in zip(start_insp, end_insp):
        try:
            p_single_breath = pressure[start:end]  # Take pressure values per inspiration
            # Translate the curve such that the maximum pressure of P_es equals zero and the minimum pressure of P_aw and P_tp equals zero
            if name == 'p_es':
                max_p_single_breath = max(p_single_breath)
                p_single_breath = [i - abs(max_p_single_breath) for i in p_single_breath]

                ptp_single_breath = np.trapz(p_single_breath, dx=dt)  # Numerical integration of pressure over time
                ptp.append(abs(ptp_single_breath))

            else:
                if min(p_single_breath) < 0:
                    min_p_single_breath = min(p_single_breath)
                    p_single_breath = [i + abs(min_p_single_breath) for i in p_single_breath]

                ptp_single_breath = np.trapz(p_single_breath, dx=dt)  # Numerical integration of pressure over time
                ptp.append(ptp_single_breath)
        except:
            ptperror += 1

    # Calculate PTP/min per breath [cmH20.s/min]
    ptp_minute = []
    for i in range(len(start_insp)-1):
        try:
            dur_min = (start_insp[i+1]-start_insp[i])/FS/60   # Duration of breath
            ptp_breath_minute = ptp[i] / dur_min              # PTP/min
            ptp_minute.append(ptp_breath_minute)
        except:
            ptperror += 1
            ptp_minute.append(NaN)

    print( "number of errors in ptp calculation is {}". format(ptperror))
    ptp_mean = round(np.mean(ptp_minute),2)  # Mean value of PTP over chosen segment

    return ptp_minute, ptp_mean
