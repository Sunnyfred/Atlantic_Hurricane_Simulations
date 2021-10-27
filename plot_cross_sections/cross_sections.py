import csv
import matplotlib.pyplot as plt
import numpy as np
from collections import OrderedDict
import matplotlib as mpl
# import matplotlib.gridspec as gridspec
from matplotlib.ticker import MaxNLocator
from matplotlib.ticker import StrMethodFormatter
import matplotlib.font_manager as font_manager
from matplotlib.patches import Patch
import string
from netCDF4 import Dataset
import json
from cartopy.feature import NaturalEarthFeature
import cartopy.crs as crs
import pickle
from wrf import (to_np, getvar, smooth2d, get_cartopy, cartopy_xlim,
                 cartopy_ylim, latlon_coords, interplevel)
from matplotlib.cm import get_cmap


# List the colors that will be used for tracing the track.
csfont = {'fontname':'Times New Roman'}
font = font_manager.FontProperties(family='Times New Roman', size=30)
fontbar = font_manager.FontProperties(family='Times New Roman', size=12)
font_wt = font_manager.FontProperties(family='Times New Roman', size=25)
colors = ['k','blue','blue','gray', 'red', \
           'blue',  'cyan', 'lightcoral', 'turquoise','red','blue','green','pink']
patterns = ['-', '--','-.','-',':',':','--','--', ':','-', '--', ':','-', '--', ':',\
            '-.', '-.', '-.', ':', '--', '-']
markers = ['s','D','^','o','*','s','+','x','X','D','^','<','>','v'] 
sizes = [7, 7, 7, 7, 7, 3, 4, 3, 3, 3, 3, 3, 6,5,4,3,2,2]




options = ["Best Track",\
            "Clz=0.0001",\
            "Clz=0.01",\
            "Clz=1",\
            "Clz=100"]

    
models = ["Clz = 0.0001",\
            "Clz = 0.01",\
            "Clz = 1",\
            "Clz = 100"]    
    
    
models_data = ["wrfout_d01_2019-08-31_18_0p001",\
            "wrfout_d01_2019-08-31_18_0p010",\
            "wrfout_d01_2019-08-31_18_1p0000",\
            "wrfout_d01_2019-08-31_18_100p0000"]
# models = ["Clz = 0.0001"]

     
heights = ["10 m",\
            "80 m",\
            "100 m",\
            "200 m",\
            "500 m"]
heights_int = [10,80,100,200,500]
    
# subplot positions 
position = [[0,0,2],[0,2,4],[0,4,6],[1,0,2],[1,2,4]]
position2 = [[0,4,0,3],[0,4,4,7],[0,4,8,11],\
             [5,9,0,3],[5,9,4,7]]

# position3 = [[[2,6,0,4],[2,6,5,9],[2,6,10,14],[2,6,15,19],[2,6,20,24]],\
#              [[7,11,0,4],[7,11,5,9],[7,11,10,14],[7,11,15,19],[7,11,20,24]],\
#              [[12,16,0,4],[12,16,5,9],[12,16,10,14],[12,16,15,19],[12,16,20,24]],\
#              [[17,21,0,4],[17,21,5,9],[17,21,10,14],[17,21,15,19], [17,21,20,24]] ]
    

position3 = [[[3,7,2,6],[3,7,7,11],[3,7,12,16],[3,7,17,21],[3,7,22,26]],\
             [[8,12,2,6],[8,12,7,11],[8,12,12,16],[8,12,17,21],[8,12,22,26]],\
             [[13,17,2,6],[13,17,7,11],[13,17,12,16],[13,17,17,21],[13,17,22,26]],\
             [[18,22,2,6],[18,22,7,11],[18,22,12,16],[18,22,17,21], [18,22,22,26]] ]
    
    





    
    
    
    
# for COAWST    
    
lat_log_bound = [[-90.5, -84.5, 23, 29],\
                 [-74, -68, 19.5, 25.5],\
                 [-47, -39, 14, 22],\
                 [-76.5, -70.5, 23, 29],\
                 [-45.5, -39.5, 16.5, 22.5]]
    
   
