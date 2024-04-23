from random import random
import matplotlib.pyplot as plt
 
TRIALS = 10**6
evidence = 0
query = 0
pall = []
pdenomall = []
 
for trial in range(1,TRIALS+1):
    randA, randB, randC, randD = ( random() for i in range(4) )
    A = (randA < 0.5)
    if A:
      B = (randB < 1.0)
      C = (randC < 1.0)
    else: 
      B = (randB < 0.5)
      C = (randC < 0.5)
    if B and C:
        D = (randD < 1.00)
    elif B and not C:
        D = (randD < 0.5)
    elif not B and C:
        D = (randD < 0.5)
    else: 
        D = (randD < 0.0)
 
    # REJECTION SAMPLING: ONLY PROCESS IF EVIDENCE True
    if D:
        evidence += 1
        if A:
            query += 1
        p = query/evidence
        pall.append(p)
    pdenom = evidence/trial
    pdenomall.append(pdenom)
 
print("P(A|D) ~=", pall[-1])
print("P(A) ~=", pdenomall[-1])
print("P(A,D) ~=", pall[-1]*pdenomall[-1])
plt.plot(pall, label = 'Pall')
plt.plot(pdenomall, label = 'Pdenomall')
plt.legend()
plt.show()