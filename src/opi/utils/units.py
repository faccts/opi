"""
Contains conversion factors for different units. These are selected to be consistent with ORCA.
See the ORCA manual as reference for some of them:
https://www.faccts.de/docs/orca/6.1/manual/contents/orcaarchitecture/conversionfactors.html
"""

# Atomic unit of length (Bohr) to Angstrom
AU_TO_ANGST: float = 0.5291772083
# Angstrom to Atomic unit of length (Bohr)
ANGST_TO_AU: float = 1.0 / AU_TO_ANGST
# Atomic unit of energy (Hartree) to kcal/mol
AU_TO_KCAL: float = 627.5096080305927
# Atomic unit of energy (Hartree) to eV
AU_TO_EV: float = 27.2113834
# eV to wavenumbers (cm**-1)
EV_TO_CM: float = 8065.54477
# Wavenumbers (cm**-1) to MHz
CM_TO_MHZ: float = 29979.2458
# Product of an energy in eV and the corresponding wavelength in nm (h * c in eV nm),
# i.e., wavelength / nm = EV_TO_NM / (energy / eV). Derived from `EV_TO_CM` to be consistent with ORCA.
EV_TO_NM: float = 1.0e7 / EV_TO_CM
# Angstrom to meter
ANGST_TO_M = 1.0e-10
# Atomic unit of mass (Dalton) to kilogram (kg)
AMU_TO_KG = 1.66053906660e-27
