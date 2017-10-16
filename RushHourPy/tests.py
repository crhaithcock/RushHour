
import state
import component

top_hash = int('000001000000000000000001000011011000000000000000011011',2)

btm_hash = int('010000000000000000010000100100100000010000000000000000',2)


state = state.State(16,top_hash,btm_hash)
comp = component.Component.from_state(state)
#graph = comp.graph.ex
#part = comp.distance_partition
#graph = comp.graph
#comp.tst_set_distance_partition()

