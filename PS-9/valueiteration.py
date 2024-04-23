import numpy as np
 
R = -1
def actionRewardFunction(initialPosition, action):
    if initialPosition in termination_states:
        return initialPosition, 0
    finalPosition = np.add(initialPosition, action)
    if R in finalPosition or finalPosition[0] == gridSize[0] or finalPosition[1] == gridSize[1] or (finalPosition == [1,1]).all():
        finalPosition = initialPosition
    return finalPosition, R
def otherActions(action):
    if action == 0 or action == 2:
        return 1, 3
    else:
        return 0, 2
 
gamma = 1
gridSize = [4,3]
termination_states = [[3,2], [3,1]]
states = [[i,j] for i in range(gridSize[0]) for j in range(gridSize[1])]
states.remove([1,1])
actions = {0: [1,0], 1: [0,1], 2: [-1,0], 3: [0,-1]}
values = np.zeros((4,3))
values[3][2] = 1
values[3][1] = -1
print("Initial Iteration")
print(values)
print()
 
for i in range(100):
    copyValues = np.copy(values)
    for s in states:
        q_values = {a: 0 for a in actions}
        for a in actions:
            s_, reward = actionRewardFunction(s, actions[a])
            q_values[a] += 0.8*(reward + gamma*values[s_[0], s_[1]])
            for a_ in otherActions(a):
                s_, reward = actionRewardFunction(s, actions[a_])
                q_values[a] += 0.1*(reward + gamma*values[s_[0], s_[1]])
        copyValues[s[0], s[1]] = np.max(list(q_values.values()))
    comparison = values == copyValues
    values = copyValues
 
    if (comparison).all():
        print("Final Iteration")
        print(values)
        break