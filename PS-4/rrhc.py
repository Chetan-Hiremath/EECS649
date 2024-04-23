import numpy as np
import random
 
#Return the number of queens conflicting in grid.
def fitness(queens, N):
    c = 0
    for q in range(len(queens)):
        for q_y in range(len(queens)):
            q_x = queens[q_y]
            if q_y != q: # Check if queens are not attacking each other.
                if q_x == queens[q]:
                    c += 1
                if abs(q - q_y) == abs(queens[q] - q_x):
                    c += 1
    return (N*(N-1))/2 - c
 
#Code Parameters
N = 8 #Grid size or number of queens
i = 0 #Evaluation count
 
#Use RRHC algorithm for the n-queens problem to print the string of digits.
for x in range(1):
    count = 0
    success = False
    while not success:
        queens = []
        count +=1
        i+=1
        #Random start state for queen n
        queens = []
        for n in range(N):
            queens.append(random.randint(0,N-1))
        #If there is a solution, then it breaks the loop and prints the solution.
        if fitness(queens, N) == N*(N-1)/2:
            print(queens)
            success = True
print('Total number of fitness evaluations: ' + str(i))
print('Average:', (i/100))