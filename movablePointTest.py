import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

ev={}


def dist(x,y):
    return np.sqrt((x[0]-y[0])**2+(x[1]-y[1])**2)

class Point(matplotlib.lines.Line2D):
    lock = None
    def __init__(self,x,y,**kwargs):
        self.x, self.y = x,y
        marker = kwargs.pop('marker','o')
        markersize = kwargs.pop('markersize',15)
        markeredgewidth = kwargs.pop('markeredgewith',2)        
        markeredgecolor = kwargs.pop('markeredgecolor','black')        
        color = kwargs.pop('color','green')
        #picker = kwargs.pop('picker',True)        
        matplotlib.lines.Line2D.__init__(self,[x],[y],marker=marker,
            markersize=markersize, 
            markeredgewidth=markeredgewidth,
            markeredgecolor=markeredgecolor,
            color=color, 
            picker=markersize,
            **kwargs)
            
    def connect(self):
        print "CONNECT"
        #self.figure.canvas.mpl_connect('pick_event', self.picked)    
        self.pressEvent = self.figure.canvas.mpl_connect('button_press_event', self.on_press)        
        self.moveEvent = self.figure.canvas.mpl_connect('motion_notify_event', self.on_motion)                
        self.releaseEvent = self.figure.canvas.mpl_connect('button_release_event', self.on_release)   
        
    def on_press(self,event):
        if event.inaxes != self.axes: return
        if Point.lock is not None: return
        contains, attrd = self.contains(event)
        if not contains: return
        x0, y0 = self.x, self.y
        self.press = x0, y0, event.xdata, event.ydata        
        
        print "pressed:", self.press
        Point.lock = self
        
        canvas = self.figure.canvas
        axes = self.axes
        self.set_animated(True)
        self.l.set_animated(True)
        canvas.draw()
        self.background = canvas.copy_from_bbox(self.axes.bbox)
        
        axes.draw_artist(self)
        axes.draw_artist(self.l)
        
        canvas.blit(axes.bbox)
        
    def on_release(self, event):
        if Point.lock is not self: return
        self.press =None
        Point.lock = None
        self.set_animated(False)
        self.l.set_animated(False)
        self.background = None
        
        
    def on_motion(self,event):
        if Point.lock is not self: return
        if event.inaxes != self.axes: return
        x0, y0, xpress, ypress = self.press

        xd = self.l.get_xdata()        
        yd = self.l.get_ydata()       

        self.set_xdata(event.xdata)        
        self.set_ydata(event.ydata)
        
        xd[self.id] = self.get_xdata()
        yd[self.id] = self.get_ydata()                        
        self.l.set_xdata(xd)
        self.l.set_ydata(yd)
        canvas = self.figure.canvas
        
        canvas.restore_region(self.background)
        self.axes.draw_artist(self)
        self.axes.draw_artist(self.l)        
        canvas.blit(self.axes.bbox)
        return


        if not contains: return
        print "moved", self.x

  
fig = plt.figure()
ax1 = fig.add_subplot(111)
p1,p2 = Point(.3,.4), Point(.8,.5)

ax1.add_line(p1)
ax1.add_line(p2)
l = matplotlib.lines.Line2D([.3,.8],[.4,.5])
ax1.add_line(l)
p1.l,p2.l = l,l
p1.id, p2.id = 0,1
p1.connect()
p2.connect()    

fig.show()

