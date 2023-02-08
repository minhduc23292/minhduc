import tkinter as Tk
# import sv_ttk
from tkinter import ttk
import os
from i18n import _
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main import Application
from keyboard.keyboard import KeyBoard
import wifi.wiless
from time import sleep
import pms.popMessage as pms
from pathlib import Path
import json
import sys
from image.image import ImageAdrr
import threading
from threading import Lock
from bateryMonitor.powerManager import *
from ds3231.ds3231B import DS3231
remainCap = 50
remainVolt = 3.8
stateOfCharge = "CHARGING"
firstTime = True
current_directory = os.getcwd()
parent_directory = os.path.dirname(os.path.dirname(current_directory))

def testVal(inStr, acttyp):
    if acttyp == '1':  # insert
        if not inStr.isdigit():
            return False
    return True


class SettingPage(Tk.Frame):
    def __init__(self, parent: "Application"):
        # sv_ttk.set_theme("light")
        self.parent = parent
        self.lock = Lock()
        self.batery=BQ27510()
        self.read_battery()
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
        self.btstyle.configure('bat.TLabel', font=('Chakra Petch', 13))
        self.btstyle.configure('normal.TLabel', font=('Chakra Petch', 12), background='white')

        self.mainFrame = Tk.Frame(self.parent, bd=1, bg='white', width=1024, height=600)
        self.mainFrame.pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)
        self.mainFrame.pack_propagate(0)

        self.featureFrame = Tk.Frame(self.mainFrame, bd=1, bg='white', width=1024, height=80)
        self.featureFrame.pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)
        self.featureFrame.pack_propagate(0)

        self.settingFrame = Tk.Frame(self.mainFrame, bd=1, bg='white', width=1024, height=520)
        self.settingFrame.pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)
        self.settingFrame.pack_propagate(0)

        self.batFrame = Tk.Frame(self.featureFrame, bd=1, bg='grey95', width=117, height=35)
        self.batFrame.pack()
        self.batFrame.place(relx=0.89, rely=0.0)
        self.batFrame.pack_propagate(0)

        self.creat_setting_feature_panel()
        self.notebook = CreatTab(self.settingFrame)
        self.generalConfigFrame=GeneralConfig(self.notebook.tab1, self.parent.origin_config)
        self.generalConfigFrame.pack(side=Tk.LEFT, fill=Tk.BOTH, expand=1)
        self.wifiConfigFrame=WifiConfig(self.notebook.tab2).pack(side=Tk.LEFT, fill=Tk.BOTH, expand=1)
        self.powerConfigFrame=Power(self.notebook.tab4, self.lock, self.batery).pack(side=Tk.LEFT, fill=Tk.BOTH, expand=1)
        self.languageConfigFrame=LanguageConfig(self.notebook.tab3, self.parent.origin_config.language_config_struct)
        self.languageConfigFrame.pack(side=Tk.LEFT, fill=Tk.BOTH, expand=1)
        self.parent.bind_class('TEntry', "<FocusIn>", self.show_key_board)
        self.parent.bind_class('TCombobox', "<<ComboboxSelected>>", self.change_state)

    def show_key_board(self, event):
        self.generalConfigFrame.applyButton.configure(state='normal')
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
        global remainCap
        self.timeLabel = ttk.Label(self.batFrame, style='bat.TLabel', text=self.get_time_now())
        self.timeLabel.after(5000, self.update_time)
        self.timeLabel.place(relx=0.05, rely=0.1)

        self.batLabel = ttk.Label(self.batFrame, style='bat.TLabel', text=f"{str(remainCap)}%", image=self.full_bat, compound=Tk.LEFT)
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

        self.configBt = ttk.Button(self.featureFrame, style='Accent.TButton', text="Setting")
        self.configBt.place(relx=0.122, rely=0.018, width=115, height=72)


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
            self.batLabel.configure(text=f"{int(averageCapacity)}%", image=self.full_bat, compound=Tk.LEFT)
        elif 30<=averageCapacity<70:
            self.batLabel.configure(text=f"{int(averageCapacity)}%", image=self.half_bat, compound=Tk.LEFT)
        else:
            self.batLabel.configure(text=f"{int(averageCapacity)}%", image=self.low_bat, compound=Tk.LEFT)
            if firstTime:
                pms.general_warning(_("Low Battery! Plug in the charger to keep it running"))
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
    def go_home(self):
        self.mainFrame.destroy()
        self.parent.go_to_home_page()

