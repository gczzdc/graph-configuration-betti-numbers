class Graph():
	def __init__(self):
		self.homological_degree=-1
		self.Betti_numbers={}
		self.Betti_number_is_unstable=set()
		self.graph.poincare_num_poly=None,
		self.graph.poincare_denom_power=None,
		self.graph.stable_poly_normalized=None
		self.adjacency_=None
		self.note=None
		self.image_file=None
		self.name=None
		self.essential_vertices_=None
		self.edges_=None
	
	def essential_vertices(self):
		if not self.essential_vertices_:
			self.build_essential_vertices()
		return self.essential_vertices_

	def edges(self):
		if not self.edges_:
			self.build_edges()
		return self.edges_

	def adjacency(self):
		if not self.adjacency_:
			self.build_adjacency()
		return self.adjacency_

	def build_essential_vertices(self):
		pass

	def build_edges(self):
		pass

	def build_adjacency(self):
		pass