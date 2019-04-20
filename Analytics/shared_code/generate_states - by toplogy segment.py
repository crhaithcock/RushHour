
import numpy as np
import sqlite3


import RHutilities as util
from constants import *

conn = db.connect('rush_hour.db')
cur = conn.cursor()




def new_pivot(pivot_position):
    #move left to right and then down.
    x,y = pivot_position
    if y < 5:
        return [x,y+1]
    else:
        return [x+1,y]


# To track the segment orientation, we need to know two things:
# 1. The current segment definition: num vertical cars, num vertical trucks
# 2. The emerging segment orientation of the board being constructed.
def generate_states_by_segment(num_cars,num_trucks,num_v_cars,num_v_trucks):
    v = np.arange([blank] * 36).reshape(6,6)
    
    if segment_already_generated(num_cars,num_trucks,num_v_cars,num_v_trucks):
        print ("Segment Already Generated")
        return


    for y in range(2):
        
        v = np.arange([blank]*36).reshape(6,6)
        
        v[2,y:y+1] = hcar
        red_col = y+1
        pivot = (0,0)
    
        recurse_segment(v,red_col,num_cars-1,num_trucks,pivot,num_v_cars,num_v_trucks) 
    

    
def segment_already_generated(num_cars,num_trucks,num_v_cars,num_v_trucks):
    ''' Test the sqlite database to see if this particular segment has already been generated.
    
    '''
    sql = '''
          select count(1)
          from segment
          where num_v_cars = %s
                and num_h_cars = %s
                and num_v_trucks = %s
                and num_h_trucks = %s 
          '''%(num_v_cars,num_cars - num_v_cars, num_v_trucks, num_trucks - num_v_trucks)

    cur.execute(sql)
    count = cur.fetchone()[0]
    return count > 0 






    
    
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
    
    
def recurse_segment(v,red_col,num_cars,num_trucks,pivot_position,num_v_cars,num_v_trucks):
    '''
        input 
            v: numpy array representing RH board
            red_col: rightmost column covered by red car
            num_cars: number of cars to still be placed on the board
            num_trucks: number of trucks still to be placed on the board
            pivot_position: 2-elt array indicating the current place to attempt to place pieces on the board
            num_v_cars: number of remaining cars that must be oriented vertically
            num_v_trucks: number of remaining trucks that must be oriented vertically
    
    '''
    pivot_row, pivot_col = pivot_position
    
    num_h_cars = num_cars = num_v_cars
    num_h_trucks = num_trucks - num_v_trucks

    
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
    if v[pivot_row,pivot_col] != blank:
        recurse_segment(v,red_col,num_cars,num_trucks,new_pivot_position,num_v_cars,num_v_trucks)
        return
    
    # test for branch exit. If not posisible to lay down remaining pieces, then end recursion
    #!!!! TODO - validate edge conditions here
    #!!!! TODO - how should this test be altered for 
    #if 2*num_cars + 3*num_trucks > 36 - 6*pivot_row + pivot_col:
    #    return
    
    for i in np.arange(pivot_row*6+pivot_col,36):
        row = i//6
        col = i%6
        
        # place hcar if possible
        if num_h_cars > 0 and col < 5 and np.all(v[row,col:col+2] == blank):
            new_v = np.copy(v)
            new_v[row,col:col+2] = hcar
            recurse_segment(new_v,red_col,num_cars-1,num_trucks,new_pivot([row,col]),num_v_cars,num_v_trucks)

        # place vcar if possible
        if num_v_cars > 0 and row < 5 and np.all(v[row:row+2,col] == blank):
            new_v = np.copy(v)
            new_v[row:row+2,col] = vcar
            recurse_segment(new_v,red_col,num_cars-1,num_trucks,new_pivot([row,col]),num_v_cars-1,num_v_trucks)
            
        #place htruck if possible
        if num_h_trucks > 0 and col < 4 and np.all(v[row,col:col+3]==blank):
            new_v = np.copy(v)
            new_v[row,col:col+3] = htruck
            recurse_segment(new_v,red_col,num_cars,num_trucks-1,new_pivot([row,col]),num_v_cars,num_v_trucks)
        
        if num_v_trucks > 0 and row < 4 and np.all(v[row:row+3,col] == blank):
            new_v = np.copy(v)
            new_v[row:row+3,col] = vtruck
            recurse_segment(new_v,red_col,num_cars,num_trucks-1,new_pivot([row,col]),num_v_cars,num_v_trucks-1)


    
#!!!! TODO - figure out mechanism for caller to set writing attributes
def configure_record_state():
    pass


def record_state(v,red_col):
    #global state_counter
    
    #state_counter += 1 
    #record_state_outfile(v,red_col)
    
    #record_state_list(v,red_col)
    record_state_sqlite(v,red_col)




def record_state_list(v,red_col):
    global state_list
    v = util.board_to_int(v)
    red_col = int(red_col) 
    state_list.append( (v,red_col)  )
    
#!!!! TODO - add file management features to this. Consider using 'with' construct.    
outfile = None    
def record_state_outfile(v,red_col):
    global outfile
    
    v_hash = str(int(''.join(vf(v.reshape(1,36))[0]),2))
    
    txt = ','.join([v_hash,str(red_col)])
    
    outfile.write(txt)
    outfile.write('\n')



# !!!! TODO - devise solution to make output selection dynamic at runtime:
#             output to hdf5 file; output to list; output to ?
#             Ideally, the recursive step makes its current call to write out a state. 
#             The switch logic is completely contained in the output routine.
state_list = []

def generate_states(num_cars, num_trucks):
    ''' Entry function for generating states.

    '''
    #global outfile
    #outfile = open(r'\\kaufmanhall.net\vol02$\Axiom\Users\CHaithcock\%d-cars-%d-trucks.txt'%(num_cars,num_trucks),'w')

    
    global state_list
    state_list = []
    
    for i in np.arange(5):
        v = np.zeros((6,6),dtype=int)
        v[2,i:i+2] = hcar        
        recurse(v,int(i+1),num_cars-1,num_trucks, [0,0])


    return state_list
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


