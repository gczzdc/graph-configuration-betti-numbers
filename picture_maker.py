
def graphmaker(node_dic, edge_dic, narrow_flag=1, scale=1):
	output = []
	output.append("\\begin{tikzpicture}")
	if scale !=1:
		output.append("[scale =")
		output.append(str(scale))
		output.append("]")
	output.append("\n")
	for node in node_dic:
		output.append('')
		output[-1]+='\\fill[black] '
		output[-1]+=str(node_dic[node])
		output[-1]+=' circle (' 
		output[-1]+=node_radius
		output[-1]+=') node(n'
		output[-1]+=str(node)
		output[-1]+='){};\n'
	for edge in edge_dic:
		for j in bend_dic[edge_dic[edge]]:
			output.append('')
			output[-1]+= '\\draw (n'
			output[-1]+= str(edge[0])
			output[-1]+= '.center) to[bend right='
			output[-1]+= str(j*narrow_flag)
			output[-1]+= '] (n'
			output[-1]+= str(edge[1])
			output[-1]+='.center);\n'
	output.append("\\end{tikzpicture}\n")
	return (output)

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