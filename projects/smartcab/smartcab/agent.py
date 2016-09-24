import random
from environment import Agent, Environment
from planner import RoutePlanner
from simulator import Simulator
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math
import random

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

    def get_q_length(self):
        return 0

class BaseLearningAgent(Agent):
    """A basic agent that learns to drive in the smartcab world."""

    def __init__(self, env):
        super(BaseLearningAgent, self).__init__(env)  # sets self.env = env, state = None, next_waypoint = None, and a default color
        self.color = 'red'  # override color
        self.planner = RoutePlanner(self.env, self)  # simple route planner to get next_waypoint

        # Initialize any additional variables here
        self.total_reward = 0
        self.was_penalized = False

        self.possible_actions = (None, 'forward', 'left', 'right')
        self.q_table = {}
        self.alpha = 0.3
        self.gamma = 0.2
        self.epsilon = 0.0
        self.trial = 0.0

    def reset(self, destination=None):
        """Reset variables used to record information about each trial.
    	
    	No parameters.
    	
    	No return value."""
        self.planner.route_to(destination)

        # Prepare for a new trip; reset any variables here, if required
        self.next_waypoint = None
        self.total_reward = 0
        self.was_penalized = False
        self.trial = self.trial + 1.0

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

        return tuple(inputs.values()), deadline

    def _select_action(self, state) :
        # get all possible q-values for the state
        all_q_vals = { action: self._get_q_value(state, action)
                        for action in self.possible_actions }

        best_q_value = max(all_q_vals.values())

        # pick the actions that yield the largest q-value for the state
        best_actions = self.possible_actions if random.random() > 1 - self.get_epsilon() else [action for action in self.possible_actions if all_q_vals[action] == best_q_value]

        # return one of the best actions at random
        return random.choice(best_actions)

    def get_alpha(self):
        return self.alpha

    def get_gamma(self):
        return self.gamma

    def get_epsilon(self):
        return self.epsilon

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
        alpha = self.get_alpha()
        gamma = self.get_gamma()

        self.q_table[(state, action)] = ((1 - alpha) * self._get_q_value(state, action)) + alpha * (reward + gamma * max_q_value)

    def get_total_reward(self):
        return self.total_reward

    def _get_q_value(self, state, action):
        return self.q_table.get((state, action), 0)

    def get_q_length(self):
        return len(self.q_table)

class OnlyInputWithoutWaypointStateAgent(BaseLearningAgent):
    
    def _get_state(self) :
        # Gather inputs
        self.next_waypoint = self.planner.next_waypoint()  # from route planner, also displayed by simulator
        inputs = self.env.sense(self)
        deadline = self.env.get_deadline(self)

        return tuple(inputs.values()), deadline
class InputWithWaypointStateAgent(BaseLearningAgent):
    def _get_state(self) :
        # Gather inputs
        self.next_waypoint = self.planner.next_waypoint()  # from route planner, also displayed by simulator
        inputs = self.env.sense(self)
        deadline = self.env.get_deadline(self)

        # include the next_waypoint into the state
        inputs['next_waypoint'] = self.next_waypoint

        return tuple(inputs.values()), deadline

class InputWithWaypointAndDeadlineStateAgent(BaseLearningAgent):
    def _get_state(self) :
        # Gather inputs
        self.next_waypoint = self.planner.next_waypoint()  # from route planner, also displayed by simulator
        inputs = self.env.sense(self)
        deadline = self.env.get_deadline(self)

        # include the next_waypoint into the state
        inputs['next_waypoint'] = self.next_waypoint
        inputs['deadline'] = deadline

        return tuple(inputs.values()), deadline

class WithoutRightStateAgent(BaseLearningAgent):
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

class LearningAgent(BaseLearningAgent):
    """An agent that learns to drive in the smartcab world."""

    def _get_state(self) :
        # Gather inputs
        self.next_waypoint = self.planner.next_waypoint()  # from route planner, also displayed by simulator
        inputs = self.env.sense(self)
        deadline = self.env.get_deadline(self)

        # include the next_waypoint into the state
        inputs['next_waypoint'] = self.next_waypoint

        # calculate if left_incomming
        inputs['left'] = 'forward' if inputs['left'] == 'forward' else None 
        inputs['oncoming'] = inputs['oncoming'] if inputs['oncoming'] != 'right' else None

        # remove the right value as it is not needed.
        del inputs['right']

        return tuple(inputs.values()), deadline
        
def run(n_trials = 100, learning_agent = LearningAgent, update_delay=0.1, display=True):
    """Run the agent for a finite number of trials."""

    # Set up environment and agent
    e = Environment()  # create environment (also adds some dummy traffic)
    a = e.create_agent(learning_agent)  # create agent
    e.set_primary_agent(a, enforce_deadline=True)  # specify agent to track
    # NOTE: You can set enforce_deadline=False while debugging to allow longer trials

    # Now simulate it
    sim = Simulator(e, update_delay=update_delay, display=display)  # create simulator (uses pygame when display=True, if available)
    # NOTE: To speed up simulation, reduce update_delay and/or set display=False

    results = sim.run(n_trials)  # run for a specified number of trials
    # NOTE: To quit midway, press Esc or close pygame window, or hit Ctrl+C on the command-line

    return results