class GeneralConfig(Tk.Frame):
    def __init__(self, parent, origin_config):
        super().__init__(parent, width=1024, height=350, bg="white")
        self.creat_genral_config_page(origin_config)

    def creat_genral_config_page(self, origin_config):
        self.prjParam1 = Tk.StringVar()
        self.prjParam2 = Tk.StringVar()
        self.prjParam3 = Tk.StringVar()
        self.prjParam1.set(origin_config.project_struct["ProjectCode"])
        self.prjParam2.set(origin_config.project_struct["CompanyName"])
        self.prjParam3.set(origin_config.project_struct["Note"])

        projectFrame = ttk.LabelFrame(self, text='Project config')
        projectFrame.grid(column=0, row=0, padx=10, pady=10, columnspan=2, sticky='wn')

        prjCodeLabel = ttk.Label(projectFrame, text=_('Project Code*'), style='white.TLabel')
        prjCodeLabel.grid(column=0, row=0, padx=10, pady=5, sticky='w')

        prjCodeEntry = ttk.Entry(projectFrame, width=30, textvariable=self.prjParam1, takefocus=False)
        # prjCodeEntry['validatecommand'] = (prjCodeEntry.register(testVal), '%P', '%d')
        prjCodeEntry.grid(column=1, row=0, padx=10, pady=5, sticky='e')

        companyLabel = ttk.Label(projectFrame, text=_('Company Name'), style='white.TLabel')
        companyLabel.grid(column=0, row=1, padx=10, pady=5, sticky='w')

        companyEntry = ttk.Entry(projectFrame, width=30, textvariable=self.prjParam2, takefocus=False)
        companyEntry.grid(column=1, row=1, padx=10, pady=5, sticky='e')

        noteLabel = ttk.Label(projectFrame, text=_('Note'), style='white.TLabel')
        noteLabel.grid(column=0, row=2, padx=10, pady=5, sticky='w')

        noteEntry = ttk.Entry(projectFrame, width=30, textvariable=self.prjParam3, takefocus=False)
        noteEntry.grid(column=1, row=2, padx=10, pady=5, sticky='e')

        self.applyButton = ttk.Button(projectFrame, text="APPLY", style="Accent.TButton",
                                      command=lambda: self.on_apply_button_clicked(origin_config))
        self.applyButton.grid(column=1, row=3, padx=10, pady=20, ipady=5, sticky='ew')


    def on_apply_button_clicked(self, origin_config):
        if self.prjParam2.get()!='':
            origin_config.project_struct["CompanyName"] = self.prjParam2.get()
        if self.prjParam1.get()!='':
            origin_config.project_struct["ProjectCode"] = self.prjParam1.get()
        if self.prjParam3.get()!='':
            origin_config.project_struct["Note"] = self.prjParam3.get()
        self.applyButton.configure(state="disable")


class CreatTab(ttk.Notebook):
    def __init__(self, parent):
        self.style=ttk.Style()
        self.style.configure('TNotebook.Tab', font=('Chakra Petch', 15), borderwidth=0)
        super().__init__(parent, cursor="arrow", height=2000, width=200, style='TNotebook')
        self.creatTab()


    def creatTab(self):
        self.tab1 = Tk.Frame(self, name="general", relief="raised", borderwidth=0)
        self.tab2 = Tk.Frame(self, name="wifi", relief="raised", borderwidth=0)
        self.tab3 = Tk.Frame(self, name="power", relief="raised", borderwidth=0)
        self.tab4 = Tk.Frame(self, name="language", relief="raised", borderwidth=0)
        self.add(self.tab1, text=_("GENERAL"))
        self.add(self.tab2, text=_("WIFI"))
        self.add(self.tab3, text=_("LANGUAGE"))
        self.add(self.tab4, text=_("POWER"))
        self.pack(side='bottom', fill="both", padx=0, pady=0, expand=0)


