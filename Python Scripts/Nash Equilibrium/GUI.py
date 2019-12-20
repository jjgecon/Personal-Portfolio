import tkinter as tk
import numpy as np
import math

#Code by Javier Gonzalez on September 2019
#For any questions please contact javierj.g18@gmail.com

#Nash Class
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
    def returnpairs(self):
        """
        This method will return the postion of the nash equilibria.
        """
        list_nash = []
        BR1, BR2 = self.createBRpairs()
        l = 0
        for i1 in BR1:
            for i2 in BR2:
                if i1 == i2:
                    l+=1
                    list_nash.append(i1[0]+1)
                    list_nash.append(i1[1]+1)
        list_nash = np.asmatrix(list_nash).reshape((l, 2))
        return list_nash

#Global GUI Functions
def inputpayoutmatrix(rows1,columns1):
    for c in range(columns1):
        for r in range(rows1):
            if c % 2 == 0:
                # in_label = tk.Label(master=payinout_frame,text=f'P1 ({r+1}) P2 ({int(c/2)+1}) :')
                # in_label.pack()
                in_payout = tk.Entry(master=main_frame)
                in_payout.insert(0,f"Payout for P1 ({r+1},{int(c/2)+1})")
                in_payout.grid(row=r,column=c)  
            else:
                # in_label = tk.Label(master=payinout_frame,text=f'P1 ({r+1}) P2 ({int(math.floor(c/2))+1}) :')
                # in_label.pack()    
                in_payout = tk.Entry(master=main_frame)
                in_payout.insert(0,f"Payout for P2 ({r+1},{int(math.floor(c/2))+1})")
                in_payout.grid(row=r,column=c)  

def prisdilema():

    actionP1.insert(0,2)
    actionP2.insert(0,2)

    in_payout = tk.Entry(master=main_frame)
    in_payout.insert(0,-8)
    in_payout.grid(row=0,column=0)  
    in_payout = tk.Entry(master=main_frame)
    in_payout.insert(0,-20)
    in_payout.grid(row=1,column=0)

    in_payout = tk.Entry(master=main_frame)
    in_payout.insert(0,-8)
    in_payout.grid(row=0,column=1)  
    in_payout = tk.Entry(master=main_frame)
    in_payout.insert(0,0)
    in_payout.grid(row=1,column=1)

    in_payout = tk.Entry(master=main_frame)
    in_payout.insert(0,0)
    in_payout.grid(row=0,column=2)  
    in_payout = tk.Entry(master=main_frame)
    in_payout.insert(0,-1)
    in_payout.grid(row=1,column=2)  

    in_payout = tk.Entry(master=main_frame)
    in_payout.insert(0,-20)
    in_payout.grid(row=0,column=3)
    in_payout = tk.Entry(master=main_frame)
    in_payout.insert(0,-1)
    in_payout.grid(row=1,column=3)

    calc_nash_clear.pack(side=tk.LEFT,padx=6)
    calc_nash_b.pack(side=tk.LEFT,padx=6)
    prisonersdilemab.forget()

def get_r_c():
    rows1 = int(actionP1.get())
    columns1 = int(actionP2.get())*2
    inputpayoutmatrix(rows1,columns1)
    input_matrix.forget()
    templategames.forget()
    calc_nash_clear.pack(side=tk.LEFT,padx=6)
    calc_nash_b.pack(side=tk.LEFT,padx=6)


def search_destroy():
    extra_widgets1 = main_frame.grid_slaves()
    extra_widgets2 = results_frame.pack_slaves()
    for l in extra_widgets1:
        l.destroy()
    for i in extra_widgets2:
        i.destroy()
    input_matrix.pack(side=tk.LEFT,padx=6)
    templategames.pack(side=tk.LEFT,padx=6)
    calc_nash_b.forget()
    calc_nash_clear.forget()
    results_frame.forget()
    actionP2.delete(0,last=10)
    actionP1.delete(0,last=10)


