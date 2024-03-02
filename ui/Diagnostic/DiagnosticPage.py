import tkinter as Tk
# import sv_ttk
from tkinter import ttk
import os
from i18n import _
import matplotlib

matplotlib.use('TKAgg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import Axes3D, proj3d
from Calculation.calculate import *
from ui.creatFigure.creatFigure import creatFig
import PlotData.PlotData as Pd
from keyboard.keyboard import KeyBoard
from image.image import ImageAdrr
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main import Application
from scipy.stats import kurtosis
from threading import Lock
import fileOperation.fileOperation as file_operation
import pms.popMessage as pms
import sqlite3 as lite
from ds3231.ds3231B import DS3231
from datetime import datetime
current_directory = os.path.dirname(os.path.realpath(__file__))
parent_directory = os.path.dirname(os.path.dirname(current_directory))
json_filename = parent_directory + '/i18n/sensor_sensitivity.json'
import ctypes
from numpy.ctypeslib import ndpointer
import json
from pathlib import Path
ad7609 = ctypes.CDLL(f'{parent_directory}/ad7609BTZ.so')
blink = 0
blink1 = 0
checkWidget = 'wasi'
track_flag = 0
grid_flag = True
summary_flag=0
view_flag=0
plot_flag=0
SensorPosition='NONE'
def testVal(inStr, acttyp):
    if acttyp == '1':  # insert
        if not inStr.isdigit():
            return False
    return True

def get_time_now():
        try:
            ds3231 = DS3231(1, 0x69)
            rtcTime=str(ds3231.read_datetime())
            return rtcTime[:10]
        except Exception as ex:
            now = datetime.now()
            current_time = now.strftime("%Y-%m-%d")
            return current_time
class DiagnosticPage(Tk.Frame):
    def __init__(self, parent: "Application"):
        self.parent = parent
        self.origin_config=parent.origin_config
        self.ZoomCanvas = Tk.Canvas()
        self.freqFuntionCanvas = Tk.Canvas()
        self.con = lite.connect(f'{parent_directory}/company.db')
        ad7609.init()
        self.lock = Lock()
        imageAddress = ImageAdrr()
        self.settingPhoto = imageAddress.settingPhoto
        self.homePhoto = imageAddress.homePhoto
        self.arrowPhoto = imageAddress.arrowPhoto
        self.zoomPhoto = imageAddress.zoomPhoto
        self.savePhoto = imageAddress.savePhoto
        self.zoomIn = imageAddress.zoomIn
        self.zoomOut = imageAddress.zoomOut
        self.panLeft = imageAddress.panLeft
        self.panRight = imageAddress.panRight
        self.cursorLeft = imageAddress.cursorLeft
        self.cursorRight = imageAddress.cursorRight
        self.function1 = imageAddress.fuction1
        self.json_pathname = Path(json_filename)
        with open(self.json_pathname, 'r', encoding='utf-8') as f:
            currentSensitivity = json.load(f)
        self.origin_config.sensor_sensitivity["acc_sensitivity"]=float(currentSensitivity["accSensitivity"])
        self.origin_config.sensor_sensitivity["vel_sensitivity"]=float(currentSensitivity["velSensitivity"])

        self.btstyle = ttk.Style()
        self.btstyle.configure('normal.TButton', font=('Chakra Petch', 15), borderwidth=1, justify=Tk.CENTER)
        self.btstyle.configure('custom.Accent.TButton', font=('Chakra Petch', 10), justify=Tk.CENTER)
        self.btstyle.configure('custom2.Accent.TButton', font=('Chakra Petch', 8), justify=Tk.CENTER)
        self.btstyle.configure('feature.Accent.TButton', font=('Chakra Petch', 15), borderwidth=1, justify=Tk.CENTER)
        self.btstyle.configure('normal.TLabel', font=('Chakra Petch', 13), background='white')
        self.btstyle.configure('red.TLabel', font=('Chakra Petch', 13), background='white', foreground='#C40069')

        self.mainFrame = Tk.Frame(self.parent, bd=1, bg='white', width=1008, height=584)
        self.mainFrame.pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)
        self.mainFrame.pack_propagate(0)

        self.featureFrame = Tk.Frame(self.mainFrame, bd=1, bg='white', width=1008, height=80)
        self.featureFrame.pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)
        self.featureFrame.pack_propagate(0)

        self.configFrame = Tk.Frame(self.mainFrame, name="trang cai dat chinh", bd=1, bg='white', width=918, height=504)
        self.configFrame.pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)
        self.configFrame.pack_propagate(0)

        self.waveformPlotFrame = Tk.Frame(self.mainFrame, name="wave", bd=1, bg='white', width=918, height=504)
        self.waveformPlotFrame.pack(side=Tk.LEFT, fill=Tk.BOTH, expand=1)
        self.waveformPlotFrame.pack_propagate(0)
        self.waveformPlotFrame.pack_forget()

        self.freqPlotFrame = Tk.Frame(self.mainFrame, name="freq", bd=1, bg='white', width=918, height=504)
        self.freqPlotFrame.pack(side=Tk.LEFT, fill=Tk.BOTH, expand=1)
        self.freqPlotFrame.pack_propagate(0)
        self.freqPlotFrame.pack_forget()

        self.generalPlotFrame = Tk.Frame(self.mainFrame, name="gene", bd=1, bg='white', width=918, height=504)
        self.generalPlotFrame.pack(side=Tk.LEFT, fill=Tk.BOTH, expand=1)
        self.generalPlotFrame.pack_propagate(0)
        self.generalPlotFrame.pack_forget()

        self.summaryPlotFrame = Tk.Frame(self.mainFrame, name="suma", bd=1, bg='white', width=918, height=504)
        self.summaryPlotFrame.pack(side=Tk.LEFT, fill=Tk.BOTH, expand=1)
        self.summaryPlotFrame.pack_propagate(0)
        self.summaryPlotFrame.pack_forget()

        self.waveformSideButtonFrame = Tk.Frame(self.mainFrame, name="wasi", bd=1, bg='white', width=90, height=504)
        self.waveformSideButtonFrame.pack(side=Tk.RIGHT, fill=Tk.Y, expand=1)
        self.waveformSideButtonFrame.pack_propagate(0)
        self.waveformSideButtonFrame.pack_forget()

        self.freqSideButtonFrame = Tk.Frame(self.mainFrame, name="frsi", bd=1, bg='white', width=90, height=504)
        self.freqSideButtonFrame.pack(side=Tk.RIGHT, fill=Tk.Y, expand=1)
        self.freqSideButtonFrame.pack_propagate(0)
        self.freqSideButtonFrame.pack_forget()

        self.generalSideButtonFrame = Tk.Frame(self.mainFrame, bd=1, bg='white', width=90, height=504)
        self.generalSideButtonFrame.pack(side=Tk.RIGHT, fill=Tk.Y, expand=1)
        self.generalSideButtonFrame.pack_propagate(0)
        self.generalSideButtonFrame.pack_forget()

        self.infoFrame= Tk.Frame(self.featureFrame, width=170, height=72, bg='white', bd=0)
        self.infoFrame.place(relx=0.711, rely=0.018)

        self.creat_diagnostic_page()

        self.parent.bind_class('TEntry', "<FocusIn>", self.show_key_board)
        self.parent.bind_class('TCombobox', "<<ComboboxSelected>>", self.change_state)

    def show_key_board(self, event):
        self.applyBt.configure(state='normal')
        self.widget = self.get_focus_widget()
        self.keyboardFrame = KeyBoard(self.widget)
        parentName = event.widget.winfo_parent()
        self.parent1 = event.widget._nametowidget(parentName)
        self.parent1.focus()

    def get_focus_widget(self):
        widget = self.parent.focus_get()
        return widget

    def change_state(self, event):
        self.applyBt.configure(state="normal")

    def creat_diagnostic_page(self):
        self.creat_diagnostic_feature_panel()
        self.creat_diagnostic_config_panel()
        self.creat_side_panel()
        self.waveformFrameCanvas = WaveformFrameCanvas(self.waveformPlotFrame)
        self.frequencyFrameCanvas = FrequencyFrameCanvas(self.freqPlotFrame)
        self.generalFrameCanvas = GeneralFrameCanvas(self.generalPlotFrame)
        self.summaryFrameCanvas = SummaryFrameCanvas(self.summaryPlotFrame)
     
    def creat_diagnostic_feature_panel(self):

        self.homeBt = ttk.Button(self.featureFrame, style='normal.TButton', text=_("Home"), image=self.homePhoto,
                                 compound=Tk.TOP, \
                                 command=self.go_home)
        self.homeBt.place(relx=0, rely=0.018, width=100, height=72)
        self.homeBt.image = self.homePhoto

        barrie=Tk.Frame(self.featureFrame, width=3, height=72, background='grey')
        barrie.place(relx=0.11, rely=0.018)

        self.configBt = ttk.Button(self.featureFrame, style='normal.TButton', text=_("Config"), \
                                   command=lambda: self.on_config_button_clicked())
        self.configBt.place(relx=0.122, rely=0.018, width=115, height=72)

        self.arrowLabel = ttk.Label(self.featureFrame, style='normal.TLabel', image=self.arrowPhoto)
        self.arrowLabel.place(relx=0.238, rely=0.25)
        self.arrowLabel.image = self.arrowPhoto

        self.waveformBt = ttk.Button(self.featureFrame, style='normal.TButton', text=_("Waveform\nAnalysis"), \
                                     command=self.on_waveform_button_clicked)
        self.waveformBt.place(relx=0.265, rely=0.018, width=143, height=72)

        self.frequencyBt = ttk.Button(self.featureFrame, style='normal.TButton', text=_("Frequency\nAnalysis"), \
                                      command=self.on_frequency_button_clicked)
        self.frequencyBt.place(relx=0.413, rely=0.018, width=143, height=72)

        self.generalBt = ttk.Button(self.featureFrame, style='normal.TButton', text=_("General\nMonitoring"), \
                                    command=self.on_general_button_clicked)
        self.generalBt.place(relx=0.562, rely=0.018, width=143, height=72)

        self.infoLabel1=ttk.Label(self.infoFrame, text=_("Information"), style="red.TLabel")
        self.infoLabel1.grid(column=0, row=0, padx=0, pady=5, sticky='w')

        self.infoLabel2 = ttk.Label(self.infoFrame, text="OK.", style="normal.TLabel", width=26)
        self.infoLabel2.grid(column=0, row=1, padx=0, pady=5, sticky='w')

    def creat_diagnostic_config_panel(self):
        def clean_frame_for_config_panel():
            for widget in self.configFrame.winfo_children():
                widget.destroy()
            self.waveformPlotFrame.pack_forget()
            self.waveformSideButtonFrame.pack_forget()
            self.freqPlotFrame.pack_forget()
            self.freqSideButtonFrame.pack_forget()
            self.generalPlotFrame.pack_forget()
            self.generalSideButtonFrame.pack_forget()
            self.summaryPlotFrame.pack_forget()
            self.configFrame.pack()
            self.waveformBt.configure(style="normal.TButton")
            self.frequencyBt.configure(style="normal.TButton")
            self.generalBt.configure(style="normal.TButton")
            self.configBt.configure(style="feature.Accent.TButton")
        clean_frame_for_config_panel()
        self.config1 = ConfigFrame(self, self.con)
        self.config1.pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)
        self.nextBt = ttk.Button(self.configFrame, text=_("APPLY & START"), style='Accent.TButton',
                                 command=lambda: self.on_start_button_clicked(True))
        self.nextBt.place(relx=0.8, rely=0.89, width=175, height=48)

        self.applyBt = ttk.Button(self.configFrame, text=_("APPLY"), style='Accent.TButton',
                                 command=lambda: self.on_apply_button_clicked(True))
        self.applyBt.place(relx=0.6, rely=0.89, width=175, height=48)

    def creat_side_panel(self):
        saveBt = ttk.Button(self.waveformSideButtonFrame, style='custom.Accent.TButton', text=_("SAVE"),
                            image=self.savePhoto,
                            compound=Tk.TOP,
                            command=self.on_save_button_clicked)
        saveBt.place(x=0, y=194, width=88, height=75)
        saveBt.image = self.savePhoto

        self.laserBt = ttk.Button(self.waveformSideButtonFrame, style='custom.Accent.TButton', text=_("LASER\nVIEW"),
                               command=self.on_laser_button_clicked)
        self.laserBt.place(x=0, y=271, width=88, height=75)

        zoomBt = ttk.Button(self.waveformSideButtonFrame, style='custom.Accent.TButton', text=_("ZOOM"),
                            image=self.zoomPhoto,
                            compound=Tk.TOP, command=lambda: self.creat_zoom_frame(1, 827, 117))
        zoomBt.place(x=0, y=348, width=88, height=75)
        zoomBt.image = self.zoomPhoto

        readData = ttk.Button(self.waveformSideButtonFrame, style='custom.Accent.TButton', text=_("READ\nSENSOR"),
                              command=self.on_read_sensor_button_clicked)
        readData.place(x=0, y=425, width=88, height=75)
###

        freqSaveBt = ttk.Button(self.freqSideButtonFrame, style='custom.Accent.TButton', text=_("SAVE"),
                                image=self.savePhoto,
                                compound=Tk.TOP,
                                command=self.on_save_button_clicked)
        freqSaveBt.place(x=0, y=425, width=88, height=75)
        freqSaveBt.image = self.savePhoto

        freqZoomBt = ttk.Button(self.freqSideButtonFrame, style='custom.Accent.TButton', text=_("ZOOM"),
                                image=self.zoomPhoto,
                                compound=Tk.TOP, command=lambda: self.creat_zoom_frame(2, 827, 117))
        freqZoomBt.place(x=0, y=348, width=88, height=75)
        freqZoomBt.image = self.zoomPhoto

        freqCursorLeftBt = ttk.Button(self.freqSideButtonFrame, style='custom.Accent.TButton', text=_("CURSOR\nLEFT"),
                                      command=lambda: self.Tracking(False))
        freqCursorLeftBt.place(x=0, y=271, width=88, height=75)

        freqCursorRightBt = ttk.Button(self.freqSideButtonFrame, style='custom.Accent.TButton', text=_("CURSOR\nRIGHT"),
                                       command=lambda: self.Tracking(True))
        freqCursorRightBt.place(x=0, y=194, width=88, height=75)

        self.freqGridtBt = ttk.Button(self.freqSideButtonFrame, style='custom.Accent.TButton', text=_("GRID ON"),
                                      command=self.on_grid_button)
        self.freqGridtBt.place(x=0, y=117, width=88, height=75)

        self.freqFunctionBt = ttk.Button(self.freqSideButtonFrame, style='custom.Accent.TButton', text=_("FUNCTION\nNONE"),
                                         command=lambda: self.creat_frequency_funtion_button_canvas(827, 40))
        self.freqFunctionBt.place(x=0, y=40, width=88, height=75)
