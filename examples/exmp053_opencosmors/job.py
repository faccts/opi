import shutil
import sys
from pathlib import Path

from opi.core import Calculator
from opi.input.simple_keywords import SolvationModel, Solvent
from opi.input.structures import Structure
from opi.output.core import Output


def run_exmp053(
    structure: Structure | None = None, working_dir: Path | None = Path("RUN")
) -> Output:
    # > recreate the working dir
    shutil.rmtree(working_dir, ignore_errors=True)
    working_dir.mkdir()

    # > if no structure is given read structure from inp.xyz
    if structure is None:
        structure = Structure.from_xyz("inp.xyz")

    # > set up the calculator
    calc = Calculator(basename="job", working_dir=working_dir)
    calc.structure = structure
    calc.input.add_simple_keywords(SolvationModel.COSMORS(Solvent.ACETONITRILE))

    # > write the input and run the calculation
    calc.write_input()
    calc.run()

    # > get the output and check some results
    output = calc.get_output()
    if not output.terminated_normally():
        print(f"ORCA calculation failed, see output file: {output.get_outfile()}")
        sys.exit(1)
    # << END OF IF

    # > Parse JSON files
    output.parse()

    # > Parse JSON files
    output.parse()

    return calc.get_output()


if __name__ == "__main__":
    output = run_exmp053()
