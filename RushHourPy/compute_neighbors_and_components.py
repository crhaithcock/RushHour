'''
Created on May 5, 2015

@author: cliff
'''

'''

This file contains a collection of methods to compute neighbors, edges, and connected components 
based on a variety of different input.

'''

from collections import deque
from collections import OrderedDict
from utilities import *
import copy
import sqlite3 as db




def topo_classes_subsets_defined_by_state_count(topo_classes_with_counts):
    """ Input: List: [x_i,x_2,...,x_n]; x_i = [t_i,c_i] = [topo_class_hash_i, count_of_states_i]
        Output: [ y_1,y_2,...,y_n]; y_i= [t_1,t_2,...t_n]; t_i= topo_class_hash;
                yi is constrained by sum(c_i)<= fixed amount
    """
        
    max_node_count = 50000
    sets_of_topo_classes = []
    current_set_topo_classes = []
    current_set_size = 0
    for [topo_class,size] in topo_classes_with_counts:
        if size + current_set_size <= max_node_count or (current_set_size == 0 and size >= max_node_count):
            current_set_topo_classes.append(topo_class)
            current_set_size = current_set_size + size
        else:
            sets_of_topo_classes.append(current_set_topo_classes)
            current_set_topo_classes = [topo_class]
            current_set_size = size
    if current_set_topo_classes:
        sets_of_topo_classes.append(current_set_topo_classes)
    return sets_of_topo_classes



def compute_connected_components(states_dict):
    """ input dict structure:  (top_hash_int, bottom_hash_int, red_car_end_a) : game_number
        output: [x_1,x_2,...x_n]; x_i = [y_i_1,y_i_2]; y1 = list of state keys, y2 = list of edges: [game_number, game_number]
    """
    connected_components = []
    white_states_dict = dict(states_dict)
    
    while white_states_dict:
        gray_states_dict = {}
        connected_component_state_keys = []
        connected_component_edges = []

        state_key,game_number = white_states_dict.popitem()
        gray_states_dict[state_key] = game_number

        while gray_states_dict:
            state_key,game_number = gray_states_dict.popitem()
            connected_component_state_keys.append(copy.copy(state_key))
    
            # Neighbors come in three flavors: white, gray, and black
            # We ignore black since the edge from black to current state was already recorded.
            nbr_state_keys = compute_neighbors_from_game_state_key(state_key)
    
            white_nbr_keys = [x for x in nbr_state_keys if x in white_states_dict]
            gray_nbr_keys = [x for x in nbr_state_keys if x in gray_states_dict]
    
            white_nbrs_dict = {k:white_states_dict[k] for k in white_nbr_keys}
            gray_states_dict.update(white_nbrs_dict)
            for k in white_nbr_keys:
                del white_states_dict[k]
    
            connected_component_edges.extend([ [game_number, states_dict[x] ] for x in white_nbr_keys] )
            connected_component_edges.extend([ [game_number, states_dict[x] ] for x in gray_nbr_keys] )
    
        # now we have a connected component
        connected_components.append( [copy.deepcopy(connected_component_state_keys) , copy.deepcopy(connected_component_edges) ] )
    
    return connected_components
      
        


def move_car_left(board_array,end_a):
    new_board_array = list(board_array)
    new_board_array[end_a - 1] = HORIZONTAL_CAR
    new_board_array[end_a + 1] = BLANK_SPACE
    return new_board_array

def move_car_right(board_array,end_b):
    new_board_array = list(board_array)
    new_board_array[end_b + 1] = HORIZONTAL_CAR
    new_board_array[end_b - 1] = BLANK_SPACE
    return new_board_array

def move_car_up(board_array,end_a):
    new_board_array = list(board_array)
    new_board_array[end_a - 6] = VERTICAL_CAR
    new_board_array[end_a + 6] = BLANK_SPACE
    return new_board_array

def move_car_down(board_array, end_b):
    new_board_array = list(board_array)
    new_board_array[end_b + 6] = VERTICAL_CAR
    new_board_array[end_b - 6] = BLANK_SPACE
    return new_board_array

def move_truck_left(board_array, end_a):
    new_board_array = list(board_array)
    new_board_array[end_a - 1] = HORIZONTAL_TRUCK
    new_board_array[end_a + 2] = BLANK_SPACE
    return new_board_array

