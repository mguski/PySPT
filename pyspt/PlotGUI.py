# -*- coding: utf-8 -*-
"""
Module for interactive plotting GUI.

Created on Fri Nov 25 17:06:58 2016
@author: mguski

"""
import  matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from .meta_functions import num2string
import numpy as np

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
            
        elif event.key == 'm':
            
            unitDict = dict(time=['s', ''], time_dB=['s','dB'], freq=['Hz', ''], freq_dB=['Hz','dB'], spec_dB=['s','Hz'], spec=['s','Hz'])
            if self.plotDomain in unitDict:
                xUnit, yUnit = unitDict[self.plotDomain]
            else:
                xUnit = yUnit = ""
                
                
#            self.survivalZoneForObjects = MeasureInPlot(self.axh, xUnit=xUnit)
            MeasureInPlot(self.axh, xUnit=xUnit, yUnit=yUnit)
            



            # cursors?



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
    
class MeasureInPlot(object):
    """ Class to measure signal in a plot. """
    def __init__(self, ax, xUnit='', yUnit=''):
        self.ax = ax
        self.fig = self.ax.get_figure()
        self.lx = ax.axhline(color='k')  # the horiz line
        self.ly = ax.axvline(color='k')  # the vert line
        self.start_x = []
        self.start_y = []
        self.status = "set_start"
        self.xUnit = xUnit
        self.yUnit = yUnit        
        self.cid_move  = self.fig.canvas.mpl_connect('motion_notify_event', self.set_start_point)
        self.cid_click = self.fig.canvas.mpl_connect('button_press_event', self.onclick)

        props = dict(boxstyle='round', facecolor='wheat') #, alpha=0.8)
        self.txt = ax.text(0.05, 0.95, '', transform=self.fig.transFigure, verticalalignment='top', horizontalalignment='left',multialignment="left", bbox=props, fontname='monospace')
        
        plt.ginput(3) # not nice but could not think of better way
               

    def set_start_point(self, event):

        if not event.inaxes:
            return

        x, y = event.xdata, event.ydata
        # update the line positions
        self.lx.set_ydata(y)
        self.ly.set_xdata(x)

        self.txt.set_text('Click to set start point:\nx={}, y={}'.format(num2string(x), num2string(y)))
        plt.draw()
        
    def set_end_point(self, event):
        if not event.inaxes:
            return
        yMin = min(self.start_y, event.ydata)
        yMax = max(self.start_y, event.ydata)
        xMin = min(self.start_x, event.xdata)
        xMax = max(self.start_x, event.xdata)
        polygonData = np.array([[xMin, yMin],[xMin, yMax],[xMax, yMax],[xMax, yMin], [xMin, yMin]])
        self.span_polygon.set_xy(polygonData)
        n2s = num2string
        if self.xUnit == "Hz":
            inverse_xUnit = "s"
        elif self.xUnit == "s":
            inverse_xUnit = "Hz"
        elif self.xUnit == "":
            inverse_xUnit = ""
        else:
            inverse_xUnit = "1/" + self.xUnit
        
        infoText =  'Start : x={}{}, y={}{}\n'.format(n2s(self.start_x), self.xUnit, n2s(self.start_y), self.yUnit) 
        infoText += 'End   : x={}{}, y={}{}\n'.format(n2s(event.xdata),  self.xUnit, n2s(event.ydata),  self.yUnit)
        infoText += 'Diff  : x={}{}, y={}{}\n'.format(n2s(event.xdata-self.start_x),  self.xUnit, n2s(event.ydata-self.start_y),  self.yUnit)
        infoText += '1 / delta_x = {}{}'.format(n2s(event.xdata-self.start_x),  inverse_xUnit)
        self.txt.set_text(infoText)
        plt.draw()


    def onclick(self, event):
        #print('button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %  (event.button, event.x, event.y, event.xdata, event.ydata))
        if event.button == 1:
            if self.status == 'set_start':
                # close crosshair         
                self.lx.set_visible(False)
                self.ly.set_visible(False)
                
                self.start_x = event.xdata
                self.start_y = event.ydata
                polygonData = np.array([[self.start_x, self.start_y],[self.start_x, self.start_y],[self.start_x, self.start_y],[self.start_x, self.start_y], [self.start_x, self.start_y]])
                self.span_polygon = Polygon(polygonData, facecolor='0.75', alpha=0.5 ) #, transform=self.ax.transData)
                self.ax.add_patch(self.span_polygon)
                self.status = 'set_end'
                self.fig.canvas.mpl_disconnect(self.cid_move)
                self.cid_move = self.fig.canvas.mpl_connect('motion_notify_event', self.set_end_point)
            elif self.status == 'set_end':               
                #plt.axhspan(yMin, yMax, xmin=xMin, xmax=xMax, facecolor='0.5', alpha=0.5)
                self.fig.canvas.mpl_disconnect(self.cid_move)
                self.status = 'finished'
            elif self.status == 'finished':
                self.fig.canvas.mpl_disconnect(self.cid_click) 
                self.close()
                
    def close(self):
        self.span_polygon.remove()
        self.lx.remove()
        self.ly.remove()
        self.txt.remove()