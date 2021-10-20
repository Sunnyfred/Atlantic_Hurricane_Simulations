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
# models = ["Clz = 0.0001"]

     
hurricanes = ["Katrina",\
            "Maria",\
            "Irma",\
            "Dorian",\
            "Lorenzo"]
    
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
    
    
    
linestyles = OrderedDict(
    [('solid',               (0, ())),
     ('dashdotted',          (0, (3, 3, 1, 3))),
     ('dashdotdotted',       (0, (3, 2, 1, 2, 1, 2))),
     ('dashed',              (0, (3, 3))),
     ('dotted',              (0, (1, 3))),
     ('dashed',              (0, (3, 3))),
     ('loosely dotted',      (0, (1, 10))),
     ('densely dotted',      (0, (1, 1))),
     ('loosely dashed',      (0, (5, 10))),
     ('densely dashed',      (0, (5, 1))),
     ('loosely dashdotted',  (0, (3, 10, 1, 10))),
     ('densely dashdotted',  (0, (3, 1, 1, 1))),
     ('loosely dashdotdotted', (0, (3, 10, 1, 10, 1, 10))),
     ('densely dashdotdotted', (0, (3, 1, 1, 1, 1, 1)))])



R = 6373.0 # approxiamte radius of earth in km




# folder for wi and wt files


dir_wi = ['C:/Users/limgr/Desktop/Katrina_wind_intensity_8km.csv',\
       'C:/Users/limgr/Desktop/Maria_wind_intensity_8km.csv',\
       'C:/Users/limgr/Desktop/Irma_wind_intensity_8km.csv',\
       'C:/Users/limgr/Desktop/Dorian_wind_intensity_8km.csv',\
       'C:/Users/limgr/Desktop/Lorenzo_wind_intensity_8km.csv']

    
dir_wt = ['C:/Users/limgr/Desktop/Katrina_track_8km.txt',\
       'C:/Users/limgr/Desktop/Maria_track_8km.txt',\
       'C:/Users/limgr/Desktop/Irma_track_8km.txt',\
       'C:/Users/limgr/Desktop/Dorian_track_8km.txt',\
       'C:/Users/limgr/Desktop/Lorenzo_track_8km.txt']    

dir_p = ['C:/Users/limgr/Desktop/Katrina_8km.p',\
       'C:/Users/limgr/Desktop/Maria_8km.p',\
       'C:/Users/limgr/Desktop/Irma_8km.p',\
       'C:/Users/limgr/Desktop/Dorian_8km.p',\
       'C:/Users/limgr/Desktop/Lorenzo_8km.p']    

dir_znt = ['C:/Users/limgr/Desktop/Katrina_ZNT_8km.csv',\
       'C:/Users/limgr/Desktop/Maria_ZNT_8km.csv',\
       'C:/Users/limgr/Desktop/Irma_ZNT_8km.csv',\
       'C:/Users/limgr/Desktop/Dorian_ZNT_8km.csv',\
       'C:/Users/limgr/Desktop/Lorenzo_ZNT_8km.csv'] 


dir_wp = ['C:/Users/limgr/Desktop/Katrina_avg_speed_8km.csv', \
          'C:/Users/limgr/Desktop/Maria_avg_speed_8km.csv', \
          'C:/Users/limgr/Desktop/Irma_avg_speed_8km.csv', \
          'C:/Users/limgr/Desktop/Dorian_avg_speed_8km.csv', \
          'C:/Users/limgr/Desktop/Lorenzo_avg_speed_8km.csv'] 
    
    
dir_zp1 = ['C:/Users/limgr/Desktop/old_simulation/Katrina_z_par1_8km.p',\
       'C:/Users/limgr/Desktop/old_simulation/Maria_z_par1_8km.p',\
       'C:/Users/limgr/Desktop/old_simulation/Irma_z_par1_8km.p',\
       'C:/Users/limgr/Desktop/old_simulation/Dorian_z_par1_8km.p',\
       'C:/Users/limgr/Desktop/old_simulation/Lorenzo_z_par1_8km.p']     
    
dir_slpp1 = ['C:/Users/limgr/Desktop/old_simulation/Katrina_slp_par1_8km.p',\
       'C:/Users/limgr/Desktop/old_simulation/Maria_slp_par1_8km.p',\
       'C:/Users/limgr/Desktop/old_simulation/Irma_slp_par1_8km.p',\
       'C:/Users/limgr/Desktop/old_simulation/Dorian_slp_par1_8km.p',\
       'C:/Users/limgr/Desktop/old_simulation/Lorenzo_slp_par1_8km.p']   
    
dir_wspdp1 = ['C:/Users/limgr/Desktop/old_simulation/Katrina_wspd_par1_8km.p',\
       'C:/Users/limgr/Desktop/old_simulation/Maria_wspd_par1_8km.p',\
       'C:/Users/limgr/Desktop/old_simulation/Irma_wspd_par1_8km.p',\
       'C:/Users/limgr/Desktop/old_simulation/Dorian_wspd_par1_8km.p',\
       'C:/Users/limgr/Desktop/old_simulation/Lorenzo_wspd_par1_8km.p']    
    
dir_pressurep1 = ['C:/Users/limgr/Desktop/old_simulation/Katrina_pressure_par1_8km.p',\
       'C:/Users/limgr/Desktop/old_simulation/Maria_pressure_par1_8km.p',\
       'C:/Users/limgr/Desktop/old_simulation/Irma_pressure_par1_8km.p',\
       'C:/Users/limgr/Desktop/old_simulation/Dorian_pressure_par1_8km.p',\
       'C:/Users/limgr/Desktop/old_simulation/Lorenzo_pressure_par1_8km.p']   
    
    


dir_zp2 = ['C:/Users/limgr/Desktop/old_simulation/Katrina_z_par2_8km.p',\
       'C:/Users/limgr/Desktop/old_simulation/Maria_z_par2_8km.p',\
       'C:/Users/limgr/Desktop/old_simulation/Irma_z_par2_8km.p',\
       'C:/Users/limgr/Desktop/old_simulation/Dorian_z_par2_8km.p',\
       'C:/Users/limgr/Desktop/old_simulation/Lorenzo_z_par2_8km.p']     
    
