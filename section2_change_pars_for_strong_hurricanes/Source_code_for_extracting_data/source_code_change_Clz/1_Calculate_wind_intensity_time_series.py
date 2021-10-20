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
Real_Hurricane_Data = ['Dorian_Real_Track_Time_NOAA.csv',
                        'Maria_Real_Track_Time_NOAA.csv',
                        'Irma_Real_Track_Time_NOAA.csv',
                        'Katrina_Real_Track_Time_NOAA.csv',
                        'Lorenzo_Real_Track_Time_NOAA.csv']
# Hurricaneall = ['Dorian']
# Real_Hurricane_Data = ['Dorian_Real_Track_Time_NOAA.csv']
gridsize = ['8km','16km']
swansize = ['swgr8p0', 'swgr16p0']
prefix = 'WRFSWAN_NoTurb_swdt10_cpdt7200_'
Dirall = ['_swh8_swt14_Clz0p0001',
       '_swh8_swt14_Clz0p01',
       '_swh8_swt14_A1200B4p5C0P11',
       '_swh8_swt14_Clz100p00']
outputpath = '/project/momen/meng/COAWST/results/WRF_VS_WRFSWAN_2/postprocessing_WRFONLY/0_Paper_figures/section2_change_pars_for_strong_winds/source_code_outputs_change_Clz/'


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

        #Initiate the lists that will contain the real data variables
        Real_Times = []
        Real_Wnd_Ints = []
        Real_Long =[]
        #Open the file that contains the real data and extract the necessary variables
        print('Real track: '+outputpath+Real_Hurricane_Data[count1])
        with open(outputpath+Real_Hurricane_Data[count1]) as f:
    	    reader = csv.reader(f)
    	    next (reader)
    	    row_header = next(reader)
    	    #print (row_header)
    	    for row in reader:
    		    YYYY = (row[row_header.index('Time - year')])
    		    MM =  (row[row_header.index('Time - month')])
    		    if (len(MM) == 1):
    			    MM = '0' + MM
    		    DD =  (row[row_header.index('Time - day')])
    		    if (len(DD) == 1):
    			    DD = '0' + DD
    		    HR =  (row[row_header.index('Time - hour')])
    		    if (len(HR) == 1):
    			    HR = '0' + HR
    		    MN =  (row[row_header.index('Time - min')])
    		    if (len(MN) == 1):
    			    MN = '0' + MN
    		    Time = YYYY + '-' + MM + '-' + DD + '_' + HR + '_' + MN
    		    Real_Wnd_Ints.append(float(row[row_header.index('Wind Speed(kt)')]))
    		    Real_Times.append(Time)
		
        print (Real_Wnd_Ints) 
        print (Real_Times)     
        rows.append(Real_Wnd_Ints)
        count1=count1+1    
    
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
                    # Get U and V components of wind intensity at 10m of altitude.
                    U10_2D = np.array(getvar(ncfile, "U10", tt))
                    #print (U10_2D.shape)
                    V10_2D = np.array(getvar(ncfile, "V10", tt))
                    #print (V10_2D.shape)
                    slp_2D = np.array(getvar(ncfile, "slp", tt))
                    slp_2D = slp_2D.flatten()
                    # Reshape the U and V into a 1D array.
                    U10_1D = U10_2D.flatten()
                    #print (U10_1D.shape)
                    V10_1D = V10_2D.flatten()
                    #print (V10_1D.shape)
                    WND_SPD_10 = U10_1D
                    # Calculate the wind intensity at each point of the map.
                    for i in range (WND_SPD_10.size - 1):
                                    WND_SPD_10[i] = math.sqrt((U10_1D[i]**2)+(V10_1D[i]**2))
                    # Search for the maximum wind intensity at aspecific time step.	
                    WND_SPD_10_max = np.amax(WND_SPD_10)
                    slp_min = np.amin(slp_2D)	
                    # List the maximum wind intensity for all time steps.	
                    row.append(WND_SPD_10_max)
                    # list all the time steps
                    Times.append(Time_Step*k)
                    k = k+1 
                
                


            print (row)
            print (Times)
            rows.append(row)
        fields = [time for time in Times]
        print (fields)
        print (rows)
        with open(outputpath+Hurricane+'_wind_intensity_'+gridsize[gk]+'.csv', 'w') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(fields) 
            csvwriter.writerows(rows)
    

            








    
