

/*  The goal - a set of all legal transitions between the exisitng states
            
                Start with a superset of the goal and winnow that set down.

                One could start with the set of all state pairs as the superset. 

                We take a different approach and start with pairs in the same combinatorial class.

                Second, since x ~ y => y ~ x, we only need only consider pairs
                where pre transition state id < post transition state id
*/



declare @intermediate_states_and_pieces as table
(
    pre_state_id        bigint,
    post_state_id       bigint,
    pre_piece_id        bigint,
    post_piece_id       bigint
)


declare @initial_state_pairs as table(
    pre_state_id    bigint,
    post_state_id    bigint
)



insert into @initial_state_pairs
select pre_state.id as pre_transition_state_id,
       post_state.id as post_transition_state_id

from puzzle_states pre_state
     join
     puzzle_states post_state

     on pre_state.combinatorial_class_id = post_state.combinatorial_class_id
        and
        pre_state.id < post_state.id



/* To determine if  x ~ y, we need to ensure the following facts

    1. x has exactly one piece placement x' not in y
    2. y has exactly one piece placement y' not in y
    3. x' and y' are linked in the piece_placements table
*/



select pre_state_id,post_state_id,piece_placement_id,count(*)
from
(
select init_pairs.pre_state_id,
       init_pairs.post_state_id,
       pre_pieces.piece_placement_id

from @initial_state_pairs init_pairs
     join
     piece_placements_puzzle_states pre_pieces
     on init_pairs.pre_state_id = pre_pieces.puzzle_state_id

Except

select init_pairs.pre_state_id,
       init_pairs.post_state_id,
       post_pieces.piece_placement_id

from @initial_state_pairs init_pairs
     join
     piece_placements_puzzle_states post_pieces
     on init_pairs.post_state_id = post_pieces.puzzle_state_id
)x
group by pre_state_id,post_state_id,piece_placement_id

/*


insert into @intermediate_states_and_pieces

/* setup for condition 1*/
select init_pairs.pre_state_id,
       init_pairs.post_state_id,
       pre_pieces.piece_placement_id,
       post_pieces.piece_placement_id /* should be null */
from @initial_state_pairs init_pairs

     join
     piece_placements_puzzle_states pre_pieces
     on init_pairs.pre_state_id = pre_pieces.puzzle_state_id

     left join
     piece_placements_puzzle_states post_pieces
     on init_pairs.post_state_id = post_pieces.puzzle_state_id
        and
        pre_pieces.id = post_pieces.id
where post_pieces.id is null

union

/* setup for condition 2*/
select init_pairs.pre_state_id,
       init_pairs.post_state_id,
       pre_pieces.piece_placement_id, /* should be null */
       post_pieces.piece_placement_id 
from    @initial_state_pairs init_pairs
        
        join
        piece_placements_puzzle_states post_pieces
        on init_pairs.post_state_id = post_pieces.puzzle_state_id
        
        left join
        piece_placements_puzzle_states pre_pieces
        on init_pairs.pre_state_id = pre_pieces.puzzle_state_id
           and
           pre_pieces.id = post_pieces.id
        


/* condition 1*/
select pre_state_id,post_state_id,pre_piece_id,count(*)
from @intermediate_states_and_pieces
where pre_piece_id is not null
group by pre_state_id,post_state_id,pre_piece_id
order by count(*) desc

*/