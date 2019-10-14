#to check:
#latex matches html (i've been checking html)

import math
import subprocess
import numpy as np

todolist=[\
'write code or find pre-made solution to position vertices automatically',\
'write code or find pre-made solution to generate graphs automatically',\
'factor polynomials',\
]

#
#
# CONFIGURATION
#
#


loud_commands=True

generate_images=False
#generate individual tex files

file_name='graph_configuration_betti_numbers'
# base_url='https://cgp.ibs.re.kr/~gabriel/'
base_url='https://drummondcole.com/gabriel/academic/'
make_files = True
#make overall data files

recompile_images=False
compile_main=False
compile_command='pdflatex'
bib_command='bibtex'
img_start_tex='\\documentclass[crop,tikz]{standalone}\n\\begin{document}\n'
img_end_tex='\\end{document}'
#tex to stand-alone pdf for image conversion

reconvert_images=False
# graphics_format = 'png'
# convert_command=('sips -s format png ', '.pdf --out ', '.png')
graphics_format = 'svg'
convert_command=('pdf2svg ', '.pdf ', '.svg')

#pdf to png

cleanup_source=False
cleanup_commands = ('rm ','.*')

# output choices for graphs
Betti_row_max_length = 20

macaulay=False
macaulay_outfile='macaulay_graph_results.txt'

#ssh

host='dreamhost:'
# host='cgphome.ibs.re.kr:'
# portscp=' -oPort=15880'
portscp=''
remote_directory='drummondcole.com/gabriel/academic/'+file_name+'/'
# remote_directory='public_html/'+file_name+'/'
ssh_upload = False
full_upload = False
css_file='graph_configs.css'


max_essential_vertices=4

# drawing choices for graphs

node_radius = "2.5pt"
# for nodes in graphs
#
# for putting in multiple edges.
# this is not a great solution, it would be better to be able to do this uniformly and automatically
# but it is good enough for now
# bend larger than +-90 starts to bend back so that 180 is straight again
# later for some graphs we'll shrink these in order to not have overlapping edges.
bend_dic={\
0:[],\
1:[0,],\
2:[-90,90],\
3:[-90,0,90],\
4:[-90,-25,25,90],\
5:[-90,-30,0,30,90],\
6:[-90,-40,-15,15,40,90]}

#
#
# TEXT FOR PRESENTATION
#
#
intro_file_base='intro'
outro_file_base='outro'


# title = 'Betti numbers of configuration spaces of small graphs'
# author = 'Gabriel C. Drummond-Cole'
# intro1 = (
# 	"The purpose of this document is to provide data about known Betti numbers "
# 	"of configuration spaces of small graphs in order to guide research and avoid "
# 	"duplicated effort.\n"
# 	"It currently contains information for connected multigraphs having at most six edges "
# 	"which contain no loops, no bivalent vertices, and no internal (i.e., non-leaf) bridges.\n"
# )
# intro2_latex=(
# 	"\nThe graph enumeration was done by hand and verified using Richard Mathar's preprint~\\cite{Mathar:SSG}.\n"
# 	"The computation was done using Macaulay2~\\cite{GraysonStillman:M2}.\n"
# 	'This approach was made possible by the polynomial action and finite generation property described in'
# 	'~\\cite{AnDrummondColeKnudsen:ESHGBG}.'
# 	"\n\n"
# 	)
# intro2_html=(
# 	"</p><p>"
# 	"The graph enumeration was done by hand and verified using Richard Mathar's preprint "
# 	'<a href="https://arxiv.org/abs/1709.09000">Statistics on Small Graphs</a>.\n'
# 	'The computation was done using <a href="http://www.math.uiuc.edu/Macaulay2/">Macaulay2</a>.\n'
# 	'This approach was made possible by the polynomial action and finite generation property described '
# 	'<a href="https://arxiv.org/abs/1806.05585">here</a>.'
# 	'</p><p>'
# 	)
# intro3=(
# 	"Information for graphs with loops can be obtained by reducing to loop-free graphs with the same number of edges.\n"
# 	"Information for a graph with bivalent vertices can be obtained from information for the graph obtained by smoothing "
# 	"the bivalent vertices.\n"
# 	"Information for disconnected graphs can be obtained from information for connected components.\n"
# 	"Information for graphs with an internal bridge can be obtained from information for the graphs obtained by cutting "
# 	"the edge into two leaves.\n"
# 	"Unstable values are indicated in bold.\n"
# 	)
data_section_title="Data for small graphs"

