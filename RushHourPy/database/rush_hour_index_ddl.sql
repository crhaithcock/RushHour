
/*
	Script to roll out Rush Hour database
*/


/*  Application software can derive a game component efficiently enogh.

	THere is no need to store more than identifying and foreign key data.

*/



create UNIQUE index idx_state on state (red_car_end_a, game_hash_top, game_hash_bottom);
create index idx_component on state (component_id);
create UNIQUE index idx_component_graph on state (component_id,node_id);




