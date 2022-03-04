"""
Calculates the mean PEEP, the energy per minute, the mechanical power,
the energy per breath and the mean energy per breath.

Author: Sanne van Deelen
Date: February 2021

Modified by Bart Keulen
Date: October 2021
"""

import numpy as np
from numpy import mean
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from constants import CONV_FACTOR, FS

rr_ = rr
pressure = p_air_trim
dynamic = 0

# Only use the ends that come after a start
for index, elem in enumerate(end_insp):
    if end_insp[index] <= start_insp[0]:
        end_insp.remove(end_insp[index])

# Check if lengths are the same
if len(start_insp) > len(end_insp):
    start_insp.remove(start_insp[-1])

e_breath = []
e_breath_pv = []
e_breath_vp = []

for start, end, peep_ in zip(start_insp, end_insp, peep):
    if end > start:
        vol_interval = volume_trim[start:end]  # Volume values of each breath
        pres_interval = pressure[start:end]  # Pressure values of each breath

        # Subtract PEEP values per breath of the pressure values
        # in case of dynamic energy calculation
        if dynamic == 1:
            pres_interval = [i-peep_ for i in pres_interval]
        else:
            pass

        # Integrate to calculate energy per breath and convert from [mL*cmH2O] to [J]
        integration_pv = CONV_FACTOR * np.trapz(pres_interval, vol_interval)
        integration_vp = CONV_FACTOR * np.trapz(vol_interval, pres_interval)

        e_breath_pv.append(integration_pv)
        e_breath_vp.append(integration_vp)

print('e_breath_pv (old):', np.mean(e_breath_pv), '\ne_breath_vp (new):', np.mean(e_breath_vp))

plt.close('all')
fig, axs = plt.subplots(2, 1)
axs[0].xaxis.set_tick_params(which='both', labelbottom=True)
axs[0].xaxis.set_tick_params(which='both', labelbottom=True)

axs[0].plot(pres_interval, vol_interval)
#axs[0].set_title('np.trapz(vol_interval, pres_interval)')
axs[0].set_xlabel('pressure')
axs[0].set_ylabel('volume')

axs[1].plot(vol_interval, pres_interval)
#axs[1].set_title('np.trapz(pres_interval, vol_interval)')
axs[1].set_xlabel('volume')
axs[1].set_ylabel('pressure')
plt.tight_layout()
plt.show()

#%%
# Calculate power per breath [J/min]
p_breath = []
for i in range(len(start_insp)-1):
    dur_min = (start_insp[i+1]-start_insp[i])/FS/60   # Duration of breath
    power = e_breath[i] / dur_min        # Power of breath
    p_breath.append(power)

# Calculate mean energy and power
mean_e_breath = round(mean(e_breath),2)
mean_p_breath = round(mean(p_breath),2)

#%%
x = np.linspace(0, 10000)
y = np.sin(x)
plt.plot(x,y)
plt.show()

int_1 = np.trapz(x,y)
print(int_1)
int_2 = np.trapz(y,x)
print(int_2)

