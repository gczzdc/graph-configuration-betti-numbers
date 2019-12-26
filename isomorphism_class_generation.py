# algorithm design
#
# GOAL:
# 
# enumerate a representative for each isomorphism class
# of undirected connected loop-free bridgeless multigraph
# with no vertices of degree 2.
#
#
# each such multigraph has an underlying simple graph
# with the same number of vertices, 
# at most the same number of edges,
# still connected
# but possibly with bridges and vertices of degree 2
#
# Step 1: use geng to generate iso reps of connected simple graphs
# with at most E vertices and at most E edges
#
# Step 2: use multig to generate iso reps from these with precisely
# E edges
#
# Step 3: discard reps where any vertex is bivalent
# [this can be read off of the adjacency matrix]
#
# Step 4: discard reps containing a bridge
# 
# except when n=2 there precisely one tree with n edges 
# which is the kind of multigraph we're looking for
# namely the join of n vertices
# because the enumeration and filtering is costly, 
# it's quicker at the margins to either not generate this tree
# or generate it separately.

import subprocess
import networkx as nx
import numpy as np

loud = False

def toggle_loud():
	global loud
	if loud:
		loud = False
	else:
		loud = True

def loud_print(thing):
	if loud:
		print(thing)

def generate_multigraphs(edge_count=2):
	answer = []

	for vertex_count in range(1,edge_count+1):
		loud_print('vertex_count: {}'.format(vertex_count))
		simple_graphs = generate_simple_graphs(vertex_count=vertex_count, 
											max_edge_count=edge_count)
		loud_print(simple_graphs)
		candidate_multigraphs = convert_to_multigraph(graph_list = simple_graphs,
														edge_count = edge_count)
		loud_print(candidate_multigraphs)
		answer.extend(process_candidates(candidate_multigraphs))
	return answer

def process_candidates(candidates):
	answer = []
	for multigraph in candidates.split('\n')[:-1]:
		loud_print(multigraph)
		adj=build_adjacency(multigraph)
		loud_print(adj)
		if no_bivalent_vertex(adj) and no_bridge(adj):
			s6 = convert_to_sparse6(adj)
			answer.append(s6)
			loud_print(s6)
	return answer

def convert_to_sparse6(adjacency):
	G = nx.from_numpy_array(np.array(adjacency), 
		parallel_edges=True, 
		create_using=nx.MultiGraph)
	loud_print(G.edges)
	return nx.to_sparse6_bytes(G).decode('ascii')[11:-1]


def prettyprint(multigraph_list):
	return '\n\n'.join([graph_format(G) for G in multigraph_list])
		
def graph_format(G):
	return '\n'.join([row_format(R) for R in G])

def row_format(R):
	return ' '.join([str(x) for x in R])



def generate_simple_graphs(geng_command= './geng', vertex_count=2, max_edge_count=2):
	process = subprocess.run([geng_command, 
					'-c', 
					str(vertex_count)#, 
					#'0:{}'.format(max_edge_count)
					],
					capture_output=True,
					text=True)
	return process.stdout

def convert_to_multigraph(multig_command='./multig', graph_list='',edge_count=2):
	process = subprocess.run([multig_command, 
							'-A',
							'-e{}'.format(edge_count)],
							input=graph_list,
							capture_output=True,
							text=True)
	return process.stdout
 
def build_adjacency(multigraph):
	split_multigraph = [int(x) for x in multigraph.split()]
	vertices = split_multigraph[0]
	adjacency = [[0 for v in range(vertices)] for v in range(vertices)]
	length = vertices
	counter=1
	for i in range(vertices):
		for j in range(vertices-i):
			adjacency[i][i+j] = split_multigraph[counter]
			adjacency[i+j][i] = split_multigraph[counter]
			counter+=1
	return adjacency

def no_bivalent_vertex(adjacency_matrix):
	for row in adjacency_matrix:
		if sum(row)==2:
			return False
	return True

def no_bridge(adjacency_matrix):
	for i in range(len(adjacency_matrix)):
		for j in range(i):
			if adjacency_matrix[i][j]==1 and sum(adjacency_matrix[i])>1 and sum(adjacency_matrix[j])>1:
				if not still_connected(adjacency_matrix,i,j):
					return False
	return True
	#need to fix this


def still_connected(adjacency_matrix,i,j):
	used = {i}
	queue = {k for k in range(len(adjacency_matrix)) if adjacency_matrix[i][k]}
	queue.discard(j)
	while queue and j not in queue:
		current = queue.pop()
		used.add(current)
		for k in range(len(adjacency_matrix)):
			if adjacency_matrix[current][k] and k not in used:
				queue.add(k)
	if j in queue:
		return True
	return False


