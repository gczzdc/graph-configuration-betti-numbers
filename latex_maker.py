from constants import (
	Betti_row_max_length,
	bib_command,
	compile_command,
	intro_tex,
	image_directory,
	loud_commands,
	outro_tex,
	data_section_title,
)

from utility import run

translator = {'\\':'\\backslash{}',\
				'^':'\\textasciicircum{}',\
				'{':'\\{',\
				'}':'\\}',\
				'_':'\\_',\
				'~':'\\textasciitilde{}',\
				'<':'\\textless{}',\
				'>':'\\textgreater{}',\
				'`':'\\textasciigrave{}'}

def latex_escape(string):
	for k in translator:
		string = string.replace(k, translator[k])
	return string


def compile_tex(filename, loud_commands=loud_commands):
	run((compile_command, filename), loud_commands)
	run((bib_command, filename), loud_commands)
	run((compile_command, filename), loud_commands)
	run((compile_command, filename), loud_commands)


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

def format_poincare_latex(num_poly, denom_power):
	# formats an internal data representation for tabular latex display
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
		poincare_tex+='\\frac{{{}}}'.format(format_poly_to_tex(num_poly))
		if denom_power>1:
			poincare_tex+= '{{(1-t)^{{{}}}}}'.format(denom_power)
		else:
			poincare_tex+= '{1-t}'				
	else:
		poincare_tex+=format_poly_to_tex(num_poly)
	return poincare_tex

def format_stable_latex(stable_poly, denom_power):
	if denom_power>2:
		stable_tex='\\frac{{{}}}'.format(format_poly_to_tex(stable_poly,var='k'))
		stable_tex +='{{{}!}}'.format(denom_power-1)
	else:
		stable_tex=format_poly_to_tex(stable_poly,var='k')
	return stable_tex



def broken_betti_number_table(graph):
	out_builder=[]
	if graph.note:
		out_builder.append('\nNote: {}\n\\\\\n'.format(graph.note))
	if not graph.Betti_numbers:
		output_builder.append('No Betti number data available\n\\\\\n')
	else:
		out_builder.append('Betti numbers $\\beta_i(B_k(\\Gamma))$:\n')
		row_length = max([len(row) for row in graph.Betti_numbers.values()])
		cap = min(row_length,Betti_row_max_length)
		out_builder.append('\\begin{center}\n')
		out_builder.append("\\renewcommand{\\arraystretch}{2}\n")
		out_builder.append('\\begin{{tabular}}{{l|{}}}\n'.format('c'*(cap+1)))
		out_builder.append('$i\\backslash k$')
		for col_number in range(cap):
			out_builder.append(' & ${}$'.format(col_number))
		out_builder.append(" & Poincar\\'e series")
		out_builder.append('\\\\\\hline\n')
		for row_number in range(graph.homological_degree+1):
			out_builder.append('${}$'.format(row_number))
			for col_number in range(min(len(graph.Betti_numbers[row_number]),cap)):
				this_number = graph.Betti_numbers[row_number][col_number]
				if (row_number,col_number) in graph.Betti_number_is_unstable:
					formatted_number = '\\mathbf{{{}}}'.format(this_number)
				else:
					formatted_number = this_number
				out_builder.append(' & ${}$'.format(formatted_number))
			out_builder.append('\n & ')
			poincare_poly = format_poincare_latex(graph.poincare_num_poly[row_number],
												graph.poincare_denom_power[row_number])
			out_builder.append('${}$ \\\\\n'.format(poincare_poly))
		out_builder.append('\\end{tabular}\n')

		out_builder.append('\\begin{tabular}{l|c}\n')
		out_builder.append('$i$ & stable polynomial value\n\\\\\\hline\n')
		for row_number in range(graph.homological_degree+1):
			out_builder.append('${}$ & '.format(row_number))
			stable_poly = format_stable_latex(graph.stable_poly_normalized[row_number],
												graph.poincare_denom_power[row_number])
			out_builder.append('${}$ \\\\\n'.format(stable_poly))
		out_builder.append('\\end{tabular}\n')	
		out_builder.append('\\end{center}\n')
	return ''.join(out_builder)

def make_table_header(graph, single_file):
	out_builder = []
	out_builder.append('\\begin{gather*}\n')
	if graph.has_image:
		out_builder.append('\\begin{tabular}{c}\n')
		if single_file:
			with open('{}/{}.tex'.format(image_directory, graph.filename),'r') as f:
				out_builder.append(f.read()) 
		else:
			out_builder.append('\\input{{{}/{}}}\n'.format(image_directory, graph.filename))
		out_builder.append('\\end{tabular}\n\\qquad{}\n')
	out_builder.append('\\\n')
	out_builder.append('\\\n')	
	out_builder.append("\\renewcommand{\\arraystretch}{1}\n")
	out_builder.append('\\left(\\begin{{array}}{{{}}}\n'.format('c'*len(graph.get_adjacency())))
	for row in graph.adjacency:
		out_builder.append('&'.join((str(n) for n in row)))
		out_builder.append('\\\\\n')
	out_builder.append('\\end{array}\\right)\n')
	out_builder.append('\\\\\n')
	out_builder.append('\\text{{{}}}\n'.format(latex_escape('>>sparse6<<{}'.format(graph.sparse6))))
	out_builder.append('\\end{gather*}\n')
	return ''.join(out_builder)

def assemble_table_for_tex(graph, single_file=False):
	out_builder=[]
	out_builder.append('\\begin{absolutelynopagebreak}\n')
	out_builder.append(make_table_header(graph, single_file))
	out_builder.append(broken_betti_number_table(graph))
	out_builder.append('\\end{absolutelynopagebreak}')
	out_builder.append('\\vspace{20pt}\n\n\\hrule\n\n\\vspace{20pt}\n')	
	return ''.join(out_builder)

def subsec_header_maker(n):
	out_builder=	[]
	if n!=0:
		out_builder.append("\\clearpage\n")
	if n!=1:
		out_builder.append("\\subsection{{Data for graphs with {} essential vertices}}\n".format(n))
	else:
		out_builder.append("\\subsection{Data for graphs with 1 essential vertex}\n")
	out_builder.append('\\ \n\\vspace{10pt}\n\\hrule\n\\vspace{20pt}\n')
	return ''.join(out_builder)

def build_betti_subsec(graph_list, n, single_file):
	subsec=subsec_header_maker(n)
	for graph in graph_list:
		subsec+= assemble_table_for_tex(graph,single_file)
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


def write_tex(graph_dic, file_base, single_file=False):
	with open(file_base+'.tex', 'w') as f:
		f.write(assemble_pdf(graph_dic, single_file))
