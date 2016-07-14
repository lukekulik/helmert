import matplotlib.pyplot as plt
import numpy as np
from outlier_long import outlierlong
from matplotlib.pyplot import *
import scipy.stats as stats

def r_squared(actual, ideal):
    actual_mean = np.mean(actual)
    ideal_dev = np.sum([(val - actual_mean)**2 for val in ideal])
    actual_dev = np.sum([(val - actual_mean)**2 for val in actual])

    return ideal_dev / actual_dev


data1 = np.load('data.npy')
#station_name='KUAL'

#npyfile =  np.load('data2005-2007.npy')


def plotter(station_name,tup,tup_special):
    #print station_name, tup
#    temp=data1[data1[:,0]==station_name]
#    tempXX=temp[(temp[:,4]!='00') & (temp[:,5]!='2011.0')]
#    xaxis=tempXX[:,5].astype('f8')+tempXX[:,4].astype('f8')/52.
#    tempXX[:,5]=tempXX[:,5].astype('f8')+tempXX[:,4].astype('f8')/52.
    

    lon,lat,height,lon_out,lat_out,height_out = outlierlong(data1)  

    # lon x-axis
    lon=lon[lon[:,0]==station_name]
    lon_temp_x = lon[np.logical_not((lon[:,2]=='0') & (lon[:,3]=='2011.0'))]
    lon_x=lon_temp_x[:,3].astype('f8')+lon_temp_x[:,2].astype('f8')/52.             # xaxis
    lon_temp_x[:,3]=lon_temp_x[:,3].astype('f8')+lon_temp_x[:,2].astype('f8')/52.   # tempXX
    # lat x-axis
    lat=lat[lat[:,0]==station_name]
    lat_temp_x = lat[np.logical_not((lat[:,2]=='0') & (lat[:,3]=='2011.0'))]
    lat_x=lat_temp_x[:,3].astype('f8')+lat_temp_x[:,2].astype('f8')/52.             # xaxis
    lat_temp_x[:,3]=lat_temp_x[:,3].astype('f8')+lat_temp_x[:,2].astype('f8')/52.   # tempXX
    # height x-axis
    height=height[height[:,0]==station_name]
    height_temp_x = height[np.logical_not((height[:,2]=='0') & (height[:,3]=='2011.0'))]
    height_x=height_temp_x[:,3].astype('f8')+height_temp_x[:,2].astype('f8')/52.               # xaxis
    height_temp_x[:,3]=height_temp_x[:,3].astype('f8')+height_temp_x[:,2].astype('f8')/52.  # tempXX
    
   
    # lon outlier x-axis
    lon_out=lon_out[lon_out[:,0]==station_name]
    lon_out=lon_out[np.logical_not((lon_out[:,2]=='0') & (lon_out[:,3]=='2011.0'))]
    xaxis_out = lon_out[:,3].astype('f8')+lon_out[:,2].astype('f8')/52.
    # lat outlier x-axis
    lat_out=lat_out[lat_out[:,0]==station_name]
    lat_out=lat_out[np.logical_not((lat_out[:,2]=='0') & (lat_out[:,3]=='2011.0'))]
    lat_out_x = lat_out[:,3].astype('f8')+lat_out[:,2].astype('f8')/52.
    # height outlier x-axis    
    height_out=height_out[height_out[:,0]==station_name]
    height_out=height_out[np.logical_not((height_out[:,2]=='0') & (height_out[:,3]=='2011.0'))]    
    height_out_x = height_out[:,3].astype('f8')+height_out[:,2].astype('f8')/52.
    
    from_date = tup[0]
    to_date = tup[1]
    

    ##### PLOT 1    
    plt.subplot(312)
    #ax = fig.add_subplot(312)
    
    plt.xticks(np.unique(np.round(lon_x).astype(np.int)))
    plt.ylabel('Longitude [mm]')
    plt.autoscale(tight=True)
    plt.ticklabel_format(useOffset=False)
    ### PLOT commands
    plt.scatter(lon_x,lon_temp_x[:,1],color='black',s=5)
    plt.scatter(xaxis_out,lon_out[:,1],color='red',s=10, marker = 'x')
    plt.minorticks_on()
    
    polyarray=lon_temp_x[lon_temp_x[:,3].astype('f8')<=from_date][:,1].astype('f8')
    res = stats.mstats.theilslopes(polyarray[:].astype('f8'), lon_x[0:len(polyarray)], 0.95)
    
    plt.plot(lon_x[0:len(polyarray)], res[1] + res[0] * lon_x[0:len(polyarray)], '-', color='#1A476F',linewidth=2)
    plt.annotate('trend = ' + str(round(res[0][0],2)) + r'$\pm$' + str(round((abs(res[0][0]-res[2])+abs(res[0][0]-res[3]))/2.,2)) + ' [mm/yr]' , (0.015, 0.08), xycoords='axes fraction', size=9, color = '#1A476F')

