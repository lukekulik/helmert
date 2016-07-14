import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt


#npyfile =  np.load('total_data_array.npy')

def outlierlong(npyfile):
    #making a list of all the station names
    allstationnames = np.unique(npyfile[1:, 0])
    #allstationnames = np.array(['ALGO','BAKO'])
    
    
    #Define initial arrays
    final_values = np.array([['name'],['final_value'],['week'],['year']]).T
    final_outlier = np.array([['name'],['final_outlier_value'],['week'],['year']]).T
    
    
    for i in range(len(allstationnames)):
    #for i in range(2):
        datafile = npyfile[npyfile[:,0] == str(allstationnames[i])]
        
        #define element with only the name
        justname = datafile[0,0]
        #define an array with only the names of same station
        names = datafile[0:,0]
        #defining array, with weeks and years
        weeks = datafile[0:,2:3]
        
        year = datafile[0:,3:4]
        #making an array with all the time steps
        time_coord=year.astype('f8')+weeks.astype('f8')/52.
        #making an array with all the lon or lat or height values        
        onlydata = np.array([datafile[0:,1]]).T
       
        #evulating the data with a least square regression analasis        
        res = stats.mstats.theilslopes(onlydata.astype('f8'), time_coord, 0.95)
        #using the res values, creat array with corresponding values
        function_outcome = res[1] + res[0] * time_coord
        
        #compute the residuals of function_outcome minus onlydata
        residual = np.subtract(function_outcome,onlydata.astype('f8'))
        #find the MAD value
        MAD = np.array(np.average(np.abs(residual).astype('f8'),axis=0))
        
        if MAD[MAD==0].size!=0:         # If any value in MAD is zero
            MAD[MAD==0]=100.              # set that entry = 1.
        
        #compute the modified Z-score
        modZscore = np.abs((0.6745*residual)/(MAD))
        
        weightmatrix = modZscore

        weightmatrix[weightmatrix<2.0]=1.
        weightmatrix[weightmatrix>2.0]=0.   # =1. for no outlier detection
        
        
        #adding the corresponding week en year number to the find outliers(which have a value of zero)
        outliers = np.column_stack((weightmatrix, weeks,year))
        #creat initial array for adding the later found outliers        
        outlierdata = np.array([['name'],['outlier position'],['week'],['year']]).T
        correct_pos = np.array([['name'],['position'],['week'],['year']]).T
        
        ##########locate the outliers###############
        outlierpositions = np.where(outliers[0:,0]=='0.0')
        
        for i in range(len(outlierpositions[0])):
            #find the position of the outlier            
            position = outlierpositions[0][i]
            #makes an array [name,data,week,year] for the found outlier          
            resultslon = np.hstack((justname,onlydata[position],weeks[position],year[position]))
            #makes final array of all outlierdata            
            outlierdata = np.vstack((outlierdata,resultslon))
        
        #getting the right data for plotting of outlier
        weeks_outlier = outlierdata[1:,2]
        year_outlier = outlierdata[1:,3]
        time_axis_outlier = year_outlier.astype('f8')+ weeks_outlier.astype('f8')/52.
        outlier_values = outlierdata[1:,1]  
        
        
        #make arrays ready 
        a = onlydata
        b = outlier_values
        
        #find intersection of outliers and alldata  
        intersection = np.intersect1d(a, b)
        #find pointers for later removing
        pointer = np.argwhere(np.in1d(a, intersection) == True)
        
        #remove the outlier value,week,year 
        name = np.delete(names, pointer)
        pos = np.delete(onlydata, pointer)
        week = np.delete(weeks, pointer)
        year = np.delete(year, pointer)
        #stack the columns together for final result
        final_correct = np.column_stack((name,pos,week,year))
        #print outlierdata
        
        '''
        #getting the right dat for plotting of correct values
        weeks_correct = final_correct[0:,2]
        year_correct = final_correct[0:,3]
        time_axis_correct = year_correct.astype('f8')+ weeks_correct.astype('f8')/52.            
        final_correct_values = final_correct[0:,1]
        
               
        
       ####plotting, just for visualisation#
        #plt.xticks(np.unique(np.round(lon_x).astype(np.int)))
        plt.ylabel('Longitude [mm]')
        plt.autoscale(tight=True)
        plt.ticklabel_format(useOffset=False)
        ### PLOT commands
        plt.scatter(time_axis_correct,final_correct_values,color='black',s=3)
        plt.plot(time_coord,function_outcome,color='green')
        plt.scatter(time_axis_outlier,outlier_values,color='red',marker = 'x')        
        plt.minorticks_on()
        plt.show()
        
        #print outlierdata
        '''
        
        final_outlier = np.vstack((final_outlier,outlierdata[1:,0:]))
        final_values = np.vstack((final_values,final_correct))
    
    return final_outlier,final_values
    
           

#final_outlier,final_values = outlierlong(npyfile)       

#print final_outlier
        