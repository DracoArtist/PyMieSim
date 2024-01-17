"""
Cylinder: Qsca vs diameter
==========================

"""

# %%
# Importing the package dependencies: numpy, PyMieSim
import numpy as np

from PyMieSim.experiment.scatterer import Cylinder
from PyMieSim.experiment.source import Gaussian
from PyMieSim.experiment import Setup


from PyMieSim import measure

# %%
# Defining the ranging parameters for the scatterer distribution
scatterer_set = Cylinder(
    diameter=np.geomspace(6.36e-09, 10000e-9, 1000),
    index=[1.4],
    n_medium=1
)

# %%
# Defining the source to be employed.
source_set = Gaussian(
    wavelength=[500e-9, 1000e-9, 1500e-9],
    polarization_value=30,
    polarization_type='linear',
    optical_power=1e-3,
    NA=0.2
)

# %%
# Defining the experiment setup
experiment = Setup(
    scatterer_set=scatterer_set,
    source_set=source_set
)

# %%
# Measuring the properties
data = experiment.Get(measure.Qsca)

# %%
# Plotting the results
figure = data.plot(
    x=scatterer_set.diameter
)

_ = figure.show()
