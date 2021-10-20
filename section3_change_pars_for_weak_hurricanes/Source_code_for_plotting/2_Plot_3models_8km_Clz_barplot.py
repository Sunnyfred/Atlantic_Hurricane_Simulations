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


     
hurricanes = ["Cristobal",\
            "Gert",\
            "Ike",\
            "Joaquin",\
            "Nicole"]

    
# subplot positions 
position = [[0,0,2],[0,2,4],[0,4,6],[1,0,2],[1,2,4]]
position2 = [[0,4,0,5],[0,4,6,11],[0,4,12,17],[5,9,0,5],[5,9,6,11]]


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


dir_wi1 = ['C:/Users/limgr/Desktop/1/Cristobal_wind_intensity_8km.csv',\
       'C:/Users/limgr/Desktop/1/Gert_wind_intensity_8km.csv',\
       'C:/Users/limgr/Desktop/1/Ike_wind_intensity_8km.csv',\
       'C:/Users/limgr/Desktop/1/Joaquin_wind_intensity_8km.csv',\
       'C:/Users/limgr/Desktop/1/Nicole_wind_intensity_8km.csv']

    
dir_wt1 = ['C:/Users/limgr/Desktop/1/Cristobal_track_8km.txt',\
       'C:/Users/limgr/Desktop/1/Gert_track_8km.txt',\
       'C:/Users/limgr/Desktop/1/Ike_track_8km.txt',\
       'C:/Users/limgr/Desktop/1/Joaquin_track_8km.txt',\
       'C:/Users/limgr/Desktop/1/Nicole_track_8km.txt']    


    

    
dir_wi2 = ['C:/Users/limgr/Desktop/2/Cristobal_wind_intensity_8km.csv',\
       'C:/Users/limgr/Desktop/2/Gert_wind_intensity_8km.csv',\
       'C:/Users/limgr/Desktop/2/Ike_wind_intensity_8km.csv',\
       'C:/Users/limgr/Desktop/2/Joaquin_wind_intensity_8km.csv',\
       'C:/Users/limgr/Desktop/2/Nicole_wind_intensity_8km.csv']

    
dir_wt2 = ['C:/Users/limgr/Desktop/2/Cristobal_track_8km.txt',\
       'C:/Users/limgr/Desktop/2/Gert_track_8km.txt',\
       'C:/Users/limgr/Desktop/2/Ike_track_8km.txt',\
       'C:/Users/limgr/Desktop/2/Joaquin_track_8km.txt',\
       'C:/Users/limgr/Desktop/2/Nicole_track_8km.txt']    




dir_wi3 = ['C:/Users/limgr/Desktop/3/Cristobal_wind_intensity_8km.csv',\
       'C:/Users/limgr/Desktop/3/Gert_wind_intensity_8km.csv',\
       'C:/Users/limgr/Desktop/3/Ike_wind_intensity_8km.csv',\
       'C:/Users/limgr/Desktop/3/Joaquin_wind_intensity_8km.csv',\
       'C:/Users/limgr/Desktop/3/Nicole_wind_intensity_8km.csv']

    
dir_wt3 = ['C:/Users/limgr/Desktop/3/Cristobal_track_8km.txt',\
       'C:/Users/limgr/Desktop/3/Gert_track_8km.txt',\
       'C:/Users/limgr/Desktop/3/Ike_track_8km.txt',\
       'C:/Users/limgr/Desktop/3/Joaquin_track_8km.txt',\
       'C:/Users/limgr/Desktop/3/Nicole_track_8km.txt']        
    
lat_log_bound = [[-90.5, -84.5, 23, 29],\
                 [-74, -68, 19.5, 25.5],\
                 [-47, -39, 14, 22],\
                 [-76.5, -70.5, 23, 29],\
                 [-45.5, -39.5, 16.5, 22.5]]
    
    
dir_wi = [dir_wi1, dir_wi2, dir_wi3]
dir_wt = [dir_wt1, dir_wt2, dir_wt3]   
    
    

def Calculate_Distance_Haversine1(x):
    return (np.sin(x[0]/2))**2
def Calculate_Distance_Haversine2(x):
    return np.cos(x[0])
def Calculate_Distance_Haversine3(x):
    return (np.sin(x[1]/2))**2




















###################
# Plot error bars #
###################

par1_error_wi_mean_all=[]
par1_error_wi_std_all=[]
par2_error_wi_mean_all=[]
par2_error_wi_std_all=[]
par3_error_wi_mean_all=[]
par3_error_wi_std_all=[]
par4_error_wi_mean_all=[]
par4_error_wi_std_all=[]