##
        generalSummatyBt = ttk.Button(self.generalSideButtonFrame, style='custom.Accent.TButton', text=_("SUMMARY"),
                                      command= self.on_summary_button_clicked)
        generalSummatyBt.place(x=0, y=348, width=88, height=75)

        generalSaveBt = ttk.Button(self.generalSideButtonFrame, style='custom.Accent.TButton',
                                            image=self.savePhoto,
                                            compound=Tk.TOP,
                                            text=_("SAVE"),
                                            command=self.on_save_button_clicked)
        generalSaveBt.image=self.savePhoto
        generalSaveBt.place(x=0, y=425, width=88, height=75)

    def go_home(self):
        self.mainFrame.destroy()
        self.parent.go_to_home_page()

    def read_sensor(self):
        self.origin_config.sensor_config = {
            "sensor_input": [],
            "sensor_position":[],
            "sensor_data": [],
            "store_sensor_data": [[],[],[]],
            "unit": [],
            "sensor_key": [],
            "sample_rate": 5120,
            "fft_line": 3200,
            "vel": [],
            "accel": [],
            "vel_data": [],
            "accel_data": [],
            "dis": [],
            "displacement_data": [],

        }
        unit = ['', '', '', '', '', '']
        chaneln = []
        self.origin_config.sensor_config["sample_rate"] = int(self.origin_config.waveform_config_struct["Fmax"] * 2.56)
        self.origin_config.sensor_config["fft_line"] = self.origin_config.waveform_config_struct["num_fft_line"]
        self.origin_config.sensor_config["sensor_input"].append(
            self.origin_config.waveform_config_struct["Sensor1"])
        self.origin_config.sensor_config["sensor_input"].append(
            self.origin_config.waveform_config_struct["Sensor2"])
        self.origin_config.sensor_config["sensor_input"].append(
            self.origin_config.waveform_config_struct["Sensor3"])
        self.origin_config.sensor_config["sensor_input"].append(
            self.origin_config.waveform_config_struct["Sensor4"])
        self.origin_config.sensor_config["sensor_key"].append(
            self.origin_config.waveform_config_struct["KeyPhase"])
        
        
        if self.origin_config.waveform_config_struct["Port1Pos"]!="NONE":
            self.origin_config.sensor_config["sensor_position"].append(1)
        else:
            self.origin_config.sensor_config["sensor_position"].append(0)

        if self.origin_config.waveform_config_struct["Port2Pos"]!="NONE":
            self.origin_config.sensor_config["sensor_position"].append(1)
        else:
            self.origin_config.sensor_config["sensor_position"].append(0)
        
        if self.origin_config.waveform_config_struct["Port3Pos"]!="NONE":
            self.origin_config.sensor_config["sensor_position"].append(1)
        else:
            self.origin_config.sensor_config["sensor_position"].append(0)

        if self.origin_config.sensor_config["sensor_input"][3] == "TACHOMETER":
            n = 6
        else:
            n = 4
        data_length = pow2(int(self.origin_config.sensor_config["fft_line"]*2.56))
        waitingTime=int(data_length/self.origin_config.sensor_config["sample_rate"])+2
        self.infoLabel2.configure(text=_("READING.....Please wait:")+ f" {str(waitingTime)} " +_("seconds."), style="red.TLabel")
        self.infoLabel2.update_idletasks()
        total_length=data_length*n+1
        ttl=[]
        # with self.lock:
        ad7609.ADCread.restype = ctypes.POINTER(ctypes.c_float * total_length)
        ad7609.ADCread.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int]
        ad7609.freeme.argtypes = ctypes.c_void_p,
        ad7609.freeme.restype = None
        kq=ad7609.ADCread(data_length, self.origin_config.sensor_config["sample_rate"], n)
        ttl=[i for i in kq.contents]
        ad7609.freeme(kq)
        actual_sample_rate= int(ttl[-1])
        chanelm=[[],[],[],[],[]]
        if n==4:
            for j in range(len(ttl)-1):
                if j%4==0:
                    chanelm[0].append(ttl[j])
                elif j%4==1:
                    chanelm[1].append(ttl[j])
                elif j%4==2:
                    chanelm[2].append(ttl[j])
                elif j%4==3:
                    chanelm[3].append(ttl[j])
                else:
                    pass
        elif n==6:
            for j in range(len(ttl)-1):
                if j%6==0:
                    chanelm[0].append(ttl[j])
                elif j%6==1:
                    chanelm[1].append(ttl[j])
                elif j%6==2:
                    pass
                    # chanelm[5].append(ttl[j])
                elif j%6==3:
                    chanelm[2].append(ttl[j])
                elif j%6==4:
                    chanelm[3].append(ttl[j])
                elif j%6==5:
                    chanelm[4].append(ttl[j])
                else:
                    pass
        for i in range(n - 1):
            chaneln.append(np.array(chanelm[i]))

        if n == 6:
            chaneln[4] = fresh_laser_pulse(chaneln[4])
            unit[3] = 'laser sensor'
        if self.origin_config.waveform_config_struct["UseTSA"] == 1 and n == 6:
            mark = []
            chanelk = []
            for i in range(len(chaneln[4]) - 1):
                if chaneln[4][i] < 0.5 and chaneln[4][i + 1] > 0.7:
                    mark.append(i + 1)
            tsa_temp_value = self.origin_config.waveform_config_struct["TSATimes"]
            if tsa_temp_value >= len(mark):
                tsa_temp_value = len(mark) - 1
            if len(mark) > 5:
                chanelk = tsa_convert(chaneln, mark, tsa_temp_value)
                self.origin_config.sensor_config["sensor_data"] = chanelk
            else:
                self.origin_config.sensor_config["sensor_data"] = chaneln

        else:
            self.origin_config.sensor_config["sensor_data"] = chaneln
        accConvertFactor=1000/self.origin_config.sensor_sensitivity["acc_sensitivity"]
        velConvertFactor=1000/self.origin_config.sensor_sensitivity["vel_sensitivity"]
        for i in range(3):
            if self.origin_config.sensor_config["sensor_input"][i] == 'Accelerometer' and self.origin_config.sensor_config["sensor_position"][i]!=0:
                self.origin_config.sensor_config["sensor_data"][i] *= accConvertFactor  # g
                self.origin_config.sensor_config["sensor_data"][i] -= np.mean(
                    self.origin_config.sensor_config["sensor_data"][i])

                unit[i] = 'g'
                self.origin_config.sensor_config["accel"].append(i)
                self.origin_config.sensor_config["vel"].append(i)
                self.origin_config.sensor_config["dis"].append(i)
                
                self.origin_config.sensor_config["vel_data"].append(
                    acc2vel(self.origin_config.sensor_config["sensor_data"][i],
                            self.origin_config.sensor_config["sample_rate"]))

                self.origin_config.sensor_config["displacement_data"].append(
                    vel2disp(acc2vel(self.origin_config.sensor_config["sensor_data"][i],
                                     self.origin_config.sensor_config["sample_rate"]),
                             self.origin_config.sensor_config["sample_rate"]))
                self.origin_config.sensor_config["store_sensor_data"][i]=\
                                        filter_data(self.origin_config.sensor_config["sensor_data"][i], "BANDPASS",
                                        dfc._PRE_HIGHPASS_FROM,
                                        self.origin_config.waveform_config_struct["Fmax"],
                                        self.origin_config.sensor_config["sample_rate"],
                                        window="Hanning")
                self.origin_config.sensor_config["accel_data"].append(
                    self.origin_config.sensor_config["store_sensor_data"][i])     

            elif self.origin_config.sensor_config["sensor_input"][i] == 'Velocity Sensor' and self.origin_config.sensor_config["sensor_position"][i]!=0:
                self.origin_config.sensor_config["sensor_data"][i] *= velConvertFactor  # mm/s
                self.origin_config.sensor_config["sensor_data"][i] -= np.mean(
                    self.origin_config.sensor_config["sensor_data"][i])
                self.origin_config.sensor_config["store_sensor_data"][i]=\
                            filter_data(self.origin_config.sensor_config["sensor_data"][i], "BANDPASS",
                            dfc._PRE_HIGHPASS_FROM,
                            dfc._RMS_LOWPASS_TO,
                            self.origin_config.sensor_config["sample_rate"],
                            window="Hanning")

                unit[i] = 'mm/s'
                self.origin_config.sensor_config["vel"].append(i)
                self.origin_config.sensor_config["dis"].append(i)
                self.origin_config.sensor_config["vel_data"].append(
                    self.origin_config.sensor_config["store_sensor_data"][i])
                self.origin_config.sensor_config["displacement_data"].append(
                    vel2disp(self.origin_config.sensor_config["sensor_data"][i],
                             self.origin_config.sensor_config["sample_rate"]))
                             
            elif self.origin_config.sensor_config["sensor_position"][i]==0:
                self.origin_config.sensor_config["sensor_data"][i] *= 0
                self.origin_config.sensor_config["store_sensor_data"][i]=self.origin_config.sensor_config["sensor_data"][i][700:-700]
                unit[i] = 'no sensor'
            else:
                pass
        self.origin_config.sensor_config["unit"] = unit
        self.infoLabel2.configure(text=_("Actual sample rate:")+ f" {str(actual_sample_rate)}", style="normal.TLabel")

    def on_laser_button_clicked(self): 
        global view_flag
        view_flag=not view_flag
        try:
            if view_flag==1:
                self.laserBt.configure(text=_("NORMAL\nVIEW"))
                _canal=self.origin_config.sensor_config["sensor_data"][4]
                _sample_rate=self.origin_config.sensor_config["sample_rate"]
                Pd.PLT.plot1chanel(self.waveformFrameCanvas.canvas1, _canal, self.origin_config.sensor_config["unit"][4], _sample_rate, win_var="Hanning")
            else:
                self.laserBt.configure(text=_("LASER\nVIEW"))
                self.on_refresh_button_clicked()
        except:
            self.infoLabel2.configure(text=_("Data errors"))
    def on_save_button_clicked(self):
        sample_rate = int(self.origin_config.waveform_config_struct["Fmax"]*2.56)
        driveCheckVal = self.origin_config.waveform_config_struct["MachineType"]
        companyName = self.origin_config.project_struct["CompanyName"]
        prjCode = self.origin_config.project_struct["ProjectCode"]
        if companyName!="" and prjCode!="":
            companyNameTuple=(companyName,)
            prjCodeTuple=(prjCode,)
            rpmVal = self.origin_config.waveform_config_struct["Speed"]
            powerVal = self.origin_config.waveform_config_struct["Power"]
            foundationVal = self.origin_config.waveform_config_struct["Foundation"]
            bearingBoreVal = self.origin_config.waveform_config_struct["BearingBore"]
            gearToothVal = self.origin_config.waveform_config_struct["GearTeeth"]
            date = self.origin_config.project_struct["Date"]
            machineName = self.origin_config.waveform_config_struct["MachineName"]

            ss1=self.origin_config.waveform_config_struct["Sensor1"][0]
            ss2=self.origin_config.waveform_config_struct["Sensor2"][0]
            ss3=self.origin_config.waveform_config_struct["Sensor3"][0]
            p1=self.origin_config.waveform_config_struct["Port1Pos"]
            p2=self.origin_config.waveform_config_struct["Port2Pos"]
            p3=self.origin_config.waveform_config_struct["Port3Pos"]
            if len(self.origin_config.sensor_config["store_sensor_data"])!=0:
                canal1 = self.origin_config.sensor_config["store_sensor_data"][0]
                canal2 = self.origin_config.sensor_config["store_sensor_data"][1]
                canal3 = self.origin_config.sensor_config["store_sensor_data"][2]
            else:
                pms.show_error(_('There is no data !'))
                return
            if len(canal1)!= 0:
                canal1_str = file_operation.conv_str_tag(canal1)
                canal2_str = file_operation.conv_str_tag(canal2)
                canal3_str = file_operation.conv_str_tag(canal3)
                # canal4_str = file_operation.conv_str_tag(canal4)

                with self.con:
                    cur = self.con.cursor()
                    exist_name=cur.execute(f"SELECT * FROM Company_ID WHERE NAME = ?", companyNameTuple)
                    arr=[b for b in exist_name]
                    exist_code=cur.execute(f"SELECT * FROM Project_ID WHERE CODE = ?", prjCodeTuple)
                    arr1=[b for b in exist_code]
                    companylist = cur.execute("SELECT * FROM Company_ID")
                    companylistarr = [b for b in companylist]
                    # projectlist = cur.execute("SELECT * FROM Project_ID")
                    # projectlistarr = [b for b in projectlist]
                    companyData={
                        "id":len(companylistarr)+1,
                        "name": companyName,
                        "address":''
                    }
                    projectData={
                        "id":len(companylistarr)+1,
                        "code":str(prjCode),
                        "power":powerVal,
                        "rpm":rpmVal,
                        "driven":str(driveCheckVal),
                        "note":str(machineName),
                        "foundation":str(foundationVal),
                        "gearTooth":gearToothVal,
                        "bearingBore":bearingBoreVal
                    }

                    channel1Data={
                        "prjCode":str(prjCode),
                        "date":str(date),
                        "position":str(p1+ss1),
                        "chanelData":str(canal1_str),
                        "sampleRate":sample_rate
                    }
                    channel2Data={
                        "prjCode":str(prjCode),
                        "date":str(date),
                        "position":str(p2+ss2),
                        "chanelData":str(canal2_str),
                        "sampleRate":sample_rate
                    }
                    channel3Data={
                        "prjCode":str(prjCode),
                        "date":str(date),
                        "position":str(p3+ss3),
                        "chanelData":str(canal3_str),
                        "sampleRate":sample_rate
                    }
                    if len(arr)==0 and len(arr1)==0:
                        if pms.company_project_dont_exist_warning()==True:
                            cur.execute(f"INSERT INTO Company_ID (COM_ID, NAME, ADR) VALUES (:id, :name, :address)", companyData)
                            cur.execute(f"""INSERT INTO Project_ID (COM_ID, CODE, POWER, RPM, DRIVEN, NOTE, FOUNDATION, GEARTOOTH, BEARINGBORE) VALUES 
                                        (:id, :code, :power, :rpm, :driven, :note, :foundation, :gearTooth, :bearingBore)""", projectData)
                            if ss1 != 'N' and p1 != "NONE":
                                cur.execute(f""" INSERT INTO DATA (CODE, DATE, POS, DATA, Sample_rate) VALUES (:prjCode, :date, :position, :chanelData, :sampleRate)""", channel1Data)
                            else:
                                pass
                            if ss2 != 'N' and p2 != "NONE":
                                cur.execute(f""" INSERT INTO DATA (CODE, DATE, POS, DATA, Sample_rate) VALUES (:prjCode, :date, :position, :chanelData, :sampleRate)""", channel2Data)
                            else:
                                pass
                            if ss3 != 'N' and p3 != "NONE":
                                cur.execute(f""" INSERT INTO DATA (CODE, DATE, POS, DATA, Sample_rate) VALUES (:prjCode, :date, :position, :chanelData, :sampleRate)""", channel3Data)
                            else:
                                pass
                            self.infoLabel2.configure(text=_("Data is saved."), style="normal.TLabel")

                        else:
                            print('Data is not save')

                    elif len(arr)==0 and len(arr1)==1:
                        pms.company_project_exist_error()

                    elif len(arr) == 1 and len(arr1) == 0:
                        if(pms.company_or_project_existed_warning())==True:
                            projectData1={
                            "id":arr[0][0],
                            "code":str(prjCode),
                            "power":powerVal,
                            "rpm":rpmVal,
                            "driven":str(driveCheckVal),
                            "note":str(machineName),
                            "foundation":str(foundationVal),
                            "gearTooth":gearToothVal,
                            "bearingBore":bearingBoreVal
                            }
                            cur.execute(f"""INSERT INTO Project_ID (COM_ID, CODE, POWER, RPM, DRIVEN, NOTE, FOUNDATION, GEARTOOTH, BEARINGBORE) 
                            VALUES (:id, :code, :power, :rpm, :driven, :note, :foundation, :gearTooth, :bearingBore)""", projectData1)
                            if ss1 != 'N' and p1 != "NONE":
                                cur.execute(f""" INSERT INTO DATA (CODE, DATE, POS, DATA, Sample_rate) VALUES (:prjCode, :date, :position, :chanelData, :sampleRate)""", channel1Data)
                            else:
                                pass
                            if ss2 != 'N' and p2 != "NONE":
                                cur.execute(f""" INSERT INTO DATA (CODE, DATE, POS, DATA, Sample_rate) VALUES (:prjCode, :date, :position, :chanelData, :sampleRate)""", channel2Data)
                            else:
                                pass
                            if ss3 != 'N' and p3 != "NONE":
                                cur.execute(f""" INSERT INTO DATA (CODE, DATE, POS, DATA, Sample_rate) VALUES (:prjCode, :date, :position, :chanelData, :sampleRate)""", channel3Data)
                            else:
                                pass
                            self.infoLabel2.configure(text=_("Data is saved."), style="normal.TLabel")
                        else:
                            pass
                    elif len(arr) == 1 and len(arr1) == 1:
                        if arr[0][0]==arr1[0][1] :
                            if pms.company_project_existed_warning()==True:
                                if ss1 != 'N' and p1 != "NONE":
                                    cur.execute(
                                        f""" INSERT INTO DATA (CODE, DATE, POS, DATA, Sample_rate) VALUES (:prjCode, :date, :position, :chanelData, :sampleRate)""", channel1Data)
                                else:
                                    pass
                                if ss2 != 'N' and p2 != "NONE":
                                    cur.execute(
                                        f""" INSERT INTO DATA (CODE, DATE, POS, DATA, Sample_rate) VALUES (:prjCode, :date, :position, :chanelData, :sampleRate)""", channel2Data)
                                else:
                                    pass
                                if ss3 != 'N' and p3 != "NONE":
                                    cur.execute(
                                        f""" INSERT INTO DATA (CODE, DATE, POS, DATA, Sample_rate) VALUES (:prjCode, :date, :position, :chanelData, :sampleRate)""", channel3Data)
                                else:
                                    pass
                                self.infoLabel2.configure(text=_("Data is saved."), style="normal.TLabel")
                            else:
                                pass
                        else:
                            pms.company_project_exist_error()
                    else:
                        pass
            else:
                pms.show_error(_('There is no data !'))
                return
        else:
            pms.show_error(_('Please input project code and company name !'))
            return   
    def get_focus_widget(self):
        widget = self.parent.focus_get()
        return widget

    def creat_zoom_frame(self, widget, x_pos, y_pos):
        global blink, blink1, checkWidget
        if blink1 == 1:
            self.freqFuntionCanvas.destroy()
            blink1=0
        focusingWidget = str(self.get_focus_widget())[9:13]
        self.ZoomCanvas.destroy()

        if focusingWidget == checkWidget:
            blink = not blink
            if blink == 1:
                if widget == 1:
                    self.creat_zoom_button_canvas(self.waveformPlotFrame, self.waveformFrameCanvas.canvas1, x_pos,
                                                  y_pos, 1)
                if widget == 2:
                    self.creat_zoom_button_canvas(self.freqPlotFrame, self.frequencyFrameCanvas.canvas2, x_pos,
                                                  y_pos, 0)
            elif blink == 0:
                self.ZoomCanvas.destroy()
        else:
            if widget == 1:
                self.creat_zoom_button_canvas(self.waveformPlotFrame, self.waveformFrameCanvas.canvas1, x_pos,
                                              y_pos, 1)
            if widget == 2:
                self.creat_zoom_button_canvas(self.freqPlotFrame, self.frequencyFrameCanvas.canvas2, x_pos,
                                              y_pos, 0)
            checkWidget = focusingWidget
            blink = 1

    def creat_zoom_button_canvas(self, widget, draw_canvas, x_pos, y_pos, function_flag):

        self.zoomstyle=ttk.Style()
        self.zoomstyle.configure('zoom.Accent.TButton', font=('Chakra Petch', 9), justify=Tk.CENTER)
        self.ZoomCanvas = Tk.Canvas(widget, width=90, height=385, bg='white')
        self.ZoomCanvas.place(x=x_pos, y=y_pos)
        button1 = ttk.Button(self.ZoomCanvas, text=_("ZOOM IN"), style='zoom.Accent.TButton', image=self.zoomIn,
                             compound=Tk.TOP,
                             command=lambda: self.view_change(draw_canvas, _type='IN'))
        button1.place(x=0, y=0, width=88, height=75)
        button1.image = self.zoomIn

        button2 = ttk.Button(self.ZoomCanvas, text=_("ZOOM OUT"), style='zoom.Accent.TButton', image=self.zoomOut,
                             compound=Tk.TOP,
                             command=lambda: self.view_change(draw_canvas, _type='OUT'))
        button2.place(x=0, y=77, width=88, height=75)
        button2.image = self.zoomOut
        button3 = ttk.Button(self.ZoomCanvas, text=_("PAN LEFT"), style='zoom.Accent.TButton', image=self.panLeft,
                             compound=Tk.TOP,
                             command=lambda: self.view_change(draw_canvas, _type='LEFT'))
        button3.place(x=0, y=154, width=88, height=75)
        button3.image = self.panLeft

        button4 = ttk.Button(self.ZoomCanvas, text=_("PAN RIGHT"), style='zoom.Accent.TButton', image=self.panRight,
                             compound=Tk.TOP,
                             command=lambda: self.view_change(draw_canvas, _type='RIGHT'))
        button4.place(x=0, y=231, width=88, height=75)
        button4.image = self.panRight

        button5 = ttk.Button(self.ZoomCanvas, text=_("RESET"), style='zoom.Accent.TButton',
                             command=self.on_refresh_button_clicked if function_flag==1 else self.on_no_filter_button_clicked)
        button5.place(x=0, y=308, width=88, height=75)

    def view_change(self, canvas, _type):
        axes_arr = canvas.figure.get_axes()
        try:
            for ax in axes_arr:
                if _type == "RIGHT":
                    [xleft, xright] = ax.get_xlim()
                    xright -= 50
                    xleft -= 50
                    ax.set_xlim(xleft, xright)

                elif _type == "LEFT":
                    [xleft, xright] = ax.get_xlim()
                    xright += 50
                    xleft += 50
                    if xright >= 0:
                        ax.set_xlim(xleft, xright)

                elif _type == "IN":
                    [xleft, xright] = ax.get_xlim()
                    xright -= 100
                    if xright < xleft + 100:
                        xright = xleft + 100
                    ax.set_xlim(xleft, xright)

                elif _type == "OUT":
                    [xleft, xright] = ax.get_xlim()
                    xright += 100
                    ax.set_xlim(xleft, xright)
            canvas.draw()
        except:
            pass

    def creat_frequency_funtion_button_canvas(self, x_pos, y_pos):
        global blink1, blink
        blink1 = not blink1
        if blink == 1:
            self.ZoomCanvas.destroy()
            blink=0
        if blink1 == 1:
            self.draw_frequency_function_button_canvas(self.freqPlotFrame, self.frequencyFrameCanvas.canvas2, x_pos,
                                                       y_pos)
        elif blink1 == 0:
            self.freqFuntionCanvas.destroy()

    def draw_frequency_function_button_canvas(self, widget, draw_canvas, x_pos, y_pos):

        self.freqFuntionCanvas = Tk.Canvas(widget, width=90, height=385, bg='white')
        self.freqFuntionCanvas.place(x=x_pos, y=y_pos)
        button1 = ttk.Button(self.freqFuntionCanvas, text=_("NONE"), style='custom2.Accent.TButton',
                             compound=Tk.TOP,
                             command=self.on_no_filter_button_clicked)
        button1.place(x=0, y=0, width=88, height=75)

        button2 = ttk.Button(self.freqFuntionCanvas, text=_("FILTER"), style='custom2.Accent.TButton',
                             compound=Tk.TOP,
                             command=self.on_filter_button_clicked)
        button2.place(x=0, y=77, width=88, height=75)
        button3 = ttk.Button(self.freqFuntionCanvas, text=_("ENVELOPED"), style='custom2.Accent.TButton',
                             compound=Tk.TOP,
                             command=self.on_envelop_button_clicked)
        button3.place(x=0, y=154, width=88, height=75)

        button4 = ttk.Button(self.freqFuntionCanvas, text=_("PSD"), style='custom2.Accent.TButton',
                             compound=Tk.TOP,
                             command=self.on_psd_button_click)
        button4.place(x=0, y=231, width=88, height=75)

        button5 = ttk.Button(self.freqFuntionCanvas, text=_("VELOCITY\nSPECTRAL"), style='custom2.Accent.TButton',
                             compound=Tk.TOP,
                             command=self.on_velocity_spectrum_button_click)
        button5.place(x=0, y=308, width=88, height=75)

    def on_no_filter_button_clicked(self):
        global grid_flag, plot_flag, track_flag
        track_flag=0
        plot_flag=0
        grid_flag = True
        self.freqGridtBt.configure(text=_("GRID ON"))
        self.freqFunctionBt.configure(text=_("FUNCTION\nNONE"))
        win_var = self.origin_config.frequency_config_struct["Window"]
        try:
            canal1 = self.origin_config.sensor_config["store_sensor_data"][0]
            canal2 = self.origin_config.sensor_config["store_sensor_data"][1]
            canal3 = self.origin_config.sensor_config["store_sensor_data"][2]
            _sample_rate = self.origin_config.sensor_config["sample_rate"]
            Pd.PLT.plot_fft(self.frequencyFrameCanvas.canvas2, canal1, canal2, canal3, _sample_rate,
                            self.origin_config.sensor_config["unit"][:3], [1, 2, 3],
                            win_var)
        except:
            pass
            # self.inforLabel2.config(text=_("Data errors."), bg="lavender", fg="red", font="Verdana 13")

    def on_filter_button_clicked(self):
        global grid_flag, plot_flag, track_flag
        plot_flag=1
        track_flag=0
        grid_flag = True
        try:
            self.freqGridtBt.configure(text=_("GRID ON"))
            self.freqFunctionBt.configure(text=_("FUNCTION\nFILTER"))
            self.filterCallback()
        except:
            pass
            # self.inforLabel2.config(text=_("Data errors."), bg="lavender", fg="red", font="Verdana 13")

    def on_envelop_button_clicked(self):
        global grid_flag, plot_flag, track_flag
        track_flag=0
        plot_flag=1
        grid_flag = True
        try:
            self.freqGridtBt.configure(text=_("GRID ON"))
            self.freqFunctionBt.configure(text=_("FUNCTION\nENVELOPED"))
            _sample_rate = self.origin_config.sensor_config["sample_rate"]
            win_var = self.origin_config.frequency_config_struct["Window"]
            env_result = calculate_enveloped_signal(self.origin_config)
            if len(env_result) != -1:
                amplitude_envelope1 = env_result[0]
                amplitude_envelope2 = env_result[1]
                amplitude_envelope3 = env_result[2]
                Pd.PLT.plot_fft(self.frequencyFrameCanvas.canvas2, amplitude_envelope1, amplitude_envelope2,
                                amplitude_envelope3,
                                _sample_rate,
                                self.origin_config.sensor_config["unit"][:3], [1, 2, 3], win_var)
        except:
            pass

    def on_psd_button_click(self):
        global grid_flag, plot_flag, track_flag
        track_flag=0
        plot_flag=1
        grid_flag = True
        try:
            self.freqGridtBt.configure(text=_("GRID ON"))
            self.freqFunctionBt.configure(text=_("FUNCTION\nPSD"))
            _sample_rate = self.origin_config.sensor_config["sample_rate"]
            canal_1 = self.origin_config.sensor_config["store_sensor_data"][0]  # Copy list by value not by reference
            canal_2 = self.origin_config.sensor_config["store_sensor_data"][1]
            canal_3 = self.origin_config.sensor_config["store_sensor_data"][2]
            win_var = self.origin_config.frequency_config_struct["Window"]
            unit = self.origin_config.frequency_config_struct["unit"]
            if (len(canal_1) != 0):
                Pd.PLT.plot_psd(self.frequencyFrameCanvas.canvas2, canal_1, canal_2, canal_3, _sample_rate,
                                self.origin_config.sensor_config["unit"][:3], [1, 2, 3], unit, win_var)

        except Exception as ex:
            print("Exception: ", ex)
    def on_velocity_spectrum_button_click(self):
        global grid_flag, plot_flag, track_flag
        track_flag=0
        plot_flag=1
        grid_flag = True
        try:
            self.freqGridtBt.configure(text=_("GRID ON"))
            self.freqFunctionBt.configure(text=_("FUNCTION\nVELOCITY\nSPECTRUM"))
            _sample_rate = self.origin_config.sensor_config["sample_rate"]
            canal_1 = self.origin_config.sensor_config["store_sensor_data"][0]  # Copy list by value not by reference
            canal_2 = self.origin_config.sensor_config["store_sensor_data"][1]
            canal_3 = self.origin_config.sensor_config["store_sensor_data"][2]
            if (len(canal_1) != 0):
                Pd.PLT.plot_velocity_spectrum(self.frequencyFrameCanvas.canvas2, canal_1, canal_2, canal_3, _sample_rate, [1, 2, 3])

        except Exception as ex:
            print("Exception: ", ex)

    def filterCallback(self):
        _sample_rate = self.origin_config.sensor_config["sample_rate"]
        canal_1 = self.origin_config.sensor_config["store_sensor_data"][0]  # Copy list by value not by reference
        canal_2 = self.origin_config.sensor_config["store_sensor_data"][1]
        canal_3 = self.origin_config.sensor_config["store_sensor_data"][2]
        filter_type = self.origin_config.frequency_config_struct["FilterType"]
        filter_from = self.origin_config.frequency_config_struct["FilterFrom"]  # high pass cutoff freq
        filter_to = self.origin_config.frequency_config_struct["FilterTo"]  # low pass cutoff freq
        window = self.origin_config.frequency_config_struct["Window"]
        if is_number(filter_from) == False or is_number(filter_to) == False:
            # self.inforLabel2.config(text=_("Filter value errors. Default cutoff frequency value is used."),
            #                         bg="lavender", fg="red", font="Verdana 13")
            filter_from = dfc._HIGHPASS_FROM
            filter_to = dfc._LOWPASS_TO
        else:
            filter_from = int(filter_from)
            filter_to = int(filter_to)
            if filter_from >= filter_to and filter_type == "BANDPASS":
                filter_from = dfc._HIGHPASS_FROM
                filter_to = dfc._LOWPASS_TO
                # self.inforLabel2.config(text=_("Filter bandpass frequency is wrong. Use the default value."),
                #                         bg="lavender", fg="red", font="Verdana 13")
            else:
                pass

        if filter_type:
            _samples_1 = filter_data(
                canal_1,
                filter_type,
                filter_from,
                filter_to,
                _sample_rate,
                window
            )
            _samples_2 = filter_data(
                canal_2,
                filter_type,
                filter_from,
                filter_to,
                _sample_rate,
                window
            )
            _samples_3 = filter_data(
                canal_3,
                filter_type,
                filter_from,
                filter_to,
                _sample_rate,
                window
            )
        n_samples = len(_samples_1)

        if (n_samples != 0):
            Pd.PLT.plot_fft(self.frequencyFrameCanvas.canvas2, _samples_1, _samples_2, _samples_3, _sample_rate,
                            self.origin_config.sensor_config["unit"][:3], [1, 2, 3], window)

    def on_read_sensor_button_clicked(self):
        global view_flag, plot_flag
        view_flag=0
        plot_flag=0
        self.laserBt.configure(text=_("LASER\nVIEW"))
        self.on_start_button_clicked(False)

    def on_refresh_button_clicked(self):
        global view_flag
        if view_flag==1:
            self.laserBt.configure(text=_("LASER\nVIEW"))
            view_flag=0
        Pd.PLT.plot_all_chanel(self.waveformFrameCanvas.canvas1,
                               self.origin_config.sensor_config["store_sensor_data"][0],
                               self.origin_config.sensor_config["store_sensor_data"][1],
                               self.origin_config.sensor_config["store_sensor_data"][2],
                               self.origin_config.sensor_config["unit"][:3],
                               self.origin_config.sensor_config["sample_rate"])

    def on_apply_button_clicked(self, from_config: bool):
        if from_config:
            self.config1.update_diagnostic_struct()
            self.applyBt.configure(state="disable")
            # self.configFrame.pack_forget()
            # self.on_waveform_button_clicked()

    def on_start_button_clicked(self, from_config: bool):
        """This button callback is responsed get the data from sensor and execute the waveform callback function"""
        global plot_flag, view_flag
        view_flag=0
        plot_flag=0
        self.laserBt.configure(text=_("LASER\nVIEW"))
        if from_config:
            self.config1.update_diagnostic_struct()
            # self.configFrame.pack_forget()
        self.read_sensor()
        self.on_waveform_button_clicked()
     
        Pd.PLT.plot_all_chanel(self.waveformFrameCanvas.canvas1,
                               self.origin_config.sensor_config["store_sensor_data"][0],
                               self.origin_config.sensor_config["store_sensor_data"][1],
                               self.origin_config.sensor_config["store_sensor_data"][2],
                               self.origin_config.sensor_config["unit"][:3],
                               self.origin_config.sensor_config["sample_rate"])
        Pd.PLT.plot_fft(self.frequencyFrameCanvas.canvas2, self.origin_config.sensor_config["store_sensor_data"][0],
                        self.origin_config.sensor_config["store_sensor_data"][1],
                        self.origin_config.sensor_config["store_sensor_data"][2],
                        self.origin_config.sensor_config["sample_rate"],
                        self.origin_config.sensor_config["unit"][:3],
                        [1, 2, 3], win_var="Hanning")


    def general_indicator_plot(self):
        try:
            vel_arr_data = []
            if len(self.origin_config.sensor_config["vel"]) > 0:

                for arr in self.origin_config.sensor_config["vel_data"]:
                    vel_arr_data.append(filter_data(arr, "BANDPASS", dfc._RMS_HIGHPASS_FROM, dfc._RMS_LOWPASS_TO,
                                                    self.origin_config.sensor_config["sample_rate"],
                                                    window="Hanning"))
                    # vel_arr_data.append(arr)
                """get the machine type, power, speed, foundation to specify the standard """
                machineType = self.origin_config.waveform_config_struct["MachineType"]
                congsuat = self.origin_config.waveform_config_struct["Power"]
                tocdo = self.origin_config.waveform_config_struct["Speed"]
                foundation = self.origin_config.waveform_config_struct["Foundation"]
                appliedStandard = iso10816_judge(machineType, tocdo, congsuat, foundation)
                Pd.PLT.plot_rms(self.generalFrameCanvas.canvas3, vel_arr_data, appliedStandard,
                                self.origin_config.sensor_config["vel"])

            else:
                Pd.PLT.clear_axes(self.generalFrameCanvas.canvas3, 2)
        except Exception as ex:
            print(ex)


        try:
            _sample_rate = self.origin_config.sensor_config["sample_rate"]
            if len(self.origin_config.sensor_config["accel"]) < 1:
                Pd.PLT.clear_axes(self.generalFrameCanvas.canvas3, 0)
                Pd.PLT.clear_axes(self.generalFrameCanvas.canvas3, 1)

            else:
                rpmVal = self.origin_config.waveform_config_struct["Speed"]
                bearing_dia = self.origin_config.waveform_config_struct["BearingBore"]
                filter_from = dfc._GE_HIGHPASS_FROM
                filter_to = dfc._GE_LOWPASS_TO
                hfcf_filter_from = dfc._HFCF_BANDPASS_FROM
                hfcf_filter_to = dfc._HFCF_BANDPASS_TO
                hfcf_arr = high_frequency_crest_factor(self.origin_config.sensor_config["accel_data"],
                                                       hfcf_filter_from, hfcf_filter_to,
                                                       [_sample_rate for _i in range(
                                                           len(self.origin_config.sensor_config["accel_data"]))],
                                                       window="Hanning")
                gE_data_arr = gE(self.origin_config.sensor_config["accel_data"], filter_from, filter_to,
                                 [_sample_rate for _i in
                                  range(len(self.origin_config.sensor_config["accel_data"]))], window="Hanning")
                Pd.PLT.plot_gE_severity(self.generalFrameCanvas.canvas3, gE_data_arr, hfcf_arr,
                                        self.origin_config.sensor_config["accel"], dfc._GE_FMAX,
                                        rpmVal, bearing_dia)
                self.side_band_energy_indicator()
        except Exception as ex:
            print(ex)
        try:
            if len(self.origin_config.sensor_config["dis"]) < 1:
                Pd.PLT.clear_axes(self.generalFrameCanvas.canvas3, 3)
            else:
                Pd.PLT.plot_displacement(self.generalFrameCanvas.canvas3,
                                         self.origin_config.sensor_config["displacement_data"],
                                         self.origin_config.sensor_config["dis"])
        except Exception as ex:
            print(ex)
    def on_config_button_clicked(self):
        global summary_flag
        if summary_flag==1:
            summary_flag=not summary_flag
        self.waveformPlotFrame.pack_forget()
        self.waveformSideButtonFrame.pack_forget()
        self.freqPlotFrame.pack_forget()
        self.freqSideButtonFrame.pack_forget()
        self.generalPlotFrame.pack_forget()
        self.generalSideButtonFrame.pack_forget()
        self.configFrame.pack(side=Tk.LEFT, fill=Tk.X, expand=1)
        self.summaryPlotFrame.pack_forget()
        self.waveformBt.configure(style="normal.TButton")
        self.frequencyBt.configure(style="normal.TButton")
        self.generalBt.configure(style="normal.TButton")
        self.configBt.configure(style="feature.Accent.TButton")

    def on_waveform_button_clicked(self):
        global summary_flag
        if summary_flag==1:
            summary_flag=not summary_flag
        self.waveformPlotFrame.pack(side=Tk.LEFT, fill=Tk.X, expand=1)
        self.waveformSideButtonFrame.pack(side=Tk.RIGHT, fill=Tk.X, expand=1)
        self.freqPlotFrame.pack_forget()
        self.freqSideButtonFrame.pack_forget()
        self.generalPlotFrame.pack_forget()
        self.generalSideButtonFrame.pack_forget()
        self.configFrame.pack_forget()
        self.summaryPlotFrame.pack_forget()
        self.waveformBt.configure(style="feature.Accent.TButton")
        self.frequencyBt.configure(style="normal.TButton")
        self.generalBt.configure(style="normal.TButton")
        self.configBt.configure(style="normal.TButton")

    def on_frequency_button_clicked(self):
        global summary_flag
        if summary_flag==1:
            summary_flag=not summary_flag
        self.waveformPlotFrame.pack_forget()
        self.waveformSideButtonFrame.pack_forget()
        self.freqPlotFrame.pack(side=Tk.LEFT, fill=Tk.X, expand=1)
        self.freqSideButtonFrame.pack(side=Tk.RIGHT, fill=Tk.X, expand=1)
        self.generalPlotFrame.pack_forget()
        self.generalSideButtonFrame.pack_forget()
        self.configFrame.pack_forget()
        self.summaryPlotFrame.pack_forget()
        self.waveformBt.configure(style="normal.TButton")
        self.frequencyBt.configure(style="feature.Accent.TButton")
        self.generalBt.configure(style="normal.TButton")
        self.configBt.configure(style="normal.TButton")

    def on_general_button_clicked(self):
        global summary_flag
        if summary_flag==1:
            summary_flag=not summary_flag
        self.waveformPlotFrame.pack_forget()
        self.waveformSideButtonFrame.pack_forget()
        self.freqPlotFrame.pack_forget()
        self.freqSideButtonFrame.pack_forget()
        self.generalPlotFrame.pack(side=Tk.LEFT, fill=Tk.X, expand=1)
        self.generalSideButtonFrame.pack(side=Tk.RIGHT, fill=Tk.X, expand=1)
        self.configFrame.pack_forget()
        self.summaryPlotFrame.pack_forget()
        self.general_indicator_plot()
        self.waveformBt.configure(style="normal.TButton")
        self.frequencyBt.configure(style="normal.TButton")
        self.generalBt.configure(style="feature.Accent.TButton")
        self.configBt.configure(style="normal.TButton")

    def on_summary_button_clicked(self):
        global summary_flag
        summary_flag=not summary_flag
        if summary_flag==1:
            self.waveformPlotFrame.pack_forget()
            self.waveformSideButtonFrame.pack_forget()
            self.freqPlotFrame.pack_forget()
            self.freqSideButtonFrame.pack_forget()
            self.generalPlotFrame.pack_forget()
            self.generalSideButtonFrame.pack(side=Tk.RIGHT, fill=Tk.X, expand=1)
            self.configFrame.pack_forget()
            self.summaryPlotFrame.pack(side=Tk.LEFT, fill=Tk.X, expand=1)
            self.waveformBt.configure(style="normal.TButton")
            self.frequencyBt.configure(style="normal.TButton")
            self.generalBt.configure(style="feature.Accent.TButton")
            self.configBt.configure(style="normal.TButton")
            try:
                # self.summaryFrameCanvas = SummaryFrameCanvas(self.summaryPlotFrame)
                self.summaryFrameCanvas.plot_summary(self.origin_config)
            except:
                pass
        else:
            self.generalPlotFrame.pack(side=Tk.LEFT, fill=Tk.X, expand=1)
            self.generalSideButtonFrame.pack(side=Tk.RIGHT, fill=Tk.X, expand=1)
            self.summaryPlotFrame.pack_forget()

    def side_band_energy_indicator(self):

        try:
            startFreq = []
            stopFreq = []
            rpm = self.origin_config.waveform_config_struct["Speed"] / 60
            SecondGMF = 2 * self.origin_config.waveform_config_struct["GearTeeth"] * rpm
            N=len(self.origin_config.sensor_config["accel"])
            if N > 0 and (SecondGMF - 3 * rpm - 5) > 0 and (
                    SecondGMF + 3 * rpm + 5) < (
                    self.origin_config.sensor_config["sample_rate"] / 2.56):
                for i in range(7):
                    startFreq.append(SecondGMF - (3 - i) * rpm - 5)
                    stopFreq.append(SecondGMF - (3 - i) * rpm + 5)
                CMFAmplitude = []
                for j in range(N):
                    [max1, freq] = tab4_tracking_signal_old(self.origin_config.sensor_config["accel_data"][j],
                                                        self.origin_config.sensor_config["sample_rate"],
                                                        [startFreq[3], stopFreq[3]])
                    CMFAmplitude.append(max1)
                sumOfSideBand = np.zeros(N)
                for k in range(N):
                    for h in range(7):
                        if h != 3:
                            [max1, freq] = tab4_tracking_signal_old(
                                self.origin_config.sensor_config["accel_data"][k],
                                self.origin_config.sensor_config["sample_rate"],
                                [startFreq[h], stopFreq[h]])
                            sumOfSideBand[k] += max1
                for k in range(N):
                    sumOfSideBand[k] /= CMFAmplitude[k]

                # Calculate the Acc Peak
                AccPeak = []
                for i in range(N):
                    arr = filter_data(
                        self.origin_config.sensor_config["accel_data"][i],
                        "HIGHPASS",
                        1000,
                        20000,
                        self.origin_config.sensor_config["sample_rate"],
                        window="Hanning"
                    )
                    AccRms = rmsValue(arr)
                    AccPeak.append(AccRms * 1.414)
                Pd.PLT.plot_SBR_severity(self.generalFrameCanvas.canvas3, sumOfSideBand, AccPeak,
                                         self.origin_config.sensor_config["accel"])

            else:
                pass
        except Exception as ex:
            print("Error", ex)

    def on_grid_button(self):
        global grid_flag
        try:
            if grid_flag == True:
                rpmVal = self.origin_config.frequency_config_struct["mesh"]
                Pd.PLT.plot_grid(self.frequencyFrameCanvas.canvas2, grid_flag, rpmVal)
                self.freqGridtBt.configure(text=_("GRID OFF"))
                grid_flag = False
            else:
                Pd.PLT.plot_grid(self.frequencyFrameCanvas.canvas2, grid_flag, 25)
                self.freqGridtBt.configure(text=_("GRID ON"))
                grid_flag = True
        except:
            pass

    def Tracking(self, dir: bool):
        global track_flag, plot_flag
        tracking_freq = self.origin_config.frequency_config_struct["TrackRange"]
        axes_arr = self.frequencyFrameCanvas.canvas2.figure.get_axes()
        if len(axes_arr) > 0:
            x1_data=axes_arr[0].get_lines()[-1].get_xdata()
            y1_data=axes_arr[0].get_lines()[-1].get_ydata()
            y2_data=axes_arr[1].get_lines()[-1].get_ydata()
            y3_data=axes_arr[2].get_lines()[-1].get_ydata()
            [xleft, xright] = axes_arr[0].get_xlim()
            if dir == True:
                if xleft >= track_flag:
                    track_flag = xleft
                if xright < track_flag:
                    return
                track_flag += tracking_freq
                start_freq = track_flag - tracking_freq
                stop_freq = track_flag
            else:
                if xright <= track_flag:
                    track_flag = xright

                track_flag -= tracking_freq
                if xleft >= track_flag:
                    track_flag = xleft
                if track_flag <= 0:
                    track_flag = 0
                start_freq = track_flag
                stop_freq = track_flag + tracking_freq
            try:
                if plot_flag==0:
                    [max1, max2, max3, phase_shift1, phase_shift2, phase_shift3, freq] = tracking_signal(
                        self.origin_config.sensor_config,
                        [start_freq,
                        stop_freq])

                    title = f'{str(freq)[:4]}' + 'hz |' + f'Ch1 {str(max1)[:5]} <{str(phase_shift1 * 180 / 3.14)[:3]}°> | Ch2 {str(max2)[:5]} <{str(phase_shift2 * 180 / 3.14)[:3]}°> | Ch3 {str(max3)[:5]} <{str(phase_shift3 * 180 / 3.14)[:3]}°>'
                    Pd.PLT.plot_grid_specific(self.frequencyFrameCanvas.canvas2, freq, title, True)
                else:
                    [max1, max2, max3, freq] = tracking_signal_no_phase_shift(
                        x1_data, y1_data, y2_data, y3_data,
                        [start_freq,
                        stop_freq])
                    if max1<0.001:
                        max1=0.000
                    if max2<0.01:
                        max2=0.000
                    if max3<0.01:
                        max3=0.000
                    title = f'{str(freq)[:4]}' + 'hz |' + f'Ch1 {str(max1)[:5]}  | Ch2 {str(max2)[:5]}  | Ch3 {str(max3)[:5]}'
                    Pd.PLT.plot_grid_specific(self.frequencyFrameCanvas.canvas2, freq, title, True)

            except:
                pass


