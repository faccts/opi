#!/usr/bin/env python3

from pathlib import Path
import shutil
import sys
import warnings

from opi.core import Calculator
from opi.input.structures.structure import Structure
from opi.input.blocks import BlockMethod
from opi.input.simple_keywords import ExternalTools
from opi.input.simple_keywords import Opt
from opi.external_methods.server import OpiServer, ServerStatus

# ------------------------------------------------------------------------
# For this example, a server and client script must be installed.
# You can get them from https://github.com/faccts/orca-external-tools
# Remember that some scripts like umaserver require additional steps
# like logging into your HuggingFace account.
# More information are given in the respective tutorial here:
# https://www.faccts.de/docs/orca/6.1/tutorials/workflows/extopt.html
# -------------------------------------------------------------------------

# Initiate Server object
server = OpiServer(
    # Change the following path to a server script, e.g., from orca-external-tools
    serverpath="/path/to/working/server/script/from/orca-external-tools"
)

# Start server
status = server.start_server(exe="bash")
if status != ServerStatus.RUNNING:
    if status == ServerStatus.ALREADY_RUNNING:
        warnings.warn("Some server was already running. Using old one.")
    elif status == ServerStatus.PORT_IN_USE:
        warnings.warn("Port for server in use. Continue on your own risk.")
    else:
        print(f"Server setup returned with error {status}")
        sys.exit(1)

# Working dir handling
working_dir = Path("RUN")
shutil.rmtree(working_dir, ignore_errors=True)
working_dir.mkdir()

# Calculator setup
structure = Structure.from_xyz("h2o.xyz")
orca_calc = Calculator(basename="extopt_ext", working_dir=working_dir)
orca_calc.structure = structure
orca_calc.input.ncores = 2
orca_calc.input.add_simple_keywords(ExternalTools.EXTOPT, Opt.OPT)
# Change the following path to a client script, e.g., from orca-external-tools
path_client = "/path/to/working/client/script/from/orca-external-tools"
orca_calc.input.add_blocks(BlockMethod(ProgExt=path_client))
orca_calc.write_input()

# Run the calculation
print("Running ORCA calculation ...", end="")
orca_calc.run()
print("   Done")

# Terminate server again
server.kill_server()
