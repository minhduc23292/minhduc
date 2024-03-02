# from distutils.core import setup
# from distutils.extension import Extension

# setup(
#   name='otani_analyzer',
#   ext_modules=[Extension("ad7609BTZ", ["ad7609BTZ.c"], libraries=['wiringPi'])],
# )


# import ctypes
# from numpy.ctypeslib import ndpointer
# ad7609 = ctypes.CDLL('/home/pi/otani_analyzer/ad7609BTZ.so')
# if __name__=="__main__":
#     ad7609.init()
#     n=6
#     data_length = 1000
#     total_length=data_length * n + 1
#     sample_rate=20000 #max=35000
#     ad7609.ADCread.restype = ctypes.POINTER(ctypes.c_float * total_length)
#     ad7609.ADCread.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int]
#     ad7609.freeme.argtypes = ctypes.c_void_p,
#     ad7609.freeme.restype = None
#     kq=ad7609.ADCread(data_length, sample_rate, n )
#     ttl=[i for i in kq.contents] # ket qua tra ve
#     print("len ttl",len(ttl))
#     ad7609.freeme(kq) # Xoa con trỏ
#     actual_sample_rate= ttl[-1] # phần tử cuối cùng là tốc độ lấy mẫu thực
#     print("sample rate:", actual_sample_rate)
#     chanelm=[[],[],[],[],[],[]]

#     if n==6:
#         for j in range(len(ttl)-1):
#             if   j%6==0:
#                 chanelm[0].append(ttl[j])
#             elif j%6==1:
#                 chanelm[1].append(ttl[j])
#             elif j%6==2:
#                 chanelm[2].append(ttl[j])
#             elif j%6==3:
#                 chanelm[3].append(ttl[j])
#             elif j%6==4:
#                 chanelm[4].append(ttl[j])
#             elif j%6==5:
#                 chanelm[5].append(ttl[j])
#             else:
#                 pass

#         print(chanelm[0][0:7])
#         print(chanelm[1][0:7])
#         print(chanelm[2][0:7])
#         print(chanelm[3][0:7])
#         print(chanelm[4][0:7])
#         print(chanelm[5][0:7])
#     if n==4:
#         for j in range(len(ttl)-1):
#             if   j%4==0:
#                 chanelm[0].append(ttl[j])
#             elif j%4==1:
#                 chanelm[1].append(ttl[j])
#             elif j%4==2:
#                 chanelm[2].append(ttl[j])
#             elif j%4==3:
#                 chanelm[3].append(ttl[j])
#             else:
#                 pass

#         print(chanelm[0][0:7])
#         print(chanelm[1][0:7])
#         print(chanelm[2][0:7])
#         print(chanelm[3][0:7])

# ad7609.turn_on_24v.restype=None
# ad7609.turn_on_24v.argtypes=None

##### Code mau so 2, su dung code tren mang#########
# import ad7768

# adc_pins = {'standby':6, 'convsta':9, 'reset':10, 'busy':24, '1stData':25, "cs": 23, "clock":11, "DoutA":8, "DoutB":7, "range":5, "os0":13, "os1":19, "os2":26, "sen1_en":21 }
# adc=ad7768.AD7606_AB(10, adc_pins,returnRaw=False)
# adc.ADCreset()
# kq=adc.ADCread()
# print(kq)

# import RPi.GPIO as GPIO
# from time import sleep
# GPIO.setmode(GPIO.BCM)
# GPIO.setwarnings(False)
# GPIO.setup(7,GPIO.OUT)
# GPIO.setup(8,GPIO.OUT)
# GPIO.setup(11,GPIO.OUT)
# for i in range(100):
#     GPIO.output(7, 1)
#     GPIO.output(11, 1)
#     sleep(0.1)
#     GPIO.output(7, 0)
#     GPIO.output(11, 0)
#     sleep(0.1)

# import smbus


# mcuBus=smbus.SMBus(1)
# adr=0x08
# character='d'
# mcuBus.write_byte(adr, ord(character))

# import sys
# import time
# import datetime
# import random
# from ds3231.ds3231B import *
# filename = time.strftime("%Y-%m-%d%H:%M:%SRTCTest") + ".txt"
# starttime = datetime.utcnow()

# ds3231 = DS3231(1, 0x68)
# ds3231.write_now()

# while True:
# 	currenttime = datetime.utcnow()
# 	deltatime = currenttime - starttime
# 	print("Raspberry Pi=\t" + time.strftime("%Y-%m-%d %H:%M:%S"))
# 	print("DS3231=\t\t%s" % ds3231.read_datetime())
# 	print("DS3231 Temp=", ds3231.getTemp())
# 	time.sleep(5.0)

# from bq25896.bq25896 import BQ25896

# bqbus=BQ25896(1, 0x6b)
# data=bqbus._write(0x02, 0x91)
# data=bqbus._read(0x05)
# print(data)
# import time
from bateryMonitor.bateryMonitor import BQ40Z50

batery = BQ40Z50()
data0 = batery.read_voltage()
data1 = batery.read_current()
data2 = batery.read_temp()
data3 = batery.read_remain_cap()
print([data0, data1, data2, data3])

# import numpy as np
# from scipy.signal import kaiserord, lfilter, firwin, freqz, firwin2
# import matplotlib.pyplot as plt

