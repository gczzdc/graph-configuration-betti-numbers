from picture_maker import (
	compile_image,
	convert_image
)

from isomorphism_class_generation import generate_multigraphs

from collections import defaultdict

from macaulay_maker import run_macaulay_script, access_macaulay_file

from macaulay_parser import incorporate_macaulay_data

from constants import (
	css_file,
	generate_graphs,
	graphics_format,
	image_directory,
	max_edges,
	recompile_images,
	reconvert_images,
	run_macaulay,
	make_files,
	compile_main,
	ssh_upload,
	full_upload,
	loud_commands,
	tex_filename
)
from utility import scp, run
from latex_maker import compile_tex, write_tex
from html_maker import write_html
from graph_class import Graph
	
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

def graphs_by_essential_vertex(graphs):
	divided_list = defaultdict(list)
	for G in graphs:
		divided_list[len(G.get_essential_vertices())].append(G)
	return divided_list

def process_files(graphs, loud_commands):
	ordered_graphs = graphs_by_essential_vertex(graphs)
	write_tex(ordered_graphs, tex_filename)
	write_tex(ordered_graphs, tex_filename+'_single', single_file = True)
	write_html(ordered_graphs, 'index.html')


def upload_files(graphs, full_upload, loud_commands):
	scp(tex_filename+'.pdf', loud_commands)
	scp('index.html', loud_commands)
	if full_upload:
		scp(css_file, loud_commands)
		scp('{}/*.{}'.format(image_directory, graphics_format),
			subdirectory=image_directory,
			loud_commands=loud_commands)

def make_graphs(min_edges, max_edges):
	graphs=[]
	for j in range(min_edges, max_edges+1):
		for sparse6 in generate_multigraphs(j):
			G=Graph(sparse6)
			G.build_img()
			graphs.append(G)
	return graphs

def deal_with_trivial_graphs_by_hand(graphs):
	#deal with trivial graphs
	for G in graphs:
		G.build_VH()
		if G.edge_count >0:
			raise ValueError('Unexpected nontrivial graph')
		if len(G.stars) != 1:
			raise ValueError('Unexpected trivial graph')
		else:
			G.note='values calculated by hand'
			G.homological_degree=0
			G.Betti_numbers={0:[1,1,0]}
			G.Betti_number_is_unstable={(0,0),(0,1)}
			G.poincare_num_poly={0:[1,1]}
			G.poincare_denom_power={0:0}
			G.stable_poly_normalized={0:[]}
			G.validity=1	

def trivial_split(graphs):
	trivial = []
	nontrivial = []
	for G in graphs:
		G.build_VH()
		if G.edge_count:
			nontrivial.append(G)
		else:
			trivial.append(G)
	return (trivial, nontrivial)

def graph_generator(
	graphs=[],
	interactive=False,
	generate_graphs=generate_graphs, 
	min_edges=0,
	max_edges=max_edges,
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
		generate_graphs=yesno('generate graphs programmatically?', generate_graphs)
		run_macaulay=yesno('manually rerun macaulay scripts to determine homology',run_macaulay)
		recompile_images=yesno('generate and recompile tex files for images',recompile_images)
		reconvert_images=yesno('reconvert images for web', reconvert_images)
		make_files=yesno('make master tex and html files',make_files)
		compile_main=yesno('make master pdf',compile_main)
		ssh_upload=yesno('upload files to remote server',ssh_upload)
		if ssh_upload:
			full_upload=yesno('upload infrequently changed files',full_upload)
	total_time=0
	if generate_graphs:
		graphs = make_graphs(min_edges, max_edges)
	
	for j,G in enumerate(graphs):
		if G.has_image:
			if recompile_images:
				if loud_commands:
					print('recompiling {} of {}'.format(j+1, len(graphs)))
				compile_image(G, loud_commands)
			if reconvert_images:
				if loud_commands:
					print('reconverting {} of {}'.format(j+1, len(graphs)))
				convert_image(G, loud_commands)

	trivial, nontrivial = trivial_split(graphs)
	if not run_macaulay:
		for G in nontrivial:
			macaulay_results = access_macaulay_file(G)
			incorporate_macaulay_data(G,macaulay_results)
	else:
		for j,G in enumerate(nontrivial):
			if loud_commands:
				print('running script graph for {} of {}'.format(j+1, len(nontrivial)))
			macaulay_results = run_macaulay_script(G)
			total_time += macaulay_results[1]
			if loud_commands:
				print('{} seconds ({} total)'.format(round(macaulay_results[1],2), round(total_time,2)))
			incorporate_macaulay_data(G,macaulay_results[0])
		print ('{} seconds total, {} seconds average spent on core M2 calculation for {} graphs;'.format(
			round(total_time, 2), round(total_time/len(nontrivial),2), len(nontrivial)))
	deal_with_trivial_graphs_by_hand(trivial)
	if make_files:
		process_files(graphs,loud_commands)
	if compile_main:
		compile_tex(tex_filename,loud_commands)
		compile_tex(tex_filename+'_single', loud_commands)
	if ssh_upload:
		upload_files(graphs, full_upload,loud_commands)
	return graphs