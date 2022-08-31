import numpy as np
import matplotlib.pyplot as plt
from buffer import buffer
import pandas as pd
import scipy.stats as stats


def calc_entropy(time_vector, p_es_data, p_air_data, volume_data, flow_data, FSAMP, figure_name):
    """Fuction calculates periodic entropy. Buffer function is used to reshape the data for periodic calculations."""
    window_len = 30
    shift_len = 10
    duration = int(window_len*FSAMP)
    data_overlap = (window_len-shift_len)*FSAMP

    p_es_data_buff, number_of_segments = buffer(p_es_data, duration, data_overlap)
    p_air_data_buff, number_of_segments = buffer(p_air_data, duration, data_overlap)
    volume_data_buff, number_of_segments = buffer(volume_data, duration, data_overlap)
    flow_data_buff, number_of_segments = buffer(flow_data, duration, data_overlap)
    time_vector_buff, number_of_segments = buffer(time_vector, duration, data_overlap)
    # Emptry data arrays that will be filled with entropy values. 
    p_es_entropy = np.empty(0)
    p_air_entropy = np.empty(0)
    volume_entropy = np.empty(0)
    flow_entropy = np.empty(0)
    time_entropy = np.empty(0)

    for k in range(0, number_of_segments-1):
        p_es_pd_series = pd.Series(p_es_data_buff[k, :])
        p_air_pd_series = pd.Series(p_air_data_buff[k, :])
        volume_pd_series = pd.Series(volume_data_buff[k, :])
        flow_pd_series = pd.Series(flow_data_buff[k, :])

        p_es_counts = p_es_pd_series.value_counts()
        p_air_counts = p_air_pd_series.value_counts()
        volume_counts = volume_pd_series.value_counts()
        flow_counts = flow_pd_series.value_counts()

        p_es_entropy_new_val = stats.entropy(p_es_counts)
        p_air_entropy_new_val = stats.entropy(p_air_counts)
        volume_entropy_new_val = stats.entropy(volume_counts)
        flow_entropy_new_val = stats.entropy(flow_counts)
        H_time = np.mean(time_vector_buff[k, :])

        p_es_entropy = np.hstack((p_es_entropy, p_es_entropy_new_val))
        p_air_entropy = np.hstack((p_air_entropy, p_air_entropy_new_val))
        volume_entropy = np.hstack((volume_entropy, volume_entropy_new_val))
        flow_entropy = np.hstack((flow_entropy, flow_entropy_new_val))
        time_entropy = np.hstack((time_entropy, H_time))
    
    # Plots of periodic entropy of all signals 
    fig, axs1 = plt.subplots(2, 2, sharex=True)

    axs_0_0_2 = axs1[0, 0].twinx()
    axs_0_1_2 = axs1[0, 1].twinx()
    axs_1_0_2 = axs1[1, 0].twinx()
    axs_1_1_2 = axs1[1, 1].twinx()

    axs1[0, 0].plot(time_vector, p_es_data, label='pressure signal')
    axs1[0, 0].set_xlabel('Time [sec]')
    axs1[0, 0].set_ylabel('Pressure [mmHg]')
    axs1[0, 0].grid(which='major')

    axs_0_0_2.set_ylabel('Entropy [shannon]')
    axs_0_0_2.plot(time_entropy, p_es_entropy, color='r', label='p_es_entropy')
    axs_0_0_2.legend(loc='upper right')

    axs1[0, 1].plot(time_vector, p_air_data, label='pressure signal')
    axs1[0, 1].set_xlabel('Time [sec]')
    axs1[0, 1].set_ylabel('Pressure [mmHg]')
    axs1[0, 1].grid(which='major')

    axs_0_1_2.set_ylabel('Entropy [shannon]')
    axs_0_1_2.plot(time_entropy, p_air_entropy, color='r', label='p_air_entropy')
    axs_0_1_2.legend(loc='upper right')

    axs1[1, 0].plot(time_vector, volume_data, label='volume signal')
    axs1[1, 0].set_xlabel('Time [sec]')
    axs1[1, 0].set_ylabel('Volume [mL]')
    axs1[1, 0].grid(which='major')

    axs_1_0_2.set_ylabel('Entropy [shannon]')
    axs_1_0_2.plot(time_entropy, volume_entropy, color='r', label='volume_entropy')
    axs_1_0_2.legend(loc='upper right')

    axs1[1, 1].plot(time_vector, flow_data, label='flow')
    axs1[1, 1].set_xlabel('Time [sec]')
    axs1[1, 1].set_ylabel('Flow [mL/sec]')
    axs1[1, 1].grid(which='major')

    axs_1_1_2.set_ylabel('Entropy [shannon]')
    axs_1_1_2.plot(time_entropy, flow_entropy, color='r', label='flow_entropy')
    axs_1_1_2.legend(loc='upper right')

    plt.tight_layout()
    plt.show()
    fig.savefig(figure_name)








