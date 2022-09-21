"""
Calculates the hysteresis area [J/min]

Author: Anne Meester
Date: February 2022

"""
import numpy as np
from numpy import mean
import matplotlib.pyplot as plt
from constants import FS


def hysteresis_area(start, pv_e_breath):
    """
    Returns pv_p_breath, mean_pv_p_breath
    """
    print(f'length pv_p = {len(pv_e_breath)}')
    print(f'start = {len(start)}')
    # Calculate power per breath [J/min]]
    pv_p_breath = []
    hysteresis_error = 0
    for i in range(len(start)-1):
        try:
            dur_min = (start[i+1]-start[i])/FS/60         # Duration per breath
            power = pv_e_breath[i]/dur_min
            pv_p_breath.append(power)
     
        except:
            hysteresis_error += 1
    mean_pv_p_breath = round(mean(pv_p_breath), 2)
    print("number of errors in hysteresis is {}". format(hysteresis_error))
    return pv_p_breath, mean_pv_p_breath