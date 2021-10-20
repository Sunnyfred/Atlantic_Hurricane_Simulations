import numpy as np
from netCDF4 import Dataset
import matplotlib.pyplot as plt
from plotly.graph_objs import Scattergeo, Layout
from plotly import offline
from cartopy import config
import matplotlib as matplot
from matplotlib.image import imread
import cartopy.crs as crs
import os
import shapely.geometry as sgeom
from cartopy.feature import NaturalEarthFeature
import csv
from wrf import (to_np, getvar, smooth2d, get_cartopy, cartopy_xlim,
                 cartopy_ylim, latlon_coords, interplevel, vinterp)
import json
from math import sin, cos, sqrt, atan2, radians
import pickle
import math






mainpath = '/project/momen/meng/COAWST/results/WRF_VS_WRFSWAN_2/'
Hurricaneall = ['Dorian','Maria','Irma','Katrina','Lorenzo']
# Hurricaneall = ['Katrina']
Real_Hurricane_Data = ['Dorian_Real_Track_Time_NOAA.csv',
                        'Maria_Real_Track_Time_NOAA.csv',
                        'Irma_Real_Track_Time_NOAA.csv',
                        'Katrina_Real_Track_Time_NOAA.csv',
                        'Lorenzo_Real_Track_Time_NOAA.csv']
days = [31, 22, 2, 28, 27]  # start day
hours = [-6, -6, -6, -6, -6] # start hour
output_interval=6
gridsize = ['8km']
swansize = [ 'swgr8p0']
prefix = 'WRFSWAN_NoTurb_swdt10_cpdt7200_'
Dirall = ['_swh8_swt14_Clz0p0001',
        '_swh8_swt14_Clz0p01',
        '_swh8_swt14_A1200B4p5C0P11',
        '_swh8_swt14_Clz100p00']
outputpath = '/project/momen/meng/COAWST/results/WRF_VS_WRFSWAN_2/postprocessing_WRFONLY/0_Paper_figures/section2_change_pars_for_strong_winds/source_code_outputs_change_Clz/'



# prefix for WRF files
wrf_pre='wrfout_d01_'
# years and months for Hurricanes (must be in the same order as in days and Hurricaneall)
years_month = ['2019-09-','2017-09-','2017-09-','2005-08-','2019-09-']
# days selected to evaluated the averged wind speed, may select some time in the middle
avg_day = ['01', '23', '03', '29', '28']
wrf_af = '_18:00:00'



# mainpath = 'C:/Users/limgr/Desktop/'
# Hurricaneall = ['Katrina']

# days = [28]  # start day
# hours = [-6] # start hour
# output_interval=6
# gridsize = ['16km']
# swansize = ['swgr16p0']
# prefix = 'WRFSWAN_NoTurb_swdt10_cpdt7200_'
# Dirall = ['_swh8_swt14_Clz0p0001']
# outputpath = 'C:/Users/limgr/Desktop/'



# prefix for WRF files
wrf_pre='wrfout_d01_'
# years and months for Hurricanes (must be in the same order as in days and Hurricaneall)
years_month = ['2019-08-','2017-09-','2017-09-','2005-08-','2019-09-']
#years_month = ['2005-08-']
# days selected to evaluated the averged wind speed, may select some time in the middle
avg_day = ['31', '22', '02', '28', '27']
#avg_day = ['29']
wrf_af = '_18:00:00'

R = 6373.0 # approxiamte radius of earth in km
max_radius = 200 # max_radius in km 
dr_step = 8 # dr_step in km
interpolat_height = 1000 # interpolat_height in m

# # This function returns a list of all wrf files in the directory.
# def list_files(Dir, ncfiles, i):
#  	for f in os.listdir(Dir):
#          if f.startswith(wrf_pre+years_month[i]+avg_day[i]+wrf_af):
#              ncfiles.append(f)
#  	print(ncfiles)
#  	return (ncfiles)




