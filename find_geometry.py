#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  9 12:11:22 2018

@author: turnertj
"""
import numpy as np

class pointdata:
    """Overpress method and data"""
    def __init__(self):
        return
    
#********************************
def find_fret_radius(fret_height,fret_width):
    a = fret_height
    c = fret_width/2.0
    fret_radius = (c**2 + a**2)/(2.0*a)
    return (fret_radius)

#********************************
def find_fret_positions(nstrings,nfrets,string_scale):
    # Initial Fret Lengths - using 12th root of 12

    Lfret = np.zeros((nstrings,nfrets))
    for i in range(0,nstrings):
        for j in range (0,nfrets):
            Lfret[i,j] = string_scale[i] - (string_scale[i]/(2.0**((j+1)/12)))
    return (Lfret)

#********************************
def find_initial_nut_saddle(Lfret,H,action,string_scale):
    # Uses the action at the 1st and the 12th fret to find the equation of a line,
    # assuming the string makes a straight line - invalid, but ok since the mass of the string is low
    
    x = 0 # just labeling the indices, for the x-direction and y-direction
    y = 1

    nstrings = np.size(Lfret,0)
    nut = np.zeros((nstrings,2))
    saddle = np.zeros((nstrings,2))

    for i in range(0,nstrings):

        # Uses the fist and the 12th fret
        y1 = H + action[i,0]
        y2 = H + action[i,11]
        x1 = Lfret[i,0]
        x2 = Lfret[i,11]

        m = (y2-y1)/(x2-x1)
        b = y1 - m*x1

        nut[i,y] = nut[i,x]*m+b
    
        saddle[i,x] = nut[i,x]+string_scale[i]
        saddle[i,y] = saddle[i,x]*m+b
    
    return(nut,saddle)

#********************************
def find_stringL(saddle,Lfret,H,R):
    #This function finds the length of the string from the saddle to the fret
    #stringL = nstrings x nfrets
    
    x = 0 # just labeling the indices, for the x-direction and y-direction
    y = 1
    nstrings = np.size(Lfret,0)
    nfrets = np.size(Lfret,1)
    
    b = H - R #accounts for the fret geometry - moves the entire system up or down until the datum goes through the center of the fret

    stringL = np.zeros((nstrings,nfrets))
    for i in range (0,nstrings):
        for j in range (0,nfrets):
            xs = saddle[i,x]
            ys = saddle[i,y]
            ys = ys - b
            d1 = xs - Lfret[i,j]
            HH = d1**2 + ys**2
            stringL[i,j] = np.sqrt(HH - R**2) # Bridge to fret length

    return(stringL)
    
    
#********************************
def find_tension_length(nut,saddle):

    x = 0  # just labeling the indices, for the x-direction and y-direction
    y = 1
    
    nstrings = np.size(nut,0)
    L = np.zeros((nstrings,1))
    for i in range (0,nstrings):
        x1 = saddle[i,x]
        y1 = saddle[i,y]
        x2 = nut[i,x]
        y2 = nut[i,y]
        L[i] = np.sqrt((x1 - x2)**2 + (y1 - y2)**2)
        
    return(L)
    
#********************************
def find_tension_length2(nut,saddle,BEFORE_Nut,AFTER_Saddle):

    x = 0  # just labeling the indices, for the x-direction and y-direction
    y = 1
    
    nstrings = np.size(nut,0)
    Lvibrate = np.zeros((nstrings,1))
    L = np.zeros((nstrings,1))

    for i in range (0,nstrings):
        x1 = saddle[i,x]
        y1 = saddle[i,y]
        x2 = nut[i,x]
        y2 = nut[i,y]
        Lvibrate[i] = np.sqrt((x1 - x2)**2 + (y1 - y2)**2)
        L[i] = Lvibrate[i] + BEFORE_Nut[i] + AFTER_Saddle[i]
        
    return(L,Lvibrate)
    
#********************************
def find_unstressed_length(T,Earea,L):
    """
    This is the unstressed length of each string, as it would be if it were
    not under tension
    
    Calcualted from Hooke's Law
    """
    nstrings = np.size(T,0)
    Lor = np.zeros((nstrings,1))
    for i in range (0, nstrings):
        Lor[i] = (L[i])/((T[i]/Earea[i]) + 1.0)

    return(Lor)
    
#********************************
def find_unstressed_length2(T,Earea,L,A,B):
    """
    This is the unstressed length of each string, as it would be if it were
    not under tension
    
    Calcualted from Hooke's Law
    """
    nstrings = np.size(T,0)
    Lor = np.zeros((nstrings,1))
    Lor_vibrate = np.zeros((nstrings,1))

    dA = np.zeros((nstrings,1))
    dB = np.zeros((nstrings,1))
    for i in range (0, nstrings):
        Lor[i] = (L[i])/((T[i]/Earea[i]) + 1.0)
        dA[i] = (T[i]/Earea[i])*A[i];
        dB[i] = (T[i]/Earea[i])*B[i];
        Lor_vibrate[i] = Lor[i] - (A[i] - dA[i]) - (B[i] - dB[i])

    return(Lor,Lor_vibrate)

#********************************
def find_fretboard_geometry(Lfret,H,R,action,FFR,nut,saddle,string_scale,over_press):

    nstrings = np.size(Lfret,0)
    nfrets = np.size(Lfret,1)
    x = 0
    y = 1
    string_press = np.zeros((nstrings,nfrets))

    x1 = Lfret[:,0]
    x2 = Lfret[:,11]
    y1 = H + action[:,0]
    y2 = H + action[:,11]
        
    if np.size(action,1) < nfrets: #We only use the 1st and 12th frets to setup action anyway
        action = np.zeros((nstrings,nfrets))
        
    for i in range (0,nstrings):
        m = (y2[i]-y1[i])/(x2[i]-x1[i])
        b = y1[i] - m*x1[i]

        nut[i,y] = nut[i,x]*m+b
    
        saddle[i,x] = nut[i,x]+string_scale[i]
        saddle[i,y] = saddle[i,x]*m+b
    
        for j in range (0,nfrets):
            action[i,j] = m*Lfret[i,j] + b - H
        
    # Find where the finger is pressed down against the fretboard
    finger = pointdata()
    finger.x = np.zeros((nstrings,nfrets))
    finger.y = np.zeros((nstrings,nfrets))

    for i in range(0,nstrings):
        finger.x[i,0] = FFR[i,0]*Lfret[i,0]
        for j in range(1,nfrets):
            d = Lfret[i,j] - Lfret[i,j-1]
            finger.x[i,j] = Lfret[i,j-1] + FFR[i,j]*d

    # Find how many line segments we have to calculate the stretched length
    nsegments = 3*np.ones((nstrings,nfrets)) # Set everything to 3 line segments at first, and then see if it needs 4

    for i in range (0,nstrings):
        (L,finger_height,sp,wrap_around) = saddle_to_finger_distance(saddle[i,],Lfret[i,0],H,R,finger.x[i,0],over_press[i,0])    
        finger.y[i,0] = finger_height
        string_press[i,0] = sp
        for j in range (1,nfrets):
            (L,finger_height,sp,wrap_around) = saddle_to_finger_distance(saddle[i,],Lfret[i,j],H,R,finger.x[i,j],over_press[i,j])
            finger.y[i,j] = finger_height
            string_press[i,j] = sp
                
            # Assume fret is a section of a cylinder
            xc = Lfret[i,j-1]
            yc = H - R
        
            # Line from the finger press down location to the nut location
            xx1 = finger.x[i,j] - xc # place zero at the fret location
            yy1 = finger_height - yc
            xx2 = nut[i,0] - xc
            yy2 = nut[i,1] - yc
            m = (yy2-yy1)/(xx2-xx1)
            b = yy1 - m*xx1
                
            # Solve intersection of finger-nut line with the equation of the circular fret
            A = (1.0 + m**2)
            B = (2.0*m*b)
            C = b**2 - R**2

            # If there is an intersection, then there is at least one real root
            # for x. Therefore the string will intersect the fret BEHIND the funger somewhere, and
            # the nsegments is 4 - To have a real root check the sum under the 
            # sqrt function
            xx1 = B**2 - 4.0*A*C
            xx2 = B**2 - 4.0*A*C
            
            if xx1 > 0.0 or xx2 > 0.0:
                nsegments[i,j] = 4

    return(nut,saddle,action,finger,string_press,nsegments)  
    

#********************************
def find_stressed_length_wraparound(nut,saddle,finger,nsegments,H,R,Lfret,over_press):

    x = 0
    y = 1
    nstrings = np.size(nut,0)
    nfrets = np.size(nsegments,1)
    
    Ls = np.zeros((nstrings,nfrets))
    string_press = np.zeros((nstrings,nfrets))
    wrap_around = np.zeros((nstrings,nfrets))
    
    (stringL) = find_stringL(saddle,Lfret,H,R) # stringL = Bridge to the Fret Length
    for i in range(0,nstrings):
        for j in range(0,nfrets):
            if nsegments[i,j] == 3:
                (L,finger_height,sp,wa) = saddle_to_finger_distance(saddle[i,],Lfret[i,j],H,R,finger.x[i,j],over_press[i,j])
                wrap_around[i,j] = wa;
                Ls[i,j] = L
                string_press[i,j] = sp
                finger.y[i,j] = finger_height
                
                xf = finger.x[i,j]
                yf = finger.y[i,j]
                xn = nut[i,x] # x-dimension of the nut - along the fretboard
                yn = nut[i,y] # y-dimension of the nut - perpendicular to the fretboard
                Ls[i,j] = Ls[i,j] + np.sqrt((xf - xn)**2 + (yf - yn)**2) # Adds the finger-to-nut dimension
                
            if nsegments[i,j] == 4:
                [L,finger_height,sp,qa] = saddle_to_finger_distance(saddle[i,],Lfret[i,j],H,R,finger.x[i,j],over_press[i,j])
                wrap_around[i,j] = wa;
                Ls[i,j] = L
                string_press[i,j] = sp
                finger.y[i,j] = finger_height
                (L) = finger_to_nut_distance(nut[i,],Lfret[i,j-1],H,R,finger.x[i,j],finger_height)
                Ls[i,j] = Ls[i,j] + L
                
    return (Ls,stringL,string_press,finger,wrap_around)

#********************************
def find_stressed_length_wraparound2(nut,saddle,finger,nsegments,H,R,Lfret,over_press,BEFORE_Nut,AFTER_Saddle):

    x = 0
    y = 1
    nstrings = np.size(nut,0)
    nfrets = np.size(nsegments,1)
    
    Ls = np.zeros((nstrings,nfrets))
    string_press = np.zeros((nstrings,nfrets))
    wrap_around = np.zeros((nstrings,nfrets))
    
    (stringL) = find_stringL(saddle,Lfret,H,R) # stringL = Bridge to the Fret Length
    for i in range(0,nstrings):
        for j in range(0,nfrets):
            if nsegments[i,j] == 3:
                (L,finger_height,sp,wa) = saddle_to_finger_distance(saddle[i,],Lfret[i,j],H,R,finger.x[i,j],over_press[i,j])
                wrap_around[i,j] = wa;
                Ls[i,j] = L
                string_press[i,j] = sp
                finger.y[i,j] = finger_height
                
                xf = finger.x[i,j]
                yf = finger.y[i,j]
                xn = nut[i,x] # x-dimension of the nut - along the fretboard
                yn = nut[i,y] # y-dimension of the nut - perpendicular to the fretboard
                Ls[i,j] = Ls[i,j] + np.sqrt((xf - xn)**2 + (yf - yn)**2) # Adds the finger-to-nut dimension
                
            if nsegments[i,j] == 4:
                [L,finger_height,sp,qa] = saddle_to_finger_distance(saddle[i,],Lfret[i,j],H,R,finger.x[i,j],over_press[i,j])
                wrap_around[i,j] = wa;
                Ls[i,j] = L
                string_press[i,j] = sp
                finger.y[i,j] = finger_height
                (L) = finger_to_nut_distance(nut[i,],Lfret[i,j-1],H,R,finger.x[i,j],finger_height)
                Ls[i,j] = Ls[i,j] + L
                
    for i in range(0,nstrings):
        Ls[i,] = Ls[i,] + BEFORE_Nut[i] + AFTER_Saddle[i]
        
    return (Ls,stringL,string_press,finger,wrap_around)

#********************************
def saddle_to_finger_distance(saddle,Lfret,H,R,finger_x,over_press):

    xs = saddle[0]
    ys = saddle[1]

    b = H - R # accounts for the fret geometry - moves the entire system up or down until the datum goes through the center of the fret
    ys = ys - b

    d1 = xs - Lfret
    HH = d1**2 + ys**2
    stringL = np.sqrt(HH - R**2) # Bridge to fret length

    tanA = ys/d1
    A = np.arctan(tanA)

    tanB = stringL/R
    B = np.arctan(tanB)

    C = A + B - np.pi/2.0

    offset = R*np.sin(C)

    DistZ = R - (R*np.cos(C))

    fret_space = Lfret - finger_x
    DistY = fret_space - offset
    DistX = DistY*np.tan(C)

    string_press = DistX + DistZ # Distance below the fret height that you need to press in order to make the string contact the fret

    # If there is any overpress, then there will be WRAP AROUND!

    DistW = R-(string_press + over_press)

    tanD = DistW/fret_space
    D = np.arctan(tanD)

    DistV = np.sqrt(DistW**2 + fret_space**2)

    cosE = R/DistV
    E = np.arccos(cosE)

    F = np.pi/2.0 - (C + D + E)
    wrap_around = F*R # Wrap Around Length
#    wrap_around = 0.0

    fret_to_finger_length = np.sqrt(DistV**2 - R**2)

    L = stringL + wrap_around + fret_to_finger_length
    finger_height = DistW + b

    return(L,finger_height,string_press,wrap_around)
    
#********************************
def finger_to_nut_distance(nut,Lfret,H,R,finger,finger_height):

    xn = nut[0]
    yn = nut[1]
   
    b = H - R # accounts for the fret geometry - moves the entire system up or down until the datum geos through the center of the fret
    yn = yn - b
    
    DistW = finger_height
    d2 = finger - Lfret
    tanD = DistW/d2
    D = np.arctan(tanD)

    DistV = np.sqrt(d2**2 + DistW**2)
    
    cosE = R/DistV
    E = np.arccos(cosE)

    d1 = Lfret - xn
    HH = d1**2 + yn**2
    StringL = np.sqrt(HH - R**2)

    tanA = yn/d1
    A = np.arctan(tanA)

    tanB = StringL/R
    B = np.arctan(tanB)

    C = A + B - np.pi/2.0
   
    F = np.pi/2.0 - (C + D + E)
    wrap_around = F*R
#    wrap_around = 0.0

    finger_to_fret = np.sqrt(DistV**2 - R**2)

    L = StringL + wrap_around + finger_to_fret
    return(L)

#******************************************************************************
def update_fret_locations(Ts,mu,fretted_freq,g,saddle,H,R):
    
    # This method uses the UPDATED hypotenuse of the string length to find the new fret
    # locations - utilizing Gary's wrap around method

    nstrings = np.size(Ts,0)
    nfrets = np.size(Ts,1)
    x = 0
    y = 1
    yc = H - R

    Lfret = np.zeros((nstrings,nfrets))
    for i in range(0,nstrings):
        sx = saddle[i,x]
        sy = saddle[i,y] - yc
        for j in range(0,nfrets):
            L = np.sqrt(Ts[i,j]*g/mu[i])/(2.0*fretted_freq[i,j]) #using this to compute the fret location on the fret board
            HH = L**2 + R**2
            d1 = np.sqrt(HH - sy**2)
            Lfret[i,j] = sx - d1

    return(Lfret)

#******************************************************************************
def shift_updated_frets(Lfret,nut,zero_fret):

    x = 0
    nstrings = np.size(Lfret,0)
    nfrets = np.size(Lfret,1)
    z_fret_pos = Lfret[0,zero_fret] # shift all fret locations based on third fret - and make the 1st string primary
    for i in range(0,nstrings):
        shift_dist = Lfret[i,zero_fret] - z_fret_pos
        for j in range(0,nfrets):
            Lfret[i,j] = Lfret[i,j] - shift_dist
        nut[i,x] = nut[i,x] - shift_dist
    
    return(Lfret,nut)

#******************************************************************************
def update_string_scaleGaryNew(Lfret,string_scale,zero_fret,even_fret,nut,saddle,scale_dist):

    # Uses Gary's new method of using the 
    x = 0
    nstrings = np.size(Lfret,0)
    d = np.zeros((nstrings,1))
    for i in range(0,nstrings):
        d[i] = Lfret[i,even_fret] - Lfret[i,zero_fret]

    for i in range(0,nstrings):
        string_scale[i] = (scale_dist/d[i])*string_scale[i]
        saddle[i,x] = nut[i,x] + string_scale[i]

    d = d - scale_dist
    return(string_scale,saddle,d)
    