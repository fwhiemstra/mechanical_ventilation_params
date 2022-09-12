"""
Inspiration start detection
- Determines the starting points of inspiration by using the acceleration of
  airway pressure (derivative of p_air)
- Defines the starting points as the first point above a specified threshold,
  after which a local maximum will follow
"""
import numpy as np
import pandas as pd

from constants import FS, RR_SEP_FRAC


def inspiration_start_detection(p_air_trim, rr_):
    """"
    Returns indices and corresponding pressure values of starts of inspiration
    """
    min_separation = RR_SEP_FRAC * (1/rr_) * 60 * FS  # no. of indices that must separate the peaks

    p_air_trim_series = pd.Series(p_air_trim)
    p_air_diff = np.diff(p_air_trim_series)  # derivative of airway pressure
    df_p_min = pd.DataFrame(data=p_air_diff, columns=['Pair-diff'])  # convert to dataframe
    inspiration = df_p_min[df_p_min['Pair-diff'] >= 0.5].index.values
    # find all derivatives higher than/equal to 0.5 (value chosen on data)
    start_insp = inspiration.tolist()  # convert to list
    
    index = 1
    while index < len(start_insp):
        if start_insp[index] - start_insp[index - 1] < min_separation:
            # find all start points with a minimal separation to exclude other fluctuations
            del start_insp[index]
        else:
            index += 1

    start_insp_values = []  # create empty list to collect start inspiration pressure values
    for i in start_insp:  # collect start inspiration pressure values
        pressure_values = p_air_trim[i]
        start_insp_values.append(pressure_values)

    return start_insp, start_insp_values
