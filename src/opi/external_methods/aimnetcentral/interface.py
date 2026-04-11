from __future__ import annotations

import shlex
import sys
from pathlib import Path
from typing import Literal

from pydantic import Field

from opi.input.blocks.block_method import BlockMethod
from opi.input.simple_keywords.base import SimpleKeyword
from opi.input.simple_keywords.external_tools import ExternalTools

from .config import AimnetCentralConfig


def get_aimnetcentral_wrapper_path() -> Path:
    return Path(__file__).with_name("run_aimnetcentral_extopt.py")


def create_aimnetcentral_extopt(
    config: AimnetCentralConfig | None = None,
    opt_type: Literal["opt", "optts"] = "opt",
) -> tuple[SimpleKeyword, BlockMethod]:
    """Create the ORCA `! extopt` + `%method ProgExt ...` pair for AIMNetCentral.
    
    Parameters
    ----------
    config : AimnetCentralConfig | None
        Configuration object for AIMNetCentral. If None, default config is used.
    opt_type : Literal["opt", "optts"]
        Optimization type. "opt" for regular geometry optimization, "optts" for
        transition state optimization. When provided, creates a new config with
        this opt_type setting.
    
    Returns
    -------
    tuple[SimpleKeyword, BlockMethod]
        The extopt keyword and method block for ORCA input.
    """
    config = config or AimnetCentralConfig()
    if opt_type != "opt":
        config = config.model_copy(update={"opt_type": opt_type})
    wrapper = get_aimnetcentral_wrapper_path()
    block = BlockMethod(
        ProgExt=sys.executable,
        Ext_Params=shlex.join([str(wrapper), *config.to_cli_args()]),
    )
    return ExternalTools.EXTOPT, block
