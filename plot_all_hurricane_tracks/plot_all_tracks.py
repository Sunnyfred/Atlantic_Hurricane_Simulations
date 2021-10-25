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
                 cartopy_ylim, latlon_coords)
import cartopy
import os
from PIL import Image
from shapely.geometry.polygon import Polygon
from shapely import geometry
from collections import namedtuple
from shapely.geometry.polygon import LinearRing

Image.MAX_IMAGE_PIXELS = None
map_location = "C:/Users/limgr/.spyder-py3/Map"
os.environ["CARTOPY_USER_BACKGROUNDS"] = map_location




# List the colors that will be used for tracing the track.
csfont = {'fontname':'Times New Roman'}
font = font_manager.FontProperties(family='Times New Roman', size=30)
fontbar = font_manager.FontProperties(family='Times New Roman', size=12)
font_wt = font_manager.FontProperties(family='Times New Roman', size=15)
colors = ['k','blue','cyan','purple', 'red', \
           'blue',  'cyan', 'lightcoral', 'turquoise','red','blue','green','pink']
patterns = ['-', '--','-.','-',':',':','--','--', ':','-', '--', ':','-', '--', ':',\
            '-.', '-.', '-.', ':', '--', '-']
markers = ['s','D','^','o','*','s','+','x','X','D','^','<','>','v'] 
sizes = [5, 7, 7, 7, 7, 3, 4, 3, 3, 3, 3, 3, 6,5,4,3,2,2]




options = ["Katrina's Best Track",\
            "Maria's Best Track",\
            "Irma's Best Track",\
            "Dorian's Best Track",\
            "Lorenzo's Best Track"]

options2 = ["Cristobal's Best Track",\
            "Gert's Best Track",\
            "Ike's Best Track",\
            "Joaquin's Best Track",\
            "Nicole's Best Track"]




     
hurricanes = ["Katrina",\
            "Maria",\
            "Irma",\
            "Dorian",\
            "Lorenzo"]
    
hurricanes2 = ["Cristobal",\
            "Gert",\
            "Ike",\
            "Joaquin",\
            "Nicole"]

    
# subplot positions 
position = [[0,0,2],[0,2,4],[0,4,6],[1,0,2],[1,2,4]]
position2 = [[0,4,0,7],[0,4,8,15],[0,4,16,23],[5,9,0,7],[5,9,8,15]]
position = [[0,8,0,8],[9,17,0,8]]

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
    
    
dir_wt2 = ['C:/Users/limgr/Desktop/Cristobal_track_8km.txt',\
       'C:/Users/limgr/Desktop/Gert_track_8km.txt',\
       'C:/Users/limgr/Desktop/Ike_track_8km.txt',\
       'C:/Users/limgr/Desktop/Joaquin_track_8km.txt',\
       'C:/Users/limgr/Desktop/Nicole_track_8km.txt']    

    
dir_p2 = ['C:/Users/limgr/Desktop/Cristobal_8km.p',\
       'C:/Users/limgr/Desktop/Gert_8km.p',\
       'C:/Users/limgr/Desktop/Ike_8km.p',\
       'C:/Users/limgr/Desktop/Joaquin_8km.p',\
       'C:/Users/limgr/Desktop/Nicole_8km.p']        
    
    
    
lat_log_bound = [[-90.5, -84.5, 23, 29],\
                 [-74, -68, 19.5, 25.5],\
                 [-47, -39, 14, 22],\
                 [-76.5, -70.5, 23, 29],\
                 [-45.5, -39.5, 16.5, 22.5]]
    
lat_log_bound = [[-93, -83, 24, 34],\
                 [-77, -67, 19, 29],\
                 [-51, -39, 14, 22],\
                 [-80, -69, 23, 29],\
                 [-47, -40, 16.5, 25.5]]   
   
