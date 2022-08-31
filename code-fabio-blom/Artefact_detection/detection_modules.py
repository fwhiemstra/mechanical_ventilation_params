from cProfile import label
from turtle import color
import numpy as np
import matplotlib.pyplot as plt


def artefact_detection(time_vector, p_es_std):
    """
    Function performs initial artefact detection based on the moving var of the signal.
    Detection is based on a higher and lower threshold of the STD.
    """
    detection_boolean_list = [None]*len(p_es_std)
    std_upper_threshold = 10
    std_lower_threshold = 0.3

    for k in range(0, len(p_es_std)-1):
        if p_es_std[k] > std_upper_threshold:
            detection_boolean_list[k] = True
        elif p_es_std[k] < std_lower_threshold:
            detection_boolean_list[k] = True
        else:
            detection_boolean_list[k] = False

    return detection_boolean_list

def plot_artefacts_detection(time_vector, detection_boolean_list, time_signal, p_es_signal):
    """
    Function plots the signal along with a boolean vector. False = No artefact, True = Artefact.
    """
    fig, axs1 = plt.subplots(1)
    axs2 = axs1.twinx()

    axs1.plot(time_signal, p_es_signal, 'b')
    axs2.plot(time_vector, detection_boolean_list, 'r')
    plt.show()


def artefact_classification(time_vector, p_es_bandpower, p_es_std, p_air_std, volume_std):
    """
    Function classifies artefact into measurement error, oesophageal peristalsis and coughing.
    """
    classification_measurement_error_boolean_list = [False]*len(time_vector)
    classification_coughing_boolean_list = [False]*len(time_vector)
    classification_es_peristalsis_boolean_list = [False]*len(time_vector)

    # Thresholds std for p_es, volume and p_air
    p_es_std_lower_threshold = 0.3
    p_es_std_upper_threshold = 10
    p_air_upper_threshold = 50               # 2.5
    volume_upper_thresold = 500             # 250

    # Threshold for bandpower
    bandpower_threshold = 0.1              # 0.01

    for k in range(0, len(time_vector)):
        if p_es_std[k] < p_es_std_lower_threshold:
            classification_measurement_error_boolean_list[k] = True
 
        if p_es_std[k] > p_es_std_upper_threshold:
            if volume_std[k] > volume_upper_thresold or p_air_std[k] > p_air_upper_threshold:
                classification_coughing_boolean_list[k] = True
            elif p_es_bandpower[k] > bandpower_threshold:
                classification_coughing_boolean_list[k] = True
            else:
                classification_es_peristalsis_boolean_list[k] = True

    return classification_measurement_error_boolean_list, classification_coughing_boolean_list, classification_es_peristalsis_boolean_list


def plot_artefacts_classification(time_vector, classification_measurement_error_boolean_list, \
    classification_coughing_boolean_list, classification_es_peristalsis_boolean_list, time_signal, p_es_signal):
    """
    Function plots the signal along with three boolean vectors.
    Three boolean vectors represent the artefacts: measurement error, coughing and oesophageal peristalsis.
    False = No artefact, True = Artefact.

    """
    fig, axs1 = plt.subplots(1)
    axs2 = axs1.twinx()
    axs1.plot(time_signal, p_es_signal, color='b')
    axs1.set_title('P_es signal')
    axs1.grid()
    axs1.set_ylabel('Pressure [mmHg]')
    axs2.plot(time_vector, classification_measurement_error_boolean_list, color='g', label='measurement error')
    axs2.plot(time_vector, classification_coughing_boolean_list, color='r', label='coughing')
    axs2.plot(time_vector, classification_es_peristalsis_boolean_list, color='y', label='esophageal peristalsis')
    axs2.legend()
    axs2.set_ylabel('Artifact True or False')
    plt.show()
    fig.savefig('measurement_error')
