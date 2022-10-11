"""Script to calculate differences between hamilton breath number data and the inspiration detection script based on flow 

Autor: Joris Behr
Date: October 2022

"""
import numpy as np
import statistics as st
from constants import ADJ_HAM

def ham_vs_script(start_insp,start_insp_ham,flow):
    try:
        if len(start_insp_ham) > len(start_insp):
            start_insp_ham = np.delete(start_insp_ham, -1)
            # print(len(start_insp_ham))
        diff_index = start_insp_ham-start_insp
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

    #Determining start flow values of script and hamilton
    flow_insp_script = flow[start_insp]
    flow_insp_ham = flow[start_insp_ham]

    #Calculating and printing mean and stdev
    print(f'script mean inspiratory start  flow is {st.mean(flow_insp_script)} and std is {st.stdev(flow_insp_script)}')
    print(f'hamilton mean inpiratory start flow is {st.mean(flow_insp_ham)} and std is {st.stdev(flow_insp_ham)}')
