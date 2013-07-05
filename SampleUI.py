import Tkinter as tk
from circle import *
from Population import Population
from options import O
from SampleFrame import ClusterFrame,Cluster


class SampleUI(tk.Frame):
    sortStat = 'name'
    """this class represens a single sample with use checkbox, label, x and y coords"""
    def __init__(self, master=None, main=None, cluster=None,text="Sample",x=0,y=0, **kwargs):
        tk.Frame.__init__(self,master, bd=2, **kwargs)
        self.cluster = None
        self.main = main
        self.color = "red"
        self.cstr = "red"
        
        #coordinates in integers
        self.x = float(x)
        self.y = float(y)
        self.name = text
        self.stats = {'name': self.name}
        #coordinates as strings, bound to xbox, ybox
        self.tX, self.tY = tk.StringVar(), tk.StringVar()

        #is visible?
        self.active = tk.IntVar()

        #setting up the widgets
        self.checkbox = tk.Checkbutton(self,bg="red", command=self.showhide, var=self.active,)
        self.checkbox.select()
        self.label = tk.Label(self,text=text)
        self.xbox = tk.Entry(self,width=4, textvariable = self.tX)
        self.tX.set(x)
        self.ybox = tk.Entry(self,width=4, textvariable = self.tY)
        self.tY.set(y)


        #the corresponding plot elements:
        #   - circH is the circle that is drawn on hyperbola plot
        #   - circP is the circle that is drawn on PWPsi plot
        #   - hyperbolas are the hyperbolas associated with this
        self.circH = Point(self,(x,y))
        self.circP = Point(self,(x,y))
        self.circH.sample = self
        self.circP.sample = self

        

        #registering events and layout
        self.tX.trace("w",lambda a,b,c,n=self.xbox:self.moved(a,n))
        self.tY.trace("w",lambda a,b,c,n=self.ybox:self.moved(a,n))
        self.checkbox.grid(column=0,row=0)
        self.label.grid(column=1,row=0,sticky="nsew")
        self.xbox.grid(column=2,row=0)
        self.ybox.grid(column=3,row=0)
        tk.Grid.columnconfigure(self,1,weight=1)


        if cluster != None:
            cluster.add_pop(self)
            self.cluster_frame = ClusterFrame(self,self.cluster)
            self.cluster_frame.grid(in_=self,column=4,row=0)


        self.hyperbolas = []
        self.psi_lines = []

    def set_color(self, color):

        self.color = color
        cint = [min(255,c *256) for c in color]
        cstr =  '#%02x%02x%02x'%tuple(cint[:3])
        self.cstr = cstr
        self.config(bg=cstr)
        self.checkbox.config(bg=cstr)
        self.label.config(bg=cstr)
        self.circH.set_color(color)
        self.circP.set_color(color)

    def set_cluster(self, cluster):
        if self.cluster is not None:
            self.cluster.remove_pop(self)
        self.main.clusters.add(cluster)
        self.cluster = cluster
        if hasattr(self, 'cluster_frame'):
            self.cluster_frame.set_mincol(cluster.mincol)
            self.cluster_frame.set_maxcol(cluster.maxcol)

    def is_active(self):
        return self.active.get()

    #self[0] and self[1] return x and y
    def __getitem__(self,x):
        if x == 0:
            return self.get_x()
        if x == 1:
            return self.get_y()
    def get_x(self):
        return float(self.x)
    def get_y(self):
        return float(self.y)
    def set_x(self,x):
        self.x = x 
    def set_y(self,y):
        self.y = y
    def get_name(self):
        return self.name
    
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
            x = float(val.get())

            self.set_x( x )
            self.circH.set_xdata([x])
            self.circP.set_xdata([x])
        #if y changed
        elif ele == str(self.tY):
            y = float(val.get())
            self.set_y( y )
            self.circH.set_ydata([y])
            self.circP.set_ydata([y])
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

    def update_(self):
        self.updateHyperbolas()
        self.updatePsiLines()
        self.circH._update()
        self.circP._update()

        self.circH.figure.canvas.draw()
        self.circP.figure.canvas.draw()
        if self.main is not None:
            self.main.update_sample_order()

    def add_line(self,l):
        self.psi_lines.append(l)
        self.circP.add_line(l)

    def add_hyperbola(self,h):
        self.hyperbolas.append(h)
        self.circH.add_line(h)


    ####################################################
    # sorting stuff and  1 sample statistics
    ###################################################

    def __lt__(self, other):
        if self.cluster == other.cluster:
            return self.stats[SampleUI.sortStat] < \
                    other.stats[SampleUI.sortStat]
        else: 
            return self.cluster < other.cluster


class SampleUIWPop(SampleUI):
    """
        simple subclass of SampleUI where x,y, name are replaced by 
        a Population object that can also be used for the class
    """
    def __init__(self, pop, master=None, main=None, cluster=None):
        x,y = pop.location[:2] # just use first two locs
        text = pop.name
        self.pop = pop
        SampleUI.__init__(self,master, cluster=cluster, main=main,text=text, x=x, y=y)
        

    def get_x(self):
        return float(self.pop.location[0])
    def get_y(self):
        return float(self.pop.location[1])
    def set_x(self,x):
        self.pop.location[0] = x 
    def set_y(self,y):
        self.pop.location[1] = y

    def get_name(self):
        return self.pop.name


class InferredOrigin(SampleUI):
    origin_counter = 0
    def __init__(self, master=None, main=None, cluster=None, text="Origin", x=0,y=0, color="red", **kwargs):
        SampleUI.__init__(self,master, main=main, cluster=cluster, text=text, x=x, y=y, **kwargs)
        self.circH.set_color("red")
        self.circP.set_color("red")
        self.circH.set_marker("+")
        self.circP.set_marker("+")
        self.circH.set_markeredgecolor("red")
        self.circP.set_markeredgecolor("red")
        
    """
        class that represents an inferred origin of a group
    """