graph_list_header_builder=[]
#graph_list_header_builder.append(
# 	"\\documentclass{amsart}\n"
# 	"\\usepackage{tikz}\n"
# 	"\\usepackage{hyperref}\n"
# 	"\\usepackage{url}\n"
# 	"\\newenvironment{absolutelynopagebreak}\n"
# 	"{\\par\\nobreak\\vfil\\penalty0\\vfilneg\n"
# 	"\\vtop\\bgroup}\n"
# 	"{\\par\\xdef\\tpd{\\the\\prevdepth}\\egroup\n"
# 	"\\prevdepth=\\tpd}\n"
# 	"\\title{"
# 	)
# graph_list_header_builder.append(title)
# graph_list_header_builder.append((
# 	"}\n"
# 	"\\author{"
# 	))
# graph_list_header_builder.append(author)
# graph_list_header_builder.append((
# 	"}\n"
# 	"\\thanks{This work was supported by IBS-R003-D1.}"
# 	"\\begin{document}\n"
# 	"\\maketitle\n"
# 	"\\section{Introduction}\n"
# 	))
# graph_list_header_builder.append(intro1)
# graph_list_header_builder.append(intro2_latex)
# graph_list_header_builder.append(intro3)
# graph_list_header_builder.append('\n')
# graph_list_header_builder.append('A web version of this document is available ')
# graph_list_header_builder.append('\\href{')
# graph_list_header_builder.append(base_url+file_name+'/')
# graph_list_header_builder.append('}{here}')
# graph_list_header_builder.append('.\n')
# if todolist:
# 	graph_list_header_builder.append('\\subsection{To do}\n')
# 	graph_list_header_builder.append('\\begin{enumerate}\n')
# 	for todo in todolist:
# 		graph_list_header_builder.append('\\item ')
# 		graph_list_header_builder.append(todo)
# 		graph_list_header_builder.append('\n')
# 	graph_list_header_builder.append('\\end{enumerate}\n')
graph_list_header_builder.append("\\clearpage\n\\section{")
graph_list_header_builder.append(data_section_title)
graph_list_header_builder.append("}\n")
graph_list_header_builder.append("\\setcounter{subsection}{-1}")
graph_list_header=''.join(graph_list_header_builder)

# graph_list_footer=(
# 	"\\bibliographystyle{amsalpha}\n"
# 	"\\begin{thebibliography}{ADK18}\n"
# 	"\\bibitem[ADK18]{AnDrummondColeKnudsen:ESHGBG}\n"
# 	"Byung Hee An, Gabriel C. Drummond-Cole, and Ben Knudsen, "
# 	"\\emph{Edge stabilization in the homology of graph braid groups}, 2018, "
# 	"\\url{https://arxiv.org/abs/1806.05585}."
# 	"\\bibitem[GS92]{GraysonStillman:M2}\n"
# 	"Daniel R Grayson and Michael E. Stillman, \\emph{Macaulay2, a software system for research in algebraic geometry}, 1992--2019, "
# 	"available at \\url{http://www.math.uiuc.edu/Macaulay2/}\n"
# 	"\\bibitem[Mat17]{Mathar:SSG}\n"
# 	"Richard Mathar, \\emph{Statistics on small graphs}, 2017, \\url{https://arxiv.org/abs/1709.09000}."
# 	"\\end{thebibliography}"
# 	"\\end{document}\n")

graph_html_header_builder=[]
#graph_html_header.append('<html>\n'
# 	'<head>\n'
# 	'<link rel="stylesheet" type="text/css" href="graph_configs.css">'
# 	'<title>\n'
# 	)
# graph_html_header_builder.append(title)
# graph_html_header_builder.append((
# 	'\n</title>\n'
# 	'<body>\n'
# 	'<h2>'
# 	))
# graph_html_header_builder.append(title)
# graph_html_header_builder.append((
# 	'</h2><br>'
# 	'<section>\n'
# 	'<h2>Introduction</h2>\n'
# 	'<p>\n'
# 	))
# graph_html_header_builder.append(intro1)
# graph_html_header_builder.append(intro2_html)
# graph_html_header_builder.append(intro3)
# graph_html_header_builder.append((
# 	'</p>\n'))
# graph_html_header_builder.append((
# 	'<p>A pdf version of this document is available '
# 	'<a href="'))
# graph_html_header_builder.append(base_url)
# graph_html_header_builder.append(file_name)
# graph_html_header_builder.append('/')
# graph_html_header_builder.append(file_name)
# graph_html_header_builder.append((
# 	'.pdf">here</a>.\n'
# 	"This work was supported by IBS-R003-D1."
# 	'</p>\n'
# 	))
# if todolist:
# 	graph_html_header_builder.append('<h3>To do</h3>\n')
# 	graph_html_header_builder.append('<ol>\n')
# 	for todo in todolist:
# 		graph_html_header_builder.append('<li>')
# 		graph_html_header_builder.append(todo)
# 		graph_html_header_builder.append('</li>')
# 	graph_html_header_builder.append('</ol>\n')
graph_html_header_builder.append((
	'</section>\n'
	'<section>\n'
	"<h2>"
	))
graph_html_header_builder.append(data_section_title)
graph_html_header_builder.append((
	'</h2>\n'
	))


graph_html_header=''.join(graph_html_header_builder)

# graph_html_footer=('</section>\n</body>\n</html>\n')



#
#
# graph definitions
#
#


stardic={3:[(1,1,1),(3,1,1),(4,1,1)],4:[(1,1,1,1),(3,1,1,1)],5:[(1,1,1,1,1),],6:[(1,1,1,1,1,1),]}

graphs={}
#0 edges
graphs['isolated_vertex']=({0:(0,0)},{})
#1 edge
graphs['isolated_edge'] = ({0:(0,0),1:(0,1)},{(0,1):1})
#thetas
for j in range(3,7):
	graphs['theta'+str(j)] = ({0:(0,0),1:(1,0)},{(0,1):j})
for j in range(3,7):
	for edgecount in stardic[j]:
		this_edges={(0,k):edgecount[k-1] for k in range(1,j+1)}
		this_nodes={0:(0,0)}
		for i in range(j):
			angle = 2*i*math.pi/j-math.pi/2
			this_nodes[i+1] = (round(math.cos(angle),2),round(math.sin(angle),2))
		graphname='star'+str(j)+''.join(['_'+str(valence) for valence in edgecount if valence !=1])
		# print graphname
		graphs[graphname] = (this_nodes,this_edges)

