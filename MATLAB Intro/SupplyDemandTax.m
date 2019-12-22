%Code by Javier Gonzalez on October 2019
%For any questions please contact javierj.g18@gmail.com
%Supply and Demand with a tax visualization and wellfare costs.

clear all
%Crear un grid de cantidades
T = 10;
n = 100;
q = transpose(linspace(0,T,n));
%Alocamos la memoria a las matrices
p_o_sin = zeros(n,1);
p_o_con = zeros(n,1);
p_d = zeros(n,1);
%Parametros
tau = 0.19; %Para acercarnos a el IVA
alpha = 1.2;
% Como necesitamos integrar usaremos funciones estaran al final del script
% p_df @(a,alpha) 15 - alpha*a;
% p_o_sinf @(a,alpha) (5 + alpha*a);
% p_o_conf @(a,b,alpha) (5 + alpha*a)/(1-b);


for i = 1:n
    %Llenamos la matriz de la oferta
    p_o_con(i,1) = p_o_conf(q(i,1),alpha,tau);
    %Llenamos oferta sin impuesto
    p_o_sin(i,1) = p_o_sinf(q(i,1),alpha);
    %Llenamos la matriz de la demanda
    p_d(i,1) = p_df(q(i,1),alpha);
end

% Vemos el Grafico
figure
plot(q,p_o_con)
hold on
plot(q,p_o_sin)
plot(q,p_d)
hold off
xlabel('Capital')
legend('Oferta Con Tax','Oferta SIN Tax','Demanda')

%Calculos del equilibrio sin tax
%La cantidad de equilibrio esta dado por:
q_equilibrio_sin = 10/(2*alpha);
% El surplus del productor estara dado por:
prod_wellfare_sin = integral(@(a)p_o_sinf(a,alpha),0,q_equilibrio_sin);
aux = integral(@(a)p_df(a,alpha),0,q_equilibrio_sin);
consumer_wellfare_sin = aux - prod_wellfare_sin;
% Reportamos
disp('-- Economia sin Impuesto --')
z = ['La cantidad de equilibrio es: ', num2str(q_equilibrio_sin)];
disp(z)
z = ['Los productores ganan: ', num2str(prod_wellfare_sin)];
disp(z)
z = ['Los consumidores ganan: ', num2str(consumer_wellfare_sin)];
disp(z)
z = ['WELLFARE TOTAL: ', num2str(consumer_wellfare_sin+prod_wellfare_sin)];
disp(z)

%Calculos del equilibrio con tax
%La cantidad de equilibrio esta dado por:
q_equilibrio_con = ((1-tau)*15-5)/(alpha*(2-tau));
% El surplus del productor estara dado por:
prod_wellfare_con = integral(@(a)p_o_conf(a,alpha,tau),0,q_equilibrio_con);
aux = integral(@(a)p_df(a,alpha),0,q_equilibrio_con);
consumer_wellfare_con = aux - prod_wellfare_con;
%Precio de equilibrio con impuestos es:
impuesto = (15 - alpha*q_equilibrio_con)*(tau);
%La recuadacion del fisco es:
recuadacion = impuesto*q_equilibrio_con;

% Reportamos
disp('-- Economia con Impuesto --')
z = ['La cantidad de equilibrio es: ', num2str(q_equilibrio_con)];
disp(z)
z = ['Los productores ganan: ', num2str(prod_wellfare_con)];
disp(z)
z = ['Los consumidores ganan: ', num2str(consumer_wellfare_con)];
disp(z)
z = ['El fisco recauda: ', num2str(recuadacion)];
disp(z)
z = ['WELLFARE TOTAL: ', num2str(consumer_wellfare_con+prod_wellfare_con+recuadacion)];
disp(z)

% En terminos porcentuales quien pierde mas beneficios?
disp('-- Tasas de Cambio por Impuesto --')
deltacons = (consumer_wellfare_con - consumer_wellfare_sin)/consumer_wellfare_sin;
deltaprod = (prod_wellfare_con - prod_wellfare_sin)/prod_wellfare_sin;
z = ['Cambio del beneficio consumidor con impuesto: ', num2str(deltacons)];
disp(z)
z = ['Cambio del beneficio productor con impuesto: ', num2str(deltaprod)];
disp(z)
z = ['Cambio del beneficio total con impuesto: ', num2str(-(consumer_wellfare_sin+prod_wellfare_sin)+(consumer_wellfare_con+prod_wellfare_con+recuadacion))];
disp(z)

function z = p_df(a,b)
    z = 15 - b*a;
end
function z = p_o_sinf(a,b)
    z = 5 + b*a;
end
function z = p_o_conf(a,b,c)
    z = (5 + b*a)/(1-c);
end
