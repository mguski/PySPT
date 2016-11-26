# -*- coding: utf-8 -*-
"""
Collection of functions


@author: mguski@alaska.edu


"""

"""
TODOs:
 - make this a module or a package? 
 - apply python naming: ClassNames, function_names, CONSTANT_VALUES, modules, packages (PEP8 Style Guide for Python)
 - rename module to pyspt
 - add to __init__ pyspt = PySPT (or PySPT = pyspt )
 - channels: channelNames, print in console output, sub reference with .ch()
 - complete all operators
 - call '__new__', by default for obj1 = obj2 ?
 - obj.addChannel() or obbj.appendChannel()
 - possibility to create empty Signal (i.e. to use append in loop)
 - tuncate channels names in __repr__
 - should Signal.copy be renamed to deepcopy, to be in accordance with python definitions?
 - giObj.freqData[0] = np.zeros(11) doen't work but raises no error
 - add channelUnits
 - add signalType: 'power' or 'energy' => add fftNorm, change rms()
 

"""
import numpy as np

# modul intern
from .Signal import Signal



# TOOLS:        
def generate_sine(freq=30e3, samplingRate=1e6, nSamples=500e3, amplitude=1.0, phaseOffset=0):
    """ Generates sine signal. """
    name ='sine [{}Hz]'.format(Signal._niceUnitPrefix_formatter(freq,0))    
    sine = Signal(np.zeros(int(nSamples)), samplingRate, comment=name)
    sine.timeData = np.float128(amplitude) * np.sin(2*np.pi*freq*sine.timeVector+phaseOffset)
    sine.channelNames = [name]
    return sine

def generate_noise(samplingRate=1e6, nSamples=int(500e3), scale=1.0, mean=0):
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
 

   
