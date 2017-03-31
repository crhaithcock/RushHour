
import copy
import pdb
import collections
import functools

Piece = collections.namedtuple('Piece', 'end_a end_b topology color symbol')

class State(Object):
    """ State encapsulates all of the data and algorthms to follow the rules of Rush Hour to
        move from one state to another by moving a piece on the game board.BaseException

        A State object also knows how to draw itself. The drawing routines may be pulled out.

        Different algorithms require distinct data structures to model the Rush Hour board
        with pieces placed on the board. These models
        Bit string
        Bit String converted to integer
        Half bit String
        Half bit String coverted to integer
        Array of Piece objects


    """
    BLANK_SPACE = '000'
    VERTICAL_CAR = '001'
    HORIZONTAL_CAR = '011'
    VERTICAL_TRUCK = '100'
    HORIZONTAL_TRUCK = '010'

    def pp(self):
        print ("Class: ", self.__class__)
        for key in self.__dict__:
            print (key, ": ", self.__dict__[key])

    def __repr__(self):
        return "%s(%r)" % (self.__class__, self.__dict__)

    def __init__(self, **kwargs):
        self.board_top_hash = None
        self.board_bottom_hash = None
        self.is_final_state = None
        self.red_car_end_a = None
        self.board_as_bit_string = ''
        self.board = []
        self.pieces = []

        self.svg_grid_size = 30
        self.svg_board_size = self.svg_grid_size  * 6

        if 'red_car_end_a' in kwargs:
            self.red_car_end_a = kwargs['red_car_end_a']
        if 'board_top_hash' in kwargs:
            self.board_top_hash = kwargs['board_top_hash']
        if 'board_bottom_hash' in kwargs:
            self.board_bottom_hash = kwargs['board_bottom_hash']

        if self.isValid():
            self.set_derived_fields()
            self.color_and_label_pieces_topologically()


    @classmethod
    def from_key(cls):
        """ Define a state using three integers: top hash, bottom hash, red car position.
            All other state values will be derived."""
        pass

#    def full_data(self):
#        pass

