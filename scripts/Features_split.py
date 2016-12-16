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

deltaT = 10
window = deltaT*10

def numWindows(tfmin, deltaT):
    """ Evaluates the number of windows that will be used
    given the total time (tot) of a particular induction.
    """
    return int( (tfmin - deltaT) + 2 )



## Array to store features
result    = []


## Splitting

for ind in np.array( metadata[:,0], dtype=int) :
    
    print ">> Processing induction id %d" % ind
    
    dataset_ = dataset[ dataset[:,0] == ind, 1: ]   # Separating a single induction
    dataset_[:,0] = dataset_[:,0]*60                # converting to minutes
    mins = np.unique( np.array( dataset_[:,0], dtype=int) )
    
    tfmin = metadata[ind,3]*60
    print ">> Duration of the induction: %4.2f" %  tfmin
    nwin = numWindows(tfmin, deltaT)    # Getting the total time
    
    mins_ind = mins[ np.logical_and( mins >= 0 , mins < int(tfmin)  ) ]
    mins_ind_fixtime = np.copy(mins_ind)

    # Finding missing time stamps
    dmins      = np.diff(mins_ind)
    locmissing = np.where( dmins > 1 )[0] + 1
    
    uplocmiss  = []  # updated location of the missing points
    
    # Adding and indexing missing time stamps
    offset = 0
    for j in range(locmissing.shape[0]):
        values = np.arange(0, dmins[locmissing[j]-1]-1) + mins_ind_fixtime[locmissing[j]-1+offset] + 1
        mins_ind_fixtime = np.insert( mins_ind_fixtime, locmissing[j]+offset, values )
        
        offset += dmins[locmissing[j]-1] - 1
        uplocmiss.append( values )

    
    print " Number of points: %d" % dataset_.shape[0]
    print mins
    # Preparing an array for the sub-sampled version of the data
    data_subsamp = np.zeros( (mins_ind_fixtime.shape[0],10) )
    
    # Constructing the subsampled array without missing points
    for tmin in mins_ind:
        data_subsamp[int(tmin),:] = dataset_[ np.abs(dataset_[:,0] - tmin) < 0.1 , 1: ].mean(axis=0)

    # Fixing missing points a posteriori
    for missed in uplocmiss:
        x0 = data_subsamp[ missed[0]  - 1 ]
        xf = data_subsamp[ missed[-1] + 1 ]
        step = 1
        alpha = (xf-x0)/float(len(missed))
        for x in missed:
            data_subsamp[x,:] = x0 + alpha*step
            step + 1

    pl.figure()
    for j in range(10):
        pl.plot(data_subsamp[:,j])
    pl.savefig('Visualizing_Ind'+str(ind)+'.png', dpi=250)
    
    # Reshaping in order to facilitate the creation of the moving windows
    induct = np.reshape(data_subsamp, (data_subsamp.shape[0] * data_subsamp.shape[1]))
    
    ## Constructing the moving window
    shape = (induct.shape[0] - window + 1, window)
    strides = induct.strides + (induct.strides[-1],)
    dataSplit = np.lib.stride_tricks.as_strided(induct, shape=shape, strides=strides)[0:-1:10]

    
    result.append( dataSplit )
    
np.save("Dataset_Split10min", result)
