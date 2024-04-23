from random import random
 
TRIALS = 10**7
probs = {'B': [0.001], 'E': [0.002], 'A': [[0.001, 0.29], [0.95, 0.98]], 'J': [0.01, 0.95], 'M': [0.01, 0.70]}
 
def likelihood_weighting(B, e, Q, n):
    counts = [0,0]
    for trial in range(1,n+1):
        sample = {}
        weight = 1
        for x in B:
            if x in e:
                v = e[x]
                sample[x] = v
                if x == 'B' or x == 'E':
                    weight *= (B[x][0]) if sample[x] else (1 - B[x][0])
                elif x == 'A':
                    weight *= (B[x][sample['B']][sample['E']]) if sample[x] else (1 - B[x][sample['B']][sample['E']])
                elif x == 'J' or x == 'M':
                    weight *= (B[x][sample['A']]) if sample[x] else (1 - B[x][sample['A']])
            else:
                if x == 'A':
                    sample[x] = (random() < B[x][sample['B']][sample['E']])
                elif x == 'J' or x == 'M':
                    sample[x] = (random() < B[x][sample['A']])
                elif x == 'B' or x == 'E':
                    sample[x] = (random() < B[x][0])
        v = sample[Q]
        counts[v] += weight
    return [round(x / sum(counts), 3) for x in counts]
 
p_b = probs['B'][0]
p_e = probs['E'][0]
e = {'M': False, 'B': True, 'E': True}
P_j = likelihood_weighting(probs, e, 'J', TRIALS)
p_j = P_j[0]
e = {'B': True, 'E': True}
P_m = likelihood_weighting(probs, e, 'M', TRIALS)
p_m = P_m[0]
 
print('P(-J, -M, B, E) =', p_j*p_m*p_b*p_e)