import Tkinter as tk
import matplotlib
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure

class PlotCanvas(tk.Frame):
    """Class wrapping matplotlib canvas"""
    def __init__(self, master, **kwargs):
        tk.Frame.__init__(self,master,bg="purple",**kwargs)
        self.fig = Figure(figsize=(5,5),dpi=200)
        self.panel = self.fig.add_subplot(111)
        self.panel.set_xlim((0,100))
        self.panel.set_ylim((0,100))

        self.dataPlot = FigureCanvasTkAgg(self.fig, master=self)
        self.dataPlot.show()
        self.dataPlot.get_tk_widget().pack(fill=tk.BOTH, expand=1)


        self.visible = True

    def redraw(self):
        self.fig.canvas.draw()

    def hide(self):
        if self.visible:
            self.grid_forget()
            self.visible = False
            print "Canvas hidden"

    def show(self):
        if not self.visible:
            self.grid(column=0, row=0, rowspan=2)
            self.visible = True
            print "Canvas shown"

    def addBGI(self,bgi):
        self.panel.imshow(bgi, zorder=0, aspect='auto', interpolation='nearest', extent=[0,100,0,100])
        print "added bgi"
