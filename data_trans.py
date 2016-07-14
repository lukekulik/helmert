import numpy as np

from getdata import getdata1, getdata2
from helmert_input import helmert_input
from helmert_comp import helmert


def get_helmert_parameters(weeks, year):
    daysinyear = 0
    for week in range(len(weeks)):
        length = len(weeks[week])
        daysinyear += length

    helmertresults = [0] * daysinyear  # makes a of zeros for rewriting the helmert solutions in it
    lennertarrays = [0] * daysinyear  # list with zeros, for replacing list with structure: ['station name' X Y Z],[etc]

    shifter = 0  # shifter is needed because of for loop in a for loop
    for week in range(len(weeks)):  # double for loop to run all days of all weeks
        # reference values for helmert transform
        REFcoord = getdata1(year + "/" + weeks[week][3])
        REFcorr = getdata2(year + "/" + weeks[week][3])
        for day in range(len(weeks[week])):  # opens data of all days and appends to previously created lists
            testdata = getdata1(year + "/" + weeks[week][day])
            cordata = getdata2(year + "/" + weeks[week][day])

            # helmertpara,lennertarray = helmert(testdata,REFcoord,cordata,REFcorr) #apply helmert transformation on data
            pos1, pos2, Q, n, lennertarray = helmert_input(testdata, REFcoord, cordata, REFcorr)
            helmertpara = helmert(pos1, pos2, Q, n)  # apply helmert transformation on data

            helmertresults[shifter + day] = helmertpara  # replacing the zero's with the wanted values
            lennertarrays[shifter + day] = lennertarray

        shifter += len(weeks[week])  # makes the shifter shift to the new place

    return helmertresults, lennertarrays


def position(rotationmatrix, translationmatrix, scaling, pos1):
    # multiply with R matrix
    data1posR = rotationmatrix * pos1  ##pos1 needs a 3x1 matrix with x,y,x coordinates (station coordinates)
    # multiply with scaling factor (K+1)
    data1posRk = data1posR * scaling + data1posR
    # add translational values
    data1posRkt = data1posRk + translationmatrix

    return data1posRkt


def apply_helmert_parameters(lennertarrays, helmertresults, year):
    NEW_length = 0
    for day in range(len(lennertarrays)):
        length = len(lennertarrays[day])
        NEW_length += length
    # print NEW_length

    NEWposition = np.array(6 * NEW_length * [0], dtype="S20").reshape(NEW_length,
                                                                      6)  # makes an array of zero's which is used for putting in the transformed positions

    shifter = 0  # shifter is needed because of for loop in a for loop
    for days in range(len(lennertarrays)):
        for stations in range(len(lennertarrays[days])):
            stationcoordinates = np.matrix(lennertarrays[days][stations][1:4],
                                           np.dtype('float64'))  # takes coordinates of station in matrix notation
            rotationmatrix = helmertresults[days][0]  # takes rotationmatrix from Helmert solutions per day per station
            translationmatrix = helmertresults[days][
                1]  # takes translationmatrix from Helmert solutions per day per staion
            scaling = helmertresults[days][2]  # takes scaling factor from Helmert solutions per day per station
            transformedposition = position(rotationmatrix, translationmatrix, scaling, stationcoordinates.T)
            transformedposition2 = np.column_stack((lennertarrays[days][stations][0], transformedposition.T,
                                                    int(days / 7.0),
                                                    float(year[-4:])))  # has dimensions of [name,X,Y,Z,week,year]

            NEWposition[stations + shifter] = transformedposition2[
                0]  # replace the zero's in NEWposition with the correct values for the stations of each day
        shifter += len(lennertarrays[days])  # shifting the iterator to keep track of position
    return NEWposition

# redundant: ~ lukasz
# def get_unique_station_names(weeks,year):
#     daynames = np.array([])
#     for week in weeks:
#         for day in week:
#             namestationperday = getnames(year + "/" + day)
#             daynames = np.append(daynames,namestationperday)
#     allstationnames = np.unique(daynames) #create list with all stationnames
#     return allstationnames
