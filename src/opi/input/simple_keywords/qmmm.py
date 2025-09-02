from opi.input.simple_keywords.base import (
    SimpleKeyword,
    SimpleKeywordBox,
)

__all__ = ("Qmmm",)


class Qmmm(SimpleKeywordBox):
    """Enum to store all simple keywords of type Qmmm."""

    FMM_QMMM = SimpleKeyword("fmm-qmmm")
    """SimpleKeyword: Use FFM approximation in QMMM."""
    IONIC_CRYSTAL_QMMM = SimpleKeyword("ionic-crystal-qmmm")
    """SimpleKeyword: Use QM/MM to simulate a condensed phase calculation."""
    MOL_CRYSTAL_QMMM = SimpleKeyword("mol-crystal-qmmm")
    """SimpleKeyword: Use QM/MM to simulate a condensed phase calculation."""
    MOLECULAR_CRYSTAL_QMMM = SimpleKeyword("molecular-crystal-qmmm")
    """SimpleKeyword: Use QM/MM to simulate a condensed phase calculation."""
    QM_AM1 = SimpleKeyword("qm/am1")
    """SimpleKeyword: Predefined QM/MM level of theory."""
    QM_AM1_MM = SimpleKeyword("qm/am1/mm")
    """SimpleKeyword: Predefined QM/MM level of theory."""
    QM_AM1_SURFF = SimpleKeyword("qm/am1/surff")
    """SimpleKeyword: Predefined QM/MM level of theory."""
    QM_GFN_FF = SimpleKeyword("qm/gfn-ff")
    """SimpleKeyword: Predefined QM/MM level of theory."""
    QM_GFN_FF_MM = SimpleKeyword("qm/gfn-ff/mm")
    """SimpleKeyword: Predefined QM/MM level of theory."""
    QM_HF_3C = SimpleKeyword("qm/hf-3c")
    """SimpleKeyword: Predefined QM/MM level of theory."""
    QM_HF_3C_MM = SimpleKeyword("qm/hf-3c/mm")
    """SimpleKeyword: Predefined QM/MM level of theory."""
    QM_HF_3C_SURFF = SimpleKeyword("qm/hf-3c/surff")
    """SimpleKeyword: Predefined QM/MM level of theory."""
    QM_PBEH_3C = SimpleKeyword("qm/pbeh-3c")
    """SimpleKeyword: Predefined QM/MM level of theory."""
    QM_PBEH_3C_MM = SimpleKeyword("qm/pbeh-3c/mm")
    """SimpleKeyword: Predefined QM/MM level of theory."""
    QM_PBEH_3C_SURFF = SimpleKeyword("qm/pbeh-3c/surff")
    """SimpleKeyword: Predefined QM/MM level of theory."""
    QM_PM3 = SimpleKeyword("qm/pm3")
    """SimpleKeyword: Predefined QM/MM level of theory."""
    QM_PM3_MM = SimpleKeyword("qm/pm3/mm")
    """SimpleKeyword: Predefined QM/MM level of theory."""
    QM_PM3_SURFF = SimpleKeyword("qm/pm3/surff")
    """SimpleKeyword: Predefined QM/MM level of theory."""
    QM_QM2 = SimpleKeyword("qm/qm2")
    """SimpleKeyword: Predefined QM/MM level of theory."""
    QM_QM2_MM = SimpleKeyword("qm/qm2/mm")
    """SimpleKeyword: Predefined QM/MM level of theory."""
    QM_QM2_SURFF = SimpleKeyword("qm/qm2/surff")
    """SimpleKeyword: Predefined QM/MM level of theory."""
    QM_R2SCAN_3C = SimpleKeyword("qm/r2scan-3c")
    """SimpleKeyword: Predefined QM/MM level of theory."""
    QM_R2SCAN_3C_MM = SimpleKeyword("qm/r2scan-3c/mm")
    """SimpleKeyword: Predefined QM/MM level of theory."""
    QM_R2SCAN_3C_SURFF = SimpleKeyword("qm/r2scan-3c/surff")
    """SimpleKeyword: Predefined QM/MM level of theory."""
    QM_R2SCAN3C = SimpleKeyword("qm/r2scan3c")
    """SimpleKeyword: Predefined QM/MM level of theory."""
    QM_R2SCAN3C_MM = SimpleKeyword("qm/r2scan3c/mm")
    """SimpleKeyword: Predefined QM/MM level of theory."""
    QM_R2SCAN3C_SURFF = SimpleKeyword("qm/r2scan3c/surff")
    """SimpleKeyword: Predefined QM/MM level of theory."""
    QM_SURFF = SimpleKeyword("qm/surff")
    """SimpleKeyword: Predefined QM/MM level of theory."""
    QM_SURFF_MM = SimpleKeyword("qm/surff/mm")
    """SimpleKeyword: Predefined QM/MM level of theory."""
    QM_XTB0 = SimpleKeyword("qm/xtb0")
    """SimpleKeyword: Predefined QM/MM level of theory."""
    QM_XTB0_MM = SimpleKeyword("qm/xtb0/mm")
    """SimpleKeyword: Predefined QM/MM level of theory."""
    QM_XTB1 = SimpleKeyword("qm/xtb1")
    """SimpleKeyword: Predefined QM/MM level of theory."""
    QM_XTB1_MM = SimpleKeyword("qm/xtb1/mm")
    """SimpleKeyword: Predefined QM/MM level of theory."""
    QM_XTB2 = SimpleKeyword("qm/xtb2")
    """SimpleKeyword: Predefined QM/MM level of theory."""
    QM_XTB2_GFN_FF = SimpleKeyword("qm/xtb2/gfn-ff")
    """SimpleKeyword: Predefined QM/MM level of theory."""
    QM_XTB2_MM = SimpleKeyword("qm/xtb2/mm")
    """SimpleKeyword: Predefined QM/MM level of theory."""
    QM_XTB2_SURFF = SimpleKeyword("qm/xtb2/surff")
    """SimpleKeyword: Predefined QM/MM level of theory."""
    QMMM = SimpleKeyword("qmmm")
    """SimpleKeyword: Use QMMM."""
    QMMMSETUP = SimpleKeyword("qmmmsetup")
    """SimpleKeyword: Use QMMM (only does the setup)."""
