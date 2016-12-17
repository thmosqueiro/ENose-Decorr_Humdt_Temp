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


## Should create plots of the inductions after subsampling?
createPlot = False

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
hashtable = []


## Splitting

for ind in np.array( metadata[:,0], dtype=int) :
    
    print ">> Processing induction id %d" % ind
    
    dataset_ = dataset[ dataset[:,0] == ind, 1: ]   # Separating a single induction
    dataset_[:,0] = dataset_[:,0]*60                # converting to minutes
    mins = np.unique( np.array( dataset_[:,0], dtype=int) )
    
    tfmin = metadata[ind,3]*60
    print " Duration of the induction: %4.2f" %  tfmin

    # Minutes during induction (there may be minutes missing due to data loss)
    mins_ind = mins[ np.logical_and( mins >= 0 , mins < int(tfmin)  ) ]

    ## Checking if the induction has at least one window
    if tfmin < 9 or mins_ind.shape[0] < 9:
        print " Induction with lower duration than threshold."
        
    else:

        # Getting the total number of windows
        nwin = numWindows(tfmin, deltaT)

        ## Finding missing time stamps

        # Fixed list of minutes
        mins_ind_fixtime = np.copy(mins_ind)
        
        # Checking if there are missing data at the beggining
        # of the induction
        if ( mins_ind[0] > 0 ): ## this means that 0 was missed
            print " Missed data at the beggining of induction "
            t0 = mins_ind[0]
            nwin = nwin - mins_ind[0]
        else:
            t0 = 0
            
        
        # Checking for missing time stamps during the induction...
        dmins      = np.diff(mins_ind)
        locmissing = np.where( dmins > 1 )[0] + 1
        if ( locmissing.shape[0]  > 0 ):
            print " Missed time stamps: %d" % np.sum( dmins[locmissing-1] )
        
        uplocmiss  = []  # updated location of the missing points
        
        # Adding and indexing missing time stamps
        offset = 0
        for j in range(locmissing.shape[0]):
            values = np.arange(0, dmins[locmissing[j]-1]-1) + mins_ind_fixtime[locmissing[j]-1+offset] + 1
            mins_ind_fixtime = np.insert( mins_ind_fixtime, locmissing[j]+offset, values )
            
            offset += dmins[locmissing[j]-1] - 1
            uplocmiss.append( values )
            
        
        # Preparing an array for the sub-sampled version of the data
        data_subsamp = np.zeros( (mins_ind_fixtime.shape[0],10) )
        
        # Constructing the subsampled array without missing points
        for tmin in mins_ind:
            data_subsamp[int(tmin) - t0,:] = dataset_[ np.abs(dataset_[:,0] - tmin) < 0.1 , 1: ].mean(axis=0)

        # Fixing missing points a posteriori
        for missed in uplocmiss:
            x0 = data_subsamp[ missed[0]  - 1 - t0]
            xf = data_subsamp[ missed[-1] +  1 - t0 ]
            step = 1
            alpha = (xf-x0)/float(len(missed))
            for x in missed:
                data_subsamp[x - t0,:] = x0 + alpha*step
                step + 1


        ## Creating plots with the subsampled version of the inductions
        if createPlot:
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
        
        print " Finished, now saving." 
        result.append( dataSplit )
        hashtable.append( ind )
        
        print ""


print ">> Saving the final dataset"
np.save("Dataset_Split10min", result)
np.save("Dataset_Split10min_hashtable", hashtable)

print "The end, my friend."
