import numpy as np
from netCDF4 import Dataset
import matplotlib.pyplot as plt
import json
from cartopy.feature import NaturalEarthFeature
import cartopy.crs as crs
import pickle
from wrf import (to_np, getvar, smooth2d, get_cartopy, cartopy_xlim,
                 cartopy_ylim, latlon_coords)


### user defined parmaters

R = 6373.0 # approxiamte radius of earth in km

# output file path
filename1 = 'C:/Users/limgr/Desktop/Katrina_track_8km.txt'
filename2 = 'C:/Users/limgr/Desktop/Gustav_track_8km.txt'
filename3 = 'C:/Users/limgr/Desktop/Maria_track_8km.txt'
filename4 = 'C:/Users/limgr/Desktop/Irma_track_8km.txt'
filename5 = 'C:/Users/limgr/Desktop/Dorian_track_8km.txt'
filename6 = 'C:/Users/limgr/Desktop/Rita_track_8km.txt'
filename7 = 'C:/Users/limgr/Desktop/Lorenzo_track_8km.txt'

filename21 = 'C:/Users/limgr/Desktop/Katrina_8km.p'
filename22 = 'C:/Users/limgr/Desktop/Gustav_8km.p'
filename23 = 'C:/Users/limgr/Desktop/Maria_8km.p'
filename24 = 'C:/Users/limgr/Desktop/Irma_8km.p'
filename25 = 'C:/Users/limgr/Desktop/Dorian_8km.p'
filename26 = 'C:/Users/limgr/Desktop/Rita_8km.p'
filename27 = 'C:/Users/limgr/Desktop/Lorenzo_8km.p'

def Calculate_Distance_Haversine1(x):
    return (np.sin(x[0]/2))**2
def Calculate_Distance_Haversine2(x):
    return np.cos(x[0])
def Calculate_Distance_Haversine3(x):
    return (np.sin(x[1]/2))**2

colors = ['black', 'blue','red','green', 'cyan', \
           'gray',  'gold', 'lightcoral', 'turquoise','red','blue','green','pink']
patterns = ['-', '--','--','--','--','--','--','--', ':','-', '--', ':','-', '--', ':',\
            '-.', '-.', '-.', ':', '--', '-']
markers = ['.',',','o','v','8','s','+','x','X','D','^','<','>','v'] 
#sizes = [10, 5, 5, 5, 4, 4, 4, 3, 3, 3, 3, 3, 6,5,4,3,2,2]
sizes = [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]















real1=[]
oussama1=[]
wrf1=[]
simu1=[]

with open( filename1, 'r' ) as f :
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
# oussama1 = np.array(oussama1, dtype=np.float32)
# wrf1 = np.array(wrf1, dtype=np.float32)
simu1 = np.array(simu1, dtype=np.float32)
real_r = np.radians(real1)
# ouss_r = np.radians(oussama1)
# wrf_r = np.radians(wrf1)
simu_r = np.radians(simu1)

# term1=np.apply_along_axis(Calculate_Distance_Haversine1, 2, ouss_r-real_r)
# term2=np.apply_along_axis(Calculate_Distance_Haversine2, 2, ouss_r)* \
#     np.apply_along_axis(Calculate_Distance_Haversine2, 2, real_r)* \
#     np.apply_along_axis(Calculate_Distance_Haversine3, 2, ouss_r-real_r)
# ouss_error1=2*R*np.arcsin(np.sqrt(term1+term2))

# term1=np.apply_along_axis(Calculate_Distance_Haversine1, 2, wrf_r-real_r)
# term2=np.apply_along_axis(Calculate_Distance_Haversine2, 2, wrf_r)* \
#     np.apply_along_axis(Calculate_Distance_Haversine2, 2, real_r)* \
#     np.apply_along_axis(Calculate_Distance_Haversine3, 2, wrf_r-real_r)
# wrf_error1=2*R*np.arcsin(np.sqrt(term1+term2))

term1=np.apply_along_axis(Calculate_Distance_Haversine1, 2, simu_r-real_r)
term2=np.apply_along_axis(Calculate_Distance_Haversine2, 2, simu_r)* \
    np.apply_along_axis(Calculate_Distance_Haversine2, 2, real_r)* \
    np.apply_along_axis(Calculate_Distance_Haversine3, 2, simu_r-real_r)
