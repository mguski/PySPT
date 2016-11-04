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
plt.figure()
t.plot_freq()

t

