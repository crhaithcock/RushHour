import numpy as np



vec_bitstring_3 = np.vectorize(lambda x: np.binary_repr(x,width=3) )


def board_to_int(v):
    t = vec_bitstring_3(v)
    return int(''.join(np.apply_along_axis(lambda x: ''.join(x), 1,t)),2)

def int_to_board(i):
    #i = '154444257952488798331863040'
    s = bin(int(i))[2:].zfill(108)
    v = np.array([int(s[i:i+3],2) for i in range(0,len(s),3)],dtype=int)
    return v.reshape((6,6))

