import random
inp = int(input("Which program should be run - 8 queens (enter 0) or TSP (enter any other digit) ? "))

if inp==0:
    def fact (n):                                       # Returns factorial of n 
        res = 1    
        for i in range(2, n+1): 
            res = res * i 
            
        return res 

    def nCr (n, r): 
        return (fact(n) / (fact(r)*fact(n - r))) 

    def fitness (a):                                    # Returns fitness value for a state of 8-queens problem 
        var = 0

        # Calculating row clashes -
        for i in range(1,9):
            x = 0
            for j in range(len(a)):
                if a[j]==i:
                    x+=1

            if x>=2:                        # At least 2 or more queens in the ith row
                var += nCr(x,2)

        # Calculating diagonal clashes - 
        for i in range(len(a)):
            for j in range(i+1,len(a)):
                x = abs(i-j)
                y = abs(a[i] - a[j])
                if(x==y):
                    var += 1
        return 29-var

    def cross_over (x,y):                   # Crossover between 2 parents to produce a child      

        ran = random.randint(1,8)        # randomly chosen crossover point 
        kid1 = x[:ran] + y[ran:]         # cross-over 1
        kid2 = y[:ran] + x[ran:]         # cross-over 2

        return [kid1, kid2]

    def random_selection (a):               # Select 2 parents from the population weighted by their fitness value
        pop1 = []
        fit1 = []
        for i in range(len(a)):
            pop1.append(a[i][1])
            fit1.append(a[i][0])

        return random.choices(pop1, weights=fit1, k=2)
    
    def mutate (kid1):                      # Mutate a particular state. Doing so induces randomization, helping model converge to global optimum faster

        ran = random.randint(0,7)       # randomly chosen mutation point
        pos = random.randint(1,8)       # randomly chosen row to which the queen in the col is moved to

        kid1[ran] = pos

    pop = [[1,1,1,1,1,1,1,1] for i in range(200)]                       # all queens on same row (number 1) initially
    iterations = 0
    bfv_per_gen = []

    while(1):
        new_pop = []
        size = len(pop)
        fitness_scores = []

        for i in range(size):
            fitness_scores.append((fitness(pop[i]),pop[i]))
        
        fitness_scores.sort()                                           # sorting by fitness scores of population

        bfv_per_gen.append(fitness_scores[size-1][0])

        if fitness_scores[size-1][0]==29:                               # Found the best state (having no pairs of attacking queens)
            break
        
        iterations+=1

        for i in range(size):

            # CHOOSING PARENTS FOR CROSSOVER
            temp = random_selection(fitness_scores)
            x = temp[0]
            y = temp[1]

            # CROSSOVER
            temp = cross_over(x,y)
            kid1 = temp[0]
            kid2 = temp[1]

            if fitness(kid1) >= fitness(kid2):
                kid = kid1
            
            else:
                kid = kid2

            # MUTATION
            z1 = [1,0]
            wt = [60, 70]                                            # Weights defining the chances of mutation taking place
            x = random.choices(z1, weights=wt, k=1)

            kid1 = []
            kid2 = []
            for k in range(8):
                kid1.append(kid[k])
                kid2.append(kid[k])

            if x[0]==1:
                mutate(kid1)
                mutate(kid2)

                if fitness(kid1) > fitness(kid2):
                    kid = kid1
                
                else:
                    kid = kid2

            new_pop.append(kid)
        
        pop = new_pop

    print('')
    print("Optimal solution was found in ", iterations, " iterations (generations).")
    print("Best fitness value for each generation: ", bfv_per_gen)
    print("Fitness value for best solution: ", fitness_scores[len(fitness_scores)-1][0])
    print("Best solution: ", fitness_scores[len(fitness_scores)-1][1])
    

