# -*- coding: utf-8 -*-
"""
Created on Fri Oct  4 16:56:20 2019

@author: CHaithcock
"""

import sys
sys.path.insert(1, 'C:/Users/chaithcock/Documents/repos/RushHour/RHGraph')


import RHConstants as const


'''
Constants for Toplogical Combinatorial Constructions.

'''

STRIPS = ['C','CC','CCC','CT','TC','T','TT']
SLOTS = range(12)
EXIT_SLOT = 2
ROW_SLOTS = SLOTS[:6]
COL_SLOTS = SLOTS[6:]

HORZ_STRIPS = {}
HORZ_STRIPS['C'] =  []
HORZ_STRIPS['C'].append([const.HORIZONTAL_CAR,const.HORIZONTAL_CAR,0,0,0,0])
HORZ_STRIPS['C'].append([0,const.HORIZONTAL_CAR,const.HORIZONTAL_CAR,0,0,0])
HORZ_STRIPS['C'].append([0,0,const.HORIZONTAL_CAR,const.HORIZONTAL_CAR,0,0])
HORZ_STRIPS['C'].append([0,0,0,const.HORIZONTAL_CAR,const.HORIZONTAL_CAR,0])
HORZ_STRIPS['C'].append([0,0,0,0,const.HORIZONTAL_CAR,const.HORIZONTAL_CAR])

HORZ_STRIPS['CC'] = []
HORZ_STRIPS['CC'].append([const.HORIZONTAL_CAR,const.HORIZONTAL_CAR,const.HORIZONTAL_CAR,const.HORIZONTAL_CAR,0,0])
HORZ_STRIPS['CC'].append([const.HORIZONTAL_CAR,const.HORIZONTAL_CAR,0,const.HORIZONTAL_CAR,const.HORIZONTAL_CAR,0])
HORZ_STRIPS['CC'].append([const.HORIZONTAL_CAR,const.HORIZONTAL_CAR,0,0,const.HORIZONTAL_CAR,const.HORIZONTAL_CAR])
HORZ_STRIPS['CC'].append([0,const.HORIZONTAL_CAR,const.HORIZONTAL_CAR,const.HORIZONTAL_CAR,const.HORIZONTAL_CAR,0])
HORZ_STRIPS['CC'].append([0,const.HORIZONTAL_CAR,const.HORIZONTAL_CAR,0,const.HORIZONTAL_CAR,const.HORIZONTAL_CAR])
HORZ_STRIPS['CC'].append([0,0,const.HORIZONTAL_CAR,const.HORIZONTAL_CAR,const.HORIZONTAL_CAR,const.HORIZONTAL_CAR])

HORZ_STRIPS['CCC'] = [ [const.HORIZONTAL_CAR]*6 ]

HORZ_STRIPS['CT'] = []
HORZ_STRIPS['CT'].append([const.HORIZONTAL_CAR] * 2 + [const.HORIZONTAL_TRUCK] * 3 + [0] )
HORZ_STRIPS['CT'].append([const.HORIZONTAL_CAR] * 2 + [0] + [const.HORIZONTAL_TRUCK] * 3 )
HORZ_STRIPS['CT'].append([0] + [const.HORIZONTAL_CAR] * 2 + [const.HORIZONTAL_TRUCK] * 3 )

HORZ_STRIPS['TC'] = []
HORZ_STRIPS['TC'].append([const.HORIZONTAL_TRUCK] * 2 + [const.HORIZONTAL_CAR] * 3 + [0] )
HORZ_STRIPS['TC'].append([const.HORIZONTAL_TRUCK] * 2 + [0] + [const.HORIZONTAL_CAR] * 3 )
HORZ_STRIPS['TC'].append([0] + [const.HORIZONTAL_TRUCK] * 2 + [const.HORIZONTAL_CAR] * 3 )

HORZ_STRIPS['T'] = []
HORZ_STRIPS['T'].append([const.HORIZONTAL_TRUCK,const.HORIZONTAL_TRUCK,const.HORIZONTAL_TRUCK,0,0,0])
HORZ_STRIPS['T'].append([0,const.HORIZONTAL_TRUCK,const.HORIZONTAL_TRUCK,const.HORIZONTAL_TRUCK,0,0])
HORZ_STRIPS['T'].append([0,0,const.HORIZONTAL_TRUCK,const.HORIZONTAL_TRUCK,const.HORIZONTAL_TRUCK,0])
HORZ_STRIPS['T'].append([0,0,0,const.HORIZONTAL_TRUCK,const.HORIZONTAL_TRUCK,const.HORIZONTAL_TRUCK])

