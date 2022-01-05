import pyspt
import sounddevice as sd
import numpy as np
import time

import matplotlib.pyplot as plt


sweep = pyspt.generate_sweep(signal_length=3, f_stop=20000,bandwidth=1/24, zero_padding=0.5)
#sweep = pyspt.dsp.normalize(sweep)


inv_sweep = pyspt.dsp.invert_spk(sweep, [20, 20000])
# inv_sweep.plot_freq()
# tmp = sweep * inv_sweep
# tmp.plot_freq()


# do meausrements
rec_dat = sd.playrec(sweep.timeData.T * 0.5, sweep.samplingRate, channels=1)
time.sleep(sweep.length)
rec = pyspt.Signal(rec_dat.T, sweep.samplingRate, domain='time')

# measurement post processing
ir = rec * inv_sweep
ir.signalType = 'energy'
ir.comment = "Impulse response"
ir.plot_freq()
ir.plot_time()

cmp = pyspt.other_functions.merge([sweep, rec])
cmp.plot_freq()

def get_delay(ir):
    idx_max = np.argmax(np.abs(ir.timeData))
    delay_time = ir.timeVector[idx_max]
    return delay_time

def signal_energy(ir, window_sig = 0.001):

    idx_max = np.argmax(np.abs(ir.timeData))
    nSamples_win = int(window_sig*ir.samplingRate)
    sig_energy = np.sum(np.power(np.abs(ir.timeData[:, idx_max-nSamples_win:idx_max+nSamples_win]), 2))

    # noise_energy = np.sum(np.power(np.abs(ir.timeData), 2)) - sig_energy
    # print(10*np.log10(sig_energy))
    # print(10*np.log10(noise_energy))
    # SNFR = 10*np.log10(  sig_energy / (window_sig*2) / (noise_energy / (ir.length - 2*window_sig)))
    # print(SNFR)
    return 10*np.log10(sig_energy)


def passband_statistics(ir, freq_low, freq_high):

    idx_low = ir.freq2index(freq_low)
    idx_high = ir.freq2index(freq_high)

    tmp_spk = ir.freqData_reference[0, idx_low:idx_high]
    tmp_spk = 20*np.log10(np.abs(tmp_spk))

    mean_tf = np.mean(tmp_spk)
    std_tf = np.std(tmp_spk)

    max_dev = max(np.abs(tmp_spk - mean_tf))

    print("Passband statistic: {} Hz - {:2.1f} kHz".format(freq_low, freq_high/1000))
    print("  mean level {:2.2f} dBFS".format(mean_tf))
    print("  std level {:2.2f} dB".format(std_tf))
    print("  max deviation {:2.2f} dB".format(max_dev))
    return [mean_tf, std_tf, max_dev]


latency = get_delay(ir)
print('Latency {:2.3f} ms '.format(latency*1000))

sig_energy = signal_energy(ir)
print("signal energy {:2.1f} dBFS".format(sig_energy))

mean_tf, std_tf, max_dev = passband_statistics(ir, 20, 20e3)
