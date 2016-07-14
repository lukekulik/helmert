import numpy as np

# Finished both conversions
# By Lennert Aerts

# test = np.array([['NTUS', 0.337065861622453E+07, 0.711877067509228E+06, 0.534978690374381E+07, 0, 2007.0]])


def transGeodetic(array):
    # INPUT: an array of x,y,z coordinates array(['station', X,Y,Z],['station',X,Y,Z], etc)
    # OUTPUT: the same array transformed to latitude, longitude and height

    Names = array[:, 0]  # array of station names
    Xarr = array[:, 1]  # array of X coordinates
    Yarr = array[:, 2]  # array of Y coordinates
    Zarr = array[:, 3]  # array of Z coordinates
    week = array[:, 4]  # array of no week
    year = array[:, 5]  # array of no year

    Xarr = np.array(Xarr, dtype='float')
    Yarr = np.array(Yarr, dtype='float')
    Zarr = np.array(Zarr, dtype='float')

    # WGS84
    a = 6378136.0  # semi major axis [m]
    # f = 1/298.257223563 #flattening
    f = 0.00335281318

    e = np.sqrt(2 * f - f * f)  # eccentricity
    #b = 6356752.3142  # semi minor axis [m]

    p = np.sqrt(Xarr * Xarr + Yarr * Yarr)  # radius in x-y plane

    lon = np.arctan2(Yarr, Xarr)  # longitude in radians (array)

    lat = np.arctan2(Zarr, (1 - e * e) * p)  # latitude in radians (array)
    N = a / np.sqrt(1 - e * e * np.sin(lat) * np.sin(lat))  # radius of curvature (m)
    h = p / np.cos(lat) - N  # height above earth surface (m)

    # should be improved (now it's arbitrary)
    for i in range(20):  # iterative procedure for increasing lat,h precision
        lat = np.arctan2(Zarr, (1 - e * e * (N / (N + h))) * p)
        N = a / np.sqrt(1 - e * e * np.sin(lat) * np.sin(lat))
        h = p / np.cos(lat) - N

    lat = lat * 180. / np.pi  # lat in degrees
    lon = lon * 180. / np.pi  # lon in degrees

    return np.dstack((Names, Xarr, Yarr, Zarr, lat, lon, h, week, year))[0]

# print transGeodetic(test)


transcoord = np.array([['ALGO', 918129.34165, -4346071.27213, 4561977.86656, 45.9558005501,
                        -78.0713685198, 201.924460742, 0, 2007.0],
                       ['NTUS', 5, 6, 7, 0.337065861622453E+07, 0.711877067509228E+06, 0.534978690374381E+07, 0,
                        2007.0],
                       ['ALGO', 918129.340434, -4346071.27047, 4561977.86919, 45.9558005786,
                        -78.0713685307, 201.925047329, 1, 2007.0],
                       ['ALGO', 918129.339259, -4346071.26586, 4561977.86064, 45.9558005559,
                        -78.0713685333, 201.91559699, 2, 2007.0],
                       ['ALGO', 918129.338932, -4346071.26735, 4561977.86317, 45.9558005627,
                        -78.0713685414, 201.918382074, 3, 2007.0],
                       ['NTUS', 5, 6, 7, 0.337065861622453E+07, 0.711877067509228E+06, 0.534978690374381E+07, 0,
                        2007.0],
                       ['ALGO', 918129.339932, -4346071.26895, 4561977.86543, 45.9558005654,
                        -78.071368533, 201.921238587, 4, 2007.0]])