def get_entries():
    rows1 = int(actionP1.get())
    columns1 = int(actionP2.get())*2
    
    #Destroy old results
    extra_widgets2 = results_frame.pack_slaves()
    for i in extra_widgets2:
        i.destroy()
    
    #Clear Nash bg colors
    entrylist = main_frame.grid_slaves()
    inm = []
    for i in entrylist:
        inm.append(int(i.get()))
        i.config(background='white')

    # label = tk.Label(master=results_frame,text=f'{inm}')
    # label.pack()

    inm = inm[::-1]

    results_frame.pack(fill=tk.X,pady=2)

    payoutmatrix=np.asmatrix(inm).reshape((columns1, rows1)).T

    a = PureNash(payoutmatrix)

    for b in a.comparepairs():
        outputresults = tk.Label(master=results_frame,text=f'{b}')
        outputresults.pack()

    #This part will color the backgorund of the Nash Equilibriums

    for i in range(a.returnpairs().shape[0]):
        r1,c1 = a.returnpairs()[i,0],a.returnpairs()[i,1]

        if c1 % 2 == 0:
            cell = main_frame.grid_slaves(row=r1-1, column=c1)
            cell[0].config(background='yellow')
            cell = main_frame.grid_slaves(row=r1-1, column=c1+1)
            cell[0].config(background='yellow')
        else:
            cell = main_frame.grid_slaves(row=r1-1, column=c1-1)
            cell[0].config(background='yellow')
            cell = main_frame.grid_slaves(row=r1-1, column=c1)
            cell[0].config(background='yellow')

def templates():
    prisonersdilemab.pack()
    input_matrix.forget()
    templategames.forget()


#Global Varaibles
rows1,columns1 = 0,0
extra_widgets1,extra_widgets2,extra_widgets3 = [],[],[]
#Columns and Rows inputs
window = tk.Tk()
window.title("Nash Equilibrium")

tittle_frame=tk.Frame(master=window,relief = 'sunken',borderwidth=2)
tittle1 = tk.Label(master=tittle_frame,text='Insert how many actions each player has:')
tittle1.pack()
tittle_frame.pack(fill = tk.X,pady=6)

in_frame1 = tk.Frame(master=window)
in_frame1.pack()

f1 = tk.Frame(master=in_frame1)
f1.pack()
actionP1_label = tk.Label(master=f1,text=f'Number of player 1 actions:')
actionP1_label.pack(side=tk.LEFT)
actionP1 = tk.Entry(master=f1)
actionP1.pack(padx=10)

f2 = tk.Frame(master=in_frame1)
f2.pack()
actionP2_label = tk.Label(master=f2,text=f'Number of player 2 actions:')
actionP2_label.pack(side=tk.LEFT)
actionP2 = tk.Entry(master=f2)
actionP2.pack(padx=10)

legend_frame = tk.Frame(master=window,relief = 'sunken',borderwidth=2)
legend_frame.pack(pady=6,fill=tk.X)

main_frame=tk.Frame(master=window)
main_frame.pack(pady=6,padx=6)

results_frame = tk.Frame(master=window,relief = 'sunken',borderwidth=2)
legend = tk.Label(master=legend_frame,text='Legend : (A1,A2) A1 Action of player 1 and A2 Action of player 2')
legend.pack()

in_frame3 = tk.Frame(master=window)
in_frame3.pack()
input_matrix = tk.Button(master=in_frame3,text='Input Payout Matrix',command = get_r_c,borderwidth=2)
input_matrix.pack(side = tk.LEFT,padx=6)
templategames = tk.Button(master=in_frame3,text='Template Games',command = templates,borderwidth=2)
templategames.pack(side = tk.LEFT,padx=6)
but2_frame=tk.Frame(master=window)
but2_frame.pack(side=tk.BOTTOM,pady=2)
calc_nash_b = tk.Button(master=but2_frame,text='Calculate Nash Equilibrums',command = get_entries ,borderwidth=2)
calc_nash_clear = tk.Button(master=but2_frame,text='Clear and Redo',command=search_destroy,borderwidth=2)
prisonersdilemab = tk.Button(master=in_frame3,command=prisdilema,text='Prisoners Delima')

window.mainloop()
