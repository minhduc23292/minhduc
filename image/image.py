from tkinter import PhotoImage
import os
import matplotlib.pyplot as plt
current_directory = os.path.dirname(os.path.realpath(__file__))

class ImageAdrr():
    def __init__(self):
        self.settingPhoto = PhotoImage(file=f"{current_directory}\setting.png")
        self.smallSettingPhoto = PhotoImage(file=f"{current_directory}\small_setting.png")
        self.homePhoto = PhotoImage(file=f"{current_directory}\home.png")
        self.diagnosPhoto = PhotoImage(file=f"{current_directory}\diagnostic.png")
        self.balancePhoto = PhotoImage(file=f"{current_directory}\Balance.png")
        self.historyPhoto = PhotoImage(file=f"{current_directory}\History.png")
        self.resonacePhoto = PhotoImage(file=f"{current_directory}\\resonance.png")

        self.arrowPhoto = PhotoImage(file=f"{current_directory}\\arrow.png")
        self.low_bat = PhotoImage(file=f"{current_directory}\low_bat.png")
        self.half_bat = PhotoImage(file=f"{current_directory}\half_bat.png")
        self.full_bat = PhotoImage(file=f"{current_directory}\\full_bat.png")
        self.waitingPhoto = PhotoImage(file=f"{current_directory}\waiting.png")
        self.zoomPhoto = PhotoImage(file=f"{current_directory}\zoom.png")
        self.zoomIn = PhotoImage(file=f"{current_directory}\zoom.png")
        self.zoomOut = PhotoImage(file=f"{current_directory}\zoom.png")
        self.panLeft = PhotoImage(file=f"{current_directory}\zoom.png")
        self.panRight = PhotoImage(file=f"{current_directory}\zoom.png")
        self.savePhoto = PhotoImage(file=f"{current_directory}\save.png")
        self.fuction1 = PhotoImage(file=f"{current_directory}\zoom.png")

        self.noWifiImage = PhotoImage(file=f"{current_directory}\wifi-strength-off-outline.png")
        self.strongWifiImage = PhotoImage(file=f"{current_directory}\wifi-strength-4.png")
        self.mediumWifiImage = PhotoImage(file=f"{current_directory}\wifi-strength-3.png")
        self.weakWifiImage = PhotoImage(file=f"{current_directory}\wifi-strength-1.png")

        self.shutdownImage = PhotoImage(file=f"{current_directory}\Shutdown.png")
        self.restartImage = PhotoImage(file=f"{current_directory}\Restart.png")


        self.iso1Photo = plt.imread(f"{current_directory}\ISO10816-1.png")
        self.gePhoto = plt.imread(f"{current_directory}\gE_picture.png")
        self.iso2vPhoto = plt.imread(f"{current_directory}\Iso10816-2.png")
        self.iso2dPhoto = plt.imread(f"{current_directory}\Iso10816-2-dis.png")
        self.iso3vPhoto = plt.imread(f"{current_directory}\Iso10816-3.png")
        self.iso3dPhoto = plt.imread(f"{current_directory}\Iso10816-3-dis.png")
        self.iso4Photo = plt.imread(f"{current_directory}\Iso10816-4.png")
        self.iso5vPhoto = plt.imread(f"{current_directory}\Iso10816-5.png")
        self.iso5dPhoto = plt.imread(f"{current_directory}\Iso10816-5mount.png")
        self.iso7Photo = plt.imread(f"{current_directory}\Iso10816-7.png")
        self.iso8hPhoto = plt.imread(f"{current_directory}\Iso10816-8h.png")
        self.iso8vPhoto = plt.imread(f"{current_directory}\Iso10816-8v.png")
        self.iso21Photo = plt.imread(f"{current_directory}\iso10816-21.png")
        self.iso21Photo = plt.imread(f"{current_directory}\iso10816-21.png")