HORZ_STRIPS['TT'] = [[const.HORIZONTAL_TRUCK]*6]


VERT_STRIPS = {}
VERT_STRIPS['C'] =  []
VERT_STRIPS['C'].append([const.VERTICAL_CAR,const.VERTICAL_CAR,0,0,0,0])
VERT_STRIPS['C'].append([0,const.VERTICAL_CAR,const.VERTICAL_CAR,0,0,0])
VERT_STRIPS['C'].append([0,0,const.VERTICAL_CAR,const.VERTICAL_CAR,0,0])
VERT_STRIPS['C'].append([0,0,0,const.VERTICAL_CAR,const.VERTICAL_CAR,0])
VERT_STRIPS['C'].append([0,0,0,0,const.VERTICAL_CAR,const.VERTICAL_CAR])

VERT_STRIPS['CC'] = []
VERT_STRIPS['CC'].append([const.VERTICAL_CAR,const.VERTICAL_CAR,const.VERTICAL_CAR,const.VERTICAL_CAR,0,0])
VERT_STRIPS['CC'].append([const.VERTICAL_CAR,const.VERTICAL_CAR,0,const.VERTICAL_CAR,const.VERTICAL_CAR,0])
VERT_STRIPS['CC'].append([const.VERTICAL_CAR,const.VERTICAL_CAR,0,0,const.VERTICAL_CAR,const.VERTICAL_CAR])
VERT_STRIPS['CC'].append([0,const.VERTICAL_CAR,const.VERTICAL_CAR,const.VERTICAL_CAR,const.VERTICAL_CAR,0])
VERT_STRIPS['CC'].append([0,const.VERTICAL_CAR,const.VERTICAL_CAR,0,const.VERTICAL_CAR,const.VERTICAL_CAR])
VERT_STRIPS['CC'].append([0,0,const.VERTICAL_CAR,const.VERTICAL_CAR,const.VERTICAL_CAR,const.VERTICAL_CAR])

VERT_STRIPS['CCC'] = [ [const.VERTICAL_CAR]*6 ]

VERT_STRIPS['CT'] = []
VERT_STRIPS['CT'].append([const.VERTICAL_CAR] * 2 + [const.VERTICAL_TRUCK] * 3 + [0] )
VERT_STRIPS['CT'].append([const.VERTICAL_CAR] * 2 + [0] + [const.VERTICAL_TRUCK] * 3 )
VERT_STRIPS['CT'].append([0] + [const.VERTICAL_CAR] * 2 + [const.VERTICAL_TRUCK] * 3 )

VERT_STRIPS['TC'] = []
VERT_STRIPS['TC'].append([const.VERTICAL_TRUCK] * 2 + [const.VERTICAL_CAR] * 3 + [0] )
VERT_STRIPS['TC'].append([const.VERTICAL_TRUCK] * 2 + [0] + [const.VERTICAL_CAR] * 3 )
VERT_STRIPS['TC'].append([0] + [const.VERTICAL_TRUCK] * 2 + [const.VERTICAL_CAR] * 3 )

VERT_STRIPS['T'] = []
VERT_STRIPS['T'].append([const.VERTICAL_TRUCK,const.VERTICAL_TRUCK,const.VERTICAL_TRUCK,0,0,0])
VERT_STRIPS['T'].append([0,const.VERTICAL_TRUCK,const.VERTICAL_TRUCK,const.VERTICAL_TRUCK,0,0])
VERT_STRIPS['T'].append([0,0,const.VERTICAL_TRUCK,const.VERTICAL_TRUCK,const.VERTICAL_TRUCK,0])
VERT_STRIPS['T'].append([0,0,0,const.VERTICAL_TRUCK,const.VERTICAL_TRUCK,const.VERTICAL_TRUCK])

VERT_STRIPS['TT'] = [[const.VERTICAL_TRUCK]*6]