for j,k,l in [(1,2,1), (1,3,1), (1,4,1),(3,2,1)]:
	graphs['a_graph_'+str(j)+'_'+str(k)+'_'+str(l)]=({0:(0,0) , 1:(0,1), 2:(0,2),3:(0,3)},{(0,1):j,(1,2):k,(2,3):l})

for j,k in [(3,1),(4,1),(5,1),(3,3)]:
	graphs['dart_graph_'+str(j)+'_'+str(k)]=({0:(0,0),1:(0,1),2:(0,2)},{(0,1):j,(1,2):k})

for j,k,l in [(2,2,1),(2,2,2),(3,2,1)]:
	graphs['triangle_graph_'+str(j)+'_'+str(k)+'_'+str(l)]=({0:(0,0),1:(-.5,-3**.5/2), 2:(.5,-3**.5/2)},{(0,1):j,(0,2):k,(1,2):l},.25)

for j,k,l,m in [(1,1,2,1),(1,1,3,1),(2,2,1,1),(2,1,2,1)]:
	graphs['triangle_graph_horn_'+str(j)+'_'+str(k)+'_'+str(l)+'_'+str(m)]=({0:(0,0),1:(-.5,-3**.5/2), 2:(.5,-3**.5/2), 3:(0,1)},{(0,1):j,(0,2):k,(1,2):l,(0,3):m},.25)
for j,k,l,m in [(1,1,2,1),(1,1,3,1)]:
	graphs['y_'+str(j)+'_'+str(k)+'_'+str(l)+'_'+str(m)]=({0:(0,0),1:(0,-1),2:(0,-2),3:(-3**.5/2,.5),4:(3**.5/2,.5)},{(0,1):l,(1,2):m,(0,3):j,(0,4):k})

# for j,k,l,m in [(1,1,2,1),]:
# 	graphs['y_'+str(j)+'_'+str(k)+'_'+str(l)+'_'+str(m)]=({0:(0,0),1:(0,-1),2:(0,-2),3:(-3**.5/2,.5),4:(3**.5/2,.5)},{(0,1):l,(1,2):m,(0,3):j,(0,4):k})

graphs['square_2_1_2_1']=({0:(0,0),1:(0,1),2:(1,1),3:(1,0)},{(0,1):1,(1,2):2,(2,3):1,(3,0):2},.25)
graphs['K4']=({0:(0,0),1:(0,1),2:(-3**.5/2,-.5),3:(3**.5/2,-.5)},{(0,1):1,(1,2):1,(1,3):1,(2,3):1,(0,3):1,(0,2):1})
graphs['caterpillar']=({0:(0,0),1:(0,1),2:(0,2),3:(0,3),4:(0,4)},{(0,1):1,(1,2):2,(2,3):2,(3,4):1})
graphs['hairytriangle']=({0:(0,0),1:(-.5,-3**.5/2), 2:(.5,-3**.5/2), 3:(-.5,3**.5/2),4:(.5,3**.5/2)},{(0,1):1,(0,2):1,(1,2):2,(0,3):1,(0,4):1},.25)
graphs['bull']=({0:(0,0),1:(-.5,-3**.5/2), 2:(.5,-3**.5/2), 3:(-.5-3**.5/2,-3**.5/2-.5),4:(.5+3**.5/2,-3**.5/2-.5)},{(0,1):2,(0,2):1,(1,2):1,(1,3):1,(2,4):1},.25)
graphs['augmented_triangle']=({0:(0,0),1:(-.5,-3**.5/2), 2:(.5,-3**.5/2), 3:(0,1),4:(-.5-3**.5/2,-3**.5/2-.5),5:(.5+3**.5/2,-3**.5/2-.5)},{(0,1):1,(0,2):1,(1,2):1,(0,3):1,(1,4):1,(2,5):1})
graphs['cross']=({0:(0,0) , 1:(0,1), 2:(0,2),3:(0,3),4:(-1,2),5:(1,2)},{(0,1):1,(1,2):2,(2,3):1,(2,4):1,(2,5):1})
graphs['bi_y']=({0:(-3**.5/2,.5),1:(3**.5/2,.5),2:(0,0),3:(0,-1),4:(-3**.5/2,-1.5),5:(3**.5/2,-1.5)},{(0,2):1,(1,2):1,(2,3):2,(3,4):1,(3,5):1})

extragraphs={}
# extragraphs['K5minus2']=({0:(0,0),1:(1,0),2:(0,1),3:(1,1),4:(.5,1.5)},{(0,1):1,(0,2):1,(0,4):1,(1,3):1,(1,4):1,(2,3):1,(2,4):1,(3,4):1}) #takes less than a minute
# extragraphs['K5minus1']=({0:(0,0),1:(1,0),2:(0,1),3:(1,1),4:(.5,1.5)},{(0,1):1,(0,2):1,(0,3):1,(0,4):1,(1,3):1,(1,4):1,(2,3):1,(2,4):1,(3,4):1}) #takes seven minutes

for j in range(3,20):
	extragraphs['theta'+str(j)] = ({0:(0,0),1:(1,0)},{(0,1):j})


# extragraphs['K5']=({0:(0,0),1:(1,0),2:(0,1),3:(1,1),4:(.5,1.5)},{(0,1):1,(0,2):1,(0,3):1,(0,4):1,(1,2):1,(1,3):1,(1,4):1,(2,3):1,(2,4):1,(3,4):1})
#
#
# MAIN
#
#


