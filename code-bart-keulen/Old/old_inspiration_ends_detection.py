"""
Inspiration end detection
"""
from scipy.signal import find_peaks
import pandas as pd

from constants import FS, RR_SEP_FRAC


def inspiration_end_detection(p_air_trim, rr_):
    """
    Returns indices and corresponding pressure values of ends of inspiration
    """
    min_separation = RR_SEP_FRAC * (1/rr_) * 60 * FS  # no. of indices that must separate the peaks
    p_air_trim_series = pd.Series(p_air_trim)
    p_max = find_peaks(p_air_trim_series, distance=min_separation)
    # find peaks of airway pressure with a minimal separation distance
    end_insp = (p_max[0]).tolist()  # convert to list

    end_insp_values = []  # create empty list to collect end inspiration pressure values
    for i in end_insp:  # collect end inspiration pressure values
        pressure_values = p_air_trim[i]
        end_insp_values.append(pressure_values)

    return end_insp, end_insp_values
