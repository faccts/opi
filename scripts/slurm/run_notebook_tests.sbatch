#!/usr/bin/env bash
#SBATCH --job-name=opi-notebooks
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=32G
#SBATCH --time=12:00:00
#
# Execute the OPI documentation notebooks and write a machine-readable summary.
#
#   Usage (normally via cron_submit_notebook_tests.sh):
#     sbatch [site flags] run_notebook_tests.sbatch <config.env> <run-dir>
#
# The #SBATCH directives above are only fallbacks for a manual submit: they are parsed
# by sbatch before any shell runs and therefore CANNOT read <config.env>. The wrapper
# passes partition/account/time/cpus/mem on the sbatch command line, which overrides them.
#
# Because #SBATCH lines are ordinary shell comments, this script also runs verbatim as
#     bash run_notebook_tests.sbatch <config.env> <run-dir>
# on a machine without SLURM. That is how it is tested.

set -euo pipefail

CONFIG="${1:?usage: run_notebook_tests.sbatch <config.env> <run-dir>}"
RUN_DIR="${2:?usage: run_notebook_tests.sbatch <config.env> <run-dir>}"

# shellcheck source=notebook_tests.env.example
source "$CONFIG"

export PATH="${NB_PATH_PREPEND}:${PATH:-}"

SCRIPT_DIR="$OPI_NB_REPO/scripts/slurm"
JOB_ID="${SLURM_JOB_ID:-local-$$}"
SUMMARY="$OPI_NB_ROOT/summary/latest.json"
ARTIFACTS="$RUN_DIR/artifacts"
mkdir -p "$OPI_NB_ROOT/summary" "$ARTIFACTS"

# ---------------------------------------------------------------------------
# Scratch. ORCA is I/O heavy, so its scratch must stay on node-local disk.
# ---------------------------------------------------------------------------
SCRATCH_BASE="${NB_SCRATCH_BASE:-${SLURM_TMPDIR:-/tmp}}"
export TMPDIR="$SCRATCH_BASE/opi-nb-$JOB_ID"
mkdir -p "$TMPDIR"
export TMP="$TMPDIR" TEMP="$TMPDIR"
export MPLCONFIGDIR="$TMPDIR/mpl" XDG_CACHE_HOME="$TMPDIR/xdg-cache"

# Caches that are expensive to rebuild live on shared storage instead: chemeleon_orca
# downloads a large checkpoint and chemprop drags in torch. Re-fetching those weekly
# is pure waste.
export UV_CACHE_DIR="$OPI_NB_ROOT/cache/uv"
export TORCH_HOME="$OPI_NB_ROOT/cache/torch"
export HF_HOME="$OPI_NB_ROOT/cache/hf"
mkdir -p "$MPLCONFIGDIR" "$XDG_CACHE_HOME" "$UV_CACHE_DIR" "$TORCH_HOME" "$HF_HOME"

cleanup() {
    rc=$?
    # No-op if pytest already wrote a real summary; otherwise flip "running" -> "aborted"
    # so latest.json can never silently keep showing last week's green result.
    python3 "$SCRIPT_DIR/summary_stub.py" --path "$SUMMARY" --status aborted \
        --job-id "$JOB_ID" --message "job exited rc=$rc before pytest wrote a summary" || true
    cp -f "$SUMMARY" "$RUN_DIR/summary.json" 2>/dev/null || true
    rm -rf "$TMPDIR"
    exit "$rc"
}
trap cleanup EXIT
# SLURM sends SIGTERM (then SIGKILL after KillWait) on `scancel` and at the wall-clock
# limit. Turning those into a normal `exit` guarantees the EXIT trap above runs, which is
# the only thing standing between a killed job and a stale-green latest.json.
trap 'exit 143' TERM
trap 'exit 130' INT

