def perceive_0 (safe, neighbor):            # All neighbors are safe
    
    for i in neighbor:
        if i not in safe:
            safe.append(i)

def perceive_1 (x, safe, unsafe, neighbor, pending, doubt, mapping):

    v = []
    if len(neighbor)==2:                     # Only 2 neighbors => the non-safe one has to be unsafe (as 1 neighbor would be safe, by which we reached this state)
        for i in neighbor:
            if i not in safe and i not in unsafe:
                unsafe.append(i)

    else:                                    # Here there are 3 or 4 neighbors - any 1 is unsafe - MAY NOT BE CONCLUSIVE
        ct = 0
        for i in neighbor:
            if i in unsafe:
                ct+=1
        
        if ct==0:                               # Still haven't found anything unsafe. 
            for i in neighbor:
                if i not in safe:
                    v.append(i)                 # Whatever is in v is a possible candidate for a unsafe state

            if len(v)==1: 
                unsafe.append(v[0])
            
            else:
                doubt.append(x)

                if len(v)==2: 
                    pending.append([mapping[str(v[0])], mapping[str(v[1])]])
                    pending.append([-1*mapping[str(v[0])], -1*mapping[str(v[1])]])
                    pending.append([-1000])


                if len(v)==3: 
                    pending.append([mapping[str(v[0])], mapping[str(v[1])], mapping[str(v[2])]])
                    pending.append([-1*mapping[str(v[0])], -1*mapping[str(v[1])]])
                    pending.append([-1*mapping[str(v[1])], -1*mapping[str(v[2])]])
                    pending.append([-1*mapping[str(v[0])], -1*mapping[str(v[2])]])
                    pending.append([-1000])

        else:                                   # ct=1; found the unsafe neighbor
            if x in doubt:
                doubt.remove(x)
            
            for i in neighbor:
                if i not in unsafe and i not in safe:
                    safe.append(i)

def perceive_2 (x, safe, unsafe, neighbor, pending, doubt, mapping):

    v = []
    if len(neighbor)==3:                        # 3 neighbors => In this case, all neighbors (except the one thru which we came here) are unsafe
        for i in neighbor:
            if i not in safe and i not in unsafe:
                unsafe.append(i)
    
    else:                                       # Here there are 4 neighbors - either 3 are unsafe or any 2 are unsafe - NOT  CONCLUSIVE
        ct = 0
        gh = 0
        for i in neighbor:
            if i not in safe and i not in unsafe:
                v.append(i)

        for i in neighbor:
            if i in unsafe:
                ct+=1

            if i in unsafe or i in safe:
                gh+=1        

        if ct==0 and len(v)==2:         # Both have to be unsafe - NO DOUBT
            unsafe.append(v[0])
            unsafe.append(v[1])
        
        elif ct==1 and len(v)==1:       # Has to be unsafe
            unsafe.append(v[0])

        elif ct<2:                        # If ct=0, then 2 or 3 unsafe;  if ct=1, then 1 or 2 unsafe
            doubt.append(x)

            if ct==0:                   # Here len(v) will be 2 or 3 ----- case of len(v)=2 discussed above
                if len(v)==3:           # 2 or more have to be unsafe
                    pending.append([mapping[str(v[0])], mapping[str(v[1])], mapping[str(v[2])]])
                    pending.append([-1*mapping[str(v[0])], mapping[str(v[1])], mapping[str(v[2])]])
                    pending.append([mapping[str(v[0])], -1*mapping[str(v[1])], mapping[str(v[2])]])
                    pending.append([mapping[str(v[0])], mapping[str(v[1])], -1*mapping[str(v[2])]])
                    pending.append([1111])   
            
            elif ct==1:                 # Here len(v) will be 1 or 2 ----- case of len(v)=1 discussed above                       
                if len(v)==2:           # 1 or 2 will be unsafe
                    pending.append([mapping[str(v[0])], mapping[str(v[1])]])
                    pending.append([2222])   
            
            pending.append([1000])
        
        elif ct==2:
            if gh==3:                     
                doubt.append(x)           # 0 or 1 unsafe is possible ; actually nothing to infer, simply this will be just a doubt state
            
            else:                          # gh=4. So, all directions are either safe or unsafe and we are sure --> NO DOUBT
                if x in doubt:
                    doubt.remove(x)

        else:                              # ct=3 ; we have found 3 unsafe neighbors, and 1 is safe (by which we came)
            if x in doubt:
                doubt.remove(x)

''' The penultimate and last elements added to 'pending', during perception help us decide how to 'infer' in the infer function - 
1. Last element is -1000 means dealing with the case when perceive was "=1" ; last element is 1000 means perceive was ">1" for the statements we are inferring
2. Similarly, second last element = 1111 implies either 2 or 3 of the states would be unsafe ;  second last element = 2222 implies either 1 or both states
would be unsafe  '''