from yattag import Doc



from constants import (
	graphics_format,
	headless_html,
	image_directory,
	data_section_title,
	Betti_row_max_length
)

def insert_poly_to_html(poly, line, text, var='t', ):
	# format polynomial (list starting with degree zero coefficient) to html.
	monomial_count = sum((1 for c in poly if c))
	#special handling if the polynomial was empty
	if monomial_count==0:
		text('0')
	seen_first_term=False
	for j,c in enumerate(poly):
		# c is the jth cofficient starting with the constant term
		if c>0:
			#if the coefficient is positive, put in a plus sign
			#not necessary for negative coefficients
			if seen_first_term:
				text('+')
			else:
				seen_first_term=True
		if c!=0:
			seen_first_term=True
			#don't write +-1 coefficients unless it's a constant term
			if c == 1:
				if j==0:
					text('1')
			elif c==-1:
				text('-')
				if j==0:
					text('1')
			else:
				text(str(c))
			#format variable and exponent
			if j>0:
				text(var)
			if j>1:
				line('sup', str(j))

def insert_poincare_poly_to_html(num_poly, denom_power, line, text):
	# formats an internal data representation for tabular html display
	#
	# input format: 
	#
	# num_poly is a list of coefficients of 
	# 	the numerator of the poincare series
	# 	by increasing degree
	# denom_power is an int
	# stable_poly_str is a list of coefficients
	#	of the stable poly, normalized by the
	# 	appropriate factorial
	#   by increasing degree
	#
	# returns a pair of bs objects 
	# for the Poincare series 
	# and for the stable polynomial
	answer=[]
	monomial_count = sum((1 for coefficient in num_poly if coefficient))
	if monomial_count !=1 and denom_power>0:
		text('(')
	insert_poly_to_html(num_poly, line, text)
	if monomial_count!=1 and denom_power>0:
		text(')')
	if denom_power>0:
		text('/(1-t)')
	if denom_power>1:
		line('sup',str(denom_power))

def insert_stable_poly_to_html(stable_poly, denom_power, line, text):
	monomial_count = sum((1 for coefficient in stable_poly if coefficient))
	if denom_power>2 and monomial_count>1:
		text('(')
	insert_poly_to_html(stable_poly, line, text)
	if denom_power>2 and monomial_count>1:
		text(')')
	if denom_power>2:
		text('/{}!'.format(denom_power-1))

def betti_number_table(graph, tag, line, stag, text, asis, attr):
	row_length = max([len(row) for row in graph.Betti_numbers.values()])
	cap = min(row_length,Betti_row_max_length)
	with tag('div', style='width:100%;clear:both'):
		with tag('p', klass='centered'):
			if graph.note:
				text('Note: {}'.format(graph.note))
				stag('br')			
			if not graph.Betti_numbers:
				text('No Betti number data available')
			else:
				asis('Betti numbers &beta;')
				line('sub','i')
				text('(B')
				line('sub','k')
				asis('(&Gamma;)):')
			with tag('p', klass='centered'):
				with tag('table',klass='centered'):
					with tag('tr'):
						with tag('th'):
							asis('i&#92;k')
						for col_number in range(cap):
							line('th',str(col_number))
						with tag('th'):
							asis('Poincar&eacute; series')
						line('th', 'stable polynomial value')
					for row_number in range(graph.homological_degree+1):
						with tag('tr'):
							line('th', str(row_number))
							for col_number in range(min(
									len(graph.Betti_numbers[row_number]),
									cap)):
								with tag('td'):
									with tag('span'):
										if (row_number,col_number) in graph.Betti_number_is_unstable:
											attr(style='font-weight:900')
										text(str(graph.Betti_numbers[row_number][col_number]))
							with tag('td'):
								insert_poincare_poly_to_html(
									graph.poincare_num_poly[row_number], 
									graph.poincare_denom_power[row_number], 
									line, 
									text)
							with tag('td'):
								insert_stable_poly_to_html(
									graph.stable_poly_normalized[row_number],
									graph.poincare_denom_power[row_number],
									line,
									text)


def make_table_header(graph, tag, line, stag, text):
	with tag('div', klass='row'):
		with tag('div', klass='colleft'):
			with tag('p', klass='centered', style='margin-right:20px'):
				alt_txt = 'picture of the graph {}'.format(graph.sparse6)
				description = '>>sparse6<<{}'.format(graph.sparse6)
				if graph.has_image:
					stag('img',
						src='{}/{}'.format(
									image_directory,
									graph.image_filename()), 
						alt=alt_txt)
					stag('br')
				text(description)
		with tag('div', klass='colright'):
			with tag('table', 
					klass='matrix',
					style='display:inline-block;margin-left:20px'):
				for row in graph.get_adjacency():
					with tag('tr'):
						for entry in row:
							line('td', str(entry), klass='matrixcell')


def assemble_table_for_html(graph, tag, line, stag, text, asis, attr):
	with tag('div'):
		make_table_header(graph, tag, line, stag, text)
		betti_number_table(graph, tag, line, stag, text, asis, attr)
		stag('hr')

def subsec_header_maker(n, tag, stag, text):
	section_name = '{}_vertices'.format(n)
	with tag('h3'):
		with tag('a', id=section_name):
			if n!=1:
				text('Data for graphs with {} essential vertices'.format(n))
			else:
				text('Data for graphs with 1 essential vertex')
	stag('hr')

def build_toc(items, tag, text):
	with tag('div'):
		with tag('ul'):
			for j in items:
				with tag('li'):
					relative_link = '#{}_vertices'.format(j)
					with tag('a', href=relative_link):
						if j != 1:
							text('Graphs with {} essential vertices'.format(j))
						else:
							text('Graphs with 1 essential vertex')

def build_betti_subsec(graph_list, n, tag, line, stag, text, asis, attr):
	subsec_header_maker(n, tag, stag, text)
	for graph in graph_list:
		assemble_table_for_html(graph, tag, line, stag, text, asis, attr)

def assemble_html(graph_dic):
	# graph_dic is a dictionary 
	# with integer keys n 
	# and values iterators of 
	# graphs data with n essential vertices
	page, tag, text = Doc().tagtext()
	line = page.line
	stag = page.stag
	asis = page.asis
	attr = page.attr

	with open(headless_html,'r') as f:
		first_part = f.read()

	with tag('html'):
		with tag('head'):
			stag('link', ('type','text/css'), rel='stylesheet', href='graph_configs.css')
			line('title','Betti numbers of unordered configuration spaces of small graphs')
			line('style','body {box-sizing: border-box;}')
		with tag('body'):
			asis(first_part)
			keys = [k for k in graph_dic if graph_dic[k]]
			keys.sort()
			with tag('section'):
				line('h2',data_section_title)
				build_toc(keys, tag, text)
				for k in keys:
					build_betti_subsec(graph_dic[k], 
										k, 
										tag, 
										line,
										stag, 
										text, 
										asis, 
										attr)

					
	return page.getvalue()

def write_html(graph_dic, file_name):
	with open(file_name, 'w') as f:
		f.write(assemble_html(graph_dic))

