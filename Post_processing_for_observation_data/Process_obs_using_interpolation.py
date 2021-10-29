import scipy.io
from sklearn.linear_model import LinearRegression
import sys
import numpy as np
import matplotlib.pyplot as plt
import math
import sys
from scipy import interpolate
from sklearn.linear_model import LinearRegression


# user input variavles
filename = ['Lorenzo_0927_0929.mat','Maria_0922_0923.mat','Katrina_0828.mat',\
            'Joaquin_1004_1006.mat','Irma_sonde0902_03.mat','Ike_0910_0912.mat',\
            'Dorian_sonde0831_0901.mat','Cristobal_0826_0828.mat']
filename = ['Dorian_sonde0831_0901.mat','Irma_sonde0902_03.mat','Katrina_0828.mat',\
            'Maria_0922_0923.mat','Lorenzo_0927_0929.mat']
#filename = ['Katrina.mat','Irma.mat','Gustav.mat','Maria.mat']
#filename = ['Ike_0910_0912.mat']
max_height = 8 # max_height + 1, level not meter
data_type = ['z', 'u', 'v'] # extracted data types, expect 3
colors = ['green', 'coral', 'purple', 'grey', 'cyan', 'orange', 'red', 'pink']
wind_speed_interval = 10 # speed inernal for bins, in meter/s
polynomial_power = 6  # polynomial fitting power
height_step = 0.1    # height step for polynomial fitting, unit m
include_profile_missing_data = 1 # consider profiles missing data or not
                                 # 1: not include
                                 # 0<=x<1: include profile contains at least x*100 % data points
                                 # other: error
obs_data_hegith_inteval = 25     # based on observation data, do not change
velocity_bins_criterion_height = 200 # create velicty bins bases on this height, unit m


interpolated_lowest_position = 50




'''
Create and initialize velocity bins
'''    
## results stores in dictionary bins, suppose wins speed in hurricane will not exceed 100 m/s
bins = {}
z_bins = {}
for i in range(wind_speed_interval, 100+wind_speed_interval, wind_speed_interval):
    bins[i] = []
    z_bins[i] = []
    
'''
Create and initialize scatter dictionary
'''    
scatter_wspd = {}
scatter_z = {}
for i in range(len(filename)):
    scatter_wspd[i] = []
    scatter_z[i] = []



