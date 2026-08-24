# Weekly notebook test run on SLURM

The notebooks in `docs/contents/notebooks/` all drive real ORCA calculations, so they can
never run in GitHub CI. These scripts run them once a week on a cluster instead, and leave
behind a machine-readable summary.

```
cron (submit host)  ->  cron_submit_notebook_tests.sh  ->  sbatch  ->  run_notebook_tests.sbatch
                                                                          |
                                                                          v
                                                          pytest -m notebooks  ->  latest.json
```

## Files

| File | Role |
|---|---|
| `notebook_tests.env.example` | Every site-specific knob. Copy to `notebook_tests.env` (gitignored) and fill in the `<<...>>` placeholders. |
| `cron_submit_notebook_tests.sh` | Cron entry point. Refreshes the checkout, prevents overlap, submits the job. |
| `run_notebook_tests.sbatch` | The job itself. Sets up scratch, ORCA and the venv, runs pytest. |
| `summary_stub.py` | Keeps `latest.json` honest when the job is killed before pytest can write it. |

## One-time setup

1. Work through the **preflight checks** below on a compute node.
2. `cp notebook_tests.env.example notebook_tests.env` and fill in every `<<...>>`.
3. Smoke test with a single notebook:
   ```bash
   # print the sbatch command without submitting
   NB_DRY_RUN=1 ./cron_submit_notebook_tests.sh

   # then, with NB_PYTEST_ARGS='-k how_to_opi' and NB_TIME=01:00:00 in the config:
   ./cron_submit_notebook_tests.sh
   squeue -u "$USER" -n opi-notebooks
   ```
4. Clear `NB_PYTEST_ARGS`, run the full suite once by hand, and read the real wall time out
   of `run.wall_time_s` in the summary. Set `NB_TIME` to roughly twice that.
5. Install the crontab entry (Sundays 03:15):
   ```cron
   SHELL=/bin/bash
   MAILTO=""
   PATH=/usr/local/bin:/usr/bin:/bin
   15 3 * * 0 /path/to/repo/scripts/slurm/cron_submit_notebook_tests.sh >> $HOME/opi-notebook-tests/logs/cron.log 2>&1
   ```

If the site's SLURM provides **`scrontab`**, prefer it: the schedule then lives inside the
scheduler, survives submit-host reboots, and suppresses overlapping runs itself. Keep the
wrapper for the git refresh and call it from the scron job.

## Output layout

```
$OPI_NB_ROOT/summary/latest.json          <- THE summary, atomically overwritten each run
$OPI_NB_ROOT/runs/<RUN_ID>/summary.json   <- archived copy of the above
$OPI_NB_ROOT/runs/<RUN_ID>/junit.xml
$OPI_NB_ROOT/runs/<RUN_ID>/job.out|job.err
$OPI_NB_ROOT/runs/<RUN_ID>/artifacts/<notebook>/   <- retained for FAILED notebooks only
$OPI_NB_ROOT/logs/cron.log
$OPI_NB_ROOT/state/last_submission
```

## Reading the summary

Run-level `status` is `running`, `completed` or `aborted`. Per-notebook `status` is
`passed`, `failed`, `timeout`, `skipped` or `error`.

```bash
# everything that did not pass
jq -r '.notebooks[] | select(.status!="passed")
       | "\(.name)\t\(.status)\t\(.error_kind): \(.error_message)"' latest.json

# headline numbers
jq '{status, totals: .run.totals, commit: .run.git.commit, orca: .run.versions.orca}' latest.json

# slowest notebooks
jq -r '.notebooks | sort_by(-.duration_s)[:5][] | "\(.duration_s)s\t\(.name)"' latest.json
```

An `aborted` status means the job died before pytest finished (wall-clock limit, OOM,
`scancel`). The notebook entries present at that point are still valid, so the last one
listed is usually the one that hung.

## Preflight checks

Run these **on a compute node** (`srun -p <partition> --pty bash`) — egress and mounts
routinely differ from the login node.

1. **Network egress — make or break.** The notebooks `pip install` at runtime and fetch
   data mid-run:
   ```bash
   curl -sSfI https://pypi.org/simple/ https://files.pythonhosted.org https://github.com \
               https://raw.githubusercontent.com https://zenodo.org \
               https://pubchem.ncbi.nlm.nih.gov > /dev/null && echo OK
   ```
   Many sites firewall compute nodes entirely. If egress is impossible, set
   `NB_HTTPS_PROXY`, or run the job on a service node instead.
2. `git --version` and `uv --version` — both must exist on the *compute* node, not just
   the submit host.
3. `uv python find '>=3.11'`. The job does not set `UV_PYTHON_DOWNLOADS=never`, so uv may
   download an interpreter. If the site forbids that, export it and provide a system 3.11+.
4. ORCA: `"$NB_ORCA_DIR/orca" --version`, the license readable from the node, and
   `ldd "$NB_ORCA_DIR/orca" | grep 'not found'` empty.
5. **Run one small `ncores=4` ORCA job inside an allocation, invoking the binary directly —
   never through `srun` or `mpirun`.** ORCA spawns its own `mpirun`. Discover any needed
   `OMPI_MCA_*` settings in one interactive session and add them to the config, rather than
   after six weeks of red summaries.
6. Scratch and quota: `.venv` with torch + chemprop + rdkit plus the uv/torch caches is
   realistically 10-20 GB, and `redox`/`led`/`covaled_ethane` produce multi-GB ORCA scratch.
7. Cron can see `sbatch`: test with `NB_DRY_RUN=1`.

## Gotchas

- **`#SBATCH` directives cannot read `notebook_tests.env`.** They are parsed by `sbatch`
  before any shell runs. Partition, account, time, CPUs and memory are therefore passed on
  the `sbatch` command line by the wrapper, which overrides the in-file directives. The
  directives that remain in the job script are only fallbacks for a manual `sbatch`.
- **Never point `OPI_NB_REPO` at a working tree you care about.** 18 of the 19 notebooks
  run `pip install --upgrade` into the active environment. The dedicated checkout exists
  precisely so that blast radius is contained; `uv sync` prunes the additions each week.
- **A red run is not automatically an OPI bug.** The notebooks install unpinned third-party
  packages, so an upstream chemprop or numpy release can turn the suite red with no OPI
  commit involved. Compare the `run.versions` block and `error_kind` across runs before
  reaching for `git bisect`.
- **State resets between runs, not within one.** Notebook 3 upgrading numpy can still break
  notebook 11 in the same job; a cluster of `ImportError`/`AttributeError` failures after
  an upgrade is the signature.
- `--export=NONE` is deliberate. If you later add `module load` to the job script, note
  that no module state is inherited from the submit host.
- `chemeleon_orca` is the expensive outlier (installs torch, downloads a large checkpoint).
  It is the first candidate for `NB_SKIP` if runtime or egress becomes a problem.

## If one job does not fit the site's wall-clock limit

The suite runs serially in a single job on purpose: the notebooks `pip install` into a
shared venv, so parallel array tasks sharing one `.venv` would corrupt it, and the summary
has to end up as one file.

If a site's limit makes that impossible, submit `--array=0-18%4`, give each task its own
`UV_PROJECT_ENVIRONMENT` on node-local scratch, point `--notebook-summary` at
`$RUN_DIR/parts/$SLURM_ARRAY_TASK_ID.json`, and chain a merge job with
`sbatch --dependency=afterany:$ARRAY_JOB_ID` that concatenates the `notebooks` arrays,
recomputes `run.totals`, and atomically replaces `latest.json`.
