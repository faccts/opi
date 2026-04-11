# exmp056_aimnetcentral_nse

This example demonstrates AIMNetCentral with NSE (Neural Spin Equilibration) for open-shell systems.

## NSE Model Requirements

The AIMNet2-NSE model (`aimnet2nse`) supports open-shell chemistry with spin-polarized charges:
- Requires `num_charge_channels=2` (vs. 1 for closed-shell models)
- Needs both `charge` and `mult` (multiplicity) inputs
- Outputs `spin_charges` in addition to regular `charges`

## Usage

### Command line (direct)

```bash
# Set multiplicity via command line
python3 run_aimnetcentral_extopt.py --model aimnet2nse --mult 2.0

# Or via config file
python3 -m opi.external_methods.aimnetcentral.run_aimnetcentral_extopt --model aimnet2nse --mult 2.0
```

### With ORCA ExtOpt (recommended)

```python
from opi.external_methods import AimnetCentralConfig, create_aimnetcentral_extopt

config = AimnetCentralConfig(
    model="aimnet2nse",
    charge=0.0,    # Molecular charge
    mult=2.0,      # Spin multiplicity (2S+1)
)

extopt_kw, aimnet_block = create_aimnetcentral_extopt(config)
```

### ORCA input file

Add to your ORCA input:
```
! extopt
%method
 ProgExt "python3"
 Ext_Params "path/to/run_aimnetcentral_extopt.py --model aimnet2nse --mult 2.0"
end
```

## NSE Model Selection

| Model | `num_charge_channels` | Use case |
|-------|----------------------|----------|
| `aimnet2`, `aimnet2_2025` | 1 | Closed-shell systems |
| `aimnet2nse` | 2 | Open-shell systems (radicals, diradicals) |
| `aimnet2pd` | 1 | Protein-ligand binding |

## Spin Multiplicity Guide

| Multiplicity | Spin (S) | Electrons | Example |
|--------------|----------|-----------|---------|
| 1 | 0 | Even | Closed-shell, singlet |
| 2 | 1/2 | Odd | Doublet, radicals |
| 3 | 1 | Even | Triplet, diradicals |
| 4 | 3/2 | Odd | Quartet, radicals |

For radicals: `multiplicity = number_of_unpaired_electrons + 1`

## Verifying Spin Charge Output

After calculation, check:
- `spin_charges`: Spin-polarized atomic charges (sum should equal `mult - 1`)
- `charges`: Total atomic charges
- For doublet (`mult=2`): `sum(spin_charges) ≈ 1.0`

## Python API

```python
from aimnet.calculators import AIMNet2Calculator, AIMNet2ASE

# Direct calculator
calc = AIMNet2Calculator("aimnet2nse")
data = {
    "coord": coord,
    "numbers": numbers,
    "charge": 0.0,
    "mult": 2.0,
}
results = calc(data)
print(results["spin_charges"])  # Spin-polarized charges

# ASE calculator
from ase import Atoms
atoms = Atoms("CH3", positions=...)
atoms.calc = AIMNet2ASE("aimnet2nse", charge=0, mult=2)
atoms.get_potential_energy()
spin_charges = atoms.calc.get_spin_charges()
```
