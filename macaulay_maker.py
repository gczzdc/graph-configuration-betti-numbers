import constants

graph_order_of_magnitude=constants.graph_order_of_magnitude

def basic_enumerator(j, graph):
	return 'G{}'.format(str(j).rjust(graph_order_of_magnitude,'0'))

def basic_namer(graph):
	if graph.name:
		return graph.name
	return '>>sparse6<<{}'.format(graph.sparse6())

def batch_macaulay_script(graph_enumerator, 
						results_file, 
						name_function=basic_namer, 
						prefix_function=basic_enumerator
						):
	command = '-- file to compute homology of configuration space of a list of graphs\n\n'
	command += '"'+results_file+'" << close\n\n'
	for j,graph in enumerate(graph_enumerator):
		command+= make_macaulay_script(graph,
							results_file,
							append=True, 
							graph_name=name_function(graph), 
							prefix=prefix_function(j,graph))
	return command

def format_macaulay_comment(string):
	ans = ''
	for line in string.split('\n'):
		ans += '-- ' + line
	return ans

def format_macaulay_output(string):
	return '"{}"'.format(string.replace('"','\\"'))


def make_macaulay_script(graph, 
						script_file, 
						append=True, 
						graph_name='', 
						prefix=''):
	essential_vertices = graph.essential_vertices()
	V = len(essential_vertices)
	m_script ='-- macaulay script for homology of configuration spaces of the graph\n'
	m_script+= format_macaulay_comment(graph_name)+'\n'
	m_script+='R = ZZ['
	edge_vars=['e{}_{}'.format(prefix,n) for n in graph.edges()]
	m_script+= ', '.join(edge_vars)
	m_script+=']\n'
	#comes in h format:
	#total number of edges (starting from zero to e-1)
	#list whose elements at index j are the half edges of v_j
	#the list entries are the edge indices.
	#no data checking, assume every vertex is essential.
	for i in range(V):
		h0=essential_vertices[i][0]
		m_script+= 'C{}v{}=chainComplex{matrix{{'.format(prefix,i)
		m_script+= ','.join(['e{}_{}-e{}_{}'.format(prefix, h, prefix, h0) for h in essential_vertices[i][1:]])
		m_script+='}}}\n'
	m_script+='C{} = '.format(prefix)
	m_script += '**'.join(['C{}v{}'.format(prefix,i) for i in range(V)])
	m_script +='\n'
	for i in range(V+1):
		m_script+= 'H{}deg{}=HH_{}(C{})\n'.format(prefix,i,i,prefix)
		m_script+= 'p{}deg{}=hilbertSeries (H{}deg{}, Reduce=> true)\n'.format(prefix,i,prefix,i)
		m_script+= 'd{}deg{}=(denominator p{}deg{})#0#1 -- reduced power of denominator\n'.format(prefix,i,prefix,i)
		m_script+= 'n{}deg{}=(numerator p{}deg{})#0 -- format example 3T4-4T2+3T\n'.format(prefix,i,prefix,i)
		if append:
			m_script+='f = openOutAppend "{}"\n'.format(results_file)
		m_script+= 'f<< "Data for graph "<<{}<<endl<<'.format(format_macaulay_output(graph_name))
		m_script+='"homological degree "<<{}'.format(i)
		m_script+= ' <<endl<<"power of 1-T: "<<d{}deg{}'.format(prefix,i)
		m_script+= ' <<endl<<"numerator poly: "<<n{}deg{}'.format(prefix,i)
		m_script+= '<<endl<<endl\n'
		m_script+='f<<close\n\n'
	return m_script	