dir_slpp2 = ['C:/Users/limgr/Desktop/old_simulation/Katrina_slp_par2_8km.p',\
       'C:/Users/limgr/Desktop/old_simulation/Maria_slp_par2_8km.p',\
       'C:/Users/limgr/Desktop/old_simulation/Irma_slp_par2_8km.p',\
       'C:/Users/limgr/Desktop/old_simulation/Dorian_slp_par2_8km.p',\
       'C:/Users/limgr/Desktop/old_simulation/Lorenzo_slp_par2_8km.p']   
    
dir_wspdp2 = ['C:/Users/limgr/Desktop/old_simulation/Katrina_wspd_par2_8km.p',\
       'C:/Users/limgr/Desktop/old_simulation/Maria_wspd_par2_8km.p',\
       'C:/Users/limgr/Desktop/old_simulation/Irma_wspd_par2_8km.p',\
       'C:/Users/limgr/Desktop/old_simulation/Dorian_wspd_par2_8km.p',\
       'C:/Users/limgr/Desktop/old_simulation/Lorenzo_wspd_par2_8km.p']    
    
dir_pressurep2 = ['C:/Users/limgr/Desktop/old_simulation/Katrina_pressure_par2_8km.p',\
       'C:/Users/limgr/Desktop/old_simulation/Maria_pressure_par2_8km.p',\
       'C:/Users/limgr/Desktop/old_simulation/Irma_pressure_par2_8km.p',\
       'C:/Users/limgr/Desktop/old_simulation/Dorian_pressure_par2_8km.p',\
       'C:/Users/limgr/Desktop/old_simulation/Lorenzo_pressure_par2_8km.p']
    

    
    
dir_zp3 = ['C:/Users/limgr/Desktop/old_simulation/Katrina_z_par3_8km.p',\
       'C:/Users/limgr/Desktop/old_simulation/Maria_z_par3_8km.p',\
       'C:/Users/limgr/Desktop/old_simulation/Irma_z_par3_8km.p',\
       'C:/Users/limgr/Desktop/old_simulation/Dorian_z_par3_8km.p',\
       'C:/Users/limgr/Desktop/old_simulation/Lorenzo_z_par3_8km.p']     
    
dir_slpp3 = ['C:/Users/limgr/Desktop/old_simulation/Katrina_slp_par3_8km.p',\
       'C:/Users/limgr/Desktop/old_simulation/Maria_slp_par3_8km.p',\
       'C:/Users/limgr/Desktop/old_simulation/Irma_slp_par3_8km.p',\
       'C:/Users/limgr/Desktop/old_simulation/Dorian_slp_par3_8km.p',\
       'C:/Users/limgr/Desktop/old_simulation/Lorenzo_slp_par3_8km.p']   
    
dir_wspdp3 = ['C:/Users/limgr/Desktop/old_simulation/Katrina_wspd_par3_8km.p',\
       'C:/Users/limgr/Desktop/old_simulation/Maria_wspd_par3_8km.p',\
       'C:/Users/limgr/Desktop/old_simulation/Irma_wspd_par3_8km.p',\
       'C:/Users/limgr/Desktop/old_simulation/Dorian_wspd_par3_8km.p',\
       'C:/Users/limgr/Desktop/old_simulation/Lorenzo_wspd_par3_8km.p']    
    
dir_pressurep3 = ['C:/Users/limgr/Desktop/old_simulation/Katrina_pressure_par3_8km.p',\
       'C:/Users/limgr/Desktop/old_simulation/Maria_pressure_par3_8km.p',\
       'C:/Users/limgr/Desktop/old_simulation/Irma_pressure_par3_8km.p',\
       'C:/Users/limgr/Desktop/old_simulation/Dorian_pressure_par3_8km.p',\
       'C:/Users/limgr/Desktop/old_simulation/Lorenzo_pressure_par3_8km.p']





dir_zp4 = ['C:/Users/limgr/Desktop/old_simulation/Katrina_z_par4_8km.p',\
       'C:/Users/limgr/Desktop/old_simulation/Maria_z_par4_8km.p',\
       'C:/Users/limgr/Desktop/old_simulation/Irma_z_par4_8km.p',\
       'C:/Users/limgr/Desktop/old_simulation/Dorian_z_par4_8km.p',\
       'C:/Users/limgr/Desktop/old_simulation/Lorenzo_z_par4_8km.p']     
    
dir_slpp4 = ['C:/Users/limgr/Desktop/old_simulation/Katrina_slp_par4_8km.p',\
       'C:/Users/limgr/Desktop/old_simulation/Maria_slp_par4_8km.p',\
       'C:/Users/limgr/Desktop/old_simulation/Irma_slp_par4_8km.p',\
       'C:/Users/limgr/Desktop/old_simulation/Dorian_slp_par4_8km.p',\
       'C:/Users/limgr/Desktop/old_simulation/Lorenzo_slp_par4_8km.p']   
    
dir_wspdp4 = ['C:/Users/limgr/Desktop/old_simulation/Katrina_wspd_par4_8km.p',\
       'C:/Users/limgr/Desktop/old_simulation/Maria_wspd_par4_8km.p',\
       'C:/Users/limgr/Desktop/old_simulation/Irma_wspd_par4_8km.p',\
       'C:/Users/limgr/Desktop/old_simulation/Dorian_wspd_par4_8km.p',\
       'C:/Users/limgr/Desktop/old_simulation/Lorenzo_wspd_par4_8km.p']    
    
dir_pressurep4 = ['C:/Users/limgr/Desktop/old_simulation/Katrina_pressure_par4_8km.p',\
       'C:/Users/limgr/Desktop/old_simulation/Maria_pressure_par4_8km.p',\
       'C:/Users/limgr/Desktop/old_simulation/Irma_pressure_par4_8km.p',\
       'C:/Users/limgr/Desktop/old_simulation/Dorian_pressure_par4_8km.p',\
       'C:/Users/limgr/Desktop/old_simulation/Lorenzo_pressure_par4_8km.p']        

    
    
    
lat_log_bound = [[-90.5, -84.5, 23, 29],\
                 [-74, -68, 19.5, 25.5],\
                 [-47, -39, 14, 22],\
                 [-76.5, -70.5, 23, 29],\
                 [-45.5, -39.5, 16.5, 22.5]]
    
    
### time 24h    
# lat_log_bound2 = [[-92, -86, 25, 30],\
#                  [-74, -68, 21.5, 25.5],\
#                  [-46, -43.5, 17, 19.5],\
#                  [-76, -73.5, 25.5, 28],\
#                  [-46, -42, 19, 23]]
   
