import tkinter as Tk
from tkinter import ttk
import os
from i18n import _
from image.image import ImageAdrr
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from main import Application

class HomePage(Tk.Frame):
    def __init__(self, parent: "Application"):
        super().__init__(parent)
        self.parent = parent
        imageAddress = ImageAdrr()
        self.settingPhoto = imageAddress.settingPhoto
        self.smallSePhoto = imageAddress.smallSettingPhoto
        self.diagnosPhoto = imageAddress.diagnosPhoto
        self.balancePhoto = imageAddress.balancePhoto
        self.historyPhoto = imageAddress.historyPhoto
        self.resonacePhoto = imageAddress.resonacePhoto
        self.creat_home_page(self.parent.origin_config)

    def creat_home_page(self, origin_config):
        global remainCap
        self.style = ttk.Style(self.parent)
        self.style.configure('home.TLabel', background='white', font=('Chakra Petch', 40))
        self.style.configure('home.TButton', font=('Chakra Petch', 18), bordercolor='black', borderwidth=1,
                             justify=Tk.CENTER)
        self.homeFrame = Tk.Frame(self.parent, bd=1, bg='white', width=1024, height=600)
        self.homeFrame.pack()
        self.homeFrame.pack_propagate(0)

        homeLabel = ttk.Label(self.homeFrame, style='home.TLabel', text="Vibration Expert", image=self.settingPhoto,
                              compound=Tk.LEFT)
        homeLabel.place(relx=0.24, rely=0.1)

        self.diagnosticButton = ttk.Button(self.homeFrame, style='home.TButton', text=_("Diagnostic"),
                                           image=self.diagnosPhoto,
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