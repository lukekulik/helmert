import csv
import numpy as np
from main import main, computer
import matplotlib.pyplot as plt


def stationyeardataV2(Averages, stationname):  # by lukasz
    out = Averages[np.where(Averages[:, 0] == stationname)]
    return out


year = 'dataset/year'  # define year to be studied (directory in filelist)
yearITRF = 'ITRF/ITRF'

startyear = 2005
endyear = 2007

# data1=np.array([])
data1 = np.array(['station_name', 'x_coord', 'y_coord', 'z_coord', 'weeknumber', 'year'])


REFyear = int((endyear + startyear) / 2.)  # determine reference year
REF1 = year + str(REFyear)  # ref year of coordinates
REF2 = yearITRF + str(REFyear)  # ref year of ITRF

NEWposition_ITRF = main(REF1, REF2)  # call year with reference year

allstationnames = np.unique(NEWposition_ITRF[:, 0])  # create list of all stationnames

# create array for reference coordinates
REFcoordinates = np.array(9 * len(allstationnames) * [0], dtype="S20").reshape(len(allstationnames), 9)
# maybe a zombie station culprit
#   but are zombie stations the median stations, that all other stations are referanced from?

# loop to receive REFcoordinate for every station
for station in range(len(allstationnames)):
    stationcoordinates = NEWposition_ITRF[NEWposition_ITRF[:, 0] == allstationnames[station]]
    REFcoord = stationcoordinates[int(len(stationcoordinates) / 2.), :]
    REFcoordinates[station] = REFcoord


# loop every year through main function to get transformed position using ITRF
for i in range(startyear, endyear + 1):
    str1 = year + str(i)
    str2 = yearITRF + str(i)
    print "Start computing year:", str1
    NEWposition_ITRF = main(str1, str2)
    
    # loop every year together with reference coordinates through computer to receive ENU
    # print REFcoordinates[REFcoordinates[:,0] == 'ALGO']
    # print NEWposition_ITRF[NEWposition_ITRF[:,0] == 'ALGO']
    REFcoordinates,ENU_Pos = computer(REFcoordinates,NEWposition_ITRF)
    data1 = np.vstack((data1, ENU_Pos))

    print "Finished computing year:", str1
    #### using vstack to get all solutions of year underneath each other, so we can use csv writer

#np.save(data,data1)

temp=data1[data1==ALGO]
xaxis=data1[:,5]+data1[:,4]/52.

plt.plot(xaxis,temp[:,1])
plt.show()


'''
# if permission denied - change filename to sth else
csvfile = open('result2.csv', 'w')
# creating a csv file to store dataa in, REMARK: don't use same filename multiple times, will give an error of 
fieldnames = ['station_name', 'lon', 'lat', 'height', 'weeknumber', 'year']
# start writing procuder
writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

# write ever row into csv file
writer.writeheader()
for i in range((len(data1)) - 1):
    writer.writerow(
        {'station_name': data1[i + 1][0], 'lon': data1[i + 1][1], 'lat': data1[i + 1][2], 'height': data1[i + 1][3],
         'weeknumber': data1[i + 1][4], 'year': data1[i + 1][5]})
csvfile.close()  # release the file from Python
'''