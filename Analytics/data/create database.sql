

/*
CREATE TABLE [IF NOT EXISTS] [schema_name].table_name (
 column_1 data_type PRIMARY KEY,
   column_2 data_type NOT NULL,
 column_3 data_type DEFAULT 0,
 table_constraint
) [WITHOUT ROWID];
*/


-- segment table tracks which segments have been generated to prevent inadvertently recomputing nodes unnecessarily
-- and to be able to pick up where 
CREATE TABLE If NOT EXISTS segment(
    id integer primary_key,
    num_v_cars integer,
    num_h_cars integer,
    num_v_trucks integer,
    num_h_trucks integer,
    num_states integer,
    num_components integer
    );
    

-- This table is intended to temporarily hold the nodes for one single combinatorial class
CREATE TABLE If NOT EXISTS node(
    id integer primary key,
    comb_class int ,
    board_int_s1 int ,
    board_int_s2 int ,
    red_col int,
    included_in_component int --boolean 0/1 - indicates node has been discovered via BFS
   );
    
create unique index if not exists idxNode on node (board_int_s1,board_int_s2,red_col);

-- 
CREATE TABLE If NOT EXISTS  comb_class(
    comb_class integer primary key,
    num_nodes int ,
    num_components,
    num_solvable_components,
    num_unsolvable_components,
    max_solution_depth
   );
    
    

CREATE TABLE If NOT EXISTS  component(
    id integer primary key,
    comb_class int ,
    repr_board_int_s1 int ,
    repr_board_int_s2 int ,
    repr_red_col int,
    is_solvable int, -- 0/1
    num_nodes int,
    density float,
    max_solution_distance int   
   );
    
    
    
    
