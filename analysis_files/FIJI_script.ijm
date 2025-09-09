//to use this script, select the experiment folder, which contains folders of images

// set camera settings
run("Camera setup", "offset=604.2 isemgain=true photons2adu=3.019 gainem=214.0 pixelsize=109.2");
setBatchMode("false");
dir = getDirectory("Choose");
folderlist = getFileList(dir);
fjpath = "C://Users//Florence//OneDrive - University of Cambridge//Desktop//fiji-win64//Fiji.app//"
for(j = 0; j < folderlist.length; j++) {
	showProgress(j+1, folderlist.length);
	subdir = dir + folderlist[j];
	resultsname = File.getName(subdir);
	resultsname = substring(resultsname, 0, 20);
	resultsname = resultsname + "_Results_TS/"; 
	svpath = subdir + resultsname;
	File.makeDirectory(svpath);
	//SBpath = subdir + "/SB/";
	//File.makeDirectory(SBpath);
	MyFunction(subdir);
}

// Closes the "Results" and "Log" windows and all image windows
function cleanUp() {
    requires("1.30e");
    if (isOpen("Results")) {
         selectWindow("Results"); 
         run("Close" );
    }
    if (isOpen("Log")) {
         selectWindow("Log");
         run("Close" );
    }
    while (nImages()>0) {
          selectImage(nImages());  
          run("Close");
    }
}
    
 
function MyFunction(j) {
	filelist = getFileList(subdir);
	for (i = 0; i< lengthOf(filelist); i ++) {
		if (endsWith(filelist[i], ".tif")){ 
			open(subdir + File.separator + filelist[i]);
			imagea = getTitle();
			root = substring(imagea,0,11);
			run("Z Project...", "start=10 projection=[Average Intensity]");
			//run("Enhance Contrast", "saturated=0.35");
			image1 = getTitle();
			selectWindow(imagea);
			close();
			run("Run analysis", "filter=[Wavelet filter (B-Spline)] scale=2.0 order=3 detector=[Centroid of connected components] watershed=false threshold=2*std(Wave.F1) estimator=[PSF: Integrated Gaussian] sigma=1.6 fitradius=5 method=[Maximum likelihood] full_image_fitting=false mfaenabled=false renderer=[Scatter plot] dxforce=false magnification=10.0 dx=10.0 colorizez=false threed=false dzforce=false repaint=50");
        	run("Export results", "filepath=loclist.csv fileformat=[CSV (comma separated)] sigma=true intensity=true chi2=false offset=false saveprotocol=true x=true y=true bkgstd=false id=true uncertainty=true frame=true detections=true");
			File.copy(fjpath+"loclist.csv", svpath+ "/"+ filelist[i] +"results.csv");
			//close();
			selectWindow("Scatter plot");
			close();
			//selectWindow(image1);
			//close();
			cleanUp();
			//run("Set Scale...", "distance=1 known=0.154 unit=µm");
			//run("Scale Bar...", "width=5 height=11 thickness=4 font=14 color=White background=None location=[Lower Right] horizontal bold hide overlay");
			//run("Flatten");
			//saveAs("tif", SBpath+ "/"+ root + "_auto.tif");
			}
		}
	}

print("All done");
