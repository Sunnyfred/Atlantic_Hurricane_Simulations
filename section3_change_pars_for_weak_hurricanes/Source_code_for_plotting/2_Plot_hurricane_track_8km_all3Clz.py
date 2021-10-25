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

Image.MAX_IMAGE_PIXELS = None
map_location = "C:/Users/limgr/.spyder-py3/Map"
os.environ["CARTOPY_USER_BACKGROUNDS"] = map_location




# List the colors that will be used for tracing the track.
csfont = {'fontname':'Times New Roman'}
font = font_manager.FontProperties(family='Times New Roman', size=30)
fontbar = font_manager.FontProperties(family='Times New Roman', size=12)
font_wt = font_manager.FontProperties(family='Times New Roman', size=25)
colors = ['k','blue','cyan','gray', 'red', \
           'blue',  'cyan', 'lightcoral', 'turquoise','red','blue','green','pink']
patterns = ['-', '--','-.','-',':',':','--','--', ':','-', '--', ':','-', '--', ':',\
            '-.', '-.', '-.', ':', '--', '-']
markers = ['s','D','^','o','*','s','+','x','X','D','^','<','>','v'] 
sizes = [7, 7, 7, 7, 7, 3, 4, 3, 3, 3, 3, 3, 6,5,4,3,2,2]




options1 = ["Best Track",\
            r"Clz$_\mathdefault{COAWST}$=0.0001",\
            r"Clz$_\mathdefault{COAWST}$=0.01",\
            r"Clz$_\mathdefault{COAWST}$=1",\
            r"Clz$_\mathdefault{COAWST}$=100"]

options2 = ["Best Track",\
            r"Clz$_\mathdefault{YSU-1}$=0.0001",\
            r"Clz$_\mathdefault{YSU-1}$=0.01",\
            r"Clz$_\mathdefault{YSU-1}$=1",\
            r"Clz$_\mathdefault{YSU-1}$=100"]
    
options3 = ["Best Track",\
            r"Clz$_\mathdefault{YSU-2}$=0.0001",\
            r"Clz$_\mathdefault{YSU-2}$=0.01",\
            r"Clz$_\mathdefault{YSU-2}$=1",\
            r"Clz$_\mathdefault{YSU-2}$=100"] 


     
hurricanes = ["Cristobal",\
            "Gert",\
            "Ike",\
            "Joaquin",\
            "Nicole"]
    
# subplot positions 
position = [[0,0,2],[0,2,4],[0,4,6],[1,0,2],[1,2,4],
            [2,0,2],[2,2,4],[2,4,6],[3,0,2],[3,2,4],
            [4,0,2],[4,2,4],[4,4,6],[5,0,2],[5,2,4]]
position2 = [[0,4,0,7],[0,4,7,14],[0,4,14,21],[5,9,0,7],[5,9,7,14],
             [10,14,0,7],[10,14,7,14],[10,14,14,21],[15,19,0,7],[15,19,7,14],
             [20,24,0,7],[20,24,7,14],[20,24,14,21],[25,29,0,7],[25,29,7,14]]

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




    
dir_wt1 = ['C:/Users/limgr/Desktop/1/Cristobal_track_8km.txt',\
       'C:/Users/limgr/Desktop/1/Gert_track_8km.txt',\
       'C:/Users/limgr/Desktop/1/Ike_track_8km.txt',\
       'C:/Users/limgr/Desktop/1/Joaquin_track_8km.txt',\
       'C:/Users/limgr/Desktop/1/Nicole_track_8km.txt']    

dir_p1 = ['C:/Users/limgr/Desktop/1/Cristobal_8km.p',\
       'C:/Users/limgr/Desktop/1/Gert_8km.p',\
       'C:/Users/limgr/Desktop/1/Ike_8km.p',\
       'C:/Users/limgr/Desktop/1/Joaquin_8km.p',\
       'C:/Users/limgr/Desktop/1/Nicole_8km.p']    

    
