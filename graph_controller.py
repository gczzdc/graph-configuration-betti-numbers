from picture_maker import (
	compile_image,
	convert_image
)

from collections import defaultdict

from macaulay_maker import make_macaulay_script

from constants import (
	recompile_images,
	reconvert_images,
	run_macaulay,
	make_files,
	compile_main,
	ssh_upload,
	full_upload,
	loud_commands
)
from utility import scp
from latex_maker import compile_tex
	
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

def process_files(graphs):
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
def graphs_by_essential_vertex(graphs):
	divided_list = defaultdict(list)
	for G in graphs:
		divided_list[G.essential_vertices].append(G)
	return divided_list
	ordered_graphs = graphs_by_essential_vertex(graphs,max_essential_vertices)
	assemble_file(ordered_graphs, graph_data, file_name+'.tex', 'pdf')
	assemble_file(ordered_graphs,graph_data, file_name+'_single.tex','pdf',single=True)
	assemble_file(ordered_graphs, graph_data, 'index.html', 'html')

def upload_files(graphs, full_upload,loud_commands):
	scp(tex_filename+'.pdf', loud_commands)
	scp('index.html', loud_commands)
	if full_upload:
		scp(css_file, loud_commands)
		for G in graphs:
			if G.has_image: 
				scp('{}.{}'.format(G.filename,graphics_format))

def graph_generator(
	graphs,
	interactive=False, 
	recompile_images=recompile_images,
	reconvert_images=reconvert_images,
	run_macaulay=run_macaulay, 
	make_files=make_files,
	compile_main=compile_main,
	ssh_upload=ssh_upload,
	full_upload=full_upload,
	loud_commands=loud_commands
	):
	if interactive:
		recompile_images=yesno('generate and recompile tex files for images',recompile_images)
		reconvert_images=yesno('reconvert images for web', reconvert_images)
		run_macaulay=yesno('run macaulay scripts to determine homology',run_macaulay)
		make_files=yesno('make master tex and html files',make_files)
		compile_main=yesno('make master pdf',compile_main)
		ssh_upload=yesno('upload files to remote server',ssh_upload)
		if ssh_upload:
			full_upload=yesno('upload infrequently changed files',full_upload)
	total_time=0
	for j,G in enumerate(graphs):
		if G.has_image:
			if recompile_images:
				compile_image(G, loud_commands)
			if reconvert_images:
				convert_image(G, loud_commands)
		if run_macaulay:
			macaulay_results = run_macaulay_script(G,j)
			total_time += macaulay_results[1]
			incorporate_macaulay_data(G,macaulay_results[0])
	if make_files:
		process_files(graphs,loud_commands)
	if compile_main:
		compile_tex(graphs,loud_commands)
	if ssh_upload:
		upload_files(graphs, full_upload,loud_commands)