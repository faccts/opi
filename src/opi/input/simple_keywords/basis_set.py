from opi.input.simple_keywords.base import (
    SimpleKeyword,
    SimpleKeywordBox,
)

__all__ = ("BasisSet",)


class BasisSet(SimpleKeywordBox):
    """Enum to store all simple keywords of type BasisSet.

    Attributes
    ----------
    G3_21G : SimpleKeyword
        BasisSet
    G3_21GSP : SimpleKeyword
        BasisSet
    G4_22GSP : SimpleKeyword
        BasisSet
    G6_31PLUSPLUSG_2D_2P : SimpleKeyword
        BasisSet
    G6_31PLUSPLUSG_2D_P : SimpleKeyword
        BasisSet
    G6_31PLUSPLUSG_2DF_2P : SimpleKeyword
        BasisSet
    G6_31PLUSPLUSG_2DF_2PD : SimpleKeyword
        BasisSet
    G6_31PLUSPLUSG_D_P : SimpleKeyword
        BasisSet
    G6_31PLUSPLUSGSTARSTAR : SimpleKeyword
        BasisSet
    G6_31PLUSG_2D_2P : SimpleKeyword
        BasisSet
    G6_31PLUSG_2D_P : SimpleKeyword
        BasisSet
    G6_31PLUSG_2D : SimpleKeyword
        BasisSet
    G6_31PLUSG_2DF_2P : SimpleKeyword
        BasisSet
    G6_31PLUSG_2DF_2PD : SimpleKeyword
        BasisSet
    G6_31PLUSG_2DF : SimpleKeyword
        BasisSet
    G6_31PLUSG_D_P : SimpleKeyword
        BasisSet
    G6_31PLUSG_D : SimpleKeyword
        BasisSet
    G6_31PLUSGSTAR : SimpleKeyword
        BasisSet
    G6_31PLUSGSTARSTAR : SimpleKeyword
        BasisSet
    G6_311PLUSPLUSG_2D_2P : SimpleKeyword
        BasisSet
    G6_311PLUSPLUSG_2D_P : SimpleKeyword
        BasisSet
    G6_311PLUSPLUSG_2DF_2P : SimpleKeyword
        BasisSet
    G6_311PLUSPLUSG_2DF_2PD : SimpleKeyword
        BasisSet
    G6_311PLUSPLUSG_3DF_3PD : SimpleKeyword
        BasisSet
    G6_311PLUSPLUSG_D_P : SimpleKeyword
        BasisSet
    G6_311PLUSPLUSGSTARSTAR : SimpleKeyword
        BasisSet
    G6_311PLUSG_2D_2P : SimpleKeyword
        BasisSet
    G6_311PLUSG_2D_P : SimpleKeyword
        BasisSet
    G6_311PLUSG_2D : SimpleKeyword
        BasisSet
    G6_311PLUSG_2DF_2P : SimpleKeyword
        BasisSet
    G6_311PLUSG_2DF_2PD : SimpleKeyword
        BasisSet
    G6_311PLUSG_2DF : SimpleKeyword
        BasisSet
    G6_311PLUSG_3DF_2P : SimpleKeyword
        BasisSet
    G6_311PLUSG_3DF_3PD : SimpleKeyword
        BasisSet
    G6_311PLUSG_3DF : SimpleKeyword
        BasisSet
    G6_311PLUSG_D_P : SimpleKeyword
        BasisSet
    G6_311PLUSG_D : SimpleKeyword
        BasisSet
    G6_311PLUSGSTAR : SimpleKeyword
        BasisSet
    G6_311PLUSGSTARSTAR : SimpleKeyword
        BasisSet
    G6_311G : SimpleKeyword
        BasisSet
    G6_311G_2D_2P : SimpleKeyword
        BasisSet
    G6_311G_2D_P : SimpleKeyword
        BasisSet
    G6_311G_2D : SimpleKeyword
        BasisSet
    G6_311G_2DF_2P : SimpleKeyword
        BasisSet
    G6_311G_2DF_2PD : SimpleKeyword
        BasisSet
    G6_311G_2DF : SimpleKeyword
        BasisSet
    G6_311G_3DF_3PD : SimpleKeyword
        BasisSet
    G6_311G_3DF : SimpleKeyword
        BasisSet
    G6_311G_D_P : SimpleKeyword
        BasisSet
    G6_311G_D : SimpleKeyword
        BasisSet
    G6_311GSTAR : SimpleKeyword
        BasisSet
    G6_311GSTARSTAR : SimpleKeyword
        BasisSet
    G6_31G : SimpleKeyword
        BasisSet
    G6_31G_2D_2P : SimpleKeyword
        BasisSet
    G6_31G_2D_P : SimpleKeyword
        BasisSet
    G6_31G_2D : SimpleKeyword
        BasisSet
    G6_31G_2DF_2P : SimpleKeyword
        BasisSet
    G6_31G_2DF_2PD : SimpleKeyword
        BasisSet
    G6_31G_2DF : SimpleKeyword
        BasisSet
    G6_31G_D_P : SimpleKeyword
        BasisSet
    G6_31G_D : SimpleKeyword
        BasisSet
    G6_31GSTAR : SimpleKeyword
        BasisSet
    G6_31GSTARSTAR : SimpleKeyword
        BasisSet
    AHGBS_5 : SimpleKeyword
        BasisSet
    AHGBS_7 : SimpleKeyword
        BasisSet
    AHGBS_9 : SimpleKeyword
        BasisSet
    AHGBSP1_5 : SimpleKeyword
        BasisSet
    AHGBSP1_7 : SimpleKeyword
        BasisSet
    AHGBSP1_9 : SimpleKeyword
        BasisSet
    AHGBSP2_5 : SimpleKeyword
        BasisSet
    AHGBSP2_7 : SimpleKeyword
        BasisSet
    AHGBSP2_9 : SimpleKeyword
        BasisSet
    AHGBSP3_5 : SimpleKeyword
        BasisSet
    AHGBSP3_7 : SimpleKeyword
        BasisSet
    AHGBSP3_9 : SimpleKeyword
        BasisSet
    ANO_PC_0 : SimpleKeyword
        BasisSet
    ANO_PC_0_POL : SimpleKeyword
        BasisSet
    ANO_PV5Z : SimpleKeyword
        BasisSet
    ANO_PV6Z : SimpleKeyword
        BasisSet
    ANO_PVDZ : SimpleKeyword
        BasisSet
    ANO_PVQZ : SimpleKeyword
        BasisSet
    ANO_PVTZ : SimpleKeyword
        BasisSet
    ANO_RCC_DZP : SimpleKeyword
        BasisSet
    ANO_RCC_FULL : SimpleKeyword
        BasisSet
    ANO_RCC_MB : SimpleKeyword
        BasisSet
    ANO_RCC_QZP : SimpleKeyword
        BasisSet
    ANO_RCC_TZP : SimpleKeyword
        BasisSet
    ANO_SZ : SimpleKeyword
        BasisSet
    ANO_SZ_DKH_SMALL : SimpleKeyword
        BasisSet
    APR_CC_PV_QPLUSD_Z : SimpleKeyword
        BasisSet
    AUG_ANO_PV5Z : SimpleKeyword
        BasisSet
    AUG_ANO_PVDZ : SimpleKeyword
        BasisSet
    AUG_ANO_PVQZ : SimpleKeyword
        BasisSet
    AUG_ANO_PVTZ : SimpleKeyword
        BasisSet
    AUG_CC_PCV5Z : SimpleKeyword
        BasisSet
    AUG_CC_PCV5Z_PP : SimpleKeyword
        BasisSet
    AUG_CC_PCV6Z : SimpleKeyword
        BasisSet
    AUG_CC_PCVDZ : SimpleKeyword
        BasisSet
    AUG_CC_PCVDZ_PP : SimpleKeyword
        BasisSet
    AUG_CC_PCVQZ : SimpleKeyword
        BasisSet
    AUG_CC_PCVQZ_PP : SimpleKeyword
        BasisSet
    AUG_CC_PCVTZ : SimpleKeyword
        BasisSet
    AUG_CC_PCVTZ_PP : SimpleKeyword
        BasisSet
    AUG_CC_PV5_PLUSD_Z : SimpleKeyword
        BasisSet
    AUG_CC_PV5Z : SimpleKeyword
        BasisSet
    AUG_CC_PV5Z_DK : SimpleKeyword
        BasisSet
    AUG_CC_PV5Z_PP : SimpleKeyword
        BasisSet
    AUG_CC_PV5Z_PP_OPTRI : SimpleKeyword
        BasisSet
    AUG_CC_PV6_PLUSD_Z : SimpleKeyword
        BasisSet
    AUG_CC_PV6Z : SimpleKeyword
        BasisSet
    AUG_CC_PV7Z : SimpleKeyword
        BasisSet
    AUG_CC_PVD_PLUSD_Z : SimpleKeyword
        BasisSet
    AUG_CC_PVDZ : SimpleKeyword
        BasisSet
    AUG_CC_PVDZ_DK : SimpleKeyword
        BasisSet
    AUG_CC_PVDZ_PP : SimpleKeyword
        BasisSet
    AUG_CC_PVDZ_PP_OPTRI : SimpleKeyword
        BasisSet
    AUG_CC_PVQ_PLUSD_Z : SimpleKeyword
        BasisSet
    AUG_CC_PVQZ : SimpleKeyword
        BasisSet
    AUG_CC_PVQZ_DK : SimpleKeyword
        BasisSet
    AUG_CC_PVQZ_PP : SimpleKeyword
        BasisSet
    AUG_CC_PVQZ_PP_OPTRI : SimpleKeyword
        BasisSet
    AUG_CC_PVT_PLUSD_Z : SimpleKeyword
        BasisSet
    AUG_CC_PVTZ : SimpleKeyword
        BasisSet
    AUG_CC_PVTZ_DK : SimpleKeyword
        BasisSet
    AUG_CC_PVTZ_J : SimpleKeyword
        BasisSet
    AUG_CC_PVTZ_PP : SimpleKeyword
        BasisSet
    AUG_CC_PVTZ_PP_OPTRI : SimpleKeyword
        BasisSet
    AUG_CC_PWCV5Z : SimpleKeyword
        BasisSet
    AUG_CC_PWCV5Z_DK : SimpleKeyword
        BasisSet
    AUG_CC_PWCV5Z_PP : SimpleKeyword
        BasisSet
    AUG_CC_PWCV5Z_PP_OPTRI : SimpleKeyword
        BasisSet
    AUG_CC_PWCVDZ : SimpleKeyword
        BasisSet
    AUG_CC_PWCVDZ_DK : SimpleKeyword
        BasisSet
    AUG_CC_PWCVDZ_PP : SimpleKeyword
        BasisSet
    AUG_CC_PWCVDZ_PP_OPTRI : SimpleKeyword
        BasisSet
    AUG_CC_PWCVQZ : SimpleKeyword
        BasisSet
    AUG_CC_PWCVQZ_DK : SimpleKeyword
        BasisSet
    AUG_CC_PWCVQZ_PP : SimpleKeyword
        BasisSet
    AUG_CC_PWCVQZ_PP_OPTRI : SimpleKeyword
        BasisSet
    AUG_CC_PWCVTZ : SimpleKeyword
        BasisSet
    AUG_CC_PWCVTZ_DK : SimpleKeyword
        BasisSet
    AUG_CC_PWCVTZ_PP : SimpleKeyword
        BasisSet
    AUG_CC_PWCVTZ_PP_OPTRI : SimpleKeyword
        BasisSet
    AUG_PC_0 : SimpleKeyword
        BasisSet
    AUG_PC_1 : SimpleKeyword
        BasisSet
    AUG_PC_2 : SimpleKeyword
        BasisSet
    AUG_PC_3 : SimpleKeyword
        BasisSet
    AUG_PC_4 : SimpleKeyword
        BasisSet
    AUG_PCH_1 : SimpleKeyword
        BasisSet
    AUG_PCH_2 : SimpleKeyword
        BasisSet
    AUG_PCH_3 : SimpleKeyword
        BasisSet
    AUG_PCH_4 : SimpleKeyword
        BasisSet
    AUG_PCJ_0 : SimpleKeyword
        BasisSet
    AUG_PCJ_1 : SimpleKeyword
        BasisSet
    AUG_PCJ_2 : SimpleKeyword
        BasisSet
    AUG_PCJ_3 : SimpleKeyword
        BasisSet
    AUG_PCJ_4 : SimpleKeyword
        BasisSet
    AUG_PCSEG_0 : SimpleKeyword
        BasisSet
    AUG_PCSEG_1 : SimpleKeyword
        BasisSet
    AUG_PCSEG_2 : SimpleKeyword
        BasisSet
    AUG_PCSEG_3 : SimpleKeyword
        BasisSet
    AUG_PCSEG_4 : SimpleKeyword
        BasisSet
    AUG_PCSSEG_0 : SimpleKeyword
        BasisSet
    AUG_PCSSEG_1 : SimpleKeyword
        BasisSet
    AUG_PCSSEG_2 : SimpleKeyword
        BasisSet
    AUG_PCSSEG_3 : SimpleKeyword
        BasisSet
    AUG_PCSSEG_4 : SimpleKeyword
        BasisSet
    AUG_PCX_1 : SimpleKeyword
        BasisSet
    AUG_PCX_2 : SimpleKeyword
        BasisSet
    AUG_PCX_3 : SimpleKeyword
        BasisSet
    AUG_PCX_4 : SimpleKeyword
        BasisSet
    CC_PCV5Z : SimpleKeyword
        BasisSet
    CC_PCV5Z_PP : SimpleKeyword
        BasisSet
    CC_PCV6Z : SimpleKeyword
        BasisSet
    CC_PCVDZ : SimpleKeyword
        BasisSet
    CC_PCVDZ_F12 : SimpleKeyword
        BasisSet
    CC_PCVDZ_F12_OPTRI : SimpleKeyword
        BasisSet
    CC_PCVDZ_PP : SimpleKeyword
        BasisSet
    CC_PCVQZ : SimpleKeyword
        BasisSet
    CC_PCVQZ_F12 : SimpleKeyword
        BasisSet
    CC_PCVQZ_F12_OPTRI : SimpleKeyword
        BasisSet
    CC_PCVQZ_PP : SimpleKeyword
        BasisSet
    CC_PCVTZ : SimpleKeyword
        BasisSet
    CC_PCVTZ_F12 : SimpleKeyword
        BasisSet
    CC_PCVTZ_F12_OPTRI : SimpleKeyword
        BasisSet
    CC_PCVTZ_PP : SimpleKeyword
        BasisSet
    CC_PV5_PLUSD_Z : SimpleKeyword
        BasisSet
    CC_PV5Z : SimpleKeyword
        BasisSet
    CC_PV5Z_DK : SimpleKeyword
        BasisSet
    CC_PV5Z_PP : SimpleKeyword
        BasisSet
    CC_PV6Z : SimpleKeyword
        BasisSet
    CC_PV7Z : SimpleKeyword
        BasisSet
    CC_PV8Z : SimpleKeyword
        BasisSet
    CC_PVD_PLUSD_Z : SimpleKeyword
        BasisSet
    CC_PVDZ : SimpleKeyword
        BasisSet
    CC_PVDZ_DK : SimpleKeyword
        BasisSet
    CC_PVDZ_DK3 : SimpleKeyword
        BasisSet
    CC_PVDZ_F12 : SimpleKeyword
        BasisSet
    CC_PVDZ_F12_CABS : SimpleKeyword
        BasisSet
    CC_PVDZ_F12_OPTRI : SimpleKeyword
        BasisSet
    CC_PVDZ_PP : SimpleKeyword
        BasisSet
    CC_PVDZ_PP_F12 : SimpleKeyword
        BasisSet
    CC_PVDZ_PP_F12_OPTRI : SimpleKeyword
        BasisSet
    CC_PVQ_PLUSD_Z : SimpleKeyword
        BasisSet
    CC_PVQZ : SimpleKeyword
        BasisSet
    CC_PVQZ_DK : SimpleKeyword
        BasisSet
    CC_PVQZ_DK3 : SimpleKeyword
        BasisSet
    CC_PVQZ_F12 : SimpleKeyword
        BasisSet
    CC_PVQZ_F12_CABS : SimpleKeyword
        BasisSet
    CC_PVQZ_F12_OPTRI : SimpleKeyword
        BasisSet
    CC_PVQZ_PP : SimpleKeyword
        BasisSet
    CC_PVQZ_PP_F12 : SimpleKeyword
        BasisSet
    CC_PVQZ_PP_F12_OPTRI : SimpleKeyword
        BasisSet
    CC_PVT_PLUSD_Z : SimpleKeyword
        BasisSet
    CC_PVTZ : SimpleKeyword
        BasisSet
    CC_PVTZ_DK : SimpleKeyword
        BasisSet
    CC_PVTZ_DK3 : SimpleKeyword
        BasisSet
    CC_PVTZ_F12 : SimpleKeyword
        BasisSet
    CC_PVTZ_F12_CABS : SimpleKeyword
        BasisSet
    CC_PVTZ_F12_OPTRI : SimpleKeyword
        BasisSet
    CC_PVTZ_PP : SimpleKeyword
        BasisSet
    CC_PVTZ_PP_F12 : SimpleKeyword
        BasisSet
    CC_PVTZ_PP_F12_OPTRI : SimpleKeyword
        BasisSet
    CC_PWCV5Z : SimpleKeyword
        BasisSet
    CC_PWCV5Z_DK : SimpleKeyword
        BasisSet
    CC_PWCV5Z_PP : SimpleKeyword
        BasisSet
    CC_PWCVDZ : SimpleKeyword
        BasisSet
    CC_PWCVDZ_DK : SimpleKeyword
        BasisSet
    CC_PWCVDZ_DK3 : SimpleKeyword
        BasisSet
    CC_PWCVDZ_PP : SimpleKeyword
        BasisSet
    CC_PWCVQZ : SimpleKeyword
        BasisSet
    CC_PWCVQZ_DK : SimpleKeyword
        BasisSet
    CC_PWCVQZ_DK3 : SimpleKeyword
        BasisSet
    CC_PWCVQZ_PP : SimpleKeyword
        BasisSet
    CC_PWCVTZ : SimpleKeyword
        BasisSet
    CC_PWCVTZ_DK : SimpleKeyword
        BasisSet
    CC_PWCVTZ_DK3 : SimpleKeyword
        BasisSet
    CC_PWCVTZ_PP : SimpleKeyword
        BasisSet
    CP : SimpleKeyword
        BasisSet
    CP_PPP : SimpleKeyword
        BasisSet
    CRENBL : SimpleKeyword
        BasisSet
    D95 : SimpleKeyword
        BasisSet
    D95P : SimpleKeyword
        BasisSet
    DEF_SV_P : SimpleKeyword
        BasisSet
    DEF_SVP : SimpleKeyword
        BasisSet
    DEF_TZVP : SimpleKeyword
        BasisSet
    DEF_TZVPP : SimpleKeyword
        BasisSet
    DEF2_MSVP : SimpleKeyword
        BasisSet
    DEF2_MTZVP : SimpleKeyword
        BasisSet
    DEF2_MTZVPP : SimpleKeyword
        BasisSet
    DEF2_QZVP : SimpleKeyword
        BasisSet
    DEF2_QZVPD : SimpleKeyword
        BasisSet
    DEF2_QZVPP : SimpleKeyword
        BasisSet
    DEF2_QZVPPD : SimpleKeyword
        BasisSet
    DEF2_SV_P : SimpleKeyword
        BasisSet
    DEF2_SVP : SimpleKeyword
        BasisSet
    DEF2_SVPD : SimpleKeyword
        BasisSet
    DEF2_TZVP : SimpleKeyword
        BasisSet
    DEF2_TZVP_F : SimpleKeyword
        BasisSet
    DEF2_TZVPD : SimpleKeyword
        BasisSet
    DEF2_TZVPP : SimpleKeyword
        BasisSet
    DEF2_TZVPPD : SimpleKeyword
        BasisSet
    DHF_QZVP : SimpleKeyword
        BasisSet
    DHF_QZVP_2C : SimpleKeyword
        BasisSet
    DHF_QZVPP : SimpleKeyword
        BasisSet
    DHF_QZVPP_2C : SimpleKeyword
        BasisSet
    DHF_SV_P : SimpleKeyword
        BasisSet
    DHF_SV_P_2C : SimpleKeyword
        BasisSet
    DHF_SVP : SimpleKeyword
        BasisSet
    DHF_SVP_2C : SimpleKeyword
        BasisSet
    DHF_TZVP : SimpleKeyword
        BasisSet
    DHF_TZVP_2C : SimpleKeyword
        BasisSet
    DHF_TZVPP : SimpleKeyword
        BasisSet
    DHF_TZVPP_2C : SimpleKeyword
        BasisSet
    DKH_DEF2_QZVPP : SimpleKeyword
        BasisSet
    DKH_DEF2_SV_P : SimpleKeyword
        BasisSet
    DKH_DEF2_SVP : SimpleKeyword
        BasisSet
    DKH_DEF2_TZVP : SimpleKeyword
        BasisSet
    DKH_DEF2_TZVP_F : SimpleKeyword
        BasisSet
    DKH_DEF2_TZVPP : SimpleKeyword
        BasisSet
    DKH_MA_DEF2_QZVPP : SimpleKeyword
        BasisSet
    DKH_MA_DEF2_SV_P : SimpleKeyword
        BasisSet
    DKH_MA_DEF2_SVP : SimpleKeyword
        BasisSet
    DKH_MA_DEF2_TZVP : SimpleKeyword
        BasisSet
    DKH_MA_DEF2_TZVP_F : SimpleKeyword
        BasisSet
    DKH_MA_DEF2_TZVPP : SimpleKeyword
        BasisSet
    DKH_QZVP : SimpleKeyword
        BasisSet
    DKH_QZVPP : SimpleKeyword
        BasisSet
    DKH_SV_P : SimpleKeyword
        BasisSet
    DKH_SVP : SimpleKeyword
        BasisSet
    DKH_TZV_P : SimpleKeyword
        BasisSet
    DKH_TZVP : SimpleKeyword
        BasisSet
    DKH_TZVPP : SimpleKeyword
        BasisSet
    EPR_II : SimpleKeyword
        BasisSet
    EPR_III : SimpleKeyword
        BasisSet
    GFN1BASIS : SimpleKeyword
        BasisSet
    GFN2BASIS : SimpleKeyword
        BasisSet
    HAV_5PLUSD_Z : SimpleKeyword
        BasisSet
    HAV_QPLUSD_Z : SimpleKeyword
        BasisSet
    HAV_TPLUSD_Z : SimpleKeyword
        BasisSet
    HAV5Z_PLUSD : SimpleKeyword
        BasisSet
    HAVQZ_PLUSD : SimpleKeyword
        BasisSet
    HAVTZ_PLUSD : SimpleKeyword
        BasisSet
    HGBS_5 : SimpleKeyword
        BasisSet
    HGBS_7 : SimpleKeyword
        BasisSet
    HGBS_9 : SimpleKeyword
        BasisSet
    HGBSP1_5 : SimpleKeyword
        BasisSet
    HGBSP1_7 : SimpleKeyword
        BasisSet
    HGBSP1_9 : SimpleKeyword
        BasisSet
    HGBSP2_5 : SimpleKeyword
        BasisSet
    HGBSP2_7 : SimpleKeyword
        BasisSet
    HGBSP2_9 : SimpleKeyword
        BasisSet
    HGBSP3_5 : SimpleKeyword
        BasisSet
    HGBSP3_7 : SimpleKeyword
        BasisSet
    HGBSP3_9 : SimpleKeyword
        BasisSet
    IGLO_II : SimpleKeyword
        BasisSet
    IGLO_III : SimpleKeyword
        BasisSet
    JUL_CC_PV_DPLUSD_Z : SimpleKeyword
        BasisSet
    JUL_CC_PV_QPLUSD_Z : SimpleKeyword
        BasisSet
    JUL_CC_PV_TPLUSD_Z : SimpleKeyword
        BasisSet
    JUN_CC_PV_DPLUSD_Z : SimpleKeyword
        BasisSet
    JUN_CC_PV_QPLUSD_Z : SimpleKeyword
        BasisSet
    JUN_CC_PV_TPLUSD_Z : SimpleKeyword
        BasisSet
    LANL08 : SimpleKeyword
        BasisSet
    LANL08_F : SimpleKeyword
        BasisSet
    LANL2DZ : SimpleKeyword
        BasisSet
    LANL2TZ : SimpleKeyword
        BasisSet
    LANL2TZ_F : SimpleKeyword
        BasisSet
    M6_31G : SimpleKeyword
        BasisSet
    M6_31GSTAR : SimpleKeyword
        BasisSet
    MA_DEF_TZVP : SimpleKeyword
        BasisSet
    MA_DEF2_MSVP : SimpleKeyword
        BasisSet
    MA_DEF2_QZVP : SimpleKeyword
        BasisSet
    MA_DEF2_QZVPP : SimpleKeyword
        BasisSet
    MA_DEF2_SV_P : SimpleKeyword
        BasisSet
    MA_DEF2_SVP : SimpleKeyword
        BasisSet
    MA_DEF2_TZVP : SimpleKeyword
        BasisSet
    MA_DEF2_TZVP_F : SimpleKeyword
        BasisSet
    MA_DEF2_TZVPP : SimpleKeyword
        BasisSet
    MA_DKH_DEF2_QZVPP : SimpleKeyword
        BasisSet
    MA_DKH_DEF2_SV_P : SimpleKeyword
        BasisSet
    MA_DKH_DEF2_SVP : SimpleKeyword
        BasisSet
    MA_DKH_DEF2_TZVP : SimpleKeyword
        BasisSet
    MA_DKH_DEF2_TZVP_F : SimpleKeyword
        BasisSet
    MA_DKH_DEF2_TZVPP : SimpleKeyword
        BasisSet
    MA_ZORA_DEF2_QZVPP : SimpleKeyword
        BasisSet
    MA_ZORA_DEF2_SV_P : SimpleKeyword
        BasisSet
    MA_ZORA_DEF2_SVP : SimpleKeyword
        BasisSet
    MA_ZORA_DEF2_TZVP : SimpleKeyword
        BasisSet
    MA_ZORA_DEF2_TZVP_F : SimpleKeyword
        BasisSet
    MA_ZORA_DEF2_TZVPP : SimpleKeyword
        BasisSet
    MAUG_CC_PV_DPLUSD_Z : SimpleKeyword
        BasisSet
    MAUG_CC_PV_QPLUSD_Z : SimpleKeyword
        BasisSet
    MAUG_CC_PV_TPLUSD_Z : SimpleKeyword
        BasisSet
    MAY_CC_PV_QPLUSD_Z : SimpleKeyword
        BasisSet
    MAY_CC_PV_TPLUSD_Z : SimpleKeyword
        BasisSet
    MIDI : SimpleKeyword
        BasisSet
    MINAO : SimpleKeyword
        BasisSet
    MINAO_AUTO_PP : SimpleKeyword
        BasisSet
    MINI : SimpleKeyword
        BasisSet
    MINIS : SimpleKeyword
        BasisSet
    MINIX : SimpleKeyword
        BasisSet
    OLD_DKH_SV_P : SimpleKeyword
        BasisSet
    OLD_DKH_SVP : SimpleKeyword
        BasisSet
    OLD_DKH_TZV_P : SimpleKeyword
        BasisSet
    OLD_DKH_TZVP : SimpleKeyword
        BasisSet
    OLD_DKH_TZVPP : SimpleKeyword
        BasisSet
    OLD_SV : SimpleKeyword
        BasisSet
    OLD_SV_P : SimpleKeyword
        BasisSet
    OLD_SVP : SimpleKeyword
        BasisSet
    OLD_TZV : SimpleKeyword
        BasisSet
    OLD_TZV_P : SimpleKeyword
        BasisSet
    OLD_TZVP : SimpleKeyword
        BasisSet
    OLD_TZVPP : SimpleKeyword
        BasisSet
    OLD_ZORA_SV_P : SimpleKeyword
        BasisSet
    OLD_ZORA_SVP : SimpleKeyword
        BasisSet
    OLD_ZORA_TZV_P : SimpleKeyword
        BasisSet
    OLD_ZORA_TZVP : SimpleKeyword
        BasisSet
    OLD_ZORA_TZVPP : SimpleKeyword
        BasisSet
    PARTRIDGE_1 : SimpleKeyword
        BasisSet
    PARTRIDGE_2 : SimpleKeyword
        BasisSet
    PARTRIDGE_3 : SimpleKeyword
        BasisSet
    PARTRIDGE_4 : SimpleKeyword
        BasisSet
    PC_0 : SimpleKeyword
        BasisSet
    PC_1 : SimpleKeyword
        BasisSet
    PC_2 : SimpleKeyword
        BasisSet
    PC_3 : SimpleKeyword
        BasisSet
    PC_4 : SimpleKeyword
        BasisSet
    PCH_1 : SimpleKeyword
        BasisSet
    PCH_2 : SimpleKeyword
        BasisSet
    PCH_3 : SimpleKeyword
        BasisSet
    PCH_4 : SimpleKeyword
        BasisSet
    PCJ_0 : SimpleKeyword
        BasisSet
    PCJ_1 : SimpleKeyword
        BasisSet
    PCJ_2 : SimpleKeyword
        BasisSet
    PCJ_3 : SimpleKeyword
        BasisSet
    PCJ_4 : SimpleKeyword
        BasisSet
    PCSEG_0 : SimpleKeyword
        BasisSet
    PCSEG_1 : SimpleKeyword
        BasisSet
    PCSEG_2 : SimpleKeyword
        BasisSet
    PCSEG_3 : SimpleKeyword
        BasisSet
    PCSEG_4 : SimpleKeyword
        BasisSet
    PCSSEG_0 : SimpleKeyword
        BasisSet
    PCSSEG_1 : SimpleKeyword
        BasisSet
    PCSSEG_2 : SimpleKeyword
        BasisSet
    PCSSEG_3 : SimpleKeyword
        BasisSet
    PCSSEG_4 : SimpleKeyword
        BasisSet
    PCX_1 : SimpleKeyword
        BasisSet
    PCX_2 : SimpleKeyword
        BasisSet
    PCX_3 : SimpleKeyword
        BasisSet
    PCX_4 : SimpleKeyword
        BasisSet
    QZVP : SimpleKeyword
        BasisSet
    QZVPP : SimpleKeyword
        BasisSet
    SAPPORO_DKH3_DZP_2012 : SimpleKeyword
        BasisSet
    SAPPORO_DKH3_QZP_2012 : SimpleKeyword
        BasisSet
    SAPPORO_DKH3_TZP_2012 : SimpleKeyword
        BasisSet
    SAPPORO_DZP_2012 : SimpleKeyword
        BasisSet
    SAPPORO_QZP_2012 : SimpleKeyword
        BasisSet
    SAPPORO_TZP_2012 : SimpleKeyword
        BasisSet
    SARC_DKH_SVP : SimpleKeyword
        BasisSet
    SARC_DKH_TZVP : SimpleKeyword
        BasisSet
    SARC_DKH_TZVPP : SimpleKeyword
        BasisSet
    SARC_ZORA_SVP : SimpleKeyword
        BasisSet
    SARC_ZORA_TZVP : SimpleKeyword
        BasisSet
    SARC_ZORA_TZVPP : SimpleKeyword
        BasisSet
    SARC2_DKH_QZV : SimpleKeyword
        BasisSet
    SARC2_DKH_QZVP : SimpleKeyword
        BasisSet
    SARC2_ZORA_QZV : SimpleKeyword
        BasisSet
    SARC2_ZORA_QZVP : SimpleKeyword
        BasisSet
    SAUG_ANO_PV5Z : SimpleKeyword
        BasisSet
    SAUG_ANO_PVDZ : SimpleKeyword
        BasisSet
    SAUG_ANO_PVQZ : SimpleKeyword
        BasisSet
    SAUG_ANO_PVTZ : SimpleKeyword
        BasisSet
    STO_3G : SimpleKeyword
        BasisSet
    SV : SimpleKeyword
        BasisSet
    SV_P : SimpleKeyword
        BasisSet
    SVP : SimpleKeyword
        BasisSet
    TZV : SimpleKeyword
        BasisSet
    TZV_P : SimpleKeyword
        BasisSet
    TZVP : SimpleKeyword
        BasisSet
    TZVPP : SimpleKeyword
        BasisSet
    UGBS : SimpleKeyword
        BasisSet
    VDZP : SimpleKeyword
        BasisSet
    W1_DZ : SimpleKeyword
        BasisSet
    W1_MTSMALL : SimpleKeyword
        BasisSet
    W1_OPT : SimpleKeyword
        BasisSet
    W1_QZ : SimpleKeyword
        BasisSet
    W1_TZ : SimpleKeyword
        BasisSet
    WACHTERSPLUSF : SimpleKeyword
        BasisSet
    X2C_QZVPALL : SimpleKeyword
        BasisSet
    X2C_QZVPALL_2C : SimpleKeyword
        BasisSet
    X2C_QZVPALL_2C_S : SimpleKeyword
        BasisSet
    X2C_QZVPALL_S : SimpleKeyword
        BasisSet
    X2C_QZVPPALL : SimpleKeyword
        BasisSet
    X2C_QZVPPALL_2C : SimpleKeyword
        BasisSet
    X2C_QZVPPALL_2C_S : SimpleKeyword
        BasisSet
    X2C_QZVPPALL_S : SimpleKeyword
        BasisSet
    X2C_SV_P_ALL : SimpleKeyword
        BasisSet
    X2C_SV_P_ALL_2C : SimpleKeyword
        BasisSet
    X2C_SV_P_ALL_S : SimpleKeyword
        BasisSet
    X2C_SVPALL : SimpleKeyword
        BasisSet
    X2C_SVPALL_2C : SimpleKeyword
        BasisSet
    X2C_SVPALL_S : SimpleKeyword
        BasisSet
    X2C_TZVPALL : SimpleKeyword
        BasisSet
    X2C_TZVPALL_2C : SimpleKeyword
        BasisSet
    X2C_TZVPALL_S : SimpleKeyword
        BasisSet
    X2C_TZVPPALL : SimpleKeyword
        BasisSet
    X2C_TZVPPALL_2C : SimpleKeyword
        BasisSet
    X2C_TZVPPALL_S : SimpleKeyword
        BasisSet
    ZORA_DEF2_QZVPP : SimpleKeyword
        BasisSet
    ZORA_DEF2_SV_P : SimpleKeyword
        BasisSet
    ZORA_DEF2_SVP : SimpleKeyword
        BasisSet
    ZORA_DEF2_TZVP : SimpleKeyword
        BasisSet
    ZORA_DEF2_TZVP_F : SimpleKeyword
        BasisSet
    ZORA_DEF2_TZVPP : SimpleKeyword
        BasisSet
    ZORA_MA_DEF2_QZVPP : SimpleKeyword
        BasisSet
    ZORA_MA_DEF2_SV_P : SimpleKeyword
        BasisSet
    ZORA_MA_DEF2_SVP : SimpleKeyword
        BasisSet
    ZORA_MA_DEF2_TZVP : SimpleKeyword
        BasisSet
    ZORA_MA_DEF2_TZVP_F : SimpleKeyword
        BasisSet
    ZORA_MA_DEF2_TZVPP : SimpleKeyword
        BasisSet
    ZORA_QZVP : SimpleKeyword
        BasisSet
    ZORA_QZVPP : SimpleKeyword
        BasisSet
    ZORA_SV_P : SimpleKeyword
        BasisSet
    ZORA_SVP : SimpleKeyword
        BasisSet
    ZORA_TZV_P : SimpleKeyword
        BasisSet
    ZORA_TZVP : SimpleKeyword
        BasisSet
    ZORA_TZVPP : SimpleKeyword
        BasisSet
    """

    G3_21G = SimpleKeyword("3-21g")
    G3_21GSP = SimpleKeyword("3-21gsp")
    G4_22GSP = SimpleKeyword("4-22gsp")
    G6_31PLUSPLUSG_2D_2P = SimpleKeyword("6-31++g(2d,2p)")
    G6_31PLUSPLUSG_2D_P = SimpleKeyword("6-31++g(2d,p)")
    G6_31PLUSPLUSG_2DF_2P = SimpleKeyword("6-31++g(2df,2p)")
    G6_31PLUSPLUSG_2DF_2PD = SimpleKeyword("6-31++g(2df,2pd)")
    G6_31PLUSPLUSG_D_P = SimpleKeyword("6-31++g(d,p)")
    G6_31PLUSPLUSGSTARSTAR = SimpleKeyword("6-31++g**")
    G6_31PLUSG_2D_2P = SimpleKeyword("6-31+g(2d,2p)")
    G6_31PLUSG_2D_P = SimpleKeyword("6-31+g(2d,p)")
    G6_31PLUSG_2D = SimpleKeyword("6-31+g(2d)")
    G6_31PLUSG_2DF_2P = SimpleKeyword("6-31+g(2df,2p)")
    G6_31PLUSG_2DF_2PD = SimpleKeyword("6-31+g(2df,2pd)")
    G6_31PLUSG_2DF = SimpleKeyword("6-31+g(2df)")
    G6_31PLUSG_D_P = SimpleKeyword("6-31+g(d,p)")
    G6_31PLUSG_D = SimpleKeyword("6-31+g(d)")
    G6_31PLUSGSTAR = SimpleKeyword("6-31+g*")
    G6_31PLUSGSTARSTAR = SimpleKeyword("6-31+g**")
    G6_311PLUSPLUSG_2D_2P = SimpleKeyword("6-311++g(2d,2p)")
    G6_311PLUSPLUSG_2D_P = SimpleKeyword("6-311++g(2d,p)")
    G6_311PLUSPLUSG_2DF_2P = SimpleKeyword("6-311++g(2df,2p)")
    G6_311PLUSPLUSG_2DF_2PD = SimpleKeyword("6-311++g(2df,2pd)")
    G6_311PLUSPLUSG_3DF_3PD = SimpleKeyword("6-311++g(3df,3pd)")
    G6_311PLUSPLUSG_D_P = SimpleKeyword("6-311++g(d,p)")
    G6_311PLUSPLUSGSTARSTAR = SimpleKeyword("6-311++g**")
    G6_311PLUSG_2D_2P = SimpleKeyword("6-311+g(2d,2p)")
    G6_311PLUSG_2D_P = SimpleKeyword("6-311+g(2d,p)")
    G6_311PLUSG_2D = SimpleKeyword("6-311+g(2d)")
    G6_311PLUSG_2DF_2P = SimpleKeyword("6-311+g(2df,2p)")
    G6_311PLUSG_2DF_2PD = SimpleKeyword("6-311+g(2df,2pd)")
    G6_311PLUSG_2DF = SimpleKeyword("6-311+g(2df)")
    G6_311PLUSG_3DF_2P = SimpleKeyword("6-311+g(3df,2p)")
    G6_311PLUSG_3DF_3PD = SimpleKeyword("6-311+g(3df,3pd)")
    G6_311PLUSG_3DF = SimpleKeyword("6-311+g(3df)")
    G6_311PLUSG_D_P = SimpleKeyword("6-311+g(d,p)")
    G6_311PLUSG_D = SimpleKeyword("6-311+g(d)")
    G6_311PLUSGSTAR = SimpleKeyword("6-311+g*")
    G6_311PLUSGSTARSTAR = SimpleKeyword("6-311+g**")
    G6_311G = SimpleKeyword("6-311g")
    G6_311G_2D_2P = SimpleKeyword("6-311g(2d,2p)")
    G6_311G_2D_P = SimpleKeyword("6-311g(2d,p)")
    G6_311G_2D = SimpleKeyword("6-311g(2d)")
    G6_311G_2DF_2P = SimpleKeyword("6-311g(2df,2p)")
    G6_311G_2DF_2PD = SimpleKeyword("6-311g(2df,2pd)")
    G6_311G_2DF = SimpleKeyword("6-311g(2df)")
    G6_311G_3DF_3PD = SimpleKeyword("6-311g(3df,3pd)")
    G6_311G_3DF = SimpleKeyword("6-311g(3df)")
    G6_311G_D_P = SimpleKeyword("6-311g(d,p)")
    G6_311G_D = SimpleKeyword("6-311g(d)")
    G6_311GSTAR = SimpleKeyword("6-311g*")
    G6_311GSTARSTAR = SimpleKeyword("6-311g**")
    G6_31G = SimpleKeyword("6-31g")
    G6_31G_2D_2P = SimpleKeyword("6-31g(2d,2p)")
    G6_31G_2D_P = SimpleKeyword("6-31g(2d,p)")
    G6_31G_2D = SimpleKeyword("6-31g(2d)")
    G6_31G_2DF_2P = SimpleKeyword("6-31g(2df,2p)")
    G6_31G_2DF_2PD = SimpleKeyword("6-31g(2df,2pd)")
    G6_31G_2DF = SimpleKeyword("6-31g(2df)")
    G6_31G_D_P = SimpleKeyword("6-31g(d,p)")
    G6_31G_D = SimpleKeyword("6-31g(d)")
    G6_31GSTAR = SimpleKeyword("6-31g*")
    G6_31GSTARSTAR = SimpleKeyword("6-31g**")
    AHGBS_5 = SimpleKeyword("ahgbs-5")
    AHGBS_7 = SimpleKeyword("ahgbs-7")
    AHGBS_9 = SimpleKeyword("ahgbs-9")
    AHGBSP1_5 = SimpleKeyword("ahgbsp1-5")
    AHGBSP1_7 = SimpleKeyword("ahgbsp1-7")
    AHGBSP1_9 = SimpleKeyword("ahgbsp1-9")
    AHGBSP2_5 = SimpleKeyword("ahgbsp2-5")
    AHGBSP2_7 = SimpleKeyword("ahgbsp2-7")
    AHGBSP2_9 = SimpleKeyword("ahgbsp2-9")
    AHGBSP3_5 = SimpleKeyword("ahgbsp3-5")
    AHGBSP3_7 = SimpleKeyword("ahgbsp3-7")
    AHGBSP3_9 = SimpleKeyword("ahgbsp3-9")
    ANO_PC_0 = SimpleKeyword("ano-pc-0")
    ANO_PC_0_POL = SimpleKeyword("ano-pc-0-pol")
    ANO_PV5Z = SimpleKeyword("ano-pv5z")
    ANO_PV6Z = SimpleKeyword("ano-pv6z")
    ANO_PVDZ = SimpleKeyword("ano-pvdz")
    ANO_PVQZ = SimpleKeyword("ano-pvqz")
    ANO_PVTZ = SimpleKeyword("ano-pvtz")
    ANO_RCC_DZP = SimpleKeyword("ano-rcc-dzp")
    ANO_RCC_FULL = SimpleKeyword("ano-rcc-full")
    ANO_RCC_MB = SimpleKeyword("ano-rcc-mb")
    ANO_RCC_QZP = SimpleKeyword("ano-rcc-qzp")
    ANO_RCC_TZP = SimpleKeyword("ano-rcc-tzp")
    ANO_SZ = SimpleKeyword("ano-sz")
    ANO_SZ_DKH_SMALL = SimpleKeyword("ano-sz-dkh-small")
    APR_CC_PV_QPLUSD_Z = SimpleKeyword("apr-cc-pv(q+d)z")
    AUG_ANO_PV5Z = SimpleKeyword("aug-ano-pv5z")
    AUG_ANO_PVDZ = SimpleKeyword("aug-ano-pvdz")
    AUG_ANO_PVQZ = SimpleKeyword("aug-ano-pvqz")
    AUG_ANO_PVTZ = SimpleKeyword("aug-ano-pvtz")
    AUG_CC_PCV5Z = SimpleKeyword("aug-cc-pcv5z")
    AUG_CC_PCV5Z_PP = SimpleKeyword("aug-cc-pcv5z-pp")
    AUG_CC_PCV6Z = SimpleKeyword("aug-cc-pcv6z")
    AUG_CC_PCVDZ = SimpleKeyword("aug-cc-pcvdz")
    AUG_CC_PCVDZ_PP = SimpleKeyword("aug-cc-pcvdz-pp")
    AUG_CC_PCVQZ = SimpleKeyword("aug-cc-pcvqz")
    AUG_CC_PCVQZ_PP = SimpleKeyword("aug-cc-pcvqz-pp")
    AUG_CC_PCVTZ = SimpleKeyword("aug-cc-pcvtz")
    AUG_CC_PCVTZ_PP = SimpleKeyword("aug-cc-pcvtz-pp")
    AUG_CC_PV5_PLUSD_Z = SimpleKeyword("aug-cc-pv5(+d)z")
    AUG_CC_PV5Z = SimpleKeyword("aug-cc-pv5z")
    AUG_CC_PV5Z_DK = SimpleKeyword("aug-cc-pv5z-dk")
    AUG_CC_PV5Z_PP = SimpleKeyword("aug-cc-pv5z-pp")
    AUG_CC_PV5Z_PP_OPTRI = SimpleKeyword("aug-cc-pv5z-pp-optri")
    AUG_CC_PV6_PLUSD_Z = SimpleKeyword("aug-cc-pv6(+d)z")
    AUG_CC_PV6Z = SimpleKeyword("aug-cc-pv6z")
    AUG_CC_PV7Z = SimpleKeyword("aug-cc-pv7z")
    AUG_CC_PVD_PLUSD_Z = SimpleKeyword("aug-cc-pvd(+d)z")
    AUG_CC_PVDZ = SimpleKeyword("aug-cc-pvdz")
    AUG_CC_PVDZ_DK = SimpleKeyword("aug-cc-pvdz-dk")
    AUG_CC_PVDZ_PP = SimpleKeyword("aug-cc-pvdz-pp")
    AUG_CC_PVDZ_PP_OPTRI = SimpleKeyword("aug-cc-pvdz-pp-optri")
    AUG_CC_PVQ_PLUSD_Z = SimpleKeyword("aug-cc-pvq(+d)z")
    AUG_CC_PVQZ = SimpleKeyword("aug-cc-pvqz")
    AUG_CC_PVQZ_DK = SimpleKeyword("aug-cc-pvqz-dk")
    AUG_CC_PVQZ_PP = SimpleKeyword("aug-cc-pvqz-pp")
    AUG_CC_PVQZ_PP_OPTRI = SimpleKeyword("aug-cc-pvqz-pp-optri")
    AUG_CC_PVT_PLUSD_Z = SimpleKeyword("aug-cc-pvt(+d)z")
    AUG_CC_PVTZ = SimpleKeyword("aug-cc-pvtz")
    AUG_CC_PVTZ_DK = SimpleKeyword("aug-cc-pvtz-dk")
    AUG_CC_PVTZ_J = SimpleKeyword("aug-cc-pvtz-j")
    AUG_CC_PVTZ_PP = SimpleKeyword("aug-cc-pvtz-pp")
    AUG_CC_PVTZ_PP_OPTRI = SimpleKeyword("aug-cc-pvtz-pp-optri")
    AUG_CC_PWCV5Z = SimpleKeyword("aug-cc-pwcv5z")
    AUG_CC_PWCV5Z_DK = SimpleKeyword("aug-cc-pwcv5z-dk")
    AUG_CC_PWCV5Z_PP = SimpleKeyword("aug-cc-pwcv5z-pp")
    AUG_CC_PWCV5Z_PP_OPTRI = SimpleKeyword("aug-cc-pwcv5z-pp-optri")
    AUG_CC_PWCVDZ = SimpleKeyword("aug-cc-pwcvdz")
    AUG_CC_PWCVDZ_DK = SimpleKeyword("aug-cc-pwcvdz-dk")
    AUG_CC_PWCVDZ_PP = SimpleKeyword("aug-cc-pwcvdz-pp")
    AUG_CC_PWCVDZ_PP_OPTRI = SimpleKeyword("aug-cc-pwcvdz-pp-optri")
    AUG_CC_PWCVQZ = SimpleKeyword("aug-cc-pwcvqz")
    AUG_CC_PWCVQZ_DK = SimpleKeyword("aug-cc-pwcvqz-dk")
    AUG_CC_PWCVQZ_PP = SimpleKeyword("aug-cc-pwcvqz-pp")
    AUG_CC_PWCVQZ_PP_OPTRI = SimpleKeyword("aug-cc-pwcvqz-pp-optri")
    AUG_CC_PWCVTZ = SimpleKeyword("aug-cc-pwcvtz")
    AUG_CC_PWCVTZ_DK = SimpleKeyword("aug-cc-pwcvtz-dk")
    AUG_CC_PWCVTZ_PP = SimpleKeyword("aug-cc-pwcvtz-pp")
    AUG_CC_PWCVTZ_PP_OPTRI = SimpleKeyword("aug-cc-pwcvtz-pp-optri")
    AUG_PC_0 = SimpleKeyword("aug-pc-0")
    AUG_PC_1 = SimpleKeyword("aug-pc-1")
    AUG_PC_2 = SimpleKeyword("aug-pc-2")
    AUG_PC_3 = SimpleKeyword("aug-pc-3")
    AUG_PC_4 = SimpleKeyword("aug-pc-4")
    AUG_PCH_1 = SimpleKeyword("aug-pch-1")
    AUG_PCH_2 = SimpleKeyword("aug-pch-2")
    AUG_PCH_3 = SimpleKeyword("aug-pch-3")
    AUG_PCH_4 = SimpleKeyword("aug-pch-4")
    AUG_PCJ_0 = SimpleKeyword("aug-pcj-0")
    AUG_PCJ_1 = SimpleKeyword("aug-pcj-1")
    AUG_PCJ_2 = SimpleKeyword("aug-pcj-2")
    AUG_PCJ_3 = SimpleKeyword("aug-pcj-3")
    AUG_PCJ_4 = SimpleKeyword("aug-pcj-4")
    AUG_PCSEG_0 = SimpleKeyword("aug-pcseg-0")
    AUG_PCSEG_1 = SimpleKeyword("aug-pcseg-1")
    AUG_PCSEG_2 = SimpleKeyword("aug-pcseg-2")
    AUG_PCSEG_3 = SimpleKeyword("aug-pcseg-3")
    AUG_PCSEG_4 = SimpleKeyword("aug-pcseg-4")
    AUG_PCSSEG_0 = SimpleKeyword("aug-pcsseg-0")
    AUG_PCSSEG_1 = SimpleKeyword("aug-pcsseg-1")
    AUG_PCSSEG_2 = SimpleKeyword("aug-pcsseg-2")
    AUG_PCSSEG_3 = SimpleKeyword("aug-pcsseg-3")
    AUG_PCSSEG_4 = SimpleKeyword("aug-pcsseg-4")
    AUG_PCX_1 = SimpleKeyword("aug-pcx-1")
    AUG_PCX_2 = SimpleKeyword("aug-pcx-2")
    AUG_PCX_3 = SimpleKeyword("aug-pcx-3")
    AUG_PCX_4 = SimpleKeyword("aug-pcx-4")
    CC_PCV5Z = SimpleKeyword("cc-pcv5z")
    CC_PCV5Z_PP = SimpleKeyword("cc-pcv5z-pp")
    CC_PCV6Z = SimpleKeyword("cc-pcv6z")
    CC_PCVDZ = SimpleKeyword("cc-pcvdz")
    CC_PCVDZ_F12 = SimpleKeyword("cc-pcvdz-f12")
    CC_PCVDZ_F12_OPTRI = SimpleKeyword("cc-pcvdz-f12-optri")
    CC_PCVDZ_PP = SimpleKeyword("cc-pcvdz-pp")
    CC_PCVQZ = SimpleKeyword("cc-pcvqz")
    CC_PCVQZ_F12 = SimpleKeyword("cc-pcvqz-f12")
    CC_PCVQZ_F12_OPTRI = SimpleKeyword("cc-pcvqz-f12-optri")
    CC_PCVQZ_PP = SimpleKeyword("cc-pcvqz-pp")
    CC_PCVTZ = SimpleKeyword("cc-pcvtz")
    CC_PCVTZ_F12 = SimpleKeyword("cc-pcvtz-f12")
    CC_PCVTZ_F12_OPTRI = SimpleKeyword("cc-pcvtz-f12-optri")
    CC_PCVTZ_PP = SimpleKeyword("cc-pcvtz-pp")
    CC_PV5_PLUSD_Z = SimpleKeyword("cc-pv5(+d)z")
    CC_PV5Z = SimpleKeyword("cc-pv5z")
    CC_PV5Z_DK = SimpleKeyword("cc-pv5z-dk")
    CC_PV5Z_PP = SimpleKeyword("cc-pv5z-pp")
    CC_PV6Z = SimpleKeyword("cc-pv6z")
    CC_PV7Z = SimpleKeyword("cc-pv7z")
    CC_PV8Z = SimpleKeyword("cc-pv8z")
    CC_PVD_PLUSD_Z = SimpleKeyword("cc-pvd(+d)z")
    CC_PVDZ = SimpleKeyword("cc-pvdz")
    CC_PVDZ_DK = SimpleKeyword("cc-pvdz-dk")
    CC_PVDZ_DK3 = SimpleKeyword("cc-pvdz-dk3")
    CC_PVDZ_F12 = SimpleKeyword("cc-pvdz-f12")
    CC_PVDZ_F12_CABS = SimpleKeyword("cc-pvdz-f12-cabs")
    CC_PVDZ_F12_OPTRI = SimpleKeyword("cc-pvdz-f12-optri")
    CC_PVDZ_PP = SimpleKeyword("cc-pvdz-pp")
    CC_PVDZ_PP_F12 = SimpleKeyword("cc-pvdz-pp-f12")
    CC_PVDZ_PP_F12_OPTRI = SimpleKeyword("cc-pvdz-pp-f12-optri")
    CC_PVQ_PLUSD_Z = SimpleKeyword("cc-pvq(+d)z")
    CC_PVQZ = SimpleKeyword("cc-pvqz")
    CC_PVQZ_DK = SimpleKeyword("cc-pvqz-dk")
    CC_PVQZ_DK3 = SimpleKeyword("cc-pvqz-dk3")
    CC_PVQZ_F12 = SimpleKeyword("cc-pvqz-f12")
    CC_PVQZ_F12_CABS = SimpleKeyword("cc-pvqz-f12-cabs")
    CC_PVQZ_F12_OPTRI = SimpleKeyword("cc-pvqz-f12-optri")
    CC_PVQZ_PP = SimpleKeyword("cc-pvqz-pp")
    CC_PVQZ_PP_F12 = SimpleKeyword("cc-pvqz-pp-f12")
    CC_PVQZ_PP_F12_OPTRI = SimpleKeyword("cc-pvqz-pp-f12-optri")
    CC_PVT_PLUSD_Z = SimpleKeyword("cc-pvt(+d)z")
    CC_PVTZ = SimpleKeyword("cc-pvtz")
    CC_PVTZ_DK = SimpleKeyword("cc-pvtz-dk")
    CC_PVTZ_DK3 = SimpleKeyword("cc-pvtz-dk3")
    CC_PVTZ_F12 = SimpleKeyword("cc-pvtz-f12")
    CC_PVTZ_F12_CABS = SimpleKeyword("cc-pvtz-f12-cabs")
    CC_PVTZ_F12_OPTRI = SimpleKeyword("cc-pvtz-f12-optri")
    CC_PVTZ_PP = SimpleKeyword("cc-pvtz-pp")
    CC_PVTZ_PP_F12 = SimpleKeyword("cc-pvtz-pp-f12")
    CC_PVTZ_PP_F12_OPTRI = SimpleKeyword("cc-pvtz-pp-f12-optri")
    CC_PWCV5Z = SimpleKeyword("cc-pwcv5z")
    CC_PWCV5Z_DK = SimpleKeyword("cc-pwcv5z-dk")
    CC_PWCV5Z_PP = SimpleKeyword("cc-pwcv5z-pp")
    CC_PWCVDZ = SimpleKeyword("cc-pwcvdz")
    CC_PWCVDZ_DK = SimpleKeyword("cc-pwcvdz-dk")
    CC_PWCVDZ_DK3 = SimpleKeyword("cc-pwcvdz-dk3")
    CC_PWCVDZ_PP = SimpleKeyword("cc-pwcvdz-pp")
    CC_PWCVQZ = SimpleKeyword("cc-pwcvqz")
    CC_PWCVQZ_DK = SimpleKeyword("cc-pwcvqz-dk")
    CC_PWCVQZ_DK3 = SimpleKeyword("cc-pwcvqz-dk3")
    CC_PWCVQZ_PP = SimpleKeyword("cc-pwcvqz-pp")
    CC_PWCVTZ = SimpleKeyword("cc-pwcvtz")
    CC_PWCVTZ_DK = SimpleKeyword("cc-pwcvtz-dk")
    CC_PWCVTZ_DK3 = SimpleKeyword("cc-pwcvtz-dk3")
    CC_PWCVTZ_PP = SimpleKeyword("cc-pwcvtz-pp")
    CP = SimpleKeyword("cp")
    CP_PPP = SimpleKeyword("cp(ppp)")
    CRENBL = SimpleKeyword("crenbl")
    D95 = SimpleKeyword("d95")
    D95P = SimpleKeyword("d95p")
    DEF_SV_P = SimpleKeyword("def-sv(p)")
    DEF_SVP = SimpleKeyword("def-svp")
    DEF_TZVP = SimpleKeyword("def-tzvp")
    DEF_TZVPP = SimpleKeyword("def-tzvpp")
    DEF2_MSVP = SimpleKeyword("def2-msvp")
    DEF2_MTZVP = SimpleKeyword("def2-mtzvp")
    DEF2_MTZVPP = SimpleKeyword("def2-mtzvpp")
    DEF2_QZVP = SimpleKeyword("def2-qzvp")
    DEF2_QZVPD = SimpleKeyword("def2-qzvpd")
    DEF2_QZVPP = SimpleKeyword("def2-qzvpp")
    DEF2_QZVPPD = SimpleKeyword("def2-qzvppd")
    DEF2_SV_P = SimpleKeyword("def2-sv(p)")
    DEF2_SVP = SimpleKeyword("def2-svp")
    DEF2_SVPD = SimpleKeyword("def2-svpd")
    DEF2_TZVP = SimpleKeyword("def2-tzvp")
    DEF2_TZVP_F = SimpleKeyword("def2-tzvp(-f)")
    DEF2_TZVPD = SimpleKeyword("def2-tzvpd")
    DEF2_TZVPP = SimpleKeyword("def2-tzvpp")
    DEF2_TZVPPD = SimpleKeyword("def2-tzvppd")
    DHF_QZVP = SimpleKeyword("dhf-qzvp")
    DHF_QZVP_2C = SimpleKeyword("dhf-qzvp-2c")
    DHF_QZVPP = SimpleKeyword("dhf-qzvpp")
    DHF_QZVPP_2C = SimpleKeyword("dhf-qzvpp-2c")
    DHF_SV_P = SimpleKeyword("dhf-sv(p)")
    DHF_SV_P_2C = SimpleKeyword("dhf-sv(p)-2c")
    DHF_SVP = SimpleKeyword("dhf-svp")
    DHF_SVP_2C = SimpleKeyword("dhf-svp-2c")
    DHF_TZVP = SimpleKeyword("dhf-tzvp")
    DHF_TZVP_2C = SimpleKeyword("dhf-tzvp-2c")
    DHF_TZVPP = SimpleKeyword("dhf-tzvpp")
    DHF_TZVPP_2C = SimpleKeyword("dhf-tzvpp-2c")
    DKH_DEF2_QZVPP = SimpleKeyword("dkh-def2-qzvpp")
    DKH_DEF2_SV_P = SimpleKeyword("dkh-def2-sv(p)")
    DKH_DEF2_SVP = SimpleKeyword("dkh-def2-svp")
    DKH_DEF2_TZVP = SimpleKeyword("dkh-def2-tzvp")
    DKH_DEF2_TZVP_F = SimpleKeyword("dkh-def2-tzvp(-f)")
    DKH_DEF2_TZVPP = SimpleKeyword("dkh-def2-tzvpp")
    DKH_MA_DEF2_QZVPP = SimpleKeyword("dkh-ma-def2-qzvpp")
    DKH_MA_DEF2_SV_P = SimpleKeyword("dkh-ma-def2-sv(p)")
    DKH_MA_DEF2_SVP = SimpleKeyword("dkh-ma-def2-svp")
    DKH_MA_DEF2_TZVP = SimpleKeyword("dkh-ma-def2-tzvp")
    DKH_MA_DEF2_TZVP_F = SimpleKeyword("dkh-ma-def2-tzvp(-f)")
    DKH_MA_DEF2_TZVPP = SimpleKeyword("dkh-ma-def2-tzvpp")
    DKH_QZVP = SimpleKeyword("dkh-qzvp")
    DKH_QZVPP = SimpleKeyword("dkh-qzvpp")
    DKH_SV_P = SimpleKeyword("dkh-sv(p)")
    DKH_SVP = SimpleKeyword("dkh-svp")
    DKH_TZV_P = SimpleKeyword("dkh-tzv(p)")
    DKH_TZVP = SimpleKeyword("dkh-tzvp")
    DKH_TZVPP = SimpleKeyword("dkh-tzvpp")
    EPR_II = SimpleKeyword("epr-ii")
    EPR_III = SimpleKeyword("epr-iii")
    GFN1BASIS = SimpleKeyword("gfn1Basis")
    GFN2BASIS = SimpleKeyword("gfn2Basis")
    HAV_5PLUSD_Z = SimpleKeyword("hav(5+d)z")
    HAV_QPLUSD_Z = SimpleKeyword("hav(q+d)z")
    HAV_TPLUSD_Z = SimpleKeyword("hav(t+d)z")
    HAV5Z_PLUSD = SimpleKeyword("hav5z(+d)")
    HAVQZ_PLUSD = SimpleKeyword("havqz(+d)")
    HAVTZ_PLUSD = SimpleKeyword("havtz(+d)")
    HGBS_5 = SimpleKeyword("hgbs-5")
    HGBS_7 = SimpleKeyword("hgbs-7")
    HGBS_9 = SimpleKeyword("hgbs-9")
    HGBSP1_5 = SimpleKeyword("hgbsp1-5")
    HGBSP1_7 = SimpleKeyword("hgbsp1-7")
    HGBSP1_9 = SimpleKeyword("hgbsp1-9")
    HGBSP2_5 = SimpleKeyword("hgbsp2-5")
    HGBSP2_7 = SimpleKeyword("hgbsp2-7")
    HGBSP2_9 = SimpleKeyword("hgbsp2-9")
    HGBSP3_5 = SimpleKeyword("hgbsp3-5")
    HGBSP3_7 = SimpleKeyword("hgbsp3-7")
    HGBSP3_9 = SimpleKeyword("hgbsp3-9")
    IGLO_II = SimpleKeyword("iglo-ii")
    IGLO_III = SimpleKeyword("iglo-iii")
    JUL_CC_PV_DPLUSD_Z = SimpleKeyword("jul-cc-pv(d+d)z")
    JUL_CC_PV_QPLUSD_Z = SimpleKeyword("jul-cc-pv(q+d)z")
    JUL_CC_PV_TPLUSD_Z = SimpleKeyword("jul-cc-pv(t+d)z")
    JUN_CC_PV_DPLUSD_Z = SimpleKeyword("jun-cc-pv(d+d)z")
    JUN_CC_PV_QPLUSD_Z = SimpleKeyword("jun-cc-pv(q+d)z")
    JUN_CC_PV_TPLUSD_Z = SimpleKeyword("jun-cc-pv(t+d)z")
    LANL08 = SimpleKeyword("lanl08")
    LANL08_F = SimpleKeyword("lanl08(f)")
    LANL2DZ = SimpleKeyword("lanl2dz")
    LANL2TZ = SimpleKeyword("lanl2tz")
    LANL2TZ_F = SimpleKeyword("lanl2tz(f)")
    M6_31G = SimpleKeyword("m6-31g")
    M6_31GSTAR = SimpleKeyword("m6-31g*")
    MA_DEF_TZVP = SimpleKeyword("ma-def-tzvp")
    MA_DEF2_MSVP = SimpleKeyword("ma-def2-msvp")
    MA_DEF2_QZVP = SimpleKeyword("ma-def2-qzvp")
    MA_DEF2_QZVPP = SimpleKeyword("ma-def2-qzvpp")
    MA_DEF2_SV_P = SimpleKeyword("ma-def2-sv(p)")
    MA_DEF2_SVP = SimpleKeyword("ma-def2-svp")
    MA_DEF2_TZVP = SimpleKeyword("ma-def2-tzvp")
    MA_DEF2_TZVP_F = SimpleKeyword("ma-def2-tzvp(-f)")
    MA_DEF2_TZVPP = SimpleKeyword("ma-def2-tzvpp")
    MA_DKH_DEF2_QZVPP = SimpleKeyword("ma-dkh-def2-qzvpp")
    MA_DKH_DEF2_SV_P = SimpleKeyword("ma-dkh-def2-sv(p)")
    MA_DKH_DEF2_SVP = SimpleKeyword("ma-dkh-def2-svp")
    MA_DKH_DEF2_TZVP = SimpleKeyword("ma-dkh-def2-tzvp")
    MA_DKH_DEF2_TZVP_F = SimpleKeyword("ma-dkh-def2-tzvp(-f)")
    MA_DKH_DEF2_TZVPP = SimpleKeyword("ma-dkh-def2-tzvpp")
    MA_ZORA_DEF2_QZVPP = SimpleKeyword("ma-zora-def2-qzvpp")
    MA_ZORA_DEF2_SV_P = SimpleKeyword("ma-zora-def2-sv(p)")
    MA_ZORA_DEF2_SVP = SimpleKeyword("ma-zora-def2-svp")
    MA_ZORA_DEF2_TZVP = SimpleKeyword("ma-zora-def2-tzvp")
    MA_ZORA_DEF2_TZVP_F = SimpleKeyword("ma-zora-def2-tzvp(-f)")
    MA_ZORA_DEF2_TZVPP = SimpleKeyword("ma-zora-def2-tzvpp")
    MAUG_CC_PV_DPLUSD_Z = SimpleKeyword("maug-cc-pv(d+d)z")
    MAUG_CC_PV_QPLUSD_Z = SimpleKeyword("maug-cc-pv(q+d)z")
    MAUG_CC_PV_TPLUSD_Z = SimpleKeyword("maug-cc-pv(t+d)z")
    MAY_CC_PV_QPLUSD_Z = SimpleKeyword("may-cc-pv(q+d)z")
    MAY_CC_PV_TPLUSD_Z = SimpleKeyword("may-cc-pv(t+d)z")
    MIDI = SimpleKeyword("midi")
    MINAO = SimpleKeyword("minao")
    MINAO_AUTO_PP = SimpleKeyword("minao-auto-pp")
    MINI = SimpleKeyword("mini")
    MINIS = SimpleKeyword("minis")
    MINIX = SimpleKeyword("minix")
    OLD_DKH_SV_P = SimpleKeyword("old-dkh-sv(p)")
    OLD_DKH_SVP = SimpleKeyword("old-dkh-svp")
    OLD_DKH_TZV_P = SimpleKeyword("old-dkh-tzv(p)")
    OLD_DKH_TZVP = SimpleKeyword("old-dkh-tzvp")
    OLD_DKH_TZVPP = SimpleKeyword("old-dkh-tzvpp")
    OLD_SV = SimpleKeyword("old-sv")
    OLD_SV_P = SimpleKeyword("old-sv(p)")
    OLD_SVP = SimpleKeyword("old-svp")
    OLD_TZV = SimpleKeyword("old-tzv")
    OLD_TZV_P = SimpleKeyword("old-tzv(p)")
    OLD_TZVP = SimpleKeyword("old-tzvp")
    OLD_TZVPP = SimpleKeyword("old-tzvpp")
    OLD_ZORA_SV_P = SimpleKeyword("old-zora-sv(p)")
    OLD_ZORA_SVP = SimpleKeyword("old-zora-svp")
    OLD_ZORA_TZV_P = SimpleKeyword("old-zora-tzv(p)")
    OLD_ZORA_TZVP = SimpleKeyword("old-zora-tzvp")
    OLD_ZORA_TZVPP = SimpleKeyword("old-zora-tzvpp")
    PARTRIDGE_1 = SimpleKeyword("partridge-1")
    PARTRIDGE_2 = SimpleKeyword("partridge-2")
    PARTRIDGE_3 = SimpleKeyword("partridge-3")
    PARTRIDGE_4 = SimpleKeyword("partridge-4")
    PC_0 = SimpleKeyword("pc-0")
    PC_1 = SimpleKeyword("pc-1")
    PC_2 = SimpleKeyword("pc-2")
    PC_3 = SimpleKeyword("pc-3")
    PC_4 = SimpleKeyword("pc-4")
    PCH_1 = SimpleKeyword("pch-1")
    PCH_2 = SimpleKeyword("pch-2")
    PCH_3 = SimpleKeyword("pch-3")
    PCH_4 = SimpleKeyword("pch-4")
    PCJ_0 = SimpleKeyword("pcj-0")
    PCJ_1 = SimpleKeyword("pcj-1")
    PCJ_2 = SimpleKeyword("pcj-2")
    PCJ_3 = SimpleKeyword("pcj-3")
    PCJ_4 = SimpleKeyword("pcj-4")
    PCSEG_0 = SimpleKeyword("pcseg-0")
    PCSEG_1 = SimpleKeyword("pcseg-1")
    PCSEG_2 = SimpleKeyword("pcseg-2")
    PCSEG_3 = SimpleKeyword("pcseg-3")
    PCSEG_4 = SimpleKeyword("pcseg-4")
    PCSSEG_0 = SimpleKeyword("pcsseg-0")
    PCSSEG_1 = SimpleKeyword("pcsseg-1")
    PCSSEG_2 = SimpleKeyword("pcsseg-2")
    PCSSEG_3 = SimpleKeyword("pcsseg-3")
    PCSSEG_4 = SimpleKeyword("pcsseg-4")
    PCX_1 = SimpleKeyword("pcx-1")
    PCX_2 = SimpleKeyword("pcx-2")
    PCX_3 = SimpleKeyword("pcx-3")
    PCX_4 = SimpleKeyword("pcx-4")
    QZVP = SimpleKeyword("qzvp")
    QZVPP = SimpleKeyword("qzvpp")
    SAPPORO_DKH3_DZP_2012 = SimpleKeyword("sapporo-dkh3-dzp-2012")
    SAPPORO_DKH3_QZP_2012 = SimpleKeyword("sapporo-dkh3-qzp-2012")
    SAPPORO_DKH3_TZP_2012 = SimpleKeyword("sapporo-dkh3-tzp-2012")
    SAPPORO_DZP_2012 = SimpleKeyword("sapporo-dzp-2012")
    SAPPORO_QZP_2012 = SimpleKeyword("sapporo-qzp-2012")
    SAPPORO_TZP_2012 = SimpleKeyword("sapporo-tzp-2012")
    SARC_DKH_SVP = SimpleKeyword("sarc-dkh-svp")
    SARC_DKH_TZVP = SimpleKeyword("sarc-dkh-tzvp")
    SARC_DKH_TZVPP = SimpleKeyword("sarc-dkh-tzvpp")
    SARC_ZORA_SVP = SimpleKeyword("sarc-zora-svp")
    SARC_ZORA_TZVP = SimpleKeyword("sarc-zora-tzvp")
    SARC_ZORA_TZVPP = SimpleKeyword("sarc-zora-tzvpp")
    SARC2_DKH_QZV = SimpleKeyword("sarc2-dkh-qzv")
    SARC2_DKH_QZVP = SimpleKeyword("sarc2-dkh-qzvp")
    SARC2_ZORA_QZV = SimpleKeyword("sarc2-zora-qzv")
    SARC2_ZORA_QZVP = SimpleKeyword("sarc2-zora-qzvp")
    SAUG_ANO_PV5Z = SimpleKeyword("saug-ano-pv5z")
    SAUG_ANO_PVDZ = SimpleKeyword("saug-ano-pvdz")
    SAUG_ANO_PVQZ = SimpleKeyword("saug-ano-pvqz")
    SAUG_ANO_PVTZ = SimpleKeyword("saug-ano-pvtz")
    STO_3G = SimpleKeyword("sto-3g")
    SV = SimpleKeyword("sv")
    SV_P = SimpleKeyword("sv(p)")
    SVP = SimpleKeyword("svp")
    TZV = SimpleKeyword("tzv")
    TZV_P = SimpleKeyword("tzv(p)")
    TZVP = SimpleKeyword("tzvp")
    TZVPP = SimpleKeyword("tzvpp")
    UGBS = SimpleKeyword("ugbs")
    VDZP = SimpleKeyword("vdzp")
    W1_DZ = SimpleKeyword("w1-dz")
    W1_MTSMALL = SimpleKeyword("w1-mtsmall")
    W1_OPT = SimpleKeyword("w1-opt")
    W1_QZ = SimpleKeyword("w1-qz")
    W1_TZ = SimpleKeyword("w1-tz")
    WACHTERSPLUSF = SimpleKeyword("wachters+f")
    X2C_QZVPALL = SimpleKeyword("x2c-qzvpall")
    X2C_QZVPALL_2C = SimpleKeyword("x2c-qzvpall-2c")
    X2C_QZVPALL_2C_S = SimpleKeyword("x2c-qzvpall-2c-s")
    X2C_QZVPALL_S = SimpleKeyword("x2c-qzvpall-s")
    X2C_QZVPPALL = SimpleKeyword("x2c-qzvppall")
    X2C_QZVPPALL_2C = SimpleKeyword("x2c-qzvppall-2c")
    X2C_QZVPPALL_2C_S = SimpleKeyword("x2c-qzvppall-2c-s")
    X2C_QZVPPALL_S = SimpleKeyword("x2c-qzvppall-s")
    X2C_SV_P_ALL = SimpleKeyword("x2c-sv(p)all")
    X2C_SV_P_ALL_2C = SimpleKeyword("x2c-sv(p)all-2c")
    X2C_SV_P_ALL_S = SimpleKeyword("x2c-sv(p)all-s")
    X2C_SVPALL = SimpleKeyword("x2c-svpall")
    X2C_SVPALL_2C = SimpleKeyword("x2c-svpall-2c")
    X2C_SVPALL_S = SimpleKeyword("x2c-svpall-s")
    X2C_TZVPALL = SimpleKeyword("x2c-tzvpall")
    X2C_TZVPALL_2C = SimpleKeyword("x2c-tzvpall-2c")
    X2C_TZVPALL_S = SimpleKeyword("x2c-tzvpall-s")
    X2C_TZVPPALL = SimpleKeyword("x2c-tzvppall")
    X2C_TZVPPALL_2C = SimpleKeyword("x2c-tzvppall-2c")
    X2C_TZVPPALL_S = SimpleKeyword("x2c-tzvppall-s")
    ZORA_DEF2_QZVPP = SimpleKeyword("zora-def2-qzvpp")
    ZORA_DEF2_SV_P = SimpleKeyword("zora-def2-sv(p)")
    ZORA_DEF2_SVP = SimpleKeyword("zora-def2-svp")
    ZORA_DEF2_TZVP = SimpleKeyword("zora-def2-tzvp")
    ZORA_DEF2_TZVP_F = SimpleKeyword("zora-def2-tzvp(-f)")
    ZORA_DEF2_TZVPP = SimpleKeyword("zora-def2-tzvpp")
    ZORA_MA_DEF2_QZVPP = SimpleKeyword("zora-ma-def2-qzvpp")
    ZORA_MA_DEF2_SV_P = SimpleKeyword("zora-ma-def2-sv(p)")
    ZORA_MA_DEF2_SVP = SimpleKeyword("zora-ma-def2-svp")
    ZORA_MA_DEF2_TZVP = SimpleKeyword("zora-ma-def2-tzvp")
    ZORA_MA_DEF2_TZVP_F = SimpleKeyword("zora-ma-def2-tzvp(-f)")
    ZORA_MA_DEF2_TZVPP = SimpleKeyword("zora-ma-def2-tzvpp")
    ZORA_QZVP = SimpleKeyword("zora-qzvp")
    ZORA_QZVPP = SimpleKeyword("zora-qzvpp")
    ZORA_SV_P = SimpleKeyword("zora-sv(p)")
    ZORA_SVP = SimpleKeyword("zora-svp")
    ZORA_TZV_P = SimpleKeyword("zora-tzv(p)")
    ZORA_TZVP = SimpleKeyword("zora-tzvp")
    ZORA_TZVPP = SimpleKeyword("zora-tzvpp")