dir_wt2 = ['C:/Users/limgr/Desktop/2/Cristobal_track_8km.txt',\
       'C:/Users/limgr/Desktop/2/Gert_track_8km.txt',\
       'C:/Users/limgr/Desktop/2/Ike_track_8km.txt',\
       'C:/Users/limgr/Desktop/2/Joaquin_track_8km.txt',\
       'C:/Users/limgr/Desktop/2/Nicole_track_8km.txt']    

dir_p2 = ['C:/Users/limgr/Desktop/2/Cristobal_8km.p',\
       'C:/Users/limgr/Desktop/2/Gert_8km.p',\
       'C:/Users/limgr/Desktop/2/Ike_8km.p',\
       'C:/Users/limgr/Desktop/2/Joaquin_8km.p',\
       'C:/Users/limgr/Desktop/2/Nicole_8km.p']       
    
    
dir_wt3 = ['C:/Users/limgr/Desktop/3/Cristobal_track_8km.txt',\
       'C:/Users/limgr/Desktop/3/Gert_track_8km.txt',\
       'C:/Users/limgr/Desktop/3/Ike_track_8km.txt',\
       'C:/Users/limgr/Desktop/3/Joaquin_track_8km.txt',\
       'C:/Users/limgr/Desktop/3/Nicole_track_8km.txt']    

dir_p3 = ['C:/Users/limgr/Desktop/3/Cristobal_8km.p',\
       'C:/Users/limgr/Desktop/3/Gert_8km.p',\
       'C:/Users/limgr/Desktop/3/Ike_8km.p',\
       'C:/Users/limgr/Desktop/3/Joaquin_8km.p',\
       'C:/Users/limgr/Desktop/3/Nicole_8km.p']       
    
    

    
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
    
lat_log_bound = [[-78, -65, 23, 36],\
                  [-76, -57, 26, 44],\
                  [-92, -82, 20, 30],\
                  [-74, -59, 24, 39],\
                  [-65, -46, 32, 42]]  
    
    
    

def Calculate_Distance_Haversine1(x):
    return (np.sin(x[0]/2))**2
def Calculate_Distance_Haversine2(x):
    return np.cos(x[0])
def Calculate_Distance_Haversine3(x):
    return (np.sin(x[1]/2))**2








########################
# Plot hurricane track #
########################






# define the canvas size 
fig = plt.figure(figsize=(18,30))
spec = mpl.gridspec.GridSpec(ncols=21, nrows=29)





