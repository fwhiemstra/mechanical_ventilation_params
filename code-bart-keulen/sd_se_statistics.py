"""
Statistics
- standard deviations
- standard errors

Author: Sanne van Deelen
Date: February 2021

Modified by Bart Keulen
Date: October 2021
"""
import math
import numpy as np

from constants import PRESSURE_TYPE


def sd_se_statistics(p_breath, dyn_p_breath, aw_p_breath, tp_p_breath,
               wob_es_breath, wob_tp_breath, ptp_es, ptp_tp,
               tp_peak, tp_swing, pressure_type):
    """
    Returns
    """
    # Power per breath
    sd_p_breath = round(np.std(p_breath), 2)
    se_p_breath = round(sd_p_breath / math.sqrt(len(p_breath)), 2)

    # Dynamic power per breath
    sd_dyn_p_breath = round(np.std(dyn_p_breath), 2)
    se_dyn_p_breath = round(sd_dyn_p_breath/ math.sqrt(len(dyn_p_breath)), 2)

    # Airway loop power per breath
    sd_aw_p_breath = round(np.std(aw_p_breath), 2)
    se_aw_p_breath = round(sd_aw_p_breath / math.sqrt(len(aw_p_breath)), 2)

    if pressure_type == PRESSURE_TYPE.TRANSPULMONARY:
        # Transpulmonary loop power per breath
        sd_tp_p_breath = round(np.std(tp_p_breath), 2)
        se_tp_p_breath = round(sd_tp_p_breath / math.sqrt(len(tp_p_breath)), 2)

        # Esophageal work of breathing per breath
        sd_wob_es_breath = round(np.std(wob_es_breath), 2)
        se_wob_es_breath = round(sd_wob_es_breath / math.sqrt(len(wob_es_breath)), 2)

        # Transpulmonary work of breathing per breath
        sd_wob_tp_breath = round(np.std(wob_tp_breath), 2)
        se_wob_tp_breath = round(sd_wob_tp_breath / math.sqrt(len(wob_tp_breath)), 2)

        # Esophageal PTP per breath
        sd_ptp_es = round(np.std(ptp_es), 2)
        se_ptp_es = round(sd_ptp_es / math.sqrt(len(ptp_es)), 2)

        # Transpulmonary PTP per breath
        sd_ptp_tp = round(np.std(ptp_tp), 2)
        se_ptp_tp = round(sd_ptp_tp / math.sqrt(len(ptp_tp)), 2)

        # Transpulmonary peak
        sd_tp_peak = round(np.std(tp_peak), 2)
        se_tp_peak = round(sd_tp_peak / math.sqrt(len(tp_peak)), 2)

        # Transpulmonary swing
        sd_tp_swing = round(np.std(tp_swing), 2)
        se_tp_swing = round(sd_tp_swing / math.sqrt(len(tp_swing)), 2)

    elif pressure_type == PRESSURE_TYPE.AIRWAY:
        # Transpulmonary loop power per breath
        sd_tp_p_breath = '-'
        se_tp_p_breath = '-'

        # Transpulmonary work of breathing per breath
        sd_wob_tp_breath = '-'
        se_wob_tp_breath = '-'

        # Esophageal work of breathing per breath
        sd_wob_es_breath = '-'
        se_wob_es_breath = '-'

        # Esophageal PTP per breath
        sd_ptp_es ='-'
        se_ptp_es = '-'

        # Transpulmonary PTP per breath
        sd_ptp_tp = '-'
        se_ptp_tp = '-'

        # Transpulmonary peak
        sd_tp_peak = '-'
        se_tp_peak = '-'

        # Transpulmonary swing
        sd_tp_swing = '-'
        se_tp_swing = '-'

    # Combine standard deviations and errors in lists
    standard_deviations = [sd_p_breath, sd_dyn_p_breath, sd_aw_p_breath, sd_tp_p_breath,
                           sd_wob_tp_breath, sd_wob_es_breath, sd_ptp_es, sd_ptp_tp, sd_tp_peak, sd_tp_swing]
    standard_errors = [se_p_breath, se_dyn_p_breath, se_aw_p_breath, se_tp_p_breath,
                       se_wob_tp_breath, se_wob_es_breath, se_ptp_es, se_ptp_tp, se_tp_peak, se_tp_swing]

    return standard_deviations, standard_errors
