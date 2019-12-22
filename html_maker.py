import constants
from bs4 import BeautifulSoup


todolist=[\
'need better format for graph name',\
'need graph data class',\
'use beautifulsoup for html generation',\
'check about html escaping in bs html generation',\
'fix css',\
'rewrite format_macaulay',\
'put image_exists in data_class',\
'put graph name in data_class',\
'change logic so that external data_dic is not needed',\
]

graphics_format = constants.graphics_format
intro_file_base= constants.intro_file_base
outro_file_base= constants.outro_file_base
data_section_title = constants.data_section_title
Betti_row_max_length = constants.Betti_row_max_length


def format_macaulay_html(pair):
	#data is a tuple with first element a denom_power string
	#second element a macaulay poly numerator
	answer=[]
	poly = pair[0]
	denom_power = pair[1]
	rational_string=''
	is_monomial=0
	for coefficient in poly:
		if coefficient:
			is_monomial+=1
	if is_monomial!=1 and denom_power>0:
		rational_string+='('
	rational_string+=format_poly_to_str(poly)
	if is_monomial!=1 and denom_power>0:
		rational_string+=')'
	if denom_power>0:
		rational_string+= '/(1-t)'
	if denom_power>1:
		rational_string+='<sup>'+str(denom_power)+'</sup>'
	answer.append(rational_string)
	c_poly=hilb_series_to_coefficient_poly(poly,denom_power)[::-1]
	if denom_power>2:
		c_poly_str='('+format_poly_to_str(c_poly,format='html',var='k')+')'
		c_poly_str +='/'+str(denom_power-1)+'!'
	else:
		c_poly_str=format_poly_to_str(c_poly,format='html',var='k')
	valid='k &gt; ' +str(len(poly)-denom_power-1)
	answer.append(c_poly_str)
	answer.append(valid)
	return(answer)


def graph_html_section(soup):
	section = soup.new_tag('section')
	section.append(soup.new_tag('h2'))
	section.h2.append(data_section_title)
	return section


def betti_number_table(gaph, data, soup):
	betti_info= soup.new_tag('div',style = 'width:100%;clear:both')
	betti_info.append(soup.new_tag('p',class_='centered'))
	if data.note:
		betti_info.p.append('Note: {}'.format(data.note))
		betti_info.p.append(soup.new_tag('br'))
	if not data.Betti_numbers:
		betti_info.p.append('No Betti number data available')
	else:
		betti_info.p.append('Betti numbers &beta;<sub>i</sub>(B<sub>k</sub>(&Gamma;)):')
		betti_table = soup.new_tag('p',class_='centered')
		row_length = max([len(row) for row in data.Betti_numbers.values()])
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
		for row_number in range(data.homological_degree+1):
			this_row=soup.new_tag('tr')
			this_row.append(soup.new_tag('th'))
			this_row.th.append(str(row_number))
			for col_number in range(min(len(data.Betti_numbers[row_number]),cap)):
				this_entry = soup.new_tag('td')
				this_entry.append(soup.new_tag('span'))
				if (row_number,col_number) in data.Betti_number_is_unstable:
					this_entry.span['style']='font-weight:900'
				this_row.append(this_entry)
			for col_number in range(cap-min(len(data.Betti_numbers[row_number]),cap)):
				this_row.append(soup.new_tag('td'))
			html_polys = format_macaulay_html(data.polys[row_number])
			Pseries = soup.new_tag('td')
			Pseries.append(html_polys[0])
			stable = soup.new_tag('td')
			stable.append(html_polys[1])
			this_row.append(Pseries)
			this_row.append(stable)
			betti_table.table.append(this_row)

		betti_info.append(betti_table)
	return betti_info


def make_table_header(graph, data, soup, image_exists):
	representations = soup.new_tag('div', class_='row')
	pic = soup.new_tag('div',class_='colleft')
	pic.append(soup.new_tag('p'))
	if image_exists:
		img_src = '{}.{}'.format(graph, graphics_format)
		alt_txt = 'picture of the graph {}'.format(graph)
		pic.p.append(soup.new_tag('img',src=img_src, alt=alt_txt, style='margin-right:20px'))
	representations.append(pic)	
	adjacency = soup.new_tag('div',class_='colright')
	adjacency.append(soup.new_tag('table', class_='matrix', style='display:inline-block;margin-left:20px'))
	for i in range(len(data.adjacency)):
		this_row = soup.new_tag('tr')
		for entry in data.adjacency[i]:
			this_entry = soup.new_tag('td',class_='matrixcell')
			this_entry.append(str(entry))
			this_row.append(this_entry)
		adjacency.table.append(this_row)
	representations.append(adjacency)
	return representations

def assemble_table_for_html(graph,data, soup, image_exists):
	overall_output = soup.new_tag('div')
	representations = make_table_header(graph, data, soup. image_exists)
	overall_output.append(representations)
	betti_info = betti_number_table(graph, data, soup)
	overall_output.append(betti_info)
	return (overall_output)

def graph_html_section_maker(soup, n):
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


def build_betti_subsec(graph_list,n,data_dic):
	subsec = BeautifulSoup('')
	subsec.append(graph_html_section_maker(subsec,n))
	for graph in graph_list[j]:
		data = data_dic[graph]
		image_exists = data.image_exists
		subsec.append(assemble_table_for_html(graph, data, subsec,image_exists))



def assemble_html(graph_list,data_dic):
	# graph_list is a list or dictionary 
	# with integer keys n 
	# and values iterators of 
	# graphs with n vertices
	with open(intro_file_base + '.html','r') as f:
		soup= BeautifulSoup(f.read())
	data_section = soup.new_tag('section')
	data_section.append(soup.new_tag('h2'))
	data_section.h2.append(data_section_title)
	keys = []
	for j in range(len(graph_list)):
		if graph_list[j]:
			keys.append(j)
	toc_div = build_toc(soup, keys)
	data_section.append(toc_div)
	for j in keys:
		this_subsec = build_betti_subsec(graph_list[j],j,data_dic)
		data_section.append(this_subsec)
	soup.html.body.append(data_section)
	return soup


def write_html(graph_list,data_dic,file_name):
	with open(file_name, 'w') as f:
		f.write(assemble_html(graph_list,data_dic).prettify())

