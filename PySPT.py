# -*- coding: utf-8 -*-
"""
Created on Fri Oct 21 14:51:07 2016

@author: mguski


TODO:
 - make this a module or a package? 
 - channesl: channelNames, prin in console output, sub reference with .ch()
 - complete all operators
 - call '__new__', by default for obj1 = obj2 ?


"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

class giSignal:
    """Class to handle and plot signals """
    # Overloaded operators:
    #  * : multiply in freq domain (= cyclic convolve)
    # ** : multiply in time  domain (elementwise)
    # /  : division  in freq domain 
    # // : division in time domain
    # %  :
    # &  : append  in time domain
    # ^  : power in ?? domain
    # |  : merge channels       TODO
    def __init__(self, data, samplingRate, iqInterleaved=False, comment=''):
        
        if iqInterleaved:  # TODO: test with >1 channel
            data = data[0::2] + 1j* data[1::2]
        self._data = data
        self.samplingRate = samplingRate
        self._domain  = 'time'
        self.comment = comment



    @property    
    def nSamples(self):
        return self._data.shape[0]
        
#    @nSamples.setter
#   def nSamples(self, nSamplesNew):
#        if nSamplesNew < self._data.shape[0]:
#            self._data = self._data[0:nSamplesNew,:]
    @property
    def length(self):
        return self.nSamples / self.samplingRate
    
    @property
    def nChannels(self):
        dataShape = self._data.shape
        if len(dataShape) == 1:
            return 1
        else:
            return dataShape[1]
        
        
        
    
    @property    
    def timeVector(self):
        return np.array([ t / self.samplingRate for t in range(self.nSamples) ])
    
    @property     
    def freqVector(self):
        return np.fft.fftshift(np.fft.fftfreq(self.nSamples, 1/self.samplingRate ))
    
    @property 
    def timeData(self):
        if self._domain == 'time':
            return self._data
        elif self._domain == 'freq':
            self._data = np.fft.ifft(np.fft.ifftshift(self._data))
            self._domain = 'time'
            return self._data
        else:
            raise ValueError('Unknown domain. Choose time or freq')
    
    @timeData.setter
    def timeData(self, vec):
        self._data = vec
        self._domain = 'time'
    
    
    @property         
    def freqData(self):
        if self._domain == 'freq':
            return self._data
        elif self._domain == 'time':
            self._data = np.fft.fftshift(np.fft.fft(self._data))
            self._domain = 'freq'
            return self._data
        else:
            raise ValueError('Unknown domain. Choose time or freq')




    def plot_time(self, show=True, ax=None, dB=False):
       if ax == None:
          ax = plt.gca()
    
       ax.xaxis.set_major_formatter( FuncFormatter(giSignal._niceUnitPrefix_formatter) ) 

         
       if dB:
         plotData_real = 20*np.log10(np.absolute(np.real(self.timeData)))
         plotData_imag = 20*np.log10(np.absolute(np.imag(self.timeData)))
         yLabelString  = 'amplitude in dB'
       else:
         plotData_real = np.real(self.timeData)
         plotData_imag = np.imag(self.timeData)
         yLabelString  = 'amplitude'
    
       ax.plot(self.timeVector, plotData_real , label='real', marker=".")
       ax.plot(self.timeVector, plotData_imag , label='imag', marker=".")
    
       ax.grid(True)
       ax.set_xlim([self.timeVector[0], self.timeVector[-1]])
       ax.set
       plt.xlabel('time in s')
       plt.legend(loc=0)
       plt.ylabel(yLabelString)	
       plt.title(self.comment)
       if show:
          plt.show()        
        
    def plot_freq(self,  show=True, ax=None, dB=True ):
    
       if ax == None:
          ax = plt.gca()
       # TODO: check if this will work:
       # ax.xaxis.set_major_formatter( ticksFormatter ) # nice SI unit prefixes
       ax.xaxis.set_major_formatter( FuncFormatter(giSignal._niceUnitPrefix_formatter) ) 
 
       if dB:
         plotData_real = 20*np.log10(np.absolute(np.real(self.freqData)))
         plotData_imag = 20*np.log10(np.absolute(np.imag(self.freqData)))
         yLabelString  = 'magintude in dB'
       else:
         plotData_real = np.real(self.freqData)
         plotData_imag = np.imag(self.freqData)
         yLabelString  = 'magnitude'
    
       plt.plot(self.freqVector, plotData_real , label='real', marker=".")
       plt.plot(self.freqVector, plotData_imag , label='imag', marker=".")
    
       plt.grid(True)
       ax.set_xlim([self.freqVector[1], self.freqVector[-1]])

        # limit ylim range to 200 dB
       if dB: 
            current_yLimit = ax.get_ylim()
            ax.set_ylim((max(current_yLimit[0], current_yLimit[1]-200) , current_yLimit[1]))
            
       plt.xlabel('frequency in Hz')
       plt.legend(loc=0)
       plt.ylabel(yLabelString)	
       plt.title(self.comment)
       if show:
          plt.show()        

    def plot_time_freq(self, show=True,  time_dB=False, freq_dB=True   ):
          
           plt.figure()
           plt.subplot(121)
           self.plot_time(show=False, dB=time_dB )
        
           plt.subplot(122)
        
           self.plot_freq(show=False, dB=freq_dB )
           if show:
              plt.show()



    def __add__(self,value,  commentSign='+'):
        output = self.copy
        output.comment = output.comment[:-6] # remove "(copy)"
        output.__iadd__( value, commentSign)  # call __iadd__
        return output 
       
    def __iadd__(self, value, commentSign='+'):
        if type(value) is giSignal:
            # TODO: export to separate function, do in current domain, if domains equal
            if self.samplingRate != value.samplingRate:
                raise ValueError('Sampling rates do not match. Unable to add.')
            if self.nSamples != value.nSamples:
                raise ValueError('Number of samples do not match. Unable to add.')
            self.timeData += value.timeData
            self.comment = '(' + self.comment + ') '+ commentSign +' (' + value.comment + ')'
            return self
        elif isinstance(value, (np.int, float)):
            self.timeData +=  value # TODO: default is time domain? or use current domain?
            self.comment = '(' + self.comment + ') '+ commentSign + ' ' + str(abs(value))
            return self
        elif isinstance(value, (np.complex)):
            self.timeData = self.timeData + value # TODO: default is time domain? or use current domain?
            self.comment = '(' + self.comment + ') + ' + str((value))
            return self
        else:
            raise ValueError('Data type not defined with giSignal')            
            
            
    def __sub__(self, value):
        return self.__add__( -value,commentSign='-')
        
    def __isub__(self,value):
        return self.__iadd__( -value,commentSign='-')
        
    def __neg__(self):
        return self * -1

    def __mul__(self, value, commentSign='*'):
        if type(value) is giSignal:
            raise ValueError('TODO: think about domain!')

            
            # TODO: export to separate function, do in current domain, if domains equal
            if self.samplingRate != value.samplingRate:
                raise ValueError('Sampling rates do not match. Unable to multiply.')
            if self.nSamples != value.nSamples:
                raise ValueError('Number of samples do not match. Unable to multiply.')
            output = self.copy
            output.timeData += value.timeData
            output.comment = '(' + self.comment + ') '+ commentSign +' (' + value.comment + ')'
            return output
        elif isinstance(value, (np.int, float, np.complex)):
            output = self.copy
            output.timeData *= value 
            output.comment = '(' + self.comment + ') '+ commentSign + ' ' + str(value)
            return output
        else:
            raise ValueError('Data type not defined with giSignal')                
              
    @property
    def copy(self):    
        return giSignal(self.timeData.copy(), self.samplingRate, comment=self.comment +' (copy)' )

               
    def _niceUnitPrefix_formatter(value, pos):
        if value == 0:
            return '0'
        
        unitPrefixes = 'afpnµm kMGTPE'
        prefixIdx = np.floor(np.log10(np.absolute(value)) / 3)
        prefix = unitPrefixes[int(prefixIdx)+6]
        multiplyFactor = 10 ** (-prefixIdx*3)
        
        if np.mod(value*multiplyFactor, 1) == 0:
            strTemplate = '{:.0f}{}'
        else:
            strTemplate = '{}{}'
        outputStr = strTemplate.format(np.round(value*multiplyFactor*1.0e12)/1.0e12, prefix )
        return outputStr
        
        
        
    def __repr__(self):       
        strTemplate = '| {:>16} : {:<76} |\n'
        classContendStr  = '\n=='    
        classContendStr += '| {} Object: |{:=>78}'.format(self.__class__.__name__, '\n')
        classContendStr += strTemplate.format('', '' )    
        classContendStr += strTemplate.format( 'nSamples',      self.nSamples)
        
        samplingRateStr = giSignal._niceUnitPrefix_formatter(self.samplingRate,0)
        classContendStr += strTemplate.format( 'samplingRate',  samplingRateStr[:-1] + ' ' + samplingRateStr[-1] + 'Hz' )
        
        lengthStr = giSignal._niceUnitPrefix_formatter(self.length ,0)
        classContendStr += strTemplate.format( 'length',  lengthStr[:-1] + ' ' + lengthStr[-1] + 's' )
        classContendStr += strTemplate.format( 'nChannels',     self.nChannels)
        classContendStr += strTemplate.format( 'comment',     self.comment)
        classContendStr += strTemplate.format( '_domain',     self._domain)
        classContendStr += '{:=>100}'.format('\n') 
        return classContendStr
    
    
    # __str__ used for print(instance)   
    #def __str__(self):
    #    return 'where is this used??'
    
    # TODO: all all reverse operations
    def __radd__(self,value):
        return self.__add__(value)
    def __rsub__(self,value):
        return self.__add__(value)
        
    def __dict__(self):
        return ['plot_time',
             'plot_freq',
             'plot_time_freq',
             'timeData', 
             'timeVector',
             'freqData',
             'freqVector' 
             'samplingRate',
             '_data',
             '_domain',
             'nSamples',
             'length',
             'nChannels',
             'comment',
             'copy']

        
def generateSine(freq=30e3, samplingRate=1e6, nSamples=int(500e3), amplitude=1, phaseOffset=0):
    sine = giSignal(np.zeros(nSamples), samplingRate, comment='sine [{}Hz]'.format(giSignal._niceUnitPrefix_formatter(freq,0)))
    sine.timeData = np.sin(2*np.pi*freq*sine.timeVector+phaseOffset)
    return sine