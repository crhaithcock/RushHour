# -*- coding: utf-8 -*-
"""
Created on Sun Jun 23 00:48:24 2019

@author: CHaithcock
"""


import networkx as nx
import svgwrite
import numpy as np

import RHState
import RHConstants

#import RHConstants

class RHComponent():
    
    def __init__(self):
        self.nxGraph = None
        self._distance_partition = None
        self._init_svg_complete = None
        self._svg_nbhd_nbr_centers = None
        self._svg_nbhd_edges = None
        
    
    def _setGraph(self,graph):
        self.nxGraph = graph
        
        
    @classmethod
    def from_state(cls,state):
        """ input well-defined state for RH Graph.
            Output: a new instance of RHComponent 
            with self.nxGraph initialized to the component
            containing the input state
        """
    
        '''
            Input: iterable that can be converted to a set. Each element of the iterable:
                    s: board as int
                    red_col: right most column covered by red_col
    
            output: list of one or more networkx graphs. Each graph is a connected component of the RH Graph.
    
                    component: a networkx graph
        '''

        #if not isinstance(state,RHState.RHState):
        #    raise Exception ("Must have single instance of RHState to build a component")
        
        g = nx.Graph()
        g.graph['solvable'] = False
        # Following CLRS BFS Algirithm
        # The input state is initial (and all as-yet undiscovered) nodes
        # are marked white
        # The initial state is popped off white states, set to grey,
        # and then the algorith is rolling to get to all states reacahble
        # from the nput state
        
        
        grey_states = set()
        grey_states.add(state)
        black_states = set()
        
        while grey_states:
        
            cur_state = grey_states.pop()

            black_states.add(cur_state) 
            g.add_node( cur_state )
            if cur_state.isSolnState():
                g.graph['solvable'] = True
                
            nbrs = cur_state.neighbors_all()
            
            # remove those neighbors that have been fully explored
            nbrs.difference_update(black_states)
            
            for nbr_state in nbrs:
               g.add_edge( cur_state, nbr_state) # also adds node to graph
               if nbr_state.isSolnState():
                   g.graph['solvable'] = True
            
            
            # add to grey_states the remaining as-yet-unfollowed neighbors
            grey_states.update(nbrs)


        # create instane and set graph 
        c = cls()
        c._setGraph(g)
        return c
    
    
    
    @classmethod
    def from_state_list(cls,states):
        """
            input: list of states with states being of expected structure
            state can be a triple (top int, bottom int, red_car_end_a)
            state can be an 2-tuple (NdArray, red_car_end_a)
            
            output: list of instances of RHComponent
        """
        ret = list()
        
        white_states = set(states)
        
        while white_states:
            g = nx.Graph()
            g.graph['solvable'] = False
            grey_states = set()
            grey_states.add(white_states.pop())
            black_states = set()
            while grey_states:
                cur_state = grey_states.pop()
                black_states.add(cur_state)
                if cur_state.isSolnState():
                    g.graph['solvable'] = True
                    
                nbrs = cur_state.neighbors_all()
                
                #remove nbrs from white_states
                white_states.difference_update(nbrs)
                
                #remove those neighbors that have been fully explored
                nbrs.difference_update(black_states)
                
                for nbr_state in nbrs:
                    g.add_edge( cur_state, nbr_state) # also adds node to graph
                    if nbr_state.isSolnState():
                        g.graph['solvable'] = True
                
                # add to grey_states the remaining as-yet-unfollowed neighbors
                grey_states.update(nbrs)
                
            # empty grey_states means we have constructed a component
            c = cls()
            c._setGraph(g)
            ret.append(c)
        
        return(ret)

    

    
    
#     ####################################################
#         
#        Data  Routines
#   
#       Input/Output/Data Conversion
#       
#       e.g. 
#        
#    #####################################################
    
    def get_nxGraph(self):
        return self.nxGraph
    
        
    def repr_state(self):
        """ Provide the deterministic unique representative state
        for this component of the RHGraph
        
        Use the lowest integer
        """
        pass
    