# ---------------------------------------------------------------------------
# ORCA and MPI. OPI reads OPI_ORCA (binary or its folder) and OPI_MPI (a PREFIX
# directory, to which it appends bin/ and lib/ itself, resolved strictly).
# ---------------------------------------------------------------------------
ORCA_BIN_DIR="$NB_ORCA_DIR${NB_ORCA_BIN_SUBDIR:+/$NB_ORCA_BIN_SUBDIR}"
export OPI_ORCA="$ORCA_BIN_DIR/orca"
export PATH="$ORCA_BIN_DIR:$PATH"
export LD_LIBRARY_PATH="$ORCA_BIN_DIR:${LD_LIBRARY_PATH:-}"

if [[ -n "${NB_MPI_PREFIX:-}" ]]; then
    export OPI_MPI="$NB_MPI_PREFIX"
    export PATH="$NB_MPI_PREFIX/bin:$PATH"
    export LD_LIBRARY_PATH="$NB_MPI_PREFIX/lib:$LD_LIBRARY_PATH"
fi

[[ -n "${NB_HTTPS_PROXY:-}" ]] && export https_proxy="$NB_HTTPS_PROXY"
[[ -n "${NB_HTTP_PROXY:-}" ]] && export http_proxy="$NB_HTTP_PROXY"

echo "== $(date -uIs) job=$JOB_ID host=$(hostname) tmpdir=$TMPDIR"
echo "== repo=$OPI_NB_REPO summary=$SUMMARY"

# Fail loudly and early rather than reporting 16 identical notebook failures.
# Note: do NOT probe with `orca --version` -- ORCA treats that as an input filename
# and exits 2. The authoritative check runs through OPI further down.
[[ -x "$OPI_ORCA" ]] || { echo "FATAL: no executable ORCA at $OPI_ORCA"; exit 78; }

# ---------------------------------------------------------------------------
# Python environment. `uv sync` is exact, so it also PRUNES whatever last week's
# notebooks pip-installed into this venv -- that is the weekly self-heal.
# ---------------------------------------------------------------------------
cd "$OPI_NB_REPO"
export UV_FROZEN=1
export UV_PROJECT_ENVIRONMENT="$OPI_NB_REPO/.venv"

uv sync --group tests --group notebooks

if [[ -n "${NB_EXTRA_PIP:-}" ]]; then
    # Deliberately outside uv.lock: keeps third-party VCS URLs out of the project lockfile.
    # shellcheck disable=SC2086
    uv pip install $NB_EXTRA_PIP
fi

# shellcheck disable=SC1091
source "$UV_PROJECT_ENVIRONMENT/bin/activate"
python -m jupyter nbconvert --version || { echo "FATAL: nbconvert missing"; exit 78; }
python -c "import pip" || { echo "FATAL: pip missing; notebooks cannot self-install"; exit 78; }

# Authoritative ORCA check: exercises the exact discovery path (OPI_ORCA/OPI_MPI) that
# the notebooks will use, rather than just poking the filesystem.
python - <<'PY' || { echo "FATAL: OPI cannot run ORCA on this node"; exit 78; }
import sys

from opi.execution.core import Runner

version = Runner().get_version()
if version is None:
    sys.exit(1)
print(f"== ORCA version: {version}")
PY

# ---------------------------------------------------------------------------
# Run.
# ---------------------------------------------------------------------------
python "$SCRIPT_DIR/summary_stub.py" --path "$SUMMARY" --status running --job-id "$JOB_ID"

export OPI_NOTEBOOKS_SKIP="$NB_SKIP"
export OPI_NOTEBOOK_CELL_TIMEOUT="$NB_CELL_TIMEOUT"
export OPI_NOTEBOOK_TIMEOUT="$NB_NOTEBOOK_TIMEOUT"

set +e
# shellcheck disable=SC2086
pytest -m notebooks -p no:randomly -ra -q \
    --basetemp="$TMPDIR/pytest" \
    --notebook-summary="$SUMMARY" \
    --notebook-artifacts-dir="$ARTIFACTS" \
    --junitxml="$RUN_DIR/junit.xml" \
    $NB_PYTEST_ARGS
rc=$?
set -e

echo "== $(date -uIs) pytest exited rc=$rc"
echo "== summary: $SUMMARY"
exit "$rc"