for kk in range(len(hurricanes)):
    
    if hurricanes[kk]=='Katrina':
        cons=6
    elif hurricanes[kk]=='Dorian':
        cons=8
    else:
        cons=10
    
    real1=[]
    oussama1=[]
    wrf1=[]
    simu1=[]

    with open( dir_wt1[kk], 'r' ) as f :
        data0 = f.read()
        data = json.loads('[' + data0.replace('}{', '},{') + ']')
    for i in range(0,len(data)):
        data2 = list(data[i].values())
        data3 = [e for sl in data2 for e in sl]
        for j in range(len(data3)):
            data3[j].pop(0)
        if i==0:
            real1.append(data3)
        # elif i==1:
        #     oussama1.append(data3)
        # elif i==2:
        #     wrf1.append(data3)
        else:
            simu1.append(data3)
    real1 = np.array(real1, dtype=np.float32)
    simu1 = np.array(simu1, dtype=np.float32)
    real_r = np.radians(real1)
    simu_r = np.radians(simu1)


    term1=np.apply_along_axis(Calculate_Distance_Haversine1, 2, simu_r-real_r)
    term2=np.apply_along_axis(Calculate_Distance_Haversine2, 2, simu_r)* \
        np.apply_along_axis(Calculate_Distance_Haversine2, 2, real_r)* \
        np.apply_along_axis(Calculate_Distance_Haversine3, 2, simu_r-real_r)
    simu_error1=2*R*np.arcsin(np.sqrt(term1+term2))




    # ax = fig.add_subplot(spec[position[kk][0],position[kk][1]:position[kk][2]])
    # ax.text(0.05, 0.9, '('+string.ascii_lowercase[kk]+')', transform=ax.transAxes, 
    #         size=30)

    slp2D = pickle.load( open( dir_p1[kk], "rb" ) )
    lats, lons = latlon_coords(slp2D)
    
    # Get the cartopy mapping object (use original data, rather than any processed data)
    cart_proj = get_cartopy(slp2D)

    # Set the GeoAxes to the projection used by WRF
    #ax = plt.axes(projection=cart_proj)
    ax = fig.add_subplot(spec[position2[kk][0]:position2[kk][1],\
                              position2[kk][2]:position2[kk][3]], projection=cart_proj)
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
    ax.set_extent(lat_log_bound[kk])
    ax.background_img(name='SR', resolution='high')

    # Show grid lines.
    gl = ax.gridlines(crs=crs.PlateCarree(), draw_labels=True,
                  linewidth=1.5, color='gray', alpha=0.8, linestyle=':')
    gl.xlabel_style = {'size': 25, 'color': 'k','fontname':'Times New Roman'}
    gl.ylabel_style = {'size': 25, 'color': 'k','fontname':'Times New Roman'}
    gl.xlabels_top = False
    gl.ylabels_right = False

    c=0

    ll=[]
    rr=[]
    for i in range(real1.shape[0]):
        for j in range(real1.shape[1]):
            if j<cons:
                ll.append(real1[i][j][0])
                rr.append(real1[i][j][1])
        ax.plot( rr, ll, color = colors[c], marker=markers[c],linewidth=2, \
                linestyle=list(linestyles.values())[c],\
                  markersize=sizes[c], transform=crs.PlateCarree())
        c+=1


    ll=[]
    rr=[]
    for i in range(simu1.shape[0]):
        for j in range(simu1.shape[1]):
            if j<cons:
                ll.append(simu1[i][j][0])
                rr.append(simu1[i][j][1])
        ax.plot( rr, ll, color = colors[c], marker=markers[c],linewidth=2, \
                linestyle=list(linestyles.values())[c],\
                  markersize=sizes[c], transform=crs.PlateCarree())
        c+=1
        ll=[]
        rr=[]
        
    if hurricanes[kk]=='Nicole':   
        for axis in ['top','bottom','left','right']:
            ax.spines[axis].set_linewidth(15)
        ax.legend(options1, bbox_to_anchor=(1., 1.), prop=font_wt, \
                frameon=False)

        
    plt.title(hurricanes[kk]+r' (COAWST)', {'size': 25}, **csfont)
    # plt.legend(['Real track','C0.0001', 'C0.01', 'C1', 'C100'],\
    #        loc = "upper right", prop={'size': 7})
    # plt.xlabel("Lon", fontsize=135)
    # plt.ylabel("Lat", fontsize=135)
    # plt.title(hurricanes[kk], {'size': 35}, **csfont)
    # plt.show()
    
    
    
    
    
    
    
    


