'''
Calculates the mean PEEP

Author: Bart Keulen
Date: October 2021
'''
from numpy import mean, median

def peep_calculator(start_insp, p_air_trim):
    '''
    Calculate mean PEEP per breath as the mean pressure 50 ms before the
    start of inspiration. The PEEP is the mean of the mean PEEP per breath.
    '''
    peep = []

    # Calculate median PEEP per breath as the median pressure 100 ms
    # before the start of inspiration. 
    # If that is not possible (<100 ms), take the mean of all values before the start
    # If that is not possible, take the start value
    for elem in start_insp:
        if elem >= 10:
            exp_pres = median(p_air_trim[elem-10:elem-1])
            peep.append(exp_pres)
        elif 1 < elem < 10:
            exp_pres = median(p_air_trim[:elem-1])
            peep.append(exp_pres)
        else:
            exp_pres = p_air_trim[elem]
            peep.append(exp_pres)
    
    # Calculate mean PEEP value
    mean_peep = round(mean(peep), 2)

    return peep, mean_peep