import tkinter as Tk
import matplotlib
matplotlib.use('TKAgg')
from matplotlib.figure import Figure
class creatFig():
    def __ini__(self):
        pass

    def creatFigure(self, num):
        ax = []
        fig1 = Figure(figsize=(8.1, 8))
        fig1.subplots_adjust(left=0.1, right=0.95, top=0.95, bottom=0.1, wspace=1, hspace=0.5)

        for idx in range(1, num + 1):
            ax.append(fig1.add_subplot(num, 1, idx))
        for idx in range(num):
            ax[idx].set_ylabel('')
            ax[idx].set_facecolor("white")
            ax[idx].grid()
        return fig1