class ConfigFrame(Tk.Frame):
    def __init__(self, parent: "self.configFrame", con):
        super().__init__(parent.configFrame, name="cai dat")
        self.con=con
        self.parent = parent
        self.origin_config=parent.origin_config
        imageAddress = ImageAdrr()
        self.smallSePhoto = imageAddress.smallSettingPhoto
        self.style = ttk.Style()
        self.style.configure('config.TLabel', font=('Chakra Petch', '13'))
        self.style.configure('config.TLabelframe', font=('Chakra Petch', '14'), bg='white', borderwidth=1)
        self.style.configure('config.TButton', font=('Chakra Petch', '15'))
        self.style.configure('config.TCombobox', font=('Chakra Petch', '15'))
        self.style.configure('config.Switch.TCheckbutton', font=('Chakra Petch', '13'))
        
        self.creat_config_frame()

    def creat_config_frame(self):
        self.wfParam1 = Tk.StringVar()
        self.wfParam2 = Tk.StringVar()
        self.wfParam3 = Tk.StringVar()
        self.wfParam4 = Tk.StringVar()
        self.wfParam5 = Tk.StringVar()
        self.wfParam6 = Tk.StringVar()
        self.wfParam7 = Tk.StringVar()
        self.wfParam8 = Tk.StringVar()
        self.wfParam9 = Tk.StringVar()
        self.wfParam10 = Tk.StringVar()
        self.wfParam11 = Tk.StringVar()
        self.wfParam12 = Tk.StringVar()
        self.wfParam13 = Tk.StringVar()
        self.wfParam14 = Tk.StringVar()
        self.wfParam15 = Tk.StringVar()
        self.wfParam16 = Tk.StringVar()
        self.wfParam17 = Tk.StringVar()
        self.wfParam18 = Tk.StringVar()

        self.tsa_check = Tk.IntVar()
        self.frqParam1 = Tk.StringVar()
        self.frqParam2 = Tk.StringVar()
        self.frqParam3 = Tk.StringVar()
        self.frqParam4 = Tk.StringVar()
        self.frqParam5 = Tk.StringVar()
        self.frqParam6 = Tk.StringVar()
        self.frqParam7 = Tk.StringVar()
        ##config default value

        self.wfParam1.set(self.origin_config.waveform_config_struct["Sensor1"])
        self.wfParam2.set(self.origin_config.waveform_config_struct["Sensor2"])
        self.wfParam3.set(self.origin_config.waveform_config_struct["Sensor3"])
        self.wfParam4.set(self.origin_config.waveform_config_struct["Sensor4"])
        self.wfParam5.set(self.origin_config.waveform_config_struct["KeyPhase"])
        self.tsa_check.set(self.origin_config.waveform_config_struct["UseTSA"])
        self.wfParam6.set(self.origin_config.waveform_config_struct["TSATimes"])
        self.wfParam7.set(self.origin_config.waveform_config_struct["Fmax"])
        self.wfParam8.set(self.origin_config.waveform_config_struct["num_fft_line"])
        self.wfParam9.set(self.origin_config.waveform_config_struct["MachineType"])
        self.wfParam10.set(self.origin_config.waveform_config_struct["Speed"])
        self.wfParam11.set(self.origin_config.waveform_config_struct["Power"])
        self.wfParam12.set(self.origin_config.waveform_config_struct["GearTeeth"])
        self.wfParam13.set(self.origin_config.waveform_config_struct["BearingBore"])
        self.wfParam14.set(self.origin_config.waveform_config_struct["MachineName"])
        self.wfParam15.set(self.origin_config.waveform_config_struct["Foundation"])
        self.wfParam16.set(self.origin_config.waveform_config_struct["Port1Pos"])
        self.wfParam17.set(self.origin_config.waveform_config_struct["Port2Pos"])
        self.wfParam18.set(self.origin_config.waveform_config_struct["Port3Pos"])

        self.frqParam1.set(self.origin_config.frequency_config_struct["FilterType"])
        self.frqParam2.set(self.origin_config.frequency_config_struct["Window"])
        self.frqParam3.set(self.origin_config.frequency_config_struct["FilterFrom"])
        self.frqParam4.set(self.origin_config.frequency_config_struct["FilterTo"])
        self.frqParam5.set(self.origin_config.frequency_config_struct["TrackRange"])
        self.frqParam6.set(self.origin_config.frequency_config_struct["mesh"])
        self.frqParam7.set(self.origin_config.frequency_config_struct["unit"])


        self.wfConfigFrame = Tk.LabelFrame(self, text='', font=('Chakra Petch', 13), border=0, \
                                           bg='white')
        self.wfConfigFrame.pack(side=Tk.TOP, fill=Tk.BOTH)

        sensorFrame = ttk.LabelFrame(self.wfConfigFrame, text=_('General config'), style='config.TLabelframe')
        sensorFrame.grid(column=0, row=0, padx=2, pady=0, ipadx=2, rowspan=10, columnspan=2, sticky='wn')

        # directionLabel = ttk.Label(sensorFrame, text=_('Type'), style='config.TLabel')
        # directionLabel.grid(column=1, row=0, padx=5, pady=5, sticky='w')

        # positionLabel = ttk.Label(sensorFrame, text=_('Position'), style='config.TLabel')
        # positionLabel.grid(column=2, row=0, padx=5, pady=5, sticky='e')
        machineType = ttk.Label(sensorFrame, text=_("Machine"), style='config.TLabel')
        machineType.grid(column=0, row=0, padx=5, pady=5, sticky='w')
        machineCombo = ttk.Combobox(sensorFrame, width=8, textvariable=self.wfParam9, state="readonly",
                                    font=('Chakra Petch', 13))
        machineCombo['value'] = ('GENERAL', "PUMP", "GEARBOX", "FAN", "CRITICAL MACHINE", 'STEAM TURBINE', "GAS TURBINE", "HYDRO TURBINE", "COMPRESSOR",
            "WIND TURBINE")
        machineCombo.grid(column=1, row=0, padx=0, pady=5, sticky="e")

        projectLabel = ttk.Label(sensorFrame, text=_("Project CFG"), style='config.TLabel')
        projectLabel.grid(column=2, row=0, padx=5, pady=3, sticky='w')

        prjButton=ttk.Button(sensorFrame, style="normal.TButton", image=self.smallSePhoto,\
                               command=self.creat_project_config_page)
        prjButton.grid(column=3, row=0, padx=0, pady=5, sticky='e')
