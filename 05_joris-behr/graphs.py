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
from constants import FS, PRESSURE_TYPE
import numpy as np


def graphs(p_air_trim, p_es_trim, p_tp_trim, volume_trim, flow_trim, end_insp, start_insp,end_insp_values,start_insp_values,
           segment_time_sec, pressure_type):


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

    end_insp_scatter = ax2.scatter(end_insp_time, end_insp_values, c='r')
    start_insp_scatter = ax2.scatter(start_insp_time, start_insp_values, c='g')
    ax3.plot(segment_time_sec, p_air_trim, 'k')
    ax5.legend((end_insp_scatter, start_insp_scatter),
            ('End of inspiration', 'Start of inspiration'), loc='upper right', shadow=True)
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



    start_vol = []
    start_aw = []
    start_es = []
    start_tp = []
    for i in start_insp:
        start_vol.append(volume_trim[i])
        start_aw.append(p_air_trim[i])
        start_es.append(p_es_trim[i])
        start_tp.append(p_tp_trim[i])

    end_vol = []
    end_aw = []
    end_es = []
    end_tp = []
    for i in end_insp:
        end_vol.append(volume_trim[i])
        end_aw.append(p_air_trim[i])
        end_es.append(p_es_trim[i])
        end_tp.append(p_tp_trim[i])



    # OPTIONAL: adding inspiration to all graphs
    # ax1.scatter(start_insp_time,start_vol,c='g')
    # ax3.scatter(start_insp_time,start_aw,c='g')
    # ax4.scatter(start_insp_time,start_es,c='g')
    # ax5.scatter(start_insp_time,start_tp,c='g')

    # ax3.scatter(end_insp_time,end_aw, c='r')
    # ax4.scatter(end_insp_time,end_es, c='r')
    # ax5.scatter(end_insp_time, end_tp, c='r')


    plt.tight_layout()
    plt.show()

