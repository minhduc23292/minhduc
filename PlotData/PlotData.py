import tkinter as Tk
import matplotlib

matplotlib.use('TKAgg')
# from curses import window
from Calculation.calculate import *
import numpy as np
from scipy import fftpack, signal, integrate

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter

import cmath
from digitalFilter.digitalFilter import filter_data
import defaultConfig.default_config as dfc
from i18n import _
import os
from scipy.stats import kurtosis
from tkinter import PhotoImage
current_directory = os.path.dirname(os.path.realpath(__file__))
parent_directory = os.path.dirname(current_directory)
save_path = f"{parent_directory}/storage/"


class PLT(FigureCanvasTkAgg):
    def plot1chanel(self, canal, unit, sample_rate, win_var="Hanning"):
        max_freq = int(sample_rate / 2.56)
        N = len(canal)
        # ----------------- Plotting ---------------
        X1 = np.linspace(0, int((N / sample_rate) * 1000), N)  # X axis, 5000 sps, 1/5 ms.
        titY = _("Amplitude") + ' ' + f'({unit})'
        axes_arr = self.figure.get_axes()
        cc = len(axes_arr)
        while cc > 0:
            self.figure.delaxes(axes_arr[cc - 1])
            cc -= 1
        self.figure.add_subplot(2, 1, 1)
        self.figure.add_subplot(2, 1, 2)
        self.figure.subplots_adjust(left=0.1, right=0.91, top=0.95, bottom=0.1)
        ax_11, ax_12 = self.figure.get_axes()
        ax_11.clear()
        ax_11.yaxis.set_major_formatter(FormatStrFormatter('%0.3f'))
        ax_11.plot(X1, canal, color='blue', linewidth=0.4)
        ax_11.set_xlabel("ms")
        ax_11.set_ylabel(titY)
        ax_11.grid()  # Shows grid.

        # Window function
        if (win_var == "Hanning"):
            w = signal.hann(N, sym=False)  # Hann (Hanning) window
        elif (win_var == "Blackman"):
            w = signal.blackman(N, sym=False)  # Blackman window
        elif (win_var == "Flatop"):
            w = signal.flattop(N, sym=False)  # Flattop window
        elif (win_var == "Reactangular"):
            w = 1  # Rectangular window
        T = 1.0 / sample_rate
        yf = fftpack.fft(canal * w) * (2*np.sqrt(2)/N)
        yf1 = np.abs(yf[:(int(N // 2))])
        xf = fftpack.fftfreq(N, T)[0:int(N // 2)]
        ax_12.clear()
        ax_12.yaxis.set_major_formatter(FormatStrFormatter('%0.3f'))
        ax_12.plot(xf[2:], yf1[2:], color='blue', linewidth=0.5)
        ax_12.grid()
        ax_12.set_xlabel("Hz")
        ax_12.set_ylabel(_("Amplitude") + f' {unit}')
        ax_12.set_xlim(xmax=max_freq)
        self.draw()

    def plot_all_chanel(self, canal_1, canal_2, canal_3, unit, sample_rate):
        num_datos = len(canal_1)
        read_time = (num_datos / sample_rate) * 1000
        # ----------------- Plotting ----------
        X1 = np.linspace(0, int(read_time), num=num_datos)  # X axis, 5000 sps, 1/5 ms.
        titX = "Ch1" + f'({unit[0]})'
        titY = "Ch2" + f'({unit[1]})'
        titZ = "Ch3" + f'({unit[2]})'
        # ax_11, ax_12, ax_13 = self.figure.get_axes()
        axes_arr = self.figure.get_axes()
        cc = len(axes_arr)
        while cc > 0:
            self.figure.delaxes(axes_arr[cc - 1])
            cc -= 1
        self.figure.add_subplot(3, 1, 1)
        self.figure.add_subplot(3, 1, 2)
        self.figure.add_subplot(3, 1, 3)
        self.figure.subplots_adjust(left=0.1, right=0.98, top=0.98, bottom=0.1)
        ax_11, ax_12, ax_13 = self.figure.get_axes()
        ax_11.set_position([0.1, 0.7, 0.87, 0.26])
        ax_12.set_position([0.1, 0.4, 0.87, 0.26])
        ax_13.set_position([0.1, 0.1, 0.87, 0.26])
        self.figure.set_visible(True)
        ax_11.clear()
        ax_11.yaxis.set_major_formatter(FormatStrFormatter('%0.3f'))
        ax_11.plot(X1, canal_1, color='blue', linewidth=0.4)
        ax_11.set_ylabel(titX)
        ax_11.set_xticks([])
        ax_11.grid()  # Shows grid.

        # Channel Y
        ax_12.clear()
        ax_12.yaxis.set_major_formatter(FormatStrFormatter('%0.3f'))
        ax_12.plot(X1, canal_2, color='blue', linewidth=0.4)
        ax_12.set_ylabel(titY)
        ax_12.set_xticks([])
        ax_12.grid()  # Shows grid.

        # Channel Z
        ax_13.clear()
        ax_13.yaxis.set_major_formatter(FormatStrFormatter('%0.3f'))
        ax_13.plot(X1, canal_3, color='blue', linewidth=0.4)
        ax_13.set_xlabel("Time[ms]")
        ax_13.set_ylabel(titZ)
        # ax_13.set_xticks([])
        ax_13.grid(axis='y')  # Shows grid.
        self.draw()


    def plot_psd(self, canal_1, canal_2, canal_3, sample_rate, unit, ch, show_unit, win_var="Hanning"):
        """Calculate the PSD of signal and plot
        Input:
            canal_1, canal_2, canal_3: [array] of signal
            sample_rate: [int] sample rate
            range: [array] range to plot
            unit:[list] list of unit
            ch: [list] list of chanel
            show_unit: [str] unit if y axis
            winvar: [str] window type
        Output:
        https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.welch.html
        https://blog.endaq.com/why-the-power-spectral-density-psd-is-the-gold-standard-of-vibration-analysis

        """
        window = "hann"
        if (win_var == "Hanning"):
            window = "hann"
        elif (win_var == "Blackman"):
            window = "blackman"
        elif (win_var == "Flatop"):
            window = "flattop"
        elif (win_var == "Reactangular"):
            window = "boxcar"
        else:
            pass
        N = len(canal_1)
        nperseg = 2048  # Segment length
        noverlab = 1024  # Number of overlap point, defaut is a half of segment
        if N < nperseg:
            nperseg = N
            noverlab = N // 2

        ax_21, ax_22, ax_23 = self.figure.get_axes()
        self.figure.set_visible(True)
        ax_21.clear()

        # Chanel X
        canal_fft = canal_1
        f, Pxx_den = signal.welch(canal_fft, sample_rate, window, nperseg=nperseg, noverlap=noverlab)
        if show_unit == "Original":
            ax_21.plot(f, Pxx_den, color='blue', linewidth=0.5)
            ax_21.set_ylabel(f"Ch{str(ch[0])}" + f' | {unit[0]}^2/Hz')
            ax_21.yaxis.set_major_formatter(FormatStrFormatter('%0.3f'))
        else:
            ax_21.plot(f, 10 * np.log10(Pxx_den), color='blue', linewidth=0.5)
            ax_21.set_ylabel(f"Ch{str(ch[0])}" + f' | dB')
            ax_21.yaxis.set_major_formatter(FormatStrFormatter('%0.1f'))
        ax_21.grid(color='green', linestyle='--', linewidth=0.3)
        ax_21.set_xticks([])

        # Chanel Y
        canal_fft = canal_2
        f, Pxx_den = signal.welch(canal_fft, sample_rate, window, nperseg=nperseg, noverlap=noverlab)
        ax_22.clear()
        if show_unit == "Original":
            ax_22.set_ylabel(f"Ch{str(ch[1])}" + f' | {unit[1]}^2/Hz')
            ax_22.yaxis.set_major_formatter(FormatStrFormatter('%0.3f'))
            ax_22.plot(f, Pxx_den, color='blue', linewidth=0.5)

        else:
            ax_22.set_ylabel(f"Ch{str(ch[1])}" + f' | dB')
            ax_22.yaxis.set_major_formatter(FormatStrFormatter('%0.1f'))
            ax_22.plot(f, 10 * np.log10(Pxx_den), color='blue', linewidth=0.5)

        ax_22.grid(color='green', linestyle='--', linewidth=0.3)
        ax_22.set_xticks([])

        # Chanel Z
        canal_fft = canal_3
        f, Pxx_den = signal.welch(canal_fft, sample_rate, window, nperseg=nperseg, noverlap=noverlab)
        ax_23.clear()
        if show_unit == "Original":
            ax_23.yaxis.set_major_formatter(FormatStrFormatter('%0.3f'))
            ax_23.plot(f, Pxx_den, color='blue', linewidth=0.5)
            ax_23.set_ylabel(f"Ch{str(ch[2])}" + f' | {unit[2]}^2/Hz')
        else:
            ax_23.yaxis.set_major_formatter(FormatStrFormatter('%0.1f'))
            ax_23.plot(f, 10 * np.log10(Pxx_den), color='blue', linewidth=0.5)
            ax_23.set_ylabel(f"Ch{str(ch[2])}" + f' | dB')
        ax_23.grid(color='green', linestyle='--', linewidth=0.3, axis='y')
        ax_23.set_xlabel('Hz', fontsize=12)
        self.draw()

    def plot_fft(self, canal_1, canal_2, canal_3, sample_rate, unit, ch, win_var="Hanning"):
        """Calculate the fft of signal and plot
        Input:
            canal_1, canal_2, canal_3: [float array] of signal
            sample_rate: [int] sample rate
            range: [array] range to plot
            unit:[list] list of unit
            ch: [list] list of chanel
            winvar: [str] window type
        Output:

        """
        N = len(canal_1)  # length of the signal
        # Window function
        if (win_var == "Hanning"):
            w = signal.hann(N, sym=False)  # Hann (Hanning) window
        elif (win_var == "Blackman"):
            w = signal.blackman(N, sym=False)  # Blackman window
        elif (win_var == "Flatop"):
            w = signal.flattop(N, sym=False)  # Flattop window
        elif (win_var == "Reactangular"):
            w = 1  # Rectangular window

        T = 1.0 / sample_rate
        y = canal_1
        yf = fftpack.fft(y * w) * (2*np.sqrt(2)/N)
        yf = yf[2:(int(N / 2))]
        xf = np.linspace(0.0, 1.0 / (2.0 * T), int(N / 2))
        ax_21, ax_22, ax_23 = self.figure.get_axes()
        ax_21.set_position([0.1, 0.7, 0.87, 0.26])
        ax_22.set_position([0.1, 0.4, 0.87, 0.26])
        ax_23.set_position([0.1, 0.1, 0.87, 0.26])
        self.figure.set_visible(True)
        ax_21.clear()
        ax_21.yaxis.set_major_formatter(FormatStrFormatter('%0.3f'))
        ax_21.plot(xf[2:], np.abs(yf), color='blue', linewidth=0.5)
        ax_21.grid(color='green', linestyle='--', linewidth=0.3)
        ax_21.set_xticks([])
        ax_21.set_ylabel(f"Ch{str(ch[0])}" + f' | {unit[0]}')

        # Channel Y

        N = len(canal_2)  # length of the signal
        T = 1.0 / sample_rate
        y = canal_2
        yf = fftpack.fft(y * w) * (2*np.sqrt(2)/N)
        yf = yf[2:int(N / 2)]
        xf = np.linspace(0.0, 1.0 / (2.0 * T), int(N / 2))

        ax_22.clear()
        ax_22.yaxis.set_major_formatter(FormatStrFormatter('%0.3f'))
        ax_22.plot(xf[2:], np.abs(yf), color='blue', linewidth=0.5)
        ax_22.grid(color='green', linestyle='--', linewidth=0.3)
        ax_22.set_xticks([])
        ax_22.set_ylabel(f"Ch{str(ch[1])}" + f' | {unit[1]}')

        # Channel Z

        N = len(canal_3)  # length of the signal
        T = 1.0 / sample_rate
        y = canal_3
        yf = fftpack.fft(y * w) * (2*np.sqrt(2)/N)
        yf = yf[2:int(N / 2)]
        xf = np.linspace(0.0, 1.0 / (2.0 * T), int(N / 2))
        ax_23.clear()
        ax_23.yaxis.set_major_formatter(FormatStrFormatter('%0.3f'))
        ax_23.plot(xf[2:], np.abs(yf), color='blue', linewidth=0.5)
        ax_23.grid(color='green', linestyle='--', linewidth=0.3, axis='y')
        ax_23.set_xlabel('Frequency [Hz]', fontsize=12)
        ax_23.set_ylabel(f"Ch{str(ch[2])}" + f' | {unit[2]}')
        self.draw()

    def plot_waterfall(self, data_arr, date_arr, sample_rate, viewRange, export_png=False):
        file_name = 'waterfall.png'
        completeName = os.path.join(save_path, file_name)
        scale = 1.2
        h_num = len(data_arr)
        axes_arr = self.figure.get_axes()
        cc = len(axes_arr)
        while cc > 0:
            self.figure.delaxes(axes_arr[cc - 1])
            cc -= 1
        self.figure.add_subplot(1, 1, 1, projection="3d")
        self.figure.set_size_inches(9.2, 10)
        self.figure.subplots_adjust(left=-0.25, right=1.1, top=1.1, bottom=0.38)
        self.figure.set_visible(True)
        ax_41, = self.figure.get_axes()
        ax_41.clear()
        ax_41.view_init(30, -80)  # tham so 1 la goc nang mat phang xy, tham so 2 la goc quay truc z
        ax_41.set_box_aspect((3, 3, 1))
        ax_41.w_xaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
        ax_41.w_yaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
        ax_41.w_zaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
        ax_41.zaxis.set_major_formatter(FormatStrFormatter('%0.2f'))

        for i in range(h_num):
            N = len(data_arr[i])
            w = signal.hann(N, sym=False)  # Hann (Hanning) window
            # xf = np.linspace(0.0, viewRange[1], int(viewRange[1]*n/sample_rate[i]))
            xf = np.linspace(0.0, sample_rate[i] / 2, int(N / 2))
            y = data_arr[i]
            yf = fftpack.fft(y * w) * (2*np.sqrt(2) / N)
            yf1 = np.abs(yf)[:int(N / 2)]
            zz = i * np.ones(len(yf1))
            if viewRange[1] < sample_rate[i] / 2.56:
                plotRange = int(viewRange[1] * N / sample_rate[i])
            else:
                plotRange = int(N / 2.56)
            if plotRange < 100:
                plotRange = 100
            ax_41.plot3D(xf[:plotRange], zz[:plotRange], yf1[:plotRange], color='black', linewidth=0.3)
        zmin, zmax = ax_41.get_zlim()
        ax_41.set_xlim3d(left=viewRange[0], right=viewRange[1])
        ax_41.set_zlim3d(0, zmax * scale)
        ax_41.set_yticks([i for i in range(len(date_arr))])
        ax_41.set_yticklabels(date_arr)
        ax_41.set_xlabel(_("Frequency(Hz)"))
        ax_41.set_zlabel(_("Amplitude"))
        if export_png == True:
            self.figure.savefig(completeName, bbox_inches='tight')
            return
        self.draw()

    def plot_all_history(self, arr, d_arr, sample_rate, viewRange, flag, tsa_use, tsa_bin, export_png=False):
        self.figure.set_size_inches(9.2, 5.2)
        file_name = ''
        h_num = len(arr)
        axes_arr = self.figure.get_axes()
        cc = len(axes_arr)
        while cc > 0:
            self.figure.delaxes(axes_arr[cc - 1])
            cc -= 1
        axes_arr = self.figure.get_axes()
        cc = len(axes_arr)
        while cc < h_num:
            self.figure.add_subplot(h_num, 1, cc + 1)
            cc += 1
        axes_arr1 = self.figure.get_axes()
        self.figure.set_visible(True)
        for i in axes_arr:
            i.cla()
            i.clear()
        num_of_axes = len(axes_arr1)
        if num_of_axes == 1:
            self.figure.subplots_adjust(left=0.1, right=0.95, top=0.95, bottom=0.15)
        if num_of_axes == 2:
            self.figure.subplots_adjust(left=0.1, right=0.95, top=0.95, bottom=0.15)
        if num_of_axes == 3:
            self.figure.subplots_adjust(left=0.1, right=0.95, top=0.95, bottom=0.15)
        if num_of_axes == 4:
            self.figure.subplots_adjust(left=0.1, right=0.95, top=0.95, bottom=0.15)
        if num_of_axes == 5:
            self.figure.subplots_adjust(left=0.1, right=0.95, top=0.95, bottom=0.15)
        if num_of_axes == 6:
            self.figure.subplots_adjust(left=0.1, right=0.95, top=0.95, bottom=0.15)
        if flag == 0 or flag == 2 or flag == 3:
            if flag == 0:
                file_name = 'frequency.png'
            elif flag == 2:
                file_name = "envelop.png"
            elif flag == 3:
                file_name = 'velocity_frequency.png'
            completeName = os.path.join(save_path, file_name)
            for i in range(h_num):
                if tsa_use == 1:
                    [yf2, xf2] = frequency_tsa(arr[i], tsa_bin, sample_rate[i])
                else:
                    n = len(arr[i])
                    if n>100:
                        w = signal.hann(n, sym=False)  # Hann (Hanning) window
                        xf2 = np.linspace(0.0, 1.0 / (2.0 / sample_rate[i]), int(n / 2))
                        xf2 = xf2[2:]
                        y = arr[i]
                        yf = fftpack.fft(y * w) * (2*np.sqrt(2) / n)
                        yf2 = np.abs(yf[2:int(n / 2)])
                    else:
                        xf2=np.zeros(10)
                        yf2=np.zeros(10)
                axes_arr1[i].yaxis.set_major_formatter(FormatStrFormatter('%0.2f'))
                axes_arr1[i].plot(xf2, yf2, color='blue', linewidth=0.5)
                axes_arr1[i].grid()
                axes_arr1[i].set_ylabel(d_arr[i] + '|')
                axes_arr1[i].set_xlim(xmax=viewRange[1], xmin=viewRange[0])
            for i in range(h_num - 1):
                axes_arr1[i].set_xticklabels([])
            axes_arr1[-1].set_xlabel(_("Frequency [Hz]"))
        elif flag == 1:
            file_name = 'waveform.png'
            completeName = os.path.join(save_path, file_name)
            for i in range(h_num):
                n = len(arr[i])
                read_time = (n / sample_rate[i]) * 1000
                X1 = np.linspace(0, int(read_time), num=n)
                axes_arr1[i].yaxis.set_major_formatter(FormatStrFormatter('%0.2f'))
                axes_arr1[i].plot(X1, arr[i], color='blue', linewidth=0.5)
                axes_arr1[i].grid()
                axes_arr1[i].set_ylabel(d_arr[i] + '|')
                [left, right] = axes_arr1[i].get_xlim()
                xmax = right
                if viewRange[1] < xmax:
                    xmax = viewRange[1]
                axes_arr1[i].set_xlim(xmax=xmax, xmin=viewRange[0])
            for i in range(h_num - 1):
                axes_arr1[i].set_xticklabels([])
            axes_arr1[-1].set_xlabel(_("Time [ms]"))
        if export_png == True:
            self.figure.savefig(completeName, bbox_inches='tight')
            return
        self.draw()

    def plot_velocity_spectrum(self, canal_1, canal_2, canal_3, sample_rate, ch):
        axes_arr1 = self.figure.get_axes()
        n=len(canal_1)
        xf2 = np.linspace(0.0, 1.0 / (2.0/sample_rate), int(n / 2))
        xf2=xf2[5:]
        w = signal.hann(n, sym=False)  # Hann (Hanning) window
        signalArr=[canal_1, canal_2, canal_3]
        for i in range(3):
            y = signalArr[i]
            yf = fftpack.fft(y * w) * (2*np.sqrt(2) / n)
            yf2 = np.abs(yf[5:int(n / 2)])
            for j in range(len(yf2)):
                yf2[j]/=0.0002*np.pi*xf2[j]
            axes_arr1[i].yaxis.set_major_formatter(FormatStrFormatter('%0.2f'))
            axes_arr1[i].plot(xf2, yf2, color='blue', linewidth=0.5)
            axes_arr1[i].grid(color='green', linestyle='--', linewidth=0.3, axis='y')
            axes_arr1[i].set_ylabel(f"Ch{str(ch[i])}" + f' | mm/s')
        for i in range(2):
            axes_arr1[i].set_xticklabels([])
        axes_arr1[-1].set_xlabel(_("Frequency [Hz]"))
        self.draw()


    def plot_velocity_spectral_kiem_tra_tich_phan(self, arr, d_arr, sample_rate, viewRange, export_png=False):
        self.figure.set_size_inches(9.2, 5.2)
        file_name='velocity_frequency.png'
        completeName = os.path.join(save_path, file_name)
        h_num = len(arr)
        axes_arr = self.figure.get_axes()
        cc=len(axes_arr)
        while cc>0:
            self.figure.delaxes(axes_arr[cc-1])
            cc-=1
        axes_arr = self.figure.get_axes()
        cc=len(axes_arr)
        while  cc<h_num:
            self.figure.add_subplot(h_num,1,cc+1)
            cc+=1
        axes_arr1 = self.figure.get_axes()
        self.figure.set_visible(True)
        for i in axes_arr:
            i.cla()
            i.clear()
        num_of_axes=len(axes_arr1)
        if num_of_axes == 1:
            self.figure.subplots_adjust(left=0.1, right=0.95, top=0.95, bottom=0.15)
        if num_of_axes == 2:
            self.figure.subplots_adjust(left=0.1, right=0.95, top=0.95, bottom=0.15)
        if num_of_axes == 3:
            self.figure.subplots_adjust(left=0.1, right=0.95, top=0.95, bottom=0.15)
        if num_of_axes == 4:
            self.figure.subplots_adjust(left=0.1, right=0.95, top=0.95, bottom=0.15)
        if num_of_axes == 5:
            self.figure.subplots_adjust(left=0.1, right=0.95, top=0.95, bottom=0.15)
        if num_of_axes == 6:
            self.figure.subplots_adjust(left=0.1, right=0.95, top=0.95, bottom= 0.15)
  
        for i in range(h_num):
            y = acc2vel(arr[i], sample_rate[i])
            # y-=np.mean(y)
            # y=filter_data(y, "BANDPASS", dfc._RMS_HIGHPASS_FROM, dfc._RMS_LOWPASS_TO,
            #                       sample_rate[i], window="Hanning")
            n = len(y)
            w = signal.hann(n, sym=False)  # Hann (Hanning) window
            xf2 = np.linspace(0.0, 1.0 / (2.0/sample_rate[i]), int(n / 2))
            xf2=xf2[5:]
            yf = fftpack.fft(y * w) * (2*np.sqrt(2) / n)
            yf2 = np.abs(yf[5:int(n / 2)])
            axes_arr1[i].yaxis.set_major_formatter(FormatStrFormatter('%0.2f'))
            axes_arr1[i].plot(xf2, yf2, color='blue', linewidth=0.5)
            axes_arr1[i].grid()
            axes_arr1[i].set_ylabel(d_arr[i]+'|')
            axes_arr1[i].set_xlim(xmax=viewRange[1], xmin=viewRange[0])
        for i in range(h_num-1):
            axes_arr1[i].set_xticklabels([])
        axes_arr1[-1].set_xlabel(_("Frequency [Hz]"))
        
        if export_png==True:
            self.figure.savefig(completeName, bbox_inches='tight')
            return
        self.draw()

    def plot_history_velocity_spectral(self, arr, d_arr, sample_rate, viewRange, tsa_use, tsa_bin, export_png=False):
        self.figure.set_size_inches(9.2, 5.2)
        file_name='velocity_frequency.png'
        completeName = os.path.join(save_path, file_name)
        h_num = len(arr)
        axes_arr = self.figure.get_axes()
        cc=len(axes_arr)
        while cc>0:
            self.figure.delaxes(axes_arr[cc-1])
            cc-=1
        axes_arr = self.figure.get_axes()
        cc=len(axes_arr)
        while  cc<h_num:
            self.figure.add_subplot(h_num,1,cc+1)
            cc+=1
        axes_arr1 = self.figure.get_axes()
        self.figure.set_visible(True)
        for i in axes_arr:
            i.cla()
            i.clear()
        num_of_axes=len(axes_arr1)
        if num_of_axes == 1:
            self.figure.subplots_adjust(left=0.1, right=0.95, top=0.95, bottom=0.15)
        if num_of_axes == 2:
            self.figure.subplots_adjust(left=0.1, right=0.95, top=0.95, bottom=0.15)
        if num_of_axes == 3:
            self.figure.subplots_adjust(left=0.1, right=0.95, top=0.95, bottom=0.15)
        if num_of_axes == 4:
            self.figure.subplots_adjust(left=0.1, right=0.95, top=0.95, bottom=0.15)
        if num_of_axes == 5:
            self.figure.subplots_adjust(left=0.1, right=0.95, top=0.95, bottom=0.15)
        if num_of_axes == 6:
            self.figure.subplots_adjust(left=0.1, right=0.95, top=0.95, bottom= 0.15)
  
        for i in range(h_num):
            if tsa_use==1:
                [yf2, xf2] = frequency_tsa(arr[i], tsa_bin, sample_rate[i] )
            else:
                n = len(arr[i])
                if n>100:
                    w = signal.hann(n, sym=False)  # Hann (Hanning) window
                    xf2 = np.linspace(0.0, 1.0 / (2.0/sample_rate[i]), int(n / 2))
                    xf2=xf2[5:]
                    y = arr[i]
                    yf = fftpack.fft(y * w) * (2*np.sqrt(2) / n)
                    yf2 = np.abs(yf[5:int(n / 2)])
                else:
                    xf2=np.ones(100)
                    yf2=np.zeros(100)
            for j in range(len(yf2)):
                yf2[j]/=0.0002*np.pi*xf2[j]
            axes_arr1[i].yaxis.set_major_formatter(FormatStrFormatter('%0.2f'))
            axes_arr1[i].plot(xf2, yf2, color='blue', linewidth=0.5)
            axes_arr1[i].grid()
            axes_arr1[i].set_ylabel(d_arr[i]+'|')
            axes_arr1[i].set_xlim(xmax=viewRange[1], xmin=viewRange[0])
        for i in range(h_num-1):
            axes_arr1[i].set_xticklabels([])
        axes_arr1[-1].set_xlabel(_("Frequency [Hz]"))
        
        if export_png==True:
            self.figure.savefig(completeName, bbox_inches='tight')
            return
        self.draw()


    def plot_trend(self, data_arr, d_arr, sample_rate_arr, sensorPosition, isoStandard, rpm, bearing_bore, view_arr,
                   export_png=False):
        file_name = "trend.png"
        completeName = os.path.join(save_path, file_name)
        h_num = len(data_arr)
        if bearing_bore != None:
            gE_alert = np.power(dfc._GE_FMAX / 1000.0, 0.43) * 1.09 * 0.0001 * rpm * np.power(bearing_bore, 0.55)
            gE_danger = 3 * gE_alert
            gE_alert_arr = np.ones(h_num + 1) * gE_alert
            gE_danger_arr = np.ones(h_num + 1) * gE_danger
        else:
            gE_alert_arr = np.zeros(h_num + 1)
            gE_danger_arr = np.zeros(h_num + 1)
        hfcf_alert = 6.5
        hfcf_danger = 15.0

        velocity_alert = np.ones(h_num + 1) * isoStandard[1]
        velocity_danger = np.ones(h_num + 1) * isoStandard[2]

        hfcf_alert_arr = np.ones(h_num + 1) * hfcf_alert
        hfcf_danger_arr = np.ones(h_num + 1) * hfcf_danger
        acc_alert = np.ones(h_num + 1) * dfc._ACC_ALERT
        acc_danger = np.ones(h_num + 1) * dfc._ACC_DANGER

        date_arr = []
        rms_arr = []
        p2p_arr = []
        gE_arr = []
        hfcf_arr = []
        Acc_Pk_arr = []
        tick_arr = [i for i in range(h_num)]
        tick_arr1 = [i for i in range(h_num + 1)]
        for i in range(h_num):
            if sensorPosition[-1] == "A":
                temp_vel_arr = acc2vel(data_arr[i], sample_rate_arr[i])
            else:
                temp_vel_arr = data_arr[i]
            vel_arr = filter_data(temp_vel_arr, "BANDPASS", dfc._RMS_HIGHPASS_FROM, dfc._RMS_LOWPASS_TO,
                                  sample_rate_arr[i], window="Hanning")
            vel_arr-=np.mean(vel_arr)
            rms_arr.append(rmsValue(vel_arr))
            date_arr.append(d_arr[i])
        rms_arr = np.flip(np.array(rms_arr))
        date_arr = np.flip(np.array(date_arr))
        if sensorPosition[-1] == "A":
            gE_arr = gE(data_arr, dfc._GE_HIGHPASS_FROM, dfc._GE_LOWPASS_TO, sample_rate_arr, window="Hanning")
            hfcf_arr = high_frequency_crest_factor(data_arr, dfc._HFCF_BANDPASS_FROM, dfc._HFCF_BANDPASS_TO, \
                                                   sample_rate_arr, window="Hanning")
            Acc_Pk_arr = Acc_Pk_indicator(data_arr, sample_rate_arr)
            # flip the array to draw in time ascending order
            gE_arr = np.flip(np.array(gE_arr))
            hfcf_arr = np.flip(np.array(hfcf_arr))
            Acc_Pk_arr = np.flip(np.array(Acc_Pk_arr))
        self.figure.set_size_inches(9.2, 5.1)
        axes_arr = self.figure.get_axes()
        cc = len(axes_arr)
        while cc > 0:
            self.figure.delaxes(axes_arr[cc - 1])
            cc -= 1
        ax_41 = self.figure.add_subplot(2, 2, 1)
        ax_41.set_position([0.08, 0.6, 0.42, 0.37])
        ax_42 = self.figure.add_subplot(2, 2, 2)
        ax_42.set_position([0.56, 0.6, 0.42, 0.37])
        ax_43 = self.figure.add_subplot(2, 2, 3)
        ax_43.set_position([0.08, 0.2, 0.42, 0.37])
        ax_44 = self.figure.add_subplot(2, 2, 4)
        ax_44.set_position([0.56, 0.2, 0.42, 0.37])
        self.figure.set_visible(True)
        ax_41, ax_42, ax_43, ax_44 = self.figure.get_axes()
        ax_41.clear()
        ax_42.clear()
        ax_43.clear()
        ax_44.clear()

        ax_41.set_ylabel(_('Amplitude'))
        ax_41.set_xticks(tick_arr)
        ax_41.set_xticklabels([], rotation=90)
        ax_41.yaxis.set_major_formatter(FormatStrFormatter('%0.1f'))

        ax_42.set_xticks(tick_arr)
        ax_42.set_xticklabels([], rotation=90)
        ax_42.yaxis.set_major_formatter(FormatStrFormatter('%0.1f'))

        ax_43.set_ylabel(_('Amplitude'))
        ax_43.set_xticks(tick_arr)
        ax_43.set_xticklabels(date_arr, rotation=90)
        ax_43.yaxis.set_major_formatter(FormatStrFormatter('%0.1f'))

        ax_44.set_xticks(tick_arr)
        ax_44.set_xticklabels(date_arr, rotation=90)
        ax_44.yaxis.set_major_formatter(FormatStrFormatter('%0.1f'))

        if view_arr[0] == 1:
            ax_44.plot(tick_arr, rms_arr, color='blue', linestyle='solid', marker='o', \
                       markerfacecolor='red', markersize=5, label=_("Velocity RMS (mm/s)"))
            ax_44.plot(tick_arr1, velocity_alert, linewidth=0.3, color="orange")
            ax_44.plot(tick_arr1, velocity_danger, linewidth=0.3, color="red")
            ax_44.text(tick_arr1[-1] - 0.1, velocity_alert[-1] + 0.1, str(velocity_alert[-1])[0:3])
            ax_44.text(tick_arr1[-1] - 0.1, velocity_danger[-1] + 0.1, str(velocity_danger[-1])[0:3])
            for index, value in enumerate(rms_arr):
                    ax_44.text(index, value+0.2, str(value)[0:4])
            ymin, ymax = ax_44.get_ylim()
            ax_44.set_ylim(0, ymax * 1.5)
            ax_44.legend(bbox_to_anchor=(1, 1), loc='upper right', borderaxespad=0.0)
            ax_44.xaxis.grid(True)
        if sensorPosition[-1] == "A":
            if view_arr[1] == 1:
                ax_42.plot(tick_arr, Acc_Pk_arr, color="blue", linestyle='solid', marker='o', \
                           markerfacecolor='red', markersize=5, label=_("Accelleration Pk (g)"))
                ax_42.plot(tick_arr1, acc_alert, linewidth=0.3, color="orange")
                ax_42.plot(tick_arr1, acc_danger, linewidth=0.3, color="red")
                ax_42.text(tick_arr1[-1] - 0.1, acc_alert[-1] + 0.1, str(acc_alert[-1])[0:3])
                ax_42.text(tick_arr1[-1] - 0.1, acc_danger[-1] + 0.1, str(acc_danger[-1])[0:3])
                for index, value in enumerate(Acc_Pk_arr):
                    ax_42.text(index, value+0.2, str(value)[0:4])
            if view_arr[2] == 1:
                ax_43.plot(tick_arr, gE_arr, color="blue", linestyle='solid', marker='o', \
                           markerfacecolor='red', markersize=5, label="BRGs-gE")
                ax_43.plot(tick_arr1, gE_alert_arr, linewidth=0.3, color="orange")
                ax_43.plot(tick_arr1, gE_danger_arr, linewidth=0.3, color="red")
                ax_43.text(tick_arr1[-1] - 0.1, gE_alert_arr[-1] + 0.1, str(gE_alert_arr[-1])[0:3])
                ax_43.text(tick_arr1[-1] - 0.1, gE_danger_arr[-1] + 0.1, str(gE_danger_arr[-1])[0:3])
                for index, value in enumerate(gE_arr):
                    ax_43.text(index, value+0.2, str(value)[0:4])
            if view_arr[3] == 1:
                ax_41.plot(tick_arr, hfcf_arr, color="blue", linestyle='solid', marker='o', \
                           markerfacecolor='red', markersize=5, label="BRGs-HFCF")
                ax_41.plot(tick_arr1, hfcf_alert_arr, linewidth=0.3, color="orange")
                ax_41.plot(tick_arr1, hfcf_danger_arr, linewidth=0.3, color="red")
                ax_41.text(tick_arr1[-1] - 0.1, hfcf_alert_arr[-1] + 0.1, str(hfcf_alert_arr[-1])[0:3])
                ax_41.text(tick_arr1[-1] - 0.1, hfcf_danger_arr[-1] + 0.1, str(hfcf_danger_arr[-1])[0:3])
                for index, value in enumerate(hfcf_arr):
                    ax_41.text(index, value+0.2, str(value)[0:4])

            ymin, ymax = ax_42.get_ylim()
            ax_42.set_ylim(0, ymax * 1.5)
            ax_42.legend(bbox_to_anchor=(1, 1), loc='upper right', borderaxespad=0.0)
            ax_42.xaxis.grid(True)

            ymin, ymax = ax_43.get_ylim()
            ax_43.set_ylim(0, ymax * 1.5)
            ax_43.legend(bbox_to_anchor=(1, 1), loc='upper right', borderaxespad=0.0)
            ax_43.xaxis.grid(True)

            ymin, ymax = ax_41.get_ylim()
            ax_41.set_ylim(0, ymax * 1.5)
            ax_41.legend(bbox_to_anchor=(1, 1), loc='upper right', borderaxespad=0.0)
            ax_41.xaxis.grid(True)
            # ax_41.xaxis.set_major_locator(dates.AutoDateLocator())
            # ax_41.xaxis.set_major_formatter(hfmt)
        if export_png == True:
            self.figure.savefig(completeName, bbox_inches='tight')
            return
        self.draw()

    def plot_displacement(self, arr, arr_name):
        dis_p2p = []
        sensor_arr = []
        for arri in arr:
            dis_p2p.append(np.ptp(arri))
        for k in arr_name:
            sensor_arr.append("Sensor" + str(k + 1))
        ax_41, ax_42, ax_43, ax_44 = self.figure.get_axes()
        ax_44.clear()
        ax_44.set_visible(True)
        ax_44.yaxis.set_major_formatter(FormatStrFormatter('%0.1f'))

        width = 0.4
        ax_44.bar(sensor_arr, dis_p2p, color="green", width=width)
        margin = (1 - width) + width / 2
        ax_44.set_xlim(-margin, len(dis_p2p) - 1 + margin)
        ax_44.set_ylabel(_('ISO-10816 Displacement (um)'))
        # ax_44.grid()
        for index, value in enumerate(dis_p2p):
            ax_44.text(index, value, str(value)[0:4])
        self.draw()

    def plot_rms(self, vel_arr, threshold, sensorPosition):
        """ Draw the rms value in bar chart and plot the threshold
        Params:
        vel_arr:[ndarray] veloctity array data
        threshold: [array] threshold of iso10816
        name: sensor position"""
        h_num = len(vel_arr)
        rms_arr = []
        sensor_arr = []
        for k in sensorPosition:
            sensor_arr.append("Sensor" + str(k + 1))
        color_arr = []
        for i in range(h_num):
            # arr[i] = arr[i] - np.mean(arr[i])
            temp_rms = rmsValue(vel_arr[i])
            rms_arr.append(temp_rms)

            if temp_rms < threshold[0]:
                color_arr.append("green")
            elif threshold[0] < temp_rms < threshold[1]:
                color_arr.append("lime")
            elif threshold[1] < temp_rms < threshold[2]:
                color_arr.append("orange")
            else:
                color_arr.append("red")

        ax_41, ax_42, ax_43, ax_44 = self.figure.get_axes()
        ax_43.clear()
        ax_42.clear()
        ax_43.set_visible(True)
        ax_43.yaxis.set_major_formatter(FormatStrFormatter('%0.1f'))

        width = 0.4
        ax_43.bar(sensor_arr, rms_arr, color=color_arr, width=width, align='center')
        margin = (1 - width) + width / 2
        ax_43.set_xlim(-margin, len(sensor_arr) - 1 + margin)
        for index, value in enumerate(rms_arr):
            ax_43.text(index, value, str(value)[0:4])
        ax_43.set_ylabel(_('ISO-10816 Velocity (mm/s)'))
        self.draw()


    def plot_gE_severity(self, gE_arr, hfcf_arr, arr_name, Fmax, rpm, bearing_dia):
        alert = np.power(Fmax / 1000.0, 0.43) * 1.09 * 0.0001 * rpm * np.power(bearing_dia, 0.55)
        danger = 3 * alert
        hfcf_alert = 6.5
        hfcf_danger = 15.0
        # sensor_arr = []
        color_arr = []
        hfcf_color_arr = []
        sensor_label = []
        for m in gE_arr:
            if m < alert:
                color_arr.append("green")
            elif alert < m < danger:
                color_arr.append("orange")
            else:
                color_arr.append("red")

        for n in hfcf_arr:
            if n < hfcf_alert:
                hfcf_color_arr.append("green")
            elif hfcf_alert < n < hfcf_danger:
                hfcf_color_arr.append("orange")
            else:
                hfcf_color_arr.append("red")

        for k in arr_name:
            sensor_label.append("Sensor" + str(k + 1))
        sensor_arr = np.arange(len(arr_name))
        ax_41, ax_42, ax_43, ax_44 = self.figure.get_axes()
        ax_41.clear()
        ax_41.set_visible(True)
        ax_41.yaxis.set_major_formatter(FormatStrFormatter('%0.1f'))

        width = 0.4
        ax_41.bar(sensor_arr, gE_arr, color=color_arr, width=width, align='center')
        ax_41.bar(sensor_arr + width, hfcf_arr, color=hfcf_color_arr, width=width)
        margin = (1 - width) + width / 2
        ax_41.set_xlim(-margin, len(gE_arr) - 1 + margin)

        ax_41.set_ylabel(_('gE/HFCF for bearing'))
        ax_41.set_xticks(sensor_arr, sensor_label)
        for index, value in enumerate(gE_arr):
            ax_41.text(index - width / 2, value, "gE")
        for index, value in enumerate(hfcf_arr):
            ax_41.text(index + width / 2, value, "HFCF")
        self.draw()

    def plot_SBR_severity(self, SBRArr, AccPeak, sensor_arr):
        sbr_alert = dfc._SBR_ALERT
        sbr_danger = dfc._SBR_DANGER
        acc_alert = dfc._ACC_ALERT
        acc_danger = dfc._ACC_DANGER
        color_arr = []
        acc_color_arr = []
        sensor_label = []
        for m in SBRArr:
            if m < sbr_alert:
                color_arr.append("green")
            elif sbr_alert < m < sbr_danger:
                color_arr.append("orange")
            else:
                color_arr.append("red")
        for n in AccPeak:
            if n < acc_alert:
                acc_color_arr.append("green")
            elif acc_alert < n < acc_danger:
                acc_color_arr.append("orange")
            else:
                acc_color_arr.append("red")
        for k in sensor_arr:
            sensor_label.append("Sensor" + str(k + 1))

        sensor_order = np.arange(len(sensor_arr))
        ax_41, ax_42, ax_43, ax_44 = self.figure.get_axes()
        ax_42.clear()
        ax_42.set_visible(True)
        ax_42.yaxis.set_major_formatter(FormatStrFormatter('%0.1f'))

        width = 0.4
        ax_42.bar(sensor_order, SBRArr, color=color_arr, width=width)
        ax_42.bar(sensor_order + width, AccPeak, color=acc_color_arr, width=width)
        margin = (1 - width) + width / 2
        ax_42.set_xlim(-margin, len(SBRArr) - 1 + margin)

        ax_42.set_ylabel(_('Sideband ratio/ Acc-Peak Gearbox'))
        ax_42.set_xticks(sensor_order, sensor_label)
        for index, value in enumerate(SBRArr):
            ax_42.text(index - width / 4, value, "SBR")
        for index, value in enumerate(AccPeak):
            ax_42.text(index + 3 * width / 4, value, "ACC")
        self.draw()

    def plot_polar(self):
        xs = [0, 3.14]
        org = [2.6, 6.5, 1.9]
        trial = org[1:3]
        vt = np.sqrt((org[1] ** 2 + org[2] ** 2 - 2 * (org[0] ** 2)) / 2)
        amp = [vt, vt]
        theta = np.arccos((org[1] ** 2 - org[2] ** 2) / (4 * vt * org[0]))
        mcom = org[0] * 10 / vt
        ax_51 = self.figure.get_axes()
        ax_51.clear()
        for x1, y1 in zip(xs, amp):
            plt.polar(x1, y1, "*")
            plt.text(x1, y1, '(%0.2f, %0.1f)' % (x1, y1))

        plt.polar(theta, org[0], "*")
        plt.text(theta, org[0], '(%0.2f, %0.1f)' % (theta, org[0]))

        plt.polar(theta + np.pi, org[0], "*")
        plt.text(theta + np.pi, org[0], '(comp mass %0.2f, %0.1f, %0.1f)' % (theta + np.pi, org[0], mcom))
        plt.plot([0, theta + np.pi], [0, org[0]], '-y')
        plt.plot([0, 0], [0, vt], '-g')
        plt.plot([0, np.pi], [0, vt], '-b')
        plt.plot([0, theta], [0, org[0]], '-r')
        self.draw()

    def plot_origin(self, phase, amplitude, flag):
        # phase=0
        # amplitude=20
        color = ['-g', '-r', '-m', '-b', 'k']
        ax_51, = self.figure.get_axes()
        # ax_51.clear()
        if flag == 0:
            ax_51.plot([0, phase], [0, amplitude], color[flag])
            ax_51.text(phase, amplitude, '(O/ %0.2f; %0.2f)' % (phase * 180 / 3.14, amplitude), color='green')
        elif flag == 1:
            ax_51.plot([0, phase], [0, amplitude], color[flag])
            ax_51.text(phase, amplitude, '(T1/ %0.2f; %0.2f)' % (phase * 180 / 3.14, amplitude), color='red')
        elif flag == 2:
            ax_51.plot([0, phase], [0, amplitude], color[flag])
            ax_51.text(phase, amplitude, '(T2/ %0.2f; %0.2f)' % (phase * 180 / 3.14, amplitude), color='magenta')
        elif flag == 3:
            ax_51.plot([0, phase], [0, amplitude], color[flag])
            ax_51.text(phase, amplitude, '(Comp/%0.2f; %0.2f)' % (phase * 180 / 3.14, amplitude), color='blue')
            ax_51.set_title(_('Dynamic balancing') + '\n' + _("Compensation mass = ") + f'{str(amplitude)[:5]}g' + _(
                'at angle =') + f'{str(phase * 180 / 3.14)[:5]}')
        elif flag == 4:
            ax_51.plot([0, phase], [0, amplitude], color[flag])
            ax_51.text(phase, amplitude, '(TM1/%0.2f; %0.2f)' % (phase * 180 / 3.14, amplitude), color='red')
        elif flag == 5:
            ax_51.plot([0, phase], [0, amplitude], color[4])
            ax_51.text(phase, amplitude, '(TM2/%0.2f; %0.2f)' % (phase * 180 / 3.14, amplitude), color='red')
        self.draw()

    def phase_array_plotter(self, phase, amplitude):
        if len(phase) > 0:
            color = ['g', 'r', 'm', 'b', 'k']
            header = ['O', 'T1', 'T2', 'Comp', 'TM1', 'TM2']
            ax_51, = self.figure.get_axes()
            ax_51.clear()
            for i in range(len(amplitude)):
                ax_51.plot([0, phase[i]], [0, amplitude[i]], color[i])
                ax_51.text(phase[i], amplitude[i],
                           '(%s/ %0.2f; %0.2f)' % (header[i], phase[i] * 180 / 3.14, amplitude[i]), color=color[i])
            self.draw()
        else:
            pass

    def plot_balancing(self, struct_balancing, flag):
        if flag == 3:
            color = ['b', 'm', 'k', 'r', 'y', 'g']
            header = ['OL', 'OR', 'T1L', 'T1R', 'T2L', 'T2R', 'TR1L', 'TR1R', 'TR2L', 'TR2R']
            ax_51, ax_61 = self.figure.get_axes()
            ax_51.cla()
            ax_61.cla()
            ax_51.set_title(_('1st plane'))
            ax_61.set_title(_('2nd plane'))
            for i in range(len(struct_balancing["run"])):
                ax_51.plot([0, struct_balancing["run"][i]["phase1"]], [0, struct_balancing["run"][i]["amplitude1"]],
                           color[i])
                ax_51.text(struct_balancing["run"][i]["phase1"], struct_balancing["run"][i]["amplitude1"],
                           '(%s/ %0.1f°; %0.2f)' % (header[i], \
                                                    struct_balancing["run"][i]["phase1"] * 180 / 3.14,
                                                    struct_balancing["run"][i]["amplitude1"]), color=color[i])

                ax_61.plot([0, struct_balancing["run"][i]["phase2"]], [0, struct_balancing["run"][i]["amplitude2"]],
                           color[i])
                ax_61.text(struct_balancing["run"][i]["phase2"], struct_balancing["run"][i]["amplitude2"],
                           '(%s/ %0.1f°; %0.2f)' % (header[i], \
                                                    struct_balancing["run"][i]["phase2"] * 180 / 3.14,
                                                    struct_balancing["run"][i]["amplitude2"]), color=color[i])
            self.draw()
            _amplitude = []
            _phase = []
            if len(struct_balancing["run"]) > 2:
                for i in range(3):
                    _amplitude.append(struct_balancing["run"][i]["amplitude1"])
                    _amplitude.append(struct_balancing["run"][i]["amplitude2"])
                    _phase.append(struct_balancing["run"][i]["phase1"])
                    _phase.append(struct_balancing["run"][i]["phase2"])
                _trial_mass1 = [struct_balancing["trial_mass1"], struct_balancing["angle1"] * np.pi / 180]
                _trial_mass2 = [struct_balancing["trial_mass2"], struct_balancing["angle2"] * np.pi / 180]
                [h11, h12, h21, h22, cw1_w, cw1_a, cw2_w, cw2_a] = two_planes_ICs(_phase, _amplitude, _trial_mass1,
                                                                                  _trial_mass2)
                if len(struct_balancing["run"]) == 3:
                    return [cw1_w, cw1_a * 180 / np.pi, cw2_w, cw2_a * 180 / np.pi, "Corr1"]
                elif len(struct_balancing["run"]) == 4:
                    PL1Trim1 = struct_balancing["run"][3]["amplitude1"] * (
                                np.cos(struct_balancing["run"][3]["phase1"]) + np.sin(
                            struct_balancing["run"][3]["phase1"]) * 1j)
                    PL2Trim1 = struct_balancing["run"][3]["amplitude2"] * (
                                np.cos(struct_balancing["run"][3]["phase2"]) + np.sin(
                            struct_balancing["run"][3]["phase2"]) * 1j)
                    CW1 = (h12 * PL2Trim1 - h22 * PL1Trim1) / (h11 * h22 - h21 * h12)
                    CW2 = (h21 * PL1Trim1 - h11 * PL2Trim1) / (h11 * h22 - h21 * h12)
                    CW1_weight = np.abs(CW1)
                    CW1_angle = (np.angle(CW1) % (2 * np.pi)) * 180 / np.pi
                    CW2_weight = np.abs(CW2)
                    CW2_angle = (np.angle(CW2) % (2 * np.pi)) * 180 / np.pi
                    return [CW1_weight, CW1_angle, CW2_weight, CW2_angle, "Trim1"]
                elif len(struct_balancing["run"]) == 5:
                    PL1Trim1 = struct_balancing["run"][4]["amplitude1"] * (
                                np.cos(struct_balancing["run"][4]["phase1"]) + np.sin(
                            struct_balancing["run"][4]["phase1"]) * 1j)
                    PL2Trim1 = struct_balancing["run"][4]["amplitude1"] * (
                                np.cos(struct_balancing["run"][4]["phase1"]) + np.sin(
                            struct_balancing["run"][4]["phase1"]) * 1j)
                    CW1 = (h12 * PL2Trim1 - h22 * PL1Trim1) / (h11 * h22 - h21 * h12)
                    CW2 = (h21 * PL1Trim1 - h11 * PL2Trim1) / (h11 * h22 - h21 * h12)
                    CW1_weight = np.abs(CW1)
                    CW1_angle = (np.angle(CW1) % (2 * np.pi)) * 180 / np.pi
                    CW2_weight = np.abs(CW2)
                    CW2_angle = (np.angle(CW2) % (2 * np.pi)) * 180 / np.pi
                    return [CW1_weight, CW1_angle, CW2_weight, CW2_angle, "Trim2"]
                else:
                    return [-1, -1]
            else:
                return [-1, -1]
        if flag == 2:
            color = ['b', 'b', 'm', 'm', 'k', 'k', 'r', 'r', 'y', 'y']
            header = ['OL', 'OR', 'T1L', 'T1R', 'T2L', 'T2R', 'TR1L', 'TR1R', 'TR2L', 'TR2R']
            ax_51, ax_61 = self.figure.get_axes()
            ax_51.cla()
            ax_61.cla()
            ax_51.set_title(_('1st plane'))
            ax_61.set_title(_('2nd plane'))
            # ax_51.set_yticklabels([])
            # ax_61.cla()
            # ax_61.grid(False)
            # ax_61.set_yticklabels([])
            for i in range(len(struct_balancing["run"])):
                if i % 2 == 0:

                    # ax_51.grid(False)
                    ax_51.plot([0, struct_balancing["run"][i]["phase1"]], [0, struct_balancing["run"][i]["amplitude1"]],
                               color[i])
                    ax_51.text(struct_balancing["run"][i]["phase1"], struct_balancing["run"][i]["amplitude1"],
                               '(%s/ %0.1f°; %0.2f)' % (header[i], \
                                                        struct_balancing["run"][i]["phase1"] * 180 / 3.14,
                                                        struct_balancing["run"][i]["amplitude1"]), color=color[i])
                else:

                    # ax_61.grid(False)
                    ax_61.plot([0, struct_balancing["run"][i]["phase1"]], [0, struct_balancing["run"][i]["amplitude1"]],
                               color[i])
                    ax_61.text(struct_balancing["run"][i]["phase1"], struct_balancing["run"][i]["amplitude1"],
                               '(%s/ %0.1f°; %0.2f)' % (header[i], \
                                                        struct_balancing["run"][i]["phase1"] * 180 / 3.14,
                                                        struct_balancing["run"][i]["amplitude1"]), color=color[i])
            self.draw()
            _amplitude = []
            _phase = []
            if len(struct_balancing["run"]) > 5:
                for i in range(6):
                    _amplitude.append(struct_balancing["run"][i]["amplitude1"])
                    _phase.append(struct_balancing["run"][i]["phase1"])
                _trial_mass1 = [struct_balancing["trial_mass1"], struct_balancing["angle1"] * np.pi / 180]
                _trial_mass2 = [struct_balancing["trial_mass2"], struct_balancing["angle2"] * np.pi / 180]
                [h11, h12, h21, h22, cw1_w, cw1_a, cw2_w, cw2_a] = two_planes_ICs(_phase, _amplitude, _trial_mass1,
                                                                                  _trial_mass2)
                if len(struct_balancing["run"]) == 6:
                    return [cw1_w, cw1_a * 180 / np.pi, cw2_w, cw2_a * 180 / np.pi, "Corr1"]
                elif len(struct_balancing["run"]) == 8:
                    PL1Trim1 = struct_balancing["run"][6]["amplitude1"] * (
                                np.cos(struct_balancing["run"][6]["phase1"]) + np.sin(
                            struct_balancing["run"][6]["phase1"]) * 1j)
                    PL2Trim1 = struct_balancing["run"][7]["amplitude1"] * (
                                np.cos(struct_balancing["run"][7]["phase1"]) + np.sin(
                            struct_balancing["run"][7]["phase1"]) * 1j)
                    CW1 = (h12 * PL2Trim1 - h22 * PL1Trim1) / (h11 * h22 - h21 * h12)
                    CW2 = (h21 * PL1Trim1 - h11 * PL2Trim1) / (h11 * h22 - h21 * h12)
                    CW1_weight = np.abs(CW1)
                    CW1_angle = (np.angle(CW1) % (2 * np.pi)) * 180 / np.pi
                    CW2_weight = np.abs(CW2)
                    CW2_angle = (np.angle(CW2) % (2 * np.pi)) * 180 / np.pi
                    return [CW1_weight, CW1_angle, CW2_weight, CW2_angle, "Trim1"]
                elif len(struct_balancing["run"]) == 10:
                    PL1Trim1 = struct_balancing["run"][8]["amplitude1"] * (
                                np.cos(struct_balancing["run"][8]["phase1"]) + np.sin(
                            struct_balancing["run"][8]["phase1"]) * 1j)
                    PL2Trim1 = struct_balancing["run"][9]["amplitude1"] * (
                                np.cos(struct_balancing["run"][9]["phase1"]) + np.sin(
                            struct_balancing["run"][9]["phase1"]) * 1j)
                    CW1 = (h12 * PL2Trim1 - h22 * PL1Trim1) / (h11 * h22 - h21 * h12)
                    CW2 = (h21 * PL1Trim1 - h11 * PL2Trim1) / (h11 * h22 - h21 * h12)
                    CW1_weight = np.abs(CW1)
                    CW1_angle = (np.angle(CW1) % (2 * np.pi)) * 180 / np.pi
                    CW2_weight = np.abs(CW2)
                    CW2_angle = (np.angle(CW2) % (2 * np.pi)) * 180 / np.pi
                    return [CW1_weight, CW1_angle, CW2_weight, CW2_angle, "Trim2"]
                else:
                    return [-1, -1]
            else:
                return [-1, -1]
        elif flag == 1:
            color = ['g', 'r', 'm', 'b', 'o']
            header = ['O', 'O+T', 'TR1', 'TR2']
            ax_51, ax_52 = self.figure.get_axes()
            ax_51.cla()
            ax_51.set_title(_('1st plane'))
            # ax_51.grid(False)
            ax_51.set_yticklabels([])
            for i in range(len(struct_balancing["run"])):
                ax_51.plot([0, struct_balancing["run"][i]["phase"]], [0, struct_balancing["run"][i]["amplitude"]],
                           color[i])
                ax_51.text(struct_balancing["run"][i]["phase"], struct_balancing["run"][i]["amplitude"],
                           '(%s/ %0.1f°; %0.2f)' % (header[i], \
                                                    struct_balancing["run"][i]["phase"] * 180 / 3.14,
                                                    struct_balancing["run"][i]["amplitude"]), color=color[i])
            self.draw()

            if len(struct_balancing["run"]) > 1:
                [T_amp, T_phase, corr_weight, corr_angle, inf_coe_weight, inf_coe_angle] = calculate_corection(
                    struct_balancing["run"][0]["phase"], \
                    struct_balancing["run"][0]["amplitude"], struct_balancing["run"][1]["phase"],
                    struct_balancing["run"][1]["amplitude"], \
                    struct_balancing["angle1"] * np.pi / 180, struct_balancing["trial_mass1"])
                # ax_51.plot([0, T_phase], [0, T_amp], color[4])
                # ax_51.text(T_phase, T_amp, '(%s/ %0.2f; %0.2f)' % (header[2], T_phase * 180 / 3.14, T_amp), color=color[4])
                # self.draw()
                if len(struct_balancing["run"]) == 2:
                    return [corr_weight, (corr_angle % 2 * np.pi) * 180 / np.pi, "Corr1"]
                elif len(struct_balancing["run"]) == 3:
                    trim_corr_weight = struct_balancing["run"][2]["amplitude"] / inf_coe_weight
                    trim_corr_angle = ((struct_balancing["run"][2]["phase"] + np.pi - inf_coe_angle) % (
                                2 * np.pi)) * 180 / np.pi
                    return [trim_corr_weight, trim_corr_angle, "Trim1"]
                elif len(struct_balancing["run"]) == 4:
                    trim_corr_weight = struct_balancing["run"][3]["amplitude"] / inf_coe_weight
                    trim_corr_angle = ((struct_balancing["run"][3]["phase"] + np.pi - inf_coe_angle) % (
                                2 * np.pi)) * 180 / np.pi
                    return [trim_corr_weight, trim_corr_angle, "Trim2"]
                else:
                    return [-1, -1]
            else:
                return [-1, -1, ]

    def balancing_array_plotter(self, phase_left, phase_right, amplitude_left, amplitude_right, trial_mass1,
                                trial_mass2):
        two_plane_amp1_origin = amplitude_left[0]
        two_plane_pha1_origin = phase_left[0]
        two_plane_amp1_trial_1 = amplitude_left[1]
        two_plane_pha1_trial_1 = phase_left[1]
        two_plane_amp1_trial_2 = amplitude_left[2]
        two_plane_pha1_trial_2 = phase_left[2]
        two_plane_amp2_origin = amplitude_right[0]
        two_plane_pha2_origin = phase_right[0]
        two_plane_amp2_trial_1 = amplitude_right[1]
        two_plane_pha2_trial_1 = phase_right[1]
        two_plane_amp2_trial_2 = amplitude_right[2]
        two_plane_pha2_trial_2 = phase_right[2]
        v_10 = two_plane_amp1_origin * np.cos(two_plane_pha1_origin) + two_plane_amp1_origin * np.sin(
            two_plane_pha1_origin) * 1j
        v_11 = two_plane_amp1_trial_1 * np.cos(two_plane_pha1_trial_1) + two_plane_amp1_trial_1 * np.sin(
            two_plane_pha1_trial_1) * 1j
        v_12 = two_plane_amp1_trial_2 * np.cos(two_plane_pha1_trial_2) + two_plane_amp1_trial_2 * np.sin(
            two_plane_pha1_trial_2) * 1j
        v_20 = two_plane_amp2_origin * np.cos(two_plane_pha2_origin) + two_plane_amp2_origin * np.sin(
            two_plane_pha2_origin) * 1j
        v_21 = two_plane_amp2_trial_1 * np.cos(two_plane_pha2_trial_1) + two_plane_amp2_trial_1 * np.sin(
            two_plane_pha2_trial_1) * 1j
        v_22 = two_plane_amp2_trial_2 * np.cos(two_plane_pha2_trial_2) + two_plane_amp2_trial_2 * np.sin(
            two_plane_pha2_trial_2) * 1j
        v11_v10 = v_11 - v_10
        v12_v10 = v_12 - v_10
        v21_v20 = v_21 - v_20
        v22_v20 = v_22 - v_20
        q2 = (v_20 * v11_v10 - v_10 * v21_v20) / (v21_v20 * v12_v10 - v22_v20 * v11_v10)
        q1 = (-v_10 - q2 * v12_v10) / v11_v10
        q1_amp = np.abs(q1)
        q2_amp = np.abs(q2)
        mass1 = q1_amp * trial_mass1
        mass2 = q2_amp * trial_mass2
        q1_pha = cmath.phase(q1)
        q2_pha = cmath.phase(q2)
        v11_v10_amp = np.abs(v11_v10)
        v22_v20_amp = np.abs(v22_v20)
        v11_v10_pha = cmath.phase(v11_v10)
        v22_v20_pha = cmath.phase(v22_v20)

    def plot_trial1(self, phase, amplitude):
        # phase = np.pi/2
        # amplitude = 20
        ax_51, = self.figure.get_axes()
        ax_51.plot([0, phase], [0, amplitude], '-r')
        ax_51.text(phase, amplitude, '(%0.1f°; %0.2f)' % (phase * 180 / 3.14, amplitude), color='red')
        self.draw()

    def plot_rebalance(self, phi0, a0, phi1, a1, trial_mass):
        ax_51, = self.figure.get_axes()
        z0 = a0 * np.cos(phi0) + (a0 * np.sin(phi0)) * 1j
        z1 = a1 * np.cos(phi1) + (a1 * np.sin(phi1)) * 1j
        azt = z1 - z0
        amp = np.abs(azt)
        aaa = a0 * trial_mass / amp
        phase = cmath.phase(azt)
        comp_phase = np.pi + phi0
        ax_51.plot([0, phase], [0, amp], '-y')
        ax_51.text(phase, amp, '(Trial/%0.1f°; %0.2f)' % (phase * 180 / 3.14, amp))
        ax_51.plot([0, comp_phase], [0, a0], '-b')
        ax_51.text(comp_phase, aaa, '(Comp/%0.1f°; %0.2f)' % ((comp_phase) * 180 / 3.14, aaa))
        ax_51.set_title(
            f'Dynamic balancing for one plane\nCompensation mass = {str(aaa)[:5]}g and make angle = {str(((comp_phase - phase) * 180 / 3.14) % 360)[:5]} degrees with trial mass')
        self.draw()

    def clear_polar(self):
        ax_51, ax_52 = self.figure.get_axes()
        ax_51.clear()
        ax_52.clear()
        ax_51.set_title(_('1st plane'))
        ax_52.set_title(_('2nd plane'))
        self.draw()

    def clear_polar2(self):
        ax_61, = self.figure.get_axes()
        ax_61.clear()
        ax_61.set_title(_('Dynamic balancing 2nd plane'))
        self.draw()

    def plot_spectrogram(self, f, t, Zxx, date):
        t *= 1000
        self.figure.set_size_inches(9.2, 5.2)
        axes_arr = self.figure.get_axes()
        cc = len(axes_arr)
        while cc > 0:
            self.figure.delaxes(axes_arr[cc - 1])
            cc -= 1
        self.figure.add_subplot(1, 1, 1)
        self.figure.subplots_adjust(left=0.1, right=0.95, top=0.92, bottom=0.15)
        self.figure.set_visible(True)
        ax_81, = self.figure.get_axes()
        ax_81.clear()
        ax_81.pcolormesh(t, f, np.abs(Zxx))
        ax_81.set_title(_('STFT Magnitude-') + f' {date}')
        ax_81.set_ylabel(_('Frequency [Hz]'))
        ax_81.set_xlabel(_('Time [ms]'))
        self.draw()

    def clear_axes(self, order_axes):
        arr_axes = self.figure.get_axes()
        arr_axes[order_axes].clear()
        self.draw()

    def plot_grid(self, flag: bool, grid_val: int):
        ax1, ax2, ax3 = self.figure.get_axes()
        [left, right] = ax1.get_xlim()

        if flag == 1:
            arr_grid = np.arange(0, right, grid_val)
            ax1.set_xticks(arr_grid, minor=True)
            ax1.xaxis.grid(True, which='minor', color="lightgray")
            ax2.set_xticks(arr_grid, minor=True)
            ax2.xaxis.grid(True, which='minor', color="lightgray")
            ax3.set_xticks(arr_grid, minor=True)
            ax3.xaxis.grid(True, which='minor', color="lightgray")
            self.draw()
        else:
            ax1.xaxis.grid(False, which='minor')
            ax2.xaxis.grid(False, which='minor')
            ax3.xaxis.grid(False, which='minor')
            self.draw()

    def plot_grid_specific(self, grid_val: float, title, set_title_flag):
        hfont = {'fontsize': 10}
        axes_arr = self.figure.get_axes()
        [left, right] = axes_arr[0].get_xlim()
        if grid_val > right:
            grid_val = right
        arr_grid = [grid_val]
        if set_title_flag:
            for i in range(len(axes_arr)):
                axes_arr[i].set_xticks(arr_grid, minor=True)
                axes_arr[i].xaxis.grid(True, which='minor', color="r")
                axes_arr[i].set_visible(True)
            axes_arr[0].set_title(title,  color="red", **hfont)
        else:
            for i in range(2):
                axes_arr[i].set_xticks(arr_grid, minor=True)
                axes_arr[i].xaxis.grid(True, which='minor', color="r")
                axes_arr[i].set_visible(True)
        self.draw()

    def plot_grid_only(self, grid_val:float):
        axes_arr = self.figure.get_axes()
        [left, right]=axes_arr[0].get_xlim()
        if grid_val>right:
            grid_val=right
        arr_grid=[grid_val]
        for i in range(len(axes_arr)):
            axes_arr[i].set_xticks(arr_grid, minor=True)
            axes_arr[i].xaxis.grid(True, which='minor', color="r")
            axes_arr[i].set_visible(True)
        self.draw()
        
    def plot_impact_test(self, canal, sample_rate, window_len, damping_factor):
        max_freq = int(sample_rate / 2.56)
        [max_pos, max_val] = find_max(canal)
        N = len(canal)
        tau = -(window_len - 1) / np.log(0.1 / damping_factor)

        w = max_val * signal.exponential(window_len, 0, tau, False)

        # ----------------- Plotting ---------------
        X1 = np.linspace(0, int((N / sample_rate) * 1000), N)  # X axis, 5000 sps, 1/5 ms.
        ax_11, ax_12, ax_13 = self.figure.get_axes()

        ax_13.clear()
        ax_13.set_visible(True)
        ax_13.yaxis.set_major_formatter(FormatStrFormatter('%0.2f'))
        ax_13.plot(X1, canal, color='blue', linewidth=0.4)
        ax_13.plot(X1[:window_len], w, color='red', linewidth=0.7)
        ax_13.set_xlabel("ms")
        ax_13.set_ylabel('g')
        ax_13.grid()  # Shows grid.
        ax_13.set_xlim(xmin=0, xmax=(3000 * window_len) / sample_rate)

        T = 1.0 / sample_rate
        y = canal[:window_len]
        yf = fftpack.fft(y * w) * (4 / N)
        yf1 = np.abs(yf[:(int(window_len // 2))])
        yfphase = np.angle(yf[:(int(window_len // 2))]) * 180 / np.pi
        xf = fftpack.fftfreq(window_len, T)[:int(window_len // 2)]

        ax_11.clear()
        ax_11.set_visible(True)
        ax_11.yaxis.set_major_formatter(FormatStrFormatter('%0.2f'))
        ax_11.plot(xf, yf1, color='blue', linewidth=0.5)
        ax_11.grid()
        ax_11.set_xlabel("Hz")
        ax_11.set_ylabel(_('Amplitude-g'))
        ax_11.set_xlim(xmax=max_freq)

        ax_12.clear()
        ax_12.set_visible(True)
        ax_12.yaxis.set_major_formatter(FormatStrFormatter('%0.0f'))
        ax_12.plot(xf, yfphase, color='blue', linewidth=0.5)
        ax_12.grid()
        ax_12.set_yticks([-180, -90, 0, 90, 180])
        ax_12.set_xlabel("Hz")
        ax_12.set_ylabel(_('Phase-degree'))
        ax_12.set_xlim(xmax=max_freq)
        self.draw()
        return [xf, yf1, yfphase]

    def plotfrf(self, acc_data, hamer_data, sample_rate, window_len, damping_factor):
        max_freq = int(sample_rate / 2.56)
        [max_pos, max_val] = find_max(acc_data)
        N = len(acc_data)
        tau = -(window_len - 1) / np.log(0.1 / damping_factor)
        w = max_val * signal.exponential(window_len, 0, tau, False)

        # ----------------- Plotting ---------------
        X1 = np.linspace(0, int((N / sample_rate) * 1000), N)  # X axis, 5000 sps, 1/5 ms.
        ax_11, ax_12, ax_13 = self.figure.get_axes()
        ax_13.clear()
        ax_13.set_visible(True)
        ax_13.yaxis.set_major_formatter(FormatStrFormatter('%0.2f'))
        ax_13.plot(X1, acc_data, color='blue', linewidth=0.4)
        ax_13.plot(X1, hamer_data, color='black', linewidth=0.4)
        ax_13.plot(X1[:window_len], w, color='red', linewidth=0.7)
        ax_13.set_xlabel("ms")
        ax_13.set_ylabel('g')
        ax_13.grid()  # Shows grid.
        ax_13.set_xlim(xmin=0, xmax=(3000 * window_len) / sample_rate)

        T = 1.0 / sample_rate
        y = acc_data[:window_len]
        yf = fftpack.fft(y * w) * (4 / N)
        yf1 = np.abs(yf[:(int(window_len // 2))])
        # yhamer = hamer_data[:window_len]
        # yfhamer = fftpack.fft(yhamer * w) * (4 / N)
        # yfhamer1 = np.abs(yf[:(int(window_len // 2))])
        # frf_arr=yf/yfhamer
        # frf_abs=np.abs(frf_arr[:(int(window_len // 2))])
        yfphase = np.angle(yf[:(int(window_len // 2))]) * 180 / np.pi
        xf = fftpack.fftfreq(window_len, T)[:int(window_len // 2)]

        ax_11.clear()
        ax_11.set_visible(True)
        ax_11.yaxis.set_major_formatter(FormatStrFormatter('%0.2f'))
        ax_11.plot(xf, yf1, color='blue', linewidth=0.5)
        # ax_11.plot(xf, np.abs(yfhamer[:(int(window_len // 2))]), color='black', linewidth=0.5)
        ax_11.grid()
        ax_11.set_xlabel("Hz")
        ax_11.set_ylabel(_('Amplitude-g'))
        ax_11.set_xlim(xmax=max_freq)

        ax_12.clear()
        ax_12.set_visible(True)
        ax_12.yaxis.set_major_formatter(FormatStrFormatter('%0.0f'))
        ax_12.plot(xf, yfphase, color='blue', linewidth=0.5)
        ax_12.grid()
        ax_12.set_yticks([-180, -90, 0, 90, 180])
        ax_12.set_xlabel("Hz")
        ax_12.set_ylabel(_('Phase-degree'))
        ax_12.set_xlim(xmax=max_freq)
        self.draw()

    def plot_average_resonance(self, xf, amplitude, phase):
        ax_11, ax_12, ax_13 = self.figure.get_axes()
        ax_13.set_visible(True)
        ax_11.clear()
        ax_11.set_visible(True)
        ax_11.yaxis.set_major_formatter(FormatStrFormatter('%0.2f'))
        ax_11.plot(xf, amplitude, color='blue', linewidth=0.4)
        ax_11.set_xlabel("hz")
        ax_11.set_ylabel('Amplitude-g')
        ax_11.grid()  # Shows grid.

        ax_12.clear()
        ax_12.set_visible(True)
        ax_12.yaxis.set_major_formatter(FormatStrFormatter('%0.0f'))
        ax_12.plot(xf, phase, color='blue', linewidth=0.4)
        ax_12.set_xlabel("hz")
        ax_12.set_ylabel(_('Phase-degree'))
        ax_12.grid()  # Shows grid.
        self.draw()

    def plot_image(self, file_name, link):
        self.figure.set_size_inches(9.2, 5.2)
        qrPhoto = plt.imread(save_path+file_name)
        axes_arr = self.figure.get_axes()
        cc=len(axes_arr)
        while cc>0:
            self.figure.delaxes(axes_arr[cc-1])
            cc-=1

        self.figure.add_subplot(1,1,1)
        self.figure.subplots_adjust(left=0.1, right=0.95, top=0.95, bottom=0.15)
        ax_11, = self.figure.get_axes()
        ax_11.clear()
        ax_11.set_title(link)
        ax_11.imshow(qrPhoto)
        ax_11.axis('off')
        ax_11.set_visible(True)
        self.draw()

def calculate_corection(phi0, a0, phi1, a1, trial_mass_angle, trial_mass):
    z0 = a0 * np.cos(phi0) + (a0 * np.sin(phi0)) * 1j
    z1 = a1 * np.cos(phi1) + (a1 * np.sin(phi1)) * 1j
    tw = trial_mass * np.cos(trial_mass_angle) + (trial_mass * np.sin(trial_mass_angle)) * 1j
    Tr = z1 - z0
    Hh = Tr / tw
    amp_T = np.abs(Tr)
    phase_T = np.angle(Tr)
    amp_H = np.abs(Hh)
    phase_H = np.angle(Hh)
    influent_coef_angle = phase_H
    influent_coef_weight = amp_H
    correction_weight = a0 / influent_coef_weight
    correction_angle = np.pi + phi0 - influent_coef_angle
    return [
        amp_T,
        phase_T,
        correction_weight,
        correction_angle,
        influent_coef_weight,
        influent_coef_angle,
    ]


def two_planes_ICs(phase, amplitude, trial_mass1, trial_mass2):
    O1 = amplitude[0] * np.cos(phase[0]) + amplitude[0] * np.sin(phase[0]) * 1j
    O2 = amplitude[1] * np.cos(phase[1]) + amplitude[1] * np.sin(phase[1]) * 1j
    OT11 = amplitude[2] * np.cos(phase[2]) + amplitude[2] * np.sin(phase[2]) * 1j
    OT21 = amplitude[3] * np.cos(phase[3]) + amplitude[3] * np.sin(phase[3]) * 1j
    OT12 = amplitude[4] * np.cos(phase[4]) + amplitude[4] * np.sin(phase[4]) * 1j
    OT22 = amplitude[5] * np.cos(phase[5]) + amplitude[5] * np.sin(phase[5]) * 1j
    TW1 = trial_mass1[0] * np.cos(trial_mass1[1]) + trial_mass1[0] * np.sin(trial_mass1[1]) * 1j
    TW2 = trial_mass2[0] * np.cos(trial_mass2[1]) + trial_mass2[0] * np.sin(trial_mass2[1]) * 1j
    H11 = (OT11 - O1) / TW1
    H12 = (OT12 - O1) / TW2
    H21 = (OT21 - O2) / TW1
    H22 = (OT22 - O2) / TW2
    # H=[[H11, H12],[H21, H22]]
    CW1 = (H12 * O2 - H22 * O1) / (H11 * H22 - H21 * H12)
    CW2 = (H21 * O1 - H11 * O2) / (H11 * H22 - H21 * H12)
    CW1_weight = np.abs(CW1)
    CW1_angle = (np.angle(CW1) % (2 * np.pi))
    CW2_weight = np.abs(CW2)
    CW2_angle = (np.angle(CW2) % (2 * np.pi))
    return [H11, H12, H21, H22, CW1_weight, CW1_angle, CW2_weight, CW2_angle]

