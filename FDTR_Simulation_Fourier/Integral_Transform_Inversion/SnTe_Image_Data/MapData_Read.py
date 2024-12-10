# -*- coding: utf-8 -*-
"""
Created on Fri May 31 10:33:15 2024

@author: eleon
"""

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from matplotlib.markers import MarkerStyle
import pylab
from pathlib import Path
import sys

sns.set_style('whitegrid', {'axes.edgecolor':'black'})
sns.set_context('notebook') # default 'notebook', or 'paper', 'talk', 'poster'


############################ FOR DATA RETRIEVAL ############################

# input = path for data retrieval (the outer folder which contains inner folders for each measured frequency)
# output = path to save csv files and png plots
input_path = Path("")
output_path = Path("")

# Select the data-containg folder
Folders = ['1MHz']
#Folders = ['1MHz', '2MHz', '4MHz', '10MHz', '20MHz']


########################### EXPERIMENT PARAMETERS ###########################

# Scan Parameters
DualScan = 1;  # Put 1 if you selected Dual scan in the measurement, 0 if you selected Line scan
               # Typically we do Dual scans
Yscan = 1; # Put 1 if you selected Y scan in the measurement
           # Typically, we do Y scans

Xrange = 120 #[um]
Yrange = 120

# Extract Xnum and Ynum dimension from one data set,
# then check that you input Xrange and Yrange correctly
check = Folders[0]
extract_dimensions = np.loadtxt(input_path / check / f'Signal{check}.txt', skiprows=0) 
Xnum = np.shape(extract_dimensions)[0]//2 - 1
Ynum = np.shape(extract_dimensions)[1] - 1

if (Xnum - Ynum) * (Xrange - Yrange) < 0:
    sys.exit('check Xrange and Yrange')

# XY GRID
Xstep = Xrange/Xnum 
Ystep = Yrange/Ynum 
x = np.outer(np.linspace(0, Xrange, Xnum+1), np.ones(Ynum+1))
y = np.outer(np.ones(Xnum+1), np.linspace(0, Yrange, Ynum+1))

# If Yscan, then flip x and y
if Yscan == 1:
    temp = x
    x = y
    y = temp


############################## ARRAY INITIALIZATION ############################

Ref_X = np.zeros(len(Folders))
Ref_Y = np.zeros(len(Folders))
Ref_Amp = np.zeros(len(Folders))
Ref_Phase = np.zeros(len(Folders))
Noise_X = np.zeros(len(Folders))
Noise_Y = np.zeros(len(Folders))
Noise_Amp = np.zeros(len(Folders))
Noise_Phase = np.zeros(len(Folders))
RefCl_X = np.zeros(len(Folders))
RefCl_Y = np.zeros(len(Folders))
RefCl_Amp = np.zeros(len(Folders))
RefCl_Phase = np.zeros(len(Folders))

SampleCl_X = np.zeros((Xnum+1, Ynum+1,len(Folders)))
SampleCl_Y = np.zeros((Xnum+1, Ynum+1,len(Folders)))
SampleCl_Amp = np.zeros((Xnum+1, Ynum+1,len(Folders)))
SampleCl_Phase = np.zeros((Xnum+1, Ynum+1,len(Folders)))
SampleCl_Phase = np.zeros((Xnum+1, Ynum+1,len(Folders)))
Phase = np.zeros((Xnum+1, Ynum+1,len(Folders)))


#################### CALCULATE PHASE AND AMPLITUDE FROM X AND Y ##################

