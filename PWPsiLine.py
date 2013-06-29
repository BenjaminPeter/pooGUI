import matplotlib.pyplot as plt
import matplotlib
import matplotlib.lines
import numpy as np



class PWPsiLine(matplotlib.lines.Line2D):
    cols = ["black", "red"]

    @staticmethod
    def dist(x,y):
        return np.sqrt((x[0]-y[0])**2+(x[1]-y[1])**2)


    @staticmethod
    def mkLine(A,B,C):
        return lambda x,y: A*x+B*y-C


    def __init__(self,ax,F1,F2, psi,weight=1, threshold=0, xlim=(0,100), ylim=(0,100), **kwargs):
        """creates a pairwise psi line. the convention here is that the line is always left to right"""
        self.F1 = F1
        self.F2 = F2
        if F1[0] < F2[0]:
            self.psi = psi 
        else:
            self.F1, self.F2 = self.F2, self.F1
            self.psi = -psi
        self.weight = weight
        self.threshold = threshold
        self.xlim = xlim
        self.ylim = ylim
        self.ax = ax
 
        vv = self.getCoords()    
        matplotlib.lines.Line2D.__init__(self,vv[:,0],vv[:,1],
            color = self.cols[psi>0],
            linewidth = abs(psi * weight),
            **kwargs)

        if abs(psi) * weight < threshold:
            self.set_visible(False)


    def getCoords(self):

        coords = np.array([[self.F1[0],self.F1[1]],
                           [self.F2[0],self.F2[1]]])

        return coords




    def redraw(self,F1=None, F2=None, psi=None, weight=None, threshold=None, xlim=None,ylim=None):
        # first, update everything
        if F1 is not None:
            self.F1 = F1
        if F2 is not None:
            self.F2 = F2

        if psi is not None:
            self.psi = psi
        if self.F1[0] > self.F2[0]:
            self.F1, self.F2 = self.F2,self.F1
            self.psi = -self.psi
            self.set_color( self.cols[ self.psi>0] )

        if threshold is not None:
            self.threshold = threshold
        if weight is not None:
            self.weight = weight
        if weight is not None or threshold is not None:
            self.set_linewidth(self.weight * self.psi)
            if self.weight * abs(self.psi) > threshold \
               and self.F1.is_active() and self.F2.is_active():
                self.set_visible( True)
            else:
                self.set_visible( False )
        if xlim is not None:
            self.xlim = xlim
        if ylim is not None:
            self.ylim = ylim
        
        print "LINEREDRAW: psi: %s, weight: %s (%s) threshold %s"%(self.psi, self.weight, self.psi * self.weight, self.threshold)
        #then, redraw
#        background = canvas.copy_from_bbox(self.ax.bbox)
        v = self.getCoords()
        self.set_xdata(v[:,0])
        self.set_ydata(v[:,1])


    def hide(self):
        print "hide psi line",self.ax.figure.canvas
        self.set_color("red")
        self.set_visible(False)


    def show(self):
        if self.F1.is_active() and self.F2.is_active():
            print "show psi"
            self.set_visible(True)

