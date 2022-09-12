import scipy
import scipy.signal as signal
import numpy as np
import matplotlib.pyplot as plt


def bandpower_per_segment(time_data, p_es_data, fs, fmin, fmax):
    """ Function that calculates the power/AUC in a periodogram over a certain frequency range."""
    f, Pxx = scipy.signal.periodogram(p_es_data, fs)
    ind_min = scipy.argmax(f > fmin) - 1
    ind_max = scipy.argmax(f > fmax) - 1
    p_es_bandpower = scipy.trapz(Pxx[:, ind_min: ind_max], f[ind_min: ind_max])

    time_vector = np.median(time_data, axis=1)

    return time_vector, p_es_bandpower
