
create table state_transition
(
	pre_transition_game_number			INTEGER,
	post_transition_game_number			INTEGER,
	comb_class_id						INTEGER	
);
create index idx_pre_transition  on state_transition ( pre_transition_game_number);            
create index idx_post_transition  on state_transition ( post_transition_game_number);            

