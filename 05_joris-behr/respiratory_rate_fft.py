"""
Respiratory Rate
- Power spectral density of the volume data is used to estimate the respiratory rate
  (rr) of the patient
- Most dominant frequency is the breathing frequency
- To prevent false determination, a minimal and maximal rr are determined

Author: Sanne van Deelen
Date: February 2021

Modified by Bart Keulen
Date: October 2021
"""
import numpy as np
import pandas as pd

from constants import FS


def respiratory_rate_fft(volume_trim):
    """"
    Returns the respiratory rate (RR)
    """
    fft = np.fft.fft(volume_trim)               # Fast fourier transform (FFT) of volume-data
    fft_array = np.array(np.abs(fft))           # Take absolute value (magnitude) of FFT
    fft_array_t = fft_array.T                   # Transpose array

    freqs = np.fft.fftfreq(fft.size, d=1/FS)    # Get frequencies of FFT
    freq_array = np.array(freqs)                # Make array of frequencies
    freq_array_t = freq_array.T                 # Transpose array
    
    # Create dataframe with FFT values of frequencies between 5 and 50/min
    freq_fft_df_all = pd.DataFrame(list(zip(freq_array_t, fft_array_t)),
                               columns=['Frequencies', 'FFT'])
    freq_fft_df = freq_fft_df_all.query('5/60 <= Frequencies <= 50/60')

    # Select most dominant frequency and convert to respiratory rate
    dominant_freq = freq_fft_df.loc[freq_fft_df.FFT.idxmax(), 'Frequencies']
    rr_ = round(dominant_freq * 60)  # Respiratory rate

    return rr_
