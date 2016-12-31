
    select  pre_transition_state_id,
            post_transition_state_id,
            pre_piece.id as 'pre_transition_piece_id',
            post_piece.id as 'post_transition_piece_id',
            case when pre_piece.left_piece_placement_id = post_piece.id
                 then 'move left'
                 when pre_piece.right_piece_placement_id = post_piece.id
                 then 'move right'
                 when pre_piece.up_piece_placement_id = post_piece.id
                 then 'move up'
                 when pre_piece.down_piece_placement_id = post_piece.id
                 then 'move down'
            end

    from

    (

    select pre_transition_state_id,post_transition_state_id,count(*) as 'count'
    from

    (
    select pre_transition_state_id,post_transition_state_id,count(*) as 'count'
    from


            (
            select puzzle_state_id as pre_transition_state_id,count(*) as num_pieces
            from piece_placements_puzzle_states
            group by puzzle_state_id
            )pre_transition_states

            join

            (
            select puzzle_state_id as post_transition_state_id,count(*) as num_pieces
            from piece_placements_puzzle_states
            group by puzzle_state_id
            )post_transition_states

            on  pre_transition_states.num_pieces = post_transition_states.num_pieces --only match states with same num pieces
                and pre_transition_states.pre_transition_state_id < post_transition_states.post_transition_state_id -- eliminate duplicates

            join

            piece_placements_puzzle_states pre_transition_pieces -- get all pieces for left side puzzle state
            on pre_transition_state_id = pre_transition_pieces.puzzle_state_id

            left join
            piece_placements_puzzle_states post_transition_pieces
            on  post_transition_state_id = post_transition_pieces.puzzle_state_id
                and pre_transition_pieces.piece_placement_id = post_transition_pieces.piece_placement_id

            where post_transition_pieces.id is null
            group by pre_transition_state_id,post_transition_state_id
            having count(*) = 1

    )state_pairs

    join

    piece_placements_puzzle_states post_transition_pieces -- get all pieces for post transition state
    on state_pairs.post_transition_state_id = post_transition_pieces.puzzle_state_id

    left join

    piece_placements_puzzle_states pre_transition_pieces
    on state_pairs.pre_transition_state_id = pre_transition_pieces.puzzle_state_id
       and
       post_transition_pieces.piece_placement_id = pre_transition_pieces.piece_placement_id

    where pre_transition_pieces.id is null
    group by pre_transition_state_id, post_transition_state_id
    having count(*) = 1

    -- at this point we now have pre and post transitions
    -- where each has exactly one piece placement not in the other state
    -- now we need to verify that the unmatched piece placements are linked to one another

    )almost_matched_states


    join
    piece_placements_puzzle_states pre_transition_pieces
    on almost_matched_states.pre_transition_state_id = pre_transition_pieces.puzzle_state_id

    join
    piece_placements_puzzle_states post_transition_pieces
    on almost_matched_states.post_transition_state_id = post_transition_pieces.puzzle_state_id
       and
       pre_transition_pieces.piece_placement_id <> post_transition_pieces.piece_placement_id

    join
    piece_placements pre_piece
    on pre_transition_pieces.piece_placement_id = pre_piece.id

    join
    piece_placements post_piece
    on post_transition_pieces.piece_placement_id = post_piece.id

    where pre_piece.left_piece_placement_id = post_piece.id
          or
          pre_piece.right_piece_placement_id = post_piece.id
          or
          pre_piece.up_piece_placement_id = post_piece.id
          or
          pre_piece.down_piece_placement_id = post_piece.id

    order by pre_transition_state_id, post_transition_state_id

    --where pre_transition_state_id = 2000000000000
