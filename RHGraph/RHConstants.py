# -*- coding: utf-8 -*-
"""
Created on Tue Jun 25 09:09:18 2019

@author: CHaithcock
"""



CAR_SYMBOLS = ['Q', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'L']
TRUCK_SYMBOLS = ['T', 'R', 'W', 'Z']

CAR_COLORS_RGB = ['7FFF00', '7FFFD4', 'D2691E', '8B008B', 'BDB76B',\
                  '8B0000', 'FF1493', '1E90FF', 'FFD700', 'ADFF2F', \
                  'CD5C5C', 'F0E68C']

TRUCK_COLORS_RGB = ['F08080', 'FFA07A', 'FF00FF', '00FA9A']


RED_COLOR_RGB = 'FF0000'
RED_SYMBOL = 'X'

BLANK_COLOR_RGB = "E6E6E6"


# For numpy implementation, want to use matrix math to apply the rules of the 
# puzzle. So, we need to space the codes for spaces such that the sum of any
# non-blank codes is not another code value. That is, for some z in the code
# space, x + y = z implies x or y is 0


"""
The choice for constants here satisfies several constraints.

* Minimize number of bits required to store the board as an integer.

* Spaced apart such that for any z from below, z = x + y implies x or y is zero.

   This requirement is especially useful for allowing certain numpy matrix operations
   to model the rules of game play efficiently.

"""

BLANK_SPACE = 0

HORIZONTAL_CAR = 6
HORIZONTAL_TRUCK = 7

VERTICAL_CAR = 4
VERTICAL_TRUCK = 5









