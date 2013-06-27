import Tkinter as tk
from circle import *
class SampleUI(tk.Frame):
    """this class represens a single sample with use checkbox, label, x and y coords"""
    def __init__(self, master=None, text="Sample",x=0,y=0):
        tk.Frame.__init__(self,master, bd=2,bg="blue")

        #coordinates in integers
        self.x = x
        self.y = y
        self.name = text
        #coordinates as strings, bound to xbox, ybox
        self.tX, self.tY = tk.StringVar(), tk.StringVar()

        #is visible?
        self.active = tk.IntVar()

        #setting up the widgets
        self.checkbox = tk.Checkbutton(self,bg="red", command=self.showhide, var=self.active,)
        self.checkbox.select()
        self.label = tk.Label(self,text=text)
        self.xbox = tk.Entry(self,width=7, textvariable = self.tX)
        self.xbox.insert(0,x)
        self.ybox = tk.Entry(self,width=7, textvariable = self.tY)
        self.ybox.insert(0,y)

        #registering events and layout
        self.tX.trace("w",lambda a,b,c,n=self.xbox:self.moved(a,n))
        self.tY.trace("w",lambda a,b,c,n=self.ybox:self.moved(a,n))
        self.checkbox.grid(column=0,row=0)
        self.label.grid(column=1,row=0)
        self.xbox.grid(column=2,row=0)
        self.ybox.grid(column=3,row=0)


        #the corresponding plot elements:
        #   - circ is the circle that is drawn
        #   - hyperbolas are the hyperbolas associated with this
        self.circ = DraggableCircle(self,(x,y),1)
        self.circ.sample = self


        self.hyperbolas = []

    def is_active(self):
        return self.active.get()

    #self[0] and self[1] return x and y
    def __getitem__(self,x):
        if x == 0:
            return float(self.x)
        if x == 1:
            return float(self.y)
    
    #function that is run when the coords of the dot are updated
    def moved(self,ele,val):
        #see if the value is actually a float, if not, return
        try:
            float(val.get())
        except:
            print "val", val
            return
        print ele, val

        #if x changed...
        if ele == str(self.tX):
            self.x = float(val.get())
            self.circ.center = (self.x,self.circ.center[1])
            print "cbx"
        #if y changed
        elif ele == str(self.tY):
            self.y = float(val.get())
            self.circ.center = (self.circ.center[0],self.y)
            print "cby"
        else: print "NO"

        #redraw, whole thing, there might be a more efficient way to do this
        self.redrawHyperbolas()
        self.circ.figure.canvas.draw()
        #self.drawCoords()
        #self.circ.center = (float(x)
      
       
    def showhide(self):
        """funcion that shows and hides this plot. It should do the following things:
        onhide:
        - 1. hide circle
        - 2. hide all hyperbolas
        onshow:
        - 1. show circle again
        - 2. show hyperbolas as long as the other focus is also active
        
        #maybe: update estimated origin
        """
        #todo
        if self.active.get():
            print "check, nHyp", len(self.hyperbolas)
            self.show()
        else:
            print "uncheck, nHyp", len(self.hyperbolas)
            self.hide()

    def hide(self):
        canvas = self.circ.figure.canvas
        print "CANVVAS", canvas
        self.circ.hide()
        for h in self.hyperbolas:
            h.set_visible(False)
        canvas.draw()

    def show(self):
        canvas = self.circ.figure.canvas
        self.circ.show()
        for h in self.hyperbolas:
            h.show()
        canvas.draw()

    def redrawHyperbolas(self):
        for h in self.hyperbolas:
            h.redraw(D=)
        self.circ.figure.canvas.draw()
