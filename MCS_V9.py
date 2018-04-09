#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Magliari Compensation System
This expands off of V8, by adding the string length from the nut to the tuner
and the saddle to the bridge pins. To test, run and comapre against FretComp 6.0 - 161007 OVERPRESS.pdf
which is Gary's calculation using the same parameters. Use the Eureqa overpress. It won't be an exact comaprison to 
Gary's, but it will be close. The difference is coming, I believe, from his choice of overpress, which
is some average of the Eureqa formulas
"""
import numpy as np
from load_string_data import load_string_set_data
from find_geometry import find_fret_radius
from find_geometry import find_fret_positions
from find_geometry import find_initial_nut_saddle
from find_geometry import find_stringL
from find_geometry import find_tension_length2
from find_geometry import find_unstressed_length2
from find_geometry import find_stressed_length_wraparound2
from find_geometry import find_fretboard_geometry
from find_geometry import update_fret_locations
from find_geometry import shift_updated_frets
from find_geometry import update_string_scaleGaryNew
from find_overpress import find_overpress
from find_overpress import update_overpress
from find_tension import find_fretted_string_tension
from find_tension import find_string_tension
from find_tuning import find_tuning
from plotting_routines import plot_delta
from plotting_routines import plot_tuning
from plotting_routines import plot_overpress

import matplotlib.pyplot as plt
from IPython import get_ipython

plt.close('all')
get_ipython().run_line_magic('matplotlib', 'qt')    

#********************************
#clears all variables
#from IPython import get_ipython
#get_ipython().magic('reset -sf')
#********************************

#constants
#********************************
g = 386.088557204286 #Gravitational Constant
#********************************

# MCS Input
#********************************
MCS_outfile = 'OutputFiles/EJ17_MCS_OPGoreFP.dat'
zero_fret = 3
even_fret = 16
niterations = 10 #For the MCS - Any positive integer here will invoke the MCS - Leave as "0" to NOT run the MCS

min_tune = -10.0 #Paramateres for plotting the tuning
max_tune = 10.0

zero_fret = zero_fret - 1 #adjust for python index system - starts at zero
even_fret = even_fret - 1

#********************************
# TEST
# To test against Gary, use string_set = 4, OP.method = Constant,
# OP.constant = 0.002, and compare Lfret_ToCut, and gary_nut, gary_saddle
#********************************

#********************************
# Instrument/String set input
#********************************
string_set = 11
# 1 = Mandolin J74 
# 2 = Mandolin J74 Detuned
# 3 = Steel String EJ16
# 4 = Steel String EJ17
# 5 = Steel String EJ16 Detuned
# 6 = Steel String EJ17 Detuned
# 7 = Classical EJ45
# 8 = Classical EJ46
# 9 = Classical EJ45 Detuned
# 10 = Classical EJ46 Detuned
#********************************
(nfrets,nstrings,Lscale,FFR,actionfile,stringprops,over_press_file,PFfile,freq_file,Pd,H,W) = load_string_set_data(string_set)
(R) = find_fret_radius(H,W)

# Guitar Setup
nut_width = 0.25 #physical width of nut
saddle_width = 0.25 #physical width of saddle

# string_length_BEFORE_Nut
A = np.zeros(nstrings)
if nstrings == 6:
    A[0] = 1.75
    A[1] = 3.5
    A[2] = 5.15
    A[3] = 5.15
    A[4] = 3.5
    A[5] = 1.75
if nstrings == 4:
    A[0] = 1.75
    A[1] = 3.5
    A[2] = 5.15
    A[3] = 5.15
if nstrings == 3:
    A[0] = 1.75
    A[1] = 3.5
    A[2] = 5.15
    
# string_length_AFTER_Saddle
B = np.zeros(nstrings)
if nstrings == 6:
    B[0] = 0.5
    B[1] = 0.5
    B[2] = 0.5
    B[3] = 0.5
    B[4] = 0.5
    B[5] = 0.5
if nstrings == 4:
    B[0] = 0.5
    B[1] = 0.5
    B[2] = 0.5
    B[3] = 0.5
if nstrings == 3:
    B[0] = 0.5
    B[1] = 0.5
    B[2] = 0.5
    
B = B + nut_width
A = A + saddle_width

#********************************
class pointdata:
    """Overpress method and data"""
    def __init__(self):
        return
    
finger = pointdata()
#********************************

#********************************
# Overpress Input
#********************************
class overpress:
    """Overpress method and data"""
    def __init__(self):
        return
    
OP = overpress()
#********************************

# Overpress from experimental data
OP.method = 'Experiment'
OP.filename = over_press_file

# No Overpress
#OP.method = 'Zeros'

# Constant Overpress
#OP.method = 'Constant'
#OP.cnst1 = 0.002

# Overpress from Eureqa
#OP.method = 'Eureqa3' #Universal Fit
#OP.method = 'Eureqa6' #Steel String Fit,
#OP.method = 'Eureqa10' #Nylon String Fit

## Overpress from Wave Theory
#OP.method = 'WaveTheory'
#OP.nsolutions = 10000
#OP.option = 1 # Uses individual string Force Decay--individual Open String Plucking Force
#OP.option = 2 # Uses average decay rate, and individual Open String Plucking Force
#OP.option = 3 # Uses supplied FDC value for the decay rate, and individual open string plucking forces
#OP.cnst1 = -0.02 # FDC
#OP.option = 4 # Uses individual decay rates and the mean (open string plucking force)
#OP.option = 5 # Uses the mean decay rate and the mean intercept (open string plucking force)
#OP.option = 6 # Uses supplied FDC value for the decay rate, and supplied open string plucking forces
#OP.cnst1 = -0.02 # FDC
#OP.cnst2 = 0.5 # Force intercept - Open String Plucking Force

# Trevor Gore Overpress method
#OP.method = 'Gore'
#OP.cnst1 = 0.75 # Fingerstyle
# OP.cnst1 = 0.85 # Flatpick
#**************************************************************************



# Initialize Fixed Arrays
string_scale = Lscale*np.ones((nstrings,1))
FFR = FFR*np.ones((nstrings,nfrets)) # Where the finger presses down on the fret board

# Frequency for each fretted position for each string - From Magliari
f = np.loadtxt(freq_file)
f = np.transpose(f)
open_freq = f[:,0]
fretted_freq = f[:,range(1,nfrets+1)]

action = np.loadtxt(actionfile) # Measured Action
action = np.transpose(action)

# Physical Constants for Strings
StringProps = np.loadtxt(stringprops) # Three column file: E*Area, mu, and Diameter
StringProps = np.transpose(StringProps)
Earea = StringProps[0,]
mu = StringProps[1,]
dia = StringProps[2,]

# Plucking Force - Used for Wave Theory OP Calcualtions
PF = np.loadtxt(PFfile)

#**************************************************************************
# Uncompensated Scenarios - Where niterations = 0
#**************************************************************************
# Use this if you are plotting the traditional saddle offsets and not iterating through the MCS
if niterations == 0:
    if nstrings == 6:
        comp = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    if nstrings == 4:
#         comp = [0.0207 0.0515 0.042 0.058]; # For the J74 OP = 0.0 stringset
#         comp = [0.0195 0.046 0.037 0.052]; # For the J74 OP = 0.0 stringset
#         comp = [0.0205 0.017 0.03 0.045]; # For the J80 OP = 0.0 stringset
#         comp = [0.025 0.02 0.035 0.053]; # For the J80 OP = 0.002 stringset
#         comp = [0.028 0.024 0.05 0.075]; # For the J80 OP = Universal Fit
         comp = [0.026, 0.024, 0.049, 0.073] # For the J80 OP = Steel String Fit
    if nstrings == 3:
        comp = [0.0, 0.0, 0.0]
    string_scaleComp = string_scale + comp
else:
    string_scaleComp = string_scale
    
#**************************************************************************
# Initial Setup - Geometry of the fretboard
#**************************************************************************
(Lfret) = find_fret_positions(nstrings,nfrets,string_scale)
Lfret_initial = Lfret
(nut,saddle) = find_initial_nut_saddle(Lfret,H,action,string_scaleComp)
(stringL) = find_stringL(saddle,Lfret,H,R)
stringL_initial = stringL
# [ko,k] = find_string_stiffness(nstrings,nfrets,Earea,string_scale,stringL);

saddle_shelf = saddle[:,0] - min(saddle[:,0])
nut_shelf = np.abs(nut[:,0] - max(nut[:,0]))
A1 = A - nut_shelf
B1 = B - saddle_shelf
#print(nut_shelf,saddle_shelf)

(L,Lvibrate) = find_tension_length2(nut,saddle,A1,B1)
(T)= find_string_tension(mu,open_freq,Lvibrate,g)

#**************************************************************************
# Incorporate Overpress
#**************************************************************************
(over_press) = find_overpress(OP,Earea,mu,Lscale,stringL,T,Lfret,H,R,action,FFR,nut,saddle,string_scaleComp,PF,Pd)
over_press = over_press[:,0:nfrets]
fig4 = 4
plot_overpress(fig4,over_press)

#**************************************************************************

#**************************************************************************
# Update Geometry/String Tensions with Overpress Included
#**************************************************************************
(nut,saddle,action,finger,string_press,nsegments) = find_fretboard_geometry(Lfret,H,R,action,FFR,nut,saddle,string_scaleComp,over_press)
print(nut)
saddle_shelf = saddle[:,0] - min(saddle[:,0]) # We use this becuase the shelf is cut into the saddle to allow for the ocmpensation, but we don't relaly move the saddle position
nut_shelf = np.abs(nut[:,0] - max(nut[:,0]))
A1 = A - nut_shelf
B1 = B - saddle_shelf

(Lor,Lor_vibrate) = find_unstressed_length2(T,Earea,L,A1,B1)
(Ls,stringL,string_press,finger,wrap_around) = find_stressed_length_wraparound2(nut,saddle,finger,nsegments,H,R,Lfret,over_press,A1,B1)   
(Ts) = find_fretted_string_tension(Ls,Lor,Earea)
(tuning2,freq2) = find_tuning(fretted_freq,Ts,mu,g,stringL)

fig1 = 1
plot_tuning(fig1,tuning2,False,max_tune,min_tune)
scale_dist = Lfret[0,even_fret] - Lfret[0,zero_fret]

#**************************************************************************
# MCS
#**************************************************************************
delta = np.zeros((nstrings,niterations))

for i in range(0,niterations):
    (L,Lvibrate) = find_tension_length2(nut,saddle,A1,B1)
    (T)= find_string_tension(mu,open_freq,Lvibrate,g)
    (over_press) = update_overpress(over_press,OP,saddle,Lfret,H,R,Earea,mu,T)
    (Lor,Lor_vibrate) = find_unstressed_length2(T,Earea,L,A1,B1)
    (Ls,stringL,string_press,finger,wrap_around) = find_stressed_length_wraparound2(nut,saddle,finger,nsegments,H,R,Lfret,over_press,A1,B1)
    (Ts) = find_fretted_string_tension(Ls,Lor,Earea)
    (Lfret) = update_fret_locations(Ts,mu,fretted_freq,g,saddle,H,R)
    (Lfret,nut) = shift_updated_frets(Lfret,nut,zero_fret)
    (string_scale,saddle,d) = update_string_scaleGaryNew(Lfret,string_scale,zero_fret,even_fret,nut,saddle,scale_dist);
    (nut,saddle,action,finger,string_press,nsegments) = find_fretboard_geometry(Lfret,H,R,action,FFR,nut,saddle,string_scale,over_press)
    delta[:,i] = np.transpose(d)
    
    saddle_shelf = saddle[:,0] - min(saddle[:,0])
    nut_shelf = np.abs(nut[:,0] - max(nut[:,0]))
    A1 = A - nut_shelf
    B1 = B - saddle_shelf

fig2 = 2
plot_delta(fig2,niterations,delta)

Lfret_final = np.mean(Lfret,axis=0)
Lfinal = np.zeros((nstrings,nfrets))
for i in range(0,nstrings):
    for j in range(0,nfrets):
        Lfinal[i,j] = Lfret_final[j]

(L_f,L_fvibrate) = find_tension_length2(nut,saddle,A1,B1)
(T_f)= find_string_tension(mu,open_freq,L_fvibrate,g)
(Lor_f,Lor_fvibrate) = find_unstressed_length2(T_f,Earea,L_f,A1,B1)
(Ls_f,stringL,sp_final,finger,wrap_around) = find_stressed_length_wraparound2(nut,saddle,finger,nsegments,H,R,Lfinal,over_press,A1,B1)
(Ts_f) = find_fretted_string_tension(Ls_f,Lor_f,Earea)
(tuning,freq) = find_tuning(fretted_freq,Ts_f,mu,g,stringL)

fig3 = 3
min_tune = np.min(tuning)
max_tune = np.max(tuning)
plot_tuning(fig3,tuning,True,max_tune,min_tune)
(nut,saddle,action,finger,string_press,nsegments) = find_fretboard_geometry(Lfinal,H,R,action,FFR,nut,saddle,string_scale,over_press)

# For comparison to Gary Magliari's simulations
gary_saddle = saddle[:,0] - min(saddle[:,0])
gary_nut = np.abs(nut[:,0] - max(nut[:,0]))

# Shifts the fretboard locations to a common zero to cut the frets
shift = np.max(nut[:,0])
nut_index = np.argmax(nut,axis=0)
nut_index = nut_index[0] + 1
Lfret_ToCut = Lfret_final - shift # These are the values for creating the actual fretboard

# Find the relative positions of the nut from the "zero" string
nut_height = nut[:,1]
nut_offset = nut[:,0] - shift # Nut Offset wil be the amount we need to machine off the nut to obtain the right intonation

# Find the saddle offset
saddle_offset = saddle[:,0] - np.min(saddle[:,0])

# Find the distance to set the saddle away from the nut - This is the
# distance from the leading edge of the saddle to the leading edge of the
# nut. This may not happen at the same string, but before cutting either
# the nut or the saddle, we should be able to use the uncut pieces to
# position the saddle accurately.
saddle_min = np.min(saddle_offset)
saddle_index = np.argmin(saddle_offset)
nut_to_saddle = string_scale[saddle_index] - np.abs(nut_offset[saddle_index]) # This gives us exactly the amount the leading edge of the nut will be from the leading edge of the saddle

print('Nut Offset = ',nut_offset, '\n')
print('Nut to Saddle = ',nut_to_saddle, '\n')
print('Final Fret Positions - To Cut =', Lfret_ToCut, '\n')
print('Saddle Offset = ', saddle_offset, '\n')

print(np.mean(Lfret_initial,0) - Lfret_ToCut - 0.072) #The 0.029 is from the top of Gary's sheet - compare this to Compensated vs Traditional
shift = Lfret_initial[0,zero_fret] - Lfret_final[zero_fret]
cvt = Lfret_initial[0,:]-shift
print(Lfret_final - cvt)