#ss1
        sensor1Label = ttk.Label(sensorFrame, text=_('Port1'), style='config.TLabel')
        sensor1Label.grid(column=0, row=1, padx=5, pady=5, sticky='w')

        sensor1Combo = ttk.Combobox(sensorFrame, width=8, textvariable=self.wfParam1, state="readonly",
                                    font=('Chakra Petch', 13))
        sensor1Combo['value'] = ("Accelerometer", "Velocity Sensor")
        sensor1Combo.grid(column=1, row=1, padx=0, pady=5, sticky='e')

        self.port1PosCombo = ttk.Combobox(sensorFrame, width=4, textvariable=self.wfParam16, state="readonly",
                                    font=('Chakra Petch', 13))
        self.port1PosCombo['value']=('NONE')
        self.port1PosCombo.grid(column=2, row=1, padx=0, pady=5, sticky='e')

#ss2
        sensor2Label = ttk.Label(sensorFrame, text=_('Port2'), style='config.TLabel')
        sensor2Label.grid(column=0, row=2, padx=5, pady=5, sticky='w')

        sensor2Combo = ttk.Combobox(sensorFrame, width=8, textvariable=self.wfParam2, state="readonly",
                                    font=('Chakra Petch', 13))
        sensor2Combo['value'] = ("Accelerometer", "Velocity Sensor")
        sensor2Combo.grid(column=1, row=2, padx=0, pady=5, sticky='e')

        self.port2PosCombo = ttk.Combobox(sensorFrame, width=4, textvariable=self.wfParam17, state="readonly",
                                    font=('Chakra Petch', 13))
        self.port2PosCombo['value']=('NONE')
        self.port2PosCombo.grid(column=2, row=2, padx=0, pady=5, sticky='e')

        port2Button=ttk.Button(sensorFrame, style="normal.TButton", image=self.smallSePhoto,\
                               command=lambda: self.creat_sensor_position_page(self.origin_config.waveform_config_struct))
        port2Button.grid(column=3, row=2, padx=0, pady=5, sticky='e')

