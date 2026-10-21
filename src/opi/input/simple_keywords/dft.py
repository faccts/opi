from opi.input.simple_keywords.base import (
    ORCAKeyword,
    SimpleKeywordBox,
)

__all__ = ("Dft",)


class Dft(SimpleKeywordBox):
    """Enum to store all simple keywords of type Dft."""

    B3LYP3C = ORCAKeyword("b3lyp3c")
    """ORCAKeyword: DFT 3c methods, does not require dispersion correction or basis set separately."""
    B973C = ORCAKeyword("b973c")
    """ORCAKeyword: DFT 3c methods, does not require dispersion correction or basis set separately."""
    PBEH3C = ORCAKeyword("pbeh3c")
    """ORCAKeyword: DFT 3c methods, does not require dispersion correction or basis set separately."""
    WB97X3C = ORCAKeyword("wb97x3c")
    """ORCAKeyword: DFT 3c methods, does not require dispersion correction or basis set separately."""
    B3LYP_GCP_D3_6_31G_D = ORCAKeyword("b3lyp-gcp-d3/6-31g(d)")
    """ORCAKeyword: Dft."""
    B3LYP_GCP_D3_6_31GSTAR = ORCAKeyword("b3lyp-gcp-d3/6-31g*")
    """ORCAKeyword: DFT - similar to 3c methods, does not require dispersion correction or basis set separately."""
    FOD = ORCAKeyword("fod")
    """ORCAKeyword: DFT with smearing for determining multireference character (TPSS/def2-TZVP, T = 5000 K)."""
    B1LYP = ORCAKeyword("b1lyp")
    """ORCAKeyword: DFT functional."""
    B1P = ORCAKeyword("b1p")
    """ORCAKeyword: DFT functional."""
    B1P86 = ORCAKeyword("b1p86")
    """ORCAKeyword: DFT functional."""
    B1PBE = ORCAKeyword("b1pbe")
    """ORCAKeyword: DFT functional."""
    B1PW = ORCAKeyword("b1pw")
    """ORCAKeyword: DFT functional."""
    B1PW91 = ORCAKeyword("b1pw91")
    """ORCAKeyword: DFT functional."""
    B2GP_PLYP = ORCAKeyword("b2gp-plyp")
    """ORCAKeyword: DFT functional."""
    B2K_PLYP = ORCAKeyword("b2k-plyp")
    """ORCAKeyword: DFT functional."""
    B2PLYP = ORCAKeyword("b2plyp")
    """ORCAKeyword: DFT functional."""
    B2T_PLYP = ORCAKeyword("b2t-plyp")
    """ORCAKeyword: DFT functional."""
    B3LYP = ORCAKeyword("b3lyp")
    """ORCAKeyword: DFT functional."""
    B3LYP_G = ORCAKeyword("b3lyp_g")
    """ORCAKeyword: DFT functional."""
    B3P = ORCAKeyword("b3p")
    """ORCAKeyword: DFT functional."""
    B3P86 = ORCAKeyword("b3p86")
    """ORCAKeyword: DFT functional."""
    B3PBE = ORCAKeyword("b3pbe")
    """ORCAKeyword: DFT functional."""
    B3PW = ORCAKeyword("b3pw")
    """ORCAKeyword: DFT functional."""
    B3PW91 = ORCAKeyword("b3pw91")
    """ORCAKeyword: DFT functional."""
    B97 = ORCAKeyword("b97")
    """ORCAKeyword: DFT functional."""
    B97_D = ORCAKeyword("b97-d")
    """ORCAKeyword: DFT functional."""
    B97_D3 = ORCAKeyword("b97-d3")
    """ORCAKeyword: DFT functional."""
    B97_D4 = ORCAKeyword("b97-d4")
    """ORCAKeyword: DFT functional."""
    B97M_D3BJ = ORCAKeyword("b97m-d3bj")
    """ORCAKeyword: DFT functional."""
    B97M_D4 = ORCAKeyword("b97m-d4")
    """ORCAKeyword: DFT functional."""
    B97M_V = ORCAKeyword("b97m-v")
    """ORCAKeyword: DFT functional."""
    BHANDHLYP = ORCAKeyword("bhandhlyp")
    """ORCAKeyword: DFT functional."""
    BHLYP = ORCAKeyword("bhlyp")
    """ORCAKeyword: DFT functional."""
    BLYP = ORCAKeyword("blyp")
    """ORCAKeyword: DFT functional."""
    BNULL = ORCAKeyword("bnull")
    """ORCAKeyword: DFT functional."""
    BP86 = ORCAKeyword("bp86")
    """ORCAKeyword: DFT functional."""
    BPBE = ORCAKeyword("bpbe")
    """ORCAKeyword: DFT functional."""
    BPW = ORCAKeyword("bpw")
    """ORCAKeyword: DFT functional."""
    BPW91 = ORCAKeyword("bpw91")
    """ORCAKeyword: DFT functional."""
    BVWN = ORCAKeyword("bvwn")
    """ORCAKeyword: DFT functional."""
    CAM_B3LYP = ORCAKeyword("cam-b3lyp")
    """ORCAKeyword: DFT functional."""
    DLPNO_B2GP_PLYP = ORCAKeyword("dlpno-b2gp-plyp")
    """ORCAKeyword: Double-hybrid DFT with DLPNO approximation."""
    DLPNO_B2K_PLYP = ORCAKeyword("dlpno-b2k-plyp")
    """ORCAKeyword: Double-hybrid DFT with DLPNO approximation."""
    DLPNO_B2PLYP = ORCAKeyword("dlpno-b2plyp")
    """ORCAKeyword: Double-hybrid DFT with DLPNO approximation."""
    DLPNO_B2T_PLYP = ORCAKeyword("dlpno-b2t-plyp")
    """ORCAKeyword: Double-hybrid DFT with DLPNO approximation."""
    DLPNO_DSD_BLYP = ORCAKeyword("dlpno-dsd-blyp")
    """ORCAKeyword: Double-hybrid DFT with DLPNO approximation."""
    DLPNO_DSD_PBEB95 = ORCAKeyword("dlpno-dsd-pbeb95")
    """ORCAKeyword: Double-hybrid DFT with DLPNO approximation."""
    DLPNO_DSD_PBEP86 = ORCAKeyword("dlpno-dsd-pbep86")
    """ORCAKeyword: Double-hybrid DFT with DLPNO approximation."""
    DLPNO_KPR2SCAN50 = ORCAKeyword("dlpno-kpr2scan50")
    """ORCAKeyword: Double-hybrid DFT with DLPNO approximation."""
    DLPNO_MPW2PLYP = ORCAKeyword("dlpno-mpw2plyp")
    """ORCAKeyword: Double-hybrid DFT with DLPNO approximation."""
    DLPNO_PBE_QIDH = ORCAKeyword("dlpno-pbe-qidh")
    """ORCAKeyword: Double-hybrid DFT with DLPNO approximation."""
    DLPNO_PBE0_2 = ORCAKeyword("dlpno-pbe0-2")
    """ORCAKeyword: Double-hybrid DFT with DLPNO approximation."""
    DLPNO_PBE0_DH = ORCAKeyword("dlpno-pbe0-dh")
    """ORCAKeyword: Double-hybrid DFT with DLPNO approximation."""
    DLPNO_PR2SCAN50 = ORCAKeyword("dlpno-pr2scan50")
    """ORCAKeyword: Double-hybrid DFT with DLPNO approximation."""
    DLPNO_PR2SCAN69 = ORCAKeyword("dlpno-pr2scan69")
    """ORCAKeyword: Double-hybrid DFT with DLPNO approximation."""
    DLPNO_PWPB95 = ORCAKeyword("dlpno-pwpb95")
    """ORCAKeyword: Double-hybrid DFT with DLPNO approximation."""
    DLPNO_R2SCAN_CIDH = ORCAKeyword("dlpno-r2scan-cidh")
    """ORCAKeyword: Double-hybrid DFT with DLPNO approximation."""
    DLPNO_R2SCAN_QIDH = ORCAKeyword("dlpno-r2scan-qidh")
    """ORCAKeyword: Double-hybrid DFT with DLPNO approximation."""
    DLPNO_R2SCAN0_2 = ORCAKeyword("dlpno-r2scan0-2")
    """ORCAKeyword: Double-hybrid DFT with DLPNO approximation."""
    DLPNO_R2SCAN0_DH = ORCAKeyword("dlpno-r2scan0-dh")
    """ORCAKeyword: Double-hybrid DFT with DLPNO approximation."""
    DLPNO_RSX_0DH = ORCAKeyword("dlpno-rsx-0dh")
    """ORCAKeyword: Double-hybrid DFT with DLPNO approximation."""
    DLPNO_RSX_QIDH = ORCAKeyword("dlpno-rsx-qidh")
    """ORCAKeyword: Double-hybrid DFT with DLPNO approximation."""
    DLPNO_SCS_B2GP_PLYP21 = ORCAKeyword("dlpno-scs-b2gp-plyp21")
    """ORCAKeyword: Double-hybrid DFT with DLPNO approximation."""
    DLPNO_SCS_PBE_QIDH = ORCAKeyword("dlpno-scs-pbe-qidh")
    """ORCAKeyword: Double-hybrid DFT with DLPNO approximation."""
    DLPNO_SCS_RSX_QIDH = ORCAKeyword("dlpno-scs-rsx-qidh")
    """ORCAKeyword: Double-hybrid DFT with DLPNO approximation."""
    DLPNO_SCS_WB2GP_PLYP = ORCAKeyword("dlpno-scs-wb2gp-plyp")
    """ORCAKeyword: Double-hybrid DFT with DLPNO approximation."""
    DLPNO_SCS_WB88PP86 = ORCAKeyword("dlpno-scs-wb88pp86")
    """ORCAKeyword: Double-hybrid DFT with DLPNO approximation."""
    DLPNO_SCS_WPBEPP86 = ORCAKeyword("dlpno-scs-wpbepp86")
    """ORCAKeyword: Double-hybrid DFT with DLPNO approximation."""
    DLPNO_SCS_SOS_B2PLYP21 = ORCAKeyword("dlpno-scs/sos-b2plyp21")
    """ORCAKeyword: Double-hybrid DFT with DLPNO approximation."""
    DLPNO_SCS_SOS_WB2PLYP = ORCAKeyword("dlpno-scs/sos-wb2plyp")
    """ORCAKeyword: Double-hybrid DFT with DLPNO approximation."""
    DLPNO_SOS_B2GP_PLYP21 = ORCAKeyword("dlpno-sos-b2gp-plyp21")
    """ORCAKeyword: Double-hybrid DFT with DLPNO approximation."""
    DLPNO_SOS_PBE_QIDH = ORCAKeyword("dlpno-sos-pbe-qidh")
    """ORCAKeyword: Double-hybrid DFT with DLPNO approximation."""
    DLPNO_SOS_RSX_QIDH = ORCAKeyword("dlpno-sos-rsx-qidh")
    """ORCAKeyword: Double-hybrid DFT with DLPNO approximation."""
    DLPNO_SOS_WB2GP_PLYP = ORCAKeyword("dlpno-sos-wb2gp-plyp")
    """ORCAKeyword: Double-hybrid DFT with DLPNO approximation."""
    DLPNO_SOS_WB88PP86 = ORCAKeyword("dlpno-sos-wb88pp86")
    """ORCAKeyword: Double-hybrid DFT with DLPNO approximation."""
    DLPNO_SOS_WPBEPP86 = ORCAKeyword("dlpno-sos-wpbepp86")
    """ORCAKeyword: Double-hybrid DFT with DLPNO approximation."""
    DLPNO_WB2GP_PLYP = ORCAKeyword("dlpno-wb2gp-plyp")
    """ORCAKeyword: Double-hybrid DFT with DLPNO approximation."""
    DLPNO_WB2PLYP = ORCAKeyword("dlpno-wb2plyp")
    """ORCAKeyword: Double-hybrid DFT with DLPNO approximation."""
    DLPNO_WB88PP86 = ORCAKeyword("dlpno-wb88pp86")
    """ORCAKeyword: Double-hybrid DFT with DLPNO approximation."""
    DLPNO_WB97M_2 = ORCAKeyword("dlpno-wb97m(2)")
    """ORCAKeyword: Double-hybrid DFT with DLPNO approximation."""
    DLPNO_WB97X_2 = ORCAKeyword("dlpno-wb97x-2")
    """ORCAKeyword: Double-hybrid DFT with DLPNO approximation."""
    DLPNO_WB97X_2_TQZ = ORCAKeyword("dlpno-wb97x-2(tqz)")
    """ORCAKeyword: Double-hybrid DFT with DLPNO approximation."""
    DLPNO_WPBEPP86 = ORCAKeyword("dlpno-wpbepp86")
    """ORCAKeyword: Double-hybrid DFT with DLPNO approximation."""
    DLPNO_WPR2SCAN50 = ORCAKeyword("dlpno-wpr2scan50")
    """ORCAKeyword: Double-hybrid DFT with DLPNO approximation."""
    DSD_BLYP = ORCAKeyword("dsd-blyp")
    """ORCAKeyword: DFT functional."""
    DSD_PBEB95 = ORCAKeyword("dsd-pbeb95")
    """ORCAKeyword: DFT functional."""
    DSD_PBEP86 = ORCAKeyword("dsd-pbep86")
    """ORCAKeyword: DFT functional."""
    G1LYP = ORCAKeyword("g1lyp")
    """ORCAKeyword: DFT functional."""
    G1P = ORCAKeyword("g1p")
    """ORCAKeyword: DFT functional."""
    G3LYP = ORCAKeyword("g3lyp")
    """ORCAKeyword: DFT functional."""
    G3P = ORCAKeyword("g3p")
    """ORCAKeyword: DFT functional."""
    GLYP = ORCAKeyword("glyp")
    """ORCAKeyword: DFT functional."""
    GP = ORCAKeyword("gp")
    """ORCAKeyword: DFT functional."""
    HFLDA = ORCAKeyword("hflda")
    """ORCAKeyword: DFT functional."""
    HFS = ORCAKeyword("hfs")
    """ORCAKeyword: DFT functional."""
    KPR2SCAN50 = ORCAKeyword("kpr2scan50")
    """ORCAKeyword: DFT functional."""
    LB94 = ORCAKeyword("lb94")
    """ORCAKeyword: DFT functional."""
    LC_BLYP = ORCAKeyword("lc-blyp")
    """ORCAKeyword: DFT functional."""
    LC_PBE = ORCAKeyword("lc-pbe")
    """ORCAKeyword: DFT functional."""
    LDA = ORCAKeyword("lda")
    """ORCAKeyword: DFT functional."""
    LRC_PBE = ORCAKeyword("lrc-pbe")
    """ORCAKeyword: DFT functional."""
    LSD = ORCAKeyword("lsd")
    """ORCAKeyword: DFT functional."""
    M06 = ORCAKeyword("m06")
    """ORCAKeyword: DFT functional."""
    M062X = ORCAKeyword("m062x")
    """ORCAKeyword: DFT functional."""
    M06L = ORCAKeyword("m06l")
    """ORCAKeyword: DFT functional."""
    MPW1LYP = ORCAKeyword("mpw1lyp")
    """ORCAKeyword: DFT functional."""
    MPW1PW = ORCAKeyword("mpw1pw")
    """ORCAKeyword: DFT functional."""
    MPW2PLYP = ORCAKeyword("mpw2plyp")
    """ORCAKeyword: DFT functional."""
    MPWLYP = ORCAKeyword("mpwlyp")
    """ORCAKeyword: DFT functional."""
    MPWPW = ORCAKeyword("mpwpw")
    """ORCAKeyword: DFT functional."""
    O3LYP = ORCAKeyword("o3lyp")
    """ORCAKeyword: DFT functional."""
    OLYP = ORCAKeyword("olyp")
    """ORCAKeyword: DFT functional."""
    OPBE = ORCAKeyword("opbe")
    """ORCAKeyword: DFT functional."""
    PBE = ORCAKeyword("pbe")
    """ORCAKeyword: DFT functional."""
    PBE_QIDH = ORCAKeyword("pbe-qidh")
    """ORCAKeyword: DFT functional."""
    PBE0 = ORCAKeyword("pbe0")
    """ORCAKeyword: DFT functional."""
    PBE0_2 = ORCAKeyword("pbe0-2")
    """ORCAKeyword: DFT functional."""
    PBE0_DH = ORCAKeyword("pbe0-dh")
    """ORCAKeyword: DFT functional."""
    PR2SCAN50 = ORCAKeyword("pr2scan50")
    """ORCAKeyword: DFT functional."""
    PR2SCAN69 = ORCAKeyword("pr2scan69")
    """ORCAKeyword: DFT functional."""
    PW1PW = ORCAKeyword("pw1pw")
    """ORCAKeyword: DFT functional."""
    PW6B95 = ORCAKeyword("pw6b95")
    """ORCAKeyword: DFT functional."""
    PW86PBE = ORCAKeyword("pw86pbe")
    """ORCAKeyword: DFT functional."""
    PW91 = ORCAKeyword("pw91")
    """ORCAKeyword: DFT functional."""
    PW91_0 = ORCAKeyword("pw91_0")
    """ORCAKeyword: DFT functional."""
    PWLDA = ORCAKeyword("pwlda")
    """ORCAKeyword: DFT functional."""
    PWP = ORCAKeyword("pwp")
    """ORCAKeyword: DFT functional."""
    PWP1 = ORCAKeyword("pwp1")
    """ORCAKeyword: DFT functional."""
    PWPB95 = ORCAKeyword("pwpb95")
    """ORCAKeyword: DFT functional."""
    R2SCAN = ORCAKeyword("r2scan")
    """ORCAKeyword: DFT functional."""
    R2SCAN_3C = ORCAKeyword("r2scan-3c")
    """ORCAKeyword: DFT functional."""
    R2SCAN_CIDH = ORCAKeyword("r2scan-cidh")
    """ORCAKeyword: DFT functional."""
    R2SCAN_QIDH = ORCAKeyword("r2scan-qidh")
    """ORCAKeyword: DFT functional."""
    R2SCAN0 = ORCAKeyword("r2scan0")
    """ORCAKeyword: DFT functional."""
    R2SCAN0_2 = ORCAKeyword("r2scan0-2")
    """ORCAKeyword: DFT functional."""
    R2SCAN0_DH = ORCAKeyword("r2scan0-dh")
    """ORCAKeyword: DFT functional."""
    R2SCAN50 = ORCAKeyword("r2scan50")
    """ORCAKeyword: DFT functional."""
    R2SCANH = ORCAKeyword("r2scanh")
    """ORCAKeyword: DFT functional."""
    REVDOD_PBEP86_D4_2021 = ORCAKeyword("revdod-pbep86-d4/2021")
    """ORCAKeyword: DFT functional."""
    REVDOD_PBEP86_2021 = ORCAKeyword("revdod-pbep86/2021")
    """ORCAKeyword: DFT functional."""
    REVDSD_PBEP86_D4_2021 = ORCAKeyword("revdsd-pbep86-d4/2021")
    """ORCAKeyword: DFT functional."""
    REVDSD_PBEP86_2021 = ORCAKeyword("revdsd-pbep86/2021")
    """ORCAKeyword: DFT functional."""
    REVPBE = ORCAKeyword("revpbe")
    """ORCAKeyword: DFT functional."""
    REVPBE0 = ORCAKeyword("revpbe0")
    """ORCAKeyword: DFT functional."""
    REVPBE38 = ORCAKeyword("revpbe38")
    """ORCAKeyword: DFT functional."""
    REVTPSS = ORCAKeyword("revtpss")
    """ORCAKeyword: DFT functional."""
    RPBE = ORCAKeyword("rpbe")
    """ORCAKeyword: DFT functional."""
    RPW86PBE = ORCAKeyword("rpw86pbe")
    """ORCAKeyword: DFT functional."""
    RSCAN = ORCAKeyword("rscan")
    """ORCAKeyword: DFT functional."""
    RSX_0DH = ORCAKeyword("rsx-0dh")
    """ORCAKeyword: DFT functional."""
    RSX_QIDH = ORCAKeyword("rsx-qidh")
    """ORCAKeyword: DFT functional."""
    SCANFUNC = ORCAKeyword("scanfunc")
    """ORCAKeyword: DFT functional."""
    SCS_B2GP_PLYP21 = ORCAKeyword("scs-b2gp-plyp21")
    """ORCAKeyword: DFT functional."""
    SCS_PBE_QIDH = ORCAKeyword("scs-pbe-qidh")
    """ORCAKeyword: DFT functional."""
    SCS_RSX_QIDH = ORCAKeyword("scs-rsx-qidh")
    """ORCAKeyword: DFT functional."""
    SCS_WB2GP_PLYP = ORCAKeyword("scs-wb2gp-plyp")
    """ORCAKeyword: DFT functional."""
    SCS_WB88PP86 = ORCAKeyword("scs-wb88pp86")
    """ORCAKeyword: DFT functional."""
    SCS_WPBEPP86 = ORCAKeyword("scs-wpbepp86")
    """ORCAKeyword: DFT functional."""
    SCS_SOS_B2PLYP21 = ORCAKeyword("scs/sos-b2plyp21")
    """ORCAKeyword: DFT functional."""
    SCS_SOS_WB2PLYP = ORCAKeyword("scs/sos-wb2plyp")
    """ORCAKeyword: DFT functional."""
    SOS_B2GP_PLYP21 = ORCAKeyword("sos-b2gp-plyp21")
    """ORCAKeyword: DFT functional."""
    SOS_PBE_QIDH = ORCAKeyword("sos-pbe-qidh")
    """ORCAKeyword: DFT functional."""
    SOS_RSX_QIDH = ORCAKeyword("sos-rsx-qidh")
    """ORCAKeyword: DFT functional."""
    SOS_WB2GP_PLYP = ORCAKeyword("sos-wb2gp-plyp")
    """ORCAKeyword: DFT functional."""
    SOS_WB88PP86 = ORCAKeyword("sos-wb88pp86")
    """ORCAKeyword: DFT functional."""
    SOS_WPBEPP86 = ORCAKeyword("sos-wpbepp86")
    """ORCAKeyword: DFT functional."""
    TPSS = ORCAKeyword("tpss")
    """ORCAKeyword: DFT functional."""
    TPSS0 = ORCAKeyword("tpss0")
    """ORCAKeyword: DFT functional."""
    TPSSH = ORCAKeyword("tpssh")
    """ORCAKeyword: DFT functional."""
    VWN = ORCAKeyword("vwn")
    """ORCAKeyword: DFT functional."""
    VWN3 = ORCAKeyword("vwn3")
    """ORCAKeyword: DFT functional."""
    VWN5 = ORCAKeyword("vwn5")
    """ORCAKeyword: DFT functional."""
    WB2GP_PLYP = ORCAKeyword("wb2gp-plyp")
    """ORCAKeyword: DFT functional."""
    WB2PLYP = ORCAKeyword("wb2plyp")
    """ORCAKeyword: DFT functional."""
    WB88PP86 = ORCAKeyword("wb88pp86")
    """ORCAKeyword: DFT functional."""
    WB97 = ORCAKeyword("wb97")
    """ORCAKeyword: DFT functional."""
    WB97M_D3BJ = ORCAKeyword("wb97m-d3bj")
    """ORCAKeyword: DFT functional."""
    WB97M_D4 = ORCAKeyword("wb97m-d4")
    """ORCAKeyword: DFT functional."""
    WB97M_D4REV = ORCAKeyword("wb97m-d4rev")
    """ORCAKeyword: DFT functional."""
    WB97M_V = ORCAKeyword("wb97m-v")
    """ORCAKeyword: DFT functional."""
    WB97M_2 = ORCAKeyword("wb97m(2)")
    """ORCAKeyword: DFT functional."""
    WB97X = ORCAKeyword("wb97x")
    """ORCAKeyword: DFT functional."""
    WB97X_2 = ORCAKeyword("wb97x-2")
    """ORCAKeyword: DFT functional."""
    WB97X_2_TQZ = ORCAKeyword("wb97x-2(tqz)")
    """ORCAKeyword: DFT functional."""
    WB97X_D3 = ORCAKeyword("wb97x-d3")
    """ORCAKeyword: DFT functional."""
    WB97X_D3BJ = ORCAKeyword("wb97x-d3bj")
    """ORCAKeyword: DFT functional."""
    WB97X_D4 = ORCAKeyword("wb97x-d4")
    """ORCAKeyword: DFT functional."""
    WB97X_D4REV = ORCAKeyword("wb97x-d4rev")
    """ORCAKeyword: DFT functional."""
    WB97X_V = ORCAKeyword("wb97x-v")
    """ORCAKeyword: DFT functional."""
    WPBEPP86 = ORCAKeyword("wpbepp86")
    """ORCAKeyword: DFT functional."""
    WPR2SCAN50 = ORCAKeyword("wpr2scan50")
    """ORCAKeyword: DFT functional."""
    WR2SCAN = ORCAKeyword("wr2scan")
    """ORCAKeyword: DFT functional."""
    X3LYP = ORCAKeyword("x3lyp")
    """ORCAKeyword: DFT functional."""
    XHF = ORCAKeyword("xhf")
    """ORCAKeyword: DFT functional."""
    XLYP = ORCAKeyword("xlyp")
    """ORCAKeyword: DFT functional."""
