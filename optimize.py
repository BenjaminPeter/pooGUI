
import numpy as np
import scipy.optimize as spo
import scipy as sp

debug_psi , debug_data = 0,0
 
def tdoa3(rawData, rowsToKeep="ALL",**kwargs):
    """
    this function estimates the origin of a range expansion.
    The input is a np.array where each row corresponds to a pairwise psi.
    The first two columns are x and y coordiante of the the first sample.
    The 3rd and 4th columns are x and y coordiante of the the other sample.
    the 5th column is the directionality index.
     
    Returns:
    the function returns the estimated parameter (x,y,v) and the mean squared error.
    """
    def model(data,pars):
        v,x,y = pars
        ix,iy,jx,jy = data.transpose().tolist()
 
        return 1/v * (sp.sqrt( (ix -x)**2 + (iy-y)**2 ) - \
                     sp.sqrt( (jx -x)**2 + (jy-y)**2 ))
 
    def jacobian(data,pars):
        v,x,y = pars
        ix,iy,jx,jy = data.transpose().tolist()
 
        dfdv= 1/v**2 * (sp.sqrt((jx-x)**2+(jy-y)**2) -
                        sp.sqrt((ix-x)**2+(iy-y)**2) )
 
        dfdx= 1/v * ( (x-ix) / sp.sqrt((ix-x)**2+(iy-y)**2) + \
                     (jx-x) / sp.sqrt((jx-x)**2+(jy-y)**2) )
 
        dfdy= 1/v * ( (y-iy) / sp.sqrt((ix-x)**2+(iy-y)**2) + \
                      (jy-y) / sp.sqrt((jx-x)**2+(jy-y)**2) )
        return dfdv,dfdx,dfdy
 
    def makeErrorFunction(psi,data):
        def errorFunction(pars):
            return psi-model(data,pars)
        return errorFunction
 
    def makeJacobianFunction(data):
        def jacobianFunction(pars):
            return jacobian(data,pars)
 
#    rawData = np.loadtxt(path)
 
    if rowsToKeep=="ALL":
        rowsToKeep = range(len(rawData))
        print rowsToKeep
    if len(rowsToKeep) < 4:
        raise ValueError("Too little data")
 
    psi = rawData[:,4]
    data = rawData[:,:4]
    debug_psi, debug_data = psi, data
    f = makeErrorFunction(psi,data)
 
    #estimates = spo.leastsq(f,full_output=1,Dfun=makeJacobianFunction(data),**kwargs)
    estimates = spo.leastsq(f,full_output=1,**kwargs)
    mse=sum(estimates[2]['fvec']**2)
 
    return estimates, mse,psi, data
