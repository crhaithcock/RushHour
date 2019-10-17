# -*- coding: utf-8 -*-
"""
Created on Sun Jun 23 01:22:56 2019

@author: CHaithcock
"""

import numpy as np
import svgwrite

import RHConstants


class RHState():
    
    def __init__(self,board,red_car_end_a):
        """
            Input (Option 1):
                board: ndArray of dypte int and size 36 
                red_car_end_a: left most position of red car must
                               must be between 12 and 16 inclusive
        
            Input (option 2):
                board: integeger representing the hash of the board
                red_car_end_a: left most position of red car must
                               must be between 12 and 16 inclusive
            
        """    
       
        
        
        #!!!!TODO - consider adding validation of board
        if isinstance(board,np.ndarray):
            if board.size  == 36:
                if board.dtype == int:
                    self._board = np.copy(board.reshape(6,6))
                else:
                    raise Exception("RH Board numpy ndarray must have dtype int")
            else:
                raise Exception("Numpy array for board must consist of 36 elements")
                
        elif isinstance(board,int):
            self._board = self._int_to_board(board)
        else:
            raise TypeError('Board Must be an Integer or an ndArray')
        
        if not (12 <= red_car_end_a <= 16):
            raise ValueError("Red Car End A must be between 12 and 16 inclusive",red_car_end_a)
        else:
            self._red_car_end_a = red_car_end_a 
            
        
        self._pieces = None
        self._init_svg()
        self._svg_pieces = None

            

    def __eq__(self,other):
        if  not isinstance(other, RHState):
            return NotImplemented
        
        if  self._board_as_int()== other._board_as_int():
            if self._red_car_end_a == other._red_car_end_a:
                return True
        
        return False
    
    def __lt__(self,other):
        if  not isinstance(other, RHState):
            return NotImplemented
        
        if self._board_as_int < other.board_as_int:
            return True

        if self._board_as_int > other.board_as_int:
            return False
        
        # if _board_as_int is same in both instances,
        # compoare red_car_end_a
        if self._red_car_end_a < other.red_car_end_a:
            return True
        
        return False
    
        
    def __hash__(self):  
        return hash ( (self._board_as_int(),self._red_car_end_a) )
    

    
