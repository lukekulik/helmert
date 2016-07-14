import numpy as np

#npyfile =  np.load('data2005-2007.npy')

def outlierlong(npyfile):
    #making a list of all the station names
    allstationnames = np.unique(npyfile[1:, 0])
    
    #print len(allstationnames)
    
    
    #Define initial arrays
    final_lon_values = np.array([['name'],['lon_value'],['week'],['year']]).T
    final_lat_values = np.array([['name'],['lat_value'],['week'],['year']]).T
    final_height_values = np.array([['name'],['height_value'],['week'],['year']]).T
    
    
    final_lon_outlier = np.array([['name'],['lon_outlier'],['week'],['year']]).T
    final_lat_outlier = np.array([['name'],['lat_outlier'],['week'],['year']]).T
    final_height_outlier = np.array([['name'],['height_outlier'],['week'],['year']]).T
    
    
    for i in range(len(allstationnames)):
        datafile = npyfile[npyfile[:, 0] == str(allstationnames[i])]
        #print datafile
        onlydata = datafile[0:, 1:4]
        
        #defining array with week & year numbers
        weekyear = datafile[0:,4:6]
        
        name = datafile[0:,0]
        justname = datafile[0,0]    
        
        #defining araay with only lon,lat,height data for concatenating with weekyear
        onlylondata = np.array([onlydata[0:,0]]).T
        onlylatdata = np.array([onlydata[0:,1]]).T
        onlyheightdata = np.array([onlydata[0:,2]]).T
        
        #making 3 arrays with lon,lat,height data with also the weekyear
        onlylondata = np.column_stack((onlylondata, weekyear))
        onlylatdata = np.column_stack((onlylatdata, weekyear))
        onlyheightdata = np.column_stack((onlyheightdata, weekyear))
        
                        
        #USING THE MODIFIED Z-METHOD
        #puts the desired data in an array
        data = np.array(onlydata).astype('f8')
        
        #find the median for the x,y,z values
        medians = np.array(np.median(onlydata.astype('f8'),axis=0))
        
        #subtracht the median from the data valuses
        residual = np.subtract(data,medians)
        
        #finds the median of the residuals
        MAD = np.array(np.median(np.abs(residual).astype('f8'),axis=0))
        
        if MAD[MAD==0].size!=0:         # If any value in MAD is zero
            MAD[MAD==0]=1.              # set that entry = 1.
            #MAD = np.array([1,1,1])
                            
        #compute the modified Z-score
        modZscore = np.abs((0.6745*residual)/(MAD))
        #weightmatrix = np.array([[1.,1.,1.],[0.,0.,0.],[1.,1.,1.]])
        #aaverage = np.average(data, axis=0, weights=weightmatrix)
        
        weightmatrix = modZscore
        weightmatrix[weightmatrix<2.]=1.
        weightmatrix[weightmatrix>2.]=0.   # =1. for no outlier detection
        
        #print weightmatrix
        
        lonoutliers= np.array([weightmatrix[:,0]]).T
        latoutliers= np.array([weightmatrix[:,1]]).T
        heightoutliers= np.array([weightmatrix[:,2]]).T
        
        lonoutliers = np.column_stack((lonoutliers, weekyear))
        latoutliers = np.column_stack((latoutliers, weekyear))
        heightoutliers = np.column_stack((heightoutliers, weekyear))
        
        #print lonoutliers
        
        
        ##########For the longitude file###############
        outlierpositionslon = np.where(lonoutliers[0:,0]=='0.0')
        outlierdatalon = np.array([['name'],['position'],['week'],['year']]).T
        datalon = np.array([['name'],['position'],['week'],['year']]).T
        
        for i in range(len(outlierpositionslon[0])):
            positionlon = outlierpositionslon[0][i]
            
            resultslon = np.hstack((justname,onlylondata[positionlon]))
            outlierdatalon = np.vstack((outlierdatalon,resultslon))
        
            
        #make arrays ready 
        a_lon= onlylondata[0:,0]
        outlierlonfinal= outlierdatalon[1:,0:]
        
        b_lon = outlierlonfinal[0:,0]
        
        #find intersection of outliers and alldata  
        intersectionlon = np.intersect1d(a_lon, b_lon)
        #find pointers for later removing
        pointerlon = np.argwhere(np.in1d(a_lon, b_lon) == True)
        
        #remove the outlier value,week,year 
        lonname = np.delete(name, pointerlon)
        lonpos = np.delete(onlylondata[0:,0], pointerlon)
        lonweek = np.delete(onlylondata[0:,1], pointerlon)
        lonyear = np.delete(onlylondata[0:,2], pointerlon)
        #stack the columns together for final result
        lonfinal = np.column_stack((lonname,lonpos,lonweek,lonyear))
        
        #print lonfinal
        
        
        
        
        ##########For the latitude file###############
        outlierpositionslat = np.where(latoutliers[0:,0]=='0.0')
        outlierdatalat = np.array([['name'],['position'],['week'],['year']]).T
        datalat = np.array([['name'],['position'],['week'],['year']]).T
        
        for i in range(len(outlierpositionslat[0])):
            positionlat = outlierpositionslat[0][i]
            
            resultslat = np.hstack((justname,onlylatdata[positionlat]))        
            outlierdatalat = np.vstack((outlierdatalat,resultslat))
        
        #make arrays ready 
        a_lat= onlylatdata[0:,0]
        outlierlatfinal = outlierdatalat[1:,0:]
        b_lat = outlierlatfinal[0:,0]
        
        #find intersection of outliers and alldata  
        intersectionlat = np.intersect1d(a_lat, b_lat)
        #find pointers for later removing
        pointerlat = np.argwhere(np.in1d(a_lat, b_lat) == True)
        
        #remove the outlier value,week,year 
        latname = np.delete(name, pointerlat)
        latpos = np.delete(onlylatdata[0:,0], pointerlat)
        latweek = np.delete(onlylatdata[0:,1], pointerlat)
        latyear = np.delete(onlylatdata[0:,2], pointerlat)
        #stack the columns together for final result
        latfinal = np.column_stack((latname,latpos,latweek,latyear))
        
        
        
        
        
        ##########For the height file###############
        outlierpositionsheight = np.where(heightoutliers[0:,0]=='0.0')
        outlierdataheight = np.array([['name'],['position'],['week'],['year']]).T
        dataheight = np.array([['name'],['position'],['week'],['year']]).T
        
        for i in range(len(outlierpositionsheight[0])):
            positionheight = outlierpositionsheight[0][i]
            
            resultsheight = np.hstack((justname,onlylatdata[positionheight]))
            outlierdataheight = np.vstack((outlierdataheight,resultsheight))
            
        #make arrays ready 
        a_height= onlyheightdata[0:,0]
        outlierheightfinal= outlierdataheight[1:,0:]
        b_height = outlierheightfinal[0:,0]
        
        #find intersection of outliers and alldata  
        intersectionheight = np.intersect1d(a_height, b_height)
        #find pointers for heighter removing
        pointerheight = np.argwhere(np.in1d(a_height, b_height) == True)
        
        #remove the outlier value,week,year 
        heightname = np.delete(name, pointerlat)
        heightpos = np.delete(onlyheightdata[0:,0], pointerheight)
        heightweek = np.delete(onlyheightdata[0:,1], pointerheight)
        heightyear = np.delete(onlyheightdata[0:,2], pointerheight)
        #stack the columns together for final result
        heightfinal = np.column_stack((heightname,heightpos,heightweek,heightyear))
        
        
        #####stacking the arrays on top of each other######
        # final output for _values   
        # fianl output for _outlier
        final_lon_values = np.vstack((final_lon_values,lonfinal))
        final_lat_values = np.vstack((final_lat_values,latfinal))
        final_height_values = np.vstack((final_height_values,heightfinal))
        
        final_lon_outlier =np.vstack((final_lon_outlier,outlierlonfinal))
        final_lat_outlier =np.vstack((final_lat_outlier,outlierlatfinal))
        final_height_outlier =np.vstack((final_height_outlier,outlierheightfinal))
        
    return final_lon_values,final_lat_values,final_height_values,final_lon_outlier,final_lat_outlier,final_height_outlier