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
#Hurricaneall = ['Dorian']
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
prefix = 'WRFONLY_NoTurb_'
Dirall = ['_isftcflx_2_changeClz_0p0001',
       '_isftcflx_2_changeClz_0p0100',
       '_isftcflx_2_changeClz_1p0000',
       '_isftcflx_2_changeClz_100p0000']
outputpath = '/project/momen/meng/COAWST/results/WRF_VS_WRFSWAN_2/postprocessing_WRFONLY/0_Paper_figures/section2_change_pars_for_strong_winds/source_code_outputs_change_Clz_isftcflx_2/'




# prefix for WRF files
wrf_pre='wrfout_d01_'
# years and months for Hurricanes (must be in the same order as in days and Hurricaneall)
years_month_day = [['2019-08-31','2019-08-31','2019-08-31','2019-08-31',\
                    '2019-09-01','2019-09-01','2019-09-01','2019-09-01','2019-09-02'],\
               ['2017-09-22','2017-09-22','2017-09-22','2017-09-22',\
                '2017-09-23','2017-09-23','2017-09-23','2017-09-23','2017-09-24'],\
               ['2017-09-02','2017-09-02','2017-09-02','2017-09-02',\
                '2017-09-03','2017-09-03','2017-09-03','2017-09-03','2017-09-04'],\
               ['2005-08-28','2005-08-28','2005-08-28','2005-08-28',\
                '2005-08-28','2005-08-28','2005-08-28','2005-08-28','2005-08-28'],\
               ['2019-09-27','2019-09-27','2019-09-27','2019-09-27',\
                '2019-09-28','2019-09-28','2019-09-28','2019-09-28','2019-09-29']]
#years_month = ['2005-08-']


#avg_day = ['29']
wrf_af = [['_00:00:00','_06:00:00','_12:00:00','_18:00:00',\
          '_00:00:00','_06:00:00','_12:00:00','_18:00:00', '_00:00:00'],\
          ['_00:00:00','_06:00:00','_12:00:00','_18:00:00',\
          '_00:00:00','_06:00:00','_12:00:00','_18:00:00', '_00:00:00'],\
          ['_00:00:00','_06:00:00','_12:00:00','_18:00:00',\
          '_00:00:00','_06:00:00','_12:00:00','_18:00:00', '_00:00:00'],\
          ['_00:00:00','_06:00:00','_12:00:00','_18:00:00',\
          '_00:00:00','_06:00:00','_12:00:00','_18:00:00', '_00:00:00'],\
          ['_00:00:00','_06:00:00','_12:00:00','_18:00:00',\
          '_00:00:00','_06:00:00','_12:00:00','_18:00:00', '_00:00:00']]

R = 6373.0 # approxiamte radius of earth in km
max_press = 1010 # max_radius in hPa 
min_press = 900 # max_radius in hPa 
dr_step = 4 # dr_step in km
interpolat_height = [10] # interpolat_height in m



min_press_factor=1.000
max_press_factor=1.005
min_press_factor=0.99
max_press_factor=1.01


my_cols = len(Hurricaneall)
ncfiles=[]
for k in range(len(Hurricaneall)):
    tmp=[]
    for i in range(len(years_month_day[0])):
        tmp.append(wrf_pre+years_month_day[k][i]+wrf_af[k][i])
    ncfiles.append(tmp)
print(ncfiles)

