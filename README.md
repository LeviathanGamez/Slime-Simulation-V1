# Slime-Simulation-V1
Simulates evolutionary dynamics through mutation, natural selection, and environmental pressure using slime-based agents. Built with object-oriented design in Pygame to model emergent behavior and adaptive systems.

# Slime Evolution Simulator

![Simulation Demo](Slime.gif)

All slimes have traits such as speed, vision range, food capacity, and water capacity. When two slimes reproduce, their offspring inherits the average of both parents’ traits with a small chance of mutation. These mutations introduce variation, allowing some slimes to become more “fit” for survival than others.

The environment generates limited food (potatoes) roughly every 8 seconds, which is not enough to sustain the rapidly growing population. This scarcity creates competition, where only the most well-adapted slimes survive. Over time, this leads to the dominance of slimes with higher speed, better vision, and greater resource capacity.

Each slime functions as an independent agent within the simulation, making decisions based on its internal state and environment. Their behavior is controlled through a state machine, allowing them to switch between actions such as searching for food, moving, and reproducing. Reproduction is constrained by energy availability, meaning a slime must accumulate enough food before it can reproduce. This ensures that only agents that efficiently gather and manage resources are able to pass on their traits.

Features:

-Mutation system
-Natural selection mechanics
-Environmental constraints
-Object-oriented design using Pygame

Controls:

- Space -> Pause
- O -> Speed up
- P -> Slow Down


