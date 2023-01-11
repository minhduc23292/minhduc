import sys
import os
import tkinter as Tk
from tkinter import ttk
from ui.home.HomePage import HomePage
import sv_ttk
from ui.Diagnostic.DiagnosticPage import DiagnosticPage
from ui.home.HomePage import HomePage
from ui.Settingpage.SettingPage import SettingPage
from ui.ResonanceModule.ResonaceModule import Resonance

class TotalConfig(object):
    def __init__(self):
        self.sensor_config = {
            "sensor_input": [],
            "sensor_data": [],
            "unit": [],
            "sensor_key": [],
            "sample_rate": 2560,
            "fft_line": 2000,
            "vel": [],
            "accel": [],
            "vel_data": [],
            "accel_data": [],
            "dis": [],
            "displacement_data": []
        }

        self.project_struct = {
            "CompanyName": "No_name",
            "ProjectCode": "A1B2C3",
            "Note": "None"
        }

        self.waveform_config_struct = {
            "Sensor1": 'HA',
            "Sensor2": 'VA',
            "Sensor3": 'AA',
            "Sensor4": 'NONE',
            "KeyPhase": "Sensor1",
            "UseTSA": 0,
            "TSATimes": 10,
            "Fmax": 2000,
            "num_fft_line": 4096,
            "MachineName": "",
            "MachineType": "GENERAL",
            "Speed": 1500,
            "Power": 1,
            "GearTeeth": 0,
            "BearingBore": 50,
            "Foundation": "Rigid"
        }

        self.frequency_config_struct={
                    "FilterType":'LOWPASS',
                    "Window":'Hanning',
                    "FilterFrom":5,
                    "FilterTo":1500,
                    "KeyPhase":"Sensor1",
                    "TrackRange":25,
                    "mesh":25,
                    "unit":"Original"
        }
        self.balancing_config_struct={
                    # "roto_type":'Overhang',
                    "num_planes":'One',
                    "num_sensors":'One',
                    "num_blades" :0,
                    "trial_mass1":5.0,
                    "trial_mass2":5.0,
                    "angle1":0,
                    "angle2":0,
                    "direction":"Clockwise",
                    "num_fft_line":2000,
                    "sample_rate":2560,
                    "sensor_type":'Velocity',
                    "sensor1":'Port1',
                    "sensor2":'Port2',
                    "run":[],
                    "trim_run":[]
        }
        self.history_config_struct={
                    "ProjectID":"",
                    "SensorPosition":"HA",
                    "PlotType":"TREND",
                    "FilterFrom":2000,
                    "FilterTo":30000,
                    "ViewLimit":5000,
                    "TrackingResolution":25,
                    "dataSample":[],
                    "sampleRate":[],
                    "Rms":1,
                    "A_Pk":1,
                    "gE":1,
                    "HFCF":1,
                    "TSA":1,
                    "TsaBin":4096

        }
        self.resonance_config_struct={
                    "Function":"Impact test",
                    "Sensor":"Port1",
                    "Hport":"Port2",
                    "Window":'Exponential',
                    "Factor":"Length",
                    "FilterType":'BANDPASS',
                    "FilterFrom":5,
                    "FilterTo":3000,
                    "sampleRate":5000,
                    "sampling_time":5,
                    "num_of_average":5,
                    "Tracking":25
        }

        self.language_config_struct={
                    "Language":"ENGLISH"
        }


class Application(Tk.Frame):

    def __init__(self, parent):
        super().__init__(parent)
        self.origin_config = TotalConfig()
        HomePage(self).pack()

    def go_to_home_page(self):
        HomePage(self)

    def go_to_diagnostic_page(self):
        DiagnosticPage(self)

    def go_to_setting_page(self):
        SettingPage(self)

    def go_to_resonance_page(self):
        Resonance(self)

if __name__=='__main__':
    root=Tk.Tk()
    sv_ttk.set_theme("light")
    root.geometry("1024x600")
    # root.call("wm", "attributes", ".", "-fullscreen", "true")
    root.resizable(0, 0)
    root.option_add('ChakraPetch', '20')
    root.title('OTANI ANALYZER')
    Application(root).pack(expand=True, fill="both")
    root.mainloop()