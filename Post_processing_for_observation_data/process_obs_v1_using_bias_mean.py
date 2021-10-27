import scipy.io
from sklearn.linear_model import LinearRegression
import sys
import numpy as np
import matplotlib.pyplot as plt
import math
import sys


# user input variavles
filename = ['Katrina.mat']
max_height = 21 # max_height + 1, level not meter
data_type = ['z', 'u', 'v'] # extracted data types, expect 3
colors = ['k','green', 'red', 'purple', 'grey']
wind_speed_interval = 10 # speed inernal for bins, in meter


# some functions
def split_accordingto_row(arr_input, cond):
    c = np.argwhere(arr_input[cond])
    return [arr_input[cond]]





# load observation data
mat = scipy.io.loadmat(filename[0])
print(mat.keys())
print(mat['u'][2][1])


            
 

# extract required data
extracted_data = []
for i in range(len(data_type)):
    extracted_data.append(mat[data_type[i]][1:max_height])
    
data_shape = []
for i in range(len(extracted_data)):
    tmp = extracted_data[i].shape
    data_shape.append(tmp)
    print(' raw data '+data_type[i]+' shape: ', tmp)
    
count = 0    
for i in range(len(data_shape)):
    if data_shape[i]==data_shape[0]:
        count += 1
if count == len(data_shape) and len(data_shape[0]) == 2:
    print('data shapes are consistent')
else:
    sys.exit('error! check raw data, data shape inconsistent')



# data engineering, remove NAN samples in extracted data
processed_data = [[] for _ in range(len(extracted_data))]
res = int(''.join(map(str, data_shape[0])))

for i in range(int(data_shape[0][0])):
    for j in range(int(data_shape[0][1])):
        if not np.isnan(extracted_data[0][i,j]) and \
            not np.isnan(extracted_data[1][i,j]) and  \
            not np.isnan(extracted_data[2][i,j]):
            continue
        else:
            extracted_data[0][i,j] = np.nan
            extracted_data[1][i,j] = np.nan            
            extracted_data[2][i,j] = np.nan            
     
  
z = extracted_data[0][:, ~np.isnan(extracted_data[0]).any(axis=0)]
u = extracted_data[1][:, ~np.isnan(extracted_data[1]).any(axis=0)]
v = extracted_data[2][:, ~np.isnan(extracted_data[2]).any(axis=0)]

     
data_shape2 = []
for i in range(len(extracted_data)):
    tmp = z.shape
    data_shape2.append(tmp)
    print(r'Remove NAN, Processed data '+data_type[i]+' shape: ', tmp)
      





# save wind speed in a list, note that each element in this list is a numpy array
wspd=[0*i for i in range(len(z))]
for i in range(len(z)):
    wspd[i] = np.sqrt(np.square(u[i]) + np.square(v[i]))
    




##### another way to obtain wspd, but has larger algorithm complexity in time/space
##### I only use it to do verification

##### another way start here #####
# for i in range(10,max_height):
#     for j in range(mat['u'].shape[1]):
#         if not np.isnan(mat['u'][i][j]) and \
#         not np.isnan(mat['v'][i][j]) and \
#         not np.isnan(mat['z'][i][j]):  
#             plt.scatter(math.sqrt(mat['u'][i][j]*mat['u'][i][j] +\
#             mat['v'][i][j]*mat['v'][i][j]), mat['z'][i][j], c='k', s=5) 
# plt.xlabel(r"$\sqrt{u^2+v^2}$", fontsize=15)
# plt.ylabel("z", fontsize=15)  
##### another way end here #####

    




# plot samples and statistics


# find max wind speed
max_ws = 0
for i in range(len(wspd)):
    if np.max(wspd[i])>max_ws:
        max_ws = np.max(wspd[i])
x_max=int((max_ws-(max_ws%10))+wind_speed_interval)
   
