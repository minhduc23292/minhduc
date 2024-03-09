import tkinter as Tk
from tkinter import ttk
import os
from i18n import _
from image.image import ImageAdrr
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from meanlab import Application

class HomePage(Tk.Frame):
    def __init__(self, parent: "Application"):
        super().__init__(parent)
        self.parent = parent
        imageAddress = ImageAdrr()
        self.settingPhoto = imageAddress.settingPhoto
        self.smallSePhoto = imageAddress.smallSettingPhoto
        self.meanLab=imageAddress.meanLab
        self.historyPhoto = imageAddress.historyPhoto

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

        homeLabel = ttk.Label(self.homeFrame, style='home.TLabel', text=" MEANLAB", image=self.meanLab,
                              compound=Tk.LEFT)
        homeLabel.place(relx=0.26, rely=0.11)

        self.historyButton = ttk.Button(self.homeFrame, style='home.TButton', text="VIBRATION\nMANAGERMENT", image=self.historyPhoto,
                                        compound=Tk.TOP, command=self.move_to_history_page)
        self.historyButton.place(relx=0.4, rely=0.42, width=200, height=150)

    def move_to_history_page(self):
        self.homeFrame.destroy()
        self.parent.go_to_history_page()