def transENU(REFcoordinates, array):
    # INPUT: an array of x,y,z,lat,lon coordinates ([X,Y,Z,lat,lon], etc)
    # OUTPUT: an array of transformed coordinates to EAST NORTH UP (ENU)

    allstationnames = np.unique(array[:, 0])  # gets stationnames present in a year

    ENUarray = np.array(6 * len(array) * [0], dtype="S20").reshape(len(array), 6)
    shifter = 0
    for station in range(len(allstationnames)):
        a = array[array[:, 0] == allstationnames[station]]  # takes all coordinates for every station for a year
        REFcoordinate = REFcoordinates[REFcoordinates[:, 0] == allstationnames[station]]
        
        if REFcoordinate.size == 0:

            REFcoordinate = a[[0]]
            print REFcoordinate
            REFcoordinates =np.append(REFcoordinates,REFcoordinate)
            REFcoordinates =REFcoordinates.reshape(len(REFcoordinates)/9.,9)


        
        #Names = a[:, 0]  # array of stationnames
        Xarr = a[:, 1]  # array of X coordinates (m)
        Yarr = a[:, 2]  # array of Y coordinates (m)
        Zarr = a[:, 3]  # array of Z coordinates (m)

        # latarr = a[:,4].astype('f8') #array of latitudes (degrees)
        # lonarr = a[:,5].astype('f8') #array of longitudes (degrees)
        # height = a[:,6].astype('f8') #array of heights

        week = a[:, 7]  # array of week numbers
        year = a[:, 8]  # array of year number

        Xarr = np.array(Xarr, dtype='float')
        Yarr = np.array(Yarr, dtype='float')
        Zarr = np.array(Zarr, dtype='float')


        for i in range(0, len(a)):
            
            A = np.matrix([[-np.sin(REFcoordinate[0, 5].astype('f8') * np.pi / 180),
                            np.cos(REFcoordinate[0, 5].astype('f8') * np.pi / 180), 0],
                           [-np.cos(REFcoordinate[0, 5].astype('f8') * np.pi / 180) * np.sin(
                               REFcoordinate[0, 4].astype('f8') * np.pi / 180),
                            -np.sin(REFcoordinate[0, 5].astype('f8') * np.pi / 180) * np.sin(
                                REFcoordinate[0, 4].astype('f8') * np.pi / 180),
                            np.cos(REFcoordinate[0, 4].astype('f8') * np.pi / 180)],
                           [np.cos(REFcoordinate[0, 5].astype('f8') * np.pi / 180) * np.cos(
                               REFcoordinate[0, 4].astype('f8') * np.pi / 180),
                            np.sin(REFcoordinate[0, 5].astype('f8') * np.pi / 180) * np.cos(
                                REFcoordinate[0, 4].astype('f8') * np.pi / 180),
                            np.sin(REFcoordinate[0, 4].astype('f8') * np.pi / 180)]])
            B = np.matrix(
                [[Xarr[i] - REFcoordinate[0, 1].astype('f8')], [Yarr[i] - REFcoordinate[0, 2].astype('f8')],
                 [Zarr[i] - REFcoordinate[0, 3].astype('f8')]])


            ENUcoord = A * B
            ENU = np.column_stack((allstationnames[station], np.array(ENUcoord.T * 1000), week[i], year[i]))

            ENUarray[i + shifter] = ENU
        shifter += len(a)  # shifting the iterator to keep track of position

    return REFcoordinates,ENUarray

# a= transENU(transcoord)
# print a
'''    
def transDeviations(array):
    #INPUT standard deviations X,Y,Z  + lat and lon of coordinates
    #OUTPUT standard deviations east,north,vertical

    sigmaX = array[:,0]         
    sigmaY = array[:,1]
    sigmaZ = array[:,2]
    lat = array[:,3]*np.pi/180
    lon = array[:,4]*np.pi/180
    
    sigmaEast = np.array([])  #array for sigma east
    sigmaNorth = np.array([]) #array for sigma north
    sigmaVert = np.array([])  #array for sigma vertical

    for i in range(len(sigmaX)):
        #transformation matrix
        R = np.matrix([[-np.sin(lon[i]),-np.sin(lat[i])*np.cos(lon[i]),np.cos(lon[i])*np.cos(lat[i])],\
                       [np.cos(lon[i]),-np.sin(lat[i])*np.sin(lon[i]),np.cos(lat[i])*np.sin(lon[i])],\
                       [0,np.cos(lat[i]),np.sin(lat[i])]])
            
        Pxyz = np.matrix([[sigmaX[i],0,0],[0,sigmaY[i],0],[0,0,sigmaZ[i]]])
        Penu = R.T*Pxyz*R

        #appending new sigmas to arrays
        sigmaEast = np.append(sigmaEast,np.sqrt(Penu[0,0]))
        sigmaNorth = np.append(sigmaNorth,np.sqrt(Penu[1,1]))
        sigmaVert = np.append(sigmaVert,np.sqrt(Penu[2,2]))
    
    Arr3 = np.dstack((sigmaEast,sigmaNorth,sigmaVert))

    return Arr3
'''


# print "Cartesian Coordinates (X,Y,Z): \n",ex,"\n"
# print "Geodetic Coordinates (X,Y,Z,lat,lon,height): \n",transGeodetic(ex),"\n"
# print transGeodetic(ex)[0][0][0]

# ex2 = transGeodetic(ex)
# print "ENU Coordinates (East,North,Up): \n",transENU(ex2),"\n"

# print "Deviations (sigmaE,sigmaN,sigmaU): \n",transDeviations(ex2)
# requires other input than "ex2" but used for testing
