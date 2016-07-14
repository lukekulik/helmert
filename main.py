from yearsplitter import yearsplitter
from weeklyaverage import weeklyaverage
from getdata import readITRFyear  # , readITRFyear_correlation
from data_trans import get_helmert_parameters, apply_helmert_parameters
from ITRF import get_helmert_ITRF_parameters, apply_helmert_ITRF_parameters, reshape_for_helmert_ITRF, \
    Averages_week_separated,remove_stations
from coord import transGeodetic, transENU

#year = 'dataset/year2005'  # define year to be studied (directory in filelist)
#yearITRF = 'ITRF/ITRF2005'


def main(year, yearITRF):  # main function returning full result when given year

    ####### extract ITRF stationnames and coordinates from all weeks in one year
    # INPUT: ITRF dataset path
    # OUTPUT:  list[ array[ void(ALGO,x,unc.),(string,float,float), (ALGO,...), ...all sta.], [week2], ...all weeks]
    REFcoord_ITRF = readITRFyear(yearITRF)


    ####### extract ITRF correlations from all weeks in one year
    # INPUT: ITRF dataset path
    # OUTPUT: matrix of correltions of all points in ITRF dataset
    # REFcorr_ITRF = readITRFyear_correlation(yearITRF)
    ###correlation change 1/4: remove comment on REFcorr_ITRF


    ####### extracts filenames of a day files from specified year 
    # INPUT: year station dataset path
    # OUTPUT:
    # weeks = list[ list[name, string, ...all days], [weeks2], ...all weeks]
    weeks = yearsplitter(year)  # creates a list of 7 filenames per spot for one year (last spot contains 8 filenames)

    ####### applies helmert to find transformation matrices
    # INPUT: weeks, year
    # OUTPUT:
    # helmertresults = list[ array[ matrix([Rxyz]), matrix([txyz]), k], [day2], ...all days]
    # lennertarrays = list[ array[ array[ALGO,x,y,z],[ARAU,...], ...all sta.], [day2], ...all days]
    helmertresults, lennertarrays = get_helmert_parameters(weeks, year)

    ####### applies transformation matrices to coordinates
    # INPUT: helmertresults, lennertarrays, year
    # OUTPUT:
    # NEWposition = array[ array[ALGO,x,y,z,week,year], [ARAU,...], ...all sta. of one year in sequence]
    NEWposition = apply_helmert_parameters(lennertarrays, helmertresults, year)

    ####### NEWposition to NEWposition_ENU          
    # INPUT: NEWposition
    # OUTPUT:
    # NEWposition_ENU = array[ array[ALGO,0,0,0,week,year], [ALGO,E,N,U,week,year], ...all same sta. in sequence]

    # 'ENU residuals, currently not used and probably wrong' 
    # NEWposition_LLH = transGeodetic(NEWposition)
    # NEWposition_ENU = transENU(NEWposition_LLH)


    # OUTLIERS AND LOOPING SHOULD BE HERE TO ITERATE HELMERT PARAMETERS


    ####### Determine weeklyaverage with transformed positions
    # INPUT: NEWposition  
    # OUTPUT:
    # Averages = array[ array[ALGO,x,y,z,week,year], [BABH,...], ...all sta. of one year in sequence]
    # StandardDeviation = array[ array[ALGO,unc_x,unc_y,unc_z,week,year], [week2], ...all weeks]
    
    Averages, StandardDeviation = weeklyaverage(NEWposition, weeks)



    ####### combining and reshaping Averages and StandardDeviation to fit in helmert_input_ITRF
    # INPUT: Averages, Standards
    # OUTPUT:
    # Averages_year_with_uncertainties = list[ array[ array[ALGO,x,unc_x], [ALGO,y,unc_y], [ALGO,z,unc_x], [ARAU,x,unc_x], ...all sta.], [week2], ...all weeks]
    Averages_year_with_uncertainties = reshape_for_helmert_ITRF(Averages, StandardDeviation, weeks)


    ####### RESEARCH QUESTION
    #Averages_year_with_uncertainties = remove_stations(Averages_year_with_uncertainties)
    
    
    ####### applies helmert to find ITRF transformation matrices
    # INPUT: Averages_year, REFcoord_ITRF, REFcorr_ITRF
    # OUTPUT:
    # helmertresults_ITRF = list[ array[ matrix([Rxyz]), matrix([txyz]), k], [week2], ...all weeks]
    helmertresults_ITRF = get_helmert_ITRF_parameters(Averages_year_with_uncertainties, REFcoord_ITRF)
    ###correlation change 2/4: add REFcorr_ITRF to helmertresults_ITRF input



    ####### separates Averages into arrays containing separate weeks
    # INPUT: Averages, weeks
    # OUTPUT:
    # Averages_weeks = list[ array[ array[ALGO,x,y,z,week,year], ...all sta.], [week2], ...all weeks]
    Averages_weeks = Averages_week_separated(Averages, weeks)

    ####### applies transformation matrices to weekly averaged coordinates
    # INPUT: helmertresults_ITRF, lennertarrays_ITRF
    # OUTPUT:
    # NEWposition_ITRF = array[ array[ALGO,x,y,z,week,year], [ARAU,...], ...all sta. of one year in sequence]
    NEWposition_ITRF = apply_helmert_ITRF_parameters(Averages_weeks, helmertresults_ITRF, year)

    ####### applies coordinate transformation from X Y Z to lat long height
    ####### returns in following format: [Station,lat,lon,height,week,year]
    # INPUT: ReferenceCoordinates(created in save_data),NEW_position_ITRF
    # OUTPUT:
    NEWellipsoidal_Pos = transGeodetic(NEWposition_ITRF)

    return NEWellipsoidal_Pos


NEWellipsoidal_Pos = main(year, yearITRF)


def computer(ReferenceCoord, Coordinates):
    ####### applies coordinate transformation from X Y Z to lat long height
    ####### returns in following format: [Station,lat,lon,height,week,year]
    # INPUT: ReferenceCoordinates(created in save_data),NEW_position_ITRF
    # OUTPUT:
    #ellipsoidal_Pos = transGeodetic(ReferenceCoord)

    ####### applies coordinate transformation from X Y Z lat lon to ENU (EAST NORTH UP)
    ####### returns in following format: [Station,X,Y,Z,East,North,Up,week,year]
    # INPUT: ellipsoidal_Pos[0] of the refence coordinates & all coordinates
    # OUTPUT:
    REFcoordinates,ENU_Pos = transENU(ReferenceCoord, Coordinates)

    return REFcoordinates,ENU_Pos

# NEWposition_ITRF = main(year,yearITRF)

# uncomment for desired print output
# print REFcoord_ITRF[0:10]
# print weeks
# print helmertresults
# print lennertarrays
# print NEWposition
# print NEWposition_LLH
# print NEWposition_ENU[np.where(ENU_Pos[:,0] == 'ALGO')][:15]
# print Averages
# print StandardDeviation
# print Averages_year_with_uncertainties
# print helmertresults_ITRF
# print Averages_weeks
# print NEWposition_ITRF
# print ellipsoidal_Pos[np.where(ellipsoidal_Pos[:,0] == 'ALGO')][:15]
# print ENU_Pos[np.where(ENU_Pos[:,0] == 'ALGO')][:15]


# data_xyz,data_lon,data_enu = main(year,yearITRF)
