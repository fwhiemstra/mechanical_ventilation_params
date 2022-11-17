"""
Plot graphs of the raw data by running the main script. Parts of interest can be found.

Author: Anne Meester
Date: February 2022

"""
import matplotlib.pyplot as plt
import math

from import_and_process_data import import_data
from constants import FS

def graphs_raw_data(p_es, p_air, volume, flow, fs_):
    """
    Plots graphs raw data
    """
    length = flow.shape[0]
    # Calculate the total time measured [minutes]
    t_dur = math.floor(len(flow)/fs_/60)

    # Make list of all inputs
    volume_list = volume.tolist()
    flow_list = flow.tolist()
    pres_air_list = p_air.tolist()
    pres_es_list = p_es.tolist()
    time_sec = [i / fs_ for i in range(0, length)]

    fields = ['pres_es', 'time_sec']
    rows = [pres_es_list, time_sec]
    

    fig = plt.figure()
    ax1 = plt.subplot2grid((2, 2), (0, 0))
    ax2 = plt.subplot2grid((2, 2), (1, 0), sharex=ax1)
    ax3 = plt.subplot2grid((2, 2), (0, 1), sharex=ax1)
    ax4 = plt.subplot2grid((2, 2), (1, 1), sharex=ax1)

    ax1.plot(time_sec,pres_es_list, 'y')
    h1 = ax1.plot(time_sec,pres_es_list)
    ax1.set_title(r'Esophageal pressure')
    ax1.set_ylabel(r'Pressure [cmH2O]')
    ax1.set_xlabel(r'Time [s]')

    ax2.plot(time_sec, pres_air_list, 'm')
    ax2.set_title(r'Airway pressure')
    ax2.set_ylabel(r'Pressure [cmH2O]')
    ax2.set_xlabel(r'Time [s]')

    ax3.plot(time_sec, volume_list, 'c')
    ax3.set_title(r'Volume')
    ax3.set_ylabel(r'Volume [mL]')
    ax3.set_xlabel(r'Time [s]')
        
    ax4.plot(time_sec, flow_list, 'b')
    ax4.set_title(r'Flow')
    ax4.set_ylabel(r'Flow [mL/s]')
    ax4.set_xlabel(r'Time [s]')

    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    # If run seperately from main, visualise data
    input_file = r'C:\Users\joris\OneDrive\Documenten\Studie\TM jaar 2&3\Q1\data\wave_mode\2\Waves_002.txt'
    [p_air, p_es, flow, volume, breath_no] = import_data(input_file)
    graphs_raw_data(p_es, p_air, volume, flow, FS)
