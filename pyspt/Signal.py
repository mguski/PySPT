# -*- coding: utf-8 -*-
"""
Created on Fri Nov 25 15:02:42 2016

@author: mguski

TODOs:
 - channels: channelNames, print in console output, sub reference with .ch()
 - complete all operators
 - call '__new__', by default for obj1 = obj2 ?
 - obj.addChannel() or obbj.appendChannel()
 - possibility to create empty Signal (i.e. to use append in loop)
 - tuncate channels names in __repr__
 - should Signal.copy be renamed to deepcopy, to be in accordance with python definitions?
 - giObj.freqData[0] = np.zeros(1) doen't work but raises no error
 - add channelUnits
 - add signalType: 'power' or 'energy' => add fftNorm, change rms()

"""
 

import numpy as np
import logging
from scipy import signal as scipySignal
import matplotlib.pyplot as plt

from matplotlib.ticker import FuncFormatter
from cycler import cycler

from .PlotGUI import PlotGUI


class Signal:
    """Class to handle signals including meta data.
    
        Internal the signal data is stored in only one domain (time or frequency)
        and is transformed if necessary. Multiple operators are overloaded and can 
        be used with two objects or scalar values:
        
           Overloaded operators:
             +   : addition     ( objA + objB or objA + 10)
             -   : subtraction  ( objA - objB or objA - 10)
             |   : merge of channel  (twoChannlObj = oneChObj | otherChObj )
             *   : multiplication with scalar
             
             NOT IMPLEMENTED
             *   : multiplication in freq domain (= cyclic convolve) 
             **  : multiply in time  domain (elementwise)  	pow(a, b)
             /   : division  in freq domain 
             //  : division in time domain   floordiv
             %   :
             &   : append  in time domain       and_(a, b)
             ^   : power in ?? domain
             Right Shift	a >> b	rshift(a, b)
             Left Shift	a << b	lshift(a, b)
             Indexing	obj[k]	getitem(obj, k)
             Indexed Assignment	obj[k] = v	setitem(obj, k, v)
             Negation (Arithmetic)	- a	neg(a)
    """
    def __init__(self, data, samplingRate, iqInterleaved=False, comment=''):
        # np.concatenate if type(data) is list?
        data = np.array(np.atleast_2d(data))
        if iqInterleaved:  
            data = data[:,0::2] + 1j* data[:,1::2]
                
        self._data         = data
        self.samplingRate  = samplingRate
        self._domain       = 'time'
        self.comment       = comment
        self._channelNames = ["ch {}".format(iCh) for iCh in range(self.nChannels)]
        self.logger        = logging.getLogger("Signal")


    @property    
    def nSamples(self):
        """ Number of samples in signal for each channel. Setting this value results in truncation or zero padding."""
        return self._data.shape[1]
        
    @nSamples.setter
    def nSamples(self, nSamplesNew):
        nSamplesNew = int(np.round(nSamplesNew))
        if nSamplesNew < self.nSamples: # cropping signal
            self.timeData = np.delete(self.timeData, range(nSamplesNew,self.nSamples), 1)
        elif nSamplesNew > self.nSamples: # adding zeros
            self.timeData = np.append(self.timeData, np.zeros((self.nChannels, nSamplesNew - self.nSamples), dtype=self._data.dtype), 1)
            
    @property
    def length(self):
        """ Length of signal in seconds. Setting this value results in truncation or zero padding."""
        return self.nSamples / self.samplingRate

    @length.setter
    def length(self, newLength):
        self.nSamples = np.round(newLength * self.samplingRate)

    
    @property
    def nChannels(self):
        """ Number of channels. """
        return self._data.shape[0]
        
    