simu_error1=2*R*np.arcsin(np.sqrt(term1+term2))



slp2D = pickle.load( open( filename21, "rb" ) )
#print(slp2D)

#slp2D.plot()
lats, lons = latlon_coords(slp2D)

# Get the cartopy mapping object (use original data, rather than any processed data)
cart_proj = get_cartopy(slp2D)


	# Set the GeoAxes to the projection used by WRF
ax = plt.axes(projection=cart_proj)
ax.stock_img()

	# Download and add the states and coastlines
states = NaturalEarthFeature(category="cultural", scale="50m",
	                             facecolor="none",
	                             name="admin_1_states_provinces_shp")
ax.add_feature(states, linewidth=.5, edgecolor="black")
ax.coastlines('50m', linewidth=0.8)


	# Set the map bounds
# ax.set_xlim(cartopy_xlim(slp2D))
# ax.set_ylim(cartopy_ylim(slp2D))
ax.set_extent([-90, -85, 24, 33])


# Show grid lines.
gl = ax.gridlines(crs=crs.PlateCarree(), draw_labels=True,
                  linewidth=1, color='black', alpha=0.5, linestyle=':')
gl.xlabel_style = {'size': 15}
gl.xlabel_style = {'color': 'black'}
gl.xlabels_top = False
gl.ylabels_left = False




c=0

ll=[]
rr=[]
for i in range(real1.shape[0]):
    for j in range(real1.shape[1]):
        if j<6:
            ll.append(real1[i][j][0])
            rr.append(real1[i][j][1])
    plt.plot( rr, ll, color = colors[c], marker='s', linestyle=patterns[c],\
             markersize=sizes[c], transform=crs.PlateCarree())
    c+=1


ll=[]
rr=[]
for i in range(simu1.shape[0]):
    for j in range(simu1.shape[1]):
        if j<6:
            ll.append(simu1[i][j][0])
            rr.append(simu1[i][j][1])
    plt.plot( rr, ll, color = colors[c], marker='s', linestyle=patterns[c],\
             markersize=sizes[c], transform=crs.PlateCarree())
    c+=1
    ll=[]
    rr=[]

plt.legend(['Real track','C0.0001', 'C0.01', 'C1', 'C100'],\
           loc = "upper right", prop={'size': 7})
plt.xlabel("Lon", fontsize=14)
plt.ylabel("Lat", fontsize=14)
plt.title("Katrina Track", {'size': 20})
plt.savefig('C:/Users/limgr/Desktop/katrina_wt_A.png')
plt.show()



























real3=[]
oussama3=[]
wrf3=[]
simu3=[]

with open( filename3, 'r' ) as f :
    data0 = f.read()
    data = json.loads('[' + data0.replace('}{', '},{') + ']')
for i in range(0,len(data)):
    data2 = list(data[i].values())
    data3 = [e for sl in data2 for e in sl]
    for j in range(len(data3)):
        data3[j].pop(0)
    if i==0:
        real3.append(data3)
    # elif i==1:
    #     oussama3.append(data3)
    # elif i==2:
    #     wrf3.append(data3)
    else:
        simu3.append(data3)
real3 = np.array(real3, dtype=np.float32)
# oussama3 = np.array(oussama3, dtype=np.float32)
# wrf3 = np.array(wrf3, dtype=np.float32)
simu3 = np.array(simu3, dtype=np.float32)
real_r = np.radians(real3)
# ouss_r = np.radians(oussama3)
# wrf_r = np.radians(wrf3)
simu_r = np.radians(simu3)

# term1=np.apply_along_axis(Calculate_Distance_Haversine1, 2, ouss_r-real_r)
# term2=np.apply_along_axis(Calculate_Distance_Haversine2, 2, ouss_r)* \
#     np.apply_along_axis(Calculate_Distance_Haversine2, 2, real_r)* \
#     np.apply_along_axis(Calculate_Distance_Haversine3, 2, ouss_r-real_r)
# ouss_error3=2*R*np.arcsin(np.sqrt(term1+term2))

# term1=np.apply_along_axis(Calculate_Distance_Haversine1, 2, wrf_r-real_r)
# term2=np.apply_along_axis(Calculate_Distance_Haversine2, 2, wrf_r)* \
#     np.apply_along_axis(Calculate_Distance_Haversine2, 2, real_r)* \
#     np.apply_along_axis(Calculate_Distance_Haversine3, 2, wrf_r-real_r)
# wrf_error3=2*R*np.arcsin(np.sqrt(term1+term2))

