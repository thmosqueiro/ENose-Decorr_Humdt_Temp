Online decorrelation of humidity and temperature in chemical sensors for continuous monitoring
====

In this repository, you will find snippets of code to exemplify how to
import, organize and plot data from [a recently published
paper](https://www.researchgate.net/publication/305385157_Online_decorrelation_of_humidity_and_temperature_in_chemical_sensors_for_continuous_monitoring)
where we propose a method for decorrelating humidity and temperature
from signals of MOX gas sensors. In particular, the code in this
repository reproduces figure 7 and first line in table 3. The dataset
is publicly available at [UCI Machine Learning repository](http://archive.ics.uci.edu/ml/datasets/Gas+sensors+for+home+activity+monitoring) and contains recordings of a gas sensor array
(picture below) composed of 8 MOX gas sensors, and a temperature and
humidity sensor. This sensor array was exposed to background home
activity while subject to two different stimuli: wine and banana. The
responses to banana and wine stimuli were recorded by placing the
stimulus close to the sensors. The duration of each stimulation varied
from 7min to 2h, with an average duration of 42min. This dataset
contains a set of time series from three different conditions: wine,
banana and background activity. There are 36 inductions with wine, 33
with banana and 31 recordings of background activity. One possible
application is to discriminate among background, wine and banana.

<img src="https://raw.githubusercontent.com/thmosqueiro/ENose-Decorr_Humdt_Temp/master/images/GasSensorArray_picture.png" width=300px style="float: left; margin: 0 0 10px 10px;" />
<img src="https://raw.githubusercontent.com/thmosqueiro/ENose-Decorr_Humdt_Temp/master/images/Sensirion.jpg" width=300px style="float: left; margin: 0 0 10px 10px;" />


Download the dataset
---

The dataset is publicly available at [UCI Machine Learning repository](http://archive.ics.uci.edu/ml/datasets/Gas+sensors+for+home+activity+monitoring), and contains recordings of a gas sensor array (see picture above). We kindly request that you cite our paper if you use our dataset (see [Relevant papers](https://github.com/thmosqueiro/ENose-Decorr_Humdt_Temp#relevant-papers) below). The size of the zipped dataset is _28MB_.


Relevant papers
---

If you find this useful, please star this repository and/or cite our paper:

Ramon Huerta, Thiago Mosqueiro, Jordi Fonollosa, Nikolai Rulkov, Irene Rodriguez-Lujan. **Online Decorrelation of Humidity and Temperature in Chemical Sensors for Continuous Monitoring.** [Chemometrics and Intelligent Laboratory Systems](https://www.researchgate.net/publication/305385157_Online_decorrelation_of_humidity_and_temperature_in_chemical_sensors_for_continuous_monitoring) 2016.


Directions for loading the dataset in python
---

For a quick & dirty example for loading our dataset in python, only numpy is necessary. Assuming that the dataset files are in the same folder, the snippet below is enough to load the data.

```
import numpy as np

## Importing dataset
metadata = np.loadtxt('HT_Sensor_metadata.dat', skiprows=1, dtype=str)

## Loading the dataset
dataset = np.loadtxt('HT_Sensor_dataset.dat', skiprows=1)
```

Then, variable metadata has all the metadata, and dataset has the actual recordings. Because file HT_Sensor_dataset.dat is 108MB, it may take a few seconds to load it (in an Intel i7 3.2GHz, it takes about 17 seconds). The time series of induction with a given id, say 17, you can use the following piece of code:

```
id = 17.
timeSeries = dataset[ dataset[:,0] == id, 1:]
```

The 1 in "1:" above removes the column with id, leaving variable _timeSeries_ with only data from the recording with id 17. 


Co-authors
---

[Ramon Huerta](http://biocircuits.ucsd.edu/huerta/), BioCircuits Institute, University of California San Diego

[Thiago Mosqueiro](http://thmosqueiro.vandroiy.com), BioCircuits Institute, University of California San Diego

[Jordi Fonollosa](https://jordifonollosa.wordpress.com/), Institute for Bioengineering of Catalunya & University of Barcelona

[Nikolai Rulkov](http://biocircuits.ucsd.edu/rulkov/), BioCircuits Institute, University of California San Diego

[Irene Rodriguez-Lujan](https://sites.google.com/site/irenerodriguezlujan/), Escuela Politecnica Superior, Universidad Autonoma de Madrid


Acknowledgements
---

* [Xuezhen (Tina) Hong](https://github.com/XuezhenHong), for reviewing and providing feedback on the code.


Dependencies
---

* Dataset, which is available at UCI Machine Learning Repository

* Python 2.*

* numpy 11.*+

* matplotlib 1.10+


License
---

**tl;dr version:** please, don't sue me and ship a copy of the License
  file with any derived product. Read License file for the actual
  terms.
