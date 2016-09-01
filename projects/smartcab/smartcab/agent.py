import random
from environment import Agent, Environment
from planner import RoutePlanner
from simulator import Simulator
import pandas as pd
import matplotlib.pyplot as plt

class RandomAgent(Agent):
    """An agent that learns to drive in the smartcab world."""

    def __init__(self, env):
        super(RandomAgent, self).__init__(env)  # sets self.env = env, state = None, next_waypoint = None, and a default color
        self.color = 'red'  # override color
        self.planner = RoutePlanner(self.env, self)  # simple route planner to get next_waypoint
        self.possible_actions = (None, 'forward', 'left', 'right')
        self.total_reward = 0
        self.was_penalized = False

    def reset(self, destination=None):
        """Reset variables used to record information about each trial.
    	
    	No parameters.
    	
    	No return value."""
        self.planner.route_to(destination)

    def update(self, t):
        """Update the learning agent.
    	
    	No Parameters.
    	
    	No Return value."""
        # Update state
        state, deadline = self._get_state()
        
        # Select action according to your policy
        action = self._select_action(state)

        # Execute action and get reward
        reward = self.env.act(self, action)

        if reward < 0:
            self.was_penalized = True

        self.total_reward += reward

        # Learn policy based on state, action, reward
        self._learn(state, action, reward)

    def _get_state(self) :
        # Gather inputs
        self.next_waypoint = self.planner.next_waypoint()  # from route planner, also displayed by simulator
        inputs = self.env.sense(self)
        deadline = self.env.get_deadline(self)

        return tuple(inputs.values()), deadline

    def _select_action(self, state) :
        # return one of the possible actions at random
        return random.choice(self.possible_actions)

    def _learn(self, state, action, reward) :
        pass

    def get_total_reward(self):
        return self.total_reward

    def _get_q_value(self, state, action):
        return self.q_table.get((state, action), 0)

class LearningAgent(Agent):
    """An agent that learns to drive in the smartcab world."""

    def __init__(self, env):
        super(LearningAgent, self).__init__(env)  # sets self.env = env, state = None, next_waypoint = None, and a default color
        self.color = 'red'  # override color
        self.planner = RoutePlanner(self.env, self)  # simple route planner to get next_waypoint

        # Initialize any additional variables here
        self.total_reward = 0
        self.was_penalized = False

        self.possible_actions = (None, 'forward', 'left', 'right')
        self.q_table = {}
        self.alpha = 0.3
        self.gamma = 0.2

    def reset(self, destination=None):
        """Reset variables used to record information about each trial.
    	
    	No parameters.
    	
    	No return value."""
        self.planner.route_to(destination)

        # Prepare for a new trip; reset any variables here, if required
        self.next_waypoint = None
        self.total_reward = 0
        self.was_penalized = False

    def update(self, t):
        """Update the learning agent.
    	
    	No Parameters.
    	
    	No Return value."""
        # Update state
        state, deadline = self._get_state()
        
        # Select action according to your policy
        action = self._select_action(state)

        # Execute action and get reward
        reward = self.env.act(self, action)

        if reward < 0:
            self.was_penalized = True

        self.total_reward += reward

        # Learn policy based on state, action, reward
        self._learn(state, action, reward)

        #print "LearningAgent.update(): state = {}, action = {}, reward = {}, deadline = {}".format(state, action, reward, deadline)  # [debug]

    def _get_state(self) :
        # Gather inputs
        self.next_waypoint = self.planner.next_waypoint()  # from route planner, also displayed by simulator
        inputs = self.env.sense(self)
        deadline = self.env.get_deadline(self)

        # include the next_waypoint into the state
        inputs['next_waypoint'] = self.next_waypoint

        # remove the right value as it is not needed.
        del inputs['right']

        return tuple(inputs.values()), deadline

    def _select_action(self, state) :
        # get all possible q-values for the state
        all_q_vals = { action: self._get_q_value(state, action)
                        for action in self.possible_actions }

        best_q_value = max(all_q_vals.values())

        # pick the actions that yield the largest q-value for the state
        best_actions = [action for action in self.possible_actions 
                        if all_q_vals[action] == best_q_value]

        # return one of the best actions at random
        return random.choice(best_actions)

    def _learn(self, state, action, reward) :
        # Q learning method 1 as described on https://discussions.udacity.com/t/next-state-action-pair/44902/11?u=limowankenobi
        # and https://www-s.acm.illinois.edu/sigart/docs/QLearning.pdf

        # get the state after the action was executed
        new_state, deadline = self._get_state()

        # get all possible q-values for actions in the new state
        all_q_vals = { action: self._get_q_value(new_state, action)
                        for action in self.possible_actions }

        # get the max q value for all actions in the new state
        max_q_value = max(all_q_vals.values())

        # Q(s,a) =(alpha) r + gamma * argmax_a'(s',a')
        self.q_table[(state, action)] = ((1 - self.alpha) * self._get_q_value(state, action)) + self.alpha * (reward + self.gamma * max_q_value)

    def get_total_reward(self):
        return self.total_reward

    def _get_q_value(self, state, action):
        return self.q_table.get((state, action), 0)

def run(n_trials, learning_agent):
    """Run the agent for a finite number of trials."""

    # Set up environment and agent
    e = Environment()  # create environment (also adds some dummy traffic)
    a = e.create_agent(learning_agent)  # create agent
    e.set_primary_agent(a, enforce_deadline=True)  # specify agent to track
    # NOTE: You can set enforce_deadline=False while debugging to allow longer trials

    # Now simulate it
    sim = Simulator(e, update_delay=0.00005, display=False)  # create simulator (uses pygame when display=True, if available)
    # NOTE: To speed up simulation, reduce update_delay and/or set display=False

    results = sim.run(n_trials)  # run for a specified number of trials
    # NOTE: To quit midway, press Esc or close pygame window, or hit Ctrl+C on the command-line

    print "Succesful Trials = {}".format(results[1])

    return results

def execute(times, n_trials, agents):
    for agent in agents:
        results = []
        for i in range(times):
            results.append(run(n_trials, agent))
        df_results = pd.DataFrame(results)
        df_results.columns = ['reward_sum', 'n_dest_reached', 'last_dest_fail', 'last_penalty']
        print df_results.describe()

if __name__ == '__main__':
    execute(10, 100, [RandomAgent])
