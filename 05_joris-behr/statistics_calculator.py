"""
Statistics
- standard deviations
- standard errors

Author: Sanne van Deelen
Date: February 2021

Modified by Bart Keulen
Date: October 2021

Modified by Anne Meester
Date: February 2022
"""
import math
from turtle import shape
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from constants import PRESSURE_TYPE

def sd_se_statistics(p_breath, aw_p_breath, es_p_breath, tp_p_breath,
               wob_es_breath, wob_tp_breath, ptp_es, ptp_tp,
               tp_peak, tp_swing, pressure_type):
    """
    Returns
    """
    # Power per breath
    sd_p_breath = round(np.std(p_breath), 2)
    se_p_breath = round(sd_p_breath / math.sqrt(len(p_breath)), 2)

    # Esophageal loop power per breath
    sd_es_p_breath = round(np.std(es_p_breath), 2)
    se_es_p_breath = round(sd_es_p_breath / math.sqrt(len(es_p_breath)), 2)

    # Airway loop power per breath
    sd_aw_p_breath = round(np.std(aw_p_breath), 2)
    se_aw_p_breath = round(sd_aw_p_breath / math.sqrt(len(aw_p_breath)), 2)

    if pressure_type == PRESSURE_TYPE.TRANSPULMONARY:
        # Transpulmonary loop power per breath
        sd_tp_p_breath = round(np.std(tp_p_breath), 2)
        se_tp_p_breath = round(sd_tp_p_breath / math.sqrt(len(tp_p_breath)), 2)

        # Esophageal work of breathing per breath
        sd_wob_es_breath = round(np.std(wob_es_breath), 2)
        se_wob_es_breath = round(sd_wob_es_breath / math.sqrt(len(wob_es_breath)), 2)

        # Transpulmonary work of breathing per breath
        sd_wob_tp_breath = round(np.std(wob_tp_breath), 2)
        se_wob_tp_breath = round(sd_wob_tp_breath / math.sqrt(len(wob_tp_breath)), 2)

        # Esophageal PTP per breath
        sd_ptp_es = round(np.std(ptp_es), 2)
        se_ptp_es = round(sd_ptp_es / math.sqrt(len(ptp_es)), 2)

        # Transpulmonary PTP per breath
        sd_ptp_tp = round(np.std(ptp_tp), 2)
        se_ptp_tp = round(sd_ptp_tp / math.sqrt(len(ptp_tp)), 2)

        # Transpulmonary peak
        sd_tp_peak = round(np.std(tp_peak), 2)
        se_tp_peak = round(sd_tp_peak / math.sqrt(len(tp_peak)), 2)

        # Transpulmonary swing
        sd_tp_swing = round(np.std(tp_swing), 2)
        se_tp_swing = round(sd_tp_swing / math.sqrt(len(tp_swing)), 2)

    elif pressure_type == PRESSURE_TYPE.AIRWAY:
        # Transpulmonary loop power per breath
        sd_tp_p_breath = '-'
        se_tp_p_breath = '-'

        # Transpulmonary work per breath
        sd_wob_tp_breath = '-'
        se_wob_tp_breath = '-'

        # Esophageal work of breathing per breath
        sd_wob_es_breath = '-'
        se_wob_es_breath = '-'

        # Esophageal PTP per breath
        sd_ptp_es ='-'
        se_ptp_es = '-'

        # Transpulmonary PTP per breath
        sd_ptp_tp = '-'
        se_ptp_tp = '-'

        # Transpulmonary peak
        sd_tp_peak = '-'
        se_tp_peak = '-'

        # Transpulmonary swing
        sd_tp_swing = '-'
        se_tp_swing = '-'

    # Combine standard deviations and errors in lists
    standard_deviations = [sd_p_breath, sd_es_p_breath, sd_aw_p_breath, sd_tp_p_breath,
                           sd_wob_tp_breath, sd_wob_es_breath, sd_ptp_es, sd_ptp_tp, sd_tp_peak, sd_tp_swing]
    standard_errors = [se_p_breath, se_es_p_breath, se_aw_p_breath, se_tp_p_breath,
                       se_wob_tp_breath, se_wob_es_breath, se_ptp_es, se_ptp_tp, se_tp_peak, se_tp_swing]

    return standard_deviations, standard_errors

def correlations(p_breath, aw_p_breath, es_p_breath, tp_p_breath,
               wob_es_breath, wob_tp_breath, ptp_es, ptp_tp,
               tp_peak, tp_swing):
    #creating dataframe from data.
    # Last values of TP peak and swing are not taken into account to ensure same length of data.
    data_dict = {'Power breath': p_breath, 'Hys aw': aw_p_breath, 'Hys aw':es_p_breath, 'Hys tp':tp_p_breath,
               'Power es':wob_es_breath, 'Power tp': wob_tp_breath, 'PTP es': ptp_es, 'PTP tp':ptp_tp,
               'tp peak':tp_peak[0:-1], 'tp swing': tp_swing[0:-1]}
    
    data = pd.DataFrame(data_dict)
    data = data.dropna()
    matrix = data.corr(method = 'pearson').round(2)
    mask = np.triu(np.ones_like(matrix, dtype=bool))

    plt.figure()
    sns.heatmap(matrix,annot = True, vmax = 1, vmin = 0, center = 0.5, cmap = 'vlag', mask=mask)
    plt.title("Heat map of correlations")
    #Saving the heatmap
    # plt.savefig('heatmap001.jpg')
    plt.tight_layout()
    plt.show()

    matrix = matrix.unstack()
    matrix = matrix[abs(matrix) >= 0.7]
    print(matrix)

  
    return matrix


