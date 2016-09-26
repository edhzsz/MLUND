# Project Report 4: Reinforcement Learning
## Train a Smartcab How to Drive

### Implement a basic driving agent

_In your report, mention what you see in the agent’s behavior. Does it eventually make it to the target location?_

To implement a basic driving agent a random action from (None, 'forward', 'left',
 'right') was chosen on each call to the update method. 
This causes the agent to wander (randomly) around the grid until eventually the
 deadline is reached or the agent arrives,
by chance, to the target.

The simulator code was modified to report the following metrics for each execution
 of each Agent that was analyzed:
* reward_sum - Total sum of the rewards obtained by the agent.
* n_dest_reached - Total number of trials in which the agent arrived to the destination
* last_dest_fail - Last trial in which the agent failed to arrive at the destination
* last_pealty - Last trial in which the agent was penalized
* len_q_vals - Size of the Q table (for agents that use Q-learning)

100 runs of 100 trials were executed for these agent with the following results:

|      | reward_sum  | n_dest_reached | last_dest_fail | last_penalty | len_qvals|
| ---- |:-----------:| --------------:|---------------:|-------------:|---------:|
|count |   100.000000 |  100.000000   |   100.000000   |      100.0   |   100.0  |
|mean  |  1676.385000 |   20.090000   |    99.840000   |      100.0   |     0.0  |
|std   |  4059.377319 |    3.348737   |     0.465366   |        0.0   |     0.0  |
|min   | -8400.000000 |   13.000000   |    97.000000   |      100.0   |     0.0  |
|25%   |  -942.375000 |   18.000000   |   100.000000   |      100.0   |     0.0  |
|50%   |  1334.500000 |   20.000000   |   100.000000   |      100.0   |     0.0  |
|75%   |  4644.875000 |   22.000000   |   100.000000   |      100.0   |     0.0  |
|max   | 10762.000000 |   30.000000   |   100.000000   |      100.0   |     0.0  |

Another 100 runs where executed without enforcing the deadline to see if a random 
agent can reach the destination before the hard limit or the hard limit (deadline
of -100).
The results are the following:

|      |   reward_sum  | n_dest_reached | last_dest_fail | last_penalty | len_qvals|
| ---- |:-------------:| --------------:|---------------:|-------------:|---------:|
|count |    100.000000 |  100.000000   |   100.000000   |      100.0   |   100.0  |
|mean  | -14220.965000 |   67.220000   |    97.640000   |      100.0   |     0.0  |
|std   |   7046.315597 |    4.757939   |     2.649643   |        0.0   |     0.0  |
|min   | -31506.500000 |   57.000000   |    87.000000   |      100.0   |     0.0  |
|25%   | -18300.000000 |   64.000000   |    96.000000   |      100.0   |     0.0  |
|50%   | -13891.000000 |   67.000000   |    99.000000   |      100.0   |     0.0  |
|75%   |  -8610.625000 |   70.000000   |   100.000000   |      100.0   |     0.0  |
|max   |   -658.000000 |   81.000000   |   100.000000   |      100.0   |     0.0  |

The basic (random) driving agent arrives to the target before the hard limit, on average,
67.2% of the time and 20.1% of the time when the deadline is enforced while being penalized
all the time.

### Identify and update state

_Justify why you picked these set of states, and how they model the agent and its environment._

From the project description we know that: 
* The smartcab gets a reward for each successfully completed trip (gets to the
 target within a pre-specified time bound).
* It also gets a smaller reward for each correct move executed at an intersection.
* It gets a small penalty for an incorrect move.
* It gets a larger penalty for violating traffic rules and/or causing an accident.

The correct moves at each intersection are calculated using the US right-of-way rules:
* On a green light, you can turn left only if there is no oncoming traffic at the
 intersection coming straight.
* On a red light, you can turn right if there is no oncoming traffic turning left
 or traffic from the left going straight.

The following information is available for the agent at each update:

* __Light__: whether the light is red or green (2 states). Going through an intersection with a red light is a traffic rule violation, so I consider this
information important and it needs to be part of the state.
* __Oncoming__: whether there is oncoming traffic, and which direction it is going (4 states). Oncoming traffic may mean the agent cannot turn left or
right, so this information needs to be in the state as well.
* __Right__: whether there is traffic from the right of the agent, and which direction it is going (4 states).
Traffic coming from the right is not mentioned in any of the traffic rules defined in the description of the project so it may not be important
for the agent to figure out if it can turn left or right, although it may be important to avoid accidents with other agents if they are not
following correctly traffic rules or if different rules for right-of-way are applied.
* __Left__: whether there is traffic from the left of the agent, and which direction it is going (4 states).
Traffic from the left going straight means the agent cannot turn right on a red light, so this needs to be in the state. It may, however, be reduced to the single
case of left going straight (2 states).
* __Next waypoint__: the direction the agent should go to reach the destination (3 states).
Without this information, the agent does not have a way to know where the target is and what is the next step in the computed route plan so
it will have to wander randomnly, For this reason I consider this information important and it needs to be in the state.
* __Deadline__: how much time the agent has left to reach its destination (50 states for the current simulation).
This value depends on the distance to the target. As the agent only knows what is the next step in the planned route and does not know the 
position of the final destination, it does not know how far it is or how to get faster. So knowing how much time is left is basically useless.

I decided to test different agents using different combinations of the inputs as part of the
state.

### Only input without waypoint or deadline
The following states are considered in this model:
- Light (2 states)
- Oncoming (4 states)
- Right (4 states)
- Left (4 states)

This produces a space of possible states of size 128 (2 x 4 x 4 x 4).

### Input and waypoint without deadline
The following states are considered in this model:
- Light (2 states)
- Oncoming (4 states)
- Right (4 states)
- Left (4 states)
- Next Waypoint (3 states)

This produces a space of possible states of size 384 (2 x 4 x 4 x 4 x 3).

### Input with waypoint and deadline
The following states are considered in this model:
- Light (2 states)
- Oncoming (4 states)
- Right (4 states)
- Left (4 states)
- Next Waypoint (3 states)
- Deadline (50 states)

This produces a space of possible states of size 19,200 (2 x 4 x 4 x 4 x 3 x 50).

### Input and waypoint without deadline nor right state
The following states are considered in this model:
- Light (2 states)
- Oncoming (4 states)
- Left (4 states)
- Next Waypoint (3 states)

This produces a space of possible states of size 96 (2 x 4 x 4 x 3).

### Input and waypoint without deadline nor right state and reduced left state
The following states are considered in this model:
- Light (2 states)
- Oncoming (4 states)
- Incomming_Left (2 states)
- Next Waypoint (3 states)

This produces a space of possible states of size 48 (2 x 4 x 2 x 3).

### Implement Q-Learning

_What changes do you notice in the agent’s behavior?_

![Rewards for the simple q-learning agent](charts/simple_q_learning_penalties_ratio.png)

### Enhance the driving agent

_Report what changes you made to your basic implementation of Q-Learning to achieve the final version of the agent. How well does it perform?_

_Does your agent get close to finding an optimal policy, i.e. reach the destination in the minimum possible time, and not incur any penalties?_