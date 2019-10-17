# -*- coding: utf-8 -*-
"""
Created on Mon Sep 23 19:45:18 2019

@author: CHaithcock
"""

import sys
sys.path.insert(1, 'C:/Users/chaithcock/Documents/repos/RushHour/RHGraph')

import itertools
import numpy as np

import RHGeneratorConstants as gen
import RHState


'''

Terms.
    Topological Strip
        There are 8 possible ways to arrange cars/trucks in a single row or column.
        Type 0: empty (no cars or trucks)
        Type 1: C   (one car)
        Type 2: CC  (two cars)
        Type 3: CCC (three cars)
        Type 4: CT  (one car one truck)
        Type 5: TC  (one truck one car)
        Type 6: T   (one truck)
        Type 7: TT  (two trucks)       
        
    Board Slot (or simply slot)
        In this construction, we consider the rush hour board as consisting
        of 6 rows and 6 columns. We oftern refer to the 12 slots without 
        distinguishing rows and columns. When important to distinguish, 
        we use the terms row slots and column slots as needed.
    
    Topological Class
        The topological class of a state is a 12-dim vector listing for each 
        row slot and column slot which topologial strip occupies that slot.
        
        Note, every state wtihin a connected component belongs to the same
        topological class.
        
        Note, two states from different connected components in the RH Graph
        may belong to the same topological class
        
        Consider this pathological example. These two states have the same 
        arrangment of topological strips, but there is no sequence of moves
        that will take us from one state to the other
        
        C C 0 T 0 0           0 0 0 T C C
        0 0 0 T 0 0           0 0 0 T 0 0  
        0 0 0 T C C           0 C C T 0 0 
        0 0 0 T 0 0           0 0 0 T 0 0 
        0 0 0 T 0 0           0 0 0 T 0 0 
        

Using the terminology above, we now outline a procedure that given a number of
cars c and trucks t to construct all possible topological classes across all
RH States with c cars and t trucks.


We use combinatorial constructions to generate all possible topological
classes. And then for each topoogical class, we construct all states belonging
to that topoligical class.

1. For a given number of cars c and trucks t, generate all possible 7-dim 
   vectors <c1,c2,c3,ct,tc,t1,t2> where
   
   c1 + c2 + c3 + ct + tc = c
        ct + tc + t1 + t2 = t
   
   c1 is the number of type 1 topological strips
   c2 is the numbef of type 2 topological strips
   c3 is the numbef of type 3 topological strips
   ct is the numbef of type 4 topological strips
   tc is the numbef of type 5 topological strips
   t1 is the numbef of type 6 topological strips
   t2 is the numbef of type 7 topological strips
   
   We will marry permutations of topological strips with subsets of slots.
   

2. For each vector <c1,c2,c3,ct,tc,t1,t2> in (1), create a bag of 
   associated topological strips.
   
   For instance for vector <2,1,0,0,1,2,0> correspods to this bag of
   topological strips: {C,C,CC,TC,T,T}.
   
   Note, for a given c and t, we can get two vectors in 1 that give rise to two 
   very different bags in (2). Consider
   
   c = 6 , t = 2
   
   <6,0,0,0,0,2,0> ==> {C,C,C,C,C,C,T,T}
   <0,0,2,0,0,0,1> ==> {CCC,CCC,TT}
   

3. For each bag of topological strips, calculate all subsets of the 12 slots
   satisifying 
   
     i) each subset contains the exit row which contains the red car
    ii) the number of slots equals the number of stips in the bag


4. For each subset in (3) calculate all distinct permutations of arranging
   the strips in the bag across the selected subset of slots given that 
   the exit row is populated with a car. That is, the exit row may not be
   populated by a T or TT strip.

    Each of these arrangements that pairs a permutation of strips with a subset
    of slots defines a topological class.
   
    For each topological class, we construct all possible states belonging
    to that class
    
5. Construct all states for a given topological class.
   This procedure is non-combinatorial. Refer to the actual code
   of this procedure for clarity on this step.
   
   
'''


# Procedure Inputs

c = 8
t = 3

'''
1. For a given number of cars c and trucks t, generate all possible 7-dim 
   vectors <c1,c2,c3,ct,tc,t1,t2> 
   
   Split this constuction into two parts
   i) all vectors with tc = ct = 0
  ii) all vectors with tc > 0 or tc > 0

'''

# Step 1.i: all 7-dim vectors with tc = tc = 0.

# create lists (1,2,...) from 1 to the most number of strips possible for each 
# toplogical strip type except for CT and TC

