import numpy as np

#Code by Javier Gonzalez on September 2019
#For any questions please contact javierj.g18@gmail.com

class PureNash:
    def __init__(self,matrix):
        self.r, self.c = matrix.shape
        self.m = matrix
    
    def p1bestresponse(self):
        """
        This method searched the payouts of Player 1 given estrategies of player 2. It will retrun a 
        list of the best responses for Player 1. The list consists of strings and intergers.
        """
        maxvalue=0
        bestresponses = []
        a=0
        for j in range(self.c):
            if j % 2 == 0:
                bestresponses.append(".")
                maxvalue = np.max(self.m[:,j])
                for i in range(self.r):
                    if self.m[i,j] == maxvalue:
                        bestresponses.append(i)
                a+=1
        bestresponses.append('.')
        return bestresponses
    
    def p2bestresponse(self):
        """
        This method searched the payouts of Player 2 given estrategies of Player 1. It will return a 
        list of the best responses for Player 1. The list consists of strings and intergers.
        """
        bestresponses = []
        for i in range(self.r):
            bestresponses.append(".")
            j2pay=[]
            for j in range(self.c):
                if j % 2 != 0:
                    j2pay.append(self.m[i,j])
            maxvalue = max(j2pay)
            for a in range(len(j2pay)):
                if j2pay[a] == maxvalue:
                    bestresponses.append(a)
        bestresponses.append('.')
        return bestresponses
    
    def createBRpairs(self):
        """
        This method will create the pair of best responses by player, in order to find the Nash equilibrium
        """
        br1 = self.p1bestresponse()
        br2 = self.p2bestresponse()
        idx1 = [i for i,v in enumerate(br1) if v in [ '.']]
        idx2 = [i for i,v in enumerate(br2) if v in [ '.']]
        idx12 = [ (idx1[i]+1,idx1[i+1]) for i in range(len(idx1)-1)]
        idx22 = [ (idx2[i]+1,idx2[i+1]) for i in range(len(idx2)-1)]
        BR1=[]
        BR2=[]
        n=0 # what does player 2 play
        for a,b in idx12:
            for t in br1[a:b]:
                    BR1.append([t,n])
            n+=1    
        n=0 #what does player 1 play
        for a,b in idx22: 
            for t in br2[a:b]:
                    BR2.append([n,t])
            n+=1
        return BR1, BR2
    
    def comparepairs(self):
        """
        This method will calculate the position of the nash equilibria, by comparing what pair of choices are
        the best response for player 1 and player 2
        """
        list_nash = []
        BR1, BR2 = self.createBRpairs()
        l = 0
        for i1 in BR1:
            for i2 in BR2:
                if i1 == i2:
                    l+=1
                    list_nash.append(f"A nash equilibrium was found in the pair of actions P1 : {i1[0]+1} and P2: {i1[1]+1}")
        if l == 0:
            list_nash.append(f"No pure nash equilibrium was found")
        return list_nash

game1 = np.matrix([[1,1,1,1],[1,1,1,1]])
a = PureNash(game1)

for b in a.comparepairs():
    print(b)