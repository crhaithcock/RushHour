

/*

    We want a set with the structure of the puzzle_state_transition_table 
        (puzzle id, puzzle id, piece id, piece id)

    We only want 4-tuples that represent legitimate state transitions.

    The logic below is based on the following observation.
    A transition exists between two puzzle states x and y iff
        1. x has 1 piece placement x' not in y
        2. y has 1 piece placement y' not in x 
        3  x' and y' are connected through the up,down,left,right piece placement relations

    


    Logical flow of query:
    1. Pair up puzzle states x , y
    2. Get all piece placements in x that are not in y (x,y,p')
    3. Get all piece placements in y that are not in x (x,y,q')
    4. Join (x,y,p') and (x,y,q') to get (x,y,p',q') and store in temp table T

    5. grouping by x,y on T along with clause having count(1) = 1 satisfy conditions 1 and 2
    6. join T onto results from 5 and test for condition 3


    To expedite the query, we require x and y be in the same combinatorial class.
    This is a necessary condition for x~y.
    Also, rather than start with all possible pairs of puzzle states, we restrict
    ourselves to one half of the adjaceny matrix with 

*/

select  x.pre_state_id,
        x.post_state_id,
        x.piece_placement_id as x_piece_id,
        y.piece_placement_id as y_piece_id 
into #possible_edges  
from

(
select  pre_state.id as pre_state_id,
        post_state.id as post_state_id,
        map.piece_placement_id

from    puzzle_states pre_state
        join
        puzzle_states post_state
        on pre_state.id < post_state.id
           and pre_state.combinatorial_class_id = post_state.combinatorial_class_id
        join
        piece_placements_puzzle_states map
        on map.puzzle_state_id = pre_state.id

except

select  pre_state.id as pre_state_id,
        post_state.id as post_state_id,
        map.piece_placement_id

from    puzzle_states pre_state
        join
        puzzle_states post_state
        on pre_state.id < post_state.id
           and pre_state.combinatorial_class_id = post_state.combinatorial_class_id
        join
        piece_placements_puzzle_states map
        on map.puzzle_state_id = post_state.id

)x

join

(

select  pre_state.id as pre_state_id,
        post_state.id as post_state_id,
        map.piece_placement_id

from    puzzle_states pre_state
        join
        puzzle_states post_state
        on pre_state.id < post_state.id
           and pre_state.combinatorial_class_id = post_state.combinatorial_class_id
        join
        piece_placements_puzzle_states map
        on map.puzzle_state_id = post_state.id

except 

select  pre_state.id as pre_state_id,
        post_state.id as post_state_id,
        map.piece_placement_id

from    puzzle_states pre_state
        join
        puzzle_states post_state
        on pre_state.id < post_state.id
           and pre_state.combinatorial_class_id = post_state.combinatorial_class_id
        join
        piece_placements_puzzle_states map
        on map.puzzle_state_id = pre_state.id

)y
on x.pre_state_id = y.pre_state_id and x.post_state_id = y.post_state_id



--select edges.pre_state,edges.post_state,x_piece_id,y_piece_id
--select edges.post_state,edges.pre_state,y_piece_id,x_piece_id

select edges.*,x_pieces.description,y_pieces.description,x_pieces.end_a,y_pieces.end_a
from
(
select *
from
#possible_edges
)edges
join
(
select pre_state_id,post_state_id,count(1) as cnt
from #possible_edges
group by pre_state_id,post_state_id
having count(1) = 1
)y 
on edges.pre_state_id = y.pre_state_id and edges.post_state_id = y.post_state_id

join
piece_placements as x_pieces
on x_pieces.id = edges.x_piece_id

join
piece_placements as y_pieces
on y_pieces.id = edges.y_piece_id

where   y_piece_id in 
        (   x_pieces.left_piece_placement_id,
            x_pieces.right_piece_placement_id,
            x_pieces.up_piece_placement_id,
            x_pieces.down_piece_placement_id
         )
order by edges.pre_state_id



