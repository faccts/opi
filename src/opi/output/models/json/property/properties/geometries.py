from opi.output.models.base.get_item import GetItem
from opi.output.models.json.property.properties.bs import BrokenSym
from opi.output.models.json.property.properties.calc_info import CalcInfo
from opi.output.models.json.property.properties.chem_shift import (
    ChemicalShift,
)
from opi.output.models.json.property.properties.ci_psi import CiPsi
from opi.output.models.json.property.properties.dft_energy import DftEnergy
from opi.output.models.json.property.properties.dipole_moment import DipoleMoment
from opi.output.models.json.property.properties.efg_tensor import EfgTensor
from opi.output.models.json.property.properties.energy_extrap import (
    EnergyExtrapolation,
)
from opi.output.models.json.property.properties.energy_list import (
    EnergyList,
)
from opi.output.models.json.property.properties.geometry import Geometry
from opi.output.models.json.property.properties.gradient import NucGradient
from opi.output.models.json.property.properties.gtensor import Gtensor
from opi.output.models.json.property.properties.hess import Hessian
from opi.output.models.json.property.properties.hirshfeld_population_analysis import (
    HirshfeldPopulationAnalysis,
)
from opi.output.models.json.property.properties.led import Led
from opi.output.models.json.property.properties.mayer_population_analysis import (
    MayerPopulationAnalysis,
)
from opi.output.models.json.property.properties.mbis_population_analysis import (
    MbisPopulationAnalysis,
)
from opi.output.models.json.property.properties.mdci_adex import MdciAdex
from opi.output.models.json.property.properties.mdci_adld import MdciAdld
from opi.output.models.json.property.properties.nat_orbitals import (
    NaturalOrbitals,
)
from opi.output.models.json.property.properties.polarizability import (
    Polarizability,
)
from opi.output.models.json.property.properties.population_analysis import (
    ChelpgPopulationAnalysis,
    LoewdinPopulationAnalysis,
    MullikenPopulationAnalysis,
)
from opi.output.models.json.property.properties.quadrupole_moment import (
    QuadrupoleMoment,
)
from opi.output.models.json.property.properties.roci_en import RoCiEnergy
from opi.output.models.json.property.properties.single_point_data import (
    SinglePointData,
)
from opi.output.models.json.property.properties.solvation import (
    SolvDetails,
)
from opi.output.models.json.property.properties.spectrum import Spectrum
from opi.output.models.json.property.properties.spin_coupling import (
    SpinSpinCoupling,
)
from opi.output.models.json.property.properties.tensor import Tensor
from opi.output.models.json.property.properties.thermo import (
    ThermochemistryEnergy,
)
from opi.output.models.json.property.properties.van_der_waals_correction import (
    VdwCorrection,
)


