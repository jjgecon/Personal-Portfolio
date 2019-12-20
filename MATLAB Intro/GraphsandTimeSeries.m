%Code by Javier Gonzalez on October 2019
%For any questions please contact javierj.g18@gmail.com
%This code will calculate the Nash Equilibrium in a normal game 2x2 with
%only one equilibrium.

clear all
%Setiamos la cantidad de periodos a ver
T = 100;
%Alocamos memoria
MA1 = zeros(T,1);
MA2 = zeros(T,1);
AR = zeros(T,1);
ARMA = zeros(T,1);

% Elegimos un numero random para empezar
MA1(1) = rand;
MA2(1) = rand;
AR(1) = rand;
ARMA(1) = rand;
% Matrices de errores
Error =rand(T,1);

%Comenzando con un MA(1)
%Definimos el coeficiente
alpha = 1.005; % Lo defino de esta forma para poder usarlo como estacionario
for i = 2:T % Ojo que comienzo en 2 y no en 1
    MA1(i)= alpha*Error(i-1) + Error(i);
end

%Comenzando con un MA(2)
%Necesitamos un segundo coeficiente y sabemos que si comienzo en 2 tendre
%un problema, pues no existe un subindice 0, tenemos que poner un if.
beta = 0.34; % Lo defino de esta forma para poder usarlo como estacionario
for i = 2:T % Ojo que comienzo en 2 y no en 1
    if i == 2
        MA2(i)= alpha*Error(i-1) + Error(i);
    else
        MA2(i)= beta*Error(i-2) + alpha*Error(i-1) + Error(i);
    end
end

%Comenzando con un AR(1) estacionario
%Como tenemos un coeficiente que es menor a 1 (beta) lo usaremos
for i = 2:T % Ojo que comienzo en 2 y no en 1
    AR(i)= beta*AR(i-1) + Error(i);
end

%Comenzando con un ARMA(1,2) no estacionario
%Necesitamos un tercer coeficiente
%voy a cambiar un poco y hacer esto como un while loop
sigma = 0.7; % Lo defino de esta forma para poder usarlo como estacionario
t=2;
while t <= T
    if t == 2
        ARMA(t)= alpha*ARMA(t-1) + 0 + sigma*Error(t-1) + Error(t);
    else
        ARMA(t)= alpha*ARMA(t-1) + beta*Error(t-2) + sigma*Error(t-1) + Error(t);
    end
    t = t+1;
end

% Ya que tenemos todas las series veamos un grafico de 2x2 para ver cada
% una.
% necesitamos setiar un gridspace
grid = linspace(0,T);
%Aqui graficamos ambas economias
figure
subplot(2,2,1)
plot(grid,MA1)
title('MA1')
xlabel('Tiempo')
subplot(2,2,2)
plot(grid,MA2)
title('MA2')
xlabel('Tiempo')
subplot(2,2,3)
plot(grid,AR)
title('AR1 Estacionario')
xlabel('Tiempo')
subplot(2,2,4)
plot(grid,ARMA)
title('ARMA(1,2) NO Estacionario')
xlabel('Tiempo')