### time 18h    
lat_log_bound2 = [[-91, -85, 24, 29],\
                 [-74, -68, 20.5, 24.5],\
                 [-45, -42.5, 17.5, 20],\
                 [-75.5, -73, 25, 27.5],\
                 [-45.5, -41, 18, 22]]    
    
    
# velocity contour levels
levels =[ [0, 10, 20, 30, 40, 50, 60, 70],
          [0, 10, 20, 30, 40, 50, 60],
          [0, 10, 20, 30, 40, 50, 60],
          [0, 10, 20, 30, 40, 50, 60],
          [0, 10, 20, 30, 40, 50, 60]]

def Calculate_Distance_Haversine1(x):
    return (np.sin(x[0]/2))**2
def Calculate_Distance_Haversine2(x):
    return np.cos(x[0])
def Calculate_Distance_Haversine3(x):
    return (np.sin(x[1]/2))**2







##############################
# Plot velocity and pressure #
##############################


 
dir_zp = [dir_zp1,dir_zp2,dir_zp3,dir_zp4]
dir_slpp = [dir_slpp1,dir_slpp2,dir_slpp3,dir_slpp4]
dir_wspdp = [dir_wspdp1,dir_wspdp2,dir_wspdp3,dir_wspdp4]
dir_pressurep = [dir_pressurep1,dir_pressurep2,dir_pressurep3,dir_pressurep4]



# define the canvas size 
fig = plt.figure(figsize=(26,22))
spec = mpl.gridspec.GridSpec(ncols=26, nrows=22)


    
for jj in range(len(models)):
    for kk in range(len(hurricanes)): 
        
        print(dir_slpp[jj][kk])
        Z_3D = pickle.load( open( dir_zp[jj][kk], "rb" ) )
        slp2D = pickle.load( open( dir_slpp[jj][kk], "rb" ) )
        press_2D = pickle.load( open( dir_slpp[jj][kk], "rb" ) )
        #WSPD_3D = np.array(pickle.load( open( dir_wspdp[jj][kk], "rb" ) ))
        WSPD_2D = np.array(pickle.load( open( dir_wspdp[jj][kk], "rb" ) ))
        press_3D = np.array(pickle.load( open( dir_pressurep[jj][kk], "rb" ) ))
    
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
        plt.title(hurricanes[kk], {'size': 35}, **csfont)

    
    
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

plt.savefig('C:/Users/limgr/Desktop/'+hurricanes[kk]+'_all_ve_pre.png', dpi=500)
plt.show()

### y label for fig array end here 








# #########################################
# # Plot normalized intensity time series #
# #########################################

# fig = plt.figure(figsize=(22,12))
# spec = mpl.gridspec.GridSpec(ncols=11, nrows=9)


# for kk in range(len(hurricanes)):
    
#     c=0
#     rows=[]
#     Times=[]
#     Times=[]
#     values=[]
#     with open(dir_wi[kk], mode='r') as csv_file:
#         csv_reader = csv.DictReader(csv_file)
#         line_count = 0
#         for row in csv_reader:
#             if line_count == 0:
#                 print(f'Column names are {", ".join(row)}')
#                 Times.append(list(row.keys()))
#                 line_count += 1
#             #print(row)
#             rows.append(row)
#             values.append(list(row.values()))
#             line_count += 1
#         print(f'Processed {line_count} lines.')
    
#     Times0=Times[0]
#     print(Times0)
#     print(values[0])
#     print(position[kk])
    
    
#     ax = fig.add_subplot(spec[position2[kk][0]:position2[kk][1],\
#                               position2[kk][2]:position2[kk][3]])
#     ax.text(0.05, 0.85, '('+string.ascii_lowercase[kk]+')', transform=ax.transAxes, 
#             size=30)


#     for i in range(0,line_count-1):
#         if i==0:
#             tmp=[float(i)*0.5144444 for i in values[i]]
#             #tmp=[float(i) for i in values[i]]
#         # elif (i!=2 and i!=3):
#         else:
#             tmp=[float(i) for i in values[i]]
#         # else:
#         #     continue
        
#         if hurricanes[kk]=='Katrina':
#             plt.plot( Times0[:5], tmp[:5], color = colors[c], \
#                       linestyle=list(linestyles.values())[c],\
#                   linewidth=5, markersize=sizes[c])
#             plt.xticks(fontsize=25)
#             plt.yticks(fontsize=25)
#             plt.ylim([25, 80])
#         elif hurricanes[kk]=='Dorian':
#             plt.plot( Times0[:-2], tmp[:-2], color = colors[c], \
#                       linestyle=list(linestyles.values())[c],\
#                   linewidth=5, markersize=sizes[c])
#             plt.xticks(fontsize=25)
#             plt.yticks(fontsize=25)
#             plt.ylim([25, 80])
#         else:
#             plt.plot( Times0, tmp, color = colors[c], \
#                       linestyle=list(linestyles.values())[c],\
#                   linewidth=5, markersize=sizes[c])
#             plt.xticks(fontsize=25)
#             plt.yticks(fontsize=25)
#             plt.gca().yaxis.set_major_formatter(StrMethodFormatter('{x:,.0f}'))
#             plt.ylim([25, 80])

#         c+=1
        
#     for axis in ['top','bottom','left','right']:
#         ax.spines[axis].set_linewidth(2)
#     ax.tick_params(length=5, width=2)
#     fig.legend(options, bbox_to_anchor=(0.89, 0.42), prop=font, \
#                 frameon=False)
    

#     if kk==0 or kk==3:
#         plt.ylabel(r'Intensity (m/s)', **csfont, fontsize=35)
#     if kk==2 or kk==3 or kk==4:
#         plt.xlabel(r"Time Series (hr)", fontsize=30, **csfont)
#     plt.title(hurricanes[kk], {'size': 30}, **csfont)

    
    
# plt.savefig('C:/Users/limgr/Desktop/'+hurricanes[kk]+'_wind_intensity_A.png', dpi=500)
# plt.show()













# ########################
# # Plot ZNT time series #
# ########################


# fig = plt.figure(figsize=(22,12))
# spec = mpl.gridspec.GridSpec(ncols=11, nrows=9)


# for kk in range(len(hurricanes)):
    