#ss3
        sensor3Label = ttk.Label(sensorFrame, text=_('Port3'), style='config.TLabel')
        sensor3Label.grid(column=0, row=3, padx=5, pady=5, sticky='w')

        sensor3Combo = ttk.Combobox(sensorFrame, width=8, textvariable=self.wfParam3, state="readonly",
                                    font=('Chakra Petch', 13))
        sensor3Combo['value'] = ("Accelerometer", "Velocity Sensor")
        sensor3Combo.grid(column=1, row=3, padx=0, pady=5, sticky='e')

        self.port3PosCombo = ttk.Combobox(sensorFrame, width=4, textvariable=self.wfParam18, state="readonly",
                                    font=('Chakra Petch', 13))
        self.port3PosCombo['value']=('NONE')
        self.port3PosCombo.grid(column=2, row=3, padx=0, pady=5, sticky='e')

        sensor4Label = ttk.Label(sensorFrame, text=_('Port4'), style='config.TLabel')
        sensor4Label.grid(column=0, row=4, padx=5, pady=5, sticky='w')

        sensor4Combo = ttk.Combobox(sensorFrame, width=8, textvariable=self.wfParam4, state="readonly",
                                    font=('Chakra Petch', 13))
        sensor4Combo['value'] = ('NONE', 'TACHOMETER')
        sensor4Combo.grid(column=1, row=4, padx=0, pady=5, sticky='e')

        keyLabel = ttk.Label(sensorFrame, text=_('Key sensor'), style='config.TLabel')
        keyLabel.grid(column=0, row=5, padx=5, pady=5, sticky="w")
        keyCombo = ttk.Combobox(sensorFrame, width=8, textvariable=self.wfParam5, state="readonly",
                                font=('Chakra Petch', 13))
        keyCombo['value'] = ('Sensor1', 'Sensor2', 'Sensor3')
        # keyCombo.current(0)
        keyCombo.grid(column=1, row=5, padx=0, pady=5, sticky="e")

        tsaCheckButton1 = ttk.Checkbutton(sensorFrame, text=_("  Use TSA"), offvalue=0, onvalue=1,
                                          variable=self.tsa_check, command=self.update_text_tsa,
                                          style="config.Switch.TCheckbutton")
        tsaCheckButton1.grid(column=1, row=6, padx=0, pady=5, sticky='w')

        tsaLabel = ttk.Label(sensorFrame, text=_("TSA times"), style='config.TLabel')
        tsaLabel.grid(column=0, row=7, padx=5, pady=5, sticky='w')
        self.tsaEntry = ttk.Entry(sensorFrame, width=10, textvariable=self.wfParam6,
                                  state="disable", font=('Chakra Petch', 13))
        self.tsaEntry.grid(column=1, row=7, padx=0, pady=5, ipadx=3, sticky='e')

        fftLineLabel = ttk.Label(sensorFrame, text=_("FFT lines"), style='config.TLabel')
        fftLineLabel.grid(column=0, row=8, padx=5, pady=5, sticky='w')
        fftLineCombo = ttk.Combobox(sensorFrame, width=8, textvariable=self.wfParam8, state="readonly", \
                                    font=('Chakra Petch', 13))
        fftLineCombo['value'] = ('1600','3200','6400','12800', '25600', '51200')
        fftLineCombo.grid(column=1, row=8, padx=0, pady=5, sticky="e")

        sampleRateLabel = ttk.Label(sensorFrame, text=_("Fmax (Hz)"), style='config.TLabel')
        sampleRateLabel.grid(column=0, row=9, padx=5, pady=5, sticky='w')
        sampleRateEntry = ttk.Entry(sensorFrame, width=10, textvariable=self.wfParam7, validate="key",
                                    font=('Chakra Petch', 13))
        sampleRateEntry['validatecommand'] = (sampleRateEntry.register(testVal), '%P', '%d')
        sampleRateEntry.grid(column=1, row=9, padx=0, pady=5, ipadx=3, sticky='e')
        ###
        frqConfigFrame = ttk.LabelFrame(self.wfConfigFrame, text=_('Filter configuration'), style='config.TLabelframe')
        frqConfigFrame.grid(column=2, row=0, padx=2, ipadx=2, pady=0, sticky='nw')

        filterLabel = ttk.Label(frqConfigFrame, text=_('Filter type'), style='config.TLabel')
        filterLabel.grid(column=0, row=0, padx=5, pady=5, sticky="w")

        filterCombo = ttk.Combobox(frqConfigFrame, width=8, textvariable=self.frqParam1, state="readonly",
                                   font=('Chakra Petch', 13))
        filterCombo['value'] = ('LOWPASS', 'HIGHPASS', 'BANDPASS')
        filterCombo.grid(column=1, row=0, padx=0, pady=5, sticky="e")

        windowLabel = ttk.Label(frqConfigFrame, text=_('Window type'), style='config.TLabel')
        windowLabel.grid(column=0, row=1, padx=5, pady=5, sticky="w")

        windowCombo = ttk.Combobox(frqConfigFrame, width=8, textvariable=self.frqParam2, state="readonly",
                                   font=('Chakra Petch', 13))
        windowCombo['value'] = ('Hanning', 'Blackman', 'Flatop')
        # sensor1Combo.current(0)
        windowCombo.grid(column=1, row=1, padx=0, pady=5, sticky="e")

        highpassFrqLabel = ttk.Label(frqConfigFrame, text=_("Filter From (Hz)"), style='config.TLabel')
        highpassFrqLabel.grid(column=0, row=2, padx=5, pady=5, sticky='w')
        highpassEntry = ttk.Entry(frqConfigFrame, width=10, textvariable=self.frqParam3, validate="key",
                                font=('Chakra Petch', 13))
        highpassEntry['validatecommand'] = (highpassEntry.register(testVal), '%P', '%d')
        highpassEntry.grid(column=1, row=2, padx=0, pady=5, ipadx=3, sticky='e')

        lowpassFrqLabel = ttk.Label(frqConfigFrame, text=_("Filter To (Hz)"), style='config.TLabel')
        lowpassFrqLabel.grid(column=0, row=3, padx=5, pady=5, sticky='w')
        lowpassEntry = ttk.Entry(frqConfigFrame, width=10, textvariable=self.frqParam4, validate="key",
                                font=('Chakra Petch', 13))
        lowpassEntry['validatecommand'] = (lowpassEntry.register(testVal), '%P', '%d')
        lowpassEntry.grid(column=1, row=3, padx=0, ipadx=3, pady=5, sticky='e')

        trackLabel = ttk.Label(frqConfigFrame, text=_("Tracking speed"), style='config.TLabel')
        trackLabel.grid(column=0, row=4, padx=5, pady=5, sticky='w')
        trackEntry = ttk.Entry(frqConfigFrame, width=10, textvariable=self.frqParam5, validate="key",
                                font=('Chakra Petch', 13))
        trackEntry['validatecommand'] = (trackEntry.register(testVal), '%P', '%d')
        trackEntry.grid(column=1, row=4, padx=0, pady=5, ipadx=3, sticky='e')

        meshLabel = ttk.Label(frqConfigFrame, text=_("Mesh grid"), style='config.TLabel')
        meshLabel.grid(column=0, row=5, padx=5, pady=5, sticky='w')
        meshEntry = ttk.Entry(frqConfigFrame, width=10, textvariable=self.frqParam6, validate="key",
                                font=('Chakra Petch', 13))
        meshEntry['validatecommand'] = (meshEntry.register(testVal), '%P', '%d')
        meshEntry.grid(column=1, row=5, padx=0, pady=5, ipadx=3, sticky='e')

        unitLabel = ttk.Label(frqConfigFrame, text=_('Unit show'), style='config.TLabel')
        unitLabel.grid(column=0, row=6, padx=5, pady=5, sticky="w")
        unitCombo = ttk.Combobox(frqConfigFrame, width=8, textvariable=self.frqParam7, state="readonly",
                                 font=('Chakra Petch', 13))
        unitCombo['value'] = ('Original', 'dB')
        unitCombo.grid(column=1, row=6, padx=0, pady=5, sticky="e")
        ###

        machineFrame = ttk.LabelFrame(self.wfConfigFrame, text=_('Machine configuration'), style="config.TLabelframe")
        machineFrame.grid(column=4, row=0, padx=2, pady=0, ipadx=2, sticky='ne')

        machineNameLabel = ttk.Label(machineFrame, text=_("Machine name"), style='config.TLabel')
        machineNameLabel.grid(column=0, row=0, padx=5, pady=5, sticky='w')
        machineNameEntry = ttk.Entry(machineFrame, width=10, textvariable=self.wfParam14,
                            font=('Chakra Petch', 13))
        machineNameEntry.grid(column=1, row=0, padx=0, pady=5, ipadx=3, sticky='e')

        speedLabel = ttk.Label(machineFrame, text=_("Speed (RPM)"), style='config.TLabel')
        speedLabel.grid(column=0, row=1, padx=5, pady=5, sticky='w')
        speedEntry = ttk.Entry(machineFrame, width=10, textvariable=self.wfParam10, validate="key",
                            font=('Chakra Petch', 13))
        speedEntry['validatecommand'] = (speedEntry.register(testVal), '%P', '%d')
        speedEntry.grid(column=1, row=1, padx=0, pady=5, ipadx=3, sticky='e')

        powerLabel = ttk.Label(machineFrame, text=_("Power (kW)"), style='config.TLabel')
        powerLabel.grid(column=0, row=2, padx=5, pady=5, sticky='w')
        powerEntry = ttk.Entry(machineFrame, width=10, textvariable=self.wfParam11, validate="key",
                            font=('Chakra Petch', 13))
        powerEntry['validatecommand'] = (powerEntry.register(testVal), '%P', '%d')
        powerEntry.grid(column=1, row=2, padx=0, pady=5, ipadx=3, sticky='e')

        TeethLabel = ttk.Label(machineFrame, text=_("Gear teeth"), style='config.TLabel')
        TeethLabel.grid(column=0, row=3, padx=5, pady=5, sticky='w')
        TeethEntry = ttk.Entry(machineFrame, width=10, textvariable=self.wfParam12, validate="key",
                            font=('Chakra Petch', 13))
        TeethEntry['validatecommand'] = (TeethEntry.register(testVal), '%P', '%d')
        TeethEntry.grid(column=1, row=3, padx=0, pady=5, ipadx=3, sticky='e')

        bearingBoreLabel = ttk.Label(machineFrame, text=_("Brgs bore(mm)"), style='config.TLabel')
        bearingBoreLabel.grid(column=0, row=4, padx=5, pady=5, sticky='w')
        bearingBoreEntry = ttk.Entry(machineFrame, width=10, textvariable=self.wfParam13, validate="key",
                            font=('Chakra Petch', 13))
        bearingBoreEntry['validatecommand'] = (bearingBoreEntry.register(testVal), '%P', '%d')
        bearingBoreEntry.grid(column=1, row=4, padx=0, pady=5, ipadx=3, sticky='e')

        foundationType = ttk.Label(machineFrame, text=_("Foundation"), style='config.TLabel')
        foundationType.grid(column=0, row=5, padx=5, pady=5, sticky='w')
        foundationCombo = ttk.Combobox(machineFrame, width=8, textvariable=self.wfParam15, state="readonly",
                                       font=('Chakra Petch', 13))
        foundationCombo['value'] = ('Rigid', "Flexible")
        foundationCombo.grid(column=1, row=5, padx=0, pady=5, sticky="e")

        # self.nextBt = ttk.Button(self.parent, text="START", style='Accent.TButton',
        #                          command=lambda: self.on_start_button_clicked(True, origin_config))
        # self.nextBt.place(relx=0.8, rely=0.89, width=167, height=48)

    def update_text_tsa(self):
        txt = self.tsa_check.get()
        if txt == 1:
            self.tsaEntry.configure(state='normal')
        else:
            self.tsaEntry.configure(state='disabled')

    def update_diagnostic_struct(self):

        self.origin_config.waveform_config_struct["Sensor1"] = self.wfParam1.get()
        self.origin_config.waveform_config_struct["Sensor2"] = self.wfParam2.get()
        self.origin_config.waveform_config_struct["Sensor3"] = self.wfParam3.get()
        self.origin_config.waveform_config_struct["Sensor4"] = self.wfParam4.get()
        self.origin_config.waveform_config_struct["Port1Pos"] = self.wfParam16.get()
        self.origin_config.waveform_config_struct["Port2Pos"] = self.wfParam17.get()
        self.origin_config.waveform_config_struct["Port3Pos"] = self.wfParam18.get()
        self.origin_config.waveform_config_struct["KeyPhase"] = self.wfParam5.get()
        self.origin_config.waveform_config_struct["UseTSA"] = self.tsa_check.get()
        self.origin_config.waveform_config_struct["MachineType"] = self.wfParam9.get()
        self.origin_config.waveform_config_struct["num_fft_line"] = int(self.wfParam8.get())
        self.origin_config.waveform_config_struct["MachineName"] = self.wfParam14.get().replace("/", "_")
        self.origin_config.waveform_config_struct["Foundation"] = self.wfParam15.get()

        self.origin_config.frequency_config_struct["FilterType"] = self.frqParam1.get()
        self.origin_config.frequency_config_struct["Window"] = self.frqParam2.get()
        if self.frqParam3.get()!='':
            self.origin_config.frequency_config_struct["FilterFrom"] = int(self.frqParam3.get())
        if self.frqParam4.get() != '':
            self.origin_config.frequency_config_struct["FilterTo"] = int(self.frqParam4.get())
        if self.frqParam5.get() != '':
            self.origin_config.frequency_config_struct["TrackRange"] = int(self.frqParam5.get())
        if self.frqParam6.get() != '':
            self.origin_config.frequency_config_struct["mesh"] = int(self.frqParam6.get())
        self.origin_config.frequency_config_struct["unit"] = self.frqParam7.get()

        tempFmax = self.wfParam7.get()
        tempTsaTimes = self.wfParam6.get()
        tempSpeed = self.wfParam10.get()
        tempPower = self.wfParam11.get()
        tempTeeth = self.wfParam12.get()
        tempBore = self.wfParam13.get()


        if self.origin_config.waveform_config_struct["Sensor4"] == "NONE":
            if int(tempFmax) <= 15000:
                self.origin_config.waveform_config_struct["Fmax"] = int(tempFmax)
            else:
                self.origin_config.waveform_config_struct["Fmax"] = 15000
        else:
            if int(tempFmax) <= 11000:
                self.origin_config.waveform_config_struct["Fmax"] = int(tempFmax)
            else:
                self.origin_config.waveform_config_struct["Fmax"] = 11000
        if self.origin_config.waveform_config_struct["Fmax"] < 1000:
            self.origin_config.waveform_config_struct["Fmax"] = 1000
        if int(tempTsaTimes) < 30:
            self.origin_config.waveform_config_struct["TSATimes"] = int(tempTsaTimes)
        else:
            self.origin_config.waveform_config_struct["TSATimes"] = 30

        if tempSpeed!='':
            self.origin_config.waveform_config_struct["Speed"] = int(tempSpeed)
        if tempPower != '':
            self.origin_config.waveform_config_struct["Power"] = int(tempPower)
        if tempTeeth != '':
            self.origin_config.waveform_config_struct["GearTeeth"] = int(tempTeeth)
        if tempBore != '':
            self.origin_config.waveform_config_struct["BearingBore"] = int(tempBore)

    def creat_sensor_position_page(self, waveform_config_struct):
        machineType=self.wfParam9.get()
        SensorPositionCanvas1=SensorPositionCanvas(self, waveform_config_struct, machineType)
        SensorPositionCanvas1.place(x=0, y=0, width=1008, height=504)

    def creat_project_config_page(self):
        projectConfigCanvas1=GeneralConfig(self, self.origin_config, self.con)
        projectConfigCanvas1.place(x=0, y=0, width=1008, height=504)

