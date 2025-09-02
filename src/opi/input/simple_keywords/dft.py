from opi.input.simple_keywords.base import (
    SimpleKeyword,
    SimpleKeywordBox,
)

__all__ = ("Dft",)


class Dft(SimpleKeywordBox):
    """Enum to store all simple keywords of type Dft."""

    B3LYP3C = SimpleKeyword("b3lyp3c")
    """SimpleKeyword: DFT 3c methods, does not require dispersion correction or basis set separately."""
    B973C = SimpleKeyword("b973c")
    """SimpleKeyword: DFT 3c methods, does not require dispersion correction or basis set separately."""
    PBEH3C = SimpleKeyword("pbeh3c")
    """SimpleKeyword: DFT 3c methods, does not require dispersion correction or basis set separately."""
    WB97X3C = SimpleKeyword("wb97x3c")
    """SimpleKeyword: DFT 3c methods, does not require dispersion correction or basis set separately."""
    B3LYP_GCP_D3_6_31G_D = SimpleKeyword("b3lyp-gcp-d3/6-31g(d)")
    """SimpleKeyword: Dft."""
    B3LYP_GCP_D3_6_31GSTAR = SimpleKeyword("b3lyp-gcp-d3/6-31g*")
    """SimpleKeyword: DFT - similar to 3c methods, does not require dispersion correction or basis set separately."""
    FOD = SimpleKeyword("fod")
    """SimpleKeyword: DFT with smearing for determining multireference character (TPSS/def2-TZVP, T = 5000 K)."""
    B1LYP = SimpleKeyword("b1lyp")
    """SimpleKeyword: DFT functional."""
    B1P = SimpleKeyword("b1p")
    """SimpleKeyword: DFT functional."""
    B1P86 = SimpleKeyword("b1p86")
    """SimpleKeyword: DFT functional."""
    B1PBE = SimpleKeyword("b1pbe")
    """SimpleKeyword: DFT functional."""
    B1PW = SimpleKeyword("b1pw")
    """SimpleKeyword: DFT functional."""
    B1PW91 = SimpleKeyword("b1pw91")
    """SimpleKeyword: DFT functional."""
    B2GP_PLYP = SimpleKeyword("b2gp-plyp")
    """SimpleKeyword: DFT functional."""
    B2K_PLYP = SimpleKeyword("b2k-plyp")
    """SimpleKeyword: DFT functional."""
    B2PLYP = SimpleKeyword("b2plyp")
    """SimpleKeyword: DFT functional."""
    B2T_PLYP = SimpleKeyword("b2t-plyp")
    """SimpleKeyword: DFT functional."""
    B3LYP = SimpleKeyword("b3lyp")
    """SimpleKeyword: DFT functional."""
    B3LYP_G = SimpleKeyword("b3lyp_g")
    """SimpleKeyword: DFT functional."""
    B3P = SimpleKeyword("b3p")
    """SimpleKeyword: DFT functional."""
    B3P86 = SimpleKeyword("b3p86")
    """SimpleKeyword: DFT functional."""
    B3PBE = SimpleKeyword("b3pbe")
    """SimpleKeyword: DFT functional."""
    B3PW = SimpleKeyword("b3pw")
    """SimpleKeyword: DFT functional."""
    B3PW91 = SimpleKeyword("b3pw91")
    """SimpleKeyword: DFT functional."""
    B97 = SimpleKeyword("b97")
    """SimpleKeyword: DFT functional."""
    B97_D = SimpleKeyword("b97-d")
    """SimpleKeyword: DFT functional."""
    B97_D3 = SimpleKeyword("b97-d3")
    """SimpleKeyword: DFT functional."""
    B97_D4 = SimpleKeyword("b97-d4")
    """SimpleKeyword: DFT functional."""
    B97M_D3BJ = SimpleKeyword("b97m-d3bj")
    """SimpleKeyword: DFT functional."""
    B97M_D4 = SimpleKeyword("b97m-d4")
    """SimpleKeyword: DFT functional."""
    B97M_V = SimpleKeyword("b97m-v")
    """SimpleKeyword: DFT functional."""
    BHANDHLYP = SimpleKeyword("bhandhlyp")
    """SimpleKeyword: DFT functional."""
    BHLYP = SimpleKeyword("bhlyp")
    """SimpleKeyword: DFT functional."""
    BLYP = SimpleKeyword("blyp")
    """SimpleKeyword: DFT functional."""
    BNULL = SimpleKeyword("bnull")
    """SimpleKeyword: DFT functional."""
    BP86 = SimpleKeyword("bp86")
    """SimpleKeyword: DFT functional."""
    BPBE = SimpleKeyword("bpbe")
    """SimpleKeyword: DFT functional."""
    BPW = SimpleKeyword("bpw")
    """SimpleKeyword: DFT functional."""
    BPW91 = SimpleKeyword("bpw91")
    """SimpleKeyword: DFT functional."""
    BVWN = SimpleKeyword("bvwn")
    """SimpleKeyword: DFT functional."""
    CAM_B3LYP = SimpleKeyword("cam-b3lyp")
    """SimpleKeyword: DFT functional."""
    DLPNO_B2GP_PLYP = SimpleKeyword("dlpno-b2gp-plyp")
    """SimpleKeyword: Double-hybrid DFT with DLPNO approximation."""
    DLPNO_B2K_PLYP = SimpleKeyword("dlpno-b2k-plyp")
    """SimpleKeyword: Double-hybrid DFT with DLPNO approximation."""
    DLPNO_B2PLYP = SimpleKeyword("dlpno-b2plyp")
    """SimpleKeyword: Double-hybrid DFT with DLPNO approximation."""
    DLPNO_B2T_PLYP = SimpleKeyword("dlpno-b2t-plyp")
    """SimpleKeyword: Double-hybrid DFT with DLPNO approximation."""
    DLPNO_DSD_BLYP = SimpleKeyword("dlpno-dsd-blyp")
    """SimpleKeyword: Double-hybrid DFT with DLPNO approximation."""
    DLPNO_DSD_PBEB95 = SimpleKeyword("dlpno-dsd-pbeb95")
    """SimpleKeyword: Double-hybrid DFT with DLPNO approximation."""
    DLPNO_DSD_PBEP86 = SimpleKeyword("dlpno-dsd-pbep86")
    """SimpleKeyword: Double-hybrid DFT with DLPNO approximation."""
    DLPNO_KPR2SCAN50 = SimpleKeyword("dlpno-kpr2scan50")
    """SimpleKeyword: Double-hybrid DFT with DLPNO approximation."""
    DLPNO_MPW2PLYP = SimpleKeyword("dlpno-mpw2plyp")
    """SimpleKeyword: Double-hybrid DFT with DLPNO approximation."""
    DLPNO_PBE_QIDH = SimpleKeyword("dlpno-pbe-qidh")
    """SimpleKeyword: Double-hybrid DFT with DLPNO approximation."""
    DLPNO_PBE0_2 = SimpleKeyword("dlpno-pbe0-2")
    """SimpleKeyword: Double-hybrid DFT with DLPNO approximation."""
    DLPNO_PBE0_DH = SimpleKeyword("dlpno-pbe0-dh")
    """SimpleKeyword: Double-hybrid DFT with DLPNO approximation."""
    DLPNO_PR2SCAN50 = SimpleKeyword("dlpno-pr2scan50")
    """SimpleKeyword: Double-hybrid DFT with DLPNO approximation."""
    DLPNO_PR2SCAN69 = SimpleKeyword("dlpno-pr2scan69")
    """SimpleKeyword: Double-hybrid DFT with DLPNO approximation."""
    DLPNO_PWPB95 = SimpleKeyword("dlpno-pwpb95")
    """SimpleKeyword: Double-hybrid DFT with DLPNO approximation."""
    DLPNO_R2SCAN_CIDH = SimpleKeyword("dlpno-r2scan-cidh")
    """SimpleKeyword: Double-hybrid DFT with DLPNO approximation."""
    DLPNO_R2SCAN_QIDH = SimpleKeyword("dlpno-r2scan-qidh")
    """SimpleKeyword: Double-hybrid DFT with DLPNO approximation."""
    DLPNO_R2SCAN0_2 = SimpleKeyword("dlpno-r2scan0-2")
    """SimpleKeyword: Double-hybrid DFT with DLPNO approximation."""
    DLPNO_R2SCAN0_DH = SimpleKeyword("dlpno-r2scan0-dh")
    """SimpleKeyword: Double-hybrid DFT with DLPNO approximation."""
    DLPNO_RSX_0DH = SimpleKeyword("dlpno-rsx-0dh")
    """SimpleKeyword: Double-hybrid DFT with DLPNO approximation."""
    DLPNO_RSX_QIDH = SimpleKeyword("dlpno-rsx-qidh")
    """SimpleKeyword: Double-hybrid DFT with DLPNO approximation."""
    DLPNO_SCS_B2GP_PLYP21 = SimpleKeyword("dlpno-scs-b2gp-plyp21")
    """SimpleKeyword: Double-hybrid DFT with DLPNO approximation."""
    DLPNO_SCS_PBE_QIDH = SimpleKeyword("dlpno-scs-pbe-qidh")
    """SimpleKeyword: Double-hybrid DFT with DLPNO approximation."""
    DLPNO_SCS_RSX_QIDH = SimpleKeyword("dlpno-scs-rsx-qidh")
    """SimpleKeyword: Double-hybrid DFT with DLPNO approximation."""
    DLPNO_SCS_WB2GP_PLYP = SimpleKeyword("dlpno-scs-wb2gp-plyp")
    """SimpleKeyword: Double-hybrid DFT with DLPNO approximation."""
    DLPNO_SCS_WB88PP86 = SimpleKeyword("dlpno-scs-wb88pp86")
    """SimpleKeyword: Double-hybrid DFT with DLPNO approximation."""
    DLPNO_SCS_WPBEPP86 = SimpleKeyword("dlpno-scs-wpbepp86")
    """SimpleKeyword: Double-hybrid DFT with DLPNO approximation."""
    DLPNO_SCS_SOS_B2PLYP21 = SimpleKeyword("dlpno-scs/sos-b2plyp21")
    """SimpleKeyword: Double-hybrid DFT with DLPNO approximation."""
    DLPNO_SCS_SOS_WB2PLYP = SimpleKeyword("dlpno-scs/sos-wb2plyp")
    """SimpleKeyword: Double-hybrid DFT with DLPNO approximation."""
    DLPNO_SOS_B2GP_PLYP21 = SimpleKeyword("dlpno-sos-b2gp-plyp21")
    """SimpleKeyword: Double-hybrid DFT with DLPNO approximation."""
    DLPNO_SOS_PBE_QIDH = SimpleKeyword("dlpno-sos-pbe-qidh")
    """SimpleKeyword: Double-hybrid DFT with DLPNO approximation."""
    DLPNO_SOS_RSX_QIDH = SimpleKeyword("dlpno-sos-rsx-qidh")
    """SimpleKeyword: Double-hybrid DFT with DLPNO approximation."""
    DLPNO_SOS_WB2GP_PLYP = SimpleKeyword("dlpno-sos-wb2gp-plyp")
    """SimpleKeyword: Double-hybrid DFT with DLPNO approximation."""
    DLPNO_SOS_WB88PP86 = SimpleKeyword("dlpno-sos-wb88pp86")
    """SimpleKeyword: Double-hybrid DFT with DLPNO approximation."""
    DLPNO_SOS_WPBEPP86 = SimpleKeyword("dlpno-sos-wpbepp86")
    """SimpleKeyword: Double-hybrid DFT with DLPNO approximation."""
    DLPNO_WB2GP_PLYP = SimpleKeyword("dlpno-wb2gp-plyp")
    """SimpleKeyword: Double-hybrid DFT with DLPNO approximation."""
    DLPNO_WB2PLYP = SimpleKeyword("dlpno-wb2plyp")
    """SimpleKeyword: Double-hybrid DFT with DLPNO approximation."""
    DLPNO_WB88PP86 = SimpleKeyword("dlpno-wb88pp86")
    """SimpleKeyword: Double-hybrid DFT with DLPNO approximation."""
    DLPNO_WB97M_2 = SimpleKeyword("dlpno-wb97m(2)")
    """SimpleKeyword: Double-hybrid DFT with DLPNO approximation."""
    DLPNO_WB97X_2 = SimpleKeyword("dlpno-wb97x-2")
    """SimpleKeyword: Double-hybrid DFT with DLPNO approximation."""
    DLPNO_WB97X_2_TQZ = SimpleKeyword("dlpno-wb97x-2(tqz)")
    """SimpleKeyword: Double-hybrid DFT with DLPNO approximation."""
    DLPNO_WPBEPP86 = SimpleKeyword("dlpno-wpbepp86")
    """SimpleKeyword: Double-hybrid DFT with DLPNO approximation."""
    DLPNO_WPR2SCAN50 = SimpleKeyword("dlpno-wpr2scan50")
    """SimpleKeyword: Double-hybrid DFT with DLPNO approximation."""
    DSD_BLYP = SimpleKeyword("dsd-blyp")
    """SimpleKeyword: DFT functional."""
    DSD_PBEB95 = SimpleKeyword("dsd-pbeb95")
    """SimpleKeyword: DFT functional."""
    DSD_PBEP86 = SimpleKeyword("dsd-pbep86")
    """SimpleKeyword: DFT functional."""
    G1LYP = SimpleKeyword("g1lyp")
    """SimpleKeyword: DFT functional."""
    G1P = SimpleKeyword("g1p")
    """SimpleKeyword: DFT functional."""
    G3LYP = SimpleKeyword("g3lyp")
    """SimpleKeyword: DFT functional."""
    G3P = SimpleKeyword("g3p")
    """SimpleKeyword: DFT functional."""
    GLYP = SimpleKeyword("glyp")
    """SimpleKeyword: DFT functional."""
    GP = SimpleKeyword("gp")
    """SimpleKeyword: DFT functional."""
    HFLDA = SimpleKeyword("hflda")
    """SimpleKeyword: DFT functional."""
    HFS = SimpleKeyword("hfs")
    """SimpleKeyword: DFT functional."""
    KPR2SCAN50 = SimpleKeyword("kpr2scan50")
    """SimpleKeyword: DFT functional."""
    LB94 = SimpleKeyword("lb94")
    """SimpleKeyword: DFT functional."""
    LC_BLYP = SimpleKeyword("lc-blyp")
    """SimpleKeyword: DFT functional."""
    LC_PBE = SimpleKeyword("lc-pbe")
    """SimpleKeyword: DFT functional."""
    LDA = SimpleKeyword("lda")
    """SimpleKeyword: DFT functional."""
    LRC_PBE = SimpleKeyword("lrc-pbe")
    """SimpleKeyword: DFT functional."""
    LSD = SimpleKeyword("lsd")
    """SimpleKeyword: DFT functional."""
    M06 = SimpleKeyword("m06")
    """SimpleKeyword: DFT functional."""
    M062X = SimpleKeyword("m062x")
    """SimpleKeyword: DFT functional."""
    M06L = SimpleKeyword("m06l")
    """SimpleKeyword: DFT functional."""
    MPW1LYP = SimpleKeyword("mpw1lyp")
    """SimpleKeyword: DFT functional."""
    MPW1PW = SimpleKeyword("mpw1pw")
    """SimpleKeyword: DFT functional."""
    MPW2PLYP = SimpleKeyword("mpw2plyp")
    """SimpleKeyword: DFT functional."""
    MPWLYP = SimpleKeyword("mpwlyp")
    """SimpleKeyword: DFT functional."""
    MPWPW = SimpleKeyword("mpwpw")
    """SimpleKeyword: DFT functional."""
    O3LYP = SimpleKeyword("o3lyp")
    """SimpleKeyword: DFT functional."""
    OLYP = SimpleKeyword("olyp")
    """SimpleKeyword: DFT functional."""
    OPBE = SimpleKeyword("opbe")
    """SimpleKeyword: DFT functional."""
    PBE = SimpleKeyword("pbe")
    """SimpleKeyword: DFT functional."""
    PBE_QIDH = SimpleKeyword("pbe-qidh")
    """SimpleKeyword: DFT functional."""
    PBE0 = SimpleKeyword("pbe0")
    """SimpleKeyword: DFT functional."""
    PBE0_2 = SimpleKeyword("pbe0-2")
    """SimpleKeyword: DFT functional."""
    PBE0_DH = SimpleKeyword("pbe0-dh")
    """SimpleKeyword: DFT functional."""
    PR2SCAN50 = SimpleKeyword("pr2scan50")
    """SimpleKeyword: DFT functional."""
    PR2SCAN69 = SimpleKeyword("pr2scan69")
    """SimpleKeyword: DFT functional."""
    PW1PW = SimpleKeyword("pw1pw")
    """SimpleKeyword: DFT functional."""
    PW6B95 = SimpleKeyword("pw6b95")
    """SimpleKeyword: DFT functional."""
    PW86PBE = SimpleKeyword("pw86pbe")
    """SimpleKeyword: DFT functional."""
    PW91 = SimpleKeyword("pw91")
    """SimpleKeyword: DFT functional."""
    PW91_0 = SimpleKeyword("pw91_0")
    """SimpleKeyword: DFT functional."""
    PWLDA = SimpleKeyword("pwlda")
    """SimpleKeyword: DFT functional."""
    PWP = SimpleKeyword("pwp")
    """SimpleKeyword: DFT functional."""
    PWP1 = SimpleKeyword("pwp1")
    """SimpleKeyword: DFT functional."""
    PWPB95 = SimpleKeyword("pwpb95")
    """SimpleKeyword: DFT functional."""
    R2SCAN = SimpleKeyword("r2scan")
    """SimpleKeyword: DFT functional."""
    R2SCAN_3C = SimpleKeyword("r2scan-3c")
    """SimpleKeyword: DFT functional."""
    R2SCAN_CIDH = SimpleKeyword("r2scan-cidh")
    """SimpleKeyword: DFT functional."""
    R2SCAN_QIDH = SimpleKeyword("r2scan-qidh")
    """SimpleKeyword: DFT functional."""
    R2SCAN0 = SimpleKeyword("r2scan0")
    """SimpleKeyword: DFT functional."""
    R2SCAN0 = SimpleKeyword("r2scan0")
    """SimpleKeyword: DFT functional."""
    R2SCAN0_2 = SimpleKeyword("r2scan0-2")
    """SimpleKeyword: DFT functional."""
    R2SCAN0_DH = SimpleKeyword("r2scan0-dh")
    """SimpleKeyword: DFT functional."""
    R2SCAN50 = SimpleKeyword("r2scan50")
    """SimpleKeyword: DFT functional."""
    R2SCANH = SimpleKeyword("r2scanh")
    """SimpleKeyword: DFT functional."""
    REVDOD_PBEP86_D4_2021 = SimpleKeyword("revdod-pbep86-d4/2021")
    """SimpleKeyword: DFT functional."""
    REVDOD_PBEP86_2021 = SimpleKeyword("revdod-pbep86/2021")
    """SimpleKeyword: DFT functional."""
    REVDSD_PBEP86_D4_2021 = SimpleKeyword("revdsd-pbep86-d4/2021")
    """SimpleKeyword: DFT functional."""
    REVDSD_PBEP86_2021 = SimpleKeyword("revdsd-pbep86/2021")
    """SimpleKeyword: DFT functional."""
    REVPBE = SimpleKeyword("revpbe")
    """SimpleKeyword: DFT functional."""
    REVPBE0 = SimpleKeyword("revpbe0")
    """SimpleKeyword: DFT functional."""
    REVPBE38 = SimpleKeyword("revpbe38")
    """SimpleKeyword: DFT functional."""
    REVTPSS = SimpleKeyword("revtpss")
    """SimpleKeyword: DFT functional."""
    RPBE = SimpleKeyword("rpbe")
    """SimpleKeyword: DFT functional."""
    RPW86PBE = SimpleKeyword("rpw86pbe")
    """SimpleKeyword: DFT functional."""
    RSCAN = SimpleKeyword("rscan")
    """SimpleKeyword: DFT functional."""
    RSX_0DH = SimpleKeyword("rsx-0dh")
    """SimpleKeyword: DFT functional."""
    RSX_QIDH = SimpleKeyword("rsx-qidh")
    """SimpleKeyword: DFT functional."""
    SCANFUNC = SimpleKeyword("scanfunc")
    """SimpleKeyword: DFT functional."""
    SCS_B2GP_PLYP21 = SimpleKeyword("scs-b2gp-plyp21")
    """SimpleKeyword: DFT functional."""
    SCS_PBE_QIDH = SimpleKeyword("scs-pbe-qidh")
    """SimpleKeyword: DFT functional."""
    SCS_RSX_QIDH = SimpleKeyword("scs-rsx-qidh")
    """SimpleKeyword: DFT functional."""
    SCS_WB2GP_PLYP = SimpleKeyword("scs-wb2gp-plyp")
    """SimpleKeyword: DFT functional."""
    SCS_WB88PP86 = SimpleKeyword("scs-wb88pp86")
    """SimpleKeyword: DFT functional."""
    SCS_WPBEPP86 = SimpleKeyword("scs-wpbepp86")
    """SimpleKeyword: DFT functional."""
    SCS_SOS_B2PLYP21 = SimpleKeyword("scs/sos-b2plyp21")
    """SimpleKeyword: DFT functional."""
    SCS_SOS_WB2PLYP = SimpleKeyword("scs/sos-wb2plyp")
    """SimpleKeyword: DFT functional."""
    SOS_B2GP_PLYP21 = SimpleKeyword("sos-b2gp-plyp21")
    """SimpleKeyword: DFT functional."""
    SOS_PBE_QIDH = SimpleKeyword("sos-pbe-qidh")
    """SimpleKeyword: DFT functional."""
    SOS_RSX_QIDH = SimpleKeyword("sos-rsx-qidh")
    """SimpleKeyword: DFT functional."""
    SOS_WB2GP_PLYP = SimpleKeyword("sos-wb2gp-plyp")
    """SimpleKeyword: DFT functional."""
    SOS_WB88PP86 = SimpleKeyword("sos-wb88pp86")
    """SimpleKeyword: DFT functional."""
    SOS_WPBEPP86 = SimpleKeyword("sos-wpbepp86")
    """SimpleKeyword: DFT functional."""
    TPSS = SimpleKeyword("tpss")
    """SimpleKeyword: DFT functional."""
    TPSS0 = SimpleKeyword("tpss0")
    """SimpleKeyword: DFT functional."""
    TPSSH = SimpleKeyword("tpssh")
    """SimpleKeyword: DFT functional."""
    VWN = SimpleKeyword("vwn")
    """SimpleKeyword: DFT functional."""
    VWN3 = SimpleKeyword("vwn3")
    """SimpleKeyword: DFT functional."""
    VWN5 = SimpleKeyword("vwn5")
    """SimpleKeyword: DFT functional."""
    WB2GP_PLYP = SimpleKeyword("wb2gp-plyp")
    """SimpleKeyword: DFT functional."""
    WB2PLYP = SimpleKeyword("wb2plyp")
    """SimpleKeyword: DFT functional."""
    WB88PP86 = SimpleKeyword("wb88pp86")
    """SimpleKeyword: DFT functional."""
    WB97 = SimpleKeyword("wb97")
    """SimpleKeyword: DFT functional."""
    WB97M_D3BJ = SimpleKeyword("wb97m-d3bj")
    """SimpleKeyword: DFT functional."""
    WB97M_D4 = SimpleKeyword("wb97m-d4")
    """SimpleKeyword: DFT functional."""
    WB97M_D4REV = SimpleKeyword("wb97m-d4rev")
    """SimpleKeyword: DFT functional."""
    WB97M_V = SimpleKeyword("wb97m-v")
    """SimpleKeyword: DFT functional."""
    WB97M_2 = SimpleKeyword("wb97m(2)")
    """SimpleKeyword: DFT functional."""
    WB97X = SimpleKeyword("wb97x")
    """SimpleKeyword: DFT functional."""
    WB97X_2 = SimpleKeyword("wb97x-2")
    """SimpleKeyword: DFT functional."""
    WB97X_2_TQZ = SimpleKeyword("wb97x-2(tqz)")
    """SimpleKeyword: DFT functional."""
    WB97X_D3 = SimpleKeyword("wb97x-d3")
    """SimpleKeyword: DFT functional."""
    WB97X_D3BJ = SimpleKeyword("wb97x-d3bj")
    """SimpleKeyword: DFT functional."""
    WB97X_D4 = SimpleKeyword("wb97x-d4")
    """SimpleKeyword: DFT functional."""
    WB97X_D4REV = SimpleKeyword("wb97x-d4rev")
    """SimpleKeyword: DFT functional."""
    WB97X_V = SimpleKeyword("wb97x-v")
    """SimpleKeyword: DFT functional."""
    WPBEPP86 = SimpleKeyword("wpbepp86")
    """SimpleKeyword: DFT functional."""
    WPR2SCAN50 = SimpleKeyword("wpr2scan50")
    """SimpleKeyword: DFT functional."""
    WR2SCAN = SimpleKeyword("wr2scan")
    """SimpleKeyword: DFT functional."""
    X3LYP = SimpleKeyword("x3lyp")
    """SimpleKeyword: DFT functional."""
    XHF = SimpleKeyword("xhf")
    """SimpleKeyword: DFT functional."""
    XLYP = SimpleKeyword("xlyp")
    """SimpleKeyword: DFT functional."""
