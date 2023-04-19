import cmath
# from msilib import sequence
import numpy as np
from scipy import fftpack, signal
from scipy.signal import hilbert
from digitalFilter.digitalFilter import filter_data
import defaultConfig.default_config as dfc
from scipy.integrate import cumulative_trapezoid

def is_number(s):
    try:
        float(s)  # for int, long and float
    except ValueError:
        return False
    return True


def rmsValue(arr):
    squareArr = np.square(arr)
    meanOfSquareArr = np.mean(squareArr)
    rms = np.sqrt(meanOfSquareArr)
    # rms=np.sqrt(np.mean(np.square(arr)))
    return rms

def rmsVelFromAccSpectrum(Acc, sample_rate):
    n = len(Acc)
    w = signal.hann(n, sym=False)  # Hann (Hanning) window
    xf2 = np.linspace(0.0, 1.0 / (2.0/sample_rate), int(n / 2))
    xf2=xf2[5:]
    yf = fftpack.fft(Acc * w) * (4 / n)
    yf2 = np.abs(yf[5:int(n / 2)])
    for j in range(len(yf2)):
        yf2[j]/=0.000204*np.pi*xf2[j]
    k=0
    sum=0
    while(xf2[k]<1000):
        sum+=np.square(yf2[k])
        k+=1
    sum/=k
    
    return np.sqrt(sum)

def crest_factor(x):
    rms_val = rmsValue(x)
    absX = np.abs(x)
    crest_val = np.max(absX) / rms_val
    return crest_val


def find_max(arr):
    pos = 0
    _max = arr[0]
    for i in range(len(arr)):
        if (arr[i] > _max):
            _max = arr[i]
            pos = i
    return [pos, _max]


def find_pos(arr, val):
    pos = 0
    n = len(arr)
    for i in range(1, n):
        if (arr[i] == val):
            pos = i
            break
    if pos > 0:
        return pos
    else:
        return -1


def pow2(a):
    i = 1
    while (2 ** i < a):
        i += 1
    return 2 ** i


def phase_shift_calculate(arr1, arr2, sample_rate, speed):
    arr1 = arr1 - np.mean(arr1)
    arr2 = arr2 - np.mean(arr2)
    N = len(arr1)
    x = int(speed / (sample_rate / 2) * (N / 2))
    w = signal.hann(N, sym=False)
    yf1 = fftpack.fft(arr1 * w) * (4 / N)
    yf2 = fftpack.fft(arr2 * w) * (4 / N)
    # yf = yf[:(int(N / 2))]
    module2 = np.abs(yf2[:(int(N / 2))])
    module1 = np.abs(yf1[:(int(N / 2))])
    phase_arr1 = np.angle(yf1)[:(int(N / 2))]
    phase_arr2 = np.angle(yf2)[:(int(N / 2))]
    selected_phase1=phase_arr1[int(x / 2): int(x * 3 / 2)]
    selected_phase2=phase_arr2[int(x / 2): int(x * 3 / 2)]
    pos2, max2 = find_max(module2[int(x / 2): int(x * 3 / 2)])
    # pos22 = find_pos(module2[0:int(x * 3 / 2)], max2)
    pos1, max1 = find_max(module1[int(x / 2): int(x * 3 / 2)])
    # pos11 = find_pos(module1[0:int(x * 3 / 2)], max1)
    return (selected_phase2[pos2] - selected_phase1[pos1])


