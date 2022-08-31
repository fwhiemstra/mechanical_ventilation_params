
import pandas as pd
import math

def export_csv(p_es, p_air, volume, flow, fs_, length, patient_id,t_dur):

    """ export raw data to csv"""
    # Make list of all inputs
    volume_list = volume.tolist()
    flow_list = flow.tolist()
    pres_air_list = p_air.tolist()
    pres_es_list = p_es.tolist()

    import datetime as DT

    time_sec_list = []
    for i in range(0, length):
        time = DT.datetime.utcfromtimestamp(i/fs_).replace(tzinfo=DT.timezone.utc).isoformat("T", "milliseconds")
        time_sec_list.append(time)

    series_list = []
    for i in range(0, length):
        listt = 'volume'
        series_list.append(listt)

    series_list1 = []
    for i in range(0, length):
        listt1 = 'flow'
        series_list1.append(listt1)

    series_list2 = []
    for i in range(0, length):
        listt2 = 'pres_air'
        series_list2.append(listt2)

    series_list3 = []
    for i in range(0, length):
        listt3 = 'pres_es'
        series_list3.append(listt3)

    volume_time = pd.DataFrame(list(zip(series_list, time_sec_list,volume_list)), columns =['series','timestamp','value'])
    flow_time = pd.DataFrame(list(zip(series_list1, time_sec_list,flow_list)), columns =['series','timestamp','value'])
    pres_air_time = pd.DataFrame(list(zip(series_list2, time_sec_list,pres_air_list)), columns =['series','timestamp','value'])
    pres_es_time = pd.DataFrame(list(zip(series_list3, time_sec_list,pres_es_list)), columns =['series','timestamp','value'])

    volume_time["label"] = ""
    flow_time["label"] = ""
    pres_air_time["label"] = ""
    pres_es_time["label"] = ""

    volume_time1 = volume_time.iloc[::5]
    print(len(volume_time1))
    flow_time1 = flow_time.iloc[::5]
    pres_air_time1 = pres_air_time.iloc[::5]
    pres_es_time1 = pres_es_time.iloc[::5]

    patient = str(patient_id)

    allinformation = volume_time1.append(flow_time1)
    allinformation1 = allinformation.append(pres_air_time1)
    allinformation2 = allinformation1.append(pres_es_time1)
    allinformation2.to_csv('annotation_export'+patient+'.csv', index=False)