for i in range(len(Folders)):
    
    name = Folders[i]
    
    # read data: X, Y, ref X, ref Y, noise X, noise Y
    Data = np.loadtxt(input_path / name / f'Signal{name}.txt', skiprows=0) # import X and Y sample signal data in V
    Correction = pd.read_excel(input_path / name / f'Correction{name}.xlsx', skiprows=0) # import correction coefficients (i.e., Noise and Reference X and Y)
    
    # get correction coefficients
    Ref_X[i] = Correction.loc[2,'Reference X [mV]'] # [mV]
    Ref_Y[i] = Correction.loc[2,'Reference Y [mV]'] # [mV]
    Noise_X[i] = Correction.loc[2,'Noise X [mV]'] # [mV]
    Noise_Y[i] = Correction.loc[2,'Noise Y [mV]'] # [mV]
    
    # verify reference and noise amplitude and phase 
    Ref_Amp[i] = np.sqrt(Ref_X[i]**2+Ref_Y[i]**2)
    Ref_Phase[i] = np.arctan(Ref_Y[i]/Ref_X[i])*180/np.pi
    print(f"Signal {name}: Reference Amplitude {Ref_Amp[i]:.3f} mV, reference phase {Ref_Phase[i]:.3f} deg.")
    
    Noise_Amp[i] = np.sqrt(Noise_X[i]**2+Noise_Y[i]**2)
    Noise_Phase[i] = np.arctan(Noise_Y[i]/Noise_X[i])*180/np.pi+180
    print(f"Signal {name}: Noise Amplitude {Noise_Amp[i]:.3f} mV, Noise phase {Noise_Phase[i]:.3f} deg.")
    
    # Remove noise from sample and reference signals
    # Potential location for bugs if switching xscan/yscan
    SampleCl_X[:,:,i] = Data[:Xnum+1,:] - Noise_X[i]/1e3 # [V] 
    SampleCl_Y[:,:,i] = Data[Xnum+1:,:] - Noise_Y[i]/1e3 # [V]
    
    RefCl_X[i] = Ref_X[i]/1e3 - Noise_X[i]/1e3 # [V]
    RefCl_Y [i]= Ref_Y[i]/1e3 - Noise_Y[i]/1e3 # [V]

    # Calculate "cleaned" amplitude and phase for sample
    SampleCl_Amp[:,:,i] = np.sqrt(SampleCl_X[:,:,i]**2+SampleCl_Y[:,:,i]**2)
    SampleCl_Phase[:,:,i] = np.arctan(SampleCl_Y[:,:,i]/SampleCl_X[:,:,i])*180/np.pi

    # Calculate "cleaned" amplitude and phase for reference
    RefCl_Amp[i] = np.sqrt(RefCl_X[i]**2+RefCl_Y[i]**2)
    RefCl_Phase[i] = np.arctan(RefCl_Y[i]/RefCl_X[i])*180/np.pi
    print(f"Signal {name}: Cleaned Reference Amplitude {RefCl_Amp[i]:.3f} V, cleaned reference phase {RefCl_Phase[i]:.3f} deg.")

    # Calculate the Phase
    Phase[:,:,i] = SampleCl_Phase[:,:,i] - RefCl_Phase[i]
    
    # Set the Phase in the range: -90 deg to 0 deg
    sample_index = 0
    if Phase[sample_index,sample_index,i] < -90:
        Phase[:,:,i] += 180
    elif Phase[sample_index,sample_index,i] > 0:
        Phase[:,:,i] += -180
    
    # Check that sample_index is characteristic of your map (e.g. not a noise spike)
    if Phase[sample_index,sample_index,i] < -90 or Phase[sample_index,sample_index,i] > 0:
        sys.exit('Phase quadrant incorrect. Try a different <sample_index>.')
    
    # Adjust Data Display according to scanning conditions
    if DualScan == 1:
        if Yscan == 1:
            for j in range(1, Phase.shape[0], 2):
                Phase[j, :, i] = Phase[j, ::-1, i]
                SampleCl_Amp[j, :, i] = SampleCl_Amp[j, ::-1, i]
        else:
            for j in range(1, Phase.shape[1], 2):
                Phase[:, j, i] = Phase[::-1, j, i]
                SampleCl_Amp[j, :, i] = SampleCl_Amp[j, ::-1, i]


################################### PLOTTING ######################################

ts = 22 # text size

for i in range(len(Folders)):
    
    name = Folders[i]
    
    fig, (ax, ax1) = plt.subplots(1, 2, figsize=(18,7))
    
    # Phase Plot
    ax.set_xlabel('x ($\mu$m)', fontsize=ts) 
    ax.set_ylabel('y ($\mu$m)', fontsize=ts) 
    ax.tick_params(axis="both", labelsize=ts-2)
    ax.grid(False)
    c = ax.pcolor(x, y, Phase[::-1,::-1,i], cmap='jet', vmin=-27, vmax=-25) # Phase[::-1,::-1,i] for showing the starting point on top right corner

    cbar = plt.colorbar(c)
    cbar.set_label('Phase [°]',  fontsize=ts)
    cbar.ax.tick_params(labelsize=ts-2)
    ax.xaxis.tick_bottom()
    ax.yaxis.tick_left()
    
    # Amplitude Plot
    ax1.set_xlabel('x ($\mu$m)', fontsize=ts) 
    ax1.set_ylabel('y ($\mu$m)', fontsize=ts) 
    ax1.tick_params(axis="both", labelsize=ts-2)
    ax1.grid(False)

    d = ax1.pcolor(x, y, SampleCl_Amp[::-1,::-1,i]*1e3, cmap='jet', vmin=9, vmax=12)
    cbar = plt.colorbar(d)
    cbar.set_label('Amplitude [mV]',  fontsize=ts)
    cbar.ax.tick_params(labelsize=ts-2)
    ax1.xaxis.tick_bottom()
    ax1.yaxis.tick_left()
    
    # Save figure
    fig.tight_layout()
    name_of_figure = f'Phase_Amplitude_{name}.png'
    plt.savefig(output_path / name_of_figure, dpi=1000, bbox_inches='tight')


################################### SAVE PHASE DATA ######################################

for i in range(len(Folders)):
    name = Folders[i]
    np.savetxt(output_path / f'Phase_{name}.txt', Phase[:, :, i], fmt='%.6f')