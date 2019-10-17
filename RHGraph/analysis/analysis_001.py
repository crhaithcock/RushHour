# -*- coding: utf-8 -*-
"""
Created on Tue Oct  8 00:09:08 2019

@author: CHaithcock
"""

import sys
#sys.path.insert(1, 'C:/Users/chaithcock/Documents/repos/RushHour/RHGraph')
sys.path.insert(1, 'C:/Users/chaithcock/Documents/repos/RushHour/RHGraph/generators')


import itertools
import sqlite3
import numpy as np
import datetime


import GenerateStatesByTopology as gen
#import RHState
#import RHComponent


sqlite3.register_adapter(np.int32, lambda val: int(val))



def init_comb_strip_keys():
    conn = sqlite3.connect(r'C:\Users\chaithcock\Documents\repos\RushHour\RHGraph\DataStore\rush_hour.db')
    cur = conn.cursor()
    
    
     
    comb_class_list = []
    vector_list = []

    for c in range(1,13):
        for t in range(5):
            strip_vectors = gen.combo_class_to_strip_counts(c,t)
            comb_class_list.append((c,t,len(strip_vectors)))
        
            for v in strip_vectors:
                vector_list.append(v+('',0,0,0))
        
        
    
    
    #cc_sql = "INSERT INTO Combclasses values(?,?,?)"
    sv_sql = "INSERT INTO StripVectors values(?,?,?,?,?,?,?,?,?,?,?)"
    cur.executemany(sv_sql,vector_list)
    
    #cur.executemany(cc_sql,comb_classes)

    conn.commit()
    conn.close()
            

def init_class_topo_keys(c,t):
    print (datetime.datetime.now())
    vectors = gen.combo_class_to_strip_counts(c,t)
    init_topo_keys(vectors)    
    print (datetime.datetime.now())


def init_topo_keys(strip_vectors):
    conn = sqlite3.connect(r'C:\Users\chaithcock\Documents\repos\RushHour\RHGraph\DataStore\rush_hour.db')
    cur = conn.cursor()
    
    class_list = []
    q_str = ','.join(['?']*17)
    sql = "INSERT INTO TopoClasses Values ("+ q_str +")"

    for v in strip_vectors:
        ct = sum(v[3:5])
        c = sum(v[:3]) + ct
        t = sum(v[5:]) + ct
    
        topo_classes = gen.from_strip_count_to_topo_classes(v)
        class_list.extend([x + [c,t,0,0,0] for x in topo_classes])
        if len(class_list) > 10000:
            cur.executemany(sql,class_list)
            conn.commit()
            class_list = []
            
    if class_list:
        cur.executemany(sql,class_list)
        conn.commit()
    
    conn.close()
    

#c = 9
c = 10
#c = 11
#c = 12

for t in range(5):
    print("starting comb class: (%i,%i)"%(c,t),flush=True)
    vectors = gen.combo_class_to_strip_counts(c,t)
    init_topo_keys(vectors)
    




# create subsets of topological classes
# 

# chweck cards for topo classes and strip_vectors

# maximize interference.

# spread strips across both rows and cols
# bias towards CC
# avoid CCC and TT

 