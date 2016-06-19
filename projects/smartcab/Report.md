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

From the project description we know that: 
* The smartcab gets a reward for each successfully completed trip (gets to the target within a pre-specified time bound).
* It also gets a smaller reward for each correct move executed at an intersection.
* It gets a small penalty for an incorrect move.
* It gets a larger penalty for violating traffic rules and/or causing an accident.

The following information is available for the agent at each update:

* Light: whether the light is red or green (2 states). Going through an intersection with a red light is a traffic rule violation, so I consider this
information important and it needs to be part of the state.
* Oncoming: whether there is oncoming traffic, and which direction it is going (4 states). Oncoming traffic may mean the agent cannot turn left or
right, so this information needs to be in the state as well.
* Right: whether there is traffic from the right of the agent, and which direction it is going (4 states).
Traffic coming from the right is not mentioned in any of the traffic rules defined in the description of the project so it is not important
for the agent to figure out if it can turn left or right, although it may be important to avoid accidents with other agents if they are not
following correctly traffic rules.
* Left: whether there is traffic from the left of the agent, and which direction it is going (4 states).
Traffic from the left going straight means the agent cannot turn right on a red light, so this needs to be in the state.
* Next waypoint: the direction the agent should go to reach the destination (3 states).
Without this information, the agent does not have a way to know where the target is and what is the next step in the computed route plan so
it will have to wander randomnly, For this reason I consider this information important and it needs to be in the state.
* Deadline: how much time the agent has left to reach its destination (50 states for the current simulation).
This value depends on the distance to the target. As the agent only knows what is the next step in the planned route and does not know the 
position of the final destination, it does not know how far it is or how to get faster. So knowing how much time is left is basically useless.

To model the agent and its enviroment I have chosen the following states:

- Light
- Oncoming
- Left
- Next Waypoint

This produces a space of possible states of size 96 (2 x 4 x 4 x 3).

The Right state could be included in the future if it is found that there are other agents not following traffic rules. Including this state
would increase the space size by 4 times.

### Implement Q-Learning

_What changes do you notice in the agent’s behavior?_

### Enhance the driving agent

_Report what changes you made to your basic implementation of Q-Learning to achieve the final version of the agent. How well does it perform?_

_Does your agent get close to finding an optimal policy, i.e. reach the destination in the minimum possible time, and not incur any penalties?_