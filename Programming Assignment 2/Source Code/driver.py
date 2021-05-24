from Agent import *                                 # See the Agent.py file
import basic_func
import perception_func
import infer_func
import clear_doubt_func
import move_func
from pysat.solvers import Glucose3

ag = Agent()
safe = [[1,1], [4,4]]                           # Stores all states agent knows are safe for sure
unsafe = []                                     # Stores all states agent knows are unsafe for sure
vis  = []                                       # Stores all states already visited by agent
store = []                                      # Stores exact path taken by the agent
dead_end = []                                   # Indicates locations from where there is only 1 option - to backtrack
mapping = basic_func.get_mapping()              # Maps each state ((i,j); 1<=i,j<=4) to an integer between 1 and 16 (for putting in KB) 
rv_mapping = basic_func.get_reverse_mapping()   # Maps the integer back to its corresponding state
doubt_states = []                               # Agent is not sure where to proceed from these states b'se it all it's neighbors aren't in safe/unsafe lists
pending_inferences = []                         # Stores all facts that couldn't be inferred now due to lack of information; but would req to be inferred later
perception_list = []                            # Stores the value the agent had perceived when it was at a particular position. Stored as a 3-tuple.
last_move = ""                                  # Useful for backtracking in some scenarios. Initial value doesn't matter cause we aren't gonna backtrack in 1st move
quit = False                                    # When true, program terminates as agent cannot safely reach [4,4] (needs to take a risk or will be dead surely)

print("Current Location ", [1,1])

for iter in range(25):                          # Just running for 25 iterations; ideally the program should terminate well before that.

    inf = False                                 # make 'inference' false at the start of each iteration. Used to make choice in move function.
    kb = Glucose3()

    x = ag.FindCurrentLocation()                # Agent moves to a location after guaranteeing it is safe, so x for sure is safe already
    if x not in vis:
        vis.append(x)

    store.append(x)

    if x==[4,4]:
        print("Exiting the maze :)")
        break
    
    neighbor = []
    basic_func.get_neighbors(neighbor, x)


    # PERCEIVING  THE  SURROUNDINGS  (NEIGHBORS)
    perception = ag.PerceiveCurrentLocation()

    if [x[0], x[1], perception] not in perception_list:
        perception_list.append([x[0], x[1], perception])

    if perception=="=0":
        perception_func.perceive_0(safe, neighbor)
    
    elif perception=="=1":
        perception_func.perceive_1(x, safe, unsafe, neighbor, pending_inferences, doubt_states, mapping)
    
    else:
        perception_func.perceive_2(x, safe, unsafe, neighbor, pending_inferences, doubt_states, mapping)

    
    # ADDING WHAT WE KNOW INTO KB, FOR MAKING INFERENCES
    for i in safe:
        kb.add_clause([-1*mapping[str(i)]])
    
    for i in unsafe:
        kb.add_clause([mapping[str(i)]])
    
    for i in range(len(pending_inferences)):
        if pending_inferences[i]!=[1000] and pending_inferences[i]!=[-1000]:            
            kb.add_clause(pending_inferences[i])
    
    ''' NOTE: Important that we don't add 1000 and -1000 both into the KB as if both are present in KB at some time, KB won't get resolved, as a literal
    cannot be both true and false at the same time '''


    # INFERRING - USING SAT SOLVER ON PROPOSITIONAL LOGIC SENTENCES
    if x not in doubt_states:
        inf = infer_func.infer(kb, safe, unsafe, pending_inferences, rv_mapping)            # If actually we inferred something, inf is returned as true


    # REMOVING  DOUBTS (CLEARING THEM FROM THE LIST)
    if len(doubt_states)!=0:
        clear_doubt_func.clear_doubt(safe, unsafe, doubt_states, perception_list)
    
    # print('')
    # print("Safe: ", safe)
    # print("Unsafe: ", unsafe)
    # print("Doubt: ", doubt_states)
    # print("Pending inf: ", pending_inferences)
    # print("Dead end: ", dead_end)

    for i in doubt_states:
        if doubt_states.count(i) > 2:
            print("Agent cannot exit the minefield safely. Hence terminating the run !")
            quit = True
            break
    
    for i in dead_end:
        if x==i:
            print("Agent cannot exit the minefield safely. Hence terminating the run !")
            quit = True
            break
    
    val = 0
    for i in neighbor:
        if i in unsafe or i in dead_end:
            val += 1

    if val == len(neighbor):                                                            # All neighbors are either dead-ends or unsafe states
        print("Agent cannot exit the minefield safely. Hence terminating the run !")
        quit = True

    if basic_func.check_dead(unsafe)==True:                                            # Checks some additional conditions so that program terminates quickly
        print("Agent cannot exit the minefield safely. Hence terminating the run !")
        quit = True

    if quit==True:
        break


    # MOVEMENT  ACROSS  THE  GRID
    last_move = move_func.move(x, inf, last_move, safe, unsafe, neighbor, vis, doubt_states, dead_end, ag, store)  


if quit==False:
    print("States visited (in order) :", end=" ")               # Printed only when agent successfully leaves the minefield at 4,4  
    for i in store:
        if i!=[4,4]:
            print(i, "-->", end=" ") 
        
        else:
            print(i)