#     c=0
#     rows=[]
#     Times=[]
#     Times=[]
#     values=[]
#     with open(dir_znt[kk], mode='r') as csv_file:
#         csv_reader = csv.DictReader(csv_file)
#         line_count = 0
#         for row in csv_reader:
#             if line_count == 0:
#                 print(f'Column names are {", ".join(row)}')
#                 Times.append(list(row.keys()))
#                 line_count += 1
#             #print(row)
#             rows.append(row)
#             values.append(list(row.values()))
#             line_count += 1
#         print(f'Processed {line_count} lines.')
    
#     Times0=Times[0]
#     print(Times0)
#     print(values[0])
#     print(position[kk])
    
    
#     ax = fig.add_subplot(spec[position2[kk][0]:position2[kk][1],\
#                               position2[kk][2]:position2[kk][3]])
#     ax.text(0.05, 0.85, '('+string.ascii_lowercase[kk]+')', transform=ax.transAxes, 
#             size=30)


#     for i in range(0,line_count-1):
#         if i==0:
#             #tmp=[float(i)*0.5144444 for i in values[i]]
#             tmp=[float(i) for i in values[i]]
#         # elif (i!=2 and i!=3):
#         else:
#             tmp=[float(i) for i in values[i]]
#         # else:
#         #     continue
        
#         if hurricanes[kk]=='Katrina':
#             plt.plot( Times0[:5], tmp[:5], color = colors[c+1], \
#                       linestyle=list(linestyles.values())[c+1],\
#                   linewidth=5, markersize=sizes[c+1])
#             plt.xticks(fontsize=25)
#             plt.yticks(fontsize=25)
#             plt.ylim([1e-5, 2.0])
#             plt.yscale('log')
#         elif hurricanes[kk]=='Dorian':
#             plt.plot( Times0[:-2], tmp[:-2], color = colors[c+1], \
#                       linestyle=list(linestyles.values())[c+1],\
#                   linewidth=5, markersize=sizes[c+1])
#             plt.xticks(fontsize=25)
#             plt.yticks(fontsize=25)
#             plt.ylim([1e-5, 2.0])
#             plt.yscale('log')
#         else:
#             plt.plot( Times0, tmp, color = colors[c+1], \
#                       linestyle=list(linestyles.values())[c+1],\
#                   linewidth=5, markersize=sizes[c+1])
#             plt.xticks(fontsize=25)
#             plt.yticks(fontsize=25)
#             plt.gca().yaxis.set_major_formatter(StrMethodFormatter('{x:,.0f}'))
#             plt.ylim([1e-5, 2.0])
#             plt.yscale('log')

#         c+=1
        
#     for axis in ['top','bottom','left','right']:
#         ax.spines[axis].set_linewidth(2)
#     ax.tick_params(length=5, width=2)
#     fig.legend(models, bbox_to_anchor=(0.89, 0.42), prop=font, \
#                 frameon=False)
    

#     if kk==0 or kk==3:
#         plt.ylabel(r'$Z_0$ (m)', **csfont, fontsize=30)
#     if kk==2 or kk==3 or kk==4:
#         plt.xlabel(r"Time Series (hr)", fontsize=30, **csfont)
#     plt.title(hurricanes[kk], {'size': 30}, **csfont)

    
    
# plt.savefig('C:/Users/limgr/Desktop/'+hurricanes[kk]+'_ZNT.png', dpi=500)
# plt.show()


































# #########################################
# # Plot averaged speed  versus radisu    #
# #########################################

# fig = plt.figure(figsize=(25,12))
# spec = mpl.gridspec.GridSpec(ncols=11, nrows=9)


# for kk in range(len(hurricanes)):
    
#     c=0
#     Times=[]
#     values=[]
#     with open(dir_wp[kk], mode='r') as csv_file:
#         csv_reader = csv.reader(csv_file, delimiter=',')
#         line_count = 0
#         for row in csv_reader:
#             if line_count % 2 == 0:
#                 # print(f'Column names are {", ".join(row)}')
#                 print(len(row))
#                 Times.append(row)
#                 line_count += 1

#             else:
#                 # print(f'value names are {", ".join(row)}')
#                 print(len(row))
#                 values.append(row)
#                 line_count += 1

#         print(f'Processed {line_count} lines.')
        
#     for i in range(int(float(line_count)/2.)):
#         values[i] = [float(x) for x in values[i]]
#         Times[i] = [float(x) for x in Times[i]]
#     print(Times[0])
#     print(values[0])
#     print(len(Times), len(values))
#     # print(position[kk])
    
    
#     ax = fig.add_subplot(spec[position2[kk][0]:position2[kk][1],\
#                               position2[kk][2]:position2[kk][3]])
#     ax.text(0.05, 0.85, '('+string.ascii_lowercase[kk]+')', transform=ax.transAxes, 
#             size=30)


#     for i in range(int(float(line_count)/2.)):
#         print(i)
#         # if i==0:
#         #     #tmp=[float(i)*0.5144444 for i in values[i]]
#         #     tmp=[float(i) for i in values[i]]
#         # # elif (i!=2 and i!=3):
#         # else:
#         #     tmp=[float(i) for i in values[i]]
#         # # else:
#         # #     continue
        
#         if hurricanes[kk]=='Katrina':
#             plt.plot( Times[i], values[i], color = colors[c+1], \
#                       linestyle=list(linestyles.values())[c+1],\
#                   linewidth=5, markersize=sizes[c+1])
#             plt.xticks(np.arange(min(Times[i]), max(Times[i])+1, 50), fontsize=25)
#             plt.yticks(fontsize=25)
#             plt.ylim([0, 80])
#             plt.xlim([0, 210])
#             # plt.xscale('log')
#             # plt.yscale('log')
#         elif hurricanes[kk]=='Dorian':
#             plt.plot( Times[i], values[i], color = colors[c+1], \
#                       linestyle=list(linestyles.values())[c+1],\
#                   linewidth=5, markersize=sizes[c])
#             plt.xticks(np.arange(min(Times[i]), max(Times[i])+1, 50), fontsize=25)
#             plt.yticks(fontsize=25)
#             plt.ylim([0, 80])
#             plt.xlim([0, 210])
#             # plt.xscale('log')
#             # plt.yscale('log')
#         else:
#             plt.plot( Times[i], values[i], color = colors[c+1], \
#                       linestyle=list(linestyles.values())[c+1],\
#                   linewidth=5, markersize=sizes[c+1])
#             plt.xticks(np.arange(min(Times[i]), max(Times[i])+1, 50), fontsize=25)
#             plt.yticks(fontsize=25)
#             plt.gca().yaxis.set_major_formatter(StrMethodFormatter('{x:,.0f}'))
#             plt.ylim([0, 80])
#             plt.xlim([0, 210])
#             # plt.xscale('log')
#             # plt.yscale('log')