#    plt.annotate('-', (0.675, 0.72), xycoords='axes fraction', color = 'red',fontsize=25,fontweight='bold')

    
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
    
    
    ##### PLOT 2
    plt.subplot(311)
    plt.title(station_name)
    plt.xticks(np.unique(np.round(lat_x).astype(np.int)))
    plt.ylabel('Latitude [mm]')
    plt.autoscale(tight=True)
    plt.ticklabel_format(useOffset=False)
    ### PLOT commands    
    plt.scatter(lat_x,lat_temp_x[:,1],color='black',s=5)
    plt.scatter(lat_out_x,lat_out[:,1],color='red',s=10, marker = 'x')
    plt.minorticks_on()
    
    polyarray=lat_temp_x[lat_temp_x[:,3].astype('f8')<=from_date][:,1].astype('f8')
    res = stats.mstats.theilslopes(polyarray[:].astype('f8'), lat_x[0:len(polyarray)], 0.90)
    plt.plot(lat_x[0:len(polyarray)], res[1] + res[0] * lat_x[0:len(polyarray)], '-', color = '#002366' )
    plt.annotate('trend = ' + str(round(res[0][0],2)) + r'$\pm$' + str(round((abs(res[0][0]-res[2])+abs(res[0][0]-res[3]))/2.,2)) + '[mm/yr]' , (0.01, 0.08), xycoords='axes fraction', size=9, color = '#002366')
    

#    polyarray=lat_temp_x[lat_temp_x[:,3].astype('f8')<=from_date][:,1].astype('f8')
#    res = stats.mstats.theilslopes(polyarray[:].astype('f8'), lat_x[0:len(polyarray)], 0.90)
#    plt.plot(lat_x[0:len(polyarray)], res[1] + res[0] * lat_x[0:len(polyarray)], 'b-')
#    plt.annotate('trend = ' + str(round(res[0][0],2)) + r'$\pm$' + str(round((abs(res[0][0]-res[2])+abs(res[0][0]-res[3]))/2.,2)) + '[mm/yr]' , (0.05, 0.1), xycoords='axes fraction')


    ### FIRST PART
#    # Trendline
#    polyarray=lat_temp_x[lat_temp_x[:,3].astype('f8')<=from_date][:,1].astype('f8')
#    z = np.polyfit(lat_x[0:len(polyarray)],polyarray,1)
#    p = np.poly1d(z)
#    plt.plot(lat_x[0:len(polyarray)],p(lat_x)[0:len(polyarray)],'r',linewidth=1.5,color='red')
#    #
#    # r^2 annotating
#    r_sq = r_squared(lat_temp_x[:,1].astype('f8')[0:len(polyarray)],p(lat_x[0:len(polyarray)]))
#    plt.annotate('r^2 = {0:2f}'.format(r_sq), (0.7, 0.7), xycoords='axes fraction')
#    #
#    # slope equation
#    polyarray=lat_temp_x[lat_temp_x[:,3].astype('f8')<=from_date][:,1].astype('f8')
#    (m,b) = np.polyfit(lat_x[0:len(polyarray)],polyarray,1)
#    yp = np.polyval([m,b],lat_x)
#    
#    plt.annotate(str(round(m,3)) + ' [mm/year]', (0.7, 0.8), xycoords='axes fraction',annotation_clip=False,clip_on=False)
#    #
#    # graph legend
#    plt.annotate('-', (0.675, 0.72), xycoords='axes fraction', color = 'red',fontsize=25,fontweight='bold')
    
    
    ### SECOND PART
    if from_date != to_date:
        # Trendline
        polyarray=lat_temp_x[lat_temp_x[:,3].astype('f8')>=to_date][:,1].astype('f8')
        len2=len(lat_x)-len(polyarray)
        (m,b) = np.polyfit(lat_x[len2:],polyarray,1)
        p = np.poly1d((m,b))
        plt.plot(lat_x[len2:],p(lat_x)[len2:],'r',linewidth=1.5,color='cyan')

        # r^2 annotating
        r_sq = r_squared(lat_temp_x[:,1].astype('f8')[len2:],p(lat_x[len2:]))
        plt.annotate('r^2 = {0:2f}'.format(r_sq), (0.7, 0.4), xycoords='axes fraction')

        # slope equation
        polyarray=lat_temp_x[lat_temp_x[:,3].astype('f8')<=from_date][:,1].astype('f8')
        yp = np.polyval([m,b],lat_x) 
        plt.annotate(str(round(m,3)) + ' [mm/year]', (0.7, 0.5), xycoords='axes fraction')

        # graph legend
        plt.annotate('-', (0.675, 0.42), xycoords='axes fraction', color = 'cyan',fontsize=20,fontweight='bold')
        
        # vertical lines at separation
        plt.axvline(from_date,color='grey',linewidth=1).set_linestyle('--')
        plt.axvline(to_date,color='grey',linewidth=1).set_linestyle('--')
    
    
    ##### PLOT 3
    plt.subplot(313)
    plt.xticks(np.unique(np.round(height_x).astype(np.int)))
    plt.xlabel('Year')
    plt.ylabel('Height [mm]')
    plt.autoscale(tight=True)
    plt.ticklabel_format(useOffset=False)
    ### PLOT commands
    plt.scatter(height_x,height_temp_x[:,1],color='black',s=5) 
    plt.scatter(height_out_x,height_out[:,1],color='red',s=10, marker = 'x')
    plt.minorticks_on()
    
    # height forces single trend line    
    from_date = tup_special[0]
    to_date = tup_special[1]
      
    ### FIRST PART
    # Trendline
    polyarray=height_temp_x[:,1].astype('f8')
    z = np.polyfit(height_x[0:len(polyarray)],polyarray,1)
    p = np.poly1d(z)
    plt.plot(height_x[0:len(polyarray)],p(height_x)[0:len(polyarray)],'r',linewidth=1.5,color='red')
    

    # r^2 annotating
    r_sq = r_squared(height_temp_x[:,1].astype('f8')[0:len(polyarray)],p(height_x[0:len(polyarray)]))
    plt.annotate('r^2 = {0:2f}'.format(r_sq), (0.7, 0.7), xycoords='axes fraction')

    # slope equation
    polyarray=height_temp_x[height_temp_x[:,3].astype('f8')<=from_date][:,3].astype('f8')
    (m,b) = np.polyfit(height_x[0:len(polyarray)],polyarray,1)
    yp = np.polyval([m,b],height_x)
    plt.annotate(str(round(m,3)) + ' [mm/year]', (0.7, 0.8), xycoords='axes fraction',annotation_clip=False,clip_on=False)

    # graph legend
    plt.annotate('-', (0.675, 0.72), xycoords='axes fraction', color = 'red',fontsize=25,fontweight='bold')
    
    
    ### SECOND PART