class GeneralConfig(Tk.Canvas):
    def __init__(self, parent, origin_config, db_connect):
        super().__init__(parent.parent.configFrame, width=1008, height=504, bg="white")
        self.con=db_connect
        self.parent=parent
        self.style = ttk.Style()
        self.style.configure('gen.TLabel', font=('Chakra Petch', 14))
        self.style.configure('gen.TLabelframe', font=('Chakra Petch', 10))
        self.style.configure('gen.TButton', font=('Chakra Petch', 15), width=40, height=40)
        self.creat_genral_config_page(origin_config)

    def creat_genral_config_page(self, origin_config):
        self.prjParam1 = Tk.StringVar()
        self.prjParam2 = Tk.StringVar()
        self.prjParam3 = Tk.StringVar()
        self.prjParam1.set(origin_config.project_struct["ProjectCode"])
        self.prjParam2.set(origin_config.project_struct["CompanyName"])
        self.prjParam3.set(origin_config.project_struct["Date"])

        projectFrame = ttk.LabelFrame(self, text=_('Project config'))
        projectFrame.pack(side="left", fill='y')

        prjCodeLabel = ttk.Label(projectFrame, text=_('Project Code*'), style='gen.TLabel')
        prjCodeLabel.grid(column=0, row=0, padx=10, pady=5, sticky='w')

        prjCodeEntry = ttk.Entry(projectFrame, width=20, textvariable=self.prjParam1, takefocus=False,
                                font=('Chakra Petch', 14))
        # prjCodeEntry['validatecommand'] = (prjCodeEntry.register(testVal), '%P', '%d')
        prjCodeEntry.grid(column=1, row=0, padx=10, pady=5, sticky='e')

        companyLabel = ttk.Label(projectFrame, text=_('Company Name'), style='gen.TLabel')
        companyLabel.grid(column=0, row=1, padx=10, pady=5, sticky='w')

        companyEntry = ttk.Entry(projectFrame, width=20, textvariable=self.prjParam2, takefocus=False,
                                font=('Chakra Petch', 14))
        companyEntry.grid(column=1, row=1, padx=10, pady=5, sticky='e')

        noteLabel = ttk.Label(projectFrame, text=_('Date'), style='gen.TLabel')
        noteLabel.grid(column=0, row=2, padx=10, pady=5, sticky='w')

        self.noteEntry = ttk.Entry(projectFrame, width=20, textvariable=self.prjParam3, takefocus=False,
                                font=('Chakra Petch', 14))
        self.noteEntry.grid(column=1, row=2, padx=10, pady=5, sticky='e')

        self.getTimeButton = ttk.Button(projectFrame, text=_("Get time now"), style="Accent.TButton",
                                      command=self.on_get_time_now_button_clicked)
        self.getTimeButton.grid(column=2, row=2, padx=10, pady=20, sticky='ew')

        self.applyButton = ttk.Button(projectFrame, text=_("APPLY"), style="Accent.TButton",
                                      command=lambda: self.on_apply_button_clicked(origin_config))
        self.applyButton.grid(column=1, row=3, padx=10, pady=20, ipady=5, sticky='ew')

        self.cancelButton = ttk.Button(projectFrame, text=_("CANCEL"), style="Accent.TButton",
                                      command=self.on_cancel_button_clicked)
        self.cancelButton.grid(column=0, row=3, padx=10, pady=20, ipady=5, sticky='ew')

        self.scrollbar = ttk.Scrollbar(self)
        self.scrollbar.pack(side="right", fill="y")

        self.PrjTable = ttk.Treeview(self, yscrollcommand=self.scrollbar.set, show=("tree",), style="Custom.Treeview")
        self.PrjTable.bind('<<TreeviewSelect>>', self.get_selected_cell)

        self.PrjTable.pack(side="left", expand=True, fill="both")
        self.PrjTable['columns'] = ('PrjID', 'machine')
        self.PrjTable.column("#0", anchor='w', width=100)
        self.PrjTable.column("PrjID",anchor='w', width=100)
        self.PrjTable.column("machine",anchor='w', width=120)

        self.PrjTable.heading("#0",text="",anchor=Tk.CENTER)
        self.PrjTable.heading("PrjID",text="ID",anchor=Tk.CENTER)
        self.PrjTable.heading("machine",text="ID",anchor=Tk.CENTER)
        self.scrollbar.config(command=self.PrjTable.yview)
        prjCodeArr=self.load_all_project_code()
        for i in range(len(prjCodeArr)):
            companyName=self.find_company_name_base_on_code(prjCodeArr[i])
            machineName=self.load_machine_name_by_code(prjCodeArr[i])
            
            self.PrjTable.insert(parent='', index='end', iid=i, text=prjCodeArr[i], values=(str(companyName), str(machineName)))


    def load_all_project_code(self):
        with self.con:
            cur=self.con.cursor()
            cur.execute(f"SELECT DISTINCT CODE FROM DATA ORDER BY DATE ASC;")
            load_data = cur.fetchall()
            load_data_arr = [i for i in load_data]
            return [arr[0] for arr in load_data_arr]
    
    def find_company_name_base_on_code(self, prjCode):
        with self.con:
            cur=self.con.cursor()
            cur.execute(f"SELECT COM_ID FROM Project_ID WHERE CODE=?", (prjCode,))
            load_data=cur.fetchall()
            com_id=load_data[0][0]
            cur.execute(f"SELECT NAME FROM Company_ID WHERE COM_ID =?", (com_id,))
            name=cur.fetchall()
            return name[0][0]

    def load_machine_name_by_code(self, prjCode):
        with self.con:
            cur=self.con.cursor()
            cur.execute(f"SELECT NOTE FROM Project_ID WHERE CODE =?", (prjCode,))
            machineName=cur.fetchall()
            return machineName[0][0]
    
    def get_selected_cell(self, event):
        self.applyButton.configure(state='normal') 
        try:
            selected_item = self.PrjTable.focus() # get the selected item
            prjID = self.PrjTable.item(selected_item)['text']
            self.prjParam1.set(prjID)
            companyName=self.PrjTable.item(selected_item)['values'][0]
            self.prjParam2.set(companyName)
        except:
            pass
    
    def on_apply_button_clicked(self, origin_config):
        
        tempPrjCode=self.prjParam1.get()
        tempCompanyName=self.prjParam2.get()
        tempDate=self.prjParam3.get()
        prjCodeArr=self.load_all_project_code()
        if tempPrjCode!='' and tempCompanyName!='':
            if validate_time(tempDate)==True:
                if prjCodeArr.count(tempPrjCode)==0:
                    origin_config.project_struct["ProjectCode"] = tempPrjCode.replace("/", "-")
                    origin_config.project_struct["CompanyName"] = tempCompanyName.replace("/", "-")
                    
                    origin_config.project_struct["Date"] = tempDate
                    self.parent.port1PosCombo["value"]=("NONE")
                    self.parent.port2PosCombo["value"]=("NONE")
                    self.parent.port3PosCombo["value"]=("NONE")
                    self.applyButton.configure(state="disable")
                    self.destroy()
                else:
                    if pms.general_warning(_("The project code is existed, do you want to measure again ?")):
                        origin_config.project_struct["ProjectCode"] = tempPrjCode.replace("/", "-")
                        origin_config.project_struct["CompanyName"] = tempCompanyName.replace("/", "-")
                        origin_config.project_struct["Date"] = tempDate

                        with self.con:
                            cur=self.con.cursor()
                            cur.execute(f"SELECT DATA, POS, Sample_rate FROM DATA WHERE CODE = ? ORDER BY DATE DESC", (origin_config.project_struct["ProjectCode"],))
                            load_data = cur.fetchall()
                            cur.execute(f"SELECT POWER, RPM, DRIVEN, BEARINGBORE, GEARTOOTH, FOUNDATION, NOTE FROM Project_ID WHERE CODE = ?", (origin_config.project_struct["ProjectCode"],))
                            machineParam = cur.fetchall()
                            load_data_arr = [i for i in load_data] #mang cac chuoi data, date [data,date,sample_rate; data, date, sample_rate]
                            machine_param_arr = [i for i in machineParam]
                            if len(load_data_arr)!=0:
                                fftLine=int((len(file_operation.extract_str(load_data_arr[0][0]))+1400)/2.56)
                                Fmax=int(load_data_arr[0][2]/2.56)
                                posList=[]
                                for i in range(len(load_data)):
                                    posList.append(load_data_arr[i][1])
                                new_list = []
                                [new_list.append(item) for item in posList if item not in new_list]
                                new_pos_arr=[item[:2] for item in new_list]
                                new_pos_arr.insert(0, "NONE")
                                for ari in machine_param_arr:
                                    try:
                                        power=int(ari[0])
                                    except:
                                        power=1
                                    try:
                                        rpm=int(ari[1])
                                    except :
                                        rpm=1500 
                                    
                                    try:
                                        bearing_bore=int(ari[3])
                                    except:
                                        bearing_bore=50 

                                    try:
                                        gear_tooth=int(ari[4])
                                    except :
                                        gear_tooth=0 
                                    driven=ari[2]
                                    foundation=ari[5]
                                    note=ari[6]

                                self.parent.wfParam8.set(fftLine)
                                self.parent.wfParam7.set(Fmax)
                                self.parent.wfParam10.set(rpm)
                                self.parent.wfParam11.set(power)
                                self.parent.wfParam12.set(gear_tooth)
                                self.parent.wfParam13.set(bearing_bore)
                                self.parent.wfParam15.set(foundation)
                                self.parent.wfParam14.set(note)
                                self.parent.wfParam9.set(driven)
                                self.parent.port1PosCombo["value"]=tuple(new_pos_arr)
                                self.parent.port2PosCombo["value"]=tuple(new_pos_arr)
                                self.parent.port3PosCombo["value"]=tuple(new_pos_arr)
                                
                        self.applyButton.configure(state="disable")
                        self.destroy()
                    else: 
                        return
            else:
                pms.general_warning(_("Date format is wrong"))
                return
        else:
            pms.general_warning(_("The project code and company name may not be empty"))
            return
    
    def on_cancel_button_clicked(self):
        self.destroy()

    def on_get_time_now_button_clicked(self):
        text=get_time_now()
        self.prjParam3.set(text)
        self.applyButton.configure(state="normal")


