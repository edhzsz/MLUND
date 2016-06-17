# Project Report 4: Reinforcement Learning
## Train a Smartcab How to Drive

### Implement a basic driving agent

_In your report, mention what you see in the agent’s behavior. Does it eventually make it to the target location?_

To implement the basic driving agent a random action from (None, 'forward', 'left', 'right') was chosen on each call to the update method. 
This causes the agent to wander (randomly) around the grid until eventually the hard limit (deadline of -100) is reached or the agent arrives,
by chance, to the target.

The simulator code was modified to report the amount of trials in which the agent arrived to the target and multiple runs of 100 trials were executed.
The basic (random) driving agent arrives to the target before the hard limit, on average, 67.4% of the time and 20.7% of the time when the deadline is enforced.

### Identify and update state

_Justify why you picked these set of states, and how they model the agent and its environment._

### Implement Q-Learning

_What changes do you notice in the agent’s behavior?_

### Enhance the driving agent

_Report what changes you made to your basic implementation of Q-Learning to achieve the final version of the agent. How well does it perform?_

_Does your agent get close to finding an optimal policy, i.e. reach the destination in the minimum possible time, and not incur any penalties?_