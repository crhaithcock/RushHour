
import numpy as np
import math
import svgwrite
import networkx as nx


import RHConstants as const
import RHneighbors as nbrs

# Jupyter notebook needs to include the following lines in order to render SVG within a cell:


#from IPython.display import SVG
#from IPython.display import HTML

#


space_size = 30
board_size = 6 * space_size
svg_border = 3 
svg_round_radius = 5

svg_size = {}
svg_size['hcar'] = (2*space_size - 2*svg_border , space_size - 2*svg_border)
svg_size['vcar'] = (space_size - 2*svg_border,  2*space_size - 2*svg_border)
svg_size['vtruck'] = (space_size - 2*svg_border , 3*space_size - 2*svg_border)
svg_size['htruck'] = (3*space_size - 2*svg_border, space_size - 2*svg_border)

CAR_COLORS = const.CAR_COLORS_WITH_HASH[:]
TRUCK_COLORS = const.TRUCK_COLORS_WITH_HASH[:]
RED_COLOR = const.RED_COLOR_WITH_HASH
blank_color = const.BLANK_COLOR_WITH_HASH



def svg_base():
    dwg = svgwrite.Drawing('nosave.svg',(board_size,board_size),debug=True)

    dwg.add(dwg.rect(insert=(0,0),size=(board_size,board_size),fill=blank_color))
    #dwg.add(dwg.rect(insert=(0,0),size=(board_size,board_size),fill='rgb(211,211,211)'))
    for x in range(7):
        dwg.add(dwg.line((30*x,0),(30*x,180),stroke='black',stroke_width=2))
        dwg.add(dwg.line((0,30*x),(180,30*x),stroke='black',stroke_width=2))
    return dwg



#dwg.add(dwg.rect(insert=(65, 35), size=(50, 20),rx=5,ry=5,fill='green',  stroke_width=3))
def svg_add_piece(dwg,nd_x,nd_y,orientation,color,text):
    car_x = nd_y* space_size + svg_border
    car_y = nd_x*space_size + svg_border
    
    size = svg_size[orientation]
    
    dwg.add(dwg.rect(insert=(car_x,car_y),size=size,rx=svg_round_radius,ry=svg_round_radius,fill=color, stroke_width=3))
    
    c_x = car_x + size[0]/2.0
    c_y = car_y + size[1]/2.0
    dwg.add(dwg.text(text,insert=(c_x,c_y),style='fill:black;text-anchor:middle;alignment-baseline:central'))
    return dwg




def svg_from_state(t,red_col):
    ''' 
        input t: integer representing a legal RH board configuration
        input red_col: rightmost column covered by the red car 

        output: instance of svgwrite drawing
        
    '''
    
    v = int_to_board(t)

    c2 = int(red_col)
    c1 = int(c2 - 1)



    car_colors = CAR_COLORS[:]
    truck_colors = TRUCK_COLORS[:]
    
    truck_symbols = TRUCK_SYMBOLS[:]
    car_symbols = CAR_SYMBOLS[:]

    dwg = svg_base()
    
    # zero out red car. We explicitly know how to mark it visually
    v[2,c1] = blank
    v[2,c2] = blank
    dwg = svg_add_piece(dwg,2,c1,'hcar',RED_COLOR,RED_SYMBOL)
    
    vcars_y =np.unique(np.where(v==vcar)[1])
    for y in vcars_y:
        for x in np.where(v[:,y] == vcar)[0][0::2]:          
            dwg = svg_add_piece(dwg,int(x),int(y),'vcar',car_colors.pop(),car_symbols.pop())
    
    hcars_x = np.unique(np.where(v==hcar)[0])
    for x in hcars_x:
        for y in np.where(v[x,:]==hcar)[0][0::2]:
            dwg = svg_add_piece(dwg,int(x),int(y),'hcar',car_colors.pop(),car_symbols.pop())
    
    vtrucks_y = np.unique(np.where(v==vtruck)[1])
    for y in vtrucks_y:
        for x in np.where(v[:,y] == vtruck)[0][0::3]:
            dwg = svg_add_piece(dwg,int(x),int(y),'vtruck',truck_colors.pop(),truck_symbols.pop())
    
    htrucks_x = np.unique(np.where(v==htruck)[0])
    for x in htrucks_x:
        for y in np.where(v[x,:]==htruck)[0][0::3]:
            dwg = svg_add_piece(dwg,int(x),int(y),'htruck',truck_colors.pop(),truck_symbols.pop())
    
    return dwg.tostring()



