# draggable Circle with the animation blit techniques; see
# http://www.scipy.org/Cookbook/Matplotlib/Animations
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from options import O
class Point(matplotlib.lines.Line2D):
    lock = None
    def __init__(self,sample,center,**kwargs):
        marker = kwargs.pop('marker','o')
        markersize = kwargs.pop('markersize',8)
        markeredgewidth = kwargs.pop('markeredgewith',1.3)        
        markeredgecolor = kwargs.pop('markeredgecolor','black')        
        color = kwargs.pop('color','green')
        #picker = kwargs.pop('picker',True)        
        matplotlib.lines.Line2D.__init__(self,[center[0]],
                                         [center[1]],
            marker=marker,
            markersize=markersize, 
            markeredgewidth=markeredgewidth,
            markeredgecolor=markeredgecolor,
            color=color, 
            picker=markersize,
            **kwargs)

        #keep a pointer to corresponding sample
        self.sample = sample

        self.press = None
        self.background = None
        self.lines =[]
            
    def add_line(self,l):
        self.lines.append(l)
        
    def connect(self):
        #self.figure.canvas.mpl_connect('pick_event', self.picked)    
        self.pressEvent = self.figure.canvas.mpl_connect('button_press_event', self.on_press)        
        self.moveEvent = self.figure.canvas.mpl_connect('motion_notify_event', self.on_motion)                
        self.releaseEvent = self.figure.canvas.mpl_connect('button_release_event', self.on_release)   


    def disconnect(self):
        print "DC"
        self.figure.canvas.mpl_disconnect(self.pressEvent)
        self.figure.canvas.mpl_disconnect(self.moveEvent)
        self.figure.canvas.mpl_disconnect(self.releaseEvent)
        
    def on_press(self,event):
        if event.inaxes != self.axes: return
        if Point.lock is not None: return
        contains, attrd = self.contains(event)
        if not contains: return
        x0, y0 = self.get_xdata(), self.get_ydata()
        self.press = x0, y0, event.xdata, event.ydata        
        
        print "pressed:", self.press
        Point.lock = self
        
        canvas = self.figure.canvas
        axes = self.axes
        self.set_animated(True)

        #set all lines/hyperbolas to animated
        for l in self.lines:
            l.on_press()

        canvas.draw()
        self.background = canvas.copy_from_bbox(self.axes.bbox)
        
        axes.draw_artist(self)
        for l in self.lines:
            axes.draw_artist(l)
        
        canvas.blit(axes.bbox)
        
    def on_release(self, event):
        if Point.lock is not self: return
        self.press =None
        Point.lock = None
        self.set_animated(False)
        #unanimate everything
        for l in self.lines:
            l.on_release()
        self.background = None
        
        # update the full figure
        #self.sample.x, self.sample.y = self.center
        #self.sample.updateHyperbolas()
        #self.sample.updatePsiLines()
        #self.figure.canvas.draw()
        
    def on_motion(self,event):
        if Point.lock is not self: return
        if event.inaxes != self.axes: return
        x0, y0, xpress, ypress = self.press
        
        if hasattr(self,"sample"):
            self.sample.set_x( event.xdata )
            self.sample.set_y( event.ydata )
            self.sample.tX.set("%2.2f"%(event.xdata))
            self.sample.tY.set("%2.2f"%(event.ydata))
        else:
            raise TypeError("samp not found")
        self.set_xdata(event.xdata)
        self.set_ydata(event.ydata)
        for l in self.lines:
            l.on_motion()
        canvas = self.figure.canvas
        
        canvas.restore_region(self.background)
        self.axes.draw_artist(self)
        for l in self.lines:
            self.axes.draw_artist(l)
        canvas.blit(self.axes.bbox)
        
        return

    def hide(self):
        self.set_visible(False)

    def show(self):
        self.set_visible(True)

    def _update(self):
        self.set_xdata(self.sample.get_x())
        self.set_ydata(self.sample.get_y())
