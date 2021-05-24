import basic_func

def clear_doubt (safe, unsafe, doubt, perception_list):
    
    i = 0
    while i<len(doubt):                             # Need to remove multiple doubt states at once
        c1 = 0
        c2 = 0
        nbrs = []
        basic_func.get_neighbors(nbrs, doubt[i])
        for j in nbrs:
            if j in safe or j in unsafe:
                c1+=1
            
            if j in unsafe:
                c2+=1
        
        if c1==len(nbrs):                            # All neighbours of the doubt state are known...so remove it from the doubt list
            doubt.remove(doubt[i])
            i-=1
        
        else:                                       # Doubt state had only 1 unsafe neighbor, and we found that. So, no more doubt :)
            for j in perception_list:
                if j[0]==doubt[i][0] and j[1]==doubt[i][1] and j[2]=="=1" and c2==1:
                    doubt.remove(doubt[i])
                    i-=1
                    break
        
        i+=1