import tkinter as Tk
# import sv_ttk
from tkinter import ttk
import matplotlib
import matplotlib.pyplot as plt
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
import pms.popMessage as pms
balancingOrder=0
click_stop_flag=False
def testVal(inStr, acttyp):
    if acttyp == '1':  # insert
        if not inStr.isdigit():
            return False
    return True

class Balancing(Tk.Frame):
    def __init__(self, parent: "Application"):
        self.parent = parent
        now = datetime.now()
        self.current_time = now.strftime("%H:%M")
        imageAddress = ImageAdrr()
        self.homePhoto = imageAddress.homePhoto
        self.low_bat = imageAddress.low_bat
        self.half_bat = imageAddress.half_bat
        self.full_bat = imageAddress.full_bat
        self.arrowPhoto = imageAddress.arrowPhoto
        self.lock = Lock()
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
        self.featureFrame.pack(side=Tk.TOP, fill=Tk.X, expand=1)
        self.featureFrame.pack_propagate(0)

        self.batFrame = Tk.Frame(self.featureFrame, bd=1, bg='grey95', width=117, height=35)
        self.batFrame.pack()
        self.batFrame.place(relx=0.89, rely=0.0)
        self.batFrame.pack_propagate(0)

        self.creat_setting_feature_panel()
        self.balancingConfigFrame = BalancingConfig(self.mainFrame, self.infoLabel2, self.parent.origin_config.balancing_config_struct)
        self.balancingConfigFrame.pack(side=Tk.TOP, fill=Tk.X, expand=1)
        self.balancingConfigFrame.pack_propagate(0)

        self.balancingAnalysisFrame = BalancingAnalysis(self.mainFrame, self.infoLabel2, self.parent.origin_config.balancing_config_struct, self.lock)
        self.balancingAnalysisFrame.pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)
        self.balancingAnalysisFrame.pack_propagate(0)
        self.balancingAnalysisFrame.pack_forget()

        self.parent.bind_class('TEntry', "<FocusIn>", self.show_key_board)
        self.parent.bind_class('TCombobox', "<<ComboboxSelected>>", self.change_state)

    def show_key_board(self, event):
        self.balancingConfigFrame.balancingApplyButton.configure(state='normal')
        self.widget = self.get_focus_widget()
        self.keyboardFrame = KeyBoard(self.widget)
        parentName = event.widget.winfo_parent()
        self.parent1 = event.widget._nametowidget(parentName)
        self.parent1.focus()

    def get_focus_widget(self):
        widget = self.parent.focus_get()
        return widget

    def change_state(self, event):
        self.balancingConfigFrame.balancingApplyButton.configure(state="normal")

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

        self.configBt = ttk.Button(self.featureFrame, style='Accent.TButton', text="Config",
                                    command=self.on_config_button_clicked)
        self.configBt.place(relx=0.122, rely=0.018, width=115, height=72)

        self.arrowLabel = ttk.Label(self.featureFrame, style='normal.TLabel', image=self.arrowPhoto)
        self.arrowLabel.place(relx=0.237, rely=0.25)
        self.arrowLabel.image = self.arrowPhoto
        
        self.analysisBt = ttk.Button(self.featureFrame, style='normal.TButton', text="Balancing",
                                   command=self.on_analysis_button_clicked)
        self.analysisBt.place(relx=0.265, rely=0.018, width=115, height=72)

        self.infoFrame= Tk.Frame(self.featureFrame, width=451, height=72, bg='white', bd=0)
        self.infoFrame.place(relx=0.41, rely=0.018)

        self.infoLabel1=ttk.Label(self.infoFrame, text="Information", style="red.TLabel")
        self.infoLabel1.grid(column=0, row=0, padx=0, pady=5, sticky='w')

        self.infoLabel2 = ttk.Label(self.infoFrame, text="Click RUN to start.", style="normal.TLabel", width=42)
        self.infoLabel2.grid(column=0, row=1, padx=0, pady=5, sticky='w')

    def on_analysis_button_clicked(self):
        self.balancingConfigFrame.pack_forget()
        self.balancingAnalysisFrame.pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)
        self.configBt.configure(style="normal.TButton")
        self.analysisBt.configure(style="Accent.TButton")

    def on_config_button_clicked(self):
        self.balancingConfigFrame.pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)
        self.balancingAnalysisFrame.pack_forget()
        self.configBt.configure(style="Accent.TButton")
        self.analysisBt.configure(style="normal.TButton")

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

