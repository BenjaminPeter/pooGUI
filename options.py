"""
this class keeps all the options and configurations for the PooGUI program as a dictionary ['setting'] -> value. Feel free to modify the values, but the settings are required to stay the same.
"""

O = {}

#the base color(s) of the population circles. Each color is used for a cluster
O['circle_color'] = ['blue', 'black', 'red', 'purple', 'brown']
#the radius of the circle (as percentage of total plot with/height)
O['circle_radius'] = .02

#the color of the hyperbolas
O['hyperbola_color'] = 'black'

#in pwpsi plot, the base multipliers for line width and threshold
O['psi_lwd'] = 4
O['psi_threshold'] = 0

#the starting point for v, x and y to find the origin of the range expansion
O['opt_start'] = [100,40,40]

#the limits of the plots
O['xlim'] = (0,200)
O['ylim'] = (10,90)
#how the plotting window expands

