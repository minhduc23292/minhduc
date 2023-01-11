import tkinter as Tk
import sv_ttk
from tkinter import ttk
import os
from i18n import _
from keyboard.keyboard import KeyBoard
from image.image import ImageAdrr
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main import Application
current_directory = os.getcwd()
parent_directory = os.path.dirname(os.path.dirname(current_directory))

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

        self.btstyle = ttk.Style()
        self.btstyle.configure('normal.TButton', font=('Chakra Petch', 12), borderwidth=5, justify=Tk.CENTER)
        self.btstyle.map('normal.TButton', foreground=[('active', 'blue')])
        self.btstyle.configure('custom.Accent.TButton', font=('Chakra Petch', 10), bordercolor='black', borderwidth=4,
                               justify=Tk.CENTER)
        self.btstyle.configure('bat.TLabel', font=('Chakra Petch', 12))
        self.btstyle.configure('normal.TLabel', font=('Chakra Petch', 12), background='white')

        self.mainFrame = Tk.Frame(self.parent, bd=1, bg='white', width=1024, height=600)
        self.mainFrame.pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)
        self.mainFrame.pack_propagate(0)

        self.featureFrame = Tk.Frame(self.mainFrame, bd=1, bg='white', width=1024, height=80)
        self.featureFrame.pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)
        self.featureFrame.pack_propagate(0)

        self.resonanceConfigFrame = ResonanceConfig(self.mainFrame, self.parent.origin_config)
        self.resonanceConfigFrame.pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)
        self.resonanceConfigFrame.pack_propagate(0)

        self.resonanceAnalysisFrame = Tk.Frame(self.mainFrame, bd=1, bg='white', width=1024, height=520)
        self.resonanceAnalysisFrame.pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)
        self.resonanceAnalysisFrame.pack_propagate(0)
        self.resonanceAnalysisFrame.pack_forget()

        self.batFrame = Tk.Frame(self.featureFrame, bd=1, bg='grey95', width=117, height=40)
        self.batFrame.pack()
        self.batFrame.place(relx=0.875, rely=0.01)
        self.batFrame.pack_propagate(0)

        self.creat_setting_feature_panel()
        self.parent.bind_class('TEntry', "<FocusIn>", self.show_key_board)
        self.parent.bind_class('TCombobox', "<<ComboboxSelected>>", self.change_state)

    def show_key_board(self, event):
        # self.generalConfigFrame.applyButton.configure(state='normal')
        self.widget = self.get_focus_widget()
        self.keyboardFrame = KeyBoard(self.widget)
        parentName = event.widget.winfo_parent()
        self.parent1 = event.widget._nametowidget(parentName)
        self.parent1.focus()

    def get_focus_widget(self):
        widget = self.parent.focus_get()
        return widget

    def change_state(self, event):
        pass
        # self.applyBt.configure(state="normal")

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
        self.homeBt.place(relx=0.015, rely=0.018, width=100, height=72)
        self.homeBt.image = self.homePhoto

        self.configBt = ttk.Button(self.featureFrame, style='normal.TButton', text="Setting")
        self.configBt.place(relx=0.128, rely=0.018, width=115, height=72)

        self.analysis = ttk.Button(self.featureFrame, style='normal.TButton', text="Resonance\nAnalysis")
        self.analysis.place(relx=0.255, rely=0.018, width=115, height=72)

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

        resonanceConfigFrame = Tk.LabelFrame(self, text=_(''), bg="white", border=0)
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
        filterFromLabel.grid(column=2, row=0, padx=10, pady=5, sticky='w')
        filterFromEntry = ttk.Entry(resonanceConfigFrame, width=14, textvariable=self.resonanceParam4)
        filterFromEntry.grid(column=3, row=0, padx=0, pady=5, sticky='e')

        filterToLabel = ttk.Label(resonanceConfigFrame, text=_("Bandpass Filter To"), style="resonance.TLabel")
        filterToLabel.grid(column=2, row=1, padx=10, pady=5, sticky='w')
        filterToEntry = ttk.Entry(resonanceConfigFrame, width=14, textvariable=self.resonanceParam5)
        filterToEntry.grid(column=3, row=1, padx=0, pady=5, sticky='e')

        viewLabel = ttk.Label(resonanceConfigFrame, text=_("Sample rate"), style="resonance.TLabel")
        viewLabel.grid(column=2, row=2, padx=10, pady=5, sticky='w')
        viewEntry = ttk.Entry(resonanceConfigFrame, width=14, textvariable=self.resonanceParam6)
        viewEntry.grid(column=3, row=2, padx=0, pady=5, sticky='e')

        meshLabel = ttk.Label(resonanceConfigFrame, text=_("Sampling time"), style="resonance.TLabel")
        meshLabel.grid(column=2, row=3, padx=10, pady=5, sticky='w')
        meshEntry = ttk.Entry(resonanceConfigFrame, width=14, textvariable=self.resonanceParam7)
        meshEntry.grid(column=3, row=3, padx=0, pady=5, sticky='e')

        trackingLabel = ttk.Label(resonanceConfigFrame, text=_("Tracking resolution"), style="resonance.TLabel")
        trackingLabel.grid(column=2, row=4, padx=10, pady=5, sticky='w')
        trackingEntry = ttk.Entry(resonanceConfigFrame, width=14, textvariable=self.resonanceParam9)
        trackingEntry.grid(column=3, row=4, padx=0, pady=5, sticky='e')

        numOfAverageLabel = ttk.Label(resonanceConfigFrame, text=_("Num of Average"), style="resonance.TLabel")
        numOfAverageLabel.grid(column=2, row=5, padx=10, pady=5, sticky='w')
        numOfAverageEntry = ttk.Entry(resonanceConfigFrame, width=14, textvariable=self.resonanceParam11)
        numOfAverageEntry.grid(column=3, row=5, padx=0, pady=5, sticky='e')

        resonanceApplyButton = ttk.Button(resonanceConfigFrame, text=_("Apply"), style="Accent.TButton",
                                    command=lambda: self.update_resonance_struct(resonance_config_struct))
        resonanceApplyButton.grid(column=3, row=6, padx=0, pady=10, ipadx=20, ipady=5, sticky='w')


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
