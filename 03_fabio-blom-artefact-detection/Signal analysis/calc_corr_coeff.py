import numpy as np
import matplotlib.pyplot as plt
from buffer import buffer


def calc_corr_coeff(time_vector, p_es_data, p_air_data, volume_data, flow_data, FSAMP, figure_name):
    """ Function calculates the periodic correlation coefficient. Buffer function is hereby used to reshape the data for calculations."""
    window_len = 30
    shift_len = 10
    duration = int(window_len*FSAMP)
    data_overlap = (window_len-shift_len)*FSAMP

    p_es_data_buff, number_of_segments = buffer(p_es_data, duration, data_overlap)
    p_air_data_buff, number_of_segments = buffer(p_air_data, duration, data_overlap)
    volume_data_buff, number_of_segments = buffer(volume_data, duration, data_overlap)
    flow_data_buff, number_of_segments = buffer(flow_data, duration, data_overlap)
    time_vector_buff, number_of_segments = buffer(time_vector, duration, data_overlap)

    # Initial empty np array that will contain correlation coefficient values over time
    cc_p_es_p_air = np.empty(0)
    cc_p_es_volume = np.empty(0)
    cc_p_es_flow = np.empty(0)

    cc_p_air_p_es = np.empty(0)
    cc_p_air_volume = np.empty(0)
    cc_p_air_flow = np.empty(0)

    cc_volume_p_es = np.empty(0)
    cc_volume_p_air = np.empty(0)
    cc_volume_flow = np.empty(0)

    cc_flow_p_es = np.empty(0)
    cc_flow_p_air = np.empty(0)
    cc_flow_volume = np.empty(0)

    cc_time = np.empty(0)

    for k in range(0, number_of_segments-1):
        # Correlation of p_es and other signals
        cc_p_es_p_air_buff = np.corrcoef(p_es_data_buff[k, :], p_air_data_buff[k, :])[0, 1]
        cc_p_es_volume_buff = np.corrcoef(p_es_data_buff[k, :], volume_data_buff[k, :])[0, 1]
        cc_p_es_flow_buff = np.corrcoef(p_es_data_buff[k, :], flow_data_buff[k, :])[0, 1]

        # Correlation of p_air and other signals
        cc_p_air_p_es_buff = np.corrcoef(p_air_data_buff[k, :], p_es_data_buff[k, :])[0, 1]
        cc_p_air_volume_buff = np.corrcoef(p_air_data_buff[k, :], volume_data_buff[k, :])[0, 1]
        cc_p_air_flow_buff = np.corrcoef(p_air_data_buff[k, :], flow_data_buff[k, :])[0, 1]

        # Correlation of volume and other signals
        cc_volume_p_es_buff = np.corrcoef(volume_data_buff[k, :], p_es_data_buff[k, :])[0, 1]
        cc_volume_p_air_buff = np.corrcoef(volume_data_buff[k, :], p_air_data_buff[k, :])[0, 1]
        cc_volume_flow_buff = np.corrcoef(volume_data_buff[k, :], flow_data_buff[k, :])[0, 1]

        # Correlation of flow and other signals
        cc_flow_p_es_buff = np.corrcoef(flow_data_buff[k, :], p_es_data_buff[k, :])[0, 1]
        cc_flow_p_air_buff = np.corrcoef(flow_data_buff[k, :], p_air_data_buff[k, :])[0, 1]
        cc_flow_volume_buff = np.corrcoef(flow_data_buff[k, :], volume_data_buff[k, :])[0, 1]

        cc_time_buff = np.mean(time_vector_buff[k, :])

        # Hstacking new correlation values to old values in vector
        # p_es correlation coefficients
        cc_p_es_p_air = np.hstack((cc_p_es_p_air, cc_p_es_p_air_buff))
        cc_p_es_volume = np.hstack((cc_p_es_volume, cc_p_es_volume_buff))
        cc_p_es_flow = np.hstack((cc_p_es_flow, cc_p_es_flow_buff))

        # p_air correlation coefficients
        cc_p_air_p_es = np.hstack((cc_p_air_p_es, cc_p_air_p_es_buff))
        cc_p_air_volume = np.hstack((cc_p_air_volume, cc_p_air_volume_buff))
        cc_p_air_flow = np.hstack((cc_p_air_flow, cc_p_air_flow_buff))

        # volume correlation coefficients
        cc_volume_p_es = np.hstack((cc_volume_p_es, cc_volume_p_es_buff))
        cc_volume_p_air = np.hstack((cc_volume_p_air, cc_volume_p_air_buff))
        cc_volume_flow = np.hstack((cc_volume_flow, cc_volume_flow_buff))

        # flow correlation coefficients
        cc_flow_p_es = np.hstack((cc_flow_p_es, cc_flow_p_es_buff))
        cc_flow_p_air = np.hstack((cc_flow_p_air, cc_flow_p_air_buff))
        cc_flow_volume = np.hstack((cc_flow_volume, cc_flow_volume_buff))

        # Time vector for plotting correlation coefficients
        cc_time = np.hstack((cc_time, cc_time_buff))


    # Plotting the correlation coefficient values over time.
    fig, axs1 = plt.subplots(2, 2, sharex=True)
    axs_0_0_2 = axs1[0, 0].twinx()
    axs_0_1_2 = axs1[0, 1].twinx()
    axs_1_0_2 = axs1[1, 0].twinx()
    axs_1_1_2 = axs1[1, 1].twinx()

    axs1[0, 0].plot(time_vector, p_es_data, label='pressure signal')
    axs1[0, 0].set_xlabel('Time [sec]')
    axs1[0, 0].set_ylabel('Pressure [mmHg]')
    axs1[0, 0].grid(which='major')

    axs_0_0_2.plot(cc_time, cc_p_es_p_air, color='y', label='cc-pes-pair')
    axs_0_0_2.set_ylabel('Correlation coefficient')
    axs_0_0_2.plot(cc_time, cc_p_es_volume, color='g', label='cc-pes-vol')
    axs_0_0_2.plot(cc_time, cc_p_es_flow, color='r', label='cc-pes-flow')
    axs_0_0_2.legend(loc='upper right')

    axs1[0, 1].plot(time_vector, p_air_data, label='pressure signal')
    axs1[0, 1].set_xlabel('Time [sec]')
    axs1[0, 1].set_ylabel('Pressure [mmHg]')
    axs1[0, 1].grid(which='major')

    axs_0_1_2.plot(cc_time, cc_p_air_p_es, color='y', label='cc-pair-pes')
    axs_0_1_2.set_ylabel('Correlation coefficient')
    # axs_0_1_2.plot(cc_time, cc_p_air_volume, color='g', label='cc-pair-vol')
    # axs_0_1_2.plot(cc_time, cc_p_air_flow, color='r', label='cc-pair-flow')
    axs_0_1_2.legend(loc='upper right')

    axs1[1, 0].plot(time_vector, volume_data, label='volume signal')
    axs1[1, 0].set_xlabel('Time [sec]')
    axs1[1, 0].set_ylabel('Volume [mL]')
    axs1[1, 0].grid(which='major')

    axs_1_0_2.plot(cc_time, cc_volume_p_es, color='y', label='cc-vol-pes')
    axs_1_0_2.set_ylabel('Correlation coefficient')
    # axs_1_0_2.plot(cc_time, cc_volume_p_air, color='g', label='cc-vol-pair')
    # axs_1_0_2.plot(cc_time, cc_volume_flow, color='r', label='cc-vol-flow')
    axs_1_0_2.legend(loc='upper right')

    axs1[1, 1].plot(time_vector, flow_data, label='flow')
    axs1[1, 1].set_xlabel('Time [sec]')
    axs1[1, 1].set_ylabel('Flow [mL/sec]')
    axs1[1, 1].grid(which='major')

    axs_1_1_2.plot(cc_time, cc_flow_p_es, color='y', label='cc-flow-pes')
    axs_1_1_2.set_ylabel('Correlation coefficient')
    # axs_1_1_2.plot(cc_time, cc_flow_p_air, color='g', label='cc-flow-pair')
    # axs_1_1_2.plot(cc_time, cc_flow_volume, color='r', label='cc-flow-vol')
    axs_1_1_2.legend(loc='upper right')
    plt.tight_layout()
    plt.show()
    fig.savefig(figure_name)
