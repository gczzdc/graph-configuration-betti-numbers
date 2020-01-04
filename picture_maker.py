from utility import run

from constants import (
	cleanup_command,
	compile_command,
	convert_command,
	img_end_tex,
	image_directory,
	graphics_format,
	img_start_tex,
	node_radius,
)

def midpoint(c1, c2):
	return ((c1[0]+c2[0])/2, (c1[1]+c2[1])/2)

def image_maker(node_dic, edge_dic, narrow=1, scale=1):
	out_builder = []
	out_builder.append("\\begin{tikzpicture}")
	out_builder.append('[scale ={}, baseline]'.format(scale))
	out_builder.append('\n')
	for node in node_dic:
		out_builder.append(
			'\\fill[black] {} circle ({}) node(n{}){{}};\n'.format(
															node_dic[node],
															node_radius,
															node))
	for edge in edge_dic:
		for j in bend_dic[edge_dic[edge]]:
			out_builder.append('\\draw (n{}.center) to'.format(edge[0]))
			bend = int(j*narrow)
			if bend > 0:
				out_builder.append('[bend right={}]'.format(bend))
			elif bend < 0:
				out_builder.append('[bend left={}]'.format(-bend))
			out_builder.append(' (n{}.center);\n'.format(edge[1]))			
	out_builder.append("\\end{tikzpicture}\n")
	return ''.join(out_builder)	

def weighted_image_maker(node_dic, edge_dic, scale=1):
	out_builder = []
	out_builder.append("\\begin{tikzpicture}")
	out_builder.append('[scale ={}, baseline]'.format(scale))
	out_builder.append('\n')
	for node in node_dic:
		out_builder.append(
			'\\fill[black] {} circle ({}) node(n{}){{}};\n'.format(
															node_dic[node],
															node_radius,
															node))
	for edge in edge_dic:
		out_builder.append('\\draw (n{}.center) to'.format(edge[0]))
		out_builder.append(' (n{}.center);\n'.format(edge[1]))
		v0 = node_dic[edge[0]]
		v1 = node_dic[edge[1]]
		edge_marker = midpoint(v0,v1)
		if edge_dic[edge]>1:
			out_builder.append(
				'\\draw {} node[inner sep=0, fill=white]{{[{}]}};\n'.format(
					edge_marker, 
					edge_dic[edge]
					))
			
	out_builder.append("\\end{tikzpicture}\n")
	return ''.join(out_builder)	

def compile_image(G, loud_commands):
	if loud_commands:
		print ('generating tex file for graph {}'.format(G.name))
	edge_dic = G.get_edges()
	data = weighted_image_maker(G.image_dic,
						edge_dic,
						scale=1)
	with open(G.filename+'.tex','w') as f:
		f.write(data)

def convert_image(G, loud_commands):
	if loud_commands:
		print ('generating {} file for graph {}'.format(graphics_format, 
														G.name))
	edge_dic = G.get_edges()
	data = weighted_image_maker(G.image_dic,
						edge_dic,
						scale=2)
	img_file_base = '{}/{}_img'.format(image_directory, G.filename)
	with open('{}.tex'.format(img_file_base),'w') as f:
		f.write(img_start_tex)
		f.write(data)
		f.write(img_end_tex)

	run((compile_command, img_file_base), loud_commands)		
	run((convert_command[0], 
		'{}_img.{}'.format(G.filename, convert_command[1],), 
		'{}/{}.{}'.format(image_directory, G.filename, graphics_format)), loud_commands)
	run((cleanup_command[0], '{}_img.{}'.format(G.filename, cleanup_command[1])), loud_commands)