#         c+=1
        
#     for axis in ['top','bottom','left','right']:
#         ax.spines[axis].set_linewidth(2)
#     ax.tick_params(length=5, width=2)
#     fig.legend(models, bbox_to_anchor=(0.89, 0.42), prop=font, \
#                 frameon=False)
    

#     if kk==0 or kk==3:
#         plt.ylabel(r'Wind Speed (m/s)', **csfont, fontsize=35)
#     if kk==2 or kk==3 or kk==4:
#         plt.xlabel(r"Radius (km)", fontsize=30, **csfont)
#     plt.title(hurricanes[kk], {'size': 30}, **csfont)

    
    
# plt.savefig('C:/Users/limgr/Desktop/'+hurricanes[kk]+'_avg_wind.png', dpi=500)
# plt.show()


























# ########################
# # Plot hurricane track #
# ########################






# fig = plt.figure(figsize=(15,10))
# spec = mpl.gridspec.GridSpec(ncols=6, nrows=2)

# for kk in range(len(hurricanes)):
    
#     real1=[]
#     oussama1=[]
#     wrf1=[]
#     simu1=[]

#     with open( dir_wt[kk], 'r' ) as f :
#         data0 = f.read()
#         data = json.loads('[' + data0.replace('}{', '},{') + ']')
#     for i in range(0,len(data)):
#         data2 = list(data[i].values())
#         data3 = [e for sl in data2 for e in sl]
#         for j in range(len(data3)):
#             data3[j].pop(0)
#         if i==0:
#             real1.append(data3)
#         # elif i==1:
#         #     oussama1.append(data3)
#         # elif i==2:
#         #     wrf1.append(data3)
#         else:
#             simu1.append(data3)
#     real1 = np.array(real1, dtype=np.float32)
#     simu1 = np.array(simu1, dtype=np.float32)
#     real_r = np.radians(real1)
#     simu_r = np.radians(simu1)


#     term1=np.apply_along_axis(Calculate_Distance_Haversine1, 2, simu_r-real_r)
#     term2=np.apply_along_axis(Calculate_Distance_Haversine2, 2, simu_r)* \
#         np.apply_along_axis(Calculate_Distance_Haversine2, 2, real_r)* \
#         np.apply_along_axis(Calculate_Distance_Haversine3, 2, simu_r-real_r)
#     simu_error1=2*R*np.arcsin(np.sqrt(term1+term2))




#     # ax = fig.add_subplot(spec[position[kk][0],position[kk][1]:position[kk][2]])
#     # ax.text(0.05, 0.9, '('+string.ascii_lowercase[kk]+')', transform=ax.transAxes, 
#     #         size=30)

#     slp2D = pickle.load( open( dir_p[kk], "rb" ) )
#     lats, lons = latlon_coords(slp2D)
    
#     # Get the cartopy mapping object (use original data, rather than any processed data)
#     cart_proj = get_cartopy(slp2D)

#     # Set the GeoAxes to the projection used by WRF
#     #ax = plt.axes(projection=cart_proj)
#     ax = fig.add_subplot(spec[position[kk][0],position[kk][1]:position[kk][2]], projection=cart_proj)
#     ax.stock_img()
    

#     # Download and add the states and coastlines
#     states = NaturalEarthFeature(category="cultural", scale="50m",
# 	                             facecolor="none",
# 	                             name="admin_1_states_provinces_shp")
#     ax.add_feature(states, linewidth=.5, edgecolor="black")
#     ax.coastlines('50m', linewidth=0.8)
#     # Set the map bounds
#     # ax.set_xlim(cartopy_xlim(slp2D))
#     # ax.set_ylim(cartopy_ylim(slp2D))
#     ax.set_extent(lat_log_bound[kk])


#     # Show grid lines.
#     gl = ax.gridlines(crs=crs.PlateCarree(), draw_labels=True,
#                   linewidth=1.5, color='gray', alpha=0.8, linestyle=':')
#     gl.xlabel_style = {'size': 15, 'color': 'k'}
#     gl.ylabel_style = {'size': 15, 'color': 'k'}
#     gl.xlabels_top = False
#     gl.ylabels_right = False

#     c=0

#     ll=[]
#     rr=[]
#     for i in range(real1.shape[0]):
#         for j in range(real1.shape[1]):
#             if j<6:
#                 ll.append(real1[i][j][0])
#                 rr.append(real1[i][j][1])
#         ax.plot( rr, ll, color = colors[c], marker=markers[c],linewidth=2, \
#                 linestyle=list(linestyles.values())[c],\
#                   markersize=sizes[c], transform=crs.PlateCarree())
#         c+=1


#     ll=[]
#     rr=[]
#     for i in range(simu1.shape[0]):
#         for j in range(simu1.shape[1]):
#             if j<6:
#                 ll.append(simu1[i][j][0])
#                 rr.append(simu1[i][j][1])
#         ax.plot( rr, ll, color = colors[c], marker=markers[c],linewidth=2, \
#                 linestyle=list(linestyles.values())[c],\
#                   markersize=sizes[c], transform=crs.PlateCarree())
#         c+=1
#         ll=[]
#         rr=[]
        
        
#     for axis in ['top','bottom','left','right']:
#         ax.spines[axis].set_linewidth(15)
#     fig.legend(options, bbox_to_anchor=(0.87, 0.42), prop=font_wt, \
#                 frameon=False)
        
#     plt.title(hurricanes[kk], {'size': 25}, **csfont)
#     # plt.legend(['Real track','C0.0001', 'C0.01', 'C1', 'C100'],\
#     #        loc = "upper right", prop={'size': 7})
#     # plt.xlabel("Lon", fontsize=135)
#     # plt.ylabel("Lat", fontsize=135)
#     # plt.title(hurricanes[kk], {'size': 35}, **csfont)
#     # plt.show()

# plt.savefig('C:/Users/limgr/Desktop/'+hurricanes[kk]+'_wt.png', dpi=500)
# plt.show()



















# # fig = plt.figure(figsize=(15,10))
# # spec = mpl.gridspec.GridSpec(ncols=6, nrows=2)

