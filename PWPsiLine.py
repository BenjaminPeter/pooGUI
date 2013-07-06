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


    def __init__(self,F1,F2, data,weight=1, threshold=0, **kwargs):
        """creates a pairwise psi line. the convention here is that the line is always left to right"""
        self.F1 = F1
        self.F2 = F2
        self.d = data
        if self.F1[0] > self.F2[0] or \
           (self.F1[0] == self.F2[0] and self.F1[1] > self.F2[1]):
            self.F1, self.F2 = self.F2, self.F1
        psi=self.d.get_default_stat(self.F1.pop,self.F2.pop)
        self.weight = weight
        self.threshold = threshold
 
        vv = self.getCoords()    
        matplotlib.lines.Line2D.__init__(self,vv[:,0],vv[:,1],
            color = self.cols[psi>0],
            linewidth = abs(psi * weight),
            **kwargs)

        if abs(psi) * weight < threshold:
            self.set_visible(False)

        assert self.F1[0] < self.F2[0] or (self.F1[0] == self.F2[0] and self.F1[1] < self.F2[1])


    def getCoords(self):
        if self.F1[0] > self.F2[0] or \
           (self.F1[0] == self.F2[0] and self.F1[1] > self.F2[1]):
            print "%f>%f or %f>%f"%(self.F1[0], self.F2[0], self.F1[1], self.F2[1])
            print "SWITCH"
            self.F1, self.F2 = self.F2,self.F1
            self.set_color( self.cols[ self.d.get_default_stat(self.F1.pop,self.F2.pop) >0])

        coords = np.array([[self.F1[0],self.F1[1]],
                           [self.F2[0],self.F2[1]]])

        assert self.F1[0] < self.F2[0] or \
           (self.F1[0] == self.F2[0] and self.F1[1] < self.F2[1])
        return coords



    def pupdate(self,F1=None, F2=None,  weight=None, threshold=None):

        visible = self.get_visible( )
        # first, update everything
        if F1 is not None:
            self.F1 = F1
        if F2 is not None:
            self.F2 = F2

        if self.F1[0] > self.F2[0]:
            self.F1, self.F2 = self.F2,self.F1
            self.set_color( self.cols[ self.d.get_default_stat(self.F1.pop,self.F2.pop)>0] )

        if threshold is not None:
            self.threshold = threshold
        if weight is not None:
            self.weight = weight
        if weight is not None or threshold is not None:
            self.set_linewidth(self.weight * self.psiObj[self.F1.pop, self.F2.pop])

        if self.weight * abs(self.psiObj[self.F1.pop,self.F2.pop]) > threshold \
           and self.F1.is_active() and self.F2.is_active():
            visible = True
        else:
            visible = False
        
        if self.F1.cluster != self.F2.cluster:
            visible = False
        self.set_visible ( visible )
        #print "LINEREDRAW: psi: %s, weight: %s (%s) threshold %s"%(visible, self.weight, 0, self.threshold)
        #then, update
        v = self.getCoords()
        self.set_xdata(v[:,0])
        self.set_ydata(v[:,1])


    def hide(self):
        self.set_visible(False)


    def show(self):
        if self.F1.is_active() and self.F2.is_active():
            print "show psi"
            self.set_visible(True)

    def on_press(self):
        """called when we want to animate the line for moving"""
        self.set_animated(True)

    def on_release(self):
        self.set_animated(False)

    def on_motion(self):
        v = self.getCoords()
        self.set_xdata(v[:,0])
        self.set_ydata(v[:,1])

        
