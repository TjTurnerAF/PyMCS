#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  8 16:51:07 2018

@author: turnertj
"""

def load_string_set_data(string_set):
    
    if string_set == 1:
        #*****MANDOLIN**************************
        nfrets = 24 #Number of Frets
        nstrings = 4
        Lscale = 13.875 #Scale Length
        FFR = 0.5 #Where the finger presses down on the fret board
        actionfile = 'inputfiles/TF14_J74NoComp_ACTION.dat'
        stringprops = 'inputfiles/J74_DETUNED.dat'
        over_press_file = 'inputfiles/TF14_J74NoComp_OVERPRESS.dat'
        freq_file = 'inputfiles/FretFrequency_30Frets_4Strings.dat'
        PFfile = 'inputfiles/J74_PF.dat'
        #Mandolin Frets
        H = 0.035 #Fret Height - taken from manufacturer
        W = 0.053 #Fret Width - taken from the manufacturer
        Pd = 2.0 #Plucking Distance from the saddle

    elif string_set == 2:
        #*****MANDOLIN DETUNED**************************
        nfrets = 24 #Number of Frets
        nstrings = 12
        Lscale = 13.875 #Scale Length
        FFR = 0.5 #Where the finger presses down on the fret board
        actionfile = 'inputfiles/TF14_J74NoComp_ACTION_DETUNED.dat'
        stringprops = 'inputfiles/J74_DETUNED.dat'
        over_press_file = 'inputfiles/TF14_J74NoComp_OVERPRESS_DETUNED.dat'
        freq_file = 'inputfiles/FretFrequency_EJ74_DETUNED.dat'
        PFfile = 'inputfiles/J74Detuned_PF.dat'
        #Mandolin Frets
        H = 0.035 #Fret Height - taken from manufacturer
        W = 0.053 #Fret Width - taken from the manufacturer
        Pd = 1.0 #Plucking Distance from the saddle

    elif string_set == 3:
        #*****Steel String GUITAR**************************
        nfrets = 24 #Number of Frets
        nstrings = 6
        Lscale = 25.5 #Scale Length
        FFR = 0.5 #Where the finger presses down on the fret board
        actionfile = 'inputfiles/TF254_EJ16NoComp_ACTION.dat'
        stringprops = 'inputfiles/EJ16.dat'
        over_press_file = 'inputfiles/TF254_EJ16NoComp_OVERPRESS.dat'
        freq_file = 'inputfiles/FretFrequency_30Frets_6Strings.dat'
        PFfile = 'inputfiles/EJ16_PF.dat'    
        # Stew Mac 148s
        H = 0.04 #Fret Height - taken from manufacturer
        W = 0.08 #Fret Width - taken from the manufacturer
        Pd = 5.0 #Plucking Distance from the saddle
        
    elif string_set == 4:
        #*****Steel String GUITAR**************************
        nfrets = 20 #Number of Frets
        nstrings = 6
        Lscale = 25.5 #Scale Length
        FFR = 0.5 #Where the finger presses down on the fret board
        actionfile = 'inputfiles/TF254_EJ17NoComp_ACTION.dat'
        stringprops = 'inputfiles/EJ17.dat'
        over_press_file = 'inputfiles/TF254_EJ17NoComp_OVERPRESS.dat'
        freq_file = 'inputfiles/FretFrequency_30Frets_6Strings.dat'
        PFfile = 'inputfiles/EJ17_PF.dat'    
        # Stew Mac 148s
        H = 0.04 #Fret Height - taken from manufacturer
        W = 0.08 #Fret Width - taken from the manufacturer
        Pd = 5.0 #Plucking Distance from the saddle
        
    elif string_set == 5:
        #*****Steel String GUITAR DETUNED**************************
        nfrets = 24 #Number of Frets
        nstrings = 18
        Lscale = 25.5 #Scale Length
        FFR = 0.5 #Where the finger presses down on the fret board
        actionfile = 'inputfiles/TF254_EJ16NoComp_ACTION_DETUNED.dat'
        stringprops = 'inputfiles/EJ16_DETUNED.dat'
        over_press_file = 'inputfiles/TF254_EJ16NoComp_OVERPRESS_DETUNED.dat'
        freq_file = 'inputfiles/FretFrequency_EJ16_DETUNED.dat'
        PFfile = 'inputfiles/EJ16Detuned_PF.dat'
        # Stew Mac 148s
        H = 0.04 #Fret Height - taken from manufacturer
        W = 0.08 #Fret Width - taken from the manufacturer
        Pd = 5.0 #Plucking Distance from the saddle
        
    elif string_set == 6:
        #*****Steel String GUITAR DETUNED**************************
        nfrets = 24 #Number of Frets
        nstrings = 18
        Lscale = 25.5 #Scale Length
        FFR = 0.5 #Where the finger presses down on the fret board
        actionfile = 'inputfiles/TF254_EJ17NoComp_ACTION_DETUNED.dat'
        stringprops = 'inputfiles/EJ17_DETUNED.dat'
        over_press_file = 'inputfiles/TF254_EJ17NoComp_OVERPRESS_DETUNED.dat'
        freq_file = 'inputfiles/FretFrequency_EJ17_DETUNED.dat'
        PFfile = 'inputfiles/EJ17Detuned_PF.dat'
        # Stew Mac 148s
        H = 0.04 #Fret Height - taken from manufacturer
        W = 0.08 #Fret Width - taken from the manufacturer
        Pd = 5.0 #Plucking Distance from the saddle
        
    elif string_set == 7:
        #*****Classical Guitar**************************
        nfrets = 24 #Number of Frets
        nstrings = 3
        Lscale = 25.5 #Scale Length
        FFR = 0.5 #Where the finger presses down on the fret board
        actionfile = 'inputfiles/TF254_EJ45NoComp_ACTION.dat'
        stringprops = 'inputfiles/EJ45.dat'
        over_press_file = 'inputfiles/TF254_EJ45NoComp_OVERPRESS.dat'
        freq_file = 'inputfiles/FretFrequency_30Frets_3Strings.dat'
        PFfile = 'inputfiles/EJ45_PF.dat'
        # Stew Mac 148s
        H = 0.04 #Fret Height - taken from manufacturer
        W = 0.08 #Fret Width - taken from the manufacturer
        Pd = 5.0 #Plucking Distance from the saddle
        
    elif string_set == 8:
        #*****Classical Guitar**************************
        nfrets = 24 #Number of Frets
        nstrings = 3
        Lscale = 25.5 #Scale Length
        FFR = 0.5 #Where the finger presses down on the fret board
        actionfile = 'inputfiles/TF254_EJ45NoComp_ACTION.dat'
        stringprops = 'inputfiles/EJ45.dat'
        over_press_file = 'inputfiles/TF254_EJ45NoComp_OVERPRESS.dat'
        freq_file = 'inputfiles/FretFrequency_30Frets_3Strings.dat'
        PFfile = 'inputfiles/EJ46_PF.dat'
        # Stew Mac 148s
        H = 0.04 #Fret Height - taken from manufacturer
        W = 0.08 #Fret Width - taken from the manufacturer
        Pd = 5.0 #Plucking Distance from the saddle

    elif string_set == 9:
        #*****Classical Guitar**************************
        nfrets = 24 #Number of Frets
        nstrings = 9
        Lscale = 25.5 #Scale Length
        FFR = 0.5 #Where the finger presses down on the fret board
        actionfile = 'inputfiles/TF254_EJ45NoComp_ACTION_DETUNED.dat'
        stringprops = 'inputfiles/EJ45_DETUNED.dat'
        over_press_file = 'inputfiles/TF254_EJ45NoComp_OVERPRESS_DETUNED.dat'
        freq_file = 'inputfiles/FretFrequency_EJ45_DETUNED.dat'
        PFfile = 'inputfiles/EJ45Detuned_PF.dat'
        # Stew Mac 148s
        H = 0.04 #Fret Height - taken from manufacturer
        W = 0.08 #Fret Width - taken from the manufacturer
        Pd = 5.0 #Plucking Distance from the saddle
        
    elif string_set == 10:
        #*****Classical Guitar**************************
        nfrets = 24 #Number of Frets
        nstrings = 9
        Lscale = 25.5 #Scale Length
        FFR = 0.5 #Where the finger presses down on the fret board
        actionfile = 'inputfiles/TF254_EJ46NoComp_ACTION_DETUNED.dat'
        stringprops = 'inputfiles/EJ46_DETUNED.dat'
        over_press_file = 'inputfiles/TF254_EJ46NoComp_OVERPRESS_DETUNED.dat'
        freq_file = 'inputfiles/FretFrequency_EJ46_DETUNED.dat'
        PFfile = 'inputfiles/EJ46Detuned_PF.dat'
        # Stew Mac 148s
        H = 0.04 #Fret Height - taken from manufacturer
        W = 0.08 #Fret Width - taken from the manufacturer
        Pd = 5.0 #Plucking Distance from the saddle
        
    elif string_set == 11: # this is Gary's average medium string properties
        #*****Steel String GUITAR**************************
        nfrets = 20 #Number of Frets
        nstrings = 6
        Lscale = 25.5 #Scale Length
        FFR = 0.5 #Where the finger presses down on the fret board
        actionfile = 'inputfiles/TF254_AVGMedNoComp_ACTION.dat'
        stringprops = 'inputfiles/AVGMed.dat'
        over_press_file = 'inputfiles/AVGMed_OVERPRESS.dat'
        freq_file = 'inputfiles/FretFrequency_30Frets_6Strings.dat'
        PFfile = 'inputfiles/EJ17_PF.dat'    
        # Stew Mac 148s
        H = 0.04 #Fret Height - taken from manufacturer
        W = 0.08 #Fret Width - taken from the manufacturer
        Pd = 5.0 #Plucking Distance from the saddle
        
    return (nfrets,nstrings,Lscale,FFR,actionfile,stringprops,over_press_file,PFfile,freq_file,Pd,H,W)