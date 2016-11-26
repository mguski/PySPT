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

a = t - r
a = r - t

# %% how to organize multiple channels ??
oneCh = np.atleast_2d(np.r_[1:6]  /10  +1)
print("one chanel:\n {}\n  shape: {}\n".format(oneCh, oneCh.shape))

twoCh_v1 = np.atleast_2d((np.vstack((oneCh, oneCh+1))))
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

