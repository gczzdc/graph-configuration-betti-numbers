import constants

def format_poly_to_tex(poly, var='t'):
	# format polynomial (list starting with degree zero coefficient) to tex.
	poly_tex=''
	for j,c in enumerate(poly):
		# c is the jth cofficient starting with the constant term
		if c>0:
			#if the coefficient is positive, put in a plus sign
			#not necessary for negative coefficients
			poly_tex+='+'
		if c!=0:
			#don't write +-1 coefficients unless it's a constant term
			if c == 1:
				if j==0:
					poly_tex+='1'
			elif c==-1:
				poly_tex += '-'
				if j==0:
					poly_tex+='1'
			else:
				poly_tex+=str(c)
			#format variable and exponent
			if j>0:
				poly_tex+=var
			if j>1:
				poly_tex+='^{{{}}}'.format(j)
				#alternate formatting because of string formatting rules
	#special handling if the polynomial was empty
	if not poly_tex:
		return '0'
	#deleting leading '+' sign
	if poly_tex[0]=='+':
		poly_tex=poly_tex[1:]
	return poly_tex

def format_macaulay_latex(pair):
	# print (pair)
	answer=[]
		#pair[0] is denom power
		#pair[1] is numer poly
	poly = pair[0]
	denom_power = pair[1]
	rational_string=''
	if denom_power>0:
		rational_string+='\\frac{'+format_poly_to_str(poly,format='latex')+'}'
		if denom_power>1:
			rational_string+= '{(1-t)^{'+str(denom_power)+'}}'
		else:
			rational_string+= '{1-t}'				
	else:
		rational_string+=format_poly_to_str(poly,format='latex')		
	answer.append(rational_string)
	c_poly=hilb_series_to_coefficient_poly(poly,denom_power)[::-1]
	if denom_power>2:
		c_poly_str='\\frac{'+format_poly_to_str(c_poly,format='latex',var='k')+'}'
		c_poly_str +='{'+str(denom_power-1)+'!}'
	else:
		c_poly_str=format_poly_to_str(c_poly,format='latex',var='k')
	answer.append(c_poly_str)
	valid=	'k > '+str(len(poly)-denom_power-1)
	answer.append(valid)
	return(answer)

def assemble_table_for_pdf(graph,data,single=False):
	#data is an object so that it's extendible
	#data should have Betti numbers
	output_builder=[]
	output_builder.append('\\begin{absolutelynopagebreak}\n')
	output_builder.append('\\[\n\\begin{tabular}{c}\n')
	if single:
		tempfile=open(graph+'.tex','r')
		output_builder.append(tempfile.read())
		tempfile.close()
	else:
		output_builder.append('\\input{')
		output_builder.append(graph)
		output_builder.append('}\n')
	output_builder.append('\\end{tabular}')
	output_builder.append('\\qquad{}\n')
	output_builder.append("\\renewcommand{\\arraystretch}{1}\n")
	output_builder.append('\\left(\\begin{array}{')
	for _ in range(len(data.adjacency[0])):
		output_builder.append('c')
	output_builder.append('}\n')
	for i in range(len(data.adjacency)):
		output_builder.append('&'.join([str(n) for n in data.adjacency[i]]))
		output_builder.append('\\\\\n')
	output_builder.append('\\end{array}\\right)')
	output_builder.append('\n\\]\n')
	if data.note:
		output_builder.append('\nNote: ')
		output_builder.append(data.note)
		output_builder.append('\n\\\\')
	if data.Betti_numbers:
		output_builder.append('\nBetti numbers $\\beta_i(B_k(\\Gamma))$:\n')
		row_length = max([len(row) for row in data.Betti_numbers.values()])
		cap = min(row_length,Betti_row_max_length)
		output_builder.append('\\begin{center}\n')
		output_builder.append("\\renewcommand{\\arraystretch}{2}\n")
		output_builder.append('\\begin{tabular}{l|')
		for j in range(cap+2):
			output_builder.append('c')
		output_builder.append('}\n')
		output_builder.append('$i\\backslash k$')
		for col_number in range(cap):
			output_builder.append(' & ')
			output_builder.append('$'+str(col_number)+'$')
		output_builder.append(" & Poincar\\'e series")
		output_builder.append(' & stable polynomial value')
		output_builder.append('\\\\\\hline\n')
		for row_number in range(data.homological_degree+1):
			output_builder.append('$'+str(row_number)+'$')
			for col_number in range(min(len(data.Betti_numbers[row_number]),cap)):
				output_builder.append(' & ')
				output_builder.append('$')
				if (row_number,col_number) in data.Betti_number_is_unstable:
					output_builder.append('\\mathbf{')
				output_builder.append(str(data.Betti_numbers[row_number][col_number]))
				if (row_number,col_number) in data.Betti_number_is_unstable:
					output_builder.append('}')
				output_builder.append('$')
			output_builder.append('\n & ')
			latex_polys = format_macaulay_latex(data.polys[row_number])
			output_builder.append('$'+latex_polys[0]+'$')
			output_builder.append(' & ')
			output_builder.append('$'+latex_polys[1]+'$')
			output_builder.append('\\\\\n')
		output_builder.append('\\end{tabular}\n')
	else:
		output_builder.append('No Betti number data available\n\\\\\n')
	output_builder.append('\\end{center}\n')
	output_builder.append('\\end{absolutelynopagebreak}')
	output_builder.append('\\vspace{20pt}\n\n\\hrule\n\n\\vspace{20pt}\n')
	return (''.join(output_builder))


def graph_section_maker(j):
	output_builder=	[]
	if j!=0:
		output_builder.append("\\clearpage\n")
	output_builder.append("\\subsection{Data for graphs with ")
	output_builder.append(str(j))
	if j==1:
		output_builder.append(' essential vertex}\n\\ \n\\vspace{10pt}\n\\hrule\n\\vspace{20pt}\n')
	else:
		output_builder.append(' essential vertices}\n\\ \n\\vspace{10pt}\n\\hrule\n\\vspace{20pt}\n')
	return (''.join(output_builder))

def assemble_pdf(graph_list,data_dic,single=False):
	output_builder=[]
	f = open(intro_file_base+'.tex','r')
	output_builder.append(f.read())
	f.close()
	output_builder.append(graph_list_header)
	for j in range(len(graph_list)):
		if graph_list[j]:
			output_builder.append(graph_section_maker(j))
			for graph in graph_list[j]:
				if graph in data_dic:
					output_builder.append(assemble_table_for_pdf(graph,data_dic[graph],single))
				else: #make an empty information thing
					output_builder.append(assemble_table_for_pdf(graph,data_class(),single))
	f = open(outro_file_base+'.tex','r')
	output_builder.append(f.read())
	f.close()
	return (''.join(output_builder))



