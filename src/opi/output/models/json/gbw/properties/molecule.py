from pydantic import Field, StrictFloat, StrictInt, StrictStr

from opi.output.models.base.get_item import GetItem
from opi.output.models.json.gbw.properties.atoms import Atoms
from opi.output.models.json.gbw.properties.densities import Densities
from opi.output.models.json.gbw.properties.molecular_orbitals import (
    MolecularOrbitals,
)
from opi.output.models.json.gbw.properties.tddft import TdDft
from opi.output.models.json.gbw.properties.two_electron_integrals import TwoElectronIntegrals


class Molecule(GetItem):
    """
    This class contains the information about the Molecule

    Attributes
    ----------
    atoms: list[Atoms]
        Contains information about the Atoms
    basename: StrictStr
        The basename of the calculation
    molecularorbital: MolecularOrbital
        Contains information about the molecular orbitals
    multiplicity: StrictInt
        multiplicity of the molecule
    charge: StrictInt
        charge of the molecule
    hftyp: StrictStr
        Used shell-type (e.g., UHF/RHF) in the calculation
    origin: tuple[StrictFloat, StrictFloat, StrictFloat]
        Origin of the molecule
    s_matrix: list[list[StrictFloat]]
        Overlap matrix
    h_matrix: list[list[StrictFloat]]
        Hcore matrix (1-el integrals)
    t_matrix: list[list[StrictFloat]]
        Kinetic energy matrix (1-el integrals)
    v_matrix: list[list[StrictFloat]]
        Nuclear attraction matrix (1-el integrals)
    hmo: list[list[list[StrictFloat]]]
        Hcore matrix in MO basis (1-el integrals)
    f_matrix: f_matrix: list[list[list[StrictFloat]]]
        Fock matrix/matrices
    j_matrix: list[list[list[StrictFloat]]]
        Coulomb integrals (2-el integrals)
    k_matrix: list[list[list[StrictFloat]]]
        Exchange integrals (2-el integrals)
    twoelintegrals: TwoElectronIntegrals | None, default = None
        Contains the available two electron integrals
    pointgroup: StrictStr
        Pointgroup of the molecule
    td_dft: TdDft | None default = None
        Contains information about td-dft calculation
    densities: Densities | None, default = None
        Contains the available densities
    """

    atoms: list[Atoms] | None = None
    basename: StrictStr | None = None
    molecularorbitals: MolecularOrbitals | None = None
    coordinateunits: StrictStr | None = None
    multiplicity: StrictInt | None = None
    charge: StrictInt | None = None
    hftyp: StrictStr | None = None
    origin: tuple[StrictFloat, StrictFloat, StrictFloat]
    s_matrix: list[list[StrictFloat]] | None = Field(default=None, alias="s-matrix")
    h_matrix: list[list[StrictFloat]] | None = Field(default=None, alias="h-matrix")
    t_matrix: list[list[StrictFloat]] | None = Field(default=None, alias="t-matrix")
    v_matrix: list[list[StrictFloat]] | None = Field(default=None, alias="v-matrix")
    hmo: list[list[list[StrictFloat]]] | None = None
    f_matrix: list[list[list[StrictFloat]]] | None = Field(default=None, alias="f-matrix")
    j_matrix: list[list[list[StrictFloat]]] | None = Field(default=None, alias="j-matrix")
    k_matrix: list[list[list[StrictFloat]]] | None = Field(default=None, alias="k-matrix")
    twoelintegrals: TwoElectronIntegrals | None = Field(default=None, alias="2elintegrals")
    pointgroup: StrictStr | None = None
    td_dft: list[TdDft] | None = Field(None, alias="td-dft")
    densities: Densities | None = None

    class Configuration:
        allow_population_by_field_name = True
