# -*- coding: utf-8 -*-
"""
Created on Fri Nov 25 17:06:58 2016

@author: mguski
"""
import  matplotlib.pyplot as plt


class PlotGUI:
    """ Class to plot Signals in an interactive GUI.
            Shortcuts:
              t  : plot linear time domain 
              f  : plot frequency domain in dB
              s  : plot spectrogramm in dB
              d  : toggel betwenn linear and dB
              """
    plt.rcParams['keymap.fullscreen'] = ''
    plt.rcParams['keymap.save'] = ''
  #  plt.rcParams['toolbar'] = 'None' # no toolbar, it uses too much shortcuts
    # no mouse over x,y positions without toolbar? TODO: add mouse over event
    def __init__(self, signalObject, plotDomain='freq_dB'):
       # with mpl.rc_context({'toolbar':'None'}):  # no toolbar, it uses too much shortcuts
        self.fgh    = plt.figure(facecolor='0.99') # help to distinguish beween PlotGUI and normal plot
        plt.suptitle("PySPT GUI")
        self.axh    = plt.subplot(111)
        self.cid       = self.fgh.canvas.mpl_connect('key_press_event', self._keyCallback)
        self.signal = signalObject
        self.plotDomain = plotDomain
        self.currentDomain = 'None'
        self.updatePlot()
        plt.show()
        
    def _keyCallback(self, event):
        print('you pressed', event.key, event.xdata, event.ydata)
        if event.key == 't':
            self.plotDomain = 'time'
            self.updatePlot()
        elif event.key == 'f':
            self.plotDomain = 'freq_dB'
            self.updatePlot()
        elif event.key == 's':
            self.plotDomain = 'spec_dB'
            self.updatePlot()
        
        # toggle lin & dB axis    
        elif event.key == 'd': # or l? or l for legend?
            self.plotDomain            
            if self.plotDomain.endswith('_dB'):  # current dB => switch to lin
                self.plotDomain = self.plotDomain[:-3]
            else:
                self.plotDomain += '_dB'
            
            self.plotDomain
            self.updatePlot()
   #     elif event.key == 'h':
            # f freq
            # t time 
            # h help
            # cursors?
            # legend?
            # channel prev / next / all?
            # toggel dB / lin?
            # set axis limits
    #    elif event.key == 'down':
            
    
    def updatePlot(self):
        
        if self.currentDomain != self.plotDomain:
            # plt.cla() # cla() doesn't remove colorbar
            for iAxes in self.fgh.axes:
                self.fgh.delaxes(iAxes)
            self.axh = plt.subplot(111)    
                         
            # plt.draw() # feedback for user? doesn't work, TODO
            if self.plotDomain == 'freq_dB':
                self.signal.plot_freq(show=False, ax=self.axh, dB=True )
            elif self.plotDomain == 'freq':
                self.signal.plot_freq(show=False, ax=self.axh, dB=False)
            elif self.plotDomain == 'time_dB':
                self.signal.plot_time(show=False, ax=self.axh, dB=True )
            elif self.plotDomain == 'time':
                self.signal.plot_time(show=False, ax=self.axh, dB=False)
            elif self.plotDomain == 'spec_dB':
                self.signal.plot_spectrogram(show=False, ax=self.axh, dB=True)
            elif self.plotDomain == 'spec':
                self.signal.plot_spectrogram(show=False, ax=self.axh, dB=False)
            else:
                print("Unkown domain to plot: {}".format(self.plotDomain))
            
            plt.draw()    
    
