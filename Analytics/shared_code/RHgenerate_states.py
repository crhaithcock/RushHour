
import numpy as np
import sqlite3 as db
import pandas as pd

import RHconstants as const
import RHutilities as util

comb_class = 0

# sql output data
SQL_SAVE_BATCH_SIZE = 10000
sql_save_count = 0
sql_set = set()
sql_conn = None
sql_columns = ['comb_class','board_int_s1','board_int_s2','red_col','included_in_component']


 
# file output data
outfile = None  

# list output data
state_list = []

# set output data
state_set = []


def new_pivot(pivot_position):
    #move left to right and then down.
    x,y = pivot_position
    if y < 5:
        return [x,y+1]
    else:
        return [x+1,y]


def generate_states(num_cars,num_trucks):

    v = np.arange([blank] * 36).reshape(6,6)
    for y in range(5):
        
        v = np.arange([blank]*36).reshape(6,6)
        
        v[2,y:y+1] = hcar
        red_col = y+1
        pivot = (0,0)

        recurse(v,red_col,num_cars-1,num_trucks,pivot)
        #recurse(s, num_cars-1,num_trucks,[0,0])
        

def new_pivot(pivot_position):
    #move left to right and then down.
    row,col = pivot_position
    if col < 5:
        return [row,col+1]
    elif col == 5 and row < 5:
        return [row+1,0]
    else:
        # else return bad value to create error
        #!!!! TODO - add proper error handling here
        return[0.5,0.5] 




    
    
    
# s is a State: numpy array representing board. And marker for position of red car
# num_cars is number of cars remaning to place on board
# num_trucks is number of trucks remaining to place on board
# pivot_position is the start position to loop through and place one car or one truck on the board.


def recurse(v,red_col,num_cars,num_trucks,pivot_position):
    '''
        input 
            v: numpy array representing RH board
            red_col: rightmost column covered by red car
            num_cars: number of cars to still be placed on the board
            num_trucks: number of trucks still to be placed on the board
            pivot_position: 2-elt array indicating the current place to attempt to place pieces on the board
    
    '''
    pivot_row, pivot_col = pivot_position
    
    # test base case exit condition
    if num_cars == 0 and num_trucks == 0:
        record_state(v,red_col)
        return
    
    # can't place piece hooked to last square
    if pivot_position == [5,5]:
        return
    
    # in all cases of a recursive call, we move to next pivot position
    new_pivot_position = new_pivot(pivot_position)
    
    # test if current position is filled - move to next position on board
    if v[pivot_row,pivot_col] != const.blank:
        recurse(v,red_col,num_cars,num_trucks,new_pivot_position)
        return
    
    # test for branch exit. If not posisible to lay down remaining pieces, then end recursion
    #!!!! TODO - validate edge conditions here
    if 2*num_cars + 3*num_trucks > 36 - 6*pivot_row + pivot_col:
        return
    
    for i in np.arange(pivot_row*6+pivot_col,36):
        row = i//6
        col = i%6
        
        # place hcar if possible
        if num_cars > 0 and col < 5 and np.all(v[row,col:col+2] == const.blank):
            new_v = np.copy(v)
            new_v[row,col:col+2] = const.hcar
            recurse(new_v,red_col,num_cars-1,num_trucks,new_pivot([row,col]))

        # place vcar if possible
        if num_cars > 0 and row < 5 and np.all(v[row:row+2,col] == const.blank):
            new_v = np.copy(v)
            new_v[row:row+2,col] = const.vcar
            recurse(new_v,red_col,num_cars-1,num_trucks,new_pivot([row,col]))
            
        #place htruck if possible
        if num_trucks > 0 and col < 4 and np.all(v[row,col:col+3]==const.blank):
            new_v = np.copy(v)
            new_v[row,col:col+3] = const.htruck
            recurse(new_v,red_col,num_cars,num_trucks-1,new_pivot([row,col]))
        
        if num_trucks > 0 and row < 4 and np.all(v[row:row+3,col] == const.blank):
            new_v = np.copy(v)
            new_v[row:row+3,col] = const.vtruck
            recurse(new_v,red_col,num_cars,num_trucks-1,new_pivot([row,col]))




#!!!! TODO - figure out mechanism for caller to set writing attributes
def configure_record_state():
    pass


def record_state(v,red_col):
    #global state_counter
    
    #state_counter += 1 
    #record_state_outfile(v,red_col)
    
    #record_state_list(v,red_col)
    #record_state_set(v,red_col)
    
    record_state_sql(v,red_col)
    
    