def correlations_xlsx(input):
    """Function to analyze data from excel file
    Shows histrogram, bar plots and correlation heatmaps"""
    
    # Selecting columns that contain data
    data = pd.read_excel(input, usecols='B:N')
    
    # Filtering data based on measuring location
    
    data_aw = data[["e_aw", "pow_aw", "hys_aw"]]
    data_es = data[["e_es", "pow_es", "hys_es", "ptp_es"]]
    data_tp= data[["e_tp", "pow_tp", "hys_tp", "ptp_tp", "tp_peak", "tp_swing"]]
    
    ## Uncomment data below to create own filtered data
    # data_fil = data[["heading1", "heading2", "heading3"]]
    
    
    ## Creating correlation matrices, spearman is used since data is not normally distributed
    matrix_tot = data.corr(method = 'spearman').round(2)
    mask_tot = np.triu(np.ones_like(matrix_tot, dtype=bool))
    
    matrix_aw = data_aw.corr(method = 'spearman').round(2)
    mask_aw = np.triu(np.ones_like(matrix_aw, dtype=bool))

    matrix_es = data_es.corr(method = 'spearman').round(2)
    mask_es = np.triu(np.ones_like(matrix_es, dtype=bool))

    matrix_tp = data_tp.corr(method = 'spearman').round(2)
    mask_tp = np.triu(np.ones_like(matrix_tp, dtype=bool))

    ## Uncomment code below to create matrix of own filtered data
    # matrix_fil = data_fil.corr(method = 'spearman').round(2)
    # mask_fil = np.triu(np.ones_like(matrix_fil, dtype=bool)) 
    
    ## Filter values based on correlation value
    # matrix_tot_fil = matrix_tot.unstack()
    # matrix_tot_fil = matrix_tot_fil[abs(matrix_tot_fil) >= 0.7]
    # print(matrix_tot_fil)   


    ## Creating figures
    # pairplots
    pp_aw = sns.pairplot(data_aw)
    pp_aw.fig.suptitle("Scatterplot matrix of airway parameters")
    plt.tight_layout()
    plt.savefig('pairplot_aw.jpg')


    pp_es = sns.pairplot(data_es)
    pp_es.fig.suptitle("Scatterplot matrix of esophageal parameters")
    plt.tight_layout()
    plt.savefig('pairplot_es.jpg')

    pp_tp = sns.pairplot(data_tp)
    pp_tp.fig.suptitle("Scatterplot matrix of transpulmonal parameters")
    plt.tight_layout()
    plt.savefig('pairplot_tp.jpg')

    ## Uncomment lines below to plot own filtered data
    # pp_fil = sns.pairplot(data_fil)
    # pp_fil.fig.suptitle("Scatterplot matrix of filtered parameters")
    # plt.tight_layout()

    plt.show()

    # Correlation heatmaps
    # To show only half of the heat map, add mask = mask_{name of data}. ie for total: mask=mask_tot
    plt.figure()
    sns.heatmap(matrix_tot,annot = True, vmax = 1, vmin = -1, center = 0, cmap = 'vlag')
    plt.title("Heat map of correlations")
    plt.tight_layout()
    plt.savefig('heatmap_tot.jpg')

    plt.figure()
    sns.heatmap(matrix_aw,annot = True, vmax = 1, vmin = 0, center = 0.5, cmap = 'vlag')
    plt.title("Heat map of airway parameter correlations")
    plt.tight_layout()
    plt.savefig('heatmap_aw.jpg')

    plt.figure()
    sns.heatmap(matrix_es,annot = True, vmax = 1, vmin = 0, center = 0.5, cmap = 'vlag')
    plt.title("Heat map of esophageal parameter correlations")
    plt.tight_layout()
    plt.savefig('heatmap_es.jpg')

    plt.figure()
    sns.heatmap(matrix_tp,annot = True, vmax = 1, vmin = 0, center = 0.5, cmap = 'vlag')
    plt.title("Heat map of transpulmonal parameter correlations")
    plt.tight_layout()
    plt.savefig('heatmap_tp.jpg')

    ## Uncomment code below to create own filtered heatmap
    # plt.figure()
    # sns.heatmap(matrix_fil,annot = True, vmax = 1, vmin = 0, center = 0.5, cmap = 'vlag')
    # plt.title("Heat map of transpulmonal parameter correlations")
    # plt.tight_layout()

    plt.show()





if __name__ == '__main__':
    """Run excel code seperately from main.py by running "python statistics_calculator.py" 
    Make sure to select correct input data directory for the data"""
    input = r"C:\Users\joris\OneDrive\Documenten\Studie\TM jaar 2&3\Q1\data\params\param_tot.xlsx"
    correlations_xlsx(input)
