import matplotlib.pyplot as plt
import matplotlib.image as mpimg

img = mpimg.imread("ch.png")


fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_ylim((0,100))
(0, 100)
ax.set_xlim((0,100))
(0, 100)
ax.imshow(img,interpolation='nearest', extent=[0,100,0,100])
fig.show()