lat_log_bound = [[-91, -85, 24, 30],\
                 [-77, -67, 19, 29],\
                 [-51, -39, 14, 22],\
                 [-78, -70, 23, 29],\
                 [-47, -40, 16.5, 25.5]]       
  
lat_log_bound = [[-95, -35, 12, 31],\
                 [-77, -67, 19, 29],\
                 [-51, -39, 14, 22],\
                 [-78, -70, 23, 29],\
                 [-47, -40, 16.5, 25.5]]      
    
    
lat_log_bound2 = [[-95, -35, 21, 40],\
                 [-77, -67, 19, 29],\
                 [-51, -39, 14, 22],\
                 [-78, -70, 23, 29],\
                 [-47, -40, 16.5, 25.5]]  
    
    

strong_month_day = [['08/31','08/31','08/31','08/31',\
                    '09/01','09/01','09/01','09/01','09/02'],\
               ['09/22','09/22','09/22','09/22',\
                '09/23','09/23','09/23','09/23','09/24'],\
               ['09/02','09/02','09/02','09/02',\
                '09/03','09/03','09/03','09/03','09/04'],\
               ['08/28','08/28','08/28','08/28',\
                '08/29','08/29','08/29','08/29','08/30'],\
               ['09/27','09/27','09/27','09/27',\
                '09/28','09/28','09/28','09/28','09/29']]
    
    
    
    
    
# define box regions    
Region = namedtuple('Region',field_names=['region_name','lonmin','lonmax','latmin','latmax'])


# Ka_region = Region(region_name="all_region",
#     lonmin = -109,    lonmax = -69,    latmin = 12.5,    latmax = 37.5,
# )

# Ma_region = Region(region_name="all_region",
#     lonmin = -93,    lonmax = -53,    latmin = 12.5,    latmax = 37.5,
# )

# Ir_region = Region(
#     region_name="all_region",
#     lonmin = -67,    lonmax = -27,    latmin = 4.5,    latmax = 29.5,
# )

# Do_region = Region(
#     region_name="all_region",
#     lonmin = -90,    lonmax = -50,    latmin = 10.5,    latmax = 35.5,
# )

# Lo_region = Region(
#     region_name="all_region",
#     lonmin = -63.1,    lonmax = -23.1,    latmin = 8.850000000000001,    latmax = 33.85,
# )

# strong_region = [Ka_region, Ma_region, Ir_region, Do_region, Lo_region]




# Cr_region = Region(
#     region_name="all_region",
#     lonmin = -88,    lonmax = -48,    latmin = 19.6,    latmax = 44.6,
# )

# Ge_region = Region(
#     region_name="all_region",
#     lonmin = -84.75,    lonmax = -44.75,    latmin = 23.6,    latmax = 48.6,
# )

# Ik_region = Region(
#     region_name="all_region",
#     lonmin = -109.3,    lonmax = -69.3,    latmin = 13.350000000000001,    latmax = 38.35,
# )

# Jo_region = Region(
#     region_name="all_region",
#     lonmin = -81.05,    lonmax = -41.05,    latmin = 22.5,    latmax = 47.5,
# )

# Ni_region = Region(
#     region_name="all_region",
#     lonmin = -73.6,    lonmax = -33.6,    latmin = 24.549999999999997,    latmax = 49.55,
# )
    
# weak_region = [Cr_region, Ge_region, Ik_region, Jo_region, Ni_region]  



 
    

def Calculate_Distance_Haversine1(x):
    return (np.sin(x[0]/2))**2
def Calculate_Distance_Haversine2(x):
    return np.cos(x[0])
def Calculate_Distance_Haversine3(x):
    return (np.sin(x[1]/2))**2






def plot_polygon(ax, region, edgecolor, linestyle):

    geom = geometry.box(minx=region.lonmin,maxx=region.lonmax,miny=region.latmin,maxy=region.latmax)
    ax.add_geometries([geom], crs=cartopy.crs.PlateCarree(), \
                      alpha=1,linewidth=2, linestyle=linestyle,\
                      facecolor='none', edgecolor=edgecolor)
    return ax














































