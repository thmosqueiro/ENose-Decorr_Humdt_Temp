Scripts
====

In the following, we describe how to use the scripts in this
folder. We assume you have downloaded our dataset from UCI Machine
Learning repository (link should be provided soon).


Reproducing Figure 7
---

In Figure 7 we showed two examples of recordings of wine and banana
stimuli, one of each. Script _Plot_Figure7.py_ reproduces this plot
using matplotlib. The inductions used in the paper were recorded on
July 23rd, and are indexed in the dataset as 17 and 19. It will
generate a PNG file file in the same folder. Just run:

```
python Plot_Figure7.py
```

It will read the dataset (which should be in the same folder as this
script), get presentations with id 17 and 19 and plot them.

Below is the result:

<img src="https://raw.githubusercontent.com/thmosqueiro/ENose-Decorr_Humdt_Temp/master/script/Huerta_etal_2016_Figure7.png" width=300px style="float: left; margin: 0 0 10px 10px;" />


Splitting data into windows of 10min
---

Because the main topic of the paper is online analyses, one possible
methodology is to split the dataset in chunks of equal size. In the
paper, we divided each induction in time series of 10min of
length. The length of the chunks is determined by variable _deltaT_
(in hours).

The script to perform this operation is called _Features_split.py_,
and should be located in this directory. Assuming that the dataset is
also in this folder, simply run the following
```
python Features_split.py
```
Once it is finished (may take 20 seconds even in fast computers), it
will save two files: "_Dataset_Split10min.npy_" with the data
reformated for supervised training, and "_Dataset_SplitHash.npy_" with
the indices for each induction. The hash will be used during the
cross-validation to ensure fair training (see description in our
[paper](https://www.researchgate.net/publication/305385157_Online_decorrelation_of_humidity_and_temperature_in_chemical_sensors_for_continuous_monitoring)). This
routine was optimized by only using numpy functions.


Supervised learning
---

In the original papel we have used the [Inhibitory Support Vector
Machine](http://www.sciencedirect.com/science/article/pii/S092540051300590X)
(click [here](http://biocircuits.ucsd.edu/huerta/software.html) for an
implementation), we will use in this example a regular Support Vector
Machine despite not being Fisher consistent for multiclass problems
(see [this
paper](http://projecteuclid.org/euclid.ejs/1444316740)). The only
extra dependence needed for this section is
[scikit-learn](http://scikit-learn.org/).