term1=np.apply_along_axis(Calculate_Distance_Haversine1, 2, simu_r-real_r)
term2=np.apply_along_axis(Calculate_Distance_Haversine2, 2, simu_r)* \
    np.apply_along_axis(Calculate_Distance_Haversine2, 2, real_r)* \
    np.apply_along_axis(Calculate_Distance_Haversine3, 2, simu_r-real_r)
simu_error3=2*R*np.arcsin(np.sqrt(term1+term2))

slp2D = pickle.load( open( filename23, "rb" ) )
#print(slp2D)

#slp2D.plot()
lats, lons = latlon_coords(slp2D)

# Get the cartopy mapping object (use original data, rather than any processed data)
cart_proj = get_cartopy(slp2D)


	# Set the GeoAxes to the projection used by WRF
ax = plt.axes(projection=cart_proj)
ax.stock_img()

	# Download and add the states and coastlines
states = NaturalEarthFeature(category="cultural", scale="50m",
	                             facecolor="none",
	                             name="admin_1_states_provinces_shp")
ax.add_feature(states, linewidth=.5, edgecolor="black")
ax.coastlines('50m', linewidth=0.8)


	# Set the map bounds
# ax.set_xlim(cartopy_xlim(slp2D))
# ax.set_ylim(cartopy_ylim(slp2D))
ax.set_extent([-75, -69, 19, 27])


# Show grid lines.
gl = ax.gridlines(crs=crs.PlateCarree(), draw_labels=True,
                  linewidth=1, color='black', alpha=0.5, linestyle=':')
gl.xlabel_style = {'size': 15}
gl.xlabel_style = {'color': 'black'}
gl.xlabels_top = False
gl.ylabels_left = False

c=0

ll=[]
rr=[]
for i in range(real3.shape[0]):
    for j in range(real3.shape[1]):
        ll.append(real3[i][j][0])
        rr.append(real3[i][j][1])
    plt.plot( rr, ll, color = colors[c], marker='s', linestyle=patterns[c],\
             markersize=sizes[c], transform=crs.PlateCarree())
    c+=1



ll=[]
rr=[]
for i in range(simu3.shape[0]):
    for j in range(simu3.shape[1]):
        ll.append(simu3[i][j][0])
        rr.append(simu3[i][j][1])
    plt.plot( rr, ll, color = colors[c], marker='s', linestyle=patterns[c],\
             markersize=sizes[c], transform=crs.PlateCarree())
    c+=1
    ll=[]
    rr=[]

plt.legend(['Real track','C0.0001', 'C0.01', 'C1', 'C100'],\
           loc = "upper right", prop={'size': 7})
plt.xlabel("Lon", fontsize=14)
plt.ylabel("Lat", fontsize=14)
plt.title("Maria Track", {'size': 20})
plt.savefig('C:/Users/limgr/Desktop/maria_wt_A.png')
plt.show()












real4=[]
oussama4=[]
wrf4=[]
simu4=[]

with open( filename4, 'r' ) as f :
    data0 = f.read()
    data = json.loads('[' + data0.replace('}{', '},{') + ']')
for i in range(0,len(data)):
    data2 = list(data[i].values())
    data3 = [e for sl in data2 for e in sl]
    for j in range(len(data3)):
        data3[j].pop(0)
    if i==0:
        real4.append(data3)
    # elif i==1:
    #     oussama4.append(data3)
    # elif i==2:
    #     wrf4.append(data3)
    else:
        simu4.append(data3)
real4 = np.array(real4, dtype=np.float32)
# oussama4 = np.array(oussama4, dtype=np.float32)
# wrf4 = np.array(wrf4, dtype=np.float32)
simu4 = np.array(simu4, dtype=np.float32)
real_r = np.radians(real4)
# ouss_r = np.radians(oussama4)
# wrf_r = np.radians(wrf4)
simu_r = np.radians(simu4)

# term1=np.apply_along_axis(Calculate_Distance_Haversine1, 2, ouss_r-real_r)
# term2=np.apply_along_axis(Calculate_Distance_Haversine2, 2, ouss_r)* \
#     np.apply_along_axis(Calculate_Distance_Haversine2, 2, real_r)* \
#     np.apply_along_axis(Calculate_Distance_Haversine3, 2, ouss_r-real_r)
# ouss_error4=2*R*np.arcsin(np.sqrt(term1+term2))

