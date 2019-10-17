# -*- coding: utf-8 -*-
"""
Created on Tue Oct  8 20:06:18 2019

@author: CHaithcock
"""


import numpy as np


import sys
sys.path.insert(1, 'C:/Users/chaithcock/Documents/repos/RushHour/RHGraph')

import RHState
import RHComponent

r1 = [6,6,0,0,6,6]
r2 = [0,0,0,0,0,0]
r3 = [0,0,6,6,0,0]
r4 = [0,0,0,0,0,0]
r5 = [0,0,0,0,0,0]
r6 = [0,0,0,0,0,0]
board = np.array( [r1,r2,r3,r4,r5,r6 ] )

s = RHState.RHState(board,14)

c = RHComponent.RHComponent.from_state(s)

g = c.nxGraph

c._init_svg()


nbr_centers = c._svg_nbhd_nbr_centers


def svg_nbrhd(component):
    pass


    
    



def svg_circles():

    nbhd_r = 150
    nbhd_cx = 325
    nbhd_cy = 250
    
    max_vert_nbrs = 7
    max_nbrs = 11
    max_horz_nbrs = max_nbrs - max_vert_nbrs
    
    
    if max_vert_nbrs == 0:
        up_centers = []
        down_centers = []
        
    else:
        # if verts is odd
        if max_vert_nbrs % 2 != 0:
            offset = (max_vert_nbrs- 1) / 2.0
        else:
            offset = max_vert_nbrs / 2 -.5
        thetas_up = np.array(np.arange(max_vert_nbrs)) - offset
    
        thetas_up_arc = .8 * ( ( (max_vert_nbrs/max_nbrs) * np.pi ) )
        thetas_up_delta = thetas_up_arc / max_vert_nbrs
    
        thetas_up = thetas_up * thetas_up_delta + np.pi/2
    
        up_x = nbhd_r * np.cos(thetas_up) 
        up_y = nbhd_r * np.sin(thetas_up)  
        up_centers = np.array(list(zip(up_x,up_y)))
        
        down_x = up_x
        down_y = up_y * -1
        down_centers = np.array(list(zip(down_x,down_y)))
    
    if max_horz_nbrs == 0:
        left_centers = []
        right_centers = []
    else:
        
        # if verts is odd
        if max_horz_nbrs % 2 != 0:
            offset = (max_horz_nbrs- 1) / 2.0
        else:
            offset = max_horz_nbrs / 2 -.5
        thetas_left = np.array(np.arange(max_horz_nbrs)) - offset
    
        thetas_left_arc = .8 * ( ( (max_horz_nbrs/max_nbrs) * np.pi ) )
        thetas_left_delta = thetas_left_arc / max_horz_nbrs
    
        thetas_left = thetas_left * thetas_left_delta + np.pi
    
        left_x = nbhd_r * np.cos(thetas_left) 
        left_y = nbhd_r * np.sin(thetas_left)  
        left_centers = np.array(list(zip(left_x,left_y)))
    
        right_x = left_x * -1
        right_y = left_y
        right_centers = np.array(list(zip(right_x,right_y)))
    
    
    
    center = '<circle cx="0" cy="0" r="10" style="fill: red"/>'
    
    vert_prototype = '<circle cx="0" cy="0" r="10" style="fill: #7FFF00"/>'
    horz_prototype = '<circle cx="0" cy="0" r="10" style="fill: #1E90FF"/>'
        
    svg = '<svg width="750" height="500" style="background: grey">'
    svg = svg + '<g transform="translate(%f,%f) scale(1,-1)">' %(nbhd_cx,nbhd_cy)
    
    for x,y in np.concatenate((up_centers,left_centers,down_centers,right_centers)):
        svg = svg + '<line x1="0" y1 ="0" x2="%f" y2="%f" stroke="black"/>'%(x,y)
        
    svg = svg + center
    for x,y in up_centers:
        svg = svg + '<g transform="translate(%f,%f)">'%(x,y)
        svg = svg + vert_prototype
        svg = svg + '</g>'
    for x,y in left_centers:
        svg = svg + '<g transform="translate(%f,%f)">'%(x,y)
        svg = svg + horz_prototype
        svg = svg + '</g>'
    for x,y in down_centers:
        svg = svg + '<g transform="translate(%f,%f)">'%(x,y)
        svg = svg + vert_prototype
        svg = svg + '</g>'
    for x,y in right_centers:
        svg = svg + '<g transform="translate(%f,%f)">'%(x,y)
        svg = svg + horz_prototype
        svg = svg + '</g>'
    
    svg = svg + '</g>'
    svg = svg + '</svg>'

    return(svg)