class WifiConfig(Tk.Frame):
    def __init__(self, parent):
        self.style = ttk.Style()
        self.style.configure('wifi.TLabel', font=('Chakra Petch', 13))
        self.style.configure('wifi.TLabelframe', font=('Chakra Petch', 15))
        self.style.configure('wifi.TButton', font=('Chakra Petch', 15), width=40, height=40)

        super().__init__(parent, width=1024, height=350, bg="white", bd=0)
        self.creat_wifi_page()
        self.focus()

    def creat_wifi_page(self):
        imageAddress = ImageAdrr()
        connectingSsid = None
        infoText = "No wifi connection"
        self.wilessParam1 = Tk.StringVar()
        self.wilessParam2 = Tk.StringVar()
        try:
            connectingSsid = wifi.wiless._get_wifi_status()
            infoText = f'WIFI: {connectingSsid["ssid"]}'

            self.wifiImage = imageAddress.noWifiImage
            if connectingSsid["ssid"] != "":
                if connectingSsid["quality"] > 0.7:
                    self.wifiImage = imageAddress.strongWifiImage
                elif connectingSsid["quality"] <= 0.7 and connectingSsid["quality"] > 0.3:
                    self.wifiImage = imageAddress.mediumWifiImage
                else:
                    self.wifiImage = imageAddress.weakWifiImage
        except:
            self.wifiImage = imageAddress.noWifiImage

        wifiLableFrame = ttk.LabelFrame(self, text='Wifi config', style="wifi.TLabelframe")
        wifiLableFrame.grid(column=0, row=0, padx=10, pady=5, columnspan=2, sticky='wn')

        wifiLabel = ttk.Label(wifiLableFrame, text=infoText, style="wifi.TLabel")
        wifiLabel.grid(column=0, row=0, padx=10, pady=5, sticky='w')

        self.imageButton1 = ttk.Button(wifiLableFrame, text="", image=self.wifiImage, style="wifi.TButton")
        self.imageButton1.grid(column=1, row=0, padx=10, pady=5, sticky='e')
        self.imageButton1.image=self.wifiImage

        ssidLabel = ttk.Label(wifiLableFrame, text="ID", style="wifi.TLabel")
        ssidLabel.grid(column=0, row=1, padx=10, pady=5, sticky='w')
        ssidCombo = ttk.Combobox(wifiLableFrame, width=14, textvariable=self.wilessParam1, state="readonly",
                                 font=("Chakra Petch", 15), takefocus=False)
        try:
            ssidCombo['value'] = wifi.wiless._scan_networks()
        except:
            ssidCombo['value'] = ("None",)
        ssidCombo.grid(column=1, row=1, padx=10, pady=5, sticky="e")

        passwordLabel = ttk.Label(wifiLableFrame, text=_("Password"), style="wifi.TLabel")
        passwordLabel.grid(column=0, row=2, padx=10, pady=5, sticky='w')

        passwordEntry = ttk.Entry(wifiLableFrame, width=17, textvariable=self.wilessParam2, takefocus=False)
        passwordEntry.grid(column=1, row=2, padx=10, pady=5, ipadx=2, sticky='e')
        # wilessCancelButton = Tk.Button(wifiLableFrame, text=_("Cancel"), width=11, height=3,
        #                                activebackground='yellow',
        #                                bg="lavender", state='normal', command=self.cancel_button)
        # wilessCancelButton.grid(column=0, row=3, padx=0, pady=10, sticky='w')

        wilessConnectButton = ttk.Button(wifiLableFrame, text=_("Connect"), command=self.connection, style="Accent.TButton")
        wilessConnectButton.width=50
        wilessConnectButton.grid(column=0, row=3, padx=0, pady=10, ipadx=20, ipady=5, sticky='e')

        wilessDisconnectButton = ttk.Button(wifiLableFrame, text=_("Disconnect"), command=self.disconnect, style="Accent.TButton")
        wilessDisconnectButton.grid(column=1, row=3, padx=10, pady=10, ipadx=14, ipady=5, sticky='e')

    def connection(self):
        try:
            current_connection = wifi.wiless._get_wifi_status()

            current_ssid = current_connection["ssid"]
            newSsid = self.wilessParam1.get()
            newPassword = self.wilessParam2.get()
            if newSsid != current_ssid and newSsid != "" and newPassword != "":
                wifi.wiless._disconnect(current_ssid)
                sleep(1)
                wifi.wiless._connect(newSsid, newPassword)
            else:
                pass

        except Exception as ex:
            print("wifi conection function error")
            print(ex)

    def disconnect(self):
        try:
            current_connection = wifi.wiless._get_wifi_status()

            current_ssid = current_connection["ssid"]
            if current_ssid != "":
                wifi.wiless._disconnect(current_ssid)
                sleep(1)
            else:
                pass
        except Exception as ex:
            print("wifi conection function error")
            print(ex)

