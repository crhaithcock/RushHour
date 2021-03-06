

import numpy as np
import networkx as nx 
from neighbors import *

'''

Algo:

node table has column: included_in_component.

Pluck element with included_in_component = 0

define white_states = {element}

while white_states:
    build component around this node.

    store component data

    update node table - set to 1 for all nodes in component

    Pluck element with included_in_component = 0
    
    white_states.add(element)
    
    


'''

def from_sql(comb_class):
    sql  "select * from node where included_in_component = 0 limit 1;
    
    white_states = {}


def gen_components(states):
    '''
        Input: set of states. Each element of the set is a tuple:
                s: board as int
                red_col: right most column covered by red_col

        output: yielded output of graphs one at a time via yield
        
                list of one or more networkx graphs. Each graph is a connected component of the RH Graph.

                component: a networkx graph
    '''

      
    white_states = states

    components = []

    while states:

        for white_state in states:
            break;
        
        white_states = set(white_state)
        
        while white_states:
            grey_states = set([white_states.pop()])

            black_states = set()

            edges = set()
            g = nx.Graph()
            solvable = False

            while grey_states:

                v,red_col = grey_states.pop()

                black_states.add((v,red_col))

                nbrs = set( (state_nbrs(v,red_col))[0] )
                g.add_node((v,red_col))
                g.nodes[(v,red_col)]['is_soln_state'] = 5 == red_col
                g.nodes[(v,red_col)]['board_int'] = v
                g.nodes[(v,red_col)]['red_col'] = red_col

                if red_col == 5:
                    solvable = True



                # build out the graph
                # graphs intended to be persisted
                # graph attribute: distance_partition: d_i: set of nodes
                for nbr_v,nbr_red_col in nbrs:
                    g.add_edge( (v,red_col) , (nbr_v,nbr_red_col) )

                # remove those neighbors that have been fully explored
                nbrs.difference_update(black_states)

                # add to grey_states the remaining as-yet-unfollowed neighbors
                grey_states.update(nbrs)

                # remove from white states all of the as-yet-unfollowed neighbors
                white_states.difference_update(nbrs)

            #apply some graph logic
            #if 5 in [ x[1][1] for x in g.nodes()]:
            #    g.graph['solvable'] = True
            #elif 5 in [ x[1][0] for x in g.nodes()]:
            #    g.graph['solvable'] = True
            #else:
            #    g.graph['solvable'] = False
            mapping = {x[0]:x[1] for x in zip( g.nodes(),range(len(g.nodes()))) }
            nx.relabel_nodes(g,mapping,copy=False)

        g.graph['solvable'] = solvable

        yield g

        states.difference_update(white_states)


def components(states):
    '''
        Input: iterable that can be converted to a set. Each element of the iterable:
                s: board as int
                red_col: right most column covered by red_col

        output: list of one or more networkx graphs. Each graph is a connected component of the RH Graph.

                component: a networkx graph
    '''

    white_states = set(states)

    components = []

    while white_states:

        grey_states = set([white_states.pop()])

        black_states = set()

        edges = set()
        g = nx.Graph()
        solvable = False
     
        while grey_states:
        
            v,red_col = grey_states.pop()

            black_states.add((v,red_col))

            nbrs = set( (state_nbrs(v,red_col))[0] )
            g.add_node((v,red_col))
            g.nodes[(v,red_col)]['is_soln_state'] = 5 == red_col
            g.nodes[(v,red_col)]['board_int'] = v
            g.nodes[(v,red_col)]['red_col'] = red_col
            
            if red_col == 5:
                solvable = True
  


            # build out the graph
            # graphs intended to be persisted
            # graph attribute: distance_partition: d_i: set of nodes
            for nbr_v,nbr_red_col in nbrs:
                g.add_edge( (v,red_col) , (nbr_v,nbr_red_col) )

            # remove those neighbors that have been fully explored
            nbrs.difference_update(black_states)

            # add to grey_states the remaining as-yet-unfollowed neighbors
            grey_states.update(nbrs)

            # remove from white states all of the as-yet-unfollowed neighbors
            white_states.difference_update(nbrs)

        #apply some graph logic
        #if 5 in [ x[1][1] for x in g.nodes()]:
        #    g.graph['solvable'] = True
        #elif 5 in [ x[1][0] for x in g.nodes()]:
        #    g.graph['solvable'] = True
        #else:
        #    g.graph['solvable'] = False
        mapping = {x[0]:x[1] for x in zip( g.nodes(),range(len(g.nodes()))) }
        nx.relabel_nodes(g,mapping,copy=False)

        g.graph['solvable'] = solvable

        components.append(g)

    return components


            
            