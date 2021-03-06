import numpy as np
import RHConstants as const


vec_bitstring_3 = np.vectorize(lambda x: np.binary_repr(x,width=3) )


def board_to_int(v):
    t = vec_bitstring_3(v)
    return int(''.join(np.apply_along_axis(lambda x: ''.join(x), 1,t)),2)

def int_to_board(i):
    #i = '154444257952488798331863040'
    s = bin(int(i))[2:].zfill(108)
    v = np.array([int(s[i:i+3],2) for i in range(0,len(s),3)],dtype=int)
    return v.reshape((6,6))

def split_int(i):
    s = bin(int(i))[2:].zfill(108)
    s1 = s[:54]
    s2 = s[54:]
    i1 = int(s1,2)
    i2 = int(s2,2)
    return (i1,i2)

def combine_ints(i1,i2):
    s1 = bin(int(i1))[2:].zfill(54) 
    s2 = bin(int(i2))[2:].zfill(54) 
    return int(s1+s2,2)

def comb_class(num_cars, num_trucks):
    return 2**num_cars * 3**num_trucks

def flip_board(v):
    ret np.flip(v,1)

def comb_class(v):
    num_cars = np.size(v[v==const.VERTICAL_CAR]) + np.size(v[v==const.HORIZONTAL_CAR])
    num_trucks = np.size(v[v==const.VERTICAL_TRUCK]) + np.size(v[v==const.HORIZONTAL_TRUCK])

    return 2**num_cars * 3**num_trucks
