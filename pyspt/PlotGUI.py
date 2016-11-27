# -*- coding: utf-8 -*-
"""
Created on Fri Nov 25 17:06:58 2016

@author: mguski
"""
import  matplotlib.pyplot as plt


class PlotGUI:
    """    Class to plot Signals in an interactive GUI.    
    
        Shortcuts:
              d  : toggel between linear and dB
              l  : toggel visibility of legend  
              h  : show help
              
        [change domain]    
              t  : plot linear time domain 
              f  : plot frequency domain in dB
              s  : plot spectrogramm in dB
              
        [channels]                  
              *  : show next channel
              /  : show previous channel
              a  : show all channels

          """
    plt.rcParams['keymap.fullscreen'] = '' #:f               # toggling
    plt.rcParams['keymap.save'] = ''       # s saving current figure
    plt.rcParams['keymap.yscale'] = ''     # l                   # toggle scaling of y-axes ('log'/'linear')

#keymap.home : h, r, home            # home or reset mnemonic
#keymap.back : left, c, backspace    # forward / backward keys to enable
#keymap.forward : right, v           #   left handed quick navigation
#keymap.pan : p                      # pan mnemonic
#keymap.zoom : o                     # zoom mnemonic            
#keymap.quit : ctrl+w, cmd+w         # close the current figure
#keymap.grid : g                     # switching on/off a grid in current axes
#keymap.yscale : 
#keymap.xscale : L, k                # toggle scaling of x-axes ('log'/'linear')
#keymap.all_axes : a                 # enable all axes
  #  plt.rcParams['toolbar'] = 'None' # no toolbar, it uses too much shortcuts
    # no mouse over x,y positions without toolbar? TODO: add mouse over event
    def __init__(self, signalObject, plotDomain='freq_dB'):
       # with mpl.rc_context({'toolbar':'None'}):  # no toolbar, it uses too much shortcuts
        self.fgh    = plt.figure(facecolor='0.99') # help to distinguish beween PlotGUI and normal plot
        plt.suptitle("PySPT GUI")
        self.axh    = plt.subplot(111)
        self.channelHandleList = []
        self.legendHandle      = []
        self.currentChannel = 'all'
        self.cid       = self.fgh.canvas.mpl_connect('key_press_event', self._keyCallback)
        self.signal = signalObject
        self.signal.PlotGUI_handle= self
        self.plotDomain = plotDomain
        self.currentDomain = 'None'
        self.helpTextBox = None
        
        self.updatePlot()
        plt.show()
        
    def _keyCallback(self, event):
       # print('you pressed', event.key, event.xdata, event.ydata)
    
        # if helptextBox is shown, just close it with any key
        if self.helpTextBox is not None:
            self.helpTextBox.remove()
            self.helpTextBox = None
            if self.currentChannel == 'all':
                self.legendHandle.set_visible(True)
            return
    
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
        elif event.key == '*': # plot next channel         
            if self.currentChannel == "all":
                self.currentChannel = 0
            else:
                self.currentChannel = (self.currentChannel + 1) %  len(self.channelHandleList )         
            self.update_visible_channels()  
            
        elif event.key == '/':   # plot prev channel     
            if self.currentChannel == "all":
                self.currentChannel = len(self.channelHandleList ) - 1
            else:
                self.currentChannel = (self.currentChannel - 1) %  len(self.channelHandleList )         
            self.update_visible_channels()              
            
        elif event.key == 'a': # plot all channels          
            self.currentChannel = "all"               
            self.update_visible_channels()
            
        elif event.key == 'h':
            self.show_help()
            
        elif event.key == 'l':
            self.legendHandle.set_visible(not self.legendHandle.get_visible())    
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
    def update_visible_channels(self):
        nChannels = len(self.channelHandleList )
        if self.currentChannel == 'all':
            channelVisList = [True for k in range(nChannels)]
            self.legendHandle.set_visible(True)
            plt.title( self.signal.comment)
        else:
            channelVisList = [self.currentChannel==iCh for iCh in range(nChannels)]
            self.legendHandle.set_visible(False)
            plt.title("Channel {} : {}".format(self.currentChannel, self.signal.channelNames[self.currentChannel]))
        
        for iChannel, channelHandler in enumerate(self.channelHandleList ):
            if isinstance(channelHandler, list):
                for iLine in range(len(channelHandler)):
                    channelHandler[iLine].set_visible(channelVisList[iChannel])
            else:
                channelHandler.set_visible(channelVisList[iChannel])
        
    
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
            
    def show_help(self):
        helpText = "\n" + self.__doc__ + "\n\n            [press any key to close help]"
        props = dict(boxstyle='round', facecolor='wheat', alpha=0.8)
        self.legendHandle.set_visible(False)
    
        self.helpTextBox = self.axh.text(0.5, 0.5, helpText, transform=self.axh.transAxes, fontsize=14,
        verticalalignment='center', horizontalalignment='center',multialignment="left", bbox=props, fontname='monospace')
    