def sql_write_data():
    
    global sql_conn
    global sql_set
    global sql_columns
    
    df = pd.DataFrame(list(sql_set),columns = sql_columns)
    df.to_sql('node',sql_conn,if_exists="append",index=False)
      
     

sql_total_record_count = 0
def record_state_sql(v,red_col):
    
    global sql_save_count
    global SQL_SAVE_BATCH_SIZE
    global sql_set
    global comb_class
    global sql_total_record_count
    
    s1,s2 = util.split_int(util.board_to_int(v))
    included_in_component = 0 # False for sqlite
    sql_set.add( (comb_class, s1, s2, int(red_col),included_in_component) )
    sql_save_count +=1
    
    if sql_save_count >= SQL_SAVE_BATCH_SIZE:
          sql_total_record_count += len(sql_set)
          sql_write_data()
          print ("%d - Records Written: %s" %(comb_class, '{:,}'.format(sql_total_record_count)))
          sql_set.clear() 
          sql_save_count = 0


def record_state_list(v,red_col):
    global state_list
    v = board_to_int(v)
    red_col = int(red_col) 
    state_list.append( (v,red_col)  )

    
def record_state_set(v,red_col):
    global state_set
    v = board_to_int(v)
    red_col = int(red_col)
    state_set.add( (v,red_col) )
#!!!! TODO - add file management features to this. Consider using 'with' construct.    

  
def record_state_outfile(v,red_col):
    global outfile
    
    v_hash = str(int(''.join(vf(v.reshape(1,36))[0]),2))
    
    txt = ','.join([v_hash,str(red_col)])
    
    outfile.write(txt)
    outfile.write('\n')



# !!!! TODO - devise solution to make output mode dynamic at runtime:
#             output to hdf5 file; output to list; output to ?
#             Ideally, the recursive step makes its current call to write out a state. 
#             The switch logic is completely contained in the output routine.
state_set = set()

def generate_states(num_cars, num_trucks,conn):
    ''' Entry function for generating states.

    '''
    global comb_class
    comb_class = util.comb_class(num_cars, num_trucks)
    
    #global outfile
    #outfile = open(r'\\kaufmanhall.net\vol02$\Axiom\Users\CHaithcock\%d-cars-%d-trucks.txt'%(num_cars,num_trucks),'w')

    
    #s state set mode enter
    #global state_set
    #state_set = set()
    
    # state list mode enter
    #global state_list
    #state_list = set()
    
    # sql mode enter
    global sql_set
    global sql_conn
    global sql_total_record_count
    sql_set = set()
    sql_conn = conn
    cur = sql_conn.cursor()
    cur.execute("delete from node")
    sql_conn.commit()
    sql_total_record_count = 0
    sql_save_count = 0
                           
    for i in np.arange(5):
        v = np.zeros((6,6),dtype=int)
        v[2,i:i+2] = const.hcar        
        recurse(v,int(i+1),num_cars-1,num_trucks, [0,0])
        
    
    #sql mode exit
    if len(sql_set)>0:
        sql_total_record_count += len(sql_set)
        sql_write_data()
        print ("%d - Total Records Written: %s"%(comb_class, "{:,}".format(sql_total_record_count) ))
 
    # state set mode exit
    #return state_set
    
    # outfile mode exit
    #outfile.close()



#!!!! - TODO & Notes

# take graph measures
#   number of nodes
#   number of edges
#   number of soln_states
#   average degree
#   degree distribution?
#   soln path structures
#   min/max measures
#   ...


# build/analyze distance partition
#   max soln distance
#   soln path structures,...


# Save to HDF5 file



# Notes on nbrs function. Return up,down,left,right lists to assist graphical display

# generate a block of nodes
# slice that block into chucks such that:
#   1. the chunk can fit in memory and be processed through the graph algorithms
#   2. if a node x is in the chunk, then the connected component containing x is in the chunk
# 
# persist the chunks for later processing
# 
# processing a chunk:
#   run BFS to create components
#   for each component:
#       take graph measures
#       generate distance partition
#       analyze distance partition
#       
#       updated rollup measures (whole graph, combinatorial class, topological class)
#           max degreea
#           max soln_distance
#           num statesa
#           average degree
#           degree histaogram?
#           num components
#           num solvable components
#           

# Visualize a neighborhood of states


