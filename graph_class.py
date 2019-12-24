class Graph():
	def __init__(self):
		self.homological_degree=-1
		self.Betti_numbers={}
		self.Betti_number_is_unstable=set()
		self.polys={}
		self.adjacency=None
		self.note=''
