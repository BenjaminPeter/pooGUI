import Tkinter as tk
import matplotlib
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
from PWPsiLine import PWPsiLine
from hyperbola import Hyperbola

class PlotCanvas(tk.Frame):
    """Class wrapping matplotlib canvas"""
    def __init__(self, master, config, **kwargs):
        print "CONF", config.xlim
        tk.Frame.__init__(self,master,bg="purple",**kwargs)
        self.fig = Figure(figsize=(5,5),dpi=200)
        self.panel = self.fig.add_subplot(111)

        self.c = config
        self.xlim = config.xlim
        self.ylim = config.ylim
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
        extent[:2] = self.xlim
        extent[2:4] = self.ylim
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
        extent[:2] = self.c.xlim
        extent[2:4] = self.c.ylim
        #aspect calculations: we want the user defined coordinates to be
        #xlim and ylim, and the aspect ratio to be defined by the bgi
        aspect=(extent[3] - extent[2]) / float((extent[1] - extent[0]))
        self.panel.set_aspect(1)

class HyperbolaCanvas(PlotCanvas):
    """
        the canvas for the hyperbola plot, also keeps all the actual
        hyperbola objects
    """
    def __init__(self, master, config, samples, data, **kwargs):
        """
            samples is a list of all the samples that are present
            statObj is the object that will produce the stats
        """
        PlotCanvas.__init__(self,master,config,**kwargs)
        self.samples = samples
        self.d = data
        self.hList = []

    def draw_all_hyperbolas(self):
        for i, s1 in enumerate(self.samples):
            for s2 in self.samples[i+1:]:
                h = Hyperbola(s1, s2, self.d, self.c)
                s1.add_hyperbola(h)
                s2.add_hyperbola(h)
                self.hList.append(h)
                
                self.panel.add_line(h)
                
        if self.visible:
            self.redraw()

    def update_(self):
        for h in self.hList:
            h.update_()
    
class PWPCanvas(PlotCanvas):
    """
        the canvas for the pairwise psi plot, also keeps all the actual
        hyperbola objects
    """
    def __init__(self, master, config, samples, data, **kwargs):
        """
            samples is a list of all the samples that are present
            statObj is the object that will produce the stats
        """
        PlotCanvas.__init__(self,master,config,**kwargs)

        self.samples = samples
        self.d = data
        self.pList = []

    def update_(self):
        for l in self.pList:
            l.update_()

    def draw_all_pairwise_psi(self):
        """
            function that draws pairwise psi
                should eventually include filters for transitive
                reduction and mst to be drawn
        """
        for i, s1 in enumerate(self.samples):
            for s2 in self.samples[i+1:]:
                stat = self.d.get_default_stat(s1.name,s2.name)
                l = PWPsiLine( s1, s2, self.d, self.c)
                s1.add_line(l)
                s2.add_line(l)
                self.pList.append(l)
                
                self.panel.add_line(l)
                
        if self.visible:
            self.redraw()

