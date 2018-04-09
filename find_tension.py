#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 12 09:37:22 2018

@author: turnertj
"""
import numpy as np

#********************************
def find_string_tension(mu,open_freq,Lvibrate,g):

    nstrings = np.size(mu,0)
    T = np.zeros((nstrings,1))
    for i in range (0, nstrings):
        T[i] = mu[i]*((2.0*Lvibrate[i]*open_freq[i])**2)/g

    return(T)
    
#********************************
def find_fretted_string_tension(Ls,Lor,Earea):

    nstrings = np.size(Ls,0)
    nfrets = np.size(Ls,1)

    Ts = np.zeros((nstrings,nfrets))
    for i in range(0,nstrings):
        for j in range (0,nfrets):
            Ts[i,j] = Earea[i]*((Ls[i,j] - Lor[i])/Lor[i])
    
    return(Ts)