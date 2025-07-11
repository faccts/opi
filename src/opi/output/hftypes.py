from opi.models.string_enum import StringEnum


class Hftypes(StringEnum):
    """Enumeration to keep track of the different wavefunction types available in ORCA"""

    RHF = "rhf"
    """Restricted Hartree-Fock or Kohn-Sham calculation."""
    UHF = "uhf"
    """Unrestricted Hartree-Fock or Kohn-Sham calculation."""
    ROHF = "rohf"
    """Restricted Open-Shell Hartree-Fock or Kohn-Sham calculation"""
    CASSCF = "casscf"
    """Multiconfigurational wavefunction calculation."""