### time 18h    
lat_log_bound2 = [[-91, -85, 24, 29],\
                 [-74, -68, 20.5, 24.5],\
                 [-45, -42.5, 17.5, 20],\
                 [-75.5, -73, 25, 27.5],\
                 [-45.5, -41, 18, 22]]    
    
    
# velocity contour levels
levels =[ [0, 10, 20, 30, 40, 50],
          [0, 10, 20, 30, 40, 50],
          [0, 10, 20, 30, 40],
          [0, 10, 20, 30, 40],
          [0, 10, 20, 30, 40, 50]]




# for WRF-YSU-2    
    
    
   
### time 18h    
lat_log_bound2 = [[-76, -73.5, 25.5, 28],\
                 [-76, -73.5, 25.5, 28],\
                 [-76, -73.5, 25.5, 28],\
                 [-76, -73.5, 25.5, 28],\
                 [-76, -73.5, 25.5, 28]]    
    
    
# velocity contour levels
levels =[ [0, 10, 20, 30, 40, 50, 60],
          [0, 10, 20, 30, 40, 50, 60],
          [0, 10, 20, 30, 40, 50, 60],
          [0, 10, 20, 30, 40, 50, 60],
          [0, 10, 20, 30, 40, 50, 60]]







##############################
# Plot velocity and pressure #
##############################





# define the canvas size 
fig = plt.figure(figsize=(26,22))
spec = mpl.gridspec.GridSpec(ncols=26, nrows=22)


    
for jj in range(len(models)):
    ncfile = Dataset("C:/Users/limgr/Desktop/Dorian_data/"+str(models_data[jj]))
    for kk in range(len(heights)):    
        
        Z_3D = np.array(getvar (ncfile, 'z'))
        press_3D = np.array(getvar (ncfile, 'pressure'))

        if(heights_int[kk]==10):

            slp2D = getvar(ncfile, "slp")
            press_2D = np.array(getvar (ncfile, 'slp'))
            U10 = np.array(getvar (ncfile, 'U10'))
            V10 = np.array(getvar (ncfile, 'V10'))    
            WSPD_2D = np.sqrt(np.square(U10)+np.square(V10))

            
        else:
            
            slp2D = getvar(ncfile, "slp")
            press_2D = np.array(getvar (ncfile, 'slp'))
            WSPD_3D = np.array(getvar (ncfile, 'wspd'))
            WSPD_2D = interplevel(WSPD_3D, Z_3D, heights_int[kk])


          
    
        #WSPD_2D = interplevel(WSPD_3D, Z_3D, 100)  # here altitude is 100m, consistent with the averaged speed profile vs radius
        #press_2D = interplevel(press_3D, Z_3D, 100)    
        smooth_slp = smooth2d(press_2D, 3, cenweight=4)
        # Get the latitude and longitude points
        lats, lons = latlon_coords(slp2D)
    
        # Get the cartopy mapping object (use original data, rather than any processed data)
        cart_proj = get_cartopy(slp2D)

        # Set the GeoAxes to the projection used by WRF
        #ax = plt.axes(projection=cart_proj)
        ax = fig.add_subplot(spec[position3[jj][kk][0]:position3[jj][kk][1], \
                              position3[jj][kk][2]:position3[jj][kk][3]], projection=cart_proj)
    

        # Download and add the states and coastlines
        states = NaturalEarthFeature(category="cultural", scale="50m",
	                             facecolor="none",
	                             name="admin_1_states_provinces_shp")
        ax.add_feature(states, linewidth=.5, edgecolor="black")
        ax.coastlines('50m', linewidth=0.8)
    
    
        # Make the contour outlines and filled contours for the smoothed sea level
        # pressure.
        # levels = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90]
        contours = plt.contour(lons, lats, press_2D, 3, colors="black",
              transform=crs.PlateCarree(), linewidths=2)
        plt.contourf(lons, lats, WSPD_2D, 8,
             levels=levels[kk], transform=crs.PlateCarree(), cmap=get_cmap("jet"))

        plt.clabel(contours, inline=True ,fmt='%.0f', fontsize=12,inline_spacing=-3)   
        
        

        # Set the map bounds
        ax.set_extent(lat_log_bound2[kk])

    


        
        
        for axis in ['top','bottom','left','right']:
            ax.spines[axis].set_linewidth(15)
        plt.title(heights[kk], {'size': 35}, **csfont)

    
    
        # Show grid lines.
        gl = ax.gridlines(crs=crs.PlateCarree(), draw_labels=True,
                  linewidth=1., color='black', alpha=0.8, linestyle='dotted')
        gl.xlabel_style = {'size': 25, 'color': 'k', 'fontname':'Times New Roman'}
        gl.ylabel_style = {'size': 25, 'color': 'k', 'fontname':'Times New Roman'}
        gl.xlabels_top = False
        gl.ylabels_right = False
        
        
        if jj==0:
            ### colorbar for fig array start here 
            ax = fig.add_subplot(spec[0:2, position3[jj][kk][2]:position3[jj][kk][3]])
            # Add a color bar
            cbar = plt.colorbar(ax=ax,fraction=0.3, orientation='horizontal')
            #cbar.ax.set_ylabel(r'Wind Speed (m/s)',labelpad=20)
            cbar.ax.set_title('Wind Speed (m/s)', **csfont, fontsize=30)
            cbar.ax.tick_params(labelsize=25) 
            # plt.legend(bbox_to_anchor=(0.9, 0.8), prop=fontbar, \
            #                 frameon=False)
            ax.axes.xaxis.set_visible(False)
            ax.axes.yaxis.set_visible(False)
            ax.set_yticks([])
            ax.set_yticklabels([])
            ax.set_xticks([])
            ax.set_xticklabels([])
            for axis in ['top','bottom','left','right']:
                ax.spines[axis].set_visible(False)