# term1=np.apply_along_axis(Calculate_Distance_Haversine1, 2, wrf_r-real_r)
# term2=np.apply_along_axis(Calculate_Distance_Haversine2, 2, wrf_r)* \
#     np.apply_along_axis(Calculate_Distance_Haversine2, 2, real_r)* \
#     np.apply_along_axis(Calculate_Distance_Haversine3, 2, wrf_r-real_r)
# wrf_error4=2*R*np.arcsin(np.sqrt(term1+term2))

term1=np.apply_along_axis(Calculate_Distance_Haversine1, 2, simu_r-real_r)
term2=np.apply_along_axis(Calculate_Distance_Haversine2, 2, simu_r)* \
    np.apply_along_axis(Calculate_Distance_Haversine2, 2, real_r)* \
    np.apply_along_axis(Calculate_Distance_Haversine3, 2, simu_r-real_r)
simu_error4=2*R*np.arcsin(np.sqrt(term1+term2))


slp2D = pickle.load( open( filename24, "rb" ) )
#print(slp2D)

#slp2D.plot()
lats, lons = latlon_coords(slp2D)

# Get the cartopy mapping object (use original data, rather than any processed data)
cart_proj = get_cartopy(slp2D)


	# Set the GeoAxes to the projection used by WRF
ax = plt.axes(projection=cart_proj)
ax.stock_img()

	# Download and add the states and coastlines
states = NaturalEarthFeature(category="cultural", scale="50m",
	                             facecolor="none",
	                             name="admin_1_states_provinces_shp")
ax.add_feature(states, linewidth=.5, edgecolor="black")
ax.coastlines('50m', linewidth=0.8)


	# Set the map bounds
# ax.set_xlim(cartopy_xlim(slp2D))
# ax.set_ylim(cartopy_ylim(slp2D))
ax.set_extent([-51, -39, 16, 20])


# Show grid lines.
gl = ax.gridlines(crs=crs.PlateCarree(), draw_labels=True,
                  linewidth=1, color='black', alpha=0.5, linestyle=':')
gl.xlabel_style = {'size': 15}
gl.xlabel_style = {'color': 'black'}
gl.xlabels_top = False
gl.ylabels_left = False

c=0

ll=[]
rr=[]
for i in range(real4.shape[0]):
    for j in range(real4.shape[1]):
        ll.append(real4[i][j][0])
        rr.append(real4[i][j][1])
    plt.plot( rr, ll, color = colors[c], marker='s', linestyle=patterns[c],\
             markersize=sizes[c], transform=crs.PlateCarree())
    c+=1


ll=[]
rr=[]
for i in range(simu4.shape[0]):
    for j in range(simu4.shape[1]):
        ll.append(simu4[i][j][0])
        rr.append(simu4[i][j][1])
    plt.plot( rr, ll, color = colors[c], marker='s', linestyle=patterns[c],\
             markersize=sizes[c], transform=crs.PlateCarree())
    c+=1
    ll=[]
    rr=[]

plt.legend(['Real track','C0.0001', 'C0.01', 'C1', 'C100'],\
           loc = "lower right", prop={'size': 7})
plt.xlabel("Lon", fontsize=14)
plt.ylabel("Lat", fontsize=14)
plt.title("Irma Track", {'size': 20})
plt.savefig('C:/Users/limgr/Desktop/irma_wt_A.png')
plt.show()













real5=[]
oussama5=[]
wrf5=[]
simu5=[]

with open( filename5, 'r' ) as f :
    data0 = f.read()
    data = json.loads('[' + data0.replace('}{', '},{') + ']')
for i in range(0,len(data)):
    data2 = list(data[i].values())
    data3 = [e for sl in data2 for e in sl]
    for j in range(len(data3)):
        data3[j].pop(0)
    if i==0:
        real5.append(data3)
    # elif i==1:
    #     oussama5.append(data3)
    # elif i==2:
    #     wrf5.append(data3)
    else:
        simu5.append(data3)
real5 = np.array(real5, dtype=np.float32)
# oussama5 = np.array(oussama5, dtype=np.float32)
# wrf5 = np.array(wrf5, dtype=np.float32)
simu5 = np.array(simu5, dtype=np.float32)
real_r = np.radians(real5)
# ouss_r = np.radians(oussama5)
# wrf_r = np.radians(wrf5)
simu_r = np.radians(simu5)

