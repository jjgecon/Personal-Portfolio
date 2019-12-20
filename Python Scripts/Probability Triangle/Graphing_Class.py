import numpy as np
import matplotlib.pyplot as plt

#Code by Javier Gonzalez on August 2019
#For any questions please contact javierj.g18@gmail.com

class ProbTriangle():
    """
    This class will explain graphicly how some empirical evidence is not consistent with Expected Utility Theory. 
    Demostrating that Allais example violates Independence Axiom. 
    The inputs should be a lotterie with 3 outcomes, at least 1 positive and greater than 0.
    """
    def __init__(self,
                 z=2, #Lowest reward, appart from zero or equal
                 Z=3, #Highest reward
                 P=0.8, #Probability of winning Z
                 p=0.6, #Probability if winning z
                 μ=.25): 
        self.z,self.Z,self.P,self.p,self.μ = z, Z, P, p, μ
        self.lotteries = ((1-self.P,0),(1-self.p,self.p),(1-self.μ*self.P,0),(1-self.μ*self.p,self.μ*self.p))
        self.lot_names = ('b1','b2','b3','b4')
        self.n_grind = 5000
        self.p1 = np.linspace(0,1,self.n_grind)
        self.grid = np.linspace(0,1,self.n_grind)
        self.hipothenuse = 1 - self.grid
        
    def u(self,x):
        "Utility function"
        return np.log(x+0.00001)
    
    def p3(self,fixed,z,Z,p1):
        "Ecuation to compute indiference curves"
        return ((fixed-self.u(z))/(self.u(Z)-self.u(z)))+p1*((self.u(z)-self.u(0))/(self.u(Z)-self.u(z)))
    
    def ufixed(self,z,Z,p1,p3):
        "Ecuation t compute fixed utility level"
        return (p1*self.u(0)+(1-p1-p3)*self.u(z)+p3*self.u(Z))

    def properEU(self):
        """
        This method will output the normal probability triangle of said lotterie
        """
        fig, ax = plt.subplots(figsize=(10, 6))
        #Set the limits of the fugure
        plt.axis([0, 1, 0, 1])

        #Set the limits of the probability triangle
        ax.set(xticks=[1], yticks=[1])
        ax.plot(self.grid,self.hipothenuse,"k",lw=0.8)

        #Arrow to show where does the curves grow
        if self.z < self.Z:
            ax.annotate(' ', xy=(0.45, 0.75), xytext=(0.75, 0.45),arrowprops={'arrowstyle': '-|>'}, fontsize='12')
            ax.text(0.53, 0.55, 'Utility Growth', rotation=-29, fontsize=14)
        else:
            ax.annotate(' ', xy=(0.75, 0.45), xytext=(0.45, 0.75),arrowprops={'arrowstyle': '-|>'}, fontsize='12')
            ax.text(0.53, 0.55, 'Utility Growth', rotation=-32, fontsize=14)

        #Plot the Indiference Curves
        for i in np.linspace(-11,1,10):
            x = self.p3(i,self.z,self.Z,self.p1)
            #mask some data points
            a = np.ma.masked_where(x+self.p1>=1, x)
            ax.plot(self.grid,a, 'k', alpha=0.1)

        ## Plot the diferent loterries according to EU
        for a,b,i in zip(self.lotteries,self.lot_names,enumerate(self.lotteries)):
            a1,a2 = a[0],a[1]
            ax.annotate(b,xy=(a1,a2),xytext=(a1+0.01, a2+0.01),fontsize=12)
            ax.scatter(a1,a2,40,'black')
            #Now I need to get the fixed utility level of each lotterie
            x = self.p3(self.ufixed(self.z,self.Z,a1,a2),self.z,self.Z,self.p1)
            a = np.ma.masked_where(x+self.p1>=1, x)
            #diferenciate colors
            if self.z < self.Z:
                if i[0] % 2 == 0:
                    color,α = 'b',1
                else: 
                    color,α = '--r',0.7
                ax.plot(self.grid,a, color,alpha=α,lw=2)
            else:
                if i[0] % 2 != 0:
                    color,α = 'b',1
                else: 
                    color,α = '--r',0.7
                ax.plot(self.grid,a, color,alpha=α,lw=2)

        #Legend to say preferences
        if self.z < self.Z:
            ax.text(0.71, 0.92, r"$b_{1}\succ b_{2}$ and $b_{3}\succ b_{4}$", 
            bbox={'facecolor': 'white', 'alpha': 0.5, 'pad': 6} ,fontsize=16)
        else:
            ax.text(0.71, 0.92, r"$b_{2}\succ b_{1}$ and $b_{4}\succ b_{3}$", 
            bbox={'facecolor': 'white', 'alpha': 0.5, 'pad': 6} ,fontsize=16)

        plt.show()
        
    def allais(self):
        """
        This method will output the graph trying to explain Allais example of violation of the Independence Axiom
        """
        fig, ax = plt.subplots(figsize=(10, 6))
        #Set the limits of the fugure
        plt.axis([0, 1, 0, 1])

        #Set the limits of the probability triangle
        ax.set(xticks=[1], yticks=[1])
        ax.plot(self.grid,self.hipothenuse,"k",lw=0.8)

        #Arrow to show where does the curves grow
        if self.z < self.Z:
            ax.annotate(' ', xy=(0.45, 0.75), xytext=(0.75, 0.45),arrowprops={'arrowstyle': '-|>'}, fontsize='12')
            ax.text(0.53, 0.55, 'Utility Growth', rotation=-29, fontsize=14)
        else:
            ax.annotate(' ', xy=(0.75, 0.45), xytext=(0.45, 0.75),arrowprops={'arrowstyle': '-|>'}, fontsize='12')
            ax.text(0.53, 0.55, 'Utility Growth', rotation=-32, fontsize=14)

        ## Plot the diferent loterries according to EU
        for a,b,i in zip(self.lotteries,self.lot_names,enumerate(self.lotteries)):
            a1,a2 = a[0],a[1]
            ax.annotate(b,xy=(a1,a2),xytext=(a1+0.01, a2+0.01),fontsize=12)
            ax.scatter(a1,a2,40,'black')
            x = self.p3(self.ufixed(self.z,self.Z,a1,a2),self.z,self.Z,self.p1)
            mask = np.ma.masked_where(x+self.p1>=1, x)
            if i[0] == 0:
                ax.plot(self.grid,mask, 'b',alpha=1,lw=2,label=r"Indifirence Curves consistent with $b_{1}\succ b_{2}$")
            else:
                ax.plot(self.grid,mask, 'b',alpha=0.2,lw=2)
            ## Plot other indiference curves
            x = self.p3(self.ufixed(self.z*0.01,self.Z,a1,a2),self.z*0.01,self.Z,self.p1)
            mask = np.ma.masked_where(x+self.p1>=1, x)
            if i[0] == 3:
                ax.plot(self.grid,mask, 'r',alpha=1,lw=2,label=r"Indifirence Curves consistent with $b_{4}\succ b_{3}$")
            else:
                ax.plot(self.grid,mask, '--r',alpha=0.2,lw=2)

        plt.legend(fontsize=12)
        plt.show()


a= ProbTriangle(μ=0.5)
a.allais()
a.properEU()