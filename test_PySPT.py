# -*- coding: utf-8 -*-
"""
Created on Wed Nov 2 09:11:11 2016

@author: mguski
"""


# %% first time call
import PySPT
import numpy as np
import sys
import matplotlib.pyplot as plt
# %%

# reload file 
del sys.modules['PySPT'] 
import PySPT



sr = 10000
phi = [ 2*np.pi*30*t / sr for t in range(3002) ]
# vec = np.sin(2*np.pi*30*tVec)
vec = np.sin(phi)+0.00

s = PySPT.giSignal(vec, sr, comment='sine test signal')
r = PySPT.giSignal(vec*2, sr, comment='sine test signal 2')

#s.plot_time_freq()
# s.plot_freq()

# %% surface test if opertrs can be called without error

r = PySPT.generateSine()
s = PySPT.generateSine(freq=500)

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

del sys.modules['PySPT'] 
import PySPT

dummyData = np.r_[1:6]  /10  +1
dummyData2ch = np.vstack((dummyData, dummyData+1))

s_1ch = PySPT.giSignal(dummyData, 1, comment="one ch")
s_2ch =  PySPT.giSignal(dummyData2ch, 1, comment="two channels")


tmp = s_2ch | s_2ch
tmp =s_1ch | s_1ch
tmp =s_1ch | s_2ch

# set number of samples
s_2ch.nSamples = 3  # truncate
s_2ch.nSamples = 11 # add tailing zeros

# set length in seconds
s_2ch.length = 3.4
s_2ch.length = 11.5



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




