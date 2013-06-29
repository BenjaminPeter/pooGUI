import Tkinter as tk

class SliderFrame(tk.Frame):
    """frame that holds sliders and some other stuff"""
    def __init__(self,master, main,v=100,width=200, **kwargs):
        tk.Frame.__init__(self,master, width=width, **kwargs)
        self.master = master
        self.main = main

        #trackers
        self.vI = tk.DoubleVar()
        self.vI.set( v )
        self.lwdI = tk.DoubleVar()
        self.lwdI.set( 1 )
        self.tI = tk.DoubleVar()
        self.tI.set( 0 )

        #the v parameter of the hyperbolas
        self.v_scale = tk.Scale(self, orient=tk.HORIZONTAL,
                        bg="red", length=200, label="v", from_=1, to=1000, variable = self.vI, resolution =0.1)

        #the number of pops for optimization
        self.npop_scale = tk.Scale(self, orient=tk.HORIZONTAL,
                        length = 200, label="number of pops", from_=1, to=10)

        #the line width
        self.lwd_scale = tk.Scale(self, orient=tk.HORIZONTAL,
                        length = 200, label="line width",
                                  from_=1, to=20,
                                 variable = self.lwdI, resolution=0.01)

        #the threshold for lines to be drawn
        self.threshold_scale = tk.Scale(self, orient=tk.HORIZONTAL,
                        length = 200, label="threshold",
                                        from_=0, to=10,
                                       variable = self.tI,
                                       resolution=0.01)
        self.vI.trace("w",lambda a,b,c,n=self.v_scale:main.changeV(a,n))
        self.lwdI.trace("w",lambda a,b,c,n=self.lwd_scale:main.changeLwd(n))
        self.tI.trace("w",lambda a,b,c,n=self.threshold_scale:main.changeThreshold(n))
        self.v_scale.grid(column=0,row=0)
        self.npop_scale.grid(column=0,row=1)
        self.lwd_scale.grid(column=0,row=2)
        self.threshold_scale.grid(column=0,row=3)

        print """made slider bfrmae"""
