from utility import run

from constants import (
	bend_dic,
	cleanup_command,
	compile_command,
	convert_command,
	img_end_tex,
	graphics_format,
	img_start_tex,
	node_radius,
)

def image_maker(node_dic, edge_dic, narrow=1, scale=1):
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
											j*narrow,
											edge[1]))			
	out_builder.append("\\end{tikzpicture}\n")
	return ''.join(out_builder)	

def compile_image(G, loud_commands):
	if loud_commands:
		print ('generating tex file for graph {}'.format(G.name))
	edge_dic = G.get_edges()
	data = image_maker(G.image_dic,
						edge_dic,
						G.narrow,
						scale=1)
	with open(G.filename+'.tex','w') as f:
		f.write(data)

def convert_image(G, loud_commands):
	if loud_commands:
		print ('generating {} file for graph {}'.format(graphics_format, 
														G.name))
	edge_dic = G.get_edges()
	data = image_maker(G.image_dic,
						edge_dic,
						G.narrow,
						scale=2)
	with open(G.filename+'_img.tex','w') as f:
		f.write(img_start_tex)
		f.write(data)
		f.write(img_end_tex)

	run('{} {}_img'.format(compile_command, G.filename))		
	run('{} {}_img.{} {}.{}'.format(convert_command[0], 
									G.filename, 
									convert_command[1], 
									G.filename, 
									graphics_format))

	run('{} {}_img.{}'.format(cleanup_command[0], 
								G.filename, 
								cleanup_command[1]))