class Power(Tk.Frame):
    def __init__(self, parent, lock, batery):
        self.lock=lock
        self.batery=batery
        self.style = ttk.Style()
        self.style.configure('power.TLabel', font=('Chakra Petch', 13))
        self.style.configure('power.TLabelframe', font=('Chakra Petch', 15))
        self.style.configure('power.TButton', font=('Chakra Petch', 20))
        super().__init__(parent, width=1024, height=423, bg="white", bd=0)
        self.creat_power_page()
        self.focus()

    def creat_power_page(self):
        imageAdress=ImageAdrr()
        shutdownImage=imageAdress.shutdownImage
        shutdownButton=ttk.Button(self, text="SHUTDOWN", compound=Tk.TOP, image=shutdownImage, style="power.TButton",
                                  command=self.on_shutdown_button_clicked)
        shutdownButton.image=shutdownImage
        shutdownButton.place(x=280, y=140, width=190, height=172)

        restartImage = imageAdress.restartImage
        restartButton = ttk.Button(self, text="RESTART", compound=Tk.TOP, image=restartImage, style="power.TButton",
                                   command=self.on_restart_button_clicked)
        restartButton.image=restartImage
        restartButton.place(x=518, y=140, width=190, height=172)

    def on_shutdown_button_clicked(self):
        if (pms.company_project_shutdown_warning()):
            with self.lock:
                self.batery.i2c_send_turn_off()
            os.system("sudo shutdown -h now")
        else:
            pass
    def on_restart_button_clicked(self):
        if (pms.general_warning("Do you want to restart the device")):
            os.system("sudo shutdown -r now")
        else:
            pass

class LanguageConfig(Tk.Frame):
    def __init__(self, parent, language_config_struct):
        json_filename = current_directory + '/i18n/language.json'
        self.json_pathname = Path(json_filename)
        self.main_pathname = Path(current_directory + '/main.py')
        self.style = ttk.Style()
        self.style.configure('language.TLabel', font=('Chakra Petch', 13))
        self.style.configure('language.TLabelframe', font=('Chakra Petch', 15))
        self.style.configure('language.TButton', font=('Chakra Petch', 20))
        super().__init__(parent, width=1024, height=432, bg='white', bd=0)
        self.creat_language_page(language_config_struct)
    def creat_language_page(self, language_config_struct):

        self.languageParam1=Tk.StringVar()
        with open(self.json_pathname, 'r', encoding='utf-8') as f:
            currentLanguage = json.load(f)
        self.languageParam1.set(currentLanguage["Language"])
        languageLabelFrame=ttk.LabelFrame(self, text="Language")
        languageLabelFrame.grid(column=0, row=0, padx=10, pady=5, columnspan=2, sticky='wn')
        languageLabel=ttk.Label(languageLabelFrame, text="Language", style="language.TLabel")
        languageLabel.grid(column=0, row=0, padx=10, pady=5, sticky='w')
        languageCombo=ttk.Combobox(languageLabelFrame, width=14, textvariable=self.languageParam1, state="readonly",
                                 font=("Chakra Petch", 15), takefocus=False)
        languageCombo["value"]=('ENGLISH','JAPANESE','VIETNAMESE')
        languageCombo.grid(column=1, row=0, padx=10, pady=5, sticky='e')
        languageButton=ttk.Button(languageLabelFrame, text="Apply", style="Accent.TButton",
                                  command=lambda:self.on_apply_button_clicked(language_config_struct))
        languageButton.grid(column=1, row=1, padx=10, pady=10, ipadx=20, ipady=5, sticky='e')

    def on_apply_button_clicked(self, language_config_struct):
        language_config_struct["Language"] = self.languageParam1.get()
        LanguageJson = {"Language": language_config_struct["Language"]}
        with open(self.json_pathname, 'r', encoding='utf-8') as f:
            cauhinh = json.load(f)
        preLanguage = cauhinh["Language"]
        with open(self.json_pathname, 'w', encoding='utf-8') as f:
            json.dump(LanguageJson, f)
        if language_config_struct["Language"] != preLanguage:
            if pms.general_warning(_("Restart is required to change the language. Do you want to restart now")):
                os.execl('/usr/bin/python', self.main_pathname, *sys.argv)
            else:
                pass
