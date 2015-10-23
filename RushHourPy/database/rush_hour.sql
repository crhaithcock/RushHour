
/*
	Script to roll out Rush Hour database
*/

create table game_state(
	game_number             int,
	comb_class_id		    int,
	game_hash_top           int,
	game_hash_bottom        int,
	is_goal_state           boolean,
	optimal_neighbor        int,
	red_car_end_a           int,
	connected_component_id  int,
	topo_class_hash         int,
	degree                  int
 );
create index idx_game_state on game_state (game_hash_top, game_hash_bottom, red_car_end_a);
create index idx_component on game_state(connected_component_id);


create table state_transition(
	comb_class_id				int,
	pre_transition_game_number	int,
	post_transition_game_number	int
 );
create index idx_pre_transition on state_transition (comb_class_id, pre_transition_game_number);
create index idx_post_transition on state_transition (comb_class_id, post_transition_game_number);
 
 
create table connected_component(
	id 				int,
	num_states		int
);
 
create table settings(
	db_version	int
	);
insert into settings values(1);