#    if from_date != to_date:
#        # Trendline
#        polyarray=height_temp_x[height_temp_x[:,3].astype('f8')>=to_date][:,1].astype('f8')
#        len2=len(height_x)-len(polyarray)
#        (m,b) = np.polyfit(height_x[len2:],polyarray,1)
#        p = np.poly1d((m,b))
#        plt.plot(height_x[len2:],p(height_x)[len2:],'r',linewidth=1.5,color='cyan')
#
#        # r^2 annotating
#        r_sq = r_squared(height_temp_x[:,3].astype('f8')[len2:],p(height_x[len2:]))
#        plt.annotate('r^2 = {0:2f}'.format(r_sq), (0.7, 0.4), xycoords='axes fraction')
#
#        # slope equation
#        plt.annotate(str(round(m,3)) + ' [mm/year]', (0.7, 0.5), xycoords='axes fraction')
#        yp = np.polyval([m,b],height_x) 
#        plt.annotate('-', (0.675, 0.42), xycoords='axes fraction', color = 'cyan',fontsize=20,fontweight='bold')
#        
#        # vertical lines at separation      
#        plt.axvline(from_date,color='grey',linewidth=1).set_linestyle('--')
#        plt.axvline(to_date,color='grey',linewidth=1).set_linestyle('--')
    

    plt.savefig('figs/'+str(station_name)+'.png', format='png', dpi=300)
    plt.clf()
    return 0

   
    
#stations=  np.unique(data1[1:,0])
stations=np.array(['TSKB','KUAL','KOKB','COCO','BAKO','IISC','KUNM','MAC1','MKEA','NTUS','PERT','PIMO','YAR1','HYDE','TNML','ALIC','PHKT'])

lst = [0]*len(stations)
lst_special = []
for sta in range(len(stations)):
    lst[sta] = (data1[data1[:,0]==stations[sta]][-1][5].astype('f8'),data1[data1[:,0]==stations[sta]][-1][5].astype('f8'))

# to force single trendline for height    
lst_special = lst

lst[np.where(stations=='KUAL')[0]]=(2005,2007.5)
lst[np.where(stations=='PHKT')[0]]=(2005,2005.5)
lst[np.where(stations=='NTUS')[0]]=(2004.9,2008)

print lst
for i in range(len(stations)):
    plotter(stations[i],lst[i],lst_special[i])

