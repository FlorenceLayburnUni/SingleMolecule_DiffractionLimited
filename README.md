# SingleMolecule_DiffractionLimited
This repository contains the analysis code associated with diffraction-limited single-molecule image analysis, led by Florence Layburn. This manuscript has been submitted for publication under the title "Nanoscopic tau aggregates in Parkinson's disease", and has been submitted to BioRxiv: https://www.biorxiv.org/content/10.1101/2025.08.28.672923v1

Required software for image analysis:
- FIJI https://imagej.net/software/fiji/downloads
- FIJI plugin THUNDERSTORM https://zitmen.github.io/thunderstorm/
- Python version 3 (tested on v 3.10.5)
- the expected install time for these software is <1 hour

Steps:
1. The FIJI macro requires images to be organised: Experiment folder/subfolders containing images/images. The macro will loop over all the image-containing folders in the Experiment folder
2. Next, the index file must be updated and included in the newly-created sub-folder of CSV file results before data extraction. So organisation looks like: Experiment folder/subfolders containing images/images/Results folder (put index file in here)
3. Now run the data extraction file in Python, only updating the file path to the Experiment folder is needed
4. The output is a compiled file for all THUNDERSTORM results from all images, as well as a summary file with mean spot numbers and intensities. These are CSV files that can be used for subsequent statistical analysis ie using R
5. The expected runtime depends on the number of images being analysed, for one folder of 360 images takes approximately 1 hour. Data extraction takes <30 seconds
Note: this analysis assumes that images are 50 frames. For different frame numbers, just edit the multiplication factor in data extraction to the desired number.
  
Example dataset:
- in the Images folder, raw single-molecule images were included, suitable to use with the accompanying analysis files
- Note: use the index file in the "example_index" folder for these image sets
