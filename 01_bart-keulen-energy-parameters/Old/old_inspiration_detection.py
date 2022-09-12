"""
Inspiration detection
"""
import pandas as pd
import numpy as np
from scipy.signal import find_peaks

from constants import FS, RR_SEP_FRAC


def inspiration_detection(volume_trim, p_air_trim, flow_trim, rr_):
    """
    Returns indices and corresponding pressure values of start and end of each inspiration
    """
    min_separation = RR_SEP_FRAC * (1/rr_) * 60 * FS  # No. of indices that must separate the peaks

    # Find starts as all derivatives higher than/equal to 0.5 (value chosen on data)
    p_air_trim_series = pd.Series(p_air_trim)
    p_air_diff = np.diff(p_air_trim_series)  # Derivative of airway pressure
    df_p_min = pd.DataFrame(data=p_air_diff, columns=['Pair-diff'])
    inspiration = df_p_min[df_p_min['Pair-diff'] >= 0.5].index.values
    start_insp = inspiration.tolist()

    # Find ends as peaks of volume with a minimal separation distance
    volume_trim_series = pd.Series(volume_trim)
    vol_max = find_peaks(volume_trim_series, distance=min_separation)
    end_insp = (vol_max[0]).tolist()

    # Find all start points with a minimal separation to exclude other fluctuations
    i = 1
    while i < len(start_insp):
        if start_insp[i] - start_insp[i - 1] > min_separation:
            i += 1           
        else:
            del start_insp[i]

    # Exclude starts or ends without corresponding starts or ends
    if start_insp[0] > end_insp[0]:
        del end_insp[0]
    if start_insp[-1] > end_insp[-1]:
        del start_insp[-1]
    
    # Exclude detected breaths with a maximum flow below 500 mL/s
    i = 0
    while i < len(start_insp):
        if max(flow_trim[start_insp[i]:end_insp[i]]) >= 500:
            i += 1
        else:
            del start_insp[i], end_insp[i]

    # Create empty list to collect inspiration pressure values
    start_insp_values = []
    end_insp_values = []

    # Collect inspiration pressure values
    for i in start_insp:
        start_pressure_values = p_air_trim[i]
        start_insp_values.append(start_pressure_values)
    
    for i in end_insp:
        end_pressure_values = p_air_trim[i]
        end_insp_values.append(end_pressure_values)

    return start_insp, start_insp_values, end_insp, end_insp_values
