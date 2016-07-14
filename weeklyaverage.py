import numpy as np


#strange things happen with BABH
# check for the real data set if it works and how the standard of 3.5 behaves for the data

#transcoord= np.array([['ARAU',4,-2,4,0,2005],['ARAU',8,4,2,0,2005],['ARAU',6,5,3,0,2005],['BABH',3,3,3,0,2005],['BABH',5,3,3,0,2005],['BABH',6,4,5,0,2005],['ALGO',1.1,1,1,1,2005],['ALGO',3,1,1,1,2005]])
#weeks = [['week1'],['week2'],['week3']]


# make a outlier detection before computing the average with first
# finding the averag of 7 days, substracting this from the values itself, take then absolute value and do something with standard deviation
# if value is bigger then the set limit, remove point and find average again


#a = transcoord[0:1,1:4]
#b = transcoord[1:4,1:4].astype('f8')

#print b
#print np.median(b,axis=1)


def weeklyaverage(transcoord, weeks):
    # Define all the stationnames
    allstationnames = np.unique(transcoord[:, 0])

    # Make a setup for final outcome, those
    finalaverages = np.array(['name', 'x-coord', 'y-coord', 'z-coord', 'week', 'year'])
    finalstd = np.array(['name', 'x-std', 'y-std', 'z-std', 'week', 'year'])

    # make a loop for all the weeks
    for w in range(len(weeks)):
        # get all the data of one week
        tempcoord = transcoord[transcoord[:, 4] == str(w)]

        for i in range(len(allstationnames)):
            # get all the data of one station for one particular week
            tempstationcoord = tempcoord[tempcoord[:, 0] == str(allstationnames[i])]

            if len(tempstationcoord) > 2:
                # only use stations where there are more then 3 data points
                # if there are less than 3 data points, skip it
                
                stationname = tempstationcoord[0:1, 0:1]
                weekyear = tempstationcoord[0:1, 4:6]
                onlydata = tempstationcoord[0:, 1:4]
                
                #USING THE MODIFIED Z-METHOD
                #puts the desired data in an array
                data = np.array(onlydata).astype('f8')
                #find the median for the x,y,z values
                medians = np.array(np.median(onlydata.astype('f8'),axis=0))
                #subtracht the median from the data valuses
                residual = np.subtract(data,medians)
                #finds the median of the residuals
                MAD = np.array(np.median(np.abs(residual).astype('f8'),axis=0))
                #MAD = np.array([1,1,1])
                if MAD[MAD==0].size!=0:         # If any value in MAD is zero
                    MAD[MAD==0]=1.              # set that entry = 1.
                    #MAD = np.array([1,1,1])
                    
                #compute the modified Z-score
                modZscore = np.abs((0.6745*residual)/(MAD))
                #weightmatrix = np.array([[1.,1.,1.],[0.,0.,0.],[1.,1.,1.]])
                #aaverage = np.average(data, axis=0, weights=weightmatrix)
                
                weightmatrix = modZscore
                weightmatrix[weightmatrix<3.5]=1.
                weightmatrix[weightmatrix>3.5]=0.   # =1. for no outlier detection
                
                #compute the averages taking into account the weight, is it or is it not an outlier
                aaverage = np.average(data, axis=0, weights=weightmatrix)
                
                # all outlier will get the value of zero
                stddata= weightmatrix*data
                
                #devide stddata into colums for x,y,z
                xdata = stddata[:,0]
                ydata = stddata[:,1]
                zdata = stddata[:,2]
                
                #remove all the zero's
                xdata = xdata[xdata!=0]
                ydata = ydata[ydata!=0]
                zdata = zdata[zdata!=0]
                
                #compute the std for x,y,z data 
                xstd = np.std(xdata.astype('f8'), axis = 0)
                ystd = np.std(ydata.astype('f8'), axis = 0)
                zstd = np.std(zdata.astype('f8'), axis = 0)
                
                #add them together in one array 
                stdtotal = np.array([xstd,ystd,zstd])
                
                # add the averages and std in one array
                averagetotal = np.hstack((stationname[0], aaverage, weekyear[0]))
                stdtotal = np.hstack((stationname[0], stdtotal, weekyear[0]))
                
                #stack the averagtotal and stdtotal together for returning array
                finalaverages = np.vstack((finalaverages, averagetotal))
                finalstd = np.vstack((finalstd, stdtotal))
                
    return finalaverages[1:, :], finalstd[1:, :]


#finalaverages,finalstd = weeklyaverage2(transcoord, weeks)
#print finalaverages