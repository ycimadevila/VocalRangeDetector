import numpy as np
import numpy.fft as tf
import scipy.io.wavfile as wf
import pywt 
import pywt.data as wt_data
from os.path import dirname, join as pjoin
from matplotlib import pyplot as plt

range_voices2 = {
    (65,349):'bajo',
    (83,440):'baritono',
    (98,523):'tenor',
    (131,784):'contralto',
    (165,880):'mezzo',
    (197,1175):'soprano'
}

range_voices = {
    (72, 301)   : 'bajo',
    (120, 440)  : 'baritono',
    (160, 500)  : 'tenor',
    (220, 817)  : 'contralto',
    (260, 920)  : 'mezzo',
    (300, 1002) : 'soprano'
}

def my_fft(path, file):
    wav_fname = pjoin(path, file)
    sample_rate, data = wf.read(wav_fname)
    data = np.transpose(data)
    
    fourier_transf = tf.fft(data[0])
    fourier_transf_norm = [np.abs(i) for i in fourier_transf]
    freq = tf.fftfreq(len(fourier_transf), d = 1 / sample_rate)
    
    fourier_transf = fourier_transf_norm[0 : int(len(fourier_transf_norm) / 2)]
    freq = freq[0: int(len(freq) / 2)]
    
    r = { }
    
    def search_range(freq, amp):
        for key,value in range_voices.items():
            if key[0] < freq < key[1]:
                try:
                    r[value] += amp
                except KeyError:
                    r[value] = amp

    for i,f in enumerate(freq):
        search_range(f,fourier_transf[i])

    def_range = 'bajo'
    max_range = 0
    for key,value in r.items():
        if value > max_range:
            max_range = value
            def_range = key
    
    return def_range, fourier_transf, freq


#### Wavelet ####

def wt(path, file):
    wav_fname = pjoin(path, file)
    _, data = wf.read(wav_fname)
    data = np.transpose(data)
 
    value = pywt.wavedec(data[0], 'db1')
    arr, _ = pywt.coeffs_to_array(value)
    data_filter = []
    
    for item in arr:
        if 65 <= np.abs(item) <= 1175:
            data_filter.append(np.abs(item))
   
    r = { }
    for key, value in range_voices2.items():
        for item in data_filter:
            if key[0] <= item <= key[1]:
                try:
                    r[value] += 1
                except KeyError:
                    r[value] = 1

    final_range = 'bajo'
    max_value = 0
    for key, value in r.items():
       if value > max_value:
           max_value = value
           final_range = key 
    
    return final_range
    
