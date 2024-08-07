|Logo|

|python|
|zenodo|
|colab|
|unittest|
|docs|
|PyPi|
|PyPi_download|


PyMieSim
========

PyMieSim is a software designed for comprehensive Mie scattering analysis, featuring a user-friendly installation and operation process. The characterization of the scattering event within PyMieSim is determined by a set of specific properties, as illustrated in the subsequent figure.

Currently, PyMieSim integrates three distinct solvers tailored to three different types of scatterers: spherical particles, infinite cylindrical particles, and core-shell spherical particles. Additional parameters governing the scattering event are contingent upon the attributes of the light source and the detector (when applicable). The attributes pertinent to each of these components are delineated in the ensuing figure.


.. image:: https://github.com/MartinPdeS/PyMieSim/raw/master/docs/images/code_structure.png
  :width: 800
  :alt: Structure of the library

The package is divided into two submodules: **single** and **experiment**. The first one (`single`) is devised to analyse properties of single scattering event, such as the far-field distribution, scattering phase function, Stokes parameters, etc. On the other hand the `experiment` submodule serves studying parameters (such as `coupling (power)`, `Qsca`, `Qext`, `g`, etc)  over large sets of `source`, `scatterer` and/or `detector` sets.


----

Getting started
****************

PyMieSim was developed to be a used in Python script as shown in the documentation section. Although, since version 1.7.0 it is possible to use the new graphical user interface. To use is, you first need to install it:

.. code-block:: python

   >>> pip install PyMieSim

Once this is done you can run the graphic interface as follows:

.. code-block:: python

   >>> python -m PyMieSim

Clicking the "Calculate" button should render the following:

|example_gui|


----

Installation
************

For common versions of Windows, Linux, and macOS, (on x86_64 architecture), the package can readily be installed using pip;

.. code-block:: python

   >>> pip install LightWave2D

----

Documentation
**************
All the latest available documentation is available `here <https://pymiesim.readthedocs.io/en/latest/>`_ or you can click the following badge:

|docs|

----

Google Colab
**************
It's 2024, you don't need to run all your code on you computer anymore. Google Colab is a platform which allows to write/use python scripts remotely.
You can open the PyMieSim.ipynb in the file to access it or click on the following "Open in Colab" badge:

|colab|

----


Installation
************

For common version of Windows, Linux and MacOS, (on x86_64 architecture), the package can readily be installed using pip;

.. code-block:: python

   >>> pip install PyMieSim

The ready to install wheel is not available for arm chip of the newer mac M1, M2 ... product. You can however install manually the package.


If, however, this fail you can build the package from scratch following the steps on the **Manual building** section.

**Note:** Wheel support now extended to `manylinux2014 <https://www.python.org/dev/peps/pep-0599/>`_.


----



Manual building
***************

To manually buld the project on your computer make sure that you do have gcc installed (c++ and fortran compiler), plus python version 3.7+.
For windows system I recommend install MingGW with g++ and fortran compiler.

This being done, the following commands should do the trick.

Linux / MacOs
~~~~~~~~~~~~~

.. code-block:: python

   >>> git clone https://github.com/MartinPdeS/PyMieSim.git
   >>> cd PyMieSim
   >>> git submodule init && git submodule update
   >>> mkdir build
   >>> cd build
   >>> cmake ../ -G"Unix Makefiles" (macOS, Linux)
   >>> cmake ../ -G"MinGW Makefiles" (Windows)
   >>> sudo make install
   >>> cd ..
   >>> python -m pip install .

----

Testing
*******

To test localy (with cloning the GitHub repository) you'll need to install the dependencies and run the coverage command as

.. code:: python

   >>> git clone https://github.com/MartinPdeS/PyMieSim.git
   >>> cd PyMieSim
   >>> pip install PyMieSim[testing]
   >>> pytest
----


Result examples
***************
Here are two examples that showcases the computational abilities of PyMieSim


# Plasmonic resonances for Core/Shell particles with SIO2 inner layer and Gold outer layer

|example_plasmon|



# Scattering efficiency as a function of diameter for spherical scatterers.

|example_qsca|



Coding examples
***************

PyMieSim was developed with the aim of being an intuitive and easy to use tool.
Below is an example that illustrate this:

