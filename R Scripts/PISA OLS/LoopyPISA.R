#Code by Javier Gonzalez on May 2019
#For any questions please contact javierj.g18@gmail.com

#Loops
PISAols <- function(ymatrix,x1,interest) {
#For an input x1 this function calculates de coeficientes of each value
#INPUTS
#x1 = x1 #Covariates matrix
#interest=2 #How many varaible does x1 have of interest
#ymatrix=m #Input matrix

#Matriz output tendra coeficiente, error estandar, t, significancia
outmatrix=matrix(0,nrow=interest, ncol=4)

#Matrices soporte
InputVarm = matrix(0,nrow=1,ncol=interest)
Errorm = matrix(0,nrow=1,ncol=interest)
mcoefaux = matrix(0,nrow=10, ncol=interest)
mcoef=matrix(0,nrow=1,ncol=interest)
tstatm = matrix(0,nrow=interest, ncol = 1)
msd= matrix(0,nrow=1, ncol=interest)
m80coef = matrix(0,nrow=80, ncol=interest)
msum = matrix(0,nrow=10,ncol=interest)
mm = matrix(0,nrow=1,ncol=interest)

set.seed(2525)

a <- sample(1:10,1) #El numero random para elegir que variable la estimo
#Regs con PV sin estimacion del error standar
math <- lm(ymatrix ~ x1, weights = dataf$W_FSTUWT)
for (int in 1:interest){
  mcoef[1,int]=mean(coef(math)[int+1,])
  mcoefaux[,int]=coef(math)[int+1,] #Me dara el vector de los coeficientes que elija
}


math <- lm(ymatrix[,a] ~ x1, weights = dataf$W_FSTUWT)
for (int in 1:interest){
  msd[1,int]=vcovHC(math, "HC1")[int+1,int+1]^2 #errores robustos
}
#Creo un vector donde guardare todos las desviaciones estandar que quiero con los Weigths de 1-80
#El coeficiente 1

#Aqui hago el loop para mis regresiones, cambiando los weights
#Como solo necesito hacer esto con 1 solo PV elijo a al azar

for (i in 1:80) {
  ols = lm(ymatrix[,a]~x1,weights=w80s[,i])
  for (int in 1:interest){
    m80coef[i,int] = coef(ols)[int+1]
  }
}
#Inputs de la tabla
# mcoef scoef y rcoef son el valor del coeficiente

# - nos falta la varianza de los estimadores.
# m80coef s80coef y r80coef seran la media de los coeficientes en los 80 weights
for (int in 1:interest){
  mm[1,int] = mean(m80coef[,int])
}
# mr =
# ms =
# Sample Varaince = msd 

# Input variance sera la (1/9)*(coef w1 - mm)^2 y asi
for (int in 1:interest) {
  for (i in 1:10) {
    msum[i,int] = (mcoefaux[i,int]-mm[1,int])^2
  }
}

for (int in 1:interest) {
  InputVarm[1,int] = sum(msum[,int])*(1/9)
  #Calculo los errores totales
  Errorm[1,int] = InputVarm[1,int] + msd[1,int]
  #Calculo de el test t para cada uno
  tstatm[int,1] = mcoef[1,int]/sqrt(Errorm[1,int])
}


#Ingresamos datos a Output
for (int in 1:interest) {
  outmatrix[int,1]=round(mcoef[1,int], digits = 4)
  outmatrix[int,2]=round(sqrt(Errorm[1,int]), digits = 4)
  outmatrix[int,3]=round(tstatm[int,1], digits = 4)
  outmatrix[int,4]=round(ifelse(abs(tstatm[int,1])>1.96,TRUE,FALSE), digits = 4)
}


#Removemos para memoria
rm("InputVarm","tstatm", "Errorm", "msum", "ols", "mm", "math", "m80coef", "interest","mcoef", "msd","mcoefaux", "ymatrix","a","i","int")
#outoput
print("(,1) Coeficients (,2) Sd (,3)T statistic (,4) Significance")
outmatrix
}
