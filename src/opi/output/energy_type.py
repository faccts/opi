from opi.models.string_enum import StringEnum


class EnergyType(StringEnum):
    """
    Enumeration of the energy types that `Output.get_energies()` and
    `Output.get_final_energy_components()` are known to return.

    ORCA names the energy types itself, so those dictionaries are keyed by plain strings and looking
    an energy up by its name is the natural way to do it. This enumeration documents the known
    names; as its members are plain strings, they can be used for the lookup as well, e.g.
    `output.get_energies()[EnergyType.MDCI_SD_T]`.

    The enumeration is not exhaustive: a calculation may well produce an energy type that is not
    listed here.
    """

    UNKNOWN = "Unknown"
    """No information about the energy is provided."""
    SCF = "SCF"
    """SCF energy from HF, DFT or SQM methods."""
    MP2 = "MP2"
    """MP2 energy."""
    MP2_OO = "MP2(OO)"
    """Orbital-optimised MP2 energy."""
    MDCI_SD = "MDCI(SD)"
    """Typically the (DLPNO-)CCSD energy."""
    MDCI_SD_T = "MDCI(SD(T))"
    """Typically the (DLPNO-)CCSD(T) energy."""
    CASSCF = "CASSCF"
    """CASSCF energy."""
    CASSCF_PT2 = "CASSCF IC-PT2: NEVPT2/CASPT2"
    """Internally contracted PT2 energy on top of a CASSCF reference."""
    AUTOCI = "AUTOCI"
    """Energy of an automatically generated CI calculation."""
    TDA_CIS = "TDA/CIS"
    """TDA-TD-DFT or CIS energy."""
    VDW = "VdW"
    """Dispersion correction, reported by `Output.get_final_energy_components()`, see also
    `Output.get_vdw_correction()`."""
    GCP = "gCP"
    """Geometrical counterpoise correction, reported by `Output.get_final_energy_components()`, see
    also `Output.get_gcp_correction()`."""
