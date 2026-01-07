# Examples for the ORCA Python Interface (OPI)

This folder contains example scripts and input files demonstrating how to use OPI with ORCA.

These examples serve **two purposes**:

- **Learning resource:** They show new users how to set up and run typical calculations with OPI.
- **Integration tests:** The same examples are executed by our test suite (see [`tests/examples`](../tests/examples)) to ensure that OPI's basic functionality and ORCA interface continue to work.

## Notes for Users

- To run an example manually, you can execute the corresponding script within the folder:

```bash
python3 job.py
```

## Notes for Contributors

- If you modify an example, make sure the corresponding test still passes.
- If you add a new example, please also add it to the list below and (if possible) add a test for it.

## List of Examples
- exmp001_scf: Perform a HF/def2-SVP single-point
- exmp002_scf_ccsdt: Perform a CCSD(T)/def2-SVP single-point
- exmp003_opt: Perform a wB97X-3c geometry optimization
- exmp004_freq: Perform a TPSS/def2-SVP frequency calculation
- exmp005_dft: Perform a B3LYP-D3/def2-SVP single-point calculation with custom D3 parameters
- exmp006_mp2: Perform a MP2/def2-TZVP single-point calculation.
- exmp007_cpcm: Perform a BP86/def2-SVP single-point calculation with implicit CPCM solvation for water
- exmp008_relativ_corr: Perform a BP86/SARC-ZORCA-SVP calculation with the ZORA approximation for scalar relativistic effects
- exmp009_rama: Perform a Raman calculation with PBE0/def2-SVP
- exmp010_uvvis: Perform a TD-DFT calculation with B3LYP/def2-TZVP + CPCM(Hexane)
- exmp011_epr: Calculate EPR properties with B3LYP/EPR-II
- exmp012_nmr: Calculate NMR properties with RI-MP2/pcSseg-2
- exmp013_bs: Perform a broken symmetry calculation with B3LYP/SVP (B3LYP/G)
- exmp014_led: Perform an LED decomposition with DLPNO-CCSD(T)/cc-pVDZ
- exmp015_pop_analysis: Get multiple population analysis results from DSD-PBEP86/def2-SVP
- exmp016_autoci: Use AUTO-CI to run CISD/def2-SVP single-point
- exmp017_roci: Perform a ROCIS calculation
- exmp018_cipsi: Perform a ICE-CI calculation
- exmp019_engrad: Perfrom an energy & gradient calculation with r²SCAN-3c
- exmp020_smd: Run a r²SCAN-3c+SMD(Water) calculation
- exmp021_basis: Run a BP86/def2-SVP energy calculation with additional diffuse function for oxygen
- exmp022_scf_block: Run a PBE0/def2-SVP energy calculation and rotate the initial SCF guess
- exmp023_thermo: Obtain thermostatistical corrections from a frequency calculation
- exmp024_blocks: Demonstrate input of blocks
- exmp025_goat: Perform a GOAT conformer search
- exmp026_scan: Perform scans of bond/angle/dihedral
- exmp027_constraints: Perform a constrained geometry optimization
- exmp028_nevpt2: Run a NEVPT2 calculation
- exmp029_oomp2: Run a OO-MP2 calculation
- exmp030_eom: Run a EOM-CCSD calculation
- exmp031_dlpno_ccsdt: Perform a DLPNO-CCSD(T) calculation
- exmp032_fragbasis: Assign different basis sets to different fragments
- exmp033_mo_getters: Access to molecular orbital data
- exmp034_strucfile: Hand structure as external file to ORCA
- exmp035_moplot: Plot cube files from density/MOs
- exmp036_solvator: Run ORCAs autosolvation workflow (solvator)
- exmp037_s2: Get the S² expectation value from an unrestricted calculation
- exmp038_integrals: Get integrals from a calculation
- exmp039_neb: Perfrom a transition state search with NEB
- exmp040_xzyfraglib: Assign fragments with external fragment library (frag_lib.xyz)
- exmp041_graph: How to print overview of the available results in output
- exmp042_element: Access cardinal numbers of a structure
- exmp043_dummy_atom: Perform a calculation with a dummy atom
- exmp044_from_ase: Get the structure from an ASE atoms object
- exmp045_existing_calc: Obtain results from an already existing calculation
- exmp046_server: Demonstrates how to use ExtOpt methods with OpiServer
- exmp047_trj: Perform calculations on all structures of a multi-xyz (trj) file
- exmp048_loc_gbw: Read localized MO coefficients and transform integrals in LMO basis
- exmp049_arbitrary_block_variable: Use arbitrary block variable in the SCF block
- exmp050_docker: Use DOCKER to dock water with water

