import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def convert_dtype(x):
    if not x:
        return ''
    try:
        return int(x)   
    except:        
        return 0


def import_data(input_x):
    """"
    Returns airway pressure, esophegeal pressure, flow and volume
    """
    read_input_file = pd.read_csv(input_x, delimiter='\t',converters={'P-Patient /cmH2O':convert_dtype,'P-Optional /cmH2O':convert_dtype,'Flow /ml/s':convert_dtype,'Volume /ml':convert_dtype})
    p_air = read_input_file["P-Patient /cmH2O"]  # Airway pressure
    p_es = read_input_file["P-Optional /cmH2O"]  # Esophageal pressure
    flow = read_input_file["Flow /ml/s"]  # Flow
    volume = read_input_file["Volume /ml"]  # Volume

    # p_air = p_air.replace('--', '0')
    p_air = pd.to_numeric(p_air)

    # p_es = p_es.replace('--', '0')
    p_es = pd.to_numeric(p_es)

    # volume = volume.replace('--', '0')
    volume = pd.to_numeric(volume)

    # flow = flow.replace('--', '0')
    flow = pd.to_numeric(flow)

    return p_air, p_es, flow, volume


def convert_to_numpy_data(p_es, p_air, volume, flow, FSAMP):
    """
    Function converts pd.series to numpy array.
    """

    dt = 1/FSAMP
    p_es_data = p_es.to_numpy().flatten()
    p_air_data = p_air.to_numpy().flatten()
    volume_data = volume.to_numpy().flatten()
    flow_data = flow.to_numpy().flatten()
    data_len = len(p_air_data)
    time_vector = np.arange(0, (data_len)/FSAMP, dt).flatten()

    # fig, axs = plt.subplots(2, 2, sharex=True)
    # axs[0, 0].plot(time_vector, p_es_data)
    # axs[0, 0].set_title('P_es signal')
    # axs[0, 0].grid(which='both')
    # axs[0, 0].set_ylabel('Pressure [mmHg]')

    # axs[0, 1].plot(time_vector, p_air)
    # axs[0, 1].set_title('P_air signal')
    # axs[0, 1].grid(which='both')
    # axs[0, 1].set_ylabel('Pressure [mmHg]')

    # axs[1, 0].plot(time_vector, volume)
    # axs[1, 0].set_title('Volume signal')
    # axs[1, 0].grid(which='both')
    # axs[1, 0].set_ylabel('Volume [mL]')
    # axs[1, 0].set_xlabel('Time [sec]')

    # axs[1, 1].plot(time_vector, flow)
    # axs[1, 1].set_title('Flow signal')
    # axs[1, 1].grid(which='both')
    # axs[1, 1].set_ylabel('Flow [mL/sec]')
    # axs[1, 1].set_xlabel('Time [sec]')
    # fig.suptitle('Normal recording of spontaneous breathing during MV', fontsize=16)
    # fig.tight_layout()
    # plt.show()
    # fig.savefig("Oesophageal_peristalsis.png")
    return p_es_data, p_air_data, volume_data, flow_data, time_vector
