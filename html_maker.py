import constants
from bs4 import BeautifulSoup


todolist=[\
'need better format for graph name',\
'need to add check for existence of image',\
'need graph data class',\
'use beautifulsoup for html generation',\
'check about html escaping in bs html generation',\
'fix css',\
'rewrite format_macaulay',\
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
	overall_output.append(betti_info)
	return (overall_output)

def graph_html_section_maker(n):
	output_builder=	['<h3><a id=',]
	output_builder.append(str(n))
	output_builder.append("_vertices></a>\n Data for graphs with ")
	output_builder.append(str(n))
	if n !=1:
		output_builder.append(' essential vertices\n</h3>\n<hr>\n')
	else:
		output_builder.append(' essential vertex\n</h3>\n<hr>\n')	
	return (''.join(output_builder))

def assemble_html(graph_list,data_dic):
	# graph_list is a list or dictionary 
	# with integer keys n 
	# and values iterators of 
	# graphs with n vertices
	output_builder=[]
	with open(intro_file_base + '.html','r') as f:
		output_builder.append(f.read())
	output_builder.append(graph_html_header)
	output_builder.append('<div><ul>\n')
	for j in range(len(graph_list)):
		output_builder.append('<li><a href="#')
		output_builder.append(str(j))
		output_builder.append('_vertices">Graphs with ')
		output_builder.append(str(j))
		output_builder.append(' vertices</a></li>\n')
	output_builder.append('</ul></div>\n')
	for j in range(len(graph_list)):
		if graph_list[j]:
			output_builder.append(graph_html_section_maker(j))
			for graph in graph_list[j]:
				if graph in data_dic:
					output_builder.append(assemble_table_for_html(graph,data_dic[graph]))
				else: #make an empty information thing
					output_builder.append(assemble_table_for_html(graph,data_class()))
	# output_builder.append(graph_html_footer)
	with open(outro_file_base+'.html','r') as f:
		output_builder.append(f.read())
	return (''.join(output_builder))

def write_html(graph_list,data_dic,file_name):
	with open(file_name, 'w') as f:
		f.write(assemble_html(graph_list,data_dic))

