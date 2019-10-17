# -*- coding: utf-8 -*-
"""
Created on Mon Jun 24 11:00:38 2019

@author: CHaithcock
"""



'''

These modular functions will permit the following analysis:
    
    1. How many topo clases are there for a given combinatorial class
    
    2. Isolote topological classes of interest (rows only, mix of rows/cols, etc., no 'CCC' no 'TT')

    3. Create a sampling of components across all of combinatorial classes
    
    
Need a data store solution (SQLite?)



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
    
    Topo Strip Vector
        7-dim vector <c1,c2,c3,ct,tc,t1,t2> encoding 
        
    
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

import sys
sys.path.insert(1, 'C:/Users/chaithcock/Documents/repos/RushHour/RHGraph')

import itertools
import numpy as np

import RHGeneratorConstants as gen
import RHState
import RHComponent




def combo_class_to_strip_counts(num_cars,num_trucks):
    c = num_cars
    t = num_trucks
    
    c1 = np.arange(c//1 + 1)  # num strips with 1 car
    c2 = np.arange(c//2 + 1)  # num strips with 2 cars
    c3 = np.arange(c//3 + 1)  # num strips with 3 cars
    
    t1 = np.arange(t//1 + 1)  # num strips with 1 truck
    t2 = np.arange(t//2 + 1)  # num strips with 2 trucks

    # create lists (1,2,...) from 1 to the most number of strips possible for each 
    # toplogical strip type except for CT and TC
    
    c1 = np.arange(c//1 + 1)  # strips with 1 car
    c2 = np.arange(c//2 + 1)  # strips with 2 cars
    c3 = np.arange(c//3 + 1)  # strips with 3 cars
    t1 = np.arange(t//1 + 1)  # strips with 1 truck
    t2 = np.arange(t//2 + 1)  # strips with 2 trucks


    
    C = [x for x in itertools.product(c1,c2,c3) if np.dot(x,[1,2,3]) == c]
    T = [x for x in itertools.product(t1,t2) if np.dot(x,[1,2]) == t]
    strip_counts_no_ct = [ x + (0,) + (0,) + y for x in C for y in T]
    
    
    # Step 1.ii: all 7-dim vectors with tc > 0 or tc > 0 
    
    # must have at least one car and at least one truck to support topological stip 
    # types CT and TC
    strip_counts_with_ct = []
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
            
        strip_counts_with_ct = CT + TC
    
    # Remove non-sensical arrangemts. At most 12 strips are permitted on the board
    # e.g. can't have c1 = 10 and t1 = 4 even though 10 cars and 4 trucks configurations are possible
    legit_strips_no_ct = [x for x in strip_counts_no_ct if sum(x) <= 12]
    legit_strips_with_ct = [x for x in strip_counts_with_ct if sum(x) <= 12]
    
    return(legit_strips_no_ct + legit_strips_with_ct)



def from_strip_count_to_topo_classes(strip_count_tuple):
    # s is one tuple out of the set of the big list of strip count tuples
    s = strip_count_tuple
    
    
    s_strip_list_nested = [x for x in [ [gen.STRIPS[i]]*s[i] for i in range(len(s))] if x]
    #looks something like [ ['C','C'] , ['CC'] , [] , [] , ['CT'], [], [], ['TT']]
    
    # flatten lists
    s_strip_list = list(itertools.chain(*s_strip_list_nested)) 
    # result looks something like [ 'C','C','CC','CT,'TT']
    
    s_slot_sets = [x for x in itertools.combinations(gen.SLOTS,sum(s)) if gen.EXIT_SLOT in x]



    s_strips_permuted = list(set(itertools.permutations(s_strip_list)))
    
    
    
    topo_classes = []
    for slot_set in s_slot_sets:
        for perm in s_strips_permuted:
            topo_class = [0] * 12
            for i in range(len(slot_set)):
                topo_class[slot_set[i]] = perm[i]
            
            # vefity exit row contains a car
            if topo_class[gen.EXIT_SLOT] not in ['T','TT']:
                topo_classes.append(topo_class)
            
    return(topo_classes)      




topo_states = {}
topo_state_count = {}

def record_topo_class_state(topo_class,state,red_car_end_a):
    
    #record_topo_class_state_count(topo_class)
    #return

    global topo_states
    state = RHState.RHState(state,red_car_end_a)
    topo_class = tuple(topo_class)
    if topo_class in topo_states:
        if topo_states[topo_class]:
            topo_states[topo_class].append(state)
        else:
            topo_states[topo_class] = [state]
    else:
        topo_states[topo_class] = [state]


def record_topo_class_state_count(topo_class):
    global topo_state_count
    
    topo_class = tuple(topo_class)
    
    if topo_class in topo_state_count:
        topo_state_count[topo_class] += 1
    else:
        topo_state_count[topo_class] = 1 


# topo_class: [c1,c2,c3,c4,c5,r1,r2,r3,r4,r5,r6]
def from_topo_class_to_states(topo_class):
    
    slots = []
    for i in range(len(topo_class)):
        if topo_class[i] != 0:
            slots.append(i)
        
    slots.remove(gen.EXIT_SLOT)
    board_strips = gen.HORZ_STRIPS[topo_class[gen.EXIT_SLOT]]
    for strip in board_strips:
        red_cars = np.where(np.array(strip)==6)
        for i in range(0,len(red_cars[0]),2):
            state = np.array([0]*36).reshape(6,6)
            state[gen.EXIT_SLOT] = strip
            red_car_end_a = i + 12
            topo_class_states_recursion(state,topo_class,slots,red_car_end_a)

def topo_class_states_recursion(state,topo_class,slots,red_car_end_a):
    #print ("\n\nentering recursion:")
    #print(topo_class)
    #print(slots)
    #print(state)
    if not slots:
        record_topo_class_state(topo_class,state,red_car_end_a)
        return
        
    loc_topo_slots = slots[:] 
    topo_slot = loc_topo_slots.pop()
    
    board_row_slot = topo_slot
    board_col_slot = topo_slot - 6

    if topo_slot in gen.ROW_SLOTS:
        board_strips = gen.HORZ_STRIPS[topo_class[topo_slot]] 
        
        for strip in board_strips:
            state[board_row_slot] = strip
            topo_class_states_recursion(state,topo_class,loc_topo_slots,red_car_end_a)

    elif topo_slot in gen.COL_SLOTS:
        board_strips = gen.VERT_STRIPS[topo_class[topo_slot]]
        
        for strip in board_strips:
            x = state[:, board_col_slot]
            if not np.any(np.logical_and(x,strip)):
                state[:,board_col_slot] = state[:,board_col_slot] + strip
                topo_class_states_recursion(state,topo_class,loc_topo_slots,red_car_end_a)
                state[:,board_col_slot] = state[:,board_col_slot] - strip
    else:
        raise ValueError("slot is not in ROW_SLOTS or COL_SLOTS",topo_slot)           



'''
comb_class_strip_vec_counts = {}
for c in range(1,13):
    for t in range(5):
        counts =   len(combo_class_to_strip_counts(c,t))
        comb_class_strip_vec_counts[(c,t)] = counts
        
        
topo_class = ['CC']*6 + [0]*6 
from_topo_class_to_states(topo_class)
states = topo_states[tuple(topo_class)]
c = RHComponent.RHComponent.from_state_list(states)


'''



