from collections import defaultdict
from Population import Population

class SimpleStat:
    """
        a single population statistic
    """
    def __init__(self, f=None):
        """
            f is a function f(a,...) that computes the pairwise stat
                from data a,b
        """
        self.f = f
        self.stats = {}

    def __setitem__(self, pop, data):
        if type(data) is np.float_ or type(data) is float:
            self.stats[pop] = data
        else:
            self.stats[pop] = f(data)

    def __getitem__(self,pop):
        return self.stats[pop]

    def __iter__(self):
        return self.stats.__iter__()




class PWStat(SimpleStat):
    def __init__(self, f=None):
        """
            f is a function f(a,b,...) that computes the pairwise stat
                from data a,b
        """
        SimpleStat.__init__(self,f=f)

    def __setitem__(self, pops, data):
        """there are two variations of this function:
            if data is a tuple, it is assumed that the stat has to
            be calculated from data[0], data[1]. Otherwise, the data
            is directly assigned
            """
        if type(data) is tuple:
            self.stats[pops] = self.f(data[0], data[1])
        else:
            self.stats[pops] = data

    def __getitem__(self, pops):
        return self.stats[pops]

    def __iter__(self):
        return self.stats.__iter__()

class AntiCommutativePWStat(PWStat):
    def __getitem__(self,pops):
        if pops[::-1] in self.stats:
            return - self.stats[ pops[::-1] ]
        else:
            return self.stats[pops]


class CommutativePWStat(PWStat):
    def __getitem__(self,pops):
        if pops[::-1] in self.stats:
            return self.stats[ pops[::-1] ]
        else:
            return self.stats[pops]

def pw_psi(v1, v2):
    """ calculates pw psi from allele frequency vectors v1 and v2 
    """
    psi, shared_snp = 0.0, 0

    for i,snp1 in enumerate(v1):
        snp2 = v2[i]
        if snp1 and snp2:
            shared_snp +=1
            psi = snp[i] - snp[j]

        if shared_snp == 0:
            return 0

        return psi / shared_snp

def psi_sum(pw_psi):
    """
        returns a SimpleStat object representing the sum of psi for
        a population, e.g. for ordering purposes
        @param pw_psi : the pairwise psi vlaues
        @type pw_psi: a PWStat object
    """
    psi = defaultdict( lambda : 0)
    for p1,p2 in pw_psi:
        psi[p1] += pw_psi[p1,p2]
        psi[p2] -= pw_psi[p1,p2]

    return dict(psi)


def psi_sum_cluster(pw_psi, sList):
    psi = defaultdict( lambda : 0)
    for i,s1 in enumerate(sList):
        for s2 in sList[i+1:]:
            if s1.cluster == s2.cluster:
                psi[s1.pop] += pw_psi[s1.pop, s2.pop]
                psi[s2.pop] -= pw_psi[s1.pop, s2.pop]
            else: print s1.cluster, s2.cluster
    return dict(psi)


def mkHeterozygosityFun(n):
    def Heterozygosity(v1):
        """calculates heterozygosity if v1 is the allele freq in [0;1]"""
        h = 0
        for i, f in enumerate(v1):
            h += 2*f*(n-f)
        return f/len(v1)
    return Heterozygosity


def order(stat ,keyfun=lambda x:x):
    """
        returns the order of the elements in a sorted list 
        @param stat:  the statistic for which the order is to be established
        @type stat: a SimpleStat object
    """
    k, v = stat.keys(), stat.values()
    if keyfun is None: keyfun = lambda x:x
    return dict([(i[1][0],i[0]) for i in enumerate(sorted([i for i in stat.iteritems()],key=lambda i: keyfun(i[1])))]) 

