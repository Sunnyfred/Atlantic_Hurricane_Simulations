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
font = font_manager.FontProperties(family='Times New Roman', size=25)
fontbar = font_manager.FontProperties(family='Times New Roman', size=12)
font_wt = font_manager.FontProperties(family='Times New Roman', size=20)
colors = ['k','blue','cyan','gray', 'red', \
           'blue',  'cyan', 'lightcoral', 'turquoise','red','blue','green','pink']

patterns = ['-', '--','-.','-',':',':','--','--', ':','-', '--', ':','-', '--', ':',\
            '-.', '-.', '-.', ':', '--', '-']
markers = ['s','D','^','o','*','>','+','x','X','D','^','<','>','v'] 
sizes = [7, 7, 7, 7, 7, 7, 4, 3, 3, 3, 3, 3, 6,5,4,3,2,2]




options = ["Best Track",\
            "Clz=0.0001",\
            "Clz=0.01",\
            "Clz=1",\
            "Clz=100"]

    
    
models = ["Clz = 0.0001",\
            "Clz = 0.01",\
            "Clz = 1",\
            "Clz = 100"]


     
hurricanes = ["Katrina",\
            "Maria",\
            "Irma",\
            "Dorian",\
            "Lorenzo"]
    
# subplot positions 
position = [[0,0,2],[0,2,4],[0,4,6],[1,0,2],[1,2,4]]
position2 = [[0,4,0,7],[0,4,8,15],[0,4,16,23],[5,9,0,7],[5,9,8,15]]


linestyles = OrderedDict(
    [('solid',               (0, ())),
     ('dashdotted',          (0, (3, 3, 1, 3))),
     ('dashdotdotted',       (0, (3, 2, 1, 2, 1, 2))),
     ('dashed',              (0, (3, 3))),
     ('dotted',              (0, (1, 3))),
     ('dashed',              (0, (3, 3))),
     ('loosely dashed',      (0, (5, 5))),
     ('loosely dotted',      (0, (1, 10))),
     ('densely dotted',      (0, (1, 1))),
     ('densely dashed',      (0, (5, 1))),
     ('loosely dashdotted',  (0, (3, 10, 1, 10))),
     ('densely dashdotted',  (0, (3, 1, 1, 1))),
     ('loosely dashdotdotted', (0, (3, 10, 1, 10, 1, 10))),
     ('densely dashdotdotted', (0, (3, 1, 1, 1, 1, 1)))])



R = 6373.0 # approxiamte radius of earth in km




# folder for wi and wt files


    
dir_znt_eyewall_bandavg = ['C:/Users/limgr/Desktop/Katrina_ZNT_eyewallbandavg_8km.csv',\
       'C:/Users/limgr/Desktop/Maria_ZNT_eyewallbandavg_8km.csv',\
       'C:/Users/limgr/Desktop/Irma_ZNT_eyewallbandavg_8km.csv',\
       'C:/Users/limgr/Desktop/Dorian_ZNT_eyewallbandavg_8km.csv',\
       'C:/Users/limgr/Desktop/Lorenzo_ZNT_eyewallbandavg_8km.csv'] 
    
       
    

def Calculate_Distance_Haversine1(x):
    return (np.sin(x[0]/2))**2
def Calculate_Distance_Haversine2(x):
    return np.cos(x[0])
def Calculate_Distance_Haversine3(x):
    return (np.sin(x[1]/2))**2















########################
# Plot ZNT time series #
########################


fig = plt.figure(figsize=(20,13))
spec = mpl.gridspec.GridSpec(ncols=23, nrows=9)


for kk in range(len(hurricanes)):
    
    c=0
    rows=[]
    Times=[]
    Times=[]
    values=[]
    with open(dir_znt_eyewall_bandavg[kk], mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                Times.append(list(row.keys()))
                line_count += 1
            #print(row)
            rows.append(row)
            values.append(list(row.values()))
            line_count += 1
        print(f'Processed {line_count} lines.')
    
    Times0=Times[0]
    print(Times0)
    print(values[0])
    print(position[kk])
    
    
    ax = fig.add_subplot(spec[position2[kk][0]:position2[kk][1],\
                              position2[kk][2]:position2[kk][3]])
    ax.text(0.05, 0.85, '('+string.ascii_lowercase[kk]+')', transform=ax.transAxes, 
            size=30, **csfont)


    for i in range(0,line_count-1):
        if i==0:
            #tmp=[float(i)*0.5144444 for i in values[i]]
            tmp=[float(i) for i in values[i]]
        # elif (i!=2 and i!=3):
        else:
            tmp=[float(i) for i in values[i]]
        # else:
        #     continue
        
        if hurricanes[kk]=='Katrina':
            plt.plot( Times0[:5], tmp[:5], color = colors[c+1], \
                      linestyle=list(linestyles.values())[i+1],\
                  linewidth=5, markersize=sizes[c+1])
            plt.xticks(fontsize=25, **csfont)
            plt.yticks(fontsize=25, **csfont)
            plt.ylim([1e-11, 1])
            plt.yscale('log')
        elif hurricanes[kk]=='Dorian':
            plt.plot( Times0[:-2], tmp[:-2], color = colors[c+1], \
                      linestyle=list(linestyles.values())[i+1],\
                  linewidth=5, markersize=sizes[c+1])
            plt.xticks(fontsize=25, **csfont)
            plt.yticks(fontsize=25, **csfont)
            plt.ylim([1e-11, 1])
            plt.yscale('log')
        else:
            plt.plot( Times0, tmp, color = colors[c+1], \
                      linestyle=list(linestyles.values())[i+1],\
                  linewidth=5, markersize=sizes[c+1])
            plt.xticks(fontsize=25, **csfont)
            plt.yticks(fontsize=25, **csfont)
            plt.gca().yaxis.set_major_formatter(StrMethodFormatter('{x:,.0f}'))
            plt.ylim([1e-11, 1])
            plt.yscale('log')

        c+=1
        
    for axis in ['top','bottom','left','right']:
        ax.spines[axis].set_linewidth(2)
    ax.tick_params(length=5, width=2)
    fig.legend(models, bbox_to_anchor=(0.87, 0.42), prop=font, \
                frameon=False)
    

    if kk==0 or kk==3:
        plt.ylabel(r'$Z_0$ (m)', **csfont, fontsize=30)
    if kk==2 or kk==3 or kk==4:
        plt.xlabel(r"Time Series (hr)", fontsize=30, **csfont)
    plt.title(hurricanes[kk], {'size': 30}, **csfont)

    
    
plt.savefig('C:/Users/limgr/Desktop/'+hurricanes[kk]+'_ZNT_eyewall_bandavg.png', dpi=500)
plt.show()


