def move_truck_right(board_array, end_b):
    new_board_array = list(board_array)
    new_board_array[end_b + 1] = HORIZONTAL_TRUCK
    new_board_array[end_b - 2] = BLANK_SPACE
    return new_board_array

def move_truck_up(board_array, end_a):
    new_board_array = list(board_array)
    new_board_array[end_a - 6] = VERTICAL_TRUCK
    new_board_array[end_a + 12] = BLANK_SPACE
    return new_board_array

def move_truck_down(board_array,end_b):
    new_board_array = list(board_array)
    new_board_array[end_b + 6] = VERTICAL_TRUCK
    new_board_array[end_b - 12] = BLANK_SPACE
    return new_board_array
 

# !!!! TODO - compute all edges for df of states.
# record the edges in db
def compute_all_edges_from_state_dict(state_dict):
    '''
        Expected Input: dict with key-value of form:
            (top_hash_int, bottom_hash_int, red_car_end_a) : game_number
        
        Output: List of records representing what should be recorded for state_transitions in db:
                [pre_transition_game_number, post_transition_game_number]
    '''
    
    edges = []
    while state_dict:
        state_key,game_number = state_dict.popitem()
        
        nbr_state_keys = compute_neighbors_from_game_state_key(state_key)
        
        nbr_edges = [ [game_number, state_dict[x] ] for x in nbr_state_keys]
        
        for key in nbr_state_keys:
            if key in state_dict:
                del state_dict[key]
        
        edges.extend(nbr_edges)
        
        
    return edges




def compute_neighbors_from_game_state_key( (top_hash, bottom_hash,red_car_end_a) ):
	''' Using state key: (game top hash, game bottom hash, red car position), determine 
	    all neighbors for the state defined by that given state kay. Return list of keys
		for all neighbor states.
	'''

	board_bit_string = from_two_ints_to_bit_string(top_hash,bottom_hash)
	nbrs_as_board_array = compute_neighbors_from_board_bit_string(board_bit_string,red_car_end_a)
    # [ b1,b2, .. bn] bi = [ board_as_array, red_car_end_a]
    # want: [ c1,c2, ... cn] ci = [top_hash_int, bottom_hash_int, red_car_end_a
    
	board_bit_strings = [ from_array_to_bit_string(x[0]) for x in nbrs_as_board_array]
	red_car_end_a_array = [x[1] for x in nbrs_as_board_array]
    
	hash_ints = [ [int(x[:54],2) , int(x[54:],2)] for x in board_bit_strings ]

	zipped = zip(hash_ints, red_car_end_a_array)
	# zipped: [d1,d2,...dn] di = ( [top_hash_int, bottom_hash_int], red_car_end_a)

	nbrs_as_state_keys = [ (x[0][0], x[0][1], x[1] ) for x in zipped ]
	#nbrs as state data: [ x1,x2,...xn] xi = [top_hash_int,  bottom_hash_int, red_car_end_a]

	return nbrs_as_state_keys
    
    


 
def compute_neighbors_from_df_index(df_game_states, index):
    top_int = df_game_states['game_hash_top'][index]
    bottom_int = df_game_states['game_hash_bottom'][index]
    board_bit_string = from_two_ints_to_bit_string(top_int, bottom_int)
    red_car_end_a = df_game_states['red_car_end_a'][index]
    return compute_neighbors_from_board_bit_string(board_bit_string, red_car_end_a)


