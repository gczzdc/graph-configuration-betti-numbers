#for ssh
host='drummondcole.com:'
directory_name='graph_configuration_betti_numbers'
remote_directory='drummondcole.com/gabriel/academic/'+directory_name+'/'

#for html
headless_html='headless.html'
css_file='graph_configs.css'

#for tex
intro_tex='intro.tex'
outro_tex='outro.tex'
tex_filename='graph_configuration_betti_numbers'
bib_command='bibtex'
compile_command ='pdflatex'

#for images
node_radius = '1.5pt'
img_start_tex='\\documentclass[crop,tikz]{standalone}\n\\begin{document}\n'
img_end_tex='\\end{document}'
graphics_format = 'svg'
convert_command =('pdf2svg', 'pdf')
cleanup_command = ('rm','*')
image_directory = 'img'

#macaulay2 io
macaulay_scriptfile = 'temp.m2'
results_file='m2_graph_results'
macaulay_directory='m2'

#for control flow
loud_commands=False
generate_graphs=True
max_edges=6
recompile_images=False
reconvert_images=False
run_macaulay=False
make_files = True
compile_main=False
ssh_upload = False
full_upload = False

#for display and utility
data_section_title="Data for small graphs"
Betti_row_max_length = 20
graph_order_of_magnitude=4


