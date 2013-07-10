import Tkinter as tk
from  matplotlib.colors import ColorConverter
import numpy as np
from options import O
from Data import *

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


class ColorGradient():
    """ Simple Color Gradient Class that ensures that
    each cluster has its own color scheme"""
    def __init__(self, c1, c2=None, cluster=None):
        c= ColorConverter()
        if c2 is None:
            self.mincol,self.maxcol = c.to_rgba(c1[0]), c.to_rgba(c1[1])
        else:
            self.mincol, self.maxcol = c.to_rgba(c1), c.to_rgba(c2)
        self.cluster = cluster

    def get_cmap(self, n):
        """
        returns a color gradient from min color to max color with n steps
        """
        if n == 0: return
        colmin,colmax = self.mincol,self.maxcol
        cmap = np.zeros((n,len(colmin)))

        for i in range (len(colmin) ):
            step = float(colmax[i] - colmin[i] )/ n
            if step != 0:
                cmap[:,i] = np.arange(colmin[i], colmax[i], step)
            else:
                cmap[:,i] = colmax[i]

        return cmap


class Cluster():
    """
        a class that represents a cluster of populations
    """

    def __len__(self):
        return self.n_pops

    def __init__(self, data, name='0'):
        self.d = data
        self.pops = []
        self.n_pops = len(self.pops)
        self.name=name
        self.origin = None

        self.col = self.d.get_free_color()


    def update_colors(self):
        """
            Sets the colors for all samples
        """
        cmap = self.col.get_cmap( self.n_pops)
        self.pops = sorted(self.pops)
        for i,sample  in enumerate(self.pops):
            sample.set_color(cmap[i])

    def add_pop(self, pop):
        pop.set_cluster( self )
        self.pops.append(pop)
        self.n_pops += 1
        self.update_colors()
        self.pops = sorted(self.pops)
        for i,p in enumerate(self.pops[1:]):
            assert p > self.pops[i] 

    def remove_pop(self, pop):
        self.pops = [p for p in self.pops if p.name != pop.name]
        self.n_pops = len(self.pops)
        self.update_colors()
        if self.n_pops ==0:
            self.d.remove_cluster(self)

    def __lt__(self, other):
        return self.name < other.name
    

class ClusterFrame(tk.Frame):
    """
        class that displays cluster information
    """
    def __init__(self, parent, data, config, *args, **kwargs):
        self.d = data
        self.c = config
        tk.Frame.__init__(self,*args, **kwargs)
        self.c1 = tk.Canvas(self, width=10,height=10, bd=0, relief='ridge', bg="red")
        self.c2 = tk.Canvas(self, width=10,height=10, bd=0, relief='ridge', bg="white")        
        self.cname = tk.StringVar()
        self.e = tk.Entry(self, textvariable = self.cname, width=4)
        self.cluster = parent.cluster
        self.parent = parent
        self.cname.set(self.cluster.name)
        self.cname.trace("w", lambda a,b,c,n=self.cname: self.changed_cluster(n))

        self.c1.grid(row=0,column=0,sticky="nsew")
        self.c2.grid(row=1,column=0,sticky="nsew")
        self.e.grid(row=0, column=1, rowspan=2, sticky="nsew")
        tk.Grid.rowconfigure(self,0,weight=1)
        tk.Grid.rowconfigure(self,1,weight=1)

        self.set_mincol(self.cluster.col.mincol)
        self.set_maxcol(self.cluster.col.maxcol)

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
        
        new_cluster = self.d.clusters[new_val]
        old_cluster = self.cluster
        #we now got the cluster with the new name, there are three possibilities:
        #1. the cluster exists, then add sample to cluster
        #2. the cluster doesnt exist, but old cluster has only one sample
        #               then, just rename cluster
        #3. cluster doesnt exist, and old cluster is big: create new cluster
        if len(new_cluster) == 0:
            if old_cluster.n_pops == 1:
                self.d.clusters[new_val] = old_cluster
                old_name = self.cluster.name
                self.cluster.name = new_val
                self.d.clusters.pop(old_name)
                print "1 renamed cluster from %s to %s"
            else:
                new_cluster.add_pop(self.parent)
                self.cluster = new_cluster
                old_cluster.remove_pop(self.parent)
                for k in self.d.clusters:
                    if self.d.clusters[k] == self.cluster:
                        assert self.parent in self.d.clusters[k].pops
                    else:
                        assert self.parent not in self.d.clusters[k].pops
                print "2: added new cluster:: "
        else:
            old_cluster.remove_pop(self.parent)
            new_cluster.add_pop(self.parent)
            print "3: adding to existing cluster"
            self.cluster = new_cluster

        self.parent.update_()
        psi_sum = psi_sum_cluster(self.d.pairwise_stats['psi'],
                                  self.d.sList)
        print "XXXX", len(self.d.sList)
        for p in self.d.pops:
            assert p in psi_sum
        self.d.add_single_pop_stat('psi_sum',psi_sum)
        self.d.update_all_colors()
        self.d.update_sample_order()