# term1=np.apply_along_axis(Calculate_Distance_Haversine1, 2, ouss_r-real_r)
# term2=np.apply_along_axis(Calculate_Distance_Haversine2, 2, ouss_r)* \
#     np.apply_along_axis(Calculate_Distance_Haversine2, 2, real_r)* \
#     np.apply_along_axis(Calculate_Distance_Haversine3, 2, ouss_r-real_r)
# ouss_error5=2*R*np.arcsin(np.sqrt(term1+term2))

# term1=np.apply_along_axis(Calculate_Distance_Haversine1, 2, wrf_r-real_r)
# term2=np.apply_along_axis(Calculate_Distance_Haversine2, 2, wrf_r)* \
#     np.apply_along_axis(Calculate_Distance_Haversine2, 2, real_r)* \
#     np.apply_along_axis(Calculate_Distance_Haversine3, 2, wrf_r-real_r)
# wrf_error5=2*R*np.arcsin(np.sqrt(term1+term2))

term1=np.apply_along_axis(Calculate_Distance_Haversine1, 2, simu_r-real_r)
term2=np.apply_along_axis(Calculate_Distance_Haversine2, 2, simu_r)* \
    np.apply_along_axis(Calculate_Distance_Haversine2, 2, real_r)* \
    np.apply_along_axis(Calculate_Distance_Haversine3, 2, simu_r-real_r)
simu_error5=2*R*np.arcsin(np.sqrt(term1+term2))

slp2D = pickle.load( open( filename25, "rb" ) )
#print(slp2D)

#slp2D.plot()
lats, lons = latlon_coords(slp2D)

# Get the cartopy mapping object (use original data, rather than any processed data)
cart_proj = get_cartopy(slp2D)


	# Set the GeoAxes to the projection used by WRF
ax = plt.axes(projection=cart_proj)
ax.stock_img()

	# Download and add the states and coastlines
states = NaturalEarthFeature(category="cultural", scale="50m",
	                             facecolor="none",
	                             name="admin_1_states_provinces_shp")
ax.add_feature(states, linewidth=.5, edgecolor="black")
ax.coastlines('50m', linewidth=0.8)


	# Set the map bounds
# ax.set_xlim(cartopy_xlim(slp2D))
# ax.set_ylim(cartopy_ylim(slp2D))
ax.set_extent([-80, -70, 23, 29])



# Show grid lines.
gl = ax.gridlines(crs=crs.PlateCarree(), draw_labels=True,
                  linewidth=1, color='black', alpha=0.5, linestyle=':')
gl.xlabel_style = {'size': 15}
gl.xlabel_style = {'color': 'black'}
gl.xlabels_top = False
gl.ylabels_left = False

c=0

ll=[]
rr=[]
for i in range(real5.shape[0]):
    for j in range(real5.shape[1]):
        ll.append(real5[i][j][0])
        rr.append(real5[i][j][1])
    plt.plot( rr[:-2], ll[:-2], color = colors[c], marker='s', linestyle=patterns[c],\
             markersize=sizes[c], transform=crs.PlateCarree())
    c+=1

    
    

ll=[]
rr=[]
for i in range(simu5.shape[0]):
    for j in range(simu5.shape[1]):
        ll.append(simu5[i][j][0])
        rr.append(simu5[i][j][1])
    plt.plot( rr[:-2], ll[:-2], color = colors[c], marker='s', linestyle=patterns[c],\
             markersize=sizes[c], transform=crs.PlateCarree())
    c+=1
    ll=[]
    rr=[]

plt.legend(['Real track','C0.0001', 'C0.01', 'C1', 'C100'],\
           loc = "upper right", prop={'size': 7})
plt.xlabel("Lon", fontsize=14)
plt.ylabel("Lat", fontsize=14)
plt.title("Dorian Track", {'size': 20})
plt.savefig('C:/Users/limgr/Desktop/dorian_wt_A.png')
plt.show()


















real7=[]
oussama7=[]
wrf7=[]
simu7=[]

with open( filename7, 'r' ) as f :
    data0 = f.read()
    data = json.loads('[' + data0.replace('}{', '},{') + ']')
