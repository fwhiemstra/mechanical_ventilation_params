"""
Calculates the energy per breath and the mean energy per breath.

Author: Sanne van Deelen
Date: February 2021

Modified by Bart Keulen
Date: October 2021

Modified by Anne Meester
Date: February 2022
"""
import numpy as np
from numpy import mean
import matplotlib.pyplot as plt

from constants import CONV_FACTOR, FS


def energy_calculator(name, start_insp, end_insp, pressure, volume_trim):
    """
    Returns e_breath, mean_e_breath, p_breath, mean_p_breath

    """

    e_breath = []
    for start, end in zip(start_insp, end_insp):
        if end > start:
            vol_interval = volume_trim[start:end]   # Volume values of each breath
            pres_interval = pressure[start:end]     # Pressure values of each breath

            # Compensate for the calibration in volume --> define start inspiration where volume = 0
            if min(vol_interval) < 0:
                ind = next(x[0] for x in enumerate(vol_interval) if x[1] >= 0)
                vol_interval = vol_interval[ind:len(vol_interval)]
                pres_interval = pres_interval[ind:len(pres_interval)]
            else:
                ind_insp = np.argmin(vol_interval)
                vol_interval = vol_interval[ind_insp:len(vol_interval)]
                pres_interval = pres_interval[ind_insp:len(pres_interval)]

            # Translate the curve such that the maximum pressure of P_es equals zero and the minimum pressure of P_aw and P_tp equals zero
            if name == 'p_es':
                if max(pres_interval) > 0:
                    max_pres = max(pres_interval)
                    pres_interval = [i - abs(max_pres) for i in pres_interval]
                elif max(pres_interval) < 0:
                    max_pres = max(pres_interval)
                    pres_interval = [i + abs(max_pres) for i in pres_interval]
            else:
                if min(pres_interval) < 0:
                    min_pres = min(pres_interval)
                    pres_interval = [i + abs(min_pres) for i in pres_interval]
                elif min(pres_interval) > 0:
                    min_pres = min(pres_interval)
                    pres_interval = [i - abs(min_pres) for i in pres_interval]

            # Integrate to calculate energy per breath and convert from [mL*cmH2O] to [J]
            integration = CONV_FACTOR * np.trapz(pres_interval, vol_interval)
            e_breath.append(abs(integration))
    
    # Calculate power per breath [J/min]
    p_breath = []
    energyerror = 0
    for i in range(len(start_insp)-1):
        dur_min = (start_insp[i+1]-start_insp[i])/FS/60   # Duration of breath
        try:
            power = e_breath[i] / dur_min        # Power of breath
        except: 
            energyerror += 1
            
        p_breath.append(power)
    print("number of errors in energy calculation is {}". format(energyerror))
    # Calculate mean energy and power
    mean_e_breath = round(mean(e_breath),2)
    mean_p_breath = round(mean(p_breath),2)

    return e_breath, mean_e_breath, p_breath, mean_p_breath
