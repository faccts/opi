from pathlib import Path


class ExtoptInterface:
    """
    Class for reading and writing ORCA files related to the ExtOpt keyword
    """

    def read_extopt_input(self, filepath: Path) -> tuple[str, int, int, int, bool, str | None]:
        """
        Reads an input file written by ORCA and returns the parsed values as a tuple.

        Attributes
        ----------
        filepath: Path
            Path to the EXT input file.

        Returns
        -------
        xyz_filename: str
        charge: int
        multiplicity: int
        number of cores: int
        do_gradient: bool
        pointcharge_filename: str | None
        """
        # Get every first entry of each line of input file
        with open(filepath, "r") as f:
            lines = [line.split(" ")[0].strip() for line in f.readlines() if line.strip()]

        if len(lines) < 5:
            raise ValueError("Input file must have at least 5 lines.")

        # Save information
        xyz_filename = lines[0]
        charge = int(lines[1])
        multiplicity = int(lines[2])
        ncores = int(lines[3])

        # Check if gradient should be calculated or not
        try:
            do_gradient = int(lines[4]) == 1
        except ValueError as err:
            raise ValueError("do_gradient from ORCA input must be 0 or 1.") from err

        # Some sanity checks
        if multiplicity < 1:
            raise ValueError("Multiplicity must be a positive integer.")
        if ncores < 1:
            raise ValueError("NCores must be a positive integer.")

        # Optional pointcharges
        pointcharge_filename = lines[5] if len(lines) >= 6 else None

        return (
            xyz_filename,
            charge,
            multiplicity,
            ncores,
            do_gradient,
            pointcharge_filename,
        )

    def write_orca_input(
        self,
        filename: Path,
        nat: int,
        etot: float,
        grad: list[float] | None = None,
    ) -> None:
        """
        Writes an input for ORCA similar to external-tools format.

        Attributes
        ----------
        filepath: Path
            Path to file to write to.
        nat: int
            number of atoms
        etot: int
            total energy in Hartree
        grad: list[float]
            gradients as plain list in Hartee/Bohr
            if not present or empty, it is not written
        """
        with open(filename, "w") as f:
            output = "#\n"
            output += "# Number of atoms\n"
            output += "#\n"
            output += f"{nat}\n"
            output += "#\n"
            output += "# Total energy [Eh]\n"
            output += "#\n"
            output += f"{etot:.12e}\n"
            if grad:
                output += "#\n"
                output += "# Gradient [Eh/Bohr] A1X, A1Y, A1Z, A2X, ...\n"
                output += "#\n"
                output += "\n".join(f"{g: .12e}" for g in grad) + "\n"
            f.write(output)
