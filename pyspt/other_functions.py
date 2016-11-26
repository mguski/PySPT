# -*- coding: utf-8 -*-
"""
Collection of functions


@author: mguski@alaska.edu


"""


import numpy as np

# modul intern
from .Signal import Signal



# TOOLS:        
def generate_sine(freq=30e3, samplingRate=1e6, nSamples=50e3, amplitude=1.0, phaseOffset=0):
    """ Generates sine signal. """
    name ='sine [{}Hz]'.format(Signal._niceUnitPrefix_formatter(freq,0))    
    sine = Signal(np.zeros(int(nSamples)), samplingRate, comment=name)
    sine.timeData = np.float128(amplitude) * np.sin(2*np.pi*freq*sine.timeVector+phaseOffset)
    sine.channelNames = [name]
    return sine

def generate_noise(samplingRate=1e6, nSamples=int(50e3), scale=1.0, mean=0):
    """ Generates white Gaussian noise signal. """
    name = 'gaussian noise ({}, {})'.format(mean, scale)
    noise = Signal(np.random.normal(loc=mean, scale=scale, size=nSamples), samplingRate, comment=name) #
    noise.channelNames = [name]
    return noise
    
    
def merge(listOfSignals):
    """ Merges list of Signal objects into one object with multiple channels. """
    nItems = len(listOfSignals)
    output = listOfSignals[0]
    for iItem in range(1,nItems):
        output |= listOfSignals[iItem]
    return output
 

   
