# draggable Circle with the animation blit techniques; see
# http://www.scipy.org/Cookbook/Matplotlib/Animations
import numpy as np
import matplotlib.pyplot as plt
import matplotlib

class DraggableCircle(matplotlib.patches.Circle):
    lock = None  # only one can be animated at a time
    def __init__(self, sample, center, radius, **kwargs):
        matplotlib.patches.Circle.__init__(self,center,radius,**kwargs)
        #keep a pointer to corresponding sample
        self.sample = sample

        self.press = None
        self.background = None

    def connect(self):
        'connect to all the events we need'
        self.cidpress = self.figure.canvas.mpl_connect(
            'button_press_event', self.on_press)
        self.cidrelease = self.figure.canvas.mpl_connect(
            'button_release_event', self.on_release)
        self.cidmotion = self.figure.canvas.mpl_connect(
            'motion_notify_event', self.on_motion)

    def on_press(self, event):
        'on button press we will see if the mouse is over us and store some data'
        if event.inaxes != self.axes: return
        if DraggableCircle.lock is not None: return
        contains, attrd = self.contains(event)
        if not contains: return
        x0, y0 = self.center
        self.press = x0, y0, event.xdata, event.ydata
        print 'event contains', self.press
        DraggableCircle.lock = self

        # draw everything but the selected Circle and store the pixel buffer
        canvas = self.figure.canvas
        axes = self.axes
        self.set_animated(True)
        canvas.draw()
        self.background = canvas.copy_from_bbox(self.axes.bbox)

        # now redraw just the Circle
        axes.draw_artist(self)

        # and blit just the redrawn area
        canvas.blit(axes.bbox)

    def on_motion(self, event):
        'on motion we will move the rect if the mouse is over us'
        if DraggableCircle.lock is not self:
            return
        if event.inaxes != self.axes: return
        x0, y0, xpress, ypress = self.press
        #print event, x0, event.xdata, xpress

        try:
            x0 = float(x0)
            y0 = float(y0)
            dx = float(event.xdata - xpress)
            dy = float(event.ydata - ypress)
            self.center = ((x0+dx,y0+dy))
            if hasattr(self,"sample"):
                self.sample.tX = str(x0+dx)
                self.sample.tY = str(y0+dy)
                self.sample.xbox.delete(0)
                self.sample.ybox.delete(0)
                self.sample.xbox.insert(0,self.sample.tX)
                self.sample.ybox.insert(0,self.sample.tY)
            else:
                raise TypeError("samp not found")
        except TypeError as t:
            print "Error",event.xdata,xpress,dx,x0
            dbx,dbxp = event.xdata,xpress
            raise t
            return

        canvas = self.figure.canvas
        axes = self.axes
        # restore the background region
        canvas.restore_region(self.background)

        # redraw just the current Circle
        axes.draw_artist(self)

        # blit just the redrawn area
        canvas.blit(axes.bbox)

    def on_release(self, event):
        'on release we reset the press data'
        if DraggableCircle.lock is not self:
            return

        self.press = None
        DraggableCircle.lock = None

        # turn off the rect animation property and reset the background
        self.set_animated(False)
        self.background = None

        #TODO: redraw all hyperbolas

        # redraw the full figure
        self.sample.x, self.sample.y = self.center
        self.sample.redrawHyperbolas()
        self.figure.canvas.draw()

    def disconnect(self):
        'disconnect all the stored connection ids'
        self.figure.canvas.mpl_disconnect(self.cidpress)
        self.figure.canvas.mpl_disconnect(self.cidrelease)
        self.figure.canvas.mpl_disconnect(self.cidmotion)

    def hide(self):
        self.set_visible(False)

    def show(self):
        self.set_visible(True)

dbx, dbxp = 0,0
if False:
    fig = plt.figure()
    ax = fig.add_subplot(111)
    plt.xlim((0,100))
    plt.ylim((0,100))
    #rects = ax.bar(range(10), 20*np.random.rand(10))

    drs = []

    dr = DraggableCircle((5,5),3)
    ax.add_patch(dr)
    dr.connect()
    drs.append(dr)

    plt.show()
