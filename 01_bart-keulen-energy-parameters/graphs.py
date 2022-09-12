"""
Plot the graphs

Author: Sanne van Deelen
Date: February 2021

Modified by Bart Keulen
Date: October 2021
"""
import matplotlib.pyplot as plt

from constants import PLOTS, FS, PRESSURE_TYPE


def graphs(show_plots, p_air_trim, p_es_trim, p_tp_trim, volume_trim, flow_trim, end_insp, start_insp,
           end_insp_values, start_insp_values, pv_starts, pv_ends, segment_time_sec, pressure_type):
    """
    plots graphs if checkbox is clicked in GUI
    """
    if show_plots == PLOTS.SHOW:
        # grid plot
        fig = plt.figure()

        if pressure_type == PRESSURE_TYPE.AIRWAY:
            ax1 = plt.subplot2grid((3, 2), (0, 0))
            ax2 = plt.subplot2grid((3, 2), (1, 0), sharex=ax1)
            ax3 = plt.subplot2grid((3, 2), (2, 0), sharex=ax1)
            ax6 = plt.subplot2grid((3, 2), (1, 0), rowspan=3)

        elif pressure_type == PRESSURE_TYPE.TRANSPULMONARY:
            ax1 = plt.subplot2grid((4, 2), (0, 0))
            ax2 = plt.subplot2grid((4, 2), (0, 1), sharex=ax1)
            ax3 = plt.subplot2grid((4, 2), (1, 0), sharex=ax1)
            ax4 = plt.subplot2grid((4, 2), (2, 0), sharex=ax1)
            ax5 = plt.subplot2grid((4, 2), (3, 0), sharex=ax1)
            ax6 = plt.subplot2grid((4, 2), (1, 1), rowspan=4)

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
        end_insp_scatter = ax3.scatter(end_insp_time, end_insp_values, c='r')
        start_insp_scatter = ax3.scatter(start_insp_time, start_insp_values, c='g')
        ax3.plot(segment_time_sec, p_air_trim, 'k')
        ax3.legend((end_insp_scatter, start_insp_scatter),
                ('End of inspiration', 'Start of inspiration'), loc='upper right', shadow=True)
        ax3.set_title(r'Airway pressure')
        ax3.set_ylabel(r'Pressure [cmH2O]')
        ax3.set_xlabel(r'Time [s]')

        for start, stop in zip(pv_starts, pv_ends):
            pres = p_air_trim[start:stop]
            vol = volume_trim[start:stop]
            ax6.plot(pres, vol)
            ax6.set_title(r'Pressure-volume loops of airway pressure')
            ax6.set_xlabel(r'Pressure [cmH2O]')
            ax6.set_ylabel(r'Volume [mL]')

        plt.tight_layout()
        plt.show()

    elif show_plots == PLOTS.NO_SHOW:
        pass

    return None
