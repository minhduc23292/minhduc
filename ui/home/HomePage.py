import tkinter as Tk
import sv_ttk
from tkinter import ttk
from tkinter import PhotoImage
import os
from i18n import _
import matplotlib

matplotlib.use('TKAgg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import Axes3D, proj3d
from Calculation.calculate import *
# from ui.Diagnostic.DiagnosticPage import DiagnosticPage
import PlotData.PlotData as Pd
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main import Application
current_directory = os.getcwd()
parent_directory = os.path.dirname(os.path.dirname(current_directory))


class HomePage(Tk.Frame):
    def __init__(self, parent: "Application"):
        super().__init__(parent)
        self.parent = parent
        self.creat_home_page(self.parent.origin_config)
        sv_ttk.set_theme("light")

    def creat_home_page(self, origin_config):
        self.style = ttk.Style(self.parent)
        self.style.configure('home.TLabel', background='white', font=('Chakra Petch', 40))
        self.style.configure('bat.TLabel', background='grey95', font=('Chakra Petch', 12))
        self.settingPhoto = PhotoImage(file=f"{current_directory}\image\setting.png")
        self.smallSePhoto = PhotoImage(file=f"{current_directory}\image\small_setting.png")
        self.diagnosPhoto = PhotoImage(file=f"{current_directory}\image\diagnostic.png")
        self.balancePhoto = PhotoImage(file=f"{current_directory}\image\Balance.png")
        self.historyPhoto = PhotoImage(file=f"{current_directory}\image\History.png")
        self.resonacePhoto = PhotoImage(file=f"{current_directory}\image\\resonance.png")
        self.vector = PhotoImage(file=f"{current_directory}\image\Vector.png")

        self.homeFrame = Tk.Frame(self.parent, bd=1, bg='white', width=1024, height=600)
        self.homeFrame.pack()
        self.homeFrame.pack_propagate(0)

        self.batFrame = Tk.Frame(self.homeFrame, bd=1, bg='grey95', width=117, height=40)
        self.batFrame.pack()
        self.batFrame.place(relx=0.875, rely=0.01)
        self.batFrame.pack_propagate(0)

        homeLabel = ttk.Label(self.homeFrame, style='home.TLabel', text="Otani Analyzer", image=self.settingPhoto,
                              compound=Tk.LEFT)
        homeLabel.place(relx=0.28, rely=0.1)

        self.timeLabel = ttk.Label(self.batFrame, style='bat.TLabel', text="20:20")
        self.timeLabel.place(relx=0.05, rely=0.1)

        self.batLabel = ttk.Label(self.batFrame, style='bat.TLabel', text="20%", image=self.vector, compound=Tk.LEFT)
        self.batLabel.place(relx=0.5, rely=0.1)

        self.diagnosticButton = ttk.Button(self.homeFrame, style='home.TButton', text="Diagnostic",
                                           image=self.resonacePhoto, \
                                           compound=Tk.TOP, command=self.move_to_diagnostic_page)
        self.diagnosticButton.place(relx=0.21, rely=0.32, width=188, height=125)

        self.balancingButton = ttk.Button(self.homeFrame, style='home.TButton', text="Dynamic\nBalancing",
                                          image=self.balancePhoto, \
                                          compound=Tk.TOP, command=self.move_to_diagnostic_page)
        self.balancingButton.place(relx=0.578, rely=0.32, width=188, height=125)

        self.resonanceButton = ttk.Button(self.homeFrame, style='home.TButton', text="Resonance\nAnalysis",
                                          image=self.resonacePhoto, \
                                          compound=Tk.TOP, command=self.move_to_diagnostic_page)
        self.resonanceButton.place(relx=0.21, rely=0.59, width=188, height=125)

        self.historyButton = ttk.Button(self.homeFrame, style='home.TButton', text="History", image=self.historyPhoto, \
                                        compound=Tk.TOP, command=self.move_to_diagnostic_page)
        self.historyButton.place(relx=0.578, rely=0.59, width=188, height=125)

        self.settingButton = ttk.Button(self.homeFrame, style='home.TButton', text="Settings", image=self.smallSePhoto, \
                                        compound=Tk.LEFT, command=self.move_to_diagnostic_page)
        self.settingButton.place(relx=0.76, rely=0.86, width=210, height=52)

        self.style.configure('home.TButton', font=('Chakra Petch', 15), bordercolor='black', borderwidth=4,
                             justify=Tk.CENTER)
        self.style.map('home.TButton',
                       foreground=[('disabled', 'yellow'),
                                   ('pressed', 'blue'),
                                   ('active', 'blue')])

    def move_to_diagnostic_page(self):
        self.homeFrame.destroy()
        self.parent.go_to_diagnostic_page()