count_file = 0
for ida in range(len(years_month_day[0])): 
    


    for gk in range(len(gridsize)):
        count1=0

        for Hurricane in Hurricaneall:
      
 


            count2=0
            
            results1=[]  
            results2=[]  
            for Dir in Dirall:
        
            
        
        
                avg_speed = []
                radi = []
                # speed_vs_r = {}
                # for i in range(len(range(0, max_radius+1, dr_step))):
                #     speed_vs_r[i]=[]
                speed_vs_slp = {i:[] for i in range (min_press, max_press+1, dr_step)}
        

                print('Current folder is: ')
                Dir_local = mainpath+Hurricane+ '/' +gridsize[gk]+ '/' +prefix+gridsize[gk]+Dir
                print(Dir_local)
                #row.append(Hurricane+Dir)
             
             
            
                day=days[count1]
                hour=hours[count1]
                day_count=0
                # Set the working space>
                os.chdir(Dir_local)
                ncfile = ncfiles[count1][ida]
                print(ncfile)
                # initiate the list that will contain the hurricane-track data
                eye_slp = []
                eye_lat = []
                eye_long = []
                max_wind_pres = []
                max_wind_lat = []
                max_wind_long = []


                
                
                for height in interpolat_height:   
                
    
         	        #print (ncfile)
         	        ncfile = Dataset(ncfile)
     	            # Get the latitude and longitude data.
         	        Z_3D   = np.array(getvar(ncfile, "z"))
         	        LAT   = np.array(getvar(ncfile, "XLAT"))
         	        latitudes = (LAT[:,0])
         	        LONG  = np.array(getvar(ncfile, "XLONG")) 
         	        longitudes = (LONG[0,:])
         	        U_3D = np.array(getvar (ncfile, 'U'))                     
         	        V_3D = np.array(getvar (ncfile, 'V'))                    
         	        levels = (Z_3D[:,0,0])
         	        # print(levels,len(levels))
         	        UR = U_3D
         	        UTH = V_3D
               
                 
                 
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
         	        # print(eye_lat)
                     
                     
                        # SLP_MX is determined by surface wind speed
         	        U10 = np.array(getvar (ncfile, 'U10'))                     
         	        V10 = np.array(getvar (ncfile, 'V10'))   
         	        wspd_2D = np.sqrt(np.square(U10)+np.square(V10))
         	        max_wind_idx = np.where(wspd_2D == np.amax(wspd_2D))
         	        # # print(max_wind_idx,max_wind_idx[0],max_wind_idx[1])
         	        # max_wind_pres.append(slp[max_wind_idx[0],max_wind_idx[1]]) 
         	        # print('max wind pressure is: '+ str(max_wind_pres[0]))
                     

         	        WSPD = np.array(getvar (ncfile, 'wspd'))  
                        # SLP_MX is determined by wind speed at 500m
         	        #wspd_2D = interplevel(WSPD, Z_3D, 500)
                        # SLP_MX is determined by wind speed at first level
         	        #wspd_2D = WSPD[0,:,:]  
         	        #max_wind_idx = np.where(wspd_2D == np.amax(wspd_2D))
         	        # print(max_wind_idx,max_wind_idx[0],max_wind_idx[1])
         	        max_wind_pres.append(slp[max_wind_idx[0],max_wind_idx[1]]) 
         	        print('max wind pressure is: '+ str(max_wind_pres[0]))
         	        print('max wind pressure is: '+ str(min_press_factor * max_wind_pres[0]))
         	        print('max wind pressure is: '+ str(max_press_factor * max_wind_pres[0]))                     
                    
                    
         	        counter = 0.0
         	        UR_avg = [i*0 for i in range(len(levels))]
         	        UTH_avg = [i*0 for i in range(len(levels))]
         	        zz = [i*0 for i in range(len(levels))]
         	        print('inital UR_avg: ', UR_avg)   
         	        print('inital UTH_avg: ', UTH_avg) 
         	        print('inital zz: ', zz) 
                     
         	        for lat_i in latitudes:

                         for lon_i in longitudes:
                             
                             Lat_idx = np.where(lat_i == latitudes)
                             Lon_idx = np.where(lon_i == longitudes)
                             
                             if (float(slp[Lat_idx[0], Lon_idx[0]]) >= min_press_factor * float(max_wind_pres[0])) \
                                 and (float(slp[Lat_idx[0], Lon_idx[0]]) <= max_press_factor * float(max_wind_pres[0])):
                                     
                                     counter = counter + 1.0
                             
                                     tmp = sin((radians(eye_lat[0]) - radians(lat_i)) / 2)**2 + \
                                         cos(radians(lat_i)) * cos(radians(eye_lat[0])) *\
                                         sin( (radians(eye_long[0]) - radians(lon_i)) / 2)**2
                                     radius = 2 * R * np.arcsin(sqrt(tmp))
                                
                                     tmp_x = sin((radians(eye_lat[0]) - radians(lat_i)) / 2)**2 + \
                                         cos(radians(lat_i)) * cos(radians(eye_lat[0])) *\
                                         sin( (radians(eye_long[0]) - radians(eye_long[0])) / 2)**2
                                     tmp_y = sin((radians(eye_lat[0]) - radians(eye_lat[0])) / 2)**2 + \
                                         cos(radians(eye_lat[0])) * cos(radians(eye_lat[0])) *\
                                         sin( (radians(eye_long[0]) - radians(lon_i)) / 2)**2                                    
                                     y_lat = 2 * R * np.arcsin(sqrt(tmp_x))
                                     x_lon = 2 * R * np.arcsin(sqrt(tmp_y))  
                                     theta = 0.0
                                
                                
                                     if x_lon==0:  
                                         if lat_i >= eye_lat[0]:
                                             theta = np.pi / 2.0
                                         else:
                                             theta = -np.pi / 2.0
                                        
                                     else:
                                         theta = np.arctan(y_lat/x_lon)
                                         if (lon_i <= eye_long[0]) and (lat_i >= eye_lat[0]):
                                             theta = np.pi - theta
                                         elif (lon_i <= eye_long[0]) and (lat_i < eye_lat[0]):
                                             theta = np.pi + theta                                        
                                         elif (lon_i > eye_long[0]) and (lat_i < eye_lat[0]):
                                             theta = - theta
                                    
              
                                     ccc = 0
                                     tmp1 = 0
                                     tmp2 = 0                                     
                                     for level_i in levels:  

                                         #Level_idx = np.where(level_i == levels)
                                         tmp1 = \
                                             float(U_3D[ccc, Lat_idx[0], Lon_idx[0]])*np.cos(theta) \
                                                 + float(V_3D[ccc, Lat_idx[0], Lon_idx[0]])*np.sin(theta)   
                                         tmp2 = \
                                             float(-U_3D[ccc, Lat_idx[0], Lon_idx[0]])*np.sin(theta) \
                                                 + float(V_3D[ccc, Lat_idx[0], Lon_idx[0]])*np.cos(theta)  
                                                 
                                         UR_avg[ccc] +=  float(tmp1)                                               
                                         UTH_avg[ccc] +=  float(tmp2) 

                                         ccc +=1                                         
                                
         	        ccc = 0         
         	        for level_i in levels: 
                         
                          #Level_idx = np.where(level_i == levels)
                          #print('level is '+str(Level_idx[0])+'at level '+str(level_i))
                         
                         UR_avg[ccc] = UR_avg[ccc]/counter                                                
                         UTH_avg[ccc] = UTH_avg[ccc]/counter                            
                         zz[ccc] = Z_3D[ccc, 0, 0]
                         ccc +=1
                                                         
         
                print('counter = '+str(counter))
                results1.append(UR_avg) 
                results2.append(UTH_avg) 
                #print(results) 
                print(zz)
                print(UR_avg)
                print(UTH_avg)
                print(results1)                                
                print(results2)

            with open(outputpath+Hurricane+'_wind_profiles_'+gridsize[gk]+'_'+str(count_file)+'.csv', 'w') as csvfile:
                    csvwriter = csv.writer(csvfile)
                    csvwriter.writerow(zz)
                    for i in range(len(results1)):
                        csvwriter.writerow(results1[i]) 
                    for i in range(len(results2)):
                        csvwriter.writerow(results2[i]) 



        
        
            count1=count1+1   
            
    count_file += 1