#     ####################################################
#         
#        Graph Analysis Routines
#   
#       e.g. Distance Partition and associated metrics
#       
#       
#        
#    #####################################################
    
    def distance_partition(self):
        if self._distance_partition:
            return self._distance_partition
        
        partition = {}
        g = self.nxGraph
        
        # states with red car as exit position define the solution state 
        partition[0] = set([x for x in g.nodes() if x.isSolnState])
        partition[1] = set()
        
        for x in partition[0]:
            partition[1].update(g.neighbors(x))
        partition[1].difference_update(partition[0])
        
        remaining_nodes = set(g.nodes())
        remaining_nodes.difference_update(partition[0])
        remaining_nodes.difference_update(partition[1])
      
        # calculate members of partition[i] by looking
        # at neighbors to nodes in partition[i-1]
        i = 2
        while remaining_nodes:
            partition[i] = set()
            for x in partition[i-1]:
                partition[i].update(set(g.neighbors(x)))
           
            partition[i].difference_update(partition[i-1])
            partition[i].difference_update(partition[i-2])
            
            remaining_nodes.difference_update(partition[i])
    
            i=i+1
            
        # set depth attribute for each node
        for depth in partition.keys():
            for node in partition[depth]:
                self.nxGraph.nodes[node]['soln_depth'] = depth
                

        self._distance_partition = partition
        return self._distance_partition
    
    
    
    def optimal_neighbor(self,state):
        pass
    
    #    if _optimal_neighbors:
    #        g.node
        


