import sys
import os
import tkinter as Tk
from tkinter import ttk
from ui.home.HomePage import HomePage
import sv_ttk
from ui.Diagnostic.DiagnosticPage import DiagnosticPage
from ui.home.HomePage import HomePage
from ui.Settingpage.SettingPage import SettingPage
from ui.ResonanceModule.ResonanceModule import Resonance
from ui.balancingModule.balancingModule import Balancing
from ui.history.historyModule import History

#temp
import threading
from threading import Lock
from bateryMonitor.powerManager import *
from ds3231.ds3231B import DS3231
from image.image import ImageAdrr
remainCap = 50
remainVolt = 3.8
stateOfCharge = "CHARGING"
firstTime = True
#temp
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
            "Date":"----_--_--",
            "Note": "None"
        }
        self.batery_struct={
            "remainCap": 50
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
            "num_fft_line": 1600,
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
        #temp
        self.ds3231 = DS3231(1, 0x68)
        self.batery=BQ27510()
        self.lock=Lock()
        imageAddress = ImageAdrr()
        self.low_bat = imageAddress.low_bat
        self.half_bat = imageAddress.half_bat
        self.full_bat = imageAddress.full_bat
        self.empty_bat = imageAddress.empty_bat
        self.lowCharging = imageAddress.lowCharging
        self.medCharging = imageAddress.medCharging
        self.fullCharging = imageAddress.fullCharging
        self.emptyCharging = imageAddress.emptyCharging
        self.batFrame = Tk.Frame(self, bd=1, bg='grey95', width=130, height=35)
        self.batFrame.pack()
        self.batFrame.place(relx=0.87, rely=0.0)
        self.batFrame.pack_propagate(0)
        self.timeLabel = ttk.Label(self.batFrame, style='bat.TLabel', text=self.get_time_now())
        self.timeLabel.after(5000, self.update_time)
        self.timeLabel.place(relx=0.05, rely=0.1)

        self.batLabel = ttk.Label(self.batFrame, style='bat.TLabel', text=f"{str(remainCap)}%", image=self.half_bat, compound=Tk.LEFT)
        self.batLabel.image = self.full_bat
        self.batLabel.after(10000, self.update_bat)
        self.batLabel.place(relx=0.5, rely=0.1)
        #temp
        self.origin_config = TotalConfig()
        HomePage(self).pack()

    #temp
    def update_time(self):
        # now = datetime.now()
        # current_time = now.strftime("%H:%M")
        current_time=self.get_time_now()
        self.timeLabel.configure(text=current_time)
        self.timeLabel.after(5000, self.update_time)

    def get_time_now(self):
        ds3231 = DS3231(1, 0x68)
        rtcTime=str(ds3231.read_datetime())
        # rtcTime=time.strftime("%Y-%m-%d %H:%M:%S")
        return rtcTime[11:16]

    def update_bat(self):
        global firstTime, remainCap, stateOfCharge, remainVolt
        t8 = threading.Thread(target=self.read_battery)
        t8.start()
        averageCapacity = remainCap
        if averageCapacity>=70:
            if stateOfCharge !="CHARGING":
                self.batLabel.configure(text=f"{int(averageCapacity)}%", image=self.full_bat, compound=Tk.LEFT)
            else:
                self.batLabel.configure(text=f"{int(averageCapacity)}%", image=self.fullCharging, compound=Tk.LEFT)
        elif 30<=averageCapacity<70:
            if stateOfCharge !="CHARGING":
                self.batLabel.configure(text=f"{int(averageCapacity)}%", image=self.half_bat, compound=Tk.LEFT)
            else:
                self.batLabel.configure(text=f"{int(averageCapacity)}%", image=self.medCharging, compound=Tk.LEFT)
        elif 10<=averageCapacity<30:
            if stateOfCharge !="CHARGING":
                self.batLabel.configure(text=f"{int(averageCapacity)}%", image=self.low_bat, compound=Tk.LEFT)
            else:
                self.batLabel.configure(text=f"{int(averageCapacity)}%", image=self.lowCharging, compound=Tk.LEFT)

        else:
            if stateOfCharge !="CHARGING":
                self.batLabel.configure(text=f"{int(averageCapacity)}%", image=self.empty_bat, compound=Tk.LEFT)
            else:
                self.batLabel.configure(text=f"{int(averageCapacity)}%", image=self.emptyCharging, compound=Tk.LEFT)
            if firstTime:
                # pms.general_warning(_("Low Battery! Plug in the charger to keep it running"))
                firstTime = False
            if remainVolt <= 2.85:
                if stateOfCharge !="CHARGING":
                    with self.lock:
                        self.batery.i2c_send_turn_off()
                    os.system("sudo shutdown -h now")
        self.batLabel.after(10000, self.update_bat)

    def read_battery(self):
        global remainCap, stateOfCharge, remainVolt
        with self.lock:
            remainCap = round(self.batery.get_remaining_capacity())
            remainVolt=self.batery.bq27510_battery_voltage()
            if self.batery.bq27510_battery_current() > 0:
                stateOfCharge = "CHARGING"
            else:
                stateOfCharge = "DISCHARGE"
    #temp
    def go_to_home_page(self):
        HomePage(self)

    def go_to_diagnostic_page(self):
        DiagnosticPage(self)

    def go_to_setting_page(self):
        SettingPage(self)

    def go_to_resonance_page(self):
        Resonance(self)

    def go_to_balancing_page(self):
        Balancing(self)
    def go_to_history_page(self):
        History(self)

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