par1_error_wi_hgh_all=[]
par2_error_wi_hgh_all=[]
par3_error_wi_hgh_all=[]
par4_error_wi_hgh_all=[]


par1_error_wi_low_all=[]
par2_error_wi_low_all=[]
par3_error_wi_low_all=[]
par4_error_wi_low_all=[]



for dirx in dir_wi:
    

    simu_error = []

    for kk in range(len(hurricanes)):

        rows1=[]
        Times1=[]
        Times1=[]
        values1=[]
        real1_track=[]


        with open(dirx[kk], mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            line_count = 0
            sim_count = 0
            for row in csv_reader:
                if line_count == 0:
                    print(f'Column names are {", ".join(row)}')
                    Times1.append(list(row.keys()))
                    real1_track.append(list(row.values()))
                    line_count += 1
                else:
                    rows1.append(row)
                    values1.append(list(row.values()))
                    line_count += 1
            print('There is totally ',(line_count-1)*(len(row)),' data points')
        simu1=np.array(values1, dtype=np.float32)
        real1=np.array(real1_track, dtype=np.float32)
        real1=real1*0.5144444
        real1=real1
        simu_error1=abs(simu1-real1[:,None])/real1[:,None]#/((line_count-3)*(len(row)))
        print('absolute pressure error')
        print(abs(simu1-real1[:,None]))
    
        simu_error.append(simu_error1)






    par1_error_wi=np.zeros((4, 9))
    par2_error_wi=np.zeros((4, 9))
    par3_erro_wir=np.zeros((4, 9))
    par4_error_wi=np.zeros((4, 9))



    simu_error1 = simu_error[0]
    simu_error2 = simu_error[1]
    simu_error3 = simu_error[2]
    simu_error4 = simu_error[3]
    simu_error5 = simu_error[4]


    par1_error_wi=np.concatenate((simu_error1[0][0][0:5],simu_error2[0][0][:],\
                            simu_error3[0][0][:],simu_error4[0][0][:-2],simu_error5[0][0][:]))
    par1_error_wi=par1_error_wi.flatten()
    par1_error_wi_mean=np.mean(par1_error_wi)
    par1_error_wi_std=np.std(par1_error_wi)
    par1_error_wi_low=np.percentile(par1_error_wi, 20)
    par1_error_wi_hgh=np.percentile(par1_error_wi, 80)


    par2_error_wi=np.concatenate((simu_error1[0][1][0:5],simu_error2[0][1][:],\
                            simu_error3[0][1][:],simu_error4[0][1][:-2],simu_error5[0][1][:]))
    par2_error_wi=par2_error_wi.flatten()
    par2_error_wi_mean=np.mean(par2_error_wi)
    par2_error_wi_std=np.std(par2_error_wi)
    par2_error_wi_low=np.percentile(par2_error_wi, 20)
    par2_error_wi_hgh=np.percentile(par2_error_wi, 80)


    par3_error_wi=np.concatenate((simu_error1[0][2][0:5],simu_error2[0][2][:],\
                            simu_error3[0][2][:],simu_error4[0][2][:-2],simu_error5[0][2][:]))
    par3_error_wi=par3_error_wi.flatten()
    par3_error_wi_mean=np.mean(par3_error_wi)
    par3_error_wi_std=np.std(par3_error_wi)
    par3_error_wi_low=np.percentile(par3_error_wi, 20)
    par3_error_wi_hgh=np.percentile(par3_error_wi, 80)



    par4_error_wi=np.concatenate((simu_error1[0][3][0:5],simu_error2[0][3][:],\
                            simu_error3[0][3][:],simu_error4[0][3][:-2],simu_error5[0][3][:]))
    par4_error_wi=par4_error_wi.flatten()
    par4_error_wi_mean=np.mean(par4_error_wi)
    par4_error_wi_std=np.std(par4_error_wi)
    par4_error_wi_low=np.percentile(par4_error_wi, 20)
    par4_error_wi_hgh=np.percentile(par4_error_wi, 80)

    par1_error_wi_mean_all.append(par1_error_wi_mean)
    par1_error_wi_std_all.append(par1_error_wi_std)
    par2_error_wi_mean_all.append(par2_error_wi_mean)
    par2_error_wi_std_all.append(par2_error_wi_std)
    par3_error_wi_mean_all.append(par3_error_wi_mean)
    par3_error_wi_std_all.append(par3_error_wi_std)
    par4_error_wi_mean_all.append(par4_error_wi_mean)
    par4_error_wi_std_all.append(par4_error_wi_std)


    par1_error_wi_low_all.append(par1_error_wi_low)
    par2_error_wi_low_all.append(par2_error_wi_low)
    par3_error_wi_low_all.append(par3_error_wi_low)
    par4_error_wi_low_all.append(par4_error_wi_low)

    par1_error_wi_hgh_all.append(par1_error_wi_hgh)
    par2_error_wi_hgh_all.append(par2_error_wi_hgh)
    par3_error_wi_hgh_all.append(par3_error_wi_hgh)
    par4_error_wi_hgh_all.append(par4_error_wi_hgh)






par1_error_wt_mean_all=[]
par1_error_wt_std_all=[]
par2_error_wt_mean_all=[]
par2_error_wt_std_all=[]
par3_error_wt_mean_all=[]
par3_error_wt_std_all=[]
par4_error_wt_mean_all=[]
par4_error_wt_std_all=[]


par1_error_wt_hgh_all=[]
par2_error_wt_hgh_all=[]
par3_error_wt_hgh_all=[]
par4_error_wt_hgh_all=[]


par1_error_wt_low_all=[]
par2_error_wt_low_all=[]
par3_error_wt_low_all=[]
par4_error_wt_low_all=[]





for dirx in dir_wt:
    

    simu_error = []

    for kk in range(len(hurricanes)):
    
        real1=[]
        oussama1=[]
        wrf1=[]
        simu1=[]

        with open( dirx[kk], 'r' ) as f :
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
        simu_error.append(simu_error1)


    par1_error=np.zeros((4, 9))
    par2_error=np.zeros((4, 9))
    par3_error=np.zeros((4, 9))
    par4_error=np.zeros((4, 9))


    simu_error1 = simu_error[0]
    simu_error2 = simu_error[1]
    simu_error3 = simu_error[2]
    simu_error4 = simu_error[3]
    simu_error5 = simu_error[4]

    par1_error_wt=np.concatenate((simu_error1[0][0:5],\
                            simu_error2[0][:],simu_error3[0][:],\
                            simu_error4[0][:-2],simu_error5[0][:]))
    par1_error_wt=par1_error_wt.flatten()
    par1_error_wt_mean=np.mean(par1_error_wt)
    par1_error_wt_std=np.std(par1_error_wt)
    par1_error_wt_low=np.percentile(par1_error_wt, 20)
    par1_error_wt_hgh=np.percentile(par1_error_wt, 80)

    par2_error_wt=np.concatenate((simu_error1[1][0:5],\
                            simu_error2[1][:],simu_error3[1][:],\
                            simu_error4[1][:-2],simu_error5[1][:]))
    par2_error_wt=par2_error_wt.flatten()
    par2_error_wt_mean=np.mean(par2_error_wt)
    par2_error_wt_std=np.std(par2_error_wt)
    par2_error_wt_low=np.percentile(par2_error_wt, 20)
    par2_error_wt_hgh=np.percentile(par2_error_wt, 80)

    par3_error_wt=np.concatenate((simu_error1[2][0:5],\
                            simu_error2[2][:],simu_error3[2][:],\
                            simu_error4[2][:-2],simu_error5[2][:]))
    par3_error_wt=par3_error_wt.flatten()
    par3_error_wt_mean=np.mean(par3_error_wt)
    par3_error_wt_std=np.std(par3_error_wt)
    par3_error_wt_low=np.percentile(par3_error_wt, 20)
    par3_error_wt_hgh=np.percentile(par3_error_wt, 80)

    par4_error_wt=np.concatenate((simu_error1[3][0:5],\
                            simu_error2[3][:],simu_error3[3][:],\
                            simu_error4[3][:-2],simu_error5[3][:]))
    par4_error_wt=par4_error_wt.flatten()
    par4_error_wt_mean=np.mean(par4_error_wt)
    par4_error_wt_std=np.std(par4_error_wt)
    par4_error_wt_low=np.percentile(par4_error_wt, 20)
    par4_error_wt_hgh=np.percentile(par4_error_wt, 80)


    par1_error_wt_mean_all.append(par1_error_wt_mean)
    par1_error_wt_std_all.append(par1_error_wt_std)
    par2_error_wt_mean_all.append(par2_error_wt_mean)
    par2_error_wt_std_all.append(par2_error_wt_std)
    par3_error_wt_mean_all.append(par3_error_wt_mean)
    par3_error_wt_std_all.append(par3_error_wt_std)
    par4_error_wt_mean_all.append(par4_error_wt_mean)
    par4_error_wt_std_all.append(par4_error_wt_std)


    par1_error_wt_low_all.append(par1_error_wt_low)
    par2_error_wt_low_all.append(par2_error_wt_low)
    par3_error_wt_low_all.append(par3_error_wt_low)
    par4_error_wt_low_all.append(par4_error_wt_low)

    par1_error_wt_hgh_all.append(par1_error_wt_hgh)
    par2_error_wt_hgh_all.append(par2_error_wt_hgh)
    par3_error_wt_hgh_all.append(par3_error_wt_hgh)
    par4_error_wt_hgh_all.append(par4_error_wt_hgh)



x_pos = np.arange(len(models))

CTEs_wi1 = [par1_error_wi_mean_all[0],\
        par2_error_wi_mean_all[0],par3_error_wi_mean_all[0],par4_error_wi_mean_all[0]]
errors_wi1 = [par1_error_wi_std_all[0],\
          par2_error_wi_std_all[0],par3_error_wi_std_all[0],par4_error_wi_std_all[0]]
percentile_10_wi1 = np.array([par1_error_wi_mean_all[0]-par1_error_wi_low_all[0],\
          par2_error_wi_mean_all[0]-par2_error_wi_low_all[0],par3_error_wi_mean_all[0]-par3_error_wi_low_all[0], \
              par4_error_wi_mean_all[0]-par4_error_wi_low_all[0]])
percentile_90_wi1 = np.array([par1_error_wi_hgh_all[0]-par1_error_wi_mean_all[0],\
          par2_error_wi_hgh_all[0]-par2_error_wi_mean_all[0],par3_error_wi_hgh_all[0]-par3_error_wi_mean_all[0], \
              par4_error_wi_hgh_all[0]-par4_error_wi_mean_all[0]])
err_wi1 = np.vstack((percentile_10_wi1, percentile_90_wi1))

CTEs_wt1 = [par1_error_wt_mean_all[0],\
        par2_error_wt_mean_all[0],par3_error_wt_mean_all[0],par4_error_wt_mean_all[0]]
errors_wt1 = [par1_error_wt_std_all[0],\
          par2_error_wt_std_all[0],par3_error_wt_std_all[0],par4_error_wt_std_all[0]]
percentile_10_wt1 = np.array([par1_error_wt_mean_all[0]-par1_error_wt_low_all[0],\
          par2_error_wt_mean_all[0]-par2_error_wt_low_all[0],par3_error_wt_mean_all[0]-par3_error_wt_low_all[0], \
              par4_error_wt_mean_all[0]-par4_error_wt_low_all[0]])
percentile_90_wt1 = np.array([par1_error_wt_hgh_all[0]-par1_error_wt_mean_all[0],\
          par2_error_wt_hgh_all[0]-par2_error_wt_mean_all[0],par3_error_wt_hgh_all[0]-par3_error_wt_mean_all[0], \
              par4_error_wt_hgh_all[0]-par4_error_wt_mean_all[0]])
err_wt1 = np.vstack((percentile_10_wt1, percentile_90_wt1))



CTEs_wi2 = [par1_error_wi_mean_all[1],\
        par2_error_wi_mean_all[1],par3_error_wi_mean_all[1],par4_error_wi_mean_all[1]]
errors_wi2 = [par1_error_wi_std_all[1],\
          par2_error_wi_std_all[1],par3_error_wi_std_all[1],par4_error_wi_std_all[1]]
percentile_10_wi2 = np.array([par1_error_wi_mean_all[1]-par1_error_wi_low_all[1],\
          par2_error_wi_mean_all[1]-par2_error_wi_low_all[1],par3_error_wi_mean_all[1]-par3_error_wi_low_all[1], \
              par4_error_wi_mean_all[1]-par4_error_wi_low_all[1]])
percentile_90_wi2 = np.array([par1_error_wi_hgh_all[1]-par1_error_wi_mean_all[1],\
          par2_error_wi_hgh_all[1]-par2_error_wi_mean_all[1],par3_error_wi_hgh_all[1]-par3_error_wi_mean_all[1], \
              par4_error_wi_hgh_all[1]-par4_error_wi_mean_all[1]])
err_wi2 = np.vstack((percentile_10_wi2, percentile_90_wi2))

CTEs_wt2 = [par1_error_wt_mean_all[1],\
        par2_error_wt_mean_all[1],par3_error_wt_mean_all[1],par4_error_wt_mean_all[1]]
errors_wt2 = [par1_error_wt_std_all[1],\
          par2_error_wt_std_all[1],par3_error_wt_std_all[1],par4_error_wt_std_all[1]]
percentile_10_wt2 = np.array([par1_error_wt_mean_all[1]-par1_error_wt_low_all[1],\
          par2_error_wt_mean_all[1]-par2_error_wt_low_all[1],par3_error_wt_mean_all[1]-par3_error_wt_low_all[1], \
              par4_error_wt_mean_all[1]-par4_error_wt_low_all[1]])
percentile_90_wt2 = np.array([par1_error_wt_hgh_all[1]-par1_error_wt_mean_all[1],\
          par2_error_wt_hgh_all[1]-par2_error_wt_mean_all[1],par3_error_wt_hgh_all[1]-par3_error_wt_mean_all[1], \
              par4_error_wt_hgh_all[1]-par4_error_wt_mean_all[1]])
err_wt2 = np.vstack((percentile_10_wt2, percentile_90_wt2))






CTEs_wi3 = [par1_error_wi_mean_all[2],\
        par2_error_wi_mean_all[2],par3_error_wi_mean_all[2],par4_error_wi_mean_all[2]]
errors_wi3 = [par1_error_wi_std_all[2],\
          par2_error_wi_std_all[2],par3_error_wi_std_all[2],par4_error_wi_std_all[2]]
percentile_10_wi3 = np.array([par1_error_wi_mean_all[2]-par1_error_wi_low_all[2],\
          par2_error_wi_mean_all[2]-par2_error_wi_low_all[2],par3_error_wi_mean_all[2]-par3_error_wi_low_all[2], \
              par4_error_wi_mean_all[2]-par4_error_wi_low_all[2]])
percentile_90_wi3 = np.array([par1_error_wi_hgh_all[2]-par1_error_wi_mean_all[2],\
          par2_error_wi_hgh_all[2]-par2_error_wi_mean_all[2],par3_error_wi_hgh_all[2]-par3_error_wi_mean_all[2], \
              par4_error_wi_hgh_all[2]-par4_error_wi_mean_all[2]])
err_wi3 = np.vstack((percentile_10_wi3, percentile_90_wi3))

CTEs_wt3 = [par1_error_wt_mean_all[2],\
        par2_error_wt_mean_all[2],par3_error_wt_mean_all[2],par4_error_wt_mean_all[2]]
errors_wt3 = [par1_error_wt_std_all[2],\
          par2_error_wt_std_all[2],par3_error_wt_std_all[2],par4_error_wt_std_all[2]]
percentile_10_wt3 = np.array([par1_error_wt_mean_all[2]-par1_error_wt_low_all[2],\
          par2_error_wt_mean_all[2]-par2_error_wt_low_all[2],par3_error_wt_mean_all[2]-par3_error_wt_low_all[2], \
              par4_error_wt_mean_all[2]-par4_error_wt_low_all[2]])
percentile_90_wt3 = np.array([par1_error_wt_hgh_all[2]-par1_error_wt_mean_all[2],\
          par2_error_wt_hgh_all[2]-par2_error_wt_mean_all[2],par3_error_wt_hgh_all[2]-par3_error_wt_mean_all[2], \
              par4_error_wt_hgh_all[2]-par4_error_wt_mean_all[2]])
err_wt3 = np.vstack((percentile_10_wt3, percentile_90_wt3))







# fig, ax = plt.subplots(1, 2, figsize=(40, 8), sharex=True)
fig = plt.figure(figsize=(8,5))
spec = mpl.gridspec.GridSpec(ncols=8, nrows=5)


ax = fig.add_subplot(spec[1:,0:4])
ax.text(0.75, 0.9, '('+string.ascii_lowercase[0]+')', transform=ax.transAxes, 
            size=20, **csfont)



bars = ax.bar(x_pos, CTEs_wi1, yerr=err_wi1, align='center', \
        color=['blue','cyan','gray', 'red'], alpha=0.8, width=0.25,\
        ecolor='k', capsize=5, edgecolor='k', linewidth=1, hatch='///')   
for i in range(len(x_pos)):
    bars[i].set(linestyle=list(linestyles.values())[0])    
    
bars = ax.bar(x_pos+0.25, CTEs_wi2, yerr=err_wi2, align='center', \
        color=['blue','cyan','gray', 'red'], alpha=0.8, width=0.25,\
        ecolor='k', capsize=5, edgecolor='k', linewidth=1, hatch='xxx')   
for i in range(len(x_pos)):
    bars[i].set(linestyle=list(linestyles.values())[0]) 
    
    
bars = ax.bar(x_pos+0.5, CTEs_wi3, yerr=err_wi3, align='center', \
        color=['blue','cyan','gray', 'red'], alpha=0.8, width=0.25,\
        ecolor='k', capsize=5, edgecolor='k', linewidth=1)   
for i in range(len(x_pos)):
    bars[i].set(linestyle=list(linestyles.values())[0])     

    
    
    
    
ax.set_ylabel(r'Normalized Intensity', **csfont, fontsize=15)
vals = ax.get_yticks()
ax.set_yticklabels(['{:,.0%}'.format(x) for x in vals], **csfont, fontsize=12)
ax.set_xticks(x_pos)
ax.set_xticklabels(models, **csfont, fontsize=10)
#ax.set_title(r'COAWST', **csfont, fontsize=20)
ax.yaxis.grid(True)



ax = fig.add_subplot(spec[1:,4:])
ax.text(0.75, 0.9, '('+string.ascii_lowercase[1]+')', transform=ax.transAxes, 
            size=20, **csfont)    


bars = ax.bar(x_pos, CTEs_wt1, yerr=err_wt1, align='center', \
        color=['blue','cyan','gray', 'red'], alpha=0.8, width=0.25,\
        ecolor='k', capsize=5, edgecolor='k', linewidth=1, hatch='///') 
for i in range(len(x_pos)):
    bars[i].set(linestyle=list(linestyles.values())[0])
    

bars = ax.bar(x_pos+0.25, CTEs_wt2, yerr=err_wt2, align='center', \
        color=['blue','cyan','gray', 'red'], alpha=0.8, width=0.25,\
        ecolor='k', capsize=5, edgecolor='k', linewidth=1, hatch='xxx') 
for i in range(len(x_pos)):
    bars[i].set(linestyle=list(linestyles.values())[0])
    
    
bars = ax.bar(x_pos+0.50, CTEs_wt3, yerr=err_wt3, align='center', \
        color=['blue','cyan','gray', 'red'], alpha=0.8, width=0.25,\
        ecolor='k', capsize=5, edgecolor='k', linewidth=1) 
for i in range(len(x_pos)):
    bars[i].set(linestyle=list(linestyles.values())[0])    

    
    
ax.set_ylabel(r'Track Error (km)', **csfont, fontsize=15)
vals = ax.get_yticks()
ax.set_yticklabels(['{}'.format(x) for x in vals], **csfont, fontsize=12)
ax.set_xticks(x_pos)
ax.set_xticklabels(models, **csfont, fontsize=10)
#ax.set_title(r'COAWST', **csfont, fontsize=20)
ax.yaxis.grid(True)



ax = fig.add_subplot(spec[0,0:])
# handles = [plt.Rectangle((0,0),1,1, facecolor=colors[i+1], \
#         linestyle=list(linestyles.values())[0], edgecolor = 'k', linewidth=1.5\
#             ) for i in range(len(models))]
# plt.legend(handles, models, ncol=4, bbox_to_anchor=(0.9, 0.8), prop=fontbar, \
#                 frameon=False)
hatch=['///','xxx','']
handles = [plt.Rectangle((0,0),1,1,hatch=hatch[i], facecolor='none',\
        linestyle=list(linestyles.values())[0], edgecolor = 'k', linewidth=1.5\
            ) for i in range(3)]
plt.legend(handles, ['COAWST', 'WRF-YSU-1', 'WRF-YSU-2'], ncol=3, \
           bbox_to_anchor=(0.85, 0.8), prop=fontbar, frameon=False)
ax.axes.xaxis.set_visible(False)
ax.axes.yaxis.set_visible(False)
ax.set_yticks([])
ax.set_yticklabels([])
ax.set_xticks([])
ax.set_xticklabels([])
for axis in ['top','bottom','left','right']:
    ax.spines[axis].set_visible(False)



# for i, v in enumerate(CTEs):
#     ax.text(i, v+0.02, str(round(v, 3)), color='red', fontweight='bold')

# Save the figure and show
fig.autofmt_xdate()
plt.tight_layout()
#plt.savefig('wind_intensity_bar_plot.png')
plt.savefig('C:/Users/limgr/Desktop/wi_wt_bar_plots.png', dpi=500)
plt.show()




