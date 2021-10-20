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
colors = ['k','blue','cyan','gray', 'red', \
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

dir_znt_eye = ['C:/Users/limgr/Desktop/Katrina_ZNT_eye_8km.csv',\
       'C:/Users/limgr/Desktop/Maria_ZNT_eye_8km.csv',\
       'C:/Users/limgr/Desktop/Irma_ZNT_eye_8km.csv',\
       'C:/Users/limgr/Desktop/Dorian_ZNT_eye_8km.csv',\
       'C:/Users/limgr/Desktop/Lorenzo_ZNT_eye_8km.csv'] 
    
dir_znt_eyewall = ['C:/Users/limgr/Desktop/Katrina_ZNT_eyewall_8km.csv',\
       'C:/Users/limgr/Desktop/Maria_ZNT_eyewall_8km.csv',\
       'C:/Users/limgr/Desktop/Irma_ZNT_eyewall_8km.csv',\
       'C:/Users/limgr/Desktop/Dorian_ZNT_eyewall_8km.csv',\
       'C:/Users/limgr/Desktop/Lorenzo_ZNT_eyewall_8km.csv'] 


dir_wp = ['C:/Users/limgr/Desktop/Katrina_avg_speed_8km.csv', \
          'C:/Users/limgr/Desktop/Maria_avg_speed_8km.csv', \
          'C:/Users/limgr/Desktop/Irma_avg_speed_8km.csv', \
          'C:/Users/limgr/Desktop/Dorian_avg_speed_8km.csv', \
          'C:/Users/limgr/Desktop/Lorenzo_avg_speed_8km.csv'] 
    
lat_log_bound = [[-90.5, -84.5, 23, 29],\
                 [-74, -68, 19.5, 25.5],\
                 [-47, -39, 14, 22],\
                 [-76.5, -70.5, 23, 29],\
                 [-45.5, -39.5, 16.5, 22.5]]
    
    

def Calculate_Distance_Haversine1(x):
    return (np.sin(x[0]/2))**2
def Calculate_Distance_Haversine2(x):
    return np.cos(x[0])
def Calculate_Distance_Haversine3(x):
    return (np.sin(x[1]/2))**2








#########################################
# Plot averaged wind speed vs radius    #
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
                Times.append([x for x in list(row.keys()) if x != None])
                line_count += 1
            #print(row)
            # if line_count%2==0 and line_count>0:
            #     continue
            # else:
            #     rows.append(row)
            line_count += 1
            print('line ' + str(line_count))
            values.append([x for x in list(row.values()) if x != None])
                
            # rows.append(row)
            # line_count += 1
            # values.append(list(row.values()))

        print(f'Processed {line_count} lines.')
        
         
    valuess = []
    for line in range(len(values)):
        if line%2!=0:
            Times.append(values[line])
        else:
            valuess.append(values[line])
    
    for i in range(len(Times)):
        for j in range(len(Times[i])):
            Times[i][j]=float(Times[i][j])
            
    for i in range(len(valuess)):
        for j in range(len(valuess[i])):
            valuess[i][j]=float(valuess[i][j])
        
            
    Times0=Times
    
    print(len(Times0[2]))
    print(len(valuess[2]))
    print(position[kk])
    
    
    ax = fig.add_subplot(spec[position2[kk][0]:position2[kk][1],\
                              position2[kk][2]:position2[kk][3]])
    ax.text(0.05, 0.85, '('+string.ascii_lowercase[kk]+')', transform=ax.transAxes, 
            size=30, **csfont)


    for i in range(len(Times0)):
        
        print(len(Times0[i]))
        print(len(valuess[i]))
        if i==0:
            #tmp=[float(i)*0.5144444 for i in values[i]]
            tmp=[i for i in valuess[i]]
        # elif (i!=2 and i!=3):
        else:
            tmp=[i for i in valuess[i]]
        # else:
        #     continue
        
        if hurricanes[kk]=='Katrina':
            plt.plot( Times0[i][:-1], tmp[:-1], color = colors[c+1], \
                      linestyle=list(linestyles.values())[c+1],\
                  linewidth=5, markersize=sizes[c+1])
            plt.xticks(fontsize=25, **csfont)
            plt.yticks(fontsize=25, **csfont)
            plt.ylim([0, 80])
        elif hurricanes[kk]=='Dorian':
            plt.plot( Times0[i][:-1], tmp[:-1], color = colors[c+1], \
                      linestyle=list(linestyles.values())[c+1],\
                  linewidth=5, markersize=sizes[c+1])
            plt.xticks(fontsize=25, **csfont)
            plt.yticks(fontsize=25, **csfont)
            plt.ylim([0, 80])
        else:
            plt.plot( Times0[i][:-2], tmp[:-2], color = colors[c+1], \
                      linestyle=list(linestyles.values())[c+1],\
                  linewidth=5, markersize=sizes[c+1])
            plt.xticks(fontsize=25, **csfont)
            plt.yticks(fontsize=25, **csfont)
            plt.gca().yaxis.set_major_formatter(StrMethodFormatter('{x:,.0f}'))
            plt.ylim([0, 80])
        print('i=',str(i))

        c+=1
        
    for axis in ['top','bottom','left','right']:
        ax.spines[axis].set_linewidth(2)
    ax.tick_params(length=5, width=2)
    fig.legend(models, bbox_to_anchor=(0.87, 0.42), prop=font, \
                frameon=False)
    

    if kk==0 or kk==3:
        plt.ylabel(r'Wind speed (m/s)', **csfont, fontsize=35)
    if kk==2 or kk==3 or kk==4:
        plt.xlabel(r"Radius (km)", fontsize=30, **csfont)
    plt.title(hurricanes[kk], {'size': 30}, **csfont)

    
    
plt.savefig('C:/Users/limgr/Desktop/'+hurricanes[kk]+'_avg_wind.png', dpi=500)
plt.show()






