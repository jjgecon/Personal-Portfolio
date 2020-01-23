%Code by Javier Gonzalez on December 2019
%For any questions please contact javierj.g18@gmail.com
% Simple Sollow Model with graphs

clear all
%Setiamos la cantidad de periodos analizar
T = 10;
% Numero de grid spaces
n = 100;
% Armamos el grid
k = transpose(linspace(0,T,n));
%Alocamos memoria
f_k = zeros(n,1);
f_k_prime = zeros(n,1);
dep = zeros(n,1);
% Usamos el parametro, para que sea concava
alpha = 0.5;
% Parametro de depreciaci�n
delta = 0.1;
% Parametro de Tecnologia
A = 1;
% Parametro de aumento de tecnologia
Aprime = 1.5;
% Usamos un loops para llenar la matriz
for i = 1:n
    % EL producto se modela como una Cobb Douglass
    % Llenamos el producto estocastico
    f_k(i,1) = A*k(i,1)^alpha;
    % Llenamos producto con tecnologia alta
    f_k_prime(i,1) = Aprime*k(i,1)^alpha;
    % Linea de dep
    dep(i,1) = (1-delta)*k(i,1);
end
% Parametro de ahorro exogeno
beta = 0.4;
% probar con los valores de beta 0.4 Y 0.8
%Beta = 0.2 no tiene estado estacionario. Pues la depresiacion se come todo
%el ahorro y por tanto es imposible ahorrar, racionalmente.
% Matris de savings del producto
savings = beta*f_k;
savings_prime = beta*f_k_prime;

% Sabemos que hay un estado estacionario si el ahorro es igual a la
% depresiacion en algun punto. Entonces tenemos que hacer un check
% EMpezare en el 2 para asegurarme que no cuenta el 0.
tol = 0.009; % Tolerancia Obtima para obtener solo 1 Estado Estacionario
% Analisis con A=1
a = 0;
z = ['-- Analisis de Estado Estacionario con A = ', num2str(A)];
disp(z)
for i = 2:n
    if abs(dep(i,1) - savings(i,1)) <= tol
        z=['Estado Estacionario en : ', num2str(k(i,1))];
        disp(z)
        z=['Con Produccion Igual a : ', num2str(f_k(i,1))];
        disp(z)
        a = a + 1;
    end
end
if a == 0
    z=['No se Encontro un Estado Estacionario'];
    disp(z)
end

% Ahora veamos con A=1.5
a = 0;
tol = 0.02;
z = ['-- Analisis de Estado Estacionario con A = ', num2str(Aprime)];
disp(z)
for i = 2:n
    if abs(dep(i,1) - savings_prime(i,1)) <= tol
        z=['Estado Estacionario en : ', num2str(k(i,1))];
        disp(z)
        z=['Con Produccion Igual a : ', num2str(f_k(i,1))];
        disp(z)
        a = a + 1;
    end
end
if a == 0
    z=['No se Encontro un Estado Estacionario'];
    disp(z)
end

% Chequiaemos cuantos estados estacionarios hay graficamente
figure
plot(k,f_k,'--k')
hold on
plot(k,savings,'k','DisplayName','Savings with A=1')
plot(k,savings_prime,'b','DisplayName','Savings with A=1.5')
plot(k,f_k_prime,'--b')
plot(k,dep,'r','DisplayName','Depreciation')
hold off
xlabel('Capital')
legend