import os
import math
import numpy as np
import matplotlib as matplot
import matplotlib.pyplot as plt
from netCDF4 import Dataset
import csv
from wrf import (to_np, getvar, smooth2d, get_cartopy, cartopy_xlim,
                 cartopy_ylim, latlon_coords)
from math import sin, cos, sqrt, atan2, radians

dr_step=8 # this is the eywall band in km
R = 6373.0 # approxiamte radius of earth in km


# List the colors that will be used for tracing the track.
colors = ['blue', 'orange', 'red', 'purple', 'brown', 'pink', 'gray', 'olive', 'cyan', 'black', 'green', 'gold', 'lightcoral', 'turquoise']
c =0


mainpath = '/project/momen/meng/COAWST/results/WRF_VS_WRFSWAN_2/'
Hurricaneall = ['Dorian','Maria','Irma','Katrina','Lorenzo']
# Hurricaneall = ['Dorian']
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
            eye_slp = []
            eye_lat = []
            eye_long = []
            max_lat = []
            max_long = []
            for tt in range(1):
                for ncfile in ncfiles:
                    ncfile = Dataset(ncfile)
                    ttt = np.array(getvar(ncfile, "times", tt))
                    print('!!!!!!',ttt)
                    WSPD_2D = np.array(getvar (ncfile, 'ZNT'))  
                 
                    ZNT_2D = np.array(getvar(ncfile, "ZNT", tt))
                    U10_2D = np.array(getvar(ncfile, "U10", tt))
                    V10_2D = np.array(getvar(ncfile, "V10", tt))
                    UV10_2D = np.square(U10_2D)+np.square(V10_2D)
                    max_idx = np.where(UV10_2D == np.amax(UV10_2D))
                
                
                    LAT   = np.array(getvar(ncfile, "XLAT"))
                    latitudes = (LAT[:,0])
                    LONG  = np.array(getvar(ncfile, "XLONG")) 
                    longitudes = (LONG[0,:])                  
     	            # Get the sea level pressure for each wrf output file.
                    slp2D = getvar(ncfile, "slp")
                    slp = np.array(slp2D)
     	            # Get theindex of the minimum value of pressure.
                    eye_idx = np.where(slp == np.amin(slp))
     	            #print (idx)
     	            # List the data of the minimum SLP
                    eye_slp.append(np.amin(slp)) 
                    eye_lat.append(latitudes[eye_idx[0]])
                    eye_long.append(longitudes[eye_idx[1]])
                    max_lat.append(latitudes[max_idx[0]])
                    max_long.append(longitudes[max_idx[1]])
                    print(eye_lat)  
                
                    tmp = sin((radians(eye_lat[0]) - radians(max_lat[0])) / 2)**2 + \
                            cos(radians(max_lat[0])) * cos(radians(eye_lat[0])) *\
                                sin( (radians(eye_long[0]) - radians(max_long[0])) / 2)**2
                    eye_wall_distance = 2 * R * np.arcsin(sqrt(tmp))

                    speed_vs_r = []
                
                    for lat_i in latitudes:
                        for lon_i in longitudes:
                            tmp = sin((radians(eye_lat[0]) - radians(lat_i)) / 2)**2 + \
                            cos(radians(lat_i)) * cos(radians(eye_lat[0])) *\
                                sin( (radians(eye_long[0]) - radians(lon_i)) / 2)**2
                            distance = 2 * R * np.arcsin(sqrt(tmp))
                            Lat_idx = np.where(lat_i == latitudes)
                            Lon_idx = np.where(lon_i == longitudes)
                            if ((distance-(dr_step/2))<eye_wall_distance) and \
                            (eye_wall_distance<(distance+(dr_step/2))) and \
                            (math.isnan(WSPD_2D[Lat_idx[0], Lon_idx[0]]) == False):
                                    speed_vs_r.append(float(WSPD_2D[Lat_idx[0], Lon_idx[0]]))
                                
                                
                    avg = 0
                    print(sum(speed_vs_r),len(speed_vs_r) )
                    if (len(speed_vs_r)!=0) and (math.isnan(sum(speed_vs_r) ) == False):
                        avg = sum(speed_vs_r) / len(speed_vs_r)
                        print(sum(speed_vs_r),len(speed_vs_r) )
                        row.append(avg)

                    else:
                        continue                


                                  
                    # list all the time steps
                    Times.append(Time_Step*k)
                    k = k+1 

            print (row)
            print (Times)
            rows.append(row)
        fields = [time for time in Times]
        print (fields)
        print (rows)
        with open(outputpath+Hurricane+'_ZNT_eyewallbandavg_'+gridsize[gk]+'.csv', 'w') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(fields) 
            csvwriter.writerows(rows)


    

            
        

    