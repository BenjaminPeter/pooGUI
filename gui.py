import matplotlib
import sys
matplotlib.use('TkAgg')
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import Tkinter as tk
import tkMessageBox, tkFileDialog
from circle import *
from SampleUI import *
from hyperbola import Hyperbola
from PWPsiLine import PWPsiLine
from matrix import SimpleTable
from StatusBar import StatusBar
from PlotCanvas import PlotCanvas
from SampleFrame import SampleFrame
from SliderFrame import SliderFrame
from options import O
import matplotlib.image as mpimg
from Data import *
from Population import Population
from optimize import *
import optimize

  
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
    #active canvas for redrawing
    activeCanvas = None
#---------------------------------------------------------------------
#   drawing stuff for points, should eventually be moved to an 
#       appropriate plotting class,psi, data
#---------------------------------------------------------------------



    def changeV(self,ele,val):
        """ 
        function that updates hyperbola when v is changed
        """

        #see if the value is actually a float, if not, return
        self.v = float( val.get() )
        #update, whole thing, there might be a more efficient way to do this
        self.updateHyperbolas()
        if self.activeCanvas == self.canvasH:
            self.activeCanvas.redraw()

    def changeLwd(self,val):
        """ 
        function that updates hyperbola when v is changed
        """

        print "Changing lwd" , val.get()
        #see if the value is actually a float, if not, return
        self.lwd = float( val.get() )
        #redraw, whole thing, there might be a more efficient way to do this
        self.updatePsiLines()
        if self.activeCanvas ==self.canvasPsi:
            self.activeCanvas.redraw()
      
    def changeThreshold(self,val):
        """ 
        function that updates hyperbola when v is changed
        """

        print "Changing threshold" , val.get()
        #see if the value is actually a float, if not, return
        self.threshold = float( val.get() )
        #update, whole thing, there might be a more efficient way to do this
        self.updatePsiLines()

        if self.activeCanvas ==self.canvasPsi:
            self.activeCanvas.redraw()
#---------------------------------------------------------------------
#   optimizing
#---------------------------------------------------------------------
    def optimizeAll(self):
        nCoords = self.nCoords
        data = np.empty((nCoords * (nCoords -1 ) /2, 5 ))
        row = 0
        for h in self.hList:
            data[row] = h.F1[0], h.F1[1], h.F2[0], h.F2[1], h.psi
            row += 1
        e,mse,p,d = optimize.tdoa3(data,x0=O["opt_start"])
        print "---------------------"
        print e[0]
        opt = InferredOrigin(x=e[0][1],y=e[0][2])
        self.canvasH.panel.add_artist( opt.circH )
        self.canvasPsi.panel.add_artist( opt.circP )
        opt.circH.connect()
        opt.circP.connect()
        self.activeCanvas.redraw()
        return e[0], mse, p, d

#---------------------------------------------------------------------
#   drawing stuff for hyperbolas, should eventually be 
#       moved to an appropriate plotting class
#---------------------------------------------------------------------
    def drawAllHyperbolas(self):
        for i, s1 in enumerate(self.sList):
            for s2 in self.sList[i+1:]:
#        i,j = 0,1
                psi = self.psi[s1.pop,s2.pop]
                h = Hyperbola(self.canvasH.panel, s1, s2, self, self.psi)
                #h = matplotlib.lines.Line2D(np.arange(0,100),np.random.normal(50,10,size = 100))
                s1.add_hyperbola(h)
                s2.add_hyperbola(h)
                self.hList.append(h)
                
                self.canvasH.panel.add_line(h)
                
        if self.activeCanvas == self.canvasH:
            self.activeCanvas.redraw()

    def updateHyperbolas(self):
        for h in self.hList:
            h.hupdate()

    def updatePsiLines(self):
        for l in self.pList:
            l.pupdate(weight=self.lwd, threshold=self.threshold)

