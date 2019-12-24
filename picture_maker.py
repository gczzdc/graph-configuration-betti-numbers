
def graphmaker(node_dic, edge_dic, narrow_flag=1, scale=1):
	out_builder = []
	out_builder.append("\\begin{tikzpicture}")
	if scale !=1:
		out_builder.append("[scale =")
		out_builder.append(str(scale))
		out_builder.append("]")
	out_builder.append("\n")
	for node in node_dic:
		out_builder.append('')
		out_builder[-1]+='\\fill[black] '
		out_builder[-1]+=str(node_dic[node])
		out_builder[-1]+=' circle (' 
		out_builder[-1]+=node_radius
		out_builder[-1]+=') node(n'
		out_builder[-1]+=str(node)
		out_builder[-1]+='){};\n'
	for edge in edge_dic:
		for j in bend_dic[edge_dic[edge]]:
			out_builder.append('')
			out_builder[-1]+= '\\draw (n'
			out_builder[-1]+= str(edge[0])
			out_builder[-1]+= '.center) to[bend right='
			out_builder[-1]+= str(j*narrow_flag)
			out_builder[-1]+= '] (n'
			out_builder[-1]+= str(edge[1])
			out_builder[-1]+='.center);\n'
	out_builder.append("\\end{tikzpicture}\n")
	return ''.join(out_builder)

def graph_file(outfile,node_dic,edge_dic,narrow_flag=1,scale=1):
	data = graphmaker(node_dic,edge_dic,narrow_flag,scale)
	f=open(outfile+'.tex','w')
	f_sa = open(outfile+'_img.tex','w')
	f.writelines(data)
	f_sa.write(img_start_tex)
	f_sa.writelines(data)
	f_sa.write(img_end_tex)
	f.close()
	f_sa.close()
	return