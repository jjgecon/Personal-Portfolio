import numpy as np
import math

#Code by Javier Gonzalez on September 2019
#For any questions please contact javierj.g18@gmail.com

r_input = int(input("How many Actions does Player 1 have?"))
c_input = int(input("How many Actions does Player 2 have?"))*2
x = np.zeros((r_input,c_input))
for r in range(r_input):
    for c in range(c_input):
        print(r,c)
        if c % 2 == 0:
            x[r,c] = input(f"Payout for P1 when P1 plays {r} and P2 {int(c/2)}")
        else:
            x[r,c] = input(f"Payout for P2 when P1 plays {r} and P2 {int(math.floor(c/2))}")
print(x)
