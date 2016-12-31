

import collections


Piece = collections.namedtuple('Piece','end_a end_b topology')	

Edge = collections.namedtuple('Edge','from_state to_state direction')


class Edge:

	REVERSE_DIRECTION_DICT = {'up':'down', 'down':'up', 'left':'right','right':'left'}
	
	def _init_(self,from_state, to_state,direction):
		self.from_state = from_state 
		self.to_state = to_state
		self.direction = direction
	
	
	def reverse_edge(self):
		
		return Edge(self.to_state,self.from_state,self.REVERSE_DIRECTION_DICT[self.direction])
		
		
			