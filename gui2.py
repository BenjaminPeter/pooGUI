from Tkinter import *
import matplotlib
import sys
matplotlib.use('TkAgg')
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure


class SampleUI(Frame):
    def __init__(self, master=None):
        Frame.__init__(self,master, bd=2)
        
        self.label = Label(text="Sample1")
        self.label.grid()
class AppUI(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master, relief=SUNKEN, bd=2)

        self.menubar = Menu(self)

        menu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="File", menu=menu)
        menu.add_command(label="New")

        menu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Edit", menu=menu)
        menu.add_command(label="Cut")
        menu.add_command(label="Copy")
        menu.add_command(label="Paste")

        try:
            self.master.config(menu=self.menubar)
        except AttributeError:
            # master is a toplevel window (Python 1.4/Tkinter 1.63)
            self.master.tk.call(master, "config", "-menu", self.menubar)

        self.canvas = Canvas(self, bg="white",  height=400,
                             bd=0, highlightthickness=0)
        #self.canvas.pack()

        self.v_scale = Scale(master,orient=HORIZONTAL)
        self.npop_scale = Scale(master,orient=HORIZONTAL)

        self.canvas.grid(column=0,row=0,rowspan=4,sticky="N")
        self.v_scale.grid(column=1,row=0,sticky="NW")
        self.npop_scale.grid(column=1,row=1,sticky="NW")

#        self.sample1 = SampleUI(self)
        self.sample1 = Label(text="bla")
        self.sample1.grid(column=1,row=2,sticky="NW")

        
root = Tk()

app = AppUI(root)
app.grid()
#app.pack()

root.mainloop()
