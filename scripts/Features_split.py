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

## Importing metadata and induction information
metadata = np.loadtxt('HT_Sensor_metadata.dat', skiprows=1, dtype=str)
metadata[ metadata[:,2] == "wine", 2 ] = 2
metadata[ metadata[:,2] == "banana", 2 ] = 2
metadata[ metadata[:,2] == "background", 2 ] = 0
metadata = np.array( metadata[:,[0,2,3,4]], dtype=float )

## Loading the dataset
dataset = np.loadtxt('HT_Sensor_dataset.dat', skiprows=1)


## Useful definitions

deltaT = 1./6.  # 10 minutes in hours
window = 10*10
onemin = 1./60.

def numWindows(tot, deltaT):
    """ Evaluates the number of windows that will be used
    given the total time (tot) of a particular induction.
    """
    return int( (tot - deltaT)*60. )



## Array to store features
result    = []


## Splitting

for ind in np.array( metadata[:20,0], dtype=int) :
    
    print ">> Processing induction id %d" % ind
    
    nwin = numWindows(metadata[ind,3], deltaT)    # Getting the total time
    
    dataset_ = dataset[ dataset[:,0] == ind, 1: ]   # Separating a single induction
    dataset_[:,0] = dataset_[:,0]*60              # converting to minutes
    mins = np.unique( np.array( dataset_[:,0], dtype=int) )
    tfmin = metadata[ind,3]*60
    
    print " Number of points: %d" % dataset_.shape[0]

    # Preparing an array for the sub-sampled version of the data
    data_subsamp = np.zeros( (mins.shape[0],11) )
    
    indx = 0
    for tmin in mins:
        data_subsamp[indx, 0] = tmin
        data_subsamp[indx, 1:] = dataset_[ np.where( np.abs(dataset_[:,0] - tmin) > 0.1 ), 1: ].mean(axis=1)
        indx += 1
    

    induct = data_subsamp[ np.logical_and( data_subsamp[:,0] >= 0 , data_subsamp[:,0] < tfmin-1  )  , 1: ]
    induct = np.reshape(induct, (induct.shape[0] * induct.shape[1]))
    
    ## Constructing the moving window
    shape = induct.shape[:-1] + (induct.shape[-1] - window + 1, window)
    strides = induct.strides + (induct.strides[-1],)
    dataSplit = np.lib.stride_tricks.as_strided(induct, shape=shape, strides=strides)[0:-1:10]

    
    result.append( dataSplit )
    
np.save("Dataset_Split10min", result)
