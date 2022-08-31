import numpy as np
from scipy.ndimage import generic_filter
import matplotlib.pyplot as plt


def calc_mov_mean_var(time_vector, p_es_data, p_air_data, volume_data, flow_data, FSAMP):
    """ Moving mean and var of all signals are calculated utiziling a generic filter. This filter is normally used in image processing
    but now applied on a 1D signal. The generic filter is a costumized filter, and its effect depends on what function you want to apply.
    Here a window size of 3000 samples was used."""

    p_es_mov_mean = generic_filter(input=p_es_data, function=np.mean, size=(3000,))
    p_es_mov_var = generic_filter(p_es_data, np.std, size=(3000,))

    p_air_mov_mean = generic_filter(input=p_air_data, function=np.mean, size=(3000,))
    p_air_mov_var = generic_filter(p_air_data, np.std, size=(3000,))

    volume_mov_mean = generic_filter(input=volume_data, function=np.mean, size=(3000,))
    volume_mov_var = generic_filter(volume_data, np.std, size=(3000,))

    flow_mov_mean = generic_filter(input=flow_data, function=np.mean, size=(3000,))
    flow_mov_var = generic_filter(flow_data, np.std, size=(3000,))

    fig1, axs1 = plt.subplots(2, 2, sharex=True)
    axs1_0_0 = axs1[0, 0].twinx()
    axs1_0_1 = axs1[0, 1].twinx()
    axs1_1_0 = axs1[1, 0].twinx()
    axs1_1_1 = axs1[1, 1].twinx()

    axs1[0, 0].plot(time_vector, p_es_data, 'b')
    axs1[0, 0].plot(time_vector, p_es_mov_mean, 'g')
    axs1[0, 0].set_title('P_es signal')
    axs1[0, 0].grid(which='both')
    axs1[0, 0].set_ylabel('Pressure [mmHg]')
    axs1_0_0.set_ylabel('STD [mmHg]')

    axs1[0, 1].plot(time_vector, p_air_data, 'b')
    axs1[0, 1]. plot(time_vector, p_air_mov_mean, 'g')
    axs1[0, 1].set_title('P_air signal')
    axs1[0, 1].grid(which='both')
    axs1[0, 1].set_ylabel('Pressure [mmHg]')
    axs1_0_1.set_ylabel('STD [mmHg]')

    axs1[1, 0].plot(time_vector, volume_data, 'b')
    axs1[1, 0].plot(time_vector, volume_mov_mean, 'g')
    axs1[1, 0].set_title('Volume signal')
    axs1[1, 0].grid(which='both')
    axs1[1, 0].set_ylabel('Volume [mL]')
    axs1[1, 0].set_xlabel('Time [sec]')
    axs1[1, 0].set_ylabel('STD [mL]')

    axs1[1, 1].plot(time_vector, flow_data, 'b')
    axs1[1, 1].plot(time_vector, flow_mov_mean, 'g')
    axs1[1, 1].set_title('Flow signal')
    axs1[1, 1].grid(which='both')
    axs1[1, 1].set_ylabel('Flow [mL/sec]')
    axs1[1, 1].set_xlabel('Time [sec]')
    axs1_1_1.set_ylabel('STD [mL/sec]')
    fig1.tight_layout()

    fig2, axs2 = plt.subplots(2, 2, sharex=True)
    axs2_0_0 = axs2[0, 0].twinx()
    axs2_0_1 = axs2[0, 1].twinx()
    axs2_1_0 = axs2[1, 0].twinx()
    axs2_1_1 = axs2[1, 1].twinx()

    axs2_2 = axs2.twinx()

    axs2.plot(time_vector, p_es_data, 'b')
    axs2_2.plot(time_vector, p_es_mov_var, 'y')
    axs2.set_title('P_es signal')
    axs2.grid(which='both')
    axs2.set_ylabel('Pressure [mmHg]')
    axs2_2.set_ylim([0, 100])
    axs2_2.set_ylabel('STD [mmHg]')

    axs2[0, 0].plot(time_vector, p_es_data, 'b')
    axs2_0_0.plot(time_vector, p_es_mov_var, 'y')
    axs2[0, 0].set_title('P_es signal')
    axs2[0, 0].grid(which='both')
    axs2[0, 0].set_ylabel('Pressure [mmHg]')
    axs2_0_0.set_ylabel('STD [mmHg]')

    axs2[0, 1]. plot(time_vector, p_air_data, 'b')
    axs2_0_1.plot(time_vector, p_air_mov_var, 'y')
    axs2[0, 1].set_title('P_air signal')
    axs2[0, 1].grid(which='both')
    axs2[0, 1].set_ylabel('Pressure [mmHg]')
    axs2_0_1.set_ylabel('STD [mmHg]')

    axs2[1, 0]. plot(time_vector, volume_data, 'b')
    axs2_1_0.plot(time_vector, volume_mov_var, 'y')
    axs2[1, 0].set_title('Volume signal')
    axs2[1, 0].grid(which='both')
    axs2[1, 0].set_ylabel('Volume [mL]')
    axs2[1, 0].set_xlabel('Time [sec]')
    axs2_1_0.set_ylabel('STD [mL]')

    axs2[1, 1].plot(time_vector, flow_data, 'b')
    axs2_1_1.plot(time_vector, flow_mov_var, 'y')
    axs2[1, 1].set_title('Flow signal')
    axs2[1, 1].grid(which='both')
    axs2[1, 1].set_ylabel('Flow [mL/sec]')
    axs2[1, 1].set_xlabel('Time [sec]')
    axs2_1_1.set_ylabel('STD [mL/sec]')
    fig2.tight_layout()

    plt.show()
    # fig1.savefig('Mean_coughing.png')
    # fig2.savefig('Std_coughing.png')

    return p_es_mov_mean, p_air_mov_mean, volume_mov_mean, flow_mov_mean, \
        p_es_mov_var, p_air_mov_var, volume_mov_var, flow_mov_var
