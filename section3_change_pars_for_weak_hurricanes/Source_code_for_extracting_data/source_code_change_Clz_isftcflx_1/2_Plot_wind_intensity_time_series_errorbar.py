import csv
import matplotlib as matplot
import matplotlib.pyplot as plt
import numpy as np

# List the colors that will be used for tracing the track.
colors = ['black','blue','red','green', 'cyan', \
           'gray',  'gold', 'lightcoral', 'turquoise','red','blue','green','pink']
patterns = ['-', '--','--','--','--','--','--','--', ':','-', '--', ':','-', '--', ':',\
            '-.', '-.', '-.', ':', '--', '-']
markers = ['.',',','o','v','8','s','+','x','X','D','^','<','>','v'] 
sizes = [10, 5, 5, 5, 4, 4, 4, 3, 3, 3, 3, 3, 6,5,4,3,2,2]
# Path to the csv file
dir1 = 'C:/Users/limgr/Desktop/Katrina_wind_intensity_8km.csv'
dir2 = 'C:/Users/limgr/Desktop/Maria_wind_intensity_8km.csv'
dir3 = 'C:/Users/limgr/Desktop/Irma_wind_intensity_8km.csv'
dir4 = 'C:/Users/limgr/Desktop/Dorian_wind_intensity_8km.csv'
dir7 = 'C:/Users/limgr/Desktop/Lorenzo_wind_intensity_8km.csv'








c=0
rows=[]
Times=[]
Times=[]
values=[]

with open(dir1, mode='r') as csv_file:
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

for i in range(0,line_count-1):
    if i==0:
        tmp=[float(i)*0.5144444 for i in values[i]]
        #tmp=[float(i) for i in values[i]]
    else:
        tmp=[float(i) for i in values[i]]
    plt.plot( Times0[:5], tmp[:5], color = colors[c], marker='s', linestyle=patterns[c],\
             markersize=sizes[c])
    c+=1


plt.legend(["Real Track", 
            "C0.0001",\
            "C0.01",\
            "C1",\
            "C100"],\
             loc = "upper right", \
    prop={'size': 7})

# plt.legend(["Oussama_NoTurb", "WRF_NoTurb", \
#             "WRFSWAN_NoTurb_swdt600_cpdt600_swgr11p1_swh2",\
#             "WRFSWAN_NoTurb_swdt60_cpdt600_swgr11p1_swh2",\
#             "WRFSWAN_NoTurb_swdt600_cpdt60_swgr11p1_swh2",\
#             "WRFSWAN_NoTurb_swdt600_cpdt600_swgr11p1_swh2",\
#             "WRFSWAN_NoTurb_swdt600_cpdt600_swgr11p1_swh4",\
#             'WRFSWAN_NoTurb_swdt600_cpdt600_swgr32p0_swh2',\
#   'WRFSWAN_NoTurb_swdt600_cpdt3600_swgr11p1_swh2'],loc = "lower center", \
#     prop={'size': 7})
    
# plt.legend(["Oussama_NoTurb", "WRF_NoTurb", \
#             "WRFSWAN_NoTurb_1",\
#             "WRFSWAN_NoTurb_2",\
#             "WRFSWAN_NoTurb_3",\
#             "WRFSWAN_NoTurb_4",\
#             "WRFSWAN_NoTurb_5",\
#             'WRFSWAN_NoTurb_6',\
#   'WRFSWAN_NoTurb_7'],loc = "lower center", \
#     prop={'size': 7})

plt.xlabel("Time Step [hr]", fontsize=14)
plt.ylabel("Intensity", fontsize=14)
plt.title("Katrina Intensity ", {'size': 20})
plt.savefig('C:/Users/limgr/Desktop/katrina_wind_intensity_A.png')
plt.show()

# Save the plot
#plt.savefig('Output.png')







c=0
rows=[]
Times=[]
Times=[]
values=[]

with open(dir2, mode='r') as csv_file:
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

for i in range(0,line_count-1):
    if i==0:
        tmp=[float(i)*0.5144444 for i in values[i]]
        #tmp=[float(i) for i in values[i]]
    else:
        tmp=[float(i) for i in values[i]]
    plt.plot( Times0[:5], tmp[:5], color = colors[c], marker='s', linestyle=patterns[c],\
             markersize=sizes[c])
    c+=1


