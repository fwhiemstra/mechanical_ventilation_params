from import_and_process_data import convert_to_numpy_data
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from constants import FS

"""This code detects coughs, filters the coughs and returns different cough parameters

Author: Jill Oudshoorn
Date: July 2022 

"""

def running_mean(x, N, mean_total):
    x = np.pad(x, N//2, constant_values = mean_total)
    cumsum = np.cumsum(np.insert(x, 0, 0))
    mean = (cumsum[N:] - cumsum[:-N]) / float(N)
    return mean

def coughdetection(p_es, p_air, volume, flow,breath_no):
    
    #Determing constants based on data frequency
    COUGH_REMOVE_SIZE = round(0.1*FS)
    RUNNING_MEAN_SIZE = round(1*FS)

    # Convert data for easier handling. Long input due to function requirements.
    p_es_signal,p_air_signal,volume_signal,flow_signal, F_signal= convert_to_numpy_data(p_es,p_air,volume,flow,FS)
    peakspositive, _ = find_peaks(p_es_signal, prominence=1)
    peakvalues_positive = p_es_signal[peakspositive]

    # detect peaks above 1.4* the mean and take the area of one peak before and two peaks after
    mean_total = sum(peakvalues_positive)/len(peakvalues_positive)
    mean_peaks = running_mean(peakvalues_positive, RUNNING_MEAN_SIZE, mean_total)
    artefact_peaks = []
    for i in range(1, len(peakspositive)-2):
        if p_es_signal[peakspositive[i]] > 1.4*mean_peaks[i]: 
            artefact_peaks.extend(list(range((peakspositive[i-1]), (peakspositive[i+2]))))
    artefact_peaks = list(set(artefact_peaks))
    
    # Plots to show the found artefact peaks
    # plt.plot(artefact_peaks,p_es_signal[artefact_peaks], "ob"); plt.plot(p_es_signal)
    # plt.show()

    # remove more than the detected cough in order to get better clean data. 
    artefact_peaks_remove = []
    for i in range(0, len(peakspositive)):
        if p_es_signal[peakspositive[i]] > 1.4*mean_peaks[i]: 
            if i <= COUGH_REMOVE_SIZE: 
                artefact_peaks_remove.extend(list(range((peakspositive[0]), (peakspositive[i+COUGH_REMOVE_SIZE]))))
            if len(artefact_peaks)-i <= COUGH_REMOVE_SIZE:
                artefact_peaks_remove.extend(list(range((peakspositive[i-COUGH_REMOVE_SIZE]), (peakspositive[-1]))))
            else:
                artefact_peaks_remove.extend(list(range((peakspositive[i-COUGH_REMOVE_SIZE]), (peakspositive[i+COUGH_REMOVE_SIZE]))))

    artefact_peaks_remove = list(set(artefact_peaks_remove))

    """ Creating artefact list"""
    cough_time = 0
    artefact_detection = [0]*len(p_es_signal)
    for i in range(0, len(artefact_peaks)):
        artefact_detection[artefact_peaks[i]] = "cough"
        cough_time+=1
    for i in range(0, len(artefact_detection)):
        if artefact_detection[i] == 0:
            artefact_detection[i] = 'no cough'
    
    """ Cough parameter calculations"""
    #time of coughing in seconds
    cough_time_total = cough_time/FS
    cough_time_percentage = cough_time/len(artefact_detection)
    
    #create dictionary with all the coughs
    def grouper(iterable):
        prev = None
        group = []
        for item in iterable:
            if prev is None or item - prev <= 1:
                group.append(item)
            else:
                yield group
                group = [item]
            prev = item
        if group:
            yield group
        return group 

    group = dict(enumerate(grouper(artefact_peaks),1))

    #number of coughs
    number_coughs = len(group)
    
    # When no cough is detected other parameters aren't calculated
    if number_coughs !=0:
        #cough_power: mean per cough, overal mean
        cough_power =[]
        for key in group:
            power = p_es_signal[group[key]]
            mean_power = sum(power)/len(power)
            cough_power.append(mean_power)
        mean_cough_power = sum(cough_power)/len(cough_power)

        #mean amplitude of cough
        cough_amplitude = []
        for key in group:
            power = p_es_signal[group[key]]
            amplitude = max(power)-min(power)
            cough_amplitude.append(amplitude)
        mean_cough_amplitude = sum(cough_amplitude)/len(cough_amplitude)
        
        #length of cough
        cough_length = []
        for key in group:
            length = len(group[key])
            cough_length.append(length)
        mean_cough_length = (sum(cough_length)/len(cough_power))/FS

        temp = (list(group))

        #time in between coughs in seconds
        mean_cough_inbetweentime = (len(p_es_signal)-cough_time)/number_coughs/FS

        #Percentage coughs >60L/min
        Number_hard_coughs = 0
        Number_mild_coughs = 0
        cough_peak_flow = []
        for key in group:
            flow_cough = flow[group[key]]
            peak_flow = max(flow_cough)
            peak_flow = float(peak_flow)
            if peak_flow >= float(60*(1000/60)): #from ml/s to L/min
                Number_hard_coughs += 1
            else:
                Number_mild_coughs += 1
            cough_peak_flow.append(peak_flow)

        # Cough peak flow
        mean_cough_peak_flow = sum(cough_peak_flow)/len(cough_peak_flow)
        max_cough_peak_flow = max(cough_peak_flow)
        percentage_hard_coughs = Number_hard_coughs/(Number_hard_coughs+Number_mild_coughs)

        """ Filtering data on coughs """
        #delete cough segments from volume, flow, airway pressure and oesophagus pressure
        p_es_clean = list(range(0, len(p_es_signal)))
        cleandata = set(p_es_clean) ^ set(artefact_peaks_remove)
        cleandata1 = [int(item) for item in cleandata]
    
        p_es_clean = p_es[cleandata1]
        p_air_clean = p_air[cleandata1]
        flow_clean = flow[cleandata1]
        volume_clean = volume[cleandata1]
        breath_no_clean = breath_no[cleandata1]

        length = len(p_es_clean)
        time_sec = [i / FS for i in range(0, length)]
    
        #_, axs = plt.subplots(2, sharey=True)
        
        # Plot with clean data
        #axs[0].plot(artefact_peaks_remove,p_es_signal[artefact_peaks_remove], "ob"); axs[0].plot(p_es_signal)
        #axs[1].plot(time_sec,p_es_clean)
        #plt.show()

        return p_es_clean,p_air_clean,flow_clean,volume_clean, breath_no_clean, artefact_detection,cough_time_total, cough_time_percentage, number_coughs, mean_cough_power, mean_cough_amplitude, mean_cough_length, mean_cough_inbetweentime, mean_cough_peak_flow, max_cough_peak_flow, percentage_hard_coughs    
    else:   
        artefact_detection =0
        cough_time_total =0
        cough_time_percentage =0
        mean_cough_power =0
        mean_cough_amplitude =0
        mean_cough_length =0
        mean_cough_inbetweentime=0
        mean_cough_peak_flow =0
        max_cough_peak_flow =0
        percentage_hard_coughs =0
        print("no coughs detected")
        return p_es, p_air, flow, volume, artefact_detection,cough_time_total, cough_time_percentage, number_coughs, mean_cough_power, mean_cough_amplitude, mean_cough_length, mean_cough_inbetweentime, mean_cough_peak_flow, max_cough_peak_flow, percentage_hard_coughs