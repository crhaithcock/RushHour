'''
Created on Jun 8, 2015

@author: cliff
'''


CAR_SYMBOLS = ['Q', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'L']
TRUCK_SYMBOLS = ['T', 'R', 'W', 'Z']

CAR_COLORS_NO_HASH = ['7FFF00', '7FFFD4', 'D2691E', '8B008B', 'BDB76B',\
                      '8B0000', 'FF1493', '1E90FF', 'FFD700', 'ADFF2F', \
                      'CD5C5C', 'F0E68C']

CAR_COLORS_WITH_HASH = ['#7FFF00', '#7FFFD4', '#D2691E', '#8B008B', '#BDB76B',\
                        '#8B0000', '#FF1493', '#1E90FF', '#FFD700', '#ADFF2F',\
                        '#CD5C5C', '#F0E68C']

TRUCK_COLORS_NO_HASH = ['F08080', 'FFA07A', 'FF00FF', '00FA9A']
TRUCK_COLORS_WITH_HASH = ['#F08080', '#FFA07A', '#FF00FF', '#00FA9A']

RED_COLOR_WITH_HASH = '#FF0000'
RED_COLOR_NO_HASH = 'FF0000'

RED_SYMBOL = 'X'

BLANK_COLOR_WITH_HASH = "#E6E6E6"
BLANK_COLOR_NO_HASH = "E6E6E6"


# Topology Values
EMPTY = '000'
ONE_CAR = '001'
TWO_CAR = '010'
THREE_CAR = '011'
ONE_TRUCK = '100'
TWO_TRUCK = '110'
ONE_CAR_ONE_TRUCK = '101'
ONE_TRUCK_ONE_CAR = '111'






# relabeling: 208-08-01

# for numpy implementation, want to use matrix math. Need to contrive values such that
# for z in values, x + y = z if an only if x or y = 0.
BLANK_SPACE = '000'

HORIZONTAL_CAR = '010'
HORIZONTAL_TRUCK = '100'

VERTICAL_CAR = '011'
VERTICAL_TRUCK = '101'

blank = 0
vcar = 4
vtruck = 5
hcar = 6
htruck = 7



# Relabeling These 2017-08-28
# Coding Scheme: 
# 3-bits: x y z
# x - orientation (0 = horizontal, 1 = vertical)
# y - Truck Bit (0 = Not Truck, 1 = Truck )
# z - Car Bit (0 = Not Car, 1 = car)
# 000 - Horizontal, Not Car, Not Truck (i.e. Empty Space)


# BLANK_SPACE = '000'

# HORIZONTAL_CAR = '001'
# HORIZONTAL_TRUCK = '010'

# VERTICAL_CAR = '101'
# VERTICAL_TRUCK = '110'


# Given dependencies throughout the code base. Keeping a copy of pre-2018-08-28 values
#BLANK_SPACE = '000'
#VERTICAL_CAR = '001'
#VERTICAL_TRUCK = '010'
#HORIZONTAL_CAR = '011'
#HORIZONTAL_TRUCK = '100'







