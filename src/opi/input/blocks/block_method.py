from typing import Literal

from pydantic import BaseModel, field_validator
from pydantic_core.core_schema import ValidationInfo

from opi.input.blocks import BlockABC
from opi.input.blocks.util import InputFilePath

__all__ = ("BlockMethod",)

# > Exchange components of LibXC (ORCA 6.1.1), for `BlockMethod.exchange`
LibXCExchange = Literal[
    "gga_x_2d_b86",
    "gga_x_2d_b86_mgc",
    "gga_x_2d_b88",
    "gga_x_2d_pbe",
    "gga_x_airy",
    "gga_x_ak13",
    "gga_x_am05",
    "gga_x_apbe",
    "gga_x_b86",
    "gga_x_b86_mgc",
    "gga_x_b86_r",
    "gga_x_b88",
    "gga_x_b88_6311g",
    "gga_x_b88m",
    "gga_x_bayesian",
    "gga_x_bcgp",
    "gga_x_beefvdw",
    "gga_x_bkl1",
    "gga_x_bkl2",
    "gga_x_bpccac",
    "gga_x_c09x",
    "gga_x_cap",
    "gga_x_chachiyo",
    "gga_x_dk87_r1",
    "gga_x_dk87_r2",
    "gga_x_eb88",
    "gga_x_ecmv92",
    "gga_x_ev93",
    "gga_x_fd_lb94",
    "gga_x_fd_revlb94",
    "gga_x_ft97_a",
    "gga_x_ft97_b",
    "gga_x_g96",
    "gga_x_gam",
    "gga_x_gg99",
    "gga_x_hcth_a",
    "gga_x_hjs_b88",
    "gga_x_hjs_b88_v2",
    "gga_x_hjs_b97x",
    "gga_x_hjs_pbe",
    "gga_x_hjs_pbe_sol",
    "gga_x_htbs",
    "gga_x_ityh",
    "gga_x_ityh_optx",
    "gga_x_ityh_pbe",
    "gga_x_kgg99",
    "gga_x_kt1",
    "gga_x_lag",
    "gga_x_lambda_ch_n",
    "gga_x_lambda_lo_n",
    "gga_x_lambda_oc2_n",
    "gga_x_lb",
    "gga_x_lbm",
    "gga_x_lg93",
    "gga_x_lspbe",
    "gga_x_lsrpbe",
    "gga_x_lv_rpw86",
    "gga_x_mb88",
    "gga_x_mpbe",
    "gga_x_mpw91",
    "gga_x_n12",
    "gga_x_ncap",
    "gga_x_ncapr",
    "gga_x_ol2",
    "gga_x_optb86b_vdw",
    "gga_x_optb88_vdw",
    "gga_x_optpbe_vdw",
    "gga_x_optx",
    "gga_x_pbe",
    "gga_x_pbe_erf_gws",
    "gga_x_pbe_gaussian",
    "gga_x_pbe_jsjr",
    "gga_x_pbe_mod",
    "gga_x_pbe_mol",
    "gga_x_pbe_r",
    "gga_x_pbe_sol",
    "gga_x_pbe_tca",
    "gga_x_pbea",
    "gga_x_pbefe",
    "gga_x_pbeint",
    "gga_x_pbek1_vdw",
    "gga_x_pbepow",
    "gga_x_pbetrans",
    "gga_x_pw86",
    "gga_x_pw91",
    "gga_x_pw91_mod",
    "gga_x_q1d",
    "gga_x_q2d",
    "gga_x_revssb_d",
    "gga_x_rge2",
    "gga_x_rpbe",
    "gga_x_rpw86",
    "gga_x_s12g",
    "gga_x_sfat",
    "gga_x_sfat_pbe",
    "gga_x_sg4",
    "gga_x_sogga",
    "gga_x_sogga11",
    "gga_x_ssb",
    "gga_x_ssb_d",
    "gga_x_ssb_sw",
    "gga_x_vmt84_ge",
    "gga_x_vmt84_pbe",
    "gga_x_vmt_ge",
    "gga_x_vmt_pbe",
    "gga_x_wc",
    "gga_x_wpbeh",
    "gga_x_xpbe",
    "hyb_gga_x_cam_s12g",
    "hyb_gga_x_cam_s12h",
    "hyb_gga_x_n12_sx",
    "hyb_gga_x_pbe_erf_gws",
    "hyb_gga_x_s12h",
    "hyb_gga_x_sogga11_x",
    "hyb_lda_x_erf",
    "hyb_mgga_x_bmk",
    "hyb_mgga_x_cf22d",
    "hyb_mgga_x_dldf",
    "hyb_mgga_x_js18",
    "hyb_mgga_x_m05",
    "hyb_mgga_x_m05_2x",
    "hyb_mgga_x_m06",
    "hyb_mgga_x_m06_2x",
    "hyb_mgga_x_m06_hf",
    "hyb_mgga_x_m06_sx",
    "hyb_mgga_x_m08_hx",
    "hyb_mgga_x_m08_so",
    "hyb_mgga_x_m11",
    "hyb_mgga_x_mn12_sx",
    "hyb_mgga_x_mn15",
    "hyb_mgga_x_ms2h",
    "hyb_mgga_x_mvsh",
    "hyb_mgga_x_pjs18",
    "hyb_mgga_x_revm06",
    "hyb_mgga_x_revm11",
    "hyb_mgga_x_revscan0",
    "hyb_mgga_x_scan0",
    "hyb_mgga_x_tau_hcth",
    "lda_x",
    "lda_x_1d_exponential",
    "lda_x_1d_soft",
    "lda_x_2d",
    "lda_x_erf",
    "lda_x_rae",
    "lda_x_rel",
    "lda_x_sloc",
    "lda_x_yukawa",
    "mgga_x_2d_js17",
    "mgga_x_2d_prhg07",
    "mgga_x_2d_prhg07_prp10",
    "mgga_x_b00",
    "mgga_x_bj06",
    "mgga_x_bloc",
    "mgga_x_br89",
    "mgga_x_br89_1",
    "mgga_x_br89_explicit",
    "mgga_x_br89_explicit_1",
    "mgga_x_edmgga",
    "mgga_x_eel",
    "mgga_x_ft98",
    "mgga_x_gdme_0",
    "mgga_x_gdme_kos",
    "mgga_x_gdme_nv",
    "mgga_x_gdme_vt",
    "mgga_x_gvt4",
    "mgga_x_gx",
    "mgga_x_hlta",
    "mgga_x_jk",
    "mgga_x_ktbm_0",
    "mgga_x_ktbm_1",
    "mgga_x_ktbm_10",
    "mgga_x_ktbm_11",
    "mgga_x_ktbm_12",
    "mgga_x_ktbm_13",
    "mgga_x_ktbm_14",
    "mgga_x_ktbm_15",
    "mgga_x_ktbm_16",
    "mgga_x_ktbm_17",
    "mgga_x_ktbm_18",
    "mgga_x_ktbm_19",
    "mgga_x_ktbm_2",
    "mgga_x_ktbm_20",
    "mgga_x_ktbm_21",
    "mgga_x_ktbm_22",
    "mgga_x_ktbm_23",
    "mgga_x_ktbm_24",
    "mgga_x_ktbm_3",
    "mgga_x_ktbm_4",
    "mgga_x_ktbm_5",
    "mgga_x_ktbm_6",
    "mgga_x_ktbm_7",
    "mgga_x_ktbm_8",
    "mgga_x_ktbm_9",
    "mgga_x_ktbm_gap",
    "mgga_x_lak",
    "mgga_x_lta",
    "mgga_x_m06_l",
    "mgga_x_m11_l",
    "mgga_x_mbeef",
    "mgga_x_mbeefvdw",
    "mgga_x_mbr",
    "mgga_x_mbrxc_bg",
    "mgga_x_mbrxh_bg",
    "mgga_x_mcml",
    "mgga_x_mggac",
    "mgga_x_mk00",
    "mgga_x_mk00b",
    "mgga_x_mn12_l",
    "mgga_x_mn15_l",
    "mgga_x_modtpss",
    "mgga_x_ms0",
    "mgga_x_ms1",
    "mgga_x_ms2",
    "mgga_x_ms2_rev",
    "mgga_x_ms2b",
    "mgga_x_ms2bs",
    "mgga_x_msb86bl",
    "mgga_x_mspbel",
    "mgga_x_msrpbel",
    "mgga_x_mtask",
    "mgga_x_mvs",
    "mgga_x_mvsb",
    "mgga_x_mvsbs",
    "mgga_x_pbe_gx",
    "mgga_x_pkzb",
    "mgga_x_r2scan",
    "mgga_x_r2scan01",
    "mgga_x_r2scanl",
    "mgga_x_r4scan",
    "mgga_x_regtm",
    "mgga_x_regtpss",
    "mgga_x_revm06_l",
    "mgga_x_revscan",
    "mgga_x_revscanl",
    "mgga_x_revtm",
    "mgga_x_revtpss",
    "mgga_x_rlda",
    "mgga_x_rmsb86bl",
    "mgga_x_rmspbel",
    "mgga_x_rmsrpbel",
    "mgga_x_rpp09",
    "mgga_x_rppscan",
    "mgga_x_rscan",
    "mgga_x_rtpss",
    "mgga_x_sa_tpss",
    "mgga_x_scan",
    "mgga_x_scanl",
    "mgga_x_task",
    "mgga_x_tau_hcth",
    "mgga_x_tb09",
    "mgga_x_th",
    "mgga_x_tlda",
    "mgga_x_tm",
    "mgga_x_tpss",
    "mgga_x_vcml",
    "mgga_x_vt84",
]

