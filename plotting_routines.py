#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 22 11:15:55 2018

@author: turnertj
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from IPython import get_ipython

def plot_tuning(fig,tuning,plim,max_tune,min_tune):
    
    nstrings = np.size(tuning,0)
    nfrets = np.size(tuning,1)
    plt.figure(fig)
    
    ps1 = 'b--'
    ps2 = 'c--'
    ps3 = 'r--'
    ps4 = 'g--'
    ps5 = 'b-'
    ps6 = 'm--'
    
    xx = np.linspace(0,nfrets,nfrets)
    
    if nstrings == 6:
        plt.plot(xx,tuning[5,],ps1,label='E2')
        plt.plot(xx,tuning[4,],ps2,label='A3')
        plt.plot(xx,tuning[3,],ps3,label='D3')
        plt.plot(xx,tuning[2,],ps4,label='G3')
        plt.plot(xx,tuning[1,],ps5,label='B3')
        plt.plot(xx,tuning[0,],ps6,label='E4')
    if nstrings == 4:
        plt.plot(xx,tuning[5,],ps1,label='E')
        plt.plot(xx,tuning[4,],ps2,label='A')
        plt.plot(xx,tuning[3,],ps3,label='D')
        plt.plot(xx,tuning[2,],ps4,label='G')
    if nstrings == 3:
        plt.plot(xx,tuning[5,],ps1,label='E2')
        plt.plot(xx,tuning[4,],ps2,label='A2')
        plt.plot(xx,tuning[3,],ps3,label='D3')
    
    if plim==False:
        max_tune = np.max(tuning)
        min_tune = np.min(tuning)
        if min_tune > 0.0:
            min_tune = 0.0
    
    plt.xlabel('Fret #')
    plt.ylabel('Tuning in Cents')
    
    xxx = np.zeros((2,1))
    yyy = np.zeros((2,1))
    xxx[0] = 1
    xxx[1] = nfrets
    yyy[0] = 0.0;
    yyy[1] = 0.0;
    plt.plot(xxx,yyy,'k:')
    
    plt.legend()
    plt.xlim(0,nfrets)
    ax = plt.gca()  # gca stands for 'get current axis'
    ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
    ax.yaxis.set_major_locator(ticker.MaxNLocator(integer=False))

    plt.ylim(min_tune,max_tune+1)
    plt.grid(True)
    plt.show() 
    
#******************************************************************************
def plot_delta(fig,niterations,delta):

    x = np.linspace(1,niterations,niterations);
    nstrings = np.size(delta,0)
    
    print('figure = ', fig)
    plt.figure()

    if nstrings == 6:
        y = delta[5,]
        plt.plot(x,y,'b',label='E2')
        
        y = delta[4,]
        plt.plot(x,y,'c',label='A2')
      
        y = delta[3,]
        plt.plot(x,y,'g',label='D3')
        
        y = delta[2,]
        plt.plot(x,y,'y',label='G3')
        
        y = delta[1,]
        plt.plot(x,y,'m',label='B3')
        
        y = delta[0,]
        plt.plot(x,y,'k',label='E4')
        


#if (nstrings == 4)
#   
#    y = delta(4,:);
#    plot(x,y,'g')
#
#    y = delta(3,:);
#    plot(x,y,'y')
#
#    y = delta(2,:);
#    plot(x,y,'m')
#
#    y = delta(1,:);
#    plot(x,y,'k')
#
#    xlabel('Iteration')
#    ylabel('Delta (zero fret to even fret)')
#    % axis([1 niterations 0 0.8])
#    legend('E','A','D','G')
#end
#
#if (nstrings == 3)
#    y = delta(3,:);
#    plot(x,y,'y')
#
#    y = delta(2,:);
#    plot(x,y,'m')
#
#    y = delta(1,:);
#    plot(x,y,'k')
#
#    xlabel('Iteration')
#    ylabel('Delta (zero fret to even fret)')
#    % axis([1 niterations 0 0.8])
#    legend('E2','A2','D3')
#end

    plt.xlim(1,niterations)
#    plt.ylim(0.0,0.8)
    plt.xlabel('Iteration')
    plt.ylabel('Delta (zero fret to even fret)')
    plt.legend()
    plt.show()

#******************************************************************************
def plot_overpress(fig,OP):
    
    nstrings = np.size(OP,0)
    nfrets = np.size(OP,1)
    plt.figure(fig)
       
    ps1 = 'b--'
    ps2 = 'c--'
    ps3 = 'r--'
    ps4 = 'g--'
    ps5 = 'b-'
    ps6 = 'm--'
    
    xx = np.linspace(1,nfrets+1,nfrets)
    
    if nstrings == 6:
        plt.plot(xx,OP[5,],ps1,label='E2')
        plt.plot(xx,OP[4,],ps2,label='A3')
        plt.plot(xx,OP[3,],ps3,label='D3')
        plt.plot(xx,OP[2,],ps4,label='G3')
        plt.plot(xx,OP[1,],ps5,label='B3')
        plt.plot(xx,OP[0,],ps6,label='E4')
    if nstrings == 4:
        plt.plot(xx,OP[5,],ps1,label='E')
        plt.plot(xx,OP[4,],ps2,label='A')
        plt.plot(xx,OP[3,],ps3,label='D')
        plt.plot(xx,OP[2,],ps4,label='G')
    if nstrings == 3:
        plt.plot(xx,OP[5,],ps1,label='E2')
        plt.plot(xx,OP[4,],ps2,label='A2')
        plt.plot(xx,OP[3,],ps3,label='D3')
    
#    if plim==False:
#        max_tune = np.max(OP)
#        min_tune = np.min(OP)
#        if min_tune > 0.0:
#            min_tune = 0.0
    
    plt.xlabel('Fret #')
    plt.ylabel('Over Press (in)')
    
#    xxx = np.zeros((2,1))
#    yyy = np.zeros((2,1))
#    xxx[0] = 1
#    xxx[1] = nfrets
#    yyy[0] = 0.0;
#    yyy[1] = 0.0;
#    plt.plot(xxx,yyy,'k:')
    
    plt.legend()
    plt.xlim(0,nfrets)
    ax = plt.gca()  # gca stands for 'get current axis'
    ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
    ax.yaxis.set_major_locator(ticker.MaxNLocator(integer=False))

    plt.xlim(1,nfrets+1)
    plt.grid(True)
    plt.show()         