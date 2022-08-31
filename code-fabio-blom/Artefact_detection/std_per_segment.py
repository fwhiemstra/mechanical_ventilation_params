import numpy as np
import matplotlib.pyplot as plt


def std_per_segment(time_data, signal_data):
    """Calculates the std per segment."""
    time_vector = np.median(time_data, axis=1)
    signal_var = np.std(signal_data, axis=1)

    return time_vector, signal_var
