import constants
from bs4 import BeautifulSoup


todolist=[\
'fix css',\
'put image_exists in data_class as image_exists',\
'put graph name in data_class as name',\
'put formatted stable poly in data class',\
]

graphics_format = constants.graphics_format
base_html= constants.base_html
data_section_title = constants.data_section_title
Betti_row_max_length = constants.Betti_row_max_length

def format_poly_to_html(poly, var='t'):
	# format polynomial (list starting with degree zero coefficient) to html.
	soup=BeautifulSoup('')
	for j,c in enumerate(poly):
		# c is the jth cofficient starting with the constant term
		if c>0:
			#if the coefficient is positive, put in a plus sign
			#not necessary for negative coefficients
			soup.append('+')
		if c!=0:
			#don't write +-1 coefficients unless it's a constant term
			if c == 1:
				if j==0:
					soup.append('1')
			elif c==-1:
				soup.append('-')
				if j==0:
					soup.append('1')
			else:
				soup.append(str(c))
			#format variable and exponent
			if j>0:
				soup.append(var)
			if j>1:
				exp = soup.new_tag('sup')
				exp.append(str(j))
				soup.append(exp)
	#special handling if the polynomial was empty
	if soup.string is None:
		return BeautifulSoup('0')
	#deleting leading '+' sign
	if soup.contents[0][0]=='+':
		soup.contents[0].replace_with(soup.contents[0][1:])
	return soup


def format_macaulay_html(num_poly, denom_power, stable_poly):
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
	poincare_soup=BeautifulSoup('')
	monomial_count = sum((1 for coefficient in num_poly if coefficient))
	if monomial_count !=1 and denom_power>0:
		poincare_soup.append('(')
	num_poly_str = format_poly_to_html(num_poly)
	poincare_soup.append(num_poly_str)
	if monomial_count!=1 and denom_power>0:
		poincare_soup.append(')')
	if denom_power>0:
		poincare_soup.append('/(1-t)')
	if denom_power>1:
		power=BeautifulSoup('')
		power.append(power.new_tag('sup'))
		power.sup.append(str(denom_power))
		poincare_soup.append(power)
	answer.append(poincare_soup)
	stable_poly_str = format_poly_to_html(stable_poly)
	stable_soup = BeautifulSoup('')
	if denom_power>2:
		stable_soup.append('(')
		stable_soup.append(stable_poly_str)
		stable_soup.append(')/{}!'.format(denom_power-1))
	else:
		stable_soup.append(stable_poly_str)
	answer.append(stable_soup)
	return answer


def graph_html_section(soup):
	section = soup.new_tag('section')
	section.append(soup.new_tag('h2'))
	section.h2.append(data_section_title)
	return section


def betti_number_table(graph,soup):
	betti_info= soup.new_tag('div',style = 'width:100%;clear:both')
	betti_info.append(soup.new_tag('p',class_='centered'))
	if graph.note:
		betti_info.p.append('Note: {}'.format(graph.note))
		betti_info.p.append(soup.new_tag('br'))
	if not graph.Betti_numbers:
		betti_info.p.append('No Betti number data available')
	else:
		betti_info.p.append('Betti numbers &beta;<sub>i</sub>(B<sub>k</sub>(&Gamma;)):')
		betti_table = soup.new_tag('p',class_='centered')
		row_length = max([len(row) for row in graph.Betti_numbers.values()])
		cap = min(row_length,Betti_row_max_length)
		betti_table.append(soup.new_tag('table',class_='centered'))
		betti_table.table.append(soup.new_tag('tr'))
		betti_table.table.tr.append(soup.new_tag('th'))
		betti_table.table.tr.th.append('i&#92;k')
		for col_number in range(cap):
			this_header = soup.new_tag('th')
			this_header.append(str(col_number))
			betti_table.tr.append(this_header)
		Pseries_header = soup.new_tag('th')
		Pseries_header.append('Poincar&eacute; series')
		stable_header = soup.new_tag('th')
		stable_header.append('stable polynomial value')
		betti_table.table.tr.append(Pseries_header)
		betti_table.table.tr.append(stable_header)
		for row_number in range(graph.homological_degree+1):
			this_row=soup.new_tag('tr')
			this_row.append(soup.new_tag('th'))
			this_row.th.append(str(row_number))
			for col_number in range(min(len(graph.Betti_numbers[row_number]),cap)):
				this_entry = soup.new_tag('td')
				this_entry.append(soup.new_tag('span'))
				if (row_number,col_number) in graph.Betti_number_is_unstable:
					this_entry.span['style']='font-weight:900'
				this_row.append(this_entry)
			for col_number in range(cap-min(len(graph.Betti_numbers[row_number]),cap)):
				this_row.append(soup.new_tag('td'))
			html_polys = format_macaulay_html(*graph.polys[row_number])
			Pseries = soup.new_tag('td')
			Pseries.append(html_polys[0])
			stable = soup.new_tag('td')
			stable.append(html_polys[1])
			this_row.append(Pseries)
			this_row.append(stable)
			betti_table.table.append(this_row)

		betti_info.append(betti_table)
	return betti_info