def tracking_signal(sensor_dict, range_freq):
    arr1 = sensor_dict["sensor_data"][0]
    arr2 = sensor_dict["sensor_data"][1]
    arr3 = sensor_dict["sensor_data"][2]
    _sample_rate = sensor_dict["sample_rate"]
    N = len(arr1)
    w = signal.hann(N, sym=False)
    yf1 = fftpack.fft(arr1 * w) * (2*np.sqrt(2) / N)
    yf2 = fftpack.fft(arr2 * w) * (2*np.sqrt(2) / N)
    yf3 = fftpack.fft(arr3 * w) * (2*np.sqrt(2) / N)
    # yf = yf[:(int(N / 2))]
    module3 = np.abs(yf3[:(int(N / 2))])
    module2 = np.abs(yf2[:(int(N / 2))])
    module1 = np.abs(yf1[:(int(N / 2))])
    phase_arr1 = np.angle(yf1)[:(int(N / 2))]
    phase_arr2 = np.angle(yf2)[:(int(N / 2))]
    phase_arr3 = np.angle(yf3)[:(int(N / 2))]
    resolution = _sample_rate / N
    key_module = None
    key_phase = None
    if sensor_dict["sensor_key"][0] == "Sensor1":
        key_module = module1
        key_phase = phase_arr1
    elif sensor_dict["sensor_key"][0] == "Sensor2":
        key_module = module2
        key_phase = phase_arr2
    elif sensor_dict["sensor_key"][0] == "Sensor3":
        key_module = module3
        key_phase = phase_arr3
    key_pos, key_max = find_max(key_module[int(range_freq[0] / resolution): int(range_freq[1] / resolution)])
    key_pos += int(range_freq[0] / resolution)
    max1 = float(module1[key_pos])
    max2 = float(module2[key_pos])
    max3 = float(module3[key_pos])
    phase_shift1 = phase_arr1[key_pos] - key_phase[key_pos]
    phase_shift2 = phase_arr2[key_pos] - key_phase[key_pos]
    phase_shift3 = phase_arr3[key_pos] - key_phase[key_pos]
    return [max1, max2, max3, phase_shift1, phase_shift2, phase_shift3, key_pos * resolution]

def tracking_signal_no_phase_shift(x1, y1, y2, y3, range_freq):
    temXarray=x1[find_nearest_element(x1, range_freq[0]): find_nearest_element(x1, range_freq[1])]
    temY2array=y2[find_nearest_element(x1, range_freq[0]): find_nearest_element(x1, range_freq[1])]    
    temY3array=y3[find_nearest_element(x1, range_freq[0]): find_nearest_element(x1, range_freq[1])]    

    [key_pos1, key_max1] = find_max(y1[find_nearest_element(x1, range_freq[0]): find_nearest_element(x1, range_freq[1])])
    key_max2=temY2array[key_pos1]
    key_max3=temY3array[key_pos1]

    return [key_max1, key_max2, key_max3, temXarray[key_pos1]]

def tab4_tracking_signal_old(data_arr, _sample_rate, range_freq):
    N = len(data_arr)
    w = signal.hann(N, sym=False)
    yf1 = fftpack.fft(data_arr * w) * (2*np.sqrt(2) / N)
    module1 = np.abs(yf1[:(int(N / 2))])
    resolution = _sample_rate / N
    [key_pos, key_max] = find_max(module1[int(range_freq[0] / resolution): int(range_freq[1] / resolution)])
    key_pos += int(range_freq[0] / resolution)
    max1 = float(module1[key_pos])
    return [max1, key_pos * resolution]

def find_nearest_element(arr, value):
    i=0
    while(arr[i]<value):
        i+=1
    return i

def tab4_tracking_signal(data_arrY, data_arrX, range_freq):
    temXarray=data_arrX[find_nearest_element(data_arrX, range_freq[0]): find_nearest_element(data_arrX, range_freq[1])]
    [key_pos, key_max] = find_max(data_arrY[find_nearest_element(data_arrX, range_freq[0]): find_nearest_element(data_arrX, range_freq[1])])
    return [key_max, temXarray[key_pos]]



