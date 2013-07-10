import matplotlib
import sys
import argparse as ap
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
from PlotCanvas import *
from SampleFrame import *
from SliderFrame import SliderFrame
from options import O
import matplotlib.image as mpimg
from Data import *
from Population import Population
from optimize import *
import optimize


  
class Data:
    """
        the main class that keeps all the samples, data, etc that are currently
        used in the program. 
    """

    def load_snp(self, data):
        print "loading: nPops=", len(self.pops)
        print data
        self.data = data
        self.add_pw_stat("psi",AntiCommutativePWStat(f=pw_psi))
        self.pw_default_stat = "psi"
        n_snp = data.shape[0]
        for i,p1 in enumerate(self.pops):
            for j,p2 in enumerate(self.pops):
                if j <= i: continue
                d1,d2 = data[:,i], data[:,j]
                psi,shared = 0.,0.
                for k in xrange(n_snp):
                    if d1[k] > 0 and d2[k] > 0:
                        psi += d1[k] - d2[k]
                        shared += 1
                if shared == 0:
                    psi =0
                psi = psi/shared
                self.pairwise_stats["psi"][p1,p2] = psi
                print "set psi for %s - %s to %f"%(p1.name, p2.name, psi)
        print [(i.name, j.name) for i, j in self.pairwise_stats["psi"]]




    def update_sample_order(self):
        self.base.update_sample_order()
    def update_all_colors(self):
        for c in self.clusters:
            self.clusters[c].update_colors()

    def __init__(self,base):
        """
            constructor. For now it just defines variables I'll need
        """
        self.base = base
        self.v = 20
        self.pops = [] #should be of type Population
        self.single_pop_stats = dict()
        self.single_pop_stats["name"] = dict()
        self.single_default_stat = None

        self.pairwise_stats = dict()
        self.pw_default_stat = None

        self.global_stats = dict()
        self.golbal_default_stat = None
        self.sort_stat = "name"

        self.init_clusters(O['cluster_colors'])

    def init_clusters(self, colors):
        class cdict(dict):
            def __missing__(s, x):
                s[x] = Cluster(self,x)
                return s[x]
        self.free_colors = set()
        self.used_colors = set()
        for col in colors:
            self.free_colors.add(ColorGradient(col))

        self.n_free_clusters = len(colors)
        self.clusters = cdict() 
        self.clusters['0'] = Cluster(self,'0')
        self.default_cluster = self.clusters['0']
        #add default cluster

    def get_free_color(self):
        c = self.free_colors.pop()
        self.used_colors.add(c)
        return c

    def remove_cluster(self, cluster):
        self.remove_color(cluster.col)
        del self.clusters[cluster.name]
        assert cluster.name not in self.clusters

    def print_clusters(self):
        print "printing clusters"
        for c in self.clusters:
            print c, [x.name for x in self.clusters[c].pops], self.clusters[c].n_pops
        print "------------------"
    def remove_color(self,c):
        self.used_colors.discard(c)
        self.free_colors.add(c)

    def get_v(self, cluster=None):
        if cluster is None:
            return self.v
    def set_v(self, v, cluster=None):
        if cluster is None:
            self.v = v
        self.base.slider_frame.vI.set(v)

    def add_pop(self, pop):
        self.pops.append(pop)
        self.single_pop_stats["name"][pop.name] = pop.name

    def add_cluster(self, cluster):
        self.clusters[cluster.name] =  cluster 

    def add_pw_stat(self, stat_name, data):
        self.pairwise_stats[stat_name] = data

    def set_pw_default_stat(self, stat_name):
        self.pw_default_stat = 'psi'

    def add_single_pop_stat(self, stat_name, data):
        self.single_pop_stats[stat_name] = data

    def get_default_stat(self, s1=None, s2=None):
        if s1 == None:
            # global
            return self.global_stats[self.global_default_stat]
        if s2 == None:
            #single pop
            return self.single_stats[self.single_default_stat][s1]
        return self.pairwise_stats[self.pw_default_stat][s1,s2]
    get_active_stat = get_default_stat
    def get_default_sort_stat(self, s1):
        return self.single_pop_stats[self.sort_stat][s1]

