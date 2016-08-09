#####
# 
# 
# 
#
# In the paper, we have used inductions of July 23rd. Looking at the
# metadata, the id of the presentations are 17 (banana) and 19 (wine).
# 
#####

## Importing libraries
import numpy as np
import pylab as pl
import pandas as pd
import matplotlib.gridspec as gridspec


## Importing metadata and induction information
metadata = np.loadtxt('HT_Sensor_metadata.dat', skiprows=1, dtype=str)
metadata[ metadata[:,2] == "wine", 2 ] = 2
metadata[ metadata[:,2] == "banana", 2 ] = 2
metadata[ metadata[:,2] == "background", 2 ] = 0
metadata = np.array( metadata[:,[0,2,3,4]], dtype=float )

## Loading the dataset
dataset = np.loadtxt('HT_Sensor_dataset.dat', skiprows=1)


## Useful definitions

deltaT = 1./6.
onemin = 1./60.

def numWindows(tot, deltaT):
    """ Evaluates the number of windows that will be used
    given the total time (tot) of a particular induction.
    """
    return int( (tot - deltaT)*60. )



## Array to store features
result    = []
hashtable = np.zeros( (metadata.shape[0]), dtype = int )


## Splitting

for ind in range(19): # metadata[:,0]

    # number of windows to be used
    nwin = numWindows(metadata[ind,3], deltaT)
    
    # restricting the dataset
    dataset_ = dataset[ dataset[:,0] == ind, 1: ]
    
    for j in range(nwin):

        # evaluating indices
        IDX = np.logical_and(
            dataset_[:,0] >= j*onemin, dataset_[:,0] < j*onemin + 10*onemin )
        
        result.append( np.reshape( dataset_[IDX, 1:] , (-1,1) ) )
        
    hashtable[ind] = len(result)


np.save("Dataset_Split10min", result)
np.save("Dataset_SplitHash", hashtable)
