# -*- coding: utf-8 -*-
"""
Created on Wed Nov 2 09:11:11 2016

@author: mguski
"""



# %% first time call
import pyspt
import numpy as np
import sys
import matplotlib.pyplot as plt
# %%

# reload file 
del sys.modules['pyspt'] 
import pyspt
help(pyspt)

# %%


sr = 10000
phi = [ 2*np.pi*30*t / sr for t in range(3002) ]
# vec = np.sin(2*np.pi*30*tVec)
vec = np.sin(phi)+0.00

s = pyspt.Signal(vec, sr, comment='sine test signal')
r = pyspt.Signal(vec*2, sr, comment='sine test signal 2')

#s.plot_time_freq()
# s.plot_freq()

# %% copy / reference 
r = pyspt.generate_sine()
t = r.copy # return a copy

if  not (r.timeData == t.timeData).all():
    raise ValueError('Copy results in different timeData values')

if  r.timeData_reference is t.timeData_reference:
    raise ValueError('obj.copy returns only reference!')

t = r # now t is only a new reference
     
if not r.timeData_reference is t.timeData_reference:
    raise ValueError('error a = b  returns no reference!')

# %%  timevector, freqVector, freq2index, time2index

r = pyspt.generate_sine()

r.timeVector
r.freqVector

testIdx = 1234
if r.time2index(r.timeVector[testIdx]) != testIdx:
    raise ValueError('time2index did not result in correct value')
if r.freq2index(r.freqVector[testIdx]) != testIdx:
    raise ValueError('freq2index did not result in correct value')


# %% fft / ifft 

r = pyspt.generate_sine() | pyspt.generate_sine(freq=10e3)
t = r.copy

t.fft()
t.ifft()
a = t - r
if  np.max(np.absolute(a.timeData)) > 1e-14:
    
    a.plot_time()
    raise ValueError('fft => ifft does not result in same values!')


a = r - t


# %% check rms() results
tmp = pyspt.generate_sine(amplitude=1)
if tmp.rms() - np.sqrt(0.5) > 1e-15:
    raise ValueError('rms in time domain wrong')
tmp.fft()
if tmp.rms() - np.sqrt(0.5) > 1e-15:
    raise ValueError('rms in freq domain wrong')


# %% surface test if opertrs can be called without error

r = pyspt.generate_sine()
s = pyspt.generate_sine(freq=500)

t = s.copy

t = s + r
t = s + 2
t = s + 2.5
t = 2 + s

t += s
t += 2
t += 2.5


t = s - r
t = s - 2
t = s - 2.5
t = 2 - s

t -= s
t -= 2
t -= 2.5

t = s*2
t = -s

t = r + s*2
plt.figure()
t.plot_time()

t.plot_freq()

t.plot_spectrogram()


# %%



dummyData = np.r_[1:6]  /10  +1
dummyData2ch = np.vstack((dummyData, dummyData+1))

s_1ch = pyspt.Signal(dummyData, 1, comment="one ch")
s_2ch =  pyspt.Signal(dummyData2ch, 1, comment="two channels")


tmp = s_2ch | s_2ch
tmp =s_1ch | s_1ch
tmp =s_1ch | s_2ch


tmp.sum() # sum up all channels
tmp.sum() # just one channel to sum up

# set number of samples
s_2ch.nSamples = 3  # truncate
s_2ch.nSamples = 11 # add tailing zeros

# set length in seconds
s_2ch.length = 3.4
s_2ch.length = 11.5


# %% time shifting
% matplotlib

plt.figure()
sig =  pyspt.Signal(range(101),1)
sig |= sig
sig.plot_time(ax=plt.subplot(511))
plt.title('original')

sig2 = pyspt.dsp.sample_shift(sig, 20, cyclic=True)
sig2.plot_time(ax=plt.subplot(523))
plt.title('cyclic shift +20 samples')
sig2 = pyspt.dsp.sample_shift(sig, 20, cyclic=False)
sig2.plot_time(ax=plt.subplot(524))
plt.title('shift +20 samples')

