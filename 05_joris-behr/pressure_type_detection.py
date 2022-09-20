 """
Pressure type detection
- Detects pressure type from the ventilator data
- Can be either airway pressure OR airway + transpulmonary pressure

Author: Sanne van Deelen
Date: February 2021
"""
from constants import PRESSURE_TYPE


def pressure_type_detection(p_es):
    """
    Returns pressure type
    1 = airway pressure
    2 = airway pressure + transpulmonary pressure
    """
    p_es_list = p_es.tolist()
    p_es_sum = sum(p_es_list)
    if p_es_sum == 0:
        pressure_type = PRESSURE_TYPE.AIRWAY
    else:
        pressure_type = PRESSURE_TYPE.TRANSPULMONARY
    return pressure_type
