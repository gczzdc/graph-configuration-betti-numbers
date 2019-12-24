class Graph():
	def __init__(self):
		self.vertices_=None
		self.edges_=None
		self.half_edges_=None
		self.adjacency_=None
		self.sparse6_=None

		self.name=None
		self.image_file=None
		self.note=None

		self.essential_vertices_=None

		self.homological_degree=-1
		self.Betti_numbers={}
		self.Betti_number_is_unstable=set()
		self.graph.poincare_num_poly=None,
		self.graph.poincare_denom_power=None,
		self.graph.stable_poly_normalized=None
	
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