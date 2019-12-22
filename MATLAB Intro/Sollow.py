# Code by Javier Gonzalez on December 2019
# For any questions please contact javierj.g18@gmail.com
# Simple Sollow Model with graphs

import numpy as np
import matplotlib.pyplot as plt

# Set time period and grid space
T,n = 1, 100

# Capital Grid
k = np.linspace(0,T,n)

# Set the functions
def production(k, alpha = 0.5,A=1):
    """ This function will define the production process"""
    return A*k**alpha

def savings(Prod, beta = 0.4):
    return beta*Prod

def depreciation(k,delta = 0.1):
    return (1-delta)*k

#Set lists
product_savings = []
product = []
product_savings_prime = []
product_prime = []
depreciationlist = []

# For loop to fill the lists
for i in k:
    product.append(production(i))
    product_savings.append(savings(production(i)))
    product_prime.append(production(i,A=1.5))     # Here we change the Technology
    product_savings_prime.append(savings(production(i,A=1.5)))
    depreciationlist.append(depreciation(i))

# Last Checks
kss = []
tol = 0.0025 # Tolerance level to 1 SS
for i in k:
    if i == 0:
        a1 = 0
        a2 = 0
    if abs(savings(production(i)) - depreciation(i)) <= tol and savings(production(i)) != 0:
        print(f'Steady State at {i:.2f} capital with A = 1')
        print(f'Production Level at {production(i):.2f} with A = 1')
        a1 += 1
        kss.append(i) #used for graphing purposes
    if abs(savings(production(i,A=1.5)) - depreciation(i)) <= tol and savings(production(i)) != 0:
        print(f'Steady State at {i:.2f} capital with A = 1.5')
        print(f'Production Level at {production(i):.2f} with A = 1.5')
        a2 += 1
        kss.append(i) #used for graphing purposes


if a1 == 0:
    print('No Steady State for A = 1')
if a2 == 0:
    print('No Steady State for A = 1.5')

# Graph
fig, ax = plt.subplots(figsize=(10, 6))
zoom = 1 #0.5 for a better zoom
plt.axis([0, zoom, 0, zoom]) #Change this for a better zoom on the SS
ax.plot(k,product,'--k')
ax.plot(k,product_savings,'k',label='Savings with A = 1')
ax.plot(k,product_prime,'--b')
ax.plot(k,product_savings_prime,'b',label='Savings with A = 1.5')
ax.plot(k,depreciationlist,'r',label='Depreciation')
for i in kss:
    line = []
    b = np.linspace(0,8,n)
    for e in k:
        line.append(i)
    ax.plot(line,b,'--g', alpha=0.2)

plt.legend()
plt.show()