for kk in range(len(hurricanes)):
    
    if hurricanes[kk]=='Katrina':
        cons=6
    elif hurricanes[kk]=='Dorian':
        cons=8
    else:
        cons=10
    
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
        # elif i==1:
        #     oussama1.append(data3)
        # elif i==2:
        #     wrf1.append(data3)
        else:
            simu1.append(data3)
    real1 = np.array(real1, dtype=np.float32)
    simu1 = np.array(simu1, dtype=np.float32)
    real_r = np.radians(real1)
    simu_r = np.radians(simu1)


    term1=np.apply_along_axis(Calculate_Distance_Haversine1, 2, simu_r-real_r)
    term2=np.apply_along_axis(Calculate_Distance_Haversine2, 2, simu_r)* \
        np.apply_along_axis(Calculate_Distance_Haversine2, 2, real_r)* \
        np.apply_along_axis(Calculate_Distance_Haversine3, 2, simu_r-real_r)
    simu_error1=2*R*np.arcsin(np.sqrt(term1+term2))




    # ax = fig.add_subplot(spec[position[kk][0],position[kk][1]:position[kk][2]])
    # ax.text(0.05, 0.9, '('+string.ascii_lowercase[kk]+')', transform=ax.transAxes, 
    #         size=30)

    slp2D = pickle.load( open( dir_p2[kk], "rb" ) )
    lats, lons = latlon_coords(slp2D)
    
    # Get the cartopy mapping object (use original data, rather than any processed data)
    cart_proj = get_cartopy(slp2D)

    # Set the GeoAxes to the projection used by WRF
    #ax = plt.axes(projection=cart_proj)
    ax = fig.add_subplot(spec[position2[kk+5][0]:position2[kk+5][1],\
                              position2[kk+5][2]:position2[kk+5][3]], projection=cart_proj)
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
    ax.set_extent(lat_log_bound[kk])
    ax.background_img(name='SR', resolution='high')

    # Show grid lines.
    gl = ax.gridlines(crs=crs.PlateCarree(), draw_labels=True,
                  linewidth=1.5, color='gray', alpha=0.8, linestyle=':')
    gl.xlabel_style = {'size': 25, 'color': 'k','fontname':'Times New Roman'}
    gl.ylabel_style = {'size': 25, 'color': 'k','fontname':'Times New Roman'}
    gl.xlabels_top = False
    gl.ylabels_right = False

    c=0

    ll=[]
    rr=[]
    for i in range(real1.shape[0]):
        for j in range(real1.shape[1]):
            if j<cons:
                ll.append(real1[i][j][0])
                rr.append(real1[i][j][1])
        ax.plot( rr, ll, color = colors[c], marker=markers[c],linewidth=2, \
                linestyle=list(linestyles.values())[c],\
                  markersize=sizes[c], transform=crs.PlateCarree())
        c+=1


    ll=[]
    rr=[]
    for i in range(simu1.shape[0]):
        for j in range(simu1.shape[1]):
            if j<cons:
                ll.append(simu1[i][j][0])
                rr.append(simu1[i][j][1])
        ax.plot( rr, ll, color = colors[c], marker=markers[c],linewidth=2, \
                linestyle=list(linestyles.values())[c],\
                  markersize=sizes[c], transform=crs.PlateCarree())
        c+=1
        ll=[]
        rr=[]
        
        
    if hurricanes[kk]=='Nicole':   
        for axis in ['top','bottom','left','right']:
            ax.spines[axis].set_linewidth(15)
        ax.legend(options2, bbox_to_anchor=(1., 1.), prop=font_wt, \
                frameon=False)

        
    plt.title(hurricanes[kk]+r' (YSU-1)', {'size': 25}, **csfont)
    # plt.legend(['Real track','C0.0001', 'C0.01', 'C1', 'C100'],\
    #        loc = "upper right", prop={'size': 7})
    # plt.xlabel("Lon", fontsize=135)
    # plt.ylabel("Lat", fontsize=135)
    # plt.title(hurricanes[kk], {'size': 35}, **csfont)
    # plt.show()    
    
    
    
    


