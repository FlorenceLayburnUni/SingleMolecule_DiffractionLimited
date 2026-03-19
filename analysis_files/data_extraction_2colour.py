import os
import subprocess
import pandas as pd
import re
from tqdm import tqdm
from os import walk
import xlrd
import shutil
import xlrd
import xlwt
import xlsxwriter
import numpy as np
import openpyxl
from pandas.errors import EmptyDataError
from openpyxl import load_workbook
import random

##Select folder of 2 colour image results files
##Output: a file similar to comdet per FOV, matching the colocalised points by index. 
##Output 2: a summary file with the number in each channel and the number colocalised per FOV
 

rootdir = 'G://2026//100326_AMYTRACKER_tau//'
subdirs = []
for subdir, dirnames, filenames in os.walk(rootdir):
    for dname in dirnames:
        if dname.endswith('Results_TS'):
            path = subdir + '/' + dname
            name =  dname[0:20] 
            
            dfs = pd.read_excel(path +'/index.xlsx',  header = None, index_col = None, sheet_name = None)
            
            sheet_list = []

            #Parse through the sheets in the Excel file, changing the dataframe to long instead of wide, removing the default index column
            #Add the dataframes to a list of DF's
            for key, value in dfs.items():
                sheet = pd.melt(value, value_name = key).drop('variable', axis = 1) 
                sheet_list.append(sheet)

            #Combine the dataframes from the list
            index1 = pd.concat(sheet_list, axis =1)
            index1 = index1.applymap(lambda x: x.strip() if isinstance(x, str) else x)
            
            
            ##2-colour analysis begins here
            dfs_ground = []
            dfs_compare = []
            fovs = []
            
            count_ground = []
            count_compare = []
            count_colocalised1 = []
            intensity_ground = []
            intensity_compare = []

            for file in os.listdir(path):
                filename = os.fsdecode(file)
                if filename.endswith('641.tifresults.csv'):
                    fovs.append(filename[:4])
                    df_ground = pd.read_csv(path + '/' + filename,  index_col = None)
                    if df_ground.empty:    # check if file is empty
                        columns = {
                            "Position": [filename[:4]],
                            "FOV": [filename[:10]],
                            "Channel": [filename[11:14]],
                            "id": [None],
                            "frame": [None],
                            "x [nm]" : [0],
                            "y [nm]": [0],
                            "sigma [nm]": [None],
                            "intensity [photon]": [0],
                            "uncertainty [nm]": [None]}
                        df_g = pd.DataFrame(columns)
                        dfs_ground.append(df_g)
                        count_ground.append(0)
                        intensity_ground.append(0)
                        
                        #count_colocalised1.append(0)
                                
                    else:
                        df_ground.insert(0, 'Position', filename[:4])
                        df_ground.insert(1, 'FOV', filename[:10])
                        df_ground.insert(2, 'Channel', filename[11:14])
                        dfs_ground.append(df_ground)
                        count_ground.append(len(df_ground))
                        intensity_ground.append(df_ground["intensity [photon]"].mean())
                        #count_colocalised1.append("")

                #elif filename.endswith('488.tifresults.csv'):
                elif filename.endswith('488.tifresults_rotated.csv'):
                    df_compare = pd.read_csv(path + '/' + filename,  index_col = None)
                    if df_compare.empty:    # check if file is empty
                        columns = {
                            "Position": [filename[:4]],
                            "FOV": [filename[:10]],
                            "Channel": [filename[11:14]],
                            "id": [None],
                            "frame": [None],
                            "x [nm]" : [0],
                            "y [nm]": [0],
                            "sigma [nm]": [None],
                            "intensity [photon]": [0],
                            "uncertainty [nm]": [None]}
                        df_c = pd.DataFrame(columns)
                        dfs_compare.append(df_c)
                        count_compare.append(0)
                        intensity_compare.append(0)
                                                       
                    else:
                        df_compare.insert(0, 'Position', filename[:4])
                        df_compare.insert(1, 'FOV', filename[:10])
                        df_compare.insert(2, 'Channel', filename[11:14])
                        dfs_compare.append(df_compare)
                        count_compare.append(len(df_compare))
                        intensity_compare.append(df_compare["intensity [photon]"].mean())
                        #count_colocalised1.append("")
                               
            FOVnumber = (fovs.count('X0Y0')) 

            def filterbycoloc(ground, compare, ground_x_index, ground_y_index, compare_x_index, compare_y_index, threshold): #modified function - check indexing
                below_threshold = []
                above_threshold = []
                df_columns = ['Position', 'FOV', 'Channel','index', 'frame', 'x [nm]', 'y [nm]', 'sigma', 'Intensity', 'uncertainty']
                for i, coords_compare in enumerate(compare):
                    counter = 0
                    for j, coords_ground in enumerate(ground):

                        distance = np.sqrt((coords_ground[ground_x_index] - coords_compare[compare_x_index])**2 + (coords_ground[ground_y_index] - coords_compare[compare_y_index])**2)
                        if distance < threshold:
                            counter = counter + 1
                    if counter > 0:
                        below_threshold.append(coords_compare)  
                    else:
                        above_threshold.append(coords_compare)

                below_df = pd.DataFrame(below_threshold, columns = df_columns)
                below_df["colocalised"] = 1
                above_df = pd.DataFrame(above_threshold, columns = df_columns)
                above_df["colocalised"] = 0
 
                df_merged = pd.concat([below_df, above_df], ignore_index=False, sort=False)
                return df_merged

            alldata_colocs = []
            count_colocalised = []
            
            for x, (i, j) in enumerate(zip(dfs_ground, dfs_compare)):
                df_ground2 = dfs_ground[x]
                df_compare2 = dfs_compare[x]
                fovname = df_ground2["FOV"].iloc[0]
                g = df_ground2.to_numpy()
                c = df_compare2.to_numpy()
                coloc_compare = filterbycoloc(g, c, 5, 6, 5, 6, 100)
                coloc_ground = filterbycoloc(c, g, 5, 6, 5, 6, 100)
                coloc_merged = pd.concat([coloc_compare, coloc_ground], ignore_index=False, sort=False)
                alldata_colocs.append(coloc_merged)
                #coloc_merged.to_csv(path + fovname + "coloc.csv")

                ##Summary df too
                try:
                    if df_ground2["intensity [photon]"].empty == True:
                        count_colocalised.append(0)
                    else:
                        count_colocalised.append(len(coloc_compare[coloc_compare["colocalised"]== 1]))
                except EmptyDataError:
                    count_colocalised.append(0)
                except KeyError:
                    count_colocalised.append(0)
  
            sample_types = ['PD', 'TBS', 'CON', 'AD','Monomer', 'Filament']
            def sample_type(row):
                for s in sample_types:
                    if s in row['Case']:
                        return s

            all_data = pd.concat(alldata_colocs).drop(['frame', 'x [nm]', 'y [nm]', 'uncertainty', 'sigma'], axis = 1) 
            all_data = index1.merge(all_data)
            all_data['Sample_Type'] = all_data.apply(sample_type, axis=1)
            all_data  = all_data.sort_values(['FOV'])
            all_data = all_data.astype({'Case': str})
            all_data['Intensity_x40'] =  all_data['Intensity'].multiply(40)
            #all_data.to_csv(path + '/' + name + "_coloc_alldata.csv", index = False)
            all_data.to_csv(path + '/' + name + "_coloc_alldata_chance.csv", index = False)


            #Summarise all date into an averaged file
            summary_df = pd.DataFrame()
            summary_df["Ch1"] = count_ground
            summary_df["Ch2"] = count_compare
            summary_df["Colocalised"] = count_colocalised
            summary_df["Position"] = fovs
            summary_df["Ch1_Intensity"] = intensity_ground
            summary_df['Ch1_Intensity_Photons'] = summary_df['Ch1_Intensity'].multiply(40)
            summary_df["Ch2_Intensity"] = intensity_compare
            summary_df['Ch2_Intensity_Photons'] = summary_df['Ch2_Intensity'].multiply(40)
            summary_df["Percentage_Ch1"] = ((summary_df["Colocalised"] / summary_df["Ch1"] )*100)
            summary_df = summary_df.fillna(value = 0)
            summary_df = index1.merge(summary_df)
            summary_df = summary_df.sort_values(['Position'])

            mean_df = (index1).merge(summary_df.groupby('Position', as_index=False)[['Ch1','Ch2', 'Colocalised', 'Percentage_Ch1', 'Ch1_Intensity_Photons', 'Ch2_Intensity_Photons']].mean(), how = 'right')
            mean_df = mean_df.sort_values(['Position'])
            
            #mean_df.to_csv(path + '/' + name + "_coloc_meandata.csv", index = False)
            mean_df.to_csv(path + '/' + name + "_coloc_meandata_chance.csv", index = False)

