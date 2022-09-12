import math
import numpy as np


def buffer(data, duration, data_overlap):
    """ Buffer function reshapes the data array into a now matrix. The new shape depends on the set duration and data_overlap.
    The new shape can be used for periodic calculations. """
    number_of_segments = int(math.ceil((len(data)-data_overlap)/(duration-data_overlap)))
    tempBuf = [data[i:i+duration] for i in range(0, len(data), (duration-int(data_overlap)))]
    tempBuf[number_of_segments-1] = np.pad(tempBuf[number_of_segments-1], (0, duration-tempBuf[number_of_segments-1].shape[0]), 'constant')
    tempBuf2 = np.vstack(tempBuf[0:number_of_segments])
    return tempBuf2, number_of_segments
