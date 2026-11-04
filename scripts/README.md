# Running the documentation notebooks

The notebooks in `docs/contents/notebooks/` are executed as a smoke test: the check is
that every cell of a notebook runs to the end without raising. Nothing is asserted about
the numbers that come out, and nothing the notebooks write is kept — each one runs in a
temporary directory that is removed afterwards.

They are **not** pytest tests. They need ORCA, they need network access (most of them
`pip install` their own extras at runtime), and a full sweep takes hours.

Two scripts do the work, and two nox sessions drive them:

| | |
|---|---|
| `scripts/run_notebook.py` | executes **one** notebook |
| `scripts/run_notebooks.py` | executes a list of them, one process each, and reports |
| `nox -s notebooks` | the above, with the notebooks you name |
| `nox -s all_notebooks` | the full whitelisted sweep, no arguments |

Both sessions are non-default, so a bare `nox` never starts a notebook run.

The scripts find the notebooks through `scripts/notebooks`, a relative symlink to
`../docs/contents/notebooks`. If the notebooks move, repoint the link rather than
editing the scripts.

## Running them

Everything after `--` is passed on to `scripts/run_notebooks.py`:

```bash
uv run nox -s notebooks -- --list          # what would run, without running it
uv run nox -s notebooks -- how_to_opi      # one notebook, by name
uv run nox -s notebooks -- how_to_opi led  # several, in the order given
uv run nox -s notebooks -- 'extrapolate_*' # by glob, quoted so the shell keeps out
uv run nox -s notebooks -- '*'             # every notebook in the directory
uv run nox -s notebooks                    # the whitelist (same as all_notebooks)
uv run nox -s all_notebooks                # the whitelist; takes no arguments
```

A name is the notebook's stem (`how_to_opi`, not `how_to_opi.ipynb`); a path works too.
A notebook named on the command line runs whether or not it is whitelisted, so the ones
left off the whitelist can still be tried by hand.

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
next to the group above, and never in your own environment. For the whitelisted notebooks
the group has it all installed already, but `--upgrade` still asks PyPI and pulls a
release newer than `uv.lock` if there is one: nothing keeps `pip` offline. None of it
accumulates: the `uv sync` at the start of the next session puts the locked versions back
and removes whatever is not in the lock file, so each run starts from the same place.

## The whitelist

`WHITELIST` at the top of `scripts/run_notebooks.py` is the one place that decides what
"all of them" means. A notebook that cannot run unattended — one that needs a GPU, a
licence or more patience than a sweep has — is left off it. `nox -s notebooks -- --list`
prints what is on it. A whitelisted notebook that no longer exists is an error, not a
silent skip.

## Timeouts

A notebook gets 60 minutes of wall clock, and no single cell more than 45 minutes;
whichever comes first ends it. `run_notebooks.py` waits 120 s beyond the notebook's own
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
scripts/run_notebooks.py how_to_opi
scripts/run_notebook.py docs/contents/notebooks/how_to_opi.ipynb
scripts/run_notebook.py --help
```
