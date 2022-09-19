"""
Trim recording to desired length
- by setting t_dur and rec_delay in the GUI

Author: Sanne van Deelen
Date: February 2021
"""


def trim_recording(rec_delay, fs_, p_es, segment_len, volume, flow, p_air, length):
    """
    Returns:
    - trimmed volume values
    - trimmed flow values
    - trimmed airway pressure values
    - trimmed esophageal pressure values
    - segment time
    - total segment length
    """
    # Make list of all inputs
    volume_list = volume.tolist()
    flow_list = flow.tolist()
    pressure_list = p_air.tolist()
    pres_es_list = p_es.tolist()

    if segment_len == 0:
        # If segment length is not defined, use all datapoints untill end of data
        data_length = length - rec_delay
    elif segment_len > length - rec_delay:
        # If segment length is longer than the length of the data,
        # use all datapoints untill end of data
        data_length = length - rec_delay
    else:
        # If segment length is defined, take chosen length
        data_length = segment_len

    # Define start and end indices
    start = rec_delay
    end = start + data_length

    # Trim recording
    volume_trim = volume_list[start:end]
    flow_trim = flow_list[start:end]
    p_air_trim = pressure_list[start:end]
    p_es_trim = pres_es_list[start:end]
    segment_time_sec = [i / fs_ for i in range(0, data_length)]

    return volume_trim, flow_trim, p_air_trim, p_es_trim, segment_time_sec, data_length