#     ####################################################
#         
#        Data  Routines
#   
#       Input/Output/Data Conversion
#       
#        
#    #####################################################

        
   
    def _board_as_bitstrings(self):
        vec_bin_repr = np.vectorize(lambda x: np.binary_repr(x,width=3))
        t = vec_bin_repr(self._board)
        return t


    def _board_as_int(self):
        vec_bin_repr = np.vectorize(lambda x: np.binary_repr(x,width=3))
        
        t = vec_bin_repr(self._board)
        return int(''.join(np.apply_along_axis(lambda x: ''.join(x), 1,t)),2)
    
    def _int_to_board(self,i):
        #i = '154444257952488798331863040'
        s = bin(int(i))[2:].zfill(108)
        v = np.array([int(s[i:i+3],2) for i in range(0,len(s),3)],dtype=int)
        return v.reshape((6,6))

    def board(self):
        return self._board

    def _red_car_cols(self):
        red_car_a_col = self._red_car_end_a % 6
        return ( (red_car_a_col, red_car_a_col + 1 ) )
                
    def as_array(self): 
        return( (self._board,self._red_car_end_a) )
        pass
    
    def as_int(self):
        return ( (self._board_as_int,self._red_car_end_a) )
        pass
    
    def get_board_as2ints(self):
        
        #return ( (self._board_as_int,self._red_car_end_a) )
        pass
    
    
    
    
    def _vehicles_by_order(self):
        pass
    
   
    def _get_pieces(self):
        if self._pieces is not None:
            return self._pieces
        
        
        discovered = np.array([False]*36).reshape(6,6)
    
        self._pieces = []
        
                                                              
        for row in range(6):
            for col in range(6):
                if not discovered[row,col] and self._board[row,col] != RHConstants.BLANK_SPACE:
    
                    piece = {}
                    piece['orientation'] = self._board[row,col]
                    piece['end_a_row'] = row
                    piece['end_a_col'] = col
                    discovered[row,col] = True
                    
                    if self._board[row,col] == RHConstants.VERTICAL_CAR:
                        discovered[row:row+2,col] = True
                        
                    
                    elif self._board[row,col] == RHConstants.VERTICAL_TRUCK:
                        discovered[row:row+3,col] = True
                    
                    elif self._board[row,col] == RHConstants.HORIZONTAL_CAR:
                        discovered[row,col:col+2] = True
                    
                    elif self._board[row,col] == RHConstants.HORIZONTAL_TRUCK:
                        discovered[row,col:col+3] = True
                        
                    self._pieces.append(piece)
        
        return self._pieces
                                             
                
        
    def _vehicles_by_type(self):
        ''' Create a list of indices capturing where vertical cars are
            
            return dict of vehicles: 
                vcars:   [ [ [x1,y1], [x2,y2] ] , ..., [ [xn,yn] , [xn',yn'] ] ]
                vtrucks: [ [ [x1,y1],[x2,y2],[x3,y3] ] ... ]
                hcars:
                htrucks:
                    
            Will walk through self._board and track:
                current location in board
                current
        '''
        
        discovered = np.array([False] * 36).reshape(6,6)
        ret = {'vcars':[], 'hcars':[], 'vtrucks':[],'htrucks':[]}
        
        
        # discover verticals by column major order
        # !!!! TODO - create a dictionary each car/truck
        # each entry in ret is a list of dictionaries
        '''
            each inner dict keys (svg_rect_args:           
            a_row
            a_col
            color
            symbol
            
            ? change loop order to loop through columns then move to next row:
                for r in range(6):
                    for c in range(6)
                        if self.board[r,c] == RHConstants.VERTICAL_CAR:
                            
                    
        '''
        for c in range(6):
            for r in range(6):
                if self._board[r,c] == RHConstants.VERTICAL_CAR:
                    if discovered[r,c] == False:
                        ret['vcars'].append([[r,c],[r+1,c]])
                        discovered[r:r+2,c] = True
                if self._board[r,c] == RHConstants.VERTICAL_TRUCK:
                    if discovered[r,c] == False:
                        ret['vtrucks'].append([[r,c],[r+1,c],[r+2,c]])
                        discovered[r:r+3,c] = True
                        
        for r in range(6):
            for c in range(6):
                 if self._board[r,c] == RHConstants.HORIZONTAL_CAR:
                     if discovered[r,c] ==  False:
                         ret['hcars'].append( [[r,c],[r,c+1]])
                         discovered[r,c:c+2] = True
                 if self._board[r,c] == RHConstants.HORIZONTAL_TRUCK:
                     if discovered[r,c] == False:
                         ret['htrucks'].append([[r,c],[r,c+1],[r,c+2]])
                         discovered[r,c:c+3] = True
        return(ret)
        
        



#     ####################################################
#         
#        Game PLay Routines       
#
#    #####################################################


    def isSolnState(self):
        return self._red_car_end_a == 16
    

