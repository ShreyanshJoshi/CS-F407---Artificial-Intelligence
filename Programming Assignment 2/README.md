## Simplified-implementation-of-Wumpus-World
This folder contains my code in Python for a project that was done in partial fulfillment of the course **CS F407 - Artificial Intelligence (AI)** at BITS Pilani for the year 2020-21. 

The task was to simulate a simplified version of a Wumpus World in Python using concepts of **Propositional Logic**. The wumpus world is simplified in the sense that instead of the traditionally present elements in a grid such as pit, stench, breeze and wumpus, in this project, we would just have pits (actually referred to as land mines in the project). There can be multiple pits in a 4x4 grid, and our agent has to safely negotiate his way from (1,1) to (4,4) in the grid (minefield) without taking any risks and without dying. Additional details can be found in the *Question.pdf* file uploaded.

### Additional Improvements - 
The code I have uploaded is tweaked and enhanced version of the code we had to submit in our assignment. I have made the following enhancements -
1. I have used a **modular paradigm** while coding and hence there would be multiple files in which the entire logic of the code would be distributed. This allows for easier debugging, readability and reusability of code (especially when code is very long, as in this project). 

2. I have also added logic in the program by which the agent will be able to figure out if it is not possible to safely negotiate a way to 4,4 without taking a risk or without dying. It prints the following message on the console in such a scenario - `Agent cannot exit the minefield safely. Hence terminating the run !`

In the project that we had to submit, it was guaranteed that the test cases would check only for those minefields where there is a safe way till 4,4. However, I added this additional feature to make the game better and much more realistic.


### Files uploaded in the 'Source Code' folder - 
* *Agent.py* - This file was provided to us, and we could call some (not all) functions in it in our code. It contains the minefields and several other fundamental functions. Rest all files have been implemented by me.
* *driver.py* - This contains the main function, and is the driver for the program - calls all other functions present in different files.
* *basic_func.py* - Contains some basic functions such as mapping grid positions to a number and vice-versa, getting neighbors for a position and checking if agent is dead or not.
* *perception_func.py* - Contains my implementation for perception. Agent has the ability to perceive in each cell of the grid that tells it information about it's neighboring cells.
* *infer_func.py* - Contains my implementation for inferencing using Propositional Logic using Knowledge Base (KB). Once inferred, agent learns some more things about the grid (minefield) which it can use in it's subsequent motions to reach 4,4.
* *clear_doubt.py* - I maintain a 'doubt' list in my code that tells the agent that states in that list cannot be inferred with the current knowledge base, and hence agent might need to come back later to those states, with some more information in it's KB to make an inference.
* *move_func.py* - Contains my implementation for movement of the agent (which direction should it move in). Performs backtracking in case there is a dead-end ahead.

### How to run code on your machine - 
To run the game locally, clone the repository and download the source files present in this folder. Store them in a designated directory (folder) on your local machine. Then simply run the *driver.py* file from terminal (from same directory) by one of the following commands - `python driver.py` or `python3 driver.py`