class SensorPositionCanvas(Tk.Canvas):
    def __init__(self, parent, waveform_config_struct, machineType):
        super().__init__(parent.parent.configFrame, width=1008, height=504, bg='white')
        self.parent = parent
        self.waveform_config_struct=waveform_config_struct
        self.newstyle = ttk.Style()
        self.newstyle.configure('pos0.TButton', font=('Chakra Petch', 7), borderwidth=1, justify=Tk.CENTER)
        self.newstyle.configure('pos1.Accent.TButton', font=('Chakra Petch', 10), justify=Tk.CENTER)
        self.newstyle.configure('pos2.Accent.TButton', font=('Chakra Petch', 7), justify=Tk.CENTER)
        self.newstyle.configure('feature.Accent.TButton', font=('Chakra Petch', 15), borderwidth=1, justify=Tk.CENTER)
        self.newstyle.configure('normal.TLabel', font=('Chakra Petch', 13), background='white')
        self.newstyle.configure('red.TLabel', font=('Chakra Petch', 13), background='white', foreground='#C40069')
        self.sensorPositionConfig(machineType)
    
    def sensorPositionConfig(self, machineType):
        self.inputParam1 = Tk.StringVar()
        self.inputParam2 = Tk.StringVar()
        self.inputParam3 = Tk.StringVar()
        self.inputParam4 = Tk.StringVar()

        self.inputParam2.set(self.waveform_config_struct["Port1Pos"])
        self.inputParam3.set(self.waveform_config_struct["Port2Pos"])
        self.inputParam4.set(self.waveform_config_struct["Port3Pos"])
        parentFrame = Tk.LabelFrame(self, text='', font=('Chakra Petch', 13), border=0, bg='white')
        parentFrame.pack(side=Tk.TOP, fill=Tk.BOTH)
        
        imageFrame = ttk.LabelFrame(parentFrame, text=(''))
        imageFrame.grid(column=0, row=0, padx=0, pady=0, sticky='wn')
        inputFrame = ttk.LabelFrame(parentFrame, text=_('Input'))
        inputFrame.grid(column=1, row=0, padx=0, pady=0, sticky='wn')
        
        imageAdress=ImageAdrr()
        if machineType=="PUMP":
            image = imageAdress.pumpPhoto
            x=[56,   56, 183, 183, 222, 390, 384, 353, 588, 595, 223, 223 ]
            y=[230, 328, 230, 328, 298, 293, 330, 355, 293, 327, 414, 458 ]
            dir=["AV", "AH", "BV", "BH", "BA", "CV", "CH", "CA", "DV", "DH", "EV", "FV"]
        elif machineType=="GENERAL" or machineType=="CRITICAL MACHINE" or machineType=="FAN":
            image = imageAdress.fanPhoto
            x=[66,   66, 204, 204, 253, 316, 316, 282, 587, 587, 528, 528]
            y=[228, 337, 228, 336, 362, 284, 337, 362, 284, 337, 420, 461 ]
            dir=["AV", "AH", "BV", "BH", "BA", "CV", "CH", "CA", "DV", "DH", "EV", "FV"]
        elif machineType=="WIND TURBINE":
            image = imageAdress.windPhoto
            x=[195, 253, 318, 412, 434, 419, 500, 510, 478, 590, 591]
            y=[240, 244, 169, 120, 173, 317, 122, 186, 173, 122, 184 ]
            dir=["AV", "BV", "CV", "DV", "DA", "EV", "FV", "FH", "FA", "GV", "GH"]
        elif machineType=="GEARBOX":
            image = imageAdress.gearboxPhoto
            x=[63 , 63 , 126, 129, 158, 428, 429, 407, 463, 513, 538, 219, 219]
            y=[271, 332, 272, 332, 317, 280, 332, 317, 245, 245, 219, 394, 439 ]
            dir=["AV", "AH", "BV", "BH", "BA", "CV", "CH", "CA", "DV", "DH", "DA", "EV", "FV"]
        else:
            image = imageAdress.pumpPhoto
            x=[56,   56, 183, 183, 222, 390, 384, 353, 588, 595, 223, 223 ]
            y=[230, 328, 230, 328, 298, 293, 330, 355, 293, 327, 414, 458 ]
            dir=["AV", "AH", "BV", "BH", "BA", "CV", "CH", "CA", "DV", "DH", "EV", "FV"]
        px = 1/plt.rcParams['figure.dpi']
        self.fig5 = Figure(figsize=(666*px, 475*px))
        self.ax_41 = self.fig5.add_subplot()
        self.ax_41.set_position([0.01, 0.01, 1, 1])
        self.ax_41.set_xticks([])
        self.ax_41.set_yticks([])
        self.ax_41.imshow(image)
        self.ax_41.axis('off')
        self.canvas4 = FigureCanvasTkAgg(self.fig5, master=imageFrame)
        self.canvas4.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)
        
        self.listBt=[]
        for i in range(15):
            self.listBt.append(Tk.Button())

        for i in range(len(x)):
            self.listBt[i]=Tk.Button(self, text='O', bg="green2", command=lambda text=dir[i], index=i: self.update_text(text, index))
            self.listBt[i].place(x=x[i], y=y[i], width=25, height=25)

        pos1Label= ttk.Label(inputFrame, text=_("Port 1"), style="pos0.TLabel")
        pos1Label.grid(column=0, row=0, padx=5, pady=0, sticky="w")
        self.port1Entry=ttk.Entry(inputFrame, width=10, textvariable=self.inputParam2, validate="key", font=('Chakra Petch', 13))
        self.port1Entry.grid(column=1, row=0, padx=5, pady=5, sticky='e')

        pos2Label= ttk.Label(inputFrame, text=_("Port 2"), style="pos0.TLabel")
        pos2Label.grid(column=0, row=1, padx=5, pady=0, sticky="w")
        self.port2Entry=ttk.Entry(inputFrame, width=10, textvariable=self.inputParam3, validate="key", font=('Chakra Petch', 13))
        self.port2Entry.grid(column=1, row=1, padx=5, pady=5, sticky='e')

        pos3Label= ttk.Label(inputFrame, text=_("Port 3"), style="pos0.TLabel")
        pos3Label.grid(column=0, row=2, padx=5, pady=0, sticky="w")
        self.port3Entry=ttk.Entry(inputFrame, width=10, textvariable=self.inputParam4, validate="key", font=('Chakra Petch', 13))
        self.port3Entry.grid(column=1, row=2, padx=5, pady=5, sticky='e')

        sensorLabel=ttk.Label(inputFrame, text=_("Select port"), style="pos0.TLabel")
        sensorLabel.grid(column=0, row=3, padx=5, pady=0, sticky="w")
        self.sensorCombo=ttk.Combobox(inputFrame, width=8, textvariable=self.inputParam1, validate="key", font=('Chakra Petch', 13),\
                                 state="readonly" )
        self.sensorCombo['value'] = ('Port1', 'Port2', 'Port3')
        self.sensorCombo.current(0)
        self.sensorCombo.bind("<<ComboboxSelected>>", self.sensor_combo_callback)  
        self.sensorCombo.grid(column=1, row=3, padx=5, pady=5, sticky='e')

        applyButton=ttk.Button(self, text=_('APPLY'), style="Accent.TButton", command=self.on_apply_button_click)
        applyButton.place(x=860, y=456, width=130, height=40)

    def update_text(self, text, index):
        global SensorPosition
        SensorPosition=text
        self.sensorCombo.event_generate('<Button-1>', x=1, y=1)
        # selectedSensor=self.inputParam1.get()
        self.listBt[index].configure(text="S", bg="#C40069")
        for i in range(len(self.listBt)):
            if i!=index:
                self.listBt[i].configure(text="O", bg="green2")
        # if selectedSensor=="Port1":
        #     self.inputParam2.set(text)
        # elif selectedSensor=="Port2":
        #     self.inputParam3.set(text)
        # else:
        #     self.inputParam4.set(text)
    def sensor_combo_callback(self, event):
        global SensorPosition
        text=self.inputParam1.get()
        if text=="Port1":
            self.inputParam2.set(SensorPosition)
        elif text=="Port2":
            self.inputParam3.set(SensorPosition)
        else:
            self.inputParam4.set(SensorPosition)
        if text=="Port1":
            self.port1Entry.configure(state="normal")
            self.port2Entry.configure(state="disable")
            self.port3Entry.configure(state="disable")
        elif text=="Port2":
            self.port1Entry.configure(state="disable")
            self.port2Entry.configure(state="normal")
            self.port3Entry.configure(state="disable")
        elif text=="Port3":
            self.port2Entry.configure(state="disable")
            self.port1Entry.configure(state="disable")
            self.port3Entry.configure(state="normal")

    def on_apply_button_click(self):
        port1Pos=self.inputParam2.get()
        port2Pos=self.inputParam3.get()
        port3Pos=self.inputParam4.get()
        if port1Pos=='':
            port1Pos="NONE"
        if port2Pos=='':
            port2Pos="NONE"
        if port3Pos=='':
            port3Pos="NONE"
        self.waveform_config_struct["Port1Pos"]=port1Pos
        self.waveform_config_struct["Port2Pos"]=port2Pos
        self.waveform_config_struct["Port3Pos"]=port3Pos
        self.parent.wfParam16.set(port1Pos)
        self.parent.wfParam17.set(port2Pos)
        self.parent.wfParam18.set(port3Pos)
        self.destroy()