c1 = np.arange(c//1 + 1)  # strips with 1 car
c2 = np.arange(c//2 + 1)  # strips with 2 cars
c3 = np.arange(c//3 + 1)  # strips with 3 cars
t1 = np.arange(t//1 + 1)  # strips with 1 truck
t2 = np.arange(t//2 + 1)  # strips with 2 trucks

C = [x for x in itertools.product(c1,c2,c3) if np.dot(x,[1,2,3]) == c]
T = [x for x in itertools.product(t1,t2) if np.dot(x,[1,2]) == t]
stip_counts_no_ct = [ x + (0,) + (0,) + y for x in C for y in T]



# Step 1.ii: all 7-dim vectors with tc > 0 or tc > 0 



# must have at least one car and at least one truck to support topological stip 
# types CT and TC
if c >= 1 and t >= 1:
    
    # min(c,t) defines the largest number of strips permitted
    # pairing a car with a truck  
    max_ct = min(c,t)
    
    CT = []
    TC = []
    
    # Each instance of CT ripples into a recalculation of the C and T lists
    for ct in range(1,max_ct + 1):
        
        c1 = np.arange((c-ct)//1 + 1)  # remaining strips with 1 car
        c2 = np.arange((c-ct)//2 + 1)  # remaining strips with 2 cars
        c3 = np.arange((c-ct)//3 + 1)  # remaining strips with 3 cars
        t1 = np.arange((t-ct)//1 + 1)  # remaining strips with 1 truck
        t2 = np.arange((t-ct)//2 + 1)  # remaining strips with 2 trucks

        C = [x for x in itertools.product(c1,c2,c3) if np.dot(x,[1,2,3]) == c-ct]
        T = [x for x in itertools.product(t1,t2) if np.dot(x,[1,2]) == t-ct]
        
        CT = CT + [x + (ct,) + (0,) + y for x in C for y in T]
        TC = TC + [x + (0,) + (ct,) + y for x in C for y in T]
        
    stip_counts_with_ct = CT + TC
 
strip_counts = stip_counts_no_ct + stip_counts_with_ct





'''
2. For each tuple (c1,c2,c3,ct,tc,t1,t2) just created in (1) create a bag of 
   associated topological strips.

   For this algorithm prototype/study, we select one 7-dim tuple and continue
   the construction from that single choice.   
   
   We use python list to encode the bag.
'''

# s is one tuple out of the set of the big list of strip count tuples
s = strip_counts[0]


s_strip_list_nested = [x for x in [ [gen.STRIPS[i]]*s[i] for i in range(len(s))] if x]
#looks something like [ ['C','C'] , ['CC'] , [] , [] , ['CT'], [], [], ['TT']]

# flatten lists
s_strip_list = list(itertools.chain(*s_strip_list_nested)) 
# result looks something like [ 'C','C','CC','CT,'TT']

'''

3. For each bag of topological strips, calculate all subsets of the 12 slots
   satisifying 
   
     i) each subset contains the exit row which contains the red car
    ii) the number of slots equals the number of stips in the bag
    
    We use itertools to generate all subsets of right size (ii) and filter for (i)
'''

s_slot_sets = [x for x in itertools.combinations(gen.SLOTS,sum(s)) if gen.EXIT_SLOT in x]


'''
4.  For each subset in (3) calculate all distinct permutations of arranging
    the strips in the bag across the selected subset of slots given that 
    the exit row is populated with a car. That is, the exit row may not be
    populated by a T or TT strip.

    Each of these arrangements that pairs a permutation of strips with a subset
    of slots defines a topological class.
    
'''

s_strips_permuted = list(itertools.permutations(s_strip_list))



topo_classes = []
for slot_set in s_slot_sets:
    for perm in s_strips_permuted:
        topo_class = [0] * 12
        for i in range(len(slot_set)):
            topo_class[slot_set[i]] = perm[i]
        
        # vefity exit row contains a car
        if topo_class[gen.EXIT_SLOT] not in ['T','TT']:
            topo_classes.append(topo_class)



'''

5. Construct all states for a given topological class.
    
'''


topo_states = {}

def record_topo_class_state(topo_class,state,red_car_end_a):
    print("\n\nRecording State")
    state = RHState.RHState(state,red_car_end_a)
    topo_class = tuple(topo_class)
    if topo_class in topo_states:
        if topo_states[topo_class]:
            topo_states[topo_class].append(state)
        else:
            topo_states[topo_class] = [state]
    else:
        topo_states[topo_class] = [state]
    

# topo_class: [c1,c2,c3,c4,c5,r1,r2,r3,r4,r5,r6]
def topo_class_states(topo_class,slot_set):
    
    slots = list(slot_set)
    slots.remove(gen.EXIT_SLOT)
    board_strips = gen.HORZ_STRIPS[topo_class[gen.EXIT_SLOT]]
    for strip in board_strips:
        red_cars = np.where(np.array(strip)==6)
        for i in range(0,len(red_cars[0]),2):
            state = np.array([0]*36).reshape(6,6)
            state[gen.EXIT_SLOT] = strip
            red_car_end_a = i + 12
            print("\n\nStarting wtih red car end a: %d"%(red_car_end_a))
            print(red_cars)
            topo_class_states_recursion(state,topo_class,slots,red_car_end_a)

def topo_class_states_recursion(state,topo_class,slots,red_car_end_a):
    #print ("\n\nentering recursion:")
    #print(topo_class)
    #print(slots)
    #print(state)
    if not slots:
        record_topo_class_state(topo_class,state,red_car_end_a)
        return
        
    loc_slots = slots[:] 
    slot = loc_slots.pop()
    
    if slot in gen.ROW_SLOTS:
        board_strips = gen.HORZ_STRIPS[topo_class[slot]] 
        
        for strip in board_strips:
            state[slot] = strip
            topo_class_states_recursion(state,topo_class,loc_slots,red_car_end_a)

    elif slot in gen.COL_SLOTS:
        board_strips = gen.VERT_STRIPS[topo_class[slot]]
        
        for strip in board_strips:
            x = state[:,slot]
            y = x + strip
            if np.all(strip == y - x):
                state[slot] = strip
                topo_class_states_recursion(state,topo_class,loc_slots,red_car_end_a)
                
    else:
        raise ValueError("slot is not in ROW_SLOTS or COL_SLOTS",slot)           
                
        
            
    






