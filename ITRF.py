import numpy as np

from data_trans import position
from helmert_input import helmert_input_ITRF
from helmert_comp import helmert




####### reshape, old
def reshape_for_helmert(array):
    Averages_reshaped = len(array) * [0]
    for week in range(len(array)):
        Averages_station_names = np.dstack((array[week][:, 0], array[week][:, 0], array[week][:, 0])).flatten()
        Averages_coord = np.dstack((array[week][:, 1], array[week][:, 2], array[week][:, 3])).flatten()
        Averages_unc = np.ones(len(Averages_coord))

        Averages_for_ITRF = np.vstack((Averages_station_names, Averages_coord, Averages_unc)).T

        Averages_reshaped[week] = Averages_for_ITRF
    return Averages_reshaped


####### combines and reshapes Averages and StandardDeviation to fit in helmert_input
def reshape_for_helmert_ITRF(Averages, StandardDeviation, weeks):
    Averages_reshaped = len(weeks) * [0]

    for week in range(len(weeks)):
        Averages_index = np.where(Averages[:, 4] == str(week))
        Averages_week = Averages[Averages_index[0][0]:Averages_index[0][-1] + 1]

        Averages_helmert_input = np.zeros([3 * len(Averages_week)])
        # 1. column
        Averages_names = np.dstack((Averages_week[:, 0], Averages_week[:, 0], Averages_week[:, 0])).flatten()
        # 2. column
        Averages_x, Averages_y, Averages_z = Averages_week[:, 1], Averages_week[:, 2], Averages_week[:, 3]
        Averages_helmert_input[0::3], Averages_helmert_input[1::3], Averages_helmert_input[2::3] = Averages_x, (
        Averages_y), Averages_z
        # 3. column
        StandardDeviation_index = np.where(StandardDeviation[:, 4] == str(week))
        StandardDeviation_week = StandardDeviation[StandardDeviation_index[0][0]:StandardDeviation_index[0][-1] + 1]
        StandardDeviation_helmert_input = np.zeros([3 * len(StandardDeviation_week)])
        StandardDeviation_x, StandardDeviation_y, StandardDeviation_z = StandardDeviation_week[:,
                                                                        1], StandardDeviation_week[:,
                                                                            2], StandardDeviation_week[:, 3]
        StandardDeviation_helmert_input[0::3], StandardDeviation_helmert_input[1::3], StandardDeviation_helmert_input[
                                                                                      2::3] = StandardDeviation_x, (
        StandardDeviation_y), StandardDeviation_z

        # stack 3 columns
        Averages_helmert_input = np.vstack((Averages_names, Averages_helmert_input, StandardDeviation_helmert_input)).T
        Averages_reshaped[week] = Averages_helmert_input
    return Averages_reshaped


####### 
def get_helmert_ITRF_parameters(coordinates, coordinates_ref):
    ###correlations change 3/4: add coordinates_ref_corr to get_helmert_ITRF_parameters input

    transformation_ITRF = []  # list for helmert solutions
    # pos_ITRF = []          #list with station positions
    # stationxyz_coordinates_ITRF = []      #list with structure: ['station name' X Y Z],[etc]

    for week in range(len(coordinates)):
        coordinates_ref_corr = np.ones(len(coordinates_ref[week]))  # identity matrix for use in helmert
        ###correlations change 4/4: comment out coordinates_ref_corr
        coordinates_corr = np.ones(len(coordinates[week]))  # identiy matrix for use in helmert

        # helmertpara = helmert_ITRF(coordinates[week],coordinates_ref[week],coordinates_corr[week],coordinates_ref_corr[week])
        pos1, pos2, Q, n = helmert_input_ITRF(coordinates[week], coordinates_ref[week], coordinates_corr[week],
                                              coordinates_ref_corr[week])
        helmertpara = helmert(pos1, pos2, Q, n)

        transformation_ITRF.append(helmertpara)

    return transformation_ITRF


####### separates Averages into an array containing one array for each week
def Averages_week_separated(Averages, weeks):
    Averages_week_separated = len(weeks) * [0]

    for week in range(len(weeks)):
        Averages_index = np.where(Averages[:, 4] == str(week))
        Averages_week = Averages[Averages_index[0][0]:Averages_index[0][-1] + 1]
        Averages_week_separated[week] = Averages_week
    return Averages_week_separated


#######   
def apply_helmert_ITRF_parameters(stationxyz_coordinates_ITRF, transformation_ITRF, year):
    NEWposition_ITRF = np.array([])  # list for transformed positions

    for week in range(len(stationxyz_coordinates_ITRF)):
        for stations in range(len(stationxyz_coordinates_ITRF[week])):
            stationcoordinates_ITRF = np.matrix(stationxyz_coordinates_ITRF[week][stations][1:4],
                                                np.dtype('float64'))  # takes coordinates of station in matrix notation
            rotationmatrix_ITRF = transformation_ITRF[week][
                0]  # takes rotationmatrix from Helmert solutions per day per station
            translationmatrix_ITRF = transformation_ITRF[week][
                1]  # takes translationmatrix from Helmert solutions per day per staion
            scaling_ITRF = transformation_ITRF[week][
                2]  # takes scaling factor from Helmert solutions per day per station

            transformedposition_ITRF = position(rotationmatrix_ITRF, translationmatrix_ITRF, scaling_ITRF,
                                                stationcoordinates_ITRF.T)
            transformedposition2_ITRF = np.column_stack((stationxyz_coordinates_ITRF[week][stations][0],
                                                         transformedposition_ITRF.T, int(week), float(year[-4:])))

            NEWposition_ITRF = np.append(NEWposition_ITRF, transformedposition2_ITRF)

    NEWposition_ITRF = NEWposition_ITRF.reshape(NEWposition_ITRF.shape[0] / 6.0,
                                                6)  # reshapes array to ['station name' X Y Z],[etc]

    return NEWposition_ITRF



####### RESEARCH QUESTION

def remove_stations(Averages_year_with_uncertainties):
    
    delete_stations = np.array(['PIMO','GUAM','KOKB','MKIA','KWJ1','DARW','TIDB','MACY','ALIC','PETS','MCIL','SHAO','TSK2','TNML'])
    
    Averages_year_with_uncertainties_keep = len(Averages_year_with_uncertainties) * [0]
    
    for week in range(len(Averages_year_with_uncertainties)):
        
        Averages_year_with_uncertainties_0 = Averages_year_with_uncertainties[week]
        Averages_year_with_uncertainties_names = Averages_year_with_uncertainties_0[:,0]
        
        pointer1 = np.argwhere(np.in1d(Averages_year_with_uncertainties_names, delete_stations) == True).flatten()
        
        Averages_year_with_uncertainties_0 = np.delete(Averages_year_with_uncertainties_0,pointer1,axis=0)
        
        Averages_year_with_uncertainties_keep[week] = Averages_year_with_uncertainties_0
    
    return Averages_year_with_uncertainties_keep