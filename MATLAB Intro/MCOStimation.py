#Code by Javier Gonzalez on December 2019
#For any questions please contact javierj.g18@gmail.com
#This code will estimate a vector of betas from linear regresion by MCO

import pandas as pd
import numpy as np

#Reading data, Its different form the other, becuase pandas assigns the 1st row a varaible names
df = pd.read_excel(r'D:\OneDrive\Programming\Personal-Portfolio\MATLAB Intro\datos_tarea1Python.xlsx')
#Getting size of data
(obs,variables) = df.values.shape
#Values
Y = df.values[:,0]
X = df.values[:,1:variables]
#Check for invertibility
A = np.transpose(X).dot(X)
if np.linalg.det(A) == 0:
    print('Matrix X nor defined')
#Estimation via MCO
B = np.transpose(X).dot(Y)
beta = np.linalg.inv(A).dot(B)
for i in range(variables-1):
    print(round(beta[i],2))