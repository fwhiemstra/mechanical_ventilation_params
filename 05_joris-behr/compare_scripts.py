"""Script to calculate differences between inspiration detection scripts

Autor: Joris Behr
Date: October 2022

"""

import numpy as np
import statistics as st


def ham_vs_script(start_insp,start_insp_2,end_insp, end_insp_2,flow,insp_detection,insp_comp):
    try:
        if len(start_insp_2) > len(start_insp):
            start_insp_2 = np.delete(start_insp_2, -1)
            
        diff_index = start_insp_2-start_insp
        mean_diff_index =st.mean(diff_index)
        diff_index_mean_sub50 = st.mean(diff_index[diff_index <45])
        diff_index_median = st.median(diff_index)
        print(f'mean difference is {mean_diff_index}')
        print(f'adjusted mean is {diff_index_mean_sub50}')
        print(f'median difference {diff_index_median}')
    except: 
        print('Difference could not be determined due to difference in length')

    #Transforming flow to an array for calculation purposes
    flow = np.array(flow)

    #Determining start flow values 
    flow_insp_1 = flow[start_insp]
    flow_insp_2 = flow[start_insp_2]
    flow_exp_1 = flow[end_insp]
    flow_exp_2 = flow[end_insp_2]


    #Calculating and printing mean and stdev
    print(f'{insp_detection} no of insp = {len(start_insp)}  mean inspiratory start flow is {st.mean(flow_insp_1)} +/- {st.stdev(flow_insp_1)}, mean expiratory start flow is {st.mean(flow_exp_1)} +/- {st.stdev(flow_exp_1)}')
    print(f'{insp_comp} no of insp {len(start_insp_2)}, mean inpiratory start flow is {st.mean(flow_insp_2)} +/- {st.stdev(flow_insp_2)},mean expiratory start flow is {st.mean(flow_exp_2)} +/- {st.stdev(flow_exp_2)}')
