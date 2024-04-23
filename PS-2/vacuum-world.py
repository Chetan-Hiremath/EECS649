from mimetypes import init
import random

class TrivialVacuumEnvironment():

    """This environment has two locations, A and B. Each can be Dirty
    or Clean. The agent perceives its location and the location's
    status. This serves as an example of how to implement a simple
    Environment."""

    def __init__(self, loc_A_status, loc_B_status):
        super().__init__()
        self.status = {loc_A: loc_A_status,
                       loc_B: loc_B_status}

    def percept(self, agent):
        """Returns the location status (Dirty/Clean)."""
        return (self.status[agent.location])

    def execute_action(self, agent, action):
        """Change agent's location and/or location's status; track performance.
        Score 10 for each dirt cleaned; -1 for each move."""
        if action == 'Right':
            agent.location = loc_B
        elif action == 'Left':
            agent.location = loc_A
        elif action == 'Suck':
            self.status[agent.location] = 'Clean'
        if self.status[loc_A] == 'Clean':
            agent.performance += 1
        if self.status[loc_B] == 'Clean':
            agent.performance += 1

class simple_reflex_agent():
    def __init__(self, location):
        self.location = location
        self.performance = 0
    
    """This agent takes action based solely on the percept. [Figure 2.10]""" 
    def action(self, percept):
        return ('Suck' if percept == 'Dirty' else 'Right' if self.location == loc_A else'Left')

# They are the two locations for the two-state environment
loc_A = (0, 0)
loc_B = (1, 0)

# All possible combinations of location status and initial location
location_state_combinations = [
('Dirty', 'Dirty', loc_A),
('Dirty', 'Dirty', loc_B),
('Clean', 'Clean', loc_A),
('Clean', 'Clean', loc_B),
('Dirty', 'Clean', loc_A),
('Dirty', 'Clean', loc_B),
('Clean', 'Dirty', loc_A),
('Clean', 'Dirty', loc_B)]
# Total score of average score calculation
gross_score = 0
for init_status in location_state_combinations:
    print('Initial state: [{}, {}, {}]'.format(init_status[0], init_status[1], 'A' if init_status[2] == loc_A else 'B'))
    environment = TrivialVacuumEnvironment(init_status[0], init_status[1])    
    reflex_agent = simple_reflex_agent(location=init_status[2])
    for i in range(1000):
        percept = environment.percept(agent=reflex_agent)
        action = reflex_agent.action(percept)
        exc = environment.execute_action(agent=reflex_agent, action=action)
    print("Performance: {}".format(reflex_agent.performance))
    print()
    gross_score+=reflex_agent.performance
print('Average score: {}'.format(gross_score/len(location_state_combinations)))