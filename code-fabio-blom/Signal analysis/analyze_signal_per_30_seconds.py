import numpy as np
import scipy.stats as stats
import pandas as pd


def analyze_signal_per_30_seconds(time_vector_segment, p_es_segment, p_air_segment, volume_segment, flow_segment):

    """ Calculate mov mean and mov var and entropy"""
    segment_len = len(p_air_segment)

    p_es_mean = np.mean(p_es_segment)
    p_es_var = np.var(p_es_segment)

    p_air_mean = np.mean(p_air_segment)
    p_air_var = np.var(p_air_segment)

    volume_mean = np.mean(volume_segment)
    volume_var = np.var(volume_segment)

    flow_mean = np.mean(flow_segment)
    flow_var = np.var(flow_segment)

    p_es_pd_series = pd.Series(p_es_segment)
    counts = p_es_pd_series.value_counts()
    entropy = stats.entropy(counts)

    corr_coeff_p_es_p_air = np.corrcoef(p_es_segment, p_air_segment)[0, 1]
    corr_coeff_p_es_volume = np.corrcoef(p_es_segment, volume_segment)[0, 1]
    corr_t = np.mean(time_vector_segment)

    return corr_coeff_p_es_p_air, corr_coeff_p_es_volume, corr_t