# > Correlation components of LibXC (ORCA 6.1.1), for `BlockMethod.correlation`
LibXCCorrelation = Literal[
    "gga_c_acgga",
    "gga_c_acggap",
    "gga_c_am05",
    "gga_c_apbe",
    "gga_c_bmk",
    "gga_c_ccdf",
    "gga_c_chachiyo",
    "gga_c_cs1",
    "gga_c_ft97",
    "gga_c_gam",
    "gga_c_gapc",
    "gga_c_gaploc",
    "gga_c_hcth_a",
    "gga_c_hyb_tau_hcth",
    "gga_c_lm",
    "gga_c_lyp",
    "gga_c_lypr",
    "gga_c_mggac",
    "gga_c_n12",
    "gga_c_n12_sx",
    "gga_c_op_b88",
    "gga_c_op_g96",
    "gga_c_op_pbe",
    "gga_c_op_pw91",
    "gga_c_op_xalpha",
    "gga_c_optc",
    "gga_c_p86",
    "gga_c_p86_ft",
    "gga_c_p86vwn",
    "gga_c_p86vwn_ft",
    "gga_c_pbe",
    "gga_c_pbe_erf_gws",
    "gga_c_pbe_gaussian",
    "gga_c_pbe_jrgx",
    "gga_c_pbe_mol",
    "gga_c_pbe_sol",
    "gga_c_pbe_vwn",
    "gga_c_pbefe",
    "gga_c_pbeint",
    "gga_c_pbeloc",
    "gga_c_pw91",
    "gga_c_q2d",
    "gga_c_regtpss",
    "gga_c_revtca",
    "gga_c_rge2",
    "gga_c_scan_e0",
    "gga_c_sg4",
    "gga_c_sogga11",
    "gga_c_sogga11_x",
    "gga_c_spbe",
    "gga_c_tau_hcth",
    "gga_c_tca",
    "gga_c_tm_lyp",
    "gga_c_tm_pbe",
    "gga_c_w94",
    "gga_c_wi",
    "gga_c_wi0",
    "gga_c_wl",
    "gga_c_xpbe",
    "gga_c_zpbeint",
    "gga_c_zpbesol",
    "gga_c_zvpbeint",
    "gga_c_zvpbeloc",
    "gga_c_zvpbesol",
    "lda_c_1d_csc",
    "lda_c_1d_loos",
    "lda_c_2d_amgb",
    "lda_c_2d_prm",
    "lda_c_br78",
    "lda_c_chachiyo",
    "lda_c_chachiyo_mod",
    "lda_c_epc17",
    "lda_c_epc17_2",
    "lda_c_epc18_1",
    "lda_c_epc18_2",
    "lda_c_gk72",
    "lda_c_gl",
    "lda_c_gombas",
    "lda_c_hl",
    "lda_c_karasiev",
    "lda_c_karasiev_mod",
    "lda_c_lp96",
    "lda_c_mcweeny",
    "lda_c_ml1",
    "lda_c_ml2",
    "lda_c_ob_pw",
    "lda_c_ob_pz",
    "lda_c_ow",
    "lda_c_ow_lyp",
    "lda_c_pk09",
    "lda_c_pmgb06",
    "lda_c_pw",
    "lda_c_pw_erf",
    "lda_c_pw_mod",
    "lda_c_pw_rpa",
    "lda_c_pz",
    "lda_c_pz_mod",
    "lda_c_rc04",
    "lda_c_rpa",
    "lda_c_rpw92",
    "lda_c_upw92",
    "lda_c_vbh",
    "lda_c_vwn",
    "lda_c_vwn_1",
    "lda_c_vwn_2",
    "lda_c_vwn_3",
    "lda_c_vwn_4",
    "lda_c_vwn_rpa",
    "lda_c_w20",
    "lda_c_wigner",
    "lda_c_xalpha",
    "mgga_c_b88",
    "mgga_c_b94",
    "mgga_c_bc95",
    "mgga_c_cc",
    "mgga_c_ccalda",
    "mgga_c_cf22d",
    "mgga_c_cs",
    "mgga_c_dldf",
    "mgga_c_hltapw",
    "mgga_c_kcis",
    "mgga_c_kcisk",
    "mgga_c_m05",
    "mgga_c_m05_2x",
    "mgga_c_m06",
    "mgga_c_m06_2x",
    "mgga_c_m06_hf",
    "mgga_c_m06_l",
    "mgga_c_m06_sx",
    "mgga_c_m08_hx",
    "mgga_c_m08_so",
    "mgga_c_m11",
    "mgga_c_m11_l",
    "mgga_c_mn12_l",
    "mgga_c_mn12_sx",
    "mgga_c_mn15",
    "mgga_c_mn15_l",
    "mgga_c_pkzb",
    "mgga_c_r2scan",
    "mgga_c_r2scan01",
    "mgga_c_r2scanl",
    "mgga_c_revm06",
    "mgga_c_revm06_l",
    "mgga_c_revm11",
    "mgga_c_revscan",
    "mgga_c_revscan_vv10",
    "mgga_c_revtm",
    "mgga_c_revtpss",
    "mgga_c_rmggac",
    "mgga_c_rppscan",
    "mgga_c_rregtm",
    "mgga_c_rscan",
    "mgga_c_scan",
    "mgga_c_scan_rvv10",
    "mgga_c_scan_vv10",
    "mgga_c_scanl",
    "mgga_c_scanl_rvv10",
    "mgga_c_scanl_vv10",
    "mgga_c_tm",
    "mgga_c_tpss",
    "mgga_c_tpss_gaussian",
    "mgga_c_tpssloc",
    "mgga_c_vsxc",
]


