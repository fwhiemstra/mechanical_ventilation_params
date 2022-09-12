from sklearn.metrics import classification_report, confusion_matrix

import pandas as pd
import numpy as np
"""
Scores the artefact detection algorithm on performance for recognizing artefacts and classifying them

"""
def artefact_scoring(artefact_scoring, artefact_timestamp, artefact_timestamp_compressed):
    
    artefact_true = artefact_timestamp
    print(len(artefact_true))
    artefact_true = artefact_true.replace(np.nan,0)
    for i in range(0 , len(artefact_true)):
        if artefact_true.iloc[i] == 0:
            artefact_true.iloc[i] = "no artefact"
        else:
            artefact_true.iloc[i] = 'artefact'

    cough_true = artefact_timestamp
    cough_true = cough_true.replace(np.nan,0)
   
    for i in range(0 , len(cough_true)):
        if cough_true.iloc[i] == 'cough':
            cough_true.iloc[i] = 'cough'
        else:
            cough_true.iloc[i] = 'no cough'

    cough_true_2 = artefact_timestamp
    cough_true_2 = cough_true_2.replace(np.nan,0)


    for i in range(0 , len(cough_true_2)):
        if cough_true_2.iloc[i] == 'cough':
            cough_true_2.iloc[i] = True
        else:
            cough_true_2.iloc[i] = False
    
    def first_true2(a):
     a = np.concatenate([[False], a, [False]])
     coughcount = np.argmin(a[np.argmax(a):])
     return coughcount
    
    coughcount = first_true2(cough_true_2)
    print(coughcount)

    tn, fp, fn, tp = confusion_matrix(cough_true, artefact_scoring).ravel()
    print(tn, fp, fn, tp)
    print(classification_report(cough_true, artefact_scoring, labels = ['cough', 'no cough']))
