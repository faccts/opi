from typing import Literal

from pydantic import field_validator

from opi.input.blocks import Block, InputFilePath
from opi.input.blocks.geom_wrapper import Internal, Internals

__all__ = ("BlockNeb",)


class BlockNeb(Block):
    """Class to model %neb block in ORCA"""

    _name: str = "neb"
    nimages: int | None = None
    interpolation: (
        Literal[
            "linear",
            "idpp",
            "xtb",
            "xtbts",
            "xtb0",
            "xtb0ts",
            "xtb1",
            "xtb1ts",
            "xtb2",
            "xtb2ts",
        ]
        | None
    ) = None
    quatern: Literal["startonly", "always", "no"] | None = None
    tangent: Literal["original", "improved"] | None = None
    free_end: bool | None = None
    free_end_type: Literal["contour", "perp", "full"] | None = None
    pal_opt: int | None = None
    free_end_ec: float | None = None
    free_end_ec_end: float | None = None
    free_end_kappa: float | None = None
    springconst: float | None = None
    springconst2: float | None = None
    springtype: Literal["dof", "original", "image", "distance", "ideal", "path"] | None = None
    energy_weighted: bool | None = None
    perpspring: Literal["cos", "tan", "costan", "dneb"] | None = None
    fix_center: bool | None = None
    remove_extern_force: bool | None = None
    convtype: Literal["all", "cionly"] | None = None
    ci: bool | None = None
    climbingimage: bool | None = None
    tol_scale: float | None = None
    tol_turn_on_ci: float | None = None
    tol_maxf_ci: float | None = None
    tol_rmsf_ci: float | None = None
    tol_maxfp_i: float | None = None
    tol_rmsfp_i: float | None = None
    reparam_type: Literal["linear", "cubic"] | None = None
    reparam: int | None = None
    tol_reparam: float | None = None
    restart_opt_on_reparam: bool | None = None
    opt_method: Literal["vpo", "fire", "lbfgs", "bfgs"] | None = None
    local: bool | None = None
    nmax: int | None = None
    maxiter: int | None = None
    maxmove: float | None = None
    stepsize: float | None = None
    lbfgs_memory: int | None = None
    lbfgs_dr: float | None = None
    lbfgs_restart_on_maxmove: bool | None = None
    lbfgs_reparam_on_restart: bool | None = None
    lbfgs_precondition: bool | None = None
    fire_initial_damp: float | None = None
    fire_damp_decr: float | None = None
    fire_step_incr: float | None = None
    fire_step_decr: float | None = None
    fire_max_step: float | None = None
    fire_retention: int | None = None
    printlevel: int | None = None
    npts_interpol: int | None = None
    prepare_frags: bool | None = None
    max_frag_dist: float | None = None
    bond_cutoff: float | None = None
    idpp_nmax: int | None = None
    idpp_tol_maxf: float | None = None
    idpp_ksp: float | None = None
    idpp_alpha: float | None = None
    idpp_maxmove: float | None = None
    idpp_quatern: bool | None = None
    idpp_debug: bool | None = None
    idpp_idealweight: bool | None = None
    idpp_dist_interpolation: int | None = None
    idpp_bilinear_partition: float | None = None
    sidpp: bool | None = None
    sidpp_reparam: bool | None = None
    sidpp_tol_maxf: float | None = None
    sidpp_energy_weighted_tangent: bool | None = None
    sidpp_even_nim: bool | None = None
    sidpp_double_nim: bool | None = None
    sidpp_ideal_springconst: bool | None = None
    tol_turn_on_zoom: float | None = None
    zoom_offset: int | None = None
    zoom_auto: bool | None = None
    zoom_alpha: float | None = None
    zoom_interpolation: Literal["linear", "cubic", "bilinear"] | None = None
    zoom_printfulltrj: bool | None = None
    neb_ts: bool | None = None
    neb_mmfts: bool | None = None
    gp_neb: bool | None = None
    gp_neb_maxuncertainty: float | None = None
    gp_neb_maxcycles: int | None = None
    nsteps_foundintermediate: int | None = None
    abortif_foundintermediate: bool | None = None
    bfgs_internalhess: bool | None = None
    checkscfconv: bool | None = None
    llt_cos: bool | None = None
    ts_inputhess: Literal["appr", "calc-hess"] | None = None
    preopt_endpoints: bool | None = None
    preopt_ends: bool | None = None
    preopt_minima: bool | None = None
    preopt: bool | None = None
    neb_ts_image: int | None = None
    neb_restart_xyzfile: InputFilePath | None = None
    neb_restart_gbwname: InputFilePath | None = None
    neb_end_xyzfile: InputFilePath | None = None
    neb_end_pdbfile: InputFilePath | None = None
    product_pdbfile: InputFilePath | None = None
    neb_ts_pdbfile: InputFilePath | None = None
    ts_pdbfile: InputFilePath | None = None
    ts: InputFilePath | None = None
    monitor_internals: Internals | None = None

    @field_validator("monitor_internals", mode="before")
    @classmethod
    def internals_str(cls, strings: list[str] | str) -> Internals:
        """
        Parameters
        ----------
        strings : list[str] | str
        """
        try:
            if isinstance(strings, list):
                internals = [Internal.from_string(s) for s in strings]
            else:
                internals = [Internal.from_string(strings)]
        except Exception as e:
            raise ValueError(f"Failed to parse strings: {e}")

        return Internals(internals=internals)

    @field_validator(
        "neb_restart_xyzfile",
        "neb_restart_gbwname",
        "neb_end_xyzfile",
        "neb_end_pdbfile",
        "product_pdbfile",
        "neb_ts_pdbfile",
        "ts_pdbfile",
        "ts",
        mode="before",
    )
    @classmethod
    def path_from_string(cls, path: str | InputFilePath) -> InputFilePath:
        """
        Parameters
        ----------
        path : str | InputFilePath
        """
        if isinstance(path, str):
            return InputFilePath.from_string(path)

        return path
