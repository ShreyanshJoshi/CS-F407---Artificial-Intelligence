def get_neighbors (a, x):                           # Returns the neighbors of state x
    
    if x==[1,1]: a.extend([[1,2],[2,1]])
    if x==[2,1]: a.extend([[1,1],[2,2],[3,1]])
    if x==[3,1]: a.extend([[2,1],[3,2],[4,1]])
    if x==[4,1]: a.extend([[3,1],[4,2]])

    if x==[1,2]: a.extend([[1,1],[2,2],[1,3]])
    if x==[2,2]: a.extend([[1,2],[2,1],[2,3],[3,2]])
    if x==[3,2]: a.extend([[2,2],[3,1],[3,3],[4,2]])
    if x==[4,2]: a.extend([[3,2],[4,1],[4,3]])

    if x==[1,3]: a.extend([[1,2],[2,3],[1,4]])
    if x==[2,3]: a.extend([[1,3],[2,2],[3,3],[2,4]])
    if x==[3,3]: a.extend([[2,3],[3,2],[4,3],[3,4]])
    if x==[4,3]: a.extend([[3,3],[4,2],[4,4]])

    if x==[1,4]: a.extend([[1,3],[2,4]])
    if x==[2,4]: a.extend([[1,4],[2,3],[3,4]])
    if x==[3,4]: a.extend([[2,4],[3,3],[4,4]])
    if x==[4,4]: a.extend([[3,4],[4,3]])

def get_mapping ():                                 # Maps a state to an integer between 1 and 16

    a = {"[1, 1]":1, "[2, 1]":2, "[3, 1]":3, "[4, 1]":4, "[1, 2]":5, "[2, 2]":6, "[3, 2]":7, "[4, 2]":8, "[1, 3]":9, "[2, 3]":10, "[3, 3]":11, "[4, 3]":12,
         "[1, 4]":13, "[2, 4]":14, "[3, 4]":15, "[4, 4]":16}

    return a

def get_reverse_mapping ():                         # Maps that integer between 1 and 16 back to that state

    a = {1:"[1, 1]", 2:"[2, 1]", 3:"[3, 1]", 4:"[4, 1]", 5:"[1, 2]", 6:"[2, 2]", 7:"[3, 2]", 8:"[4, 2]", 9:"[1, 3]", 10:"[2, 3]", 11:"[3, 3]", 12:"[4, 3]",
         13:"[1, 4]", 14:"[2, 4]", 15:"[3, 4]", 16:"[4, 4]"}

    return a

def check_dead (unsafe):               # Using what agent inferred till now (unsafe list), this function figures out whether agent will be dead for sure or not 
                                       # in trying to reach [4,4]
    ct = 0
    for i in unsafe:
        if i==[4,3]:
            ct+=1
        
        if i==[3,4]:
            ct+=1
    
    if ct==2:                           # Both [3,4] and [4,3] are unsafe, so agent has no way to reach [4,4]. 
        return True

    for i in range(1,5):                
        ct = 0
        for j in range(1,5):
            if [i,j] in unsafe:
                ct+=1
        
        if ct==4:                       # All columns for a particular row are unsafe, so agent cannot cross that row
            return True
        
    for i in range(1,5):
        ct = 0
        for j in range(1,5):
            if [j,i] in unsafe:
                ct+=1
        
        if ct==4:                       # All rows for a particular column are unsafe, so agent cannot cross that column
            return True
    
    for j in range(1,5):
        if [1,j] in unsafe:
            last = j

            if [2,last-1] in unsafe or [2,last] in unsafe or [2,last+1] in unsafe:
                if [2,last-1] in unsafe: 
                    last = last-1
                
                elif [2,last+1] in unsafe:
                    last = last+1

                if [3,last-1] in unsafe or [3,last] in unsafe or [3,last+1] in unsafe:
                    if [3,last-1] in unsafe: 
                        last = last-1
                    
                    elif [3,last+1] in unsafe:
                        last = last+1

                    if [4,last-1] in unsafe or [4,last] in unsafe or [4,last+1] in unsafe:
                        return True

    
    for i in range(1,5):
        if [i,1] in unsafe:
            last = i

            if [last-1,2] in unsafe or [last,2] in unsafe or [last+1,2] in unsafe:
                if [last-1,2] in unsafe: 
                    last = last-1
                
                elif [last+1,2] in unsafe:
                    last = last+1

                if [last-1,3] in unsafe or [last,3] in unsafe or [last+1,3] in unsafe:
                    if [last-1,3] in unsafe: 
                        last = last-1
                    
                    elif [last+1,3] in unsafe:
                        last = last+1

                    if [last-1,4] in unsafe or [last,4] in unsafe or [last+1,4] in unsafe:
                        return True
        
        
    return False