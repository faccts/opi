from opi.input.simple_keywords.base import (
    ORCAKeyword,
    SimpleKeywordBox,
)

__all__ = ("Qmmm",)


class Qmmm(SimpleKeywordBox):
    """Enum to store all simple keywords of type Qmmm."""

    FMM_QMMM = ORCAKeyword("fmm-qmmm")
    """ORCAKeyword: Use FFM approximation in QMMM."""
    IONIC_CRYSTAL_QMMM = ORCAKeyword("ionic-crystal-qmmm")
    """ORCAKeyword: Use QM/MM to simulate a condensed phase calculation."""
    MOL_CRYSTAL_QMMM = ORCAKeyword("mol-crystal-qmmm")
    """ORCAKeyword: Use QM/MM to simulate a condensed phase calculation."""
    MOLECULAR_CRYSTAL_QMMM = ORCAKeyword("molecular-crystal-qmmm")
    """ORCAKeyword: Use QM/MM to simulate a condensed phase calculation."""
    QM_AM1 = ORCAKeyword("qm/am1")
    """ORCAKeyword: Predefined QM/MM level of theory."""
    QM_AM1_MM = ORCAKeyword("qm/am1/mm")
    """ORCAKeyword: Predefined QM/MM level of theory."""
    QM_AM1_SURFF = ORCAKeyword("qm/am1/surff")
    """ORCAKeyword: Predefined QM/MM level of theory."""
    QM_GFN_FF = ORCAKeyword("qm/gfn-ff")
    """ORCAKeyword: Predefined QM/MM level of theory."""
    QM_GFN_FF_MM = ORCAKeyword("qm/gfn-ff/mm")
    """ORCAKeyword: Predefined QM/MM level of theory."""
    QM_HF_3C = ORCAKeyword("qm/hf-3c")
    """ORCAKeyword: Predefined QM/MM level of theory."""
    QM_HF_3C_MM = ORCAKeyword("qm/hf-3c/mm")
    """ORCAKeyword: Predefined QM/MM level of theory."""
    QM_HF_3C_SURFF = ORCAKeyword("qm/hf-3c/surff")
    """ORCAKeyword: Predefined QM/MM level of theory."""
    QM_PBEH_3C = ORCAKeyword("qm/pbeh-3c")
    """ORCAKeyword: Predefined QM/MM level of theory."""
    QM_PBEH_3C_MM = ORCAKeyword("qm/pbeh-3c/mm")
    """ORCAKeyword: Predefined QM/MM level of theory."""
    QM_PBEH_3C_SURFF = ORCAKeyword("qm/pbeh-3c/surff")
    """ORCAKeyword: Predefined QM/MM level of theory."""
    QM_PM3 = ORCAKeyword("qm/pm3")
    """ORCAKeyword: Predefined QM/MM level of theory."""
    QM_PM3_MM = ORCAKeyword("qm/pm3/mm")
    """ORCAKeyword: Predefined QM/MM level of theory."""
    QM_PM3_SURFF = ORCAKeyword("qm/pm3/surff")
    """ORCAKeyword: Predefined QM/MM level of theory."""
    QM_QM2 = ORCAKeyword("qm/qm2")
    """ORCAKeyword: Predefined QM/MM level of theory."""
    QM_QM2_MM = ORCAKeyword("qm/qm2/mm")
    """ORCAKeyword: Predefined QM/MM level of theory."""
    QM_QM2_SURFF = ORCAKeyword("qm/qm2/surff")
    """ORCAKeyword: Predefined QM/MM level of theory."""
    QM_R2SCAN_3C = ORCAKeyword("qm/r2scan-3c")
    """ORCAKeyword: Predefined QM/MM level of theory."""
    QM_R2SCAN_3C_MM = ORCAKeyword("qm/r2scan-3c/mm")
    """ORCAKeyword: Predefined QM/MM level of theory."""
    QM_R2SCAN_3C_SURFF = ORCAKeyword("qm/r2scan-3c/surff")
    """ORCAKeyword: Predefined QM/MM level of theory."""
    QM_R2SCAN3C = ORCAKeyword("qm/r2scan3c")
    """ORCAKeyword: Predefined QM/MM level of theory."""
    QM_R2SCAN3C_MM = ORCAKeyword("qm/r2scan3c/mm")
    """ORCAKeyword: Predefined QM/MM level of theory."""
    QM_R2SCAN3C_SURFF = ORCAKeyword("qm/r2scan3c/surff")
    """ORCAKeyword: Predefined QM/MM level of theory."""
    QM_SURFF = ORCAKeyword("qm/surff")
    """ORCAKeyword: Predefined QM/MM level of theory."""
    QM_SURFF_MM = ORCAKeyword("qm/surff/mm")
    """ORCAKeyword: Predefined QM/MM level of theory."""
    QM_XTB0 = ORCAKeyword("qm/xtb0")
    """ORCAKeyword: Predefined QM/MM level of theory."""
    QM_XTB0_MM = ORCAKeyword("qm/xtb0/mm")
    """ORCAKeyword: Predefined QM/MM level of theory."""
    QM_XTB1 = ORCAKeyword("qm/xtb1")
    """ORCAKeyword: Predefined QM/MM level of theory."""
    QM_XTB1_MM = ORCAKeyword("qm/xtb1/mm")
    """ORCAKeyword: Predefined QM/MM level of theory."""
    QM_XTB2 = ORCAKeyword("qm/xtb2")
    """ORCAKeyword: Predefined QM/MM level of theory."""
    QM_XTB2_GFN_FF = ORCAKeyword("qm/xtb2/gfn-ff")
    """ORCAKeyword: Predefined QM/MM level of theory."""
    QM_XTB2_MM = ORCAKeyword("qm/xtb2/mm")
    """ORCAKeyword: Predefined QM/MM level of theory."""
    QM_XTB2_SURFF = ORCAKeyword("qm/xtb2/surff")
    """ORCAKeyword: Predefined QM/MM level of theory."""
    QMMM = ORCAKeyword("qmmm")
    """ORCAKeyword: Use QMMM."""
    QMMMSETUP = ORCAKeyword("qmmmsetup")
    """ORCAKeyword: Use QMMM (only does the setup)."""
