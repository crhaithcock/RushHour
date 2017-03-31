

#  A set of states has been calculated most likely using a combinatorial algorithm.
# This module contains the code to calculate the edge structure between those states.


import copy
from collections import deque
from collections import Counter
import itertools
import pdb
import math
import networkx as nx
import state




class Component(Object):
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
    def from_keys(cls, keys_dict):
        ''' Instantiate an instance of Component based on data from a
            data store rather than derive from a single state.
        '''
        pass


    @classmethod
    def from_state(cls, state):
        """ Derive the component containing the given State."""

        root = copy.deepcopy(state)
        derive_component_from_root()
        return cls(state(root))

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



        state_nodeid_map = {}
        id_gen = itertools.count(1)
        reverse_direction = {'left':'right', 'right':'left', 'up':'down', 'down':'up'}

        node_id = next(id_gen)
        state_nodeid_map[self.root] = node_id

        # Follow breadht
        self.graph.add_node(node_id, stateObj=self.root)
        self.state_node_map[self.root] = node_id
        grey_states.append(self.root)


        while grey_states:
            #pdb.set_trace()

            state = grey_states.popleft()
            #pdb.set_trace()
            node_id = state_nodeid_map[state]

            black_states.append(state)

            # maybe have State return a dict rather than list of 2-elt lists.
            nbrs = state.derive_neighbors()

            black_nbrs = [k for k in nbrs if k[0] in black_states]
            grey_nbrs = [k for k in nbrs if k[0] in grey_states]
            white_nbrs = [k for k in nbrs if k not in black_nbrs and k not in grey_nbrs]

            #pdb.set_trace()

            for nbr in grey_nbrs:

                nbr_state = nbr[0]
                nbr_direction = nbr[1]
                nbr_node_id = state_nodeid_map[nbr_state]
                self.graph.add_edge(node_id, nbr_node_id, direction=dir)
                self.graph.add_edge(nbr_node_id, node_id, direction=reverse_direction[dir])

            for [white_state, dir] in white_nbrs:

                state_nodeid_map[white_state] = next(id_gen)
                white_id = state_nodeid_map[white_state]
                self.graph.add_node(white_id, stateObj=white_state)
                self.state_node_map[white_state] = white_id

                self.graph.add_edge(node_id, white_id, direction=dir)
                self.graph.add_edge(white_id, node_id, direction=reverse_direction[dir])

                grey_states.append(white_state)

    @property
    def distance_partition(self):
        ''' TBD - docstring'''
        if self._distance_partition:
            return self._distance_partition

        graph = self.graph

        final_states = [n for n in nx.nodes_iter(G) if graph.node[n]['stateObj'].is_final_state]
        non_final_states = [n for n in graph.nodes() if n not in final_states]
        self._distance_partition = {}


        #!!!! TODO - HERE. Fix ME!!
        for state in non_final_states:

            # Note, we only find a minimal solution to one final_state.
            # There may be multiple minimal paths to more than one state.
            # Finding the one minimal path supports game play hints and determining.
            # the distance partition for the game component.
            # There is potential value in finding larger subsets of minimal paths as
            # part of a measure of difficulty.

            # For each final state f_state find a minimal path from n to f_state
            soln_paths = {f_state: [x for x in nx.shortest_path(G, state, f_state)] \
                            for f_state in final_states}

            # Across all the minimal n-f_state paths, find the shortest length
            soln_path_lengths = {f_state: len(soln_paths[f_state]) for f_state in final_states}
            shortest_soln_path_len = min([x for x in soln_path_lengths.values()])
            soln_dist = shortest_soln_path_len - 1

            # Record one of the minmial solution paths
            min_dist_f_state = [f_state for f_state in soln_path_lengths.keys() \
                    if soln_path_lengths[f_state] == shortest_soln_path_len][0]


            graph.node[n]['soln_path'] = soln_paths[min_dist_f_state]
            graph.node[n]['soln_dist'] = soln_dist
            graph.node[n]['optimal_neighbor'] = G.node[n]['soln_path'][1]


            if soln_dist in self._distance_partition:
                self._distance_partition[soln_dist].append(n)
            else:
                self._distance_partition[soln_dist] = [n]

        self._distance_partition[0] = final_states

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
        radius = 200

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
            svg = svg + '<g transform=" translate(%d,%d) scale(%f)">'%(x-x_offset, y-y_offset, scale) + self.graph.node[node]['stateObj'].svg + '</g>'

        svg = svg + '<g transform=" translate(%d,%d) scale(%f)">'%(cx-x_offset, cy-y_offset, scale) + self.graph.node[center]['stateObj'].svg + '</g>'
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

    