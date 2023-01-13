import tkinter as Tk
import sv_ttk
from tkinter import ttk
import matplotlib
matplotlib.use('TKAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os
from i18n import _
from keyboard.keyboard import KeyBoard
from ui.creatFigure.creatFigure import creatFig
from image.image import ImageAdrr
from datetime import datetime
import threading
from threading import Lock
import time
import numpy as np
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from main import Application

current_directory = os.getcwd()
parent_directory = os.path.dirname(os.path.dirname(current_directory))
import ctypes
from numpy.ctypeslib import ndpointer
ad7609 = ctypes.CDLL(f'{current_directory}/ad7609BTZ.so')
from digitalFilter.digitalFilter import filter_data
from Calculation.calculate import *
import PlotData.PlotData as Pd

window_len = 2001
damping_factor = 10
resonance_data=[]
amplitude_resonance_arr=[]
phase_resonance_arr=[]
amplitude_add_arr=[]
phase_add_arr=[]
x_arr=[]

def testVal(inStr, acttyp):
    if acttyp == '1':  # insert
        if not inStr.isdigit():
            return False
    return True

class Resonance(Tk.Frame):
    def __init__(self, parent: "Application"):
        # sv_ttk.set_theme("light")
        self.parent = parent
        now = datetime.now()
        self.current_time = now.strftime("%H:%M")
        imageAddress = ImageAdrr()
        self.homePhoto = imageAddress.homePhoto
        self.low_bat = imageAddress.low_bat
        self.half_bat = imageAddress.half_bat
        self.full_bat = imageAddress.full_bat
        self.arrowPhoto = imageAddress.arrowPhoto
        
        self.btstyle = ttk.Style()
        self.btstyle.configure('normal.TButton', font=('Chakra Petch', 13), borderwidth=5, justify=Tk.CENTER)
        self.btstyle.map('normal.TButton', foreground=[('active', 'blue')])
        self.btstyle.configure('custom.Accent.TButton', font=('Chakra Petch', 10), bordercolor='black', borderwidth=4,
                               justify=Tk.CENTER)
        self.btstyle.configure('bat.TLabel', font=('Chakra Petch', 13))
        self.btstyle.configure('normal.TLabel', font=('Chakra Petch', 13), background='white')
        self.btstyle.configure('red.TLabel', font=('Chakra Petch', 13), background='white', foreground='red')

        self.mainFrame = Tk.Frame(self.parent, bd=1, bg='white', width=1024, height=600)
        self.mainFrame.pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)
        self.mainFrame.pack_propagate(0)

        self.featureFrame = Tk.Frame(self.mainFrame, bd=1, bg='white', width=1024, height=80)
        self.featureFrame.pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)
        self.featureFrame.pack_propagate(0)

        self.batFrame = Tk.Frame(self.featureFrame, bd=1, bg='grey95', width=117, height=35)
        self.batFrame.pack()
        self.batFrame.place(relx=0.89, rely=0.0)
        self.batFrame.pack_propagate(0)
        self.creat_setting_feature_panel()

        self.resonanceConfigFrame = ResonanceConfig(self.mainFrame, self.parent.origin_config)
        self.resonanceConfigFrame.pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)
        self.resonanceConfigFrame.pack_propagate(0)

        self.resonanceAnalysisFrame = ResonanceAnalysis(self.mainFrame, self.parent.origin_config, self.infoLabel2)
        self.resonanceAnalysisFrame.pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)
        self.resonanceAnalysisFrame.pack_propagate(0)
        self.resonanceAnalysisFrame.pack_forget()

        self.parent.bind_class('TEntry', "<FocusIn>", self.show_key_board)
        self.parent.bind_class('TCombobox', "<<ComboboxSelected>>", self.change_state)

    def show_key_board(self, event):
        self.resonanceConfigFrame.resonanceApplyButton.configure(state='normal')
        self.widget = self.get_focus_widget()
        self.keyboardFrame = KeyBoard(self.widget)
        parentName = event.widget.winfo_parent()
        self.parent1 = event.widget._nametowidget(parentName)
        self.parent1.focus()

    def get_focus_widget(self):
        widget = self.parent.focus_get()
        return widget

    def change_state(self, event):
        self.resonanceConfigFrame.resonanceApplyButton.configure(state="normal")

    def creat_setting_feature_panel(self):

        self.timeLabel = ttk.Label(self.batFrame, style='bat.TLabel', text=self.current_time)
        self.timeLabel.after(5000, self.update_time)
        self.timeLabel.place(relx=0.05, rely=0.1)

        self.batLabel = ttk.Label(self.batFrame, style='bat.TLabel', text="20%", image=self.full_bat, compound=Tk.LEFT)
        self.batLabel.image = self.full_bat
        self.batLabel.after(10000, self.update_bat)
        self.batLabel.place(relx=0.5, rely=0.1)

        self.homeBt = ttk.Button(self.featureFrame, style='normal.TButton', text="Home", image=self.homePhoto,
                                 compound=Tk.TOP,
                                 command=self.go_home)
        self.homeBt.place(relx=0.0, rely=0.018, width=100, height=72)
        self.homeBt.image = self.homePhoto

        barrie=Tk.Frame(self.featureFrame, width=3, height=72, background='grey')
        barrie.place(relx=0.11, rely=0.018)

        self.configBt = ttk.Button(self.featureFrame, style='normal.TButton', text="Config",
                                    command=self.on_config_button_clicked)
        self.configBt.place(relx=0.122, rely=0.018, width=115, height=72)

        self.arrowLabel = ttk.Label(self.featureFrame, style='normal.TLabel', image=self.arrowPhoto)
        self.arrowLabel.place(relx=0.237, rely=0.25)
        self.arrowLabel.image = self.arrowPhoto
        
        self.analysis = ttk.Button(self.featureFrame, style='normal.TButton', text="Resonance\nAnalysis",
                                   command=self.on_analysis_button_clicked)
        self.analysis.place(relx=0.265, rely=0.018, width=115, height=72)

        self.infoFrame= Tk.Frame(self.featureFrame, width=451, height=72, bg='white', bd=0)
        self.infoFrame.place(relx=0.41, rely=0.018)

        self.infoLabel1=ttk.Label(self.infoFrame, text="Information", style="red.TLabel")
        self.infoLabel1.grid(column=0, row=0, padx=0, pady=5, sticky='w')

        self.infoLabel2 = ttk.Label(self.infoFrame, text="Click the READ SENSOR and make a hit.", style="normal.TLabel")
        self.infoLabel2.grid(column=0, row=1, padx=0, pady=5, sticky='w')

    def on_analysis_button_clicked(self):
        self.resonanceConfigFrame.pack_forget()
        self.resonanceAnalysisFrame.pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)

    def on_config_button_clicked(self):
        self.resonanceConfigFrame.pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)
        self.resonanceAnalysisFrame.pack_forget()

    def update_time(self):
        now = datetime.now()
        current_time = now.strftime("%H:%M")
        self.timeLabel.configure(text=current_time)
        self.timeLabel.after(5000, self.update_time)

    def update_bat(self):
        remain_bat=90
        if remain_bat>=70:
            self.batLabel.configure(text=f"{int(remain_bat)}%", image=self.full_bat, compound=Tk.LEFT)
        elif 30<=remain_bat<70:
            self.batLabel.configure(text=f"{int(remain_bat)}%", image=self.half_bat, compound=Tk.LEFT)
        else:
            self.batLabel.configure(text=f"{int(remain_bat)}%", image=self.low_bat, compound=Tk.LEFT)
        self.batLabel.after(10000, self.update_bat)
    def go_home(self):
        self.mainFrame.destroy()
        self.parent.go_to_home_page()


