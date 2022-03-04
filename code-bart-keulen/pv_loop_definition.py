"""
Defines the start and end points of the transpulmonary PV-loop

Author: Sanne van Deelen
Date: February 2021

Modified by Bart Keulen
Date: October 2021
"""
import pandas as pd
from math import floor
from constants import RR_SEP_FRAC, FS


def pv_loop_definition(rr_, start_insp, volume_trim):
    """
    Defines the start and end points of the transpulmonary PV-loop
    """

    min_separation = 0.8 * (1/rr_) * 60 * FS  # No. of indices that must separate the PV-ends
    max_separation = 1.2 * (1/rr_) * 60 * FS  # No. of indices that can maximally separate the PV-ends

    pv_starts = start_insp[:-1].copy()
    volume_df = pd.DataFrame(volume_trim, columns=['volume'])

    # Find minimum volume during a breathing cycle
    pv_ends = []
    for start, end in zip(pv_starts[:-1],pv_starts[1:]):
        half_duration = floor((end-start)/2)
        vol_breath = volume_df[start+half_duration:end]
        loop_end = vol_breath.idxmin()
        pv_ends.append(loop_end[0])

    # Only use the ends that come after a start
    for idx, elem in enumerate(pv_ends):
        if pv_ends[idx] <= pv_starts[0]:
            del pv_ends[idx]
    
    # Only use the starts that come before an end
    for idx, elem in enumerate(pv_starts):
        if pv_ends[-1] <= pv_starts[idx]:
            del pv_starts[idx]

    # Remove loops which are separated more than the set limits
    i = 1
    while i < len(pv_ends):
        if pv_ends[i] - pv_starts[i] < min_separation:
            del pv_ends[i], pv_starts[i]
        elif pv_ends[i] - pv_starts[i] > max_separation:
            del pv_ends[i], pv_starts[i]
        else:
            i += 1

    # Collect start of PV-loop volume values
    pv_starts_values = []
    for i in pv_starts:
        volume_values = volume_trim[i]
        pv_starts_values.append(volume_values)

    # Collect end of PV-loop volume values
    pv_ends_values = []
    for i in pv_ends:
        volume_values = volume_trim[i]
        pv_ends_values.append(volume_values)

    return pv_ends, pv_ends_values, pv_starts, pv_starts_values