#     ####################################################
#         
#        Display Routines
#   
#           State Neighborhood
#           Distance Partition (spiral?)        
#       
#       
#        
#    #####################################################
    
    def _init_svg_nbhd_centers(self):

        if self._svg_nbhd_nbr_centers:
            return  #already been calculated. No need to repeat calcs.
     
        
        centers = {}
         
        # choose random state to ascertain svg edge structure
        s = list(self.nxGraph.nodes())[0]

        pieces = s.svg_pieces()
        vcar = RHConstants.VERTICAL_CAR
        vtruck = RHConstants.VERTICAL_TRUCK
        hcar = RHConstants.HORIZONTAL_CAR
        htruck = RHConstants.HORIZONTAL_TRUCK
        
        vert_pieces = [x for x in pieces if x['orientation'] in [vcar,vtruck]]
        horz_pieces = [x for x in pieces if x['orientation'] in [hcar,htruck]]
        
        nbhd_r = self._svg_nbhd_radius
        
     
        max_vert_nbrs = len(vert_pieces)
        max_horz_nbrs = len(horz_pieces)
        max_nbrs = max_vert_nbrs + max_horz_nbrs
        
        if max_vert_nbrs != 0:
        
            # cenetring nodes requires different math depending upon whether
            # even or odd number of neighbors to distribute across image
            if max_vert_nbrs % 2 != 0:
                offset = (max_vert_nbrs- 1) / 2.0
            else:
                offset = max_vert_nbrs / 2.0 -.5
            
            # place holder list for each neighbor
            thetas_up = np.array(np.arange(max_vert_nbrs)) - offset
        
            # arc span the neighboars are to be distributed across
            thetas_up_arc = .8 * ( ( (max_vert_nbrs/max_nbrs) * np.pi ) )
            
            #spacing between each neighbor in the imaage
            thetas_up_delta = thetas_up_arc / max_vert_nbrs
        
            #replacing values in place holder array with the angle for that
            #particular neighbor
            thetas_up = thetas_up * thetas_up_delta + np.pi/2
        
            # convert array of angles into array of x,y coordinates
            up_x = nbhd_r * np.cos(thetas_up) 
            up_y = nbhd_r * np.sin(thetas_up)  
            up_centers = np.array(list(zip(up_x,up_y)))
            
            # reflect across x-axis to set bottom neighbor x,y coordinates
            down_x = up_x
            down_y = up_y * -1
            down_centers = np.array(list(zip(down_x,down_y)))
    
            #cycle through vertical pieces to create dictionary
            # self._svg_nbr_centers['color-dir'] = [x,y]
            
            sorted_verts = sorted(vert_pieces, key=lambda x:x['end_a_col'] * 6 + x['end_a_row'])
            for i in range(len(up_centers)):
                color_up = sorted_verts[i]['color'] + '-up'
                color_down = sorted_verts[i]['color'] + '-down'
                
                centers[color_up] = up_centers[i]
                centers[color_down] = down_centers[i]
                
                
            
        if max_horz_nbrs != 0:
            
            # if verts is odd
            if max_horz_nbrs % 2 != 0:
                offset = (max_horz_nbrs- 1) / 2.0
            else:
                offset = max_horz_nbrs / 2 -.5
            
            thetas_left = np.array(np.arange(max_horz_nbrs)) - offset
        
            thetas_left_arc = .8 * ( ( (max_horz_nbrs/max_nbrs) * np.pi ) )
            thetas_left_delta = thetas_left_arc / max_horz_nbrs
        
            thetas_left = thetas_left * thetas_left_delta + np.pi
        
            left_x = nbhd_r * np.cos(thetas_left) 
            left_y = nbhd_r * np.sin(thetas_left)  
            left_centers = np.array(list(zip(left_x,left_y)))
        
            right_x = left_x * -1
            right_y = left_y
            right_centers = np.array(list(zip(right_x,right_y)))
        
            sorted_verts = sorted(horz_pieces, key=lambda x:x['end_a_row'] * 6 + x['end_a_col'])
            for i in range(len(right_centers)):
                color_left = sorted_verts[i]['color'] + '-left'
                color_right = sorted_verts[i]['color'] + '-right'
                
                centers[color_left] = left_centers[i]
                centers[color_right] = right_centers[i]
                
        
        self._svg_nbhd_nbr_centers = centers
    
        
    def _init_svg_nbhd_edges(self):
        if self._svg_nbhd_edges:
            return # no need to recalc edges
      
        edges = {}
        
        for key in self._svg_nbhd_nbr_centers.keys():
            color = key[:key.find('_')]
            [x,y] = self._svg_nbhd_nbr_centers[key]
            edges[key] = '<line x1="0" y1="0" x2="%f" y2="%f" stroke="%s" />'%(x,y,color)
              
        
    def _init_svg(self):
        '''
            * Set global drawing parameters such as width and height.
            * Set fixed positions for centers of neighbors.
            * Create a dictionary of edges drawings to be used as a data source
              drawing a particular svg neighborhood.
              
              
            
        '''
        if self._init_svg_complete:
            return
        
        img_width = 600
        img_height = 400
        
        
        self._svg_nbhd_img_width = img_width
        self._svg_nbhd_img_height = img_height
        self._svg_nbhd_radius = 150
        self._svg_nbhd_center_x = img_width / 2.0
        self._sbg_nbhc_center_y = img_width / 2.0
           
        self._init_svg_nbhd_centers()
        self._init_svg_nbhd_edges() 
      
        
        self._init_svg_complete = True
    
    
        
    def _svg_base(self):
        if self._svg_base_dwg:
            return self._svg_base_dwg
        
        self._init_svg()
        
       
        dwg = svgwrite.Drawing('nosave.svg',(self._svg_nbhd_width,self._svg_nbhd_height),debug=True)

        
        
        dwg.add(dwg.rect(insert=(0,0),size=(self._svg_nbhd_width,self._svg_nbhd_height),\
                         fill='#'+RHConstants.BLANK_COLOR_RGB))
        
        
        
        for x in range(7):
            dwg.add(dwg.line((30*x,0),(30*x,180),stroke='black',stroke_width=2))
            dwg.add(dwg.line((0,30*x),(180,30*x),stroke='black',stroke_width=2))
        return dwg
    
    
    def svg_neighborhood(self,state):
        ''' 
          return string with svg code to render.
          
        Draw SVG with RHState state in center and neighbors spread around
        '''
        
        '''
            Assume scale of 1 for single board on screen
            With a fixed buffer around it
            
            Then scale each board by 1/n where n boards are in the neighborhood.
            
            Draw lines from center of car to center of car using same color.
            Maybe combine CSS tags and id?
            
            
            <svg width="100%" height="100%" viewBox="-100 -100 200 200" version="1.1"
                    xmlns="http://www.w3.org/2000/svg"
                    xmlns:xlink="http://www.w3.org/1999/xlink">
                <circle cx="-50" cy="-50" r="30" style="fill:red" />
                <image x="10" y="20" width="80" height="80" xlink:href="recursion.svg" />
            </svg>



        Algorithm:
            see jupyter notebook for insights into nesting SVGs
            
            common_scale = 1/ (len(nbrs)+1)
            
            placement_data:
                top_left_x 
                top_left_y
                scale
                
            line_data:
                nbr_x
                nbr_y
                center_x
                center_y
                color
    
                
            


        '''
        
        center = state
        nbrs = self.nxGraph.neighbors(center)
        
        
        
        
        
        
        
        
    
    
    def svg_component(self):
        pass
    
    
    
    