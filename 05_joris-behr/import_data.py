"""
Import data from input file
- import airway pressure, esophegeal pressure, flow and volume from
  input .txt file from the Hamilton C6 Mechanical Ventilator

Author: Sanne van Deelen
Date: February 2021
"""
import pandas as pd

def convert_dtype(x):
    if not x:
        return ''
    try:
        return float(x)   
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
    breath_no = read_input_file["Breath Number"]
    

    return p_air, p_es, flow, volume, breath_no