class BalancingConfig(Tk.Frame):
    def __init__(self, parent, infoLabel, balancing_config_struct):
        super().__init__(parent, width=1024, height=520, background='white')
        self.parent=parent
        self.infoLabel=infoLabel
        self.style = ttk.Style()
        self.style.configure('balancing.TLabel', font=('Chakra Petch', 13), bg='white')
        self.style.configure('balancing.TLabelframe', font=('Chakra Petch', 15), bg='white', borderwidth=0)
        self.style.configure('balancing.TButton', font=('Chakra Petch', 15))
        self.style.configure('balancing.TEntry', font=('Chakra Petch', 15))
        self.creatConfig(balancing_config_struct)
    def creatConfig(self, balancing_config_struct):
        self.balParam1=Tk.StringVar()
        self.balParam2=Tk.StringVar()
        self.balParam3=Tk.StringVar()
        self.balParam4=Tk.StringVar()
        self.balParam5=Tk.StringVar()
        self.balParam6=Tk.StringVar()
        self.balParam7=Tk.StringVar()
        self.balParam8=Tk.StringVar()
        self.balParam9=Tk.StringVar()
        self.balParam10=Tk.StringVar()
        self.balParam11=Tk.StringVar()
        self.balParam12=Tk.StringVar()
        self.balParam13=Tk.StringVar()
        self.balParam14=Tk.StringVar()
        self.balParam15=Tk.StringVar()
        self.balParam16=Tk.StringVar()
        self.balParam17=Tk.StringVar()
        self.balParam18=Tk.StringVar()
        self.balParam19=Tk.StringVar()
        self.balParam20=Tk.StringVar()
        self.balParam21=Tk.StringVar()
        self.balParam22=Tk.StringVar()

        # self.balParam1.set(balancing_config_struct["roto_type"])
        self.balParam2.set(balancing_config_struct["num_planes"])
        self.balParam3.set(balancing_config_struct["num_sensors"])
        self.balParam4.set(balancing_config_struct["num_blades"])
        self.balParam5.set(balancing_config_struct["trial_mass1"])
        self.balParam6.set(balancing_config_struct["trial_mass2"])
        self.balParam7.set(balancing_config_struct["direction"])
        self.balParam8.set(balancing_config_struct["num_fft_line"])
        self.balParam9.set(balancing_config_struct["sample_rate"])
        self.balParam10.set(balancing_config_struct["sensor_type"])
        self.balParam11.set(balancing_config_struct["sensor1"])
        self.balParam12.set(balancing_config_struct["sensor2"])
        self.balParam13.set(balancing_config_struct["angle1"])
        self.balParam14.set(balancing_config_struct["angle2"])


        BalancingFrame = ttk.LabelFrame(self, text=_('Configuration'), style='balancing.TLabelframe')
        BalancingFrame.pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)

        numOfPlane = ttk.Label(BalancingFrame, text=_('Num of planes'), style='balancing.TLabel')
        numOfPlane.grid(column=0, row=1, padx=5, pady=5, sticky="w")
        numPlaneCombo=ttk.Combobox(BalancingFrame, width=10, textvariable=self.balParam2, state="readonly", font=('Chakra Petch', 13))
        numPlaneCombo['value'] = ('One','Two')
        numPlaneCombo.grid(column=1, row=1, padx=0, pady=5, sticky="w")
        # self.numPlaneCombo.current(0)

        numOfSensors = ttk.Label(BalancingFrame, text=_('Num of sensors'), style='balancing.TLabel')
        numOfSensors.grid(column=0, row=2, padx=5, pady=5, sticky="w")
        numSensorCombo=ttk.Combobox(BalancingFrame, width=10, textvariable=self.balParam3, state="readonly", font=('Chakra Petch', 13))
        numSensorCombo['value'] = ('One','Two')
        numSensorCombo.grid(column=1, row=2, padx=0, pady=5, sticky="w")
        # self.numSensorCombo.current(0)

        sensorType = ttk.Label(BalancingFrame, text=_('Sensor type'), style='balancing.TLabel')
        sensorType.grid(column=0, row=3, padx=5, pady=5, sticky="w")
        sensorTypeCombo=ttk.Combobox(BalancingFrame, width=10, textvariable=self.balParam10, state="readonly", font=('Chakra Petch', 13))
        sensorTypeCombo['value'] = ('Velocity','Acceleration')
        sensorTypeCombo.grid(column=1, row=3, padx=0, pady=5, sticky="w")
        # self.sensorTypeCombo.current(0)

        sensor1Lable = ttk.Label(BalancingFrame, text=_('Sensor1'), style='balancing.TLabel')
        sensor1Lable.grid(column=0, row=4, padx=5, pady=5, sticky="w")
        sensor1Combo=ttk.Combobox(BalancingFrame, width=10, textvariable=self.balParam11, state="readonly", font=('Chakra Petch', 13))
        sensor1Combo['value'] = ('Port1','Port2','Port3')
        sensor1Combo.grid(column=1, row=4, padx=0, pady=5, sticky="w")
        # self.sensor1Combo.current(1)

        sensor2Lable = ttk.Label(BalancingFrame, text=_('Sensor2'), style='balancing.TLabel')
        sensor2Lable.grid(column=0, row=5, padx=5, pady=5, sticky="w")
        sensor2Combo=ttk.Combobox(BalancingFrame, width=10, textvariable=self.balParam12, state="readonly", font=('Chakra Petch', 13))
        sensor2Combo['value'] = ('Port1','Port2','Port3')
        sensor2Combo.grid(column=1, row=5, padx=0, pady=5, sticky="w")
        # self.sensor2Combo.current(1)

        mass1Label = ttk.Label(BalancingFrame, text=_("Trial mass 1 (g)"), style='balancing.TLabel')
        mass1Label.grid(column=0, row=6, padx=5, pady=5, sticky="w")
        mass1Entry = ttk.Entry(BalancingFrame, width=14, textvariable=self.balParam5, style="balancing.TEntry",
                                validate="key")
        mass1Entry['validatecommand'] = (mass1Entry.register(testVal), '%P', '%d')
        mass1Entry.grid(column=1, row=6, padx=0, pady=5, sticky="w")

        mass2Label = ttk.Label(BalancingFrame, text=_("Trial mass 2 (g)"), style='balancing.TLabel')
        mass2Label.grid(column=0, row=7, padx=5, pady=5, sticky="w")
        mass2Entry = ttk.Entry(BalancingFrame, width=14, textvariable=self.balParam6, style="balancing.TEntry",
                                validate="key")
        mass2Entry['validatecommand'] = (mass2Entry.register(testVal), '%P', '%d')
        mass2Entry.grid(column=1, row=7, padx=0, pady=5, sticky="w")

        mass1AngelLabel = ttk.Label(BalancingFrame, text=_("Angle 1 (deg)"), style='balancing.TLabel')
        mass1AngelLabel.grid(column=2, row=6, padx=5, pady=5, sticky="w")
        mass1AngleEntry = ttk.Entry(BalancingFrame, width=14, textvariable=self.balParam13, style="balancing.TEntry",
                                validate="key")
        mass1AngleEntry['validatecommand'] = (mass1AngleEntry.register(testVal), '%P', '%d')
        mass1AngleEntry.grid(column=3, row=6, padx=0, pady=5, sticky="w")

        mass2AngelLabel = ttk.Label(BalancingFrame, text=_("Angle 2 (deg)"), style='balancing.TLabel')
        mass2AngelLabel.grid(column=2, row=7, padx=5, pady=5, sticky="w")
        mass2AngleEntry = ttk.Entry(BalancingFrame, width=14, textvariable=self.balParam14, style="balancing.TEntry",
                                validate="key")
        mass2AngleEntry['validatecommand'] = (mass2AngleEntry.register(testVal), '%P', '%d')
        mass2AngleEntry.grid(column=3, row=7, padx=0, pady=5, sticky="w")


        direction = ttk.Label(BalancingFrame, text=_("Rotating dir"), style='balancing.TLabel')
        direction.grid(column=2, row=1, padx=5, pady=5, sticky="w")
        dirCombo=ttk.Combobox(BalancingFrame, width=10, textvariable=self.balParam7, state="readonly", font=('Chakra Petch', 13))
        dirCombo['value'] = ('Clockwise','Counter-Clockwise')
        dirCombo.grid(column=3, row=1, padx=0, pady=5, sticky="w")
        # self.dirCombo.current(0)

        fftLine = ttk.Label(BalancingFrame, text=_('FFT lines'), style='balancing.TLabel')
        fftLine.grid(column=2, row=2, padx=5, pady=5, sticky="w")
        numLineCombo=ttk.Combobox(BalancingFrame, width=10, textvariable=self.balParam8, state="readonly", font=('Chakra Petch', 13))
        numLineCombo['value'] = ('1000','1200','1500','2000','4000','8000','16000')
        numLineCombo.grid(column=3, row=2, padx=0, pady=5, sticky="w")
        # self.numLineCombo.current(2)
        
        balancingSampleRate = ttk.Label(BalancingFrame, text=_("Sample rate"), style='balancing.TLabel')
        balancingSampleRate.grid(column=2, row=3, padx=5, pady=5, sticky="w")
        SampleRateEntry = ttk.Entry(BalancingFrame, width=14, textvariable=self.balParam9, style="balancing.TEntry",
                                    validate="key")
        SampleRateEntry['validatecommand'] = (SampleRateEntry.register(testVal), '%P', '%d')
        SampleRateEntry.grid(column=3, row=3, padx=0, pady=5, sticky="w")

        numOfBlades = ttk.Label(BalancingFrame, text=_('Num of blades'), style='balancing.TLabel')
        numOfBlades.grid(column=2, row=4, padx=5, pady=5, sticky="w")
        numBladeEntry = ttk.Entry(BalancingFrame, width=14, textvariable=self.balParam4, style="balancing.TEntry",
                                    validate="key")
        numBladeEntry['validatecommand'] = (numBladeEntry.register(testVal), '%P', '%d')
        numBladeEntry.grid(column=3, row=4, padx=0, pady=5, sticky="w")

        corr_weight_devide = ttk.Label(BalancingFrame, text=_("CW split"), style='balancing.TLabel')
        corr_weight_devide.grid(column=2, row=8, padx=5, pady=5, sticky="w")
        corr_weight_1 = ttk.Label(BalancingFrame, text="CW1", style='balancing.TLabel')
        corr_weight_1.grid(column=2, row=9, padx=5, pady=5, sticky="w")
        corr_weight_2 = ttk.Label(BalancingFrame, text="CW2", style='balancing.TLabel')
        corr_weight_2.grid(column=2, row=10, padx=5, pady=5, sticky="w")

        # self.CW1Entry = ttk.Entry(BalancingFrame, width=14, textvariable=self.balParam15, bg='white', font="Verdana 16")
        # self.CW1Entry.grid(column=3, row=10, padx=0, pady=5, sticky="w")
        # self.CW2Entry = ttk.Entry(BalancingFrame, width=14, textvariable=self.balParam16, bg='white', font="Verdana 16")
        # self.CW2Entry.grid(column=3, row=11, padx=0, pady=5, sticky="w")

        CW1ChangeAngle1Entry = ttk.Entry(BalancingFrame, width=14, textvariable=self.balParam15, state="readonly", style="balancing.TEntry")
        CW1ChangeAngle1Entry.grid(column=3, row=8, padx=0, pady=5, sticky="w")
        CW1ChangeAngle2Entry = ttk.Entry(BalancingFrame, width=14, textvariable=self.balParam16, state="readonly", style="balancing.TEntry")
        CW1ChangeAngle2Entry.grid(column=4, row=8, padx=0, pady=5, sticky="w")

        CW2ChangeAngle1Entry = ttk.Entry(BalancingFrame, width=14, textvariable=self.balParam17, state="readonly", style="balancing.TEntry")
        CW2ChangeAngle1Entry.grid(column=5, row=8, padx=0, pady=5, sticky="w")
        CW2ChangeAngle2Entry = ttk.Entry(BalancingFrame, width=14, textvariable=self.balParam18, state="readonly", style="balancing.TEntry")
        CW2ChangeAngle2Entry.grid(column=6, row=8, padx=0, pady=5, sticky="w")

        CW1Mass1Entry = ttk.Entry(BalancingFrame, width=14, textvariable=self.balParam19, state="readonly", style="balancing.TEntry")
        CW1Mass1Entry.grid(column=3, row=9, padx=0, pady=5, sticky="w")
        CW1Mass2Entry = ttk.Entry(BalancingFrame, width=14, textvariable=self.balParam20, state="readonly", style="balancing.TEntry")
        CW1Mass2Entry.grid(column=4, row=9, padx=0, pady=5, sticky="w")

        CW2Mass1Entry = ttk.Entry(BalancingFrame, width=14, textvariable=self.balParam21, state="readonly", style="balancing.TEntry")
        CW2Mass1Entry.grid(column=5, row=10, padx=0, pady=5, sticky="w")
        CW2Mass2Entry = ttk.Entry(BalancingFrame, width=14, textvariable=self.balParam22, state="readonly", style="balancing.TEntry")
        CW2Mass2Entry.grid(column=6, row=10, padx=0, pady=5, sticky="w")

        self.balancingApplyButton = ttk.Button(BalancingFrame, text=_("Apply"), style="Accent.TButton",
                                    command=lambda:self.update_config_struct(balancing_config_struct))
        self.balancingApplyButton.grid(column=4, row=11, padx=0, pady=5, ipadx=35, ipady=5, sticky='w')

        self.CWDevideButton = ttk.Button(BalancingFrame, text=_("Calulate"), style="Accent.TButton")
        self.CWDevideButton.grid(column=6, row=11, padx=0, pady=5, ipadx=30, ipady=5, sticky='w')


    def update_config_struct(self, balancing_config_struct):
        self.balancingApplyButton.configure(state='disable')
        balancing_config_struct["num_planes"]=self.balParam2.get()
        balancing_config_struct["num_sensors"]=self.balParam3.get()
        balancing_config_struct["direction"]=self.balParam7.get()
        balancing_config_struct["num_fft_line"]=int(self.balParam8.get())
        balancing_config_struct["sensor_type"]=self.balParam10.get()
        balancing_config_struct["sensor1"]=self.balParam11.get()
        balancing_config_struct["sensor2"]=self.balParam12.get()

        tempBlades=self.balParam4.get()
        tempMass1=self.balParam5.get()
        tempMass2=self.balParam6.get()
        tempSampleRate=self.balParam9.get()
        tempAngle1=int(self.balParam13.get())
        tempAngle2=int(self.balParam14.get())
        if balancing_config_struct["num_planes"]=="One":
            if is_number(tempBlades)==False or is_number(tempMass1)==False or is_number(tempSampleRate)==False or is_number(tempAngle1)==False:
                self.infoLabel.config(text=_("Parameter errors. Check the input type."))
                return
            else:
                balancing_config_struct["num_blades"]=int(tempBlades)
                balancing_config_struct["trial_mass1"]=float(tempMass1)
                balancing_config_struct["trial_mass2"]=float(tempMass2)
                if int(tempSampleRate)<=5000:
                    balancing_config_struct["sample_rate"]=int(tempSampleRate)
                else:
                    balancing_config_struct["sample_rate"]=5000
                balancing_config_struct["angle1"] = int(tempAngle1)
                self.infoLabel.config(text=_("OK"))
        else:
            if is_number(tempBlades)==False or is_number(tempMass1)==False or is_number(tempMass2)==False or is_number(tempSampleRate)==False\
             or is_number(tempAngle1)==False or is_number(tempAngle2)==False:
                self.infoLabel.config(text=_("Parameter errors. Check the input type."))
                return
            else:
                balancing_config_struct["num_blades"]=int(tempBlades)
                balancing_config_struct["trial_mass1"]=float(tempMass1)
                balancing_config_struct["trial_mass2"]=float(tempMass2)
                balancing_config_struct["sample_rate"]=int(tempSampleRate)
                balancing_config_struct["angle1"] = int(tempAngle1)
                balancing_config_struct["angle2"] = int(tempAngle2)
                self.infoLabel.config(text=_("OK")) 


