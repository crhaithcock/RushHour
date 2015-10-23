'''
Created on Aug 25, 2015

@author: cliff
'''

import constants
import tables 
import numpy as np




#################################
#
#
#    Board represents the Rush Hour board as a linear array.
#    Grouped Car Placements is a list of lists. The sublist at index i is the set of cars with 'end_a' located at index i.
#    Grouped Truck Placements is the analogue to Grouped Car Placements
#
###################################


# Shared Global Structures
PiecePlacements = [{}] * 108 # list of dictionaries: {end_a:; end_b; length:; orientation;topology_code}
RedCarPiecePlacements = []
PiecePlacementsInUse = []  # Stack that facilitates recording state.
Board = [constants.BLANK_SPACE] * 36
GroupedCarPlacements = [[]] * 36    
GroupedTruckPlacements = [[]] * 36

h5_directory = r'C:\Users\cliff\workspace\Rush Hour With Python\data'
h5_file = None


def insert_PiecePlacement(index,end_a,end_b, length, orientation,topology_code):
    Board[index]['end_a'] = end_a
    Board[index]['end_b'] = end_b
    Board[index]['length'] = length
    Board[index]['orientation'] = orientation
    Board[index]['topology_code'] = topology_code


def init_PiecePlacements():
    index = 0
    
    # horizontal cars
    for i in range(6):
        for j in range(5):
            end_a = 6*i+j
            end_b = 6*i+j+1
            insert_PiecePlacement(index,end_a, end_b, 2, 'Horizontal', constants.HORIZONTAL_CAR)
            GroupedCarPlacements[ end_a ].append(PiecePlacements[index])
            if end_a in range(12,18):
                RedCarPiecePlacements.append(PiecePlacements[index])
            index = index + 1
            
    # vertical cars
    for i in range(5):
        for j in range(6):
            end_a = 6*i+j
            end_b =  6*i+j+6
            insert_PiecePlacement(index, end_a,end_b, 2, 'Vertical',constants.VERTICAL_CAR)
            GroupedCarPlacements[ Board[index]['end_a'] ].append(PiecePlacements[index])
            index = index + 1 
    
    # horizontal trucks
    for i in range(6):
        for j in range(4):
            end_a = 6*i+j
            end_b = 6*i+j+2
            insert_PiecePlacement(index,end_a, end_b, 3, 'Horizontal',constants.HORIZONTAL_TRUCK)
            GroupedTruckPlacements[ Board[index]['end_a'] ].append(PiecePlacements[index])
            index = index + 1
    
    # vertical trucks
    for i in range(6):
        for j in range(4):
            end_a =  6*i+j
            end_b = 6*i+j+12
            insert_PiecePlacement(index, 6*i+j, 6*i+j+6, 3, 'Vertical',constants.VERTICAL_TRUCK)
            GroupedTruckPlacements[ Board[index]['end_a'] ].append(PiecePlacements[index])
            index = index + 1


class State(tables.IsDescription):
    game_number  = tables.Int64Col()
    game_hash_top = tables.Int64Col()
    game_hash_bottom = tables.Int64Col()
    red_car_end_a = tables.Int64Col()
    is_goal_state = tables.Int64Col()
    degree = tables.Int64Col()
    
   
   
'''
    hdf5 file structure.
    Each run of this progra will produce a new single file for the combinatorial class.
    Afterwards, perhaps all of hte files will be glued together.
    
    Basic Group / Table Structure:
    
    /comb_class
    /comb_class/states # index on toplogical hash
    /comb_class/edges  # index
    /comb_class/sorted_states
    
'''
         
def init_hdf5(num_cars,num_trucks):


    
    h5_filename = '%d_cars_%d_trucks.hdf5' %(num_cars,num_trucks)
    
    group_comb_class = 'comb_class_%d' %(2**num_cars * 3**num_trucks)
    
    
    h5_file = tables.open_file(h5_directory + r'/' + h5_filename)
    
    
    # setup groups and table to hold state data
    h5_file.create_group('/', group_comb_class, 'Combinatorial Class for 2 cars and 2 trucks')
    
     
    

     
def init():
    init_PiecePlacements()
    init_hdf5()
    
    
def record_state_hdf5():
    pass

def record_state():
    # record_state_csv()
    record_state_hdf5()
    # record_state_sqlite()
    

def place_piece_on_board(piece_placement):
    
    Board[piece_placement['end_a']] = piece_placement['topology_code']
    Board[piece_placement['end_b']] = piece_placement['orientaion_code']
    
    if piece_placement['length'] == 3:
        if piece_placement['orientation'] == 'Vertical':
            Board[piece_placement['end_a'] + 6] = piece_placement['topology_code']
        else:
            Board[piece_placement['end_a'] + 1] = piece_placement['topology_code']


def remove_piece_from_board(piece_placement):
    
    Board[piece_placement['end_a']] = constants.BLANK_SPACE
    Board[piece_placement['end_b']] = constants.BLANK_SPACE
    
    if piece_placement['length'] == 3:
        if piece_placement['orientation'] == 'Vertical':
            Board[piece_placement['end_a'] + 6] = constants.BLANK_SPACE
        else:
            Board[piece_placement['end_a'] + 1] = constants.BLANK_SPACE
            

def board_spaces_are_open(piece_placement):
    
    if Board[piece_placement['end_a']] != constants.BLANK_SPACE:
        return False
    
    if Board[piece_placement['end_b']] != constants.BLANK_SPACE:
        return False

    if piece_placement['length'] == 3:
        if piece_placement['orientation'] == 'Vertical':
            if Board[piece_placement['end_a'] + 6] != constants.BLANK_SPACE:
                return False
        else:
            if Board[piece_placement['end_a'] + 1] != constants.BLANK_SPACE:
                return False

    # All conditions leading to existence of a non-open space have been tested.    
    return True



def main_loop(num_cars,num_trucks):
    
    #Place red car on board and then remaining pieces recursively
    for i in RedCarPiecePlacements:
        place_piece_on_board(i)
        place_remaining_pieces_on_board(num_cars-1, num_trucks,0)
        remove_piece_from_board(i)
        
   
        
def place_remaining_pieces_on_board(num_cars,num_trucks,start_pos):
    
    if num_cars == 0 and num_trucks == 0:
        record_state
        return
    
    if num_cars > 0:
        for i in range(start_pos,len(Board)):
            for car in GroupedCarPlacements[i]:
                if board_spaces_are_open(car):
                    place_piece_on_board(car)
                    PiecePlacementsInUse.push(car)
                    place_remaining_pieces_on_board(num_cars-1, num_trucks, start_pos+1)
                    remove_piece_from_board(car)
                    PiecePlacementsInUse.pop()
    
    if num_trucks > 0:
        for i in range(start_pos):
            for truck in GroupedTruckPlacements[i]:
                if board_spaces_are_open(truck):
                    place_piece_on_board(truck)
                    PiecePlacementsInUse.push(truck)
                    place_remaining_pieces_on_board(num_cars, num_trucks-1, start_pos+1)
                    remove_piece_from_board(truck)
                    PiecePlacementsInUse.pop()    

    # We have run through all possible placements for the next car/truck
    # If we were unable to place a piece, then no further recursion takes place 
    # and no final state is recorded.
    
    
    
    
    
