import random
from random import choice

def turn_right(direction):
    x, y = direction
    return y, -x

def turn_left(direction):
    x, y = direction
    return -y, x

def vector_add(a, b):
    """Component-wise addition of two vectors."""
    return tuple(map(sum, zip(a, b)))

def argmax(seq, fn):
    """Return an element with the highest fn(seq[i]) score; tie goes to the first one."""
    best = seq[0]; best_score = fn(best)
    for x in seq:
        x_score = fn(x)
        if x_score > best_score:
            best, best_score = x, x_score
    return best

def random_policy(mdp, state):
    """Choose an action at random."""
    return choice(mdp.actions(state))

class MDP:
    """A Markov Decision Process, defined by an initial state, transition model,
    and reward function. We also keep track of a gamma value, for use by
    algorithms. The transition model is represented somewhat differently from
    the text. Instead of T(s, a, s') being a probability number for each
    state/action/state triplet, we instead have T(s, a) return a list of (p, s')
    pairs. We also keep track of the possible states, terminal states, and
    actions for each state. [page 615]"""

    def __init__(self, init, actlist, terminals, gamma=.9):
        self.init = init
        self.actlist = actlist
        self.terminals = terminals
        self.gamma = gamma
        self.states = set()
        self.reward = {}

    def R(self, state):
        """Return a numeric reward for this state."""
        return self.reward[state]

    def T(self, state, action):
        """Transition model. From a state and an action, return a list
        of (result-state, probability) pairs."""
        raise NotImplementedError("T method must be implemented in subclasses")

    def actions(self, state):
        """Set of actions that can be performed in this state. By default, a
        fixed list of actions, except for terminal states. Override this
        method if you need to specialize by state."""
        if state in self.terminals:
            return [None]
        else:
            return self.actlist

class GridMDP(MDP):
    """A two-dimensional grid MDP, as in [Figure 17.1]. All you have to do is
    specify the grid as a list of lists of rewards; use None for an obstacle
    (unreachable state). Also, you should specify the terminal states.
    An action is an (x, y) unit vector; e.g. (1, 0) means move east."""

    def __init__(self, grid, terminals, init=(0, 0), gamma=.9):
        grid.reverse()  # because we want row 0 on the bottom, not on the top
        super().__init__(init, actlist=((1, 0), (0, 1), (-1, 0), (0, -1)), terminals=terminals, gamma=gamma)
        self.grid = grid
        self.rows = len(grid)
        self.cols = len(grid[0])
        for x in range(self.cols):
            for y in range(self.rows):
                self.reward[x, y] = grid[y][x]
                if grid[y][x] is not None:
                    self.states.add((x, y))

    def T(self, state, action):
        if action is None:
            return [(0.0, state)]
        else:
            return [(0.8, self.go(state, action)),
                    (0.1, self.go(state, turn_right(action))),
                    (0.1, self.go(state, turn_left(action)))]

    def go(self, state, direction):
        """Return the state that results from going in this direction."""
        state1 = vector_add(state, direction)
        return state1 if state1 in self.states else state

    def to_grid(self, mapping):
        """Convert a mapping from (x, y) to v into a [[..., v, ...]] grid."""
        return list(reversed([[mapping.get((x, y), None)
                               for x in range(self.cols)]
                              for y in range(self.rows)]))

    def to_arrows(self, policy):
        chars = {(1, 0): '>', (0, 1): '^', (-1, 0): '<', (0, -1): 'v', None: '.'}
        return self.to_grid(dict([(s, chars[a]) for (s, a) in policy.items()]))

def value_iteration(mdp, epsilon=0.001):
    """Solving an MDP by value iteration. [Fig. 17.4]"""
    U1 = {s: 0 for s in mdp.states}
    R, T, gamma = mdp.R, mdp.T, mdp.gamma
    while True:
        U = U1.copy()
        delta = 0
        for s in mdp.states:
            U1[s] = R(s) + gamma * max([sum([p * U[s1] for (p, s1) in T(s, a)])
                                        for a in mdp.actions(s)])
            delta = max(delta, abs(U1[s] - U[s]))
        if delta < epsilon * (1 - gamma) / gamma:
            return U

def best_policy(mdp, U):
    """Given an MDP and a utility function U, determine the best policy,
    as a mapping from state to action. (Equation 17.4)"""
    pi = {}
    for s in mdp.states:
        pi[s] = argmax(mdp.actions(s), lambda a: expected_utility(a, s, U, mdp))
    return pi

def expected_utility(a, s, U, mdp):
    """The expected utility of doing a in state s, according to the MDP and U."""
    return sum([p * U[s1] for (p, s1) in mdp.T(s, a)])

def policy_iteration(mdp):
    """Solve an MDP by policy iteration [Fig. 17.7]"""
    U = {s: 0 for s in mdp.states}
    pi = {s: choice(mdp.actions(s)) for s in mdp.states}
    while True:
        U = policy_evaluation(pi, U, mdp)
        unchanged = True
        for s in mdp.states:
            a = argmax(mdp.actions(s), lambda a: expected_utility(a, s, U, mdp))
            if a != pi[s]:
                pi[s] = a
                unchanged = False
        if unchanged:
            return pi

def policy_evaluation(pi, U, mdp, k=20):
    """Return an updated utility mapping U from each state in the MDP to its
    utility, using an approximation (modified policy iteration)."""
    R, T, gamma = mdp.R, mdp.T, mdp.gamma
    for _ in range(k):
        for s in mdp.states:
            U[s] = R(s) + gamma * sum([p * U[s1] for (p, s1) in T(s, pi[s])])
    return U

def pDUE(mdp, trails=1000, alpha=0.1):
    util = {state: 0 for state in mdp.states}
    counts = {state: 0 for state in mdp.states}
    for _ in range(trails):
        state = mdp.init
        while state not in mdp.terminals:
            action = random_policy(mdp, state)
            next_state, reward = random.choice(mdp.T(state, action))
            counts[state] += 1
            util[state] += (reward + mdp.gamma * util[next_state] - util[state]) / counts[state]
            state = next_state
    return util

# Corrected instantiation of GridMDP
grid_mdp = GridMDP([[-0.04, -0.04, -0.04, 1], [-0.04, None, -0.04, -1], [-0.04, -0.04, -0.04, -0.04]], terminals=[(3, 2), (3, 1)], gamma=1)

estimated_utilities_random = pDUE(grid_mdp)
utility_grid = grid_mdp.to_grid(estimated_utilities_random)
for row in utility_grid:
    print([f"{value:.2f}" if value is not None else "None" for value in row])