def graph_generator(
	interactive=False, 
	recompile_images=recompile_images,
	reconvert_images=reconvert_images,
	# cleanup_source=cleanup_source,
	macaulay=macaulay, 
	make_files=make_files,
	compile_main=compile_main,
	ssh_upload=ssh_upload,
	full_upload=full_upload
	):
	if interactive:
		recompile_images=yesno('generate and recompile tex files for images',recompile_images)
		reconvert_images=yesno('reconvert images for web', reconvert_images)
		# cleanup_source=yesno('delete image source files',cleanup_source)
		macaulay=yesno('run macaulay scripts to determine homology',macaulay)
		make_files=yesno('make master tex and html files',make_files)
		compile_main=yesno('make master pdf',compile_main)
		ssh_upload=yesno('upload files to remote server',ssh_upload)
		if ssh_upload:
			full_upload=yesno('upload infrequently changed files',full_upload)
	if reconvert_images:
		for graph in graphs:
			if loud_commands:
				print ('generating tex file for',graph)
			if len(graphs[graph])==2:
				graph_file(graph,graphs[graph][0],graphs[graph][1],narrow_flag=1,scale=2)
			else:
				graph_file(graph,graphs[graph][0],graphs[graph][1],narrow_flag=graphs[graph][2],scale=2)
			run(compile_command+ ' '+graph+'_img')		
			run(convert_command[0]+graph+'_img'+convert_command[1]+graph+convert_command[2])
			run(cleanup_commands[0]+graph+'_img'+cleanup_commands[1])
	if recompile_images:
		for graph in graphs:
			if loud_commands:
				print ('generating tex file for',graph)
			if len(graphs[graph])==2:
				graph_file(graph,graphs[graph][0],graphs[graph][1],narrow_flag=1,scale=1)
			else:
				graph_file(graph,graphs[graph][0],graphs[graph][1],narrow_flag=graphs[graph][2],scale=1)
			run(cleanup_commands[0]+graph+'_img'+cleanup_commands[1])
	if macaulay:
		batch_macaulay_script(graphs,macaulay_outfile)
		run('m2 --script temp.m2')
	if make_files:
		graph_data=process_macaulay_file(macaulay_outfile)
		graph_data['isolated_vertex'] = data_class()
		graph_data['isolated_vertex'].polys[0] = [[1,1],0,2]
		# graph_data['isolated_vertex'].latextriples[0]=['1','0',2]
		# graph_data['isolated_vertex'].htmltriples[0]=['1','0',2]
		graph_data['isolated_vertex'].homological_degree=0
		# graph_data['isolated_vertex'].adjacency=[[0,],]
		graph_data['isolated_vertex'].Betti_numbers[0]=[1,1,0]
		graph_data['isolated_vertex'].Betti_number_is_unstable.add((0,0))
		graph_data['isolated_vertex'].Betti_number_is_unstable.add((0,1))		
		graph_data['isolated_vertex'].note='values calculated by hand'
		graph_data['isolated_edge'] = data_class()
		# graph_data['isolated_edge'].latextriples[0]=['\\frac{1}{1-t}','1',2]
		# graph_data['isolated_edge'].htmltriples[0]=['1/(1-t)','1',2]
		graph_data['isolated_edge'].polys[0] = [[1,],1,0]
		# graph_data['isolated_edge'].adjacency=[[0,1],[1,0]]
		graph_data['isolated_edge'].homological_degree=0
		graph_data['isolated_edge'].Betti_numbers[0]=[1,]
		graph_data['isolated_edge'].note='values calculated by hand'
		for graph in graphs:
			v = len(graphs[graph][0])
			graph_data[graph].adjacency=[[0 for i in range(v)] for j in range(v)] 
			for e in graphs[graph][1]:
				graph_data[graph].adjacency[e[0]][e[1]] += graphs[graph][1][e]
				if e[0]!=e[1]:
					graph_data[graph].adjacency[e[1]][e[0]] += graphs[graph][1][e]
	
		# graph_data['isolated_edge']
		#for graph in graph_data:
			# print (graph)
			# print (graph_data[graph].Betti_numbers)
		ordered_graphs = graphs_by_essential_vertex(graphs,max_essential_vertices)
		assemble_file(ordered_graphs, graph_data, file_name+'.tex', 'pdf')
		assemble_file(ordered_graphs,graph_data, file_name+'_single.tex','pdf',single=True)
		assemble_file(ordered_graphs, graph_data, 'index.html', 'html')
	if compile_main:
		run(compile_command+' '+file_name)
		run(bib_command+' '+file_name)
		run(compile_command+' '+file_name)
		run(compile_command+' '+file_name)
	if ssh_upload:
		scp(file_name+'.pdf')
		scp('index.html')
		if full_upload:
			scp(css_file)
			for graph in graphs:
				scp(graph+'.'+graphics_format)
	if loud_commands:
		print ('total graphs', len(graphs))



#
#
# BASIC UTILITY
#
#



def run(whatever, loud=loud_commands):
	if loud:
		print (whatever)
	output=subprocess.getoutput(whatever)
	if loud and output:
		print (output)

def yesno(prompt, default):
	if default ==False:
		textadd = ' (default: no) '
	if default ==True:
		textadd = ' (default: yes) '
	respval = input(prompt+textadd)
	if respval.lower() in ['y','yes']:
		return(True)
	if respval.lower() in ['n','no']:
		return(False)
	return(default)

def factorial(n):
	if n<0:
		raise(Error)
	if n==0:
		return (1)
	return (n*factorial(n-1))


#
#
# change of presentation for data of graphs and polynomials
#
#