#    def key(self):
#
#        return (self.top_hash, self.bottom_hash, self.red_car_end_a)
#        pass


    def __is_valid(self):
        """Confirm values set for the state are consistent with the internal data model
            and the rules of the Rush Hour game"""
        if self.board_top_hash is None:
            print("top hash is none")
            return False
        if self.board_bottom_hash is None:
            print("bottom hash is none")
            return False
        if self.red_car_end_a not in range(12, 18):
            print("red car out of range")
            return False

        return True

        # top hash int is set
        # bottom hash is set
        # red car end a is set and within domain values
        # space by board space is feasible domain values
        # space by board space creates legit board - feasbile layout or cars and trucks.

    def set_derived_fields(self):
        """Sets derived fields such as board_as_bit_string."""
        if self.isValid():
            self.board_as_bit_string = bin(self.board_top_hash)[2:].zfill(54) +\
                                       bin(self.board_bottom_hash)[2:].zfill(54)
            self.board = [self.board_as_bit_string[i:i+3] for i in range(0, 108, 3)]
            self.set_array_of_pieces()

            if self.red_car_end_a == 16:
                self.is_final_state = True
            else:
                self.is_final_state = False


    @functools.total_ordering
    def __lt__(self, other):
        if type(other) is type(self):
            return self.red_car_end_a > other.red_car_end_a or\
                   (self.red_car_end_a == other.red_car_end_a and\
                    int(self.board_as_bit_string, 2) < int(other.board_as_bit_string, 2))
        return False

    def __eq__(self, other):
        if type(other) is type(self):
            return self.board_top_hash == other.board_top_hash and\
                   self.board_bottom_hash == other.board_bottom_hash and\
                   self.red_car_end_a == other.red_car_end_a
        return False

    def __ne__(self, other):
        if type(other) is type(self):
            return not self.__eq__(other)
        return True

    def __hash__(self):
        return hash((self.board_top_hash, self.board_bottom_hash, self.red_car_end_a))



    def neighbor_from_move_car_left(self, car_end_a):
        """Create a new state derived from the current state by moving the indicated
           car left one space. Returns an instance of State."""

        nbr = copy.deepcopy(self)
        nbr_board = nbr.board()

        new_board[car_end_a - 1] = self.HORIZONTAL_CAR
        new_board[car_end_a + 1] = self.BLANK_SPACE
        nbr.set_board_hash_from_array(new_board)

        if self.red_car_end_a == car_end_a:
            nbr.red_car_end_a = nbr.red_car_end_a - 1

        return nbr


    def set_board_hash_from_array(self, board):
        """ Convert data representation of Rush Hour board.
            Starting with array of Pieces, define the two half board integers.
        """
        bit_string = ''.join(board)
        self.board_top_hash = int(bit_string[:54], 2)
        self.board_bottom_hash = int(bit_string[54:], 2)
        return


    def set_array_of_pieces(self):
        """ Convert data representation of Rush Hour board.
            Create an array of Piece objects defined by an array of bit strings."""

        board = copy.copy(self.board)

        self.pieces = []
        for i in range(36):
            if board[i] == self.VERTICAL_CAR:
                self.pieces.append(Piece(end_a=i,\
                                         end_b=i+6,\
                                         topology=self.VERTICAL_CAR,\
                                         symbol=None,\
                                         color=None))

                board[i] = self.BLANK_SPACE
                board[i+6] = self.BLANK_SPACE

            elif board[i] == self.HORIZONTAL_CAR:
                self.pieces.append(Piece(end_a=i,\
                                         end_b=i+1,\
                                         topology=self.HORIZONTAL_CAR,\
                                         symbol=None,\
                                         color=None))
                board[i] = self.BLANK_SPACE
                board[i+1] = self.BLANK_SPACE

            elif board[i] == self.VERTICAL_TRUCK:
                self.pieces.append(Piece(end_a=i,\
                                         end_b=i + 12,\
                                         topology=self.VERTICAL_TRUCK,\
                                         symbol=None,\
                                         color=None))
                board[i] = self.BLANK_SPACE
                board[i+6] = self.BLANK_SPACE
                board[i+12] = self.BLANK_SPACE

            elif board[i] == self.HORIZONTAL_TRUCK:
                self.pieces.append(Piece(end_a=i,\
                                         end_b=i+2,\
                                         topology=self.HORIZONTAL_TRUCK,\
                                         symbol=None,\
                                         color=None))
                board[i] = self.BLANK_SPACE
                board[i+1] = self.BLANK_SPACE
                board[i+2] = self.BLANK_SPACE



    def can_move_left(self, piece):
        """Moving a piece left requires piece to not be on left edge
           and space to left of piece must be unoccupied"""
        if piece.end_a % 6 == 0 or\
           piece.topology not in [self.HORIZONTAL_CAR, self.HORIZONTAL_TRUCK]:
            return False
        return self.board[piece.end_a - 1] == self.BLANK_SPACE

    def can_move_right(self, piece):
        """Moving a piece right requires piece to not be on right edge
           and space to right of piece must be unoccupied"""
        if piece.end_b % 6 == 5 or\
           piece.topology not in [self.HORIZONTAL_CAR, self.HORIZONTAL_TRUCK]:
            return False
        return self.board[piece.end_b + 1] == self.BLANK_SPACE

    def can_move_up(self, piece):
        """Moving a piece up requires piece to not be on top edge
           and space above piece must be unoccupied"""
        if piece.end_a in range(6) or\
           piece.topology not in [self.VERTICAL_CAR, self.VERTICAL_TRUCK]:
            return False
        return self.board[piece.end_a - 6] == self.BLANK_SPACE

    def can_move_down(self, piece):
        """Moving a piece down requires piece to not be on bottom edge
           and space below piece must be unoccupied"""
        if piece.end_b in range(30, 36) or\
           piece.topology not in [self.VERTICAL_CAR, self.VERTICAL_TRUCK]:
            return False
        return self.board[piece.end_b + 6] == self.BLANK_SPACE

    def derive_state_by_moving_piece(self, piece, direction):
        """Input: Piece is iterable [end_a, end_b] """

        board = copy.copy(self.board)
        if direction == 'left' and self.can_move_left(piece):
            board[piece[0] - 1] = board[piece[0]]
            board[piece[1]] = self.BLANK_SPACE
        elif direction == 'right' and self.can_move_right(piece):
            board[piece[1] + 1] = board[piece[1]]
            board[piece[0]] = self.BLANK_SPACE
        elif direction == 'up' and self.can_move_up(piece):
            board[piece[0] - 6] = board[piece[0]]
            board[piece[1]] = self.BLANK_SPACE
        elif direction == 'down' and self.can_move_down(piece):
            board[piece[1] + 6] = board[piece[1]]
            board[piece[0]] = self.BLANK_SPACE
        else:
            return None

        bit_string = ''.join(board)
        board_top_hash = int(bit_string[:54], 2)
        board_bottom_hash = int(bit_string[54:], 2)

        if self.red_car_end_a == piece[0] and direction in ('left', 'right'):
            if direction == 'left':
                red_car_end_a = self.red_car_end_a - 1
            elif direction == 'right':
                red_car_end_a = self.red_car_end_a + 1
        else:
            red_car_end_a = self.red_car_end_a

        nbr_state_dict = {'red_car_end_a':red_car_end_a,\
                          'board_top_hash':board_top_hash,\
                          'board_bottom_hash':board_bottom_hash}
        nbr_state = State(**nbr_state_dict)
        return nbr_state


    def derive_neighbors(self):
        """ Derives neighbors of this State based on the rules of Rush Hour.
            This method returns an array of States."""

        neighbors = []

        for piece in self.pieces:
            if self.can_move_left(piece):
                nbr = self.derive_state_by_moving_piece(piece, 'left')
                neighbors.append([nbr, 'left'])

            if self.can_move_right(piece):
                nbr = self.derive_state_by_moving_piece(piece, 'right')
                neighbors.append([nbr, 'right'])

            if self.can_move_down(piece):
                nbr = self.derive_state_by_moving_piece(piece, 'down')
                neighbors.append([nbr, 'down'])

            if self.can_move_up(piece):
                nbr = self.derive_state_by_moving_piece(piece, 'up')
                neighbors.append([nbr, 'up'])
        return neighbors





    ###########################################
    ##
    ##            Display Routines
    ##
    ##
    ############################################

    car_symbols = ['Q', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'L']
    truck_symbols = ['T', 'R', 'W', 'Z']
    car_colors = ['7FFF00', '7FFFD4', 'D2691E', '8B008B', 'BDB76B', '8B0000', 'FF1493',\
                  '1E90FF', 'FFD700', 'ADFF2F', 'CD5C5C', 'F0E68C']
    truck_colors = ['F08080', 'FFA07A', 'FF00FF', '00FA9A']

    RED_COLOR = 'FF0000'
    RED_SYMBOL = 'X'
    BLANK_COLOR = "E6E6E6"

    def sort_pieces_topologically(self):
        """Sorting pieces topologically allows applying a labeling algorithm
           to the cars and trucks that is consistent when traversing throuh the Rush Hour Graph"""

        v_cars = sorted([p for p in self.pieces if p.topology == self.VERTICAL_CAR],\
                        key=lambda p: p.end_a)
        v_trucks = sorted([p for p in self.pieces if p.topology == self.VERTICAL_TRUCK],\
                        key=lambda p: p.end_a)
        h_cars = sorted([p for p in self.pieces if p.topology == self.HORIZONTAL_CAR],\
                        key=lambda p: p.end_a)
        h_trucks = sorted([p for p in self.pieces if p.topology == self.HORIZONTAL_TRUCK],\
                        key=lambda p: p.end_a)

        self.pieces = v_cars + h_cars + v_trucks + h_trucks

    def color_and_label_pieces_topologically(self):
        self.sort_pieces_topologically()

        car_index = truck_index = 0

        car_topologies = [self.VERTICAL_CAR, self.HORIZONTAL_CAR]
        truck_topologies = [self.VERTICAL_TRUCK, self.HORIZONTAL_TRUCK]

        colored_pieces = []

        for piece in self.pieces:
            if piece.end_a == self.red_car_end_a:
                colored_pieces.append(Piece(end_a=piece.end_a,\
                                            end_b=piece.end_b,\
                                            topology=piece.topology,\
                                            symbol=self.RED_SYMBOL,\
                                            color=self.RED_COLOR))

            elif piece.topology in car_topologies:
                colored_pieces.append(Piece(end_a=piece.end_a,
                                            end_b=piece.end_b,\
                                            topology=piece.topology,\
                                            symbol=self.car_symbols[car_index],\
                                            color=self.car_colors[car_index]))
                car_index = car_index + 1

            else:
                colored_pieces.append(Piece(end_a=piece.end_a,\
                                            end_b=piece.end_b,\
                                            topology=piece.topology,\
                                            symbol=self.truck_symbols[truck_index],\
                                            color=self.truck_colors[truck_index]))
                truck_index = truck_index + 1

        self.pieces = colored_pieces

    def sort_pieces_combintorially(self):
        self.pieces = sorted(self.pieces, key=lambda p: p.end_a)


    @property
    def svg_width(self):
        return self.svg_board_size

    @property
    def svg_height(self):
        return self.svg_board_size

    @property
    def svg(self):

        grid_size = self.svg_grid_size
        board_size = self.svg_board_size

        svg = '<svg width="'+str(board_size)+'" height="'+str(board_size)+\
              '" xmlns="http://www.w3.org/2000/svg">'

        # Board Outline
        svg = svg + """<rect x="0" y="0" width = "%d" height = "%d" """\
                    %(board_size, board_size) +\
                    """style="fill:#%s; stroke:black; stroke-width:2; stroke-opacity:0.5;"/> """\
                    %(self.BLANK_COLOR)

        # car/truck dimensions
        inner_offset = 2
        car_outer_height = grid_size
        car_outer_width = grid_size * 2
        car_inner_x = inner_offset
        car_inner_y = inner_offset
        car_inner_height = car_outer_height - (inner_offset * 2)
        car_inner_width = car_outer_width - (inner_offset * 2)


        truck_outer_height = grid_size
        truck_outer_width = grid_size*3
        truck_inner_x = inner_offset
        truck_inner_y = inner_offset
        truck_inner_height = truck_outer_height - (inner_offset * 2)
        truck_inner_width = truck_outer_width - (inner_offset * 2)

        svg = svg + '<defs>'
        svg = svg + '    <g id="car" >'
        svg = svg + '        <rect x="0" y="0" height="' + str(car_outer_height) +\
                                '" width="' + str(car_outer_width) +\
                                '" style="opacity:0.0"/>'
        svg = svg + '        <rect x="' + str(car_inner_x)+ '" y="' + str(car_inner_y) + '" '
        svg = svg + 'height ="' + str(car_inner_height) +\
                    '" width="'+ str(car_inner_width) + '" rx="5" ry="5"/>'
        svg = svg + '    </g>'

        svg = svg + '    <g id="truck" >'
        svg = svg + '        <rect x="0" y="0" height="' + str(truck_outer_height) +\
                                '" width="' + str(truck_outer_width) +\
                                '" style="opacity:0.0"/>'
        svg = svg + '        <rect x="' + str(truck_inner_x)+ '" y="' + str(truck_inner_y) + '" '
        svg = svg + 'height ="' + str(truck_inner_height) + '" width="'+\
                                  str(truck_inner_width) + '" rx="5" ry="5"/>'
        svg = svg + '    </g>'
        svg = svg + '</defs>'


        # draw grid lines
        for i in range(1, 6):
            svg = svg + '<line x1="0" y1="%d" x2="%d" y2="%d" style="stroke: black;"/>'\
                        %(i*grid_size, board_size, i*grid_size)
            svg = svg + '<line x1="%d" y1="0" x2="%d" y2="%d" style="stroke: black;"/>'\
                        %(i*grid_size, i*grid_size, board_size)

        # index into color and symbol arrays
        #car_index = 0
        #truck_index = 0

        for piece in self.pieces:
            col = piece.end_a % 6
            row = int(piece.end_a / 6)
            x = col * grid_size
            y = row * grid_size
            rot_x = x + grid_size * .5
            rot_y = y + grid_size * .5
            text_symbol = piece.symbol
            color = piece.color

            text_style = ' text-anchor="middle" alignment-baseline="central"'+\
                         ' style="font-weight:bold" '
            xform_rotate = 'transform="rotate(90,' + str(rot_x)+','+str(rot_y)+')"'
            if piece.topology == self.VERTICAL_CAR:
                svg = svg + '<use xlink:href="#car" x="'+ str(x) +'" y="'+ str(y) +\
                            '"' + xform_rotate + ' style="fill:#'+color+'" ;" />'
                text_x = ' x="' + str(x + car_outer_height / 2) + '"'
                text_y = ' y="' + str(y + car_outer_width / 2)  + '"'
                svg = svg + '<text ' + text_x + text_y + text_style + '>' + text_symbol + '</text>'
            if piece.topology == self.VERTICAL_TRUCK:
                svg = svg + '<use xlink:href="#truck" x="'+ str(x) +'" y="'+str(y)+\
                            '"' +  xform_rotate +' style="fill:#'+color+'" ;" />'
                text_x = ' x="' + str(x + truck_outer_height / 2) + '"'
                text_y = ' y="' + str(y + truck_outer_width / 2)  + '"'
                svg = svg + '<text ' + text_x + text_y + text_style + '>' + text_symbol + '</text>'
            if piece.topology == self.HORIZONTAL_CAR:

                svg = svg + '<use xlink:href="#car" x="'+ str(x) +'" y="'+str(y)+\
                            '" style="fill:#'+color+'" ;" />'

                text_x = ' x="' + str(x + car_outer_width / 2) + '"'
                text_y = ' y="' + str(y + car_outer_height / 2)  + '"'
                svg = svg + '<text ' + text_x + text_y + text_style + '>' + text_symbol + '</text>'

            if piece.topology == self.HORIZONTAL_TRUCK:
                svg = svg + '<use xlink:href="#car" x="'+ str(x) +\
                            '" y="'+str(y)+ 'style="fill:#'+color+'" ;" />'
                text_x = ' x="' + str(x + truck_outer_width / 2) + '"'
                text_y = ' y="' + str(y + truck_outer_height / 2)  + '"'
                svg = svg + '<text ' + text_x + text_y + text_style + '>' + text_symbol + '</text>'

        red_col = self.red_car_end_a % 6
        red_row = int(self.red_car_end_a / 6)
        red_x = red_col * grid_size
        red_y = red_row * grid_size

        svg = svg + '<use xlink:href="#car" x="'+ str(red_x) +'" y="'+str(red_y)+\
                    '" style="fill:#'+ self.RED_COLOR +'" ;" />'
        text_x = ' x="' + str(red_x + car_outer_width * .5) + '"'
        text_y = ' y="' + str(red_y + car_outer_height * .5)  + '"'
        text_symbol = 'X'
        svg = svg + '<text ' + text_x + text_y + text_style + '>' + text_symbol + '</text>'


        svg = svg + """</svg>"""


        return svg


    def set_colors(self, colors=None, sort='topological'):

        if sort == 'topological':
            self.sort_pieces_topologically

        if colors is not None:
            pass


    # !!!! TODO - Add inputs to allow color scheme to be passed in
    # !!!! (car_colors = [ . . . ], truck_colors = [ . . .] )
    def repr_html_table(self, color_order='topological'):
        """Generate a well formed HTML table representation of the board"""
        board_symbols = [""] * 36
        board_colors = [self.BLANK_COLOR] * 36
        car_index = 0
        truck_index = 0

        board_symbols[self.red_car_end_a] = self.RED_SYMBOL
        board_symbols[self.red_car_end_a+1] = self.RED_SYMBOL
        board_colors[self.red_car_end_a] = self.RED_COLOR
        board_colors[self.red_car_end_a+1] = self.RED_COLOR

        if color_order not in ('construction', 'topological'):
            return "<table />"

        pieces = [p for p in self.pieces if p.end_a != self.red_car_end_a]

        if color_order == 'topological':
            pieces.sort(key=lambda p: p.topology)
        if color_order == 'constuction':
            pieces.sort(key=lambda p: p.end_a)

        for p in pieces:
            if p.topology in (self.VERTICAL_CAR, self.HORIZONTAL_CAR):
                board_symbols[p.end_a] = self.car_symbols[car_index]
                board_symbols[p.end_b] = self.car_symbols[car_index]
                board_colors[p.end_a] = self.car_colors[car_index]
                board_colors[p.end_b] = self.car_colors[car_index]
                car_index = car_index + 1

            if p.topology == self.VERTICAL_TRUCK:
                board_symbols[p.end_a] = self.truck_symbols[truck_index]
                board_symbols[p.end_a + 6] = self.truck_symbols[truck_index]
                board_symbols[p.end_b] = self.truck_symbols[truck_index]
                board_colors[p.end_a] = self.truck_colors[truck_index]
                board_colors[p.end_a + 6] = self.truck_colors[truck_index]
                board_colors[p.end_b] = self.truck_colors[truck_index]
                truck_index = truck_index + 1

            if p.topology == self.HORIZONTAL_TRUCK:
                board_symbols[p.end_a] = self.truck_symbols[truck_index]
                board_symbols[p.end_a + 1] = self.truck_symbols[truck_index]
                board_symbols[p.end_b] = self.truck_symbols[truck_index]
                board_colors[p.end_a] = self.truck_colors[truck_index]
                board_colors[p.end_a + 1] = self.truck_colors[truck_index]
                board_colors[p.end_b] = self.truck_colors[truck_index]
                truck_index = truck_index + 1

        html_data = zip(board_colors, board_symbols)
        html_cells = ['<td bgcolor="%s" style="width:30px; height:30px;'  %x +\
                      ' vertical-align:middle; text-align:center">%s</td>' for x in html_data]
        return '<table>' + ''.join(['<tr>' + ''.join(html_cells[i:i+6]) + '</tr>'\
                                    for i in range(0, 35, 6)]) +\
               '</table>'



#example state from board with 2 cars and 2 trucks.
STATE_DICT = {'board_top_hash':7599893090940448,\
              'board_bottom_hash':2200105390080,\
              'red_car_end_a':13}
TEST_STATE = State(**state_dict)



     