def svg_from_state_generated_order(t,red_col):
    '''
        Two natural orders to the nodes:
            1. state generation (watch a piece walk down the board)
                - linear mapping down the board range(36)
   
            2. game order (colors match neighbors in a presntation of the RH Graph)
                - order rows and color horiztonal pieces
                - order cols and color vertical pieces
                
    '''
    v = int_to_board(t)

    c2 = red_col
    c1 = c2 - 1

    car_colors = CAR_COLORS[:]
    truck_colors = TRUCK_COLORS[:]

    truck_symbols = TRUCK_SYMBOLS[:]
    car_symbols = CAR_SYMBOLS[:]

    dwg = svg_base()

    # zero out red car. We explicitly know how to mark it visually
    v[2,c1] = blank
    v[2,c2] = blank
    dwg = svg_add_piece(dwg,2,c1,'hcar',RED_COLOR_WITH_HASH,RED_SYMBOL)

    end_positions = []
    
    vcars_y =np.unique(np.where(v==vcar)[1])
    for y in vcars_y:
        for x in np.where(v[:,y] == vcar)[0][0::2]:          
            #dwg = svg_add_piece(dwg,int(x),int(y),'vcar',car_colors.pop(),car_symbols.pop())
            end_positions.append([int(x),int(y)])

    hcars_x = np.unique(np.where(v==hcar)[0])
    for x in hcars_x:
        for y in np.where(v[x,:]==hcar)[0][0::2]:
            #dwg = svg_add_piece(dwg,int(x),int(y),'hcar',car_colors.pop(),car_symbols.pop())
            end_positions.append([int(x),int(y)])

    vtrucks_y = np.unique(np.where(v==vtruck)[1])
    for y in vtrucks_y:
        for x in np.where(v[:,y] == vtruck)[0][0::3]:
            #dwg = svg_add_piece(dwg,int(x),int(y),'vtruck',truck_colors.pop(),truck_symbols.pop())
            end_positions.append([int(x),int(y)])

    htrucks_x = np.unique(np.where(v==htruck)[0])
    for x in htrucks_x:
        for y in np.where(v[x,:]==htruck)[0][0::3]:
            #dwg = svg_add_piece(dwg,int(x),int(y),'htruck',truck_colors.pop(),truck_symbols.pop())
            end_positions.append([int(x),int(y)])

    end_positions = sorted(end_positions)
    for row,col in end_positions:
        if v[row,col] == hcar:
            dwg = svg_add_piece(dwg,int(row),int(col),'hcar',car_colors.pop(),car_symbols.pop() )
        elif v[row,col] == vcar:
            dwg = svg_add_piece(dwg,int(row),int(col),'vcar',car_colors.pop(),car_symbols.pop() )
        elif v[row,col] == htruck:
            dwg = svg_add_piece(dwg,int(row),int(col),'htruck',truck_colors.pop(),truck_symbols.pop() )
        else:
            dwg = svg_add_piece(dwg,int(row),int(col),'vtruck',truck_colors.pop(),truck_symbols.pop() )
    return dwg


