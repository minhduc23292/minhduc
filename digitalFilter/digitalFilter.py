from enum import Enum
from typing import Sequence
import numpy as np
# from numpy.core.records import array
import popup.pop_message as pms
from scipy.signal import hann, blackman, flattop, lfilter, firwin, iirfilter


def build_filter(N, fc, window):
    """Construct filter using the windowing method for filter parameters M
    number of taps, cut-off frequency fc and window. Window defaults to None
    i.e. a rectangular window."""
    if not N % 2:
        N += 1
    n = np.arange(N)
    h = np.sinc(2 * fc * (n - (N - 1) / 2.))
    if (window == "Hanning"):
        w = hann(N, sym=False)  # Hann (Hanning) window
    elif (window == "Blackman"):
        w = blackman(N, sym=False)  # Blackman window
    elif (window == "Flatop"):
        w = flattop(N, sym=False)  # Flattop window
    elif (window == "Reactangular"):
        w = 1  # Rectangular window
    else:
        w = hann(N, sym=False)  # Hann (Hanning) window
    h = h * w
    return h / h.sum()


def filter_data(
        samples: Sequence[float],
        filter_type: str,
        high_pass_cut_off_freq: int,
        low_pass_cut_off_freq: int,
        sample_rate: int,
        window: str
):
    
    if high_pass_cut_off_freq >= sample_rate / 3:
        high_pass_cut_off_freq = sample_rate / 3
    if low_pass_cut_off_freq >= sample_rate / 2.56:
        low_pass_cut_off_freq = int(sample_rate / 2.56) - 1.0
    if low_pass_cut_off_freq <= 0 or high_pass_cut_off_freq <= 0:
        return samples

    if (filter_type == ''):
        return samples

    else:
        M = 700
        # Select the filter type
        if filter_type == "LOWPASS":
            fc = low_pass_cut_off_freq / sample_rate
            ham_lp = build_filter(M, fc, window)
            _samples = np.convolve(samples, ham_lp)
            _samples = _samples[M:-M]

        elif filter_type == "HIGHPASS":
            fc = high_pass_cut_off_freq / sample_rate
            ham_lp = build_filter(M, fc, window)
            ham_hp = -ham_lp
            ham_hp[M // 2] += 1
            _samples = np.convolve(samples, ham_hp)
            _samples = _samples[M:-M]

        elif filter_type == "BANDPASS":
            fc_lp = low_pass_cut_off_freq / sample_rate
            fc_hp = high_pass_cut_off_freq / sample_rate
            ham_lp = build_filter(M, fc_lp, window)
            temp_ham_hp = build_filter(M, fc_hp, window)
            ham_hp = -temp_ham_hp
            ham_hp[M // 2] += 1
            ham_bp = np.convolve(ham_lp, ham_hp)
            _samples = np.convolve(samples, ham_bp)
            _samples = _samples[2 * M: -2 * M]
        else:
            _samples = samples
        return _samples


def sum_2_array_not_same_length(arr1: Sequence[float], arr2: Sequence[float]):
    if len(arr1) <= len(arr2):
        arr3 = arr2[:len(arr1)]
        return arr1 + arr3
    else:
        arr3 = arr1[:len(arr2)]
        return arr2 + arr3


def iir_filter_data(
        samples: Sequence[float],
        filter_type: str,
        high_pass_cut_off_freq: int,
        low_pass_cut_off_freq: int,
        sample_rate: int,
        window: str
):
    if high_pass_cut_off_freq >= sample_rate / 3:
        high_pass_cut_off_freq = sample_rate / 3
    if low_pass_cut_off_freq >= sample_rate / 2.56:
        low_pass_cut_off_freq = int(sample_rate / 2.56) - 1.0
    if (filter_type == ''):
        pms.empty_entry_error('sample rate or filter type')
        return samples
    else:
        order = 5
        # Select the filter type
        if filter_type == "LOWPASS":
            b, a = iirfilter(order, low_pass_cut_off_freq, fs=sample_rate, btype="lowpass", ftype="butter", output='ba')

        elif filter_type == "HIGHPASS":
            b, a = iirfilter(order, high_pass_cut_off_freq, fs=sample_rate, btype="highpass", ftype="butter",
                             output='ba')

        elif filter_type == "BANDPASS":
            if high_pass_cut_off_freq >= low_pass_cut_off_freq:
                return samples
            else:
                b, a = iirfilter(order, [high_pass_cut_off_freq, low_pass_cut_off_freq], fs=sample_rate,
                                 btype="bandpass", ftype="butter", output='ba')
        filteredSignal = lfilter(b, a, samples)
        return filteredSignal


def bandpass_firwin(ntaps, lowcut, highcut, fs, window='hamming'):
    nyq = 0.5 * fs
    taps = firwin(ntaps, [lowcut, highcut], nyq=nyq, pass_zero=False,
                  window=window, scale=False)
    return taps


def lowpass_firwin(ntaps, lowcut, fs, window='hamming'):
    nyq = 0.5 * fs
    taps = firwin(ntaps, lowcut, nyq=nyq, pass_zero="lowpass",
                  window=window, scale=False)
    return taps


def highpass_firwin(ntaps, highcut, fs, window='hamming'):
    nyq = 0.5 * fs
    taps = firwin(ntaps, highcut, nyq=nyq, pass_zero="highpass",
                  window=window, scale=False)
    return taps

    """FIR Filter"""


def checking_filter_data(
        samples: Sequence[float],
        filter_type: str,
        high_pass_cut_off_freq: int,
        low_pass_cut_off_freq: int,
        sample_rate: int,
        window: str
):
    if (window == "Hanning"):
        _window = "hamming"
    elif (window == "Blackman"):
        _window = "blackman"
    elif (window == "Flatop"):
        _window = "flattop"
    else:
        _window = "hamming"
    if high_pass_cut_off_freq >= sample_rate / 3:
        high_pass_cut_off_freq = sample_rate / 3
    if low_pass_cut_off_freq >= sample_rate / 2.56:
        low_pass_cut_off_freq = int(sample_rate / 2.56) - 1.0
    if low_pass_cut_off_freq <= 0 or high_pass_cut_off_freq <= 0:
        return samples

    if (filter_type == ''):
        return samples
    else:
        ntaps = 4097  # ntaps phai la so le
        if not ntaps % 2:
            ntaps += 1
        # Select the filter type
        if filter_type == "LOWPASS":
            taps_hamming = lowpass_firwin(ntaps, low_pass_cut_off_freq, fs=sample_rate, window=_window)

        elif filter_type == "HIGHPASS":
            taps_hamming = highpass_firwin(ntaps, high_pass_cut_off_freq, fs=sample_rate, window=_window)

        elif filter_type == "BANDPASS":
            if high_pass_cut_off_freq >= low_pass_cut_off_freq:
                return samples
            else:
                taps_hamming = bandpass_firwin(ntaps, high_pass_cut_off_freq, low_pass_cut_off_freq, fs=sample_rate,
                                               window=_window)
        filteredSignal = lfilter(taps_hamming, 1.0, samples)
        # print("low_pass_cut_off_freq", low_pass_cut_off_freq)
        # print("high_pass_cut_off_freq", high_pass_cut_off_freq)
        # print("sample_rate", sample_rate)
        # print(" do dai truoc filter", len(samples))
        # print(" do dai sau filter", len(filteredSignal))
        return filteredSignal[ntaps:]