for i in range(0,len(data)):
    data2 = list(data[i].values())
    data3 = [e for sl in data2 for e in sl]
    for j in range(len(data3)):
        data3[j].pop(0)
    if i==0:
        real7.append(data3)
    # elif i==1:
    #     oussama5.append(data3)
    # elif i==2:
    #     wrf5.append(data3)
    else:
        simu7.append(data3)
real7 = np.array(real7, dtype=np.float32)
# oussama5 = np.array(oussama5, dtype=np.float32)
# wrf5 = np.array(wrf5, dtype=np.float32)
simu7 = np.array(simu7, dtype=np.float32)
real_r = np.radians(real7)
# ouss_r = np.radians(oussama5)
# wrf_r = np.radians(wrf5)
simu_r = np.radians(simu7)

# term1=np.apply_along_axis(Calculate_Distance_Haversine1, 2, ouss_r-real_r)
# term2=np.apply_along_axis(Calculate_Distance_Haversine2, 2, ouss_r)* \
#     np.apply_along_axis(Calculate_Distance_Haversine2, 2, real_r)* \
#     np.apply_along_axis(Calculate_Distance_Haversine3, 2, ouss_r-real_r)
# ouss_error5=2*R*np.arcsin(np.sqrt(term1+term2))

# term1=np.apply_along_axis(Calculate_Distance_Haversine1, 2, wrf_r-real_r)
# term2=np.apply_along_axis(Calculate_Distance_Haversine2, 2, wrf_r)* \
#     np.apply_along_axis(Calculate_Distance_Haversine2, 2, real_r)* \
#     np.apply_along_axis(Calculate_Distance_Haversine3, 2, wrf_r-real_r)
# wrf_error5=2*R*np.arcsin(np.sqrt(term1+term2))

term1=np.apply_along_axis(Calculate_Distance_Haversine1, 2, simu_r-real_r)
term2=np.apply_along_axis(Calculate_Distance_Haversine2, 2, simu_r)* \
    np.apply_along_axis(Calculate_Distance_Haversine2, 2, real_r)* \
    np.apply_along_axis(Calculate_Distance_Haversine3, 2, simu_r-real_r)
simu_error7=2*R*np.arcsin(np.sqrt(term1+term2))

slp2D = pickle.load( open( filename27, "rb" ) )
#print(slp2D)

#slp2D.plot()
lats, lons = latlon_coords(slp2D)

# Get the cartopy mapping object (use original data, rather than any processed data)
cart_proj = get_cartopy(slp2D)


	# Set the GeoAxes to the projection used by WRF
ax = plt.axes(projection=cart_proj)
ax.stock_img()

	# Download and add the states and coastlines
states = NaturalEarthFeature(category="cultural", scale="50m",
	                             facecolor="none",
	                             name="admin_1_states_provinces_shp")
ax.add_feature(states, linewidth=.5, edgecolor="black")
ax.coastlines('50m', linewidth=0.8)


	# Set the map bounds
# ax.set_xlim(cartopy_xlim(slp2D))
# ax.set_ylim(cartopy_ylim(slp2D))
ax.set_extent([-50, -35, 12, 28])



# Show grid lines.
gl = ax.gridlines(crs=crs.PlateCarree(), draw_labels=True,
                  linewidth=1, color='black', alpha=0.5, linestyle=':')
gl.xlabel_style = {'size': 15}
gl.xlabel_style = {'color': 'black'}
gl.xlabels_top = False
gl.ylabels_left = False

c=0

ll=[]
rr=[]
for i in range(real7.shape[0]):
    for j in range(real7.shape[1]):
        ll.append(real7[i][j][0])
        rr.append(real7[i][j][1])
    plt.plot( rr, ll, color = colors[c], marker='s', linestyle=patterns[c],\
             markersize=sizes[c], transform=crs.PlateCarree())
    c+=1

    
    

ll=[]
rr=[]
for i in range(simu7.shape[0]):
    for j in range(simu7.shape[1]):
        ll.append(simu7[i][j][0])
        rr.append(simu7[i][j][1])
    plt.plot( rr, ll, color = colors[c], marker='s', linestyle=patterns[c],\
             markersize=sizes[c], transform=crs.PlateCarree())
    c+=1
    ll=[]
    rr=[]

plt.legend(['Real track','C0.0001', 'C0.01', 'C1', 'C100'],\
           loc = "upper right", prop={'size': 7})
