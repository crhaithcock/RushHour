    

/*
NOTES / TODO:
    wrap this logic in a proc that takes a combinatorial class is as an input -
            this will provide an encapsulation that is in parity with the node generation
            routines that build the puzzle states based on a combinatorial classes

    
    re-think the problem/variables in terms of nodes with in-edges and nodes with
            out-edges. This may be clearer than pre-state and post-state bound variable
            names. The logic is then looking for two nodes x,y such there is an out-edge from
            x to y and an in-edge from y to x.


    algorithm:
    
    out-edges:
    build pairs of puzzle states (x,y)
    for each pair, build a list of pieces that are in x but not in y

    
    in-edges:
    build


*/


declare @comb_class_id int
set @comb_class_id = 4

if OBJECT_ID('tempdb..#base_state_one_mismatched_piece') is not null
    drop table #base_state_one_mismatched_piece
select  pairs.base_puzzle_state_id
        ,pairs.potential_neighbor_state_id
        ,base_puzzle.red_car_piece_placement_id as base_puzzle_state_red_car_id
        ,base_pieces.piece_placement_id as base_pieces_unmatched_piece_id
    into #base_state_one_mismatched_piece
from
    (
        select  base_state.id as base_puzzle_state_id
                ,potential_neighbor_state.id as potential_neighbor_state_id
        from    puzzle_states base_state
                join
                puzzle_states potential_neighbor_state
                on base_state.combinatorial_class_id = potential_neighbor_state.combinatorial_class_id
                and base_state.id <> potential_neighbor_state.id
                join
                piece_placements_puzzle_states base_state_pieces
                on base_state.id = base_state_pieces.puzzle_state_id
                 
                left join
                piece_placements_puzzle_states potential_neighbor_state_pieces
                on  potential_neighbor_state.id = potential_neighbor_state_pieces.puzzle_state_id
                    and base_state_pieces.piece_placement_id = potential_neighbor_state_pieces.piece_placement_id
        where   base_state.combinatorial_class_id = @comb_class_id
                and potential_neighbor_state_pieces.id is null
        group by base_state.id, potential_neighbor_state.id
        having count(1) = 1
    )pairs
    
    join puzzle_states base_puzzle 
    on pairs.base_puzzle_state_id = base_puzzle.id
    

    join
    piece_placements_puzzle_states base_pieces
    on pairs.base_puzzle_state_id = base_pieces.puzzle_state_id
   
    left join
    piece_placements_puzzle_states nbr_pieces
    on pairs.potential_neighbor_state_id = nbr_pieces.puzzle_state_id
       and base_pieces.piece_placement_id = nbr_pieces.piece_placement_id
    where nbr_pieces.piece_placement_id is null
order by pairs.base_puzzle_state_id, pairs.potential_neighbor_state_id



if OBJECT_ID('tempdb..#neighbor_state_one_mismatched_piece') is not null
    drop table #neighbor_state_one_mismatched_piece
select  pairs.base_puzzle_state_id as base_puzzle_state_id
        ,pairs.potential_neighbor_state_id as potential_neighbor_state_id
        ,nbr_puzzle_state.red_car_piece_placement_id as potential_neighbor_state_red_car_id
        ,nbr_pieces.piece_placement_id as potential_neighbor_pieces_unmatched_piece_id
into #neighbor_state_one_mismatched_piece
from (
        select  base_state.id as base_puzzle_state_id
                ,potential_neighbor_state.id as potential_neighbor_state_id
        from
                puzzle_states base_state
                join
                puzzle_states potential_neighbor_state
                on base_state.combinatorial_class_id = potential_neighbor_state.combinatorial_class_id
                   and base_state.id <> potential_neighbor_state.id
                join
                piece_placements_puzzle_states potential_neighbor_state_pieces 
                on potential_neighbor_state.id = potential_neighbor_state_pieces.puzzle_state_id
             
                left join
                piece_placements_puzzle_states base_state_pieces
                on  base_state.id = base_state_pieces.puzzle_state_id
                    and base_state_pieces.piece_placement_id = potential_neighbor_state_pieces.piece_placement_id
        where   potential_neighbor_state.combinatorial_class_id =  @comb_class_id
                and base_state_pieces.id is null
        group by base_state.id, potential_neighbor_state.id
        having count(1) = 1
    )pairs
    
    join puzzle_states nbr_puzzle_state
    on pairs.potential_neighbor_state_id = nbr_puzzle_state.id

    join piece_placements_puzzle_states nbr_pieces
    on pairs.potential_neighbor_state_id = nbr_pieces.puzzle_state_id
    
    left join piece_placements_puzzle_states base_pieces
    on pairs.base_puzzle_state_id = base_pieces.puzzle_state_id
       and
       nbr_pieces.piece_placement_id = base_pieces.piece_placement_id
where base_pieces.id is null
order by pairs.base_puzzle_state_id,pairs.potential_neighbor_state_id


--select top 5 *
--from #base_state_one_mismatched_piece
--select top 5 *
--from #neighbor_state_one_mismatched_piece

--delete from puzzle_state_transitions

insert into puzzle_state_transitions
select   base.base_puzzle_state_id
        ,base.potential_neighbor_state_id
        ,base_piece.id
        ,nbr_piece.id
        ,''
from #neighbor_state_one_mismatched_piece nbr
     join
     #base_state_one_mismatched_piece base
     on base.base_puzzle_state_id = nbr.base_puzzle_state_id
        and
        base.potential_neighbor_state_id = nbr.potential_neighbor_state_id
        --and base.base_puzzle_state_id = 4000000000000
        --and base.potential_neighbor_state_id in (4000000000001,4000000000054)
     join
     piece_placements base_piece
     on base.base_pieces_unmatched_piece_id = base_piece.id
    
     join
     piece_placements nbr_piece
     on nbr.potential_neighbor_pieces_unmatched_piece_id = nbr_piece.id
where   (nbr.potential_neighbor_state_red_car_id =  base.base_puzzle_state_red_car_id
         or
         (base.base_pieces_unmatched_piece_id = base.base_puzzle_state_red_car_id
          and
          nbr.potential_neighbor_pieces_unmatched_piece_id =nbr.potential_neighbor_state_red_car_id
         )
        )
        and
        (   base_piece.left_piece_placement_id = nbr_piece.id
            or
            base_piece.right_piece_placement_id = nbr_piece.id
            or
            base_piece.down_piece_placement_id = nbr_piece.id
            or
            base_piece.up_piece_placement_id = nbr_piece.id
        )
   --     and base.base_puzzle_state_id = 4000000000022
order by 1,2
    

--
--select *
--from #base_state_one_mismatched_piece
--where base_puzzle_state_id = 4000000000000
--and potential_neighbor_state_id in (4000000000001,4000000000054)
--
--select *
--from #neighbor_state_one_mismatched_piece
--where base_puzzle_state_id = 4000000000000
--and potential_neighbor_state_id in (4000000000001,4000000000054)
--
--

