# Import libraries
import numpy as np
import matplotlib.pyplot as plt

# Import modules
from import_and_process_data import import_data, convert_to_numpy_data
from buffer import buffer
from std_per_segment import std_per_segment
from bandpower_per_segment import bandpower_per_segment
from detection_modules import artefact_classification, artefact_detection, plot_artefacts_detection, plot_artefacts_classification

# Constant
FSAMP = 100

my_file = '../1__211006132800_Waves_001.txt'
p_air, p_es, flow, volume = import_data(my_file)
p_es_signal, p_air_signal, volume_signal, flow_signal, time_signal = \
    convert_to_numpy_data(p_es, p_air, volume, flow, FSAMP)

window_len = 20             # 30
shift_len = 10
duration = int(window_len*FSAMP)
data_overlap = (window_len-shift_len)*FSAMP

p_es_data, number_segments = buffer(p_es_signal, duration, data_overlap)
p_air_data, number_segments = buffer(p_air_signal, duration, data_overlap)
volume_data, number_segments = buffer(volume_signal, duration, data_overlap)
flow_data, number_segments = buffer(flow_signal, duration, data_overlap)
time_data, number_segments = buffer(time_signal, duration, data_overlap)


time_vector, p_es_std = std_per_segment(time_data, p_es_data)
time_vector, p_air_std = std_per_segment(time_data, p_air_data)
time_vector, volume_std = std_per_segment(time_data, volume_data)
time_vector, flow_std = std_per_segment(time_data, flow_data)

fig, axs = plt.subplots(2, 2, sharex=True)
axs[0, 0].plot(time_vector, p_es_std)
axs[0, 1].plot(time_vector, p_air_std)
axs[1, 0].plot(time_vector, volume_std)
axs[1, 1].plot(time_vector, flow_std)
plt.show()


time_vector, p_es_bandpower = bandpower_per_segment(time_data, p_es_data, fs=FSAMP, fmin=25, fmax=30)
fig, axs1 = plt.subplots(2, sharex=True)
axs2 = axs1[0].twinx()
axs1[0].plot(time_signal, p_es_signal)
axs2.plot(time_vector, p_es_bandpower, color='r')
axs1[1].plot(time_vector, volume_std, color='y')
plt.show()


detection_boolean_list = artefact_detection(time_vector, p_es_std)
plot_artefacts_detection(time_vector, detection_boolean_list, time_signal, p_es_signal)

classification_measurement_error_boolean_list, classification_coughing_boolean_list, classification_es_peristalsis_boolean_list = \
    artefact_classification(time_vector, p_es_bandpower, p_es_std, p_air_std, volume_std)

plot_artefacts_classification(time_vector, classification_measurement_error_boolean_list, \
    classification_coughing_boolean_list, classification_es_peristalsis_boolean_list, time_signal, p_es_signal)