for gk in range(len(gridsize)):
    count1=0

    for Hurricane in Hurricaneall:


        results=[]  
        for Dir in Dirall:
        
            
        
        
            avg_speed = []
            radi = []
            # speed_vs_r = {}
            # for i in range(len(range(0, max_radius+1, dr_step))):
            #     speed_vs_r[i]=[]
            speed_vs_r = {i:[] for i in range (0, max_radius+1, dr_step)}
        

            print('Current folder is: ')
            Dir_local = mainpath+Hurricane+ '/' +gridsize[gk]+ '/' +prefix+swansize[gk]+Dir
            print(Dir_local)
            #row.append(Hurricane+Dir)
             
            
            day=days[count1]
            hour=hours[count1]
            day_count=0
            # Set the working space>
            os.chdir(Dir_local)
            # # initiate the list that will contain all wrf files in Dir directory.
            ncfiles = []
            # # Use the list_files function to list all the wrf files in the directory.
            # ncfiles = list_files(Dir_local, ncfiles, count1)
            # Sort the ncfiles 
            ncfiles = [wrf_pre+years_month[count1]+avg_day[count1]+wrf_af]
            # ncfiles = ['wrfout_d01_2005-08-29_00%3A00%3A00']
            print (ncfiles)
            # initiate the list that will contain the hurricane-track data
            eye_slp = []
            eye_lat = []
            eye_long = []
            print(ncfiles)

            for ncfile in ncfiles:  
                
    
     	        #print (ncfile)
     	        ncfile = Dataset(ncfile)
     	        # Get the latitude and longitude data.
     	        LAT   = np.array(getvar(ncfile, "XLAT"))
     	        latitudes = (LAT[:,0])
     	        LONG  = np.array(getvar(ncfile, "XLONG")) 
     	        longitudes = (LONG[0,:])
     	        Z_3D = np.array(getvar (ncfile, 'z'))
     	        U10_2D = np.array(getvar (ncfile, 'U10'))                
     	        V10_2D = np.array(getvar (ncfile, 'V10'))                  
     	        WSPD_2D = np.sqrt(np.square(V10_2D)+np.square(U10_2D))                

     	        #interp_levels = [interpolat_height]
     	        #WSPD_3D = np.array(getvar (ncfile, 'wspd'))
     	        #WSPD_2D = interplevel(WSPD_3D, Z_3D, interpolat_height)
     	        # WSPD_2D = vinterp(ncfile, \
              #             field=WSPD_3D,\
              #             vert_coord="ght",\
              #             interp_levels=interp_levels,\
              #             extrapolate=True,\
              #             field_type="z",\
              #             log_p=True) 
                 
                 
                 
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
     	        print(eye_lat)

                 
     	        for lat_i in latitudes:
                    for lon_i in longitudes:
                        	tmp = sin((radians(eye_lat[0]) - radians(lat_i)) / 2)**2 + \
                                cos(radians(lat_i)) * cos(radians(eye_lat[0])) *\
                                    sin( (radians(eye_long[0]) - radians(lon_i)) / 2)**2
                        	distance = 2 * R * np.arcsin(sqrt(tmp))
                        	Lat_idx = np.where(lat_i == latitudes)
                        	Lon_idx = np.where(lon_i == longitudes)

                        	for rr in range(0, max_radius+1, dr_step):    
                                	# print(rr)
                                	if ((rr-(dr_step/2))<distance) and (distance<(rr+(dr_step/2))) and (math.isnan(WSPD_2D[Lat_idx[0], Lon_idx[0]]) == False):
                                        	speed_vs_r[rr].append(float(WSPD_2D[Lat_idx[0], Lon_idx[0]]))

                                            
                                            
     	        for i in range (0, max_radius+1, dr_step):
                    avg = 0
                    print(sum(speed_vs_r[i]),len(speed_vs_r[i]) )
                    if (len(speed_vs_r[i])!=0) and (math.isnan(sum(speed_vs_r[i]) ) == False):
                        avg = sum(speed_vs_r[i]) / len(speed_vs_r[i])
                        print(sum(speed_vs_r[i]),len(speed_vs_r[i]) )
                        avg_speed.append(avg)
                        radi.append(i)
                    else:
                        continue
                    
                                                           
         
            results.append(radi)   
            results.append(avg_speed) 
            #print(results) 


                                

        # fields = [rr for rr in range(0, max_radius+1, dr_step)]
        # print (fields)
        with open(outputpath+Hurricane+'_avg_speed_'+gridsize[gk]+'.csv', 'w') as csvfile:
                csvwriter = csv.writer(csvfile)
                # csvwriter.writerow(fields) 
                for i in range(len(results)):
                    csvwriter.writerow(results[i]) 


        
        
        count1=count1+1   