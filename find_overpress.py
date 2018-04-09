#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  9 16:13:51 2018

@author: turnertj
"""
import numpy as np
from find_geometry import find_initial_nut_saddle
from find_geometry import find_tension_length
from find_geometry import find_unstressed_length
from find_geometry import find_fretboard_geometry
from find_geometry import find_stressed_length_wraparound
from find_geometry import find_stringL
from find_tension import find_fretted_string_tension
import numpy.matlib

#********************************
def find_overpress(OP,Earea,mu,Lscale,stringL,T,Lfret,H,R,action,FFR,nut,saddle,string_scaleComp,PF,Pd):

    nstrings = np.size(Lfret,0)
    nfrets = np.size(Lfret,1)
    
    if OP.method == 'Experiment':
        over_press = np.loadtxt(OP.filename); # Measured Overpress Values
        over_press = np.transpose(over_press)

    if OP.method == 'Zeros':
        over_press = np.zeros((nstrings,nfrets))

    if OP.method == 'Constant':
        OPC = OP.cnst1
        over_press =OPC*np.ones((nstrings,nfrets))

    if OP.method == 'Eureqa3':
        (over_press) = Eureqa_OverpressUNIVERSAL3(Earea,mu,stringL,T)

    if OP.method == 'Eureqa6':
        (over_press) = Eureqa_OverpressUNIVERSAL6(Earea,mu,stringL,T)
        
    if OP.method == 'Eureqa10':
        (over_press) = Eureqa_OverpressUNIVERSAL10(Earea,mu,stringL,T)

    if OP.method == 'WaveTheory':
        (over_press) = WaveTheoryOverpress(nstrings,nfrets,OP,PF,Lfret,Lscale,Earea,Pd,action,H,R,FFR,T)

    if OP.method == 'Gore':
        picking_factor = OP.cnst1
        (over_press) = GoreOverpress(nstrings,nfrets,picking_factor,Lfret,H,R,action,FFR,nut,saddle,string_scaleComp)

    return (over_press)

#********************************
def Eureqa_OverpressUNIVERSAL3(EA1,mu1,stringL,Tension):

    # UNIVERSAL FIT #2
    nstrings = np.size(stringL,0)
    nfrets = np.size(stringL,1)
    
    over_press = np.zeros((nstrings,nfrets))

    for i in range (0,nstrings):
        EA = EA1[i]
        mu = mu1[i]
        T = Tension[i]
        for j in range (0,nfrets):
            L = stringL[i,j]
            over_press[i,j] = (0.0309477062056007 + 536.478488683596*mu*L + 0.45078723151166*EA*mu - 0.00285734428235631*T - 3334.02793617732*mu)/(1.01429651748782 + T + 28106.9797489247*mu*T) - 6.06093150413197*mu 
            #if (over_press(i,j) < 0.0005)
            #    over_press(i,j) = 0.0005;
    
    return(over_press)

#********************************
def Eureqa_OverpressUNIVERSAL6(EA1,mu1,stringL,Tension):

    # UNIVERSAL FIT #2
    nstrings = np.size(stringL,0)
    nfrets = np.size(stringL,1)
    
    over_press = np.zeros((nstrings,nfrets))

    for i in range(0,nstrings):
        EA = EA1[i]
        mu = mu1[i]
        T = Tension[i]
        for j in range(0, nfrets):
            L = stringL[i,j]
            over_press[i,j] = (7734.93191519131*mu*L**2 + EA*mu*L**2 - 142427302.38658*L*mu**2)/(687.542199515901*T + 6084277.82931012*mu*T + 772.335598329031*mu*T**2*L**2)
   
    return(over_press)
    
#********************************
def Eureqa_OverpressUNIVERSAL10(EA1,mu1,stringL,Tension):

    # UNIVERSAL FIT #2

    nstrings = np.size(stringL,0)
    nfrets = np.size(stringL,1)
    
    over_press = np.zeros((nstrings,nfrets))

    for i in range(0,nstrings):
        mu = mu1[i]
        T = Tension[i]
        for j in range(0,nfrets):
            L = stringL[i,j]
            over_press[i,j] = 0.4290407107*mu*L + (L - 7.450257878)/(L + 76.7581170146975*T - 109.497992913015)
    
    return(over_press)
    
    
#********************************
def WaveTheoryOverpress(OP,PF,Lfret,Lscale,Earea,Pd,action,H,R,FFR,T):
    
    P = np.zeros((2,1))
    P[0] = np.mean(PF[:,0])
    P[1] = np.mean(PF[:,1])
    
    nstrings = np.size(Lfret,0)
    nfrets = np.size(Lfret,1)
    
    string_scale = Lscale*np.ones((nstrings,1))
    (nut,saddle) = find_initial_nut_saddle(nstrings,Lfret,H,action,string_scale)
    (L) = find_tension_length(nstrings,nut,saddle)
    (Lor) = find_unstressed_length(nstrings,T,Earea,L)

    (over_press) = np.zeros((nstrings,nfrets)) # Start with a zero OP, which should not influence the finger values we need to work out OP values
    (nut,saddle,action,finger_x,finger_y,string_press,nsegments) = find_fretboard_geometry(nstrings,nfrets,Lfret,H,R,action,FFR,nut,saddle,string_scale,over_press)
#    print(nsegments)
    (Ls,stringL,string_press,finger_x,finger_y) = find_stressed_length_wraparound(nfrets,nstrings,nut,saddle,finger_x,finger_y,nsegments,H,R,Lfret,over_press)
    (Ts) = find_fretted_string_tension(nfrets,nstrings,Ls,Lor,Earea)
    
    # Determines the force of the pluck from the experimental over_press
    FF = np.zeros((nstrings,nfrets))
    for i in range (0,nstrings):
        for j in range (0,nfrets):
            if OP.option == 1:
                FF[i,j] = PF[i,0]*Lfret[i,j] + PF[i,1] # Uses the individual string properties
                
            if OP.option == 2:
                FF[i,j] = P[0]*Lfret[i,j] + PF[i,1] # Uses average decay rate, and individual open string plucking forces
                                
            if OP.option == 3:
                FF[i,j] = OP.cnst1*Lfret[i,j] + PF[i,1]  # Uses supplied FDC value for the decay rate, and individual open string plucking forces

            if OP.option == 4:
                FF[i,j] = PF[i,0]*Lfret[i,j] + P[1] # Uses the mean intercept (open string plucking force) and individual decay rates
                
            if OP.option == 5:
                FF[i,j] = P[0]*Lfret[i,j] + P[1] # Uses the mean intercept (open string plucking force) and the mean decay rate, averaged across all strings

            if OP.option == 6:
                FF[i,j] = OP.cnst1*Lfret[i,j] + OP.cnst2 # Uses supplied FDC value for the decay rate, and supplied open string plucking forces
   
    # Finds the plucking d for the given plucking Force
    d_sol = np.zeros((nstrings,nfrets))
    over_press = np.zeros((nstrings,nfrets))
    theta = np.zeros((nstrings,nfrets))
    alpha = np.zeros((nstrings,nfrets))
    for string_num in range (0,nstrings):
        Lvibrate = Lscale - Lfret[string_num,]
        d = np.linspace(0,2.0,OP.nsolutions)
        residual_error = np.zeros((OP.nsolutions,1))
        for j in range (0,nfrets):
            for i in range (0,OP.nsolutions):
                L1 = np.sqrt(d[i]**2 + (Lvibrate[j] - Pd)**2)
                L2 = np.sqrt(d[i]**2 + Pd**2)
                dL = (L1 + L2 ) - Lvibrate[j]
                dT = Earea[string_num]*dL/Lvibrate[j]
                Force_total = Ts[string_num,j] + dT
                residual_error[i] = d[i] - FF[string_num,j]*L1/Force_total
 
            residual_error = np.abs(residual_error)
            index = np.argmin(residual_error)
            d_sol[string_num,j] = d[index]
        
        SP = string_press[string_num,]
        finger_pos = finger_x[string_num,]
        F2 = Lfret[string_num,] - finger_pos # distance between finger location and fret
        for i in range(0,nfrets):
            theta[string_num,i] = np.arctan(d_sol[string_num,i]/(Lvibrate[i] - Pd))
            alpha[string_num,i] = np.arctan(SP[i]/F2[i])
            over_press[string_num,i] = F2[i]*np.tan(theta[string_num,i] + alpha[string_num,i]) - SP[i]
    return(over_press)
    
#********************************
def GoreOverpress(picking_factor,Lfret,H,R,action,FFR,nut,saddle,string_scaleComp):

    nstrings = np.size(Lfret,0)
    nfrets = np.size(Lfret,1)
    
    over_press = np.zeros((nstrings,nfrets)) # Start with a zero OP, which should not influence the string_press values we need to work out Gore's OP values
    (nut,saddle,action,finger_x,finger_y,string_press,nsegments) = find_fretboard_geometry(nstrings,nfrets,Lfret,H,R,action,FFR,nut,saddle,string_scaleComp,over_press)

    go = 0.5 # Trevor uses a 0.5mm deflection as the OP + string_press at the 1st fret
    go = go/25.4 # Convert to inches - he uses metric in his book

    go = go*picking_factor
    g = np.zeros((nfrets,1))
    g[0] = go
    for i in range(1,nfrets):
        g[i] = go*(Lfret[0,i] - Lfret[0,i-1])/Lfret[0,0]

    over_press = np.matlib.repmat(g,1,nstrings)
    over_press = np.transpose(over_press)
#    over_press = over_press
#    print (over_press, string_press)
    over_press = over_press - string_press # Gore's definition includes the string_press, so subtract it to get our OP
    
    return(over_press)

#********************************
def update_overpress(over_press,OP,saddle,Lfret,H,R,Earea,mu,T):
    
    # Updates the over_press in the MCS iterations, for those methods of
    # over_press determination that need to be updated - i.e. vary with the
    # updated fretboard/string geometry
          
    if OP.method == 'Eureqa3':
        (stringL) = find_stringL(saddle,Lfret,H,R)
        (over_press) = Eureqa_OverpressUNIVERSAL3(Earea,mu,stringL,T)

    if OP.method == 'Eureqa6':
        (stringL) = find_stringL(saddle,Lfret,H,R)
        (over_press) = Eureqa_OverpressUNIVERSAL6(Earea,mu,stringL,T)

    if OP.method == 'Eureqa10':
        (stringL) = find_stringL(saddle,Lfret,H,R)
        (over_press) = Eureqa_OverpressUNIVERSAL10(Earea,mu,stringL,T)
        
    return(over_press)