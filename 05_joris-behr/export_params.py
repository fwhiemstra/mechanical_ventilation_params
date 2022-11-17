"""Script to export parameters to csv

Author: Joris Behr
Date: October 2022

"""
import pandas as pd

def export_params(e_aw, e_es, e_tp, pow_aw, pow_es, pow_tp, e_hys_aw, e_hys_es, e_hys_tp, hys_aw, hys_es, hys_tp, ptp_es, ptp_tp, tp_peak, tp_swing):
    # print(len(e_aw), len(e_es), len(e_tp), len(pow_aw), len(pow_es), len(pow_tp), len(hys_aw), len(hys_es), len(hys_tp), len(ptp_es), len(ptp_tp), len(tp_peak), len(tp_swing))
    data = {"e_aw": e_aw, "e_es": e_es,"e_tp": e_tp,"pow_aw": pow_aw,"pow_es": pow_es,"pow_tp": pow_tp,"e_hys_aw": e_hys_aw, "e_hys_es": e_hys_es, "e_hys_tp": e_hys_tp,  "hys_aw": hys_aw,"hys_es": hys_es,"hys_tp": hys_tp,"ptp_es": ptp_es,"ptp_tp": ptp_tp,"tp_peak": tp_peak,"tp_swing": tp_swing}
    data = pd.DataFrame.from_dict(data,orient='index').T
    data = data.dropna()
    data.to_excel('param009.xlsx')

def param_to_df(e_aw, e_es, e_tp, pow_aw, pow_es, pow_tp, e_hys_aw, e_hys_es, e_hys_tp, hys_aw, hys_es, hys_tp, ptp_es, ptp_tp, tp_peak, tp_swing):
    data = {"e_aw": e_aw, "e_es": e_es,"e_tp": e_tp,"pow_aw": pow_aw,"pow_es": pow_es,"pow_tp": pow_tp,"e_hys_aw": e_hys_aw, "e_hys_es": e_hys_es, "e_hys_tp": e_hys_tp,  "hys_aw": hys_aw,"hys_es": hys_es,"hys_tp": hys_tp,"ptp_es": ptp_es,"ptp_tp": ptp_tp,"tp_peak": tp_peak,"tp_swing": tp_swing}
    data = pd.DataFrame.from_dict(data,orient='index').T
    data = data.dropna()
    return data