# # for kk in range(len(hurricanes)):
    
# #     real1=[]
# #     oussama1=[]
# #     wrf1=[]
# #     simu1=[]

# #     with open( dir_wt[kk], 'r' ) as f :
# #         data0 = f.read()
# #         data = json.loads('[' + data0.replace('}{', '},{') + ']')
# #     for i in range(0,len(data)):
# #         data2 = list(data[i].values())
# #         data3 = [e for sl in data2 for e in sl]
# #         for j in range(len(data3)):
# #             data3[j].pop(0)
# #         if i==0:
# #             real1.append(data3)
# #         # elif i==1:
# #         #     oussama1.append(data3)
# #         # elif i==2:
# #         #     wrf1.append(data3)
# #         else:
# #             simu1.append(data3)
# #     real1 = np.array(real1, dtype=np.float32)
# #     simu1 = np.array(simu1, dtype=np.float32)
# #     real_r = np.radians(real1)
# #     simu_r = np.radians(simu1)


# #     term1=np.apply_along_axis(Calculate_Distance_Haversine1, 2, simu_r-real_r)
# #     term2=np.apply_along_axis(Calculate_Distance_Haversine2, 2, simu_r)* \
# #         np.apply_along_axis(Calculate_Distance_Haversine2, 2, real_r)* \
# #         np.apply_along_axis(Calculate_Distance_Haversine3, 2, simu_r-real_r)
# #     simu_error1=2*R*np.arcsin(np.sqrt(term1+term2))


# #     m = Basemap(projection='merc', llcrnrlat=lat_log_bound[kk][2],\
# #                 urcrnrlat=lat_log_bound[kk][3], \
# #                 llcrnrlon=lat_log_bound[kk][0], \
# #                 urcrnrlon=lat_log_bound[kk][1], resolution= 'f' )
# #     m.drawstates()
# #     m.drawmeridians([-100, -90, -80, -70, -60, -50, -40, ], color='k', textcolor='k', linewidth=1.5,
# #      zorder=None, dashes=[6, 1000], labels=[1, 0, 0, 1], labelstyle=None, fmt='%g', xoffset=None, 
# #      yoffset=None, ax=None, latmax=None, fontsize=12)
# #     m.drawparallels([10, 15, 20, 25, 30, 35], color='k', textcolor='k', linewidth=1.5, zorder=None, dashes=[6, 1000], 
# #     	labels=[1, 0, 0, 1], labelstyle=None, fmt='%g', xoffset=None, yoffset=None, ax=None, latmax=None, fontsize=12)
# #     m.drawmapscale(-101, 8, -96, 8, 1000, barstyle='fancy', units='km', fontsize=8)
# #     m.drawcoastlines(linewidth=0.7, linestyle='solid', color='grey')
# #     m.drawcountries()
# #     m.shadedrelief()
# #     m.drawmapboundary()


# #     # ax = fig.add_subplot(spec[position[kk][0],position[kk][1]:position[kk][2]])
# #     # ax.text(0.05, 0.9, '('+string.ascii_lowercase[kk]+')', transform=ax.transAxes, 
# #     #         size=30)

# #     slp2D = pickle.load( open( dir_p[kk], "rb" ) )
# #     lats, lons = latlon_coords(slp2D)
    
# #     # Get the cartopy mapping object (use original data, rather than any processed data)
# #     cart_proj = get_cartopy(slp2D)

# #     # Set the GeoAxes to the projection used by WRF
# #     #ax = plt.axes(projection=cart_proj)
# #     ax = fig.add_subplot(spec[position[kk][0],position[kk][1]:position[kk][2]], projection=cart_proj)
# #     ax.stock_img()
    

# #     # Download and add the states and coastlines
# #     states = NaturalEarthFeature(category="cultural", scale="50m",
# # 	                             facecolor="none",
# # 	                             name="admin_1_states_provinces_shp")
# #     ax.add_feature(states, linewidth=.5, edgecolor="black")
# #     ax.coastlines('50m', linewidth=0.8)
# #     # Set the map bounds
# #     # ax.set_xlim(cartopy_xlim(slp2D))
# #     # ax.set_ylim(cartopy_ylim(slp2D))
# #     ax.set_extent(lat_log_bound[kk])


# #     # Show grid lines.
# #     gl = ax.gridlines(crs=crs.PlateCarree(), draw_labels=True,
# #                   linewidth=1.5, color='gray', alpha=0.8, linestyle=':')
# #     gl.xlabel_style = {'size': 15, 'color': 'k'}
# #     gl.ylabel_style = {'size': 15, 'color': 'k'}
# #     gl.xlabels_top = False
# #     gl.ylabels_right = False

# #     c=0

# #     ll=[]
# #     rr=[]
# #     for i in range(real1.shape[0]):
# #         for j in range(real1.shape[1]):
# #             if j<6:
# #                 ll.append(real1[i][j][0])
# #                 rr.append(real1[i][j][1])
# #         ax.plot( rr, ll, color = colors[c], marker=markers[c],linewidth=2, linestyle=patterns[c],\
# #                  markersize=sizes[c], transform=crs.PlateCarree())
# #         c+=1


# #     ll=[]
# #     rr=[]
# #     for i in range(simu1.shape[0]):
# #         for j in range(simu1.shape[1]):
# #             if j<6:
# #                 ll.append(simu1[i][j][0])
# #                 rr.append(simu1[i][j][1])
# #         ax.plot( rr, ll, color = colors[c], marker=markers[c],linewidth=2, linestyle=patterns[c],\
# #                  markersize=sizes[c], transform=crs.PlateCarree())
# #         c+=1
# #         ll=[]
# #         rr=[]
        
        
# #     for axis in ['top','bottom','left','right']:
# #         ax.spines[axis].set_linewidth(15)
# #     fig.legend(options, bbox_to_anchor=(0.87, 0.42), prop=font_wt, \
# #                frameon=False)
        
# #     plt.title(hurricanes[kk], {'size': 25}, **csfont)
# #     # plt.legend(['Real track','C0.0001', 'C0.01', 'C1', 'C100'],\
# #     #        loc = "upper right", prop={'size': 7})
# #     # plt.xlabel("Lon", fontsize=135)
# #     # plt.ylabel("Lat", fontsize=135)
# #     # plt.title(hurricanes[kk], {'size': 35}, **csfont)
# #     # plt.show()