def make_table_header(graph, soup):
	representations = soup.new_tag('div', class_='row')
	pic = soup.new_tag('div',class_='colleft')
	pic.append(soup.new_tag('p'))
	if graph.image_file:
		alt_txt = 'picture of the graph {}'.format(graph.name)
		pic.p.append(soup.new_tag('img',
					src=graph.image_file, 
					alt=alt_txt, 
					style='margin-right:20px'))
	representations.append(pic)	
	adjacency = soup.new_tag('div',class_='colright')
	adjacency.append(soup.new_tag('table', class_='matrix', style='display:inline-block;margin-left:20px'))
	for i in range(len(graph.adjacency)):
		this_row = soup.new_tag('tr')
		for entry in graph.adjacency[i]:
			this_entry = soup.new_tag('td',class_='matrixcell')
			this_entry.append(str(entry))
			this_row.append(this_entry)
		adjacency.table.append(this_row)
	representations.append(adjacency)
	return representations

def assemble_table_for_html(graph, soup):
	overall_output = soup.new_tag('div')
	representations = make_table_header(graph, soup)
	overall_output.append(representations)
	betti_info = betti_number_table(graph, soup)
	overall_output.append(betti_info)
	return (overall_output)

def subsec_header_maker(soup, n):
	section = soup.new_tag('h3')
	section_name = '{}_vertices'.format(n)
	section.append(soup.new_tag('a', id=section_name))
	if n!=1:
		section.append('Data for graphs with {} essential vertices'.format(n))
	else:
		section.append('Data for graphs with 1 essential vertex')
	section.append(soup.new_tag('hr'))
	return section

def build_toc(soup, items):
	toc_div = soup.new_tag('div')
	toc_div.append(soup.new_tag('ul'))
	for j in items:
		this_item = soup.new_tag('li')
		relative_link = '#{}_vertices'.format(j)
		this_item.append(soup.new_tag('a',href=relative_link))
		if j != 1:
			this_item.a.append('Graphs with {} essential vertices'.format(j))
		else:
			this_item.a.append('Graphs with 1 essential vertex')

		toc_div.ul.append(this_item)
	return toc_div


def build_betti_subsec(graph_list,n):
	subsec = BeautifulSoup('')
	subsec.append(subsec_header_maker(subsec,n))
	for graph in graph_list[n]:
		subsec.append(assemble_table_for_html(graph, subsec))
	return subsec



def assemble_html(graph_dic):
	# graph_dic is a dictionary 
	# with integer keys n 
	# and values iterators of 
	# graphs data with n essential vertices
	with open(base_html,'r') as f:
		soup= BeautifulSoup(f.read())
	data_section = soup.new_tag('section')
	data_section.append(soup.new_tag('h2'))
	data_section.h2.append(data_section_title)
	keys = [k for k in graph_dic if graph_dic[k]]
	keys.sort()
	toc_div = build_toc(soup, keys)
	data_section.append(toc_div)
	for k in keys:
		this_subsec = build_betti_subsec(graph_list[k],k)
		data_section.append(this_subsec)
	soup.html.body.append(data_section)
	return soup


def write_html(graph_list,data_dic,file_name):
	with open(file_name, 'w') as f:
		f.write(assemble_html(graph_list,data_dic).prettify())

