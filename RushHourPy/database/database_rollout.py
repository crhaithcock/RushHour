'''
Created on May 7, 2015

@author: cliff
'''
import sys
import sqlite3
import itertools

conn = sqlite3.connect('./data/rush_hour.db')
db_cursor = conn.cursor()

DB_VERSION = 1

''' 
    select count(1)
    from sqlite_master
    where type='table' and name = 'version';
'''

    
def rollout_migrations_from_version(cur_db_version):
 
    # Assume all 
    while cur_db_version < DB_VERSION:
        next_db_version = cur_db_version + 1
        func = getattr(sys.modules[__name__], "rollout_migration_from_version_%s_to_version_%s" % (cur_db_version,next_db_version) )
        func()
        cur_db_version = next_db_version
        

def rollout_state_tables_from_version_0_to_version_1():
    print "here"
    sql_tables_states_shared_def = '''
    
        (
            game_number            int,
            game_hash_top          int,
            game_hash_bottom       int,
            is_goal_state          boolean,
            optimal_neighbor       int,
            red_car_end_a          int,
            connected_componen_id  int,
            topo_class_hash        int,
            degree                 int
        )
        '''
     
    sql_tables_states =[(''' create table state_for_comb_class_%i_cars_%i_trucks''' +
                           sql_tables_states_shared_def) % x 
                           for x in itertools.product(range(1,13),range(0,5))]
    
    #!!!! each index requires a unique name
    sql_index_states = ['''  create index board on combinatorial_classes_%s_cars_%s_trucks 
                             (game_hash_top, game_hash_bottom, red_car_end_a)
                         '''  %x for x in itertools.product(range(1,13),range(0,5)) ]
    
    return (sql_tables_states,sql_index_states)


def rollout_state_transition_tables_from_version_0_to_version_1():
    
    cars_trucks = itertools.product(range(1,13),range(0,5))

    sql_idx1 = ["create index idx1 on state_transition_comb_class_%s_cars_%s_trucks (pre_transition_game_number) " % x
                for x in cars_trucks]
    
    sql_idx2 = ["create index idx2 on state_transition_comb_class_%s_cars_%s_trucks (post_transition_game_number)"  % x
                for x in cars_trucks]
    
    sql_transition = [ '''
                            create table state_transition_for_comb_class_%s_cars_%s_trucks (
                                    pre_transition_game_number    int,
                                    post_transition_game_number   int
                                    ) ''' %x for x in cars_trucks
                     ]
    
    for sql in sql_transition:
        db_cursor.execute(sql)
    
    for sql in sql_idx1:
        db_cursor.execute(sql)
        
    for sql in sql_idx2:
        db_cursor.execute(sql)

    conn.commit
    
def rollout_component_tables_from_version_0_to_version_1():
    
    cars_trucks = itertools.product(range(1,13),range(0,5))
    
    sql_components = [ ''' 
                        create table component_for_comb_class_%s_cars_%s_trucks (
                            id    int,
                            num_states int
                     ''' %x for x in cars_trucks]
    
    for sql in sql_components:
        db_cursor.execute(sql)

    conn.commit

def rollout_migration_from_version_0_to_version_1():
    
    target_db_version = 1
    #===========================================================================
    # sql = '''
    #    create table settings(
    #    db_version    int
    #    ); 
    #    '''
    #===========================================================================
            
    #db_cursor.execute(sql)
    
    rollout_state_tables_from_version_0_to_version_1()
    rollout_state_transition_tables_from_version_0_to_version_1()
    rollout_component_tables_from_version_0_to_version_1()

    db_cursor.execute("insert ito db_version values(%s);" %(target_db_version))
    conn.commit

    
def rollout_current_db_version():
    
        
    db_cursor.execute("select count() from sqlite_master where type = 'table' and name = 'settings'")
    if db_cursor.fetchone()[0] == 0:
        rollout_migrations_from_version(0)
    
    else:
        db_cursor.execute("select db_version from settings")
        db_version = db_cursor.fetchone()[0]
        rollout_migrations_from_version(db_version)


#rollout_current_db_version()

#conn.close()
