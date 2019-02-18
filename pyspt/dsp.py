# -*- coding: utf-8 -*-
"""
Module contains collection of dsp functions.

"""
import numpy as np
from scipy import signal as scipySignal


# DSP
def time_shift(obj, shiftTime, cyclic=True):
    """ Applies time shift to signal that outSig(t) = inSig(t + shiftTime). """
    nSamples = np.round(shiftTime*obj.samplingRate)
    output = sample_shift(obj, nSamples, cyclic=cyclic)
    return output
        
def sample_shift(obj, nSamples, cyclic=True):
    """ Applies sample shift to signal that outSig[n] = inSig[n + nSamples]. """
    output = obj.copy 
    nSamples = np.round(nSamples) # round and convert to array
    # nSamples one value => same shift for all channels
    if nSamples.size == 1:
        nSamples = int(nSamples)
        if cyclic:
            output.timeData = np.roll(output.timeData, -nSamples, axis=1)
        else:
            if nSamples < 0:  # add leading zeros
                output.timeData = np.concatenate((np.zeros((obj.nChannels, -nSamples)), obj.timeData_reference ), axis=1)
            else:   # truncate first part
                output.timeData = output.timeData[:, nSamples:]        
        return output
    # each channel individual shift    
    elif nSamples.size == obj.nChannels:
        tData_ref = output.timeData_reference
        for iChannel in range(obj.nChannels):
            if cyclic:
                tData_ref[iChannel,:] = np.roll(output.timeData[iChannel, :], -int(nSamples[iChannel]))
            else:
                obj.logger.error("time/sample_shift: only cyclic shifts are supported for individual shifts of channels.")  # TODO: smarter way than calling two functions with same input?
                raise ValueError("time/sample_shift: only cyclic shifts are supported for individual shifts of channels.")
        return output
    else:
        obj.logger.error("time/sample_shift: invalid input! size of shift time/samples has to be 1 or nSamples.")  # TODO: smarter way than calling two functions with same input?
        raise ValueError("time/sample_shift: invalid input! size of shift time/samples has to be 1 or nSamples.")
    
def resample(obj, newSamplingRate, method='fft', window=None): 
   """ Resamples signal to obtain newSamplingRate. Only fft method tested jet..."""
   output = obj.copy
   if method.lower() == 'fft':
       output.timeData = scipySignal.resample(output.timeData, int(output.nSamples/obj.samplingRate*newSamplingRate), axis=1, window=window)
       output.samplingRate = newSamplingRate
       return output
   elif method.lower() == 'poly':
       raise ValueError("methof poly not tested") # TODO: (implement and) test 
       from fractions import Fraction
       frac = Fraction(newSamplingRate/obj.samplingRate).limit_denominator(100)
       num = frac.numerator
       den = frac.denominator
       if num/den != newSamplingRate/obj.samplingRate:
           print("resampling not exact, error {} % ")
       output.timeData = scipySignal.resample_poly(output.timeData, num, den, axis=1, window=('kaiser', 5.0))
       output.samplingRate *= num/den
       return output
   else:
       raise ValueError("unknown vaule for method: {} (fft or poly possible)".format(method))
       
def frequency_mixer(inputSignal, mixingFrequency):
    """ Apply up/down mixing with mixingFrequency. """
    outputSignal = inputSignal.copy
    outputSignal.timeData = np.multiply( outputSignal.timeData, np.exp(1j*2*np.pi*mixingFrequency*outputSignal.timeVector))
    return outputSignal
   
def hilbert_transform(obj):
    """ The Hilbert transform derives the analytic representation of a real signal. """
    output = obj.copy
    output.freqData = output.freqData * 0.5*(np.sign(obj.freqVector)+1)
    return output   

def x_fade_spk(in_a, in_b, fade_vec):

    if in_a.samplingRate != in_b.samplingRate:
        print("Error: sampling rates not equal")

    if in_a.nSamples != in_b.nSamples:
        print("Error: nSamples not equal")

    f0_idx = in_a.freq2index( fade_vec[0])
    f1_idx = in_a.freq2index( fade_vec[1])

    nBins = f1_idx - f0_idx
    winFcn = np.hanning(nBins*2+1)
    fade_in = winFcn[:nBins+1]
    fade_out = winFcn[nBins:]

    # TODO multiple channels

    output = in_a.copy
    tmp_spk = output.freqData
    tmp_spk[:, f0_idx:f1_idx+1] *= fade_out
    tmp_spk[:, f0_idx:f1_idx + 1] += fade_in * in_b.freqData[:, f0_idx:f1_idx + 1]
    tmp_spk[:, f1_idx:] = in_b.freqData[:, f1_idx:]
    output.freqData = tmp_spk
    return output


def invert_spk(audio_object, freq_vec, beta=10**(-200/20)):

    # b = audio_object.copy * 0 + beta
    b = audio_object.copy
    b.freqData = b.freqData*0 + beta
    # a = audio_object.copy * 0 + 1
    a = audio_object.copy
    a.freqData = a.freqData * 0 + 1


    f_low = freq_vec[0]
    f_high = freq_vec[1]

    epsilon = x_fade_spk(a, b, [f_low / np.sqrt(2), f_low])
    if f_high < min(f_high * np.sqrt(2), epsilon.samplingRate / 2):
        epsilon = x_fade_spk(epsilon, a, [f_high, min(f_high*np.sqrt(2), epsilon.samplingRate/2)])


    epsilon.freqData = epsilon.freqData * np.max(np.abs(audio_object.freqData))**2 * 50 / 100
    # epsilon = epsilon * max(np.abs(audio_object.freqData))**2 *50 /100

    tmp_spk = audio_object.freqData

    # kirkeby regularization
    tmp_spk = np.conj(tmp_spk) / (np.conj(tmp_spk) * tmp_spk + epsilon.freqData)
    output = audio_object.copy
    output.freqData = tmp_spk
    return output

def normalize(audio_object):
    audio_object.timeData = audio_object.timeData / np.max(np.abs(audio_object.timeData ))
    return audio_object







      
