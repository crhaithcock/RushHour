


create table IF NOT EXISTS CombClasses(
	num_cars	int,
	num_trucks	int,
	stat_num_strip_vectors int,
	
	PRIMARY KEY (num_cars,num_trucks)
);


create table IF NOT EXISTS StripVectors(
	c1 int,
	c2 int,
	c3 int,
	ct int,
	tc int,
	t1 int,
	t2 int,
	
	stat_status text,
	stat_num_topo_classes int,
	stat_num_completed_classes int,
	stat_num_states int,
	
	PRIMARY KEY (c1,c2,c3,ct,tc,t1,t2)
);

create table IF NOT EXISTS TopoClasses(
	row1 int, 
	row2 int, 
	row3 int, 
	row4 int, 
	row5 int, 
	row6 int, 
	col1 int, 
	col2 int, 
	col3 int, 
	col4 int, 
	col5 int, 	
	col6 int,
	
	-- comb class markers
	num_cars int,
	num_trucks int,
	
	
	num_components int,
	num_solvable_componente int,
	num_states int,
	
	PRIMARY KEY (row1,row2,row3,row4,row5,row6,col1,col2,col3,col4,col5,col6)
);


create table IF NOT EXISTS Component(
	state_int int PRIMARY KEY,
	
	num_states int,
	avg_degree int,
	max_depth int
);


	
	

	
	