plt.legend(["Real Track", 
            "C0.0001",\
            "C0.01",\
            "C1",\
            "C100"],\
             loc = "upper right", \
    prop={'size': 7})


plt.xlabel("Time Step [hr]", fontsize=14)
plt.ylabel("Intensity", fontsize=14)
plt.title("Maria Intensity ", {'size': 20})
plt.savefig('C:/Users/limgr/Desktop/maria_wind_intensity_A.png')
plt.show()














c=0
rows=[]
Times=[]
Times=[]
values=[]

with open(dir3, mode='r') as csv_file:
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

for i in range(0,line_count-1):
    if i==0:
        tmp=[float(i)*0.5144444 for i in values[i]]
        #tmp=[float(i) for i in values[i]]
    else:
        tmp=[float(i) for i in values[i]]
    plt.plot( Times0, tmp, color = colors[c], marker='s', linestyle=patterns[c],\
             markersize=sizes[c])
    c+=1


plt.legend(["Real Track", 
            "C0.0001",\
            "C0.01",\
            "C1",\
            "C100"],\
             loc = "upper right", \
    prop={'size': 7})


plt.xlabel("Time Step [hr]", fontsize=14)
plt.ylabel("Intensity", fontsize=14)
plt.title("Irma Intensity ", {'size': 20})
plt.savefig('C:/Users/limgr/Desktop/irma_wind_intensity_A.png')
plt.show()













c=0
rows=[]
Times=[]
Times=[]
values=[]

with open(dir4, mode='r') as csv_file:
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

for i in range(0,line_count-1):
    if i==0:
        tmp=[float(i)*0.5144444 for i in values[i]]
        #tmp=[float(i) for i in values[i]]
    else:
        tmp=[float(i) for i in values[i]]
    plt.plot( Times0[:-2], tmp[:-2], color = colors[c], marker='s', linestyle=patterns[c],\
             markersize=sizes[c])
    c+=1


plt.legend(["Real Track", 
            "C0.0001",\
            "C0.01",\
            "C1",\
            "C100"],\
             loc = "upper right", \
    prop={'size': 7})



plt.xlabel("Time Step [hr]", fontsize=14)
plt.ylabel("Intensity", fontsize=14)
plt.title("Dorian Intensity ", {'size': 20})
plt.savefig('C:/Users/limgr/Desktop/dorian_wind_intensity_A.png')
plt.show()










c=0
rows=[]
Times=[]
Times=[]
values=[]

with open(dir7, mode='r') as csv_file:
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

for i in range(0,line_count-1):
    if i==0:
        tmp=[float(i)*0.5144444 for i in values[i]]
        #tmp=[float(i) for i in values[i]]
    else:
        tmp=[float(i) for i in values[i]]
    plt.plot( Times0, tmp, color = colors[c], marker='s', linestyle=patterns[c],\
             markersize=sizes[c])
    c+=1


plt.legend(["Real Track", 
            "C0.0001",\
            "C0.01",\
            "C1",\
            "C100"],\
             loc = "upper right", \
    prop={'size': 7})



plt.xlabel("Time Step [hr]", fontsize=14)
plt.ylabel("Intensity", fontsize=14)
plt.title("Lorenzo Intensity ", {'size': 20})
plt.savefig('C:/Users/limgr/Desktop/lorenzo_wind_intensity_A.png')
plt.show()












rows1=[]
Times1=[]
Times1=[]
values1=[]

rows2=[]
Times2=[]
Times2=[]
values2=[]

rows3=[]
Times3=[]
Times3=[]
values3=[]

rows4=[]
Times4=[]
Times4=[]
values4=[]

rows5=[]
Times5=[]
Times5=[]
values5=[]

rows6=[]
Times6=[]
Times6=[]
values6=[]

rows7=[]
Times7=[]
Times7=[]
values7=[]

# Set the working space.
#os.chdir(Dir_Output)

# Initiate the varaibles that will contain the output files.
#Forecast_Outputs_NoTurb = ""
#Real_Output = ""

