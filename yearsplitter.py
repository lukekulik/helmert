import os

import numpy as np


###########creating sets of all files per week####################

def yearsplitter(year):  # modified by lukasz to avoid for loops
    days = os.listdir(year)  # lists/takes all files in directory 'year'
    days.sort(key=str.lower)  # sort days ascending order
    days_array = np.array(days)  # convert to numpy array for faster operation

    t = round(days_array.shape[0] / 7)  # ~52.14 # calculate the number of full weeks
    # print t
    # print len(days_array)
    # print days_array[0:7*t].shape
    weeks_array = days_array[0:7 * t].reshape(t, 7)  # reshape the array into ~52 rows of weeks with columns of days

    weeks = weeks_array.tolist()  # back to list, because arrays have to be regular
    weeks[51] = weeks[51] + days_array[7 * t:].tolist()  # adding the remainder to week 52
    # print weeks[0]
    # print weeks[51]
    return weeks


###########creating sets of all ITRF files per week####################

def yearsplitterITRF(year):
    weeks = os.listdir(year)  # lists/takes all files in directory 'ITRF/yearITRF'
    weeks.sort(key=str.lower)  # sort days ascending order
    weeks = np.array(weeks)  # added conversion to numpy array for faster operation ~ lukasz
    return weeks
