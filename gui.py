import matplotlib
import sys
matplotlib.use('TkAgg')
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import Tkinter as tk
import tkMessageBox, tkFileDialog
from circle import *
from SampleUI import SampleUI
from hyperbola import Hyperbola
from matrix import SimpleTable

  
class PooGUI(tk.Frame):
    """the main frame with the GUI, contains three sections and a menu bar
        - the main section is the plotting area using matplotlib
        - in the top right are sliders,
        - bottom right is a list of samples

        we have the following objects:
            -sList: a list of all samples
            -hList: a list of all hyperbolas
            -data: the raw SNP data (mbsData obj?)
            -coords: data structure with coordinates
            -psi: np.array[s1,s2] : psi
            -sampNameDict: dict[sampName] -> sampId
            -v: constant multiplier of hyperbolas
            -xlim, ylim: plotting limits
        """
#---------------------------------------------------------------------
#   drawing stuff
#---------------------------------------------------------------------
    def setCoords(self):
        """
        this function updates the coordinates of the sample points, called on load
        """
        nCoords = self.coords.shape[0]
        for sampleUI in self.sList:
            sampleUI.destroy()
        self.sList, self.hList = [], []
        self.sampNameDict = {}
        for i in range(nCoords):
            self.sList.append( SampleUI(self.sample_frame,
                                        i,text=self.coords[i,0],
                                        x = self.coords[i,1],
                                        y=self.coords[i,2] ))
            self.sList[i].grid(column=0,row=i)
            self.panel.add_patch(self.sList[i].circ)
            self.sList[i].circ.connect()

            self.sampNameDict[self.sList[i].name] = i


    def drawCoords(self):
        self.fig.canvas.draw()

    def drawAllHyperbolas(self):
        for i in xrange(len(self.coords)-1):
            for j in xrange(i+1,len(self.coords)):
#        i,j = 0,1
                psi = self.psiDict[i,j]
                h = Hyperbola(self.panel,self.sList[i], self.sList[j], self.v,psi)
                #h = matplotlib.lines.Line2D(np.arange(0,100),np.random.normal(50,10,size = 100))
                self.sList[i].hyperbolas.append(h)
                self.sList[j].hyperbolas.append(h)
                self.hList.append(h)
                
                self.panel.add_line(h)
                
        self.fig.canvas.draw()


    def changeV(self,ele,val):
        """ 
        function that updates hyperbola when v is changed
        """

        #see if the value is actually a float, if not, return
        self.v = float( val.get() )
        #redraw, whole thing, there might be a more efficient way to do this
        self.redrawHyperbolas()
        self.fig.canvas.draw()
        #self.drawCoords()
        #self.circ.center = (float(x)
      
        
    def redrawHyperbolas(self):
        for h in self.hList:
            h.redraw(v = self.v)

    def optimizeAll(self):
        nCoords = len( self.coords )
        data = np.empty((nCoords * (nCoords -1 ) /2, 5 ))
        row = 0
        for h in self.hList:
            data[row] = h.F1[0], h.F1[1], h.F2[0], h.F2[1], h.psi
            row += 1
        print data
        import optimize
        e = optimize.tdoa3(data,x0=[100,50,50])
        print "---------------------"
        print e
        return data

#---------------------------------------------------------------------
#   loading files and data
#---------------------------------------------------------------------
    def loadSNP(self):
        """loads SNP and saves them in data"""
        f = tkFileDialog.askopenfile(mode='r')
        self.data = np.loadtxt(f)

    def loadCoords(self,f=None):
        """loads Coords and saves them in data"""
        if f is None:
            f = tkFileDialog.askopenfile(mode='r',initialfile="coords.txt")

        self.coords = np.loadtxt(f,dtype="S100")
        self.setCoords()
        self.drawCoords()
        self.nCoords = len(self.coords)

    def loadPsi(self,f=None):
        """loads Coords and saves them in data"""
        if f is None:
            f = tkFileDialog.askopenfile(mode='r',initialfile="psi.txt")

        nCoords = 1
        psiRaw = np.loadtxt(f, dtype="S100")
        psiDict = {}
        for row in psiRaw:
            psiDict[self.sampNameDict[row[0]],
                    self.sampNameDict[row[1]]] = float(row[2])
        self.psiDict = psiDict

        self.initPsiMatrix()
        
    def loadBGI(self):
        """loads Background image"""
        f = tkFileDialog.askopenfile(mode='r')
        self.bgi = np.loadtxt(f)
        


#---------------------------------------------------------------------
# various constructors
#---------------------------------------------------------------------

    def initPsiMatrix(self):
        """initializes Matrix containing psi values
        should do the following:
            1. display matrix of Edits? MatrixWidget
            2. load data and display it
            3. colorcode
        """
        pass