class ResonanceConfig(Tk.Frame):
    def __init__(self, parent, origin_config):
        super().__init__(parent, width=1024, height=520, bg='white')
        self.style = ttk.Style()
        self.style.configure('resonance.TLabel', font=('Chakra Petch', 13), bg='white')
        self.style.configure('resonance.TLabelframe', font=('Chakra Petch', 15), bg='white', borderwidth=0)
        self.style.configure('resonance.TButton', font=('Chakra Petch', 15))
        self.resonance_analysis_setting(origin_config.resonance_config_struct)

    def resonance_analysis_setting(self, resonance_config_struct):
        self.resonanceParam0 = Tk.StringVar()
        self.resonanceParam1 = Tk.StringVar()
        self.resonanceParam2 = Tk.StringVar()
        self.resonanceParam3 = Tk.StringVar()
        self.resonanceParam4 = Tk.StringVar()
        self.resonanceParam5 = Tk.StringVar()
        self.resonanceParam6 = Tk.StringVar()
        self.resonanceParam7 = Tk.StringVar()
        self.resonanceParam8 = Tk.StringVar()
        self.resonanceParam9 = Tk.StringVar()
        self.resonanceParam10 = Tk.StringVar()
        self.resonanceParam11 = Tk.StringVar()
        ##config default value
        self.resonanceParam0.set(resonance_config_struct["Function"])
        self.resonanceParam1.set(resonance_config_struct["Sensor"])
        self.resonanceParam2.set(resonance_config_struct["Window"])
        self.resonanceParam3.set(resonance_config_struct["FilterType"])
        self.resonanceParam4.set(resonance_config_struct["FilterFrom"])
        self.resonanceParam5.set(resonance_config_struct["FilterTo"])
        self.resonanceParam6.set(resonance_config_struct["sampleRate"])
        self.resonanceParam7.set(resonance_config_struct["sampling_time"])
        self.resonanceParam8.set(resonance_config_struct["Factor"])
        self.resonanceParam9.set(resonance_config_struct["Tracking"])
        self.resonanceParam10.set(resonance_config_struct["Hport"])
        self.resonanceParam11.set(resonance_config_struct["num_of_average"])

        resonanceConfigFrame = Tk.LabelFrame(self, text=_(' '), bg="white", border=0)
        resonanceConfigFrame.pack(side=Tk.TOP, fill=Tk.BOTH)

        functionLabel = ttk.Label(resonanceConfigFrame, text=_('Function'), style="resonance.TLabel")
        functionLabel.grid(column=0, row=0, padx=10, pady=5, sticky="w")
        functionCombo = ttk.Combobox(resonanceConfigFrame, width=10, textvariable=self.resonanceParam0,
                                     state="readonly")
        functionCombo['value'] = ('Impact test', 'FRF')
        functionCombo.grid(column=1, row=0, padx=0, pady=5, sticky="e")

        sensorLabel = ttk.Label(resonanceConfigFrame, text=_('Sensor Port'), style="resonance.TLabel")
        sensorLabel.grid(column=0, row=1, padx=10, pady=5, sticky="w")
        sensorCombo = ttk.Combobox(resonanceConfigFrame, width=10, textvariable=self.resonanceParam1, state="readonly")
        sensorCombo['value'] = ('Port1', 'Port2', 'Port3')
        sensorCombo.grid(column=1, row=1, padx=0, pady=5, sticky="e")

        hamerLabel = ttk.Label(resonanceConfigFrame, text=_('Hammer Port'), style="resonance.TLabel")
        hamerLabel.grid(column=0, row=2, padx=10, pady=5, sticky="w")
        hamerCombo = ttk.Combobox(resonanceConfigFrame, width=10, textvariable=self.resonanceParam10, state="readonly")
        hamerCombo['value'] = ('Port1', 'Port2', 'Port3')
        hamerCombo.grid(column=1, row=2, padx=0, pady=5, sticky="e")

        windowLabel = ttk.Label(resonanceConfigFrame, text=_('Window Type'), style="resonance.TLabel")
        windowLabel.grid(column=0, row=3, padx=10, pady=5, sticky="w")
        windowCombo = ttk.Combobox(resonanceConfigFrame, width=10, textvariable=self.resonanceParam2, state="readonly")
        windowCombo['value'] = ('Exponential')
        windowCombo.grid(column=1, row=3, padx=0, pady=5, sticky="e")

        factorLabel = ttk.Label(resonanceConfigFrame, text=_('Window Factor'), style="resonance.TLabel")
        factorLabel.grid(column=0, row=4, padx=10, pady=5, sticky="w")

        factorCombo = ttk.Combobox(resonanceConfigFrame, width=10, textvariable=self.resonanceParam8, state="readonly")
        factorCombo['value'] = ('Length', "Damping ratio")
        factorCombo.grid(column=1, row=4, padx=0, pady=5, sticky="e")

        filterLabel = ttk.Label(resonanceConfigFrame, text=_('Filter Type'), style="resonance.TLabel")
        filterLabel.grid(column=0, row=5, padx=10, pady=5, sticky="w")
        filterCombo = ttk.Combobox(resonanceConfigFrame, width=10, textvariable=self.resonanceParam3, state="readonly")
        filterCombo['value'] = ('BANDPASS')
        filterCombo.grid(column=1, row=5, padx=0, pady=5, sticky="e")

        filterFromLabel = ttk.Label(resonanceConfigFrame, text=_("Bandpass Filter From"), style="resonance.TLabel")
        filterFromLabel.grid(column=2, row=0, padx=20, pady=5, sticky='w')
        filterFromEntry = ttk.Entry(resonanceConfigFrame, width=14, textvariable=self.resonanceParam4)
        filterFromEntry.grid(column=3, row=0, padx=0, pady=5, sticky='e')

        filterToLabel = ttk.Label(resonanceConfigFrame, text=_("Bandpass Filter To"), style="resonance.TLabel")
        filterToLabel.grid(column=2, row=1, padx=20, pady=5, sticky='w')
        filterToEntry = ttk.Entry(resonanceConfigFrame, width=14, textvariable=self.resonanceParam5)
        filterToEntry.grid(column=3, row=1, padx=0, pady=5, sticky='e')

        viewLabel = ttk.Label(resonanceConfigFrame, text=_("Sample rate"), style="resonance.TLabel")
        viewLabel.grid(column=2, row=2, padx=20, pady=5, sticky='w')
        viewEntry = ttk.Entry(resonanceConfigFrame, width=14, textvariable=self.resonanceParam6)
        viewEntry.grid(column=3, row=2, padx=0, pady=5, sticky='e')

        meshLabel = ttk.Label(resonanceConfigFrame, text=_("Sampling time"), style="resonance.TLabel")
        meshLabel.grid(column=2, row=3, padx=20, pady=5, sticky='w')
        meshEntry = ttk.Entry(resonanceConfigFrame, width=14, textvariable=self.resonanceParam7)
        meshEntry.grid(column=3, row=3, padx=0, pady=5, sticky='e')

        trackingLabel = ttk.Label(resonanceConfigFrame, text=_("Tracking resolution"), style="resonance.TLabel")
        trackingLabel.grid(column=2, row=4, padx=20, pady=5, sticky='w')
        trackingEntry = ttk.Entry(resonanceConfigFrame, width=14, textvariable=self.resonanceParam9)
        trackingEntry.grid(column=3, row=4, padx=0, pady=5, sticky='e')

        numOfAverageLabel = ttk.Label(resonanceConfigFrame, text=_("Num of Average"), style="resonance.TLabel")
        numOfAverageLabel.grid(column=2, row=5, padx=20, pady=5, sticky='w')
        numOfAverageEntry = ttk.Entry(resonanceConfigFrame, width=14, textvariable=self.resonanceParam11)
        numOfAverageEntry.grid(column=3, row=5, padx=0, pady=5, sticky='e')

        self.resonanceApplyButton = ttk.Button(resonanceConfigFrame, text=_("Apply"), style="Accent.TButton",
                                    command=lambda: self.update_resonance_struct(resonance_config_struct))
        self.resonanceApplyButton.grid(column=3, row=6, padx=0, pady=10, ipadx=36, ipady=5, sticky='w')


    def update_resonance_struct(self, resonance_config_struct):
        resonance_config_struct["Function"] = self.resonanceParam0.get()
        resonance_config_struct["Factor"] = self.resonanceParam8.get()
        resonance_config_struct["Sensor"] = self.resonanceParam1.get()
        resonance_config_struct["Hport"] = self.resonanceParam10.get()
        resonance_config_struct["Window"] = self.resonanceParam2.get()
        resonance_config_struct["FilterType"] = self.resonanceParam3.get()

        tempSamplerate = self.resonanceParam6.get()
        tempSamplingtime = self.resonanceParam7.get()
        tempFilterFrom = self.resonanceParam4.get()
        tempFilterTo = self.resonanceParam5.get()
        tempTracking = self.resonanceParam9.get()
        tempAverage = self.resonanceParam11.get()

        if int(tempSamplerate) <= 10000:
            resonance_config_struct["sampleRate"] = int(tempSamplerate)
        else:
            resonance_config_struct["sampleRate"] = 10000
        if int(tempSamplingtime) < 10:
            resonance_config_struct["sampling_time"] = int(tempSamplingtime)
        else:
            resonance_config_struct["sampling_time"] = 10
        resonance_config_struct["FilterFrom"] = int(tempFilterFrom)
        resonance_config_struct["FilterTo"] = int(tempFilterTo)
        resonance_config_struct["Tracking"] = int(tempTracking)
        resonance_config_struct["num_of_average"] = int(tempAverage)

        self.resonanceApplyButton.configure(state="disable")
