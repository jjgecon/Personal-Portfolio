# Code by Javier Gonzalez on October 2019
# For any questions please contact javierj.g18@gmail.com
# Simple Sollow Model with graphs

import numpy as np
import matplotlib.pyplot as plt

# Set time period and grid space
T,n = 10, 100

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
tol = 0.009 # Tolerance level to 1 SS
for i in k:
    if i == 0:
        a = 0
    if abs(savings(production(i)) - depreciation(i)) <= tol:
        print(f'Steady State at {i:.2f} capital')
        print(f'Production Level at {production(i):.2f} capital')
        a += 1

if a == 0:
    print('No Steady State')

# Graph
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(k,product)
ax.plot(k,product_savings)
ax.plot(k,depreciationlist)
plt.show()