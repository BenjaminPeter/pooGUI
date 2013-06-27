from Tkinter import *
import numpy as np
#root = Tk()
#c = Canvas(root,width=600,height=600,background="white")

def D(x,y):
    return np.sqrt( (x[0]-y[0])**2 + (x[1]-y[1])**2 )
def hyperbola(p1,p2,psi,mar=[0,0,600,600]):
    #find point s between foci:
    k = D(p1,p2)
    s = [0,0]
    dev = ( psi + k ) / 2. /k 
    s[0] = p1[0] + dev * (p2[0] - p1[0])
    s[1] = p1[1] + dev * (p2[1] - p1[1])

    #now, go in one direction and find other points on hyperbola
    
    return s
