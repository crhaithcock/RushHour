

import numpy as np

import networkx as nx



def distance_partition(g):
    ''' 
        input: NetworkX graph g. Assumption: g is a maximal connected subgraph of RH Graph.

        output: list of sets of nodes: partition

                partition[0] = {soln_states}

                partition[i] = {states | soln_dist(states) = i , i integer g.t.e to 0}

    '''

    partition = {}


    partition[0] = set([x for x in g.nodes() if g.node[x]['is_soln_state']])

    remaining_nodes = set(g.nodes())
    remaining_nodes.difference_update(partition[0])
    i = 1

    while remaining_nodes:
        partition[i] = set()
        for x in partition[i-1]:
            nbrs = set(g.neighbors(x) )
            remaining_nodes.difference_update(nbrs)
           
            # delete from neighbors those in partition[i-2] and partition[i-1]
            nbrs.difference_update(partition[i-1])
            
            #!!! TDODO - consider ...perhaps an explicit construciton of the dist = 1 set to bootsrap the iteration makes more sense.
            if i > 1:
                nbrs.difference_update(partition[i-2])
            
            partition[i].update(nbrs)
        i=i+1

    max_partition_idx = len(partition) - 1
    for i in range(len(partition)):
        for x in partition[i]:
            g.nodes[x]['soln_distance'] = i
            g.nodes[x]['board_int'] = g.nodes[x]['board_int']
            if i > 0:
                g.nodes[x]['inner_nbrs'] = set(g[x]) & partition[i-1] 
            if i < max_partition_idx:
                 g.nodes[x]['outer_nbrs'] = set(g[x]) & partition[i+1]

    g.graph['distance_partition'] = partition