#########################################################################
# This function returns a list of all the files in the output directory.#
#########################################################################

#def list_files (Dir, Forecast_Outputs_NoTurb, Real_Output):
#  for f in os.listdir(Dir):
#    if (f == "Real_Output.csv"):
#      Real_Output = f
#    elif (f.find('NoTurb') != -1):
#      Forecast_Outputs_NoTurb = f
#  return (Forecast_Outputs_NoTurb, Real_Output)


# Calling the list_files function to classify files according to the turbulence model
#(Forecast_Outputs_NoTurb, Real_Output) = list_files (Dir_Output, Forecast_Outputs_NoTurb, Real_Output)
#print (Real_Output)
#print (Forecast_Outputs_Smag2D)
#print (Forecast_Outputs_NoTurb)

###################################################################
# This function returns a list of wind speed for each output file.#
###################################################################


real1_track=[]
oussama1=[]
wrf1=[]

with open(dir1, mode='r') as csv_file:
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








real2_track=[]
oussama2=[]
wrf2=[]

with open(dir2, mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    line_count = 0
    sim_count = 0
    for row in csv_reader:
        if line_count == 0:
            print(f'Column names are {", ".join(row)}')
            Times2.append(list(row.keys()))
            real2_track.append(list(row.values()))
            line_count += 1
        else:
            rows2.append(row)
            values2.append(list(row.values()))
            line_count += 1
    print('There is totally ',(line_count-1)*(len(row)),' data points')
simu2=np.array(values2, dtype=np.float32)
real2=np.array(real2_track, dtype=np.float32)
real2=real2*0.5144444
real2=real2
simu_error2=abs(simu2-real2[:,None])/real2[:,None]#/((line_count-3)*(len(row)))
print('absolute pressure error')
print(abs(simu2-real2[:,None]))


















real3_track=[]
oussama3=[]
wrf3=[]

with open(dir3, mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    line_count = 0
    sim_count = 0
    for row in csv_reader:
        if line_count == 0:
            print(f'Column names are {", ".join(row)}')
            Times3.append(list(row.keys()))
            real3_track.append(list(row.values()))
            line_count += 1
        else:
            rows3.append(row)
            values3.append(list(row.values()))
            line_count += 1
    print('There is totally ',(line_count-1)*(len(row)),' data points')
simu3=np.array(values3, dtype=np.float32)
real3=np.array(real3_track, dtype=np.float32)
real3=real3*0.5144444
real3=real3
simu_error3=abs(simu3-real3[:,None])/real3[:,None]#/((line_count-3)*(len(row)))
print('absolute pressure error')
print(abs(simu3-real3[:,None]))


















real4_track=[]
oussama4=[]
wrf4=[]

with open(dir4, mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    line_count = 0
    sim_count = 0
    for row in csv_reader:
        if line_count == 0:
            print(f'Column names are {", ".join(row)}')
            Times4.append(list(row.keys()))
            real4_track.append(list(row.values()))
            line_count += 1
        else:
            rows4.append(row)
            values4.append(list(row.values()))
            line_count += 1
    print('There is totally ',(line_count-1)*(len(row)),' data points')
simu4=np.array(values4, dtype=np.float32)
real4=np.array(real4_track, dtype=np.float32)
real4=real4*0.5144444
real4=real4
simu_error4=abs(simu4-real4[:,None])/real4[:,None]#/((line_count-3)*(len(row)))
print('absolute pressure error')
print(abs(simu4-real4[:,None]))










real7_track=[]
oussama7=[]
wrf7=[]

with open(dir7, mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    line_count = 0
    sim_count = 0
    for row in csv_reader:
        if line_count == 0:
            print(f'Column names are {", ".join(row)}')
            Times7.append(list(row.keys()))
            real7_track.append(list(row.values()))
            line_count += 1
        else:
            rows7.append(row)
            values7.append(list(row.values()))
            line_count += 1
    print('There is totally ',(line_count-1)*(len(row)),' data points')
simu7=np.array(values7, dtype=np.float32)
real7=np.array(real7_track, dtype=np.float32)
real7=real7*0.5144444
real7=real7
simu_error7=abs(simu7-real7[:,None])/real7[:,None]#/((line_count-3)*(len(row)))
print('absolute pressure error')
print(abs(simu7-real7[:,None]))














#ouss_all=np.append(ouss1[0][:],ouss2[0][:],ouss3[0][:],ouss4[0][:],axis=0)
#error_all=np.append(error1[0][1][:],error2[0][1][:],error3[0][1][:],error4[0][1][:], axis=0)
ouss_error=np.zeros((4, 4))
wrf_error=np.zeros((4, 4))
par1_error=np.zeros((4, 4))
par2_error=np.zeros((4, 4))
par3_error=np.zeros((4, 4))
par4_error=np.zeros((4, 4))
par5_error=np.zeros((4, 4))
# par6_error=np.zeros((4, 9))
# par7_error=np.zeros((4, 9))
# par8_error=np.zeros((4, 9))
# par9_error=np.zeros((4, 9))


# print(np.shape(values4))
# print(np.shape(error4))
# print(ouss_error)
# print(simu_error)





# par1_error[0]=simu_error1[0][0][:]
# par1_error[1]=simu_error2[0][0][:]
# par1_error[2]=simu_error3[0][0][:]
# par1_error[3]=simu_error4[0][0][:]
# par1_error[4]=simu_error5[0][0][:]
# par1_error[5]=simu_error6[0][0][:]
par1_error=np.concatenate((simu_error1[0][0][0:5],simu_error2[0][0][:],\
                           simu_error3[0][0][:],simu_error4[0][0][:-2],simu_error7[0][0][:]))
par1_error=par1_error.flatten()
par1_error_mean=np.mean(par1_error)
par1_error_std=np.std(par1_error)





# par2_error[0]=simu_error1[0][1][:]
# par2_error[1]=simu_error2[0][1][:]
# par2_error[2]=simu_error3[0][1][:]
# par2_error[3]=simu_error4[0][1][:]
# par2_error[4]=simu_error5[0][1][:]
# par2_error[5]=simu_error6[0][1][:]
par2_error=np.concatenate((simu_error1[0][1][0:5],simu_error2[0][1][:],\
                           simu_error3[0][1][:],simu_error4[0][1][:-2],simu_error7[0][1][:]))
par2_error=par2_error.flatten()
par2_error_mean=np.mean(par2_error)
par2_error_std=np.std(par2_error)






# par3_error[0]=simu_error1[0][2][:]
# par3_error[1]=simu_error2[0][2][:]
# par3_error[2]=simu_error3[0][2][:]
# par3_error[3]=simu_error4[0][2][:]
# par3_error[4]=simu_error5[0][2][:]
# par3_error[5]=simu_error6[0][2][:]
par3_error=np.concatenate((simu_error1[0][2][0:5],simu_error2[0][2][:],\
                           simu_error3[0][2][:],simu_error4[0][2][:-2],simu_error7[0][2][:]))
par3_error=par3_error.flatten()
par3_error_mean=np.mean(par3_error)
par3_error_std=np.std(par3_error)






# par4_error[0]=simu_error1[0][3][:]
# par4_error[1]=simu_error2[0][3][:]
# par4_error[2]=simu_error3[0][3][:]
# par4_error[3]=simu_error4[0][3][:]
# par4_error[4]=simu_error5[0][3][:]
# par4_error[5]=simu_error6[0][3][:]
par4_error=np.concatenate((simu_error1[0][3][0:5],simu_error2[0][3][:],\
                           simu_error3[0][3][:],simu_error4[0][3][:-2],simu_error7[0][3][:]))
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
ax.set_ylabel('Intensity')
ax.set_xticks(x_pos)
ax.set_xticklabels(hurricanes)
ax.set_title('Hurricanes')
ax.yaxis.grid(True)
for i, v in enumerate(CTEs):
    ax.text(i, v+0.02, str(round(v, 3)), color='red', fontweight='bold')
# Save the figure and show
fig.autofmt_xdate()
plt.tight_layout()
#plt.savefig('wind_intensity_bar_plot.png')
plt.savefig('C:/Users/limgr/Desktop/wind_intensity_bar_plot.png')
plt.show()


