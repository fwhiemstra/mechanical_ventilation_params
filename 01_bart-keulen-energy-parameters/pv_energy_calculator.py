"""
Calculates the dynamic transpulmonary energy per breath and per minute

Author: Sanne van Deelen
Date: February 2021

Modified by Bart Keulen
Date: October 2021
"""
import numpy as np
from numpy import mean

from constants import CONV_FACTOR, FS


def pv_energy_calculator(pv_starts, pv_ends, pressure, volume_trim):
    """
    Returns pv_e_breath, mean_pv_e_breath, pv_p_breath, mean_pv_p_breath
    """

    def poly_area(_x_, _y_):
        """
        Function to calculate the area of a polygon
        """
        return 0.5*np.abs(np.dot(_x_, np.roll(_y_, 1))-np.dot(_y_, np.roll(_x_, 1)))

    # Only use the ends that come after a start
    for index, elem in enumerate(pv_ends):
        if pv_ends[index] <= pv_starts[0]:
            del pv_ends[index]

    pv_e_breath = []
    for index, start in enumerate(pv_starts[:-1]):  # Last breath is excluded
        end = pv_ends[index]
        if end > start:
            pressure_interval_raw = pressure[start:end]  # Pressure values of each breath
            pressure_interval = [i - pressure_interval_raw[0] for i in pressure_interval_raw]   # First value is subtracted in order to begin loop at 0 cmH2O
            vol_interval = volume_trim[start:end]  # Volume values of each breath

            # Calculate energy by calculating the area enclosed by the PV-loop (hysteresis area)
            # and convert from [mL*cmH2O] to [J]
            poly = CONV_FACTOR * poly_area(pressure_interval, vol_interval)
            pv_e_breath.append(poly)
            
    # Calculate power per breath [J/min]
    pv_p_breath = []
    for i in range(len(pv_starts)-1):
        dur_min = (pv_starts[i+1]-pv_starts[i])/FS/60   # Duration of breath
        power = pv_e_breath[i] / dur_min                # Power of breath
        pv_p_breath.append(power)

    # Calculate mean energy and power
    mean_pv_e_breath = round(mean(pv_e_breath),2)
    mean_pv_p_breath = round(mean(pv_p_breath),2)
    
    return pv_e_breath, mean_pv_e_breath, pv_p_breath, mean_pv_p_breath
