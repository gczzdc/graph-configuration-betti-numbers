from constants import drawn_graphs_file

def read_graph_pix():
	with open(drawn_graphs_file,'r') as f:
		data = f.read()
	raw_graphs = data.split('\n\n')
	processed_graphs = {}
	for graph in raw_graphs:
		lines = graph.split('\n')
		key = lines[0]
		narrow = lines[-1].split('=')[1].strip()
		name = lines[-2].split('=')[1].strip()
		node_dic = {j-1: eval(lines[j]) for j in range(1, len(graph_lines-2))}
		processed_graphs[key]=(node_dic, name, narrow)
	return processed_graphs

def assign_pix_to_graphs(graphs):
	pix = read_graph_pix()
	for graph in graphs:
		if graph.sparse6 in pix:
			info = pix[graph.sparse6]
			graph.name = info.name
			graph.narrow = info.narrow
			graph.image_dic = info.node_dic
			graph.filename = info.name
			graph.has_image = True
			