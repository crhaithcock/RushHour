

# Combinatorial algorithm to generate all states for a given fixed number
# of cars and trucks. The number of cars and trucks defines the combinatorial
# class of a state in the RushHour graph.

import sqlite3
import collections

BLANK_SPACE = '000'
VERTICAL_CAR = '001'
VERTICAL_TRUCK = '010'
HORIZONTAL_CAR = '011'
HORIZONTAL_TRUCK = '100'



states_to_save = collections.deque()
record_count = 0

# The recursion ends with a completed state that can be recorded.
#
# recursion process:
# There are five possible locations for placing the red car.
#
# Place red Car.
# Call function Replace
# Set cur position at top left corner

# A state is uniquely defined by the positions of the cars/trucks and the position of the red car.

RED_CAR_END_A_POSITIONS = range(12, 18)
BOARD = [BLANK_SPACE] * 36
red_car_end_a = 0

TOPOLOGY_OFFSET = {VERTICAL_CAR:[0, 6], HORIZONTAL_CAR:[0, 1], \
                   VERTICAL_TRUCK:[0, 6, 12], HORIZONTAL_TRUCK:[0, 1, 2]}




def add_piece(end_a, piece_topology):
    """Add a piece to the board of bit strings.
       Input: end_a position: (top left most position of the piece being placed
              piece_topology: one of four constant values that defined length and orientation
       Output: board is updated per the inputs.
    """
    for board_space in TOPOLOGY_OFFSET[piece_topology]:
        BOARD[board_space+end_a] = piece_topology

def remove_piece(end_a, piece_topology):
    """ Remove piece from board. """
    for board_space in TOPOLOGY_OFFSET[piece_topology]:
        BOARD[board_space+end_a] = BLANK_SPACE

def board_is_open(end_a, piece_topology):
    """Check that that the board is open to allow placement of piece """
    board_positions = [end_a + x for x in TOPOLOGY_OFFSET[piece_topology]]

    # Exclude structurally impossible situations:
    # Pieces extending off board to right or bottom.
    if piece_topology == HORIZONTAL_CAR:
        if end_a % 6 == 5:
            return False
    if piece_topology == HORIZONTAL_TRUCK:
        if end_a %6 > 3:
            return False
    if piece_topology == VERTICAL_CAR:
        if int(end_a / 6) == 5:
            return False
    if piece_topology == VERTICAL_TRUCK:
        if int(end_a / 6) > 3:
            return False

    #print(end_a, piece_topology)
    return all([BOARD[x] == BLANK_SPACE for x in board_positions])


def generate_states(num_cars, num_trucks):
    """ Generate all possible states for the input combinatorial class."""

    comb_class = 2**num_cars*3**num_trucks
    red_car_positions = range(12, 17)

    for end_a in red_car_positions:
        red_car_end_a = end_a
        add_piece(end_a, HORIZONTAL_CAR)
        place_remaining_pieces(0, num_cars-1, num_trucks, red_car_end_a, comb_class)
        remove_piece(end_a, HORIZONTAL_CAR)

    flush_data()

def place_remaining_pieces(cur_position, num_cars, num_trucks, red_car_end_a, comb_class):
    """ Recursive algorithm to complete placing pieces on the board."""
    global BOARD

    # short circuit recursion for impossible configurations

    # if remaining pieces require more spaces than available, bail out of recursion
    if (len(BOARD) - cur_position) < 2*num_cars + 3 * num_trucks:
        return
    


    if num_cars == num_trucks == 0:

        top_hash_int, bottom_hash_int = board_to_ints()
        record_state(red_car_end_a, top_hash_int, bottom_hash_int, comb_class)
        return

    if num_cars > 0:
        for pos in range(cur_position, len(BOARD)):
            if board_is_open(pos, VERTICAL_CAR):
                add_piece(pos, VERTICAL_CAR)
                place_remaining_pieces(pos + 1, num_cars - 1, num_trucks, red_car_end_a, comb_class)
                remove_piece(pos, VERTICAL_CAR)

            if board_is_open(pos, HORIZONTAL_CAR):
                add_piece(pos, HORIZONTAL_CAR)
                place_remaining_pieces(pos+2, num_cars-1, num_trucks, red_car_end_a, comb_class)
                remove_piece(pos, HORIZONTAL_CAR)

    if num_trucks > 0:
        for pos in range(cur_position, len(BOARD)):
            if board_is_open(pos, VERTICAL_TRUCK):
                add_piece(pos, VERTICAL_TRUCK)
                place_remaining_pieces(pos + 1, num_cars-1, num_trucks, red_car_end_a, comb_class)
                remove_piece(pos, VERTICAL_TRUCK)

            if board_is_open(pos, HORIZONTAL_TRUCK):
                add_piece(pos, HORIZONTAL_TRUCK)
                place_remaining_pieces(pos+3, num_cars, num_trucks-1, red_car_end_a, comb_class)
                remove_piece(pos, HORIZONTAL_TRUCK)




BATCH_SIZE = 50000
states_to_save = collections.deque()
record_count = 0
batch_count = 0
def record_state(red_car_end_a=None, top_hash_int=None,\
                 bottom_hash_int=None, comb_class=None):

    """ Record State Information in SQLITE"""
    global states_to_save
    global record_count
    global cur
    global batch_count

    if red_car_end_a:
        states_to_save.append([red_car_end_a, top_hash_int, bottom_hash_int, comb_class])
        record_count = record_count + 1

    if record_count >= BATCH_SIZE:
        batch_count = batch_count + 1
        print("saving batch %d of size %d" %(batch_count, len(states_to_save)))
        conn = sqlite3.connect("./data/rush_hour.db")
        conn.isolation_level = None
        cur = conn.cursor()
        cur.execute("begin")
        for state in states_to_save:
            insert_str = """insert into game_state(red_car_end_a,game_hash_top
                            , game_hash_bottom , comb_class_id)
                            values ({!s}, {!s} , {!s} ,{!s})"""\
                            .format(state[0], state[1], state[2], state[3])
            cur.execute(insert_str)
        cur.execute("commit")
        conn.close()

        states_to_save = collections.deque()
        record_count = 0

def flush_data():
    """ Record State Information in SQLITE"""
    global states_to_save
    global record_count

    record_count = BATCH_SIZE + 1

    record_state()


def board_to_ints():
    global BOARD
    bit_string = ''.join(BOARD)
    board_top_hash = int(bit_string[:54], 2)
    board_bottom_hash = int(bit_string[54:], 2)

    return (board_top_hash, board_bottom_hash)

#begin script

generate_states(2,2)
#for num_cars in range(1,13):
#    for num_trucks in range(5):
#        generate_states(num_cars,num_trucks)


