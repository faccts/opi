"""
Module that contains `Runner` class which facilities execution of ORCA binaries.
"""

import json
from collections.abc import Sequence
from pathlib import Path

from opi.execution.base import BaseRunner
from opi.lib.orca_binary import OrcaBinary


class Runner(BaseRunner):
    """
    This class should be to used to execute the following ORCA binaries:
    - `orca`
    - `orca_plot`
    - `orca_2json`
    """

    def run_orca(
        self, inpfile: Path, /, *extra_args: str, silent: bool = True, timeout: int = -1
    ) -> None:
        """
        Execute ORCA's main binary and pass the path to the main input file as well as extra arguments.

        Parameters
        ----------
        inpfile : Path
            Path to ORCA's main input file.
        *extra_args: str
            Additional arguments passed to ORCA.
        silent : bool, default: True
            Capture and discard STDOUT and STDERR.
        timeout : int, default: -1
            Optional timeout in seconds to wait for process to complete.
        """
        if not inpfile.is_file():
            # Raises an error if the input file does not exist
            raise FileNotFoundError(f"Input file {inpfile} does not exist")

        # Sets the output and error file from the inpfile.
        outfile = inpfile.with_suffix(".out")
        errfile = inpfile.with_suffix(".err")

        # > CLI arguments
        arguments = [inpfile.name]
        if extra_args:
            # > All extra arguments are passed as second argument to ORCA.
            arguments += list(extra_args)

        # Run the Orca calculation
        self.run(
            OrcaBinary.ORCA,
            arguments,
            stdout=outfile,
            stderr=errfile,
            silent=silent,
            timeout=timeout,
        )

    def run_orca_plot(
        self,
        gbwfile: Path,
        stdin_list: list[str],
        /,
        *extra_args: str,
        silent: bool = True,
        timeout: int = -1,
    ) -> None:
        """
        Executes the orca_plot binary in the interactive mode and passes the gbw path, an input string, and extra
        arguments to the binary. Note that currently only the interactive mode (orca_plot (gbw) -i) is supported.

        Parameters
        ----------
        gbwfile : Path
            Path to an ORCA geometry, basis set, wavefunction (gbw) file.
        stdin_list : list[str]
            Input string handed to stdin of orca_plot.
        *extra_args: str
            Additional arguments passed to orca_plot.
        silent : bool, default: True
            Capture and discard STDOUT and STDERR.
        timeout : int, default: -1
            Optional timeout in seconds to wait for process to complete.

        Raises
        ----------
        FileNotFoundError
            If the gbw file for plotting does not exist.
        ValueError
            If no stdin_list for the input of orca_plot is provided.
        """
        if not gbwfile.is_file():
            raise FileNotFoundError(f"GBW file {gbwfile} does not exist")

        if not stdin_list:
            raise ValueError("stdin_list is required but was empty or not provided.")

        # Sets the output and error file from the gbwfile.
        outfile = gbwfile.with_suffix(".plot.out")
        errfile = gbwfile.with_suffix(".plot.err")

        # > CLI arguments
        arguments = [gbwfile.name]
        # > Request interactive plot mode by adding "-i"
        arguments += ["-i"]
        if extra_args:
            # > All extra arguments are passed as third argument to orca_plot.
            arguments += list(extra_args)

        # > Generate stdin string from stdin list
        stdin_str = "\n".join(stdin_list) + "\n"

        # Run orca_plot
        self.run(
            OrcaBinary.ORCA_PLOT,
            arguments,
            stdin_str=stdin_str,
            stdout=outfile,
            stderr=errfile,
            silent=silent,
            timeout=timeout,
        )

    def run_orca_2json(
        self, args: Sequence[str] = (), /, *, working_dir: Path | None = None
    ) -> None:
        """
        Execute `orca_2json` with given arguments.

        Parameters
        ----------
        args : Sequence[str], default: ()
            Arguments to pass to `orca_2json`.
        """
        self.run(OrcaBinary.ORCA_2JSON, args, cwd=working_dir)

    def create_property_json(self, basename: str, /, *, force: bool = False) -> None:
        """
        Create the `<basename>.property.json` file from `<basename>.property.txt`.

        Parameters
        ----------
        basename : str
            Basename of ORCA calculation.
        force : bool, default: False
            Overwrite existing JSON file with no mercy.
        """

        property_json_file = Path(f"{basename}.property.json")
        if property_json_file.is_file() and not force:
            return
        else:
            # > Delete eventually existing ".property.json" and recreate
            property_json_file.unlink(missing_ok=True)
            self.run_orca_2json([basename, "-property"])

    def create_gbw_json(
        self,
        basename: str,
        /,
        *,
        force: bool = False,
        config: dict[str, bool | str | list[str | int]] | None = None,
        suffix: str = ".gbw",
    ) -> None:
        """
        Create the `<basename>.json` file from `<basename>.gbw`.

        Parameters
        ----------
        basename : str
            Basename of ORCA calculation.
        force : bool, default: False
            Overwrite existing JSON file with no mercy.
        config : dict[str, bool | str | list[str | int]] | None, default: None
            Determine contents of gbw-json file.
            For details about the configuration refer to the ORCA manual "9.3.2 Configuration file"
        suffix: str, default: ".gbw"
            Suffix of the gbw file that will be used for json creation.
        """
        gbw_json_file = self.working_dir / f"{basename}.json"
        config_file = gbw_json_file.with_suffix(".json.conf")

        if gbw_json_file.is_file() and not force:
            return
        else:
            # > Delete eventually existing ".json" and recreate
            gbw_json_file.unlink(missing_ok=True)
            config_file.unlink(missing_ok=True)

            # > Create JSON-config file if given:
            if config_fmt := self.format_gbw_json_config(config):
                config_file.write_text(config_fmt)
            # > Create JSON from GBW file - Use only the filename to not confuse orca
            gbw_filename = str(gbw_json_file.with_suffix(suffix).name)
            self.run_orca_2json([gbw_filename], working_dir=gbw_json_file.parent)

    @staticmethod
    def format_gbw_json_config(config: dict[str, bool | str | list[str | int]] | None) -> str:
        """
        Format contents for gbw-json config file that determines which properties are stored in the gbw-json file.
        For details about the configuration refer to the ORCA manual "9.3.2 Configuration file"

        Parameters
        ----------
        config : dict[str bool | str | list[str | int]] | None
        """
        if not config:
            return ""
        else:
            return json.dumps(config, indent=4, check_circular=False, allow_nan=False)

    def create_jsons(
        self,
        basename: str,
        /,
        *,
        force: bool = False,
        config: dict[str, bool | str | list[str | int]] | None = None,
    ) -> None:
        """
        Create the `<basename>.json` and the `<basename>.property.json` files.

        Parameters
        ----------
        basename : str
            Basename of ORCA calculation.
        force : bool, default: False
            Overwrite any JSON file with no mercy.
        config : dict[str | bool | str | list[str | int]] | None, default: None
            Determine contents of gbw-json file.
            For details about the configuration refer to the ORCA manual "9.3.2 Configuration file".
        """
        self.create_gbw_json(basename, force=force, config=config)
        self.create_property_json(basename, force=force)