#        self.matrixTL = tk.Toplevel(self.master)
        #self.psiMat = SimpleTable(

    def initMenubar(self):
        """
        this function loads and populates the menubar, and will register its events
        """
        self.menubar = tk.Menu(self)

        menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="File", menu=menu)
        menu.add_command(label="Load SNP",command=self.loadSNP)
        menu.add_command(label="Load Coords", command=self.loadCoords)
        menu.add_command(label="Load Background Image", command=self.loadBGI)
        menu.add_command(label="Quit", command=self.quit)

        menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Edit", menu=menu)
        menu.add_command(label="Set Reference Coordinates")

        menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="View", menu=menu)
        menu.add_command(label="Hyperbolas")
        menu.add_command(label="Pairwise Psi")

        menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Run", menu=menu)
        menu.add_command(label="Find Origin All", command=self.optimizeAll)
        menu.add_command(label="Find Origin Visible")

        try:
            self.master.config(menu=self.menubar)
        except AttributeError:
            # master is a toplevel window (Python 1.4/Tkinter 1.63)
            self.master.tk.call(master, "config", "-menu", self.menubar)

    def initCanvas(self,master):
        """
        this function creates the matplotlib canvas that will be used 
        to draw stuff
        """
        self.fig = Figure(figsize=(3,3), dpi=200)
        self.panel = self.fig.add_subplot(111)
        #t = np.arange(0.0,100.0,1)
        #s = np.sin(2*np.pi*t/100.)*50+50
        #self.panel.plot(t,s)
        self.panel.set_xlim((0,100))
        self.panel.set_ylim((0,100))

        self.dataPlot = FigureCanvasTkAgg(self.fig, master=master)
        #self.dataPlot.mpl_connect('button_press_event',dummyCallBack)
        self.dataPlot.show()
        self.dataPlot.get_tk_widget().grid(column=0, row=0, rowspan=2)
        #self.dataPlot.get_tk_widget().pack()

    def initStatusbar(self,master):
        """function that creates a status bar at the bottom of the window"""
        pass
    
    def initSliderFrame(self,master):
        self.v = 100
        self.vI = tk.IntVar()
        self.vI.set( self.v )
        self.slider_frame = tk.Frame(master, width=200,heigh=500,bg="blue")
        self.v_scale = tk.Scale(self.slider_frame, orient=tk.HORIZONTAL,
                        bg="red", length=200, label="v", from_=1, to=1000, variable = self.vI)
        self.npop_scale = tk.Scale(self.slider_frame, orient=tk.HORIZONTAL,
                        length = 200, label="number of pops", from_=1, to=10)

        self.vI.trace("w",lambda a,b,c,n=self.v_scale:self.changeV(a,n))

        self.slider_frame.grid(column=1, row=0)
        #self.slider_frame.pack()
        self.v_scale.grid(column=0,row=0,sticky="ns")
        self.npop_scale.grid(column=0,row=1,sticky="ns")

    
    def initSampleFrame(self,master):
        self.sample_frame = tk.Frame(master, width=200, heigh=100, bg="green")
        self.sList = []
        for i in range(4):
            self.sList.append( SampleUI(self.sample_frame,i, text="SS%d"%i) )
            self.sList[i].grid(column=0,row=i)
            self.sampNameDict[self.sList[i].name] = i
        self.sample_frame.grid(column=1, row=1)
        #self.sample_frame.pack()

    def __init__(self, master=None):
        """the main constructor of the frame. As it is quite big,
        i split it up into subfunctions for the various ui parts.
        Might be worth to instead use children classes instead.

        The main app window will have a status bar at the bottom with
        progress messages and stuff. The main window will be
        the square matplotlib canvas on the right and a narrowish bar
        with samples, sliders, etc on the right
        """
        tk.Frame.__init__(self, master, relief=tk.SUNKEN, bd=2)

        self.master = master
        self.sampNameDict={}
        
        self.initMenubar()
        self.initCanvas(master)
        #self.initStatusbar(master)
        self.initSliderFrame(master)
        self.initSampleFrame(master)

        #enable expansion
        #tk.Grid.rowconfigure(self,0,weight=1)
        #tk.Grid.rowconfigure(self,1,weight=1)
        #tk.Grid.columnconfigure(self,1,weight=1)
        #tk.Grid.columnconfigure(self,0,weight=1)


#---------------------------------------------------------------------
#   other stuff
#---------------------------------------------------------------------
    def quit(self):
        """quits app"""
        print "bla"
        root.quit()
        root.destroy()

        
root = tk.Tk()

app = PooGUI(root)
#load some data
app.loadCoords("data.test.loc")
app.loadPsi("data.test.psi")
app.v = 200
app.drawAllHyperbolas()
#app.grid()
app.grid()

root.mainloop()
