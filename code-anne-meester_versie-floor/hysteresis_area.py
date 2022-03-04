"""
Calculates the hysteresis area [J/min]

Author: Anne Meester
Date: February 2022

"""
import numpy as np
from numpy import mean
import matplotlib.pyplot as plt
from constants import CONV_FACTOR, FS
from intersect import intersection


def hysteresis_area(start, pv_e_breath):
    """
    Returns pv_e_breath, mean_pv_e_breath, pv_p_breath, mean_pv_p_breath
    """

    # Calculate power per breath [J/min]]
    pv_p_breath = []
    for i in range(len(start)-1):
        dur_min = (start[i+1]-start[i])/FS/60             # Duration per breath
        power = pv_e_breath[i]/dur_min
        pv_p_breath.append(power)

    mean_pv_p_breath = round(mean(pv_p_breath), 2)

    return pv_p_breath, mean_pv_p_breath