for fi in range(len(filename)):
    




    # load observation data
    mat = scipy.io.loadmat(filename[fi])
    print(mat.keys())




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
    
    
    
    '''    
    get the height_idx and sample_idx for all NAN data points 
    
    sample_idx is 1D list that contains dropesonde index for non-NAN 
    
    height_idx is 2D list, position 0 is the dropesonde index, position 1 is
    the non-NAN data height index for each dropsonde
    '''    

    height_idx0 = [[] for _ in range(int(data_shape[0][1]))]     
    for i in range(int(data_shape[0][1])):
        for j in range(int(data_shape[0][0])):
            if not np.isnan(extracted_data[0][j,i]) and \
                not np.isnan(extracted_data[1][j,i]) and  \
                    not np.isnan(extracted_data[2][j,i]):
                        height_idx0[i].append(j)
   

    sample_idx = []
    height_idx = []
    for i in range(len(height_idx0)):
        if (include_profile_missing_data==1):
            if(len(height_idx0[i])==int(data_shape[0][0])):
                sample_idx.append(i)
                height_idx.append(height_idx0[i])  
        elif (0<=include_profile_missing_data<1):
            if(len(height_idx0[i])>=int(data_shape[0][0])*include_profile_missing_data):
                sample_idx.append(i)
                height_idx.append(height_idx0[i])           
        else:
            sys.exit("include_profile_missing_data is not valid, choose a value between [0, 1]")
        
        


    '''
    calculate wind speed based on sample and height idxes,
    wind speed= sqrt(u^2+v^2)
    '''
    
    
    wspd = [[] for _ in range(len(sample_idx))]  
    z = [[] for _ in range(len(sample_idx))] 
    count = 0
    for i in sample_idx:
        for j in height_idx[count]:
            tmp1 = math.sqrt((extracted_data[1][j,i])*(extracted_data[1][j,i])\
                             +(extracted_data[2][j,i])*(extracted_data[2][j,i]))
            tmp2 = extracted_data[0][j,i]
            wspd[count].append(tmp1)
            z[count].append(tmp2)
        count += 1
            


        
    '''
    curve-fitting for each sample
    '''


    # find max wind speed
    max_ws = 0
    for i in range(len(wspd)):
        if np.max(wspd[i])>max_ws:
            max_ws = np.max(wspd[i])
    x_max=int((max_ws-(max_ws%10))+wind_speed_interval)
    # print(x_max)
    # for i in range(len(wspd)):
    #     print(len(wspd[i]))




    '''
    plot extracted data points and fitted curves
    '''


    f = {}
    z_new = z
    wspd_new = wspd
    # scatter_wspd[filename[fi]] = wspd
    # scatter_z[filename[fi]] = z
    for i in range(len(sample_idx)):
    #for kk in range(1):
    #    i=rd
        #plt.scatter(wspd[i], z[i], c='k', s=9)
        # calculate polynomial
        #f[i] = np.poly1d(np.polyfit( z_new[i], wspd_new[i], polynomial_power))
        f[i] = interpolate.interp1d(z[i], wspd[i], fill_value='extrapolate')
        
        # calculated new variables based on polynomial function
        z_new[i] = np.linspace(obs_data_hegith_inteval, (max_height-1)*obs_data_hegith_inteval, \
                int(float(max_height-1)*obs_data_hegith_inteval/height_step))
        wspd_new[i] = f[i](z_new[i])
        
         
        # plt.plot(wspd_new[i], z_new[i], c=colors[fi], linewidth=1, linestyle='dashed') 
        # #plt.xlim([0, x_max])
        # #plt.ylim([0, max_height*obs_data_hegith_inteval])  
        # #plt.title(filename[fi])
        
        # plt.xlim([0, 80])
        # plt.ylim([-10, 210]) 
        # #plt.show()
        

        

    '''
    Update velocity bins and average over each bin
    '''    

    

    ### split the samples based on wind speed with 10m interval at max_height


    bin_number = int(x_max/wind_speed_interval)
    
    bin_borders = []
    for i in range(bin_number+1):
        bin_borders.append(i*wind_speed_interval)
    
    
    for j in range(1,bin_number+1):
        tmp = [] 
        tmp_z = [] 
        for i in range(len(wspd_new)):
            if (bin_borders[j-1] <= wspd_new[i][-1] < bin_borders[j]):  # based on top wind speed
                tmp.append(wspd_new[i])
                tmp_z.append(z_new[i])
        bins[bin_borders[j]].extend(tmp)
        z_bins[bin_borders[j]].extend(tmp_z)
            

    if (fi==len(filename)-1):
        wspd_means = []
        z_means = []
        for key in bins:
            if key!= 10 and key<=80:
                if (len(z_bins[key]) != 0):
                        # print(bins[key])
                        wspd_means.append(sum(bins[key])/len(bins[key]))
                        z_means.append(sum(z_bins[key])/len(z_bins[key]))
                        # plt.plot(np.mean(bins[key],axis=0), \
                        #   np.mean(z_bins[key],axis=0), \
                        #       c='k', linewidth=2)   
                        plt.scatter(np.mean(bins[key],axis=0)[::200], \
                          np.mean(z_bins[key],axis=0)[::200], \
                              c='k') 
                        # bins0 = bins[key][::200]
                        # z_bins0 = z_bins[key][::200]
                        # plt.errorbar(np.mean(bins0,axis=1), \
                        #   np.mean(z_bins0,axis=1), yerr=np.std(z_bins0,axis=1))
                        # plt.errorbar(x, y + 3, yerr=yerr, label='both limits (default)')
                else:
                    continue


        # plt.yscale('log')        
# #plt.xlabel(r"$\sqrt{u^2+v^2}$ and ", fontsize=15)
# plt.text(20, 3.85, r"$\sqrt{u^2+v^2}$ &", fontsize=15, color='k')
# plt.text(38, 3.85, r"$\overline{\sqrt{u^2+v^2}}$", fontsize=15, color='r')
# plt.ylabel("z (m)", fontsize=15)  
        # plt.xlim([0, 100])
        # plt.ylim([-10, 210])  
# plt.title('obs data all bins')  
        # plt.savefig('C:/Users/limgr/obs_data_all_bins_log.png', dpi=500)
    #plt.show() 
   
# print(wspd_means)
# print(len(wspd_means))   
# print(len(wspd_means[0]))  


# f2={}
# for i in range(len(wspd_means)):
#     f2[i] = interpolate.interp1d(z_means[i], wspd_means[i], fill_value='extrapolate')
#     print(f2[i](10))
#     plt.scatter(f2[i](10), 10, c='r', s=9) 
    
    
    

