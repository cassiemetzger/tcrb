import numpy as np 
import matplotlib.pyplot as plt
import astropy 
from astropy.io import fits
from astropy.table import Table
import pandas as pd
import math

def julian_to_gregorian(JDN):
    """
    Convert Julian Day Number (JDN) to a Gregorian date.
    """
    J = JDN + 0.5
    j = int(J)
    f = J - j
    g = int((j - 1867216.25) / 36524.25)
    g = j + 1 + g - int(g / 4)
    h = g + 1524
    i = int((h - 122.1) / 365.25)
    k = int(365.25 * i)
    l = int((h - k) / 30.6001)
    
    day = h - k - int(30.6001 * l) + f
    if l < 14:
        month = l - 1
    else:
        month = l - 13
    if month > 2:
        year = i - 4716
    else:
        year = i - 4715
    
    return int(year), int(month), int(day)

def editing(data): 
    for i in range(len(data['Uncertainty'])): 
        if(data['Uncertainty'][i] == '0,01'): 
            data['Uncertainty'][i] = 0.01
    for i in range(len(data['Uncertainty'])): 
        if(data['Uncertainty'][i] == '0,03'): 
            data['Uncertainty'][i] = 0.03
    V_mag = []
    V_JD = []
    V_uncert = []
    for i in range(len(data)): 
        if(data['Validation Flag'][i] == 'V' or data['Validation Flag'][i] == 'Z'):
            if(data['Band'][i] == 'V'): 
                V_mag.append(data['Magnitude'][i])
                V_JD.append(float(data['JD'][i]))
                V_uncert.append(float(data['Uncertainty'][i]))
    return V_mag, V_JD, V_uncert

def filted_out_upper_limits(V_mag, V_JD, V_uncert):
    i_list = []
    filtered_V_mag = []
    filtered_V_JD = []
    filtered_V_uncert = []
    for i in range(len(V_mag)):
        if(isinstance(V_mag[i], str)  == False or V_mag[i].startswith('<') == False):
            V_mag[i] = float(V_mag[i]) 
            filtered_V_mag.append(V_mag[i])
            filtered_V_JD.append(V_JD[i])
            filtered_V_uncert.append(V_uncert[i])
    return filtered_V_mag, filtered_V_JD, filtered_V_uncert
def dates(filtered_V_JD): 
    max = julian_to_gregorian(np.max(filtered_V_JD))
    title = '0' +str(max[1])+ str(max[2]) + str(max[0])
    max = str(max[1]) + '/' + str(max[2]) + '/' + str(max[0])
    min = julian_to_gregorian(np.min(filtered_V_JD))
    min = str(min[1]) + '/' + str(min[2]) + '/' + str(min[0])
    return min, max, title
def plt_lc(filtered_V_JD, filtered_V_mag, filtered_V_uncert, min, max, title): 
    plt.errorbar(filtered_V_JD, filtered_V_mag, yerr = filtered_V_uncert, fmt = '.', color = 'black')
    plt.xlabel('JD')
    plt.ylabel('Magnitude')
    plt.title(f'T CrB Johnson V Band Mag ({min}-{max})')
    plt.savefig(f'./plots/{title}.png')


file = input("Enter the file name: ")
data = pd.read_csv(file, delimiter = ',')
V_mag, V_JD, V_uncert = editing(data)
filtered_V_mag, filtered_V_JD, filtered_V_uncert = filted_out_upper_limits(V_mag, V_JD, V_uncert)
min, max, title = dates(filtered_V_JD)
plt_lc(filtered_V_JD, filtered_V_mag, filtered_V_uncert, min, max, title)