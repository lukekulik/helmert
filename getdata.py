import numpy as np

from yearsplitter import yearsplitterITRF

# import pandas as pd

##################

def getdata1(name):
    f1 = open(name, 'r')
    n1 = int(((f1.readline()).split())[
                 0])  # number of entries in f1, reads the number at begin of file about amount of entries

    data = f1.readlines()

    data = data[0:]  # deletes

    result = np.genfromtxt(data, usecols=(1, 4, 6), skip_footer=n1, dtype=[('1', 'a4'), ('4', 'f8'), (
    '6', 'f8')])  # gets the station name, coordinate and deviations

    return result


##################

def getdata2(name):
    f1 = open(name, 'r')
    n1 = int(((f1.readline()).split())[
                 0])  # number of entries in f1, reads the number at begin of file about amount of entries

    data2 = f1.readlines()

    data2 = data2[0:]  # deletes

    result2 = np.genfromtxt(data2, usecols=2, skip_header=n1,
                            dtype='f8')  # gets the coorealations between the different coordinates

    return result2


##################

def getdataITRF(name):  ### reads ITRF files, removes both corrolations and x,y,z VEL entries
    f1 = open(name, 'r')
    n1 = f1.next()
    n1 = int(n1[2:5])
    f1.close()

    with open(name) as myfile:
        head = [next(myfile) for x in xrange(n1)]
    # print head
    dataITRF = np.genfromtxt(head, usecols=(1, 4, 6), dtype=[('1', 'a4'), ('4', 'f8'), ('6', 'f8')], skip_header=1)

    dataITRF = dataITRF[0:]  # deletes

    # deleteindex = []    # create array for indexes to be deleted from ITRF array, x,y,z VEL entries
    xindex = np.arange(3, n1 - 2, 6)
    yindex = np.arange(4, n1 - 1, 6)
    zindex = np.arange(5, n1, 6)
    deleteindex = np.concatenate((xindex, yindex, zindex))  # combines indexes to one array, unsorted

    dataITRF = np.delete(dataITRF, deleteindex)  # deletes x,y,z VEL entries, left with x,y,z STA entries

    return dataITRF


##################

def readITRFyear(yearITRF):  # Uses the function getdataITRF and extracts all
    weeksITRF = yearsplitterITRF(yearITRF)  # useful data from all ITRF files in specified folder.
    # Output array structure: [[(sta,x,unc),(sta,y,unc),...],[week2],...]
    datayearITRF = []

    for weekITRF in weeksITRF:
        dataITRF = getdataITRF(yearITRF + "/" + weekITRF)
        datayearITRF.append(dataITRF)

    return datayearITRF

    ##################

    # def readITRFyear_correlation(yearITRF):
    #     weeksITRF = yearsplitterITRF(yearITRF)

    #     datayearITRF = len(weeksITRF)*[0]

    #     for weekITRF in range(len(weeksITRF)):
    #         #print weekITRF
    #         dataITRF = getdata2ITRF_panda(yearITRF + "/" + weeksITRF[weekITRF])
    #         datayearITRF[weekITRF]=dataITRF

    #     return datayearITRF

    ##################

    # def getdata2ITRF_panda(name):   # optimized correlations by lukasz
    #     f1 = open(name,'r')
    #     n1 = f1.next()
    #     #print name
    #     n1 = int(n1[2:5])
    #     n2 = n1*(n1+1)/2-n1

    #     result2 = pd.read_csv(name, names=['A', 'B', 'correlations'],skiprows=n1+1,delim_whitespace=True)

    #     xindex = np.arange(4,n1+1,6)
    #     yindex = np.arange(5,n1+1,6)
    #     zindex = np.arange(6,n1+1,6)
    #     deleteindex = np.sort(np.concatenate((xindex,yindex,zindex))) # generating list of values (vel) to be deleted

    #     result3=result2[result2.A.isin(deleteindex)==0] # removing velocity values
    #     result4=result3[result3.B.isin(deleteindex)==0]

    #     df2 = result4.pivot(index='A', columns='B', values='correlations')

    #     # possibly slow:
    #     corr = df2.values.tolist()
    #     corr.insert(0, [np.nan] * len(corr))
    #     corr = pd.DataFrame(corr)
    #     corr[len(corr) - 1] = [np.nan] * len(corr)
    #     for i in range(len(corr)): #ugh
    #         corr.iat[i, i] = 1.  # Set diagonal to 1.00
    #         corr.iloc[i, i:] = corr.iloc[i:, i].values  # Flip matrix.

    #     return corr.as_matrix()

    # print readITRFyear_correlation('ITRF/ITRF2007')




    # discontinued :


    ##################
    # def getdata2ITRF(name):      ### reads ITRF files, collects unc. data. Removes correlations and x,y,z VEL entries
    #     f1 = open(name,'r')
    #     n1 = f1.next()
    #     n1 = int(n1[2:5])
    #     n2 = n1*(n1+1)/2-n1

    #     result2=np.genfromtxt(f1,usecols=(2),skip_header=n1,dtype='f8')

    #     return result2




    ##################

    # def getnames(name):     ###makes an array (n,1) of all X,Y,Z coordinates of all stations
    #     f1 = open(name,'r')
    #     n1=int(((f1.readline()).split())[0]) # number of entries in f1, reads the number at begin of file about amount of entries

    #     data4 = f1.readlines()

    #     data4 = data4[0:] # deletes

    #     result4=np.genfromtxt(data4,usecols=(1),skip_footer=n1,dtype='a4') #gets the station name

    #     result4=np.array([result4]).T  ##making a transpose of the matrix, gives matrix of [n,1]

    #     return result4


    # ##################

    # def getcoordinates(name):     ###makes an array (n,1) of all X,Y,Z coordinates of all stations
    #     f1 = open(name,'r')
    #     n1=int(((f1.readline()).split())[0]) # number of entries in f1, reads the number at begin of file about amount of entries

    #     data3 = f1.readlines()

    #     data3 = data3[0:] # deletes

    #     result3=np.genfromtxt(data3,usecols=(4),skip_footer=n1,dtype='f8') #gets the station name, coordinate and deviations

    #     result3=np.array([result3]).T  ##making a transpose of the matrix, gives matrix of [n,1]

    #     return result3




    # ##################

    # def dataweeklyaverage(name):
    #     f1 = open(name,'r')
    #     n1=int(((f1.readline()).split())[0]) # number of entries in f1, reads the number at begin of file about amount of entries

    #     dataWA = f1.readlines()

    #     dataWA = dataWA[0:] # deletes

    #     result=np.genfromtxt(dataWA,usecols=(1,4,6),skip_footer=n1,dtype=[('1', 'a4'), ('4', 'f8'),('6', 'f8')])
    #     #print n1
    #     return result
