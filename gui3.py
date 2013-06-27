from Tkinter import *
class PLTCanvas(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        f = Figure(figsize=(5,4), dpi=100)
        a = f.add_subplot(111)
        t = np.arange(0.0,3.0,0.01)
        s = np.sin(2*np.pi*t)
        a.plot(t,s)


        dataPlot = FigureCanvasTkAgg(f, master=master)
        dataPlot.show()
        #self = dataPlot.get_tk_widget()

class PooGUI(Frame):
    def __init__(self, master=None):
        Frame.__init__(self,master)
        self.master.title("POO")
        
        self.master.rowconfigure(0, weight=1)
        self.master.columnconfigure(0, weight=1)

        for i in range(2):
            self.master.button = Button(master, text = "Button {0}".format(i))
            self.master.button.grid(row=3, column=i, sticky=W+E)

        for r in range(4):
            self.master.rowconfigure(r,weight=1)
            self.master.columnconfigure(r,weight=1)

        self.Frame1 = Frame(master, bg="red")
        self.Frame1.b = Label(text="Label")
        self.Frame1.b.grid()
        self.Frame1.grid(row = 0, column = 0, rowspan = 3, columnspan = 1, sticky = W+E+N+S) 
        self.Frame2 = Frame(master, bg="blue")
        self.Frame2.grid(row = 0, column = 1, rowspan = 3, columnspan = 1, sticky = W+E+N+S)
        self.Frame3 = Frame(master, bg="green")
        self.Frame3.grid(row = 1, column = 1, rowspan = 6, columnspan = 3, sticky = W+E+N+S)

root = Tk()
app = PooGUI(master=root)
app.mainloop()

