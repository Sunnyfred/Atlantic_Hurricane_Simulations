import csv
import matplotlib.pyplot as plt
import numpy as np


file = open("C:/Users/limgr/Desktop/Katrina_wind_profiles_8km.csv")
csvreader = csv.reader(file)
header = next(csvreader)

rows = []
for row in csvreader:
    rows.append(row)
rows = [[float(i) for i in row] for row in rows]
print(rows)
file.close()





file = open("C:/Users/limgr/Desktop/Vel_data_Eye.csv")
csvreader = csv.reader(file)
header = next(csvreader)

rows22 = []
for row in csvreader:
    rows22.append(row)
rows22 = [[float(i) for i in row] for row in rows22]
print(rows22)
file.close()

# function used to transpose 2D list
def transpose(l1, l2):
    for i in range(len(l1[0])):
        # print(i)
        row =[]
        for item in l1:
            row.append(item[i])
        l2.append(row)
    return l2
 
# Driver code

rows2 = []
print(transpose(rows22, rows2))


#colors = np.random.rand(len(rows[0]))
plt.scatter(rows[1], rows[0], c='r', s=15, label=r'$u_r-Meng.py$') 
plt.plot(rows2[1], rows2[0], c='r', label=r'$u_r-micheikh.ncl$')   
plt.scatter(rows[2], rows[0], c='k', s=15, label=r'$u_{\theta}-Meng.py$')   
plt.plot(rows2[2], rows2[0], c='k', label=r'$u_{\theta}-micheikh.ncl$') 
plt.legend()
plt.ylim([0, 5000]) 
plt.legend()

plt.savefig('C:/Users/limgr/Desktop/comparison.png', dpi=500)
plt.show()

