# Running the documentation notebooks

`run_notebooks.py` executes the notebooks in `docs/contents/notebooks/` and writes a
machine-readable summary of what happened. They drive real ORCA calculations and install
their own third-party dependencies at runtime, so they can never run in GitHub CI — this
script is how they get exercised anywhere else.

Every notebook runs

- in **its own process**, so a crashed kernel costs one notebook, not the run,
- in **its own scratch directory**, so nothing is written next to the notebook sources,
- under **its own wall-clock limit**, enforced by killing the whole process group — an
  ORCA that outlives its notebook cannot keep burning the machine.

## Setup

The notebooks run in whatever Python environment the script runs in:

```bash
uv sync --group notebooks
```

That group carries `nbclient`, `ipykernel`, `nbformat` and — because the notebooks
themselves run `!{sys.executable} -m pip install ...`, and uv-created environments have no
`pip` — `pip`.

ORCA is found the way OPI always finds it (`OPI_ORCA`, the config file, `$PATH`). The
script prints the version it resolved before it starts; `NOT FOUND` there means every
ORCA notebook is about to fail.

## Locally

```bash
# every notebook, one at a time
scripts/run_notebooks.py local

# one notebook, keeping its working directory for inspection
scripts/run_notebooks.py local how_to_opi --keep all

# a subset, by name or glob
scripts/run_notebooks.py local 'extrapolate_*' redox

# what would run?
scripts/run_notebooks.py list
```

Or through nox, which syncs the dependency group for you:

```bash
uv run nox -s notebooks -- local how_to_opi
```

`-j N` runs N notebooks at once. It is off by default for a reason: nearly every notebook
`pip install`s into the running environment, and concurrent installs into one environment
corrupt it. Use it only with notebooks you know do not install anything.

## On SLURM

One array task per notebook, submitted from the login node:

```bash
scripts/run_notebooks.py slurm \
    --partition normal --account myproject \
    --time 08:00:00 --cpus-per-task 8 --mem 32G --max-parallel 4
```

The command returns as soon as the array is queued and prints the run directory. Add
`--wait` to block and report at the end instead, or check on it later with:

```bash
scripts/run_notebooks.py report notebook-runs/20260914T101500Z
```

Notes on the SLURM mode:

- `--time`, `--cpus-per-task` and `--mem` are **per notebook**, not for the suite. Sizing
  one job for the slowest notebook is exactly what the per-notebook layout avoids.
- `--max-parallel` throttles the array (`--array=0-N%max`). Keep it low enough that the
  notebooks are not fighting each other for cores.
- The tasks inherit your submitting environment (`--export=ALL`), including the active
  virtualenv, and the job script calls the interpreter you submitted with by absolute
  path. So the environment you tested with on the login node is the one that runs — as
  long as it lives on shared storage.
- For anything the environment cannot carry (`module load`, sourcing a site profile,
  exporting `OPI_ORCA`), put the shell snippet in a file and pass `--preamble FILE`; it is
  inserted into the job script verbatim.
- `--dry-run` writes the job script and prints it without submitting. Use it to check the
  directives before spending queue time.
- The generated `<run-dir>/job.sh` is a complete, re-submittable record of the run.

A single notebook of an existing run can always be re-run by hand, on the same node or
another one:

```bash
scripts/run_notebooks.py task <run-dir> <index>      # index as in manifest.json
```

## Output layout

```
notebook-runs/<RUN_ID>/
├── manifest.json          what was queued, with what settings, from which commit
├── job.sh                 the submitted sbatch script (SLURM runs only)
├── summary.json           the merged result; rewritten by every `report`
├── results/<name>.json    one result per notebook, written as each finishes
├── logs/<name>.log        stdout/stderr of each notebook's execution
├── logs/slurm-%A_%a.out   the array tasks' own output (SLURM runs only)
├── executed/<name>.ipynb  the executed notebook, always kept — outputs and tracebacks
└── artifacts/<name>/      the working directory, per --keep (default: failures only)
```

Per-notebook status is `passed`, `failed` (a cell raised), `timeout` (a cell or the whole
notebook overran), `error` (something went wrong around the notebook: dead kernel, no
kernelspec, the supervisor could not do its job), `skipped`, or `missing` (no result file
— the task has not run yet, or it was killed hard enough to write nothing).

Run status is `completed` when every notebook has a result and `incomplete` otherwise.
The exit code is 0 only if nothing failed, timed out, errored or went missing.

## Reading the summary

```bash
S=notebook-runs/<RUN_ID>/summary.json

# everything that did not pass
jq -r '.notebooks[] | select(.status!="passed" and .status!="skipped")
       | "\(.name)\t\(.status)\t\(.error.kind): \(.error.message)"' "$S"

# headline numbers and provenance
jq '{status, totals, orca: .environment.versions.orca, commit: .environment.git.commit}' "$S"

# slowest notebooks
jq -r '.notebooks | map(select(.duration_s)) | sort_by(-.duration_s)[:5][]
       | "\(.duration_s)s\t\(.name)"' "$S"

# resubmit just the failures
scripts/run_notebooks.py slurm $(jq -r '.notebooks[]
    | select(.status=="failed" or .status=="timeout") | .name' "$S")
```

## Skipped notebooks

Four notebooks cannot run unattended and are skipped by default:

| Notebook | Why |
|---|---|
| `extopt`, `ir_spectrum`, `ml_properties` | require external tooling |
| `opencosmors` | its openCOSMO-RS_py install instruction is in a markdown cell, so the import always fails |

Change the list with `--skip a,b,c` (`--skip ''` skips nothing), or override it for one
notebook by naming it explicitly: `run_notebooks.py local opencosmors` runs it.

## Gotchas

- **The notebooks install into the environment they run in.** 18 of the 19 run
  `pip install --upgrade`. Do not point this at an environment you care about; use a
  dedicated one and recreate it (`uv sync`) before each unattended run, which also prunes
  what the last one left behind.
- **A red run is not automatically an OPI bug.** The notebooks install unpinned
  third-party packages, so a new chemprop or numpy release can turn them red with no OPI
  commit involved. Compare `environment.versions` and `error.kind` across runs before
  reaching for `git bisect`.
- **Notebooks need network egress**, both for those installs and for data they fetch at
  runtime. On a cluster, check this on a *compute* node — it routinely differs from the
  login node — and set `https_proxy` in the `--preamble` if the site needs one.
- **Keep the scratch base on node-local disk.** ORCA is I/O heavy. The default is
  `$SLURM_TMPDIR` if the site sets it, else `$TMPDIR`, else the system temp directory;
  override with `--scratch-base`.
- **`chemeleon_orca` is the expensive outlier** — it installs torch and downloads a large
  checkpoint. It is the first candidate for `--skip` if runtime or egress is a problem.
- Run one ORCA job of your own inside an allocation before trusting a first cluster run.
  ORCA spawns its own `mpirun`, so it must be launched directly, never through `srun`.

## A weekly unattended run

There is no cron wrapper: the script is the wrapper. A crontab entry on the submit host
is enough, because a fresh timestamped run directory is created on every invocation and
`squeue` throttling is the array's job, not a lock file's.

```cron
SHELL=/bin/bash
MAILTO=""
15 3 * * 0 cd /path/to/opi && git pull --ff-only && uv sync --group notebooks && \
           .venv/bin/python scripts/run_notebooks.py slurm --partition normal \
           --time 08:00:00 >> $HOME/opi-notebooks-cron.log 2>&1
```

If the site offers `scrontab`, prefer it: the schedule then lives in the scheduler and
survives submit-host reboots.