for j in range(len(z[0])):
    if j == 0 or j==(len(z[0])-int(len(z[0])/8)) or j==(len(z[0])-int(len(z[0])/4)) \
    or j==(len(z[0])-int(len(z[0])/2)) or j==len(z[0])-1:
        for i in range(max_height-1):
            plt.scatter(wspd[i][j], z[i][j], c='k', s=5)   

        plt.xlabel(r"$\sqrt{u^2+v^2}$", fontsize=15)
        plt.ylabel("z (m)", fontsize=15) 
        plt.xlim([0, x_max])
        plt.ylim([0, max_height*10])
        plt.title('obs data sample '+str(j)+' of the total '+str(len(z[0]))+' available samples')
        plt.savefig('C:/Users/limgr/obs_data_sample_'+str(j)+'.png', dpi=500)
        plt.show()  


    
for i in range(max_height-1):
    #colors = np.random.rand(int(wspd[i].shape[0]))
    plt.scatter(wspd[i], z[i], c='k', s=5)   

plt.xlabel(r"$\sqrt{u^2+v^2}$", fontsize=15)
plt.ylabel("z (m)", fontsize=15)  
plt.xlim([0, x_max])  
plt.ylim([0, max_height*10])  
plt.title('obs data all combined')
plt.savefig('C:/Users/limgr/obs_data_combined.png', dpi=500)
plt.show()      
    



    
wspd_mean = [0*i for i in range(len(wspd))] 
print(len(z), len(z[0]), len(z[1])) 
for i in range(len(z)):
    #(sum(wspd[i]),len(wspd[i]))
    wspd_mean[i] += sum(wspd[i])/len(wspd[i])    
    

for i in range(max_height-1):
    #colors = np.random.rand(int(wspd[i].shape[0]))
    plt.scatter(wspd_mean[i], i*10, c='k', s=5)   

plt.xlabel(r"$\overline{\sqrt{u^2+v^2}}$", fontsize=15)
plt.ylabel("z (m)", fontsize=15)  
plt.xlim([0, x_max]) 
plt.ylim([0, max_height*10])  
plt.title('obs data mean wind profile')  
plt.savefig('C:/Users/limgr/obs_data_wind_profile.png', dpi=500)
plt.show()  

        
        
for i in range(max_height-1):
    #colors = np.random.rand(int(wspd[i].shape[0]))
    plt.scatter(wspd_mean[i], i*10, c='k', s=5)  
        
plt.yscale('log')        
plt.xlabel(r"$\overline{\sqrt{u^2+v^2}}$", fontsize=15)
plt.ylabel("z (m)", fontsize=15)  
plt.xlim([0, x_max])
plt.ylim([0, max_height*10]) 
plt.title('obs data mean wind profile log-linear plot')  
plt.savefig('C:/Users/limgr/obs_data_wind_profile_log.png', dpi=500)
plt.show()     






### split the samples based on wind speed with 10m interval at max_height


bin_number = int(x_max/10)
bins_tmp = []
bin_tmp = wspd[-1]
bin_tmp = np.array(bin_tmp)
right_hand_number = x_max - wind_speed_interval


for i in range(bin_number):
    bins_tmp.append(split_accordingto_row(bin_tmp, bin_tmp[:]>right_hand_number)[0])  
    bin_tmp = [k for k in bin_tmp if k not in bins_tmp[i]]
    bin_tmp = np.array(bin_tmp)
    right_hand_number -= wind_speed_interval
    


bins = []
for i in range(bin_number):
    bins.append(bins_tmp[bin_number-1-i])
    


bins_idx = []
for i in range(bin_number):
    tmp=[]
    for j in range(len(bins[i])):
        if len(np.where(bins[i][j]==wspd[-1])[0])==1:
            tmp.append(int(np.where(bins[i][j]==wspd[-1])[0][0]))
        else:
            for k in range(len(np.where(bins[i][j]==wspd[-1])[0])):
                tmp.append(int(np.where(bins[i][j]==wspd[-1])[0][k]))
    bins_idx.append(tmp)

