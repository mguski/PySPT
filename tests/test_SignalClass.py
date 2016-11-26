# -*- coding: utf-8 -*-
"""
Some unittests for pyspt. Most test just check for occurring runtime errors.
Only a few check for correct results...

Created on Fri Nov 25 18:27:42 2016

@author: mguski
"""
"""
Method                   Checks that	
assertEqual(a, b)	    a == b	 
assertNotEqual(a, b)	    a != b	 
assertTrue(x)	         bool(x) is True	 
assertFalse(x)	         bool(x) is False	 
assertIs(a, b)	         a is b	2.7
assertIsNot(a, b)        a is not b
assertIsNone(x)          x is None
assertIsNotNone(x)       x is not None
assertIn(a, b)           a in b	
assertNotIn(a, b)        a not in b	
assertIsInstance(a, b)   isinstance(a, b)
assertNotIsInstance(a, b)  not isinstance(a, b)

"""



import unittest
import numpy as np
import matplotlib.pyplot as plt
import pyspt

@unittest.skip("skipping plot test since every figure has to be closed by hand")
class TestPlotFunctions(unittest.TestCase):
 
    def test_plot_time(self):
        r = pyspt.generate_sine()
        r.plot_time(show=False)
        
    def test_freq_time(self):
        r = pyspt.generate_sine()
        r.plot_freq(show=False)
        
    def test_spectrogram_time(self):
        r = pyspt.generate_sine()
        r.plot_spectrogram(show=False)
        



class TestDSPfunctions(unittest.TestCase):

    def test_hilbert(self):
        sine = pyspt.generate_sine(freq=3, samplingRate=10e3, nSamples=10e3)
        sineH = pyspt.dsp.hilbert_transform(sine)
        
    def test_resample(self):
        sig = pyspt.generate_sine() + pyspt.generate_noise()*(1/80)

        sig3 = pyspt.dsp.resample(sig, 500e3)
        self.assertEqual(sig3.samplingRate, 500e3)
        self.assertEqual(sig.length, sig3.length)
        
        sig3 = pyspt.dsp.resample(sig, 2e6)
        self.assertEqual(sig3.samplingRate, 2e6)
        self.assertEqual(sig.length, sig3.length)
        
    def test_time_shift_for_individual_channels(self):
        sig =  pyspt.Signal(range(101),1)
        sig |= sig

        sig2 = pyspt.dsp.time_shift(sig, [-10, 10] )   # list
        sig2 = pyspt.dsp.time_shift(sig, np.array([-10, 10])) # array of int
        sig2 = pyspt.dsp.time_shift(sig, np.array([-1.10, 10.1]) )        # array of float

    def test_sample_shift_for_individual_channels(self):
        sig =  pyspt.Signal(range(101),1)
        sig |= sig
        sig2 = pyspt.dsp.sample_shift(sig, [-10, 10] )   # list
        sig2 = pyspt.dsp.sample_shift(sig, np.array([-10, 10])) # array of int
        sig2 = pyspt.dsp.sample_shift(sig, np.array([-1.10, 10.1]) )        # array of float

    def test_time_shift(self):    
        plt.figure()
        sig =  pyspt.Signal(range(101),1)
        sig |= sig
        plot = False
        if plot:
            # % matplotlib
            sig.plot_time(ax=plt.subplot(511))
            plt.title('original')
         
        sig2 = pyspt.dsp.sample_shift(sig, 20, cyclic=True)
        if plot:
            sig2.plot_time(ax=plt.subplot(523))
            plt.title('cyclic shift +20 samples')
        sig2 = pyspt.dsp.sample_shift(sig, 20, cyclic=False)
        if plot:
            sig2.plot_time(ax=plt.subplot(524))
            plt.title('shift +20 samples')
            
        sig2 = pyspt.dsp.sample_shift(sig, -20, cyclic=True)
        if plot:
            sig2.plot_time(ax=plt.subplot(525))
            plt.title('cyclic shift -20 samples')
        sig2 = pyspt.dsp.sample_shift(sig, -20, cyclic=False)
        if plot:
            sig2.plot_time(ax=plt.subplot(526))
            plt.title('shift -20 samples')
        
        sig2 = pyspt.dsp.time_shift(sig, 40, cyclic=True)
        if plot:
            sig2.plot_time(ax=plt.subplot(527))
            plt.title('cyclic shift 40 sec')
        sig2 = pyspt.dsp.time_shift(sig, 40, cyclic=False)
        if plot:
            sig2.plot_time(ax=plt.subplot(528))
            plt.title('shift 40 sec')
        
        sig2 = pyspt.dsp.time_shift(sig, -40, cyclic=True)
        if plot:
            sig2.plot_time(ax=plt.subplot(529))
            plt.title('cyclic shift -40 sec')
        sig2 = pyspt.dsp.time_shift(sig, -40, cyclic=False)
        if plot:
            sig2.plot_time(ax=plt.subplot(5,2,10))
            plt.title('shift -40 sec')
            
    def test_frequency_mixer(self):
        mixingFreq = 200e3
        inputSignal = pyspt.generate_sine() 
        outputSignal2 = pyspt.dsp.frequency_mixer(inputSignal, mixingFreq)
                
        