def compute_neighbors_from_board_bit_string(board_bit_string, red_car_end_a):
    
    board_array = from_bit_string_to_array(board_bit_string)
    neighbors = []
    pieces = board_as_bit_string(board_bit_string)

    for piece in pieces:
        # if horizontal car not on left edge and piece to left is blank, move car left one piece
        if piece[1] == HORIZONTAL_CAR and piece[0] %6 > 0 and board_array[piece[0] - 1] == BLANK_SPACE:
            nbr_board_array = move_car_left(board_array,piece[0])
            if piece[0] == red_car_end_a:
                neighbors.append( (nbr_board_array, red_car_end_a - 1))
            else:
                neighbors.append( (nbr_board_array,red_car_end_a))
        
        # if horizontal car not on right edge and piece to right is blank, move car right one piece
        if piece[1] == HORIZONTAL_CAR and piece[0] %6 < 4 and board_array[piece[0] + 2] == BLANK_SPACE:
            nbr_board_array = move_car_right(board_array,piece[0]+1)
            if piece[0] == red_car_end_a:
                neighbors.append( (nbr_board_array, red_car_end_a + 1))
            else:
                neighbors.append( (nbr_board_array,red_car_end_a))
        
        # if vertical car not on top edge and piece above is blank, move car up
        if piece[1] == VERTICAL_CAR and piece[0] > 5 and board_array[piece[0] - 6] == BLANK_SPACE:
            neighbors.append( (move_car_up(board_array,piece[0]), red_car_end_a) )
        
        # if vertical car not on bottom edge and piece below is blank, move car down
        if piece[1] == VERTICAL_CAR and piece[0] < 24 and board_array[piece[0] + 12] == BLANK_SPACE:
            neighbors.append( (move_car_down(board_array,piece[0] + 6), red_car_end_a) )
        
        # if horizontal truck not on left edge and piece to left is blank, move truck left
        if piece[1] == HORIZONTAL_TRUCK and piece[0]%6 > 0 and board_array[piece[0]-1] == BLANK_SPACE:
            neighbors.append( (move_truck_left(board_array,piece[0]) ,red_car_end_a ) )
        
        # if horizontal truck not on right edge and piece to right is blank, move truck right
        if piece[1] == HORIZONTAL_TRUCK and piece[0]%6 < 3 and board_array[piece[0]+3] == BLANK_SPACE:
            neighbors.append( (move_truck_right(board_array,piece[0]+2), red_car_end_a) )
            
        # if vertical truck not on top edge and piece above is blank, move truck up
        if piece[1] == VERTICAL_TRUCK and piece[0] > 5 and board_array[piece[0] - 6] == BLANK_SPACE:
            neighbors.append( (move_truck_up(board_array,piece[0]), red_car_end_a) )
            
        # if vertical truck and not on bottom edge and piece below is blank, move truck down
        if piece[1] == VERTICAL_TRUCK and piece[0] < 18 and board_array[piece[0] + 18] == BLANK_SPACE:
            neighbors.append( (move_truck_down(board_array,piece[0] + 12), red_car_end_a) )
    
    return neighbors
    
    
def neighbors(state):
    top_int = state['game_hash_top']
    bottom_int = state['game_hash_bottom']
    board_bit_string = from_two_ints_to_bit_string(top_int, bottom_int)
    red_car_end_a = state['red_car_end_a']
    return compute_neighbors_from_board_bit_string(board_bit_string, red_car_end_a)



def compute_edges_from_df_of_states(states):
    white_list = states
    black_list = []
    gray_list = deque()
    
    '''need game_number, top_hash, bottom_hash to compute edges, document edges, and update states
       need to start with all final states '''
    
    solution_states = [s for s in white_list if s.is_goal_state]
    for x in solution_states:
        gray_list.append(x)
        
    while gray_list:
        state = gray_list.popleft()
        nbrs = neighbors(state)
        
        gray_nbrs = [x for x in nbrs if x in gray_list]
        for x in gray_nbrs:
            add_edge(x.game_number, state.game_number)
        
        white_nbrs = [x for x in nbrs if x in white_list]
        while white_nbrs:
            x = white_nbrs.pop()
            x.solution_depth = state.solution_depth + 1
            x.optimal_nbr = state.game_number
            x.color = 'grey' # !!!! not sure if i want to add a color attribute to the data
            add_edge(x.game_number,state.game_number)
            gray_list.append(x)
        
        black_list.append(state)
        state.color = 'black' #!!!! how to encode color? - by list name or by data attribute?
        
    # At this point all nodes connected to a solution state have been discovered. Now we have an unknown forest
    # of unsolvable games
    
    while white_list:
        grey_list = deque
        grey_list.append(white_list.pop())
        while grey_list:
            state = grey_list.pop
            nbrs = neighbors(state)
            grey_nbrs = [x for x in nbrs if x in grey_list]
            for x in grey_nbrs:
                add_edge(x.game_number,state.game_number)
                
            white_nbrs = [x for x in nbrs if x in white_list]
            while white_nbrs:
                x = white_nbrs.pop()
                add_edge(x.game_number,state.game_number)
                x.solution_depth = -1
                x.optimal_nbr = None
                x.color = 'grey'
                grey_list.append(x)
                white_list.remove(x)
                 
            state.color = 'black'
            black_list.append(state)
        
                
                