print('total number of bin index is: '+str(sum([len(arr) for arr in bins_idx])))

# remove duplicated idx
bins_idx_unique = []
for i in range(len(bins_idx)):
    tmp = []
    for j in bins_idx[i]:
        if j not in tmp:
            tmp.append(j)
    bins_idx_unique.append(tmp)

print('remove duplicated ones, the bin indexes are: '+str(bins_idx_unique))
print('remove duplicated ones, total number of bin index is: '+ \
      str(sum([len(arr) for arr in bins_idx_unique])))
if sum([len(arr) for arr in bins_idx_unique])==z.shape[1]:
    print('The total indexes is equal to sample number.')
else:
    sys.exit('Error! The total indexes is not equal to sample number!')



wspd = np.transpose(wspd)

bins_wspd=[]

for j in range(len(bins_idx_unique)):
    tmp=[]
    for k in range(len(bins_idx_unique[j])):
        for i in range(len(wspd)):
            if i==int(bins_idx_unique[j][k]):
                tmp.append(wspd[i])
    bins_wspd.append(tmp)
    
    
for i in range(len(bins_wspd)):
    bins_wspd[i] = np.transpose(bins_wspd[i])
    
    
    
    
    
z = np.transpose(z)    
    
bins_z=[]    

for j in range(len(bins_idx_unique)):
    tmp=[]
    for k in range(len(bins_idx_unique[j])):
        for i in range(len(z)):
            if i==int(bins_idx_unique[j][k]):
                tmp.append(z[i])
    bins_z.append(tmp)
    
    
    
for i in range(len(bins_z)):
    bins_z[i] = np.transpose(bins_z[i])    
    
    
    
# plot bins    
    
    
bin_count=0    
for i in range(len(bins_z)):
    #colors = np.random.rand(int(wspd[i].shape[0]))
    plt.scatter(bins_wspd[i], bins_z[i], c='k', s=5)  
    plt.plot(np.mean(bins_wspd[i], axis=1), np.mean(bins_z[i], axis=1), c='r')
        
    plt.yscale('log')        
    #plt.xlabel(r"$\sqrt{u^2+v^2}$ and ", fontsize=15)
    plt.text(20, 3.85, r"$\sqrt{u^2+v^2}$ &", fontsize=15, color='k')
    plt.text(38, 3.85, r"$\overline{\sqrt{u^2+v^2}}$", fontsize=15, color='r')
    plt.ylabel("z (m)", fontsize=15)  
    plt.xlim([0, x_max])
    plt.ylim([0, max_height*10]) 
    plt.title('obs data bin '+str(bin_count+1))  
    plt.savefig('C:/Users/limgr/obs_data_bin_'+str(bin_count+1)+'_log.png', dpi=500)
    plt.show() 
    bin_count += 1





for i in range(len(bins_z)):
    #colors = np.random.rand(int(wspd[i].shape[0]))
    plt.scatter(bins_wspd[i], bins_z[i], c='k', s=5)  
    plt.plot(np.mean(bins_wspd[i], axis=1), np.mean(bins_z[i], axis=1), c='r')
    bin_count += 1

plt.yscale('log')        
#plt.xlabel(r"$\sqrt{u^2+v^2}$ and ", fontsize=15)
plt.text(20, 3.85, r"$\sqrt{u^2+v^2}$ &", fontsize=15, color='k')
plt.text(38, 3.85, r"$\overline{\sqrt{u^2+v^2}}$", fontsize=15, color='r')
plt.ylabel("z (m)", fontsize=15)  
plt.xlim([0, x_max])
plt.ylim([0, max_height*10]) 
plt.title('obs data all bins')  
plt.savefig('C:/Users/limgr/obs_data_all_bins_log.png', dpi=500)
plt.show() 
   
        