class data_class():
	def __init__(self):
		self.homological_degree=-1
		self.Betti_numbers={}
		self.Betti_number_is_unstable=set()
		# self.latextriples={}
		self.polys={}
		self.adjacency=None
		# self.htmltriples={}
		self.note=''

def essential_vertices(graph):
	vertices = {}
	for edge in graph:
		for v in edge:
			if v not in vertices:
				vertices[v]=0
			vertices[v]+=graph[edge]
	essential_vertices =0
	for v in vertices:
		if vertices[v]>2:
			essential_vertices+=1
	return (essential_vertices)


def e_pres_to_h_pres(graph):
	h_graph= [sum(graph[1].values()),]
	vertices=list(graph[0].keys())
	h_graph.append([[] for _ in graph[0]])
	counter = 0
	for vert_pair in graph[1]:
		for _ in range(graph[1][vert_pair]):
			for vert in vert_pair:
				h_graph[-1][vertices.index(vert)].append(counter)
			counter+=1
	return h_graph


def hilb_series_to_coefficient_poly(numerator, denom_power,cutoff=-1):
	# print (numerator, type(numerator))
	#hilb series is of the form numerator/(1-T)^denom_power
	#numerator is formatted as an array starting with LOWEST power.
	#start by generating the formula for coefficients
	#output formatted starting with HIGHEST power
	#should be divided by (denom_power-1) factorial
	ans = []
	if denom_power==0:
		return([])
	for i in range(len(numerator[:min(cutoff,len(numerator)-1)])+1):
		this_term=[numerator[i],]
		for j in range(1,denom_power):
			this_term=np.polymul(this_term, [1,j-i])
			# print(this_term)
		# print (ans, this_term)
		ans=np.polyadd(ans,this_term)
	return [int(n) for n in ans]

def graphs_by_essential_vertex(graphs,stop):
	response =[[] for _ in range(stop+1)]
	for graph in graphs:
		response[essential_vertices(graphs[graph][1])].append(graph)
	return (response)
# graphs_by_essential_vertex[0].append('isolated_vertex')
# graphs_by_essential_vertex[0].append('isolated_edge')

# graphs_by_essential_vertex[1].append('star3')
# graphs_by_essential_vertex[1].append('star4')
# graphs_by_essential_vertex[1].append('star5')
# graphs_by_essential_vertex[1].append('star6')

# graphs_by_essential_vertex[2].append('theta3')
# graphs_by_essential_vertex[2].append('theta4')
# graphs_by_essential_vertex[2].append('theta5')
# graphs_by_essential_vertex[2].append('theta6')
# graphs_by_essential_vertex[2].append('dart_graph_3_1')
# graphs_by_essential_vertex[2].append('dart_graph_4_1')
# graphs_by_essential_vertex[2].append('dart_graph_5_1')
# graphs_by_essential_vertex[2].append('star3_3')
# graphs_by_essential_vertex[2].append('star3_4')
# graphs_by_essential_vertex[2].append('star4_3')
# graphs_by_essential_vertex[2].append('bi_y')
# graphs_by_essential_vertex[2].append('y_1_1_2_1')
# graphs_by_essential_vertex[2].append('y_1_1_3_1')
# graphs_by_essential_vertex[2].append('a_graph_1_2_1')
# graphs_by_essential_vertex[2].append('a_graph_1_3_1')
# graphs_by_essential_vertex[2].append('a_graph_1_4_1')
# graphs_by_essential_vertex[2].append('cross')

# graphs_by_essential_vertex[3].append('bull')
# graphs_by_essential_vertex[3].append('augmented_triangle')
# graphs_by_essential_vertex[3].append('dart_graph_3_3')
# graphs_by_essential_vertex[3].append('a_graph_3_2_1')
# graphs_by_essential_vertex[3].append('caterpillar')
# graphs_by_essential_vertex[3].append('triangle_graph_2_2_1')
# graphs_by_essential_vertex[3].append('triangle_graph_2_2_2')
# graphs_by_essential_vertex[3].append('triangle_graph_3_2_1')
# graphs_by_essential_vertex[3].append('triangle_graph_horn_1_1_2_1')
# graphs_by_essential_vertex[3].append('triangle_graph_horn_1_1_3_1')
# graphs_by_essential_vertex[3].append('triangle_graph_horn_2_2_1_1')
# graphs_by_essential_vertex[3].append('triangle_graph_horn_2_1_2_1')
# graphs_by_essential_vertex[3].append('hairytriangle')

# graphs_by_essential_vertex[4].append('K4')
# graphs_by_essential_vertex[4].append('square_2_1_2_1')





#
#
# MACAULAY IO
#
#



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

