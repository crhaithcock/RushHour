'''
Created on Apr 27, 2015

@author: cliff
'''

from collections import deque
from constants import *


def from_array_to_bit_string(board_array):
    return ''.join(board_array)

def from_bit_string_to_array(board_bit_string):
    return [board_bit_string[i:i+3] for i in range(0,108,3)]

def from_int_to_half_bit_string(hash_int):
    return bin(hash_int)[2:].zfill(54)

def from_int_to_half_board_array(hash_int):
    bit_string = bin(hash_int)[2:].zfill(54)
    return [bit_string[i:i+3] for i in range(0,54,3)]
    
def from_array_to_two_bit_strings(board_array):
    full_string = from_array_to_bit_string(board_array)
    output = [full_string[:54],full_string[54:]]
    return output

def from_two_ints_to_bit_string(top_hash_int, bottom_hash_int):
    return bin(top_hash_int)[2:].zfill(54) + bin(bottom_hash_int)[2:].zfill(54)
    
def from_bit_string_to_pieces_array(board_bit_string):
    board_array = from_bit_string_to_array(board_bit_string)
    for i in range(36):
        if board_array[i] == VERTICAL_CAR:
            board_array[i+6] = BLANK_SPACE
        
        if board_array[i] == HORIZONTAL_CAR:
            board_array[i+1] = BLANK_SPACE  
        
        if board_array[i] == VERTICAL_TRUCK:
            board_array[i+6] = BLANK_SPACE 
            board_array[i+12] = BLANK_SPACE
        
        if board_array[i] == HORIZONTAL_TRUCK:
            board_array[i+1] = BLANK_SPACE
            board_array[i+2] = BLANK_SPACE
        
    indexed_board = zip(range(36),board_array)
    
    return [x for x in indexed_board if x[1] != BLANK_SPACE]







########################################
#
#    Display Methods
#
########################################
    
def html_table_for_board_bit_string_construction_coloring(board_bit_string,red_car_end_a):
    """The coloring scheme of this algorithm will color all nodes within a combinatorial class
        in a consistent fashion. The colors will follow pieces as they move down the board in the 
        recursive algorithm that calcuates all states for a given combinatorial class.
    """
    board_symbols = [""] * 36
    board_colors = [""] * 36
    car_index = 0
    truck_index = 0
    board_symbols[red_car_end_a] = RED_SYMBOL
    board_symbols[red_car_end_a+1] = RED_SYMBOL
    board_colors[red_car_end_a] = RED_COLOR
    board_colors[red_car_end_a+1] = RED_COLOR
    board_string_split = [ board_bit_string[i:i+3] for i in range(0,108,3)]
    for i in range(36):
        if board_symbols[i] == "":
            
            # empty piece
            if board_string_split[i] == "000":
                board_colors[i] = BLANK_COLOR

            # vertical car
            if board_string_split[i] == "001":
                board_symbols[i]   = car_symbols[car_index]
                board_symbols[i+6] = car_symbols[car_index]
                board_colors[i]    = car_colors[car_index]
                board_colors[i+6]  = car_colors[car_index]
                car_index = car_index + 1

            # vertical truck
            if board_string_split[i] == "010":
                board_symbols[i] = truck_symbols[truck_index]
                board_symbols[i+6] = truck_symbols[truck_index]
                board_symbols[i+12] = truck_symbols[truck_index]
                board_colors[i] = truck_colors[truck_index]
                board_colors[i+6] = truck_colors[truck_index]
                board_colors[i+12] = truck_colors[truck_index]
                truck_index = truck_index + 1

            # horizontal car
            if board_string_split[i] == "011":
                board_symbols[i] = car_symbols[car_index]
                board_symbols[i+1] = car_symbols[car_index]
                board_colors[i] = car_colors[car_index]
                board_colors[i+1] = car_colors[car_index]
                car_index = car_index + 1

            # horizontal truck
            if board_string_split[i] == "100":
                board_symbols[i] = truck_symbols[truck_index]
                board_symbols[i+1] = truck_symbols[truck_index]
                board_symbols[i+2] = truck_symbols[truck_index]
                board_colors[i] = truck_colors[truck_index]
                board_colors[i+1] = truck_colors[truck_index]
                board_colors[i+2] = truck_colors[truck_index]
                truck_index = truck_index + 1

    html_data = zip(board_colors, board_symbols)
    html_cells = ['<td bgcolor="%s" style="width:30px; height:30px; vertical-align:middle; text-align:center">%s</td>' %x for x in html_data]
    return '<table>' + ''.join(['<tr>' + ''.join(html_cells[i:i+6]) + '</tr>'  for i in range(0,35,6)]) + '</table>'
    #return  board_string_split

	
def html_table_for_bit_string_game_coloring(board_bit,red_car_end_a):
    pass

    
    
    
    
    
    


