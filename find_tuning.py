#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 20 14:20:51 2018

@author: turnertj
"""
import numpy as np

#******************************************************************************
            
def  find_tuning(fretted_freq,Ts,mu,g,stringL):
    
    nstrings = np.size(stringL,0)
    nfrets = np.size(stringL,1)
    tuning = np.zeros((nstrings,nfrets+1))
    freq = np.zeros((nstrings,nfrets))

    for i in range(0,nstrings):
        for j in range(0,nfrets):    
            freq[i,j] = np.sqrt(Ts[i,j]*g/mu[i])/(2.0*stringL[i,j])
            b = fretted_freq[i,j]
            tuning[i,j+1] = 1200.0*np.log2(freq[i,j]/b)          
           
    return(tuning,freq)

#******************************************************************************


