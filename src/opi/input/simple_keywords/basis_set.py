from opi.input.simple_keywords.base import (
    ORCAKeyword,
    SimpleKeywordBox,
)

__all__ = ("BasisSet",)


class BasisSet(SimpleKeywordBox):
    """Enum to store all simple keywords of type BasisSet."""

    G3_21G = ORCAKeyword("3-21g")
    """ORCAKeyword: BasisSet."""
    G3_21GSP = ORCAKeyword("3-21gsp")
    """ORCAKeyword: BasisSet."""
    G4_22GSP = ORCAKeyword("4-22gsp")
    """ORCAKeyword: BasisSet."""
    G6_31PLUSPLUSG_2D_2P = ORCAKeyword("6-31++g(2d,2p)")
    """ORCAKeyword: BasisSet."""
    G6_31PLUSPLUSG_2D_P = ORCAKeyword("6-31++g(2d,p)")
    """ORCAKeyword: BasisSet."""
    G6_31PLUSPLUSG_2DF_2P = ORCAKeyword("6-31++g(2df,2p)")
    """ORCAKeyword: BasisSet."""
    G6_31PLUSPLUSG_2DF_2PD = ORCAKeyword("6-31++g(2df,2pd)")
    """ORCAKeyword: BasisSet."""
    G6_31PLUSPLUSG_D_P = ORCAKeyword("6-31++g(d,p)")
    """ORCAKeyword: BasisSet."""
    G6_31PLUSPLUSGSTARSTAR = ORCAKeyword("6-31++g**")
    """ORCAKeyword: BasisSet."""
    G6_31PLUSG_2D_2P = ORCAKeyword("6-31+g(2d,2p)")
    """ORCAKeyword: BasisSet."""
    G6_31PLUSG_2D_P = ORCAKeyword("6-31+g(2d,p)")
    """ORCAKeyword: BasisSet."""
    G6_31PLUSG_2D = ORCAKeyword("6-31+g(2d)")
    """ORCAKeyword: BasisSet."""
    G6_31PLUSG_2DF_2P = ORCAKeyword("6-31+g(2df,2p)")
    """ORCAKeyword: BasisSet."""
    G6_31PLUSG_2DF_2PD = ORCAKeyword("6-31+g(2df,2pd)")
    """ORCAKeyword: BasisSet."""
    G6_31PLUSG_2DF = ORCAKeyword("6-31+g(2df)")
    """ORCAKeyword: BasisSet."""
    G6_31PLUSG_D_P = ORCAKeyword("6-31+g(d,p)")
    """ORCAKeyword: BasisSet."""
    G6_31PLUSG_D = ORCAKeyword("6-31+g(d)")
    """ORCAKeyword: BasisSet."""
    G6_31PLUSGSTAR = ORCAKeyword("6-31+g*")
    """ORCAKeyword: BasisSet."""
    G6_31PLUSGSTARSTAR = ORCAKeyword("6-31+g**")
    """ORCAKeyword: BasisSet."""
    G6_311PLUSPLUSG_2D_2P = ORCAKeyword("6-311++g(2d,2p)")
    """ORCAKeyword: BasisSet."""
    G6_311PLUSPLUSG_2D_P = ORCAKeyword("6-311++g(2d,p)")
    """ORCAKeyword: BasisSet."""
    G6_311PLUSPLUSG_2DF_2P = ORCAKeyword("6-311++g(2df,2p)")
    """ORCAKeyword: BasisSet."""
    G6_311PLUSPLUSG_2DF_2PD = ORCAKeyword("6-311++g(2df,2pd)")
    """ORCAKeyword: BasisSet."""
    G6_311PLUSPLUSG_3DF_3PD = ORCAKeyword("6-311++g(3df,3pd)")
    """ORCAKeyword: BasisSet."""
    G6_311PLUSPLUSG_D_P = ORCAKeyword("6-311++g(d,p)")
    """ORCAKeyword: BasisSet."""
    G6_311PLUSPLUSGSTARSTAR = ORCAKeyword("6-311++g**")
    """ORCAKeyword: BasisSet."""
    G6_311PLUSG_2D_2P = ORCAKeyword("6-311+g(2d,2p)")
    """ORCAKeyword: BasisSet."""
    G6_311PLUSG_2D_P = ORCAKeyword("6-311+g(2d,p)")
    """ORCAKeyword: BasisSet."""
    G6_311PLUSG_2D = ORCAKeyword("6-311+g(2d)")
    """ORCAKeyword: BasisSet."""
    G6_311PLUSG_2DF_2P = ORCAKeyword("6-311+g(2df,2p)")
    """ORCAKeyword: BasisSet."""
    G6_311PLUSG_2DF_2PD = ORCAKeyword("6-311+g(2df,2pd)")
    """ORCAKeyword: BasisSet."""
    G6_311PLUSG_2DF = ORCAKeyword("6-311+g(2df)")
    """ORCAKeyword: BasisSet."""
    G6_311PLUSG_3DF_2P = ORCAKeyword("6-311+g(3df,2p)")
    """ORCAKeyword: BasisSet."""
    G6_311PLUSG_3DF_3PD = ORCAKeyword("6-311+g(3df,3pd)")
    """ORCAKeyword: BasisSet."""
    G6_311PLUSG_3DF = ORCAKeyword("6-311+g(3df)")
    """ORCAKeyword: BasisSet."""
    G6_311PLUSG_D_P = ORCAKeyword("6-311+g(d,p)")
    """ORCAKeyword: BasisSet."""
    G6_311PLUSG_D = ORCAKeyword("6-311+g(d)")
    """ORCAKeyword: BasisSet."""
    G6_311PLUSGSTAR = ORCAKeyword("6-311+g*")
    """ORCAKeyword: BasisSet."""
    G6_311PLUSGSTARSTAR = ORCAKeyword("6-311+g**")
    """ORCAKeyword: BasisSet."""
    G6_311G = ORCAKeyword("6-311g")
    """ORCAKeyword: BasisSet."""
    G6_311G_2D_2P = ORCAKeyword("6-311g(2d,2p)")
    """ORCAKeyword: BasisSet."""
    G6_311G_2D_P = ORCAKeyword("6-311g(2d,p)")
    """ORCAKeyword: BasisSet."""
    G6_311G_2D = ORCAKeyword("6-311g(2d)")
    """ORCAKeyword: BasisSet."""
    G6_311G_2DF_2P = ORCAKeyword("6-311g(2df,2p)")
    """ORCAKeyword: BasisSet."""
    G6_311G_2DF_2PD = ORCAKeyword("6-311g(2df,2pd)")
    """ORCAKeyword: BasisSet."""
    G6_311G_2DF = ORCAKeyword("6-311g(2df)")
    """ORCAKeyword: BasisSet."""
    G6_311G_3DF_3PD = ORCAKeyword("6-311g(3df,3pd)")
    """ORCAKeyword: BasisSet."""
    G6_311G_3DF = ORCAKeyword("6-311g(3df)")
    """ORCAKeyword: BasisSet."""
    G6_311G_D_P = ORCAKeyword("6-311g(d,p)")
    """ORCAKeyword: BasisSet."""
    G6_311G_D = ORCAKeyword("6-311g(d)")
    """ORCAKeyword: BasisSet."""
    G6_311GSTAR = ORCAKeyword("6-311g*")
    """ORCAKeyword: BasisSet."""
    G6_311GSTARSTAR = ORCAKeyword("6-311g**")
    """ORCAKeyword: BasisSet."""
    G6_31G = ORCAKeyword("6-31g")
    """ORCAKeyword: BasisSet."""
    G6_31G_2D_2P = ORCAKeyword("6-31g(2d,2p)")
    """ORCAKeyword: BasisSet."""
    G6_31G_2D_P = ORCAKeyword("6-31g(2d,p)")
    """ORCAKeyword: BasisSet."""
    G6_31G_2D = ORCAKeyword("6-31g(2d)")
    """ORCAKeyword: BasisSet."""
    G6_31G_2DF_2P = ORCAKeyword("6-31g(2df,2p)")
    """ORCAKeyword: BasisSet."""
    G6_31G_2DF_2PD = ORCAKeyword("6-31g(2df,2pd)")
    """ORCAKeyword: BasisSet."""
    G6_31G_2DF = ORCAKeyword("6-31g(2df)")
    """ORCAKeyword: BasisSet."""
    G6_31G_D_P = ORCAKeyword("6-31g(d,p)")
    """ORCAKeyword: BasisSet."""
    G6_31G_D = ORCAKeyword("6-31g(d)")
    """ORCAKeyword: BasisSet."""
    G6_31GSTAR = ORCAKeyword("6-31g*")
    """ORCAKeyword: BasisSet."""
    G6_31GSTARSTAR = ORCAKeyword("6-31g**")
    """ORCAKeyword: BasisSet."""
    AHGBS_5 = ORCAKeyword("ahgbs-5")
    """ORCAKeyword: BasisSet."""
    AHGBS_7 = ORCAKeyword("ahgbs-7")
    """ORCAKeyword: BasisSet."""
    AHGBS_9 = ORCAKeyword("ahgbs-9")
    """ORCAKeyword: BasisSet."""
    AHGBSP1_5 = ORCAKeyword("ahgbsp1-5")
    """ORCAKeyword: BasisSet."""
    AHGBSP1_7 = ORCAKeyword("ahgbsp1-7")
    """ORCAKeyword: BasisSet."""
    AHGBSP1_9 = ORCAKeyword("ahgbsp1-9")
    """ORCAKeyword: BasisSet."""
    AHGBSP2_5 = ORCAKeyword("ahgbsp2-5")
    """ORCAKeyword: BasisSet."""
    AHGBSP2_7 = ORCAKeyword("ahgbsp2-7")
    """ORCAKeyword: BasisSet."""
    AHGBSP2_9 = ORCAKeyword("ahgbsp2-9")
    """ORCAKeyword: BasisSet."""
    AHGBSP3_5 = ORCAKeyword("ahgbsp3-5")
    """ORCAKeyword: BasisSet."""
    AHGBSP3_7 = ORCAKeyword("ahgbsp3-7")
    """ORCAKeyword: BasisSet."""
    AHGBSP3_9 = ORCAKeyword("ahgbsp3-9")
    """ORCAKeyword: BasisSet."""
    ANO_PC_0 = ORCAKeyword("ano-pc-0")
    """ORCAKeyword: BasisSet."""
    ANO_PC_0_POL = ORCAKeyword("ano-pc-0-pol")
    """ORCAKeyword: BasisSet."""
    ANO_PV5Z = ORCAKeyword("ano-pv5z")
    """ORCAKeyword: BasisSet."""
    ANO_PV6Z = ORCAKeyword("ano-pv6z")
    """ORCAKeyword: BasisSet."""
    ANO_PVDZ = ORCAKeyword("ano-pvdz")
    """ORCAKeyword: BasisSet."""
    ANO_PVQZ = ORCAKeyword("ano-pvqz")
    """ORCAKeyword: BasisSet."""
    ANO_PVTZ = ORCAKeyword("ano-pvtz")
    """ORCAKeyword: BasisSet."""
    ANO_RCC_DZP = ORCAKeyword("ano-rcc-dzp")
    """ORCAKeyword: BasisSet."""
    ANO_RCC_FULL = ORCAKeyword("ano-rcc-full")
    """ORCAKeyword: BasisSet."""
    ANO_RCC_MB = ORCAKeyword("ano-rcc-mb")
    """ORCAKeyword: BasisSet."""
    ANO_RCC_QZP = ORCAKeyword("ano-rcc-qzp")
    """ORCAKeyword: BasisSet."""
    ANO_RCC_TZP = ORCAKeyword("ano-rcc-tzp")
    """ORCAKeyword: BasisSet."""
    ANO_SZ = ORCAKeyword("ano-sz")
    """ORCAKeyword: BasisSet."""
    ANO_SZ_DKH_SMALL = ORCAKeyword("ano-sz-dkh-small")
    """ORCAKeyword: BasisSet."""
    APR_CC_PV_QPLUSD_Z = ORCAKeyword("apr-cc-pv(q+d)z")
    """ORCAKeyword: BasisSet."""
    AUG_ANO_PV5Z = ORCAKeyword("aug-ano-pv5z")
    """ORCAKeyword: BasisSet."""
    AUG_ANO_PVDZ = ORCAKeyword("aug-ano-pvdz")
    """ORCAKeyword: BasisSet."""
    AUG_ANO_PVQZ = ORCAKeyword("aug-ano-pvqz")
    """ORCAKeyword: BasisSet."""
    AUG_ANO_PVTZ = ORCAKeyword("aug-ano-pvtz")
    """ORCAKeyword: BasisSet."""
    AUG_CC_PCV5Z = ORCAKeyword("aug-cc-pcv5z")
    """ORCAKeyword: BasisSet."""
    AUG_CC_PCV5Z_PP = ORCAKeyword("aug-cc-pcv5z-pp")
    """ORCAKeyword: BasisSet."""
    AUG_CC_PCV6Z = ORCAKeyword("aug-cc-pcv6z")
    """ORCAKeyword: BasisSet."""
    AUG_CC_PCVDZ = ORCAKeyword("aug-cc-pcvdz")
    """ORCAKeyword: BasisSet."""
    AUG_CC_PCVDZ_PP = ORCAKeyword("aug-cc-pcvdz-pp")
    """ORCAKeyword: BasisSet."""
    AUG_CC_PCVQZ = ORCAKeyword("aug-cc-pcvqz")
    """ORCAKeyword: BasisSet."""
    AUG_CC_PCVQZ_PP = ORCAKeyword("aug-cc-pcvqz-pp")
    """ORCAKeyword: BasisSet."""
    AUG_CC_PCVTZ = ORCAKeyword("aug-cc-pcvtz")
    """ORCAKeyword: BasisSet."""
    AUG_CC_PCVTZ_PP = ORCAKeyword("aug-cc-pcvtz-pp")
    """ORCAKeyword: BasisSet."""
    AUG_CC_PV5_PLUSD_Z = ORCAKeyword("aug-cc-pv5(+d)z")
    """ORCAKeyword: BasisSet."""
    AUG_CC_PV5Z = ORCAKeyword("aug-cc-pv5z")
    """ORCAKeyword: BasisSet."""
    AUG_CC_PV5Z_DK = ORCAKeyword("aug-cc-pv5z-dk")
    """ORCAKeyword: BasisSet."""
    AUG_CC_PV5Z_PP = ORCAKeyword("aug-cc-pv5z-pp")
    """ORCAKeyword: BasisSet."""
    AUG_CC_PV5Z_PP_OPTRI = ORCAKeyword("aug-cc-pv5z-pp-optri")
    """ORCAKeyword: BasisSet."""
    AUG_CC_PV6_PLUSD_Z = ORCAKeyword("aug-cc-pv6(+d)z")
    """ORCAKeyword: BasisSet."""
    AUG_CC_PV6Z = ORCAKeyword("aug-cc-pv6z")
    """ORCAKeyword: BasisSet."""
    AUG_CC_PV7Z = ORCAKeyword("aug-cc-pv7z")
    """ORCAKeyword: BasisSet."""
    AUG_CC_PVD_PLUSD_Z = ORCAKeyword("aug-cc-pvd(+d)z")
    """ORCAKeyword: BasisSet."""
    AUG_CC_PVDZ = ORCAKeyword("aug-cc-pvdz")
    """ORCAKeyword: BasisSet."""
    AUG_CC_PVDZ_DK = ORCAKeyword("aug-cc-pvdz-dk")
    """ORCAKeyword: BasisSet."""
    AUG_CC_PVDZ_PP = ORCAKeyword("aug-cc-pvdz-pp")
    """ORCAKeyword: BasisSet."""
    AUG_CC_PVDZ_PP_OPTRI = ORCAKeyword("aug-cc-pvdz-pp-optri")
    """ORCAKeyword: BasisSet."""
    AUG_CC_PVQ_PLUSD_Z = ORCAKeyword("aug-cc-pvq(+d)z")
    """ORCAKeyword: BasisSet."""
    AUG_CC_PVQZ = ORCAKeyword("aug-cc-pvqz")
    """ORCAKeyword: BasisSet."""
    AUG_CC_PVQZ_DK = ORCAKeyword("aug-cc-pvqz-dk")
    """ORCAKeyword: BasisSet."""
    AUG_CC_PVQZ_PP = ORCAKeyword("aug-cc-pvqz-pp")
    """ORCAKeyword: BasisSet."""
    AUG_CC_PVQZ_PP_OPTRI = ORCAKeyword("aug-cc-pvqz-pp-optri")
    """ORCAKeyword: BasisSet."""
    AUG_CC_PVT_PLUSD_Z = ORCAKeyword("aug-cc-pvt(+d)z")
    """ORCAKeyword: BasisSet."""
    AUG_CC_PVTZ = ORCAKeyword("aug-cc-pvtz")
    """ORCAKeyword: BasisSet."""
    AUG_CC_PVTZ_DK = ORCAKeyword("aug-cc-pvtz-dk")
    """ORCAKeyword: BasisSet."""
    AUG_CC_PVTZ_J = ORCAKeyword("aug-cc-pvtz-j")
    """ORCAKeyword: BasisSet."""
    AUG_CC_PVTZ_PP = ORCAKeyword("aug-cc-pvtz-pp")
    """ORCAKeyword: BasisSet."""
    AUG_CC_PVTZ_PP_OPTRI = ORCAKeyword("aug-cc-pvtz-pp-optri")
    """ORCAKeyword: BasisSet."""
    AUG_CC_PWCV5Z = ORCAKeyword("aug-cc-pwcv5z")
    """ORCAKeyword: BasisSet."""
    AUG_CC_PWCV5Z_DK = ORCAKeyword("aug-cc-pwcv5z-dk")
    """ORCAKeyword: BasisSet."""
    AUG_CC_PWCV5Z_PP = ORCAKeyword("aug-cc-pwcv5z-pp")
    """ORCAKeyword: BasisSet."""
    AUG_CC_PWCV5Z_PP_OPTRI = ORCAKeyword("aug-cc-pwcv5z-pp-optri")
    """ORCAKeyword: BasisSet."""
    AUG_CC_PWCVDZ = ORCAKeyword("aug-cc-pwcvdz")
    """ORCAKeyword: BasisSet."""
    AUG_CC_PWCVDZ_DK = ORCAKeyword("aug-cc-pwcvdz-dk")
    """ORCAKeyword: BasisSet."""
    AUG_CC_PWCVDZ_PP = ORCAKeyword("aug-cc-pwcvdz-pp")
    """ORCAKeyword: BasisSet."""
    AUG_CC_PWCVDZ_PP_OPTRI = ORCAKeyword("aug-cc-pwcvdz-pp-optri")
    """ORCAKeyword: BasisSet."""
    AUG_CC_PWCVQZ = ORCAKeyword("aug-cc-pwcvqz")
    """ORCAKeyword: BasisSet."""
    AUG_CC_PWCVQZ_DK = ORCAKeyword("aug-cc-pwcvqz-dk")
    """ORCAKeyword: BasisSet."""
    AUG_CC_PWCVQZ_PP = ORCAKeyword("aug-cc-pwcvqz-pp")
    """ORCAKeyword: BasisSet."""
    AUG_CC_PWCVQZ_PP_OPTRI = ORCAKeyword("aug-cc-pwcvqz-pp-optri")
    """ORCAKeyword: BasisSet."""
    AUG_CC_PWCVTZ = ORCAKeyword("aug-cc-pwcvtz")
    """ORCAKeyword: BasisSet."""
    AUG_CC_PWCVTZ_DK = ORCAKeyword("aug-cc-pwcvtz-dk")
    """ORCAKeyword: BasisSet."""
    AUG_CC_PWCVTZ_PP = ORCAKeyword("aug-cc-pwcvtz-pp")
    """ORCAKeyword: BasisSet."""
    AUG_CC_PWCVTZ_PP_OPTRI = ORCAKeyword("aug-cc-pwcvtz-pp-optri")
    """ORCAKeyword: BasisSet."""
    AUG_PC_0 = ORCAKeyword("aug-pc-0")
    """ORCAKeyword: BasisSet."""
    AUG_PC_1 = ORCAKeyword("aug-pc-1")
    """ORCAKeyword: BasisSet."""
    AUG_PC_2 = ORCAKeyword("aug-pc-2")
    """ORCAKeyword: BasisSet."""
    AUG_PC_3 = ORCAKeyword("aug-pc-3")
    """ORCAKeyword: BasisSet."""
    AUG_PC_4 = ORCAKeyword("aug-pc-4")
    """ORCAKeyword: BasisSet."""
    AUG_PCH_1 = ORCAKeyword("aug-pch-1")
    """ORCAKeyword: BasisSet."""
    AUG_PCH_2 = ORCAKeyword("aug-pch-2")
    """ORCAKeyword: BasisSet."""
    AUG_PCH_3 = ORCAKeyword("aug-pch-3")
    """ORCAKeyword: BasisSet."""
    AUG_PCH_4 = ORCAKeyword("aug-pch-4")
    """ORCAKeyword: BasisSet."""
    AUG_PCJ_0 = ORCAKeyword("aug-pcj-0")
    """ORCAKeyword: BasisSet."""
    AUG_PCJ_1 = ORCAKeyword("aug-pcj-1")
    """ORCAKeyword: BasisSet."""
    AUG_PCJ_2 = ORCAKeyword("aug-pcj-2")
    """ORCAKeyword: BasisSet."""
    AUG_PCJ_3 = ORCAKeyword("aug-pcj-3")
    """ORCAKeyword: BasisSet."""
    AUG_PCJ_4 = ORCAKeyword("aug-pcj-4")
    """ORCAKeyword: BasisSet."""
    AUG_PCSEG_0 = ORCAKeyword("aug-pcseg-0")
    """ORCAKeyword: BasisSet."""
    AUG_PCSEG_1 = ORCAKeyword("aug-pcseg-1")
    """ORCAKeyword: BasisSet."""
    AUG_PCSEG_2 = ORCAKeyword("aug-pcseg-2")
    """ORCAKeyword: BasisSet."""
    AUG_PCSEG_3 = ORCAKeyword("aug-pcseg-3")
    """ORCAKeyword: BasisSet."""
    AUG_PCSEG_4 = ORCAKeyword("aug-pcseg-4")
    """ORCAKeyword: BasisSet."""
    AUG_PCSSEG_0 = ORCAKeyword("aug-pcsseg-0")
    """ORCAKeyword: BasisSet."""
    AUG_PCSSEG_1 = ORCAKeyword("aug-pcsseg-1")
    """ORCAKeyword: BasisSet."""
    AUG_PCSSEG_2 = ORCAKeyword("aug-pcsseg-2")
    """ORCAKeyword: BasisSet."""
    AUG_PCSSEG_3 = ORCAKeyword("aug-pcsseg-3")
    """ORCAKeyword: BasisSet."""
    AUG_PCSSEG_4 = ORCAKeyword("aug-pcsseg-4")
    """ORCAKeyword: BasisSet."""
    AUG_PCX_1 = ORCAKeyword("aug-pcx-1")
    """ORCAKeyword: BasisSet."""
    AUG_PCX_2 = ORCAKeyword("aug-pcx-2")
    """ORCAKeyword: BasisSet."""
    AUG_PCX_3 = ORCAKeyword("aug-pcx-3")
    """ORCAKeyword: BasisSet."""
    AUG_PCX_4 = ORCAKeyword("aug-pcx-4")
    """ORCAKeyword: BasisSet."""
    CC_PCV5Z = ORCAKeyword("cc-pcv5z")
    """ORCAKeyword: BasisSet."""
    CC_PCV5Z_PP = ORCAKeyword("cc-pcv5z-pp")
    """ORCAKeyword: BasisSet."""
    CC_PCV6Z = ORCAKeyword("cc-pcv6z")
    """ORCAKeyword: BasisSet."""
    CC_PCVDZ = ORCAKeyword("cc-pcvdz")
    """ORCAKeyword: BasisSet."""
    CC_PCVDZ_F12 = ORCAKeyword("cc-pcvdz-f12")
    """ORCAKeyword: BasisSet."""
    CC_PCVDZ_F12_OPTRI = ORCAKeyword("cc-pcvdz-f12-optri")
    """ORCAKeyword: BasisSet."""
    CC_PCVDZ_PP = ORCAKeyword("cc-pcvdz-pp")
    """ORCAKeyword: BasisSet."""
    CC_PCVQZ = ORCAKeyword("cc-pcvqz")
    """ORCAKeyword: BasisSet."""
    CC_PCVQZ_F12 = ORCAKeyword("cc-pcvqz-f12")
    """ORCAKeyword: BasisSet."""
    CC_PCVQZ_F12_OPTRI = ORCAKeyword("cc-pcvqz-f12-optri")
    """ORCAKeyword: BasisSet."""
    CC_PCVQZ_PP = ORCAKeyword("cc-pcvqz-pp")
    """ORCAKeyword: BasisSet."""
    CC_PCVTZ = ORCAKeyword("cc-pcvtz")
    """ORCAKeyword: BasisSet."""
    CC_PCVTZ_F12 = ORCAKeyword("cc-pcvtz-f12")
    """ORCAKeyword: BasisSet."""
    CC_PCVTZ_F12_OPTRI = ORCAKeyword("cc-pcvtz-f12-optri")
    """ORCAKeyword: BasisSet."""
    CC_PCVTZ_PP = ORCAKeyword("cc-pcvtz-pp")
    """ORCAKeyword: BasisSet."""
    CC_PV5_PLUSD_Z = ORCAKeyword("cc-pv5(+d)z")
    """ORCAKeyword: BasisSet."""
    CC_PV5Z = ORCAKeyword("cc-pv5z")
    """ORCAKeyword: BasisSet."""
    CC_PV5Z_DK = ORCAKeyword("cc-pv5z-dk")
    """ORCAKeyword: BasisSet."""
    CC_PV5Z_PP = ORCAKeyword("cc-pv5z-pp")
    """ORCAKeyword: BasisSet."""
    CC_PV6Z = ORCAKeyword("cc-pv6z")
    """ORCAKeyword: BasisSet."""
    CC_PV7Z = ORCAKeyword("cc-pv7z")
    """ORCAKeyword: BasisSet."""
    CC_PV8Z = ORCAKeyword("cc-pv8z")
    """ORCAKeyword: BasisSet."""
    CC_PVD_PLUSD_Z = ORCAKeyword("cc-pvd(+d)z")
    """ORCAKeyword: BasisSet."""
    CC_PVDZ = ORCAKeyword("cc-pvdz")
    """ORCAKeyword: BasisSet."""
    CC_PVDZ_DK = ORCAKeyword("cc-pvdz-dk")
    """ORCAKeyword: BasisSet."""
    CC_PVDZ_DK3 = ORCAKeyword("cc-pvdz-dk3")
    """ORCAKeyword: BasisSet."""
    CC_PVDZ_F12 = ORCAKeyword("cc-pvdz-f12")
    """ORCAKeyword: BasisSet."""
    CC_PVDZ_F12_CABS = ORCAKeyword("cc-pvdz-f12-cabs")
    """ORCAKeyword: BasisSet."""
    CC_PVDZ_F12_OPTRI = ORCAKeyword("cc-pvdz-f12-optri")
    """ORCAKeyword: BasisSet."""
    CC_PVDZ_PP = ORCAKeyword("cc-pvdz-pp")
    """ORCAKeyword: BasisSet."""
    CC_PVDZ_PP_F12 = ORCAKeyword("cc-pvdz-pp-f12")
    """ORCAKeyword: BasisSet."""
    CC_PVDZ_PP_F12_OPTRI = ORCAKeyword("cc-pvdz-pp-f12-optri")
    """ORCAKeyword: BasisSet."""
    CC_PVQ_PLUSD_Z = ORCAKeyword("cc-pvq(+d)z")
    """ORCAKeyword: BasisSet."""
    CC_PVQZ = ORCAKeyword("cc-pvqz")
    """ORCAKeyword: BasisSet."""
    CC_PVQZ_DK = ORCAKeyword("cc-pvqz-dk")
    """ORCAKeyword: BasisSet."""
    CC_PVQZ_DK3 = ORCAKeyword("cc-pvqz-dk3")
    """ORCAKeyword: BasisSet."""
    CC_PVQZ_F12 = ORCAKeyword("cc-pvqz-f12")
    """ORCAKeyword: BasisSet."""
    CC_PVQZ_F12_CABS = ORCAKeyword("cc-pvqz-f12-cabs")
    """ORCAKeyword: BasisSet."""
    CC_PVQZ_F12_OPTRI = ORCAKeyword("cc-pvqz-f12-optri")
    """ORCAKeyword: BasisSet."""
    CC_PVQZ_PP = ORCAKeyword("cc-pvqz-pp")
    """ORCAKeyword: BasisSet."""
    CC_PVQZ_PP_F12 = ORCAKeyword("cc-pvqz-pp-f12")
    """ORCAKeyword: BasisSet."""
    CC_PVQZ_PP_F12_OPTRI = ORCAKeyword("cc-pvqz-pp-f12-optri")
    """ORCAKeyword: BasisSet."""
    CC_PVT_PLUSD_Z = ORCAKeyword("cc-pvt(+d)z")
    """ORCAKeyword: BasisSet."""
    CC_PVTZ = ORCAKeyword("cc-pvtz")
    """ORCAKeyword: BasisSet."""
    CC_PVTZ_DK = ORCAKeyword("cc-pvtz-dk")
    """ORCAKeyword: BasisSet."""
    CC_PVTZ_DK3 = ORCAKeyword("cc-pvtz-dk3")
    """ORCAKeyword: BasisSet."""
    CC_PVTZ_F12 = ORCAKeyword("cc-pvtz-f12")
    """ORCAKeyword: BasisSet."""
    CC_PVTZ_F12_CABS = ORCAKeyword("cc-pvtz-f12-cabs")
    """ORCAKeyword: BasisSet."""
    CC_PVTZ_F12_OPTRI = ORCAKeyword("cc-pvtz-f12-optri")
    """ORCAKeyword: BasisSet."""
    CC_PVTZ_PP = ORCAKeyword("cc-pvtz-pp")
    """ORCAKeyword: BasisSet."""
    CC_PVTZ_PP_F12 = ORCAKeyword("cc-pvtz-pp-f12")
    """ORCAKeyword: BasisSet."""
    CC_PVTZ_PP_F12_OPTRI = ORCAKeyword("cc-pvtz-pp-f12-optri")
    """ORCAKeyword: BasisSet."""
    CC_PWCV5Z = ORCAKeyword("cc-pwcv5z")
    """ORCAKeyword: BasisSet."""
    CC_PWCV5Z_DK = ORCAKeyword("cc-pwcv5z-dk")
    """ORCAKeyword: BasisSet."""
    CC_PWCV5Z_PP = ORCAKeyword("cc-pwcv5z-pp")
    """ORCAKeyword: BasisSet."""
    CC_PWCVDZ = ORCAKeyword("cc-pwcvdz")
    """ORCAKeyword: BasisSet."""
    CC_PWCVDZ_DK = ORCAKeyword("cc-pwcvdz-dk")
    """ORCAKeyword: BasisSet."""
    CC_PWCVDZ_DK3 = ORCAKeyword("cc-pwcvdz-dk3")
    """ORCAKeyword: BasisSet."""
    CC_PWCVDZ_PP = ORCAKeyword("cc-pwcvdz-pp")
    """ORCAKeyword: BasisSet."""
    CC_PWCVQZ = ORCAKeyword("cc-pwcvqz")
    """ORCAKeyword: BasisSet."""
    CC_PWCVQZ_DK = ORCAKeyword("cc-pwcvqz-dk")
    """ORCAKeyword: BasisSet."""
    CC_PWCVQZ_DK3 = ORCAKeyword("cc-pwcvqz-dk3")
    """ORCAKeyword: BasisSet."""
    CC_PWCVQZ_PP = ORCAKeyword("cc-pwcvqz-pp")
    """ORCAKeyword: BasisSet."""
    CC_PWCVTZ = ORCAKeyword("cc-pwcvtz")
    """ORCAKeyword: BasisSet."""
    CC_PWCVTZ_DK = ORCAKeyword("cc-pwcvtz-dk")
    """ORCAKeyword: BasisSet."""
    CC_PWCVTZ_DK3 = ORCAKeyword("cc-pwcvtz-dk3")
    """ORCAKeyword: BasisSet."""
    CC_PWCVTZ_PP = ORCAKeyword("cc-pwcvtz-pp")
    """ORCAKeyword: BasisSet."""
    CP = ORCAKeyword("cp")
    """ORCAKeyword: BasisSet."""
    CP_PPP = ORCAKeyword("cp(ppp)")
    """ORCAKeyword: BasisSet."""
    CRENBL = ORCAKeyword("crenbl")
    """ORCAKeyword: BasisSet."""
    D95 = ORCAKeyword("d95")
    """ORCAKeyword: BasisSet."""
    D95P = ORCAKeyword("d95p")
    """ORCAKeyword: BasisSet."""
    DEF_SV_P = ORCAKeyword("def-sv(p)")
    """ORCAKeyword: BasisSet."""
    DEF_SVP = ORCAKeyword("def-svp")
    """ORCAKeyword: BasisSet."""
    DEF_TZVP = ORCAKeyword("def-tzvp")
    """ORCAKeyword: BasisSet."""
    DEF_TZVPP = ORCAKeyword("def-tzvpp")
    """ORCAKeyword: BasisSet."""
    DEF2_MSVP = ORCAKeyword("def2-msvp")
    """ORCAKeyword: BasisSet."""
    DEF2_MTZVP = ORCAKeyword("def2-mtzvp")
    """ORCAKeyword: BasisSet."""
    DEF2_MTZVPP = ORCAKeyword("def2-mtzvpp")
    """ORCAKeyword: BasisSet."""
    DEF2_QZVP = ORCAKeyword("def2-qzvp")
    """ORCAKeyword: BasisSet."""
    DEF2_QZVPD = ORCAKeyword("def2-qzvpd")
    """ORCAKeyword: BasisSet."""
    DEF2_QZVPP = ORCAKeyword("def2-qzvpp")
    """ORCAKeyword: BasisSet."""
    DEF2_QZVPPD = ORCAKeyword("def2-qzvppd")
    """ORCAKeyword: BasisSet."""
    DEF2_SV_P = ORCAKeyword("def2-sv(p)")
    """ORCAKeyword: BasisSet."""
    DEF2_SVP = ORCAKeyword("def2-svp")
    """ORCAKeyword: BasisSet."""
    DEF2_SVPD = ORCAKeyword("def2-svpd")
    """ORCAKeyword: BasisSet."""
    DEF2_TZVP = ORCAKeyword("def2-tzvp")
    """ORCAKeyword: BasisSet."""
    DEF2_TZVP_F = ORCAKeyword("def2-tzvp(-f)")
    """ORCAKeyword: BasisSet."""
    DEF2_TZVPD = ORCAKeyword("def2-tzvpd")
    """ORCAKeyword: BasisSet."""
    DEF2_TZVPP = ORCAKeyword("def2-tzvpp")
    """ORCAKeyword: BasisSet."""
    DEF2_TZVPPD = ORCAKeyword("def2-tzvppd")
    """ORCAKeyword: BasisSet."""
    DHF_QZVP = ORCAKeyword("dhf-qzvp")
    """ORCAKeyword: BasisSet."""
    DHF_QZVP_2C = ORCAKeyword("dhf-qzvp-2c")
    """ORCAKeyword: BasisSet."""
    DHF_QZVPP = ORCAKeyword("dhf-qzvpp")
    """ORCAKeyword: BasisSet."""
    DHF_QZVPP_2C = ORCAKeyword("dhf-qzvpp-2c")
    """ORCAKeyword: BasisSet."""
    DHF_SV_P = ORCAKeyword("dhf-sv(p)")
    """ORCAKeyword: BasisSet."""
    DHF_SV_P_2C = ORCAKeyword("dhf-sv(p)-2c")
    """ORCAKeyword: BasisSet."""
    DHF_SVP = ORCAKeyword("dhf-svp")
    """ORCAKeyword: BasisSet."""
    DHF_SVP_2C = ORCAKeyword("dhf-svp-2c")
    """ORCAKeyword: BasisSet."""
    DHF_TZVP = ORCAKeyword("dhf-tzvp")
    """ORCAKeyword: BasisSet."""
    DHF_TZVP_2C = ORCAKeyword("dhf-tzvp-2c")
    """ORCAKeyword: BasisSet."""
    DHF_TZVPP = ORCAKeyword("dhf-tzvpp")
    """ORCAKeyword: BasisSet."""
    DHF_TZVPP_2C = ORCAKeyword("dhf-tzvpp-2c")
    """ORCAKeyword: BasisSet."""
    DKH_DEF2_QZVPP = ORCAKeyword("dkh-def2-qzvpp")
    """ORCAKeyword: BasisSet."""
    DKH_DEF2_SV_P = ORCAKeyword("dkh-def2-sv(p)")
    """ORCAKeyword: BasisSet."""
    DKH_DEF2_SVP = ORCAKeyword("dkh-def2-svp")
    """ORCAKeyword: BasisSet."""
    DKH_DEF2_TZVP = ORCAKeyword("dkh-def2-tzvp")
    """ORCAKeyword: BasisSet."""
    DKH_DEF2_TZVP_F = ORCAKeyword("dkh-def2-tzvp(-f)")
    """ORCAKeyword: BasisSet."""
    DKH_DEF2_TZVPP = ORCAKeyword("dkh-def2-tzvpp")
    """ORCAKeyword: BasisSet."""
    DKH_MA_DEF2_QZVPP = ORCAKeyword("dkh-ma-def2-qzvpp")
    """ORCAKeyword: BasisSet."""
    DKH_MA_DEF2_SV_P = ORCAKeyword("dkh-ma-def2-sv(p)")
    """ORCAKeyword: BasisSet."""
    DKH_MA_DEF2_SVP = ORCAKeyword("dkh-ma-def2-svp")
    """ORCAKeyword: BasisSet."""
    DKH_MA_DEF2_TZVP = ORCAKeyword("dkh-ma-def2-tzvp")
    """ORCAKeyword: BasisSet."""
    DKH_MA_DEF2_TZVP_F = ORCAKeyword("dkh-ma-def2-tzvp(-f)")
    """ORCAKeyword: BasisSet."""
    DKH_MA_DEF2_TZVPP = ORCAKeyword("dkh-ma-def2-tzvpp")
    """ORCAKeyword: BasisSet."""
    DKH_QZVP = ORCAKeyword("dkh-qzvp")
    """ORCAKeyword: BasisSet."""
    DKH_QZVPP = ORCAKeyword("dkh-qzvpp")
    """ORCAKeyword: BasisSet."""
    DKH_SV_P = ORCAKeyword("dkh-sv(p)")
    """ORCAKeyword: BasisSet."""
    DKH_SVP = ORCAKeyword("dkh-svp")
    """ORCAKeyword: BasisSet."""
    DKH_TZV_P = ORCAKeyword("dkh-tzv(p)")
    """ORCAKeyword: BasisSet."""
    DKH_TZVP = ORCAKeyword("dkh-tzvp")
    """ORCAKeyword: BasisSet."""
    DKH_TZVPP = ORCAKeyword("dkh-tzvpp")
    """ORCAKeyword: BasisSet."""
    EPR_II = ORCAKeyword("epr-ii")
    """ORCAKeyword: BasisSet."""
    EPR_III = ORCAKeyword("epr-iii")
    """ORCAKeyword: BasisSet."""
    GFN1BASIS = ORCAKeyword("gfn1Basis")
    """ORCAKeyword: BasisSet."""
    GFN2BASIS = ORCAKeyword("gfn2Basis")
    """ORCAKeyword: BasisSet."""
    HAV_5PLUSD_Z = ORCAKeyword("hav(5+d)z")
    """ORCAKeyword: BasisSet."""
    HAV_QPLUSD_Z = ORCAKeyword("hav(q+d)z")
    """ORCAKeyword: BasisSet."""
    HAV_TPLUSD_Z = ORCAKeyword("hav(t+d)z")
    """ORCAKeyword: BasisSet."""
    HAV5Z_PLUSD = ORCAKeyword("hav5z(+d)")
    """ORCAKeyword: BasisSet."""
    HAVQZ_PLUSD = ORCAKeyword("havqz(+d)")
    """ORCAKeyword: BasisSet."""
    HAVTZ_PLUSD = ORCAKeyword("havtz(+d)")
    """ORCAKeyword: BasisSet."""
    HGBS_5 = ORCAKeyword("hgbs-5")
    """ORCAKeyword: BasisSet."""
    HGBS_7 = ORCAKeyword("hgbs-7")
    """ORCAKeyword: BasisSet."""
    HGBS_9 = ORCAKeyword("hgbs-9")
    """ORCAKeyword: BasisSet."""
    HGBSP1_5 = ORCAKeyword("hgbsp1-5")
    """ORCAKeyword: BasisSet."""
    HGBSP1_7 = ORCAKeyword("hgbsp1-7")
    """ORCAKeyword: BasisSet."""
    HGBSP1_9 = ORCAKeyword("hgbsp1-9")
    """ORCAKeyword: BasisSet."""
    HGBSP2_5 = ORCAKeyword("hgbsp2-5")
    """ORCAKeyword: BasisSet."""
    HGBSP2_7 = ORCAKeyword("hgbsp2-7")
    """ORCAKeyword: BasisSet."""
    HGBSP2_9 = ORCAKeyword("hgbsp2-9")
    """ORCAKeyword: BasisSet."""
    HGBSP3_5 = ORCAKeyword("hgbsp3-5")
    """ORCAKeyword: BasisSet."""
    HGBSP3_7 = ORCAKeyword("hgbsp3-7")
    """ORCAKeyword: BasisSet."""
    HGBSP3_9 = ORCAKeyword("hgbsp3-9")
    """ORCAKeyword: BasisSet."""
    IGLO_II = ORCAKeyword("iglo-ii")
    """ORCAKeyword: BasisSet."""
    IGLO_III = ORCAKeyword("iglo-iii")
    """ORCAKeyword: BasisSet."""
    JUL_CC_PV_DPLUSD_Z = ORCAKeyword("jul-cc-pv(d+d)z")
    """ORCAKeyword: BasisSet."""
    JUL_CC_PV_QPLUSD_Z = ORCAKeyword("jul-cc-pv(q+d)z")
    """ORCAKeyword: BasisSet."""
    JUL_CC_PV_TPLUSD_Z = ORCAKeyword("jul-cc-pv(t+d)z")
    """ORCAKeyword: BasisSet."""
    JUN_CC_PV_DPLUSD_Z = ORCAKeyword("jun-cc-pv(d+d)z")
    """ORCAKeyword: BasisSet."""
    JUN_CC_PV_QPLUSD_Z = ORCAKeyword("jun-cc-pv(q+d)z")
    """ORCAKeyword: BasisSet."""
    JUN_CC_PV_TPLUSD_Z = ORCAKeyword("jun-cc-pv(t+d)z")
    """ORCAKeyword: BasisSet."""
    LANL08 = ORCAKeyword("lanl08")
    """ORCAKeyword: BasisSet."""
    LANL08_F = ORCAKeyword("lanl08(f)")
    """ORCAKeyword: BasisSet."""
    LANL2DZ = ORCAKeyword("lanl2dz")
    """ORCAKeyword: BasisSet."""
    LANL2TZ = ORCAKeyword("lanl2tz")
    """ORCAKeyword: BasisSet."""
    LANL2TZ_F = ORCAKeyword("lanl2tz(f)")
    """ORCAKeyword: BasisSet."""
    M6_31G = ORCAKeyword("m6-31g")
    """ORCAKeyword: BasisSet."""
    M6_31GSTAR = ORCAKeyword("m6-31g*")
    """ORCAKeyword: BasisSet."""
    MA_DEF_TZVP = ORCAKeyword("ma-def-tzvp")
    """ORCAKeyword: BasisSet."""
    MA_DEF2_MSVP = ORCAKeyword("ma-def2-msvp")
    """ORCAKeyword: BasisSet."""
    MA_DEF2_QZVP = ORCAKeyword("ma-def2-qzvp")
    """ORCAKeyword: BasisSet."""
    MA_DEF2_QZVPP = ORCAKeyword("ma-def2-qzvpp")
    """ORCAKeyword: BasisSet."""
    MA_DEF2_SV_P = ORCAKeyword("ma-def2-sv(p)")
    """ORCAKeyword: BasisSet."""
    MA_DEF2_SVP = ORCAKeyword("ma-def2-svp")
    """ORCAKeyword: BasisSet."""
    MA_DEF2_TZVP = ORCAKeyword("ma-def2-tzvp")
    """ORCAKeyword: BasisSet."""
    MA_DEF2_TZVP_F = ORCAKeyword("ma-def2-tzvp(-f)")
    """ORCAKeyword: BasisSet."""
    MA_DEF2_TZVPP = ORCAKeyword("ma-def2-tzvpp")
    """ORCAKeyword: BasisSet."""
    MA_DKH_DEF2_QZVPP = ORCAKeyword("ma-dkh-def2-qzvpp")
    """ORCAKeyword: BasisSet."""
    MA_DKH_DEF2_SV_P = ORCAKeyword("ma-dkh-def2-sv(p)")
    """ORCAKeyword: BasisSet."""
    MA_DKH_DEF2_SVP = ORCAKeyword("ma-dkh-def2-svp")
    """ORCAKeyword: BasisSet."""
    MA_DKH_DEF2_TZVP = ORCAKeyword("ma-dkh-def2-tzvp")
    """ORCAKeyword: BasisSet."""
    MA_DKH_DEF2_TZVP_F = ORCAKeyword("ma-dkh-def2-tzvp(-f)")
    """ORCAKeyword: BasisSet."""
    MA_DKH_DEF2_TZVPP = ORCAKeyword("ma-dkh-def2-tzvpp")
    """ORCAKeyword: BasisSet."""
    MA_ZORA_DEF2_QZVPP = ORCAKeyword("ma-zora-def2-qzvpp")
    """ORCAKeyword: BasisSet."""
    MA_ZORA_DEF2_SV_P = ORCAKeyword("ma-zora-def2-sv(p)")
    """ORCAKeyword: BasisSet."""
    MA_ZORA_DEF2_SVP = ORCAKeyword("ma-zora-def2-svp")
    """ORCAKeyword: BasisSet."""
    MA_ZORA_DEF2_TZVP = ORCAKeyword("ma-zora-def2-tzvp")
    """ORCAKeyword: BasisSet."""
    MA_ZORA_DEF2_TZVP_F = ORCAKeyword("ma-zora-def2-tzvp(-f)")
    """ORCAKeyword: BasisSet."""
    MA_ZORA_DEF2_TZVPP = ORCAKeyword("ma-zora-def2-tzvpp")
    """ORCAKeyword: BasisSet."""
    MAUG_CC_PV_DPLUSD_Z = ORCAKeyword("maug-cc-pv(d+d)z")
    """ORCAKeyword: BasisSet."""
    MAUG_CC_PV_QPLUSD_Z = ORCAKeyword("maug-cc-pv(q+d)z")
    """ORCAKeyword: BasisSet."""
    MAUG_CC_PV_TPLUSD_Z = ORCAKeyword("maug-cc-pv(t+d)z")
    """ORCAKeyword: BasisSet."""
    MAY_CC_PV_QPLUSD_Z = ORCAKeyword("may-cc-pv(q+d)z")
    """ORCAKeyword: BasisSet."""
    MAY_CC_PV_TPLUSD_Z = ORCAKeyword("may-cc-pv(t+d)z")
    """ORCAKeyword: BasisSet."""
    MIDI = ORCAKeyword("midi")
    """ORCAKeyword: BasisSet."""
    MINAO = ORCAKeyword("minao")
    """ORCAKeyword: BasisSet."""
    MINAO_AUTO_PP = ORCAKeyword("minao-auto-pp")
    """ORCAKeyword: BasisSet."""
    MINI = ORCAKeyword("mini")
    """ORCAKeyword: BasisSet."""
    MINIS = ORCAKeyword("minis")
    """ORCAKeyword: BasisSet."""
    MINIX = ORCAKeyword("minix")
    """ORCAKeyword: BasisSet."""
    OLD_DKH_SV_P = ORCAKeyword("old-dkh-sv(p)")
    """ORCAKeyword: BasisSet."""
    OLD_DKH_SVP = ORCAKeyword("old-dkh-svp")
    """ORCAKeyword: BasisSet."""
    OLD_DKH_TZV_P = ORCAKeyword("old-dkh-tzv(p)")
    """ORCAKeyword: BasisSet."""
    OLD_DKH_TZVP = ORCAKeyword("old-dkh-tzvp")
    """ORCAKeyword: BasisSet."""
    OLD_DKH_TZVPP = ORCAKeyword("old-dkh-tzvpp")
    """ORCAKeyword: BasisSet."""
    OLD_SV = ORCAKeyword("old-sv")
    """ORCAKeyword: BasisSet."""
    OLD_SV_P = ORCAKeyword("old-sv(p)")
    """ORCAKeyword: BasisSet."""
    OLD_SVP = ORCAKeyword("old-svp")
    """ORCAKeyword: BasisSet."""
    OLD_TZV = ORCAKeyword("old-tzv")
    """ORCAKeyword: BasisSet."""
    OLD_TZV_P = ORCAKeyword("old-tzv(p)")
    """ORCAKeyword: BasisSet."""
    OLD_TZVP = ORCAKeyword("old-tzvp")
    """ORCAKeyword: BasisSet."""
    OLD_TZVPP = ORCAKeyword("old-tzvpp")
    """ORCAKeyword: BasisSet."""
    OLD_ZORA_SV_P = ORCAKeyword("old-zora-sv(p)")
    """ORCAKeyword: BasisSet."""
    OLD_ZORA_SVP = ORCAKeyword("old-zora-svp")
    """ORCAKeyword: BasisSet."""
    OLD_ZORA_TZV_P = ORCAKeyword("old-zora-tzv(p)")
    """ORCAKeyword: BasisSet."""
    OLD_ZORA_TZVP = ORCAKeyword("old-zora-tzvp")
    """ORCAKeyword: BasisSet."""
    OLD_ZORA_TZVPP = ORCAKeyword("old-zora-tzvpp")
    """ORCAKeyword: BasisSet."""
    PARTRIDGE_1 = ORCAKeyword("partridge-1")
    """ORCAKeyword: BasisSet."""
    PARTRIDGE_2 = ORCAKeyword("partridge-2")
    """ORCAKeyword: BasisSet."""
    PARTRIDGE_3 = ORCAKeyword("partridge-3")
    """ORCAKeyword: BasisSet."""
    PARTRIDGE_4 = ORCAKeyword("partridge-4")
    """ORCAKeyword: BasisSet."""
    PC_0 = ORCAKeyword("pc-0")
    """ORCAKeyword: BasisSet."""
    PC_1 = ORCAKeyword("pc-1")
    """ORCAKeyword: BasisSet."""
    PC_2 = ORCAKeyword("pc-2")
    """ORCAKeyword: BasisSet."""
    PC_3 = ORCAKeyword("pc-3")
    """ORCAKeyword: BasisSet."""
    PC_4 = ORCAKeyword("pc-4")
    """ORCAKeyword: BasisSet."""
    PCH_1 = ORCAKeyword("pch-1")
    """ORCAKeyword: BasisSet."""
    PCH_2 = ORCAKeyword("pch-2")
    """ORCAKeyword: BasisSet."""
    PCH_3 = ORCAKeyword("pch-3")
    """ORCAKeyword: BasisSet."""
    PCH_4 = ORCAKeyword("pch-4")
    """ORCAKeyword: BasisSet."""
    PCJ_0 = ORCAKeyword("pcj-0")
    """ORCAKeyword: BasisSet."""
    PCJ_1 = ORCAKeyword("pcj-1")
    """ORCAKeyword: BasisSet."""
    PCJ_2 = ORCAKeyword("pcj-2")
    """ORCAKeyword: BasisSet."""
    PCJ_3 = ORCAKeyword("pcj-3")
    """ORCAKeyword: BasisSet."""
    PCJ_4 = ORCAKeyword("pcj-4")
    """ORCAKeyword: BasisSet."""
    PCSEG_0 = ORCAKeyword("pcseg-0")
    """ORCAKeyword: BasisSet."""
    PCSEG_1 = ORCAKeyword("pcseg-1")
    """ORCAKeyword: BasisSet."""
    PCSEG_2 = ORCAKeyword("pcseg-2")
    """ORCAKeyword: BasisSet."""
    PCSEG_3 = ORCAKeyword("pcseg-3")
    """ORCAKeyword: BasisSet."""
    PCSEG_4 = ORCAKeyword("pcseg-4")
    """ORCAKeyword: BasisSet."""
    PCSSEG_0 = ORCAKeyword("pcsseg-0")
    """ORCAKeyword: BasisSet."""
    PCSSEG_1 = ORCAKeyword("pcsseg-1")
    """ORCAKeyword: BasisSet."""
    PCSSEG_2 = ORCAKeyword("pcsseg-2")
    """ORCAKeyword: BasisSet."""
    PCSSEG_3 = ORCAKeyword("pcsseg-3")
    """ORCAKeyword: BasisSet."""
    PCSSEG_4 = ORCAKeyword("pcsseg-4")
    """ORCAKeyword: BasisSet."""
    PCX_1 = ORCAKeyword("pcx-1")
    """ORCAKeyword: BasisSet."""
    PCX_2 = ORCAKeyword("pcx-2")
    """ORCAKeyword: BasisSet."""
    PCX_3 = ORCAKeyword("pcx-3")
    """ORCAKeyword: BasisSet."""
    PCX_4 = ORCAKeyword("pcx-4")
    """ORCAKeyword: BasisSet."""
    QZVP = ORCAKeyword("qzvp")
    """ORCAKeyword: BasisSet."""
    QZVPP = ORCAKeyword("qzvpp")
    """ORCAKeyword: BasisSet."""
    SAPPORO_DKH3_DZP_2012 = ORCAKeyword("sapporo-dkh3-dzp-2012")
    """ORCAKeyword: BasisSet."""
    SAPPORO_DKH3_QZP_2012 = ORCAKeyword("sapporo-dkh3-qzp-2012")
    """ORCAKeyword: BasisSet."""
    SAPPORO_DKH3_TZP_2012 = ORCAKeyword("sapporo-dkh3-tzp-2012")
    """ORCAKeyword: BasisSet."""
    SAPPORO_DZP_2012 = ORCAKeyword("sapporo-dzp-2012")
    """ORCAKeyword: BasisSet."""
    SAPPORO_QZP_2012 = ORCAKeyword("sapporo-qzp-2012")
    """ORCAKeyword: BasisSet."""
    SAPPORO_TZP_2012 = ORCAKeyword("sapporo-tzp-2012")
    """ORCAKeyword: BasisSet."""
    SARC_DKH_SVP = ORCAKeyword("sarc-dkh-svp")
    """ORCAKeyword: BasisSet."""
    SARC_DKH_TZVP = ORCAKeyword("sarc-dkh-tzvp")
    """ORCAKeyword: BasisSet."""
    SARC_DKH_TZVPP = ORCAKeyword("sarc-dkh-tzvpp")
    """ORCAKeyword: BasisSet."""
    SARC_ZORA_SVP = ORCAKeyword("sarc-zora-svp")
    """ORCAKeyword: BasisSet."""
    SARC_ZORA_TZVP = ORCAKeyword("sarc-zora-tzvp")
    """ORCAKeyword: BasisSet."""
    SARC_ZORA_TZVPP = ORCAKeyword("sarc-zora-tzvpp")
    """ORCAKeyword: BasisSet."""
    SARC2_DKH_QZV = ORCAKeyword("sarc2-dkh-qzv")
    """ORCAKeyword: BasisSet."""
    SARC2_DKH_QZVP = ORCAKeyword("sarc2-dkh-qzvp")
    """ORCAKeyword: BasisSet."""
    SARC2_ZORA_QZV = ORCAKeyword("sarc2-zora-qzv")
    """ORCAKeyword: BasisSet."""
    SARC2_ZORA_QZVP = ORCAKeyword("sarc2-zora-qzvp")
    """ORCAKeyword: BasisSet."""
    SAUG_ANO_PV5Z = ORCAKeyword("saug-ano-pv5z")
    """ORCAKeyword: BasisSet."""
    SAUG_ANO_PVDZ = ORCAKeyword("saug-ano-pvdz")
    """ORCAKeyword: BasisSet."""
    SAUG_ANO_PVQZ = ORCAKeyword("saug-ano-pvqz")
    """ORCAKeyword: BasisSet."""
    SAUG_ANO_PVTZ = ORCAKeyword("saug-ano-pvtz")
    """ORCAKeyword: BasisSet."""
    STO_3G = ORCAKeyword("sto-3g")
    """ORCAKeyword: BasisSet."""
    SV = ORCAKeyword("sv")
    """ORCAKeyword: BasisSet."""
    SV_P = ORCAKeyword("sv(p)")
    """ORCAKeyword: BasisSet."""
    SVP = ORCAKeyword("svp")
    """ORCAKeyword: BasisSet."""
    TZV = ORCAKeyword("tzv")
    """ORCAKeyword: BasisSet."""
    TZV_P = ORCAKeyword("tzv(p)")
    """ORCAKeyword: BasisSet."""
    TZVP = ORCAKeyword("tzvp")
    """ORCAKeyword: BasisSet."""
    TZVPP = ORCAKeyword("tzvpp")
    """ORCAKeyword: BasisSet."""
    UGBS = ORCAKeyword("ugbs")
    """ORCAKeyword: BasisSet."""
    VDZP = ORCAKeyword("vdzp")
    """ORCAKeyword: BasisSet."""
    W1_DZ = ORCAKeyword("w1-dz")
    """ORCAKeyword: BasisSet."""
    W1_MTSMALL = ORCAKeyword("w1-mtsmall")
    """ORCAKeyword: BasisSet."""
    W1_OPT = ORCAKeyword("w1-opt")
    """ORCAKeyword: BasisSet."""
    W1_QZ = ORCAKeyword("w1-qz")
    """ORCAKeyword: BasisSet."""
    W1_TZ = ORCAKeyword("w1-tz")
    """ORCAKeyword: BasisSet."""
    WACHTERSPLUSF = ORCAKeyword("wachters+f")
    """ORCAKeyword: BasisSet."""
    X2C_QZVPALL = ORCAKeyword("x2c-qzvpall")
    """ORCAKeyword: BasisSet."""
    X2C_QZVPALL_2C = ORCAKeyword("x2c-qzvpall-2c")
    """ORCAKeyword: BasisSet."""
    X2C_QZVPALL_2C_S = ORCAKeyword("x2c-qzvpall-2c-s")
    """ORCAKeyword: BasisSet."""
    X2C_QZVPALL_S = ORCAKeyword("x2c-qzvpall-s")
    """ORCAKeyword: BasisSet."""
    X2C_QZVPPALL = ORCAKeyword("x2c-qzvppall")
    """ORCAKeyword: BasisSet."""
    X2C_QZVPPALL_2C = ORCAKeyword("x2c-qzvppall-2c")
    """ORCAKeyword: BasisSet."""
    X2C_QZVPPALL_2C_S = ORCAKeyword("x2c-qzvppall-2c-s")
    """ORCAKeyword: BasisSet."""
    X2C_QZVPPALL_S = ORCAKeyword("x2c-qzvppall-s")
    """ORCAKeyword: BasisSet."""
    X2C_SV_P_ALL = ORCAKeyword("x2c-sv(p)all")
    """ORCAKeyword: BasisSet."""
    X2C_SV_P_ALL_2C = ORCAKeyword("x2c-sv(p)all-2c")
    """ORCAKeyword: BasisSet."""
    X2C_SV_P_ALL_S = ORCAKeyword("x2c-sv(p)all-s")
    """ORCAKeyword: BasisSet."""
    X2C_SVPALL = ORCAKeyword("x2c-svpall")
    """ORCAKeyword: BasisSet."""
    X2C_SVPALL_2C = ORCAKeyword("x2c-svpall-2c")
    """ORCAKeyword: BasisSet."""
    X2C_SVPALL_S = ORCAKeyword("x2c-svpall-s")
    """ORCAKeyword: BasisSet."""
    X2C_TZVPALL = ORCAKeyword("x2c-tzvpall")
    """ORCAKeyword: BasisSet."""
    X2C_TZVPALL_2C = ORCAKeyword("x2c-tzvpall-2c")
    """ORCAKeyword: BasisSet."""
    X2C_TZVPALL_S = ORCAKeyword("x2c-tzvpall-s")
    """ORCAKeyword: BasisSet."""
    X2C_TZVPPALL = ORCAKeyword("x2c-tzvppall")
    """ORCAKeyword: BasisSet."""
    X2C_TZVPPALL_2C = ORCAKeyword("x2c-tzvppall-2c")
    """ORCAKeyword: BasisSet."""
    X2C_TZVPPALL_S = ORCAKeyword("x2c-tzvppall-s")
    """ORCAKeyword: BasisSet."""
    ZORA_DEF2_QZVPP = ORCAKeyword("zora-def2-qzvpp")
    """ORCAKeyword: BasisSet."""
    ZORA_DEF2_SV_P = ORCAKeyword("zora-def2-sv(p)")
    """ORCAKeyword: BasisSet."""
    ZORA_DEF2_SVP = ORCAKeyword("zora-def2-svp")
    """ORCAKeyword: BasisSet."""
    ZORA_DEF2_TZVP = ORCAKeyword("zora-def2-tzvp")
    """ORCAKeyword: BasisSet."""
    ZORA_DEF2_TZVP_F = ORCAKeyword("zora-def2-tzvp(-f)")
    """ORCAKeyword: BasisSet."""
    ZORA_DEF2_TZVPP = ORCAKeyword("zora-def2-tzvpp")
    """ORCAKeyword: BasisSet."""
    ZORA_MA_DEF2_QZVPP = ORCAKeyword("zora-ma-def2-qzvpp")
    """ORCAKeyword: BasisSet."""
    ZORA_MA_DEF2_SV_P = ORCAKeyword("zora-ma-def2-sv(p)")
    """ORCAKeyword: BasisSet."""
    ZORA_MA_DEF2_SVP = ORCAKeyword("zora-ma-def2-svp")
    """ORCAKeyword: BasisSet."""
    ZORA_MA_DEF2_TZVP = ORCAKeyword("zora-ma-def2-tzvp")
    """ORCAKeyword: BasisSet."""
    ZORA_MA_DEF2_TZVP_F = ORCAKeyword("zora-ma-def2-tzvp(-f)")
    """ORCAKeyword: BasisSet."""
    ZORA_MA_DEF2_TZVPP = ORCAKeyword("zora-ma-def2-tzvpp")
    """ORCAKeyword: BasisSet."""
    ZORA_QZVP = ORCAKeyword("zora-qzvp")
    """ORCAKeyword: BasisSet."""
    ZORA_QZVPP = ORCAKeyword("zora-qzvpp")
    """ORCAKeyword: BasisSet."""
    ZORA_SV_P = ORCAKeyword("zora-sv(p)")
    """ORCAKeyword: BasisSet."""
    ZORA_SVP = ORCAKeyword("zora-svp")
    """ORCAKeyword: BasisSet."""
    ZORA_TZV_P = ORCAKeyword("zora-tzv(p)")
    """ORCAKeyword: BasisSet."""
    ZORA_TZVP = ORCAKeyword("zora-tzvp")
    """ORCAKeyword: BasisSet."""
    ZORA_TZVPP = ORCAKeyword("zora-tzvpp")
    """ORCAKeyword: BasisSet."""
