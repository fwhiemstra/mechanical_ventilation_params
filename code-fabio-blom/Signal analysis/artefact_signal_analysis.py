# Import modules
from import_and_process_data import import_data, convert_to_numpy_data
from calc_mov_mean_var import calc_mov_mean_var
from calc_corr_coeff import calc_corr_coeff
from calc_spectogram import calc_spectrogram
from calc_entropy import calc_entropy
from try_out_artefact_algorithm import artefact_detection, artefact_classification, plot_artefacts_detection


# Constant
FSAMP = 100

my_file = '15_220207192455_Waves_001.txt'                                           # Enter the file pathway name in here
p_air, p_es, flow, volume = import_data(my_file)                                    # Airway pressure, Esophageal pressure, Lung Volume, Air flow are imported as pd.series
p_es_data, p_air_data, volume_data, flow_data, time_vector = \
    convert_to_numpy_data(p_es, p_air, volume, flow, FSAMP)                         # Pd.series are converted to np.array for personal preference

p_es_mean, p_air_mean, volume_mean, flow_mean, p_es_var, p_air_var, volume_var, flow_var = calc_mov_mean_var(time_vector, p_es_data, p_air_data, volume_data, flow_data, FSAMP)                 # The moving mean and variance are calculated over time.

calc_corr_coeff(time_vector, p_es_data, p_air_data, volume_data, flow_data, FSAMP, 'cc_data_coughing.png')        # Correlation coefficients of raw p_es compared to other raw signals are plotted over time
calc_corr_coeff(time_vector, p_es_mean, p_air_mean, volume_mean, flow_mean, FSAMP, 'cc_mean_coughing.png')        # Correlation coefficients of mean p_es compared to other mean signals are plotted over time
calc_corr_coeff(time_vector, p_es_var, p_air_var, volume_var, flow_var, FSAMP, 'cc_var_coughing.png')             # Correlation coefficients of var p_es compared to other var signals are plotted over time

calc_entropy(time_vector, p_es_data, p_air_data, volume_data, flow_data, FSAMP, 'entropy_coughing')               # entropy of all signals are calculated over time

p_es_bandpower, p_es_t, p_es_f = calc_spectrogram(p_es_data, p_air_data, volume_data, flow_data, FSAMP)           # spectrogram of all signals is plotted over time and the bandpower is calculated
