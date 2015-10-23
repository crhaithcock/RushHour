'''
Created on Jun 8, 2015

@author: cliff
'''

from constants import *
from utilities import *

def html_table_array_for_state_data_component_coloring(data):
   
    html_tables = ['<td>' + html_table_for_state_data_component_coloring(x[0],x[1],x[2]) + '</td>' for x in data] 
    
    if len(html_tables) > 4:
        rows = [ html_tables[4*i:4*i+4] for i in range(len(html_tables)/4)]
        if len(html_tables) % 4 != 0:
            rows.append(html_tables[-(len(html_tables)%4):])
    else:
        rows = [html_tables]
    
    return '<table>' + ''.join(['<tr>' + ''.join(x) + '</tr>' for x in rows]) + '</table'


def html_table_array_for_board_array_component_coloring(data):
      
    html_tables = ['<td>' + html_table_for_board_array_component_coloring(x[0],x[1]) + '</td>' for x in data]
    
    rows = [ html_tables[4*i:4*i+4] for i in range(len(html_tables)/4)]
    if len(html_tables) % 4 != 0:
        rows.append(html_tables[-(len(html_tables)%4):])
    
    return '<table>' + ''.join(['<tr>' + ''.join(x) + '</tr>' for x in rows]) + '</table'
    
    

def html_table_for_state_data_component_coloring(top_hash_int,bottom_hash_int,red_car_end_a):
    board_bit_string = from_two_ints_to_bit_string(top_hash_int,bottom_hash_int)
    return html_table_for_board_bit_string_component_coloring(board_bit_string,red_car_end_a)



def html_table_for_df_index_component_coloring(df_game_states, index):
    top_int = df_game_states['game_hash_top'][index]
    bottom_int = df_game_states['game_hash_bottom'][index]
    board_bit_string = from_two_ints_to_bit_string(top_int, bottom_int)
    red_car_end_a = df_game_states['red_car_end_a'][index]
    return html_table_for_board_bit_string_component_coloring(board_bit_string, red_car_end_a)



def html_table_for_board_array_component_coloring(board_array,red_car_end_a):
    return html_table_for_board_bit_string_component_coloring(from_array_to_bit_string(board_array), red_car_end_a)

# !!!! TODO Complete this method and the then the layers that will call this
def html_table_for_board_bit_string_component_coloring(board_bit_string,red_car_end_a):
    board_symbols = [""] * 36
    board_colors = [BLANK_COLOR] * 36
    car_index = 0
    truck_index = 0
    
    board_symbols[red_car_end_a] = RED_SYMBOL
    board_symbols[red_car_end_a+1] = RED_SYMBOL
    board_colors[red_car_end_a] = RED_COLOR
    board_colors[red_car_end_a+1] = RED_COLOR
    
    data = zip(range(36),[ board_bit_string[i:i+3] for i in range(0,108,3)])
    verticals = sorted([x for x in data if x[1] in [VERTICAL_CAR,VERTICAL_TRUCK]], key=lambda x: x[0])
    
    horizontals = sorted([x for x in data if x[1] in [HORIZONTAL_CAR,HORIZONTAL_TRUCK]], key=lambda x:x[0])
    
    for x in verticals:
        if board_colors[x[0]] == BLANK_COLOR:
            if x[1] == VERTICAL_CAR:
                board_colors[x[0]]          = car_colors[car_index]
                board_colors[x[0] + 6 ]     = car_colors[car_index]
                board_symbols[x[0]]         = car_symbols[car_index]
                board_symbols[x[0] + 6]     = car_symbols[car_index]
                car_index +=1
                
            if x[1] == VERTICAL_TRUCK:
                board_colors[x[0]]          = truck_colors[truck_index]
                board_colors[x[0] + 6 ]     = truck_colors[truck_index]
                board_colors[x[0] + 12 ]    = truck_colors[truck_index]
                board_symbols[x[0]]         = truck_symbols[truck_index]
                board_symbols[x[0] + 6]     = truck_symbols[truck_index]
                board_symbols[x[0] + 12]    = truck_symbols[truck_index]
                truck_index += 1
    
    for x in horizontals:
        if board_colors[x[0]] == BLANK_COLOR:
            if x[1] == HORIZONTAL_CAR:
                board_colors[x[0]]          = car_colors[car_index]
                board_colors[x[0] + 1 ]     = car_colors[car_index]
                board_symbols[x[0]]         = car_symbols[car_index]
                board_symbols[x[0] + 1]     = car_symbols[car_index]
                car_index +=1
                
            if x[1] == HORIZONTAL_TRUCK:
                board_colors[x[0]]          = truck_colors[truck_index]
                board_colors[x[0] + 1 ]     = truck_colors[truck_index]
                board_colors[x[0] + 2 ]     = truck_colors[truck_index]
                board_symbols[x[0]]         = truck_symbols[truck_index]
                board_symbols[x[0] + 1]     = truck_symbols[truck_index]
                board_symbols[x[0] + 2]     = truck_symbols[truck_index]
                truck_index +=1

    html_data = zip(board_colors, board_symbols)
    html_cells = ['<td bgcolor="%s" style="width:30px; height:30px; vertical-align:middle; text-align:center">%s</td>' %x for x in html_data]
    return '<table>' + ''.join(['<tr>' + ''.join(html_cells[i:i+6]) + '</tr>'  for i in range(0,35,6)]) + '</table>'
    #return  board_string_split
    
    

def html_table_for_board_array_construction_coloring(board_array,red_car_end_a):
    return html_table_for_board_bit_string_construction_coloring(from_array_to_bit_string(board_array),red_car_end_a)


    
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


def html_table_for_df_index_construction_coloring(df_game_states, index):
    top_int = df_game_states['game_hash_top'][index]
    bottom_int = df_game_states['game_hash_bottom'][index]
    board_bit_string = from_two_ints_to_bit_string(top_int, bottom_int)
    red_car_end_a = df_game_states['red_car_end_a'][index]
    return html_table_for_board_bit_string_construction_coloring(board_bit_string, red_car_end_a)






############################################################
#
#
#    TEST Code - 
#
#
############################################################
