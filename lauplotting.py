import matplotlib.pyplot as plt
import numpy as np
from lau_outlierlong import outlierlong
from matplotlib.pyplot import *
import scipy.stats as stats

npyfile =  np.load('total_data_array.npy')

'''
#defining input arrays for lon,lat,height
data_lon = np.column_stack((npyfile[0:,0],npyfile[0:,1],npyfile[0:,4],npyfile[0:,5]))
data_lat = np.column_stack((npyfile[0:,0],npyfile[0:,2],npyfile[0:,4],npyfile[0:,5]))
data_height = np.column_stack((npyfile[0:,0],npyfile[0:,3],npyfile[0:,4],npyfile[0:,5]))

outlierdata_lon,final_correct_lon = outlierlong(data_lon)
outlierdata_lat,final_correct_lat = outlierlong(data_lat) 
outlierdata_height,final_correct_height = outlierlong(data_height)   


np.save('outlierdata_lon.npy',outlierdata_lon)
np.save('outlierdata_lat.npy',outlierdata_lat)
np.save('outlierdata_height.npy',outlierdata_height)

np.save('final_correct_lon.npy',final_correct_lon)
np.save('final_correct_lat.npy',final_correct_lat)
np.save('final_correct_height.npy',final_correct_height)

'''

#Loading the above arrays, this is quicker
outlierdata_lon = np.load('outlierdata_lon.npy')
outlierdata_lat = np.load('outlierdata_lat.npy')
outlierdata_height = np.load('outlierdata_height.npy')

final_correct_lon = np.load('final_correct_lon.npy')
final_correct_lat = np.load('final_correct_lat.npy')
final_correct_height = np.load('final_correct_height.npy')



def r_squared(actual, ideal):
    actual_mean = np.mean(actual)
    ideal_dev = np.sum([(val - actual_mean)**2 for val in ideal])
    actual_dev = np.sum([(val - actual_mean)**2 for val in actual])

    return ideal_dev / actual_dev
    

    
def lauplotter(outlierdata_lon,final_correct_lon,outlierdata_lat,final_correct_lat,outlierdata_height,final_correct_height):
    
    station_name=outlierdata_lon[1,0]
    
    ###PLOTTING FOR THE LONGITUDINAL VALUES#####
    
    #getting the right data for plotting of outlier
    weeks_outlier_lon = outlierdata_lon[1:,2]
    year_outlier_lon = outlierdata_lon[1:,3]
    time_axis_outlier_lon = year_outlier_lon.astype('f8')+ weeks_outlier_lon.astype('f8')/52.
    outlier_values_lon = outlierdata_lon[1:,1]  
    
     #getting the right dat for plotting of correct values
    weeks_correct_lon = final_correct_lon[0:,2]
    year_correct_lon = final_correct_lon[0:,3]
    time_axis_correct_lon = year_correct_lon.astype('f8')+ weeks_correct_lon.astype('f8')/52.            
    final_correct_values_lon = final_correct_lon[0:,1]
    
    
    ## PLOT commands#####
    plt.subplot(311)
    plt.title(station_name)
    #plt.xticks(np.unique(np.round(lon_x).astype(np.int))) ###don't know where this is for
    plt.ylabel('Longitude [mm]')
    plt.autoscale(tight=True)
    plt.ticklabel_format(useOffset=False)
    
    ### PLOT commands#####
    plt.scatter(time_axis_outlier_lon,outlier_values_lon,color='red',s=10, marker = 'x')
    plt.scatter(time_axis_correct_lon,final_correct_values_lon,color='black',s=3)
    plt.minorticks_on()
       
    #polyarray=lon_temp_x[lon_temp_x[:,3].astype('f8')<=from_date][:,1].astype('f8')  ##WHERE IS THIS FOR????
    res_lon = stats.mstats.theilslopes(final_correct_values_lon.astype('f8'), time_axis_correct_lon, 0.95)
    plt.plot(time_axis_correct_lon, res_lon[1] + res_lon[0] * time_axis_correct_lon, '-', color='#1A476F',linewidth=2)
    plt.annotate('trend = ' + str(round(res_lon[0][0],2)) + r'$\pm$' + str(round((abs(res_lon[0][0]-res_lon[2])+abs(res_lon[0][0]-res_lon[3]))/2.,2)) + ' [mm/yr]' , (0.015, 0.08), xycoords='axes fraction', size=9, color = '#1A476F')

    '''
    NEEDS TO BE FIXED
### SECOND PART
    if from_date != to_date:
        polyarray=lon_temp_x[lon_temp_x[:,3].astype('f8')>=to_date][:,1].astype('f8')
        len2=len(lon_x)-len(polyarray)
        res = stats.mstats.theilslopes(polyarray[:].astype('f8'), lon_x[len2:], 0.90)
        plt.plot(lon_x[len2:], res[1] + res[0] * lon_x[len2:], '-', color = '#707070')
        plt.annotate('trend = ' + str(round(res[0][0],2)) + r'$\pm$' + str(round((abs(res[0][0]-res[2])+abs(res[0][0]-res[3]))/2.,2)) + ' [mm/yr]' , (0.68, 0.08), xycoords='axes fraction', size=9, color = '#505050')

#        plt.annotate('-', (0.675, 0.42), xycoords='axes fraction', color = 'cyan',fontsize=20,fontweight='bold')
        plt.axvline(from_date,color='grey',linewidth=1).set_linestyle('--')
        plt.axvline(to_date,color='grey',linewidth=1).set_linestyle('--')
 
    '''
    
    

