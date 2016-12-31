


declare @reached as table(
    id bigint
)



declare @root_id as bigint
set @root_id = 4000000000007

insert into @reached values ( @root_id ) -- substitute root id as needed
while ( @@rowcount > 0 )
begin
    insert into @reached
    select distinct post_transition_puzzle_state_id
    from puzzle_state_transitions child
         join
         @reached parent on parent.id = pre_transition_puzzle_state_id
    where child.post_transition_puzzle_state_id not in ( select id from @reached )
end


--select *
--from @reached


select x.*,z.row,z.col,z.end_a,z.end_b,z.*
from @reached x
     join
     piece_placements_puzzle_states y
     on x.id = y.puzzle_state_id
     join
     piece_placements z on y.piece_placement_id = z.id
order by x.id


