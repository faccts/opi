# Changelog

## [2.0.0] - 2026-02-10

### Added 
- Added Pydantic output models for S, H, F, J and K integrals. #7
- Added templates for bug reports, feature requests and pull requests. #4
- Added function to access optimized structure easier from `Output` class. #10
- Added `Output._safe_get()` function to search output tree. #10
- Addition of functions in `Output` to check if geometry optimization and SCF have converged. #12
- Add parameters to `Output.parse()` function to control whether respective JSON file is parsed or not. #33
- Enable use of ExtOPT wrappers. #30
- Addition of new getter functions to `Output` for easier access to energies. #32
- Added `Element.from_atomic_number()` to get corresponding `Element` from atomic number. #52
- Added getters to `Output` for molecular orbitals. #56
- Initial support for `orca_plot`, which allows plotting of molecular orbitals, densities and spin-densities. #60
- Added getters for `Output` attributes. #83
- Introduce `MOData` class to hold index and spin channel data. #83
- Added support for multiple GBW files. #83
- Added `atomic_number` to `Element` class. #93
- Added `Output.print_graph()` that shows which fields in the output are populated. #84
- Added class methods to initialize Structure class: #96
  - `from_ase()` : from Atoms object of ASE
  - `from_list()`: from a list
  - `from_xyz_string()`: to directly read XYZ string
  - `from_trj_xyz()`: reads multi-XYZ files and returns list of Structure objects.(#138)
- Added `get_version()` and `check_version()` to get ORCA version from main binary and return or check it against minimum required version for OPI respectively. #112
- Added property `Strucure.nelectrons` to count number of electrons. #117
- Added `UserWarning` for if multiplicity in `Structure` and number of electrons are invalid. #127
- Added `Structure.set_ls_multiplicity()` which set the low-spin multiplicity on the `Structure`. #127
- Functions to check if multiplicity of given structure is physically reasoanble. #127
- Added `Calculator.write_and_run()` to write the ORCA `.inp` file and execute the calculation in one go. #124
- Added example tests using pytest. These are marked by the marker "examples". #137 
- Introduction of tests that require ORCA binaries, these are marked by marker "orca". #137
- Added support for adding arbitrary options to blocks which will be printed in the block along with the other options. #61
- `PropertyResults` and `GbwResults` objects can now be initialized from JSON files. #159
- Introduction of OPI unit tests . These tests are marked with marker "unit".
  - Input-side unit tests are marked with marker "input". #145
  - Output-side unit tests are marked with marker "output". #170
- Added `Properties` class for reading (relative) energies from comment line of multi-XYZ files. #151
- Extension of DFT related keywords in `BlockMethod`. #173
- Added `IrMode` class for keeping IR data. #168
- Addition of strict argument to `BaseStructureFile`. #189
- `IntGroupEnd` class created to model certain attributes in blocks. #190
- Additional functionality for `BlockBasis` added. #43
- Added `PopulationAnalysisWithAtomicCharges` for population analysis with atomic charge info.

### Fixed 
- Fixed the links on the tutorial start page. #2
- Fixed bug where `%moinp` block was printed without quotation marks around the path. #50
- Fixed `nuc` attribute in nmr to include index 0. #89
- Type annotation for fragments to `StrictNonNegativeInt`. #90
- Type annotation for `MayerPopulationAnalysis.nbondordersprint` changed to `StrictNonNegativeInt`. #99
- Renamed `xyzfraglib` to `xzyfraglib` in `BlockFrag`. #98
- Solved error using CPCM with `epsilon=inf`. #101
- Fixed bug in `OrcaVersion` not recognizing '-f.x' tags in ORCA version string. #112
- Fixed `opi.__version__` which would previously always show '0.0.0'. #122
- Fixed lookup of ORCA binaries on Windows. #123
- Fixed several Windows compatibility issues. #134
- Fixewd reading of structures from files with empty lines at the end. #138
- Fixed inconsistent indexing in `Structure.add_atom()`. #152
- Fixed inconsistency in return type of `_buffer` method in `Structure`. #151
- Fixed error in formatting of `QMMM` block attributes. #190
- Common IDE configuration directories now added to `.gitignore`, preventing git from tracking them. #192
- Fix to `fragproc` attribute in `BlockFrag`. #43
- Fixed header of documentation showing always OPI version 1.x. #194
- Fixed values of block options being automatically converted to lowercase. #191
- Fixed example 40 not taking `working_dir`.
- Fixed test of example 47 not receiving a `working_dir`.

## Changed
- Raised minimal required ORCA version to 6.1.1. The test examples where updated accordingly.
- Configuration of a path to Open MPI is now optional. #17
- `Element` enum is now case-insensitive. #52
- `Input.get_structure()` now adds fragment IDs to the structure with argument `with_fragments`. #34
- HOMO and LUMO getters now keep information about the index and MO channel. #83
- `Output.gbw_json_file()` is now a list of JSON files. #83
- `Calculator` class now does ORCA binary version check by default, but it can be turned off. #112
- Moved create logic in `Output` from `init()` to `parse()`. #116
- If Ruff alters source code then Nox exits with non-zero-status. #126
- `Calculator.write_input()` now returns boolean that says whether an existing input has been overwritten. #124
  - Overwriting existing input can be controlled using `force` argument.
- `Calculator.run()` now returns boolean that indicates whether the ORCA calculation terminated normally. #124
- Allow variable suffixes when creating gbw JSON files. #147
- Calculator.write_input() now delegates formatting to `Input.format_before_coords()` and `Input.format_after_coords()`. #155
- `Output.parse()` now delegates parsing of gbw and property JSON files to `Output.parse_gbw()` and `Output.parse_property()` respectively. #172
- `property_json_file` and `gbw_json_files` are now properties, allowing custom JSON file names to be set via setters. #172 
- Improved typing of the `_orca_environment` decorator using PEP 612 (`ParamSpec` and `Concatenate`), preserving function signatures for IDEs and type checkers. #182
