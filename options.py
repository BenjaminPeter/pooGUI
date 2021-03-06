"""
this class keeps all the options and configurations for the PooGUI program as a dictionary ['setting'] -> value. Feel free to modify the values, but the settings are required to stay the same.
"""

O = {}

#the base color(s) of the population circles. Each color is used for a cluster
O['cluster_colors'] = [['white','green'], \
                       ['#ffeeee','orange'], \
                       ['black','yellow'], \
                       ['white','blue'], \
                       ['white','purple']\
]
#the radius of the circle (as percentage of total plot with/height)
O['circle_radius'] = .02

#the color of the hyperbolas
O['hyperbola_color'] = 'black'

#in pwpsi plot, the base multipliers for line width and threshold
O['psi_lwd'] = 4
O['psi_threshold'] = 0

#options for hyperbola plot
O['hyp_npts'] = 100 # the number of points of the hyperbola
O['hyp_min_e'] = 0 # max eccentricity s.t. the hyperbola is displayed NYI!!!
O['hyp_lwd'] = 1 # line width of hyperbola

#the starting point for v, x and y to find the origin of the range expansion
O['opt_start'] = [100,40,40]

#the limits of the plots
O['xlim'] = (0,200)
O['ylim'] = (10,130)
#how the plotting window expands