###PLOTTING FOR THE LATUDINAL VALUES#####
    
    #getting the right data for plotting of outlier
    weeks_outlier_lat = outlierdata_lat[1:,2]
    year_outlier_lat = outlierdata_lat[1:,3]
    time_axis_outlier_lat = year_outlier_lat.astype('f8')+ weeks_outlier_lat.astype('f8')/52.
    outlier_values_lat = outlierdata_lat[1:,1]  
    
     #getting the right dat for plotting of correct values
    weeks_correct_lat = final_correct_lat[0:,2]
    year_correct_lat = final_correct_lat[0:,3]
    time_axis_correct_lat = year_correct_lat.astype('f8')+ weeks_correct_lat.astype('f8')/52.            
    final_correct_values_lat = final_correct_lat[0:,1]
    
    ### PLOT commands#####
    plt.subplot(312)
    #plt.xticks(np.unique(np.round(lat_x).astype(np.int))) ###don't know where this is for
    plt.ylabel('Latitude [mm]')
    plt.autoscale(tight=True)
    plt.ticklabel_format(useOffset=False)
    
    plt.scatter(time_axis_outlier_lat,outlier_values_lat,color='red',s=10, marker = 'x')
    plt.scatter(time_axis_correct_lat,final_correct_values_lat,color='black',s=3)
    plt.minorticks_on()
       
    #polyarray=lat_temp_x[lat_temp_x[:,3].astype('f8')<=from_date][:,1].astype('f8')
    res_lat = stats.mstats.theilslopes(final_correct_values_lat.astype('f8'), time_axis_correct_lat, 0.95)
    plt.plot(time_axis_correct_lat, res_lat[1] + res_lat[0] * time_axis_correct_lat, '-', color='#1A476F',linewidth=2)
    plt.annotate('trend = ' + str(round(res_lat[0][0],2)) + r'$\pm$' + str(round((abs(res_lat[0][0]-res_lat[2])+abs(res_lat[0][0]-res_lat[3]))/2.,2)) + ' [mm/yr]' , (0.015, 0.08), xycoords='axes fraction', size=9, color = '#1A476F')