def phase_shift(arr1, arr2, samples_per_second):
    arr11 = arr1 - np.mean(arr1)
    arr21 = arr2 - np.mean(arr2)
    std_x = np.std(arr1)
    std_y = np.std(arr2)
    n = len(arr1)
    freq_Hz = 25
    num_samples = len(arr1)
    t = np.linspace(0.0, (num_samples / samples_per_second), num_samples)
    ab_corr = np.correlate(arr11, arr21, 'full')
    dt = np.linspace(-t[-1], t[-1], 2 * num_samples)
    # t_shift_alt = (1.0 / sample_rate) * ab_corr.argmax() - t[-1]
    t_shift = dt[ab_corr.argmax()]
    phase_shift1 = 2 * np.pi * (((t_shift / (1 / freq_Hz)) % 1.0))
    # phase_shift = 2*np.pi*(t_shift / (1.0 / freq_Hz))
    # phase_shift = 2 * np.pi * (((0.5 + t_shift / (1.0 / freq_Hz)) % 1.0) - 0.5)
    return phase_shift1


def vtrial(a0, phi0, a1, phi1):
    z0 = a0 * np.cos(phi0) + (a0 * np.sin(phi0)) * 1j
    z1 = a1 * np.cos(phi1) + (a1 * np.sin(phi1)) * 1j
    azt = z1 - z0
    amp = np.abs(azt)
    phase = cmath.phase(azt)
    return np.pi - phase + phi0
    # azt = np.sqrt(a0**2+a1**2-2*a0*a1*np.cos(phi0-phi1))\


def tsa_convert(arr, pulse_position, tsa_value):
    temp_arr = []
    for i in range(5):
        temp_arr.append(arr[i][pulse_position[0]:pulse_position[-1]])
    sum_arr = np.array(temp_arr)
    for i in range(3):
        for k in range(tsa_value):
            sum_arr[i] += np.roll(temp_arr[i], pulse_position[k + 1] - pulse_position[0])
        sum_arr[i] /= tsa_value + 1
    return sum_arr  # mang 5 phan tu


def acc2vel_sai(accel_arr, sample_rate):
    vel_arr = []
    dt = 1 / sample_rate
    for i in range(len(accel_arr) - 2):
        velocity = 9800.0 * (accel_arr[i + 2] + 4 * accel_arr[i + 1] + accel_arr[i]) * dt / 3  # mm/s
        vel_arr.append(velocity)
    return vel_arr


def vel2disp(vel_arr, sample_rate): #mm/s->um
    N = len(vel_arr)
    xt = np.linspace(0.0, N/sample_rate, N)
    d = cumulative_trapezoid(vel_arr, xt)*1000
    d=filter_data(
                            d,
                            "BANDPASS",
                            5,
                            1000,
                            sample_rate,
                            window="Hanning"
                            )
    d-=np.mean(d)
    return d

def acc2vel(accel_arr, sample_rate): #g->mm/s
    # dt=1/sample_rate
    # velocity = np.zeros_like(accel_arr)
    # velocity[0] = 0
    # for i in range(1, len(accel_arr)):
    #     velocity[i] = velocity[i-1] + 0.5 * (accel_arr[i-1] + accel_arr[i]) * dt
    # return velocity*9800
    N = len(accel_arr)
    xt = np.linspace(0.0, N/sample_rate, N)
    v = cumulative_trapezoid(accel_arr, xt)*9800
    v=filter_data(
                            v,
                            "BANDPASS",
                            5,
                            1000,
                            sample_rate,
                            window="Hanning"
                            )
    v-=np.mean(v)
    return v

def gE(arr, filter_from: int, filter_to: int, sample_rate, window: str):
    gE_arr = []
    for i in range(len(arr)):
        _samples_1 = filter_data(
            arr[i],
            "BANDPASS",
            filter_from,
            filter_to,
            sample_rate[i],
            window
        )
        analytical_signal = hilbert(_samples_1)
        amplitude_envelope = np.abs(analytical_signal)
        amplitude_envelope = filter_data(
            amplitude_envelope,
            "LOWPASS",
            filter_from,
            filter_to,
            sample_rate[i],
            window
        )
        # p2p=1.8*np.max(amplitude_envelope)
        rms_val = rmsValue(amplitude_envelope)
        p2p = 2 * rms_val * np.sqrt(2)
        gE_arr.append(p2p)
    return gE_arr


""" calculate the HFCF of bearing """


