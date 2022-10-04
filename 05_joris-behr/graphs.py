"""
Plot the graphs

Author: Sanne van Deelen
Date: February 2021

Modified by Bart Keulen
Date: October 2021

Modified by Anne Meester
Date: February 2022
"""
import matplotlib.pyplot as plt
import numpy as np
from constants import FS, PRESSURE_TYPE, ADJ_HAM


def graphs(p_air_trim, p_es_trim, p_tp_trim, volume_trim, flow_trim, end_insp, start_insp,start_insp_ham,
           end_insp_values, start_insp_values, segment_time_sec, pressure_type):

    # grid plot
    fig = plt.figure()

    if pressure_type == PRESSURE_TYPE.AIRWAY:
        ax1 = plt.subplot2grid((3, 1), (0, 0))
        ax2 = plt.subplot2grid((3, 1), (1, 0), sharex=ax1)
        ax3 = plt.subplot2grid((3, 1), (2, 0), sharex=ax1)

    elif pressure_type == PRESSURE_TYPE.TRANSPULMONARY:
        ax1 = plt.subplot2grid((3, 2), (0, 0))
        ax2 = plt.subplot2grid((3, 2), (1, 0), sharex=ax1)
        ax3 = plt.subplot2grid((3, 2), (2, 0), sharex=ax1)
        ax4 = plt.subplot2grid((3, 2), (0, 1), sharex=ax1)
        ax5 = plt.subplot2grid((3, 2), (1, 1), sharex=ax1)

        ax4.plot(segment_time_sec, p_es_trim, 'y')
        ax4.set_title(r'Esophageal pressure')
        ax4.set_ylabel(r'Pressure [cmH2O]')
        ax4.set_xlabel(r'Time [s]')

        ax5.plot(segment_time_sec, p_tp_trim, 'm')
        ax5.set_title(r'Transpulmonary pressure')
        ax5.set_ylabel(r'Pressure [cmH2O]')
        ax5.set_xlabel(r'Time [s]')

    ax1.plot(segment_time_sec, volume_trim, 'c')
    ax1.set_title(r'Volume')
    ax1.set_ylabel(r'Volume [mL]')
    ax1.set_xlabel(r'Time [s]')
        
    ax2.plot(segment_time_sec, flow_trim, 'b')
    ax2.set_title(r'Flow')
    ax2.set_ylabel(r'Flow [mL/s]')
    ax2.set_xlabel(r'Time [s]')

    if len(start_insp_values) > len(start_insp):
        start_insp_values.remove(start_insp_values[-1])
    end_insp_time = [i / FS for i in end_insp]
    start_insp_time = [i / FS for i in start_insp]
    start_insp_time_ham = [i / FS for i in start_insp_ham-ADJ_HAM]

    end_insp_scatter = ax2.scatter(end_insp_time, end_insp_values, c='r')
    start_insp_scatter = ax2.scatter(start_insp_time, start_insp_values, c='g')
    start_insp_scatter_ham = ax2.scatter(start_insp_time_ham, np.array(flow_trim)[start_insp_ham-ADJ_HAM], c='b')
    ax3.plot(segment_time_sec, p_air_trim, 'k')
    ax5.legend((end_insp_scatter, start_insp_scatter, start_insp_scatter_ham),
            ('End of inspiration', 'Start of inspiration', 'Hamilton breath data'), loc='upper right', shadow=True)
    ax3.set_title(r'Airway pressure')
    ax3.set_ylabel(r'Pressure [cmH2O]')
    ax3.set_xlabel(r'Time [s]')

    end_vol_values = []
    for i in end_insp:
        end_values = volume_trim[i]
        end_vol_values.append(end_values)
    end_insp_vol = ax1.scatter(end_insp_time, end_vol_values, c='r')

    start_p_es = []
    for i in start_insp:
        start_values = p_es_trim[i]
        start_p_es.append(start_values)
    start_insp_pes = ax4.scatter(start_insp_time, start_p_es, c='g')

    plt.tight_layout()
    plt.show()

