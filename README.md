# SingleMolecule_DiffractionLimited
This repository contains the analysis code associated with diffraction-limited single-molecule image analysis, led by Florence Layburn. This manuscript has been submitted for publication under the title "Nanoscopic tau aggregates in Parkinson's disease", and has been submitted to BioRxiv: https://www.biorxiv.org/content/10.1101/2025.08.28.672923v1

Required software for image analysis:
- FIJI https://imagej.net/software/fiji/downloads
- FIJI plugin THUNDERSTORM https://zitmen.github.io/thunderstorm/
- Python version 3

Steps:
1. The FIJI macro requires images to be organised Experiment folder -> subfolders containing images -> images. The macro will loop over all the image-containing folders in the Experiment folder
2. After automated FIJI analysis is complete, data extraction can be performed using the python script provided. The index file must be included in the newly-created sub-folder of CSV file results (Created from THUNDERSTORM)
3. The output is a compiled file for all THUNDERSTORM results from all images, as well as a summary file with mean spot numbers and intensities. 
  
Example dataset:
- in the Images folder, raw single-molecule images were included, suitable to use with the accompanying analysis files
- Note: use the index file in the "example_index" folder for these image sets
