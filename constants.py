#for ssh
host='dreamhost:'
portscp=''
remote_directory='drummondcole.com/gabriel/academic/'+file_name+'/'

#for html
base_html='base.html'
css_file='graph_configs.css'

#for tex
intro_tex='intro.tex'
outro_tex='outro.tex'
tex_filename='graph_configuration_betti_numbers'
bib_command='bibtex'
compile_command ='pdflatex'

#for images
node_radius = '2.5pt'
img_start_tex='\\documentclass[crop,tikz]{standalone}\n\\begin{document}\n'
img_end_tex='\\end{document}'
graphics_format = 'svg'
convert_command =('pdf2svg', 'pdf')
cleanup_command = ('rm ','*')
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

#macaulay2 io
macaulay_scriptfile = 'temp.m2'
results_file='m2_graph_results'

#for control flow
loud_commands=True
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


