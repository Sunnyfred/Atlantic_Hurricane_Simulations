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
font_wt = font_manager.FontProperties(family='Times New Roman', size=20)
colors = ['blue','cyan','gray', 'red','blue','cyan','gray', 'red', \
           'blue',  'cyan', 'lightcoral', 'turquoise','red','blue','green','pink']
patterns = ['-', '--','-.','-',':',':','--','--', ':','-', '--', ':','-', '--', ':',\
            '-.', '-.', '-.', ':', '--', '-']
markers = ['s','D','^','o','*','s','+','x','X','D','^','<','>','v'] 
sizes = [7, 7, 7, 7, 7, 3, 4, 3, 3, 3, 3, 3, 6,5,4,3,2,2]




options = [r"$Clz_{8km}$=0.0001",\
            r"$Clz_{8km}$=0.01",\
            r"$Clz_{8km}$=1",\
            r"$Clz_{8km}$=100"]

    
    
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
position2 = [[0,4,0,7],[0,4,8,15],[0,4,16,23],[5,9,0,7],[5,9,8,15],[5,9,16,23]]


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


dir_wp = ['C:/Users/limgr/Desktop/Katrina_wind_profiles_8km_1.csv',\
       'C:/Users/limgr/Desktop/Maria_wind_profiles_8km_1.csv',\
       'C:/Users/limgr/Desktop/Irma_wind_profiles_8km_1.csv',\
       'C:/Users/limgr/Desktop/Dorian_wind_profiles_8km_1.csv',\
       'C:/Users/limgr/Desktop/Lorenzo_wind_profiles_8km_1.csv']

   
    

def Calculate_Distance_Haversine1(x):
    return (np.sin(x[0]/2))**2
def Calculate_Distance_Haversine2(x):
    return np.cos(x[0])
def Calculate_Distance_Haversine3(x):
    return (np.sin(x[1]/2))**2









#########################################
# Plot normalized intensity time series #
#########################################


fig = plt.figure(figsize=(20,13))
spec = mpl.gridspec.GridSpec(ncols=23, nrows=9)

for kk in range(len(hurricanes)):
    
    c=0
    rows=[]
    Times=[]
    Times=[]
    values=[]
    with open(dir_wp[kk], mode='r') as csv_file:
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
    
    Times0=[float(x)/1000 for x in Times[0]]
    for i in range(len(values)):
        values[i] = [float(x) for x in values[i]]
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
        
        if c<=3:
            plt.plot( tmp, Times0, color = colors[c], \
                      linestyle=list(linestyles.values())[3],\
                  linewidth=5, markersize=sizes[c])
            plt.xticks(fontsize=25, **csfont)
            plt.yticks(fontsize=25, **csfont)
            if kk == 2:
                plt.ylim([1.5, 2.5])
            else:
                plt.ylim([0, 1])
        else:
            plt.plot( tmp, Times0, color = colors[c], \
                      linestyle=list(linestyles.values())[0],\
                  linewidth=5, markersize=sizes[c])
            plt.xticks(fontsize=25, **csfont)
            plt.yticks(fontsize=25, **csfont)
            plt.gca().yaxis.set_major_formatter(StrMethodFormatter('{x:,.0f}'))
            
            if kk == 2:
                plt.ylim([1.5, 2.5])
            else:
                plt.ylim([0, 1])

        c+=1
        
    for axis in ['top','bottom','left','right']:
        ax.spines[axis].set_linewidth(2)
    ax.tick_params(length=5, width=2)
    fig.legend(options, bbox_to_anchor=(0.87, 0.42), prop=font, \
                frameon=False)
    

    if kk==0 or kk==3:
        plt.ylabel(r'Altitude (km)', **csfont, fontsize=35)
    if kk==2 or kk==3 or kk==4:
        plt.xlabel(r"$u_r$ and $u_{\theta}$ (m/s)", fontsize=30, **csfont)
    plt.title(hurricanes[kk], {'size': 30}, **csfont)

    
   

ax = fig.add_subplot(spec[position2[5][0]:position2[5][1],\
                              position2[5][2]:position2[5][3]])    
ax.text(0.05, 0.9, r'$0.99 \leq \frac{slp}{slp_{max-wi}} \leq 1.01$', \
        transform=ax.transAxes, size=30, **csfont)    
ax.axes.xaxis.set_visible(False)
ax.axes.yaxis.set_visible(False)
ax.set_yticks([])
ax.set_yticklabels([])
ax.set_xticks([])
ax.set_xticklabels([])
for axis in ['top','bottom','left','right']:
    ax.spines[axis].set_visible(False)

plt.savefig('C:/Users/limgr/Desktop/'+hurricanes[kk]+'_wind_profiles.png', dpi=500)
plt.show()