def execute(times, n_trials, agents):
    for agent in agents:
        print "Runs for Agent: [{}]".format(agent.__name__)
        print ""
        print "-----------"
        results = []
        for i in range(times):
            run_results = run(n_trials=n_trials, learning_agent=agent, display=False, update_delay=0.0)
            print "Run {}. Succesful Trials = {}".format(i + 1, run_results[1])
            results.append(run_results)

        df_results = pd.DataFrame(results)
        df_results.columns = ['reward_sum', 'n_dest_reached', 'last_dest_fail', 'last_penalty', 'len_qvals']

        print "-----------"        
        print ""
        print df_results.describe()
        print "==================================================================================="
        print ""

        df_results.to_csv('{}_results.csv'.format(agent.__name__))

def build_parametrized_agent(alpha, gamma, epsilon, agent):
    def constructor(env):
        new_agent = agent(env)
        new_agent.alpha = alpha
        new_agent.gamma = gamma
        new_agent.epsilon = epsilon
        return new_agent

    return constructor

def run_parametrized(n_trials, times, agent, n_steps=11): 
    total_results = pd.DataFrame([])
    for alpha in np.linspace(0.0, 1.0, num=n_steps):
        last_penalties = []
        last_dest_fails = []
        len_qvals = []
        for gamma in np.linspace(0.0, 1.0, num=n_steps):
            for epsilon in np.linspace(0.0, 0.2, num=n_steps):
                results = []
                for i in range(times):
                    run_results = run(n_trials=n_trials, learning_agent=build_parametrized_agent(alpha, gamma, epsilon, agent), display=False, update_delay=0.0)
                    run_results.append(alpha)
                    run_results.append(gamma)
                    run_results.append(epsilon)
                    results.append(run_results)
                df_results = pd.DataFrame(results)
                df_results.columns = ['reward_sum', 'n_dest_reached', 'last_dest_fail', 'last_penalty', 'len_qvals', 'alpha', 'gamma', 'epsilon']
                print(results)
                total_results = pd.concat([total_results, df_results])

    total_results.to_csv('{}_parametrized_total_results.csv'.format(agent.__name__))

def get_decaying_alpha_based_on_trial(self):
    return 1.0 / self.trial

def get_slow_decaying_alpha_based_on_trial(self):
    return 1.0 / math.log(self.trial + 2.0)

def get_decaying_epsilon_based_on_trial(self):
    return 0.2 / math.log(self.trial + 2.0)

def run_decaying_learning_parametrized(n_trials, times, agent, n_steps=11): 
    total_results = pd.DataFrame([])
    last_penalties = []
    last_dest_fails = []
    len_qvals = []
    alpha = 0.0

    for gamma in np.linspace(0.0, 1.0, num=n_steps):
        results = []
        for i in range(times):
            run_results = run(n_trials=n_trials, learning_agent=build_parametrized_agent(alpha, gamma, 0.0, agent), display=False, update_delay=0.0)
            run_results.append(alpha)
            run_results.append(gamma)
            results.append(run_results)

        df_results = pd.DataFrame(results)
        df_results.columns = ['reward_sum', 'n_dest_reached', 'last_dest_fail', 'last_penalty', 'len_qvals', 'alpha', 'gamma']
        print(results)
        total_results = pd.concat([total_results, df_results])

        last_penalties.append(df_results["last_penalty"].mean())
        last_dest_fails.append(df_results["last_dest_fail"].mean())
        len_qvals.append(df_results["len_qvals"].mean())

    plt.figure(1)
    plt.plot(np.linspace(0.0, 1.0, num=n_steps), last_penalties)

    plt.figure(2)
    plt.plot(np.linspace(0.0, 1.0, num=n_steps), last_dest_fails)

    plt.figure(3)
    plt.plot(np.linspace(0.0, 1.0, num=n_steps), len_qvals)
            
    total_results.to_csv('{}_decaying_learning_parametrized_total_results.csv'.format(agent.__name__))

    plt.show()

if __name__ == '__main__':
    #run(display=True, update_delay=0.3)
    #execute(10, 100, [RandomAgent, OnlyInputWithoutWaypointStateAgent, InputWithWaypointStateAgent, WithoutRightStateAgent, LearningAgent])
    #execute(10, 100, [build_parametrized_agent(0.1, 0.2, 0.1, LearningAgent)])
    #run_parametrized(100, 100, InputWithWaypointAndDeadlineStateAgent, 11)

    InputWithWaypointAndDeadlineStateAgent.get_alpha = get_decaying_alpha_based_on_trial
    InputWithWaypointAndDeadlineStateAgent.get_epsilon = get_decaying_epsilon_based_on_trial

    run_decaying_learning_parametrized(100, 100, InputWithWaypointAndDeadlineStateAgent, 11)
    