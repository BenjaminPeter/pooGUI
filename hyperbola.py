import matplotlib.pyplot as plt
import matplotlib
import matplotlib.lines
import numpy as np


class LineBase(matplotlib.lines.Line2D):

    @staticmethod
    def dist(x,y):
        return np.sqrt((x[0]-y[0])**2+(x[1]-y[1])**2)

    def __init__(self,ax, F1, F2, psiObj, **kwargs):
        if F1[0] > F2[0] or (F1[0] == F2[0] and F1[1] > F2[1]):
            self.F1, self.F2 = self.F2, self.F1
        self.F1 = F1
        self.F2 = F2

        self.psiObj = psiObj
        psi=psiObj[self.F1.pop,self.F2.pop]

        self.ax = ax

        vv = self.getCoords()    
        matplotlib.lines.Line2D.__init__(self,vv[:,0],vv[:,1],**kwargs)



    def hide(self):
        self.set_visible(False)

    def show(self):
        if self.F1.is_active() and self.F2.is_active() and \
           self.F1.cluster == self.F2.cluster:
            print "hide hyp"
            self.set_visible(True)

    def on_press(self):
        self.set_animated(True)

    def on_release(self):
        self.set_animated(False)

    def on_motion(self):
        v = self.getCoords()
        self.set_xdata(v[:,0])
        self.set_ydata(v[:,1])
class Hyperbola(matplotlib.lines.Line2D):
        

    @staticmethod
    def dist(x,y):
        return np.sqrt((x[0]-y[0])**2+(x[1]-y[1])**2)


    def __init__(self,ax,F1,F2,vObj, psiObj,nPts=100, **kwargs):
        self.F1 = F1
        #self.F1.hyperbolas.append(self)
        self.F2 = F2
        #self.F2.hyperbolas.append(self)
        #vObj is the object e.g. PooGui, whose property v is the
        #multiplier for psi
        self.vObj = vObj
        if F1[0] > F2[0] or (F1[0] == F2[0] and F1[1] > F2[1]):
            self.F1, self.F2 = self.F2, self.F1
        self.psi=psiObj[self.F1.pop, self.F2.pop]
        self.D = vObj.v*self.psi
        self.nPts = nPts
        self.ax = ax

        
        vv = self.getCoords()    
        matplotlib.lines.Line2D.__init__(self,vv[:,0],vv[:,1],**kwargs)


    def getCoords(self):

        a = self.D/2
        c = self.dist(self.F1, self.F2)/2
        b = np.sqrt(c*c - a*a)
        Origin = (self.F1[0] + self.F2[0])/2 , (self.F1[1] + self.F2[1])/2

        if self.F2[0] != self.F1[0]:
            alpha = np.arctan((self.F2[1]-self.F1[1])/(self.F2[0]-self.F1[0]))
        else:
            alpha = np.pi/2

        t = np.arange(-2*np.pi, 2*np.pi,0.1)
        x = a * np.cosh(t)
        y = b * np.sinh(t)

        coords = np.empty((len(t),2))
        coords[:,0] = x
        coords[:,1] = y

        rotMat = np.matrix([[np.cos(-alpha), -np.sin(-alpha)],
                            [np.sin(-alpha),np.cos(-alpha)]])

        coordsRot = coords * rotMat + Origin

        return coordsRot




    def hupdate(self,F1=None, F2=None,psi=None):
        # first, update everything
        if F1 is not None:
            self.F1 = F1
        if F2 is not None:
            self.F2 = F2
        if psi is not None:
            self.psi = psi
        self.D = self.vObj.v * self.psi
        
        if self.F1.cluster == self.F2.cluster:
            self.set_visible(True)
        else:
            self.set_visible(False)
#        print "PREH", type(self.F1)
#        print "HYPERREDRAW:",(self.F1[0],self.F1[1]), (self.F2[0],self.F2[1]) ,self.vObj.v * self.psi
        #then, update
#        background = canvas.copy_from_bbox(self.ax.bbox)
        v = self.getCoords()
        self.set_xdata(v[:,0])
        self.set_ydata(v[:,1])

    def hide(self):
        self.set_visible(False)


    def show(self):
        if self.F1.is_active() and self.F2.is_active() and \
           self.F1.cluster == self.F2.cluster:
            print "hide hyp"
            self.set_visible(True)

    def on_press(self):
        self.set_animated(True)

    def on_release(self):
        self.set_animated(False)

    def on_motion(self):
        v = self.getCoords()
        self.set_xdata(v[:,0])
        self.set_ydata(v[:,1])

if False:
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_xlim((0,100))
    ax.set_ylim((0,100))
    h = Hyperbola(ax,(30,3),(5,5),1)
    #ax.add_line(h)
    fig.show()