def add_edge(x_game_number, y_game_number):
    pass

        
def persist_solution_paths_for_comb_class(comb_class_id):
    conn = db.connect('C:/Users/cliff/workspace/rushHour/Data Model and SQL/Schema Definition and Bulk Load/rush_hour.db')
    cursor = conn.cursor()
    
    sql = 'select distinct connected_component_id from game_state where comb_class_id = %d' %(comb_class_id)
    cursor.execute(sql)
    component_ids = cursor.fetchall()
    for component_id in component_ids:
        solution_path_data = solution_paths_for_connected_component(component_id)
        #set_solution_data_for_connected_component(id,cursor)
        update_sql = """update game_state 
                       set optimal_transition_game_number = ?, solution_distance = ? 
                       where comb_class_id = ? and game_number = ?"""
                       
        update_data = [ (v['optimal_nbr_game_number'], v['depth'],comb_class_id, k) for k,v in solution_path_data.items() ]
        cursor.executemany(update_sql,update_data)
        conn.commit()

def solution_paths_for_connected_component(connected_component_id):
    """ returns dictionary {k,v} k=game_number from db; v={'depth': ? , 'optimal_solution_nbr': ? }
        for each node in the connected component
    """ 
    
    conn = db.connect('C:/Users/cliff/workspace/rushHour/Data Model and SQL/Schema Definition and Bulk Load/rush_hour.db')
    db_cursor = conn.cursor()
    
    
    # gather data
    sql = """ select s.comb_class_id, s.game_number, s.is_goal_state
              from connected_component c
                   inner join game_state s on c.id = s.connected_component_id
              where connected_component_id = %d
          """%(connected_component_id)
    db_cursor.execute(sql)
    component_states = db_cursor.fetchall() 
    
    sql = """select distinct t.*
             from connected_component c
                  inner join game_state s on c.id = s.connected_component_id 
                  inner join state_transition t 
                  on (s.comb_class_id = t.comb_class_id
                      and s.game_number = t.pre_transition_game_number
                     )
                      or
                     (t.comb_class_id = s.comb_class_id 
                      and s.game_number = t.post_transition_game_number 
                     )
             where c.id = %d
           """%(connected_component_id)
    
    db_cursor.execute(sql)
    component_edges = db_cursor.fetchall()
    

    # run algorithm
    adj_list = {x[1]:[] for x in component_states} # component_state = ()
    for [x,y,z]in component_edges: # [t1,t2,...tn] ti = (pre_tran_state_game_number, post_tran_state_game_number, comb_class_id):
        adj_list[x].append(y)
        adj_list[y].append(x)
        
    # component_states: (comb class id, game number, is Goal State?)
    # states as an array of dictionaries: [d1,d2,d3,...dn] di = {game_number:{'depth':,'optimal_nbr_game_number}}
    
    white_states = { x[1]:{'depth':None, 'optimal_nbr_game_number':None} for x in component_states if x[2] !=1}
    gray_states =  OrderedDict( { x[1]:{'depth':0, 'optimal_nbr_game_number':None} for x in component_states if x[2] == 1 })
    black_states = {}
    
    while gray_states:
        cur_state_key,cur_state_values = gray_states.popitem(last=False)
        for nbr in adj_list[cur_state_key]:
            if nbr in white_states:
                gray_states[nbr] = {'depth': cur_state_values['depth'] + 1, 'optimal_nbr_game_number':cur_state_key} 
                del white_states[nbr]
        black_states[cur_state_key] = cur_state_values
        
    
    distance_partition_max = max( v['depth'] for k,v in black_states.items()  )
    distance_partition = { i:[] for i in range(distance_partition_max + 1) }
    for k,v in black_states.items() :
        (distance_partition[v['depth'] ]).append(k)
    
    return black_states

    
    
    
    
    
    
    
    
    
    
    
