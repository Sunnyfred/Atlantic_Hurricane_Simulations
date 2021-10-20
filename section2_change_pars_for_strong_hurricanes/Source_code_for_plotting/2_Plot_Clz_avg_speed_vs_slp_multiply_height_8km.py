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


dir_wp1 = ['C:/Users/limgr/Desktop/Katrina_avg_speed_slp_10m_8km.csv', \
          'C:/Users/limgr/Desktop/Maria_avg_speed_slp_10m_8km.csv', \
          'C:/Users/limgr/Desktop/Irma_avg_speed_slp_10m_8km.csv', \
          'C:/Users/limgr/Desktop/Dorian_avg_speed_slp_10m_8km.csv', \
          'C:/Users/limgr/Desktop/Lorenzo_avg_speed_slp_10m_8km.csv'] 

dir_wp2 = ['C:/Users/limgr/Desktop/Katrina_avg_speed_slp_100m_8km.csv', \
          'C:/Users/limgr/Desktop/Maria_avg_speed_slp_100m_8km.csv', \
          'C:/Users/limgr/Desktop/Irma_avg_speed_slp_100m_8km.csv', \
          'C:/Users/limgr/Desktop/Dorian_avg_speed_slp_100m_8km.csv', \
          'C:/Users/limgr/Desktop/Lorenzo_avg_speed_slp_100m_8km.csv'] 
    
dir_wp3 = ['C:/Users/limgr/Desktop/Katrina_avg_speed_slp_500m_8km.csv', \
          'C:/Users/limgr/Desktop/Maria_avg_speed_slp_500m_8km.csv', \
          'C:/Users/limgr/Desktop/Irma_avg_speed_slp_500m_8km.csv', \
          'C:/Users/limgr/Desktop/Dorian_avg_speed_slp_500m_8km.csv', \
          'C:/Users/limgr/Desktop/Lorenzo_avg_speed_slp_500m_8km.csv'] 



dir_wp = [dir_wp1, dir_wp2, dir_wp3]

interpolat_height = [10, 100, 500] # interpolat_height in m



#########################################
# Plot averaged wind speed vs radius    #
#########################################

count = 0

for height in interpolat_height:
    
    
    
    
    fig = plt.figure(figsize=(20,13))
    spec = mpl.gridspec.GridSpec(ncols=23, nrows=9)

    for kk in range(len(hurricanes)):
    
        c=0
        rows=[]
        Times=[]
        Times=[]
        values=[]
        with open(dir_wp[count][kk], mode='r') as csv_file:
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
                tmp0 = []
                tmp0 = list(row.values())


                tmp = []
                if isinstance(tmp0[-1],list):
                    tmp = tmp0[-1]
                    tmp0.pop(-1)
                    for i in range(len(tmp)):
                        tmp0.append(tmp[i])
                print(tmp0)
            
                values.append([x for x in tmp0 if x != None])            
            
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
        ax.text(0.75, 0.85, str(height)+'m', transform=ax.transAxes, size=30, **csfont)

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
                plt.xticks(np.arange(min(Times0[i]), max(Times0[i])+1, 15))
                plt.yticks(fontsize=25, **csfont)
                plt.ylim([0, 80])
            elif hurricanes[kk]=='Dorian':
                plt.plot( Times0[i][:-1], tmp[:-1], color = colors[c+1], \
                      linestyle=list(linestyles.values())[c+1],\
                  linewidth=5, markersize=sizes[c+1])
                plt.xticks(fontsize=25, **csfont)
                plt.xticks(np.arange(min(Times0[i]), max(Times0[i])+1, 10))
                plt.yticks(fontsize=25, **csfont)
                plt.ylim([0, 80])
            else:
                plt.plot( Times0[i][:-2], tmp[:-2], color = colors[c+1], \
                      linestyle=list(linestyles.values())[c+1],\
                  linewidth=5, markersize=sizes[c+1])
                plt.xticks(fontsize=25, **csfont)
                plt.xticks(np.arange(min(Times0[i]), max(Times0[i])+1, 10))
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
            plt.xlabel(r"Sea-Level Pressure (hPa)", fontsize=30, **csfont)
        plt.title(hurricanes[kk], {'size': 30}, **csfont)

    
    
    plt.savefig('C:/Users/limgr/Desktop/'+hurricanes[kk]+'_avg_wind_vs_slp_'+str(height)+'m_8km.png', dpi=500)
    plt.show()


    count += 1



