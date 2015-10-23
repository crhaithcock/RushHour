
--drop table game_state;

create table game_state
(
	game_number 					INTEGER,
	comb_class_id 					INTEGER,
	game_hash_top 					INTEGER,
	game_hash_bottom 				INTEGER,
	is_goal_state 					INTEGER,
	optimal_transition_game_number  INTEGER,
	red_car_end_a 					INTEGER,
	topo_class_hash 				INTEGER,	
	connected_component_id 			INTEGER,
	degree 							INTEGER,
	solution_distance 				INTEGER,
	
    CONSTRAINT game_state_pk PRIMARY KEY (comb_class_id, game_number)
);

create index idx_game_state_hash on game_state(game_hash_top, game_hash_bottom,red_car_end_a);
create index idx_game_state_component on game_state(connected_component_id);

-- create alternate indexes?


