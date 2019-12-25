from constants import (
	bend_dic,
	img_end_tex,
	img_start_tex,
	node_radius,
)

def image_maker(node_dic, edge_dic, narrow_flag=1, scale=1):
	out_builder = []
	out_builder.append("\\begin{tikzpicture}")
	if scale !=1:
		out_builder.append('[scale ={}]'.format(scale))
	out_builder.append('\n')
	for node in node_dic:
		out_builder.append(
			'\\fill[black] {} circle ({}) node(n{}){{}};\n'.format(
															node_dic[node],
															node_radius,
															node))
	for edge in edge_dic:
		for j in bend_dic[edge_dic[edge]]:
			out_builder.append(
				'\\draw (n{}.center) to[bend right={}] (n{}.center);\n'.format(
											edge[0],
											j*narrow_flag),
											edge[1])			
	out_builder.append("\\end{tikzpicture}\n")
	return ''.join(out_builder)

def image_files(outfile,node_dic,edge_dic,narrow_flag=1,scale=1):
	data = image_maker(node_dic,edge_dic,narrow_flag,scale)
	with open(outfile+'.tex','w') as f:
		f.write(data)
	with open(outfile+'_img.tex','w') as f:
		f.write(img_start_tex)
		f.write(data)
		f.write(img_end_tex)

def compile_images(graphs, loud_commands):
	for G in graphs:
		if loud_commands:
			print ('generating tex file for graph {}'.format(graph.name))
		if G.image_dic:
			edge_dic = G.edges()
		picture_maker.image_files(filebase, G.image_dic, edge_dic, G.narrow_flag, scale=1)

		if len(graphs[graph])==2:
			graph_file(graph,graphs[graph][0],graphs[graph][1],narrow_flag=1,scale=1)
		else:
			graph_file(graph,graphs[graph][0],graphs[graph][1],narrow_flag=graphs[graph][2],scale=1)
		run(cleanup_commands[0]+graph+'_img'+cleanup_commands[1])


def convert_images(graphs):
	for graph in graphs:
	if loud_commands:
		print ('generating tex file for',graph)
	if len(graphs[graph])==2:
		graph_file(graph,graphs[graph][0],graphs[graph][1],narrow_flag=1,scale=2)
	else:
		graph_file(graph,graphs[graph][0],graphs[graph][1],narrow_flag=graphs[graph][2],scale=2)
	run(compile_command+ ' '+graph+'_img')		
	run(convert_command[0]+graph+'_img'+convert_command[1]+graph+convert_command[2])
	run(cleanup_commands[0]+graph+'_img'+cleanup_commands[1])