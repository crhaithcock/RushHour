

select *

from
     (puzzle_states as x ,
      puzzle_states as y
     )
     
     join
     piece_placements_puzzle_states x_join
     on x.id = x_join.puzzle_state_id

     join
     piece_placements x_pieces
     on x_join.piece_placement_id = x_pieces.id
     
     join
     piece_placements_puzzle_states y_join
     on y.id = y_join.puzzle_state_id
     
     left join
     piece_placements y_pieces
     on y_join.piece_placement_id = y.id and
        x_pieces.id = y_pieces.id

where x.id < y.id and y_pieces.id is null

order by x.id






