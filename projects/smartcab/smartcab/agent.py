import random
from environment import Agent, Environment
from planner import RoutePlanner
from simulator import Simulator

class LearningAgent(Agent):
    """An agent that learns to drive in the smartcab world."""

    def __init__(self, env):
        super(LearningAgent, self).__init__(env)  # sets self.env = env, state = None, next_waypoint = None, and a default color
        self.color = 'red'  # override color
        self.planner = RoutePlanner(self.env, self)  # simple route planner to get next_waypoint

        # Initialize any additional variables here

    def reset(self, destination=None):
        self.planner.route_to(destination)

        # Prepare for a new trip; reset any variables here, if required
        self.next_waypoint = None

    def update(self, t):
        # Gather inputs
        self.next_waypoint = self.planner.next_waypoint()  # from route planner, also displayed by simulator
        inputs = self.env.sense(self)
        deadline = self.env.get_deadline(self)

        # Update state
        state = {'next_waypoint': self.next_waypoint, 'inputs': inputs }
        
        # Select action according to your policy
        action = self._select_action(state)

        # Execute action and get reward
        reward = self.env.act(self, action)

        # Learn policy based on state, action, reward
        self._learn(state, action, reward)

        print "LearningAgent.update(): state = {}, action = {}, reward = {}, deadline = {}".format(state, action, reward, deadline)  # [debug]

    def _select_action(self, state) :
        # TODO: Select action according to your policy
        actions = [None, 'forward', 'left', 'right']
        return random.choice(actions)

    def _learn(self, state, action, reward) :
        # TODO: Learn policy based on state, action, reward
        pass

def run():
    """Run the agent for a finite number of trials."""

    # Set up environment and agent
    e = Environment()  # create environment (also adds some dummy traffic)
    a = e.create_agent(LearningAgent)  # create agent
    e.set_primary_agent(a, enforce_deadline=True)  # specify agent to track
    # NOTE: You can set enforce_deadline=False while debugging to allow longer trials

    # Now simulate it
    sim = Simulator(e, update_delay=0.001, display=False)  # create simulator (uses pygame when display=True, if available)
    # NOTE: To speed up simulation, reduce update_delay and/or set display=False

    sim.run(n_trials=100)  # run for a specified number of trials
    # NOTE: To quit midway, press Esc or close pygame window, or hit Ctrl+C on the command-line


if __name__ == '__main__':
    run()
