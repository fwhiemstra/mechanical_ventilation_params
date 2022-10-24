"""
Calculates the dynamic energy per breath and the power per minute

Author: Anne Meester
Date: February 2022

"""
import numpy as np
from numpy import NaN, mean, nan
from constants import CONV_FACTOR
from intersect import intersection


def pv_energy_calculator(start, end, pressure, volume, plot_name, ax):
    """
    Returns pv_e_breath, mean_pv_e_breath, pv_p_breath, mean_pv_p_breath
    """

    pv_insp_breath = []
    pv_exp_breath = []
    pv_e_breath = []
    pvenergyerror =0


    # For all breaths determine the pressures and volumes during inspiration and expiration.
    for start_insp, end_insp, end_exp, start_exp in zip(start[:-1], end[:-1], start[1:], end[:-1]):
        try:
            if end_insp > start_insp and end_exp > start_exp:
                vol_insp_org = volume[start_insp:(end_insp+1)]                  # Volume values of each inspiration
                pres_insp_org = pressure[start_insp:(end_insp+1)]               # Pressure values of each inspiration
                vol_exp_org = volume[start_exp:end_exp]                         # Volume values of each expiration
                pres_exp_org = pressure[start_exp:end_exp]                      # Pressure values of each expiration

                # Delete negative volume values due to calibration
                if min(vol_insp_org) < 0:
                    ind_insp = next(x[0] for x in enumerate(vol_insp_org) if x[1] >= 0)
                    vol_insp = vol_insp_org[ind_insp:len(vol_insp_org)]
                    pres_insp = pres_insp_org[ind_insp:len(pres_insp_org)]
                else:
                    ind_insp = np.argmin(vol_insp_org)
                    vol_insp = vol_insp_org[ind_insp:len(vol_insp_org)]
                    pres_insp = pres_insp_org[ind_insp:len(pres_insp_org)]

                if min(vol_exp_org) < 0:
                    ind_exp = next(x[0] for x in enumerate(vol_exp_org) if x[1] <= 0)
                    vol_exp = vol_exp_org[0:ind_exp]
                    pres_exp = pres_exp_org[0:ind_exp]
                else:
                    ind_exp = np.argmin(vol_exp_org)
                    vol_exp = vol_exp_org[0:ind_exp]
                    pres_exp = pres_exp_org[0:ind_exp]

                # Plot the PV loops:
                ax.plot(pres_insp, vol_insp, color = 'lawngreen')
                ax.plot(pres_exp, vol_exp, color = 'orange')
                ax.set_title(plot_name)
                ax.set(xlabel='Pressure [cmH2O]', ylabel='Volume [mL]')

                # Negative pressure values give erroneous results when integrating. Both the inspiratory
                # and expiratory leg (entire hysteresis loop) should be shifted to positive.
                if not pres_exp or not pres_insp:               # See if the list is empty
                    pres_insp = [nan]
                    vol_insp = [nan]
                    pres_exp = [nan]
                    vol_exp = [nan]
                else:
                    if min(pres_exp) < 0 and min(pres_insp) < 0:
                        if min(pres_exp) <= min(pres_insp):
                            min_pres = min(pres_exp)
                            pres_insp = [i + abs(min_pres) for i in pres_insp]
                            pres_exp = [i + abs(min_pres) for i in pres_exp]
                        else:
                            min_pres = min(pres_insp)
                            pres_insp = [i + abs(min_pres) for i in pres_insp]
                            pres_exp = [i + abs(min_pres) for i in pres_exp]
                    elif min(pres_exp) < 0 or min(pres_insp) < 0:
                        if min(pres_exp) < min(pres_insp):
                            min_pres = min(pres_exp)
                            pres_insp = [i + abs(min_pres) for i in pres_insp]
                            pres_exp = [i + abs(min_pres) for i in pres_exp]
                        else:
                            min_pres = min(pres_insp)
                            pres_insp = [i + abs(min_pres) for i in pres_insp]
                            pres_exp = [i + abs(min_pres) for i in pres_exp]
       
      
                # Remove the small loop: the HA in spontaneous breathing can consist of two loops.
                # The small loop should not be included in the calculation
                # First, the intersection between the inspiratory leg and the expiratory leg must be determined
                intersect_pres, intersect_vol = intersection(pres_insp, vol_insp, pres_exp, vol_exp)

                # If the intersection is between volume 0-150 mL, this becomes the minimum point of the HA
                vol_150 = []
                pres_150 = []
                ind_150 = []
                i = 0
                if len(intersect_vol) > 1:
                    while i < len(intersect_vol):
                        try:
                            if intersect_vol[i] > 0 and intersect_vol[i] < 150:
                                vol_150.append(intersect_vol[i])
                                pres_150.append(intersect_pres[i])
                                ind_150.append(i)
                                i += 1
                            else:
                                i += 1
                        except:
                            pvenergyerror +=1
                            pv_e_breath.append(NaN)
                            continue
            
                if len(vol_150) > 0:
                    try:
                        intrs_vol = max(vol_150)        
                        ind_insp = next(x[0] for x in enumerate(vol_insp) if x[1] >= intrs_vol)
                        ind_exp = next(x[0] for x in enumerate(vol_exp) if x[1] <= intrs_vol)
                        pres_insp = pres_insp[ind_insp:len(pres_insp)]
                        vol_insp = vol_insp[ind_insp:len(vol_insp)]
                        pres_exp = pres_exp[0:ind_exp]
                        vol_exp = vol_exp[0:ind_exp]
                    except:
                        pvenergyerror +=1
                        pv_e_breath.append(NaN)

                # The direction of expiration is right to left, this must be reversed to
                # obtain a positive value when integrating.
                pres_exp_new = pres_exp[::-1]
                vol_exp_new = vol_exp[::-1]

                # Integrate to calculate energy per breath and convert from [mL*cmH2O] to [J]
                # - First: integrate over the inspiratory and expiratory leg separately
                # - Second: the difference between these areas is the Hysteresis Area
                integration_insp = CONV_FACTOR * np.trapz(pres_insp, vol_insp)
                integration_exp = CONV_FACTOR * np.trapz(pres_exp_new, vol_exp_new)
                integration = abs(integration_insp-integration_exp)
                pv_insp_breath.append(integration_insp)
                pv_exp_breath.append(integration_exp)
                pv_e_breath.append(integration)
        except:
            pvenergyerror +=1
            pv_e_breath.append(NaN)

    # Remove empty values in list
    # pv_e_breath = [i for i in pv_e_breath if i != 0]

    # Calculate mean energy
    mean_pv_e_breath = round(mean(pv_e_breath), 2)
    print("number of errors in pv energy calculation is {}". format(pvenergyerror))

    return pv_e_breath, mean_pv_e_breath