plt.xlabel("Lon", fontsize=14)
plt.ylabel("Lat", fontsize=14)
plt.title("Lorenzo Track", {'size': 20})
plt.savefig('C:/Users/limgr/Desktop/lorenzo_wt_A.png')
plt.show()























ouss_error=np.zeros((6, 9))
wrf_error=np.zeros((6, 9))
par1_error=np.zeros((6, 9))
par2_error=np.zeros((6, 9))
par3_error=np.zeros((6, 9))
par4_error=np.zeros((6, 9))
par5_error=np.zeros((6, 9))
# par6_error=np.zeros((4, 9))
# par7_error=np.zeros((4, 9))
# par8_error=np.zeros((4, 9))
# par9_error=np.zeros((4, 9))






# par1_error[0]=simu_error1[0][:]
# par1_error[1]=simu_error2[0][:]
# par1_error[2]=simu_error3[0][:]
# par1_error[3]=simu_error4[0][:]
# par1_error[4]=simu_error5[0][:]
# par1_error[5]=simu_error6[0][:]
par1_error=np.concatenate((simu_error1[0][0:5],\
                           simu_error3[0][:],simu_error4[0][:],\
                           simu_error5[0][:-2],simu_error7[0][:]))
par1_error=par1_error.flatten()
par1_error_mean=np.mean(par1_error)
par1_error_std=np.std(par1_error)








# par2_error[0]=simu_error1[1][:]
# par2_error[1]=simu_error2[1][:]
# par2_error[2]=simu_error3[1][:]
# par2_error[3]=simu_error4[1][:]
# par2_error[4]=simu_error5[1][:]
# par2_error[5]=simu_error6[1][:]
par2_error=np.concatenate((simu_error1[1][0:5],\
                           simu_error3[1][:],simu_error4[1][:],\
                           simu_error5[1][:-2],simu_error7[1][:]))
par2_error=par2_error.flatten()
par2_error_mean=np.mean(par2_error)
par2_error_std=np.std(par2_error)




# par3_error[0]=simu_error1[2][:]
# par3_error[1]=simu_error2[2][:]
# par3_error[2]=simu_error3[2][:]
# par3_error[3]=simu_error4[2][:]
# par3_error[4]=simu_error5[2][:]
# par3_error[5]=simu_error6[2][:]
par3_error=np.concatenate((simu_error1[2][0:5],\
                           simu_error3[2][:],simu_error4[2][:],\
                           simu_error5[2][:-2],simu_error7[2][:]))
par3_error=par3_error.flatten()
par3_error_mean=np.mean(par3_error)
par3_error_std=np.std(par3_error)




# par4_error[0]=simu_error1[3][:]
# par4_error[1]=simu_error2[3][:]
# par4_error[2]=simu_error3[3][:]
# par4_error[3]=simu_error4[3][:]
# par4_error[4]=simu_error5[3][:]
# par4_error[5]=simu_error6[3][:]
par4_error=np.concatenate((simu_error1[3][0:5],\
                           simu_error3[3][:],simu_error4[3][:],\
                           simu_error5[3][:-2],simu_error7[3][:]))
par4_error=par4_error.flatten()
par4_error_mean=np.mean(par4_error)
par4_error_std=np.std(par4_error)






hurricanes = ['C0.0001', 'C0.01', 'C1', 'C100']
x_pos = np.arange(len(hurricanes))
CTEs = [par1_error_mean,par2_error_mean,\
        par3_error_mean,par4_error_mean]
errors = [par1_error_std,par2_error_std,\
          par3_error_std,par4_error_std]


fig, ax = plt.subplots()
ax.bar(x_pos, CTEs, yerr=errors, align='center', alpha=0.5, ecolor='black', capsize=10)
ax.set_ylabel('Wind track error')
ax.set_xticks(x_pos)
ax.set_xticklabels(hurricanes)
ax.set_title('Hurricanes')
ax.yaxis.grid(True)
for i, v in enumerate(CTEs):
    ax.text(i, v + 3, str(round(v, 3)), color='red', fontweight='bold')
# Save the figure and show
fig.autofmt_xdate()
plt.tight_layout()
#plt.savefig('wind_intensity_bar_plot.png')
plt.savefig('C:/Users/limgr/Desktop/wt_errorbar_A.png')
plt.show()










