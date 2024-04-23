#Source- This code is modified, used, and borrowed from EECS 649: Lec 2 - The Turing Test's Simulated Luenberger's Weather Model's Python Code.

import random

#States are Heads (H) and Tails (T).
def func(set, state, HT, TH):
  incorrect = 0
  for i in range(10):
    r = random.random() #Pick a random number from 0 to 1.
    if (state == "H"):
      if r <= HT:  #HT probability state changes to tails. If not, then the state is unchanged.
        nextstate = "T"
      else:
        nextstate = "H"
    elif (state == "T"):
      if r <= TH:  #TH probability state changes to heads. If not, then the state is unchanged.
        nextstate = "H"
      else:
        nextstate = "T"
    if nextstate != set[i]: #The number of wrong guesses is recorded if states and data set's states are not same.
      incorrect+=1 
    state = nextstate
    if state == "H": #The state H is added in the string of H and T if the condition is true.
      print("H", end=' ')
    elif state == "T": #The state T is added in the string of H and T if the condition is true.
      print("T", end=' ')
  print("")
  print(incorrect, "wrong guesses") #Tally the number of wrong guesses.
  print("")
 
actual_firstset = ["T", "H", "H", "H", "H", "T", "H", "H", "T", "H"] #The last 10 transitions and their values of the first data set.
actual_secondset = ["H", "T", "T", "H", "H", "T", "T", "H", "T", "H"]  #The last 10 transitions and their values of the second data set.
initial_state = "H" #The initial state or H.
print(*actual_firstset) #The first data set.
output = func(actual_firstset, initial_state, 0.5, 0.5) #The output for the first data set. (HT Probability = 0.5, and TH Probability = 0.5) 
print(*actual_secondset) #The second data set.
output2 = func(actual_secondset, initial_state, 0.7, 0.6) #The output for the second data set. (HT Probability = 0.7, and TH Probability = 0.6)
