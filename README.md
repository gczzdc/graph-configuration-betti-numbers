# graph-configuration-betti-numbers
This repository consists of tools and wrappers for the computation of the Betti numbers of configuration spaces of graphs. 

More information about the mathematics behind the package is contained in headless.html and intro.tex, which should contain the same information.

See https://drummondcole.com/gabriel/academic/graph_configuration_betti_numbers/ for the output of the main scripts here.

Dependencies:

The scripts use geng and multig (packaged with nauty) for graph generation. 
To use that functionality, these two programs should be in the local directory (not in the path).

The scripts use macaulay2 for the core computation.  
To use that functionality, M2 should be in the path. 

The scripts use pdflatex and pdf2svg for image generation and conversion. 
To use that functionality, these two programs should be in the path. 

The scripts use pdflatex and bibtex for pdf generation. 
To use that functionality, these two programs should be in the path.

The scripts use yattag for html generation.
To use that functionality, this python package should be installed

The scripts use sftp and my server for uploading. 
To use that functionality, sftp should be in the path. 
You should change the server settings in constansts.py to something you can log into. 
