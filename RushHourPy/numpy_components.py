

import numpy as np
import networkx as nx
from numpy_neighbors import *



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

        while grey_states:
        
            v,red_col = grey_states.pop()

            black_states.add((v,red_col))

            nbrs = set( (state_nbrs(v,red_col))[0] )
            g.add_node((v,red_col))

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
        if 5 in [ x[1][1] for x in g.nodes()]:
            g.graph['solvable'] = True
        elif 5 in [ x[1][0] for x in g.nodes()]:
            g.graph['solvable'] = True
        else:
            g.graph['solvable'] = False
        components.append(g)

    return components


            
            