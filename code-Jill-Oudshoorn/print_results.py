"""
Summary
- generates cough summary table containing cough parameters
"""
from tkinter import *

def print_results(patient_id, cough_time_total, cough_time_percentage, number_coughs, mean_cough_power, mean_cough_amplitude, mean_cough_length, mean_cough_inbetweentime, mean_cough_peak_flow,max_cough_peak_flow,  percentage_hard_coughs ):

    class Table:
        """
        Create table
        """
        def __init__(self, root):
            # code for creating table
            for i in range(total_rows):
                for j in range(total_columns):
                    if i == 0 and j == len(lst[0])-1:
                        self.e = Entry(root, width=15, fg='#003c7d',
                                    font=('Arial', 12, 'bold'))
                    elif i == 0:
                        self.e = Entry(root, width=35, fg='#003c7d',
                                    font=('Arial', 12, 'bold'))
                    elif j == len(lst[0])-1:
                        self.e = Entry(root, width=15, fg='#003c7d',
                                    font=('Arial', 12))
                    else:
                        self.e = Entry(root, width=35, fg='#003c7d',
                                    font=('Arial', 12))
                    self.e.grid(row=i, column=j)
                    self.e.insert(END, lst[i][j])


    lst = [('Parameter', 'Value', 'Unit'),
            ('Patient ID', patient_id, ''),
            ('total cough time', cough_time_total, 'seconds'),
            ('percentage coughing', cough_time_percentage, ''),
            ('number of coughs', number_coughs, ''),
            ('mean cough power', mean_cough_power, 'cmH2O'),
            ('mean cough amplitude', mean_cough_amplitude, 'cmH2O'),
            ('mean_cough_length', mean_cough_length, 'seconds'),
            ('mean time inbetween coughs', mean_cough_inbetweentime, 'seconds'),
            ('mean cough peak flow', mean_cough_peak_flow, 'ml/s' ),
            ('max cough peak flow', max_cough_peak_flow, 'ml/s'),
            ('percentage coughs > 60L/min', percentage_hard_coughs, '')]

    # find total number of rows and columns in list
    total_rows = len(lst)
    total_columns = len(lst[0])

    # create root window
    root = Tk()
    table = Table(root)
    root.mainloop()