import numpy as np
import random
 
def fitness(queens, N):
    global total_f
    global f
    f += 1
    total_f += 1
    c = 0 # Number of conflicts
    #Return the number of queens conflicting in grid.
    for q in range(len(queens)):
        for q_y in range(len(queens)):
            q_x = queens[q_y]
            if q_y != q: # Check all other queens
                if q_x == queens[q]: # If queens are in same column
                    c += 1
                if abs(q - q_y) == abs(queens[q] - q_x): # If queens share a diagonal
                    c += 1
    return (N*(N-1))/2 - c
 
#Choose the successor by the Min-Conflict algorithm.
def successor(queens, N):
    global rand_choice
    global last_q
    if rand_choice:     # Random choice queen
        q = random.choice(queens)
    else:               # Cyclic choice queen
        last_q = (last_q + 1) % N
        q = last_q
    successors = []     # Successor states for queen q
    for i in range(N):  # Each possible position for q
        qc = queens.copy()
        qc[q] = i
        successors.append(qc)
    best_f = -1         # Fitness of best successor
    for s in successors:
        f = fitness(s,N)
        if f > best_f:
            best_s = s  # Update best successor
            best_f = f  # Update best fitness
    return best_s
 
#Code Parameters
success = False
x = 0   # Iteration of function evaluation
total_f = 0 # Total number of evaluations
f = 0   # Number of evaluations per attempt
s_total_f = 0   # Successful number of evaluations
 
while x < 1:
    rand_choice = False # Choose random queen to minimize conflict; cyclic if False
    last_q = -1 # Last evaluated queen (for cyclic queen selection)
    N = 8       # Grid size, number of queens
    i = 0       # Epoch count
    queens = []
    for n in range(N):
        queens.append(random.randint(0,N-1))
    for i in range(25):
        queens = successor(queens,N)
        #If there is a solution, then it breaks the loop and prints the solution and results.
        if fitness(queens,N) == (N*(N-1))/2:
            print(queens)
            success = True
            total_f += i
            break
    if success == True:
        success = False
        x+=1
print('Total number of fitness evaluations:', total_f)
print('Average:',(total_f/100))