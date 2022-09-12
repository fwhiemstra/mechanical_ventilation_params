"""
Calculates the mean PEEP, the energy per minute, the mechanical power,
the energy per breath and the mean energy per breath.

Author: Sanne van Deelen
Date: February 2021

Modified by Bart Keulen
Date: October 2021
"""
import numpy as np
from numpy import mean

from constants import CONV_FACTOR, FS

def energy_calculator(start_insp, end_insp, pressure, volume_trim, rr_, peep, dynamic=0):
    """
    Returns e_breath, mean_e_breath, p_breath, mean_p_breath

    Can be calculated as static energy (dynamic=0) or dynamic energy (dynamic=1).
    The dynamic energy is calculated using the pressure minus the peep.
    """

    # Only use the ends that come after a start
    for index, elem in enumerate(end_insp):
        if end_insp[index] <= start_insp[0]:
            end_insp.remove(end_insp[index])

    # Check if lengths are the same
    if len(start_insp) > len(end_insp):
        start_insp.remove(start_insp[-1])

    e_breath = []
    for start, end, peep_ in zip(start_insp, end_insp, peep):
        if end > start:
            vol_interval = volume_trim[start:end]  # Volume values of each breath
            pres_interval = pressure[start:end]  # Pressure values of each breath

            # Subtract PEEP values per breath of the pressure values
            # in case of dynamic energy calculation
            if dynamic == 1:
                pres_interval = [i-peep_ for i in pres_interval]
            else:
                pass

            # Integrate to calculate energy per breath and convert from [mL*cmH2O] to [J]
            integration = CONV_FACTOR * np.trapz(pres_interval, vol_interval)
            e_breath.append(integration)

    # Calculate power per breath [J/min]
    p_breath = []
    for i in range(len(start_insp)-1):
        dur_min = (start_insp[i+1]-start_insp[i])/FS/60   # Duration of breath
        power = e_breath[i] / dur_min        # Power of breath
        p_breath.append(power)

    # Calculate mean energy and power
    mean_e_breath = round(mean(e_breath),2)
    mean_p_breath = round(mean(p_breath),2)

    return e_breath, mean_e_breath, p_breath, mean_p_breath