#---------------------------------------------------------------------
#   drawing stuff for pw psi, should eventually be 
#       moved to an appropriate plotting class
#---------------------------------------------------------------------
    def drawAllPairwisePsi(self):
        """
            function that draws pairwise psi
                should eventually include filters for transitive
                reduction and mst to be drawn
        """
        for i, s1 in enumerate(self.sList):
            for s2 in self.sList[i+1:]:
#        i,j = 0,1
                psi = self.psi[s1.pop, s2.pop]
                l = PWPsiLine(self.canvasH.panel,
                              s1, s2, self.psi)
                s1.add_line(l)
                s2.add_line(l)
                self.pList.append(l)
                
                self.canvasPsi.panel.add_line(l)
                
        if self.canvasPsi == self.activeCanvas:
            self.canvasPsi.redraw()


#------------------------------------Hyperbola---------------------------------
#   loading files and data
#---------------------------------------------------------------------
    def loadSNP(self):
        """loads SNP and saves them in data"""
        f = tkFileDialog.askopenfile(mode='r')
        self.data = np.loadtxt(f)

    def loadCoords(self,f=None):
        """loads Coords, creates the corresponding UI elements
            and the circles for plotting
        """

        self.popOrder = {}

        #reset everything:
        for sampleUI in self.sList:
            sampleUI.destroy()
        self.sList, self.hList, self.pList = [], [], []

        if f is None:
            f = tkFileDialog.askopenfile(mode='r',initialfile="coords.txt")

        for i,line in enumerate(open(f)):
            p = Population()
            p.load_line(line)

            #popOrder is a dict[Population] => ordering index
            self.popOrder[ p ] = i
            sUI = SampleUIWPop(pop=p, master=self.sample_frame)
            sUI.grid(column=0,row=i, sticky="ew")

            #create plotting circles and register events
            self.canvasH.panel.add_artist( sUI.circH )
            self.canvasPsi.panel.add_artist( sUI.circP )
            sUI.circH.connect()
            sUI.circP.connect()
            
            self.sList.append( sUI )

        self.nCoords = len( self.sList )
        self.activeCanvas.redraw()

    def loadPsi(self,f=None):
        """loads Psi directly. Assumes Coordinates are already loaded"""
        if f is None:
            f = tkFileDialog.askopenfile(mode='r',initialfile="psi.txt")

        self.psi = AntiCommutativePWStat(f=pw_psi)
        psiRaw = np.loadtxt(f, dtype="S100")
        for row in psiRaw:
            self.psi[ row[0], row[1] ] =  float(row[2])

        self.initPsiMatrix(self.master)
        
    def loadBGI(self, f=None):
        """loads Background image"""
        if f is None:
            f = tkFileDialog.askopenfile(mode='r')

        try:
            self.bgi = mpimg.imread(f)
        except:
            raise ValueError("could not read image file, see"+ \
                             " matplotlib.image.imread for"+ \
                             " supported formats")
        self.canvasH.addBGI(self.bgi)
        self.canvasPsi.addBGI(self.bgi)

    def removeBGI(self):
        self.canvasH.removeBGI()
        self.canvasPsi.removeBGI()
        self.activeCanvas.redraw()

        


