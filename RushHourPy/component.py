

#  A set of states has been calculated most likely using a combinatorial algorithm.
# This module contains the code to calculate the edge structure between those states.


import copy
from collections import deque
from collections import Counter
import itertools
import pdb
import math
import networkx as nx
import sqlite3


import state




class Component(object):
    ''' A component encodes the RH Graph for a single instance
        of a RH puzzle using breath first search.
        Note that each NxGraph is associated with a State object.
    '''

    def __init__(self, root=None):
        # Graph Data (nxGraph)
        self.graph = None
        self.root = root
        self.state_node_map = {} #dictionary to map states to nodes

        # RH Solution Data/Metrics
        self._distance_partition = None
        self._optimal_paths = []
        self.max_solution_length = None


        # General Graph Metrics
        if self.root is not None:
            self.derive_component_from_root()


    @classmethod
    def from_keys(cls, nodes, edges):
        pass


    def _graph_from_sqlite(self,comp_id):
        
        sql = '''select red_car_end_a, top_hash_int, bottom_hash,nx_node_id 
                 from state where component_id = {!s}'''.format(comp_id)        
        
        pass
    

    @classmethod
    def from_state(cls, state):
        """ Derive the component containing the given State."""

        comp = Component()
        comp.root = copy.deepcopy(state)
        comp.derive_component_from_root()
        return comp


    def derive_component_from_root(self):
        ''' Derive all reachable nodes from root following the rules of
            the RH puzzle using a breath first search.
            Note each node of the component graph is associated with State object.
            We create an arbitrary list of integers to use with nxGraph, and we keep a dictionary
            to map each node's integer id to that node's associated State object.
        '''
        if self.root is None:
            return

        ### new approach using NetworkX
        self.graph = nx.DiGraph()


        grey_states = deque()
        black_states = deque()



        self.state_node_map = {}
        id_gen = itertools.count(1)
        reverse_direction = {'left':'right', 'right':'left', 'up':'down', 'down':'up'}

        node_id = next(id_gen)
        self.state_node_map[self.root] = node_id

        # Follow breadht
        self.graph.add_node(node_id, stateObj=self.root)
        self.state_node_map[self.root] = node_id
        grey_states.append(self.root)


        while grey_states:
            #pdb.set_trace()

            state = grey_states.popleft()
            #pdb.set_trace()
            node_id = self.state_node_map[state]

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
                grey_node_id = self.state_node_map[grey_state]
                self.graph.add_edge(node_id, grey_node_id, direction=grey_direction)
                self.graph.add_edge(grey_node_id, node_id, direction=reverse_direction[grey_direction])
            
            for nbr in white_nbrs:
                white_state = nbr['state']
                white_direction = nbr['direction']
                white_id = next(id_gen)

                self.graph.add_node(white_id, stateObj=white_state)
                self.state_node_map[white_state] = white_id

                self.graph.add_edge(node_id, white_id, direction=white_direction)
                self.graph.add_edge(white_id, node_id, direction=reverse_direction[white_direction])

                grey_states.append(white_state)


    @property
    def distance_partition(self):
        ''' TBD - docstring - consider block model.'''

        # calc once
        if self._distance_partition == None:
            self._define_distance_partition()
            return self._distance_partition
        else:
            return self._distance_partition


    

    def _define_distance_partition(self):
        

        graph = self.graph
        distance_partition = self._distance_partition
        distance_partition = {}


        final_nodes = [n for n in graph.nodes() if graph.node[n]['stateObj'].is_final_state]
        if len(final_nodes) == 0:
            return

        # Boot strap first two partitions, then loop through the rest.
        distance_partition[0] = {}
        distance_partition[0]['nodes'] = set(final_nodes)
        
        p0_edges = graph.in_edges(final_nodes)
        p0_nbrs = set([ e[0] for e in p0_edges])

        
       

        frontier_dist = 0
        new_frontier_nodes = p0_nbrs - set(final_nodes)
        while len(new_frontier_nodes) > 0:
            distance_partition[frontier_dist+1] = {}
            distance_partition[frontier_dist+1]['nodes'] = new_frontier_nodes
            
            frontier_dist = frontier_dist + 1

            nbrs = set([ e[0] for e in graph.in_edges(new_frontier_nodes)])
            partioned_nbrs = distance_partition[frontier_dist-1]['nodes'] | distance_partition[frontier_dist]['nodes']     
            new_frontier_nodes = nbrs - partioned_nbrs

        self._distance_partition = copy.deepcopy(distance_partition)

    

                        

        
    def _set_distance_partition_nodes(self):
        # Note, we only find a minimal solution to one final_state.
        # There may be multiple minimal paths to more than one state.
        # Finding the one minimal path supports game play hints and determining.
        # the distance partition for the game component.
        # There is potential value in finding larger subsets of minimal paths as
        # part of a measure of difficulty.

        # For each non final state, build all paths to all final states.
        # From this set of many solution paths, choose one of minimal length.

        
        graph = self.graph
        self._distance_partition['nodes'] = {}

        final_nodes = [n for n in graph.nodes() if graph.node[n]['stateObj'].is_final_state]
        non_final_nodes = [n for n in graph.nodes() if n not in final_nodes]
           
            # Across all of those minimal paths, find a shortest path.
            # That shortest path defines (in part or whole):
            #             solution distance (steps to solve);
            #             optimal move neighbor (solution hint)
            #             distance partition
            #             distance graph (weighted nodes and weighted edges)

            # Across all the many solution paths starting with node, find the shortest length path
            # Extract a shortest length path
            # defines:
            #   solution_distance
            #   a mimimal solution path
        
        for node in non_final_nodes:
            
            shortest_soln_paths = {f_node: [path for path in nx.shortest_path(graph, node, f_node)] \
                            for f_node in final_nodes}
            soln_lens = {f_node:len(shortest_soln_paths[f_node]) for\
                         f_node in shortest_soln_paths.keys()}
            min_soln_len = min([soln_lens[n] for n in soln_lens])

            min_soln_path = [shortest_soln_paths[f_node] for f_node in soln_lens\
                            if soln_lens[f_node] == min_soln_len][0]

            soln_dist = min_soln_len -1 
            self.graph.node[node]['soln_dist'] = soln_dist 

            self.graph.node[node]['soln_path'] = min_soln_path
            self.graph.node[node]['soln_dist'] = soln_dist
            self.graph.node[node]['optimal_neighbor'] = graph.node[node]['soln_path'][1]


            if soln_dist in self._distance_partition['nodes']:
                self._distance_partition['nodes'][soln_dist].append(node)
            else:
                self._distance_partition[soln_dist] = [node]

        self._distance_partition[0] = final_nodes
        for f_node in final_nodes:
            self.graph.node[f_node]['soln_path'] = [f_node]
            self.graph.node[f_node]['soln_dist'] = 0
            self.graph.node[f_node]['optimal_neighbor'] = f_node

        return self._distance_partition


    def optimal_path(self, state):
        #return self._optimal_paths[s]
        """ Identify a path from a given State to a solution that
            is as short any other path to a solution.
            Note, even though there may be more than one such path,
            this method only returns one such path."""

        if not self._optimal_paths:
            return None

        if isinstance(state, state):
            return self._optimal_paths[self.state_node_map[state]][0]
        else:
            return self._optimal_paths[state][0]



    #### Display Routines


    # SVG Image of component
    # Graph Layout - what is the best generic solution?
    # HTML output?
    # SVG output?
    # Highlight solution states.
    # Highlight longest path?

    # Ancitipated Interaction UX:
    #      select a state and see the optimal path light update
    #

    def distance_partition_layout(self):
        '''TBD - complete docsctring'''
        x_delta = 50
        y_delta = 50
        pos = {}
        for i in range(len(self.distance_partition)):
            for j in range(len(self.distance_partition[i])):
                pos[self.distance_partition[i][j]] = [i * x_delta, j * y_delta]
        return pos


    def svg_neighborhood(self, center):
        '''TBD - complete docstring'''
        width = 500
        height = 500
        center_x = width / 2
        center_y = height / 2
        r = radius = 200

        # organize neighbors by direction for particular drawing outcome
        nbrs = {'left':[], 'right':[], 'up':[], 'down':[]}
        for node in nx.neighbors(self.graph, center):
            dir = self.graph[center][node]['direction']
            nbrs[dir].append(node)

        cardinal_rho = {'left':180.0, 'right':0.0, 'up':90.0, 'down':270.0}

        rho_offset = 30.0
        nbr_pos = {}

        for dir in nbrs:
            rho_base = cardinal_rho[dir]

            rng = len(nbrs[dir])
            if rng > 0:
                a_rho = rho_base + rho_offset
                b_rho = rho_base - rho_offset
                rho_delta = (b_rho - a_rho)/rng

                for i in range(rng):
                    theta = math.radians(a_rho + i * rho_delta)
                    x_pos = center_x + r * math.cos(theta)
                    y_pos = center_y + r * math.sin(theta)
                    nbr_pos[nbrs[dir][i]] = [x_pos, y_pos]

        svg = ''
        svg = svg + '<svg width="%d"'%(width)
        svg = svg + ' height="%d" xmlns="http://www.w3.org/2000/svg">'%(height)

        scale = 0.5
        x_offset = scale * self.graph.node[center]['stateObj'].svg_width / 2.0
        y_offset = scale * self.graph.node[center]['stateObj'].svg_height / 2.0

        for node in nbr_pos:
            [x_pos, y_pos] = nbr_pos[node]
            svg = svg + '<line x1="%d" y1="%d" x2="%d" y2="%d" style="stroke:black"/>'%(center_x, center_y, x_pos, y_pos)
            #svg = svg + '<g transform=" translate(%d,%d) scale(%f)">'%(x-x_offset, y-y_offset, scale) + self.graph.node[node]['stateObj'].svg + '</g>'

        #svg = svg + '<g transform=" translate(%d,%d) scale(%f)">'%(cx-x_offset, cy-y_offset, scale) + self.graph.node[center]['stateObj'].svg + '</g>'
        svg = svg + '</svg>'

        return svg


    def draw_distance_graph(self):
        """Draw using matplotlib. Draw a graph with one node for each cell and
           weighted edges for number of edges between cells."""
        pass

    def svg_distance_partition(self):
        '''TBD - docsctring'''

        num_cells = len(self.distance_partition)
        max_nodes = max([len(self.distance_partition[x]) for x in self.distance_partition])

        cell_width = 100
        cell_height = 50 * max_nodes

        svg_width = cell_width * num_cells
        svg_height = cell_height * 1.2
        center_y = svg_height / 2.0

        y_delta = float(cell_height) / float(max_nodes)
        pos = {}

        for i in self.distance_partition:
            counter = 0
            offset_rng_start = -int(len(self.distance_partition[i])/2)
            offset_rng_end = len(self.distance_partition[i]) - offset_rng_start
            offset = (offset_rng_start, offset_rng_end)

            for j in range(len(self.distance_partition[i])):

                x_pos = cell_width / 2.0 + i*cell_width
                y_pos = center_y + math.pow(-1, j) * offset[j] * y_delta

                pos[self.distance_partition[i][j]] = [x_pos, y_pos]

        #pos = self.distance_partition_layout()
        #for k in pos:
        #    pos[k][0] = pos[k][0]+ 50
        #    pos[k][1] = 500 - (pos[k][1]+ 50)

        # now build the svg
        svg = '<svg width="'+ str(svg_width)+'" height="'+str(svg_height)+'" transform="translate(50,50)" xmlns="http://www.w3.org/2000/svg">'

        for i in range(len(self.distance_partition)-1):
            for v1 in self.distance_partition[i]:
                for v2 in self.distance_partition[i+1]:
                    if v2 in self.graph[v1]:
                        svg = svg + '\n<line x1="%d" y1="%d" x2="%d" y2="%d" style="stroke:black"/>'%(pos[v1][0], pos[v1][1], pos[v2][0], pos[v2][1])

        for cell in self.distance_partition:
            for node in self.distance_partition[cell]:
                svg = svg + '\n<circle cx="%f" cy="%f" r="%f" fill="black"/>'%(pos[node][0], pos[node][1], 10)

        svg = svg + '</svg>'

        return svg

    