def high_frequency_crest_factor(arr, filter_from: int, filter_to: int, sample_rate, window: str):
    hfcf_arr = []
    for i in range(len(arr)):
        _samples_1 = filter_data(
            arr[i],
            "BANDPASS",
            filter_from,
            filter_to,
            sample_rate[i],
            window
        )
        crestFactor = crest_factor(_samples_1)
        hfcf_arr.append(crestFactor)
    return hfcf_arr


# def fresh_laser_pulse(laserArr):
#     for i in range(len(laserArr)):
#         if laserArr[i] <= 1:
#             laserArr[i] = 0
#         else:
#             laserArr[i] = 2.5
#     return laserArr

def fresh_laser_pulse(laserArr):
    mean=np.mean(laserArr)
    for i in range(len(laserArr)):
        if laserArr[i]<= mean:
            laserArr[i]=0
        else:
            laserArr[i]=1
    return laserArr

def fresh_tacho_pulse(tachoArr, symCheck):
    if symCheck==1:
        tachoArr*=-1
    tachoArr-=np.min(tachoArr)
    # mean=np.mean(tachoArr)
    # for i in range(len(tachoArr)):
    #     if tachoArr[i]< mean:
    #         tachoArr[i]=mean
    #     else:
    #         pass
    # tachoArr-=mean
    return tachoArr

def iso10816_judge(machineType, tocdo, congsuat, foundation="Rigid"):
    if foundation == None:
        foundation = "Rigid"
    if machineType == "GENERAL" or machineType == "PUMP" or machineType == "GEARBOX" or machineType == "FAN":
        if congsuat <= 15.0:
            return dfc.iso10816["iso108161"]["class1"]
        elif 15.0 < congsuat <= 75.0:
            return dfc.iso10816["iso108161"]["class2"]
        elif congsuat > 75.0 and foundation == "Rigid":
            return dfc.iso10816["iso108161"]["class3"]
        elif congsuat > 75.0 and foundation == "Flexible":
            return dfc.iso10816["iso108161"]["class4"]

    elif machineType == "STEAM TURBINE":
        if tocdo == 1500:
            return dfc.iso10816["iso108162"]["class1"]
        elif tocdo == 3000:
            return dfc.iso10816["iso108162"]["class2"]
        else:
            return dfc.iso10816["iso108162"]["class2"]
    elif machineType == "CRITICAL MACHINE":
        if 15.0 <= congsuat <= 300.0 and foundation == "Rigid":
            return dfc.iso10816["iso108163"]["class2"]
        elif 15.0 <= congsuat <= 300.0 and foundation == "Flexible":
            return dfc.iso10816["iso108163"]["class1"]
        elif 300.0 <= congsuat <= 50000.0 and foundation == "Rigid":
            return dfc.iso10816["iso108163"]["class3"]
        elif 300.0 <= congsuat <= 50000.0 and foundation == "Flexible":
            return dfc.iso10816["iso108163"]["class2"]
        else:
            return dfc.iso10816["iso108163"]["class2"]
    elif machineType == "PUMP":
        if congsuat <= 200:
            return dfc.iso10816["iso108167"]["class1"]
        elif congsuat > 200:
            return dfc.iso10816["iso108167"]["class2"]
        else:
            return dfc.iso10816["iso108167"]["class1"]
    else:
        return dfc.iso10816["iso108160"]["class1"]


def Acc_Pk_indicator(data_arr, sample_rate_arr):
    Acc_Pk_arr = []
    for i in range(len(data_arr)):
        filtered_signal = filter_data(
            data_arr[i],
            "HIGHPASS",
            1000,
            20000,
            sample_rate_arr[i],
            window="Hanning"
        )
        AccRms = rmsValue(filtered_signal)
        Acc_Pk_arr.append(AccRms * 1.414)
    return Acc_Pk_arr