#!!!!TODO - add error handling for bad inputs
    def neighbor(self,end_a,direction):
        
        nbr_board = np.copy(self.board)
        
        # !!!! Data Validation
        
        if direction == 'up':
            nbr_board[end_a-6] = self.board[end_a]
            if self.board[end_a] == RHConstants.VERTICAL_CAR:
                nbr_board[end_a + 6] = RHConstants.BLANK_SPACE
            else:
                nbr_board[end_a+12] = RHConstants.BLANK_SPACE
                
        elif direction == 'down':
            nbr_board[end_a] = RHConstants.BLANK_SPACE
            if self.board[end_a] == RHConstants.VERTICAL_CAR:
                nbr_board[end_a+12] = RHConstants.VERTICAL_CAR
            else:
                nbr_board[end_a+18] = RHConstants.VERTICAL_CAR

        elif direction == 'left':
            nbr_board[end_a-1] = self.board[end_a]
            if self.board[end_a] == RHConstants.HORIZONTAL_CAR:
                nbr_board[end_a+1] = RHConstants.BLANK_SPACE
                if self._red_car_end_a == end_a:
                    red_car_end_a = self.red_car_end_a - 1
            else:
                nbr_board[end_a+2] = RHConstants.BLANK_SPACE
                
        elif direction == 'right':
            nbr_board[end_a] = RHConstants.BLANK_SPACE
            if self.board[end_a] == RHConstants.HORIZONTAL_CAR:
                nbr_board[end_a+2] = RHConstants.HORIZONTAL_CAR
                if self._red_car_end_a == end_a:
                    red_car_end_a = self.red_car_end_a + 1
                else:
                    nbr_board[end_a + 2] = RHConstants.VERTICAL_TRUCK
        
        return RHState(nbr_board,red_car_end_a)
                

    def neighbors_all(self):
        d = self.neighbors_down()
        u = self.neighbors_up()
        l = self.neighbors_left()
        r = self.neighbors_right()
        
        
        return d.union(u).union(l).union(r)
        

    def neighbors_up(self):
        
        ret = set()   
        mv_x = -self._board + np.roll(self._board,-1,0)
        #set bottom most column to zeros. Only want matches against legit up moves
        mv_x[5,:] = 0


        mv_car = np.where(mv_x==RHConstants.VERTICAL_CAR)
        mv_truck = np.where(mv_x ==RHConstants.VERTICAL_TRUCK)
    
        mv_up_car = list(zip(mv_car[0],mv_car[1]))
        mv_up_truck = list(zip(mv_truck[0], mv_truck[1]))
 
 
    
        for x,y in mv_up_car:
            nbr_board = np.copy(self._board)
            nbr_board[x,y] = RHConstants.VERTICAL_CAR
            nbr_board[x+2,y] = RHConstants.BLANK_SPACE
            
            ret.add( RHState(nbr_board,self._red_car_end_a ) )
    
        for x,y in mv_up_truck:
            nbr_board = np.copy(self._board)
            nbr_board[x,y] = RHConstants.VERTICAL_TRUCK
            nbr_board[x+3,y] = RHConstants.BLANK_SPACE
            ret.add( RHState(nbr_board,self._red_car_end_a) )
    

       
        return(ret)
    
    def neighbors_down(self):
        
        ret = set()   
        mv_x = -self._board + np.roll(self._board,1,0)
        #set bottom most column to zeros. Only want matches against legit up moves
        mv_x[0,:] = 0


        mv_car = np.where(mv_x==RHConstants.VERTICAL_CAR)
        mv_truck = np.where(mv_x ==RHConstants.VERTICAL_TRUCK)
    
        mv_up_car = list(zip(mv_car[0],mv_car[1]))
        mv_up_truck = list(zip(mv_truck[0], mv_truck[1]))
 

        for x,y in mv_up_car:
            nbr_board = np.copy(self._board)
            nbr_board[x,y] = RHConstants.VERTICAL_CAR
            nbr_board[x-2,y] = RHConstants.BLANK_SPACE
            
            ret.add( RHState(nbr_board,self._red_car_end_a ) )
    
        for x,y in mv_up_truck:
            nbr_board = np.copy(self._board)
            nbr_board[x,y] = RHConstants.VERTICAL_TRUCK
            nbr_board[x-3,y] = RHConstants.BLANK_SPACE
            ret.add( RHState(nbr_board,self._red_car_end_a) )
    

       
        return(ret)
 


    def neighbors_left(self):
                
        ret = set()
        
        mv_x = -self._board + np.roll(self._board,-1,1)
        # set right most column to all zeros to eliminate non-legit left move matches.
        mv_x[:,5] = 0
        #mv_x = mv_x[:,:5]
    
        mv_car = np.where(mv_x==RHConstants.HORIZONTAL_CAR)
        mv_truck = np.where(mv_x ==RHConstants.HORIZONTAL_TRUCK)
    
        mv_left_car = list(zip(mv_car[0],mv_car[1]))
        mv_left_truck = list(zip(mv_truck[0], mv_truck[1]))
    
        for x,y in mv_left_car:
            nbr_board = np.copy(self._board)
            nbr_board[x,y] = RHConstants.HORIZONTAL_CAR
            nbr_board[x,y+2] = RHConstants.BLANK_SPACE
            
            # Test if red car is moving left
            # Note, y+1, y+2 must be a horizontal car
            # so, either y+1 and y+2 are the red cols or 
            # neither is a a red col
            # if have moved the red car, then y is on the left side of the car
            # and red_car_end_a = y
            if x == 2 and y+1 in self._red_car_cols():
                red_car_end_a = self._red_car_end_a - 1
            else:
                red_car_end_a = self._red_car_end_a
                
            ret.add( RHState(nbr_board,red_car_end_a ) )
    
        for x,y in mv_left_truck:
            nbr_board = np.copy(self._board)
            nbr_board[x,y] = RHConstants.HORIZONTAL_TRUCK
            nbr_board[x,y+3] = RHConstants.BLANK_SPACE
            ret.add( RHState(nbr_board,self._red_car_end_a) )
    
        return(ret)
    

    def neighbors_right(self):
        """ 
        Create a list of all neighbor states to self that are reached by
        moving a car or truck right.
        
        Depends on Constants being properly spaced per notes in constants file.
        
        Uses Numpy Roll to effectively move all pieces to the right one place
        and then evaluates which results to determine wihch moves were 
        legitimate per Rush Hour puzzle rules.
        
        """
        ret = set()
        
        mv_x = -self._board + np.roll(self._board,1,1)
        #set left most column to zeros. Only want matches against legit right moves
        mv_x[:,0] = 0


        mv_car = np.where(mv_x==RHConstants.HORIZONTAL_CAR)
        mv_truck = np.where(mv_x ==RHConstants.HORIZONTAL_TRUCK)
    
        mv_right_car = list(zip(mv_car[0],mv_car[1]))
        mv_right_truck = list(zip(mv_truck[0], mv_truck[1]))
    
        for x,y in mv_right_car:
            nbr_board = np.copy(self._board)
            nbr_board[x,y] = RHConstants.HORIZONTAL_CAR
            nbr_board[x,y-2] = RHConstants.BLANK_SPACE
            
            # Test if red car is moving left
            # Note, y+1, y+2 must be a horizontal car
            # so, either y-2 and y-1 are the red cols or 
            # neither is a a red col
            # if have moved the red car, then y is on the right side of the car
            # and red_car_end_a = y
            if x == 2 and y-2 in self._red_car_cols():
                red_car_end_a = self._red_car_end_a + 1
            else:
                red_car_end_a = self._red_car_end_a
                
            ret.add( RHState(nbr_board,red_car_end_a ) )
            
        # y is on the right side of the truck    
        for x,y in mv_right_truck:
            nbr_board = np.copy(self._board)
            nbr_board[x,y] = RHConstants.HORIZONTAL_TRUCK
            nbr_board[x,y-3] = RHConstants.BLANK_SPACE
            ret.add( RHState(nbr_board,self._red_car_end_a) )
    
        return(ret)


        
    
