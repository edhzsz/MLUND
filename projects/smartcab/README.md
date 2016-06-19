# Project 4: Reinforcement Learning
## Train a Smartcab How to Drive

### Install

This project requires **Python 2.7** with the [pygame](https://www.pygame.org/wiki/GettingStarted
) library installed

### Code

Template code is provided in the `smartcab/agent.py` python file. Additional supporting python code can be found in `smartcab/enviroment.py`, `smartcab/planner.py`, and `smartcab/simulator.py`. Supporting images for the graphical user interface can be found in the `images` folder. While some code has already been implemented to get you started, you will need to implement additional functionality for the `LearningAgent` class in `agent.py` when requested to successfully complete the project. 

### Run

In a terminal or command window, navigate to the top-level project directory `smartcab/` (that contains this README) and run one of the following commands:

```python smartcab/agent.py```  
```python -m smartcab.agent```

This will run the `agent.py` file and execute your agent code.

## Project Description

### Environment
Your smartcab operates in an idealized grid-like city, with roads going North-South and East-West.
Other vehicles may be present on the roads, but no pedestrians.
There is a traffic light at each intersection that can be in one of two states: North-South open or East-West open.

US right-of-way rules apply:
On a green light, you can turn left only if there is no oncoming traffic at the intersection coming straight.
On a red light, you can turn right if there is no oncoming traffic turning left or traffic from the left going straight.

### Inputs
Assume that a higher-level planner assigns a route to the smartcab, splitting it into waypoints at each intersection.
And time in this world is quantized. At any instant, the smartcab is at some intersection.
Therefore, the next waypoint is always either one block straight ahead, one block left, one block right, one block back or exactly there (reached the destination).

The smartcab only has an egocentric view of the intersection it is currently at (sorry, no accurate GPS, no global location).
It is able to sense whether the traffic light is green for its direction of movement (heading), and whether there is a car at
the intersection on each of the incoming roadways (and which direction they are trying to go).

In addition to this, each trip has an associated timer that counts down every time step.
If the timer is at 0 and the destination has not been reached, the trip is over, and a new one may start.

### Outputs
At any instant, the smartcab can either stay put at the current intersection, move one block forward, one block left, or one block right (no backward movement).

### Rewards
The smartcab gets a reward for each successfully completed trip.
A trip is considered “successfully completed” if the passenger is dropped off at the desired destination (some intersection)
within a pre-specified time bound (computed with a route plan).

It also gets a smaller reward for each correct move executed at an intersection.
It gets a small penalty for an incorrect move, and a larger penalty for violating traffic rules and/or causing an accident.

### Goal
Design the AI driving agent for the smartcab. It should receive the above-mentioned inputs at each time step t, and generate an output move.
Based on the rewards and penalties it gets, the agent should learn an optimal policy for driving on city roads, obeying traffic rules correctly, and trying to reach the destination within a goal time.

## Tasks

### Implement a basic driving agent
Implement the basic driving agent, which processes the following inputs at each time step:

* Next waypoint location, relative to its current location and heading,
* Intersection state (traffic light and presence of cars), and,
* Current deadline value (time steps remaining),
* And produces some random move/action (None, 'forward', 'left', 'right'). Don’t try to implement the correct strategy! That’s exactly what your agent is supposed to learn.

Run this agent within the simulation environment with enforce_deadline set to False (see run function in agent.py), and observe how it performs.
In this mode, the agent is given unlimited time to reach the destination. The current state, action taken by your agent and reward/penalty earned are shown in the simulator.

_In your report, mention what you see in the agent’s behavior. Does it eventually make it to the target location?_

### Identify and update state
Identify a set of states that you think are appropriate for modeling the driving agent.
The main source of state variables are current inputs, but not all of them may be worth representing.
Also, you can choose to explicitly define states, or use some combination (vector) of inputs as an implicit state.

At each time step, process the inputs and update the current state.
Run it again (and as often as you need) to observe how the reported state changes through the run.

_Justify why you picked these set of states, and how they model the agent and its environment._

### Implement Q-Learning
Implement the Q-Learning algorithm by initializing and updating a table/mapping of Q-values at each time step.
Now, instead of randomly selecting an action, pick the best action available from the current state based on Q-values, and return that.

Each action generates a corresponding numeric reward or penalty (which may be zero).
Your agent should take this into account when updating Q-values. Run it again, and observe the behavior.

_What changes do you notice in the agent’s behavior?_

### Enhance the driving agent
Apply the reinforcement learning techniques you have learnt, and tweak the parameters (e.g. learning rate, discount factor, action selection method, etc.),
to improve the performance of your agent.
Your goal is to get it to a point so that within 100 trials, the agent is able to learn a feasible policy - i.e. reach the destination within the allotted time,
with net reward remaining positive.

_Report what changes you made to your basic implementation of Q-Learning to achieve the final version of the agent. How well does it perform?_

_Does your agent get close to finding an optimal policy, i.e. reach the destination in the minimum possible time, and not incur any penalties?_

The formulas for updating Q-values can be found in [this](https://www.udacity.com/course/viewer?&_ga=1.195155432.55316324.1459427136#!/c-ud728-nd/l-5446820041/m-634899057) video.