.. code:: python

   import numpy
   from PyMieSim.experiment.detector import Photodiode
   from PyMieSim.experiment.scatterer import Sphere
   from PyMieSim.experiment.source import Gaussian
   from PyMieSim.experiment import Setup

   from PyMieSim import measure
   from PyOptik import UsualMaterial

   source = Gaussian(
       wavelength=1200e-9,
       polarization_value=90,
       polarization_type='linear',
       optical_power=1e-3,
       NA=0.2
   )

   scatterer = Sphere(
       diameter=numpy.linspace(100e-9, 3000e-9, 600),
       material=UsualMaterial.BK7,
       medium_index=1.0,
       source=source
   )

   detector = Photodiode(
       NA=[0.15, 0.1, 0.05],
       phi_offset=-180.0,
       gamma_offset=0.0,
       sampling=600,
       polarization_filter=None
   )

   experiment = Setup(
       scatterer=scatterer,
       source=source,
       detector=detector
   )

   data = experiment.get(measure.coupling)

   figure = data.plot(
       x=experiment.diameter,
       y_scale='linear',
       normalize=True
   )

   figure.show()


Plenty of other examples are available online, I invite you to check the `examples <https://pymiesim.readthedocs.io/en/master/gallery/index.html>`_
section of the documentation.


----

Scientific article
******************
The associated article is free of access on this link `article <https://opg.optica.org/optcon/fulltext.cfm?uri=optcon-2-3-520&id=526697>`_


Citing this work?
******************
I spent a full year to develop this tool for you to use so if it helped you in your research, I would greatly appreciate you citing the article associated to my work. Many thanks!

.. code-block:: none

   @article{PoinsinetdeSivry-Houle:23,
       author = {Martin Poinsinet de Sivry-Houle and Nicolas Godbout and Caroline Boudoux},
       journal = {Opt. Continuum},
       keywords = {Light scattering; Mie theory; Optical coherence tomography; Radiation pressure; Scattering theory; Surface plasmon resonance},
       number = {3},
       pages = {520--534},
       publisher = {Optica Publishing Group},
       title = {PyMieSim: an open-source library for fast and flexible far-field Mie scattering simulations},
       volume = {2},
       month = {Mar},
       year = {2023},
       url = {https://opg.optica.org/optcon/abstract.cfm?URI=optcon-2-3-520},
       doi = {10.1364/OPTCON.473102},
       abstract = {},
   }

----



Contact Information
************************
As of 2024, the project is still under development. If you want to collaborate, it would be a pleasure! I encourage you to contact me.

PyMieSim was written by `Martin Poinsinet de Sivry-Houle <https://github.com/MartinPdS>`_  .

Email:`martin.poinsinet-de-sivry@polymtl.ca <mailto:martin.poinsinet-de-sivry@polymtl.ca?subject=PyMieSim>`_ .

.. |python| image:: https://img.shields.io/pypi/pyversions/pymiesim.svg
   :target: https://www.python.org/

.. |zenodo| image:: https://zenodo.org/badge/DOI/10.5281/zenodo.5593704.svg
   :target: https://doi.org/10.5281/zenodo.4556074

.. |colab| image:: https://colab.research.google.com/assets/colab-badge.svg
   :target: https://colab.research.google.com/drive/1FUi_hRUXxCVvkHBY10YE1yR-nTATcDei?usp=sharing

.. |docs| image:: https://readthedocs.org/projects/pymiesim/badge/?version=latest
   :target: https://pymiesim.readthedocs.io/en/latest/

.. |PyPi| image:: https://badge.fury.io/py/PyMieSim.svg
    :target: https://badge.fury.io/py/PyMieSim

.. |Logo| image:: https://github.com/MartinPdeS/PyMieSim/raw/master/docs/images/logo.png

.. |example_plasmon| image:: https://github.com/MartinPdeS/PyMieSim/raw/master/docs/images/plasmonic_resonances.png

.. |example_qsca| image:: https://github.com/MartinPdeS/PyMieSim/raw/master/docs/images/Qsca_diameter.png

.. |PyPi_download| image:: https://img.shields.io/pypi/dm/PyMieSim.svg
   :target: https://pypistats.org/packages/pymiesim

.. |unittest| image:: https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/MartinPdeS/f0955be398d59efac69042c1b0fbece2/raw/a3b36ca9f6bebaab5180686bef481ed0d2ebfb71/PyMieSimcoverage_badge.json

.. |code_structure| image:: https://github.com/MartinPdeS/PyMieSim/raw/master/docs/images/code_structure.png
  :width: 800
  :alt: Structure of the library

.. |example_gui| image:: https://github.com/MartinPdeS/PyMieSim/raw/master/docs/images/example_gui.png
  :width: 800
  :alt: Structure of the library
