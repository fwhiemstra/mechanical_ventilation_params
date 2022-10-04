"""Script to calculate differences between hamilton breath number data and the inspiration detection script 

Autor: Joris Behr
Date: October 2022

"""



import numpy as np
from requests import delete


def ham_vs_script(start_insp,start_insp_ham):
    print(len(start_insp_ham))
    if len(start_insp_ham) > len(start_insp):
        start_insp_ham = np.delete(start_insp_ham, -1)
        print(len(start_insp_ham))
    diff_index = start_insp_ham-start_insp
    print(diff_index)