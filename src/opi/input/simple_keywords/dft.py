from opi.input.simple_keywords.base import (
    SimpleKeyword,
    SimpleKeywordBox,
)

__all__ = ("Dft",)


class Dft(SimpleKeywordBox):
    """Enum to store all simple keywords of type Dft.

    Attributes
    ----------
    B3LYP3C : SimpleKeyword
        DFT 3c methods, do not require dispersion correction or basis set
    B973C : SimpleKeyword
        DFT 3c methods, do not require dispersion correction or basis set
    PBEH3C : SimpleKeyword
        DFT 3c methods, do not require dispersion correction or basis set
    WB97X3C : SimpleKeyword
        DFT 3c methods, do not require dispersion correction or basis set
    B3LYP_GCP_D3_6_31G_D : SimpleKeyword
        Dft
    B3LYP_GCP_D3_6_31GSTAR : SimpleKeyword
        DFT like 3c methods, do not require dispersion correction or basis set
    FOD : SimpleKeyword
        DFT with smearing for determining multireference character (TPSS/def2-TZVP, T = 5000 K)
    B1LYP : SimpleKeyword
        DFT functional
    B1P : SimpleKeyword
        DFT functional
    B1P86 : SimpleKeyword
        DFT functional
    B1PBE : SimpleKeyword
        DFT functional
    B1PW : SimpleKeyword
        DFT functional
    B1PW91 : SimpleKeyword
        DFT functional
    B2GP_PLYP : SimpleKeyword
        DFT functional
    B2K_PLYP : SimpleKeyword
        DFT functional
    B2PLYP : SimpleKeyword
        DFT functional
    B2T_PLYP : SimpleKeyword
        DFT functional
    B3LYP : SimpleKeyword
        DFT functional
    B3LYP_G : SimpleKeyword
        DFT functional
    B3P : SimpleKeyword
        DFT functional
    B3P86 : SimpleKeyword
        DFT functional
    B3PBE : SimpleKeyword
        DFT functional
    B3PW : SimpleKeyword
        DFT functional
    B3PW91 : SimpleKeyword
        DFT functional
    B97 : SimpleKeyword
        DFT functional
    B97_D : SimpleKeyword
        DFT functional
    B97_D3 : SimpleKeyword
        DFT functional
    B97_D4 : SimpleKeyword
        DFT functional
    B97M_D3BJ : SimpleKeyword
        DFT functional
    B97M_D4 : SimpleKeyword
        DFT functional
    B97M_V : SimpleKeyword
        DFT functional
    BHANDHLYP : SimpleKeyword
        DFT functional
    BHLYP : SimpleKeyword
        DFT functional
    BLYP : SimpleKeyword
        DFT functional
    BNULL : SimpleKeyword
        DFT functional
    BP86 : SimpleKeyword
        DFT functional
    BPBE : SimpleKeyword
        DFT functional
    BPW : SimpleKeyword
        DFT functional
    BPW91 : SimpleKeyword
        DFT functional
    BVWN : SimpleKeyword
        DFT functional
    CAM_B3LYP : SimpleKeyword
        DFT functional
    DLPNO_B2GP_PLYP : SimpleKeyword
        Double-hybrid DFT with DLPNO approximation
    DLPNO_B2K_PLYP : SimpleKeyword
        Double-hybrid DFT with DLPNO approximation
    DLPNO_B2PLYP : SimpleKeyword
        Double-hybrid DFT with DLPNO approximation
    DLPNO_B2T_PLYP : SimpleKeyword
        Double-hybrid DFT with DLPNO approximation
    DLPNO_DSD_BLYP : SimpleKeyword
        Double-hybrid DFT with DLPNO approximation
    DLPNO_DSD_PBEB95 : SimpleKeyword
        Double-hybrid DFT with DLPNO approximation
    DLPNO_DSD_PBEP86 : SimpleKeyword
        Double-hybrid DFT with DLPNO approximation
    DLPNO_KPR2SCAN50 : SimpleKeyword
        Double-hybrid DFT with DLPNO approximation
    DLPNO_MPW2PLYP : SimpleKeyword
        Double-hybrid DFT with DLPNO approximation
    DLPNO_PBE_QIDH : SimpleKeyword
        Double-hybrid DFT with DLPNO approximation
    DLPNO_PBE0_2 : SimpleKeyword
        Double-hybrid DFT with DLPNO approximation
    DLPNO_PBE0_DH : SimpleKeyword
        Double-hybrid DFT with DLPNO approximation
    DLPNO_PR2SCAN50 : SimpleKeyword
        Double-hybrid DFT with DLPNO approximation
    DLPNO_PR2SCAN69 : SimpleKeyword
        Double-hybrid DFT with DLPNO approximation
    DLPNO_PWPB95 : SimpleKeyword
        Double-hybrid DFT with DLPNO approximation
    DLPNO_R2SCAN_CIDH : SimpleKeyword
        Double-hybrid DFT with DLPNO approximation
    DLPNO_R2SCAN_QIDH : SimpleKeyword
        Double-hybrid DFT with DLPNO approximation
    DLPNO_R2SCAN0_2 : SimpleKeyword
        Double-hybrid DFT with DLPNO approximation
    DLPNO_R2SCAN0_DH : SimpleKeyword
        Double-hybrid DFT with DLPNO approximation
    DLPNO_RSX_0DH : SimpleKeyword
        Double-hybrid DFT with DLPNO approximation
    DLPNO_RSX_QIDH : SimpleKeyword
        Double-hybrid DFT with DLPNO approximation
    DLPNO_SCS_B2GP_PLYP21 : SimpleKeyword
        Double-hybrid DFT with DLPNO approximation
    DLPNO_SCS_PBE_QIDH : SimpleKeyword
        Double-hybrid DFT with DLPNO approximation
    DLPNO_SCS_RSX_QIDH : SimpleKeyword
        Double-hybrid DFT with DLPNO approximation
    DLPNO_SCS_WB2GP_PLYP : SimpleKeyword
        Double-hybrid DFT with DLPNO approximation
    DLPNO_SCS_WB88PP86 : SimpleKeyword
        Double-hybrid DFT with DLPNO approximation
    DLPNO_SCS_WPBEPP86 : SimpleKeyword
        Double-hybrid DFT with DLPNO approximation
    DLPNO_SCS_SOS_B2PLYP21 : SimpleKeyword
        Double-hybrid DFT with DLPNO approximation
    DLPNO_SCS_SOS_WB2PLYP : SimpleKeyword
        Double-hybrid DFT with DLPNO approximation
    DLPNO_SOS_B2GP_PLYP21 : SimpleKeyword
        Double-hybrid DFT with DLPNO approximation
    DLPNO_SOS_PBE_QIDH : SimpleKeyword
        Double-hybrid DFT with DLPNO approximation
    DLPNO_SOS_RSX_QIDH : SimpleKeyword
        Double-hybrid DFT with DLPNO approximation
    DLPNO_SOS_WB2GP_PLYP : SimpleKeyword
        Double-hybrid DFT with DLPNO approximation
    DLPNO_SOS_WB88PP86 : SimpleKeyword
        Double-hybrid DFT with DLPNO approximation
    DLPNO_SOS_WPBEPP86 : SimpleKeyword
        Double-hybrid DFT with DLPNO approximation
    DLPNO_WB2GP_PLYP : SimpleKeyword
        Double-hybrid DFT with DLPNO approximation
    DLPNO_WB2PLYP : SimpleKeyword
        Double-hybrid DFT with DLPNO approximation
    DLPNO_WB88PP86 : SimpleKeyword
        Double-hybrid DFT with DLPNO approximation
    DLPNO_WB97M_2 : SimpleKeyword
        Double-hybrid DFT with DLPNO approximation
    DLPNO_WB97X_2 : SimpleKeyword
        Double-hybrid DFT with DLPNO approximation
    DLPNO_WB97X_2_TQZ : SimpleKeyword
        Dft
    DLPNO_WPBEPP86 : SimpleKeyword
        Double-hybrid DFT with DLPNO approximation
    DLPNO_WPR2SCAN50 : SimpleKeyword
        Double-hybrid DFT with DLPNO approximation
    DSD_BLYP : SimpleKeyword
        DFT functional
    DSD_PBEB95 : SimpleKeyword
        DFT functional
    DSD_PBEP86 : SimpleKeyword
        DFT functional
    G1LYP : SimpleKeyword
        DFT functional
    G1P : SimpleKeyword
        DFT functional
    G3LYP : SimpleKeyword
        DFT functional
    G3P : SimpleKeyword
        DFT functional
    GLYP : SimpleKeyword
        DFT functional
    GP : SimpleKeyword
        DFT functional
    HFLDA : SimpleKeyword
        DFT functional
    HFS : SimpleKeyword
        DFT functional
    KPR2SCAN50 : SimpleKeyword
        DFT functional
    LB94 : SimpleKeyword
        DFT functional
    LC_BLYP : SimpleKeyword
        DFT functional
    LC_PBE : SimpleKeyword
        DFT functional
    LDA : SimpleKeyword
        DFT functional
    LRC_PBE : SimpleKeyword
        DFT functional
    LSD : SimpleKeyword
        DFT functional
    M06 : SimpleKeyword
        DFT functional
    M062X : SimpleKeyword
        DFT functional
    M06L : SimpleKeyword
        DFT functional
    MPW1LYP : SimpleKeyword
        DFT functional
    MPW1PW : SimpleKeyword
        DFT functional
    MPW2PLYP : SimpleKeyword
        DFT functional
    MPWLYP : SimpleKeyword
        DFT functional
    MPWPW : SimpleKeyword
        DFT functional
    O3LYP : SimpleKeyword
        DFT functional
    OLYP : SimpleKeyword
        DFT functional
    OPBE : SimpleKeyword
        DFT functional
    PBE : SimpleKeyword
        DFT functional
    PBE_QIDH : SimpleKeyword
        DFT functional
    PBE0 : SimpleKeyword
        DFT functional
    PBE0_2 : SimpleKeyword
        DFT functional
    PBE0_DH : SimpleKeyword
        DFT functional
    PR2SCAN50 : SimpleKeyword
        DFT functional
    PR2SCAN69 : SimpleKeyword
        DFT functional
    PW1PW : SimpleKeyword
        DFT functional
    PW6B95 : SimpleKeyword
        DFT functional
    PW86PBE : SimpleKeyword
        DFT functional
    PW91 : SimpleKeyword
        DFT functional
    PW91_0 : SimpleKeyword
        DFT functional
    PWLDA : SimpleKeyword
        DFT functional
    PWP : SimpleKeyword
        DFT functional
    PWP1 : SimpleKeyword
        DFT functional
    PWPB95 : SimpleKeyword
        DFT functional
    R2SCAN : SimpleKeyword
        DFT functional
    R2SCAN_3C : SimpleKeyword
        DFT functional
    R2SCAN_CIDH : SimpleKeyword
        DFT functional
    R2SCAN_QIDH : SimpleKeyword
        DFT functional
    R2SCAN0 : SimpleKeyword
        DFT functional
    R2SCAN0 : SimpleKeyword
        DFT functional
    R2SCAN0_2 : SimpleKeyword
        DFT functional
    R2SCAN0_DH : SimpleKeyword
        DFT functional
    R2SCAN50 : SimpleKeyword
        DFT functional
    R2SCANH : SimpleKeyword
        DFT functional
    REVDOD_PBEP86_D4_2021 : SimpleKeyword
        DFT functional
    REVDOD_PBEP86_2021 : SimpleKeyword
        DFT functional
    REVDSD_PBEP86_D4_2021 : SimpleKeyword
        DFT functional
    REVDSD_PBEP86_2021 : SimpleKeyword
        DFT functional
    REVPBE : SimpleKeyword
        DFT functional
    REVPBE0 : SimpleKeyword
        DFT functional
    REVPBE38 : SimpleKeyword
        DFT functional
    REVTPSS : SimpleKeyword
        DFT functional
    RPBE : SimpleKeyword
        DFT functional
    RPW86PBE : SimpleKeyword
        DFT functional
    RSCAN : SimpleKeyword
        DFT functional
    RSX_0DH : SimpleKeyword
        DFT functional
    RSX_QIDH : SimpleKeyword
        DFT functional
    SCANFUNC : SimpleKeyword
        DFT functional
    SCS_B2GP_PLYP21 : SimpleKeyword
        DFT functional
    SCS_PBE_QIDH : SimpleKeyword
        DFT functional
    SCS_RSX_QIDH : SimpleKeyword
        DFT functional
    SCS_WB2GP_PLYP : SimpleKeyword
        DFT functional
    SCS_WB88PP86 : SimpleKeyword
        DFT functional
    SCS_WPBEPP86 : SimpleKeyword
        DFT functional
    SCS_SOS_B2PLYP21 : SimpleKeyword
        DFT functional
    SCS_SOS_WB2PLYP : SimpleKeyword
        DFT functional
    SOS_B2GP_PLYP21 : SimpleKeyword
        DFT functional
    SOS_PBE_QIDH : SimpleKeyword
        DFT functional
    SOS_RSX_QIDH : SimpleKeyword
        DFT functional
    SOS_WB2GP_PLYP : SimpleKeyword
        DFT functional
    SOS_WB88PP86 : SimpleKeyword
        DFT functional
    SOS_WPBEPP86 : SimpleKeyword
        DFT functional
    TPSS : SimpleKeyword
        DFT functional
    TPSS0 : SimpleKeyword
        DFT functional
    TPSSH : SimpleKeyword
        DFT functional
    VWN : SimpleKeyword
        DFT functional
    VWN3 : SimpleKeyword
        DFT functional
    VWN5 : SimpleKeyword
        DFT functional
    WB2GP_PLYP : SimpleKeyword
        DFT functional
    WB2PLYP : SimpleKeyword
        DFT functional
    WB88PP86 : SimpleKeyword
        DFT functional
    WB97 : SimpleKeyword
        DFT functional
    WB97M_D3BJ : SimpleKeyword
        DFT functional
    WB97M_D4 : SimpleKeyword
        DFT functional
    WB97M_D4REV : SimpleKeyword
        DFT functional
    WB97M_V : SimpleKeyword
        DFT functional
    WB97M_2 : SimpleKeyword
        DFT functional
    WB97X : SimpleKeyword
        DFT functional
    WB97X_2 : SimpleKeyword
        DFT functional
    WB97X_2_TQZ : SimpleKeyword
        DFT functional
    WB97X_D3 : SimpleKeyword
        DFT functional
    WB97X_D3BJ : SimpleKeyword
        DFT functional
    WB97X_D4 : SimpleKeyword
        DFT functional
    WB97X_D4REV : SimpleKeyword
        DFT functional
    WB97X_V : SimpleKeyword
        DFT functional
    WPBEPP86 : SimpleKeyword
        DFT functional
    WPR2SCAN50 : SimpleKeyword
        DFT functional
    WR2SCAN : SimpleKeyword
        DFT functional
    X3LYP : SimpleKeyword
        DFT functional
    XHF : SimpleKeyword
        DFT functional
    XLYP : SimpleKeyword
        DFT functional
    """

    B3LYP3C = SimpleKeyword("b3lyp3c")
    B973C = SimpleKeyword("b973c")
    PBEH3C = SimpleKeyword("pbeh3c")
    WB97X3C = SimpleKeyword("wb97x3c")
    B3LYP_GCP_D3_6_31G_D = SimpleKeyword(
        "b3lyp-gcp-d3/6-31g(d)"
    )  # DFT like 3c methods, do not require dispersion correction or basis set
    B3LYP_GCP_D3_6_31GSTAR = SimpleKeyword("b3lyp-gcp-d3/6-31g*")
    FOD = SimpleKeyword("fod")
    B1LYP = SimpleKeyword("b1lyp")
    B1P = SimpleKeyword("b1p")
    B1P86 = SimpleKeyword("b1p86")
    B1PBE = SimpleKeyword("b1pbe")
    B1PW = SimpleKeyword("b1pw")
    B1PW91 = SimpleKeyword("b1pw91")
    B2GP_PLYP = SimpleKeyword("b2gp-plyp")
    B2K_PLYP = SimpleKeyword("b2k-plyp")
    B2PLYP = SimpleKeyword("b2plyp")
    B2T_PLYP = SimpleKeyword("b2t-plyp")
    B3LYP = SimpleKeyword("b3lyp")
    B3LYP_G = SimpleKeyword("b3lyp_g")
    B3P = SimpleKeyword("b3p")
    B3P86 = SimpleKeyword("b3p86")
    B3PBE = SimpleKeyword("b3pbe")
    B3PW = SimpleKeyword("b3pw")
    B3PW91 = SimpleKeyword("b3pw91")
    B97 = SimpleKeyword("b97")
    B97_D = SimpleKeyword("b97-d")
    B97_D3 = SimpleKeyword("b97-d3")
    B97_D4 = SimpleKeyword("b97-d4")
    B97M_D3BJ = SimpleKeyword("b97m-d3bj")
    B97M_D4 = SimpleKeyword("b97m-d4")
    B97M_V = SimpleKeyword("b97m-v")
    BHANDHLYP = SimpleKeyword("bhandhlyp")
    BHLYP = SimpleKeyword("bhlyp")
    BLYP = SimpleKeyword("blyp")
    BNULL = SimpleKeyword("bnull")
    BP86 = SimpleKeyword("bp86")
    BPBE = SimpleKeyword("bpbe")
    BPW = SimpleKeyword("bpw")
    BPW91 = SimpleKeyword("bpw91")
    BVWN = SimpleKeyword("bvwn")
    CAM_B3LYP = SimpleKeyword("cam-b3lyp")
    DLPNO_B2GP_PLYP = SimpleKeyword("dlpno-b2gp-plyp")
    DLPNO_B2K_PLYP = SimpleKeyword("dlpno-b2k-plyp")
    DLPNO_B2PLYP = SimpleKeyword("dlpno-b2plyp")
    DLPNO_B2T_PLYP = SimpleKeyword("dlpno-b2t-plyp")
    DLPNO_DSD_BLYP = SimpleKeyword("dlpno-dsd-blyp")
    DLPNO_DSD_PBEB95 = SimpleKeyword("dlpno-dsd-pbeb95")
    DLPNO_DSD_PBEP86 = SimpleKeyword("dlpno-dsd-pbep86")
    DLPNO_KPR2SCAN50 = SimpleKeyword("dlpno-kpr2scan50")
    DLPNO_MPW2PLYP = SimpleKeyword("dlpno-mpw2plyp")
    DLPNO_PBE_QIDH = SimpleKeyword("dlpno-pbe-qidh")
    DLPNO_PBE0_2 = SimpleKeyword("dlpno-pbe0-2")
    DLPNO_PBE0_DH = SimpleKeyword("dlpno-pbe0-dh")
    DLPNO_PR2SCAN50 = SimpleKeyword("dlpno-pr2scan50")
    DLPNO_PR2SCAN69 = SimpleKeyword("dlpno-pr2scan69")
    DLPNO_PWPB95 = SimpleKeyword("dlpno-pwpb95")
    DLPNO_R2SCAN_CIDH = SimpleKeyword("dlpno-r2scan-cidh")
    DLPNO_R2SCAN_QIDH = SimpleKeyword("dlpno-r2scan-qidh")
    DLPNO_R2SCAN0_2 = SimpleKeyword("dlpno-r2scan0-2")
    DLPNO_R2SCAN0_DH = SimpleKeyword("dlpno-r2scan0-dh")
    DLPNO_RSX_0DH = SimpleKeyword("dlpno-rsx-0dh")
    DLPNO_RSX_QIDH = SimpleKeyword("dlpno-rsx-qidh")
    DLPNO_SCS_B2GP_PLYP21 = SimpleKeyword("dlpno-scs-b2gp-plyp21")
    DLPNO_SCS_PBE_QIDH = SimpleKeyword("dlpno-scs-pbe-qidh")
    DLPNO_SCS_RSX_QIDH = SimpleKeyword("dlpno-scs-rsx-qidh")
    DLPNO_SCS_WB2GP_PLYP = SimpleKeyword("dlpno-scs-wb2gp-plyp")
    DLPNO_SCS_WB88PP86 = SimpleKeyword("dlpno-scs-wb88pp86")
    DLPNO_SCS_WPBEPP86 = SimpleKeyword("dlpno-scs-wpbepp86")
    DLPNO_SCS_SOS_B2PLYP21 = SimpleKeyword("dlpno-scs/sos-b2plyp21")
    DLPNO_SCS_SOS_WB2PLYP = SimpleKeyword("dlpno-scs/sos-wb2plyp")
    DLPNO_SOS_B2GP_PLYP21 = SimpleKeyword("dlpno-sos-b2gp-plyp21")
    DLPNO_SOS_PBE_QIDH = SimpleKeyword("dlpno-sos-pbe-qidh")
    DLPNO_SOS_RSX_QIDH = SimpleKeyword("dlpno-sos-rsx-qidh")
    DLPNO_SOS_WB2GP_PLYP = SimpleKeyword("dlpno-sos-wb2gp-plyp")
    DLPNO_SOS_WB88PP86 = SimpleKeyword("dlpno-sos-wb88pp86")
    DLPNO_SOS_WPBEPP86 = SimpleKeyword("dlpno-sos-wpbepp86")
    DLPNO_WB2GP_PLYP = SimpleKeyword("dlpno-wb2gp-plyp")
    DLPNO_WB2PLYP = SimpleKeyword("dlpno-wb2plyp")
    DLPNO_WB88PP86 = SimpleKeyword("dlpno-wb88pp86")
    DLPNO_WB97M_2 = SimpleKeyword("dlpno-wb97m(2)")
    DLPNO_WB97X_2 = SimpleKeyword("dlpno-wb97x-2")
    DLPNO_WB97X_2_TQZ = SimpleKeyword(
        "dlpno-wb97x-2(tqz)"
    )  # Double-hybrid DFT with DLPNO approximation
    DLPNO_WPBEPP86 = SimpleKeyword("dlpno-wpbepp86")
    DLPNO_WPR2SCAN50 = SimpleKeyword("dlpno-wpr2scan50")
    DSD_BLYP = SimpleKeyword("dsd-blyp")
    DSD_PBEB95 = SimpleKeyword("dsd-pbeb95")
    DSD_PBEP86 = SimpleKeyword("dsd-pbep86")
    G1LYP = SimpleKeyword("g1lyp")
    G1P = SimpleKeyword("g1p")
    G3LYP = SimpleKeyword("g3lyp")
    G3P = SimpleKeyword("g3p")
    GLYP = SimpleKeyword("glyp")
    GP = SimpleKeyword("gp")
    HFLDA = SimpleKeyword("hflda")
    HFS = SimpleKeyword("hfs")
    KPR2SCAN50 = SimpleKeyword("kpr2scan50")
    LB94 = SimpleKeyword("lb94")
    LC_BLYP = SimpleKeyword("lc-blyp")
    LC_PBE = SimpleKeyword("lc-pbe")
    LDA = SimpleKeyword("lda")
    LRC_PBE = SimpleKeyword("lrc-pbe")
    LSD = SimpleKeyword("lsd")
    M06 = SimpleKeyword("m06")
    M062X = SimpleKeyword("m062x")
    M06L = SimpleKeyword("m06l")
    MPW1LYP = SimpleKeyword("mpw1lyp")
    MPW1PW = SimpleKeyword("mpw1pw")
    MPW2PLYP = SimpleKeyword("mpw2plyp")
    MPWLYP = SimpleKeyword("mpwlyp")
    MPWPW = SimpleKeyword("mpwpw")
    O3LYP = SimpleKeyword("o3lyp")
    OLYP = SimpleKeyword("olyp")
    OPBE = SimpleKeyword("opbe")
    PBE = SimpleKeyword("pbe")
    PBE_QIDH = SimpleKeyword("pbe-qidh")
    PBE0 = SimpleKeyword("pbe0")
    PBE0_2 = SimpleKeyword("pbe0-2")
    PBE0_DH = SimpleKeyword("pbe0-dh")
    PR2SCAN50 = SimpleKeyword("pr2scan50")
    PR2SCAN69 = SimpleKeyword("pr2scan69")
    PW1PW = SimpleKeyword("pw1pw")
    PW6B95 = SimpleKeyword("pw6b95")
    PW86PBE = SimpleKeyword("pw86pbe")
    PW91 = SimpleKeyword("pw91")
    PW91_0 = SimpleKeyword("pw91_0")
    PWLDA = SimpleKeyword("pwlda")
    PWP = SimpleKeyword("pwp")
    PWP1 = SimpleKeyword("pwp1")
    PWPB95 = SimpleKeyword("pwpb95")
    R2SCAN = SimpleKeyword("r2scan")
    R2SCAN_3C = SimpleKeyword("r2scan-3c")
    R2SCAN_CIDH = SimpleKeyword("r2scan-cidh")
    R2SCAN_QIDH = SimpleKeyword("r2scan-qidh")
    R2SCAN0 = SimpleKeyword("r2scan0")
    R2SCAN0 = SimpleKeyword("r2scan0")
    R2SCAN0_2 = SimpleKeyword("r2scan0-2")
    R2SCAN0_DH = SimpleKeyword("r2scan0-dh")
    R2SCAN50 = SimpleKeyword("r2scan50")
    R2SCANH = SimpleKeyword("r2scanh")
    REVDOD_PBEP86_D4_2021 = SimpleKeyword("revdod-pbep86-d4/2021")
    REVDOD_PBEP86_2021 = SimpleKeyword("revdod-pbep86/2021")
    REVDSD_PBEP86_D4_2021 = SimpleKeyword("revdsd-pbep86-d4/2021")
    REVDSD_PBEP86_2021 = SimpleKeyword("revdsd-pbep86/2021")
    REVPBE = SimpleKeyword("revpbe")
    REVPBE0 = SimpleKeyword("revpbe0")
    REVPBE38 = SimpleKeyword("revpbe38")
    REVTPSS = SimpleKeyword("revtpss")
    RPBE = SimpleKeyword("rpbe")
    RPW86PBE = SimpleKeyword("rpw86pbe")
    RSCAN = SimpleKeyword("rscan")
    RSX_0DH = SimpleKeyword("rsx-0dh")
    RSX_QIDH = SimpleKeyword("rsx-qidh")
    SCANFUNC = SimpleKeyword("scanfunc")
    SCS_B2GP_PLYP21 = SimpleKeyword("scs-b2gp-plyp21")
    SCS_PBE_QIDH = SimpleKeyword("scs-pbe-qidh")
    SCS_RSX_QIDH = SimpleKeyword("scs-rsx-qidh")
    SCS_WB2GP_PLYP = SimpleKeyword("scs-wb2gp-plyp")
    SCS_WB88PP86 = SimpleKeyword("scs-wb88pp86")
    SCS_WPBEPP86 = SimpleKeyword("scs-wpbepp86")
    SCS_SOS_B2PLYP21 = SimpleKeyword("scs/sos-b2plyp21")
    SCS_SOS_WB2PLYP = SimpleKeyword("scs/sos-wb2plyp")
    SOS_B2GP_PLYP21 = SimpleKeyword("sos-b2gp-plyp21")
    SOS_PBE_QIDH = SimpleKeyword("sos-pbe-qidh")
    SOS_RSX_QIDH = SimpleKeyword("sos-rsx-qidh")
    SOS_WB2GP_PLYP = SimpleKeyword("sos-wb2gp-plyp")
    SOS_WB88PP86 = SimpleKeyword("sos-wb88pp86")
    SOS_WPBEPP86 = SimpleKeyword("sos-wpbepp86")
    TPSS = SimpleKeyword("tpss")
    TPSS0 = SimpleKeyword("tpss0")
    TPSSH = SimpleKeyword("tpssh")
    VWN = SimpleKeyword("vwn")
    VWN3 = SimpleKeyword("vwn3")
    VWN5 = SimpleKeyword("vwn5")
    WB2GP_PLYP = SimpleKeyword("wb2gp-plyp")
    WB2PLYP = SimpleKeyword("wb2plyp")
    WB88PP86 = SimpleKeyword("wb88pp86")
    WB97 = SimpleKeyword("wb97")
    WB97M_D3BJ = SimpleKeyword("wb97m-d3bj")
    WB97M_D4 = SimpleKeyword("wb97m-d4")
    WB97M_D4REV = SimpleKeyword("wb97m-d4rev")
    WB97M_V = SimpleKeyword("wb97m-v")
    WB97M_2 = SimpleKeyword("wb97m(2)")
    WB97X = SimpleKeyword("wb97x")
    WB97X_2 = SimpleKeyword("wb97x-2")
    WB97X_2_TQZ = SimpleKeyword("wb97x-2(tqz)")
    WB97X_D3 = SimpleKeyword("wb97x-d3")
    WB97X_D3BJ = SimpleKeyword("wb97x-d3bj")
    WB97X_D4 = SimpleKeyword("wb97x-d4")
    WB97X_D4REV = SimpleKeyword("wb97x-d4rev")
    WB97X_V = SimpleKeyword("wb97x-v")
    WPBEPP86 = SimpleKeyword("wpbepp86")
    WPR2SCAN50 = SimpleKeyword("wpr2scan50")
    WR2SCAN = SimpleKeyword("wr2scan")
    X3LYP = SimpleKeyword("x3lyp")
    XHF = SimpleKeyword("xhf")
    XLYP = SimpleKeyword("xlyp")
