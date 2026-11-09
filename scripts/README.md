# Running the documentation notebooks

The notebooks in `docs/contents/notebooks/` are executed as a smoke test: the check is
that every cell of a notebook runs to the end without raising. Nothing is asserted about
the numbers that come out, and nothing the notebooks write is kept — each one runs in a
temporary directory that is removed afterwards.

They are **not** pytest tests. They need ORCA, the session's `uv sync` needs network
access, and a full sweep takes hours.

Two scripts do the work, and two nox sessions drive them:

| | |
|---|---|
| `scripts/run_notebook.py` | executes **one** notebook |
| `scripts/sweep_notebooks.py` | executes a list of them, one process each, and reports |
| `nox -s notebooks` | the above, with the notebooks you name, or else the whitelist |
| `nox -s all_notebooks` | the above, with every notebook, whitelisted or not |

Both sessions are non-default, so a bare `nox` never starts a notebook run.

The scripts find the notebooks through `scripts/notebooks`, a relative symlink to
`../docs/contents/notebooks`. If the notebooks move, repoint the link rather than
editing the scripts.

## Running them

Everything after `--` is passed on to `scripts/sweep_notebooks.py`:

```bash
uv run nox -s notebooks                    # the whitelist
uv run nox -s notebooks -- --list          # what would run, without running it
uv run nox -s notebooks -- how_to_opi      # one notebook, by name
uv run nox -s notebooks -- how_to_opi led  # several, in the order given
uv run nox -s notebooks -- 'extrapolate_*' # by glob, quoted so the shell keeps out
uv run nox -s all_notebooks                # every notebook, whitelisted or not
uv run nox -s all_notebooks -- --list      # ...and which ones that is
```

A name is the notebook's stem (`how_to_opi`, not `how_to_opi.ipynb`); a path works too.
A notebook named on the command line runs whether or not it is whitelisted, so the ones
left off the whitelist can still be tried by hand.

`all_notebooks` is `notebooks -- '*'` under a name of its own: it ignores the whitelist
and runs everything in `docs/contents/notebooks/`. The notebooks off the whitelist are off
it for a reason, so expect some of that run to fail; several also need packages the
`notebooks` group does not hold, and `PIP_NO_INDEX=0` (see below) gives them a chance.

The session installs OPI and the `notebooks` dependency group into `.nox/notebooks` and
runs the notebooks in it. The group holds `nbclient`, `nbformat`, `nbconvert` and
`ipykernel`; `pip`, which uv-created environments otherwise lack; and what the whitelisted
notebooks install for themselves (`matplotlib`, `numpy`, `pandas`, `py3dmol`, `seaborn`).

That environment is also where the notebooks put their own dependencies. Most of them
open with a cell along the lines of

```python
!{sys.executable} -m pip install --upgrade pandas py3Dmol matplotlib
```

and `sys.executable` is the kernel's interpreter, which is the one running the session --
so whatever those cells install lands in `.nox/notebooks/lib/python3.*/site-packages`,
next to the group above, and never in your own environment.

In practice they install nothing. `run_notebook.py` sets `PIP_NO_INDEX=1`, so `pip`
cannot reach PyPI, and finds everything the whitelisted notebooks ask for already
installed from the group, at the version in `uv.lock`. A sweep therefore tests exactly
what the lock file holds, whatever has been released since. To test a newer release,
upgrade it in the lock file (`uv lock --upgrade-package pandas`).

A notebook that needs a package the group does not have fails -- not at its `pip` cell,
since a failed `!` command does not raise, but at the import that follows. Add the package
to the group, or let that run reach PyPI:

```bash
PIP_NO_INDEX=0 uv run nox -s notebooks -- chemeleon_orca
```

Whatever such a run installs does not accumulate: the `uv sync` at the start of the next
session puts the locked versions back and removes whatever is not in the lock file.

## The whitelist

`WHITELIST` at the top of `scripts/sweep_notebooks.py` is the one place that decides what
a plain run (`nox -s notebooks`) works through. A notebook that cannot run unattended —
one that needs a GPU, a licence or more patience than a sweep has — is left off it.
`nox -s notebooks -- --list` prints what is on it. A whitelisted notebook that no longer
exists is an error, not a silent skip.

## Timeouts

A notebook gets 60 minutes of wall clock, and no single cell more than 45 minutes;
whichever comes first ends it. `sweep_notebooks.py` waits 120 s beyond the notebook's own
budget, then asks the runner to stop, gives it 30 s to clean up, and kills whatever is
left of it (a kernel, an ORCA).

```bash
uv run nox -s notebooks -- led --timeout 7200 --cell-timeout 3600
```

## Reading the result

Cells are printed as they run, and the run ends with one line per notebook:

```
========================================================================
  OK       how_to_opi     5.1 s
  FAILED   led           1m 03s
  KILLED   redox         1h 02m
------------------------------------------------------------------------
  3 notebooks: 1 ok, 1 failed, 1 killed -- 1h 03m total
```

`FAILED` means a cell raised (the traceback is above, and execution stopped there rather
than carrying on with broken state); `KILLED` means the notebook outlasted its budget and
the grace period on top. The exit status is 0 only if every notebook was `OK`, so the nox
session fails if any did not.

Notebooks run one at a time on purpose: several of them `pip install` into the environment
they are running in, and concurrent installs into one environment corrupt it.

## Without nox

The scripts are standalone — in an environment that has the `notebooks` group installed:

```bash
scripts/sweep_notebooks.py how_to_opi
scripts/run_notebook.py docs/contents/notebooks/how_to_opi.ipynb
scripts/run_notebook.py --help
```
