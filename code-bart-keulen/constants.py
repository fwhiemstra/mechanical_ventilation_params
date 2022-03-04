"""
Constants used within the mechanical power calculator

Author: Sanne van Deelen
Date: February 2021
"""
# constants from GUI


class PRESSURE_TYPE:
    AIRWAY = 1
    TRANSPULMONARY = 2


class VENTILATION_MODE:
    VCV = 1
    PCV = 2


class INSP_HOLD:
    ZERO_PERCENT = 1
    TEN_PERCENT = 2
    NONE = 3


class PLOTS:
    SHOW = 1
    NO_SHOW = 2


class SUMMARY:
    SHOW = 1
    NO_SHOW = 2


class OUTPUT_FILE:
    EXISTING_FILE = 1
    NEW_FILE = 2


# Other constants
""" sample frequency [samples per second] """
FS = 100
""" conversion factor from [ml * cmH2O] to [Joules] """
CONV_FACTOR = 0.000098
""" fraction of breath time used for minimal separation of breaths
(0.7 is obtained from MATLAB script, unknown why this number is chosen) """
RR_SEP_FRAC = 0.7
