# Code by Javier Gonzalez on October 2019
# For any questions please contact javierj.g18@gmail.com
# Simple Sollow Model with graphs

import numpy as np
import matplotlib.pyplot as plt

# Set time period and grid space
T,n = 0.5, 100

# Capital Grid
k = np.linspace(0,T,n)

# Set the functions
def production(k, alpha = 0.5):
    """ This function will define the production process"""
    return k**alpha

def savings(Prod, beta = 0.4):
    return beta*Prod

def depreciation(k,delta = 0.1):
    return (1-delta)*k

#Set lists
product_savings = []
product = []
depreciationlist = []

# For loop to fill the lists
for i in k:
    product.append(production(i))
    product_savings.append(savings(production(i)))
    depreciationlist.append(depreciation(i))

# Last Checks
kss = []
tol = 0.0009 # Tolerance level to 1 SS
for i in k:
    if i == 0:
        a = 0
    if abs(savings(production(i)) - depreciation(i)) <= tol:
        print(f'Steady State at {i:.2f} capital')
        print(f'Production Level at {production(i):.2f}')
        a += 1
        kss.append(i) #used for graphing purposes


if a == 0:
    print('No Steady State')

# Graph
fig, ax = plt.subplots(figsize=(10, 6))
zoom = 0.5 #0.5 for a better zoom
plt.axis([0, zoom, 0, zoom]) #Change this for a better zoom on the SS
ax.plot(k,product)
ax.plot(k,product_savings)
ax.plot(k,depreciationlist)
for i in kss:
    line = []
    b = np.linspace(0,8,n)
    for e in k:
        line.append(i)
    ax.plot(line,b,'--r', alpha=0.2)

plt.show()