else:
    def cost (a, b):                                         # Returns cost value for a state of TSP          
        dist = 0    

        for i in range(len(a)-1):
            cur = a[i]
            nxt = a[i+1]
            flag = 0
            for j in range(len(b)):
                if ((b[j][0]==cur and b[j][1]==nxt) or (b[j][0]==nxt and b[j][1]==cur)):
                    dist += b[j][2]
                    flag = 1
                    break
                
            if flag==0:
                dist += 100000
        
        cur = a[len(a)-1]
        nxt = a[0]
        flag = 0
        for j in range(len(b)):
            if ((b[j][0]==cur and b[j][1]==nxt) or (b[j][0]==nxt and b[j][1]==cur)):
                dist += b[j][2]
                flag = 1
                break
                
        if flag==0:
            dist += 100000

        return dist

    def random_selection (a, b):                              # Select 2 parents from the population weighted by their fitness value

        pop = []
        cost = []
        for i in range(len(a)):
            pop.append(b[i])
            cost.append(1000000/a[i])                         # Defined fitness value as 1000000 / corresponding cost value

        return random.choices(pop, weights=cost, k=2)

    def get_child(x, y, z1, z2):                              # Returns a child from parents x and y using an algorithm (described in question)                          

        kid = ['!','!','!','!','!','!','!','!','!','!','!','!','!','!']
        kid[z1:z2] = x[z1:z2]

        temp = 0
        i = 0
        while i < len(y) and temp < len(y):
            if kid[temp] != '!':
                temp += z2-z1
                continue

            if y[i] in x[z1:z2]:
                i+=1
                continue
            
            kid[temp] = y[i]
            temp += 1
            i += 1 
        
        return kid

    def crossover (x, y):                                       # Crossover between 2 parents to produce a child    

        z1 = random.randint(0,13)
        z2 = random.randint(0,13)
    
        if z1 > z2:         # without loss of generality, assume that z1 <= z2
            temp = z1
            z1 = z2
            z2 = temp
        
        kid1 = get_child(x,y,z1,z2)
        kid2 = get_child(y,x,z1,z2)
            
        return [kid1, kid2]

    def mutate (kid1):                                          # Mutate a particular state by swapping 2 random elements of the state.

        ran1 = random.randint(0,13)       
        ran2 = random.randint(0,13)
        
        z = kid1[ran1]
        kid1[ran1] = kid1[ran2]
        kid1[ran2] = z


    pop = [['A','B','C','D','E','F','G','H','I','J','K','L','M','N'] for i in range(1000)]

    distances = []
    distances.extend([('A','G',150), ('A','J',200), ('A','L',120), ('B','H',190), ('B','I',400), ('B','N',130), ('C','D',600), ('C','E',220), ('C','F',400), 
    ('C','I',200), ('D','F',210), ('D','K',300), ('E','I',180), ('F','K',370), ('F','L',600), ('F','M',260), ('F','N',900), ('G','K',550), ('G','L',180), 
    ('H','J',560), ('H','N',170), ('I','N',600), ('J','L',160), ('J','N',500), ('K','M',240), ('L','M',400)])

    min1 = 100000
    iterations = 0
    last_progress = 0
    bcv_per_gen = []

    while(1):
        new_pop = []
        size = len(pop)
        cost_list = []

        for i in range(size):
            cost_list.append(cost(pop[i],distances))
        
        for i in range(size):
            if cost_list[i] < min1:
                min1 = cost_list[i]
                min2 = pop[i]
                last_progress = iterations                     # In this iteration, we found a lower value of round-trip cost 
        
        xx = 10000000
        for i in range(size):
            if cost_list[i] < xx:
                xx = cost_list[i]

        bcv_per_gen.append(xx)                                 # Stores the best (least) cost value for any state in this generation

        if iterations-last_progress == 100:                    # No improvement in cost value for last 100 iterations. So, break hoping that minimum has been reached
            break

        iterations += 1
        
        for i in range(size):

            # CHOOSING PARENTS FOR CROSSOVER
            temp1 = random_selection(cost_list, pop)
            x = temp1[0]
            y = temp1[1]

            # CROSSOVER - 
            temp1 = crossover(x,y)
            kid1 = temp1[0]
            kid2 = temp1[1]      

            if cost(kid1, distances) < cost(kid2, distances):
                kid = kid1
            
            else:
                kid = kid2
            
            # MUTATION - 
            z1 = [1,0]
            wt = [45, 50]                       
            x = random.choices(z1, weights=wt, k=1)

            kid1 = []
            kid2 = []
            for k in range(14):
                kid1.append(kid[k])
                kid2.append(kid[k])

            if x[0]==1:
            
                mutate(kid1)
                mutate(kid2)

                if cost(kid1,distances) < cost(kid2,distances):
                    kid = kid1
                
                else:
                    kid = kid2

            new_pop.append(kid)
        
        pop = new_pop

    a = [bcv_per_gen[i] for i in range(last_progress+1)]
    print('')
    print("The code ran for ", iterations , " iterations  (generations), but the optimal solution was found in " , last_progress , " iterations  (generations).")
    print("Best (lowest) cost value for each generation ", a)
    print("Path cost of best solution" , min1)
    print("Best solution: " , min2)
    