class BalancingAnalysis(Tk.Frame):
    def __init__(self, parent:"mainFrame", infoLabel, balancing_config_struct, lock):
        super().__init__(parent, width=1008 , height=504 , bg='white')
        self.parent = parent
        self.balancing_config_struct = balancing_config_struct
        self.lock = lock
        ad7609.init()
        self.infoLabel = infoLabel
        self.balancing_analysis_page()
    def balancing_analysis_page(self):
        self.balancingPlotFrame = BalancingPlotCanvas(self)
        self.balancingPlotFrame.pack(side=Tk.LEFT, fill=Tk.BOTH, expand=1)
        self.balancingPlotFrame.pack_propagate(0)

        self.balancingSideFrame = SideButtonFrame(self, self.balancing_config_struct, self.infoLabel, self.lock,
                                                 self.balancingPlotFrame.canvas5)
        self.balancingSideFrame.pack(side=Tk.RIGHT, fill=Tk.Y, expand=1)
        self.balancingSideFrame.pack_propagate(0)

class SideButtonFrame(Tk.Frame):
    def __init__(self, parent, balancing_config_struct, infoLabel, lock, canvas):
        super().__init__(parent, bd=1, bg='white', width=90, height=504)
        self.parent=parent
        self.balancing_config_struct=balancing_config_struct
        self.infoLabel=infoLabel
        self.lock = lock
        self.canvas=canvas
        self.style = ttk.Style()
        self.style.configure('custom.TLabel', font=('Chakra Petch', 13), bg='white')
        self.style.configure('red.TLabel', font=('Chakra Petch', 13), bg='white', foreground='red')
        self.style.configure('custom.TLabelframe', font=('Chakra Petch', 15), bg='white', borderwidth=0)
        self.style.configure('custom.TButton', font=('Chakra Petch', 15))
        imageAddress = ImageAdrr()
        self.ZoomCanvas = Tk.Canvas()
        self.factorCanvas = Tk.Canvas()
        self.zoomPhoto = imageAddress.zoomPhoto
        self.savePhoto = imageAddress.savePhoto
        self.zoomIn = imageAddress.zoomIn
        self.zoomOut = imageAddress.zoomOut
        self.panLeft = imageAddress.panLeft
        self.panRight = imageAddress.panRight
        self.function1 = imageAddress.fuction1
        self.creat_button()

    def creat_button(self):
        self.functionBt = ttk.Button(self, style='custom.Accent.TButton', text="START\nINITIAL\nRUN",
                                compound=Tk.TOP, command=self.balancing_button)
        self.functionBt.place(x=0, y=425, width=88, height=75)

        self.resetBt = ttk.Button(self, style='custom.Accent.TButton', text="RESET",
                                compound=Tk.TOP, command=self.reset_balancing)
        self.resetBt.place(x=0, y=348, width=88, height=75)


    def change_state(self):
        global click_stop_flag
        click_stop_flag= not click_stop_flag

    def stop_button(self):
        self.change_state()

    def reset_balancing(self):
        global balancingOrder, click_stop_flag
        click_stop_flag=False
        balancingOrder=0
        self.balancing_config_struct["run"]=[]
        self.balancing_config_struct["trim_run"]=[]
        Pd.PLT.clear_polar(self.canvas)
        self.functionBt.configure(state="normal", text=_("START\nINITIAL\nRUN"))
        self.infoLabel.config(text="")

    def balancing_button(self):
        global balancingOrder
        balancingOrder+=1
        # print("order=",balancingOrder)
        if self.balancing_config_struct["num_planes"]=="One":
            if balancingOrder==1:
                _balancingLabel="Initial"
                self.functionBt.configure(text=_("STOP"))
                self.functionBt.update_idletasks()
                self.resetBt.configure(state="disable")
                self.resetBt.update_idletasks()
                self.infoLabel.config(text= _("Wait until phase and amplitude is stable and click STOP"))
                self.infoLabel.update_idletasks()
            if balancingOrder==2:
                self.change_state()
                self.functionBt.configure(text=_("TRIAL\nRUN"))
                self.functionBt.update_idletasks()
                self.resetBt.configure(state="normal")
                self.resetBt.update_idletasks()
                self.infoLabel.config(text= _("Next step: Execute the trial run"))
                self.infoLabel.update_idletasks()
            if balancingOrder==3:
                _balancingLabel="Trial"
                self.functionBt.configure(text=_("STOP"))
                self.functionBt.update_idletasks()
                self.resetBt.configure(state="disable")
                self.resetBt.update_idletasks()
                self.infoLabel.config(text= _("Wait until phase and amplitude is stable and click STOP"))
                self.infoLabel.update_idletasks()
            if balancingOrder==4:
                self.change_state()
                self.functionBt.configure(text=_("TRIM 1\nRUN"))
                self.functionBt.update_idletasks()
                self.resetBt.configure(state="normal")
                self.resetBt.update_idletasks()
                self.infoLabel.config(text= _("Next step: Execute the first trim run"))
                self.infoLabel.update_idletasks()
            if balancingOrder==5:
                _balancingLabel="Trim1"
                self.functionBt.configure(text=_("STOP"))
                self.functionBt.update_idletasks()
                self.resetBt.configure(state="disable")
                self.resetBt.update_idletasks()
                self.infoLabel.config(text= _("Wait until phase and amplitude is stable and click STOP"))
                self.infoLabel.update_idletasks()
            if balancingOrder==6:
                self.change_state()
                self.functionBt.configure(text=_("TRIM 2\nRUN"))
                self.functionBt.update_idletasks()
                self.resetBt.configure(state="normal")
                self.resetBt.update_idletasks()
                self.infoLabel.config(text= _("Next step: Execute the second trim run"))
                self.infoLabel.update_idletasks()
            if balancingOrder==7:
                _balancingLabel="Trim2"
                self.functionBt.configure(text=_("STOP"))
                self.functionBt.update_idletasks()
                self.resetBt.configure(state="disable")
                self.resetBt.update_idletasks()
                self.infoLabel.config(text= _("Wait until phase and amplitude is stable and click STOP"))
                self.infoLabel.update_idletasks()
            if balancingOrder==8:
                self.change_state()
                self.functionBt.configure(text=_("END\nPROCESS"))
                self.functionBt.update_idletasks()
                self.resetBt.configure(state="normal")
                self.resetBt.update_idletasks()
                self.infoLabel.config(text= _("Next step: Finish!"))
            if  balancingOrder<9 :
                if balancingOrder%2==1:
                    self.change_state()
                    t1 = threading.Thread(target=self.one_plane_read_label_data, args=(_balancingLabel, self.lock))
                    t1.start()
                else:
                    pass
            else:
                balancingOrder=0
                self.functionBt.configure(state="disable", text=_("INITIAL\nRUN"))
                self.functionBt.update_idletasks()
                return
        else:
            if self.balancing_config_struct["num_sensors"]=="One":
                if balancingOrder==1:
                    _balancingLabel="InitialPL1"
                    self.functionBt.configure(text=_("STOP"))
                    self.functionBt.update_idletasks()
                    self.resetBt.configure(state="disable")
                    self.resetBt.update_idletasks()
                    self.infoLabel.config(text= _("Wait until phase and amplitude is stable and click STOP"))
                if balancingOrder==2:
                    _balancingLabel="Stop"
                    self.change_state()
                    self.functionBt.configure(text=_("INITIAL\nPL2"))
                    self.functionBt.update_idletasks()
                    self.resetBt.configure(state="normal")
                    self.resetBt.update_idletasks()
                    self.infoLabel.config(text= _("Next step: Initial Run, Collect data on the plane 2"))
                    self.infoLabel.update_idletasks()
                if balancingOrder==3:
                    _balancingLabel="InitialPL2"
                    self.functionBt.configure(text=_("STOP"))
                    self.functionBt.update_idletasks()
                    self.resetBt.configure(state="disable")
                    self.resetBt.update_idletasks()
                    self.infoLabel.config(text= _("Wait until phase and amplitude is stable and click STOP"))
                    self.infoLabel.update_idletasks()
                if balancingOrder==4:
                    _balancingLabel="Stop"
                    self.change_state()
                    self.functionBt.configure(text=_("TRIAL 1\nPL1"))
                    self.functionBt.update_idletasks()
                    self.resetBt.configure(state="normal")
                    self.resetBt.update_idletasks()
                    self.infoLabel.config(text= _("Next step: First Trial Run, Collect data on the plane 1"))
                    self.infoLabel.update_idletasks()
                if balancingOrder==5:
                    _balancingLabel="Trial1PL1"
                    self.functionBt.configure(text=_("STOP"))
                    self.functionBt.update_idletasks()
                    self.resetBt.configure(state="disable")
                    self.resetBt.update_idletasks()
                    self.infoLabel.config(text= _("Wait until phase and amplitude is stable and click STOP"))
                    self.infoLabel.update_idletasks()
                if balancingOrder==6:
                    _balancingLabel="Stop"
                    self.change_state()
                    self.functionBt.configure(text=_("TRIAL 1\nPL2"))
                    self.functionBt.update_idletasks()
                    self.resetBt.configure(state="normal")
                    self.resetBt.update_idletasks()
                    self.infoLabel.config(text= _("Next step: First Trial Run, Collect data on the plane 2"))
                    self.infoLabel.update_idletasks()
                if balancingOrder==7:
                    _balancingLabel="Trial1PL2"
                    self.functionBt.configure(text=_("STOP"))
                    self.functionBt.update_idletasks()
                    self.resetBt.configure(state="disable")
                    self.resetBt.update_idletasks()
                    self.infoLabel.config(text= _("Wait until phase and amplitude is stable and click STOP"))
                    self.infoLabel.update_idletasks()
                if balancingOrder==8:
                    _balancingLabel="Stop"
                    self.change_state()
                    self.functionBt.configure(text=_("TRIAL 2\nPL1"))
                    self.functionBt.update_idletasks()
                    self.resetBt.configure(state="normal")
                    self.resetBt.update_idletasks()
                    self.infoLabel.config(text= _("Next step: Second Trial Run, Collect data on the plane 1"))
                    self.infoLabel.update_idletasks()
                if balancingOrder==9:
                    _balancingLabel="Trial2PL1"
                    self.functionBt.configure(text=_("STOP"))
                    self.functionBt.update_idletasks()
                    self.resetBt.configure(state="disable")
                    self.resetBt.update_idletasks()
                    self.infoLabel.config(text= _("Wait until phase and amplitude is stable and click STOP"))
                    self.infoLabel.update_idletasks()
                if balancingOrder==10:
                    _balancingLabel="Stop"
                    self.change_state()
                    self.functionBt.configure(text=_("TRIAL 2\nPL2"))
                    self.functionBt.update_idletasks()
                    self.resetBt.configure(state="normal")
                    self.resetBt.update_idletasks()
                    self.infoLabel.config(text= _("Next step: Second Trial Run, Collect data on the plane 2"))
                    self.infoLabel.update_idletasks()
                if balancingOrder==11:
                    _balancingLabel="Trial2PL2"
                    self.functionBt.configure(text=_("STOP"))
                    self.functionBt.update_idletasks()
                    self.resetBt.configure(state="disable")
                    self.resetBt.update_idletasks()
                    self.infoLabel.config(text= _("Wait until phase and amplitude is stable and click STOP"))
                    self.infoLabel.update_idletasks()
                if balancingOrder==12:
                    _balancingLabel="Stop"
                    self.change_state()
                    self.functionBt.configure(text=_("TRIM 1\nPL1"))
                    self.functionBt.update_idletasks()
                    self.resetBt.configure(state="normal")
                    self.resetBt.update_idletasks()
                    self.infoLabel.config(text= _("Next step: First Trim Run, Collect data on the plane 1"))
                    self.infoLabel.update_idletasks()
                if balancingOrder==13:
                    _balancingLabel="Trim1PL1"
                    self.functionBt.configure(text=_("STOP"))
                    self.functionBt.update_idletasks()
                    self.resetBt.configure(state="disable")
                    self.resetBt.update_idletasks()
                    self.infoLabel.config(text= _("Wait until phase and amplitude is stable and click STOP"))
                    self.infoLabel.update_idletasks()
                if balancingOrder==14:
                    _balancingLabel="Stop"
                    self.change_state()
                    self.functionBt.configure(text=_("TRIM 1\nPL2"))
                    self.functionBt.update_idletasks()
                    self.resetBt.configure(state="normal")
                    self.resetBt.update_idletasks()
                    self.infoLabel.config(text= _("Next step: First Trim Run, Collect data on the plane 2"))
                    self.infoLabel.update_idletasks()
                if balancingOrder==15:
                    _balancingLabel="Trim1PL2"
                    self.functionBt.configure(text=_("STOP"))
                    self.functionBt.update_idletasks()
                    self.resetBt.configure(state="disable")
                    self.resetBt.update_idletasks()
                    self.infoLabel.config(text= _("Wait until phase and amplitude is stable and click STOP"))
                    self.infoLabel.update_idletasks()
                if balancingOrder==16:
                    _balancingLabel="Stop"
                    self.change_state()
                    self.functionBt.configure(text=_("TRIM 2\nPL1"))
                    self.functionBt.update_idletasks()
                    self.resetBt.configure(state="normal")
                    self.resetBt.update_idletasks()
                    self.infoLabel.config(text= _("Next step: Second Trim Run, Collect data on the plane 1"))
                    self.infoLabel.update_idletasks()
                if balancingOrder==17:
                    _balancingLabel="Trim2PL1"
                    self.functionBt.configure(text=_("STOP"))
                    self.functionBt.update_idletasks()
                    self.resetBt.configure(state="disable")
                    self.resetBt.update_idletasks()
                    self.infoLabel.config(text= _("Wait until phase and amplitude is stable and click STOP"))
                    self.infoLabel.update_idletasks()
                if balancingOrder==18:
                    _balancingLabel="Stop"
                    self.change_state()
                    self.functionBt.configure(text=_("TRIM 2\nPL2"))
                    self.functionBt.update_idletasks()
                    self.resetBt.configure(state="normal")
                    self.resetBt.update_idletasks()
                    self.infoLabel.config(text= _("Next step: Second Trim Run, Collect data on the plane 2"))
                    self.infoLabel.update_idletasks()
                if balancingOrder==19:
                    _balancingLabel="Trim2PL2"
                    self.functionBt.configure(text=_("STOP"))
                    self.functionBt.update_idletasks()
                    self.resetBt.configure(state="disable")
                    self.resetBt.update_idletasks()
                    self.infoLabel.config(text= _("Wait until phase and amplitude is stable and click STOP"))
                    self.infoLabel.update_idletasks()
                if balancingOrder==20:
                    _balancingLabel="Stop"
                    self.change_state()
                    self.functionBt.configure(text=_("INITIAL 1\nPL1"), state="disable")
                    self.functionBt.update_idletasks()
                    self.resetBt.configure(state="normal")
                    self.resetBt.update_idletasks()
                    self.infoLabel.config(text= _("Next step: Second Trim Run, Collect data on the plane 2"))
                    self.infoLabel.update_idletasks()
                if balancingOrder<21:
                    if balancingOrder%2==1:
                        self.change_state()
                        t2 = threading.Thread(target=self.two_plane_read_label_data, args=(_balancingLabel, self.lock))
                        t2.start()
                    else:
                        pass
                else:
                    balancingOrder=0
                    return
            elif self.balancing_config_struct["num_sensors"]=="Two":
                if balancingOrder==1:
                    _balancingLabel="Initial"
                    self.functionBt.configure(text=_("STOP"))
                    self.functionBt.update_idletasks()
                    self.resetBt.configure(state="disable")
                    self.resetBt.update_idletasks()
                    self.infoLabel.config(text= _("Wait until phase and amplitude is stable and click STOP"))
                    self.infoLabel.update_idletasks()
                if balancingOrder==2:
                    _balancingLabel="Stop"
                    self.change_state()
                    self.functionBt.configure(text=_("TRIAL 1\nRUN"))
                    self.functionBt.update_idletasks()
                    self.resetBt.configure(state="normal")
                    self.resetBt.update_idletasks()
                    self.infoLabel.config(text= _("Next step: First Trial Run, Mount the sensor on two planes and execute"))
                    self.infoLabel.update_idletasks()
                if balancingOrder==3:
                    _balancingLabel="Trial1"
                    self.functionBt.configure(text=_("STOP"))
                    self.functionBt.update_idletasks()
                    self.resetBt.configure(state="disable")
                    self.resetBt.update_idletasks()
                    self.infoLabel.config(text= _("Wait until phase and amplitude is stable and click STOP"))
                    self.infoLabel.update_idletasks()
                if balancingOrder==4:
                    _balancingLabel="Stop"
                    self.change_state()
                    self.functionBt.configure(text=_("TRIAL 2\nRUN"))
                    self.functionBt.update_idletasks()
                    self.resetBt.configure(state="normal")
                    self.resetBt.update_idletasks()
                    self.infoLabel.config(text= _("Next step: Second Trial Run, Mount the sensor on two planes and execute"))
                    self.infoLabel.update_idletasks()
                if balancingOrder==5:
                    _balancingLabel="Trial2"
                    self.functionBt.configure(text=_("STOP"))
                    self.functionBt.update_idletasks()
                    self.resetBt.configure(state="disable")
                    self.resetBt.update_idletasks()
                    self.infoLabel.config(text= _("Wait until phase and amplitude is stable and click STOP"))
                    self.infoLabel.update_idletasks()
                if balancingOrder==6:
                    _balancingLabel="Stop"
                    self.change_state()
                    self.functionBt.configure(text=_("TRIM 1\nRUN"))
                    self.functionBt.update_idletasks()
                    self.resetBt.configure(state="normal")
                    self.resetBt.update_idletasks()
                    self.infoLabel.config(text= _("Next step: First Trim Run, Mount the sensor on two planes and execute"))
                    self.infoLabel.update_idletasks()
                if balancingOrder==7:
                    _balancingLabel="Trim1"
                    self.functionBt.configure(text=_("STOP"))
                    self.functionBt.update_idletasks()
                    self.resetBt.configure(state="disable")
                    self.resetBt.update_idletasks()
                    self.infoLabel.config(text= _("Wait until phase and amplitude is stable and click STOP"))
                    self.infoLabel.update_idletasks()
                if balancingOrder==8:
                    _balancingLabel="Stop"
                    self.change_state()
                    self.functionBt.configure(text=_("TRIM 2\nRUN"))
                    self.functionBt.update_idletasks()
                    self.resetBt.configure(state="normal")
                    self.resetBt.update_idletasks()
                    self.infoLabel.config(text= _("Next step: Second Trim Run, Mount the sensor on two planes and execute"))
                    self.infoLabel.update_idletasks()
                if balancingOrder==9:
                    _balancingLabel="Trim2"
                    self.functionBt.configure(text=_("STOP"))
                    self.functionBt.update_idletasks()
                    self.resetBt.configure(state="disable")
                    self.resetBt.update_idletasks()
                    self.infoLabel.config(text= _("Wait until phase and amplitude is stable and click STOP"))
                    self.infoLabel.update_idletasks()
                if balancingOrder==10:
                    _balancingLabel="Stop"
                    self.change_state()
                    self.functionBt.configure(text=_("INITIAL\nRUN"), state='disable')
                    self.functionBt.update_idletasks()
                    self.resetBt.configure(state="normal")
                    self.resetBt.update_idletasks()
                    self.infoLabel.config(text= _("Next step: Initial Run, Mount the sensor on two planes and execute"))
                    self.infoLabel.update_idletasks()   
                if  balancingOrder<11 :
                    if balancingOrder%2==1:
                        self.change_state()
                        t6 = threading.Thread(target=self.two_plane_read_label_data, args=(_balancingLabel, self.lock))
                        t6.start()
                    else:
                        pass
                else:
                    balancingOrder=0
                    return

    def one_plane_read_label_data(self, label, lock):
        global click_stop_flag
        while click_stop_flag:
            chanelv=[[],[],[],[]]
            chanelm=[[],[],[],[],[]]
            chaneln=[]
            numADCChanel=6
            data_length = pow2(self.balancing_config_struct["num_fft_line"]) + 2
            total_length=numADCChanel*data_length+1
            ttl=[]
            with lock:
                ad7609.ADCread.restype = ctypes.POINTER(ctypes.c_float * total_length)
                ad7609.ADCread.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int]
                ad7609.freeme.argtypes = ctypes.c_void_p,
                ad7609.freeme.restype = None
                kq=ad7609.ADCread(data_length, self.balancing_config_struct["sample_rate"], int(numADCChanel))
                ttl=[i for i in kq.contents]
                ad7609.freeme(kq)
            # print("actual_sample_rate:", ttl[-1])
            
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
            for i in range(numADCChanel-1):
                chaneln.append(np.array(chanelm[i][2:]))

            for i in range(3):
                if self.balancing_config_struct["sensor_type"]=='Acceleration':
                    chanelv[i]=chaneln[i][2:]*10 #g
                    chanelv[i]-=np.mean(chanelv[i])
                    unit='g'
                elif self.balancing_config_struct["sensor_type"]=='Velocity':
                    chanelv[i]=chaneln[i][2:]*254  # mm/s
                    chanelv[i]-=np.mean(chanelv[i])
                    unit='mm/s'
                else:
                    pass
            chaneln[4] /= 2 #0
            chanelv[3]=chaneln[4][2:]
            if self.balancing_config_struct["sensor1"]=='Port1':
                samplePlaneData=chanelv[0]
            elif self.balancing_config_struct["sensor1"]=='Port2':
                samplePlaneData=chanelv[1]
            elif self.balancing_config_struct["sensor1"]=='Port3':
                samplePlaneData=chanelv[2]
            else:
                pass
            laserSample=chanelv[3]
            
            _samplePlaneData = filter_data(samplePlaneData, "LOWPASS", dfc._RMS_HIGHPASS_FROM, dfc._RMS_LOWPASS_TO, 
                                            self.balancing_config_struct["sample_rate"], window="Hanning")
            _laserSample = filter_data(laserSample, "LOWPASS", dfc._RMS_HIGHPASS_FROM, dfc._RMS_LOWPASS_TO, 
                                            self.balancing_config_struct["sample_rate"], window="Hanning")
            _laserSample=fresh_laser_pulse(_laserSample)
            _amplitude = rmsValue(_samplePlaneData)
            _phase = phase_shift2(_laserSample, _samplePlaneData, self.balancing_config_struct["sample_rate"], 25)%(2*np.pi)
            current_run = {
                "label": label,
                "amplitude": _amplitude,
                "phase": _phase,
            }
            if len(self.balancing_config_struct["run"])==0:
                self.balancing_config_struct["run"].append(current_run)
            else:
                if self.balancing_config_struct["run"][-1]["label"] != label:
                    self.balancing_config_struct["run"].append(current_run)
                else:
                    self.balancing_config_struct["run"].pop()
                    self.balancing_config_struct["run"].append(current_run)
            num_run = len(self.balancing_config_struct["run"])
            if num_run==0:
                pms.general_warning(_("Data errors."))
                
            else:
                result=Pd.PLT.plot_balancing(self.canvas, self.balancing_config_struct, 1)
                if result[-1]=="Corr1":
                    self.infoLabel.config(text=f"Correction Weight: {str(result[0])[:4]}g | Correction Angel: {str(int(result[1]))}°")
                    self.balancing_config_struct["trim_run"].append(result)
                if result[-1]=="Trim1":
                    self.infoLabel.config(text=f"Trim Weight 1: {str(result[0])[:4]}g | Trim Angel 1: {str(int(result[1]))}°")
                    self.balancing_config_struct["trim_run"].append(result)
                if result[-1]=="Trim2":
                    self.infoLabel.config(text=f"Trim Weight 2: {str(result[0])[:4]}g | Trim Angel 2: {str(int(result[1]))}°")
                    self.balancing_config_struct["trim_run"].append(result)
                else:
                    pass
            
    def two_plane_read_label_data(self, label, lock):
        global click_stop_flag
        while click_stop_flag:
            
            chanelv=[[],[],[],[]]
            chanelm=[[],[],[],[],[]]
            chaneln=[]
            numADCChanel=6
            data_length = pow2(self.balancing_config_struct["num_fft_line"]) + 2
            total_length=numADCChanel*data_length+1
            ttl=[]
            with lock:
                ad7609.ADCread.restype = ctypes.POINTER(ctypes.c_float * total_length)
                ad7609.ADCread.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int]
                ad7609.freeme.argtypes = ctypes.c_void_p,
                ad7609.freeme.restype = None
                kq=ad7609.ADCread(data_length, self.balancing_config_struct["sample_rate"], int(numADCChanel))
                ttl=[i for i in kq.contents]
                ad7609.freeme(kq)
            # print("actual_sample_rate:", ttl[-1])
            
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
            for i in range(numADCChanel-1):
                chaneln.append(np.array(chanelm[i][2:]))            
            for i in range(3):
                if self.balancing_config_struct["sensor_type"]=='Acceleration':
                    chanelv[i]=chaneln[i][2:]*10 #g
                    chanelv[i]-=np.mean(chanelv[i])
                elif self.balancing_config_struct["sensor_type"]=='Velocity':
                    chanelv[i]=chaneln[i][2:]*254  # mm/s
                    chanelv[i]-=np.mean(chanelv[i])
                else:
                    pass
            chaneln[4] /= 2 #0
            chanelv[3]=chaneln[4][2:]
            if self.balancing_config_struct["sensor1"]=='Port1':
                samplePlane1Data=chanelv[0]
            elif self.balancing_config_struct["sensor1"]=='Port2':
                samplePlane1Data=chanelv[1]
            elif self.balancing_config_struct["sensor1"]=='Port3':
                samplePlane1Data=chanelv[2]
            else:
                pass
            if self.balancing_config_struct["sensor2"]=='Port1':
                samplePlane2Data=chanelv[0]
            elif self.balancing_config_struct["sensor2"]=='Port2':
                samplePlane2Data=chanelv[1]
            elif self.balancing_config_struct["sensor2"]=='Port3':
                samplePlane2Data=chanelv[2]
            else:
                pass
            laserSample=chanelv[3]
            
            _samplePlane1Data = filter_data(samplePlane1Data, "LOWPASS", dfc._RMS_HIGHPASS_FROM, dfc._RMS_LOWPASS_TO, self.balancing_config_struct["sample_rate"], window="Hanning")
            _samplePlane2Data = filter_data(samplePlane2Data, "LOWPASS", dfc._RMS_HIGHPASS_FROM, dfc._RMS_LOWPASS_TO, self.balancing_config_struct["sample_rate"], window="Hanning")
            _laserSample = filter_data(laserSample, "LOWPASS", dfc._RMS_HIGHPASS_FROM, dfc._RMS_LOWPASS_TO, self.balancing_config_struct["sample_rate"], window="Hanning")
            _laserSample=fresh_laser_pulse(_laserSample)
            _amplitude1 = rmsValue(_samplePlane1Data)
            _amplitude2 = rmsValue(_samplePlane2Data)   
            _phase1 = phase_shift2(_laserSample, _samplePlane1Data, self.balancing_config_struct["sample_rate"], 25)%(2*np.pi)
            _phase2 = phase_shift2(_laserSample, _samplePlane2Data, self.balancing_config_struct["sample_rate"], 25)%(2*np.pi)
            current_run = {
                "label": label,
                "amplitude1": _amplitude1,
                "phase1": _phase1,
                "amplitude2": _amplitude2,
                "phase2": _phase2,
                "vibration_signal":_samplePlane1Data,
                "laser": _laserSample
            }
            if len(self.balancing_config_struct["run"])==0:
                self.balancing_config_struct["run"].append(current_run)
            else:
                if self.balancing_config_struct["run"][-1]["label"] != label:
                    self.balancing_config_struct["run"].append(current_run)
                else:
                    self.balancing_config_struct["run"].pop()
                    self.balancing_config_struct["run"].append(current_run)
            num_run = len(self.balancing_config_struct["run"])
            if num_run==0:
                pms.general_warning(_("Data errors."))
                return -1
            else:
                if self.balancing_config_struct["num_sensors"]=="One":
                    result=Pd.PLT.plot_balancing(self.canvas, self.balancing_config_struct, 2)
                elif self.balancing_config_struct["num_sensors"]=="Two":
                    result=Pd.PLT.plot_balancing(self.canvas, self.balancing_config_struct, 3)
                if result[-1]=="Corr1":
                    self.infoLabel.config(text=f"Corr PL1 W: {str(result[0])[:4]}g | A: {str(int(result[1]))}° || Corr PL2 W: {str(result[2])[:4]}g | A: {str(int(result[3]))}°")
                    self.balancing_config_struct["trim_run"].append(result)
                if result[-1]=="Trim1":
                    self.infoLabel.config(text=f"Trim1 PL1 W: {str(result[0])[:4]}g | A: {str(int(result[1]))}° || PL2 W: {str(result[2])[:4]}g | A: {str(int(result[3]))}°")
                    self.balancing_config_struct["trim_run"].append(result)
                if result[-1]=="Trim2":
                    self.infoLabel.config(text=f"Trim2 PL1 W: {str(result[0])[:4]}g | A: {str(int(result[1]))}° || PL2 W: {str(result[2])[:4]}g | A: {str(int(result[3]))}°")
                    self.balancing_config_struct["trim_run"].append(result)
                else:
                    pass




class BalancingPlotCanvas(Tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bd=1, bg='white', width=918, height=504)
        fig5 = plt.figure(figsize=(8.2,8.1))
        ax_51 = fig5.add_subplot(1,2,1, projection='polar')
        ax_51.set_position([0.03, 0.1, 0.45, 0.7])
        ax_51.set_title('1st plane')
        ax_51.set_facecolor("lavender")
        ax_51.grid(False)
        ax_52 = fig5.add_subplot(1,2,2, projection='polar')
        ax_52.set_position([0.5, 0.1, 0.45, 0.7])
        ax_52.set_title('2nd plane')
        ax_52.set_facecolor("lightyellow")
        ax_52.grid(False)
        self.canvas5 = FigureCanvasTkAgg(fig5, master=self)
        self.canvas5.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)