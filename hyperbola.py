import matplotlib.pyplot as plt
import matplotlib
import matplotlib.lines
import numpy as np



class Hyperbola(matplotlib.lines.Line2D):
        

    @staticmethod
    def dist(x,y):
        return np.sqrt((x[0]-y[0])**2+(x[1]-y[1])**2)


    @staticmethod
    def mkHyperbola(F1,F2,D):
        return lambda x,y: (Hyperbola.dist((x,y),F1)-Hyperbola.dist((x,y),F2)-D)
    

    @staticmethod
    def mkLine(A,B,C):
        return lambda x,y: A*x+B*y-C


    def __init__(self,ax,F1,F2,v, psi,nPts=500,xlim=(0,100), ylim=(0,100), **kwargs):
        self.F1 = F1
        #self.F1.hyperbolas.append(self)
        self.F2 = F2
        #self.F2.hyperbolas.append(self)
        self.v = v
        if F1[0] < F2[0]:
            self.psi = psi 
        else:
            #self.F1, self.F2 = self.F2, self.F1
            self.psi = -psi
        self.D = v*self.psi
        self.nPts = nPts
        self.xlim = xlim
        self.ylim = ylim
        self.ax = ax

        
        vv = self.getCoords()    
        matplotlib.lines.Line2D.__init__(self,vv[:,0],vv[:,1],**kwargs)


    def getCoordsOld(self):
        xmin,xmax=self.xlim
        ymin,ymax=self.ylim

        self.hyperbola=self.mkHyperbola(self.F1,self.F2,self.D)
        A=np.linspace(xmin,xmax,self.nPts)
        B=np.linspace(ymin,ymax,self.nPts)
        X,Y=np.meshgrid(A,B)
        
        #get contour
        print X.shape,Y.shape
        contour = matplotlib.contour.ContourSet(self.ax,X, Y, self.hyperbola(X,Y), 0, zdir='z',alpha=0)

        p = contour.collections[0].get_paths()[0]
        del contour
        
        v = p.vertices
        return v
#        global gX,gY
#        gX,gY = X,Y

    def getCoords(self):
        xmin, xmax = self.xlim
        ymin, ymax = self.ylim

        a = self.D/2
        c = self.dist(self.F1, self.F2)/2
        b = np.sqrt(c*c - a*a)
        Origin = (self.F1[0] + self.F2[0])/2 , (self.F1[1] + self.F2[1])/2

        if self.F2[0] != self.F1[0]:
            alpha = np.arctan((self.F2[1]-self.F1[1])/(self.F2[0]-self.F1[0]))
        else:
            alpha = np.pi/2

        t = np.arange(-2*np.pi, 2*np.pi,0.01)
        x = a * np.cosh(t)
        y = b * np.sinh(t)

        coords = np.empty((len(t),2))
        coords[:,0] = x
        coords[:,1] = y

        rotMat = np.matrix([[np.cos(-alpha), -np.sin(-alpha)],
                            [np.sin(-alpha),np.cos(-alpha)]])

        coordsRot = coords * rotMat + Origin

        return coordsRot




    def redraw(self,F1=None, F2=None, v=None,psi=None,xlim=None,ylim=None):
        # first, update everything
        if F1 is not None:
            self.F1 = F1
        if F2 is not None:
            self.F2 = F2
        if v is not None:
            self.v = v
            self.D = self.v * self.psi
        if psi is not None:
            self.psi = psi
            self.D = self.v * self.psi
        if xlim is not None:
            self.xlim = xlim
        if ylim is not None:
            self.ylim = ylim
        
        print "HYPERREDRAW:",(self.F1[0],self.F1[1]), (self.F2[0],self.F2[1]) ,self.v * self.psi
        #then, redraw
#        background = canvas.copy_from_bbox(self.ax.bbox)
        v = self.getCoords()
        self.set_xdata(v[:,0])
        self.set_ydata(v[:,1])

    def hide(self):
        print "hide hyp",self.ax.figure.canvas
        self.set_color("red")
        self.set_visible(False)


    def show(self):
        if self.F1.is_active() and self.F2.is_active():
            print "hide hyp"
            self.set_visible(True)
if False:
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_xlim((0,100))
    ax.set_ylim((0,100))
    h = Hyperbola(ax,(30,3),(5,5),1)
    #ax.add_line(h)
    fig.show()


