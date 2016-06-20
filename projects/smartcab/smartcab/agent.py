import random
from environment import Agent, Environment
from planner import RoutePlanner
from simulator import Simulator
import matplotlib.pyplot as plt

class LearningAgent(Agent):
    """An agent that learns to drive in the smartcab world."""

    def __init__(self, env):
        super(LearningAgent, self).__init__(env)  # sets self.env = env, state = None, next_waypoint = None, and a default color
        self.color = 'red'  # override color
        self.planner = RoutePlanner(self.env, self)  # simple route planner to get next_waypoint

        # Initialize any additional variables here
        self.total_reward = 0
        self.actions_count = 0
        self.penalties = 0

        self.possible_actions = (None, 'forward', 'left', 'right')
        self.q_table = {}
        self.learn_rate = 0.5

        self.all_penalties = []
        self.all_actions = []
        self.penalties_ratio = []

    def reset(self, destination=None):
        """Reset variables used to record information about each trial.
    	
    	No parameters.
    	
    	No return value."""
        self.planner.route_to(destination)

        self.all_penalties.append(self.penalties)
        self.all_actions.append(self.actions_count)
        ratio = 1 if self.actions_count == 0 else (self.penalties / float(self.actions_count))
        self.penalties_ratio.append(ratio)

        # Prepare for a new trip; reset any variables here, if required
        self.next_waypoint = None
        self.total_reward = 0
        self.actions_count = 0
        self.penalties = 0
        self.q_table = {}

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
            self.penalties += 1

        self.actions_count += 1

        self.total_reward += reward

        # Learn policy based on state, action, reward
        self._learn(state, action, reward)

        print "LearningAgent.update(): state = {}, action = {}, reward = {}, deadline = {}".format(state, action, reward, deadline)  # [debug]

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

        # Q(s,a) = r + learn_rate * argmax_a'(s',a')
        self.q_table[(state, action)] = reward + self.learn_rate * max_q_value

    def get_total_reward(self):
        return self.total_reward

    def _get_q_value(self, state, action):
        return self.q_table.get((state, action), 100)

def run():
    """Run the agent for a finite number of trials."""

    # Set up environment and agent
    e = Environment()  # create environment (also adds some dummy traffic)
    a = e.create_agent(LearningAgent)  # create agent
    e.set_primary_agent(a, enforce_deadline=True)  # specify agent to track
    # NOTE: You can set enforce_deadline=False while debugging to allow longer trials

    # Now simulate it
    sim = Simulator(e, update_delay=0.001, display=True)  # create simulator (uses pygame when display=True, if available)
    # NOTE: To speed up simulation, reduce update_delay and/or set display=False

    sim.run(n_trials=100)  # run for a specified number of trials
    # NOTE: To quit midway, press Esc or close pygame window, or hit Ctrl+C on the command-line

    print "Succesful Trials = {}".format(sim.succesful_trials)
    plt.plot(sim.trials_rewards)
    plt.ylabel('Total Reward')
    plt.savefig('total_reward.png')
    plt.close()

    plt.plot(a.all_penalties)
    plt.plot(a.all_actions)
    plt.ylabel('Penalties')
    plt.savefig('penalties_per_trial.png')
    plt.close()

    plt.plot(a.penalties_ratio)
    plt.ylabel('Penalties ratio')
    plt.savefig('penalties_ratio_per_trial.png')
    plt.close()

if __name__ == '__main__':
    run()
