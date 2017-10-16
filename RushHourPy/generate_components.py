


import sqlite3
import pandas as pd
import networkx as nx
#import pickle
from collections import deque
import itertools
import copy

import constants
import state


# global databse connection for reuse 
db_conn = None
db_cur = None



def generate_components(num_cars,num_trucks):

    global db_cur
    global db_conn

    comb_class_id = 2**num_cars * 3**num_trucks

    open_db(num_cars, num_trucks)

    #single db query
    #total_states_sql = "select count(*) from state where comb_class_id = {!s}".format(comb_class_id)
    
    #sharded db query
    total_states_sql = "select count(1) from state"
    total_states_res = db_cur.execute(total_states_sql).fetchone()
    total_states = total_states_res[0]
    


    unassigned_state_sql = \
        """ select red_car_end_a, game_hash_top, game_hash_bottom
            from state
            component_id is null
            limit 1
        """.format(comb_class_id)
    
    unnassigned_state = db_cur.execute(unassigned_state_sql).fetchone()

    graphed_states = 0
    component_counter = 0
    while unnassigned_state:
        [red_car_end_a, top_hash_int, bottom_hash_int] = unnassigned_state
    
        s = state.State(red_car_end_a,top_hash_int,bottom_hash_int)
        
        print("\n\nBuidling Compoment From State")
        s.print_board()

        graph = derive_component_from_state(s)
        set_soln_distances(graph)

        component_counter = component_counter + 1
        graphed_states = graphed_states + len(graph.nodes())

        print ("\n\nSaving Compoment {!s}".format(component_counter))
        print ("Total Nodes: {!s}  total nodes graphed: {!s}  nodes remaining: {!s}"\
                 .format(total_states,graphed_states,total_states - graphed_states ))
        component_to_db(comb_class_id,graph)

        unnassigned_state = db_cur.execute(unassigned_state_sql).fetchone()




def open_db(num_cars,num_trucks):
    global db_conn
    global db_cur
    
    db_name = "rush_hour_{!s}_cars_{!s}_trucks.db".format(num_cars,num_trucks)
    db_path = "./database/"+db_name
    db_conn = sqlite3.connect(db_path)
    db_conn.isolation_level = None
    db_cur = db_conn.cursor()

    print("DB Opened . . .")
    
def create_tables():
    pass

def indexes():
    pass

def close_db():
    pass

def component_to_db(comb_class_id,graph):

    

    #!!!! TODO Deeper dive on stats: distance partition data
    #   Component Stat: Max Distance
    #   State Attibute: solution neighbor


    # Graph Statistics
    num_states = len(graph.nodes())
    num_soln_states = len([v for v in graph.nodes() if graph.node[v]['stateObj'].is_final_state ])
    diameter = nx.algorithms.diameter(graph)
    min_cut_size = -1 #nlen(nx.algorithms.minimum_edge_cut(graph))
    density = nx.density(graph)
    is_solvable = 1 if num_soln_states > 0 else 0
    #topo_class = graph.node[1]['stateObj'].topo_class

    distances = [graph.node[v]['stateObj'].soln_dist for v in graph.nodes_iter()]
    distances = [x for x in distances if x is not None]
    if len(distances) == 0:
        max_distance = -1
    else:
        max_distance = max(distances)
    

    # create new component record
    sql = "select ifnull(max(id),0) from component"
    new_comp_id = db_cur.execute(sql).fetchone()[0] + 1

    sql = """ insert into component(id, comb_class_id) values ({!s},{!s}) """.format(new_comp_id,comb_class_id)

    db_cur.execute(sql)

    # create component stats 
    sql = """insert into comp_stats(component_id, num_states, num_soln_states, diameter, min_cut_size, density,is_solvable) 
            values ({!s}, {!s}, {!s}, {!s}, {!s}, {!s},{!s} )
            """.format(new_comp_id, num_states, num_soln_states,diameter, min_cut_size, density,is_solvable)
    db_cur.execute(sql)


    # save graph edge structure
    sql = " insert into comp_edges (component_id,source_node_id,target_node_id,direction) values(?,?,?,?) "
    params =[ [new_comp_id, e[0],e[1], graph[e[0]][e[1]]['direction'] ] for e in  graph.edges_iter() ]
    db_cur.execute("begin")
    db_cur.executemany(sql,params)
    db_cur.execute("commit")


    # update all of the associated states:

    sql = """update state set component_id = ?, node_id = ?, soln_dist = ? \
            where red_car_end_a = ? and
                    game_hash_top = ? and
                    game_hash_bottom = ?
            """

    params = [ [new_comp_id,v,graph.node[v]['stateObj'].soln_dist] + list(graph.node[v]['stateObj'].key())  for v in graph.nodes_iter()]
    #comb_class_list = [comb_class_id] * num_states

    db_cur.execute("begin")
    db_cur.executemany(sql,params)
    db_cur.execute("commit")


def set_soln_distances(graph):
    
    nodes = deque()


    nodes.extend( [n for n in graph.nodes_iter() if graph.node[n]['stateObj'].soln_dist == 0])
    while nodes:
    
        n = nodes.popleft()
        n_dist = graph.node[n]['stateObj'].soln_dist
    
        for x in graph.neighbors(n):
            
            if graph.node[x]['stateObj'].soln_dist is None:
                graph.node[x]['stateObj'].soln_dist = n_dist + 1
                nodes.append(x)
    


def derive_component_from_state(root):
    
    graph = nx.DiGraph()

    grey_states = deque()
    black_states = deque()



    state_node_map = {}
    id_gen = itertools.count(1)
    reverse_direction = {'left':'right', 'right':'left', 'up':'down', 'down':'up'}

    node_id = next(id_gen)
    state_node_map[root] = node_id

    # Follow breadht
    graph.add_node(node_id, stateObj=root)
    state_node_map[root] = node_id
    grey_states.append(root)



    while grey_states:
        #pdb.set_trace()

        state = grey_states.popleft()
        #pdb.set_trace()
        node_id = state_node_map[state]

        black_states.append(state)

        # maybe have State return a dict rather than list of 2-elt lists.
        nbrs = state.derive_neighbors()

        black_nbrs = [k for k in nbrs if k['state'] in black_states]
        grey_nbrs = [k for k in nbrs if k['state'] in grey_states]
        white_nbrs = [k for k in nbrs if k not in black_nbrs and k not in grey_nbrs]

        #pdb.set_trace()

        for nbr in grey_nbrs:

            grey_state = nbr['state']
            grey_direction = nbr['direction']
            grey_node_id = state_node_map[grey_state]
            graph.add_edge(node_id, grey_node_id, direction=grey_direction)
            graph.add_edge(grey_node_id, node_id, direction=reverse_direction[grey_direction])
        
        for nbr in white_nbrs:
            white_state = nbr['state']
            white_direction = nbr['direction']
            white_id = next(id_gen)

            graph.add_node(white_id, stateObj=white_state)
            state_node_map[white_state] = white_id

            graph.add_edge(node_id, white_id, direction=white_direction)
            graph.add_edge(white_id, node_id, direction=reverse_direction[white_direction])

            grey_states.append(white_state)


    return graph


        
