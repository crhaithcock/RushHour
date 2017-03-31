

"""

A collection of states as defined by the cards available in the board game.

"""
from State import State

#######################################
#
#    Original Set - Beginner Level
#
#########################################
state_dict = {'board_top_hash':int('011011000000000100100000000100000100100011011100000100', 2),\
              'board_bottom_hash':int('100000000100000000001000000000011011001000010010010000', 2),\
              'red_car_end_a':13}

GAME_001 = State(**state_dict)


state_dict = {'board_top_hash':int('001000000010010010001000000001000100011011000001001100', 2),\
              'board_bottom_hash':int('010010010000001100000000001000011011011011001011011000', 2),\
              'red_car_end_a':12}
GAME_002 = State(**state_dict)



#######################################
#
#     Original Set - Intermediate
#
#########################################


state_dict = {'board_top_hash':int('100011011100000000100000000100000000100011011100000000', 2),\
              'board_bottom_hash':int('000000001010010010000000001000000001000000010010010001', 2),\
              'red_car_end_a':13}
GAME_011 = State(**state_dict)

state_dict = {'board_top_hash':int('001011011000000100001000100000000100011011100000000100', 2),\
              'board_bottom_hash':int('000000100010010010000000000000001000010010010000001000', 2),\
              'red_car_end_a':12}
GAME_012 = State(**state_dict)



#######################################
#
#     Original Set - Advanced
#
#########################################


state_dict = {'board_top_hash':int('011011001100000000100000001100000000100011011100000000',2), 'board_bottom_hash':int('100010010010000000000000000000000000000000000010010010',2), 'red_car_end_a':13 }
GAME_021 = State(**state_dict)

state_dict = {'board_top_hash':int('000000001010010010001000001100011011001011011100000000',2), 'board_bottom_hash':int('000001000100011011001001011011000001001010010010000001',2), 'red_car_end_a':13 }
GAME_022 = State(**state_dict)



#######################################
#
#     Original Set - Expert
#
#########################################


state_dict = {'board_top_hash':int('011011000010010010000000000001011011001011011001000100',2), 'board_bottom_hash':int('001000100011011100011011100000000100000000100010010010',2), 'red_car_end_a':13 }
GAME_031 = State(**state_dict)