# # plt.savefig('C:/Users/limgr/Desktop/'+hurricanes[kk]+'_wt.png', dpi=500)
# # plt.show()































# ###################
# # Plot error bars #
# ###################



# simu_error = []

# for kk in range(len(hurricanes)):

#     rows1=[]
#     Times1=[]
#     Times1=[]
#     values1=[]
#     real1_track=[]


#     with open(dir_wi[kk], mode='r') as csv_file:
#         csv_reader = csv.DictReader(csv_file)
#         line_count = 0
#         sim_count = 0
#         for row in csv_reader:
#             if line_count == 0:
#                 print(f'Column names are {", ".join(row)}')
#                 Times1.append(list(row.keys()))
#                 real1_track.append(list(row.values()))
#                 line_count += 1
#             else:
#                 rows1.append(row)
#                 values1.append(list(row.values()))
#                 line_count += 1
#         print('There is totally ',(line_count-1)*(len(row)),' data points')
#     simu1=np.array(values1, dtype=np.float32)
#     real1=np.array(real1_track, dtype=np.float32)
#     real1=real1*0.5144444
#     real1=real1
#     simu_error1=abs(simu1-real1[:,None])/real1[:,None]#/((line_count-3)*(len(row)))
#     print('absolute pressure error')
#     print(abs(simu1-real1[:,None]))
    
#     simu_error.append(simu_error1)






# par1_error_wi=np.zeros((4, 9))
# par2_error_wi=np.zeros((4, 9))
# par3_erro_wir=np.zeros((4, 9))
# par4_error_wi=np.zeros((4, 9))



# simu_error1 = simu_error[0]
# simu_error2 = simu_error[1]
# simu_error3 = simu_error[2]
# simu_error4 = simu_error[3]
# simu_error5 = simu_error[4]


# par1_error_wi=np.concatenate((simu_error1[0][0][0:5],simu_error2[0][0][:],\
#                            simu_error3[0][0][:],simu_error4[0][0][:-2],simu_error5[0][0][:]))
# par1_error_wi=par1_error_wi.flatten()
# par1_error_wi_mean=np.mean(par1_error_wi)
# par1_error_wi_std=np.std(par1_error_wi)
# par1_error_wi_low=np.percentile(par1_error_wi, 10)
# par1_error_wi_hgh=np.percentile(par1_error_wi, 90)


# par2_error_wi=np.concatenate((simu_error1[0][1][0:5],simu_error2[0][1][:],\
#                            simu_error3[0][1][:],simu_error4[0][1][:-2],simu_error5[0][1][:]))
# par2_error_wi=par2_error_wi.flatten()
# par2_error_wi_mean=np.mean(par2_error_wi)
# par2_error_wi_std=np.std(par2_error_wi)
# par2_error_wi_low=np.percentile(par2_error_wi, 10)
# par2_error_wi_hgh=np.percentile(par2_error_wi, 90)


# par3_error_wi=np.concatenate((simu_error1[0][2][0:5],simu_error2[0][2][:],\
#                            simu_error3[0][2][:],simu_error4[0][2][:-2],simu_error5[0][2][:]))
# par3_error_wi=par3_error_wi.flatten()
# par3_error_wi_mean=np.mean(par3_error_wi)
# par3_error_wi_std=np.std(par3_error_wi)
# par3_error_wi_low=np.percentile(par3_error_wi, 10)
# par3_error_wi_hgh=np.percentile(par3_error_wi, 90)



# par4_error_wi=np.concatenate((simu_error1[0][3][0:5],simu_error2[0][3][:],\
#                            simu_error3[0][3][:],simu_error4[0][3][:-2],simu_error5[0][3][:]))
# par4_error_wi=par4_error_wi.flatten()
# par4_error_wi_mean=np.mean(par4_error_wi)
# par4_error_wi_std=np.std(par4_error_wi)
# par4_error_wi_low=np.percentile(par4_error_wi, 10)
# par4_error_wi_hgh=np.percentile(par4_error_wi, 90)




# simu_error = []

# for kk in range(len(hurricanes)):
    
#     real1=[]
#     oussama1=[]
#     wrf1=[]
#     simu1=[]

#     with open( dir_wt[kk], 'r' ) as f :
#         data0 = f.read()
#         data = json.loads('[' + data0.replace('}{', '},{') + ']')
#     for i in range(0,len(data)):
#         data2 = list(data[i].values())
#         data3 = [e for sl in data2 for e in sl]
#         for j in range(len(data3)):
#             data3[j].pop(0)
#         if i==0:
#             real1.append(data3)
#         # elif i==1:
#         #     oussama1.append(data3)
#         # elif i==2:
#         #     wrf1.append(data3)
#         else:
#             simu1.append(data3)
#     real1 = np.array(real1, dtype=np.float32)
#     simu1 = np.array(simu1, dtype=np.float32)
#     real_r = np.radians(real1)
#     simu_r = np.radians(simu1)


#     term1=np.apply_along_axis(Calculate_Distance_Haversine1, 2, simu_r-real_r)
#     term2=np.apply_along_axis(Calculate_Distance_Haversine2, 2, simu_r)* \
#         np.apply_along_axis(Calculate_Distance_Haversine2, 2, real_r)* \
#         np.apply_along_axis(Calculate_Distance_Haversine3, 2, simu_r-real_r)
#     simu_error1=2*R*np.arcsin(np.sqrt(term1+term2))
#     simu_error.append(simu_error1)


# par1_error=np.zeros((4, 9))
# par2_error=np.zeros((4, 9))
# par3_error=np.zeros((4, 9))
# par4_error=np.zeros((4, 9))


# simu_error1 = simu_error[0]
# simu_error2 = simu_error[1]
# simu_error3 = simu_error[2]
# simu_error4 = simu_error[3]
# simu_error5 = simu_error[4]

# par1_error_wt=np.concatenate((simu_error1[0][0:5],\
#                            simu_error2[0][:],simu_error3[0][:],\
#                            simu_error4[0][:-2],simu_error5[0][:]))
# par1_error_wt=par1_error_wt.flatten()
# par1_error_wt_mean=np.mean(par1_error_wt)
# par1_error_wt_std=np.std(par1_error_wt)

# par2_error_wt=np.concatenate((simu_error1[1][0:5],\
#                            simu_error2[1][:],simu_error3[1][:],\
#                            simu_error4[1][:-2],simu_error5[1][:]))
# par2_error_wt=par2_error_wt.flatten()
# par2_error_wt_mean=np.mean(par2_error_wt)
# par2_error_wt_std=np.std(par2_error_wt)


