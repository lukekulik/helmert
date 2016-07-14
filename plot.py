import matplotlib.pyplot as plt
import numpy as np
from outlier_long import outlierlong
from matplotlib.pyplot import *

def r_squared(actual, ideal):
    actual_mean = np.mean(actual)
    ideal_dev = np.sum([(val - actual_mean)**2 for val in ideal])
    actual_dev = np.sum([(val - actual_mean)**2 for val in actual])

    return ideal_dev / actual_dev


# Not orking yet. But a little more structured than yesterday. 
# first defines x-axis for lon,lat,height separatly


data1 = np.load('data.npy')
#station_name='KUAL'

#npyfile =  np.load('data2005-2007.npy')


def plotter(station_name,tup):
    
    temp=data1[data1[:,0]==station_name]
    tempXX=temp[(temp[:,4]!='00') & (temp[:,5]!='2011.0')]
    xaxis=tempXX[:,5].astype('f8')+tempXX[:,4].astype('f8')/52.
    tempXX[:,5]=tempXX[:,5].astype('f8')+tempXX[:,4].astype('f8')/52.
    
    
    lon,lat,height,lon_out,lat_out,height_out = outlierlong(data1)
    # lon x-axis
    lon=lon[lon[:,0]==station_name]
    lon_temp_x = lon[(lon[:,2]!='00') & (lon[:,3]!='2011.0')]
    lon_x=lon_temp_x[:,3].astype('f8')+lon_temp_x[:,2].astype('f8')/52.             # xaxis
    lon_temp_x[:,3]=lon_temp_x[:,3].astype('f8')+lon_temp_x[:,2].astype('f8')/52.   # tempXX
    # lat x-axis
    lat=lat[lat[:,0]==station_name]
    lat_temp_x = lat[(lat[:,2]!='00') & (lat[:,3]!='2011.0')]
    lat_x=lat_temp_x[:,3].astype('f8')+lat_temp_x[:,2].astype('f8')/52.             # xaxis
    lat_temp_x[:,3]=lat_temp_x[:,3].astype('f8')+lat_temp_x[:,2].astype('f8')/52.   # tempXX
    # height x-axis
    height=height[height[:,0]==station_name]
    height_temp_x = height[(height[:,2]!='00') & (height[:,3]!='2011.0')]
    height_x=lon_temp_x[:,3].astype('f8')+height_temp_x[:,2].astype('f8')/52.               # xaxis
    height_temp_x[:,3]=height_temp_x[:,3].astype('f8')+height_temp_x[:,2].astype('f8')/52.  # tempXX

   
    # lon outlier x-axis
    lon_out=lon_out[1:]
    lon_out=lon_out[lon_out[:,0]==station_name]
    lon_out=lon_out[(lon_out[:,2]!='00') & (lon_out[:,3]!='2011.0')]    
    xaxis_out = lon_out[:,3].astype('f8')+lon_out[:,2].astype('f8')/52.
    # lat outlier x-axis    
    lat_out=lat_out[1:]
    lat_out=lat_out[lat_out[:,0]==station_name]
    lat_out=lat_out[(lat_out[:,2]!='00') & (lat_out[:,3]!='2011.0')]    
    lat_out_x = lat_out[:,3].astype('f8')+lat_out[:,2].astype('f8')/52.
    # height outlier x-axis    
    height_out=height_out[1:]
    height_out=height_out[height_out[:,0]==station_name]
    height_out=height_out[(height_out[:,2]!='00') & (height_out[:,3]!='2011.0')]    
    height_out_x = height_out[:,3].astype('f8')+height_out[:,2].astype('f8')/52.
    
    from_date = tup[0]
    to_date = tup[1]
    

    ##### PLOT 1    
    plt.subplot(311)
    plt.title(station_name)
    plt.xticks(np.unique(np.round(lon_x).astype(np.int)))
    plt.xlabel('Year')
    plt.ylabel('Longitude [mm]')
    plt.autoscale(tight=True)
    plt.ticklabel_format(useOffset=False)
    ### PLOT commands
    plt.scatter(lon_x,lon_temp_x[:,1],color='black',s=8)
    plt.scatter(xaxis_out,lon_out[:,1],color='green',s=10, marker = 'x')

    ### FIRST PART
    # Trendline
    polyarray=lon_temp_x[lon_temp_x[:,3].astype('f8')<=from_date][:,2].astype('f8')
    z = np.polyfit(lon_x[0:len(polyarray)],polyarray,1)
    p = np.poly1d(z)
    plt.plot(lon_x[0:len(polyarray)],p(lon_x)[0:len(polyarray)],'r',linewidth=2,color='red')

    # r^2 annotating
    r_sq = r_squared(lon_temp_x[:,2].astype('f8')[0:len(polyarray)],p(lon_x[0:len(polyarray)]))
    plt.annotate('r^2 = {0:2f}'.format(r_sq), (0.7, 0.7), xycoords='axes fraction')

    # slope equation
    polyarray=lon_temp_x[lon_temp_x[:,3].astype('f8')<=from_date][:,2].astype('f8')
    (m,b) = np.polyfit(lon_x[0:len(polyarray)],polyarray,1)
    yp = np.polyval([m,b],lon_x)
    plt.annotate(str(round(m,3)) + ' [mm/year]', (0.7, 0.8), xycoords='axes fraction',annotation_clip=False,clip_on=False)
    
    # graph legend
    plt.annotate('-', (0.675, 0.72), xycoords='axes fraction', color = 'red',fontsize=25,fontweight='bold')

    
    ### SECOND PART
    if from_date != to_date:
        # Trendline        
        polyarray=lon_temp_x[lon_temp_x[:,3].astype('f8')>=to_date][:,2].astype('f8')
        len2=len(lon_x)-len(polyarray)
        (m,b) = np.polyfit(lon_x[len2:],polyarray,1)
        p = np.poly1d((m,b))
        plt.plot(lon_x[len2:],p(lon_x)[len2:],'r',linewidth=2,color='cyan')

        # r^2 annotating
        r_sq = r_squared(lon_temp_x[:,2].astype('f8')[len2:],p(lon_x[len2:]))
        plt.annotate('r^2 = {0:2f}'.format(r_sq), (0.7, 0.4), xycoords='axes fraction')

        # slope equation
        polyarray=lon_temp_x[lon_temp_x[:,3].astype('f8')<=from_date][:,2].astype('f8')
        yp = np.polyval([m,b],lon_x) 
        plt.annotate(str(round(m,3)) + ' [mm/year]', (0.7, 0.5), xycoords='axes fraction')

        # graph legend
        plt.annotate('-', (0.675, 0.42), xycoords='axes fraction', color = 'cyan',fontsize=20,fontweight='bold')
        
        # vertical lines at separation
        plt.axvline(from_date,color='grey',linewidth=1).set_linestyle('--')
        plt.axvline(to_date,color='grey',linewidth=1).set_linestyle('--')
    
    
    ##### PLOT 2
    plt.subplot(312)
    plt.xticks(np.unique(np.round(lat_x).astype(np.int)))
    plt.xlabel('Year')
    plt.ylabel('Latitude [mm]')
    plt.autoscale(tight=True)
    plt.ticklabel_format(useOffset=False)
    ### PLOT commands    
    plt.scatter(lat_x,lat_temp_x[:,1],color='black',s=8)
    
    ### FIRST PART
    # Trendline
    polyarray=lat_temp_x[lat_temp_x[:,3].astype('f8')<=from_date][:,1].astype('f8')
    z = np.polyfit(lat_x[0:len(polyarray)],polyarray,1)
    p = np.poly1d(z)
    plt.plot(lat_x[0:len(polyarray)],p(lat_x)[0:len(polyarray)],'r',linewidth=2,color='red')
    #
    # r^2 annotating
    r_sq = r_squared(lat_temp_x[:,1].astype('f8')[0:len(polyarray)],p(lat_x[0:len(polyarray)]))
    plt.annotate('r^2 = {0:2f}'.format(r_sq), (0.7, 0.7), xycoords='axes fraction')
    #
    # slope equation
    polyarray=lat_temp_x[lat_temp_x[:,3].astype('f8')<=from_date][:,1].astype('f8')
    (m,b) = np.polyfit(lat_x[0:len(polyarray)],polyarray,1)
    yp = np.polyval([m,b],lat_x)
    plt.annotate(str(round(m,3)) + ' [mm/year]', (0.7, 0.8), xycoords='axes fraction',annotation_clip=False,clip_on=False)
    #
    # graph legend
    plt.annotate('-', (0.675, 0.72), xycoords='axes fraction', color = 'red',fontsize=25,fontweight='bold')
    
    
    ### SECOND PART
    if from_date != to_date:
        # Trendline
        polyarray=lat_temp_x[lat_temp_x[:,3].astype('f8')>=to_date][:,1].astype('f8')
        len2=len(lat_x)-len(polyarray)
        (m,b) = np.polyfit(lat_x[len2:],polyarray,1)
        p = np.poly1d((m,b))
        plt.plot(lat_x[len2:],p(lat_x)[len2:],'r',linewidth=2,color='cyan')

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
    plt.scatter(height_x,height_temp_x[:,1],color='black',s=8)    
    
    ### FIRST PART
    # Trendline
    polyarray=height_temp_x[height_temp_x[:,3].astype('f8')<=from_date][:,3].astype('f8')
    z = np.polyfit(height_x[0:len(polyarray)],polyarray,1)
    p = np.poly1d(z)
    plt.plot(height_temp_x[0:len(polyarray)],p(height_x)[0:len(polyarray)],'r',linewidth=2,color='red')
    
    # r^2 annotating
    r_sq = r_squared(height_temp_x[:,3].astype('f8')[0:len(polyarray)],p(height_x[0:len(polyarray)]))
    plt.annotate('r^2 = {0:2f}'.format(r_sq), (0.7, 0.7), xycoords='axes fraction')

    # slope equation
    polyarray=height_temp_x[height_temp_x[:,3].astype('f8')<=from_date][:,3].astype('f8')
    (m,b) = np.polyfit(height_x[0:len(polyarray)],polyarray,1)
    yp = np.polyval([m,b],height_x)
    plt.annotate(str(round(m,3)) + ' [mm/year]', (0.7, 0.8), xycoords='axes fraction',annotation_clip=False,clip_on=False)

    # graph legend
    plt.annotate('-', (0.675, 0.72), xycoords='axes fraction', color = 'red',fontsize=25,fontweight='bold')
    
    
    ### SECOND PART
    if from_date != to_date:
        # Trendline
        polyarray=height_temp_x[height_temp_x[:,3].astype('f8')>=to_date][:,3].astype('f8')
        len2=len(height_x)-len(polyarray)
        (m,b) = np.polyfit(height_x[len2:],polyarray,1)
        p = np.poly1d((m,b))
        plt.plot(height_x[len2:],p(height_x)[len2:],'r',linewidth=2,color='cyan')

        # r^2 annotating
        r_sq = r_squared(height_temp_x[:,3].astype('f8')[len2:],p(height_x[len2:]))
        plt.annotate('r^2 = {0:2f}'.format(r_sq), (0.7, 0.4), xycoords='axes fraction')

        # slope equation
        plt.annotate(str(round(m,3)) + ' [mm/year]', (0.7, 0.5), xycoords='axes fraction')
        yp = np.polyval([m,b],height_x) 
        plt.annotate('-', (0.675, 0.42), xycoords='axes fraction', color = 'cyan',fontsize=20,fontweight='bold')
        
        # vertical lines at separation      
        plt.axvline(from_date,color='grey',linewidth=1).set_linestyle('--')
        plt.axvline(to_date,color='grey',linewidth=1).set_linestyle('--')
    

    plt.savefig('figs/'+str(station_name)+'.png', format='png', dpi=300)
    plt.clf()
    return 0

   
    
#stations=  np.unique(data1[1:,0])
stations=np.array(['KUAL','KOKB'])#,'COCO','BAKO','IISC','KUNM','MAC1','MKEA','NTUS','PERT','PIMO','YAR1','HYDE','TNML','ALIC','PHKT'])

lst = [0]*len(stations)
for sta in range(len(stations)):
    lst[sta] = (data1[data1[:,0]==stations[sta]][-1][5].astype('f8'),data1[data1[:,0]==stations[sta]][-1][5].astype('f8'))
    

lst[np.where(stations=='KUAL')[0]]=(2005,2005.25)
#lst[np.where(stations=='PHKT')[0]]=(2005,2005.5)
#lst[np.where(stations=='NTUS')[0]]=(2004.9,2008)

print lst
for i in range(len(stations)):
    plotter(stations[i],lst[i])

