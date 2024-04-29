import numpy as np

# Define the MDP environment
class GridWorldMDP:
    def __init__(self, n_rows, n_cols, gamma, R):
        self.n_rows = n_rows
        self.n_cols = n_cols
        self.gamma = gamma
        self.R = R
        self.states = [(i, j) for i in range(n_rows) for j in range(n_cols)]
        self.actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        self.transition_probs = {
            'UP': (-1, 0),
            'DOWN': (1, 0),
            'LEFT': (0, -1),
            'RIGHT': (0, 1)
        }

    def is_terminal(self, state):
        return state not in [(0, 0), (3, 2)]

    def step(self, state, action):
        if self.is_terminal(state):
            return state, 0
        next_row = max(0, min(state[0] + self.transition_probs[action][0], self.n_rows - 1))
        next_col = max(0, min(state[1] + self.transition_probs[action][1], self.n_cols - 1))
        next_state = (next_row, next_col)
        reward = self.R
        return next_state, reward

# Passive Direct Utility Estimation
def passive_direct_utility_estimation(mdp, policy, n_trials):
    state_values = np.zeros((mdp.n_rows, mdp.n_cols))
    returns = {(i, j): [] for i in range(mdp.n_rows) for j in range(mdp.n_cols)}

    for _ in range(n_trials):
        episode = []
        state = (0, 0)
        while not mdp.is_terminal(state):
            action = policy[state]
            next_state, reward = mdp.step(state, action)
            episode.append((state, reward))
            state = next_state

        G = 0
        for t in range(len(episode) - 1, -1, -1):
            state, reward = episode[t]
            G = mdp.gamma * G + reward
            if state not in [x[0] for x in episode[:t]]:
                returns[state].append(G)
                state_values[state] = np.mean(returns[state])

    return state_values

# Define the optimal policy
optimal_policy = {
    (0, 0): 'RIGHT', (0, 1): 'RIGHT', (0, 2): 'RIGHT',
    (1, 0): 'UP',    (1, 1): None,    (1, 2): 'LEFT',
    (2, 0): 'UP',    (2, 1): 'UP',    (2, 2): 'LEFT',
    (3, 0): 'UP',    (3, 1): 'UP',    (3, 2): None
}

# Define the random policy
random_policy = {
    (i, j): np.random.choice(['UP', 'DOWN', 'LEFT', 'RIGHT']) for i in range(4) for j in range(3)
}

# Define constants
gamma = 1
R = -0.04
n_trials = 1000

# Create MDP instance
mdp = GridWorldMDP(n_rows=4, n_cols=3, gamma=gamma, R=R)

# Evaluate optimal policy
optimal_state_values = passive_direct_utility_estimation(mdp, optimal_policy, n_trials)
print("Optimal Policy State Values:")
print(optimal_state_values)

# Evaluate random policy
random_state_values = passive_direct_utility_estimation(mdp, random_policy, n_trials)
print("\nRandom Policy State Values:")
print(random_state_values)