#---------------------------------------------------------------------
# various constructors
#---------------------------------------------------------------------

    def initPsiMatrix(self,master):
        """initializes Matrix containing psi values
        should do the following:
            1. display matrix of Edits? MatrixWidget
            2. load data and display it
            3. colorcode
        """
        pass
        self.matrixTL = tk.Toplevel(master)
        self.psiMat = SimpleTable(self.matrixTL)
        self.psiMat.grid(sticky="nsew")
        self.psiMat.fill(self)
        self.psiMat.fillLabels(self)
        "psi filled"

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
        menu.add_command(label="Hyperbolas", 
                         command=self.showHyperbolaCanvas)
        menu.add_command(label="Pairwise Psi", 
                         command=self.showPsiCanvas)

        menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Run", menu=menu)
        menu.add_command(label="Find Origin All", command=self.optimizeAll)
        menu.add_command(label="Find Origin Visible")

        try:
            self.master.config(menu=self.menubar)
        except AttributeError:
            # master is a toplevel window (Python 1.4/Tkinter 1.63)
            self.master.tk.call(master, "config", "-menu", self.menubar)

    def initCanvasHyperbolas(self,master, active=False):
        """
        this function creates the matplotlib canvas that will be used 
        to draw stuff
        master: parent frame
        active: is this displayed on startup?
        """
        self.canvasH = PlotCanvas(master, width=300, height=300)
        self.canvasH.grid(column=0,row=0,rowspan=2,sticky="ewns")
        if not active:
            self.canvasH.hide()
        else:
            self.activeCanvas = self.canvasH

    def initCanvasPairwisePsi(self,master, active=False):
        """
        this function creates the matplotlib canvas that will be used 
        to draw stuff
        master: parent frame
        active: is this displayed on startup?
        """
        self.canvasPsi = PlotCanvas(master, width=300, height=300)
        self.canvasPsi.grid(column=0,row=0,rowspan=2,sticky="ewns")
        if not active:
            self.canvasPsi.hide()
        else:
            self.activeCanvas = self.canvasPsi

    def initStatusbar(self,master):
        """function that creates a status bar at the bottom of the window"""
        self.sb = StatusBar(self)
        self.sb.grid(row=2,column=0,columnspan=2, sticky="ew")
    
    def initSliderFrame(self,master):
        self.v = 100
        self.slider_frame = SliderFrame(master,self, v=self.v)
        self.slider_frame.grid(column=1, row=0, sticky="")
    
    def initSampleFrame(self,master):
        self.sample_frame = SampleFrame(master, width=200, height=100)
        self.sList = []
        for i in range(4):
            self.sList.append( SampleUI(self.sample_frame,i, text="SS%d"%i) )
            self.sList[i].grid(column=0,row=i)
            self.sampNameDict[self.sList[i].name] = i
        self.sample_frame.grid(column=1, row=1, sticky="ns")
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
        tk.Frame.__init__(self, master, relief=tk.SUNKEN)

        self.master = master
        self.sampNameDict={}
        
        self.initCanvasHyperbolas(master)
        self.initCanvasPairwisePsi(master, active=True)
        self.initStatusbar(master)
        self.initSliderFrame(master)
        self.initSampleFrame(master)
        self.initMenubar()

        #enable expansion
        #tk.Grid.rowconfigure(self,0,weight=1)
        tk.Grid.rowconfigure(self,1,weight=10)
        tk.Grid.rowconfigure(self,2,weight=1)
        tk.Grid.columnconfigure(self,1,weight=1)
        tk.Grid.columnconfigure(self,2,weight=1)
        tk.Grid.columnconfigure(self,0,weight=2)


        self.loadOptions()

    def loadOptions(self):
        self.lwd = O['psi_lwd']
        self.threshold = O['psi_threshold']





#---------------------------------------------------------------------
#   other stuff
#---------------------------------------------------------------------
    def quit(self):
        """quits app"""
        print "bye"
        root.quit()
        root.destroy()

    def showPsiCanvas(self):
        self.canvasH.hide()
        self.canvasPsi.show()
        self.activeCanvas = self.canvasPsi
        for s in self.sList:
            s.updateCircles()
        self.activeCanvas.redraw()

    def showHyperbolaCanvas(self):
        self.canvasH.show()
        self.activeCanvas = self.canvasH
        self.canvasPsi.hide()
        for s in self.sList:
            s.updateCircles()
        self.activeCanvas.redraw()
        
root = tk.Tk()

app = PooGUI(root)
#load some data
app.loadCoords("data.test.loc")
app.loadPsi("data.test.psi")
app.loadBGI("ch.png")
app.v = 100
app.drawAllHyperbolas()
app.drawAllPairwisePsi()
#e,mse,psi,data = app.optimizeAll()
app.grid()
tk.Grid.rowconfigure(root,0,weight=1)
tk.Grid.columnconfigure(root,0,weight=1)

root.mainloop()
