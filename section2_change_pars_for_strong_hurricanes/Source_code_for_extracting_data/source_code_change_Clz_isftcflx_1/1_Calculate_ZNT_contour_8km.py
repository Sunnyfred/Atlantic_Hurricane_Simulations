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
                 cartopy_ylim, latlon_coords, interplevel)
import json
from math import sin, cos, sqrt, atan2, radians
import pickle
import math






mainpath = '/project/momen/meng/COAWST/results/WRF_VS_WRFSWAN_2/'
Hurricaneall = ['Dorian','Maria','Irma','Katrina','Lorenzo']
Real_Hurricane_Data = ['Dorian_Real_Track_Time_NOAA.csv',
                        'Maria_Real_Track_Time_NOAA.csv',
                        'Irma_Real_Track_Time_NOAA.csv',
                        'Katrina_Real_Track_Time_NOAA.csv',
                        'Lorenzo_Real_Track_Time_NOAA.csv']
days = [31, 22, 2, 28, 27]  # start day
hours = [-6, -6, -6, -6, -6] # start hour
output_interval=6
gridsize = ['8km']
swansize = [  'swgr8p0']
prefix = 'WRFONLY_NoTurb_'
Dirall = ['_isftcflx_1_changeClz_0p0001',
       '_isftcflx_1_changeClz_0p0100',
       '_isftcflx_1_changeClz_1p0000',
       '_isftcflx_1_changeClz_100p0000']
outputpath = '/project/momen/meng/COAWST/results/WRF_VS_WRFSWAN_2/postprocessing_WRFONLY/0_Paper_figures/section2_change_pars_for_strong_winds/source_code_outputs_change_Clz_isftcflx_1/'




# prefix for WRF files
wrf_pre='wrfout_d01_'
# years and months for Hurricanes (must be in the same order as in days and Hurricaneall)
years_month = ['2019-08-','2017-09-','2017-09-','2005-08-','2019-09-']
# days selected to evaluated the averged wind speed, may select some time in the middle
avg_day = ['31', '22', '02', '28', '27']
wrf_af = '_18:00:00'





for gk in range(len(gridsize)):
    count1=0

    for Hurricane in Hurricaneall:

        count2=0
        for Dir in Dirall:
        

            print('Current folder is: ')
            Dir_local = mainpath+Hurricane+ '/' +gridsize[gk]+ '/' +prefix+gridsize[gk]+Dir
            print(Dir_local)
            #row.append(Hurricane+Dir)
             
            
            day=days[count1]
            hour=hours[count1]
            day_count=0
            # Set the working space>
            os.chdir(Dir_local)
            ncfiles = []
            ncfiles = [wrf_pre+years_month[count1]+avg_day[count1]+wrf_af]

            print(ncfiles)

            for ncfile in ncfiles:  
    

     	        ncfile = Dataset(ncfile)
     	        z = np.array(getvar (ncfile, 'z'))
     	        # #WSPD = np.array(getvar (ncfile, 'wspd'))
     	        # U10 = np.array(getvar (ncfile, 'U10'))
     	        # V10 = np.array(getvar (ncfile, 'V10'))
     	        # WSPD = np.sqrt(np.square(U10)+np.square(V10))
     	        slp2D = getvar(ncfile, "slp")
     	        ZNT2d = np.array(getvar (ncfile, 'ZNT'))
     	        # PRESSURE = np.array(getvar (ncfile, 'pressure'))

                


     	        pickle.dump( ZNT2d, open( outputpath+Hurricane+'_ZNT_par'+str(count2+1)+'_'+gridsize[gk]+'.p', "wb" ) )                                 
     	        pickle.dump( slp2D, open( outputpath+Hurricane+'_slp_par'+str(count2+1)+'_'+gridsize[gk]+'.p', "wb" ) )
     	        pickle.dump( z, open( outputpath+Hurricane+'_z_par'+str(count2+1)+'_'+gridsize[gk]+'.p', "wb" ) )   
            count2=count2+1
        count1=count1+1   