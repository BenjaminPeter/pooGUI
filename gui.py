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
from PWPsiLine import PWPsiLine
from matrix import SimpleTable
from StatusBar import StatusBar
from PlotCanvas import PlotCanvas
from SampleFrame import SampleFrame
from SliderFrame import SliderFrame
import matplotlib.image as mpimg

  
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
#       appropriate plotting class
#---------------------------------------------------------------------
    def setCoords(self):
        """
        this function updates the coordinates of the sample points, called on load
        """
        nCoords = self.coords.shape[0]
        for sampleUI in self.sList:
            sampleUI.destroy()
        self.sList, self.hList, self.pList = [], [], []
        self.sampNameDict = {}
        for i in range(nCoords):
            self.sList.append( SampleUI(self.sample_frame,
                                        i,text=self.coords[i,0],
                                        x = self.coords[i,1],
                                        y=self.coords[i,2] ))
            self.sList[i].grid(column=0,row=i, sticky="ew")
            self.canvasH.panel.add_patch(self.sList[i].circH)
            self.canvasPsi.panel.add_patch(self.sList[i].circP)
            self.sList[i].circH.connect()
            self.sList[i].circP.connect()

            self.sampNameDict[self.sList[i].name] = i

            self.lwd, self.threshold = 1,0



    def changeV(self,ele,val):
        """ 
        function that updates hyperbola when v is changed
        """

        #see if the value is actually a float, if not, return
        self.v = float( val.get() )
        #redraw, whole thing, there might be a more efficient way to do this
        self.redrawHyperbolas()
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
        self.redrawPsiLines()
        if self.activeCanvas ==self.canvasPsi:
            self.activeCanvas.redraw()
      
    def changeThreshold(self,val):
        """ 
        function that updates hyperbola when v is changed
        """

        print "Changing threshold" , val.get()
        #see if the value is actually a float, if not, return
        self.threshold = float( val.get() )
        #redraw, whole thing, there might be a more efficient way to do this
        self.redrawPsiLines()

        if self.activeCanvas ==self.canvasPsi:
            self.activeCanvas.redraw()
#---------------------------------------------------------------------
#   optimizing
#---------------------------------------------------------------------
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
#   drawing stuff for hyperbolas, should eventually be 
#       moved to an appropriate plotting class
#---------------------------------------------------------------------
    def drawAllHyperbolas(self):
        for i in xrange(len(self.coords)-1):
            for j in xrange(i+1,len(self.coords)):
#        i,j = 0,1
                psi = self.psiDict[i,j]
                h = Hyperbola(self.canvasH.panel,self.sList[i], self.sList[j], self.v,psi)
                #h = matplotlib.lines.Line2D(np.arange(0,100),np.random.normal(50,10,size = 100))
                self.sList[i].hyperbolas.append(h)
                self.sList[j].hyperbolas.append(h)
                self.hList.append(h)
                
                self.canvasH.panel.add_line(h)
                
        if self.activeCanvas == self.canvasH:
            self.activeCanvas.redraw()

    def redrawHyperbolas(self):
        for h in self.hList:
            h.redraw(v = self.v)

    def redrawPsiLines(self):
        for l in self.pList:
            l.redraw(weight=self.lwd, threshold=self.threshold)

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
        for i in xrange(len(self.coords)-1):
            for j in xrange(i+1,len(self.coords)):
#        i,j = 0,1
                psi = self.psiDict[i,j]
                l = PWPsiLine(self.canvasH.panel,
                              self.sList[i], self.sList[j], psi)
                self.sList[i].psi_lines.append(l)
                self.sList[j].psi_lines.append(l)
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
        """loads Coords and saves them in data"""
        if f is None:
            f = tkFileDialog.askopenfile(mode='r',initialfile="coords.txt")

        self.coords = np.loadtxt(f,dtype="S100")
        self.setCoords()
        self.activeCanvas.redraw()
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
        self.psiMat.grid()

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
        self.slider_frame = SliderFrame(master,self, v=self.v,bg="pink")
        self.slider_frame.grid(column=1, row=0, sticky="")
    
    def initSampleFrame(self,master):
        self.sample_frame = SampleFrame(master, width=200, heigh=100, bg="green")
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
        tk.Frame.__init__(self, master, relief=tk.SUNKEN,bg="purple")

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



#---------------------------------------------------------------------
#   other stuff
#---------------------------------------------------------------------
    def quit(self):
        """quits app"""
        print "bla"
        root.quit()
        root.destroy()

    def showPsiCanvas(self):
        print "ABC"
        self.canvasH.hide()
        self.canvasPsi.show()
        self.activeCanvas = self.canvasPsi
        for s in self.sList:
            s.redrawCircles()
        self.activeCanvas.redraw()

    def showHyperbolaCanvas(self):
        print "CDFF"
        self.canvasH.show()
        self.activeCanvas = self.canvasH
        self.canvasPsi.hide()
        for s in self.sList:
            s.redrawCircles()
        self.activeCanvas.redraw()
        
root = tk.Tk()

app = PooGUI(root)
#load some data
app.loadCoords("data.test.loc")
app.loadPsi("data.test.psi")
app.loadBGI("ch2.png")
app.v = 200
app.drawAllHyperbolas()
app.drawAllPairwisePsi()
app.grid()
tk.Grid.rowconfigure(root,0,weight=1)
tk.Grid.columnconfigure(root,0,weight=1)

root.mainloop()
