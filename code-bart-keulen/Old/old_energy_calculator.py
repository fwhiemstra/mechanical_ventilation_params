"""
Calculates the mechanical power
"""
import numpy as np
from numpy import mean

from constants import CONV_FACTOR


def energy_calculator(start_insp, end_insp, p_air_trim, volume_trim, rr_):
    """
    Returns the average energy per breath and the mechanical power
    """

    for index, elem in enumerate(end_insp):  # only use the ends that come after a start
        if end_insp[index] <= start_insp[0]:
            end_insp.remove(end_insp[index])

    if len(start_insp) > len(end_insp):  # check if lengths are the same
        start_insp.remove(start_insp[-1])

    e_breath = []  # create empty list for the energy per breath
    for start, end in zip(start_insp, end_insp):
        if end > start:
            vol_interval = volume_trim[start:end]  # volume values of each breath
            pres_interval = p_air_trim[start:end]  # p_air values of each breath
            integration = CONV_FACTOR * np.trapz(pres_interval, vol_interval)
            # integrate to calculate energy
            # convert from [ml * cmH2O] to [Joules]
            e_breath.append(integration)

    e_breath_minute = []  # create empty list for mean energy per breath per minute
    per_minute = [e_breath[i * int(rr_):(i + 1) * int(rr_)]
                  for i in range((len(e_breath) + int(rr_) - 1) // int(rr_))]

    # splits list in one-minute segments
    for minute in per_minute:
        mean_e_minute = mean(minute)  # calculates mean energy per minute
        e_breath_minute.append(mean_e_minute)

    e_per_minute = [i * rr_ for i in e_breath_minute]  # convert to mechanical power [J/min]
    mech_power = round(mean(e_per_minute), 2)  # calculate mechanical power, round off 2 decimals

    return mech_power, e_per_minute, e_breath
