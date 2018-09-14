
import numpy as np 
from numpy_display import *
from numpy_utilities import *
from constants import *


#!!!! TODO - return lists of up, down, left, right to assist with drawing a neighborhood

def state_nbrs(t,red_col):
    '''
       Compute all neighbrs via legal moves in the rush hour puzzle.

       Input: integer representing a legal configuration of pieces on the rush hour puzzle board.

       output: set of 2-tuples (x,red_col):
               x: integer represenation of of the (6,6) ndarray
               red_col: the rightmost column covered by the red car
    '''
        

    ret = set()
    mv_right = set()
    mv_left = set()
   
    mv_up = set()
    mv_down = set()
   
    v = int_to_board(t)
    red_cols = [red_col-1,red_col]

    # Move right
    mv_x = -v + np.roll(v,1,1)
    mv_x = mv_x[:,1:]

    mv_car = np.where(mv_x==hcar)
    mv_truck = np.where(mv_x ==htruck)

    mv_right_car = list(zip(mv_car[0],mv_car[1]))
    mv_right_truck = list(zip(mv_truck[0], mv_truck[1]))

    for x,y in mv_right_car:
        new = np.copy(v)
        new[x,y+1] = hcar
        new[x,y-1] = blank
        if x == 2 and ( y ==red_col-1 or y == red_col ):
            mv_right.add( (board_to_int(new),y+1) ) 
        else:
            mv_right.add( (board_to_int(new),red_col) )

    for x,y in mv_right_truck:
        new = np.copy(v)
        new[x,y+1] = htruck
        new[x,y-2] = blank
        mv_right.add( (board_to_int(new),red_col) )

    ret.update(mv_right)
        

    # Move Left
    mv_x = -v + np.roll(v,-1,1)
    mv_x = mv_x[:,:5]

    mv_car = np.where(mv_x==hcar)
    mv_truck = np.where(mv_x ==htruck)

    mv_left_car = list(zip(mv_car[0],mv_car[1]))
    mv_left_truck = list(zip(mv_truck[0], mv_truck[1]))

    for x,y in mv_left_car:
        new = np.copy(v)
        new[x,y] = hcar
        new[x,y+2] = blank
        if x == 2 and y+2 in red_cols:
            mv_left.add( (board_to_int(new),y+1) ) 
        else:
            mv_left.add( (board_to_int(new),red_col) )

    for x,y in mv_left_truck:
        new = np.copy(v)
        new[x,y] = htruck
        new[x,y+3] = blank
        mv_left.add( (board_to_int(new),red_col) )

    ret.update(mv_left)

    # Move up
    
    mv_x = -v + np.roll(v,-1,0)
    mv_x = mv_x[:5]

    mv_car = np.where(mv_x==vcar)
    mv_truck = np.where(mv_x ==vtruck)

    mv_up_car = list(zip(mv_car[0],mv_car[1]))
    mv_up_truck = list(zip(mv_truck[0], mv_truck[1]))


    for x,y in mv_up_car:
        new = np.copy(v)
        new[x,y] = vcar
        new[x+2,y] = blank
        mv_up.add( (board_to_int(new),red_col) )

    for x,y in mv_up_truck:
        #x,y = mv_up_truck[0]
        new = np.copy(v)
        new[x,y] = vtruck
        new[x+3,y] = blank
        mv_up.add( (board_to_int(new),red_col) )

    ret.update(mv_up)


    # move down
    mv_x = -v + np.roll(v,1,0)
    mv_x = mv_x[1:]
                
    mv_car = np.where(mv_x==vcar)
    mv_truck = np.where(mv_x ==vtruck)

    mv_down_car = list(zip(mv_car[0],mv_car[1]))
    mv_down_truck = list(zip(mv_truck[0], mv_truck[1]))

    for x,y in mv_down_car:
        new = np.copy(v)
        new[x+1,y] = vcar
        new[x-1,y] = blank
        mv_down.add( (board_to_int(new),red_col) )

    for x,y in mv_down_truck:
        new = np.copy(v)
        new[x+1,y] = vtruck
        new[x-2,y] = blank
        mv_down.add( (board_to_int(new),red_col) )

    ret.update(mv_down)

    # the order of right, up, left, down influenced by convetions of polor coordinates and trig
    return (ret,mv_right,mv_up,mv_left,mv_down)


if __name__ == "__main__":

    v1 = np.array([blank]*36).reshape(6,6)

    v1[2,3:5] = hcar
    v1[4,1:3] = hcar
    #v1[2:4,0] = vcar
    #v1[3:,5] = vtruck

    dwg = svg_neighborhood(board_to_int(v1),1)
    #HTML(dwg.tostring())    


    