def make_macaulay_script(graph,outfile,scriptfile,append=True, graph_name='',prefix=''):
	edges=range(graph[0])
	ess_vert= [j for j in graph[1] if len(j)>1]
	V=len(ess_vert)
	m_script=''
	m_script+='-- macaulay script for homology of configuration spaces of the graph '
	m_script+=graph_name+'\n'
	m_script+='R = ZZ['
	edge_vars=['e'+prefix+'_'+str(n) for n in edges]
	m_script+= ', '.join(edge_vars)
	m_script+=']\n'
	#comes in h format:
	#total number of edges (starting from zero to e-1)
	#list whose elements at index j are the half edges of v_j
	#the list entries are the edge indices.
	#no data checking, assume every vertex is essential.
	for i in range(V):
		h0=str(ess_vert[i][0])
		m_script+= 'C'+prefix+'v'+str(i)+'=chainComplex{matrix{{'
		m_script+= ','.join(['e'+prefix+'_'+str(h)+'-e'+prefix+'_'+h0 for h in ess_vert[i][1:]])
		m_script+='}}}\n'
	m_script+='C'+prefix+' = '
	m_script += '**'.join(['C'+prefix+'v'+str(i) for i in range(V)])
	# for i in range(V):
	# 	m_script+= 'C'+prefix+'v'+str(i)+'**'
	# # if V==0:
	# 	m_script+='chainComplex{matrix{{}}}**'
	m_script +='\n'
	for i in range(V+1):
		m_script+= 'H'+prefix+'deg'+str(i)+'=HH_'+str(i)+'(C'+prefix+')\n'
		m_script+= 'p'+prefix+'deg'+str(i)+'=hilbertSeries (H'+prefix+'deg'+str(i)+', Reduce=> true)\n'
		m_script+= 'd'+prefix+'deg'+str(i)+'=(denominator p'+prefix+'deg'+str(i)+')#0#1 -- reduced power of denominator\n'
		m_script+= 'n'+prefix+'deg'+str(i)+'=(numerator p'+prefix+'deg'+str(i)+')#0 -- format example 3T4-4T2+3T\n' 
		if append:
			m_script+='f = openOutAppend "'+outfile+'"\n'
		m_script+= 'f<< "Data for graph '+graph_name+'"<<endl<<' 
		m_script+='"homological degree "<<'+str(i)
		m_script+= ' <<endl<<"power of 1-T: "<<d' +prefix+'deg'+str(i)
		m_script+= ' <<endl<<"numerator poly: "<<n' +prefix+'deg'+str(i)
		m_script+= '<<endl<<endl\n'
		m_script+='f<<close\n\n'
	if append:
		f=open(scriptfile,'a')
	else:
		f=open(scriptfile,'w')
	f.write(m_script)
	f.close()
	
def batch_macaulay_script(dic_of_graphs,outfile,tempfile='temp.m2'):
	open(tempfile,'w').close()
	f= open(tempfile,'w')
	f.write('-- file to compute homology of configuration space of a list of graphs\n\n')
	f.write('"'+outfile+'" << close\n\n')
	f.close()
	for j,graph in enumerate(dic_of_graphs):
		h_graph = e_pres_to_h_pres(dic_of_graphs[graph])
		if graph in ['isolated_vertex','isolated_edge']:
		 	pass
		else:
			make_macaulay_script(h_graph,outfile,tempfile,append=True, graph_name=graph, prefix='G'+str(j)+'')

def parse_macaulay_poly(s):
	# print ('s',s,type(s))
	#this looks like eg. T3+6T4-3T5
	last_power=-1
	regime = 'coefficient'
	if s[0]=='-':
		coefficient_string='-'
		start_saltus=1
	else:
		coefficient_string=''
		start_saltus=0
	answer=[]
	for c in s[start_saltus:]:
		# print ('c',c,type(c))
		if c=='T':
			regime='exponent'
			exponent_string=''
			if not coefficient_string:
				#monic positive nonconstant leading term
				coefficient=1
			elif coefficient_string[-1] in '+-':
				coefficient_string+='1'
				#monic term
				coefficient=int(coefficient_string)
			else:
				coefficient=int(coefficient_string)
		elif c in ['+','-']:
			if regime=='coefficient':
				#found constant term
				coefficient=int(coefficient_string)
				answer.append(coefficient)
			else:
				if not exponent_string:
					exponent=1
				else:
					exponent=int(exponent_string)
				for _ in range(exponent-len(answer)):
					answer.append(0)
				answer.append(coefficient)
			regime='coefficient'
			coefficient_string=c
		elif regime=='coefficient':
			coefficient_string+=c
		elif regime=='exponent':
			exponent_string+=c
	if regime=='coefficient': #constant poly
		answer.append(int(coefficient_string))
	else:
		if not exponent_string:
			exponent=1
		else:
			exponent=int(exponent_string)
		for _ in range(exponent-len(answer)):
			answer.append(0)
		answer.append(coefficient)
	return(answer)

def process_macaulay_file(mf=macaulay_outfile):
	f= open(mf,'r')
	macaulay_data=f.readlines()
	f.close()
	answer = {}
	for j in range(0,len(macaulay_data),5):
		graph_name=macaulay_data[j].split('Data for graph')[1].strip()
		if graph_name not in answer:
			answer[graph_name]= data_class()
		degree = int(macaulay_data[j+1].split('homological degree')[1].strip())
		denom_power = int(macaulay_data[j+2].split(':')[1].strip())
		num_poly = parse_macaulay_poly(macaulay_data[j+3].split(':')[1].strip())
		valid = len(num_poly) - denom_power - 1
		answer[graph_name].polys[degree]=(num_poly,denom_power,valid)
		# answer[graph_name].latextriples[degree]=format_macaulay_latex([[denom_power,num_poly],])[0]
		# answer[graph_name].htmltriples[degree]=format_macaulay_html([[denom_power,num_poly],])[0]
		# print (graph_name,degree)
	for G in answer:
		answer[G].homological_degree=len(answer[G].polys)-1
		# print (k, 'degree', answer[k].homological_degree)
		length_test=[]
		for i in answer[G].polys:
			# converted_poly = hilb_series_to_coefficient_poly(answer[G].polys[i][0],answer[G].polys[i][1])
			# print (k, x, answer[k].latextriples[x])
			length_test.append(int(answer[G].polys[i][2]))
		maxlen = max(length_test)+1
		for i in range(answer[G].homological_degree+1):
			answer[G].Betti_numbers[i]=[]
			for k in range(maxlen+1):
				coef_poly= hilb_series_to_coefficient_poly(answer[G].polys[i][0],answer[G].polys[i][1],k)[::-1]
					#cutting off to get unstable value
				full_coef_poly = hilb_series_to_coefficient_poly(answer[G].polys[i][0],answer[G].polys[i][1])[::-1]
					#not cutting off to get stable prediction
				denom_fact = factorial(answer[G].polys[i][1]-1)
				this_Betti=0
				# print (coef_poly,full_coef_poly)
				# print (G)
				# input()
				for j,c in enumerate(coef_poly):
					this_Betti += k**j * c
				if this_Betti % denom_fact:
					print (G, i,k, this_Betti, denom_fact, 'error in fraction',answer[G].polys[i])
					raise(Exception)
				this_Betti =this_Betti // denom_fact
				this_Betti_stable=0
				for j,c in enumerate(full_coef_poly):
					this_Betti_stable += k**j * c
				this_Betti_stable = this_Betti_stable / denom_fact
				##
				answer[G].Betti_numbers[i].append(int(this_Betti))
				if this_Betti != this_Betti_stable:
					answer[G].Betti_number_is_unstable.add((i,k))
		# generate betti numbers
	return answer
