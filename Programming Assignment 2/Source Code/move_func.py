import basic_func

def move_doubt (x, temp, flox, ag):

    flag = False
    if len(temp)!=0:                     # If available, choose a unvisited yet safe state to go next 
        for i in temp:
            if i[0]>x[0] and i[1]==x[1]:
                ag.TakeAction('Right')
                last = "Right"
                flag = True
                break
        
        if flag==False:
            for i in temp:
                if i[0]==x[0] and i[1]>x[1]:
                    ag.TakeAction('Up')
                    last = "Up"
                    flag = True
                    break
        
        if flag==False:
            for i in temp:
                if i[0]==x[0] and i[1]<x[1]:
                    ag.TakeAction('Down')
                    last = "Down"
                    flag = True
                    break
        
        if flag==False:
            for i in temp:    
                if i[0]<x[0] and i[1]==x[1]:
                    ag.TakeAction('Left')
                    last = "Left"
                    flag = True
                    break
    
    if flag==False:                          # No unvisited and safe neighbor, so backtrack to one of visited and safe now.
        for i in flox:
            if i[0]>x[0] and i[1]==x[1]:
                ag.TakeAction('Right')
                last = "Right"
                flag = True
                break
            
        if flag==False:
            for i in flox:
                if i[0]==x[0] and i[1]>x[1]:
                    ag.TakeAction('Up')
                    last = "Up"
                    flag = True
                    break
        
        if flag==False:      
            for i in flox:    
                if i[0]<x[0] and i[1]==x[1]:
                    ag.TakeAction('Left')
                    last = "Left"
                    flag = True
                    break   

        if flag==False:
            for i in flox:
                if i[0]==x[0] and i[1]<x[1]:
                    ag.TakeAction('Down')
                    last = "Down"
                    flag = True
                    break
        
    return last


def move_no_doubt (x, inf, last, unsafe, neighbor, vis, doubt, dead_end, temp, flox, zulo, ag, store):
    
    flag = False
    if len(temp)!=0:                            # We must first explore unvisited yet safe neighbors to reach [4,4] faster.              
        for i in temp:
            if i[0]>x[0] and i[1]==x[1]:
                ag.TakeAction('Right')
                last = "Right"
                flag = True
                break
        
        if flag==False:
            for i in temp:
                if i[0]==x[0] and i[1]>x[1]:
                    ag.TakeAction('Up')
                    last = "Up"
                    flag = True
                    break
        
        if inf==True and flag==False:              # If we inferred something new at this point, backtrack to try the doubt state that we had left at that time
            if last=="Up":
                ag.TakeAction("Down")
                last = "Down"
            
            elif last=="Down":
                ag.TakeAction("Up")
                last = "Up"

            elif last=="Right":
                ag.TakeAction("Left")
                last = "Left"
            
            else:
                ag.TakeAction("Right")
                last = "Right"
            
            return last
        
        if flag==False:
            for i in temp:
                if i[0]==x[0] and i[1]<x[1]:
                    ag.TakeAction('Down')
                    last = "Down"
                    flag = True
                    break
        
        if flag==False:
            for i in temp:    
                if i[0]<x[0] and i[1]==x[1]:
                    ag.TakeAction('Left')
                    last = "Left"
                    flag = True
                    break
    
    elif len(zulo)!=0 and store.count(zulo[0])<=1:       # Since normal path was not available, explore the doubt state again (if not visited more than twice)
        if zulo[0][0]==x[0] and zulo[0][1]>x[1]:
            ag.TakeAction('Up')
            last = "Up"
        
        elif zulo[0][0]==x[0] and zulo[0][1]<x[1]:
            ag.TakeAction('Down')
            last = "Down"
        
        elif zulo[0][0]>x[0] and zulo[0][1]==x[1]:
            ag.TakeAction('Right')
            last = "Right"
        
        elif zulo[0][0]<x[0] and zulo[0][1]==x[1]:
            ag.TakeAction('Left')
            last = "Left"

    else:                                       # Otherwise, explore an already visited and safe state.
        xy = 0
        if x not in dead_end:
            for i in neighbor:                          # All neighbors except the one from which we came are unsafe / dead-ends
                if i in dead_end or i in unsafe:
                    xy += 1

            if xy==len(neighbor)-1:
                dead_end.append(x)  
            
            else:
                flag = 0
                for i in neighbor:
                    if i not in doubt and i not in dead_end and i not in unsafe:
                        nbrs = []
                        basic_func.get_neighbors(nbrs,i)
                        for j in nbrs:
                            if j not in vis and j not in unsafe:
                                flag = 1
                
                if flag==0:                         # All neighbors have been explored (as much as possible) - none of them have safe yet unvisited neighbor
                    dead_end.append(x)

        flag = False
        if len(flox)!=0:
            for i in flox:
                if i[0]>x[0] and i[1]==x[1]:
                    ag.TakeAction('Right')
                    last = "Right"
                    flag = True
                    break
        
            if flag==False:
                for i in flox:
                    if i[0]==x[0] and i[1]>x[1]:
                        ag.TakeAction('Up')
                        last = "Up"
                        flag = True
                        break
            
            if flag==False:
                for i in flox:    
                    if i[0]<x[0] and i[1]==x[1]:
                        ag.TakeAction('Left')
                        last = "Left"
                        flag = True
                        break

            if flag==False:
                for i in flox:
                    if i[0]==x[0] and i[1]<x[1]:
                        ag.TakeAction('Down')
                        last = "Down"
                        flag = True
                        break
    return last


def move (x, inf, last, safe, unsafe, neighbor, vis, doubt, dead_end, ag, store):

    temp = []
    flox = []
    zulo = []
    for i in range(1,5):
        for j in range(1,5):
            if ([i,j] not in vis) and ([i,j] in safe) and ([i,j] in neighbor) and ([i,j] not in dead_end):
                temp.append([i,j])
            
            if ([i,j] in vis) and ([i,j] in safe) and ([i,j] in neighbor) and ([i,j] not in dead_end) and ([i,j] not in doubt):
                flox.append([i,j])

            if ([i,j] in doubt) and ([i,j] in neighbor):
                zulo.append([i,j])
    
    
    if x not in doubt:
        return move_no_doubt(x, inf, last, unsafe, neighbor, vis, doubt, dead_end, temp, flox, zulo, ag, store)
        
    else:
        return move_doubt(x, temp, flox, ag)

        

        
