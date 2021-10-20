import csv
import matplotlib as matplot
import matplotlib.pyplot as plt
import numpy as np

# List the colors that will be used for tracing the track.
colors = ['blue','red','green', 'cyan', 'brown', \
           'gray',  'gold', 'lightcoral', 'green','red','blue','green','pink']
patterns = ['-', '--','--','--','--','--','--','--', ':','-', '--', ':','-', '--', ':',\
            '-.', '-.', '-.', ':', '--', '-']
markers = ['.',',','o','v','8','s','+','x','X','D','^','<','>','v'] 
sizes = [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5,4,3,2,2]
# Path to the csv file
dir1 = 'C:/Users/limgr/Desktop/Katrina_ZNT.csv'
dir3 = 'C:/Users/limgr/Desktop/Maria_ZNT.csv'
dir4 = 'C:/Users/limgr/Desktop/Irma_ZNT.csv'
dir5 = 'C:/Users/limgr/Desktop/Dorian_ZNT.csv'
dir7 = 'C:/Users/limgr/Desktop/Lorenzo_ZNT.csv'








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
        #tmp=[float(i)*0.5144444 for i in values[i]]
        tmp=[float(i) for i in values[i]]
    else:
        tmp=[float(i) for i in values[i]]
    plt.plot( Times0[:5], tmp[:5], color = colors[c], marker='s', linestyle=patterns[c],\
              markersize=sizes[c])
    c+=1


plt.legend(["C0.0001", 
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
plt.yscale("log")
plt.xlabel("Time Step [hr]", fontsize=14)
plt.ylabel("Z0", fontsize=14)
plt.title("Katrina Surface Roughness ", {'size': 20})
plt.savefig('C:/Users/limgr/Desktop/katrina_ZNT_A.png')
plt.show()

# Save the plot
#plt.savefig('Output.png')
















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
        #tmp=[float(i)*0.5144444 for i in values[i]]
        tmp=[float(i) for i in values[i]]
    else:
        tmp=[float(i) for i in values[i]]
    plt.plot( Times0, tmp, color = colors[c], marker='s', linestyle=patterns[c],\
              markersize=sizes[c])
    c+=1


plt.legend(["C0.0001", 
            "C0.01",\
            "C1",\
            "C100"],\
              loc = "upper right", \
    prop={'size': 7})

plt.yscale("log")
plt.xlabel("Time Step [hr]", fontsize=14)
plt.ylabel("Z0", fontsize=14)
plt.title("Maria Surface Roughness ", {'size': 20})
plt.savefig('C:/Users/limgr/Desktop/maria_ZNT_A.png')
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
        #tmp=[float(i)*0.5144444 for i in values[i]]
        tmp=[float(i) for i in values[i]]
    else:
        tmp=[float(i) for i in values[i]]
    plt.plot( Times0, tmp, color = colors[c], marker='s', linestyle=patterns[c],\
              markersize=sizes[c])
    c+=1


plt.legend(["C0.0001", 
            "C0.01",\
            "C1",\
            "C100"],\
              loc = "upper right", \
    prop={'size': 7})


plt.yscale("log")
plt.xlabel("Time Step [hr]", fontsize=14)
plt.ylabel("Z0", fontsize=14)
plt.title("Irma Surface Roughness ", {'size': 20})
plt.savefig('C:/Users/limgr/Desktop/irma_ZNT_A.png')
plt.show()














c=0
rows=[]
Times=[]
Times=[]
values=[]

with open(dir5, mode='r') as csv_file:
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
        #tmp=[float(i)*0.5144444 for i in values[i]]
        tmp=[float(i) for i in values[i]]
    else:
        tmp=[float(i) for i in values[i]]
    plt.plot( Times0, tmp, color = colors[c], marker='s', linestyle=patterns[c],\
              markersize=sizes[c])
    c+=1


plt.legend(["C0.0001", 
            "C0.01",\
            "C1",\
            "C100"],\
              loc = "upper right", \
    prop={'size': 7})


plt.yscale("log")
plt.xlabel("Time Step [hr]", fontsize=14)
plt.ylabel("Z0", fontsize=14)
plt.title("Dorian Surface Roughness ", {'size': 20})
plt.savefig('C:/Users/limgr/Desktop/dorian_ZNT_A.png')
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
        #tmp=[float(i)*0.5144444 for i in values[i]]
        tmp=[float(i) for i in values[i]]
    else:
        tmp=[float(i) for i in values[i]]
    plt.plot( Times0, tmp, color = colors[c], marker='s', linestyle=patterns[c],\
              markersize=sizes[c])
    c+=1


plt.legend(["C0.0001", 
            "C0.01",\
            "C1",\
            "C100"],\
              loc = "upper right", \
    prop={'size': 7})


plt.yscale("log")
plt.xlabel("Time Step [hr]", fontsize=14)
plt.ylabel("Z0", fontsize=14)
plt.title("Lorenzo Surface Roughness ", {'size': 20})
plt.savefig('C:/Users/limgr/Desktop/lorenzo_ZNT_A.png')
plt.show()




















