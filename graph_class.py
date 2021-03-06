import networkx as nx
import numpy as np
from constants import graphics_format

unsafe = '?@[\\]^`{|}'
safe = '0123456789'
translator = ''.maketrans(unsafe, safe,':')

def safe_encode(sparse6):
	return sparse6.translate(translator)


translator = {':':''}
for j in range(63,127):
	translator[chr(j)]=str(j-53)

def safe_encode(string):
	return ''.join([translator[j] for j in string])

class Graph():
	def __init__(self,sparse6):
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

		self.sparse6=sparse6
		self.has_sparse6=True
		#mckay sparse6 format


		self.name=sparse6
		self.using_sparse6_name=True
		self.safe_name = safe_encode(sparse6)
		self.image_dic=None
		self.filename = 'G'+self.safe_name
		self.note=None
		self.has_image = False

		self.essential_vertices=None

		self.homological_degree=-1
		self.Betti_numbers={}
		self.Betti_number_is_unstable=set()
		self.poincare_num_poly={},
		self.poincare_denom_power={},
		self.stable_poly_normalized={}
		self.validity=-1	

	def build_img(self):
		G = nx.from_sparse6_bytes(self.sparse6.encode('ascii'))
		try:
			node_dic = {k:tuple(v) for k,v in nx.planar_layout(G).items()}
		except nx.NetworkXException:
			node_dic = {k:tuple(v) for k,v in nx.circular_layout(G, scale=0.6).items()}
		self.image_dic = node_dic
		self.has_image = True

	def degree_sequence(self):
		self.build_VH()
		return sorted([len(v) for v in self.stars], reverse=True)

	def image_filename(self):
		return '{}.{}'.format(self.filename,graphics_format)

	def VE_to_adjacency(self):
		self.adjacency = [ [0 for i in range(self.vertex_count)] for j in range(self.vertex_count)]
		for e,multiplicity in self.edges.items():
			self.adjacency[e[0]][e[1]] = multiplicity
			self.adjacency[e[1]][e[0]] = multiplicity
		self.has_adjacency=True

	def adjacency_to_VE(self):
		self.vertex_count = len(self.adjacency)
		self.edges = {}
		for i in range(self.vertex_count):
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
		G = nx.from_sparse6_bytes(self.sparse6.encode('ascii'))
		self.adjacency = nx.to_numpy_array(G).astype(int).tolist()
		self.has_adjacency=True

	def adjacency_to_sparse6(self):
		G = nx.from_numpy_array(np.array(self.adjacency), 
			parallel_edges=True, 
			create_using=nx.MultiGraph)
		self.sparse6 = nx.to_sparse6_bytes(G).decode('ascii')[11:-1]
		self.has_sparse6=True

	def sparse6_to_VE(self):
		if not self.has_adjacency:
			self.sparse6_to_adjacency()
		self.adjacency_to_VE()

	def sparse6_to_VH(self):
		if not self.has_adjacency:
			self.sparse6_to_adjacency()
		self.adjacency_to_VH()

	def VE_to_sparse6(self):
		if not self.has_adjacency:
			self.VE_to_adjacency()
		self.adjacency_to_sparse6()

	def VH_to_sparse6(self):
		if not self.has_adjacency:
			self.VH_to_adjacency()
		self.adjacency_to_sparse6()

	def VH_to_adjacency(self):
		if not self.has_VE:
			self.VH_to_VE()
		self.VE_to_adjacency()

	def adjacency_to_VH(self):
		if not self.has_VE:
			self.adjacency_to_VE()
		self.VE_to_VH()

	def get_essential_vertices(self):
		if not self.essential_vertices:
			self.build_essential_vertices()
		return self.essential_vertices

	def get_edges(self):
		if not self.has_VE:
			self.build_VE()
		return self.edges

	def get_sparse6(self):
		if not self.has_sparse6:
			self.build_sparse6()
		return self.sparse6

	def get_adjacency(self):
		if not self.has_adjacency:
			self.build_adjacency()
		return self.adjacency

	def build_essential_vertices(self):
		if not self.has_VH:
			self.build_VH()
		self.essential_vertices = [v for v in self.stars if len(v)>2]

	def build_VE(self):
		if self.has_VE:
			return
		elif self.has_adjacency:
			self.adjacency_to_VE()
		elif self.has_VH:
			self.VH_to_VE()
		elif self.has_sparse6:
			self.sparse6_to_VE()
		else:
			raise ConvertError('cannot build VE format; no data type recognized')

	def build_VH(self):
		if self.has_VH:
			return
		elif self.has_VE:
			self.VE_to_VH()
		elif self.has_adjacency:
			self.adjacency_to_VH()
		elif self.has_sparse6:
			self.sparse6_to_VH()
		else:
			raise ConvertError('cannot build VH format; no data type recognized')

	def build_adjacency(self):
		if self.has_adjacency:
			return
		elif self.has_VE:
			self.VE_to_adjacency()
		elif self.has_VH:
			self.VH_to_adjacency()
		elif self.has_sparse6:
			self.sparse6_to_adjacency()
		else:
			raise ConvertError('cannot build adjacency matrix; no data type recognized')

	def build_sparse6(self):
		if self.has_sparse6:
			return
		elif self.has_VE:
			self.VE_to_sparse6()
		elif self.has_adjacency:
			self.adjacency_to_sparse6()
		elif self.has_VH:
			self.VH_to_sparse6()
		else:
			raise ConvertError('cannot build sparse6 format; no data type recognized')