class Geometries(GetItem):
    """
    Contains the geometry dependent calculated results in the ORCA job

    Attributes
    ----------
    geometry: Geometry | None, default = None
        Contains information about the molecule
    energy: EnergyList | None, default = None
        Contains information about the energies
    single_point_data: SinglePointData | None, default = None
        Contains information about the singlepoint
    mulliken_population_analysis: list[PopulationAnalysis] | None, default = None
        Contains information about the Mulliken Population analyse
    loewdin_population_analysis: list[PopulationAnalysis] | None, default = None
        Contains information about the Loewdin Population analyse
    chelpg_population_analysis: list[PopulationAnalysis] | None, default = None
        Contains the information about the charges from electrostatic potentials using a grid-based population analysis (CHELPG)
    hirshfeld_population_analysis: list[HirshfeldPopulationAnalysis] | None, default = None
        Contains information about the Hirshfeld population analyse
    mayer_population_analysis: list[MayerPopulationAnalysis] | None, default = None
        Contains information about the Mayer population analyse
    mbis_population_analysis: list[MbisPopAnalysis] | None, default = None
        Contains information about the MBIS population analysis
    calculation_info: CalcInfo | None, default = None
        Contains information of the Calculation
    dipole_moment: list[Dipole] | None, default = None
        Contains information about the dipole moment
    nuclear_gradient: list[NucGradient] | None, default = None
        Contains information about the nuclear gradients for geometry Optimization
    dft_energy: list[DftEnergy] | None, default = None
        Contains information about all energies calculated for DFT
    vdw_correction: VdwCorrection | None, default = None
        Contains information about the Van-der-Waals correction
    hessian: Hessian | None, default = None
        Contains information about the Hessian-matrix
    solvation_details: SolvDetails | None, default = None
        Contains information about the used solvent and the solvent model
    polarizability: list[Polarizability] | None, default = None
        Contains information about the polarizability of the molecule
    absorption_spectrum: list[Spectrum] | None, default = None
        Contains the information about the calculated UVVis spectra
    ecd_spectrum: list[Spectrum] | None, default = None
        Contains the information about the calculated ecd spectra
    a_tensor: list[Tensor] | None, default = None
        Contains all the A-Tensor of the EPR calculation
    efg_tensor: list[EfgTensor] | None, default = None
        Contains all the EFG-Tensor of the EPR calculation
    g_tensor: list[Gtensor] | None, default = None
        Contains all the G-Tensor of the EPR calculation
    spin_spin_coupling: SpinSpinCoupling | None, default = None
        Contains information about the Spin-SpinCoupling
    chemical_shift: list[ChemicalShift] | None, default = None
        Contains information about the chemical shift on SCF level
    natural_orbitals: NaturalOrbitals | None, default = None
        Contains information about the natural orbitals
    mdci_led: Led | None, default = None
        Contains information about the local energy decomposition (LED)
    mdci_adld: MdciAdld | None, default = None
        Contains information about the mdci atomic decomposition of London dispersion (ADLD)
    mdci_adex: MdciAdex | None, default = None
        Contains information about the atomic decomposition of exchange (ADEX)
    broken_symmetry: BrokenSym | None, default = None
        Contains information about the broken symmetry calculation
    quadrupole_moment: list[QuadrupleMoment] | None, default = None
        Contains the information about the SCF calculated quadruple moment
    cipsi_energies: list[CiPsi] | None, default = None
        Contains the information about the CIPSI calculation
    energy_extrapolation: EnergyExtrapolation | None, default = None
        Contains information about the energy extrapolation
    roci_energy: list[RoCiEnergy] | None, default = None
        Contains information about the ROCI energy
    thermochemistry_energies: list[ThermochemistryEnergy] | None = None
        Contains information about thermostatistical corrections
        and final free energies
    """

    geometry: Geometry | None = None
    energy: EnergyList | None = None
    single_point_data: SinglePointData | None = None
    mulliken_population_analysis: list[MullikenPopulationAnalysis] | None = None
    loewdin_population_analysis: list[LoewdinPopulationAnalysis] | None = None
    chelpg_population_analysis: list[ChelpgPopulationAnalysis] | None = None
    hirshfeld_population_analysis: list[HirshfeldPopulationAnalysis] | None = None
    mayer_population_analysis: list[MayerPopulationAnalysis] | None = None
    mbis_population_analysis: list[MbisPopulationAnalysis] | None = None
    calculation_info: CalcInfo | None = None
    dipole_moment: list[DipoleMoment] | None = None
    nuclear_gradient: list[NucGradient] | None = None
    dft_energy: DftEnergy | None = None
    vdw_correction: VdwCorrection | None = None
    hessian: Hessian | None = None
    solvation_details: SolvDetails | None = None
    polarizability: list[Polarizability] | None = None
    absorption_spectrum: list[Spectrum] | None = None
    ecd_spectrum: list[Spectrum] | None = None
    a_tensor: list[Tensor] | None = None
    efg_tensor: list[EfgTensor] | None = None
    g_tensor: list[Gtensor] | None = None
    spin_spin_coupling: list[SpinSpinCoupling] | None = None
    chemical_shift: list[ChemicalShift] | None = None
    natural_orbitals: NaturalOrbitals | None = None
    mdci_led: Led | None = None
    mdci_adld: MdciAdld | None = None
    mdci_adex: MdciAdex | None = None
    broken_symmetry: BrokenSym | None = None
    quadrupole_moment: list[QuadrupoleMoment] | None = None
    cipsi_energies: list[CiPsi] | None = None
    energy_extrapolation: EnergyExtrapolation | None = None
    roci_energy: list[RoCiEnergy] | None = None
    thermochemistry_energies: list[ThermochemistryEnergy] | None = None
