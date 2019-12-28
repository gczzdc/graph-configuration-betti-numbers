from constants import drawn_graphs_file

def read_graph_pix():
	with open(drawn_graphs_file,'r') as f:
		data = f.read()
	raw_graphs = data.split('\n\n')
	processed_graphs = {}
	for graph in raw_graphs:
		lines = graph.strip().split('\n')
		key = lines[0]
		try:
			narrow = float(lines[-1].split('=')[1].strip())
			name = lines[-2].split('=')[1].strip()
			node_dic = {j-1: eval(lines[j]) for j in range(1, len(lines)-2)}
			processed_graphs[key]=(node_dic, name, narrow)
		except:
			print('Error')
			for j in lines:
				print(j)
			input()
	return processed_graphs

def assign_pix_to_graphs(graphs):
	pix = read_graph_pix()
	for graph in graphs:
		if graph.sparse6 in pix:
			info = pix[graph.sparse6]
			graph.name = info[1]
			graph.narrow = info[2]
			graph.image_dic = info[0]
			graph.filename = info[1]
			graph.has_image = True
			