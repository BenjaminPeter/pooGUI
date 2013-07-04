import Tkinter as tk
from circle import *
from Population import Population
from options import O


class SampleUI(tk.Frame):
    """this class represens a single sample with use checkbox, label, x and y coords"""
    def __init__(self, master=None, id=-1,text="Sample",x=0,y=0):
        tk.Frame.__init__(self,master, bd=2,bg="blue")
        
        #the sample id. Should be the index of self in PooGUI.sList
        self.id = id
        #coordinates in integers
        self.x = float(x)
        self.y = float(y)
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
        self.tX.set(x)
        self.ybox = tk.Entry(self,width=7, textvariable = self.tY)
        self.tY.set(y)


        #registering events and layout
        self.tX.trace("w",lambda a,b,c,n=self.xbox:self.moved(a,n))
        self.tY.trace("w",lambda a,b,c,n=self.ybox:self.moved(a,n))
        self.checkbox.grid(column=0,row=0)
        self.label.grid(column=1,row=0)
        self.xbox.grid(column=2,row=0)
        self.ybox.grid(column=3,row=0)


        #the corresponding plot elements:
        #   - circH is the circle that is drawn on hyperbola plot
        #   - circP is the circle that is drawn on PWPsi plot
        #   - hyperbolas are the hyperbolas associated with this
        self.circH = Point(self,(x,y))
        self.circP = Point(self,(x,y))
        self.circH.sample = self
        self.circP.sample = self


        self.hyperbolas = []
        self.psi_lines = []

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
        if Point.lock == self.circH or Point.lock == self.circP:
            return
        print "MOVE FIRED"
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
            self.circH.set_xdata([self.x])
            self.circP.set_xdata([self.x])
        #if y changed
        elif ele == str(self.tY):
            self.y = float(val.get())
            self.circH.set_ydata([self.x])
            self.circP.set_ydata([self.y])
        else: print "NO"

        #update, whole thing, there might be a more efficient way to do this
        self.updateHyperbolas()
        self.updatePsiLines()
        self.circH._update()
        self.circP._update()

        self.circH.figure.canvas.draw()
        self.circP.figure.canvas.draw()
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
        canvasH = self.circH.figure.canvas
        canvasP = self.circP.figure.canvas
        print "CANVVAS", canvasH, canvasP
        self.circH.hide()
        self.circP.hide()
        for h in self.hyperbolas:
            h.set_visible(False)
        for l in self.psi_lines:
            l.set_visible(False)
        canvasH.draw()
        canvasP.draw()

    def show(self):
        canvasH = self.circH.figure.canvas
        canvasP = self.circP.figure.canvas
        self.circH.show()
        self.circP.show()
        for h in self.hyperbolas:
            h.show()
        for l in self.psi_lines:
            l.show()
        canvasH.draw()
        canvasP.draw()

    def updateHyperbolas(self):
        for h in self.hyperbolas:
            h.hupdate()

    def updatePsiLines(self):
        for l in self.psi_lines:
            l.pupdate()

    def updateCircles(self):
        self.circH._update()
        self.circP._update()

    def add_line(self,l):
        self.psi_lines.append(l)
        self.circP.add_line(l)

    def add_hyperbola(self,h):
        self.hyperbolas.append(h)
        self.circH.add_line(h)


class SampleUIWPop(SampleUI):
    """
        simple subclass of SampleUI where x,y, name are replaced by 
        a Population object that can also be used for the class
    """
    def __init__(self, pop, master=None, id=-1):
        x,y = pop.location[:2] # just use first two locs
        text = pop.name
        SampleUI.__init__(self,master, id=id, text=text, x=x, y=y)
        
        self.pop = pop

        def __getitem__(self,x):
            print "SAMPLEUIWPOP.__getitem__", self.pop.location
            if x==0:
                return self.pop.location[0]
            elif x==1:
                return self.pop.location[1]

        def moved(self,ele, val):
            SampleUI.moved(ele,val)
            self.pop.location[0] = self.x
            self.pop.location[1] = self.y

            #delete x, y created by moved as they are saved in self.pop
            del self.x
            del self.y

class InferredOrigin(SampleUI):
    origin_counter = 0
    def __init__(self, master=None, text="Origin", x=0,y=0):
        SampleUI.__init__(self,master, text=text, x=x, y=y)
        self.circH.set_color("red")
        self.circP.set_color("red")
        
    """
        class that represents an inferred origin of a group
    """
