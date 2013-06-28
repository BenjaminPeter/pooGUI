#since I suck at doing geometry, I'll try the plotting of a hyperbola in R first



dist <- function(a,b)return(sqrt((a[1]-b[1])^2 + (a[2]-b[2])^2))

translate<-function(coords,trans){
    c2 <-c()
    for(i in 1:ncol(coords))
        c2<-cbind(c2,coords[,i]+trans[i])
    return(c2)
}

#dummy params for now
F1 <- c(10,10)
F2 <- c(30,40)
D <- 13

plotHyperbola<-function(F1,F2,D,...){
    #in the common parametrization, a is the dist from origin to hyperbola on the x axis
    #c is the distance from origin to either focus
    #and b is related to them by a^2 + b^2 = c^2
    #finally epsilon is the eccentrity e = c/a
    #D = |F1,S| - |F2,S| 
    #D = c+a -(c-a) = 2a
    a <- D/2
    c <- dist(F1,F2)/2
    bsq <- c^2 - a^2
    b <- sqrt(bsq)
    e = c/a
    e <<- e
    Origin<- c((F1[1] + F2[1]) / 2,(F1[2] + F2[2]) / 2)
    #alpha is the angle at which the foci are to be rotated:
    alpha = atan((F2[2]-F1[2])/(F2[1]-F1[1]))


    #for now, don't worry about bounding box
    t <- seq(-2*pi, 2*pi, by=0.01)
    x <- a * cosh(t)
    y <- b * sinh(t)



    coords<-cbind(x,y)

    #generate rotation matrix
    rotMat <- cbind( c(cos(-alpha), sin(-alpha)), c(-sin(-alpha), cos(-alpha)))
    #revRotMat <- cbind( c(cos(alpha), sin(alpha)), c(sin(-alpha), cos(alpha)))

    par(mfrow=c(1,2),pty="s")

    #plot untransformed hyperbola
    plot(coords,xlim=c(-100,100),ylim=c(-100,100),type="l",...)
    abline(h=0,col="grey")
    abline(v=0,col="grey")
    fociRot <- cbind(c(c,-c),c(0,0))
    points(fociRot)

    #add rotated
    lines(coords %*% rotMat,col="red")
    points((F1-Origin)[1],(F1-Origin)[2],col="red")
    points((F2-Origin)[1],(F2-Origin)[2],col="red")



            

    plot(translate(coords,Origin),xlim=c(-100,100),ylim=c(-100,100),type="l",...)
    points(t(F1),col="red")
    points(t(F2),col="red")
    points(translate(fociRot,Origin))
    points(translate(fociRot,Origin))
    lines(translate((coords %*% rotMat),Origin),col="red")
    abline(h=c(0,Origin[2]),col="grey",lty=2:1)
    abline(v=c(0,Origin[1]),col="grey",lty=2:1)
    finalCoords<-translate((coords %*% rotMat),Origin)
    
    #BBox stuff is still unifinished
    #inBounds <- which(0 < finalCoords[,1] & finalCoords[,1] <100 & 0 < finalCoords[,2] & finalCoords[,2] <100)
    #inBounds2 <- c(max(1,min(inBounds)-1),min(length(finalCoords),max(inBounds+1)))
    #finalCoordsBounded<- finalCoords[0 < finalCoords[,1] & finalCoords[,1] <100 & 0 < finalCoords[,2] & finalCoords[,2] <100,]


    #bbox<-cbind(c(0,0),c(100,100))
    #rect.matirx <- function(a,...)return(rect(a[1,1],a[1,2],a[2,1],a[2,2]))
    Origin <<- Origin
    fociRot <<- fociRot
    finalCoords
}