# par3_error_wt=np.concatenate((simu_error1[2][0:5],\
#                            simu_error2[2][:],simu_error3[2][:],\
#                            simu_error4[2][:-2],simu_error5[2][:]))
# par3_error_wt=par3_error_wt.flatten()
# par3_error_wt_mean=np.mean(par3_error_wt)
# par3_error_wt_std=np.std(par3_error_wt)


# par4_error_wt=np.concatenate((simu_error1[3][0:5],\
#                            simu_error2[3][:],simu_error3[3][:],\
#                            simu_error4[3][:-2],simu_error5[3][:]))
# par4_error_wt=par4_error_wt.flatten()
# par4_error_wt_mean=np.mean(par4_error_wt)
# par4_error_wt_std=np.std(par4_error_wt)





# x_pos = np.arange(len(models))

# CTEs_wi = [par1_error_wi_mean,\
#         par2_error_wi_mean,par3_error_wi_mean,par4_error_wi_mean]
# errors_wi = [par1_error_wi_std,\
#           par2_error_wi_std,par3_error_wi_std,par4_error_wi_std]
# # percentile_10_wi = np.array([par1_error_wi_mean-par1_error_wi_low,\
# #           par4_error_wi_mean-par4_error_wi_low,par5_error_wi_mean-par5_error_wi_low, \
# #               par6_error_wi_mean-par6_error_wi_low,par7_error_wi_mean-par7_error_wi_low])
# # percentile_90_wi = np.array([par1_error_wi_hgh-par1_error_wi_mean,\
# #           par4_error_wi_hgh-par1_error_wi_mean,par5_error_wi_hgh-par5_error_wi_mean, \
# #               par6_error_wi_hgh-par6_error_wi_mean,par7_error_wi_hgh-par7_error_wi_mean])
# # err_wi = np.vstack((percentile_10_wi, percentile_90_wi))

# CTEs_wt = [par1_error_wt_mean,\
#         par2_error_wt_mean,par3_error_wt_mean,par4_error_wt_mean]
# errors_wt = [par1_error_wt_std,\
#           par2_error_wt_std,par3_error_wt_std,par4_error_wt_std]
# # percentile_10_wt = np.array([par1_error_wt_mean-par1_error_wt_low,\
# #           par4_error_wt_mean-par4_error_wt_low,par5_error_wt_mean-par5_error_wt_low, \
# #               par6_error_wt_mean-par6_error_wt_low,par7_error_wt_mean-par7_error_wt_low])
# # percentile_90_wt = np.array([par1_error_wt_hgh-par1_error_wt_mean,\
# #           par4_error_wt_hgh-par1_error_wt_mean,par5_error_wt_hgh-par5_error_wt_mean, \
# #               par6_error_wt_hgh-par6_error_wt_mean,par7_error_wt_hgh-par7_error_wt_mean])
# # err_wt = np.vstack((percentile_10_wt, percentile_90_wt))



# # fig, ax = plt.subplots(1, 2, figsize=(40, 8), sharex=True)
# fig = plt.figure(figsize=(8,5))
# spec = mpl.gridspec.GridSpec(ncols=8, nrows=5)


# ax = fig.add_subplot(spec[1:,0:4])
# ax.text(0.05, 0.9, '('+string.ascii_lowercase[0]+')', transform=ax.transAxes, 
#             size=15)
# bars = ax.bar(x_pos, CTEs_wi, yerr=errors_wi, align='center', \
#        color=['blue','blue','gray', 'red'], alpha=0.8,\
#        ecolor='k', capsize=10, edgecolor='k', linewidth=3)   
# for i in range(len(x_pos)):
#     bars[i].set(linestyle=list(linestyles.values())[i+1])    
# ax.set_ylabel(r'Normalized Intensity', **csfont, fontsize=15)
# vals = ax.get_yticks()
# ax.set_yticklabels(['{:,.0%}'.format(x) for x in vals])
# ax.set_xticks(x_pos)
# ax.set_xticklabels(models, **csfont, fontsize=10)
# #ax.set_title(r'COAWST', **csfont, fontsize=20)
# ax.yaxis.grid(True)



# ax = fig.add_subplot(spec[1:,4:])
# ax.text(0.05, 0.9, '('+string.ascii_lowercase[1]+')', transform=ax.transAxes, 
#             size=15)    
# bars = ax.bar(x_pos, CTEs_wt, yerr=errors_wt, align='center', \
#        color=['blue','blue','gray', 'red'], alpha=0.8,\
#        ecolor='k', capsize=10, edgecolor='k', linewidth=3) 
# for i in range(len(x_pos)):
#     bars[i].set(linestyle=list(linestyles.values())[i+1])
# ax.set_ylabel(r'Track Error (km)', **csfont, fontsize=15)
# vals = ax.get_yticks()
# ax.set_yticklabels(['{}'.format(x) for x in vals])
# ax.set_xticks(x_pos)
# ax.set_xticklabels(models, **csfont, fontsize=10)
# #ax.set_title(r'COAWST', **csfont, fontsize=20)
# ax.yaxis.grid(True)



# ax = fig.add_subplot(spec[0,0:])
# handles = [plt.Rectangle((0,0),1,1, facecolor=colors[i+1], \
#         linestyle=list(linestyles.values())[i+1], edgecolor = 'k', linewidth=1.5\
#             ) for i in range(len(models))]
# plt.legend(handles, models, ncol=4, bbox_to_anchor=(0.9, 0.8), prop=fontbar, \
#                frameon=False)
# ax.axes.xaxis.set_visible(False)
# ax.axes.yaxis.set_visible(False)
# ax.set_yticks([])
# ax.set_yticklabels([])
# ax.set_xticks([])
# ax.set_xticklabels([])
# for axis in ['top','bottom','left','right']:
#     ax.spines[axis].set_visible(False)



# # for i, v in enumerate(CTEs):
# #     ax.text(i, v+0.02, str(round(v, 3)), color='red', fontweight='bold')

# # Save the figure and show
# fig.autofmt_xdate()
# plt.tight_layout()
# #plt.savefig('wind_intensity_bar_plot.png')
# plt.savefig('C:/Users/limgr/Desktop/wi_wt_bar_plots.png', dpi=500)
# plt.show()


