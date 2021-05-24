def infer (kb, safe, unsafe, pending, rv_mapping):

    inf = False
    while True:            # We need to infer repeatedly from the KB till we can make no more inferences
                           # Since, initial inferences depend on later inferences (added later to the list), we start inferring from the end of the 'pending' list
        xx = False
        ll = len(pending)

        if ll>=3 and pending[ll-1][0]==-1000:           # Perception was "=1". 
            if ll>=5:
                if len(pending[ll-5])==3:
                    cur = ll-5
                
                else:
                    cur = ll-3
            else:
                cur = ll-3

            ct = 0
            ct1 = 0
            for i in pending[cur]:
                a = rv_mapping[i]
                g = [int(a[1]),int(a[4])]
                
                if g in safe or g in unsafe:
                    ct+=1
                
                if g in unsafe:
                    ct1+=1
                
            if ct==len(pending[cur])-1 or ct1==1:       # Only 1 unsafe --> Either we know the unsafe place, or we are sure about all but 1 of the places.
                kb.solve()
                solution = kb.get_model()

                for i in solution:
                    if i > 0 and i<1000:                                              
                        a = rv_mapping[i]
                        g = [int(a[1]),int(a[4])]
                        if g not in unsafe:
                            unsafe.append(g)
            
                
                for i in pending[cur]:
                    a = rv_mapping[i]       
                    g = [int(a[1]),int(a[4])]
                    if g not in unsafe and g not in safe:
                        safe.append(g)

                if cur==ll-3:                           # Remove the last 3 elements of list
                    for i in range(3):
                        pending.pop()
                
                else:                                   # Remove the last 5 elements of list
                    for i in range(5):
                        pending.pop()
                
                inf = True
                xx = True


        elif ll>=3 and pending[ll-1][0]==1000:      # Perception was ">1".    
            flag1 = pending[ll-2][0]

            if flag1==2222:
                ct1 = 0
                ct2 = 0
                for i in pending[ll-3]:
                    a = rv_mapping[i]
                    g = [int(a[1]),int(a[4])]
                    
                    if g in unsafe:
                        ct1+=1
                    
                    if g in safe:
                        ct2+=1
          
                if ct1==2 or ct2==1:                # 1 or 2 unsafe --> Either both are already unsafe or we know 1 is safe, only then we can conclude from KB
                    kb.solve()
                    solution = kb.get_model()
                    for i in solution:
                        if i > 0 and i<1000:                                              
                            a = rv_mapping[i]
                            g = [int(a[1]),int(a[4])]
                            if g not in unsafe:
                                unsafe.append(g)


                    for i in range(3):
                        pending.pop()
                    
                    inf = True
                    xx = True
            
            elif flag1==1111:
                ct1 = 0
                ct2 = 0
                for i in pending[ll-6]:
                    a = rv_mapping[i]
                    g = [int(a[1]),int(a[4])]
                    
                    if g in unsafe:
                        ct1+=1
                    
                    if g in safe:
                        ct2+=1
                
                if ct1==3 or ct2==1:                     # 2 or 3 unsafe --> Either all 3 are unsafe, or 1 is safe only then we can be sure and infer from KB
                    kb.solve()
                    solution = kb.get_model()

                    for i in solution:
                        if i > 0 and i<1000:                                              
                            a = rv_mapping[i]
                            g = [int(a[1]),int(a[4])]
                            if g not in unsafe:
                                unsafe.append(g)
                
                    for i in range(6):
                        pending.pop()
     
                    inf = True
                    xx = True

        if xx==False:
            break

    return inf