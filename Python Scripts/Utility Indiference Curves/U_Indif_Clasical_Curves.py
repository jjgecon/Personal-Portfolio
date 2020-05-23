# By Javier Gonzalez 5/21/2020 javierj.g18@gmail.com
# Some clasical utility vectors dfisplayed in matplotlib

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.axes3d import Axes3D
from matplotlib import cm
import numpy as np

def graphUIC(title, colormap = cm.cool):
    n = 100
    xgrid = np.linspace(1,10,n)
    x1,x2 = np.meshgrid(xgrid[::-1],xgrid)
    uu = utility(x1, x2)
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection='3d')

    ax.contour(x1, x2, uu , zdir='z', offset = 1,cmap=colormap)
    a = ax.plot_surface(x1,
                    x2,
                    uu,
                    rstride=7, cstride=7,
                    alpha = .5,
                    linewidth=1,
                    cmap = colormap)

    ax.view_init(elev=25,azim=-130)
    ax.set_xlabel('Good 1')
    ax.set_ylabel('Good 2')
    ax.set_zlabel('Utility Level')
    ax.set_title(title)
    fig.colorbar(a, ax=ax, shrink=0.5, aspect=5)
    plt.show()

#Cobb-Douglass constant returns to scale
def utility(x1,x2,α=.5):
    return (x1**α)*(x2**(1-α))

graphUIC('Constant Returns Cobb-Douglass')

#Cobb-Douglass increasing returns to scale
def utility(x1,x2,α=.6,beta=.6):
    return (x1**α)*(x2**beta)

graphUIC('Increasing Returns Cobb-Douglass')

#Cobb-Douglass decreasing returns to scale
def utility(x1,x2,α=.4,beta=.4):
    return (x1**α)*(x2**beta)

graphUIC('Decreasing Returns Cobb-Douglass')

#Perfect Substitutes
def utility(x1,x2):
    return x1 + x2

graphUIC('Perfect Substitutes')

def utility(x1,x2):
    out = np.zeros_like(x1)
    # x1 y x2 son arrays
    for i in range(len(x1)): #select the row
        out_aux = np.zeros_like(x1[i])
        j = 0
        for x11,x22 in zip(x1[i],x2[i]):
            out_aux[j]=(min(x11,x22))
            j += 1
        out[i] = out_aux
    return out

graphUIC('Perfect Complements (Leontief)')

def utility(x1,x2):
    mu = 0.5
    sigma = 0.5
    rho = (sigma-1)/sigma
    return (mu*(x1**rho) + (1-mu)*(x2**rho))**(1/rho)

graphUIC('CES subtitutes $\sigma = 0.5$')

def utility(x1,x2):
    mu = 0.5
    sigma = 3
    rho = (sigma-1)/sigma
    return (mu*(x1**rho) + (1-mu)*(x2**rho))**(1/rho)

graphUIC('CES subtitutes $\sigma = 3$')

def utility(x1,x2):
    mu = 0.5
    sigma = 9
    rho = (sigma-1)/sigma
    return (mu*(x1**rho) + (1-mu)*(x2**rho))**(1/rho)

graphUIC('CES subtitutes $\sigma = 9$')