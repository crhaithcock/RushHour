
/*
	Script to roll out Rush Hour database
*/


/*  Application software can derive a game component efficiently enogh.

	THere is no need to store more than identifying and foreign key data.

*/


create table state(
	
	-- Key
	 red_car_end_a           int
	,game_hash_top           int
	,game_hash_bottom        int
	

	-- 2**12*3**4 combinatorial classe
	-- each combinatorial class consists of game components
	-- each combinatorial class consists of topological classes. it is unclare if this attribute is useful
 
	,comb_class_id		    int 
	,topo_class_hash        int


	-- GamePlay Data
	,is_soln_state           boolean
	

	-- State Graph Data
	,component_id  			int		-- A component represents all reachable states from a given starting board configuration.
	,node_id				int		-- Node ID used in NetworkX model
	,soln_nbr_id			int		-- Networkx node for node to follow for an optimal path to solution.
	,soln_dist				int		-- Minimal number of moves required to solve

	);


create table component(
	id 				int,
	comb_class_id	int,
	topo_class		int
);


create table comp_stats(
	component_id		int,
	num_states			int,
	num_soln_states		int,
	density				float,
	is_solvable			boolean,
	diameter			int,
	min_cut_size		int
);


create table comp_edges(
	component_id			int,
	source_node_id			int,
	target_node_id			int,
	direction				text
);


create table comp_dist_partition(
	comp_id				int,
	soln_dist			int,
	node_id				int
);


 create table combinatorial_class(
	id							int,
	num_cars					int,
	num_trucks					int,

	-- graph statistics for analytics
	num_components  			int,
	num_solvable_components 	int,
	num_states					int
 );



create table topology(
	comb_class_id				int,
	topology_1					text,
	toplogy_2					text,
	num_states					int,
	deg_sum						int,
	deg_max						int,
	deg_zero_count				int
);

