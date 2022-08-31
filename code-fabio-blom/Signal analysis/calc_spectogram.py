import matplotlib.pyplot as plt
import scipy.signal as signal
import scipy
import numpy as np

#%%
def bandpower(pxx, f, fmin, fmax):
    """ Function that calculates the power/AUC in a periodogram over a certain frequency range."""
    ind_min = scipy.argmax(f > fmin) - 1
    ind_max = scipy.argmax(f > fmax) - 1
    p_es_bandpower = scipy.trapz(pxx[ind_min: ind_max], f[ind_min: ind_max])
    return p_es_bandpower


def calc_spectrogram(p_es_data, p_air_data, volume_data, flow_data, FSAMP):
    """ Function plots the spectrogram of the signal and calculates the periodic bandpower over time."""

    fig, axs = plt.subplots(1, sharex=True, sharey=True)

    pxx_p_es,  freq_p_es, t_p_es, cax_p_es = axs.specgram(p_es_data, noverlap=512, NFFT=2048, Fs=FSAMP)
    fig.colorbar(cax_p_es, ax=axs).set_label('Intensity [dB]')
    axs.set_ylim([0, 20])
    axs.set_ylabel('Frequency [Hz]')
    axs.set_title('P_es signal')

    pxx_p_es,  freq_p_es, t_p_es, cax_p_es = axs[0, 0].specgram(p_es_data, noverlap=512, NFFT=2048, Fs=FSAMP)
    fig.colorbar(cax_p_es, ax=axs[0, 0]).set_label('Intensity [dB]')
    axs[0, 0].set_ylim([0, 20])
    axs[0, 0].set_ylabel('Frequency [Hz]')
    axs[0, 0].set_title('P_es signal')

    pxx_p_air,  freq_p_air, t_p_air, cax_p_air = axs[0, 1].specgram(p_air_data, noverlap=512, NFFT=2048, Fs=FSAMP)
    fig.colorbar(cax_p_air, ax=axs[0, 1]).set_label('Intensity [dB]')
    axs[0, 1].set_ylim([0, 20])
    axs[0, 1].set_ylabel('Frequency [Hz]')
    axs[0, 1].set_title('P_air signal')

    pxx_volume,  freq_volume, t_volume, cax_volume = axs[1, 0].specgram(volume_data, noverlap=512, NFFT=2048, Fs=FSAMP)
    fig.colorbar(cax_volume, ax=axs[1, 0]).set_label('Intensity [dB]')
    axs[1, 0].set_ylim([0, 20])
    axs[1, 0].set_ylabel('Frequency [Hz]')
    axs[1, 0].set_ylabel('Time [sec]')
    axs[1, 0].set_title('Volume signal')

    pxx_flow,  freq_flow, t_flow, cax_flow = axs[1, 1].specgram(flow_data, noverlap=512, NFFT=2048, Fs=FSAMP)
    fig.colorbar(cax_flow, ax=axs[1, 1]).set_label('Intensity [dB]')
    axs[1, 1].set_ylim([0, 20])
    axs[1, 1].set_ylabel('Frequency [Hz]')
    axs[1, 1].set_ylabel('Time [sec]')
    axs[1, 1].set_title('Flow signal')
    plt.show()
    fig.savefig("Spectrogram_coughing.png")

    p_es_f, p_es_t, p_es_sxx = signal.spectrogram(p_es_data, fs=FSAMP, noverlap=512, nperseg=2048)
    p_es_bandpower = np.empty(0)
    for k in range(0, len(p_es_t)):
        p_es_bandpower_at_time_period = bandpower(p_es_sxx[:, k], p_es_f, fmin=25, fmax=30)
        p_es_bandpower = np.hstack((p_es_bandpower, p_es_bandpower_at_time_period))

    plt.plot(p_es_t, p_es_bandpower)
    plt.show()

    return p_es_bandpower, p_es_t, p_es_f