########################
# Plot hurricane track #
########################



real = []
real2 = []



for kk in range(len(hurricanes)):
    
    # if hurricanes[kk]=='Katrina':
    #     cons=6
    # elif hurricanes[kk]=='Dorian':
    #     cons=8
    # else:
    #     cons=10
    
    cons=10
    
    real1=[]
    oussama1=[]
    wrf1=[]
    simu1=[]

    with open( dir_wt[kk], 'r' ) as f :
        data0 = f.read()
        data = json.loads('[' + data0.replace('}{', '},{') + ']')
    for i in range(0,len(data)):
        data2 = list(data[i].values())
        data3 = [e for sl in data2 for e in sl]
        for j in range(len(data3)):
            data3[j].pop(0)
        if i==0:
            real1.append(data3)
        else:
            continue
    real1 = np.array(real1, dtype=np.float32)
    real.append(real1)
    # simu1 = np.array(simu1, dtype=np.float32)
    # real_r = np.radians(real1)
    # simu_r = np.radians(simu1)


    # term1=np.apply_along_axis(Calculate_Distance_Haversine1, 2, simu_r-real_r)
    # term2=np.apply_along_axis(Calculate_Distance_Haversine2, 2, simu_r)* \
    #     np.apply_along_axis(Calculate_Distance_Haversine2, 2, real_r)* \
    #     np.apply_along_axis(Calculate_Distance_Haversine3, 2, simu_r-real_r)
    # simu_error1=2*R*np.arcsin(np.sqrt(term1+term2))
    
    
    
    
    
for kk in range(len(hurricanes2)):
    
    
    real1=[]
    oussama1=[]
    wrf1=[]
    simu1=[]

    with open( dir_wt2[kk], 'r' ) as f :
        data0 = f.read()
        data = json.loads('[' + data0.replace('}{', '},{') + ']')
    for i in range(0,len(data)):
        data2 = list(data[i].values())
        data3 = [e for sl in data2 for e in sl]
        for j in range(len(data3)):
            data3[j].pop(0)
        if i==0:
            real1.append(data3)
        else:
            continue
    real1 = np.array(real1, dtype=np.float32)
    real2.append(real1)
    
    
    
    