def frequency_tsa(arr, step, sample_rate):
    if len(arr)>1000:
        try:
            _index = np.arange(0, len(arr) + 1, step, dtype=int)
            if len(_index) > 4:
                N = 2 * step
                sum_fft = np.zeros(N)
                w = signal.hann(N, sym=False)
                for i in range(len(_index) - 2):
                    temp_arr = arr[_index[i]:_index[i + 2]]
                    yf = fftpack.fft(temp_arr * w) * (2*np.sqrt(2) / N)
                    yf = np.abs(yf)
                    sum_fft += yf
                T = 1.0 / sample_rate
                sum_fft = sum_fft[5:int(N / 2)] / (len(_index) - 2)
                xf = np.linspace(0.0, 1.0 / (2.0 * T), int(N / 2))
                return [sum_fft, xf[5:]]
            else:
                N = len(arr)
                w = signal.hann(N, sym=False)  # Hann (Hanning) window
                xf = np.linspace(0.0, 1.0 / (2.0 / sample_rate), int(N / 2))
                xf = xf[2:]
                yf = fftpack.fft(arr * w) * (2*np.sqrt(2) / N)
                yf = np.abs(yf[2:int(N / 2)])
                return [yf, xf]
        except:
            yf=np.zeros(100)
            xf=np.ones(100)
            return[yf, xf]
    else:
        yf=np.zeros(100)
        xf=np.ones(100)
        return[yf, xf]


def calculate_enveloped_signal(origin_config):
    try:
        _sample_rate = origin_config.sensor_config["sample_rate"]
        canal_1 = origin_config.sensor_config["sensor_data"][0]  # Copy list by value not by reference
        canal_2 = origin_config.sensor_config["sensor_data"][1]
        canal_3 = origin_config.sensor_config["sensor_data"][2]
        filter_type = "BANDPASS"
        filter_from = origin_config.frequency_config_struct["FilterFrom"]  # high pass cutoff freq
        filter_to = origin_config.frequency_config_struct["FilterTo"]  # low pass cutoff freq
        win_var = origin_config.frequency_config_struct["Window"]

        filter_from = int(filter_from)
        filter_to = int(filter_to)
        if filter_from >= filter_to and filter_type == "BANDPASS":
            filter_from = dfc._ENV_BANDPASS_FROM
            filter_to = dfc._ENV_BANDPASS_TO

        if filter_type:
            _samples_1 = filter_data(
                canal_1,
                filter_type,
                filter_from,
                filter_to,
                _sample_rate,
                win_var
            )
            _samples_2 = filter_data(
                canal_2,
                filter_type,
                filter_from,
                filter_to,
                _sample_rate,
                win_var
            )
            _samples_3 = filter_data(
                canal_3,
                filter_type,
                filter_from,
                filter_to,
                _sample_rate,
                win_var
            )

        analytical_signal1 = hilbert(_samples_1)
        analytical_signal2 = hilbert(_samples_2)
        analytical_signal3 = hilbert(_samples_3)
        # enveloped_signal1= _samples_1 + 1j*analytical_signal1
        # enveloped_signal2= _samples_2 + 1j*analytical_signal2
        # enveloped_signal3= _samples_3 + 1j*analytical_signal3

        amplitude_envelope1 = np.abs(analytical_signal1)
        amplitude_envelope2 = np.abs(analytical_signal2)
        amplitude_envelope3 = np.abs(analytical_signal3)

        amplitude_envelope1 = filter_data(
            amplitude_envelope1,
            "LOWPASS",
            filter_from,
            filter_to / 2,
            _sample_rate,
            win_var
        )
        amplitude_envelope2 = filter_data(
            amplitude_envelope2,
            "LOWPASS",
            filter_from,
            filter_to / 2,
            _sample_rate,
            win_var
        )
        amplitude_envelope3 = filter_data(
            amplitude_envelope3,
            "LOWPASS",
            filter_from,
            filter_to / 2,
            _sample_rate,
            win_var
        )
        n_samples = len(amplitude_envelope1)
        if (n_samples != 0):
            return [amplitude_envelope1, amplitude_envelope2, amplitude_envelope3]
        else:
            return -1
    except:
        return -1