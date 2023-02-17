import tkinter as Tk
# import sv_ttk
from tkinter import ttk
import os
from i18n import _
from image.image import ImageAdrr
from datetime import datetime
from typing import TYPE_CHECKING
import threading
from threading import Lock
from bateryMonitor.powerManager import *
from ds3231.ds3231B import DS3231
import pms.popMessage as pms
if TYPE_CHECKING:
    from main import Application
current_directory = os.getcwd()
parent_directory = os.path.dirname(os.path.dirname(current_directory))
remainCap = 50
remainVolt = 3.8
stateOfCharge = "CHARGING"
firstTime = True

class HomePage(Tk.Frame):
    def __init__(self, parent: "Application"):
        super().__init__(parent)
        self.parent = parent
        imageAddress = ImageAdrr()
        self.lock = Lock()
        self.batery=BQ27510()
        self.settingPhoto = imageAddress.settingPhoto
        self.smallSePhoto = imageAddress.smallSettingPhoto
        self.diagnosPhoto = imageAddress.diagnosPhoto
        self.balancePhoto = imageAddress.balancePhoto
        self.historyPhoto = imageAddress.historyPhoto
        self.resonacePhoto = imageAddress.resonacePhoto
        # self.low_bat = imageAddress.low_bat
        # self.half_bat = imageAddress.half_bat
        # self.full_bat = imageAddress.full_bat
        # self.empty_bat = imageAddress.empty_bat
        # self.lowCharging = imageAddress.lowCharging
        # self.medCharging = imageAddress.medCharging
        # self.fullCharging = imageAddress.fullCharging
        # self.emptyCharging = imageAddress.emptyCharging
        # self.read_battery()
        self.creat_home_page(self.parent.origin_config)

    def creat_home_page(self, origin_config):
        global remainCap
        self.style = ttk.Style(self.parent)
        self.style.configure('home.TLabel', background='white', font=('Chakra Petch', 40))
        self.style.configure('bat.TLabel', background='grey95', font=('Chakra Petch', 13))
        self.style.configure('home.TButton', font=('Chakra Petch', 18), bordercolor='black', borderwidth=1,
                             justify=Tk.CENTER)
        self.homeFrame = Tk.Frame(self.parent, bd=1, bg='white', width=1024, height=600)
        self.homeFrame.pack()
        self.homeFrame.pack_propagate(0)

        # self.batFrame = Tk.Frame(self.homeFrame, bd=1, bg='grey95', width=130, height=35)
        # self.batFrame.pack()
        # self.batFrame.place(relx=0.87, rely=0.0)
        # self.batFrame.pack_propagate(0)

        homeLabel = ttk.Label(self.homeFrame, style='home.TLabel', text="Otani Analyzer", image=self.settingPhoto,
                              compound=Tk.LEFT)
        homeLabel.place(relx=0.28, rely=0.1)

        # self.timeLabel = ttk.Label(self.batFrame, style='bat.TLabel', text=self.get_time_now())
        # self.timeLabel.after(5000, self.update_time)
        # self.timeLabel.place(relx=0.05, rely=0.1)

        # self.batLabel = ttk.Label(self.batFrame, style='bat.TLabel', text=f"{str(remainCap)}%", image=self.full_bat, compound=Tk.LEFT)
        # self.batLabel.image = self.full_bat
        # self.batLabel.after(10000, self.update_bat)
        # self.batLabel.place(relx=0.5, rely=0.1)

        self.diagnosticButton = ttk.Button(self.homeFrame, style='home.TButton', text=_("Diagnostic"),
                                           image=self.resonacePhoto,
                                           compound=Tk.TOP, command=self.move_to_diagnostic_page)
        self.diagnosticButton.place(relx=0.21, rely=0.32, width=188, height=125)

        self.balancingButton = ttk.Button(self.homeFrame, style='home.TButton', text=_("Dynamic\nBalancing"),
                                          image=self.balancePhoto,
                                          compound=Tk.TOP, command=self.move_to_balancing_page)
        self.balancingButton.place(relx=0.578, rely=0.32, width=188, height=125)

        self.resonanceButton = ttk.Button(self.homeFrame, style='home.TButton', text=_("Resonance\nAnalysis"),
                                          image=self.resonacePhoto,
                                          compound=Tk.TOP, command=self.move_to_resonance_page)
        self.resonanceButton.place(relx=0.21, rely=0.59, width=188, height=125)

        self.historyButton = ttk.Button(self.homeFrame, style='home.TButton', text=_("History"), image=self.historyPhoto,
                                        compound=Tk.TOP, command=self.move_to_history_page)
        self.historyButton.place(relx=0.578, rely=0.59, width=188, height=125)

        self.settingButton = ttk.Button(self.homeFrame, style='home.TButton', text=_("Settings"), image=self.smallSePhoto,
                                        compound=Tk.LEFT, command=self.move_to_setting_page)
        self.settingButton.place(relx=0.76, rely=0.86, width=210, height=52)


    def move_to_diagnostic_page(self):
        self.homeFrame.destroy()
        self.parent.go_to_diagnostic_page()

    def move_to_setting_page(self):
        self.homeFrame.destroy()
        self.parent.go_to_setting_page()

    def move_to_resonance_page(self):
        self.homeFrame.destroy()
        self.parent.go_to_resonance_page()

    def move_to_balancing_page(self):
        self.homeFrame.destroy()
        self.parent.go_to_balancing_page()

    def move_to_history_page(self):
        self.homeFrame.destroy()
        self.parent.go_to_history_page()
        
    # def update_time(self):
    #     # now = datetime.now()
    #     # current_time = now.strftime("%H:%M")
    #     current_time=self.get_time_now()
    #     self.timeLabel.configure(text=current_time)
    #     self.timeLabel.after(5000, self.update_time)

    # def get_time_now(self):
    #     ds3231 = DS3231(1, 0x68)
    #     rtcTime=str(ds3231.read_datetime())
    #     # rtcTime=time.strftime("%Y-%m-%d %H:%M:%S")
    #     return rtcTime[11:16]

    # def update_bat(self):
    #     global firstTime, remainCap, stateOfCharge, remainVolt
    #     t8 = threading.Thread(target=self.read_battery)
    #     t8.start()
    #     averageCapacity = remainCap
    #     if averageCapacity>=70:
    #         if stateOfCharge !="CHARGING":
    #             self.batLabel.configure(text=f"{int(averageCapacity)}%", image=self.full_bat, compound=Tk.LEFT)
    #         else:
    #             self.batLabel.configure(text=f"{int(averageCapacity)}%", image=self.fullCharging, compound=Tk.LEFT)
    #     elif 30<=averageCapacity<70:
    #         if stateOfCharge !="CHARGING":
    #             self.batLabel.configure(text=f"{int(averageCapacity)}%", image=self.half_bat, compound=Tk.LEFT)
    #         else:
    #             self.batLabel.configure(text=f"{int(averageCapacity)}%", image=self.medCharging, compound=Tk.LEFT)
    #     elif 10<=averageCapacity<30:
    #         if stateOfCharge !="CHARGING":
    #             self.batLabel.configure(text=f"{int(averageCapacity)}%", image=self.low_bat, compound=Tk.LEFT)
    #         else:
    #             self.batLabel.configure(text=f"{int(averageCapacity)}%", image=self.lowCharging, compound=Tk.LEFT)

    #     else:
    #         if stateOfCharge !="CHARGING":
    #             self.batLabel.configure(text=f"{int(averageCapacity)}%", image=self.empty_bat, compound=Tk.LEFT)
    #         else:
    #             self.batLabel.configure(text=f"{int(averageCapacity)}%", image=self.emptyCharging, compound=Tk.LEFT)
    #         if firstTime:
    #             pms.general_warning(_("Low Battery! Plug in the charger to keep it running"))
    #             firstTime = False
    #         if remainVolt <= 2.85:
    #             if stateOfCharge !="CHARGING":
    #                 with self.lock:
    #                     self.batery.i2c_send_turn_off()
    #                 os.system("sudo shutdown -h now")
    #     self.batLabel.after(10000, self.update_bat)

    # def read_battery(self):
    #     global remainCap, stateOfCharge, remainVolt
    #     with self.lock:
    #         remainCap = round(self.batery.get_remaining_capacity())
    #         remainVolt=self.batery.bq27510_battery_voltage()
    #         if self.batery.bq27510_battery_current() > 0:
    #             stateOfCharge = "CHARGING"
    #         else:
    #             stateOfCharge = "DISCHARGE"

