# Changelog

## [Unreleased] - ReleaseDate

### Added
- Improve support for OpenCOSMO-RS (#205)
- Add missing pydantic fields for calculation timings (#211)
- Added `scalmp2c` to `BlockMethod` (#212)
- Add SCF (spin-)density matrix to `Output` (#204)

### Changed
- Refactored methods from Runner into BaseRunner (#193)

### Deprecated
### Removed
### Fixed

## [2.0.0] - 2026-02-10

### Breaking Changes
- **Minimum required ORCA version is now 6.1.1**.
  Older ORCA versions are no longer supported. ORCA version 6.1.0 can still be used by setting up the `Calculator` 
  without the version check and disabling it in the `Output`, but it is no longer supported.
- Remove redundant simple keywords. #48
- `Output.gbw_json_file` was replaced by `Output.gbw_json_files` (list of JSON files). #83
- `property_json_file` and `gbw_json_files` are now properties, allowing custom JSON file names to be set via setters. #116 #172 

### Added
#### Input
- Added support for adding arbitrary options to blocks which will be printed in the block along with the other options. #61
- Added class methods to initialize `Structure` class: #96
  - `from_ase()` : from Atoms object of ASE
  - `from_list()`: from a list
  - `from_xyz_block()`: to directly read XYZ string
  - `from_trj_xyz()`: reads multi-XYZ files and returns list of Structure objects. #138
- Added property `Structure.nelectrons` to count number of electrons. #117
- Added `UserWarning` for if multiplicity in `Structure` and number of electrons are invalid. #127
- Added `Structure.set_ls_multiplicity()` which set the low-spin multiplicity on the `Structure`. #127
- Functions to check if multiplicity of given structure is physically reasonable. #127
- Added `Properties` class for reading (relative) energies from comment line of multi-XYZ files. #151
- Extension of DFT related keywords in `BlockMethod`. #173
- Addition of strict argument to `BaseStructureFile`. #189

##### Calculator
- Added `get_version()` and `check_version()` to get ORCA version from main binary and return or check it against minimum required version for OPI respectively. #112
- Added `Calculator.write_and_run()` to write the ORCA `.inp` file and execute the calculation in one go. #124

#### Output
- Added getter helper functions for easier access to various `Output` attributes such as:
  - `get_structure()` function to access the (optimized) structure. #10 #34
  - `get_final_energy()` and `get_energies()` for access to the final energy and contributions to it. #32 #49
  - `get_gradient()` for access to the nuclear gradient. #56
  - `get_mos()`, `get_homo()`, `get_lumo()`, for access to molecular orbitals. #56 #83
  - `get_s2()` for SCF S², and several getters for thermo corrections and atomic charges. #83
  - `get_ir()` for access to IR intensities which are stored in `IrMode`. #168
- Addition of functions in `Output` to check if geometry optimization and SCF have converged. #12
- Added `Output.print_graph()` that shows which fields in the output are populated. #84
- Initial support for `orca_plot`, which allows plotting of molecular orbitals, densities and spin-densities. #60
- Add parameters to `Output.parse()` function to control whether respective JSON file is parsed or not. #33
- Added support for parsing multiple GBW files. #83
- Added `Element.from_atomic_number()` to get corresponding `Element` from atomic number. #52
- Added `atomic_number` to `Element` class. #93
- Allow variable suffixes when creating gbw JSON files. #147
- `PropertyResults` and `GbwResults` objects can now be initialized from JSON files. #159

#### Tests
- Added example tests. These run the examples from the example folder using the local ORCA installation (not for CI). They are marked by the marker "examples". #137
- Introduction of OPI unit tests (For CI use). These tests are marked with marker "unit":
  - Input-side unit tests are marked with marker "input". #145
  - Output-side unit tests are marked with marker "output". #170

#### External Methods
- Enable use of ExtOPT wrappers. #30 #55

### Fixed 
- Fixed the links on the tutorial start page. #2
- Fix to `fragproc` attribute in `BlockFrag`. #43
- Fixed bug where `%moinp` block was printed without quotation marks around the path. #50
- Fixed `nuc` attribute in nmr to include index 0. #89
- Change type annotation for fragments to `StrictNonNegativeInt` for the Solvator. #90
- Change type annotation for `MayerPopulationAnalysis.nbondordersprint` to `StrictNonNegativeInt`. #99
- Renamed `xyzfraglib` to `xzyfraglib` in `BlockFrag`. #98
- Solved error using CPCM with `epsilon=inf`. #101
- Fixed bug in `OrcaVersion` not recognizing '-f.x' tags in ORCA version string. #112
- Fixed `opi.__version__` which would previously always show '0.0.0'. #122
- Fixed lookup of ORCA binaries on Windows. #123
- Fixed several Windows compatibility issues. #134
- Fixed reading of structures from files with empty lines at the end. #138
- Fixed inconsistent indexing in `Structure.add_atom()`. #152
- Fixed inconsistency in return type of `_buffer` method in `Structure`. #151
- Fixed error in formatting of `QMMM` block attributes. #190
- Fixed values of block options being automatically converted to lowercase. #191
- Fixed header of documentation showing always OPI version 1.x. #194

## Changed
- Configuration of a path to Open MPI is now optional. #17
- `Element` enum is now case-insensitive. #52
- `Calculator` class now does ORCA binary version check by default, but it can be turned off. #112
- `Calculator.write_input()` now returns boolean that says whether an existing input has been overwritten. #124
  - Overwriting existing input can be controlled using `force` argument.
- `Calculator.run()` now returns boolean that indicates whether the ORCA calculation terminated normally. #124
- If Ruff alters source code then Nox exits with non-zero-status. #126
- Calculator.write_input() now delegates formatting to `Input.format_before_coords()` and `Input.format_after_coords()`. #155
