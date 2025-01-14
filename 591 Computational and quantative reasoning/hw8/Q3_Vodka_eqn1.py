# -*- coding: utf-8 -*-
"""
Created on Sat Dec  8 18:51:26 2018

@author: DaveyJones
"""

# This example describe how to integrate ODEs with scipy.integrate module and how
# to use the matplotlib module to plot trajectories, directions field and others
# useful informations.
# 
# == Presentation of the Lokta-Volterra Model ==
# 
# 
# We will have a look at the Lokta-Volterra model, laso known as the
# predator-prey equations, re a pair of first order, non-linear, differential
# equations frequently used to describe the dynamics of biological systems in
# which two species interact, one a predator and one its prey. They were proposed
# independently by Alfred J. Lotka in 1925 and Vito Volterra in 1926 :
# du/dt =  a*u -   b*u*v
# dv/dt = -c*v + d*b*u*v 
# 
# with the following notations :
# 
# *  u : number of prey (for example rabbits)
# 
# *  v : number of predators (for example foxes)  
#   
# * a, b, c, d are constant parameters defining the behavior of the population :    
# 
#   + a is the natural growing rate of rabbits, when there's no foxes
# 
#   + b is the natural dying rate of rabbits, due to predation
# 
#   + c is the natural dying rate of foxes, when there's no rabbits
# 
#   + d is the factor descibing how many catched rabbits let create new rabbits
# 
# 
# We will use X=[u, v] to describe the state of both populations.
# Definition of the equations:
#
from numpy import *
import pylab as p


# du/dt =  a*u -   b*u*v
# dv/dt = -c*v + d*b*u*v 

def dX_dt(X, t=0):
    """ Return the growth rate of foxes and rabbits populations. """
    return array([ X[0]-X[0]*X[0]-.7*X[0]*X[1],  
                   X[1]-X[1]*X[1]-.3*X[0]*X[1]])
# 
# === Population equilibrium ===
# 
# Before using scipy to integrate this system, we will have a closer look on 
# position equilibrium. Equilibrium occurs when the growth rate is equal to 0.
# This gives two fixed points:
# 
X_f0 = array([0., 0.])
X_f1 = array([0.3, 0.89])
all(dX_dt(X_f0) == zeros(2) ) and all(dX_dt(X_f1) == zeros(2)) # => True 
# 
# === Stability of the fixed points ===
# Near theses two points, the system can be linearized :
# dX_dt = A_f*X where A is the Jacobian matrix evaluated at the corresponding point.
# We have to define the Jacobian matrix:
# 
def d2X_dt2(X, t=0):
    """ Return the jacobian matrix evaluated in X. """
    return array([[1-2*X[0]-.7*X[1] , -.7*X[0]],
                  [1-2*X[1]-.3*X[0] ,-.3*X[1]]])  
# 
# So, near X_f0, which represents the extinction of both species, we have:
# A_f0 = d2X_dt2(X_f0)                    # >>> array([[ 1. , -0. ],
#                                         #            [ 0. , -1.5]])
# 
# Near X_f0, the number of rabbits increase and the population of foxes decrease.
# X_f0 is a [http://en.wikipedia.org/wiki/Saddle_point saddle point].
# 
# Near X_f1, we have :
A_f1 = d2X_dt2(X_f1)                   # >>> array([[ 0.  , -2.  ],
                                        #            [ 0.75,  0.  ]])

# whose eigenvalues are +/- sqrt(ca).j :
lambda1, lambda2 = linalg.eigvals(A_f1) # >>> (1.22474j, -1.22474j)

# They are imaginary number, so the fox and rabbit populations are periodic and
# their period is given by :
T_f1 = 2*pi/abs(lambda1)                # >>> 5.130199
#         
# == Integrating the ODE using scipy.integate ==
# 
# Now we will use the scipy.integrate module to integrate the ODE.
# This module offers a  method named odeint, very easy to use to integrade ODE:
# 
from scipy import integrate

t = linspace(0, 15,  1000)              # time
X0 = array([0.2,0.2])                     # initials conditions: 10 rabbits and 5 foxes  

X, infodict = integrate.odeint(dX_dt, X0, t, full_output=True)
infodict['message']                     # >>> 'Integration successful.'
# 
# `infodict` is optionnal, and you can omit the `full_output` argument if you don't want it.
# type "info(odeint)" if you want more information about odeint inputs and outputs.
# 
# We will use matplotlib to plot the evolution of both populations:
# 
rabbits, foxes = X.T

f1 = p.figure()
p.plot(t, rabbits, 'r-', label='Rabbits')
p.plot(t, foxes  , 'b-', label='Foxes')
p.grid()

p.legend(loc='best')
p.xlabel('time')
p.ylabel('population')
p.title('Evolution of fox and rabbit populations')
f1.savefig('rabbits_and_foxes_1.png')
# 
# 
# The populations are indeed periodic, and their period is near to the T_f1 we calculated.
# 
# == Plotting directions field and trajectories in the phase plane ==
# 
# We will plot some trajectories in a phase plane for different starting
# points between X__f0 and X_f1.
# 
# We will ue matplotlib's colormap to define colors for the trajectories.
# These colormaps are very useful to make nice plots.
# Have a look on ShowColormaps if you want more information.
# 
values = linspace(0.3, 0.9, 5)                          # position of X0 between X_f0 and X_f1
vcolors = p.cm.Greens(linspace(0.3, 1., len(values)))   # colors for each trajectory

f2 = p.figure()

#-------------------------------------------------------
# plot trajectories
for v, col in zip(values, vcolors): 
    X0 = v * X_f1                               # starting point
    X = integrate.odeint( dX_dt, X0, t)         # we don't need infodict here
    p.plot( X[:,0], X[:,1], lw=3.5*v, color=col, label='X0=(%.f, %.f)' % ( X0[0], X0[1]) )

#-------------------------------------------------------
# define a grid and compute direction at each point
ymax = p.ylim(ymin=0)[1]                        # get axis limits
xmax = p.xlim(xmin=0)[1] 
nb_points   = 20                      

x = linspace(0, xmax, nb_points)
y = linspace(0, ymax, nb_points)

X1 , Y1  = meshgrid(x, y)                       # create a grid
DX1, DY1 = dX_dt([X1, Y1])                      # compute growth rate on the gridt
M = (hypot(DX1, DY1))                           # Norm of the growth rate 
M[ M == 0] = 1.                                 # Avoid zero division errors 
DX1 /= M                                        # Normalize each arrows
DY1 /= M                                  

#-------------------------------------------------------
# Drow direction fields, using matplotlib 's quiver function
# I choose to plot normalized arrows and to use colors to give information on
# the growth speed
p.title('Trajectories and direction field')
Q = p.quiver(X1, Y1, DX1, DY1, M, pivot='mid', cmap=p.cm.autumn)
p.xlabel('Number of Rabbits')
p.ylabel('Number of Foxes')
p.legend()
p.grid()
p.xlim(0, xmax)
p.ylim(0, ymax)
f2.savefig('rabbits_and_foxes_2.png')