#writer = pd.ExcelWriter(rootdir  + dname[0:6] + '_summaryTS_2col.xlsx')   
writer = pd.ExcelWriter(rootdir  + dname[0:6] + '_summaryTS_2col_chance.xlsx')
for subdir, dirnames, filenames in os.walk(rootdir):
    for dname in dirnames:
        if  dname.endswith(('Results_TS')):
            path2 = subdir + '/' + dname
            files = os.listdir(path2)
            for file in files:
                #if file.endswith('meandata.csv'):
                if file.endswith('meandata_chance.csv'):
                    resultsdf = pd.read_csv(path2 + '/' + file, index_col = None)
                    sheetname = file[7:20]
                    resultsdf.to_excel(writer, sheet_name = sheetname, index = False)  
writer.close()

summaryalldata_dflist = []
for subdir, dirnames, filenames in os.walk(rootdir):
    for dname in dirnames:
        if  dname.endswith(('Results_TS')):
            path3 = subdir + '/' + dname
            files = os.listdir(path3)
            for file in files:
                #if file.endswith('alldata.csv'):
                if file.endswith('alldata_chance.csv'):
                    sumall_datadf = pd.read_csv(path3 + '/' + file, index_col = None, dtype = 'str')
                    summaryalldata_dflist.append(sumall_datadf)
                
summaryall_data = pd.concat(summaryalldata_dflist)              
#summaryall_data.to_csv(rootdir  + '/' + dname[0:6] + '_all_data_2col.csv', index = False)
summaryall_data.to_csv(rootdir  + '/' + dname[0:6] + '_all_data_2col_chance.csv', index = False)
print('Done')   
