import sys
import os
import tkinter as Tk
from tkinter import ttk
from ui.batteryFrame import BatteryFrame
from ui.home.HomePage import HomePage
import sv_ttk
from ui.Diagnostic.DiagnosticPage import DiagnosticPage
from ui.home.HomePage import HomePage
from ui.Settingpage.SettingPage import SettingPage
from ui.ResonanceModule.ResonanceModule import Resonance
from ui.balancingModule.balancingModule import Balancing
from ui.history.historyModule import History

class TotalConfig(object):
    def __init__(self):
        self.sensor_config = {
            "sensor_input": [],
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
            "displacement_data": []
        }

        self.sensor_sensitivity= {
            "acc_sensitivity": 100.0,
            "vel_sensitivity":4.0,
            "hammer_sensitivity":12.0
        }

        self.project_struct = {
            "CompanyName": "No_name",
            "ProjectCode": "A1B2C3",
            "Date":"----_--_--",
            "Note": "None"
        }
        self.batery_struct={
            "remainCap": 50
        }
        self.waveform_config_struct = {
            "Sensor1": 'NONE',
            "Sensor2": 'NONE',
            "Sensor3": 'NONE',
            "Sensor4": 'NONE',
            "Port1Pos": 'NONE',
            "Port2Pos": 'NONE',
            "Port3Pos": 'NONE',
            "KeyPhase": "Sensor1",
            "UseTSA": 0,
            "TSATimes": 10,
            "Fmax": 2000,
            "num_fft_line": 3200,
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
                    "roto_mass":1000,
                    "grade":6.3,
                    "radius":1000,
                    "trial_remove":True,
                    "origin":"LASER POINT",
                    "num_planes":'One',
                    "num_sensors":'One',
                    "num_blades" :4,
                    "trial_mass1":5.0,
                    "trial_mass2":5.0,
                    "angle1":0,
                    "angle2":0,
                    "balancing_speed":1500,
                    "direction":"Clockwise",
                    "num_fft_line":2048,
                    "sample_rate":2048,
                    "sensor_type":'Velocity',
                    "sensor1":'Port1',
                    "sensor2":'Port2',
                    "run":[],
                    "trim_run":[]
        }
        self.history_config_struct={
                    "ProjectID":"",
                    "SensorPosition":"",
                    "PlotType":"TREND",
                    "FilterFrom":1400,
                    "FilterTo":14000,
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
                    "sampleRate":4096,
                    "sampling_time":4,
                    "num_of_average":3,
                    "Tracking":25
        }

        self.language_config_struct={
                    "Language":"ENGLISH"
        }


class Application(Tk.Frame):

    def __init__(self, parent):
        global remainCap
        super().__init__(parent, padx=8, pady=8, bg='#ffffff')
        
        # Configure font globally
        self.style = ttk.Style(parent)
        self.style.configure('Accent.TButton', font=('Chakra Petch', 13))
        
        self.batFrame = BatteryFrame(self)
        self.batFrame.pack()
        self.batFrame.place(relx=0.87, rely=0.0)
        self.batFrame.pack_propagate(0)
        
        self.origin_config = TotalConfig()
        HomePage(self).pack()
        self.batFrame.tkraise()

    def go_to_home_page(self):
        HomePage(self)
        self.batFrame.tkraise()

    def go_to_diagnostic_page(self):
        DiagnosticPage(self)
        self.batFrame.tkraise()

    def go_to_setting_page(self):
        SettingPage(self)
        self.batFrame.tkraise()

    def go_to_resonance_page(self):
        Resonance(self)
        self.batFrame.tkraise()

    def go_to_balancing_page(self):
        Balancing(self)
        self.batFrame.tkraise()
    
    def go_to_history_page(self):
        History(self)
        self.batFrame.tkraise()

    def _quit(self):
        root.quit()
        root.destroy()
        exit()

if __name__=='__main__':
    try:
        root=Tk.Tk()
        sv_ttk.set_theme("light")
        root.geometry("1024x600")
        root.call("wm", "attributes", ".", "-fullscreen", "true")
        root.resizable(0, 0)
        root.option_add('ChakraPetch', '20')
        root.title('OTANI ANALYZER')
        app=Application(root)
        app.pack(expand=True, fill="both")
        root.mainloop()
    except KeyboardInterrupt:
        print("quit the app")
        app._quit()