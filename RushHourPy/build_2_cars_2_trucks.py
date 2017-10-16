

import sqlite3
import state
import component
import generate_states
import generate_components
import importlib



# 2 cars, 2 tucks: id = 2**2 * 3**2 = 36
#comb_class_id = 36
#generate_states.generate_states(1,1)
#generate_components.generate_components(6)



# sql_stmt = """ Select red_car_end_a, game_hash_top, game_hash_bottom
#                from state
#                where comb_class_id = %d and connected_component_id is NULL
#                --limit 1
#             """%(comb_class_id)

#cur.execute(sql_stmt)

#names = [d[0] for d in cur.description]
#(red_car_end_a,top_hash,bottom_hash) = cur.fetchone()

#(red_car_end_a, top_hash, bottom_hash) = (12,7760490508431362,0)
#print(cur.fetchone())
#s = state.State(red_car_end_a, bottom_hash, top_hash)

#nbrs = s.derive_neighbors()

#all_states = [state.State(db_state['red_car_end_a'], db_state['game_hash_top'], db_state['game_hash_bottom']) for\
#              x in cur.fetchall()]

#nbrd = component.Component().from_state(s)

#p = nbrd.distance_partition


#cur.close()
#conn.close()
