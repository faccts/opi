from pathlib import Path
from opi.core import Calculator
import shutil
from opi.input.structures.structure import Structure
from opi.input.simple_keywords import (
    Wft,
    BasisSet,
    Dlpno,
    AuxBasisSet,
    RelativisticCorrection,
    ShellType,
    Scf,
)
from opi.input.blocks import BlockMdci, BlockMp2


def run_mp2_based_dlpnocc_extrapolation(structure: Structure, wd: Path = Path("RUN")):
    """
    Perform the MP2-based correction scheme to approach the limit of a complete pair natural orbitals space in
    DLPNO-CCSD(T) calculations according to J. Chem. Theory Comput. 2023, 19, 13, 4023–4032
    """

    # > HF and CC type
    HF_TYPE = ShellType.UHF
    CC_TYPE = Wft.DLPNO_CCSD_T1 # or Wft.DLPNO_CCSD_T

    # > Modify these by hand as desired
    BASIS_SET = BasisSet.AUG_CC_PVDZ_DK
    REL = RelativisticCorrection.DKH2
    AUX_BASIS = AuxBasisSet.AUTOAUX
    DLPNO_THRESH = Dlpno.TIGHTPNO  # or Dlpno.NORMALPNO

    # > MDCI block for DLPNO-CCSD(T) calculation
    cc_mdci_block = BlockMdci()
    cc_mdci_block.usefulllmp2guess = False
    cc_mdci_block.maxiter = 100

    # > MP2 block for DLPNO-MP2 calculation
    mp2_block = BlockMp2()

    # > Adjust DLPNO-MP2 settings to DLPNO-CCSD(T) settings
    # > Normal PNO settings
    if DLPNO_THRESH == Dlpno.NORMALPNO:
        mp2_block.tcutpno = 3.33 * 10e-7
        mp2_block.tcutdo = 1 * 10e-2
        mp2_block.tcutmkn = 1 * 10e-3
    # > Tight PNO Settings
    elif DLPNO_THRESH == Dlpno.TIGHTPNO:
        mp2_block.tcutpno = 1 * 10e-7
        mp2_block.tcutdo = 5 * 10e-3
        mp2_block.tcutmkn = 1 * 10e-3
    else:
        raise ValueError("Unkown DLPNO_THRESH")

    # > DLPNO-CCSD(T1)
    dlpno_cc_calc = Calculator(basename="dlpno_ccsdt", working_dir=wd)
    dlpno_cc_calc.structure = structure
    dlpno_cc_calc.input.add_simple_keywords(
        HF_TYPE, CC_TYPE, REL, BASIS_SET, AUX_BASIS, DLPNO_THRESH
    )
    dlpno_cc_calc.input.add_blocks(cc_mdci_block)

    # > Write and run the calculation
    status = dlpno_cc_calc.write_and_run()
    if not status:
        raise RuntimeError("DLPNO-CCSD(T) calculation did not terminate normally!")

    # > Get the output
    dlpno_cc_out = dlpno_cc_calc.get_output()
    dlpno_cc_out.parse()

    # > DLPNO-MP2 Calculation
    dlpno_mp2_calc = Calculator(basename="dlpno_mp2", working_dir=wd)
    dlpno_mp2_calc.structure = structure
    dlpno_mp2_calc.input.add_simple_keywords(
        HF_TYPE, Wft.DLPNO_MP2, REL, BASIS_SET, AUX_BASIS, Scf.MOREAD, Scf.NOITER
    )
    dlpno_mp2_calc.input.moinp = wd / "dlpno_ccsdt.gbw"
    dlpno_mp2_calc.input.add_blocks(mp2_block)

    # > Write and run the calculation
    status = dlpno_mp2_calc.write_and_run()
    if not status:
        raise RuntimeError("DLPNO-MP2 calculation did not terminate normally!")

    # > Get the output
    dlpno_mp2_out = dlpno_mp2_calc.get_output()
    dlpno_mp2_out.parse()

    # > RI-MP2 Calculation
    ri_mp2_calc = Calculator(basename="ri_mp2", working_dir=wd)
    ri_mp2_calc.structure = structure
    ri_mp2_calc.input.add_simple_keywords(
        HF_TYPE, Wft.RIMP2, REL, BASIS_SET, AUX_BASIS, Scf.MOREAD, Scf.NOITER
    )
    ri_mp2_calc.input.moinp = wd / "dlpno_ccsdt.gbw"

    # > Write and run the calculation
    ri_mp2_calc.write_and_run()
    if not status:
        raise RuntimeError("RI-MP2 calculation did not terminate normally!")

    # > Get the output
    ri_mp2_out = ri_mp2_calc.get_output()
    ri_mp2_out.parse()

    energy_dlpno_cc = dlpno_cc_out.get_final_energy()
    corr_energy_dlpno_mp2 = dlpno_mp2_out.get_energies()["MP2"].correnergy[0][0]
    corr_energy_ri_mp2 = ri_mp2_out.get_energies()["MP2"].correnergy[0][0]

    extrapolated_energy = energy_dlpno_cc + (corr_energy_ri_mp2 - corr_energy_dlpno_mp2)

    # > return final extrapolated energy
    return extrapolated_energy

if __name__ == "__main__":
    xyz_string = """3

    O         -3.56626        1.77639        0.00000
    H         -2.59626        1.77639        0.00000
    H         -3.88959        1.36040       -0.81444"""
    structure = Structure.from_xyz_block(xyz_string)
    wd = Path("RUN")
    shutil.rmtree(wd, ignore_errors=True)
    wd.mkdir()
    energy = run_mp2_based_dlpnocc_extrapolation(structure, wd)
    print(f"FINAL EXTRAPOLATED ENERGY: {energy}")
