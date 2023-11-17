"""
Samples Properties
==================
"""

from PyMieSim.scatterer import Sphere
from PyMieSim.source import PlaneWave

source = PlaneWave(
    wavelength=450e-9,
    linear_polarization=0,
    amplitude=1
)

scatterer = Sphere(
    diameter=800e-9,
    source=source,
    index=1.4)

scatterer.print_properties()


# ___________________________OUTPUT___________________________________

# ----------------------------------------------------------------------
# Efficiencies   | Qsca             | 4.029799032677242
# ----------------------------------------------------------------------
#                | Qext             | 4.029799032677242
# ----------------------------------------------------------------------
#                | Qabs             | 0.0
# ----------------------------------------------------------------------
#                | Qback            | 4.973830378796597
# ----------------------------------------------------------------------
#                | Qratio           | 1.2342626365395144
# ----------------------------------------------------------------------
#                | Qpr              | 0.7925897259835781
# ----------------------------------------------------------------------
# cross-sections | Csca             | 2.025597925840332e-12 m²  (2.03e+00 μm²)
# ----------------------------------------------------------------------
#                | Cext             | 2.025597925840332e-12 m²  (2.03e+00 μm²)
# ----------------------------------------------------------------------
#                | Cabs             | 0 m²
# ----------------------------------------------------------------------
#                | Cback            | 2.5001198365166603e-12 m²  (2.50e+00 μm²)
# ----------------------------------------------------------------------
#                | Cratio           | 6.204080690484652e-13 m²  (6.20e+05 nm²)
# ----------------------------------------------------------------------
#                | Cpr              | 3.98399049673721e-13 m²  (3.98e+05 nm²)
# ----------------------------------------------------------------------
# others         | area             | 5.026548245743668e-13 m²  (5.03e+05 nm²)
# ----------------------------------------------------------------------
#                | index            | 1.4
# ----------------------------------------------------------------------
#                | g                | 0.7925897259835781
# ----------------------------------------------------------------------
