
insert into game_state 
select 	 game_number
		,comb_class_id
		,game_hash_top
		,game_hash_bottom
		,is_goal_state
		,optimal_neighbor 
		,red_car_end_a
		,topo_class_hash
		,connected_component_id
		,degree
		,NULL as solution_distance
from states;
