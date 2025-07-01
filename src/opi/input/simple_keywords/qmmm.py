from opi.input.simple_keywords.base import (
    SimpleKeyword,
    SimpleKeywordBox,
)

__all__ = ("Qmmm",)


class Qmmm(SimpleKeywordBox):
    """Enum to store all simple keywords of type Qmmm.

    Attributes
    ----------
    FMM_QMMM : SimpleKeyword
        Use FFM approximation in QMMM
    IONIC_CRYSTAL_QMMM : SimpleKeyword
        Use QM/MM to simulate a condensed phase calculation
    MOL_CRYSTAL_QMMM : SimpleKeyword
        Use QM/MM to simulate a condensed phase calculation
    MOLECULAR_CRYSTAL_QMMM : SimpleKeyword
        Use QM/MM to simulate a condensed phase calculation
    QM_AM1 : SimpleKeyword
        Predefined QM/MM level of theory
    QM_AM1_MM : SimpleKeyword
        Predefined QM/MM level of theory
    QM_AM1_SURFF : SimpleKeyword
        Predefined QM/MM level of theory
    QM_GFN_FF : SimpleKeyword
        Predefined QM/MM level of theory
    QM_GFN_FF_MM : SimpleKeyword
        Predefined QM/MM level of theory
    QM_HF_3C : SimpleKeyword
        Predefined QM/MM level of theory
    QM_HF_3C_MM : SimpleKeyword
        Predefined QM/MM level of theory
    QM_HF_3C_SURFF : SimpleKeyword
        Predefined QM/MM level of theory
    QM_PBEH_3C : SimpleKeyword
        Predefined QM/MM level of theory
    QM_PBEH_3C_MM : SimpleKeyword
        Predefined QM/MM level of theory
    QM_PBEH_3C_SURFF : SimpleKeyword
        Predefined QM/MM level of theory
    QM_PM3 : SimpleKeyword
        Predefined QM/MM level of theory
    QM_PM3_MM : SimpleKeyword
        Predefined QM/MM level of theory
    QM_PM3_SURFF : SimpleKeyword
        Predefined QM/MM level of theory
    QM_QM2 : SimpleKeyword
        Predefined QM/MM level of theory
    QM_QM2_MM : SimpleKeyword
        Predefined QM/MM level of theory
    QM_QM2_SURFF : SimpleKeyword
        Predefined QM/MM level of theory
    QM_R2SCAN_3C : SimpleKeyword
        Predefined QM/MM level of theory
    QM_R2SCAN_3C_MM : SimpleKeyword
        Predefined QM/MM level of theory
    QM_R2SCAN_3C_SURFF : SimpleKeyword
        Predefined QM/MM level of theory
    QM_R2SCAN3C : SimpleKeyword
        Predefined QM/MM level of theory
    QM_R2SCAN3C_MM : SimpleKeyword
        Predefined QM/MM level of theory
    QM_R2SCAN3C_SURFF : SimpleKeyword
        Predefined QM/MM level of theory
    QM_SURFF : SimpleKeyword
        Predefined QM/MM level of theory
    QM_SURFF_MM : SimpleKeyword
        Predefined QM/MM level of theory
    QM_XTB0 : SimpleKeyword
        Predefined QM/MM level of theory
    QM_XTB0_MM : SimpleKeyword
        Predefined QM/MM level of theory
    QM_XTB1 : SimpleKeyword
        Predefined QM/MM level of theory
    QM_XTB1_MM : SimpleKeyword
        Predefined QM/MM level of theory
    QM_XTB2 : SimpleKeyword
        Predefined QM/MM level of theory
    QM_XTB2_GFN_FF : SimpleKeyword
        Predefined QM/MM level of theory
    QM_XTB2_MM : SimpleKeyword
        Predefined QM/MM level of theory
    QM_XTB2_SURFF : SimpleKeyword
        Predefined QM/MM level of theory
    QMMM : SimpleKeyword
        Use QMMM
    QMMMSETUP : SimpleKeyword
        Use QMMM (only does the setup)
    """

    FMM_QMMM = SimpleKeyword("fmm-qmmm")
    IONIC_CRYSTAL_QMMM = SimpleKeyword("ionic-crystal-qmmm")
    MOL_CRYSTAL_QMMM = SimpleKeyword("mol-crystal-qmmm")
    MOLECULAR_CRYSTAL_QMMM = SimpleKeyword("molecular-crystal-qmmm")
    QM_AM1 = SimpleKeyword("qm/am1")
    QM_AM1_MM = SimpleKeyword("qm/am1/mm")
    QM_AM1_SURFF = SimpleKeyword("qm/am1/surff")
    QM_GFN_FF = SimpleKeyword("qm/gfn-ff")
    QM_GFN_FF_MM = SimpleKeyword("qm/gfn-ff/mm")
    QM_HF_3C = SimpleKeyword("qm/hf-3c")
    QM_HF_3C_MM = SimpleKeyword("qm/hf-3c/mm")
    QM_HF_3C_SURFF = SimpleKeyword("qm/hf-3c/surff")
    QM_PBEH_3C = SimpleKeyword("qm/pbeh-3c")
    QM_PBEH_3C_MM = SimpleKeyword("qm/pbeh-3c/mm")
    QM_PBEH_3C_SURFF = SimpleKeyword("qm/pbeh-3c/surff")
    QM_PM3 = SimpleKeyword("qm/pm3")
    QM_PM3_MM = SimpleKeyword("qm/pm3/mm")
    QM_PM3_SURFF = SimpleKeyword("qm/pm3/surff")
    QM_QM2 = SimpleKeyword("qm/qm2")
    QM_QM2_MM = SimpleKeyword("qm/qm2/mm")
    QM_QM2_SURFF = SimpleKeyword("qm/qm2/surff")
    QM_R2SCAN_3C = SimpleKeyword("qm/r2scan-3c")
    QM_R2SCAN_3C_MM = SimpleKeyword("qm/r2scan-3c/mm")
    QM_R2SCAN_3C_SURFF = SimpleKeyword("qm/r2scan-3c/surff")
    QM_R2SCAN3C = SimpleKeyword("qm/r2scan3c")
    QM_R2SCAN3C_MM = SimpleKeyword("qm/r2scan3c/mm")
    QM_R2SCAN3C_SURFF = SimpleKeyword("qm/r2scan3c/surff")
    QM_SURFF = SimpleKeyword("qm/surff")
    QM_SURFF_MM = SimpleKeyword("qm/surff/mm")
    QM_XTB0 = SimpleKeyword("qm/xtb0")
    QM_XTB0_MM = SimpleKeyword("qm/xtb0/mm")
    QM_XTB1 = SimpleKeyword("qm/xtb1")
    QM_XTB1_MM = SimpleKeyword("qm/xtb1/mm")
    QM_XTB2 = SimpleKeyword("qm/xtb2")
    QM_XTB2_GFN_FF = SimpleKeyword("qm/xtb2/gfn-ff")
    QM_XTB2_MM = SimpleKeyword("qm/xtb2/mm")
    QM_XTB2_SURFF = SimpleKeyword("qm/xtb2/surff")
    QMMM = SimpleKeyword("qmmm")
    QMMMSETUP = SimpleKeyword("qmmmsetup")
