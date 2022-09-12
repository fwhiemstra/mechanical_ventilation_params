"""
Dynamic mechanical power
- mechanical power - PEEP
- PEEP = positive end-expiratory pressure
"""
import numpy as np
from numpy import mean

from constants import CONV_FACTOR


def dynamic_mech_power(start_insp, end_insp, p_air_trim, volume_trim, rr_):
    """
    Returns mean PEEP and dynamic mechanical power
    """

    for index, elem in enumerate(end_insp):  # only use the ends that come after a start
        if end_insp[index] <= start_insp[0]:
            end_insp.remove(end_insp[index])

    if len(start_insp) > len(end_insp):  # check if lengths are the same
        start_insp.remove(start_insp[-1])

    # Calculate mean PEEP per breath as the mean pressure 50 ms before the
    # start of inspiration. The PEEP is the mean of the mean PEEP per breath.
    peep = []
    for elem in start_insp:
        if elem >= 5:
            exp_pres = mean(p_air_trim[elem-5:elem-1])
            peep.append(exp_pres)
        else:
            exp_pres = p_air_trim[elem]
            peep.append(exp_pres)
    mean_peep = round(mean(peep), 2)

    dyn_e_breath = []  # create empty list for the dynamic energy per breath
    for start, end, peep_ in zip(start_insp, end_insp, peep):
        if end > start:
            vol_interval = volume_trim[start:end]  # volume values of each breath
            pres_interval = p_air_trim[start:end]  # p_air values of each breath
            pres_minuspeep = [i-peep_ for i in pres_interval]
            integration = CONV_FACTOR * np.trapz(pres_minuspeep, vol_interval)
            # integrate to calculate energy
            # convert from [ml * cmH2O] to [Joules]
            dyn_e_breath.append(integration)

    dyn_e_breath_minute = []  # create empty list for energy per breath per minute
    dyn_per_minute = [dyn_e_breath[i * int(rr_):(i + 1) * int(rr_)]
                      for i in range((len(dyn_e_breath) + int(rr_) - 1) // int(rr_))]

    # Splits list is one-minute segments
    for minute in dyn_per_minute:
        dyn_mean_e_minute = mean(minute)  # calculates mean energy per minute
        dyn_e_breath_minute.append(dyn_mean_e_minute)

    dyn_e_per_minute = [i * rr_ for i in dyn_e_breath_minute]  # convert to mechanical power [J/min]
    dyn_mech_power = round(mean(dyn_e_per_minute), 2)  # calculate mechanical power and round off

    return mean_peep, dyn_mech_power
