import Tkinter as tk
from  matplotlib.colors import ColorConverter
import numpy as np
from options import O

class SampleFrame(tk.Frame):
    """class that contains all the sample UI elements"""
    def __init__(self,master, **kwargs):
        tk.Frame.__init__(self,master, **kwargs)
        self.master=master


    def update_sample_order(self, sList):
        """
            updates the order sample appear in the Sample Frame
            this is somewhat poorly done on self.master.sList
            pop_order is a dict[pop] -> position
        """
        for i,s in enumerate(sList):
            s.grid(column=0, row=i, sticky="ew")
class OriginFrame(SampleFrame):
    """ class with all inferred origins"""
    def __init__(self,master, **kwargs):
        SampleFrame.__init__(self,master, **kwargs)
        self.master = master


class Cluster():
    """
        a class that represents a cluster of populations
    """

    colorSchemes = O['cluster_colors']
    freeIds = range( (len(colorSchemes)))
    cur_clusters = []

    @staticmethod
    def addC(c):
        Cluster.cur_clusters.append(c)
        print "add cluster"
    def __init__(self, name='0'):
        self.mincol=[1,1,1]
        self.maxcol=[1,1,1]
        self.pops = []
        self.n_pops = len(self.pops)
        self.name=name
        self.id = Cluster.freeIds.pop(0)
        cs = Cluster.colorSchemes[self.id]
        self.set_colors(cs[0],cs[1])
        Cluster.addC(self)
        #Cluster.cur_clusters.append(self)
        print "Cluster__init",Cluster.cur_clusters
        self.origin = None


    def set_colors(self, mincol, maxcol):
        """
            Sets the colors for all samples
        """
        c= ColorConverter()
        self.mincol, self.maxcol = c.to_rgba(mincol), c.to_rgba(maxcol)
        self.update_colors()

    def update_colors(self):
        """
            Sets the colors for all samples
        """
        colmin, colmax = self.mincol, self.maxcol
        n = self.n_pops
        cmap = np.zeros((n,len(colmin)))
        if n == 0: return

        for i in range (len(colmin) ):
            step = float(colmax[i] - colmin[i] )/ n
            if step != 0:
                cmap[:,i] = np.arange(colmin[i], colmax[i], step)
            else:
                cmap[:,i] = colmax[i]

        self.pops = sorted(self.pops)
        for i,sample  in enumerate(self.pops):
            sample.set_color(cmap[i])

        return cmap

    def add_pop(self, pop):
        pop.set_cluster( self )
        self.pops.append(pop)
        self.n_pops += 1
        self.update_colors()

    def remove_pop(self, pop):
        pop.cluster = None
        self.pops = [p for p in self.pops if p != pop]
        self.n_pops = len(self.pops)
        self.update_colors()
        if self.n_pops ==0:
            Cluster.freeIds.append(self.id)
            Cluster.cur_clusters = [c for c in Cluster.cur_clusters if c != self]
    
    @staticmethod
    def get_cluster_by_name(cname):
        for c in Cluster.cur_clusters:
            if c.name == cname:
                return c
        return None


class ClusterFrame(tk.Frame):
    """
        class that displays cluster information
    """
    def __init__(self, parent, cluster, *args, **kwargs):
        tk.Frame.__init__(self,*args, **kwargs)
        self.c1 = tk.Canvas(self, width=10,height=10, bd=0, relief='ridge', bg="red")
        self.c2 = tk.Canvas(self, width=10,height=10, bd=0, relief='ridge', bg="white")        
        self.cname = tk.StringVar()
        self.e = tk.Entry(self, textvariable = self.cname, width=4)
        self.cluster = cluster
        self.parent = parent
        self.cname.set(cluster.name)
        self.cname.trace("w", lambda a,b,c,n=self.cname: self.changed_cluster(n))

        self.c1.grid(row=0,column=0,sticky="nsew")
        self.c2.grid(row=1,column=0,sticky="nsew")
        self.e.grid(row=0, column=1, rowspan=2, sticky="nsew")
        tk.Grid.rowconfigure(self,0,weight=1)
        tk.Grid.rowconfigure(self,1,weight=1)

        self.set_mincol(cluster.mincol)
        self.set_maxcol(cluster.maxcol)

    def set_mincol(self, color):
        cint = [min(255,c *256) for c in color]
        cstr =  '#%02x%02x%02x'%tuple(cint[:3])
        self.c1.config(bg=cstr)
    def set_maxcol(self, color):
        cint = [min(255,c *256) for c in color]
        cstr =  '#%02x%02x%02x'%tuple(cint[:3])
        self.c2.config(bg=cstr)

    def changed_cluster(self,sender):
        new_val = sender.get()
        if new_val == "": return
        
        new_cluster = Cluster.get_cluster_by_name(new_val)
        #we now got the cluster with the new name, there are three possibilities:
        #1. the cluster exists, then add sample to cluster
        #2. the cluster doesnt exist, but old cluster has only one sample
        #               then, just rename cluster
        #3. cluster doesnt exist, and old cluster is big: create new cluster
        if new_cluster is None:
            if self.cluster.n_pops == 1:
                self.cluster.name = new_val
                print "changing name", Cluster.cur_clusters
            else:
                c = Cluster(name=new_val)
                self.cluster.remove_pop(self.parent)
                c.add_pop(self.parent)
                print "adding cluster", Cluster.cur_clusters
        else:
            self.cluster.remove_pop(self.parent)
            new_cluster.add_pop(self.parent)
            print "adding to existing cluster", Cluster.cur_clusters

        self.parent.update_()

