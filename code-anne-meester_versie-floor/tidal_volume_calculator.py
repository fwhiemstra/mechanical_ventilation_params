"""
Tidal volume calculation

Author: Sanne van Deelen
Date: February 2021

Modified by Bart Keulen
Date: October 2021

Modified by Anne Meester
Date: February 2022

"""
from numpy import mean


def tidal_volume_calculator(start_insp, end_insp, volume_trim):
    """
    Returns the mean tidal volume of the segment
    """

    # Calculate tidal volume as volume difference between start and end inspiration
    tidal_volume = []
    for start, end in zip(start_insp, end_insp):
        volume_values = volume_trim[end] - 0
        tidal_volume.append(volume_values)

    # Calculate mean tidal volume
    mean_tidal_volume = round(mean(tidal_volume), 2)

    return tidal_volume, mean_tidal_volume
