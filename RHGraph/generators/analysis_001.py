# -*- coding: utf-8 -*-
"""
Created on Tue Oct  8 00:09:08 2019

@author: CHaithcock
"""

import sys
#sys.path.insert(1, 'C:/Users/chaithcock/Documents/repos/RushHour/RHGraph')
#sys.path.insert(1, 'C:/Users/chaithcock/Documents/repos/RushHour/RHGraph/generators')


import sqlite3 
import itertools
#import numpy as np


import GenerateStatesByTopology as gen
#import RHState
#import RHComponent


comb_classes = list(itertools.product(range(1,13),range(5)))

comb_vectors = {}
vector_topo_counts = {}


def init_data_tables():
    '''
        set the keys in the tables:
            Comb_Class (60 records)
            StripVectors (~2300 records)
            
        topo classes are derived from StripVectors
        Can calculate on a vector by vector basis
        
        
    '''
    conn = sqlite3.connect(r'C:\Users\chaithcock\Documents\repos\RushHour\RHGraph\DataStore\rush_hour.db')
    cur= conn.cursor()

    comb_classes = []
    strip_vectors = []
    
    for c in range(1,13):
        for t in range(5):
            vectors = gen.combo_class_to_strip_counts(c,t)
            comb_classes.append((c,t,len(vectors)))
            for v in vectors:
                strip_vectors.append(v + ('',0,0,0))            

    comb_class_sql = "INSERT INTO CombClasses Values (?,?,?)"
    strip_vec_sql = "INSERT INTO StripVectors Values (?,?,?,?,?,?,?,?,?,?,?)"
    cur.executemany(comb_class_sql,comb_classes)
    cur.executemany(strip_vec_sql,strip_vectors)

    conn.commit()
    conn.close()
        

def init_vector_topo_counts():
    for (c,t) in comb_classes:
        
        comb_vectors[(c,t)] = gen.combo_class_to_strip_counts(c,t)
        for vector in comb_vectors[(c,t)]:
            vector_topo_counts[vector] = {'comb_class':(c,t)}
        
        
        
def build_vector_topo_counts(c,t):
    comb_vectors[(c,t)] = gen.combo_class_to_strip_counts(c,t)
    
    
    for key in comb_vectors.keys():
        for vector in comb_vectors[key]:
            topo_classes = gen.from_strip_count_to_topo_classes(vector)
            
            vector_topo_counts[vector] = len(topo_classes)
            

    
    
    
    


# create subsets of topological classes
# 

# chweck cards for topo classes and strip_vectors

# maximize interference.

# spread strips across both rows and cols
# bias towards CC
# avoid CCC and TT

 