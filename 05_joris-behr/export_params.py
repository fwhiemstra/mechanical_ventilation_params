"""Script to export parameters to csv

Author: Joris Behr
Date: October 2022

"""
import pandas as pd

def export_params(e_aw, e_es, e_tp, pow_aw, pow_es, pow_tp, pow_dyn_aw, pow_dyn_es, pow_dyn_tp, ptp_es, ptp_tp, tp_peak, tp_swing):
    print(len(e_aw), len(e_es), len(e_tp), len(pow_aw), len(pow_es), len(pow_tp), len(pow_dyn_aw), len(pow_dyn_es), len(pow_dyn_tp), len(ptp_es), len(ptp_tp), len(tp_peak), len(tp_swing))
    data = {"e_aw": e_aw, "e_es": e_es,"e_tp": e_tp,"pow_aw": pow_aw,"pow_es": pow_es,"pow_tp": pow_tp,"pow_dyn_aw": pow_dyn_aw,"pow_dyn_es": pow_dyn_es,"pow_dyn_tp": pow_dyn_tp,"ptp_es": ptp_es,"ptp_tp": ptp_tp,"tp_peak": tp_peak,"tp_swing": tp_swing}
    data = pd.DataFrame.from_dict(data,orient='index').T
    data = data.dropna()
    data.to_excel('param009.xlsx')



