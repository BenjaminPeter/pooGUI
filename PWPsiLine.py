import matplotlib.pyplot as plt
import matplotlib
import matplotlib.lines
import numpy as np
from hyperbola import LineBase



class PWPsiLine(LineBase):
    cols = ["black", "red"]


    def __init__(self,F1,F2, data, config, **kwargs):
        """creates a pairwise psi line. the convention here is that the line is always left to right"""
 
        LineBase.__init__(self, F1, F2, data, config,
            **kwargs)

        weight = self.c.psi_lwd
        threshold = self.c.psi_threshold
        psi = self.d.get_default_stat(F1.pop, F2.pop)
        self.set_color(self.cols[psi>0])
        self.set_lw(abs(psi * weight))
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

    def update_(self,F1=None, F2=None):
        """
        updates the plot and all lines. If F1, F2 are passed they are updated as well, otherwise the config element is used
        """

        visible = self.get_visible( )
        # first, update everything
        if F1 is not None:
            self.F1 = F1
        if F2 is not None:
            self.F2 = F2

        if self.F1[0] > self.F2[0]:
            self.F1, self.F2 = self.F2,self.F1
            self.set_color( self.cols[ self.d.get_default_stat(self.F1.pop,self.F2.pop)>0] )

        psi = self.d.get_default_stat(self.F1, self.F2)
        self.set_linewidth(self.c.psi_lwd * psi)

        if self.c.psi_lwd * abs(psi) > self.c.psi_threshold \
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


        