class TestOtherFunctions(unittest.TestCase):

    def test_generate_sine(self):
        r = pyspt.generate_sine()
        r = pyspt.generate_sine(freq=100, samplingRate=10e3, amplitude=2, nSamples= 1000, phaseOffset=3.14)
        self.assertIsInstance(r, pyspt.Signal)
        
    def test_generate_noise(self):
        r = pyspt.generate_noise()
        r = pyspt.generate_noise(samplingRate=10e3, scale=2, nSamples= 1000, mean=11)
        self.assertIsInstance(r, pyspt.Signal)
        
    def test_mere_list(self):
        allSig = []
        for iSig in range(10):
            allSig.append(pyspt.generate_sine(freq=10*iSig+10, samplingRate=500, nSamples=1e3))
        
        multCh = pyspt.merge(allSig)
        self.assertEqual(multCh.nChannels, 10)


            
class TestSignalClass(unittest.TestCase):

    def test_signal_class_init(self):
        sr = 10000
        phi = [ 2*np.pi*30*t / sr for t in range(3002) ]
        vec = np.sin(phi)
        r = pyspt.Signal(vec, sr, comment='sine test signal')
        self.assertIsInstance(r, pyspt.Signal)


        
    def test_copy_vs_reference(self):
        r = pyspt.generate_sine()
        
        t = r.copy # return a copy        
        self.assertTrue((r.timeData == t.timeData).all(), msg='Copy results in different timeData values')
        self.assertIsNot(r.timeData_reference, t.timeData_reference, msg='obj.copy returns only reference!')
        
        t = r # now t is only a new reference
        self.assertIs(r.timeData_reference, t.timeData_reference, msg= 'error a = b  returns no reference!')

    def test_time_vector(self):
        r = pyspt.generate_sine()
        self.assertTrue((r.timeVector == np.array(range(r.nSamples))/r.samplingRate).all())
        
    def test_call_properties(self):
        r = pyspt.generate_sine()
        tmp = r.freqVector
        tmp = r.freqData
        tmp = r.timeData
         
    def test_time2index(self):
        r = pyspt.generate_sine()
        testIdx = 1234
        self.assertEqual(r.time2index(r.timeVector[testIdx]), testIdx, msg='time2index did not result in correct value')

    def test_freq2index(self):
        r = pyspt.generate_sine()
        testIdx = 1234
        self.assertEqual(r.freq2index(r.freqVector[testIdx]), testIdx, msg='freq2index did not result in correct value')

    def test_nSamples(self):
        r = pyspt.generate_sine()
        self.assertEqual(r._data.shape[1], r.nSamples)
        
    def test_nSamples_setter(self):
        r = pyspt.generate_sine()
        r.nSamples = 10
        self.assertEqual(r.nSamples, 10)
        r.nSamples = 100
        self.assertEqual(r.nSamples, 100)
        
    def test_length(self):
        r = pyspt.generate_sine()
        self.assertEqual(r.length, r.nSamples/r.samplingRate)
        
    def test_length_setter(self):
        r = pyspt.generate_sine()
        r.length = 0.1
        self.assertEqual(r.length, 0.1)
        r.length = 0.2
        self.assertEqual(r.length, 0.2)
        
        

    
    def test_nChannels(self):
        r = pyspt.generate_sine()
        self.assertEqual(r._data.shape[0], r.nChannels)
         
    def test_fft_ifft(self):
        r = pyspt.generate_sine() | pyspt.generate_sine(freq=10e3)
        t = r.copy
        t.fft()
        t.ifft()
        difference = t - r
        self.assertTrue(np.max(np.absolute(difference.timeData)) < 1e-14, msg='fft => ifft does not result in same values!')
    
    def test_rms_results(self):
        tmp = pyspt.generate_sine(nSamples=500e3, amplitude=1)
        self.assertTrue( tmp.rms() - np.sqrt(0.5) < 1e-15, msg='rms in time domain wrong')
        tmp.fft()
        self.assertTrue( tmp.rms() - np.sqrt(0.5) < 1e-15, msg= 'rms in freq domain wrong')
        
    def test_add(self):
        r = pyspt.generate_sine(nSamples=10)
        s = pyspt.generate_sine(nSamples=10, freq=500)
        
        t = s + r
        t = s + 2
        t = s + 2.5
        t = 2 + s
        t = 2.5 + s
        t += s
        t += 2
        t += 2.5
        
    def test_minus(self):
        r = pyspt.generate_sine(nSamples=10)
        s = pyspt.generate_sine(nSamples=10, freq=500)
        
        t = s - r
        t = s - 2
        t = s - 2.5
        t = 2 - s
        t = 2.5 - s
        t -= s
        t -= 2
        t -= 2.5
        
    def test_multiply_with_scalar(self):
        r = pyspt.generate_sine(nSamples=10)
        
        t = r * 2
        t = r * 2.1
        # t = 2 * r TODO
        
    def test_negative(self):
        r = pyspt.generate_sine(nSamples=10)
        t  = - r
        
    def test_channel_merge(self):
        dummyData = np.r_[1:6]  /10  +1
        dummyData2ch = np.vstack((dummyData, dummyData+1))

        s_1ch = pyspt.Signal(dummyData, 1, comment="one ch")
        s_2ch =  pyspt.Signal(dummyData2ch, 1, comment="two channels")
                
        tmp = s_2ch | s_2ch
        self.assertEqual(tmp.nChannels, 4)
        tmp =s_1ch | s_1ch
        self.assertEqual(tmp.nChannels, 2)
        tmp =s_1ch | s_2ch
        self.assertEqual(tmp.nChannels, 3)


    def test_channel_sum(self):
        dummyData = np.r_[1:6]  /10  +1
        dummyData2ch = np.vstack((dummyData, dummyData+1))
        s_2ch =  pyspt.Signal(dummyData2ch, 1, comment="two channels")
        s_2ch.sum()
        

if __name__ == '__main__':
    unittest.main()