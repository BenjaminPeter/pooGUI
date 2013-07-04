import Tkinter as tk
import matplotlib
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
from options import O

class PlotCanvas(tk.Frame):
    """Class wrapping matplotlib canvas"""
    def __init__(self, master, **kwargs):
        tk.Frame.__init__(self,master,bg="purple",**kwargs)
        self.fig = Figure(figsize=(5,5),dpi=200)
        self.panel = self.fig.add_subplot(111)

        self.xlim = O['xlim']
        self.ylim = O['ylim']
        self.panel.set_xlim(self.xlim)
        self.panel.set_ylim(self.ylim)
        self.panel.set_aspect(1)

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
        self.removeBGI()

        extent = [0,0,0,0]
        extent[:2] = O['xlim']
        extent[2:4] = O['ylim']
        #aspect calculations: we want the user defined coordinates to be
        #xlim and ylim, and the aspect ratio to be defined by the bgi
        aspect=(extent[3] - extent[2]) / float((extent[1] - extent[0]))
        aspect2=bgi.shape[1]/float(bgi.shape[0])
        self.bgi = self.panel.imshow(bgi, zorder=0, interpolation='nearest', extent=extent)
        print "added bgi, aspect=%f/%f"%(aspect,aspect2)
        if aspect2==1: aspect2=1.001
        self.aspect=1/aspect/aspect2
        self.panel.set_aspect(self.aspect)
        self.redraw()

    def removeBGI(self):
        try:
            self.bgi.remove()
            del self.bgi
        except AttributeError:
            pass
        extent = [0,0,0,0]
        extent[:2] = O['xlim']
        extent[2:4] = O['ylim']
        #aspect calculations: we want the user defined coordinates to be
        #xlim and ylim, and the aspect ratio to be defined by the bgi
        aspect=(extent[3] - extent[2]) / float((extent[1] - extent[0]))
        self.panel.set_aspect(1)
