class Graph():
	def __init__(self):
		self.vertices=None
		self.edges=None
		self.half_edges=None
		self.adjacency=None
		self.sparse6=None

		self.has_sparse6 = False
		self.has_VE = False
		self.has_adjacency = False
		self.has_HVi = False

		self.name=None
		self.image_file=None
		self.note=None

		self.essential_vertices=None

		self.homological_degree=-1
		self.Betti_numbers={}
		self.Betti_number_is_unstable=set()
		self.graph.poincare_num_poly=None,
		self.graph.poincare_denom_power=None,
		self.graph.stable_poly_normalized=None	

	def essential_vertices(self):
		if not self.essential_vertices:
			self.build_essential_vertices()
		return self.essential_vertices

	def edges(self):
		if not self.has_VE:
			self.build_VE()
		return self.edges

	def adjacency(self):
		if not self.has_adjacency:
			self.build_adjacency()
		return self.adjacency

	def build_essential_vertices(self):
		if not self.has_VE:
			self.build_VE()
		pass

	def build_VE(self):
		pass

	def build_adjacency(self):
		if self.adjacency:
			return
		if self.vertices:

# def essential_vertices(graph):
# 	vertices = {}
# 	for edge in graph:
# 		for v in edge:
# 			if v not in vertices:
# 				vertices[v]=0
# 			vertices[v]+=graph[edge]
# 	essential_vertices =0
# 	for v in vertices:
# 		if vertices[v]>2:
# 			essential_vertices+=1
# 	return (essential_vertices)

# def e_pres_to_h_pres(graph):
# 	h_graph= [sum(graph[1].values()),]
# 	vertices=list(graph[0].keys())
# 	h_graph.append([[] for _ in graph[0]])
# 	counter = 0
# 	for vert_pair in graph[1]:
# 		for _ in range(graph[1][vert_pair]):
# 			for vert in vert_pair:
# 				h_graph[-1][vertices.index(vert)].append(counter)
# 			counter+=1
# 	return h_graph