### linear regression

# print(wspd_means[0])
# print(np.log(z_means[0]))    
# wspd_means0=[]
# for i in range(len(wspd_means)):
#     wspd_means0.append(LinearRegression().fit(np.array(wspd_means[i]).reshape(-1, 1), \
#                                               np.log(z_means[0])))
        
        
# for i in range(len(wspd_means)):
#     line = np.linspace(-10, 20+i*10, 1000, endpoint=False).reshape(-1, 1)
#     plt.plot(line, np.exp(wspd_means0[i].predict(line)), linewidth=2, color="green", \
#               label = 'linear regression')


# plt.xlim([0, 80])
# plt.ylim([0, 500])    
# plt.show()
# plt.savefig('C:/Users/limgr/obs_data_all_bins.png', dpi=500)



print(wspd_means[0])
print(np.log(z_means[0]))    
wspd_means0=[]
wspd_10=[]
for i in range(len(wspd_means)):
    wspd_means0.append(LinearRegression().fit(np.array(wspd_means[i]).reshape(-1, 1), \
                                              np.log(z_means[0])))
    #print('linear regression coeff: '+str(wspd_means0[i].coef_)\
    #      +', intercept: '+str(wspd_means0[i].intercept_))
    print('speed range '+str(i)+' 10m wind speed is: '+\
          str((np.log(10)-wspd_means0[i].intercept_)/wspd_means0[i].coef_))
    wspd_10.append((np.log(10)-wspd_means0[i].intercept_)/wspd_means0[i].coef_)
        
roughness=[]        
for i in range(len(wspd_means)):
    roughness.append(np.exp(wspd_means0[i].predict(np.array([0]).reshape(-1,1)))[0])
    line = np.linspace(-10, 20+i*10, 1000, endpoint=False).reshape(-1, 1)
    plt.plot(line, np.exp(wspd_means0[i].predict(line)), linewidth=2, color="green", \
              label = 'linear regression')
    # for j in range(len(line)):
    #     if np.exp(wspd_means0[i].predict(line[j]))==10:
    #         print('speed range '+str(i)+' 10 meter velocity is: '+str(line[j]))
        
    print('roughness for velocity between '+str(10+10*i)+' m/s and '+\
    str(20+10*i)+' m/s is: ', np.exp(wspd_means0[i].predict(np.array([0]).reshape(-1,1))))
        
# z_means0=[]
# for i in range(len(z_means)):
#     z_means0.append(LinearRegression().fit(np.log(np.array(z_means[i])).reshape(-1, 1), \
#                                               wspd_means[i]))
# print(len(z_means))
        
# for i in range(len(z_means)):
#     line = np.linspace(0, i*25, 1000, endpoint=False).reshape(-1, 1)
#     plt.plot(z_means0[i].predict(line), np.exp(line),  linewidth=2, color="green")
#     print('10 m velocity', z_means0[i].predict(np.array([10]).reshape(-1,1)))       
     

plt.yscale('log')
plt.xlim([0, 80])
plt.ylim([10, 500])    
plt.savefig('C:/Users/limgr/obs_data_all_bins.png', dpi=500)
plt.show()




### plot roughness
for i in range(len(wspd_means)):
    plt.scatter(wspd_10[i], roughness[i], linewidth=2, color="green")

plt.yscale('log')  
plt.savefig('C:/Users/limgr/obs_data_all_roughnessvsu10.png', dpi=500)
plt.show()




### evaluate and plot u*, u* = kappa*u10/ln(10/z0)
ustar = []
for i in range(len(roughness)):
    ustar.append(wspd_10[i]*0.41/np.log(10/roughness[i]))
for i in range(len(roughness)):
    plt.scatter(wspd_10[i], ustar[i], linewidth=2, color="green")
#plt.yscale('log')  
plt.savefig('C:/Users/limgr/obs_data_all_ustarvsu10.png', dpi=500)
plt.show()

    


### evaluate and plot cd*, cd = u*^2/u10^2
for i in range(len(roughness)):
    plt.scatter(wspd_10[i], ustar[i]*ustar[i]/wspd_10[i]/wspd_10[i], linewidth=2, color="green")
#plt.yscale('log')  
plt.savefig('C:/Users/limgr/obs_data_all_cdvsu10.png', dpi=500)
plt.show()

