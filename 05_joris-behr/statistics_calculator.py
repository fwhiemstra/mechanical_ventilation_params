"""
Statistics
- standard deviations
- standard errors

Author: Sanne van Deelen
Date: February 2021

Modified by Bart Keulen
Date: October 2021

Modified by Anne Meester
Date: February 2022
"""
import math
from turtle import shape
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from constants import PRESSURE_TYPE

def sd_se_statistics(p_breath, aw_p_breath, es_p_breath, tp_p_breath,
               wob_es_breath, wob_tp_breath, ptp_es, ptp_tp,
               tp_peak, tp_swing, pressure_type):
    """
    Returns
    """
    # Power per breath
    sd_p_breath = round(np.std(p_breath), 2)
    se_p_breath = round(sd_p_breath / math.sqrt(len(p_breath)), 2)

    # Esophageal loop power per breath
    sd_es_p_breath = round(np.std(es_p_breath), 2)
    se_es_p_breath = round(sd_es_p_breath / math.sqrt(len(es_p_breath)), 2)

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

        # Transpulmonary work per breath
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
    standard_deviations = [sd_p_breath, sd_es_p_breath, sd_aw_p_breath, sd_tp_p_breath,
                           sd_wob_tp_breath, sd_wob_es_breath, sd_ptp_es, sd_ptp_tp, sd_tp_peak, sd_tp_swing]
    standard_errors = [se_p_breath, se_es_p_breath, se_aw_p_breath, se_tp_p_breath,
                       se_wob_tp_breath, se_wob_es_breath, se_ptp_es, se_ptp_tp, se_tp_peak, se_tp_swing]

    return standard_deviations, standard_errors

def correlations(p_breath, aw_p_breath, es_p_breath, tp_p_breath,
               wob_es_breath, wob_tp_breath, ptp_es, ptp_tp,
               tp_peak, tp_swing):
    #creating dataframe from data.
    # Last values of TP peak and swing are not taken into account to ensure same length of data.
    data_dict = {'Power breath': p_breath, 'Hys aw': aw_p_breath, 'Hys aw':es_p_breath, 'Hys tp':tp_p_breath,
               'Power es':wob_es_breath, 'Power tp': wob_tp_breath, 'PTP es': ptp_es, 'PTP tp':ptp_tp,
               'tp peak':tp_peak[0:-1], 'tp swing': tp_swing[0:-1]}
    
    data = pd.DataFrame(data_dict)
    data = data.dropna()
    matrix = data.corr(method = 'pearson').round(2)
    mask = np.triu(np.ones_like(matrix, dtype=bool))

    plt.figure()
    sns.heatmap(matrix,annot = True, vmax = 1, vmin = 0, center = 0.5, cmap = 'vlag', mask=mask)
    plt.title("Heat map of correlations")
    #Saving the heatmap
    # plt.savefig('heatmap001.jpg')
    plt.tight_layout()
    plt.show()

    matrix = matrix.unstack()
    matrix = matrix[abs(matrix) >= 0.7]
    print(matrix)

  
    return matrix