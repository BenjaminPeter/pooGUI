import matplotlib
from matplotlib.lines import Line2D
from matplotlib.patches import Circle
import matplotlib.pyplot as plt
import numpy as np

fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_xlim((0,100))
ax.set_ylim((0,100))
l = Line2D(np.arange(0,100),np.arange(100,000,-1))
c = Circle((10,10),20)
ax.add_line(l)
ax.add_artist(c)
fig.show()

l.set_color("red")
c.set_color("red")
fig.canvas.draw()


