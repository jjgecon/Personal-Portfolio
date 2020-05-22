# By Javier Gonzalez 5/21/2020 javierj.g18@gmail.com

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.axes3d import Axes3D
from matplotlib import cm
import numpy as np

def graphUIC():
    n = 100
    xgrid = np.linspace(1,10,n)
    x1,x2 = np.meshgrid(xgrid[::-1],xgrid)
    uu = utility(x1, x2)
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection='3d')

    ax.contourf(x1, x2, uu , zdir='z', offset = 1,cmap=cm.cividis, alpha = .3)
    a = ax.plot_surface(x1,
                    x2,
                    uu,
                    rstride=7, cstride=7,
                    alpha = .7,
                    linewidth=1,
                    cmap = cm.cividis)

    ax.view_init(elev=25,azim=-130)
    ax.set_xlabel('Good 1')
    ax.set_ylabel('Good 2')
    ax.set_zlabel('Utility Level')
    ax.set_title('Utility and Indiference Curves with 2 goods')
    fig.colorbar(a, ax=ax, shrink=0.5, aspect=5)
    plt.show()

#Cobb-Douglass constant returns to scale
def utility(x1,x2,α=.5):
    return (x1**α)*(x2**(1-α))
def x1_calc(x2,fixedu,α=.5):
    return (fixedu/(x2**(1-α)))**(1/α)

graphUIC()

#Cobb-Douglass increasing returns to scale
def utility(x1,x2,α=.5,beta=.8):
    return (x1**α)*(x2**beta)
def x1_calc(x2,fixedu,α=.5,beta=.6):
    return (fixedu/(x2**beta))**(1/α)

graphUIC()

#Cobb-Douglass decreasing returns to scale
def utility(x1,x2,α=.5,beta=.2):
    return (x1**α)*(x2**beta)
def x1_calc(x2,fixedu,α=.5,beta=.2):
    return (fixedu/(x2**beta))**(1/α)

graphUIC()

#Perfect Substitutes
def utility(x1,x2):
    return x1 + x2
def x1_calc(x2,fixedu):
    return fixedu - x2

graphUIC()

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

graphUIC()