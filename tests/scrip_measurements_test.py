import pyspt



imp1 = pyspt.generate_impulse() * 1e3
imp2 = pyspt.generate_impulse() * 1e6

# test rms
# s = pyspt.generate_sine(samplingRate=44100, nSamples=44100, freq=100)
# print(s.rms())
# s.fft()
# print(s.rms())

print(imp1.rms())
imp1.fft()

print(imp1.rms())
imp1.ifft()

print(imp1.rms())
imp1.fft()



res = pyspt.dsp.x_fade_spk(imp1, imp2, [100, 1000])
#res.plot_freq()



sweep = pyspt.generate_sweep(signal_length=0.7, f_stop=18000,bandwidth=0)
# sweep.plot_freq()
#sweep = pyspt.dsp.normalize(sweep)


inv_sweep = pyspt.dsp.invert_spk(sweep, [20, 18000])
# inv_sweep.plot_freq()
tmp = sweep * inv_sweep
tmp.plot_freq()



import sounddevice as sd
import time
rec_dat = sd.playrec(sweep.timeData.T, sweep.samplingRate, channels=1)
time.sleep(sweep.length)
rec = pyspt.Signal(rec_dat.T, sweep.samplingRate, domain='time')

ir = rec * inv_sweep
ir.signalType = 'energy'
ir.plot_freq()


# print('nSamples= {}, size {}\n'.format(sweep.nSamples, sweep._data.shape))
# sweep.fft()
# print('nSamples= {}, size {}\n'.format(sweep.nSamples, sweep._data.shape))
# sweep.ifft()
# print('nSamples= {}, size {}\n'.format(sweep.nSamples, sweep._data.shape))

#sweep.plot_freq()