import constants

intro_tex=constants.intro_tex
outro_tex=constants.outro_tex
data_section_title=constants.data_section_title

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
	#special handling if the polynomial was empty
	if not poly_tex:
		return '0'
	#deleting leading '+' sign
	if poly_tex[0]=='+':
		poly_tex=poly_tex[1:]
	return poly_tex

def format_macaulay_latex(num_poly, denom_power, stable_poly):
	# formats an internal data representation for tabular html display
	#
	# input format: 
	#
	# num_poly is a list of coefficients of 
	# 	the numerator of the poincare series
	# denom_power is an int
	# stable_poly_str is a list of coefficients
	#	of the stable poly, normalized by the
	# 	appropriate factorial
	#
	# returns a pair of bs objects 
	# for the Poincare series 
	# and for the stable polynomial
	answer=[]
	poincare_tex=''
	if denom_power>0:
		poincare_tex+='\\frac{{{}}}'.format(format_poly_to_tex(poly))
		if denom_power>1:
			poincare_tex+= '{{(1-t)^{{{}}}}}'.format(denom_power)
		else:
			poincare_tex+= '{1-t}'				
	else:
		poincare_tex+=format_poly_to_tex(poly)		
	answer.append(poincare_tex)
	if denom_power>2:
		stable_tex='\\frac{{{}}}'.format(format_poly_to_tex(stable_poly,var='k'))
		stable_tex +='{{{}!}}'.format(denom_power-1)
	else:
		stable_tex=format_poly_to_tex(stable_poly,var='k')
	answer.append(stable_tex)
	return answer

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



def assemble_table_for_tex(graph, single_file=False):
	out_builder=[]
	out_builder.append('\\begin{absolutelynopagebreak}\n')
	out_builder.append(make_table_header(graph, single_file))
	out_builder.append(betti_number_table(graph))
	out_builder.append('\\end{absolutelynopagebreak}')
	out_builder.append('\\vspace{20pt}\n\n\\hrule\n\n\\vspace{20pt}\n')	
	return ''.join(out_builder)

def subsec_header_maker(n):
	out_builder=	[]
	if n!=0:
		out_builder.append("\\clearpage\n")
	if j!=1:
		out_builder.append("\\subsection{{Data for graphs with {} essential vertices}}\n".format(j))
	else:
		out_builder.append("\\subsection{Data for graphs with 1 essential vertex}\n")
	out_builder.append('\\ \n\\vspace{10pt}\n\\hrule\n\\vspace{20pt}\n')
	return ''.join(out_builder)

def build_betti_subsec(graph_list,n, single_file):
	subsec=subsec_header_builder(n)
	for graph in graph_list[n]:
		subsec+=append(assemble_table_for_tex(graph,single_file))
	return subsec


def assemble_pdf(graph_dic,single_file=False):
	# graph_dic is a dictionary 
	# with integer keys n 
	# and values iterators of 
	# graphs data with n essential vertices
	out_builder=[]
	with open(intro_tex, 'r') as f:
		out_builder.append(f.read())
	out_builder.append("\\clearpage\n")
	out_builder.append("\\section{{{}}}\n".format(data_section_title))
	out_builder.append("\\setcounter{subsection}{-1}\n")
	keys = [k for k in graph_dic if graph_dic[k]]
	keys.sort()
	for k in keys:
		out_builder.append(build_betti_subsec(graph_dic[k],k, single_file))
	with open(outro_tex,'r') as f:
		out_builder.append(f.read())
	return ''.join(out_builder)



