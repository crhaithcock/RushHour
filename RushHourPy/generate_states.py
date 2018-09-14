

# Combinatorial algorithm to generate all states for a given fixed number
# of cars and trucks. The number of cars and trucks defines the combinatorial
# class of a state in the RushHour graph.

import sqlite3
import collections
from collections import defaultdict

import state
import constants

BLANK_SPACE = constants.BLANK_SPACE
VERTICAL_CAR = constants.VERTICAL_CAR
VERTICAL_TRUCK = constants.VERTICAL_TRUCK
HORIZONTAL_CAR = constants.HORIZONTAL_CAR
HORIZONTAL_TRUCK = constants.HORIZONTAL_TRUCK

# global db connection to be resused without reopening the connection
db_conn = None  #sqlite3 connection
db_cur = None   # sqlite3 cursor


# global counters
num_states = 0
num_soln_states = 0


# data to manage saving batches of records.
BATCH_SIZE = 50000
states_to_save = collections.deque()
record_count = 0
batch_count = 0



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


def open_db(num_cars,num_trucks):
    global db_conn
    global db_cur

    db_name = "rush_hour_{!s}_cars_{!s}_trucks.db".format(num_cars,num_trucks)
    db_path = "./database/"+db_name
    db_conn = sqlite3.connect(db_path)
    db_conn.isolation_level = None
    db_cur = db_conn.cursor()

    print("Opened DB: " + db_path)
    # create tables statement
    with open('./database/rush_hour_tables_ddl.sql', 'r') as sqlfile:
        sql=sqlfile.read()

    db_cur.executescript(sql)
    db_conn.commit()



def close_db():
    global db_cur
    global db_conn

    db_conn.close()



def generate_states(num_cars, num_trucks):
    """ Generate all possible states for the input combinatorial class."""
    global db_conn

    #open_db(num_cars,num_trucks)

    comb_class = 2**num_cars*3**num_trucks
    red_car_positions = range(12, 17)

    #sql = "insert into combinatorial_class (id,num_cars,num_trucks)values({!s},{!s},{!s})"\
    #       .format(comb_class,num_cars,num_trucks)
    #db_conn.commit()


    for red_car_end_a in red_car_positions:

        print("Initializing With Red Car in Position: %d"%(red_car_end_a))
        add_piece(red_car_end_a, HORIZONTAL_CAR)
        #print_board(red_car_end_a)

        place_remaining_pieces(0, num_cars-1, num_trucks, red_car_end_a, comb_class)
        remove_piece(red_car_end_a, HORIZONTAL_CAR)

    #flush_data(comb_class)

    #close_db()






def place_remaining_pieces(cur_position, num_cars, num_trucks, red_car_end_a, comb_class):
    """ Recursive algorithm to complete placing pieces on the board."""

    # short circuit recursion for impossible configurations

    # if remaining pieces require more spaces than available, bail out of recursion
    if (len(BOARD) - cur_position) < 2*num_cars + 3 * num_trucks:
        return



    if num_cars == num_trucks == 0:

        top_hash_int, bottom_hash_int = board_to_ints()
        save_graph_stats(state.State(red_car_end_a,top_hash_int,bottom_hash_int))


        #record_state(red_car_end_a, top_hash_int, bottom_hash_int, comb_class)
        return

    if num_cars > 0:
        for pos in range(cur_position, len(BOARD)):

            if board_is_open(pos, HORIZONTAL_CAR):
                add_piece(pos, HORIZONTAL_CAR)
                #print_board(red_car_end_a)
                place_remaining_pieces(pos+2, num_cars-1, num_trucks, red_car_end_a, comb_class)
                remove_piece(pos, HORIZONTAL_CAR)

            if board_is_open(pos, VERTICAL_CAR):
                add_piece(pos, VERTICAL_CAR)
                #print_board(red_car_end_a)
                place_remaining_pieces(pos + 1, num_cars - 1, num_trucks, red_car_end_a, comb_class)
                remove_piece(pos, VERTICAL_CAR)

    if num_trucks > 0:
        for pos in range(cur_position, len(BOARD)):

            if board_is_open(pos, HORIZONTAL_TRUCK):
                add_piece(pos, HORIZONTAL_TRUCK)
                #print_board(red_car_end_a)
                place_remaining_pieces(pos+3, num_cars, num_trucks-1, red_car_end_a, comb_class)
                remove_piece(pos, HORIZONTAL_TRUCK)


            if board_is_open(pos, VERTICAL_TRUCK):
                add_piece(pos, VERTICAL_TRUCK)
                #print_board(red_car_end_a)
                place_remaining_pieces(pos + 1, num_cars, num_trucks-1, red_car_end_a, comb_class)
                remove_piece(pos, VERTICAL_TRUCK)