sig2 = pyspt.dsp.sample_shift(sig, -20, cyclic=True)
sig2.plot_time(ax=plt.subplot(525))
plt.title('cyclic shift -20 samples')
sig2 = pyspt.dsp.sample_shift(sig, -20, cyclic=False)
sig2.plot_time(ax=plt.subplot(526))
plt.title('shift -20 samples')

sig2 = pyspt.dsp.time_shift(sig, 40, cyclic=True)
sig2.plot_time(ax=plt.subplot(527))
plt.title('cyclic shift 40 sec')
sig2 = pyspt.dsp.time_shift(sig, 40, cyclic=False)
sig2.plot_time(ax=plt.subplot(528))
plt.title('shift 40 sec')


sig2 = pyspt.dsp.time_shift(sig, -40, cyclic=True)
sig2.plot_time(ax=plt.subplot(529))
plt.title('cyclic shift -40 sec')
sig2 = pyspt.dsp.time_shift(sig, -40, cyclic=False)
sig2.plot_time(ax=plt.subplot(5,2,10))
plt.title('shift -40 sec')

# %%

del sys.modules['pyspt'] 
import pyspt

n = pyspt.generate_noise()


# %%
del sys.modules['pyspt'] 
import pyspt


sig =  pyspt.Signal(range(101),1)
sig |= sig

sig2 = pyspt.dsp.time_shift(sig, [-10, 10], )
sig2.plot_time()
# %% test merge of list with signals

allSig = []
for iSig in range(10):
    allSig.append(pyspt.generate_sine(freq=10*iSig+10, samplingRate=500, nSamples=1e3))

multCh = pyspt.merge(allSig)


# %%

sine = pyspt.generate_sine(freq=3e3, samplingRate=10e3, nSamples=10e3)

sineH = pyspt.dsp.hilbert_transform(sine)
sine.plot_freq()
# %% test resampling

sig = pyspt.generate_sine() + pyspt.generate_noise()*(1/80)

sig3 = pyspt.dsp.resample(sig, 500e3)
sig3 = pyspt.dsp.resample(sig, 2e6)


# %% frequency mixer

mixingFreq = 200e3
inputSignal = pyspt.generate_sine() #+ pyspt.generateNoise()*(1/80)
outputSignal2 = pyspt.dsp.frequency_mixer(inputSignal, mixingFreq)
outputSignal2.plot_freq()


# %% how to organize multiple channels ??
oneCh = np.r_[1:6]  /10  +1
print("one chanel:\n {}\n  shape: {}\n".format(oneCh, oneCh.shape))

twoCh_v1 = np.vstack((oneCh, oneCh+1))
print("two chanels version 1:\n {}\n  shape: {}\n".format(twoCh_v1, twoCh_v1.shape))
# - shape changes
# + console output looks intuitive
# + direct access k-th ch with self._data[k-1]  twoCh_v1[1] 


twoCh_v2 = np.vstack((oneCh, oneCh+1)).T
print("two chanels version 2:\n {}\n  shape: {}\n".format(twoCh_v2, twoCh_v2.shape))
# + first index of shape is always nSamples
# - console output missleading

"""
# _data, time/freq-Data as matrix or array???

# pro matrix
 - for arrays: nSamples not at same posioon in shape for one or more channels
 - for arrays: console output lines up all n-th samples and not signale channels


# pro array
 - output of most functions is array
   i.e. <array> = np.fft(<matrix>)
 - elementwise operations nicer:
   sigAtPoint.freqData[iAntenna] *= np.exp(-1j*2*np.pi*freqVec*timeDiff_vector[iAntenna])
   sigAtPoint.freqData[iAntenna] = np.multiply(sigAtPoint.freqData[iAntenna], np.exp(-1j*2*np.pi*freqVec*timeDiff_vector[iAntenna]))
 - freqVector, timeData, rms also return arrays
   
   
"""

