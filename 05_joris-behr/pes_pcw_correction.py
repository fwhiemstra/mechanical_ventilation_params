"""Script to adjust pes to obtain pmus, according to de vries et al. 2018
Author: Joris Behr
Date: october 2022

"""

import numpy as np

def pes_pcw_correction(pes):
    C_kg_VC = 0.67
    C_VC_Ccw = 0.04
    weight = np.random.normal(80,10)

    pcw = weight*C_kg_VC*C_VC_Ccw
    pes = pes - pcw
    return pes, pcw