#
#
# IO
#
#

def access_graph_data(graph):
	try:
		f = open(graph+'.data','r')
	except:
		return (False)
	raw_data=f.read()
	f.close()
	Betti_number_data =raw_data.split('Betti numbers')[1]
	rows = Betti_number_data.strip().split('\n')
	return ([[int(x) for x in row.split()] for row in rows])


def scp(file_name, loud_commands=loud_commands):
	run('sftp'+portscp+' '+host + remote_directory + " <<< $'put " + file_name+"\nexit'", loud_commands)



#
#
# output text and graphics formatting
#
#

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


def format_poly_to_str(poly, format='html', var='t'):
	rational_string=''
	for j,c in enumerate(poly):
		if c>0:
			rational_string+='+'
		if c!=0:
			if c == 1:
				if j==0:
					rational_string+='1'
			elif c==-1:
				rational_string += '-'
				if j==0:
					rational_string+='1'
			else:
				rational_string+=str(c)
			if j>0:
				rational_string+=var
			if j>1:
				if format=='html':
					rational_string+='<sup>'+str(j)+'</sup>'
				elif format=='latex':
					rational_string+='^{'+str(j)+'}'
	if not rational_string:
		return '0'
	if rational_string[0]=='+':
		rational_string=rational_string[1:]
	# if rational_string=='':
	# 	rational_string='1'
	
	return (rational_string)

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
	# else:
	# 	row_length=0
		cap = min(row_length,Betti_row_max_length)
		output_builder.append('\\begin{center}\n')
		output_builder.append("\\renewcommand{\\arraystretch}{2}\n")
		output_builder.append('\\begin{tabular}{l|')
		for j in range(cap+2):
			output_builder.append('c')
		output_builder.append('}\n')
		output_builder.append('$i\\backslash k$')
	# output_builder.append('\\[\\begin{tikzpicture}\n\\matrix (m) [matrix of nodes,\n')
	# output_builder.append('nodes in empty cells\n]\n{\n')
	# output_builder.append('\\begin{scope} \\tikz\\node[overlay] at (-.8ex,-0.4ex){\\footnotesize i};')
	# output_builder.append('\\tikz\\node[overlay] at (1ex,0.5ex){\\footnotesize k}; \\end{scope}\n')
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
		# answer[graph_name].latextriples[degree]=[0]
		# answer[graph_name].htmltriples[degree]=format_macaulay_html([[denom_power,num_poly],])[0]
			latex_polys = format_macaulay_latex(data.polys[row_number])
			output_builder.append('$'+latex_polys[0]+'$')
				# data.latextriples[row_number][0])
			output_builder.append(' & ')
			output_builder.append('$'+latex_polys[1]+'$')
			output_builder.append('\\\\\n')
		output_builder.append('\\end{tabular}\n')
	else:
		output_builder.append('No Betti number data available\n\\\\\n')
	# if data.latextriple:
	# 	output_builder.append()
	# 	# output_builder.append('\n\\\\\n')
	# 	# output_builder.append('\n\\\\\n')
	# 	# output_builder.append('a priori stability starts at weight ')
	# 	output_builder.append(data.latextriple[2])
	# 	output_builder.append('.\n\\\\\n')
	output_builder.append('\\end{center}\n')
	output_builder.append('\\end{absolutelynopagebreak}')
	output_builder.append('\\vspace{20pt}\n\n\\hrule\n\n\\vspace{20pt}\n')
	# output_builder.append('};\n')
	# output_builder.append('\\draw (m-1-1.north west) -- (m-1-1.south east);\n')
	# output_builder.append('\\draw (m-1-2.north west) -- (m-')	
	# output_builder.append(str(len(data.Betti_numbers)+1))
	# output_builder.append('-2.south west);\n')
	# output_builder.append('\\end{tikzpicture}\n\\]\n')
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


