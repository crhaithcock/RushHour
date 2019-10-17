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

c = 5
t = 2

c1 = np.arange(c//1 + 1)  # num strips with 1 car
c2 = np.arange(c//2 + 1)  # num strips with 2 cars
c3 = np.arange(c//3 + 1)  # num strips with 3 cars

t1 = np.arange(t//1 + 1)  # num strips with 1 truck
t2 = np.arange(t//2 + 1)  # num strips with 2 trucks


'''
General Array Structure


c1 - num instances of TOPO_ONE_CAR
c2 - num instances of TOPO_TWO_CARS
c3 - num instances of TOPO_THREE_CARS
ct - num instances of TOPO_CAR_TRUCK
tc - num instances of TOPO_TRUCK_CAR
t1 - num instances of TOPO_ONE_TRUCK
t1 - num instances of TOPOT_TWO_TRUCKS

'''


# Start with constructing TOPO Counts without CT or TC
C = [x for x in itertools.product(c1,c2,c3) if np.dot(x,[1,2,3]) == c]
T = [x for x in itertools.product(t1,t2) if np.dot(x,[1,2]) == t]
set_no_ct = [ x + (0,) + (0,) + y for x in C for y in T]


# Contruct the TOPO Counts with CT and TC
# Each instance of of set_1 with c1 >= 1 is eligible to be replaced with CT and TC
# These are the only instances in which TC or CT can appear in the counts
set_with_ct = []

if c >= 1 and t >= 1:
    C_CT = []
    
    C_CT_eligible = [x for x in C if x[0] >= 1]
    
    for (c1,c2,c3) in C_CT_eligible: 
        r = np.arange(min(c1,t)) + 1 
        C_CT = C_CT + [(c1-i,c2,c3,i,0) for i in r]
        C_CT = C_CT + [(c1-i,c2,c3,0,i) for i in r]
        
    T_CT = [x for x in itertools.product(t1,t2) if np.dot(x,[1,2]) == (t-1)]

    set_with_ct = [x + y for x in C_CT for y in T_CT]
    

topo_set = set_no_ct + set_with_ct

STRIPS = ['C','CC','CCC','CT','TC','T','TT']
SLOTS = range(12)
EXIT_SLOT = 2
ROW_SLOTS = SLOTS[:6]
COL_SLOTS = SLOTS[6:]

# protoyping loop through topo_set

# for each strip_list s in topo_set -- need better name

# strip_list is a 7-elt list of strip_counts
s = topo_set[0]
s_tot_strips = sum(s)

# s = [c1,2,c3,ct,tc,t1,t2]
# this  strip count gives rise to a set of slot arrangements

s_topo_type_nested = [x for x in [ [STRIPS[i]]*s[i] for i in range(len(s))] if x]

#temp looks something like [ ['C','C'] , ['CC'] , [] , [] , ['CT'], [], [], ['TT']]
# marrying the counts in s with the list STRIPS

# flatten the above result into a single list of strips to be distributed
# accross a combinatorial subset of rows/cols
s_topo_type = list(itertools.chain(*s_topo_type_nested))
# result looks something like [ 'C','C','CC','CT,'TT']

s_topo_type_perms = list(itertools.permutations(s_topo_type))
# build out all possible permutations of s_topo_type
# this list of permutations will be combined with a particular subset of row/cols
# to build out the topo classes


# now find sets of roww/cols to pair with elts of s_topo_type_perms
s_all_slot_sets = [x for x in itertools.combinations(SLOTS,s_tot_strips) if EXIT_SLOT in x]

# Now loop through each slot set as each slot set gives rise to a set of 
# topo classes

# for each slot in s_slot_set
s_slot_set = s_all_slot_sets[0]


# s_slot = [1,2,5,9,11] - a list of rows/cols selected to be filled with
# strips in by s_topo_type
# one such distribution of elts of s_topo_type across one s_slot is a topo_class

# We now marry the permutation of topo strips
# with this subset of row/col slots
# some of the matches are incompatible with game rules
# must have a red car in exit row

s_slot_admissible_topo_types = [x for x in s_topo_type_perms if x[2] not in ['T','TT'] ]

topo_classes = []

for topo_type in s_slot_admissible_topo_types:
    topo_class = [0]*12
    for i in range(len(topo_type)):
        topo_class[s_slot_set[i]] = topo_type[i]
    topo_classes.append(topo_class)


    # Each Topo Class defines a set of states. This set of states will coontains
    # one or more components of the RH Graph. THis is the smallest such set
    # I have figured out how to construct to feed into the graph algorithms


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
    slots.remove(EXIT_SLOT)
    board_strips = gen.HORZ_STRIPS[topo_class[EXIT_SLOT]]
    for strip in board_strips:
        red_cars = np.where(np.array(strip)==6)
        for i in range(0,len(red_cars[0]),2):
            state = np.array([0]*36).reshape(6,6)
            state[EXIT_SLOT] = strip
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
    
    if slot in ROW_SLOTS:
        board_strips = gen.HORZ_STRIPS[topo_class[slot]] 
        
        for strip in board_strips:
            state[slot] = strip
            topo_class_states_recursion(state,topo_class,loc_slots,red_car_end_a)

    elif slot in COL_SLOTS:
        board_strips = gen.VERT_STRIPS[topo_class[slot]]
        
        for strip in board_strips:
            x = state[:,slot]
            y = x + strip
            if np.all(strip == y - x):
                state[slot] = strip
                topo_class_states_recursion(state,topo_class,loc_slots,red_car_end_a)
                
    else:
        raise ValueError("slot is not in ROW_SLOTS or COL_SLOTS",slot)           
                
        
            
    