class ResonanceAnalysis(Tk.Frame):
    def __init__(self, parent:"mainFrame", origin_config, infoLabel):
        super().__init__(parent, width=1024 , height=520 , bg='white')
        self.parent = parent
        self.origin_config = origin_config
        self.lock = Lock()
        ad7609.init()
        self.infoLabel = infoLabel
        self.resonance_analysis_page()
    def resonance_analysis_page(self):
        self.resonancePlotFrame = ResonancePlotCanvas(self)
        self.resonancePlotFrame.pack(side=Tk.LEFT, fill=Tk.BOTH, expand=1)
        self.resonancePlotFrame.pack_propagate(0)

        self.resonaceSideFrame = SideButtonFrame(self, self.origin_config, self.infoLabel, self.lock,
                                                 self.resonancePlotFrame.canvas1)
        self.resonaceSideFrame.pack(side=Tk.RIGHT, fill=Tk.Y, expand=1)
        self.resonaceSideFrame.pack_propagate(0)

class SideButtonFrame(Tk.Frame):
    def __init__(self, parent, origin_config, infoLabel, lock, canvas):
        super().__init__(parent, bd=1, bg='white', width=90, height=520)
        self.parent=parent
        self.origin_config=origin_config
        self.infoLabel=infoLabel
        self.lock = lock
        self.canvas=canvas
        self.style = ttk.Style()
        self.style.configure('custom.TLabel', font=('Chakra Petch', 13), bg='white')
        self.style.configure('red.TLabel', font=('Chakra Petch', 13), bg='white', foreground='red')
        self.style.configure('custom.TLabelframe', font=('Chakra Petch', 15), bg='white', borderwidth=0)
        self.style.configure('custom.TButton', font=('Chakra Petch', 15))
        imageAddress = ImageAdrr()
        self.zoomPhoto = imageAddress.zoomPhoto
        self.savePhoto = imageAddress.savePhoto
        self.zoomIn = imageAddress.zoomIn
        self.zoomOut = imageAddress.zoomOut
        self.panLeft = imageAddress.panLeft
        self.panRight = imageAddress.panRight
        self.function1 = imageAddress.fuction1
        self.creat_button()

    def creat_button(self):
        self.readSensorBt = ttk.Button(self, style='custom.Accent.TButton', text="READ\nSENSOR",
                                compound=Tk.TOP, command=self.on_read_sensor_clicked)
        self.readSensorBt.place(relx=0, rely=0.83, width=88, height=75)

        self.freqZoomBt = ttk.Button(self, style='custom.Accent.TButton', text="ZOOM",
                                compound=Tk.TOP)
        self.freqZoomBt.place(relx=0, rely=0.678, width=88, height=75)

        self.freqCursorLeftBt = ttk.Button(self, style='custom.Accent.TButton', text="CURSOR\nLEFT",
                                      )
        self.freqCursorLeftBt.place(relx=0, rely=0.527, width=88, height=75)

        self.freqCursorRightBt = ttk.Button(self, style='custom.Accent.TButton', text="CURSOR\nRIGHT",
                                       )
        self.freqCursorRightBt.place(relx=0, rely=0.375, width=88, height=75)

        self.freqGridtBt = ttk.Button(self, style='custom.Accent.TButton', text="GRID ON",
                                      )
        self.freqGridtBt.place(relx=0, rely=0.223, width=88, height=75)

        self.freqFunctionBt = ttk.Button(self, style='custom.Accent.TButton', text="FUNCTION\nNONE",
                                         )
        self.freqFunctionBt.place(relx=0, rely=0.07, width=88, height=75)

    def on_read_sensor_clicked(self):
        self.readSensorBt.configure(state="disable")
        self.readSensorBt.update_idletasks()
        if self.origin_config.resonance_config_struct['Function'] == "Impact test":
            try:
                t3 = threading.Thread(target=self.frf, args=(0, self.lock))
                t3.start()
                t4 = threading.Thread(target=self.update_label,
                                      args=(self.origin_config.resonance_config_struct["sampling_time"],))
                t4.start()

            except:
                self.readSensorBt.configure(state="normal")
        elif self.origin_config.resonance_config_struct['Function'] == "FRF":
            try:
                t3 = threading.Thread(target=self.frf, args=(1, self.lock))
                t3.start()
                t4 = threading.Thread(target=self.update_label,
                                      args=(self.origin_config.resonance_config_struct["sampling_time"],))
                t4.start()

            except:
                self.readSensorBt.configure(state="normal")

    def update_label(self, num):
        while num >= 0:
            self.infoLabel.configure(text=_("Time remain: ") + f'{str(num)}', style='custom.TLabel')
            self.infoLabel.update_idletasks()
            num -= 1
            time.sleep(1)


    def frf(self, flag, lock):
        global resonance_data, damping_factor, window_len, amplitude_resonance_arr, phase_resonance_arr, x_arr
        resonance_data = []
        self.readSensorBt.configure(state="disable")
        self.readSensorBt.update_idletasks()

        numOfChanel = 4
        chaneln = []
        data_length = self.origin_config.resonance_config_struct["sampleRate"] * \
                      self.origin_config.resonance_config_struct["sampling_time"]
        total_length = data_length * numOfChanel + 1  # 4 cong , +1 là acctual sampling rate
        ttl = []
        with lock:
            ad7609.ADCread.restype = ctypes.POINTER(ctypes.c_float * total_length)
            ad7609.ADCread.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int]
            ad7609.freeme.argtypes = ctypes.c_void_p,
            ad7609.freeme.restype = None
            kq = ad7609.ADCread(data_length, self.origin_config.resonance_config_struct["sampleRate"], numOfChanel)
            ttl = [i for i in kq.contents]
            ad7609.freeme(kq)
        # print("actual_sample_rate:", ttl[-1])
        chanelm = [[], [], [], []]

        for j in range(len(ttl) - 1):
            if j % 4 == 0:
                chanelm[0].append(ttl[j])
            elif j % 4 == 1:
                chanelm[1].append(ttl[j])
            elif j % 4 == 2:
                chanelm[2].append(ttl[j])
            elif j % 4 == 3:
                chanelm[3].append(ttl[j])
            else:
                pass

        for i in range(3):
            chaneln.append(np.array(chanelm[i][2:]))

        # for i in range(3):
        #     chanelv[i]=chaneln[i][2:]*10 #g
        #     chanelv[i]-=np.mean(chanelv[i])

        if self.origin_config.resonance_config_struct["Sensor"] == 'Port1':
            sampleData = chaneln[0]
        elif self.origin_config.resonance_config_struct["Sensor"] == 'Port2':
            sampleData = chaneln[1]
        elif self.origin_config.resonance_config_struct["Sensor"] == 'Port3':
            sampleData = chaneln[2]
        else:
            pass

        sampleData -= np.mean(sampleData)
        sampleData *= 10.0
        if self.origin_config.resonance_config_struct["Hport"] == 'Port1':
            hamerData = chaneln[0]
        elif self.origin_config.resonance_config_struct["Hport"] == 'Port2':
            hamerData = chaneln[1]
        elif self.origin_config.resonance_config_struct["Hport"] == 'Port3':
            hamerData = chaneln[2]
        else:
            pass
        hamerData -= np.mean(hamerData)
        hamerData *= 83.3
        try:
            if flag == 0:
                bp_filter_data = filter_data(sampleData, "BANDPASS",
                                             self.origin_config.resonance_config_struct["FilterFrom"], \
                                             self.origin_config.resonance_config_struct["FilterTo"],
                                             self.origin_config.resonance_config_struct["sampleRate"], "Reactangular")
                [max_pos, max_val] = find_max(bp_filter_data)
                resonance_data = bp_filter_data[max_pos - 20:]
                if len(resonance_data) < window_len:
                    self.infoLabel.configure(text=_('This hit is invalid. Make a new hit.'), style='red.TLabel')
                    self.readSensorBt.configure(state="normal")
                    return
                else:
                    [x_arr, amplitude_arr, phase_arr] = Pd.PLT.plot_impact_test(self.canvas, resonance_data,
                                                                                self.origin_config.resonance_config_struct[
                                                                                    "sampleRate"], window_len,
                                                                                damping_factor)
                    amplitude_resonance_arr = amplitude_arr
                    phase_resonance_arr = phase_arr
                    self.readSensorBt.configure(state="normal")
                    self.readSensorBt.update_idletasks()
            elif flag == 1:
                [max_pos, max_val] = find_max(sampleData)
                resonance_data = sampleData[max_pos - 20:]
                hamer_data = hamerData[max_pos - 20:]
                Pd.PLT.plotfrf(self.canvas, resonance_data, hamer_data,
                               self.origin_config.resonance_config_struct["sampleRate"], window_len, damping_factor)
        except Exception as ex:
            print(ex)
        self.readSensorBt.configure(state="normal")
class ResonancePlotCanvas(Tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bd=1, bg='white', width=934, height=520)
        fig1 = creatFig.creatFigure(self, 3)
        fig1.set_visible(True)
        self.canvas1 = FigureCanvasTkAgg(fig1, master=self)
        self.canvas1.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)