class WaveformFrameCanvas():
    def __init__(self, parent: "waveformPlotFrame"):
        self.parent = parent
        self.creat_waveform_canvas()

    def creat_waveform_canvas(self):
        fig1 = creatFig.creatFigure(self.parent, 3)
        fig1.set_visible(True)
        self.canvas1 = FigureCanvasTkAgg(fig1, master=self.parent)
        self.canvas1.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)


class FrequencyFrameCanvas():
    def __init__(self, parent: "freqPlotFrame"):
        self.parent = parent
        self.creat_frequency_canvas()

    def creat_frequency_canvas(self):
        fig2 = creatFig.creatFigure(self.parent, 3)
        fig2.set_visible(True)
        self.canvas2 = FigureCanvasTkAgg(fig2, master=self.parent)
        self.canvas2.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)


class GeneralFrameCanvas():
    def __init__(self, parent: "generalPlotFrame"):
        self.parent = parent
        self.creat_general_canvas()

    def creat_general_canvas(self):
        fig3 = Figure(figsize=(8.1, 8))
        ax_31 = fig3.add_subplot(2, 2, 1)
        ax_31.set_facecolor("lavender")
        ax_31.set_position([0.08, 0.55, 0.4, 0.42])
        ax_31.set_ylabel('gE/HFCF for bearing')
        ax_31.grid()
        ax_31.set_visible(True)

        ax_32 = fig3.add_subplot(2, 2, 2)
        ax_32.set_facecolor("lavender")
        ax_32.set_position([0.57, 0.55, 0.42, 0.42])  # góc dưới trái, trên phải, theo thử tự x,y
        ax_32.set_ylabel('Sideband ratio/ Acc-Peak Gearbox')
        ax_32.set_visible(True)

        ax_33 = fig3.add_subplot(2, 2, 3)
        ax_33.set_facecolor("lavender")
        ax_33.set_position([0.08, 0.07, 0.4, 0.41])
        ax_33.set_ylabel('Standard ISO-10816 (mm/s)')
        ax_33.set_visible(True)

        ax_34 = fig3.add_subplot(2, 2, 4)
        ax_34.set_facecolor("lavender")
        ax_34.set_position([0.57, 0.08, 0.42, 0.41])
        ax_34.set_ylabel('ISO-10816 Displacement (um)')
        ax_34.set_visible(True)
        fig3.set_visible(True)
        self.canvas3 = FigureCanvasTkAgg(fig3, master=self.parent)
        self.canvas3.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)

class SummaryFrameCanvas():
    def __init__(self, parent: "summaryPlotFrame"):
        self.parent = parent
        self.creat_summary_canvas()
    def creat_summary_canvas(self):
        self.detailFrame = Tk.LabelFrame(self.parent, bg='white')
        self.detailFrame.pack(side=Tk.TOP, fill=Tk.BOTH)
        self.myTable = ttk.Treeview(self.detailFrame, height=3)
        self.myTable.grid(column=0, row=0, padx=(5, 5), pady=5, sticky='e')
        self.myTable['columns'] = ('Channel', 'A-Peak', 'A-PkPk', 'A-RMS', 'V-Peak', 'V-PkPk', 'V-RMS', 'D-Peak', 'D-PkPk', 'D-RMS', 'Crest', 'Kutorsis')
        self.myTable.column("#0", width=0,  stretch=Tk.NO)
        self.myTable.column("Channel", anchor=Tk.CENTER, width=80)
        self.myTable.column("A-Peak", anchor=Tk.CENTER, width=73)
        self.myTable.column("A-PkPk", anchor=Tk.CENTER, width=73)
        self.myTable.column("A-RMS", anchor=Tk.CENTER, width=73)
        self.myTable.column("V-Peak", anchor=Tk.CENTER, width=73)
        self.myTable.column("V-PkPk", anchor=Tk.CENTER, width=73)
        self.myTable.column("V-RMS", anchor=Tk.CENTER, width=73)
        self.myTable.column("D-Peak", anchor=Tk.CENTER, width=73)
        self.myTable.column("D-PkPk", anchor=Tk.CENTER, width=73)
        self.myTable.column("D-RMS", anchor=Tk.CENTER, width=73)
        self.myTable.column("Crest", anchor=Tk.CENTER, width=73)
        self.myTable.column("Kutorsis", anchor=Tk.CENTER, width=78)
    
        self.myTable.heading("#0",text="",anchor=Tk.CENTER)
        self.myTable.heading("Channel",text="Channel",anchor=Tk.CENTER)
        self.myTable.heading("A-Peak",text="A-Peak",anchor=Tk.CENTER)
        self.myTable.heading("A-PkPk",text="A-PkPk",anchor=Tk.CENTER)
        self.myTable.heading("A-RMS",text="A-RMS",anchor=Tk.CENTER)
        self.myTable.heading("V-Peak",text="V-Peak",anchor=Tk.CENTER)
        self.myTable.heading("V-PkPk",text="V-PkPk",anchor=Tk.CENTER)
        self.myTable.heading("V-RMS",text="V-RMS",anchor=Tk.CENTER)
        self.myTable.heading("D-Peak",text="D-Peak",anchor=Tk.CENTER)
        self.myTable.heading("D-PkPk",text="D-PkPk",anchor=Tk.CENTER)
        self.myTable.heading("D-RMS",text="D-RMS",anchor=Tk.CENTER)
        self.myTable.heading("Crest",text="Crest",anchor=Tk.CENTER)
        self.myTable.heading("Kutorsis",text="Kutorsis",anchor=Tk.CENTER)

        self.graphFrame = Tk.LabelFrame(self.parent, bg='white', borderwidth=0)
        self.graphFrame.pack(side=Tk.TOP, fill=Tk.BOTH)
        self.fig4 = Figure(figsize=(9.8,3.6))
        self.ax_41 = self.fig4.add_subplot(1,2,1)
        self.ax_41.set_position([0.01, 0.01, 0.48, 0.95])
        self.ax_41.set_xticks([])
        self.ax_41.set_yticks([])

        self.ax_42 = self.fig4.add_subplot(1,2,2)
        self.ax_42.set_position([0.5, 0.01, 0.48, 0.95])
        self.ax_42.set_xticks([])
        self.ax_42.set_yticks([])

        self.fig4.set_visible(True)
        self.canvas4 = FigureCanvasTkAgg(self.fig4, master=self.graphFrame)
        self.canvas4.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)

    def plot_summary(self, origin_config):
        imageAdress=ImageAdrr()
        for row in self.myTable.get_children():
            self.myTable.delete(row)
        for i in range(3):
            try:
                a_index = origin_config.sensor_config["accel"].index(i)
                # Apeak = max(np.abs(origin_config.sensor_config["accel_data"][a_index]))
                # APp = np.ptp(origin_config.sensor_config["accel_data"][a_index])
                Arms = rmsValue(origin_config.sensor_config["accel_data"][a_index])
                Apeak=np.sqrt(2)*Arms
                APp=2*Apeak
                Acrest = Apeak / Arms
                Akutor = kurtosis(origin_config.sensor_config["accel_data"][a_index])
            except:
                a_index = -1
                Apeak = "None "
                APp = "None "
                Arms = "None "
                Acrest = "None "
                Akutor = "None "
            try:
                v_index = origin_config.sensor_config["vel"].index(i)
                filtered_data = filter_data(origin_config.sensor_config["vel_data"][v_index], "BANDPASS",
                                            dfc._RMS_HIGHPASS_FROM,
                                            dfc._RMS_LOWPASS_TO, origin_config.sensor_config["sample_rate"],
                                            window="Hanning")
                # Vpeak = max(np.abs(filtered_data))
                # VPp = np.ptp(filtered_data)
                Vrms = rmsValue(filtered_data)
                Vpeak=np.sqrt(2)*Vrms
                VPp=2*Vpeak
                # Vcrest = Vpeak / Vrms
                # Vkutor = kurtosis(filtered_data)
            except:
                v_index = -1
                Vpeak = "None "
                VPp = "None "
                Vrms = "None "
                # Vcrest = "None "
                # Vkutor = "None "
            try:
                d_index = origin_config.sensor_config["dis"].index(i)
                # Dpeak = max(np.abs(origin_config.sensor_config["displacement_data"][d_index]))
                # DPp = np.ptp(origin_config.sensor_config["displacement_data"][d_index])
                Drms = rmsValue(origin_config.sensor_config["displacement_data"][d_index])
                Dpeak=np.sqrt(2)*Drms
                DPp=2*Dpeak
                # Dcrest = Dpeak / Drms
                # Dkutor = kurtosis(origin_config.sensor_config["displacement_data"][d_index])
            except:
                d_index = -1
                Dpeak = "None "
                DPp = "None "
                Drms = "None "
                # Dcrest = "None "
                # Dkutor = "None "
                
            self.myTable.insert(parent='', index='end', iid=i, text='', values=("Channel " + str(i+1), str(Apeak)[:5], str(APp)[0:5], str(Arms)[0:5],\
                                                                                str(Vpeak)[0:5], str(VPp)[0:5], str(Vrms)[0:5],\
                                                                                str(Dpeak)[0:5], str(DPp)[0:5], str(Drms)[0:5], str(Acrest)[0:5], str(Akutor)[0:5]))

        if origin_config.waveform_config_struct["MachineType"] == "GENERAL":
            image = imageAdress.iso1Photo
            image1 = imageAdress.gePhoto
        elif origin_config.waveform_config_struct["MachineType"] == "STEAM TURBINE":
            image = imageAdress.iso2vPhoto
            image1 = imageAdress.iso2dPhoto
        elif origin_config.waveform_config_struct["MachineType"] == "CRITICAL MACHINE":
            image = imageAdress.iso3vPhoto
            image1 = imageAdress.iso3dPhoto
        elif origin_config.waveform_config_struct["MachineType"] == "GAS TURBINE":
            image = imageAdress.iso4Photo
            image1 = imageAdress.iso4Photo
        elif origin_config.waveform_config_struct["MachineType"] == "HYDRO TURBINE":
            image = imageAdress.iso5vPhoto
            image1 = imageAdress.iso5dPhoto
        elif origin_config.waveform_config_struct["MachineType"] == "PUMP":
            image = imageAdress.iso7Photo
            image1 = imageAdress.iso7Photo
        elif origin_config.waveform_config_struct["MachineType"] == "COMPRESSOR":
            image = imageAdress.iso8hPhoto
            image1 = imageAdress.iso8vPhoto
        elif origin_config.waveform_config_struct["MachineType"] == "WIND TURBINE":
            image = imageAdress.iso21Photo
            image1 = imageAdress.iso21Photo

        ax_41, ax_42 = self.fig4.get_axes()
        ax_41.clear()
        ax_41.imshow(image)
        ax_41.axis('off')
        ax_41.set_visible(True)

        ax_42.clear()
        ax_42.imshow(image1)
        ax_42.axis('off')
        ax_42.set_visible(True)
        self.canvas4.draw()