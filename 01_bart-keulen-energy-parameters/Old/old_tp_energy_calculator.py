"""
Calculates the dynamic transpulmonary energy per breath and per minute
"""
import numpy as np
from numpy import mean

from constants import CONV_FACTOR


def tp_energy_calculator(start_insp, pv_ends, p_air_trim, p_es_trim, volume_trim, rr_, pressure_type):
    """
    Returns tp_e_breath, tp_e_per_minute, tp_mech_power
    """
    p_tp = []  # create empty list for transpulmonal pressure
    for elem_air, elem_es in zip(p_air_trim, p_es_trim):
        p_tp_elem = elem_air - elem_es
        p_tp.append(p_tp_elem)

    def poly_area(_x_, _y_):
        """
        function to calculate the area of a polygon
        """
        return 0.5*np.abs(np.dot(_x_, np.roll(_y_, 1))-np.dot(_y_, np.roll(_x_, 1)))

    for index, elem in enumerate(pv_ends):  # only use the ends that come after a start
        if pv_ends[index] <= start_insp[0]:
            pv_ends.remove(pv_ends[index])

    tp_e_breath = []  # create empty list for the transpulmonal energy per breath
    for index, elem in enumerate(start_insp[:-1]):  # create better code (make len matching)
        start = elem
        end = pv_ends[index]
        if end > start:
            p_tp_interval = p_tp[start:end]  # p_tp values of each breath 
            vol_interval = volume_trim[start:end]  # volume values of each breath
            poly = CONV_FACTOR * poly_area(p_tp_interval, vol_interval)
            # calculate polyarea to calculate energy
            # polyarea is the area enclosed by the PV-loop
            # convert from [ml * cmH2O] to [Joules]
            tp_e_breath.append(poly)

    tp_e_breath_minute = []  # create empty list for mean energy per breath per minute
    tp_per_minute = [tp_e_breath[i * int(rr_):(i + 1) * int(rr_)]
                        for i in range((len(tp_e_breath) + int(rr_) - 1) // int(rr_))]

    # Split list in one-minute segments
    for minute in tp_per_minute:
        mean_e_minute = mean(minute)
        tp_e_breath_minute.append(mean_e_minute)

    tp_e_per_minute = [i * rr_ for i in tp_e_breath_minute]  # mechanical power [J/min]
    tp_mech_power = round(mean(tp_e_per_minute), 2)  # calculate tranpulmonal mechanical power
    
    return p_tp, tp_e_breath, tp_e_per_minute, tp_mech_power
