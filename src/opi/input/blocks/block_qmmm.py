from typing import Literal

from pydantic import field_validator

from opi.input.blocks import Block, InputFilePath, IntGroup
from opi.input.simple_keywords import SimpleKeyword

__all__ = ("BlockQmmm",)


class BlockQmmm(Block):
    """Class to model %qmmm block in ORCA"""

    _name: str = "qmmm"
    nsubsystems: int | None = None
    systemtype: Literal["protein", "crystal"] | None = None
    hflayers: int | None = None
    ecplayers: int | None = None
    outerpclayers: int | None = None
    chargealteration: Literal["z0", "z1", "z2", "z3", "rcd", "cs"] | None = None
    coupling: Literal["additive", "subtractive"] | None = None
    embedding: Literal["electrostatic", "mechanical"] | None = None
    deleteladoublecounting: bool | None = None
    deletelabonddoublecounting: bool | None = None
    lagraddistribution: Literal["lever", "full"] | None = None
    dist_atomsaroundopt: float | None = None
    dist_atomsaroundunitcell: float | None = None
    qmcore_extension: float | None = None
    qmcore_type: Literal["atoms", "fragments"] | None = None
    activecore_extension: float | None = None
    activecore_type: Literal["atoms", "fragments"] | None = None
    scale_rcd: float | None = None
    scale_cs: float | None = None
    printlevel: int | None = None
    printoptregion: bool | None = None
    printoptregionext: bool | None = None
    printqmregion: bool | None = None
    printqm2region: bool | None = None
    printpdb: bool | None = None
    printfulltrj: bool | None = None
    use_active_infofrompdb: bool | None = None
    use_qm_infofrompdb: bool | None = None
    use_qm2_infofrompdb: bool | None = None
    use_qm3_infofrompdb: bool | None = None
    use_mm2_infofrompdb: bool | None = None
    dist_c_hla: float | None = None
    dist_o_hla: float | None = None
    dist_n_hla: float | None = None
    qmla_dist_scheme: Literal["standard"] | None = None
    h_dist_input: Literal["read", "qm2"] | None = None
    forcefieldinput: Literal["orca", "charmm", "amber"] | None = None
    do_nb_for_fixed_fixed: bool | None = None
    rigid_mm_water: bool | None = None
    extendactiveregion: Literal["cov_bonds", "distance"] | None = None
    conv_charges: bool | None = None
    conv_charges_maxncycles: int | None = None
    conv_charges_convthresh: float | None = None
    enforcetotalcharge: bool | None = None
    mult_total: int | None = None
    charge_total: float | None = None
    mult_medium: int | None = None
    charge_medium: float | None = None
    charge_hflayer: int | None = None
    scale_formalcharge_ecpatom: float | None = None
    scale_formalcharge_mmatom: float | None = None
    scale_qm2charges_mmatom: float | None = None
    autodetectqccharge: bool | None = None
    nunitcellatoms: int | None = None
    conv_charge_useqmcoreonly: bool | None = None
    mmgrad_prescreen: bool | None = None
    solv_scheme: Literal["cpcm_b", "cpcm_c"] | None = None
    oniom_boundary: Literal["bonded", "nonbonded"] | None = None
    autoff_qm2_optlarge: bool | None = None
    autoff_qm2_optsmall: bool | None = None
    autoff_qm2_method: (
        Literal[
            "xtb0",
            "xtb1",
            "xtb2",
            "gfnff",
            "hf3c",
            "pbeh3c",
            "r2scan3c",
            "pm3",
            "am1",
            "surff",
            "qm2",
        ]
        | None
    ) = None
    charge_method: Literal["hirshfeld", "mbis", "chelpg", "mulliken", "loewdin"] | None = None
    keep_qmmm_files: bool | None = None
    autofrag_useqm1region: bool | None = None
    dofmm: bool | None = None
    dovfmm: bool | None = None
    mam: int | None = None
    levels: int | None = None
    doboxdimopt: bool | None = None
    boxdiminp: float | None = None
    hflayergto: SimpleKeyword | None = None
    hflayerecp: SimpleKeyword | None = None
    ecplayerecp: SimpleKeyword | None = None
    qmatoms: IntGroup | None = None
    activeatoms: IntGroup | None = None
    optregion_fixedatoms: IntGroup | None = None
    qm2atoms: IntGroup | None = None
    hflayeratoms: IntGroup | None = None
    qm3atoms: IntGroup | None = None
    h_dist_filename: InputFilePath | None = None
    qmqm2_qmlink_offfilename: InputFilePath | None = None
    oniom3_qmqm2_offfilename: InputFilePath | None = None
    forcefieldfilename: InputFilePath | None = None
    fffilename: InputFilePath | None = None
    orcafffilename: InputFilePath | None = None
    gfnff_topo_qm1: InputFilePath | None = None
    gfnff_topo_qm2: InputFilePath | None = None
    gfnff_topo_qm3: InputFilePath | None = None
    atomtype_filename: InputFilePath | None = None
    qm2custommethod: SimpleKeyword | None = None
    qm2custombasis: SimpleKeyword | None = None
    qm2customfile: InputFilePath | None = None

    @field_validator(
        "qmatoms",
        "activeatoms",
        "optregion_fixedatoms",
        "qm2atoms",
        "hflayeratoms",
        "qm3atoms",
        mode="before",
    )
    @classmethod
    def intgroup_from_list(cls, inp: IntGroup | list[int]) -> IntGroup:
        """
        Parameters
        ----------
        inp : IntGroup | list[int]
        """
        if isinstance(inp, list):
            return IntGroup.init(inp)
        else:
            return inp

    @field_validator(
        "h_dist_filename",
        "qmqm2_qmlink_offfilename",
        "oniom3_qmqm2_offfilename",
        "forcefieldfilename",
        "fffilename",
        "orcafffilename",
        "gfnff_topo_qm1",
        "gfnff_topo_qm2",
        "gfnff_topo_qm3",
        "atomtype_filename",
        "qm2customfile",
        mode="before",
    )
    @classmethod
    def path_from_string(cls, path: str | InputFilePath) -> InputFilePath:
        """
        Parameters
        ----------
        path : str | InputFilePath
        """
        if isinstance(path, str):
            return InputFilePath.from_string(path)
        else:
            return path
