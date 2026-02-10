from enum import StrEnum


class OrcaBinary(StrEnum):
    """
    List of relevant ORCA binaries.
    """

    ORCA = "orca"
    ORCA_2JSON = "orca_2json"
    ORCA_2AIM = "orca_2aim"
    ORCA_2MKL = "orca_2mkl"
    ORCA_CRYSTALPREP = "orca_crystalprep"
    ORCA_LFT = "orca_lft"
    ORCA_LOC = "orca_loc"
    ORCA_MAPSPC = "orca_mapspc"
    ORCA_MERGEFRAG = "orca_mergefrag"
    ORCA_PLOT = "orca_plot"
    ORCA_PLTVIB = "orca_pltvib"
    ORCA_VIB = "orca_vib"
