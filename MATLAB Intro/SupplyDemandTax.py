# Code by Javier Gonzalez on October 2019
# For any questions please contact javierj.g18@gmail.com
# Supply and Demand with a tax visualization and wellfare costs.

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad

T,n= 10, 100
q = np.linspace(0,T,n)

# Ecuations
def p_df(a,b):
    return 15 - b*a
def p_o_wof(a,b):
    return 5 + b*a
def p_o_wf(a,b,c):
    return (5 + b*a)/(1-c)

# Parameters
tau = 0.19
alpha = 1.2

# Store the data
p_o_w = [] #Supply with tax
p_o_wo = [] #Supply without tax
p_d = [] #Demmand

for i in q:
    p_o_wo.append(p_o_wof(i,alpha))
    p_o_w.append(p_o_wf(i,alpha,tau))
    p_d.append(p_df(i,alpha))


#Equilibrium without tax
q_eq_wo = 10/(2*alpha)
p_eq_wo = 15 - alpha*q_eq_wo
integrand = lambda x: 5 + alpha*x
prod_wellfare_wo, error = quad(integrand, 0, q_eq_wo) 
integrand = lambda x: 15 - alpha*x
aux, error = quad(integrand, 0, q_eq_wo) 
consumer_wellfare_wo = aux - prod_wellfare_wo
print("-- Economy Without Taxes --")
print(f"Equilibrium Capital: {q_eq_wo:.2f}")
print(f"Equilibrium Price: {p_eq_wo:.2f}")
print(f"Consumer Wellfare: {consumer_wellfare_wo:.2f}")
print(f"Supply Wellfare: {prod_wellfare_wo:.2f}")
print(f"Total Wellfare: {(prod_wellfare_wo+consumer_wellfare_wo):.2f}")

#Equilibrium with tax
q_eq_w = ((1-tau)*15-5)/(alpha*(2-tau))
p_eq_w = 15 - alpha*q_eq_w
integrand = lambda x: (5 + alpha*x)/(1-tau)
prod_wellfare_w, error = quad(integrand, 0, q_eq_w) 
integrand = lambda x: 15 - alpha*x
aux, error = quad(integrand, 0, q_eq_w) 
consumer_wellfare_w = aux - prod_wellfare_w
fiscal_revenue = p_eq_w*tau*q_eq_w
print("-- Economy With Taxes --")
print(f"Equilibrium Capital: {q_eq_w:.2f}")
print(f"Equilibrium Price: {p_eq_w:.2f}")
print(f"Consumer Wellfare: {consumer_wellfare_w:.2f}")
print(f"Supply Wellfare: {prod_wellfare_w:.2f}")
print(f"Fiscal Revenue: {fiscal_revenue:.2f}")
print(f"Total Wellfare: {(prod_wellfare_w+consumer_wellfare_w+fiscal_revenue):.2f}")

#Change Rates and Loss
print("-- Tax Changes --")
print(f'Consumer Wellfare Change: {(consumer_wellfare_w-consumer_wellfare_wo)/(consumer_wellfare_wo):.2f}%')
print(f'Producers Wellfare Change: {(prod_wellfare_w-prod_wellfare_wo)/(prod_wellfare_wo):.2f}%')
print(f'Total Wellfare Change: {(prod_wellfare_w+consumer_wellfare_w+fiscal_revenue)-(prod_wellfare_wo+consumer_wellfare_wo):.2f}')

# Graph
fig, ax = plt.subplots(figsize=(10, 6))
plt.axis([0, 10,0,18])
ax.plot(q,p_o_wo,'--r' ,label = 'Supply Without Taxes',zorder=-1)
ax.plot(q,p_o_w,'-r', label = 'Supply With Taxes',zorder=-1)
ax.plot(q,p_d, label = 'Demand',zorder=-1)
ax.scatter(q_eq_wo,p_eq_wo,40,'black',zorder=1)
ax.annotate('Equilibrium Without Taxes',xy=(q_eq_wo,p_eq_wo),
            xytext=(q_eq_wo+0.4, p_eq_wo-0.2),fontsize=10,
            arrowprops={'arrowstyle': '<|-'})
ax.scatter(q_eq_w,p_eq_w,40,'black',zorder=1)
ax.annotate('Equilibrium With Taxes',xy=(q_eq_w,p_eq_w),
            xytext=(q_eq_w-1.3, p_eq_w+2),fontsize=10,
            arrowprops={'arrowstyle': '<|-'})
plt.legend()
plt.show()