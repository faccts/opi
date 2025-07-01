from opi.input.simple_keywords.base import (
    SimpleKeyword,
    SimpleKeywordBox,
)

__all__ = ("Gcp",)


class Gcp(SimpleKeywordBox):
    """Enum to store all simple keywords of type Gcp.

    Attributes
    ----------
    GCP_DFT_631G_D : SimpleKeyword
        Correction for basis set errors (Method/basis set dependent)
    GCP_DFT_631GSTAR : SimpleKeyword
        Correction for basis set errors (Method/basis set dependent)
    GCP_DFT_631GD : SimpleKeyword
        Correction for basis set errors (Method/basis set dependent)
    GCP_DFT_LANL : SimpleKeyword
        Correction for basis set errors (Method/basis set dependent)
    GCP_DFT_MINIS : SimpleKeyword
        Correction for basis set errors (Method/basis set dependent)
    GCP_DFT_SV_P : SimpleKeyword
        Correction for basis set errors (Method/basis set dependent)
    GCP_DFT_SV_P_H_C : SimpleKeyword
        Correction for basis set errors (Method/basis set dependent)
    GCP_DFT_SV : SimpleKeyword
        Correction for basis set errors (Method/basis set dependent)
    GCP_DFT_SVP : SimpleKeyword
        Correction for basis set errors (Method/basis set dependent)
    GCP_DFT_SVX : SimpleKeyword
        Correction for basis set errors (Method/basis set dependent)
    GCP_DFT_TZ : SimpleKeyword
        Correction for basis set errors (Method/basis set dependent)
    GCP_FILE : SimpleKeyword
        Correction for basis set errors (Method/basis set dependent)
    GCP_HF_631G_D : SimpleKeyword
        Correction for basis set errors (Method/basis set dependent)
    GCP_HF_631GSTAR : SimpleKeyword
        Correction for basis set errors (Method/basis set dependent)
    GCP_HF_631GD : SimpleKeyword
        Correction for basis set errors (Method/basis set dependent)
    GCP_HF_MINIS : SimpleKeyword
        Correction for basis set errors (Method/basis set dependent)
    GCP_HF_MINIX : SimpleKeyword
        Correction for basis set errors (Method/basis set dependent)
    GCP_HF_SV_P : SimpleKeyword
        Correction for basis set errors (Method/basis set dependent)
    GCP_HF_SV_P_H_C : SimpleKeyword
        Correction for basis set errors (Method/basis set dependent)
    GCP_HF_SV : SimpleKeyword
        Correction for basis set errors (Method/basis set dependent)
    GCP_HF_SVP : SimpleKeyword
        Correction for basis set errors (Method/basis set dependent)
    GCP_HF_SVX : SimpleKeyword
        Correction for basis set errors (Method/basis set dependent)
    GCP_HF_TZ : SimpleKeyword
        Correction for basis set errors (Method/basis set dependent)
    """

    GCP_DFT_631G_D = SimpleKeyword(
        "gcp(dft/631g(d))"
    )
    GCP_DFT_631GSTAR = SimpleKeyword(
        "gcp(dft/631g*)"
    )
    GCP_DFT_631GD = SimpleKeyword(
        "gcp(dft/631gd)"
    )
    GCP_DFT_LANL = SimpleKeyword(
        "gcp(dft/lanl)"
    )
    GCP_DFT_MINIS = SimpleKeyword(
        "gcp(dft/minis)"
    )
    GCP_DFT_SV_P = SimpleKeyword(
        "gcp(dft/sv(p))"
    )
    GCP_DFT_SV_P_H_C = SimpleKeyword(
        "gcp(dft/sv(p/h,c))"
    )
    GCP_DFT_SV = SimpleKeyword(
        "gcp(dft/sv)"
    )
    GCP_DFT_SVP = SimpleKeyword(
        "gcp(dft/svp)"
    )
    GCP_DFT_SVX = SimpleKeyword(
        "gcp(dft/svx)"
    )
    GCP_DFT_TZ = SimpleKeyword(
        "gcp(dft/tz)"
    )
    GCP_FILE = SimpleKeyword(
        "gcp(file)"
    )
    GCP_HF_631G_D = SimpleKeyword(
        "gcp(hf/631g(d))"
    )
    GCP_HF_631GSTAR = SimpleKeyword(
        "gcp(hf/631g*)"
    )
    GCP_HF_631GD = SimpleKeyword(
        "gcp(hf/631gd)"
    )
    GCP_HF_MINIS = SimpleKeyword(
        "gcp(hf/minis)"
    )
    GCP_HF_MINIX = SimpleKeyword(
        "gcp(hf/minix)"
    )
    GCP_HF_SV_P = SimpleKeyword(
        "gcp(hf/sv(p))"
    )
    GCP_HF_SV_P_H_C = SimpleKeyword(
        "gcp(hf/sv(p/h,c))"
    )
    GCP_HF_SV = SimpleKeyword(
        "gcp(hf/sv)"
    )
    GCP_HF_SVP = SimpleKeyword(
        "gcp(hf/svp)"
    )
    GCP_HF_SVX = SimpleKeyword(
        "gcp(hf/svx)"
    )
    GCP_HF_TZ = SimpleKeyword(
        "gcp(hf/tz)"
    )
