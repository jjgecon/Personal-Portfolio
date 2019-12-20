%Code by Javier Gonzalez on December 2019
%For any questions please contact javierj.g18@gmail.com
%This code will estimate a vector of betas from linear regresion by MCO

clear all
clc
format bank
%Veamos data para eso utilizaremos
[Data] = xlsread('datos_tarea1');

%Necesitamos ver la cantidad de observaciones que tiene la data
[obs,vars] = size(Data);
%Elegimos una columna para tener como Y
Y = Data(:,1);
%Setiamos los covaraidos
X = Data(:,2:vars);
%Chequiamos que el determinante sea distinto de 0
if det(transpose(X)*X) == 0
    disp("Matriz de Covariados mal definida")
end
%Terminamos estimando el beta
beta = inv(transpose(X)*X)*(transpose(X)*Y)

%El output son los coeficientes estimados