#     ####################################################
#         
#        Display Routines       
#
#    #####################################################


    ###################################
    #
    #   HTML Table Logic
    #
    ###################################
    
    def HTMLTable(self, order = 'GamePlay'):
        """
            Return well-fomed HTML Table markup to represent the board
          
            valid order options:
                    - generative - displays for easily walking state generation algorithm
                    Color coding scheme of cars/trucks is different 
                    
                    - Color coding aligns with game play.
                      All states within one component will have consisten coloring
                      scheme.
                
        """
        
        html_colors = np.array([RHConstants.BLANK_COLOR_RGB] *36).reshape(6,6)
        html_symbols = np.array([' ']*36).reshape(6,6)
        
        
        # Keep track of which color/symbol will be painted next
        car_index = 0
        truck_index = 0
        
        v = self._vehicles()
        hcars = v['hcars']
        vcars = v['vcars']
        htrucks = v['htrucks']
        vtrucks = v['vtrucks']
        
        
        for car in hcars:
            for r,c in car:
                if r == 2 and c in self._red_car_cols():
                    html_colors[r,c] = RHConstants.RED_COLOR_RGB
                    html_symbols[r,c] = RHConstants.RED_SYMBOL  
                else:
                    html_colors[r,c] = RHConstants.CAR_COLORS_RGB[car_index]
                    html_symbols[r,c] = RHConstants.CAR_SYMBOLS[car_index]
            car_index +=1         
    
        for car in vcars:
            for r,c in car:
                html_colors[r,c] = RHConstants.CAR_COLORS_RGB[car_index]
                html_symbols[r,c] = RHConstants.CAR_SYMBOLS[car_index]
            car_index +=1
        
        
        for truck in htrucks:
            for r,c in truck:
                
                html_colors[r,c] = RHConstants.TRUCK_COLORS_RGB[truck_index]
                html_symbols[r,c] = RHConstants.TRUCK_SYMBOLS[truck_index]
            truck_index +=1
                

        for truck in vtrucks:
            for r,c in truck:
                html_colors[r,c] = RHConstants.TRUCK_COLORS_RGB[truck_index]
                html_symbols[r,c] = RHConstants.TRUCK_SYMBOLS[truck_index]
            truck_index +=1
                
        # !!!! TODO - craft text of html table
        
        
        
        html = '<table>'
        for r in range(6):
            html = html + '<tr>'
            for c in range(6):
                html = html + '<td bgcolor = "' + html_colors[r,c] + '" '
                html = html + ' style="width:30px; height:30px; vertical-align:middle; text-align:center">'
                html = html + html_symbols[r,c]
                html = html + '</td>'
                # ['<td bgcolor="%s" style="width:30px; height:30px; vertical-align:middle; text-align:center">%s</td>' 

            html = html + '</tr>'
        
        html = html + '</table>'
        return(html)
     
        
        ##############################
        #
        #  SVG Display Logic
        #
        ##############################
        
    def _init_svg(self):
        self._svg_dwg = None
        self._svg_space_size = 30
        self._svg_board_size = 6 * self._svg_space_size
        self._svg_border = 3 
        self._svg_round_radius = 5

        self._svg_size = {}
        self._svg_size[RHConstants.HORIZONTAL_CAR] = \
                (2*self._svg_space_size - 2*self._svg_border , \
                 self._svg_space_size - 2*self._svg_border)
        
        self._svg_size[RHConstants.VERTICAL_CAR] = \
                (self._svg_space_size - 2*self._svg_border, \
                 2*self._svg_space_size - 2*self._svg_border)
        
        self._svg_size[RHConstants.VERTICAL_TRUCK] = \
                (self._svg_space_size - 2*self._svg_border, \
                 3*self._svg_space_size - 2*self._svg_border)
        
        self._svg_size[RHConstants.HORIZONTAL_TRUCK] = \
                (3*self._svg_space_size - 2*self._svg_border, \
                 self._svg_space_size - 2*self._svg_border)
            
    
    # !!!! TODO - consider having a 6x6 array of colors and text
    
    def svg_neighbors(self):
        '''
            cycle through the svg_pieces attempting using the piece color to 
            denote the edge color
            
    
            data structure for verts[]:
                edge_color: RHConstants Color
                nbr_state: RHState
                    
            verts = {}    
        '''
        pass
    
    
    
    def svg_edge_colors(self):
    
        '''
            When components sets out to draw a neighborhood and navigate through
            the component, it needs to know the number of edges vertical 
            horizontal. These don't structurally change during navigation of
            a complenent
            
            
        '''
        pass
    
    
    def svg_edge_color(self,other):
        '''
            RHComponent builds out SVGs. 
        '''
        diff = other._board - self._board
        
        # positive marks cell filled by moving piece from self to other
        # negative marks cell emptied by moving piece from self to other
        [pos_row,pos_col] = np.array(np.where(diff>0)).transpose()[0]
        [neg_row,neg_col] = np.array(np.where(diff<0)).transpose()[0]
       
        orientation = diff[diff>0][0]
        
        if orientation in [RHConstants.VERTICAL_CAR, RHConstants.VERTICAL_TRUCK]:
            self_end_a_col = pos_col # arbitrary choice for col
            if pos_row > neg_row:
                self_end_a_row = pos_row + 1
            else:
                self_end_a_row = neg_row
        
        if orientation in [RHConstants.HORIZONTAL_CAR, RHConstants.HORIZONTAL_TRUCK]:
            self_end_a_row = pos_row #arbitrary choice for row
            if pos_col > neg_col:
                self_end_a_col = neg_col
            else:
                self_end_a_col = pos_col + 1
        
        edge_piece = [x for x in self.svg_pieces if \
                          x['end_a_row'] == self_end_a_row and \
                          x['end_a_col'] == self_end_a_col ][0]
        
        return (edge_piece['color'])
    
        
    def svg_pieces(self):
        '''
            Add color coding to the pieces in a predictable way such that all
            states in a connected components are drawn with the same piece coloring.
            
            Also intended to be used by RHComponent to permit drawing a graph
            from the perspective of a single state.

        '''
        if self._svg_pieces:
            return self._svg_pieces
        
        car_colors = ['#' + x for x in RHConstants.CAR_COLORS_RGB]
        car_symbols = RHConstants.CAR_SYMBOLS[:]
        truck_colors = ['#' + x for x in  RHConstants.TRUCK_COLORS_RGB ]
        truck_symbols = RHConstants.TRUCK_SYMBOLS[:]
    
        red_car_color = '#' + RHConstants.RED_COLOR_RGB
        red_car_symbol = RHConstants.RED_SYMBOL
        
        ret = []
        
        verticals = [ x for x in self._get_pieces() if x['orientation'] \
                 in [RHConstants.VERTICAL_CAR, RHConstants.VERTICAL_TRUCK] ]
        
        horizontals = [ x for x in self._get_pieces() if x['orientation'] \
                 in [RHConstants.HORIZONTAL_CAR, RHConstants.HORIZONTAL_TRUCK] ]
        
        for col in range(6):
            col_verts = [x for x in verticals if x['end_a_col'] == col]
            sorted_verts = sorted(col_verts, key=lambda x:x['end_a_row'])
            for v in sorted_verts:
                piece = {}
                piece['orientation'] = v['orientation']
                piece['end_a_col'] = v['end_a_col']
                piece['end_a_row'] = v['end_a_row']
                if piece['orientation'] == RHConstants.VERTICAL_CAR:
                    piece['color'] = car_colors.pop()
                    piece['text'] = car_symbols.pop()
                else:
                    piece['color'] = truck_colors.pop()
                    piece['text'] = truck_symbols.pop()
             
                ret.append(piece)
        
        for row in range(6):
            row_horiz = [x for x in horizontals if x['end_a_row'] == row]
            sorted_horiz = sorted(row_horiz, key=lambda x:x['end_a_col'])
            for h in sorted_horiz:
                piece = {}
                piece['orientation'] = h['orientation']
                piece['end_a_col'] = h['end_a_col']
                piece['end_a_row'] = h['end_a_row']
                
                if piece['orientation'] == RHConstants.HORIZONTAL_CAR:
                    if piece['end_a_row'] == 2 and piece['end_a_col'] in self._red_car_cols():
                        piece['color'] = red_car_color
                        piece['text'] = red_car_symbol
                    else:
                        piece['color'] = car_colors.pop()
                        piece['text'] = car_symbols.pop()
                else:    
                    piece['color'] = truck_colors.pop()
                    piece['text'] = truck_symbols.pop()
                
                ret.append(piece)
        
        self._svg_pieces = ret
        return(self._svg_pieces)
        
 

    '''
    
    
    supress edge algo:
    
    have array of dicts for the various nbhrd compass points
    
    x:
    y:
    color:
    js_id:
    visibility:
    
    
    in RHState:
    
    - build neighborhood by moving svg_pieces
    - have 4 lists of dicts 
        - up_nbrs = []
        - left_nbrs = []
        - down_nbrs = []
        - right_nbrs = []
    
    
    
    
    
    '''

    def svg(self):
        if self._svg_dwg is not None:
            return self._svg_dwg.tostring()
        
        # Build out SVG if not already built out
        dwg = self._svg_base()
        
        for piece in self._svg_pieces:
            row = piece['end_a_row']
            col = piece['end_a_col']
            orient = piece['orientation']
            color = piece['color']
            text = piece['text']
            
            dwg = self._svg_add_piece(dwg,row,col,orient,color,text)
        
        self._svg_dwg = dwg
        
        return self._svg_dwg.tostring()
    
    
    

    def _svg_base(self):
        dwg = svgwrite.Drawing('nosave.svg',(self._svg_board_size,self._svg_board_size),debug=True)

        dwg.add(dwg.rect(insert=(0,0),size=(self._svg_board_size,self._svg_board_size),\
                         fill='#'+RHConstants.BLANK_COLOR_RGB))
        for x in range(7):
            dwg.add(dwg.line((30*x,0),(30*x,180),stroke='black',stroke_width=2))
            dwg.add(dwg.line((0,30*x),(180,30*x),stroke='black',stroke_width=2))
        return dwg

    #dwg.add(dwg.rect(insert=(65, 35), size=(50, 20),rx=5,ry=5,fill='green',  stroke_width=3))
    #def svg_add_piece(dwg,nd_x,nd_y,orientation,color,text):   
    def _svg_add_piece(self,dwg,nd_row,nd_col,piece_type,color,text):
        s = self._svg_space_size
        b = self._svg_border
    
        svg_x = nd_col * s + b
        svg_y = nd_row * s + b
        
        size = self._svg_size[piece_type]
        
        dwg.add(dwg.rect(insert=(svg_x,svg_y),size=size,\
                         rx=self._svg_round_radius,\
                         ry=self._svg_round_radius,\
                         fill=color, \
                         stroke_width=3))
        
        c_x = svg_x + size[0]/2.0
        c_y = svg_y + size[1]/2.0
        dwg.add(dwg.text(text,insert=(c_x,c_y),style='fill:black;text-anchor:middle;alignment-baseline:central'))
        return dwg


    '''
        A vehicle data type:
            orientation: RHConstants.VERTICAL_CAR
            end_a_col
            end_a_row
            
                
    '''
    
    
    def _svg_vehicles(self):
        
        ''' 9/1/19 - experimental approach to putting svg logic in one place
                    Not being used
        two dicts for each piece on the board
            rect_args:
                x
                y
                size 
                rx
                ry
                fill_color
                stroke_width
            
            text_args:
                text
                c_x
                y_x
                style
                
             '''
        
        ret = {'verticals':[], 'horizontals':[]}
        
        
        
        # by creating this copies of the color/symbol arrays, we can use
        # arrray.pop() to cycle through the colors and avoid index math steps                
        car_colors = ['#' + x for x in RHConstants.CAR_COLORS_RGB]
        car_symbols = RHConstants.CAR_SYMBOLS[:]
        truck_colors = ['#' + x for x in  RHConstants.TRUCK_COLORS_RGB ]
        truck_symbols = RHConstants.TRUCK_SYMBOLS[:]
        
        red_car_color = '#' + RHConstants.RED_COLOR_RGB
        red_car_symbool = RHConstants.RED_SYMBOL
        
        text_style = 'fill:black;text-anchor:middle;alignment-baseline:central'
        
        discovered = np.aray([False]*36).reshape(6,6)
        ret = {'vcars':[], 'hcars':[], 'vtrucks':[],'htrucks':[]}
        
                        
        for row in range(6):
            for col in range(6):
                x = col * self._svg_space_size + self._svg_border
                y = row * self._svg_space_size + self._svg_border
                
                if discovered[r,c] == False:
                    if self._board[r,c] == RHConstants.VERTICAL_CAR:
                        discovered[r,c] = True
                        discovered[r+1,c] = True
                        width,height =  self._svg_size['vcar']
                        
                        car_dict = {}
                        car_dict['rect_args'] = {}
                        car_dict['text_args'] = {}
                        
                        rect_args =car_dict['rect_args']
                        rect_args['insert_x'] = x
                        rect_args['insert_y'] = y
                        rect_args['size'] = (width,height)
                        rect_args['rx'] = self._svg_round_radius
                        rect_args['ry'] = self._svg_round_radius
                        rect_args['fill_color'] = car_colors.pop()
                        rect_args['stroke_width'] = car_symbold.pop()
                        
                        text_args = car_dict['text_args']
                        text_args['text'] = car_symbols.pop()
                        text_args['c_x'] =  x + width/2.0
                        text_args['c_y'] =  y + height/2.0
                        text_args['style'] = text_stye
      
                        ret['vcars'].append(car_dict)
                        
                    
                        
                    
                    
                
                
                
    