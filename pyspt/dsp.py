# -*- coding: utf-8 -*-
"""
Module contains collection of dsp functions.

"""
import numpy as np
from scipy import signal as scipySignal


# DSP
def time_shift(obj, shiftTime, cyclic=True):
    """ Applies time shift to signal that outSig(t) = inSig(t - shiftTime). """
    nSamples = np.round(shiftTime*obj.samplingRate)
    output = sample_shift(obj, nSamples, cyclic=cyclic)
    return output
        
def sample_shift(obj, nSamples, cyclic=True):
    """ Applies sample shift to signal that outSig[n] = inSig[n - nSamples]. """
    output = obj.copy 
    nSamples = np.round(nSamples) # rounc and convert to array
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
                tData_ref[iChannel,:] = np.roll(output.timeData[iChannel, :], -int(nSamples[iChannel]), axis=1)
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
       output.timeData = signal.resample_poly(output.timeData, num, den, axis=1, window=('kaiser', 5.0))
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
    output.freqData = np.multiply(output.freqData, 0.5*(np.sign(obj.freqVector)+1))
    return output   


      