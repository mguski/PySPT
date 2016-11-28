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
import importlib
%matplotlib
# %%

# reload file 
del sys.modules['pyspt'] 
import pyspt
help(pyspt)


# %%

testSig = np.array(range(80)).reshape((8,10))
t = pyspt.Signal(testSig, 1)


plt.plot(testSig.T)


# %%



del sys.modules['pyspt'] 
import pyspt

defaultColorCycle = ['r', 'g', 'b', 'y']
lineStyles = ['-', '--']


imagCycler = (cycler('color', [ c  for c in defaultColorCycle for i in range(2)]) + cycler('linestyle', lineStyles*len(defaultColorCycle)))
ax = plt.subplot(111)
ax.set_prop_cycle(imagCycler)

lineHandles = plt.plot(testSig.T)
# %%


#del sys.modules[] 
#import pyspt

#importlib.reload(pyspt)
import pyspt
import numpy as np

testSig = np.array(range(40)).reshape((4,10))
t = pyspt.Signal(testSig*(1+1j*0.9), 1)
s = pyspt.generate_sine()
s.plot_time()
#t = pyspt.Signal(testSig, 1)
#t.plot_freq()

