#Code by Javier Gonzalez on December 2019
#For any questions please contact javierj.g18@gmail.com
# Code intended to teach graphing tools, for loops and if statements
# Some stochastic processes

import numpy as np
import matplotlib.pyplot as plt

np.random.seed(20)
def MA1(et,μ=1.005):
    return μ*et

def MA2(et,et_1,μ=1.005,α=0.34):
    return μ*et+α*et_1

def AR1(xt_1,et,β=0.34):
    return xt_1*β+et

def ARMA(xt_1,et_2,et_1,et,γ=0.34,β=1.005,sigma=0.7):
    return xt_1*β+et_1*γ+et_2*sigma+et

n = 100
e = abs(np.random.randn(n))
seriesMA1 = []
seriesMA2 = []
seriesAR1 = []
seriesARMA = []
zero = []
for t in range(n):
    zero.append(np.mean(e))
    a1 = MA1(e[t])
    seriesMA1.append(a1)
    if t == 0:
        a2 = AR1(xt_1 = 0, et=  e[t])
        seriesAR1.append(a2)
        a3 = MA2(e[t],0)
        seriesMA2.append(a3)
        a4 = ARMA(xt_1 = 0 , et_2=0, et_1=0,et=  e[t])
        seriesARMA.append(a4)
    elif t == 1:
        a2 = AR1(xt_1 = seriesAR1[t-1] , et=  e[t])
        seriesAR1.append(a2)
        a3 = MA2(e[t],e[t-1])
        seriesMA2.append(a3)
        a4 = ARMA(xt_1 = seriesARMA[t-1] , et_2=0, et_1=e[t-1],et=  e[t])
        seriesARMA.append(a4)
    else:
        a2 = AR1(xt_1 = seriesAR1[t-1] , et=  e[t])
        seriesAR1.append(a2)
        a3 = MA2(e[t],e[t-1])
        seriesMA2.append(a3)
        a4 = ARMA(xt_1 = seriesARMA[t-1] , et_2=e[t-2], et_1=e[t-1],et=  e[t])
        seriesARMA.append(a4)

fig, axes = plt.subplots(2, 2, figsize=(10, 12))
axes[0, 0].plot(seriesMA1)
axes[0, 1].plot(seriesMA2)
axes[1, 0].plot(seriesAR1)
axes[1, 1].plot(seriesARMA)
# Esto es para poner una linea en torno a la media del error
axes[0, 0].plot(zero,'--k',alpha=0.2)
axes[0, 1].plot(zero,'--k',alpha=0.2)
axes[1, 0].plot(zero,'--k',alpha=0.2)
axes[1, 1].plot(zero,'--k',alpha=0.2)
# Titulos
axes[0, 0].set(title="MA(1)")
axes[0, 1].set(title="MA(2)")
axes[1, 0].set(title="AR(1)")
axes[1, 1].set(title="ARMA(1,2)")
plt.show()