"""
Main module of OPI.
This module contains the `Calculator` class which combines job setup (i.e. input creation), execution and parsing of results.
"""

from os import PathLike
from pathlib import Path
from typing import Any, cast

from opi.execution.core import Runner
from opi.input.arbitrary_string import ArbitraryStringPos
from opi.input.blocks.block_output import BlockOutput
from opi.input.core import Input
from opi.input.structures.structure import Structure
from opi.input.structures.structure_file import BaseStructureFile
from opi.output.core import Output


class Calculator:
    """
    The Calculator class is a convenience class that combines job setup (i.e. input creation), execution and parsing of results.
    Each of these steps can also be performed individually using the respective `Input`, `Runner` and `Output` classes.
    Only for input creation the `Calculator` class and `Input` class are required. As the former
    contains the chemical structural information, while the latter contains all the other ORCA input parameters.
    This allows for an almost completely independent treatment of calculation and structural parameters.

    Attributes
    ----------
    _basename | basename: str
        Basename of the calculation.
    _working_dir | working_dir: Path | None
        Optional working directory.
    structure: Structure | BaseStructureFile
        Primary structure of the calculation. This can either be a `Structure` which is converted into ORCA's `*xyz`
         block or class derived from `BaseStructureFile` which is just passed onto ORCA.
    _inpfile | inpfile: Path | None
        Path to ORCA input file. Read-only property.
    json_via_input: bool, default: True
        Tell ORCA to automatically create the JSONs files automatically.
        Can only be disabled after initialization of a `Calculator` (not recommended!).
    _input | input: Input
        Contains all ORCA input parameters except for the primary structural information.
    """

    def __init__(
        self,
        basename: str,
        working_dir: Path | str | PathLike[str] | None = None,
        *,
        version_check: bool = True,
    ) -> None:
        """
        Parameters
        ----------
        basename : str
            Basename of the calculation. Each file created by ORCA starts with this prefix.
        working_dir : Path | str | None, default=None
            Optional working direction. Is passed on to `Runner` and `Output` classes.
        version_check : bool, default: True
            Check ORCA's binary version upon initialization.
            Important: May create significant computational overhead if many `Calculators` are initialized concurrently.
        """

        # -----------------------------
        # > Job Parameters
        # -----------------------------
        # > Basename of calculation
        self._basename: str = ""
        self.basename: str = basename
        # > Working dir. Must exist!
        self._working_dir: Path = Path.cwd()
        self.working_dir: Path = cast(Path, working_dir)

        # -----------------------------
        # > Primary Structure
        # -----------------------------
        self.structure: Structure | BaseStructureFile | None = None

        # -----------------------------
        # > Input File
        # -----------------------------
        self._inpfile: Path | None = None

        # -----------------------------
        # > HELPER VARIABLES
        # -----------------------------
        # // Force JSON write in ORCA output block
        self.json_via_input: bool = True

        # -----------------------------
        # > ORCA INPUT
        # -----------------------------
        self._input: Input = Input()

        # ----------------------------
        # > BINARY VERSION CHECK
        # ----------------------------
        if version_check:
            # > Raises RuntimeError if version is not compatible or cannot be determined.
            self.check_version()

    # &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
    # PROPERTIES
    # &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
    @property
    def basename(self) -> str:
        if not self._basename:
            raise ValueError("The basename cannot be empty!")
        return self._basename

    @basename.setter
    def basename(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError(f"`basename` must be a string, not {type(value)}.")
        # > Check if basename contains whitespaces
        if " " in value:
            raise ValueError("The basename cannot contain spaces.")
        # > Basename cannot be empty
        if not value:
            raise ValueError("The basename cannot contain be empty.")
        # > Assign new basename
        self._basename = value

    @property
    def input(self) -> Input:
        return self._input

    @input.setter
    def input(self, value: Input, /) -> None:
        """
        Parameters
        ----------
        value : Input
        """
        self._input = value

    @property
    def inpfile(self) -> Path | None:
        return self._inpfile

    @inpfile.setter
    def inpfile(self, value: Any, /) -> None:
        """
        Read-only property.

        Parameters
        ----------
        value : Any
        """
        raise AttributeError(f"{self.__class__.__name__}.inpfile: is a read-only property.")

    @property
    def working_dir(self) -> Path:
        return self._working_dir

    @working_dir.setter
    def working_dir(self, value: Path | str | PathLike[str] | None) -> None:
        """
        Parameters
        ----------
        value : Path | str | PathLike[str] | None
        """
        # > Unsetting working_dir by setting it to CWD.
        # > Thereby, working_dir is never "unset".
        if value is None:
            self._working_dir = Path.cwd()
        else:
            value = Path(value)
            if not value.is_dir():
                raise ValueError(
                    f"{self.__class__.__name__}.working_dir: {value} does is not a directory!"
                )
            # > Completely resolving path
            self._working_dir = value.expanduser().resolve()

    # &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
    # METHODS
    # &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
    def write_input(self) -> None:
        """
        Function to create the ORCA input file `.inp`.

        Raises
        ------
        RuntimeError
          * When `.inp` cannot be written.
        ValueError
          * When the `moinp` path is given, and it is not a subpath of the working directory.
        """

        assert self.working_dir
        self._inpfile = self.working_dir / f"{self.basename}.inp"

        # add JSON generation to output blocks
        if self.json_via_input:
            self._set_json_output_block()

        try:
            input_param = self.input
            simple_keywords = input_param.simple_keywords
            blocks = input_param.blocks.values() if input_param.blocks else ()
            arbitrary_strings = input_param.arbitrary_strings

            assert self.inpfile is not None
            with self.inpfile.open("w") as inp:
                # ---------------------------------
                # > Arbitrary Strings: top
                # ---------------------------------
                if arbitrary_strings:
                    for item in arbitrary_strings:
                        if item.pos is ArbitraryStringPos.TOP:
                            inp.write(f"{item.format_orca()}\n")

                # ---------------------------------
                # > Simple Keywords
                # ---------------------------------
                if simple_keywords:
                    for keyword in simple_keywords:
                        if isinstance(keyword, str):
                            inp.write(f"!{keyword}\n")
                        else:
                            inp.write(f"!{keyword.format_orca()}\n")

                # ---------------------------------
                # > Special Strings
                # ---------------------------------
                if (memory := input_param.memory) is not None:
                    inp.write(f"%maxcore {memory:d}\n")
                if (ncores := input_param.ncores) is not None:
                    inp.write(f"%pal\n    nprocs {ncores:d}\nend\n")
                if (moinp := input_param.moinp) is not None:
                    inp.write(f'%moinp "{moinp.relative_to(self.working_dir)}"\n')

                # ---------------------------------
                # > Block Options: Before coords
                # ---------------------------------
                if blocks:
                    for block in blocks:
                        if not block.aftercoord:
                            inp.write(f"\n{block.format_orca()}\n")

                # ---------------------------------
                # > Arbitrary Strings: Before Coords
                # ---------------------------------
                if arbitrary_strings:
                    for item in arbitrary_strings:
                        if item.pos is ArbitraryStringPos.BEFORE_COORDS:
                            inp.write(f"\n{item}\n")

                # ---------------------------------
                # > Coords block
                # ---------------------------------
                if self.structure:
                    if isinstance(self.structure, BaseStructureFile):
                        inp.write(f"{self.structure.format_orca(self.working_dir)} ")
                    else:
                        inp.write(f"\n{self.structure.format_orca()}\n")

                # ---------------------------------
                # > Block options: After coords
                # ---------------------------------
                if blocks:
                    for block in blocks:
                        if block.aftercoord:
                            inp.write(f"\n{block.format_orca()}\n")

                # ---------------------------------
                # > Arbitrary Strings: Bottom
                # ---------------------------------
                if arbitrary_strings:
                    for item in arbitrary_strings:
                        if item.pos is ArbitraryStringPos.BOTTOM:
                            inp.write(f"\n{item}\n")

        except IOError as err:
            raise RuntimeError(
                # Raises an error if the input file cannot be written
                f"Error writing input file {self.inpfile}: {err}"
            ) from err

    def _set_json_output_block(self) -> None:
        """
        Set

        %output
            jsongbwfile True

            jsonpropfile True
        end

        thereby telling ORCA to also create respective JSON files automatically.
        """
        output_block = self.input.get_blocks(BlockOutput, create_missing=True)[BlockOutput]
        # > assert correct type of block for mypy
        assert isinstance(output_block, BlockOutput)
        output_block.jsongbwfile = True
        output_block.jsonpropfile = True

    def _create_runner(self) -> "Runner":
        """Create a `Runner` object passing on `self.working_dir`."""
        return Runner(working_dir=self.working_dir)

    def run(self, *, timeout: int = -1) -> None:
        """
        Execute ORCA calculation.

        Parameters
        ----------
        timeout : int, default: = -1
            Timeout in seconds to wait for ORCA process.
            If value is smaller than zero, wait indefinitely.
        """
        runner = self._create_runner()
        assert self.inpfile
        runner.run_orca(self.inpfile, timeout=timeout)

    def create_jsons(self, *, force: bool = False) -> None:
        """
        Thin-wrapper around `Runner.create_jsons()`.
        Create the `<basename>.json` and the `<basename>.property.json` file.
        This function is by default not required.
        As ORCA is told to automatically create the JSON files.

        Parameters
        ----------
        force : bool, default: False
            Overwrite any existing ORCA JSON file.
        """
        runner = self._create_runner()
        runner.create_jsons(self.basename, force=force)

    def get_output(self) -> "Output":
        """
        Get an instance of `Output` setup for the current job.
        Can be called before execution of job.
        """
        return Output(
            basename=self.basename,
            working_dir=self.working_dir,
        )

    def check_version(self) -> None:
        """
        Check if the ORCA version of the binary is compatible with the current OPI version.
        Soft-wrapper around Runner.check_version().

        Raises
        ------
        RuntimeError: If version could not be determined or is not compatible.
        """
        runner = self._create_runner()
        # > Can raise RuntimeError
        try:
            runner.check_version(ignore_errors=False)
        except RuntimeError:
            raise