for kk in range(1):
    
    # if hurricanes[kk]=='Katrina':
    #     cons=6
    # elif hurricanes[kk]=='Dorian':
    #     cons=8
    # else:
    #     cons=10
    



    # ax = fig.add_subplot(spec[position[kk][0],position[kk][1]:position[kk][2]])
    # ax.text(0.05, 0.9, '('+string.ascii_lowercase[kk]+')', transform=ax.transAxes, 
    #         size=30)

    slp2D = pickle.load( open( dir_p[kk], "rb" ) )
    lats, lons = latlon_coords(slp2D)
    
    # Get the cartopy mapping object (use original data, rather than any processed data)
    cart_proj = get_cartopy(slp2D)

    # Set the GeoAxes to the projection used by WRF
    #ax = plt.axes(projection=cart_proj)
    
    fig = plt.figure(figsize=(12,12))
    spec = mpl.gridspec.GridSpec(ncols=8, nrows=17)
    
    
    
    ax = fig.add_subplot(spec[position[0][0]:position[0][1],position[0][2]:position[0][3]], projection=cart_proj)
    # ax.stock_img()
    

    # Download and add the states and coastlines
    states = NaturalEarthFeature(category="cultural", scale="50m",
	                             facecolor="none",
	                             name="admin_1_states_provinces_shp")
    ax.add_feature(states, linewidth=.5, edgecolor="black")
    ax.coastlines('50m', linewidth=0.8)
    # Set the map bounds
    # ax.set_xlim(cartopy_xlim(slp2D))
    # ax.set_ylim(cartopy_ylim(slp2D))
    ax.set_extent(lat_log_bound[0])
    ax.background_img(name='SR', resolution='high')
    


 

    # Show grid lines.
    gl = ax.gridlines(crs=crs.PlateCarree(), draw_labels=True,
                  linewidth=1.5, color='gray', alpha=0.8, linestyle=':')
    gl.xlabel_style = {'size': 20, 'color': 'k','fontname':'Times New Roman'}
    gl.ylabel_style = {'size': 20, 'color': 'k','fontname':'Times New Roman'}
    gl.xlabels_top = False
    gl.ylabels_right = False

    c=0
    
    real_kk = []
    real_kk = real[0]

    ll=[]
    rr=[]
    for i in range(real_kk.shape[0]):
        for j in range(real_kk.shape[1]):
            if j<6:
                ll.append(real_kk[i][j][0])
                rr.append(real_kk[i][j][1])
        ax.plot( rr, ll, color = colors[c], marker=markers[0],linewidth=2, \
                linestyle=list(linestyles.values())[0],\
                  markersize=sizes[0], transform=crs.PlateCarree())
    for k in range(0, len(ll),3):
        ax.text( rr[k]+0.5, ll[k]+0.5, strong_month_day[c][k], color = colors[c], \
                 transform=crs.Geodetic(), fontsize='xx-large', **csfont)
    #plot_polygon(ax, strong_region[c], colors[c], list(linestyles.values())[0])
    c+=1

        


    real_kk = []
    real_kk = real[1]
    ll=[]
    rr=[]
    for i in range(real_kk.shape[0]):
        for j in range(real_kk.shape[1]):
            if j<cons:
                ll.append(real_kk[i][j][0])
                rr.append(real_kk[i][j][1])
        ax.plot( rr, ll, color = colors[c], marker=markers[0],linewidth=2, \
                linestyle=list(linestyles.values())[0],\
                  markersize=sizes[0], transform=crs.PlateCarree())
    for k in range(0, len(ll),3):
        ax.text( rr[k]+0.5, ll[k]+0.5, strong_month_day[c][k], color = colors[c], \
                 transform=crs.Geodetic(), fontsize='xx-large', **csfont)
    c+=1
        
    real_kk = []
    real_kk = real[2]
    ll=[]
    rr=[]
    for i in range(real_kk.shape[0]):
        for j in range(real_kk.shape[1]):
            if j<cons:
                ll.append(real_kk[i][j][0])
                rr.append(real_kk[i][j][1])
        ax.plot( rr, ll, color = colors[c], marker=markers[0],linewidth=2, \
                linestyle=list(linestyles.values())[0],\
                  markersize=sizes[0], transform=crs.PlateCarree())
    #plot_polygon(ax, strong_region[c], colors[c], list(linestyles.values())[0])
    for k in range(0, len(ll),3):
        ax.text( rr[k], ll[k]+1, strong_month_day[c][k], color = colors[c], \
                 transform=crs.Geodetic(), fontsize='xx-large', **csfont)
    c+=1   
        
        
    real_kk = []
    real_kk = real[3]
    ll=[]
    rr=[]
    for i in range(real_kk.shape[0]):
        for j in range(real_kk.shape[1]):
            if j<7:
                ll.append(real_kk[i][j][0])
                rr.append(real_kk[i][j][1])
        ax.plot( rr, ll, color = colors[c], marker=markers[0],linewidth=2, \
                linestyle=list(linestyles.values())[0],\
                  markersize=sizes[0], transform=crs.PlateCarree())
    #plot_polygon(ax, strong_region[c], colors[c], list(linestyles.values())[0])
    for k in range(0, len(ll),4):
        print(c)
        ax.text( rr[k], ll[k]+1.5, strong_month_day[c][k], color = colors[c], \
                 transform=crs.Geodetic(), fontsize='xx-large', **csfont)
    c+=1
        
        
    real_kk = []
    real_kk = real[4]
    ll=[]
    rr=[]
    for i in range(real_kk.shape[0]):
        for j in range(real_kk.shape[1]):
            if j<cons:
                ll.append(real_kk[i][j][0])
                rr.append(real_kk[i][j][1])
        ax.plot( rr, ll, color = colors[c], marker=markers[0],linewidth=2, \
                linestyle=list(linestyles.values())[0],\
                  markersize=sizes[0], transform=crs.PlateCarree())
    #plot_polygon(ax, strong_region[c], colors[c], list(linestyles.values())[0])
    for k in range(0, len(ll),3):
        ax.text( rr[k]+0.5, ll[k]+1, strong_month_day[c][k], color = colors[c], \
                 transform=crs.Geodetic(), fontsize='xx-large', **csfont)
    c+=1
        
        

        
        
        
        
    for axis in ['top','bottom','left','right']:
        ax.spines[axis].set_linewidth(15)
    fig.legend(options, bbox_to_anchor=(0.9, 0.87), prop=font_wt, \
                frameon=False)
        
    plt.title('Strong Hurricanes', {'size': 25}, **csfont)
    # plt.legend(['Real track','C0.0001', 'C0.01', 'C1', 'C100'],\
    #        loc = "upper right", prop={'size': 7})
    # plt.xlabel("Lon", fontsize=135)
    # plt.ylabel("Lat", fontsize=135)
    # plt.title(hurricanes[kk], {'size': 35}, **csfont)
    # plt.show()
    
    
    
    
    
    
    
    
    
    
    ax = fig.add_subplot(spec[position[1][0]:position[1][1],position[1][2]:position[1][3]], projection=cart_proj)
    # ax.stock_img()
    

    # Download and add the states and coastlines
    states = NaturalEarthFeature(category="cultural", scale="50m",
	                             facecolor="none",
	                             name="admin_1_states_provinces_shp")
    ax.add_feature(states, linewidth=.5, edgecolor="black")
    ax.coastlines('50m', linewidth=0.8)
    # Set the map bounds
    # ax.set_xlim(cartopy_xlim(slp2D))
    # ax.set_ylim(cartopy_ylim(slp2D))
    ax.set_extent(lat_log_bound2[0])
    ax.background_img(name='SR', resolution='high')

    # Show grid lines.
    gl = ax.gridlines(crs=crs.PlateCarree(), draw_labels=True,
                  linewidth=1.5, color='gray', alpha=0.8, linestyle=':')
    gl.xlabel_style = {'size': 20, 'color': 'k','fontname':'Times New Roman'}
    gl.ylabel_style = {'size': 20, 'color': 'k','fontname':'Times New Roman'}
    gl.xlabels_top = False
    gl.ylabels_right = False

    c=0
    

        
        
        
    real_kk = []
    real_kk = real2[0]

    ll=[]
    rr=[]
    for i in range(real_kk.shape[0]):
        for j in range(real_kk.shape[1]):
            if j<cons:
                ll.append(real_kk[i][j][0])
                rr.append(real_kk[i][j][1])
        ax.plot( rr, ll, color = colors[c], marker=markers[0],linewidth=2, \
                linestyle=list(linestyles.values())[3],\
                  markersize=sizes[0], transform=crs.PlateCarree())
    #plot_polygon(ax, weak_region[c], colors[c], list(linestyles.values())[3])
    for k in range(0, len(ll),3):
        ax.text( rr[k]-4, ll[k], strong_month_day[c][k], color = colors[c], \
                 transform=crs.Geodetic(), fontsize='xx-large', **csfont)
    c+=1

    real_kk = []
    real_kk = real2[1]
    ll=[]
    rr=[]
    for i in range(real_kk.shape[0]):
        for j in range(real_kk.shape[1]):
            if j<cons:
                ll.append(real_kk[i][j][0])
                rr.append(real_kk[i][j][1])
        ax.plot( rr, ll, color = colors[c], marker=markers[0],linewidth=2, \
                linestyle=list(linestyles.values())[3],\
                  markersize=sizes[0], transform=crs.PlateCarree())
    #plot_polygon(ax, weak_region[c], colors[c], list(linestyles.values())[3])
    for k in range(0, len(ll),3):
        ax.text( rr[k]+1.5, ll[k], strong_month_day[c][k], color = colors[c], \
                 transform=crs.Geodetic(), fontsize='xx-large', **csfont)
    c+=1
        
    real_kk = []
    real_kk = real2[2]
    ll=[]
    rr=[]
    for i in range(real_kk.shape[0]):
        for j in range(real_kk.shape[1]):
            if j<cons:
                ll.append(real_kk[i][j][0])
                rr.append(real_kk[i][j][1])
        ax.plot( rr, ll, color = colors[c], marker=markers[0],linewidth=2, \
                linestyle=list(linestyles.values())[3],\
                  markersize=sizes[0], transform=crs.PlateCarree())
    #plot_polygon(ax, weak_region[c], colors[c], list(linestyles.values())[3])
    for k in range(0, len(ll),3):
        ax.text( rr[k]+0.5, ll[k]+0.5, strong_month_day[c][k], color = colors[c], \
                 transform=crs.Geodetic(), fontsize='xx-large', **csfont)
    c+=1   
        
        
    real_kk = []
    real_kk = real2[3]
    ll=[]
    rr=[]
    for i in range(real_kk.shape[0]):
        for j in range(real_kk.shape[1]):
            if j<cons:
                ll.append(real_kk[i][j][0])
                rr.append(real_kk[i][j][1])
        ax.plot( rr, ll, color = colors[c], marker=markers[0],linewidth=2, \
                linestyle=list(linestyles.values())[3],\
                  markersize=sizes[0], transform=crs.PlateCarree())
    #plot_polygon(ax, weak_region[c], colors[c], list(linestyles.values())[3])
    for k in range(0, len(ll),3):
        ax.text( rr[k]+1, ll[k]+0.5, strong_month_day[c][k], color = colors[c], \
                 transform=crs.Geodetic(), fontsize='xx-large', **csfont)
    c+=1
        
        
    real_kk = []
    real_kk = real2[4]
    ll=[]
    rr=[]
    for i in range(real_kk.shape[0]):
        for j in range(real_kk.shape[1]):
            if j<cons:
                ll.append(real_kk[i][j][0])
                rr.append(real_kk[i][j][1])
        ax.plot( rr, ll, color = colors[c], marker=markers[0],linewidth=2, \
                linestyle=list(linestyles.values())[3],\
                  markersize=sizes[0], transform=crs.PlateCarree())
    #plot_polygon(ax, weak_region[c], colors[c], list(linestyles.values())[3])
    for k in range(0, len(ll),3):
        ax.text( rr[k]+1, ll[k]-1, strong_month_day[c][k], color = colors[c], \
                 transform=crs.Geodetic(), fontsize='xx-large', **csfont)
    c+=1        
        
        
        
        
        
        
        
    for axis in ['top','bottom','left','right']:
        ax.spines[axis].set_linewidth(15)
    ax.legend(options2, bbox_to_anchor=(1, 0.4), prop=font_wt, \
                frameon=False)
        
    plt.title('Weak Hurricanes', {'size': 25}, **csfont)
    # plt.legend(['Real track','C0.0001', 'C0.01', 'C1', 'C100'],\
    #        loc = "upper right", prop={'size': 7})
    # plt.xlabel("Lon", fontsize=135)
    # plt.ylabel("Lat", fontsize=135)
    # plt.title(hurricanes[kk], {'size': 35}, **csfont)
    # plt.show()    
    
    
    
    
    
    
    
    
    
    
    
    

plt.savefig('C:/Users/limgr/Desktop/'+hurricanes[kk]+'_wt.png', dpi=500)
plt.show()


















