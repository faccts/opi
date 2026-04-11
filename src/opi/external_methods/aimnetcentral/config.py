from __future__ import annotations

from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class AimnetCentralConfig(BaseModel):
    """Configuration for running AIMNet2 through ORCA's ExtOpt interface.

    Units
    -----
    - Coordinates are passed by ORCA in Angstrom.
    - Energies must be returned to ORCA in Hartree.
    - Gradients must be returned to ORCA in Hartree/Bohr.

    Notes
    -----
    `model` accepts AIMNetCentral registry aliases (for example `aimnet2`,
    `aimnet2_2025`, `aimnet2nse`, `aimnet2pd`), Hugging Face repo ids, or a
    local exported model path accepted by `aimnet.calculators.AIMNet2Calculator`.
    """

    model_config = ConfigDict(extra="forbid")

    model: str = Field(default="aimnet2_2025")
    device: str | None = Field(default=None)
    compile_model: bool = Field(default=False)
    ensemble_member: int = Field(default=0, ge=0, le=3)
    revision: str | None = Field(default=None)
    token: str | None = Field(default=None)
    charge: float | None = Field(default=None)
    mult: float | None = Field(default=None)
    forces: bool = Field(default=True)
    nb_threshold: int = Field(default=120, ge=1)
    needs_coulomb: bool | None = Field(default=None)
    needs_dispersion: bool | None = Field(default=None)
    coulomb_method: Literal["simple", "dsf", "ewald"] | None = Field(default=None)
    coulomb_cutoff: float = Field(default=15.0, gt=0.0)
    dsf_alpha: float = Field(default=0.2, gt=0.0)
    ewald_accuracy: float = Field(default=1.0e-8, gt=0.0)
    dftd3_cutoff: float | None = Field(default=None, gt=0.0)
    dftd3_smoothing_fraction: float | None = Field(default=None, gt=0.0)
    use_pbc: bool = Field(default=False)
    redirect_stdout: Path | None = Field(default=None)
    opt_type: Literal["opt", "optts"] = Field(default="opt")
    compute_hessian: bool = Field(default=False, description="Compute Hessian via finite differences after optimization")

    def to_cli_args(self) -> list[str]:
        args = ["--model", self.model]
        if self.device is not None:
            args += ["--device", self.device]
        if self.compile_model:
            args.append("--compile")
        if self.ensemble_member != 0:
            args += ["--ensemble-member", str(self.ensemble_member)]
        if self.revision is not None:
            args += ["--revision", self.revision]
        if self.token is not None:
            args += ["--token", self.token]
        if self.charge is not None:
            args += ["--charge", str(self.charge)]
        if self.mult is not None:
            args += ["--mult", str(self.mult)]
        if not self.forces:
            args.append("--no-forces")
        if self.nb_threshold != 120:
            args += ["--nb-threshold", str(self.nb_threshold)]
        if self.needs_coulomb is True:
            args.append("--needs-coulomb")
        elif self.needs_coulomb is False:
            args.append("--no-needs-coulomb")
        if self.needs_dispersion is True:
            args.append("--needs-dispersion")
        elif self.needs_dispersion is False:
            args.append("--no-needs-dispersion")
        if self.coulomb_method is not None:
            args += ["--coulomb-method", self.coulomb_method]
            if self.coulomb_method == "dsf":
                args += ["--coulomb-cutoff", str(self.coulomb_cutoff), "--dsf-alpha", str(self.dsf_alpha)]
            elif self.coulomb_method == "ewald":
                args += ["--ewald-accuracy", str(self.ewald_accuracy)]
        if self.dftd3_cutoff is not None:
            args += ["--dftd3-cutoff", str(self.dftd3_cutoff)]
        if self.dftd3_smoothing_fraction is not None:
            args += ["--dftd3-smoothing-fraction", str(self.dftd3_smoothing_fraction)]
        if self.use_pbc:
            args.append("--pbc")
        if self.redirect_stdout is not None:
            args += ["--redirect-stdout", str(self.redirect_stdout)]
        if self.compute_hessian:
            args.append("--hessian")
        args += ["--opt-type", self.opt_type]
        return args
