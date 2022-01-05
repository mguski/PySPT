# -*- coding: utf-8 -*-
"""
Collection of functions


@author: mguski@alaska.edu


"""


import numpy as np
import scipy.signal

# modul intern
from .Signal import Signal



# Generate:        
def generate_sine(freq=30e3, samplingRate=1e6, nSamples=50e3, amplitude=1.0, phaseOffset=0):
    """ Generates sine signal. """
    name ='sine [{}Hz]'.format(Signal._niceUnitPrefix_formatter(freq,0))    
    sine = Signal(np.zeros(int(nSamples)), samplingRate, comment=name)
    sine.timeData = np.float(amplitude) * np.sin(2*np.pi*freq*sine.timeVector+phaseOffset)
    sine.channelNames = [name]
    return sine

def generate_noise(samplingRate=1e6, nSamples=int(50e3), scale=1.0, mean=0):
    """ Generates white Gaussian noise signal. """
    name = 'gaussian noise ({}, {})'.format(mean, scale)
    noise = Signal(np.random.normal(loc=mean, scale=scale, size=nSamples), samplingRate, comment=name) #
    noise.channelNames = [name]
    return noise


def generate_impulse(samplingRate=44100, signal_length=2, amplitude=1):
    tmp_data = np.zeros(int(signal_length * samplingRate))
    tmp_data[0] = 1
    sig = Signal(tmp_data, samplingRate, comment="Impulse")
    return sig

def generate_sweep(f_start=20, f_stop=20000, sampling_rate=44100, signal_length=3.0, zero_padding=0.3, method='logarithmic', bandwidth=2/12):


    name = "Sweep {}Hz - {}Hz".format(Signal._niceUnitPrefix_formatter(f_start, 0), Signal._niceUnitPrefix_formatter(f_stop, 0))
    f_start = f_start * 2 ** (-bandwidth)
    f_stop = min(f_stop * 2 ** bandwidth, sampling_rate/2)

    time_vec = np.arange(0, signal_length+zero_padding, 1/sampling_rate)
    time_data = scipy.signal.chirp(time_vec, f_start, signal_length, f_stop, method=method, phi=-90)

    # TODO new function time_window()
    # window
    nSamples_win = int(sampling_rate/f_stop*200 + 4 )
    window = np.hanning(nSamples_win*2)
    time_data[int(signal_length*sampling_rate-nSamples_win):int(signal_length*sampling_rate)] *= window[nSamples_win:]
    time_data[int(signal_length*sampling_rate-1):] = 0

    # test fade in
    # wave_lenth_factor = 1/8
    # nSamples_win = int(sampling_rate/f_start * wave_lenth_factor)
    # window = np.hanning(nSamples_win*2)
    # time_data[:nSamples_win] *= window[:nSamples_win]

    sweep = Signal(time_data, sampling_rate, comment=name)
    sweep.channelNames = [name]
    return sweep




# other    
def merge(listOfSignals):
    """ Merges list of Signal objects into one object with multiple channels. """
    nItems = len(listOfSignals)
    output = listOfSignals[0]
    for iItem in range(1,nItems):
        output |= listOfSignals[iItem]
    return output
 

   