# Global Data to udpate for stats

def graph_stats_factory():
    ret = { 'num_states':0, \
            'num_soln_states':0, \
            'num_isolated_states':0, \
            'deg_sum':0, \
            'deg_hist': defaultdict(int) \
          }
    return ret


graph_stats = defaultdict(graph_stats_factory)

def save_graph_stats(state):
    comb_class = state.combinatorial_class
    topo_1 = state.topo_class_1
    topo_2 = state.topo_class_2
    deg = state.degree

    stats = graph_stats[(comb_class,topo_1,topo_2)]

    stats['num_states'] = stats['num_states'] + 1
    stats['deg_hist'][deg] = stats['deg_hist'][deg] + 1
    stats['deg_sum'] = stats['deg_sum'] + deg
    if deg == 0:
        stats['num_isolated_states'] = stats['num_isolated_states'] + 1

    if state.is_final_state:
        stats['num_soln_states'] =  stats['num_soln_states'] + 1

    #graph_stats[(comb_class,topo_1,topo_2)] = stats



    



def record_state(red_car_end_a=None, top_hash_int=None,\
                 bottom_hash_int=None, comb_class=None):

    global states_to_save
    global record_count
    global batch_count
    global db_cur
    global num_soln_states
    global num_states

    if red_car_end_a:
        states_to_save.append([red_car_end_a, top_hash_int, bottom_hash_int, comb_class])
        record_count = record_count + 1
        num_states = num_states + 1
        if red_car_end_a == 16:
            num_soln_states = num_soln_states + 1

    if record_count >= BATCH_SIZE:
    #if False:
        batch_count = batch_count + 1
        
        if red_car_end_a is None:
            red_car_end_a = 'None'
        print("saving batch {!s} of size {!s}. red car position: {!s}".format(batch_count, len(states_to_save),red_car_end_a))
        

        sql = """insert into state(red_car_end_a,game_hash_top
                            , game_hash_bottom , comb_class_id,is_soln_state)
                            values (?,?,?,?,?)"""
        non_soln_params = [ [s[0],s[1],s[2],s[3],0] for s in states_to_save if s[0] != 16]
        soln_params = [ [s[0],s[1],s[2],s[3],1] for s in states_to_save if s[0] == 16]
        params = non_soln_params + soln_params
        db_cur.execute("begin")
        db_cur.executemany(sql,params)
        db_cur.execute("commit")

        states_to_save = collections.deque()
        record_count = 0




def flush_data(comb_class):
    """ Record State Information in SQLITE"""
    
    global record_count
    global num_soln_states
    global num_states

    record_count = BATCH_SIZE + 1

    record_state()
    

    # !!!!TODO Updated comb_class with state counts
    sql = "update combinatorial_class set num_state = {!s} and num_soln_states = {!s}"\
          .format(num_states,num_soln_states)
    
    #!!!! HERE
    # What can be measured while passing through the states?
    # Topology distributions:
    #       Comb_class_id
    #       Topo_Class_id
    #       num_states
    #
    # Looking for levels to slice apart sets of states for in-memory analysis.
    #   







def board_to_ints():
    global BOARD
    bit_string = ''.join(BOARD)
    board_top_hash = int(bit_string[:54], 2)
    board_bottom_hash = int(bit_string[54:], 2)

    return (board_top_hash, board_bottom_hash)

#begin script

#generate_states(2,2)
#for num_cars in range(1,13):
#    for num_trucks in range(5):
#        generate_states(num_cars,num_trucks)