for kk in range(len(hurricanes)):
    
    if hurricanes[kk]=='Katrina':
        cons=6
    elif hurricanes[kk]=='Dorian':
        cons=8
    else:
        cons=10
    
    real1=[]
    oussama1=[]
    wrf1=[]
    simu1=[]

    with open( dir_wt3[kk], 'r' ) as f :
        data0 = f.read()
        data = json.loads('[' + data0.replace('}{', '},{') + ']')
    for i in range(0,len(data)):
        data2 = list(data[i].values())
        data3 = [e for sl in data2 for e in sl]
        for j in range(len(data3)):
            data3[j].pop(0)
        if i==0:
            real1.append(data3)
        # elif i==1:
        #     oussama1.append(data3)
        # elif i==2:
        #     wrf1.append(data3)
        else:
            simu1.append(data3)
    real1 = np.array(real1, dtype=np.float32)
    simu1 = np.array(simu1, dtype=np.float32)
    real_r = np.radians(real1)
    simu_r = np.radians(simu1)


    term1=np.apply_along_axis(Calculate_Distance_Haversine1, 2, simu_r-real_r)
    term2=np.apply_along_axis(Calculate_Distance_Haversine2, 2, simu_r)* \
        np.apply_along_axis(Calculate_Distance_Haversine2, 2, real_r)* \
        np.apply_along_axis(Calculate_Distance_Haversine3, 2, simu_r-real_r)
    simu_error1=2*R*np.arcsin(np.sqrt(term1+term2))




    # ax = fig.add_subplot(spec[position[kk][0],position[kk][1]:position[kk][2]])
    # ax.text(0.05, 0.9, '('+string.ascii_lowercase[kk]+')', transform=ax.transAxes, 
    #         size=30)

    slp2D = pickle.load( open( dir_p3[kk], "rb" ) )
    lats, lons = latlon_coords(slp2D)
    
    # Get the cartopy mapping object (use original data, rather than any processed data)
    cart_proj = get_cartopy(slp2D)

    # Set the GeoAxes to the projection used by WRF
    #ax = plt.axes(projection=cart_proj)
    ax = fig.add_subplot(spec[position2[kk+10][0]:position2[kk+10][1],\
                              position2[kk+10][2]:position2[kk+10][3]], projection=cart_proj)
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
    ax.set_extent(lat_log_bound[kk])
    ax.background_img(name='SR', resolution='high')

    # Show grid lines.
    gl = ax.gridlines(crs=crs.PlateCarree(), draw_labels=True,
                  linewidth=1.5, color='gray', alpha=0.8, linestyle=':')
    gl.xlabel_style = {'size': 25, 'color': 'k','fontname':'Times New Roman'}
    gl.ylabel_style = {'size': 25, 'color': 'k','fontname':'Times New Roman'}
    gl.xlabels_top = False
    gl.ylabels_right = False

    c=0

    ll=[]
    rr=[]
    for i in range(real1.shape[0]):
        for j in range(real1.shape[1]):
            if j<cons:
                ll.append(real1[i][j][0])
                rr.append(real1[i][j][1])
        ax.plot( rr, ll, color = colors[c], marker=markers[c],linewidth=2, \
                linestyle=list(linestyles.values())[c],\
                  markersize=sizes[c], transform=crs.PlateCarree())
        c+=1


    ll=[]
    rr=[]
    for i in range(simu1.shape[0]):
        for j in range(simu1.shape[1]):
            if j<cons:
                ll.append(simu1[i][j][0])
                rr.append(simu1[i][j][1])
        ax.plot( rr, ll, color = colors[c], marker=markers[c],linewidth=2, \
                linestyle=list(linestyles.values())[c],\
                  markersize=sizes[c], transform=crs.PlateCarree())
        c+=1
        ll=[]
        rr=[]
        
        
    if hurricanes[kk]=='Nicole':   
        for axis in ['top','bottom','left','right']:
            ax.spines[axis].set_linewidth(15)
        ax.legend(options3, bbox_to_anchor=(1., 1.), prop=font_wt, \
                frameon=False)

        
    plt.title(hurricanes[kk]+r' (YSU-2)', {'size': 25}, **csfont)
    # plt.legend(['Real track','C0.0001', 'C0.01', 'C1', 'C100'],\
    #        loc = "upper right", prop={'size': 7})
    # plt.xlabel("Lon", fontsize=135)
    # plt.ylabel("Lat", fontsize=135)
    # plt.title(hurricanes[kk], {'size': 35}, **csfont)
    # plt.show()    
    
    
    
    
    

plt.savefig('C:/Users/limgr/Desktop/wt_all3Clz.png', dpi=500)
plt.show()












