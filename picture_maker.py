import constants
img_start_tex = constants.img_start_tex
img_end_tex = constants.img_end_tex
node_radius = constants.node_radius

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