from opi.input.simple_keywords.base import (
    ORCAKeyword,
    SimpleKeywordBox,
)

__all__ = ("Gcp",)


class Gcp(SimpleKeywordBox):
    """Enum to store all simple keywords of type Gcp."""

    GCP_DFT_631G_D = ORCAKeyword("gcp(dft/631g(d))")
    """ORCAKeyword: Correction for basis set errors (Method/basis set dependent)."""
    GCP_DFT_631GSTAR = ORCAKeyword("gcp(dft/631g*)")
    """ORCAKeyword: Correction for basis set errors (Method/basis set dependent)."""
    GCP_DFT_631GD = ORCAKeyword("gcp(dft/631gd)")
    """ORCAKeyword: Correction for basis set errors (Method/basis set dependent)."""
    GCP_DFT_LANL = ORCAKeyword("gcp(dft/lanl)")
    """ORCAKeyword: Correction for basis set errors (Method/basis set dependent)."""
    GCP_DFT_MINIS = ORCAKeyword("gcp(dft/minis)")
    """ORCAKeyword: Correction for basis set errors (Method/basis set dependent)."""
    GCP_DFT_SV_P = ORCAKeyword("gcp(dft/sv(p))")
    """ORCAKeyword: Correction for basis set errors (Method/basis set dependent)."""
    GCP_DFT_SV_P_H_C = ORCAKeyword("gcp(dft/sv(p/h,c))")
    """ORCAKeyword: Correction for basis set errors (Method/basis set dependent)."""
    GCP_DFT_SV = ORCAKeyword("gcp(dft/sv)")
    """ORCAKeyword: Correction for basis set errors (Method/basis set dependent)."""
    GCP_DFT_SVP = ORCAKeyword("gcp(dft/svp)")
    """ORCAKeyword: Correction for basis set errors (Method/basis set dependent)."""
    GCP_DFT_SVX = ORCAKeyword("gcp(dft/svx)")
    """ORCAKeyword: Correction for basis set errors (Method/basis set dependent)."""
    GCP_DFT_TZ = ORCAKeyword("gcp(dft/tz)")
    """ORCAKeyword: Correction for basis set errors (Method/basis set dependent)."""
    GCP_FILE = ORCAKeyword("gcp(file)")
    """ORCAKeyword: Correction for basis set errors (Method/basis set dependent)."""
    GCP_HF_631G_D = ORCAKeyword("gcp(hf/631g(d))")
    """ORCAKeyword: Correction for basis set errors (Method/basis set dependent)."""
    GCP_HF_631GSTAR = ORCAKeyword("gcp(hf/631g*)")
    """ORCAKeyword: Correction for basis set errors (Method/basis set dependent)."""
    GCP_HF_631GD = ORCAKeyword("gcp(hf/631gd)")
    """ORCAKeyword: Correction for basis set errors (Method/basis set dependent)."""
    GCP_HF_MINIS = ORCAKeyword("gcp(hf/minis)")
    """ORCAKeyword: Correction for basis set errors (Method/basis set dependent)."""
    GCP_HF_MINIX = ORCAKeyword("gcp(hf/minix)")
    """ORCAKeyword: Correction for basis set errors (Method/basis set dependent)."""
    GCP_HF_SV_P = ORCAKeyword("gcp(hf/sv(p))")
    """ORCAKeyword: Correction for basis set errors (Method/basis set dependent)."""
    GCP_HF_SV_P_H_C = ORCAKeyword("gcp(hf/sv(p/h,c))")
    """ORCAKeyword: Correction for basis set errors (Method/basis set dependent)."""
    GCP_HF_SV = ORCAKeyword("gcp(hf/sv)")
    """ORCAKeyword: Correction for basis set errors (Method/basis set dependent)."""
    GCP_HF_SVP = ORCAKeyword("gcp(hf/svp)")
    """ORCAKeyword: Correction for basis set errors (Method/basis set dependent)."""
    GCP_HF_SVX = ORCAKeyword("gcp(hf/svx)")
    """ORCAKeyword: Correction for basis set errors (Method/basis set dependent)."""
    GCP_HF_TZ = ORCAKeyword("gcp(hf/tz)")
    """ORCAKeyword: Correction for basis set errors (Method/basis set dependent)."""