#    @property
#    def ch(self, channelNumber):
#        channelNumber = np.array(channelNumber)
#        if np.any(channelNumber > self.nChannels):
#            print('Only {} channels. Index out of bounds for {}'.fomrat(self.nChannels, channelNumber))
#            return
#        output = self.copy
#        output._data = output._data[channelNumber]
#        output.channelNames = [output.channelNames[i] for i in channelNumber]
#        return output

    @property
    def channelNames(self):
        """ List of strings to describe each channel. """
        while (len(self._channelNames) < self.nChannels):
            self._channelNames.append("")
        return self._channelNames         
    
    @channelNames.setter
    def channelNames(self, names):
        self._channelNames = names

        
    @property    
    def timeVector(self):
        """ Time vector in seconds. Calculated each time using nSamples and samplingRate."""
        return np.array([ t / self.samplingRate for t in range(self.nSamples) ])
    
    @property     
    def freqVector(self):
        """ Frequency vector in Hz. Calculated each time using nSamples and samplingRate."""
        return np.fft.fftshift(np.fft.fftfreq(self.nSamples, 1/self.samplingRate ))
        
    def time2index(self, time):
        """ Returns the index of the sample to the given time."""
        if time > self.length:
            self.logger.warning("time2index: requested time ({}) is larger than signal length ({})! Returning nSamples.".format(time, self.length))
            return self.nSamples
        if time < 0:
            self.logger.warning("time2index: requested time ({}) is negative! Returning zero.".format(time))
            return 0            
        return int(np.round(time * self.samplingRate))
        
    def freq2index(self, freq):
        """ Returns the index of the sample to the given frequency."""
        if freq > self.samplingRate / 2 :
            self.logger.warning("freq2index: requested frequency ({}) is higher than half sampling rate ({})! Returning half sampling rate.".format(freq, self.samplingRate/2))
            return self.samplingRate / 2
        if freq <  -self.samplingRate / 2 :
            self.logger.warning("freq2index: requested frequency ({}) is lower than half sampling rate ({})! Returning minus half sampling rate.".format(freq, self.samplingRate/2))
            return -self.samplingRate / 2
        return int(np.argmin(abs(self.freqVector - np.array(freq)))) # TODO: calculate directly without generating freqVector
        


    
    # convert internal data to frequency domain
    # freqData is effective value (not amplitude) for power signals (energy not supported TODO )
    def fft(self):
        """ Function transforms internal _data into frequency domain (if necessary). 
            Applies  fft norm for power signals so that spectrum gives rms values.
            """
        if self._domain == 'time':
            self._data = np.fft.fftshift(np.fft.fft(self._data), axes=1) / self.nSamples / np.sqrt(2) # TODO: don't scale DC value??
            self._domain = 'freq'
            self.logger.info('fft: changing _domain from time to freq')
        elif self._domain == 'freq':
            self.logger.debug('fft: _domain is already freq, doing nothing')
        else:
            self.logger.error('fft: Unknown domain: {}. Choose time or freq'.format(self._domain))            
            raise ValueError('Unknown domain: {}. Choose time or freq'.format(self._domain))        
    
    # convert internal data into time domain
    def ifft(self):
        """ Function transforms internal _data into time domain (if necessary). """
        if self._domain == 'freq':
            self._data = np.fft.ifft(np.fft.ifftshift(self._data, axes=1)) * self.nSamples * np.sqrt(2) # TODO:don't scale DC value?
            self._domain = 'time'
            self.logger.info('ifft: changing _domain from freq to time')
        elif self._domain == 'time':
            self.logger.debug('fft: _domain is already time, doing nothing')
        else:
            self.logger.error('fft: Unknown domain: {}. Choose time or freq'.format(self._domain))            
            raise ValueError('Unknown domain: {}. Choose time or freq'.format(self._domain))      

    
    
    @property 
    def timeData(self):
        """ Returns copy of signal data in time domain. Output is array of size nChannels x nSamples. """
        self.ifft()
        return self._data.copy()

    @property 
    def timeData_reference(self):
        """ Returns reference of signal data in time domain. Output is array of size nChannels x nSamples. """
        self.ifft()
        return self._data
 
    @timeData.setter
    def timeData(self, vec):
        self._data = np.atleast_2d(vec.copy())
        self._domain = 'time'
    
    
    @property         
    def freqData_reference(self):
        """ Returns reference of signal data in frequency domain. Output is array of size nChannels x nSamples. """
        self.fft()
        return self._data
        
    @freqData_reference.setter         
    def freqData_reference(self, freqData):
        self._data = np.atleast_2d(freqData)
        self._domain = 'freq'       
        
        
    @property         
    def freqData(self):
        """ Returns copy of signal data in frequency domain. Output is array of size nChannels x nSamples. """
        self.fft()
        return self._data.copy()

    @freqData.setter
    def freqData(self, vec):
        self._data = np.atleast_2d(vec.copy())
        self._domain = 'freq'


    def plot_time(self, show=True, ax=None, dB=False):
       """ Plots signal in time domain (using PlotGUI class)."""
       if ax is None:   
           return PlotGUI(self, plotDomain=['time', 'time_dB'][dB])
    
       plotData = self.timeData
       xValues  = self.timeVector
       
       onlyRealValues = np.isrealobj(plotData) or np.isreal(plotData).all() # first test for real object to be fatser
       if not onlyRealValues:
           plotData = np.reshape(np.hstack((np.real(plotData),np.imag(plotData))), (self.nChannels*2,self.nSamples))
           legendList = [ chName+post for chName in self.channelNames for post in [' (real)' , ' (imag)' ]]
       else:
           legendList = self.channelNames

       if dB:
         plotData = 20*np.log10(np.absolute(plotData))
         yLabelString  = 'amplitude in dB'
       else:
         yLabelString  = 'amplitude'    
    
       xLabelString = 'time in s'
       
       self._plot_data(ax, xValues, plotData, xLabelString, yLabelString, legendList, show, onlyRealValues, None)
       
       
    def plot_freq(self,  show=True, ax=None, dB=True ):
       """ Plots signal in frequency domain (using PlotGUI class)."""
       if ax is None:   
           return PlotGUI(self, plotDomain=['freq', 'freq_dB'][dB])
           
       plotData = self.freqData
       xValues  = self.freqVector       
 
       onlyRealValues = dB or np.isrealobj(plotData) or np.isreal(plotData).all() # first test for real object to be fatser

       if not onlyRealValues and not dB:
           plotData = np.reshape(np.hstack((np.real(plotData),np.imag(plotData))), (self.nChannels*2,self.nSamples))
           legendList = [ chName+post for chName in self.channelNames for post in [' (real)' , ' (imag)' ]]
       else:
           legendList = self.channelNames 
 
       if dB:
         plotData = 20*np.log10(np.absolute(plotData))
         yLabelString  = 'magintude in dB'
       else:
         yLabelString  = 'magintude' 
         
       xLabelString = 'frequency in Hz'
       
       if dB: 
           yLimRange = 200
       else:
           yLimRange = None
           
       self._plot_data(ax, xValues, plotData, xLabelString, yLabelString, legendList, show, onlyRealValues, yLimRange)


          
       
       
    # internal function to plot the data
    def _plot_data(self, ax, xValues, plotData, xLabelString, yLabelString, legendList, show, onlyRealValues, yLimRange):
       ax.xaxis.set_major_formatter( FuncFormatter(Signal._niceUnitPrefix_formatter) ) 

       defaultColorCycle = ['b', 'g', 'r', 'y']
       lineStyles = ['-', '--']
       if onlyRealValues:
           cycler2use = (cycler('color', defaultColorCycle ) )
       else:
           cycler2use = (cycler('color', [ c  for c in defaultColorCycle for i in range(2)]) + cycler('linestyle', lineStyles*len(defaultColorCycle)))
       ax.set_prop_cycle(cycler2use)
       
       lineHandles = ax.plot(xValues, plotData.T  , marker=".")
       
       if onlyRealValues:
           self.PlotGUI_handle.channelHandleList = lineHandles
       else:
           self.PlotGUI_handle.channelHandleList  = [ [lineHandles[2*iCh], lineHandles[2*iCh+1]]  for iCh in range(int(len(lineHandles)/2)) ]           
    
       ax.grid(True)
       ax.set_xlim([xValues[0], xValues[-1]])
       
       plt.xlabel(xLabelString)
       self.PlotGUI_handle.legendHandle = plt.legend(legendList, loc=0)
       plt.ylabel(yLabelString)	
       plt.title(self.comment)
       
       if yLimRange:
            current_yLimit = ax.get_ylim()
            ax.set_ylim((max(current_yLimit[0], current_yLimit[1]-yLimRange) , current_yLimit[1]))

       
       if show:
          plt.show()        
 
       
   
       
       
    def plot_spectrogram(self,  show=True, ax=None, dB=True, nSamplesWindow='auto', windowType=('tukey', 0.25) ):
       """ Plots signal as spectrogram (using PlotGUI class)."""
       if ax is None:   
           return PlotGUI(self, plotDomain=['spec', 'spec_dB'][dB])

       ax.xaxis.set_major_formatter( FuncFormatter(Signal._niceUnitPrefix_formatter) ) 
       ax.yaxis.set_major_formatter( FuncFormatter(Signal._niceUnitPrefix_formatter) ) 
       if nSamplesWindow == 'auto': # TODO:  convert to lower case
           nSamplesWindow = np.round(self.nSamples/100) # also limit by min/max
           

       f, t, Sxx = scipySignal.spectrogram(self.timeData, self.samplingRate, nperseg=nSamplesWindow, window=windowType )
       
       f   = np.fft.fftshift(f) # fftshift because pcolor has a problem with not monotonous freqVector       
       Sxx = np.fft.fftshift(Sxx)
       
       cLabelString  = 'magnitude'
       if dB:
         Sxx = 20*np.log10(np.absolute(Sxx)) # TODO: check if Sxx is amplitude and not power
         cLabelString  = 'magintude in dB'
    
       plt.pcolormesh(t, f, Sxx.squeeze(), vmax=Sxx.max(), vmin=np.max((Sxx.min(),Sxx.max()-200)) ) 
       ax.axis((t.min(), t.max(), f.min(), f.max() ))
       cBar = plt.colorbar()
       
       # labels
       plt.ylabel('Frequency [Hz]')                                             # limit dynamic range to 200 dB
       plt.xlabel('Time [sec]')
       cBar.ax.set_ylabel(cLabelString, rotation=90)
       plt.title(self.comment)
       
       if show:
          plt.show()           
          
    def plot_time_freq(self, show=True,  time_dB=False, freq_dB=True ):
        """ Plots signal in time and frequency domain (using PlotGUI class)."""
        plt.figure()
        plt.subplot(121)
        self.plot_time(show=False, dB=time_dB )
    
        plt.subplot(122)
    
        self.plot_freq(show=False, dB=freq_dB )
        if show:
           plt.show()

    def __add__(self,value,  commentSign='+'):
        output = self.copy
        output.__iadd__( value, commentSign)  # call __iadd__
        return output 
       
    def __iadd__(self, value, commentSign='+'):
        if type(value) is Signal:
            # TODO: export to separate function, do in current domain, if domains equal
            if self.samplingRate != value.samplingRate:
                raise ValueError('Sampling rates do not match. Unable to add.')
            if self.nSamples != value.nSamples:
                raise ValueError('Number of samples do not match. Unable to add.')
            self.timeData = self.timeData + value.timeData
            self.comment = '(' + self.comment + ') '+ commentSign +' (' + value.comment + ')'
            return self
        elif isinstance(value, (np.int, float)):
            self.timeData = self.timeData + value # TODO: default is time domain? or use current domain?
            self.comment = '(' + self.comment + ') '+ commentSign + ' ' + str(abs(value))
            return self
        elif isinstance(value, (np.complex)):
            self.timeData = self.timeData + value # TODO: default is time domain? or use current domain?
            self.comment = '(' + self.comment + ') + ' + str((value))
            return self
        else:
            raise ValueError('Data type not defined with Signal')            
            
            
    def __sub__(self, value):
        return self.__add__( -value,commentSign='-')
        
    def __isub__(self,value):
        return self.__iadd__( -value,commentSign='-')
        
    def __neg__(self):
        return self * -1

    def __mul__(self, value, commentSign='*'):
        if type(value) is Signal:
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
            output._data = output._data  * value 
            output.comment = '(' + self.comment + ') '+ commentSign + ' ' + str(value)
            return output
        else:
            raise ValueError('Data type not defined with Signal')                
  
  

    def __or__(self, secondObj):
        """ Merge two objects into one with multiple channels. c = a | b """
        # _checkCompatibility(self, secondObj) nSamples, samplingRate, sync domains?
        output = self.copy
        output._sync_domains(secondObj)
        output._data = np.vstack((output._data, secondObj._data.copy()))
        output._channelNames = output._channelNames + secondObj._channelNames
        if output.comment != secondObj.comment:
            output.comment = "(" + output.comment + ") merged with (" + secondObj.comment + ")"
        return output
        
    def _sync_domains(self, obj2):
        """ Changes the domain of calling object to second object. """
        if self._domain != obj2._domain:
            if obj2._domain == "time":
                self.ifft()
            elif obj2._domain == "freq":
                self.fft()
            else:
                raise ValueError("Unknown domain: {}. Can not sync domains.".format(self._domain))
            

    def __getitem__(self, index):
        # TODO: reference or copy? refernece possible? obj[2] *=2 ??
        output = self.copy
        
        
        
     
    def sum(self):
         """ Sums up all channel of one object. """
         if self.nChannels > 1:
             self._data = np.sum(self._data, axis=0)
         else:
             self.logger.warning('sum is doing nothing, only one channel')
    
    
    def rms(self):
        """ Calculates root mean square (for continous waveform). """
        if self._domain == 'freq':
            # time: sqrt( 1/T *int(|s(t)|**2)) = sqrt( 1/T * sum(|s(n) * deltaT |**2)) with deltaT = 1 / samplingRate
            rmsValues  = np.sqrt(np.sum(np.absolute(np.power(self._data ,2)), axis=1 )/self.length) 
             #            np.sqrt(np.sum(np.array(np.absolute(tmp.freqData) )**2 )*tmp.samplingRate/tmp.nSamples)
            self.logger.info('rms in time domain')
        elif self._domain == 'time':
            rmsValues  = np.sqrt(np.sum(np.absolute(np.power(self._data ,2)), axis=1)/self.length/self.samplingRate)
             #            np.sqrt(np.sum(np.absolute(np.power(tmp._data  ,2)), axis=1 )/tmp.length /tmp.samplingRate )
            self.logger.info('rms in freq domain')
        else:
            raise ValueError('Unknown domain') 
           
        return np.array(rmsValues).squeeze()

#np.sqrt(np.sum(np.array(np.absolute(tmp.freqData) )**2 )*tmp.samplingRate/tmp.nSamples)
    @property
    def copy(self):
        """ Returns a deep(?) copy of the object."""
        return Signal(self.timeData.copy(), self.samplingRate, comment=self.comment ) # TODO: keep upto date: channelNames

               
    def _niceUnitPrefix_formatter(value, pos):
        """ Formater function to retun string with SI unit prefixes (kilo, Mega,...) """
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
        """ Shows content summary for console output. """
        strTemplate = '| {:>16} : {:<76} |\n'
        classContendStr  = '\n=='    
        classContendStr += '| {} Object: |{:=>78}'.format(self.__class__.__name__, '\n')
        classContendStr += strTemplate.format('', '' )    
        classContendStr += strTemplate.format( 'nSamples',      self.nSamples)
        
        samplingRateStr = Signal._niceUnitPrefix_formatter(self.samplingRate,0)
        classContendStr += strTemplate.format( 'samplingRate',  samplingRateStr[:-1] + ' ' + samplingRateStr[-1] + 'Hz' )
        
        lengthStr = Signal._niceUnitPrefix_formatter(self.length ,0)
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