### y label for fig array start here 
ax = fig.add_subplot(spec[3:7, 0:1])
ax.axes.xaxis.set_visible(False)
ax.axes.yaxis.set_visible(False)
ax.set_yticks([])
ax.set_yticklabels([])
ax.set_xticks([])
ax.set_xticklabels([])
for axis in ['top','bottom','left','right']:
    ax.spines[axis].set_visible(False)
ax.text(0.6, 0.2, models[0], transform=ax.transAxes, 
             size=30, rotation=90, **csfont)


ax = fig.add_subplot(spec[8:12, 0:1])
ax.axes.xaxis.set_visible(False)
ax.axes.yaxis.set_visible(False)
ax.set_yticks([])
ax.set_yticklabels([])
ax.set_xticks([])
ax.set_xticklabels([])
for axis in ['top','bottom','left','right']:
    ax.spines[axis].set_visible(False)
ax.text(0.6, 0.2, models[1], transform=ax.transAxes, 
             size=30, rotation=90, **csfont)


ax = fig.add_subplot(spec[13:17, 0:1])
ax.axes.xaxis.set_visible(False)
ax.axes.yaxis.set_visible(False)
ax.set_yticks([])
ax.set_yticklabels([])
ax.set_xticks([])
ax.set_xticklabels([])
for axis in ['top','bottom','left','right']:
    ax.spines[axis].set_visible(False)
ax.text(0.6, 0.3, models[2], transform=ax.transAxes, 
             size=30, rotation=90, **csfont)
  
    

ax = fig.add_subplot(spec[18:22, 0:1])
ax.axes.xaxis.set_visible(False)
ax.axes.yaxis.set_visible(False)
ax.set_yticks([])
ax.set_yticklabels([])
ax.set_xticks([])
ax.set_xticklabels([])
for axis in ['top','bottom','left','right']:
    ax.spines[axis].set_visible(False)
ax.text(0.6, 0.2, models[3], transform=ax.transAxes, 
             size=30, rotation=90, **csfont)

plt.savefig('C:/Users/limgr/Desktop/'+str(heights_int[kk])+'_all_ve_pre.png', dpi=500)
plt.show()