def assemble_table_for_html(graph,data):
		#data is an object so that it's extendible
	#data should have Betti numbers
	output_builder=[]
	output_builder.append('<div class="row">\n')
	# output_builder.append('<div class="colleft" style="width:50%;float:left;text-align:right">\n')
	output_builder.append('<div class="colleft">\n')
	output_builder.append('<p><img src="')
	output_builder.append(graph)
	output_builder.append('.')
	output_builder.append(graphics_format)
	output_builder.append('" alt="picture of the graph ')
	output_builder.append(graph)
	output_builder.append('" ')
	output_builder.append('style="margin-right:20px"')#;margin-bottom:20px;margin-top:10px"')
	output_builder.append('></p>\n')
	output_builder.append('</div>\n')
	# output_builder.append('<div class="colright" style="width:50%;float:left;text-align:left">\n')
	output_builder.append('<div class="colright">\n')
	output_builder.append('<table class="matrix" ')
	output_builder.append('style="display:inline-block;margin-left:20px">\n')#;margin-bottom:20px;margin-top:10px">\n')
	for i in range(len(data.adjacency)):
		output_builder.append('<tr>\n')
		for j in range(len(data.adjacency[0])):
			output_builder.append('<td class="matrixcell">\n')
			output_builder.append(str(data.adjacency[i][j]))
			output_builder.append('</td>\n')
		output_builder.append('</tr>\n')
	output_builder.append('</table>\n')
	output_builder.append('</div>\n')
	output_builder.append('</div>\n')
	# output_builder.append('<p class="centered">\n')
	# output_builder.append('<img src="')
	# output_builder.append(graph)
	# output_builder.append('.')
	# output_builder.append(graphics_format)
	# output_builder.append('" alt="picture of the graph ')
	# output_builder.append(graph)
	# output_builder.append('">\n')
	# output_builder.append('<table class="matrix">\n')
	# for i in range(len(data.adjacency)):
	# 	output_builder.append('<tr>\n')
	# 	for j in range(len(data.adjacency[0])):
	# 		output_builder.append('<td class="matrixcell">\n')
	# 		output_builder.append(str(data.adjacency[i][j]))
	# 		output_builder.append('</td>\n')
	# 	output_builder.append('</tr>\n')
	# output_builder.append('</table>\n')
	# output_builder.append('</p>\n')
	output_builder.append('<div style="width:100%;clear:both"><p class="centered">\n')
	if data.note:
		output_builder.append('Note: ')
		output_builder.append(data.note)
		output_builder.append('\n<br>\n')
	if data.Betti_numbers:
		output_builder.append('Betti numbers &beta;<sub>i</sub>(B<sub>k</sub>(&Gamma;)):')
		output_builder.append('\n</p>\n<p class="centered">')
		row_length = max([len(row) for row in data.Betti_numbers.values()])
		cap = min(row_length,Betti_row_max_length)
		output_builder.append('<table class="centered">\n')
		output_builder.append('<tr>\n')
		output_builder.append('<th>i&#92;k</th>\n')
		for col_number in range(cap):
			output_builder.append('<th>')
			output_builder.append(str(col_number))
			output_builder.append('</th>\n')
		output_builder.append('<th>')
		output_builder.append('Poincar&eacute; series')
		output_builder.append('</th>\n')
		output_builder.append('<th>')
		output_builder.append('stable polynomial value')
		output_builder.append('</th>\n')
		output_builder.append('</tr>\n')
		for row_number in range(data.homological_degree+1):
			output_builder.append('<tr>\n<th>')
			output_builder.append(str(row_number))
			output_builder.append('</th>\n')
			for col_number in range(min(len(data.Betti_numbers[row_number]),cap)):
				output_builder.append('<td>')
				if (row_number,col_number) in data.Betti_number_is_unstable:
					output_builder.append('<span style="font-weight:900">')
				output_builder.append(str(data.Betti_numbers[row_number][col_number]))
				if (row_number,col_number) in data.Betti_number_is_unstable:
					output_builder.append('</span>')
				output_builder.append('</td>\n')
			for col_number in range(cap-min(len(data.Betti_numbers[row_number]),cap)):
				output_builder.append('<td></td>\n')
			output_builder.append('<td>')
			html_polys = format_macaulay_html(data.polys[row_number])
			output_builder.append(html_polys[0])
			output_builder.append('</td>\n')
			output_builder.append('<td>')
			output_builder.append(html_polys[1])
			# output_builder.append(data.htmltriples[row_number][0])
			# output_builder.append(data.htmltriples[row_number][1])
			output_builder.append('</td>\n')
			output_builder.append('</tr>\n')
		output_builder.append('</table>\n')
	else:
		output_builder.append('No Betti number data available')
	output_builder.append('</p></div>\n')
	output_builder.append('<hr>\n')
	return (''.join(output_builder))

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
	output_builder=[]
	f = open(intro_file_base+'.html','r')
	output_builder.append(f.read())
	f.close()
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
	f = open(outro_file_base+'.html','r')
	output_builder.append(f.read())
	f.close()
	return (''.join(output_builder))

def assemble_file(graph_list,data_dic,file_name,filetype='pdf',single=False):
	f = open(file_name, 'w')
	if filetype=='pdf':
		f.write(assemble_pdf(graph_list,data_dic,single))
	elif filetype=='html':
		f.write(assemble_html(graph_list,data_dic))
	f.close()
	return






# for graph in graphs:
	# these_numbers = access_graph_data(graph)
	# if these_numbers:
	# graph_data[graph]=data_class()
		# graph_data[graph].Betti_numbers = these_numbers


# fake_data=data_class()
# fake_data.Betti_numbers=[[2,10,3,5],[1,2],[0,0,10,11,1,4,9]]

# assemble_file(graphs_by_essential_vertex,{'star3':fake_data},'test.tex','pdf')
# assemble_file(graphs_by_essential_vertex,graph_data,'test.html','html')


