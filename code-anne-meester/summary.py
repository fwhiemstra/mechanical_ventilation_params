"""
Summary
- generates summary table containing:
  Patient ID, Pressure Type,
  Respiratory Rate, Tidal Volume, PEEP,
  Work of breathing, transpulmonary work, airway work
  Oesophageal hysteresis area, transpulmonary hysteresis area
  Oesophageal pressure-time product


Author: Sanne van Deelen
Date: February 2021

Modified by Bart Keulen
Date: October 2021

Modified by Anne Meester
Date: February 2022
"""
from tkinter import *

def summary(patient_id, pressure_type, rr_, mean_tidal_volume, mean_peep,
            mech_power, wob_tp_mean, wob_es_mean, aw_loop_power, tp_loop_power, ptp_es_mean,
            ptp_tp_mean, tp_peak_mean, tp_swing_mean):

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

    if pressure_type == 1:
        p_type = 'Airway pressure'

        lst = [('Patient ID', patient_id, 'Unit'),
                ('Pressure Type', p_type, ''),
                ('Respiratory Rate', rr_, '/min'),
                ('Tidal Volume', mean_tidal_volume, 'mL'),
                ('PEEP', mean_peep, 'cmH2O'),
                ('Mechanical Power', mech_power, 'J/min')]

    elif pressure_type == 2:
        p_type = 'Transpulmonary + airway pressure'

        lst = [('Parameter', 'Value', 'Unit'),
                ('Patient ID', patient_id, ''),
                ('Pressure Type', p_type, ''),
                ('Respiratory Rate', rr_, '/min'),
                ('Tidal Volume', mean_tidal_volume, 'mL'),
                ('PEEP', mean_peep, 'cmH2O'),
                ('Airway power', mech_power, 'J/min'),
                ('Airway Hysteresis Area', aw_loop_power, 'J/min'),
                ('Esophageal Pressure-Time Product', ptp_es_mean, 'cmH20*s/min'),
                ('Esophageal power of Breathing', wob_es_mean, 'J/min'),
                ('Transpulmonary Pressure-Time Product', ptp_tp_mean, 'cmH20*s/min'),
                ('Transpulmonary power', wob_tp_mean, 'J/min'),
                ('Transpulmonary Hysteresis Area', tp_loop_power, 'J/min'),
                ('Transpulmonary Peak Pressure', tp_peak_mean, 'cmH2O'),
                ('Transpulmonary Swing', tp_swing_mean, 'cmH2O')]

    # find total number of rows and columns in list
    total_rows = len(lst)
    total_columns = len(lst[0])

    # create root window
    root = Tk()
    table = Table(root)
    root.mainloop()
