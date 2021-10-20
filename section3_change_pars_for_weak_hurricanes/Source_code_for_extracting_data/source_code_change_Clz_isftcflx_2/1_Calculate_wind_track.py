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
                 cartopy_ylim, latlon_coords)
import json
from math import sin, cos, sqrt, atan2, radians
import pickle







mainpath = '/project/momen/meng/COAWST/results/WRF_VS_WRFSWAN_2/'
Hurricaneall = ['Gert','Nicole','Joaquin','Cristobal','Ike']
Real_Hurricane_Data = ['Gert_Real_Track_Time_NOAA.csv',
                        'Nicole_Real_Track_Time_NOAA.csv',
                        'Joaquin_Real_Track_Time_NOAA.csv',
                        'Cristobal_Real_Track_Time_NOAA.csv',
                        'Ike_Real_Track_Time_NOAA.csv']
days = [15, 14, 4, 26, 10]  # start day
hours = [-6, -6, -6, -6, -6] # start hour
output_interval=6
# Hurricaneall = ['Dorian']
# Real_Hurricane_Data = ['Dorian_Real_Track_Time_NOAA.csv']
# days = [29]  # start day
# hours = [-6] # start hour
gridsize = ['8km','16km']
Dirall = ['_isftcflx_2_changeClz_0p0001',
       '_isftcflx_2_changeClz_0p0100',
       '_isftcflx_2_changeClz_1p0000',
       '_isftcflx_2_changeClz_100p0000']
outputpath = '/project/momen/meng/COAWST/results/WRF_VS_WRFSWAN_2/postprocessing_WRFONLY/0_Paper_figures/section3_change_pars_for_weak_winds/source_code_outputs_change_Clz_isftcflx_2/'


# This function returns a list of all wrf files in the directory.
def list_files(Dir, ncfiles):
 	for f in os.listdir(Dir):
 	 	if f.startswith('wrfout'):
 	 	 	ncfiles.append(f)
 	return (ncfiles)




for grids in gridsize:
    count1=0
    

    for Hurricane in Hurricaneall:
    
    

    
        # Initiate the lists that will contain all the necessary data to plot the hurricane's truck.
        Real_Times = []
        Real_Lat = []
        Real_Long =[]
        Real_hour=[]
        Real_day=[]
        real_dic={}
        with open(outputpath+Real_Hurricane_Data[count1]) as f:
     	    reader = csv.reader(f)
     	    # Move to the row containing the row headers. 
     	    next (reader)
     	    row_header = next(reader)
     	    # Extract the data necessary to plot the real truck.
     	    for row in reader:
     	 	    Real_Lat.append(float(row[row_header.index('Lat')]))
     	 	    Real_Long.append(float(row[row_header.index('Lon')]))
     	 	    Real_hour.append(int(row[row_header.index('Time - hour')]))	
     	 	    Real_day.append(int(row[row_header.index('Time - day')]))		

        for i in range(len(Real_day)):
            real_dic[Real_day[i]]=[]
    
        for i in range(len(Real_day)):
            real_dic[Real_day[i]].append([Real_hour[i],Real_Lat[i],Real_Long[i]])
        print(real_dic)
        with open(outputpath+Hurricane+'_track_'+grids+'.txt', 'w') as outfile:
            json.dump(real_dic, outfile)
     
    
    
    


 

        results=[]  
        for Dir in Dirall:
        
        
        

            print('Current folder is: ')
            Dir_local = mainpath+Hurricane+ '/' +grids+ '/' +'WRFONLY_NoTurb_'+grids+Dir
            print(Dir_local)
            #row.append(Hurricane+Dir)
        
        
            simu_dic = {}
            for i in range(len(Real_day)):
                simu_dic[Real_day[i]]=[]
        
        
            day=days[count1]
            hour=hours[count1]
            day_count=0
            # Set the working space>
            os.chdir(Dir_local)
            # initiate the list that will contain all wrf files in Dir directory.
            ncfiles = []
            # Use the list_files function to list all the wrf files in the directory.
            ncfiles = list_files(Dir_local, ncfiles)
            # Sort the ncfiles 
            ncfiles = sorted(ncfiles)
            #print (ncfiles)
            # initiate the list that will contain the hurricane-track data
            min_slp = []
            min_lat = []
            min_long = []

            for ncfile in ncfiles:  
    
     	        #print (ncfile)
     	        ncfile = Dataset(ncfile)
     	        # Get the latitude and longitude data.
     	        LAT   = np.array(getvar(ncfile, "XLAT"))
     	        latitudes = (LAT[:,0])
     	        LONG  = np.array(getvar(ncfile, "XLONG")) 
     	        longitudes = (LONG[0,:])
     	        # Get the sea level pressure for each wrf output file.
     	        slp2D = getvar(ncfile, "slp")
     	        slp = np.array(slp2D)
     	        # Get theindex of the minimum value of pressure.
     	        idx = np.where(slp == np.amin(slp))
     	        #print (idx)
     	        # List the data of the minimum SLP
     	        min_slp.append(np.amin(slp)) 
     	        min_lat.append(latitudes[idx[0]])
     	        min_long.append(longitudes[idx[1]])
     	        if day_count > 3:
     	 	        if day==31:
     	 	 	        day=1
     	 	        else:
     	 	 	        day+=1
     	 	        day_count=0
     	        day_count += 1 
    
     	        hour += output_interval
     	        if hour == 24:
     	 	        hour=0    
     	        print(day, hour)
     	        simu_dic[day].append([hour,latitudes[idx[0]].tolist()[0],longitudes[idx[1]].tolist()[0]])
            results.append(simu_dic)
            print(results)


        with open(outputpath+Hurricane+'_track_'+grids+'.txt', 'w') as outfile:  
            json.dump(real_dic, outfile) 
            for i in range(len(results)):    
                json.dump(results[i], outfile)     
            
        pickle.dump( slp2D, open( outputpath+Hurricane+'_'+grids+'.p', "wb" ) )
        
        
        count1=count1+1   