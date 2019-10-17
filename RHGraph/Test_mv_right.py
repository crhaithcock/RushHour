# -*- coding: utf-8 -*-
"""
Created on Sun Aug 18 21:22:38 2019

@author: CHaithcock
"""

import RHState

s1 = RHState.RHState(int('110110000000100101101000000000100101101110110000000101101000000110110000100111111111000000100000000111111111',2),13)


nbrs = list(s1.neighbors_right())

print(s1._board)

print(nbrs[0]._board)