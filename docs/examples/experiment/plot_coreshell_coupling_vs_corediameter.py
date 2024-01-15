"""
CoreShell: Coupling vs diameter
===============================

"""

# %%
# Importing the package dependencies: numpy, PyMieSim
import numpy
from PyMieSim.experiment import CoreShellSet, SourceSet, Setup, PhotodiodeSet
from PyMieSim import measure
from PyMieSim.materials import BK7, Silver

# %%
# Defining the ranging parameters for the scatterer distribution
# Here we look at core/shell scatterers and use constant shell diameter
# with variable core diameter
scatterer_set = CoreShellSet(
    core_diameter=numpy.geomspace(100e-09, 600e-9, 400),
    shell_width=800e-9,
    core_material=Silver,
    shell_material=BK7,
    n_medium=1
)

# %%
# Defining the source to be employed.
# The source is always a plane wave in the LMT framework.
# The amplitude is set to one per default.
source_set = SourceSet(
    wavelength=1200e-9,
    linear_polarization=90,
    optical_power=1e-3,
    NA=0.2
)

# %%
# Defining the detector to be employed.
# The detector is here set as a photodiode with different available numerical aperture [NA]
detector_set = PhotodiodeSet(
    NA=[0.1, 0.05],
    phi_offset=-180.0,
    gamma_offset=0.0,
    sampling=600,
    polarization_filter=None
)

# %%
# Defining the experiment setup
# With the source and scatterers defined we set them together
# in an experiment.
experiment = Setup(
    scatterer_set=scatterer_set,
    source_set=source_set,
    detector_set=detector_set
)

# %%
# Measuring the properties
# We are interesting here in the coupling parameter.
data = experiment.Get(measure.coupling)

# %%
# Plotting the results
figure = data.plot(
    x=scatterer_set.core_diameter,
    y_scale='linear',
    normalize=True,
    add_box=True
)

_ = figure.show()