# # Nyquist rate.
# nyq_rate = 20000 / 2

# # Width of the roll-off region.
# width = 500 / nyq_rate

# # Attenuation in the stop band.
# ripple_db = 12.0

# num_of_taps, beta = kaiserord(ripple_db, width)
# if num_of_taps % 2 == 0:
#     num_of_taps = num_of_taps + 1

# # Cut-off frequency.
# cutoff_hz = 5000.0

# # Estimate the filter coefficients.
# taps = firwin(num_of_taps, cutoff_hz/nyq_rate, window=('kaiser', beta), pass_zero=False)

# w, h = freqz(taps, worN=4000)

# plt.plot((w/np.pi)*nyq_rate, 20*np.log10(np.abs(h)), linewidth=2)

# plt.axvline(cutoff_hz + width*nyq_rate, linestyle='--', linewidth=1, color='g')
# plt.axvline(cutoff_hz - width*nyq_rate, linestyle='--', linewidth=1, color='g')
# plt.axhline(-ripple_db, linestyle='--', linewidth=1, color='c')
# delta = 10**(-ripple_db/20)
# plt.axhline(20*np.log10(1 + delta), linestyle='--', linewidth=1, color='r')
# plt.axhline(20*np.log10(1 - delta), linestyle='--', linewidth=1, color='r')

# plt.xlabel('Frequency (Hz)')
# plt.ylabel('Gain (dB)')
# plt.title('Frequency Response')
# plt.ylim(-40, 5)
# plt.grid(True)
# plt.show()
# from scipy.signal import firwin, remez, kaiser_atten, kaiser_beta

# # # Several flavors of bandpass FIR filters.

# def bandpass_firwin(ntaps, lowcut, highcut, fs, window='hamming'):
#     nyq = 0.5 * fs
#     taps = firwin(ntaps, [lowcut, highcut], nyq=nyq, pass_zero=False,
#                   window=window, scale=False)
#     return taps

# def lowpass_firwin(ntaps, lowcut, fs, window='hamming'):
#     nyq = 0.5 * fs
#     taps = firwin(ntaps, lowcut, nyq=nyq, pass_zero="lowpass",
#                   window=window, scale=False)
#     return taps

# def highpass_firwin(ntaps, highcut, fs, window='hamming'):
#     nyq = 0.5 * fs
#     taps = firwin(ntaps, highcut, nyq=nyq, pass_zero="highpass",
#                   window=window, scale=False)
#     return taps

# def rmsValue(arr):
#     squareArr=np.square(arr)
#     meanOfSquareArr=np.mean(squareArr)
#     rms=np.sqrt(meanOfSquareArr)
#     # rms=np.sqrt(np.mean(np.square(arr)))
#     return rms

# if __name__ == "__main__":
#     import numpy as np
#     import matplotlib.pyplot as plt
#     from scipy import signal
#     from scipy.signal import freqz, lfilter
#     from scipy import fftpack
#     plt.figure(1, figsize=(12, 9))
#     plt.clf()
#     # Sample rate and desired cutoff frequencies (in Hz).
#     fs = 5000
#     lowcut = 1000
#     highcut = 1000
#     N=10000
#     mt = np.linspace(0, N/fs, N, endpoint=False)
#     ch1=10*np.cos(2 * np.pi * 200 * mt+np.pi/2)  + 2*np.cos(2 * np.pi * 1500 * mt)
#     ntaps = 129
#     if not ntaps % 2:
#         ntaps += 1
#     # taps_hamming = bandpass_firwin(ntaps, lowcut, highcut, fs=fs)
#     taps_hamming = lowpass_firwin(ntaps, lowcut, fs=fs)
#     # taps_hamming = highpass_firwin(ntaps, lowcut, fs=fs)
#     w, h = freqz(taps_hamming, 1, worN=2000)
#     plt.subplot(221)
#     plt.plot((fs * 0.5 / np.pi) * w, abs(h), label="Hamming window")
#     plt.title(r'Freq response')
#     plt.grid(True)
#     plt.subplot(222)
#     h_Phase = np.unwrap(np.arctan2(np.imag(h),np.real(h)))
#     plt.plot(fs * 0.5 / np.pi * w, h_Phase)
#     plt.title(r'Phase response')

#     filtered_signal= lfilter(taps_hamming, 1.0, ch1)
#     T=1.0/fs
#     w = signal.hann(N, sym=False)
#     yf = fftpack.fft(filtered_signal * w) * (4 / N)
#     yf1 = np.abs(yf[:(int(N // 2))])
#     xf=fftpack.fftfreq(N, T)[0:int(N//2)]
#     print("root rms:", rmsValue(ch1))
#     print("filteredRms:", rmsValue(filtered_signal[ntaps:]))
#     plt.subplot(223)
#     plt.plot(xf, yf1, label="fft")
#     plt.title("FFT")
#     plt.grid(True)

#     plt.subplot(224)
#     plt.plot(mt[ntaps:ntaps+200], filtered_signal[ntaps:ntaps+200], label="filtered Signal")
#     plt.plot(mt[0:200], ch1[0:200], color='red', label="root Signal")   
#     plt.title("Filtered_Signal")
#     plt.grid(True)
#     # plt.xlim(0, 0.2)
#     plt.show()
