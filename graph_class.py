class Graph():
	def __init__(self):
		self.vertex_count=0
		# a non-negative integer
		self.edges=None
		# a dictionary of ordered pairs with keys
		# pairs of vertices
		self.has_VE=False


		self.edge_count=0
		# a non-negative integer
		self.stars=None
		# a list of lists, one for each vertex
		#where each vertex list is of edges adjacent to the vertex
		#each edge must appear twice is the union of these lists.
		self.has_VH=False

		self.adjacency=None
		self.has_adjacency = False
		#full adjacency matrix as a list of lists.

		self.sparse6=None
		self.has_sparse6 = False
		#mckay sparse6 format


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

	def VE_to_adjacency(self):
		self.adjacency = [ [0 for i in range(self.vertex_count)] for j in range(self.vertex_count)]
		for e,multiplicity in self.edges.items():
			self.adjacency[e[0]][e[1]] = multiplicity
			self.adjacency[e[1]][e[0]] = multiplicity
		self.has_adjacency=True

	def adjacency_to_VE(self):
		self.vertex_count = len(self.adjacency)
		self.edges = {}
		for i in range(self.vertex_count)
			for j in range(i+1):
				multiplicity=self.adjacency[i][j]
				if multiplicity:
					self.edges[(j,i)]=multiplicity
		self.has_VE=True

	def VE_to_VH(self):
		self.edge_count=sum(self.edges.values())
		self.stars = [[] for _ in range(self.vertex_count)]
		counter = 0
		for vertex_pair, multiplicity in self.edges.items():
			for _ in range(multiplicity):
				for vertex in vertex_pair:
					self.stars[vertex].append(counter)
				counter+=1
		self.has_VH = True

	def VH_to_VE(self):
		self.vertex_count=len(self.stars)
		temp_edges = {}
		for j, star in enumerate(self.stars):
			for e in star:
				if e in edges:
					temp_edges[e].append(j)
				else:
					temp_edges[e]=[j,]
		self_edges={}
		for e, pair in temp_edges.items():
			key = tuple(pair)
			if key in self.edges:
				self.edges[key]+=1
			else:
				self.edges[key]=1
		self.has_VE=True

	def sparse6_to_adjacency(self):
		pass
	def sparse6_to_VE(self):
		pass
	def sparse6_to_VH(self):
		pass
	def VE_to_sparse6(self):
		pass
	def VH_to_sparse6(self):
		pass
	def adjacency_to_sparse6(self):
		pass


	def VH_to_adjacency(self):
		if not self.has_VE:
			self.VH_to_VE()
		self.VE_to_adjacency()

	def adjacency_to_VH(self):
		if not self.has_VE:
			self.adjacency_to_VE()
		self.VE_to_VH()

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