def svg_neighborhood(v,red_col):
    ''''
        Input: v: integer encoding of ndarray
               red_col: rightmost column (0...5) covered by the red car

        Ouptput:    string consisting of svg markup


    '''


    (all_nbrs,right_nbrs,up_nbrs,left_nbrs,down_nbrs) = state_nbrs(v, int(red_col) )

    ordered_nbrs = [[],[],[],[]]
    ordered_nbrs[0] = sorted(list(right_nbrs), reverse=True)
    ordered_nbrs[1] = sorted(list(up_nbrs))
    ordered_nbrs[2] = sorted(list(left_nbrs))
    ordered_nbrs[3] = sorted(list(down_nbrs))



    # use nested SVG to map these out.

    r = 200
    cx = cy = 200

    
    
    # define lower and upper bounds for 4 regions of unit circle    
    a = [-45+10,45+10,135+10,225+10]
    b = [45-10,135-10,225-10,-45-10]
    counts = [len(right_nbrs), len(up_nbrs),len(left_nbrs),len(down_nbrs)]
    nbrs_x = [ [], [], [], [] ]
    nbrs_y = [ [], [], [], [] ]

    for i in range(4):
        n = counts[i]
        if n > 0:
            c = a[i]
            d = b[i]
            denom = max(1,n-1)
            rads =  [(math.pi/180)*(c+((d-c)/(denom))*i)  for i in range(n)]
            nbrs_x[i] = [ cy + r*math.cos(rad) for rad in rads]
            nbrs_y[i] = [ cy + r*math.sin(rad) for rad in rads]
           
   
    #n = len(all_nbrs)
    #b = 360 - 360/(n-1)
    #a = 0
    #rads = [(math.pi/180)*(a+((b-a)/(n-1))*i)  for i in range(n)]
    #nbrs_x = [ cy + r*math.cos(rad) for rad in rads]
    #nbrs_y = [ cy + r*math.sin(rad) for rad in rads]

    svg = '<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="600" height="600">'

    for i in range(4):
        for j in range( counts[i]):
            x = nbrs_x[i][j]
            y = nbrs_y[i][j]
            states,red_col_y = ordered_nbrs[i][j]

            svg += '<line stroke="black" stroke-width="2" x1="%d" x2="%d" y1="%d" y2="%d" />'%(cx+45,x+45,cy+45,y+45)

            svg += '<svg x="%d" y = "%d">'%(x,y)
            svg += '<g transform = "scale(.5)">'
            svg += svg_from_state(states,red_col_y)
            svg += '</g></svg>'


    svg += '<svg x="%d" y = "%d">'%(cx,cy)
    svg += '<g transform = "scale(.5)">'
    svg += svg_from_state(v,red_col)
    svg += '</g></svg>'


    svg += '</svg>'



    return svg


def d3_graph(g):
    '''
        Input: Networkx Graph g that is a single connected component from the RH Graph.
               Assumption: every node has attribute ['isSolnNode]

        Output: graph g'
                The graph g' will be shaped to support d3 integration
                * Add node attribute 'svg' with result from svg_from_state
                * Add node attribute x,y for position within d3 svg output

                * Relabel nodes
                * Apply partition algorithm to relabeled graph
    '''
    
    ''' Algorithm Notes:

        layout constants . . .
        
        for each partition p:
            
            required parameters:
            partition_cx
            partition_cy
            radius #for circle layout per partition
            radius

            create a <g> </g>
            for each node v in p:
                node_cx = cosine function
                node_cy = cosine function
                add <circle></circle> to SVG
                
    
    Phase 1:
        Render json that can feed into d3 v4
        Mark solution nodes and render with force algorithm
    
    Phase 2:
        Add interactivity
            - node hover shows board svg
            - select node and light up solution tree
            - semantic zoom
                - full graph (nodes and links )
                - neighborhood 

    Phase 3:
        render distance partition presentation of the graph.    

    '''


    pass


def graph_json(g):
    '''
        Input: NetworkX Graph g.

        Output: string containing well-formed json representaton of g.

        Will create a new graph and peel off only those pieces needed for web presntation. Will 
        modify data strucutres as needed to faciliiate translation to json (e.g. replace sets with lists)

    '''
    g_out = nx.Graph()

    for n in g.nodes:
        g_out.add_node(n)
        g_out.nodes[n]['soln_dist'] = g.nodes[n]['soln_distance']
        if 'inner_nbrs' in g.nodes[n]:
            g_out.nodes[n]['inner_nbrs'] = list(g.nodes[n]['inner_nbrs'])
        if 'outer_nbrs' in g.nodes[n]:
            g_out.nodes[n]['outer_nbrs'] = list(g.nodes[n]['outer_nbrs'])


    g_out.add_edges_from(g.edges())

    return nx.readwrite.json_graph.node_link_data(g_out)
    