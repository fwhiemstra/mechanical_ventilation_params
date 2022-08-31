import pandas as pd
from datetime import datetime
from datetime import timezone
import pandas

def annotate_import(input_x, input_annotation, fs_):
    """"
    Returns airway pressure, esophegeal pressure, flow, volume, timestamp 
    """
    read_input_file2 = pd.read_csv(input_x, delimiter='\t')
    p_air = read_input_file2["P-Patient /cmH2O"]  # Airway pressure
    p_es = read_input_file2["P-Optional /cmH2O"]  # Esophageal pressure
    flow = read_input_file2["Flow /ml/s"]  # Flow
    volume = read_input_file2["Volume /ml"]  # Volume
    length = flow.shape[0]
    print(length)
    read_input_file = pd.read_csv(input_annotation)
    read_input_file1 = pd.DataFrame(read_input_file)
   
    p_air_raw = read_input_file1.loc[read_input_file1['series']=='pres_air']
    p_es_raw = read_input_file1.loc[read_input_file1['series']=='pres_es']
    flow_raw = read_input_file1.loc[read_input_file1['series']=='flow']
    volume_raw = read_input_file1.loc[read_input_file1['series']=='volume']
    print(len(volume_raw))
    
    time_sec = [i / fs_ for i in range(0, length)]
    artefact_timestamp = p_es_raw['label']
    artefact_timestamp1 = artefact_timestamp.repeat(5)
    print(len(artefact_timestamp1))
    artefact_timestamp_compressed = pd.DataFrame(list(zip(artefact_timestamp1, time_sec)))
      
   
    return p_air, p_es, flow, volume, artefact_timestamp1, artefact_timestamp_compressed