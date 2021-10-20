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
Hurricaneall = ['Dorian','Maria','Irma','Katrina','Lorenzo']
# Hurricaneall = ['Dorian']
gridsize = '/16km/'
gridsize2 = '16km'
Dirall = ['WRFONLY_NoTurb_16km_isftcflx_1_changeClz_1p0000_MYJ',
       'WRFONLY_NoTurb_16km_isftcflx_0_changeClz_1p0000',
       'WRFSWAN_NoTurb_swdt10_cpdt7200_swgr16p0_swh8_swt14_A1200B4p5C0P11',
       'WRFONLY_NoTurb_16km_isftcflx_1_changeClz_1p0000',
       'WRFONLY_NoTurb_16km_isftcflx_2_changeClz_1p0000']
outputpath = '/project/momen/meng/COAWST/results/WRF_VS_WRFSWAN_2/postprocessing_WRFONLY/0_Paper_figures/section1_default_comparison_for_strong_winds/source_codes_outputs/16km/'


# This function returns a list of all wrf files in the directory.
def list_files(Dir, ncfiles):
 	for f in os.listdir(Dir):
 	 	if f.startswith('wrfout'):
 	 	 	ncfiles.append(f)
 	return (ncfiles)



for Hurricane in Hurricaneall:
    rows=[]
    for Dir in Dirall:

        print('Current folder is: ')
        Dir_local = mainpath+Hurricane+gridsize+Dir
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
    with open(outputpath+Hurricane+'_ZNT_eye_'+gridsize2+'.csv', 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(fields) 
        csvwriter.writerows(rows)
    

            
        

    