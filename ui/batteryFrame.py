import tkinter as Tk
from tkinter import ttk
import threading
from threading import Lock
import os
from datetime import datetime
from bateryMonitor.bateryMonitor import BQ40Z50
from PCF85063.PCF85063ATT import PCF85063
from image.image import ImageAdrr

remainCap = 50
remainVolt = 3.8
stateOfCharge = "CHARGING"
firstTime = True

class BatteryFrame(Tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, bd=1, bg='white', width=130, height=35, **kwargs)
        self.style = ttk.Style()
        self.style.configure('bat.TLabel', font=('Chakra Petch', 13))
        self.batery=BQ40Z50()
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
        # self.batFrame = Tk.Frame(self, bd=1, bg='grey95', width=130, height=35)
        # self.batFrame.pack()
        # self.batFrame.place(relx=0.87, rely=0.0)
        # self.batFrame.pack_propagate(0)
        self.timeLabel = ttk.Label(self, style='bat.TLabel', text=self.get_time_now())
        self.timeLabel.after(5000, self.update_time)
        self.timeLabel.place(relx=0.05, rely=0.1)

        self.batLabel = ttk.Label(self, style='bat.TLabel', text=f"{str(remainCap)}%", image=self.half_bat, compound=Tk.LEFT)
        self.batLabel.image = self.full_bat
        self.batLabel.after(10000, self.update_bat)
        self.batLabel.place(relx=0.5, rely=0.1)

    def update_time(self):
        # now = datetime.now()
        # current_time = now.strftime("%H:%M")
        current_time=self.get_time_now()
        self.timeLabel.configure(text=current_time)
        self.timeLabel.after(5000, self.update_time)

    def get_time_now(self):
        try:
            pcf85063 = PCF85063()
            rtcTime=pcf85063.readTime()
            time=f"{str(rtcTime[2])}:{str(rtcTime[1])}"
            # rtcTime=time.strftime("%Y-%m-%d %H:%M:%S")
            return time
        except Exception as ex:
            now = datetime.now()
            current_time = now.strftime("%H:%M")
            return current_time

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
            if remainVolt <= 10.0:
                if stateOfCharge !="CHARGING":
                    try:
                        with self.lock:
                            self.batery.i2c_send_turn_off()
                    except:
                        pass
                    os.system("sudo shutdown -h now")
        self.batLabel.after(10000, self.update_bat)

    def read_battery(self):
        global remainCap, stateOfCharge, remainVolt
        with self.lock:
            try:
                remainCap = round(self.batery.read_remain_cap())
                remainVolt=self.batery.read_voltage()
                if self.batery.read_current() > 0:
                    stateOfCharge = "CHARGING"
                else:
                    stateOfCharge = "DISCHARGE"
            except:
                pass
                # remainCap = 30
                # remainVolt = 3.0
                # stateOfCharge = "DISCHARGE"