class Config:
    def __init__(self, data,**kwargs):
        for k,v in data.iteritems():
            setattr(self,k,v)
        for k,v in kwargs.iteritems():
            setattr(self,k,v)


        print self.xlim

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
            -v: constant multiplier of hyperbolas
            -xlim, ylim: plotting limits
        """
#---------------------------------------------------------------------
#   drawing stuff for points, should eventually be moved to an 
#       appropriate plotting class,psi, data
#---------------------------------------------------------------------

    def dummyElements(self):
        #vars I need
        self.activeCanvas
        self.canvas['H'] #replace with self.canvas[]...
        self.canvas['Psi']
        self.sample_frame
        self.origin_frame
        self.slider_frame
        self.bgi
        self.matrixTL
        self.psimatrix
        #vars in config
        self.lwd #should be in either plot...
        self.threshold
        #vars in Data
        self.v
        self.clusters
        self.psi
        self.data
        self.psi_sum
        self.oList
        self.hList #??
        self.sList #???
        #vars I don't need

        #maybees

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
        self.d = Data(self)
        self.c = Config(O)
        
        self.canvas = dict()
        self.d.sList = []
        self.d.oList = []
        self.init_canvas_hyperbolas()
        self.init_canvas_pwp(active=True)
        self.init_sample_frame()
        #self.init_statusbar()
        self.init_slider_frame()
        self.init_menubar()

        #enable expansion
        tk.Grid.rowconfigure(self,1,weight=10)
        tk.Grid.rowconfigure(self,2,weight=1)
        tk.Grid.columnconfigure(self,1,weight=1)
        tk.Grid.columnconfigure(self,2,weight=1)
        tk.Grid.columnconfigure(self,0,weight=2)

    def initPsiMatrix(self,master):
        """initializes Matrix containing psi values
        should do the following:
            1. display matrix of Edits? MatrixWidget
            2. load data and display it
            3. colorcode
        """
        self.matrixTL = tk.Toplevel(master)
        self.psi_matrix = SimpleTable(self.matrixTL)
        self.psi_matrix.grid(sticky="nsew")
        self.psi_matrix.fill(self.d.sList,self.d.pairwise_stats['psi'])
        self.psi_matrix.fill_labels(self.d.sList)

    def init_menubar(self):
        """
        this function loads and populates the menubar, and will register its events
        """
        self.menubar = tk.Menu(self)

        menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="File", menu=menu)
        menu.add_command(label="Load SNP",command=self.loadSNP)
        menu.add_command(label="Load Coords", command=self.loadCoords)
        menu.add_command(label="Load Background Image", command=self.loadBGI)
        menu.add_command(label="Save plot", command=self.save_plot)
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

    def init_canvas_hyperbolas(self, active=False):
        """
        this function creates the matplotlib canvas that will be used 
        to draw stuff
        master: parent frame
        active: is this displayed on startup?
        """
        self.canvas['H'] = HyperbolaCanvas(self, self.c,
                                           self.d.sList,
                                           self.d, width=300, height=300)
        self.canvas['H'].grid(column=0,row=0,rowspan=3,sticky="ewns")
        if not active:
            self.canvas['H'].hide()
        else:
            self.activeCanvas = self.canvas['H']

    def init_canvas_pwp(self, active=False):
        """
        this function creates the matplotlib canvas that will be used 
        to draw stuff
        master: parent frame
        active: is this displayed on startup?
        """
        self.canvas['Psi'] = PWPCanvas(self, self.c, self.d.sList,
                                       self.d, width=300, height=300)
        self.canvas['Psi'].grid(column=0,row=0,rowspan=3,sticky="ewns")
        if not active:
            self.canvas['Psi'].hide()
        else:
            self.activeCanvas = self.canvas['Psi']

    def init_statusbar(self):
        """function that creates a status bar at the bottom of the window"""
        self.sb = StatusBar(self)
        self.sb.grid(row=3,column=0,columnspan=2, sticky="ew")
    
    def init_slider_frame(self):
        self.slider_frame = SliderFrame(self,self, v=self.d.get_v())
        self.slider_frame.grid(column=1, row=0, sticky="")
    
    def init_sample_frame(self):
        self.sample_frame = SampleFrame(self, width=200, height=100)
        self.origin_frame = OriginFrame(self, width=200, height=100)
        for i in range(4):
            self.add_sample( SampleUI(master=self.sample_frame,
                                        data=self.d, config=self.c,
                                        cluster=None, text="SS%d"%i) )
            self.d.sList[i].grid(column=0,row=i)
        self.sample_frame.grid(column=1, row=1, sticky="ns")
        self.origin_frame.grid(column=1, row=2, sticky="ns")

#--------------------------------------------------

    def reset_sample_list(self):
        #reset everything:
        for sampleUI in self.d.sList:
            sampleUI.destroy()
        self.d.sList = []

        self.canvas['H'].samples = []
        self.canvas['Psi'].samples = []

    def add_sample(self, s):
        self.d.sList.append(s)
        self.canvas['H'].samples.append(s)
        self.canvas['Psi'].samples.append(s)

    def changeV(self,ele,val):
        """ 
        function that updates hyperbola when v is changed
        """

        #see if the value is actually a float, if not, return
        self.d.set_v( float( val.get() ))
        #update, whole thing, there might be a more efficient way to do this
        self.canvas['H'].update_()
        if self.activeCanvas == self.canvas['H']:
            self.activeCanvas.redraw()

    def changeLwd(self,val):
        """ 
        function that updates hyperbola when v is changed
        """

        print "Changing lwd" , val.get()
        #see if the value is actually a float, if not, return
        self.c.psi_lwd = float( val.get() )
        #redraw, whole thing, there might be a more efficient way to do this
        self.canvas['Psi'].update_()
        if self.activeCanvas ==self.canvas['Psi']:
            self.activeCanvas.redraw()
      
    def changeThreshold(self,val):
        """ 
        function that updates hyperbola when v is changed
        """

        print "Changing threshold" , val.get()
        #see if the value is actually a float, if not, return
        self.c.psi_threshold = float( val.get() )
        #update, whole thing, there might be a more efficient way to do this
        self.canvas['Psi'].update_()

        if self.activeCanvas ==self.canvas['Psi']:
            self.activeCanvas.redraw()
#---------------------------------------------------------------------
#   optimizing, should move to data
#---------------------------------------------------------------------
    def optimizeAll(self):
        ev,msev, pv,dv = [],[],[],[]
        activeStat = self.d.get_active_stat
        for cluster_id in self.d.clusters:
            cluster = self.d.clusters[cluster_id]
            n_pops = cluster.n_pops
            if n_pops <= 3:
                print "Warning, Cluster too small"
            data = np.empty((n_pops * (n_pops -1 ) /2, 5 ))
            row = 0
            for i, s1 in enumerate(cluster.pops):
                for j0, s2 in enumerate(cluster.pops[i+1:]):
                    j = i+j0 + 1
                    data[row] = s1.get_x(), s1.get_y(), \
                                s2.get_x(), s2.get_y(), \
                                self.d.get_active_stat(s1.pop, s2.pop)
                    row += 1
            e,mse,p,d = optimize.tdoa3(data,x0=O["opt_start"])
            print e[0]
            ev.append(e[0])
            msev.append(mse)
            pv.append(p)
            dv.append(d)
            self.d.set_v( e[0][0] )
            self.slider_frame.v_scale.set( e[0][0] )
            self.canvas['H'].update_()
            if self.activeCanvas == self.canvas['H']:
                self.activeCanvas.redraw()

            if cluster.origin is None:
                opt = \
                InferredOrigin(master=self.origin_frame,x=e[0][1],y=e[0][2],
                               text="Origin "+cluster.name)
                opt.set_color("red")
                cluster.origin = opt
            else:
                opt = cluster.origin
                opt.tX.set("%2.2f"%(e[0][1]))
                opt.tY.set("%2.2f"%(e[0][2]))
                opt.set_x(e[0][1])
                opt.set_y(e[0][2])
                opt.update_()
                print "UPDATED ORIGN"

            self.d.oList.append(opt)
            opt.grid(in_=self.origin_frame)
            self.canvas['H'].panel.add_artist( opt.circH )
            self.canvas['H'].update_()
            self.canvas['Psi'].panel.add_artist( opt.circP )
            #origins shouldn't be movable
            #opt.circH.connect()
            #opt.circP.connect()
            self.activeCanvas.redraw()
        return ev, msev, pv, dv


#------------------------------------Hyperbola---------------------------------
#   loading files and data
#---------------------------------------------------------------------
    def loadSNP(self,f=None):
        """loads SNP and saves them in data"""
        if f == None:
            f = tkFileDialog.askopenfile(mode='r')
        self.d.load_snp( np.loadtxt(f) )
        self.canvas['H'].draw_all_hyperbolas()
        self.canvas['Psi'].draw_all_pairwise_psi()
        self.initPsiMatrix(self.master)

#---------------------------- Sorting stuff ------------------------
#   this set of functions handles all the sorting of elements
#--------------------------------------------------


    def update_sample_order(self):
        """
            when the samples are sorted and have to be reordered, this function
            does it
        """
        self.d.sList = sorted(self.d.sList)
        self.sample_frame.update_sample_order(self.d.sList)
        self.psi_matrix.update_sample_order(self.d.sList)

#--------------------------------------------------
    def loadCoords(self,f=None):
        """loads Coords, creates the corresponding UI elements
            and the circles for plotting
        """

        default_cluster = self.d.default_cluster
        self.reset_sample_list()

        if f is None:
            f = tkFileDialog.askopenfile(mode='r',initialfile="coords.txt")

        for i,line in enumerate(open(f)):
            p = Population()
            p.load_line(line)
            self.d.add_pop(p)

            sUI = SampleUIWPop(pop=p, master=self.sample_frame, 
                               config = self.c, data=self.d,
                               cluster=default_cluster)
            sUI.grid(column=0,row=i, sticky="ew")

            #create plotting circles and register events
            self.canvas['H'].panel.add_artist( sUI.circH )
            self.canvas['Psi'].panel.add_artist( sUI.circP )
            sUI.circH.connect()
            sUI.circP.connect()
            
            self.add_sample( sUI )

        self.nCoords = len( self.d.sList )
        self.activeCanvas.redraw()

    def loadPsi(self,f=None):
        """loads Psi directly. Assumes Coordinates are already loaded"""
        if f is None:
            f = tkFileDialog.askopenfile(mode='r',initialfile="psi.txt")

        self.d.add_pw_stat('psi', AntiCommutativePWStat(f=pw_psi))
        if self.d.pw_default_stat is None:
            self.d.set_pw_default_stat('psi')

        psiRaw = np.loadtxt(f, dtype="S100")
        for row in psiRaw:
            self.d.pairwise_stats['psi'][ row[0], row[1] ] =  float(row[2])

        psi_sum = psi_sum_cluster(self.d.pairwise_stats['psi'],
                                  self.d.sList)
        self.d.add_single_pop_stat('psi_sum',psi_sum)
        self.d.sort_stat="psi_sum"

        self.initPsiMatrix(self.master)
        self.d.update_all_colors()
        self.d.update_sample_order()
            
        #self.set_colors()
        self.canvas['H'].draw_all_hyperbolas()
        self.canvas['Psi'].draw_all_pairwise_psi()

        
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
        self.canvas['H'].addBGI(self.bgi)
        self.canvas['Psi'].addBGI(self.bgi)

    def removeBGI(self):
        self.canvas['H'].removeBGI()
        self.canvas['Psi'].removeBGI()
        self.activeCanvas.redraw()

    def save_plot(self, f=None):
        if f == None:
            f = tkFileDialog.asksaveasfilename(initialfile="plot.pdf")
        self.activeCanvas.fig.savefig(f)

        


#---------------------------------------------------------------------
# various constructors
#---------------------------------------------------------------------

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
        self.canvas['H'].hide()
        self.canvas['Psi'].show()
        self.activeCanvas = self.canvas['Psi']
        for s in self.d.sList:
            s.updateCircles()
        self.activeCanvas.redraw()

    def showHyperbolaCanvas(self):
        self.canvas['H'].show()
        self.activeCanvas = self.canvas['H']
        self.canvas['Psi'].hide()
        for s in self.d.sList:
            s.updateCircles()
        self.activeCanvas.redraw()
        

#parsing
parser = ap.ArgumentParser(
    description="pooGUI origin inference program",
    add_help=True
)
parser.add_argument("--bgi",type=str, help="The background image to be "+\
                    "displayed on the plots", default="examples/ch.png")
parser.add_argument("--loc_file",type=str, help="The loc file ",
                    default="examples/data.test2.loc")
parser.add_argument("--psi_file",type=str, help="The psi file ",
                    default="examples/data.test.psi")
parser.add_argument("--snp_file",type=str, help="The snp file ", default=None)
args = parser.parse_args()
print args



root = tk.Tk()

app = PooGUI(root)
#load some data
if args.loc_file is not None:
    app.loadCoords(args.loc_file)
if  args.snp_file is None:
    if args.psi_file is not None:
        app.loadPsi(args.psi_file)
else:
    app.loadSNP(args.snp_file)

if args.bgi is not None:
    app.loadBGI(args.bgi)
#app.v = 100
#app.canvas['H'].draw_all_hyperbolas()
#app.canvas['Psi'].draw_all_pairwise_psi()
e,mse,psi,data = app.optimizeAll()
app.grid()
tk.Grid.rowconfigure(root,0,weight=1)
tk.Grid.rowconfigure(root,1,weight=1)
tk.Grid.columnconfigure(root,0,weight=1)
#app.save_plot("bla.pdf")



root.mainloop()
