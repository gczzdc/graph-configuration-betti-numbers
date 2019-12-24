import constants

recompile_images = constants.recompile_images
reconvert_images = constants.reconvert_images
run_macaulay = constants.run_macaulay
make_files = constants.make_files
compile_main = constants.compile_main
ssh_upload = constants.ssh_upload
full_upload = constants.full_upload

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