class ExternalParam(BaseModel):
    """
    Class to model `extparamx', `extparamx` and `extparamxc` attributes in `BlockMethod`.

    Attributes
    -----------
    field_name: str
        Field name.

    parameters: dict[str, float]
        Dictionary of parameter values.

    """

    field_name: str | None = None
    parameters: dict[str, float]

    @classmethod
    def from_string(cls, field_name: str | None, strings: str | list[str]) -> "ExternalParam":
        """Create a `ExternalParam` instance from a string or list of strings such as:
        '_bt 0.00444' or ['_bt 0.00444', '_alpha 19.823391']"""
        params = {}
        if isinstance(strings, str):
            strings = [strings]
        for string in strings:
            # split string into parameter name and value
            paramname, value = string.rsplit(" ", maxsplit=1)
            params[paramname.strip()] = float(value.strip())

        return ExternalParam(field_name=field_name, parameters=params)

    def __str__(self) -> str:
        lines = []

        for i, (key, value) in enumerate(self.parameters.items()):
            if i == 0:
                # when formatting block input for orca, the first line will already include field name
                lines.append(f'"{key}" {value}')
            else:
                # lines after first line need to add the field name
                lines.append(f'    {self.field_name} "{key}" {value}')

        return "\n".join(lines)


class BlockMethod(BlockABC):
    """Class to model %method block in ORCA"""

    _name: str = "Method"

    method: Literal["dft"] | None = None
    exchange: (
        Literal[
            "x_nox",
            "x_slater",
            "x_becke",
            "x_wb88",
            "x_g96",
            "x_pw91",
            "x_mpw",
            "x_pbe",
            "x_rpbe",
            "x_optx",
            "x_x",
            "x_tpss",
            "x_b97d",
            "x_b97becke",
            "x_scan",
            "x_rscan",
            "x_r2scan",
        ]
        | LibXCExchange
        | None
    ) = None
    correlation: (
        Literal[
            "c_noc",
            "c_vwn5",
            "c_vwn3",
            "c_pwlda",
            "c_p86",
            "c_pw91",
            "c_pbe",
            "c_lyp",
            "c_tpss",
            "c_b97d",
            "c_b97becke",
            "c_scan",
            "c_rscan",
            "c_r2scan",
        ]
        | LibXCCorrelation
        | None
    ) = None
    ldaopt: Literal["c_noc", "c_pwlda", "c_vwn5", "c_vwn3"] | None = None
    xalpha: float | None = None
    xbeta: float | None = None
    xkappa: float | None = None
    xmuepbe: float | None = None
    cbetapbe: float | None = None
    rangesepexx: bool | None = None
    rangesepmu: float | None = None
    rangesepscal: float | None = None
    scalhfx: float | None = None
    scaldfx: float | None = None
    scalggac: float | None = None
    scalldac: float | None = None
    scalmp2c: float | None = None
    extparamx: ExternalParam | None = None
    extparamc: ExternalParam | None = None
    extparamxc: ExternalParam | None = None

    # > Options DFT-D
    d3s6: float | None = None
    d3a1: float | None = None
    d3s8: float | None = None
    d3a2: float | None = None

    # > Number of CPSCF iterations
    z_maxiter: int | None = None

    # > Options for Extopt
    ProgExt: InputFilePath | None = None  # Path to wrapper script
    Ext_Params: str | None = None  # Arbitrary optional command line arguments

    @field_validator("ProgExt", mode="before")
    @classmethod
    def path_from_string(cls, path: str | InputFilePath) -> InputFilePath:
        """
        Parameters
        ----------
        path : str | InputFilePath
        """
        if isinstance(path, str):
            return InputFilePath.from_string(path)
        else:
            return path

    @field_validator("extparamx", "extparamc", "extparamxc", mode="before")
    @classmethod
    def init_ext_param(
        cls, inp: str | list[str] | dict[str, float] | ExternalParam, info: ValidationInfo
    ) -> ExternalParam:
        """
        Allows user to input dict or list of strings for external parameter attributes, the initialization of `ExternalParam` is done internally.
        Also sets field name which is required for formatting of external parameters attributes.

        Parameters
        ----------
        inp: list[str]| dict[str, float]| ExternalParam

        info: ValidationInfo

        Returns
        -------
        ExternalParam
            ExternalParam instance
        """
        field_name = info.field_name
        if isinstance(inp, ExternalParam):
            if inp.field_name is None:
                inp.field_name = field_name
            return inp
        elif isinstance(inp, dict):
            return ExternalParam(field_name=field_name, parameters=inp)
        else:
            return ExternalParam.from_string(field_name, inp)

    @field_validator("method", "exchange", "correlation", "ldaopt", mode="before")
    @classmethod
    def string_tolower(cls, inp: str) -> str:
        """If input is a string, convert it to lowercase. This allows for case-insensitive validation.

        Examples
        --------
        BlockMethod(method='DFT')
        BlockMethod(method='dft')
        BlockMethod(method='dFT')

        All of these will be accepted if `dft` is valid literal.
        """
        return inp.lower()