###PLOTTING FOR THE HEIGHT VALUES#####
    
    #getting the right data for plotting of outlier
    weeks_outlier_height = outlierdata_height[1:,2]
    year_outlier_height = outlierdata_height[1:,3]
    time_axis_outlier_height = year_outlier_height.astype('f8')+ weeks_outlier_height.astype('f8')/52.
    outlier_values_height = outlierdata_height[1:,1]  
    
     #getting the right dat for plotting of correct values
    weeks_correct_height = final_correct_height[0:,2]
    year_correct_height = final_correct_height[0:,3]
    time_axis_correct_height = year_correct_height.astype('f8')+ weeks_correct_height.astype('f8')/52.            
    final_correct_values_height = final_correct_height[0:,1]
    
    ### PLOT commands#####
    plt.subplot(313)
    #plt.xticks(np.unique(np.round(height_x).astype(np.int))) ###don't know where this is for
    plt.ylabel('Height [mm]')
    plt.autoscale(tight=True)
    plt.ticklabel_format(useOffset=False)
    
    plt.scatter(time_axis_outlier_height,outlier_values_height,color='red',s=10, marker = 'x')
    plt.scatter(time_axis_correct_height,final_correct_values_height,color='black',s=3)
    plt.minorticks_on()
    
    #polyarray=height_temp_x[height_temp_x[:,3].astype('f8')<=from_date][:,1].astype('f8')
    res_height = stats.mstats.theilslopes(final_correct_values_height.astype('f8'), time_axis_correct_height, 0.95)
    plt.plot(time_axis_correct_height, res_height[1] + res_height[0] * time_axis_correct_height, '-', color='#1A476F',linewidth=2)
    plt.annotate('trend = ' + str(round(res_height[0][0],2)) + r'$\pm$' + str(round((abs(res_height[0][0]-res_height[2])+abs(res_height[0][0]-res_height[3]))/2.,2)) + ' [mm/yr]' , (0.015, 0.08), xycoords='axes fraction', size=9, color = '#1A476F')


    
    
    plt.savefig('figs2/'+str(station_name)+'.png', format='png', dpi=300)
    plt.clf()
    return 0
    



##RUNNING IT FOR ALL THE STATIONS

stations=np.array(['TSKB','KUAL','KOKB','COCO','BAKO','IISC','KUNM','MAC1','MKEA','NTUS','PERT','PIMO','YAR1','HYDE','TNML','ALIC','PHKT'])
#stations=np.array(['KUAL','BAKO'])
#print len(stations)

'''####THIS IS FOR WHEN EARTHQUAKE OCCURS
data1 = np.load('total_data_array.npy')

lst = [0]*len(stations)
lst_special = []
for sta in range(len(stations)):
    lst[sta] = (data1[data1[:,0]==stations[sta]][-1][5].astype('f8'),data1[data1[:,0]==stations[sta]][-1][5].astype('f8'))

# to force single trendline for height    
lst_special = lst

lst[np.where(stations=='KUAL')[0]]=(2005,2007.5)
'''


#make a loop so for all stations graphs will be made
for i in range(len(stations)):
    #the 1 is needed, otherwise all the rest of the data cant be selected    
    outlierdata_lon1 = outlierdata_lon[outlierdata_lon[:,0] == str(stations[i])]
    outlierdata_lat1 = outlierdata_lat[outlierdata_lat[:,0] == str(stations[i])]
    outlierdata_height1 = outlierdata_lat[outlierdata_lat[:,0] == str(stations[i])]
    
    final_correct_lon1 = final_correct_lon[final_correct_lon[:,0] == str(stations[i])]
    final_correct_lat1 = final_correct_lat[final_correct_lat[:,0] == str(stations[i])]
    final_correct_height1 = final_correct_height[final_correct_height[:,0] == str(stations[i])]
    
    lauplotter(outlierdata_lon1,final_correct_lon1,outlierdata_lat1,final_correct_lat1,outlierdata_height1,final_correct_height1)

  



#lst[np.where(stations=='PHKT')[0]]=(2005,2005.5)
#lst[np.where(stations=='NTUS')[0]]=(2004.9,2008)


#for i in range(len(stations)):
#    plotter(stations[i],lst[i],lst_special[i])
    
    

#lauplotter(outlierdata_lon,final_correct_lon,outlierdata_lat,final_correct_lat,outlierdata_height,final_correct_height)

    
    
    
    
    
    
    