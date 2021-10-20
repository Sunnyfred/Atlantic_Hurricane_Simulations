import os
import math
import numpy as np
import matplotlib as matplot
import matplotlib.pyplot as plt
from netCDF4 import Dataset
import csv
from wrf import (to_np, getvar, smooth2d, get_cartopy, cartopy_xlim,
                 cartopy_ylim, latlon_coords)



# List the colors that will be used for tracing the track.
colors = ['blue', 'orange', 'red', 'purple', 'brown', 'pink', 'gray', 'olive', 'cyan', 'black', 'green', 'gold', 'lightcoral', 'turquoise']
c =0


mainpath = '/project/momen/meng/COAWST/results/WRF_VS_WRFSWAN_2/'
Hurricaneall = ['Gert','Nicole','Joaquin','Cristobal','Ike']
Real_Hurricane_Data = ['Gert_Real_Track_Time_NOAA.csv',
                        'Nicole_Real_Track_Time_NOAA.csv',
                        'Joaquin_Real_Track_Time_NOAA.csv',
                        'Cristobal_Real_Track_Time_NOAA.csv',
                        'Ike_Real_Track_Time_NOAA.csv']
# Hurricaneall = ['Dorian']
# Real_Hurricane_Data = ['Dorian_Real_Track_Time_NOAA.csv']
gridsize = ['8km','16km']
swansize = ['swgr8p0', 'swgr16p0']
prefix = 'WRFSWAN_NoTurb_swdt10_cpdt7200_'
Dirall = ['_swh8_swt14_Clz0p0001',
       '_swh8_swt14_Clz0p01',
       '_swh8_swt14_A1200B4p5C0P11',
       '_swh8_swt14_Clz100p00']
outputpath = '/project/momen/meng/COAWST/results/WRF_VS_WRFSWAN_2/postprocessing_WRFONLY/0_Paper_figures/section3_change_pars_for_weak_winds/source_code_outputs_change_Clz/'


# This function returns a list of all wrf files in the directory.
def list_files(Dir, ncfiles):
 	for f in os.listdir(Dir):
 	 	if f.startswith('wrfout'):
 	 	 	ncfiles.append(f)
 	return (ncfiles)



for gk in range(len(gridsize)):
    count1=0

    for Hurricane in Hurricaneall:
        rows=[]
        for Dir in Dirall:
    
            print('Current folder is: ')
            Dir_local = mainpath+Hurricane+ '/' +gridsize[gk]+ '/' +prefix+swansize[gk]+Dir
            print(Dir_local)
            #row.append(Hurricane+Dir)
            
            # Set the working space>
            os.chdir(Dir_local)
            # initiate the list that will contain all wrf files in Dir directory.
            ncfiles = []
            # Use the list_files function to list all the wrf files in the directory.
            ncfiles = list_files(Dir_local, ncfiles)
            ncfiles = sorted(ncfiles)
            print (ncfiles)
            # initiate the list that will contain the hurricane-track data.
            row = []
            # Identify the time step
            Time_Step = 6
            k = 0
            # initiate the list that will contain the times.
            Times = []
            for tt in range(1):
                for ncfile in ncfiles:
                    ncfile = Dataset(ncfile)
                    ttt = np.array(getvar(ncfile, "times", tt))
                    print('!!!!!!',ttt)
                    slp_2D = np.array(getvar(ncfile, "slp", tt))
                    # slp_2D = slp_2D.flatten()
                    ZNT_2D = np.array(getvar(ncfile, "ZNT", tt))
                    # ZNT_2D = ZNT_2D.flatten()
                    # Get theindex of the minimum value of pressure.
                    idx = np.where(slp_2D == np.amin(slp_2D))
                    # List the maximum wind intensity for all time steps.	
                    row.append(float(ZNT_2D[(np.amin(idx[0]),np.amin(idx[1]))]))
                    # list all the time steps
                    Times.append(Time_Step*k)
                    k = k+1 

            print (row)
            print (Times)
            rows.append(row)
        fields = [time for time in Times]
        print (fields)
        print (rows)
        with open(outputpath+Hurricane+'_ZNT_eye_'+gridsize[gk]+'.csv', 'w') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(fields) 
            csvwriter.writerows(rows)
    
        count1=count1+1
            
        

    