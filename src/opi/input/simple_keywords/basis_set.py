from opi.input.simple_keywords.base import (
    SimpleKeyword,
    SimpleKeywordBox,
)

__all__ = ("BasisSet",)


class BasisSet(SimpleKeywordBox):
    """Enum to store all simple keywords of type BasisSet."""

    G3_21G = SimpleKeyword("3-21g")
    """SimpleKeyword: BasisSet."""
    G3_21GSP = SimpleKeyword("3-21gsp")
    """SimpleKeyword: BasisSet."""
    G4_22GSP = SimpleKeyword("4-22gsp")
    """SimpleKeyword: BasisSet."""
    G6_31PLUSPLUSG_2D_2P = SimpleKeyword("6-31++g(2d,2p)")
    """SimpleKeyword: BasisSet."""
    G6_31PLUSPLUSG_2D_P = SimpleKeyword("6-31++g(2d,p)")
    """SimpleKeyword: BasisSet."""
    G6_31PLUSPLUSG_2DF_2P = SimpleKeyword("6-31++g(2df,2p)")
    """SimpleKeyword: BasisSet."""
    G6_31PLUSPLUSG_2DF_2PD = SimpleKeyword("6-31++g(2df,2pd)")
    """SimpleKeyword: BasisSet."""
    G6_31PLUSPLUSG_D_P = SimpleKeyword("6-31++g(d,p)")
    """SimpleKeyword: BasisSet."""
    G6_31PLUSPLUSGSTARSTAR = SimpleKeyword("6-31++g**")
    """SimpleKeyword: BasisSet."""
    G6_31PLUSG_2D_2P = SimpleKeyword("6-31+g(2d,2p)")
    """SimpleKeyword: BasisSet."""
    G6_31PLUSG_2D_P = SimpleKeyword("6-31+g(2d,p)")
    """SimpleKeyword: BasisSet."""
    G6_31PLUSG_2D = SimpleKeyword("6-31+g(2d)")
    """SimpleKeyword: BasisSet."""
    G6_31PLUSG_2DF_2P = SimpleKeyword("6-31+g(2df,2p)")
    """SimpleKeyword: BasisSet."""
    G6_31PLUSG_2DF_2PD = SimpleKeyword("6-31+g(2df,2pd)")
    """SimpleKeyword: BasisSet."""
    G6_31PLUSG_2DF = SimpleKeyword("6-31+g(2df)")
    """SimpleKeyword: BasisSet."""
    G6_31PLUSG_D_P = SimpleKeyword("6-31+g(d,p)")
    """SimpleKeyword: BasisSet."""
    G6_31PLUSG_D = SimpleKeyword("6-31+g(d)")
    """SimpleKeyword: BasisSet."""
    G6_31PLUSGSTAR = SimpleKeyword("6-31+g*")
    """SimpleKeyword: BasisSet."""
    G6_31PLUSGSTARSTAR = SimpleKeyword("6-31+g**")
    """SimpleKeyword: BasisSet."""
    G6_311PLUSPLUSG_2D_2P = SimpleKeyword("6-311++g(2d,2p)")
    """SimpleKeyword: BasisSet."""
    G6_311PLUSPLUSG_2D_P = SimpleKeyword("6-311++g(2d,p)")
    """SimpleKeyword: BasisSet."""
    G6_311PLUSPLUSG_2DF_2P = SimpleKeyword("6-311++g(2df,2p)")
    """SimpleKeyword: BasisSet."""
    G6_311PLUSPLUSG_2DF_2PD = SimpleKeyword("6-311++g(2df,2pd)")
    """SimpleKeyword: BasisSet."""
    G6_311PLUSPLUSG_3DF_3PD = SimpleKeyword("6-311++g(3df,3pd)")
    """SimpleKeyword: BasisSet."""
    G6_311PLUSPLUSG_D_P = SimpleKeyword("6-311++g(d,p)")
    """SimpleKeyword: BasisSet."""
    G6_311PLUSPLUSGSTARSTAR = SimpleKeyword("6-311++g**")
    """SimpleKeyword: BasisSet."""
    G6_311PLUSG_2D_2P = SimpleKeyword("6-311+g(2d,2p)")
    """SimpleKeyword: BasisSet."""
    G6_311PLUSG_2D_P = SimpleKeyword("6-311+g(2d,p)")
    """SimpleKeyword: BasisSet."""
    G6_311PLUSG_2D = SimpleKeyword("6-311+g(2d)")
    """SimpleKeyword: BasisSet."""
    G6_311PLUSG_2DF_2P = SimpleKeyword("6-311+g(2df,2p)")
    """SimpleKeyword: BasisSet."""
    G6_311PLUSG_2DF_2PD = SimpleKeyword("6-311+g(2df,2pd)")
    """SimpleKeyword: BasisSet."""
    G6_311PLUSG_2DF = SimpleKeyword("6-311+g(2df)")
    """SimpleKeyword: BasisSet."""
    G6_311PLUSG_3DF_2P = SimpleKeyword("6-311+g(3df,2p)")
    """SimpleKeyword: BasisSet."""
    G6_311PLUSG_3DF_3PD = SimpleKeyword("6-311+g(3df,3pd)")
    """SimpleKeyword: BasisSet."""
    G6_311PLUSG_3DF = SimpleKeyword("6-311+g(3df)")
    """SimpleKeyword: BasisSet."""
    G6_311PLUSG_D_P = SimpleKeyword("6-311+g(d,p)")
    """SimpleKeyword: BasisSet."""
    G6_311PLUSG_D = SimpleKeyword("6-311+g(d)")
    """SimpleKeyword: BasisSet."""
    G6_311PLUSGSTAR = SimpleKeyword("6-311+g*")
    """SimpleKeyword: BasisSet."""
    G6_311PLUSGSTARSTAR = SimpleKeyword("6-311+g**")
    """SimpleKeyword: BasisSet."""
    G6_311G = SimpleKeyword("6-311g")
    """SimpleKeyword: BasisSet."""
    G6_311G_2D_2P = SimpleKeyword("6-311g(2d,2p)")
    """SimpleKeyword: BasisSet."""
    G6_311G_2D_P = SimpleKeyword("6-311g(2d,p)")
    """SimpleKeyword: BasisSet."""
    G6_311G_2D = SimpleKeyword("6-311g(2d)")
    """SimpleKeyword: BasisSet."""
    G6_311G_2DF_2P = SimpleKeyword("6-311g(2df,2p)")
    """SimpleKeyword: BasisSet."""
    G6_311G_2DF_2PD = SimpleKeyword("6-311g(2df,2pd)")
    """SimpleKeyword: BasisSet."""
    G6_311G_2DF = SimpleKeyword("6-311g(2df)")
    """SimpleKeyword: BasisSet."""
    G6_311G_3DF_3PD = SimpleKeyword("6-311g(3df,3pd)")
    """SimpleKeyword: BasisSet."""
    G6_311G_3DF = SimpleKeyword("6-311g(3df)")
    """SimpleKeyword: BasisSet."""
    G6_311G_D_P = SimpleKeyword("6-311g(d,p)")
    """SimpleKeyword: BasisSet."""
    G6_311G_D = SimpleKeyword("6-311g(d)")
    """SimpleKeyword: BasisSet."""
    G6_311GSTAR = SimpleKeyword("6-311g*")
    """SimpleKeyword: BasisSet."""
    G6_311GSTARSTAR = SimpleKeyword("6-311g**")
    """SimpleKeyword: BasisSet."""
    G6_31G = SimpleKeyword("6-31g")
    """SimpleKeyword: BasisSet."""
    G6_31G_2D_2P = SimpleKeyword("6-31g(2d,2p)")
    """SimpleKeyword: BasisSet."""
    G6_31G_2D_P = SimpleKeyword("6-31g(2d,p)")
    """SimpleKeyword: BasisSet."""
    G6_31G_2D = SimpleKeyword("6-31g(2d)")
    """SimpleKeyword: BasisSet."""
    G6_31G_2DF_2P = SimpleKeyword("6-31g(2df,2p)")
    """SimpleKeyword: BasisSet."""
    G6_31G_2DF_2PD = SimpleKeyword("6-31g(2df,2pd)")
    """SimpleKeyword: BasisSet."""
    G6_31G_2DF = SimpleKeyword("6-31g(2df)")
    """SimpleKeyword: BasisSet."""
    G6_31G_D_P = SimpleKeyword("6-31g(d,p)")
    """SimpleKeyword: BasisSet."""
    G6_31G_D = SimpleKeyword("6-31g(d)")
    """SimpleKeyword: BasisSet."""
    G6_31GSTAR = SimpleKeyword("6-31g*")
    """SimpleKeyword: BasisSet."""
    G6_31GSTARSTAR = SimpleKeyword("6-31g**")
    """SimpleKeyword: BasisSet."""
    AHGBS_5 = SimpleKeyword("ahgbs-5")
    """SimpleKeyword: BasisSet."""
    AHGBS_7 = SimpleKeyword("ahgbs-7")
    """SimpleKeyword: BasisSet."""
    AHGBS_9 = SimpleKeyword("ahgbs-9")
    """SimpleKeyword: BasisSet."""
    AHGBSP1_5 = SimpleKeyword("ahgbsp1-5")
    """SimpleKeyword: BasisSet."""
    AHGBSP1_7 = SimpleKeyword("ahgbsp1-7")
    """SimpleKeyword: BasisSet."""
    AHGBSP1_9 = SimpleKeyword("ahgbsp1-9")
    """SimpleKeyword: BasisSet."""
    AHGBSP2_5 = SimpleKeyword("ahgbsp2-5")
    """SimpleKeyword: BasisSet."""
    AHGBSP2_7 = SimpleKeyword("ahgbsp2-7")
    """SimpleKeyword: BasisSet."""
    AHGBSP2_9 = SimpleKeyword("ahgbsp2-9")
    """SimpleKeyword: BasisSet."""
    AHGBSP3_5 = SimpleKeyword("ahgbsp3-5")
    """SimpleKeyword: BasisSet."""
    AHGBSP3_7 = SimpleKeyword("ahgbsp3-7")
    """SimpleKeyword: BasisSet."""
    AHGBSP3_9 = SimpleKeyword("ahgbsp3-9")
    """SimpleKeyword: BasisSet."""
    ANO_PC_0 = SimpleKeyword("ano-pc-0")
    """SimpleKeyword: BasisSet."""
    ANO_PC_0_POL = SimpleKeyword("ano-pc-0-pol")
    """SimpleKeyword: BasisSet."""
    ANO_PV5Z = SimpleKeyword("ano-pv5z")
    """SimpleKeyword: BasisSet."""
    ANO_PV6Z = SimpleKeyword("ano-pv6z")
    """SimpleKeyword: BasisSet."""
    ANO_PVDZ = SimpleKeyword("ano-pvdz")
    """SimpleKeyword: BasisSet."""
    ANO_PVQZ = SimpleKeyword("ano-pvqz")
    """SimpleKeyword: BasisSet."""
    ANO_PVTZ = SimpleKeyword("ano-pvtz")
    """SimpleKeyword: BasisSet."""
    ANO_RCC_DZP = SimpleKeyword("ano-rcc-dzp")
    """SimpleKeyword: BasisSet."""
    ANO_RCC_FULL = SimpleKeyword("ano-rcc-full")
    """SimpleKeyword: BasisSet."""
    ANO_RCC_MB = SimpleKeyword("ano-rcc-mb")
    """SimpleKeyword: BasisSet."""
    ANO_RCC_QZP = SimpleKeyword("ano-rcc-qzp")
    """SimpleKeyword: BasisSet."""
    ANO_RCC_TZP = SimpleKeyword("ano-rcc-tzp")
    """SimpleKeyword: BasisSet."""
    ANO_SZ = SimpleKeyword("ano-sz")
    """SimpleKeyword: BasisSet."""
    ANO_SZ_DKH_SMALL = SimpleKeyword("ano-sz-dkh-small")
    """SimpleKeyword: BasisSet."""
    APR_CC_PV_QPLUSD_Z = SimpleKeyword("apr-cc-pv(q+d)z")
    """SimpleKeyword: BasisSet."""
    AUG_ANO_PV5Z = SimpleKeyword("aug-ano-pv5z")
    """SimpleKeyword: BasisSet."""
    AUG_ANO_PVDZ = SimpleKeyword("aug-ano-pvdz")
    """SimpleKeyword: BasisSet."""
    AUG_ANO_PVQZ = SimpleKeyword("aug-ano-pvqz")
    """SimpleKeyword: BasisSet."""
    AUG_ANO_PVTZ = SimpleKeyword("aug-ano-pvtz")
    """SimpleKeyword: BasisSet."""
    AUG_CC_PCV5Z = SimpleKeyword("aug-cc-pcv5z")
    """SimpleKeyword: BasisSet."""
    AUG_CC_PCV5Z_PP = SimpleKeyword("aug-cc-pcv5z-pp")
    """SimpleKeyword: BasisSet."""
    AUG_CC_PCV6Z = SimpleKeyword("aug-cc-pcv6z")
    """SimpleKeyword: BasisSet."""
    AUG_CC_PCVDZ = SimpleKeyword("aug-cc-pcvdz")
    """SimpleKeyword: BasisSet."""
    AUG_CC_PCVDZ_PP = SimpleKeyword("aug-cc-pcvdz-pp")
    """SimpleKeyword: BasisSet."""
    AUG_CC_PCVQZ = SimpleKeyword("aug-cc-pcvqz")
    """SimpleKeyword: BasisSet."""
    AUG_CC_PCVQZ_PP = SimpleKeyword("aug-cc-pcvqz-pp")
    """SimpleKeyword: BasisSet."""
    AUG_CC_PCVTZ = SimpleKeyword("aug-cc-pcvtz")
    """SimpleKeyword: BasisSet."""
    AUG_CC_PCVTZ_PP = SimpleKeyword("aug-cc-pcvtz-pp")
    """SimpleKeyword: BasisSet."""
    AUG_CC_PV5_PLUSD_Z = SimpleKeyword("aug-cc-pv5(+d)z")
    """SimpleKeyword: BasisSet."""
    AUG_CC_PV5Z = SimpleKeyword("aug-cc-pv5z")
    """SimpleKeyword: BasisSet."""
    AUG_CC_PV5Z_DK = SimpleKeyword("aug-cc-pv5z-dk")
    """SimpleKeyword: BasisSet."""
    AUG_CC_PV5Z_PP = SimpleKeyword("aug-cc-pv5z-pp")
    """SimpleKeyword: BasisSet."""
    AUG_CC_PV5Z_PP_OPTRI = SimpleKeyword("aug-cc-pv5z-pp-optri")
    """SimpleKeyword: BasisSet."""
    AUG_CC_PV6_PLUSD_Z = SimpleKeyword("aug-cc-pv6(+d)z")
    """SimpleKeyword: BasisSet."""
    AUG_CC_PV6Z = SimpleKeyword("aug-cc-pv6z")
    """SimpleKeyword: BasisSet."""
    AUG_CC_PV7Z = SimpleKeyword("aug-cc-pv7z")
    """SimpleKeyword: BasisSet."""
    AUG_CC_PVD_PLUSD_Z = SimpleKeyword("aug-cc-pvd(+d)z")
    """SimpleKeyword: BasisSet."""
    AUG_CC_PVDZ = SimpleKeyword("aug-cc-pvdz")
    """SimpleKeyword: BasisSet."""
    AUG_CC_PVDZ_DK = SimpleKeyword("aug-cc-pvdz-dk")
    """SimpleKeyword: BasisSet."""
    AUG_CC_PVDZ_PP = SimpleKeyword("aug-cc-pvdz-pp")
    """SimpleKeyword: BasisSet."""
    AUG_CC_PVDZ_PP_OPTRI = SimpleKeyword("aug-cc-pvdz-pp-optri")
    """SimpleKeyword: BasisSet."""
    AUG_CC_PVQ_PLUSD_Z = SimpleKeyword("aug-cc-pvq(+d)z")
    """SimpleKeyword: BasisSet."""
    AUG_CC_PVQZ = SimpleKeyword("aug-cc-pvqz")
    """SimpleKeyword: BasisSet."""
    AUG_CC_PVQZ_DK = SimpleKeyword("aug-cc-pvqz-dk")
    """SimpleKeyword: BasisSet."""
    AUG_CC_PVQZ_PP = SimpleKeyword("aug-cc-pvqz-pp")
    """SimpleKeyword: BasisSet."""
    AUG_CC_PVQZ_PP_OPTRI = SimpleKeyword("aug-cc-pvqz-pp-optri")
    """SimpleKeyword: BasisSet."""
    AUG_CC_PVT_PLUSD_Z = SimpleKeyword("aug-cc-pvt(+d)z")
    """SimpleKeyword: BasisSet."""
    AUG_CC_PVTZ = SimpleKeyword("aug-cc-pvtz")
    """SimpleKeyword: BasisSet."""
    AUG_CC_PVTZ_DK = SimpleKeyword("aug-cc-pvtz-dk")
    """SimpleKeyword: BasisSet."""
    AUG_CC_PVTZ_J = SimpleKeyword("aug-cc-pvtz-j")
    """SimpleKeyword: BasisSet."""
    AUG_CC_PVTZ_PP = SimpleKeyword("aug-cc-pvtz-pp")
    """SimpleKeyword: BasisSet."""
    AUG_CC_PVTZ_PP_OPTRI = SimpleKeyword("aug-cc-pvtz-pp-optri")
    """SimpleKeyword: BasisSet."""
    AUG_CC_PWCV5Z = SimpleKeyword("aug-cc-pwcv5z")
    """SimpleKeyword: BasisSet."""
    AUG_CC_PWCV5Z_DK = SimpleKeyword("aug-cc-pwcv5z-dk")
    """SimpleKeyword: BasisSet."""
    AUG_CC_PWCV5Z_PP = SimpleKeyword("aug-cc-pwcv5z-pp")
    """SimpleKeyword: BasisSet."""
    AUG_CC_PWCV5Z_PP_OPTRI = SimpleKeyword("aug-cc-pwcv5z-pp-optri")
    """SimpleKeyword: BasisSet."""
    AUG_CC_PWCVDZ = SimpleKeyword("aug-cc-pwcvdz")
    """SimpleKeyword: BasisSet."""
    AUG_CC_PWCVDZ_DK = SimpleKeyword("aug-cc-pwcvdz-dk")
    """SimpleKeyword: BasisSet."""
    AUG_CC_PWCVDZ_PP = SimpleKeyword("aug-cc-pwcvdz-pp")
    """SimpleKeyword: BasisSet."""
    AUG_CC_PWCVDZ_PP_OPTRI = SimpleKeyword("aug-cc-pwcvdz-pp-optri")
    """SimpleKeyword: BasisSet."""
    AUG_CC_PWCVQZ = SimpleKeyword("aug-cc-pwcvqz")
    """SimpleKeyword: BasisSet."""
    AUG_CC_PWCVQZ_DK = SimpleKeyword("aug-cc-pwcvqz-dk")
    """SimpleKeyword: BasisSet."""
    AUG_CC_PWCVQZ_PP = SimpleKeyword("aug-cc-pwcvqz-pp")
    """SimpleKeyword: BasisSet."""
    AUG_CC_PWCVQZ_PP_OPTRI = SimpleKeyword("aug-cc-pwcvqz-pp-optri")
    """SimpleKeyword: BasisSet."""
    AUG_CC_PWCVTZ = SimpleKeyword("aug-cc-pwcvtz")
    """SimpleKeyword: BasisSet."""
    AUG_CC_PWCVTZ_DK = SimpleKeyword("aug-cc-pwcvtz-dk")
    """SimpleKeyword: BasisSet."""
    AUG_CC_PWCVTZ_PP = SimpleKeyword("aug-cc-pwcvtz-pp")
    """SimpleKeyword: BasisSet."""
    AUG_CC_PWCVTZ_PP_OPTRI = SimpleKeyword("aug-cc-pwcvtz-pp-optri")
    """SimpleKeyword: BasisSet."""
    AUG_PC_0 = SimpleKeyword("aug-pc-0")
    """SimpleKeyword: BasisSet."""
    AUG_PC_1 = SimpleKeyword("aug-pc-1")
    """SimpleKeyword: BasisSet."""
    AUG_PC_2 = SimpleKeyword("aug-pc-2")
    """SimpleKeyword: BasisSet."""
    AUG_PC_3 = SimpleKeyword("aug-pc-3")
    """SimpleKeyword: BasisSet."""
    AUG_PC_4 = SimpleKeyword("aug-pc-4")
    """SimpleKeyword: BasisSet."""
    AUG_PCH_1 = SimpleKeyword("aug-pch-1")
    """SimpleKeyword: BasisSet."""
    AUG_PCH_2 = SimpleKeyword("aug-pch-2")
    """SimpleKeyword: BasisSet."""
    AUG_PCH_3 = SimpleKeyword("aug-pch-3")
    """SimpleKeyword: BasisSet."""
    AUG_PCH_4 = SimpleKeyword("aug-pch-4")
    """SimpleKeyword: BasisSet."""
    AUG_PCJ_0 = SimpleKeyword("aug-pcj-0")
    """SimpleKeyword: BasisSet."""
    AUG_PCJ_1 = SimpleKeyword("aug-pcj-1")
    """SimpleKeyword: BasisSet."""
    AUG_PCJ_2 = SimpleKeyword("aug-pcj-2")
    """SimpleKeyword: BasisSet."""
    AUG_PCJ_3 = SimpleKeyword("aug-pcj-3")
    """SimpleKeyword: BasisSet."""
    AUG_PCJ_4 = SimpleKeyword("aug-pcj-4")
    """SimpleKeyword: BasisSet."""
    AUG_PCSEG_0 = SimpleKeyword("aug-pcseg-0")
    """SimpleKeyword: BasisSet."""
    AUG_PCSEG_1 = SimpleKeyword("aug-pcseg-1")
    """SimpleKeyword: BasisSet."""
    AUG_PCSEG_2 = SimpleKeyword("aug-pcseg-2")
    """SimpleKeyword: BasisSet."""
    AUG_PCSEG_3 = SimpleKeyword("aug-pcseg-3")
    """SimpleKeyword: BasisSet."""
    AUG_PCSEG_4 = SimpleKeyword("aug-pcseg-4")
    """SimpleKeyword: BasisSet."""
    AUG_PCSSEG_0 = SimpleKeyword("aug-pcsseg-0")
    """SimpleKeyword: BasisSet."""
    AUG_PCSSEG_1 = SimpleKeyword("aug-pcsseg-1")
    """SimpleKeyword: BasisSet."""
    AUG_PCSSEG_2 = SimpleKeyword("aug-pcsseg-2")
    """SimpleKeyword: BasisSet."""
    AUG_PCSSEG_3 = SimpleKeyword("aug-pcsseg-3")
    """SimpleKeyword: BasisSet."""
    AUG_PCSSEG_4 = SimpleKeyword("aug-pcsseg-4")
    """SimpleKeyword: BasisSet."""
    AUG_PCX_1 = SimpleKeyword("aug-pcx-1")
    """SimpleKeyword: BasisSet."""
    AUG_PCX_2 = SimpleKeyword("aug-pcx-2")
    """SimpleKeyword: BasisSet."""
    AUG_PCX_3 = SimpleKeyword("aug-pcx-3")
    """SimpleKeyword: BasisSet."""
    AUG_PCX_4 = SimpleKeyword("aug-pcx-4")
    """SimpleKeyword: BasisSet."""
    CC_PCV5Z = SimpleKeyword("cc-pcv5z")
    """SimpleKeyword: BasisSet."""
    CC_PCV5Z_PP = SimpleKeyword("cc-pcv5z-pp")
    """SimpleKeyword: BasisSet."""
    CC_PCV6Z = SimpleKeyword("cc-pcv6z")
    """SimpleKeyword: BasisSet."""
    CC_PCVDZ = SimpleKeyword("cc-pcvdz")
    """SimpleKeyword: BasisSet."""
    CC_PCVDZ_F12 = SimpleKeyword("cc-pcvdz-f12")
    """SimpleKeyword: BasisSet."""
    CC_PCVDZ_F12_OPTRI = SimpleKeyword("cc-pcvdz-f12-optri")
    """SimpleKeyword: BasisSet."""
    CC_PCVDZ_PP = SimpleKeyword("cc-pcvdz-pp")
    """SimpleKeyword: BasisSet."""
    CC_PCVQZ = SimpleKeyword("cc-pcvqz")
    """SimpleKeyword: BasisSet."""
    CC_PCVQZ_F12 = SimpleKeyword("cc-pcvqz-f12")
    """SimpleKeyword: BasisSet."""
    CC_PCVQZ_F12_OPTRI = SimpleKeyword("cc-pcvqz-f12-optri")
    """SimpleKeyword: BasisSet."""
    CC_PCVQZ_PP = SimpleKeyword("cc-pcvqz-pp")
    """SimpleKeyword: BasisSet."""
    CC_PCVTZ = SimpleKeyword("cc-pcvtz")
    """SimpleKeyword: BasisSet."""
    CC_PCVTZ_F12 = SimpleKeyword("cc-pcvtz-f12")
    """SimpleKeyword: BasisSet."""
    CC_PCVTZ_F12_OPTRI = SimpleKeyword("cc-pcvtz-f12-optri")
    """SimpleKeyword: BasisSet."""
    CC_PCVTZ_PP = SimpleKeyword("cc-pcvtz-pp")
    """SimpleKeyword: BasisSet."""
    CC_PV5_PLUSD_Z = SimpleKeyword("cc-pv5(+d)z")
    """SimpleKeyword: BasisSet."""
    CC_PV5Z = SimpleKeyword("cc-pv5z")
    """SimpleKeyword: BasisSet."""
    CC_PV5Z_DK = SimpleKeyword("cc-pv5z-dk")
    """SimpleKeyword: BasisSet."""
    CC_PV5Z_PP = SimpleKeyword("cc-pv5z-pp")
    """SimpleKeyword: BasisSet."""
    CC_PV6Z = SimpleKeyword("cc-pv6z")
    """SimpleKeyword: BasisSet."""
    CC_PV7Z = SimpleKeyword("cc-pv7z")
    """SimpleKeyword: BasisSet."""
    CC_PV8Z = SimpleKeyword("cc-pv8z")
    """SimpleKeyword: BasisSet."""
    CC_PVD_PLUSD_Z = SimpleKeyword("cc-pvd(+d)z")
    """SimpleKeyword: BasisSet."""
    CC_PVDZ = SimpleKeyword("cc-pvdz")
    """SimpleKeyword: BasisSet."""
    CC_PVDZ_DK = SimpleKeyword("cc-pvdz-dk")
    """SimpleKeyword: BasisSet."""
    CC_PVDZ_DK3 = SimpleKeyword("cc-pvdz-dk3")
    """SimpleKeyword: BasisSet."""
    CC_PVDZ_F12 = SimpleKeyword("cc-pvdz-f12")
    """SimpleKeyword: BasisSet."""
    CC_PVDZ_F12_CABS = SimpleKeyword("cc-pvdz-f12-cabs")
    """SimpleKeyword: BasisSet."""
    CC_PVDZ_F12_OPTRI = SimpleKeyword("cc-pvdz-f12-optri")
    """SimpleKeyword: BasisSet."""
    CC_PVDZ_PP = SimpleKeyword("cc-pvdz-pp")
    """SimpleKeyword: BasisSet."""
    CC_PVDZ_PP_F12 = SimpleKeyword("cc-pvdz-pp-f12")
    """SimpleKeyword: BasisSet."""
    CC_PVDZ_PP_F12_OPTRI = SimpleKeyword("cc-pvdz-pp-f12-optri")
    """SimpleKeyword: BasisSet."""
    CC_PVQ_PLUSD_Z = SimpleKeyword("cc-pvq(+d)z")
    """SimpleKeyword: BasisSet."""
    CC_PVQZ = SimpleKeyword("cc-pvqz")
    """SimpleKeyword: BasisSet."""
    CC_PVQZ_DK = SimpleKeyword("cc-pvqz-dk")
    """SimpleKeyword: BasisSet."""
    CC_PVQZ_DK3 = SimpleKeyword("cc-pvqz-dk3")
    """SimpleKeyword: BasisSet."""
    CC_PVQZ_F12 = SimpleKeyword("cc-pvqz-f12")
    """SimpleKeyword: BasisSet."""
    CC_PVQZ_F12_CABS = SimpleKeyword("cc-pvqz-f12-cabs")
    """SimpleKeyword: BasisSet."""
    CC_PVQZ_F12_OPTRI = SimpleKeyword("cc-pvqz-f12-optri")
    """SimpleKeyword: BasisSet."""
    CC_PVQZ_PP = SimpleKeyword("cc-pvqz-pp")
    """SimpleKeyword: BasisSet."""
    CC_PVQZ_PP_F12 = SimpleKeyword("cc-pvqz-pp-f12")
    """SimpleKeyword: BasisSet."""
    CC_PVQZ_PP_F12_OPTRI = SimpleKeyword("cc-pvqz-pp-f12-optri")
    """SimpleKeyword: BasisSet."""
    CC_PVT_PLUSD_Z = SimpleKeyword("cc-pvt(+d)z")
    """SimpleKeyword: BasisSet."""
    CC_PVTZ = SimpleKeyword("cc-pvtz")
    """SimpleKeyword: BasisSet."""
    CC_PVTZ_DK = SimpleKeyword("cc-pvtz-dk")
    """SimpleKeyword: BasisSet."""
    CC_PVTZ_DK3 = SimpleKeyword("cc-pvtz-dk3")
    """SimpleKeyword: BasisSet."""
    CC_PVTZ_F12 = SimpleKeyword("cc-pvtz-f12")
    """SimpleKeyword: BasisSet."""
    CC_PVTZ_F12_CABS = SimpleKeyword("cc-pvtz-f12-cabs")
    """SimpleKeyword: BasisSet."""
    CC_PVTZ_F12_OPTRI = SimpleKeyword("cc-pvtz-f12-optri")
    """SimpleKeyword: BasisSet."""
    CC_PVTZ_PP = SimpleKeyword("cc-pvtz-pp")
    """SimpleKeyword: BasisSet."""
    CC_PVTZ_PP_F12 = SimpleKeyword("cc-pvtz-pp-f12")
    """SimpleKeyword: BasisSet."""
    CC_PVTZ_PP_F12_OPTRI = SimpleKeyword("cc-pvtz-pp-f12-optri")
    """SimpleKeyword: BasisSet."""
    CC_PWCV5Z = SimpleKeyword("cc-pwcv5z")
    """SimpleKeyword: BasisSet."""
    CC_PWCV5Z_DK = SimpleKeyword("cc-pwcv5z-dk")
    """SimpleKeyword: BasisSet."""
    CC_PWCV5Z_PP = SimpleKeyword("cc-pwcv5z-pp")
    """SimpleKeyword: BasisSet."""
    CC_PWCVDZ = SimpleKeyword("cc-pwcvdz")
    """SimpleKeyword: BasisSet."""
    CC_PWCVDZ_DK = SimpleKeyword("cc-pwcvdz-dk")
    """SimpleKeyword: BasisSet."""
    CC_PWCVDZ_DK3 = SimpleKeyword("cc-pwcvdz-dk3")
    """SimpleKeyword: BasisSet."""
    CC_PWCVDZ_PP = SimpleKeyword("cc-pwcvdz-pp")
    """SimpleKeyword: BasisSet."""
    CC_PWCVQZ = SimpleKeyword("cc-pwcvqz")
    """SimpleKeyword: BasisSet."""
    CC_PWCVQZ_DK = SimpleKeyword("cc-pwcvqz-dk")
    """SimpleKeyword: BasisSet."""
    CC_PWCVQZ_DK3 = SimpleKeyword("cc-pwcvqz-dk3")
    """SimpleKeyword: BasisSet."""
    CC_PWCVQZ_PP = SimpleKeyword("cc-pwcvqz-pp")
    """SimpleKeyword: BasisSet."""
    CC_PWCVTZ = SimpleKeyword("cc-pwcvtz")
    """SimpleKeyword: BasisSet."""
    CC_PWCVTZ_DK = SimpleKeyword("cc-pwcvtz-dk")
    """SimpleKeyword: BasisSet."""
    CC_PWCVTZ_DK3 = SimpleKeyword("cc-pwcvtz-dk3")
    """SimpleKeyword: BasisSet."""
    CC_PWCVTZ_PP = SimpleKeyword("cc-pwcvtz-pp")
    """SimpleKeyword: BasisSet."""
    CP = SimpleKeyword("cp")
    """SimpleKeyword: BasisSet."""
    CP_PPP = SimpleKeyword("cp(ppp)")
    """SimpleKeyword: BasisSet."""
    CRENBL = SimpleKeyword("crenbl")
    """SimpleKeyword: BasisSet."""
    D95 = SimpleKeyword("d95")
    """SimpleKeyword: BasisSet."""
    D95P = SimpleKeyword("d95p")
    """SimpleKeyword: BasisSet."""
    DEF_SV_P = SimpleKeyword("def-sv(p)")
    """SimpleKeyword: BasisSet."""
    DEF_SVP = SimpleKeyword("def-svp")
    """SimpleKeyword: BasisSet."""
    DEF_TZVP = SimpleKeyword("def-tzvp")
    """SimpleKeyword: BasisSet."""
    DEF_TZVPP = SimpleKeyword("def-tzvpp")
    """SimpleKeyword: BasisSet."""
    DEF2_MSVP = SimpleKeyword("def2-msvp")
    """SimpleKeyword: BasisSet."""
    DEF2_MTZVP = SimpleKeyword("def2-mtzvp")
    """SimpleKeyword: BasisSet."""
    DEF2_MTZVPP = SimpleKeyword("def2-mtzvpp")
    """SimpleKeyword: BasisSet."""
    DEF2_QZVP = SimpleKeyword("def2-qzvp")
    """SimpleKeyword: BasisSet."""
    DEF2_QZVPD = SimpleKeyword("def2-qzvpd")
    """SimpleKeyword: BasisSet."""
    DEF2_QZVPP = SimpleKeyword("def2-qzvpp")
    """SimpleKeyword: BasisSet."""
    DEF2_QZVPPD = SimpleKeyword("def2-qzvppd")
    """SimpleKeyword: BasisSet."""
    DEF2_SV_P = SimpleKeyword("def2-sv(p)")
    """SimpleKeyword: BasisSet."""
    DEF2_SVP = SimpleKeyword("def2-svp")
    """SimpleKeyword: BasisSet."""
    DEF2_SVPD = SimpleKeyword("def2-svpd")
    """SimpleKeyword: BasisSet."""
    DEF2_TZVP = SimpleKeyword("def2-tzvp")
    """SimpleKeyword: BasisSet."""
    DEF2_TZVP_F = SimpleKeyword("def2-tzvp(-f)")
    """SimpleKeyword: BasisSet."""
    DEF2_TZVPD = SimpleKeyword("def2-tzvpd")
    """SimpleKeyword: BasisSet."""
    DEF2_TZVPP = SimpleKeyword("def2-tzvpp")
    """SimpleKeyword: BasisSet."""
    DEF2_TZVPPD = SimpleKeyword("def2-tzvppd")
    """SimpleKeyword: BasisSet."""
    DHF_QZVP = SimpleKeyword("dhf-qzvp")
    """SimpleKeyword: BasisSet."""
    DHF_QZVP_2C = SimpleKeyword("dhf-qzvp-2c")
    """SimpleKeyword: BasisSet."""
    DHF_QZVPP = SimpleKeyword("dhf-qzvpp")
    """SimpleKeyword: BasisSet."""
    DHF_QZVPP_2C = SimpleKeyword("dhf-qzvpp-2c")
    """SimpleKeyword: BasisSet."""
    DHF_SV_P = SimpleKeyword("dhf-sv(p)")
    """SimpleKeyword: BasisSet."""
    DHF_SV_P_2C = SimpleKeyword("dhf-sv(p)-2c")
    """SimpleKeyword: BasisSet."""
    DHF_SVP = SimpleKeyword("dhf-svp")
    """SimpleKeyword: BasisSet."""
    DHF_SVP_2C = SimpleKeyword("dhf-svp-2c")
    """SimpleKeyword: BasisSet."""
    DHF_TZVP = SimpleKeyword("dhf-tzvp")
    """SimpleKeyword: BasisSet."""
    DHF_TZVP_2C = SimpleKeyword("dhf-tzvp-2c")
    """SimpleKeyword: BasisSet."""
    DHF_TZVPP = SimpleKeyword("dhf-tzvpp")
    """SimpleKeyword: BasisSet."""
    DHF_TZVPP_2C = SimpleKeyword("dhf-tzvpp-2c")
    """SimpleKeyword: BasisSet."""
    DKH_DEF2_QZVPP = SimpleKeyword("dkh-def2-qzvpp")
    """SimpleKeyword: BasisSet."""
    DKH_DEF2_SV_P = SimpleKeyword("dkh-def2-sv(p)")
    """SimpleKeyword: BasisSet."""
    DKH_DEF2_SVP = SimpleKeyword("dkh-def2-svp")
    """SimpleKeyword: BasisSet."""
    DKH_DEF2_TZVP = SimpleKeyword("dkh-def2-tzvp")
    """SimpleKeyword: BasisSet."""
    DKH_DEF2_TZVP_F = SimpleKeyword("dkh-def2-tzvp(-f)")
    """SimpleKeyword: BasisSet."""
    DKH_DEF2_TZVPP = SimpleKeyword("dkh-def2-tzvpp")
    """SimpleKeyword: BasisSet."""
    DKH_MA_DEF2_QZVPP = SimpleKeyword("dkh-ma-def2-qzvpp")
    """SimpleKeyword: BasisSet."""
    DKH_MA_DEF2_SV_P = SimpleKeyword("dkh-ma-def2-sv(p)")
    """SimpleKeyword: BasisSet."""
    DKH_MA_DEF2_SVP = SimpleKeyword("dkh-ma-def2-svp")
    """SimpleKeyword: BasisSet."""
    DKH_MA_DEF2_TZVP = SimpleKeyword("dkh-ma-def2-tzvp")
    """SimpleKeyword: BasisSet."""
    DKH_MA_DEF2_TZVP_F = SimpleKeyword("dkh-ma-def2-tzvp(-f)")
    """SimpleKeyword: BasisSet."""
    DKH_MA_DEF2_TZVPP = SimpleKeyword("dkh-ma-def2-tzvpp")
    """SimpleKeyword: BasisSet."""
    DKH_QZVP = SimpleKeyword("dkh-qzvp")
    """SimpleKeyword: BasisSet."""
    DKH_QZVPP = SimpleKeyword("dkh-qzvpp")
    """SimpleKeyword: BasisSet."""
    DKH_SV_P = SimpleKeyword("dkh-sv(p)")
    """SimpleKeyword: BasisSet."""
    DKH_SVP = SimpleKeyword("dkh-svp")
    """SimpleKeyword: BasisSet."""
    DKH_TZV_P = SimpleKeyword("dkh-tzv(p)")
    """SimpleKeyword: BasisSet."""
    DKH_TZVP = SimpleKeyword("dkh-tzvp")
    """SimpleKeyword: BasisSet."""
    DKH_TZVPP = SimpleKeyword("dkh-tzvpp")
    """SimpleKeyword: BasisSet."""
    EPR_II = SimpleKeyword("epr-ii")
    """SimpleKeyword: BasisSet."""
    EPR_III = SimpleKeyword("epr-iii")
    """SimpleKeyword: BasisSet."""
    GFN1BASIS = SimpleKeyword("gfn1Basis")
    """SimpleKeyword: BasisSet."""
    GFN2BASIS = SimpleKeyword("gfn2Basis")
    """SimpleKeyword: BasisSet."""
    HAV_5PLUSD_Z = SimpleKeyword("hav(5+d)z")
    """SimpleKeyword: BasisSet."""
    HAV_QPLUSD_Z = SimpleKeyword("hav(q+d)z")
    """SimpleKeyword: BasisSet."""
    HAV_TPLUSD_Z = SimpleKeyword("hav(t+d)z")
    """SimpleKeyword: BasisSet."""
    HAV5Z_PLUSD = SimpleKeyword("hav5z(+d)")
    """SimpleKeyword: BasisSet."""
    HAVQZ_PLUSD = SimpleKeyword("havqz(+d)")
    """SimpleKeyword: BasisSet."""
    HAVTZ_PLUSD = SimpleKeyword("havtz(+d)")
    """SimpleKeyword: BasisSet."""
    HGBS_5 = SimpleKeyword("hgbs-5")
    """SimpleKeyword: BasisSet."""
    HGBS_7 = SimpleKeyword("hgbs-7")
    """SimpleKeyword: BasisSet."""
    HGBS_9 = SimpleKeyword("hgbs-9")
    """SimpleKeyword: BasisSet."""
    HGBSP1_5 = SimpleKeyword("hgbsp1-5")
    """SimpleKeyword: BasisSet."""
    HGBSP1_7 = SimpleKeyword("hgbsp1-7")
    """SimpleKeyword: BasisSet."""
    HGBSP1_9 = SimpleKeyword("hgbsp1-9")
    """SimpleKeyword: BasisSet."""
    HGBSP2_5 = SimpleKeyword("hgbsp2-5")
    """SimpleKeyword: BasisSet."""
    HGBSP2_7 = SimpleKeyword("hgbsp2-7")
    """SimpleKeyword: BasisSet."""
    HGBSP2_9 = SimpleKeyword("hgbsp2-9")
    """SimpleKeyword: BasisSet."""
    HGBSP3_5 = SimpleKeyword("hgbsp3-5")
    """SimpleKeyword: BasisSet."""
    HGBSP3_7 = SimpleKeyword("hgbsp3-7")
    """SimpleKeyword: BasisSet."""
    HGBSP3_9 = SimpleKeyword("hgbsp3-9")
    """SimpleKeyword: BasisSet."""
    IGLO_II = SimpleKeyword("iglo-ii")
    """SimpleKeyword: BasisSet."""
    IGLO_III = SimpleKeyword("iglo-iii")
    """SimpleKeyword: BasisSet."""
    JUL_CC_PV_DPLUSD_Z = SimpleKeyword("jul-cc-pv(d+d)z")
    """SimpleKeyword: BasisSet."""
    JUL_CC_PV_QPLUSD_Z = SimpleKeyword("jul-cc-pv(q+d)z")
    """SimpleKeyword: BasisSet."""
    JUL_CC_PV_TPLUSD_Z = SimpleKeyword("jul-cc-pv(t+d)z")
    """SimpleKeyword: BasisSet."""
    JUN_CC_PV_DPLUSD_Z = SimpleKeyword("jun-cc-pv(d+d)z")
    """SimpleKeyword: BasisSet."""
    JUN_CC_PV_QPLUSD_Z = SimpleKeyword("jun-cc-pv(q+d)z")
    """SimpleKeyword: BasisSet."""
    JUN_CC_PV_TPLUSD_Z = SimpleKeyword("jun-cc-pv(t+d)z")
    """SimpleKeyword: BasisSet."""
    LANL08 = SimpleKeyword("lanl08")
    """SimpleKeyword: BasisSet."""
    LANL08_F = SimpleKeyword("lanl08(f)")
    """SimpleKeyword: BasisSet."""
    LANL2DZ = SimpleKeyword("lanl2dz")
    """SimpleKeyword: BasisSet."""
    LANL2TZ = SimpleKeyword("lanl2tz")
    """SimpleKeyword: BasisSet."""
    LANL2TZ_F = SimpleKeyword("lanl2tz(f)")
    """SimpleKeyword: BasisSet."""
    M6_31G = SimpleKeyword("m6-31g")
    """SimpleKeyword: BasisSet."""
    M6_31GSTAR = SimpleKeyword("m6-31g*")
    """SimpleKeyword: BasisSet."""
    MA_DEF_TZVP = SimpleKeyword("ma-def-tzvp")
    """SimpleKeyword: BasisSet."""
    MA_DEF2_MSVP = SimpleKeyword("ma-def2-msvp")
    """SimpleKeyword: BasisSet."""
    MA_DEF2_QZVP = SimpleKeyword("ma-def2-qzvp")
    """SimpleKeyword: BasisSet."""
    MA_DEF2_QZVPP = SimpleKeyword("ma-def2-qzvpp")
    """SimpleKeyword: BasisSet."""
    MA_DEF2_SV_P = SimpleKeyword("ma-def2-sv(p)")
    """SimpleKeyword: BasisSet."""
    MA_DEF2_SVP = SimpleKeyword("ma-def2-svp")
    """SimpleKeyword: BasisSet."""
    MA_DEF2_TZVP = SimpleKeyword("ma-def2-tzvp")
    """SimpleKeyword: BasisSet."""
    MA_DEF2_TZVP_F = SimpleKeyword("ma-def2-tzvp(-f)")
    """SimpleKeyword: BasisSet."""
    MA_DEF2_TZVPP = SimpleKeyword("ma-def2-tzvpp")
    """SimpleKeyword: BasisSet."""
    MA_DKH_DEF2_QZVPP = SimpleKeyword("ma-dkh-def2-qzvpp")
    """SimpleKeyword: BasisSet."""
    MA_DKH_DEF2_SV_P = SimpleKeyword("ma-dkh-def2-sv(p)")
    """SimpleKeyword: BasisSet."""
    MA_DKH_DEF2_SVP = SimpleKeyword("ma-dkh-def2-svp")
    """SimpleKeyword: BasisSet."""
    MA_DKH_DEF2_TZVP = SimpleKeyword("ma-dkh-def2-tzvp")
    """SimpleKeyword: BasisSet."""
    MA_DKH_DEF2_TZVP_F = SimpleKeyword("ma-dkh-def2-tzvp(-f)")
    """SimpleKeyword: BasisSet."""
    MA_DKH_DEF2_TZVPP = SimpleKeyword("ma-dkh-def2-tzvpp")
    """SimpleKeyword: BasisSet."""
    MA_ZORA_DEF2_QZVPP = SimpleKeyword("ma-zora-def2-qzvpp")
    """SimpleKeyword: BasisSet."""
    MA_ZORA_DEF2_SV_P = SimpleKeyword("ma-zora-def2-sv(p)")
    """SimpleKeyword: BasisSet."""
    MA_ZORA_DEF2_SVP = SimpleKeyword("ma-zora-def2-svp")
    """SimpleKeyword: BasisSet."""
    MA_ZORA_DEF2_TZVP = SimpleKeyword("ma-zora-def2-tzvp")
    """SimpleKeyword: BasisSet."""
    MA_ZORA_DEF2_TZVP_F = SimpleKeyword("ma-zora-def2-tzvp(-f)")
    """SimpleKeyword: BasisSet."""
    MA_ZORA_DEF2_TZVPP = SimpleKeyword("ma-zora-def2-tzvpp")
    """SimpleKeyword: BasisSet."""
    MAUG_CC_PV_DPLUSD_Z = SimpleKeyword("maug-cc-pv(d+d)z")
    """SimpleKeyword: BasisSet."""
    MAUG_CC_PV_QPLUSD_Z = SimpleKeyword("maug-cc-pv(q+d)z")
    """SimpleKeyword: BasisSet."""
    MAUG_CC_PV_TPLUSD_Z = SimpleKeyword("maug-cc-pv(t+d)z")
    """SimpleKeyword: BasisSet."""
    MAY_CC_PV_QPLUSD_Z = SimpleKeyword("may-cc-pv(q+d)z")
    """SimpleKeyword: BasisSet."""
    MAY_CC_PV_TPLUSD_Z = SimpleKeyword("may-cc-pv(t+d)z")
    """SimpleKeyword: BasisSet."""
    MIDI = SimpleKeyword("midi")
    """SimpleKeyword: BasisSet."""
    MINAO = SimpleKeyword("minao")
    """SimpleKeyword: BasisSet."""
    MINAO_AUTO_PP = SimpleKeyword("minao-auto-pp")
    """SimpleKeyword: BasisSet."""
    MINI = SimpleKeyword("mini")
    """SimpleKeyword: BasisSet."""
    MINIS = SimpleKeyword("minis")
    """SimpleKeyword: BasisSet."""
    MINIX = SimpleKeyword("minix")
    """SimpleKeyword: BasisSet."""
    OLD_DKH_SV_P = SimpleKeyword("old-dkh-sv(p)")
    """SimpleKeyword: BasisSet."""
    OLD_DKH_SVP = SimpleKeyword("old-dkh-svp")
    """SimpleKeyword: BasisSet."""
    OLD_DKH_TZV_P = SimpleKeyword("old-dkh-tzv(p)")
    """SimpleKeyword: BasisSet."""
    OLD_DKH_TZVP = SimpleKeyword("old-dkh-tzvp")
    """SimpleKeyword: BasisSet."""
    OLD_DKH_TZVPP = SimpleKeyword("old-dkh-tzvpp")
    """SimpleKeyword: BasisSet."""
    OLD_SV = SimpleKeyword("old-sv")
    """SimpleKeyword: BasisSet."""
    OLD_SV_P = SimpleKeyword("old-sv(p)")
    """SimpleKeyword: BasisSet."""
    OLD_SVP = SimpleKeyword("old-svp")
    """SimpleKeyword: BasisSet."""
    OLD_TZV = SimpleKeyword("old-tzv")
    """SimpleKeyword: BasisSet."""
    OLD_TZV_P = SimpleKeyword("old-tzv(p)")
    """SimpleKeyword: BasisSet."""
    OLD_TZVP = SimpleKeyword("old-tzvp")
    """SimpleKeyword: BasisSet."""
    OLD_TZVPP = SimpleKeyword("old-tzvpp")
    """SimpleKeyword: BasisSet."""
    OLD_ZORA_SV_P = SimpleKeyword("old-zora-sv(p)")
    """SimpleKeyword: BasisSet."""
    OLD_ZORA_SVP = SimpleKeyword("old-zora-svp")
    """SimpleKeyword: BasisSet."""
    OLD_ZORA_TZV_P = SimpleKeyword("old-zora-tzv(p)")
    """SimpleKeyword: BasisSet."""
    OLD_ZORA_TZVP = SimpleKeyword("old-zora-tzvp")
    """SimpleKeyword: BasisSet."""
    OLD_ZORA_TZVPP = SimpleKeyword("old-zora-tzvpp")
    """SimpleKeyword: BasisSet."""
    PARTRIDGE_1 = SimpleKeyword("partridge-1")
    """SimpleKeyword: BasisSet."""
    PARTRIDGE_2 = SimpleKeyword("partridge-2")
    """SimpleKeyword: BasisSet."""
    PARTRIDGE_3 = SimpleKeyword("partridge-3")
    """SimpleKeyword: BasisSet."""
    PARTRIDGE_4 = SimpleKeyword("partridge-4")
    """SimpleKeyword: BasisSet."""
    PC_0 = SimpleKeyword("pc-0")
    """SimpleKeyword: BasisSet."""
    PC_1 = SimpleKeyword("pc-1")
    """SimpleKeyword: BasisSet."""
    PC_2 = SimpleKeyword("pc-2")
    """SimpleKeyword: BasisSet."""
    PC_3 = SimpleKeyword("pc-3")
    """SimpleKeyword: BasisSet."""
    PC_4 = SimpleKeyword("pc-4")
    """SimpleKeyword: BasisSet."""
    PCH_1 = SimpleKeyword("pch-1")
    """SimpleKeyword: BasisSet."""
    PCH_2 = SimpleKeyword("pch-2")
    """SimpleKeyword: BasisSet."""
    PCH_3 = SimpleKeyword("pch-3")
    """SimpleKeyword: BasisSet."""
    PCH_4 = SimpleKeyword("pch-4")
    """SimpleKeyword: BasisSet."""
    PCJ_0 = SimpleKeyword("pcj-0")
    """SimpleKeyword: BasisSet."""
    PCJ_1 = SimpleKeyword("pcj-1")
    """SimpleKeyword: BasisSet."""
    PCJ_2 = SimpleKeyword("pcj-2")
    """SimpleKeyword: BasisSet."""
    PCJ_3 = SimpleKeyword("pcj-3")
    """SimpleKeyword: BasisSet."""
    PCJ_4 = SimpleKeyword("pcj-4")
    """SimpleKeyword: BasisSet."""
    PCSEG_0 = SimpleKeyword("pcseg-0")
    """SimpleKeyword: BasisSet."""
    PCSEG_1 = SimpleKeyword("pcseg-1")
    """SimpleKeyword: BasisSet."""
    PCSEG_2 = SimpleKeyword("pcseg-2")
    """SimpleKeyword: BasisSet."""
    PCSEG_3 = SimpleKeyword("pcseg-3")
    """SimpleKeyword: BasisSet."""
    PCSEG_4 = SimpleKeyword("pcseg-4")
    """SimpleKeyword: BasisSet."""
    PCSSEG_0 = SimpleKeyword("pcsseg-0")
    """SimpleKeyword: BasisSet."""
    PCSSEG_1 = SimpleKeyword("pcsseg-1")
    """SimpleKeyword: BasisSet."""
    PCSSEG_2 = SimpleKeyword("pcsseg-2")
    """SimpleKeyword: BasisSet."""
    PCSSEG_3 = SimpleKeyword("pcsseg-3")
    """SimpleKeyword: BasisSet."""
    PCSSEG_4 = SimpleKeyword("pcsseg-4")
    """SimpleKeyword: BasisSet."""
    PCX_1 = SimpleKeyword("pcx-1")
    """SimpleKeyword: BasisSet."""
    PCX_2 = SimpleKeyword("pcx-2")
    """SimpleKeyword: BasisSet."""
    PCX_3 = SimpleKeyword("pcx-3")
    """SimpleKeyword: BasisSet."""
    PCX_4 = SimpleKeyword("pcx-4")
    """SimpleKeyword: BasisSet."""
    QZVP = SimpleKeyword("qzvp")
    """SimpleKeyword: BasisSet."""
    QZVPP = SimpleKeyword("qzvpp")
    """SimpleKeyword: BasisSet."""
    SAPPORO_DKH3_DZP_2012 = SimpleKeyword("sapporo-dkh3-dzp-2012")
    """SimpleKeyword: BasisSet."""
    SAPPORO_DKH3_QZP_2012 = SimpleKeyword("sapporo-dkh3-qzp-2012")
    """SimpleKeyword: BasisSet."""
    SAPPORO_DKH3_TZP_2012 = SimpleKeyword("sapporo-dkh3-tzp-2012")
    """SimpleKeyword: BasisSet."""
    SAPPORO_DZP_2012 = SimpleKeyword("sapporo-dzp-2012")
    """SimpleKeyword: BasisSet."""
    SAPPORO_QZP_2012 = SimpleKeyword("sapporo-qzp-2012")
    """SimpleKeyword: BasisSet."""
    SAPPORO_TZP_2012 = SimpleKeyword("sapporo-tzp-2012")
    """SimpleKeyword: BasisSet."""
    SARC_DKH_SVP = SimpleKeyword("sarc-dkh-svp")
    """SimpleKeyword: BasisSet."""
    SARC_DKH_TZVP = SimpleKeyword("sarc-dkh-tzvp")
    """SimpleKeyword: BasisSet."""
    SARC_DKH_TZVPP = SimpleKeyword("sarc-dkh-tzvpp")
    """SimpleKeyword: BasisSet."""
    SARC_ZORA_SVP = SimpleKeyword("sarc-zora-svp")
    """SimpleKeyword: BasisSet."""
    SARC_ZORA_TZVP = SimpleKeyword("sarc-zora-tzvp")
    """SimpleKeyword: BasisSet."""
    SARC_ZORA_TZVPP = SimpleKeyword("sarc-zora-tzvpp")
    """SimpleKeyword: BasisSet."""
    SARC2_DKH_QZV = SimpleKeyword("sarc2-dkh-qzv")
    """SimpleKeyword: BasisSet."""
    SARC2_DKH_QZVP = SimpleKeyword("sarc2-dkh-qzvp")
    """SimpleKeyword: BasisSet."""
    SARC2_ZORA_QZV = SimpleKeyword("sarc2-zora-qzv")
    """SimpleKeyword: BasisSet."""
    SARC2_ZORA_QZVP = SimpleKeyword("sarc2-zora-qzvp")
    """SimpleKeyword: BasisSet."""
    SAUG_ANO_PV5Z = SimpleKeyword("saug-ano-pv5z")
    """SimpleKeyword: BasisSet."""
    SAUG_ANO_PVDZ = SimpleKeyword("saug-ano-pvdz")
    """SimpleKeyword: BasisSet."""
    SAUG_ANO_PVQZ = SimpleKeyword("saug-ano-pvqz")
    """SimpleKeyword: BasisSet."""
    SAUG_ANO_PVTZ = SimpleKeyword("saug-ano-pvtz")
    """SimpleKeyword: BasisSet."""
    STO_3G = SimpleKeyword("sto-3g")
    """SimpleKeyword: BasisSet."""
    SV = SimpleKeyword("sv")
    """SimpleKeyword: BasisSet."""
    SV_P = SimpleKeyword("sv(p)")
    """SimpleKeyword: BasisSet."""
    SVP = SimpleKeyword("svp")
    """SimpleKeyword: BasisSet."""
    TZV = SimpleKeyword("tzv")
    """SimpleKeyword: BasisSet."""
    TZV_P = SimpleKeyword("tzv(p)")
    """SimpleKeyword: BasisSet."""
    TZVP = SimpleKeyword("tzvp")
    """SimpleKeyword: BasisSet."""
    TZVPP = SimpleKeyword("tzvpp")
    """SimpleKeyword: BasisSet."""
    UGBS = SimpleKeyword("ugbs")
    """SimpleKeyword: BasisSet."""
    VDZP = SimpleKeyword("vdzp")
    """SimpleKeyword: BasisSet."""
    W1_DZ = SimpleKeyword("w1-dz")
    """SimpleKeyword: BasisSet."""
    W1_MTSMALL = SimpleKeyword("w1-mtsmall")
    """SimpleKeyword: BasisSet."""
    W1_OPT = SimpleKeyword("w1-opt")
    """SimpleKeyword: BasisSet."""
    W1_QZ = SimpleKeyword("w1-qz")
    """SimpleKeyword: BasisSet."""
    W1_TZ = SimpleKeyword("w1-tz")
    """SimpleKeyword: BasisSet."""
    WACHTERSPLUSF = SimpleKeyword("wachters+f")
    """SimpleKeyword: BasisSet."""
    X2C_QZVPALL = SimpleKeyword("x2c-qzvpall")
    """SimpleKeyword: BasisSet."""
    X2C_QZVPALL_2C = SimpleKeyword("x2c-qzvpall-2c")
    """SimpleKeyword: BasisSet."""
    X2C_QZVPALL_2C_S = SimpleKeyword("x2c-qzvpall-2c-s")
    """SimpleKeyword: BasisSet."""
    X2C_QZVPALL_S = SimpleKeyword("x2c-qzvpall-s")
    """SimpleKeyword: BasisSet."""
    X2C_QZVPPALL = SimpleKeyword("x2c-qzvppall")
    """SimpleKeyword: BasisSet."""
    X2C_QZVPPALL_2C = SimpleKeyword("x2c-qzvppall-2c")
    """SimpleKeyword: BasisSet."""
    X2C_QZVPPALL_2C_S = SimpleKeyword("x2c-qzvppall-2c-s")
    """SimpleKeyword: BasisSet."""
    X2C_QZVPPALL_S = SimpleKeyword("x2c-qzvppall-s")
    """SimpleKeyword: BasisSet."""
    X2C_SV_P_ALL = SimpleKeyword("x2c-sv(p)all")
    """SimpleKeyword: BasisSet."""
    X2C_SV_P_ALL_2C = SimpleKeyword("x2c-sv(p)all-2c")
    """SimpleKeyword: BasisSet."""
    X2C_SV_P_ALL_S = SimpleKeyword("x2c-sv(p)all-s")
    """SimpleKeyword: BasisSet."""
    X2C_SVPALL = SimpleKeyword("x2c-svpall")
    """SimpleKeyword: BasisSet."""
    X2C_SVPALL_2C = SimpleKeyword("x2c-svpall-2c")
    """SimpleKeyword: BasisSet."""
    X2C_SVPALL_S = SimpleKeyword("x2c-svpall-s")
    """SimpleKeyword: BasisSet."""
    X2C_TZVPALL = SimpleKeyword("x2c-tzvpall")
    """SimpleKeyword: BasisSet."""
    X2C_TZVPALL_2C = SimpleKeyword("x2c-tzvpall-2c")
    """SimpleKeyword: BasisSet."""
    X2C_TZVPALL_S = SimpleKeyword("x2c-tzvpall-s")
    """SimpleKeyword: BasisSet."""
    X2C_TZVPPALL = SimpleKeyword("x2c-tzvppall")
    """SimpleKeyword: BasisSet."""
    X2C_TZVPPALL_2C = SimpleKeyword("x2c-tzvppall-2c")
    """SimpleKeyword: BasisSet."""
    X2C_TZVPPALL_S = SimpleKeyword("x2c-tzvppall-s")
    """SimpleKeyword: BasisSet."""
    ZORA_DEF2_QZVPP = SimpleKeyword("zora-def2-qzvpp")
    """SimpleKeyword: BasisSet."""
    ZORA_DEF2_SV_P = SimpleKeyword("zora-def2-sv(p)")
    """SimpleKeyword: BasisSet."""
    ZORA_DEF2_SVP = SimpleKeyword("zora-def2-svp")
    """SimpleKeyword: BasisSet."""
    ZORA_DEF2_TZVP = SimpleKeyword("zora-def2-tzvp")
    """SimpleKeyword: BasisSet."""
    ZORA_DEF2_TZVP_F = SimpleKeyword("zora-def2-tzvp(-f)")
    """SimpleKeyword: BasisSet."""
    ZORA_DEF2_TZVPP = SimpleKeyword("zora-def2-tzvpp")
    """SimpleKeyword: BasisSet."""
    ZORA_MA_DEF2_QZVPP = SimpleKeyword("zora-ma-def2-qzvpp")
    """SimpleKeyword: BasisSet."""
    ZORA_MA_DEF2_SV_P = SimpleKeyword("zora-ma-def2-sv(p)")
    """SimpleKeyword: BasisSet."""
    ZORA_MA_DEF2_SVP = SimpleKeyword("zora-ma-def2-svp")
    """SimpleKeyword: BasisSet."""
    ZORA_MA_DEF2_TZVP = SimpleKeyword("zora-ma-def2-tzvp")
    """SimpleKeyword: BasisSet."""
    ZORA_MA_DEF2_TZVP_F = SimpleKeyword("zora-ma-def2-tzvp(-f)")
    """SimpleKeyword: BasisSet."""
    ZORA_MA_DEF2_TZVPP = SimpleKeyword("zora-ma-def2-tzvpp")
    """SimpleKeyword: BasisSet."""
    ZORA_QZVP = SimpleKeyword("zora-qzvp")
    """SimpleKeyword: BasisSet."""
    ZORA_QZVPP = SimpleKeyword("zora-qzvpp")
    """SimpleKeyword: BasisSet."""
    ZORA_SV_P = SimpleKeyword("zora-sv(p)")
    """SimpleKeyword: BasisSet."""
    ZORA_SVP = SimpleKeyword("zora-svp")
    """SimpleKeyword: BasisSet."""
    ZORA_TZV_P = SimpleKeyword("zora-tzv(p)")
    """SimpleKeyword: BasisSet."""
    ZORA_TZVP = SimpleKeyword("zora-tzvp")
    """SimpleKeyword: BasisSet."""
    ZORA_TZVPP = SimpleKeyword("zora-tzvpp")
    """SimpleKeyword: BasisSet."""
