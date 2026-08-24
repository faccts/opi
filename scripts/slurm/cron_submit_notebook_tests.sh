#!/usr/bin/env bash
#
# Weekly submitter for the OPI notebook test suite. Runs from cron on a SLURM submit host.
#
#   crontab entry (Sundays 03:15):
#     SHELL=/bin/bash
#     MAILTO=""
#     PATH=/usr/local/bin:/usr/bin:/bin
#     15 3 * * 0 /path/to/repo/scripts/slurm/cron_submit_notebook_tests.sh >> $HOME/opi-notebook-tests/logs/cron.log 2>&1
#
# Set NB_DRY_RUN=1 (or edit it in the config) to print the sbatch command instead of
# submitting -- that is how this script is tested on a machine without SLURM.

set -euo pipefail

CONFIG="${OPI_NB_CONFIG:-$(dirname "$(readlink -f "$0")")/notebook_tests.env}"
if [[ ! -f "$CONFIG" ]]; then
    echo "FATAL: no config at $CONFIG (copy notebook_tests.env.example and fill it in)" >&2
    exit 78
fi
# Remember an environment-supplied dry-run request: the config is sourced next and
# would otherwise silently overwrite it, turning `NB_DRY_RUN=1 ./this.sh` into a real
# submission.
_dry_run_override="${NB_DRY_RUN:-}"

# shellcheck source=notebook_tests.env.example
source "$CONFIG"

if [[ -n "$_dry_run_override" ]]; then
    NB_DRY_RUN="$_dry_run_override"
fi

# cron starts with a nearly empty environment, so never rely on an inherited PATH.
export PATH="${NB_PATH_PREPEND}:${PATH:-}"

log() { echo "[$(date -uIs)] $*"; }

mkdir -p "$OPI_NB_ROOT"/{logs,runs,summary,state,cache}

# Stops a manual invocation racing the cron one. The squeue check below is the layer
# that matters for the queue itself.
exec 9>"$OPI_NB_ROOT/state/cron.lock"
if ! flock -n 9; then
    log "another wrapper instance holds the lock; skipping"
    exit 0
fi

# A dry run only prints the sbatch command line, so it must not insist on SLURM being
# present -- that is precisely what makes this script testable off the submit host.
required_tools=(uv git)
[[ "${NB_DRY_RUN:-0}" == "1" ]] || required_tools+=(sbatch squeue)
for tool in "${required_tools[@]}"; do
    command -v "$tool" >/dev/null || { log "FATAL: '$tool' not on PATH (check NB_PATH_PREPEND)"; exit 78; }
done

# ---------------------------------------------------------------------------
# Overlap prevention. A job still PENDING behind a busy partition after six days
# must not get a sibling.
# ---------------------------------------------------------------------------
# `squeue -u` needs the account name; cron's environment may not carry $USER at all,
# and `set -u` would abort on the bare expansion.
if [[ "${NB_DRY_RUN:-0}" == "1" ]]; then
    log "DRY RUN: skipping the squeue overlap check"
else
    active="$(squeue -h -u "${USER:-$(id -un)}" -n "$NB_JOB_NAME" -o '%i %T' | tr '\n' ';')"
    if [[ -n "${active//[[:space:];]/}" ]]; then
        log "SKIP: previous '$NB_JOB_NAME' job(s) still active: $active"
        exit 0
    fi
fi

# ---------------------------------------------------------------------------
# Refresh the dedicated checkout. This is never a developer working tree: the
# notebooks pip-install into whatever environment they run in.
# ---------------------------------------------------------------------------
if [[ ! -d "$OPI_NB_REPO/.git" ]]; then
    log "cloning $OPI_NB_GIT_URL -> $OPI_NB_REPO"
    git clone "$OPI_NB_GIT_URL" "$OPI_NB_REPO"
fi

# Tags matter: the build backend is uv-dynamic-versioning, and a tagless tree
# silently reports version 0.0.0 in every summary.
git -C "$OPI_NB_REPO" fetch --quiet --tags --prune origin
git -C "$OPI_NB_REPO" checkout --quiet "$OPI_NB_BRANCH"
git -C "$OPI_NB_REPO" reset --hard --quiet "origin/$OPI_NB_BRANCH"
# Drop anything last week's notebooks left in the tree, but keep the (expensive) venv.
git -C "$OPI_NB_REPO" clean -qfdx -e .venv
commit="$(git -C "$OPI_NB_REPO" rev-parse --short HEAD)"

RUN_ID="$(date -u +%Y%m%dT%H%M%SZ)"
RUN_DIR="$OPI_NB_ROOT/runs/$RUN_ID"
mkdir -p "$RUN_DIR"

sbatch_args=(
    --parsable
    --job-name="$NB_JOB_NAME"
    --partition="$NB_PARTITION"
    --time="$NB_TIME"
    --cpus-per-task="$NB_CPUS"
    --mem="$NB_MEM"
    --output="$RUN_DIR/job.out"
    --error="$RUN_DIR/job.err"
    # The job sources $CONFIG itself, so it needs nothing from cron's environment.
    --export=NONE
)
[[ -n "$NB_ACCOUNT" ]] && sbatch_args+=(--account="$NB_ACCOUNT")
[[ -n "$NB_QOS" ]] && sbatch_args+=(--qos="$NB_QOS")
[[ -n "$NB_MAIL" ]] && sbatch_args+=(--mail-user="$NB_MAIL" --mail-type=FAIL,TIME_LIMIT)
# shellcheck disable=SC2206
[[ -n "$NB_EXTRA_SBATCH_ARGS" ]] && sbatch_args+=($NB_EXTRA_SBATCH_ARGS)

cmd=(sbatch "${sbatch_args[@]}" "$OPI_NB_REPO/scripts/slurm/run_notebook_tests.sbatch" "$CONFIG" "$RUN_DIR")

if [[ "${NB_DRY_RUN:-0}" == "1" ]]; then
    log "DRY RUN: ${cmd[*]}"
    exit 0
fi

jobid="$("${cmd[@]}")"
log "submitted job $jobid  run=$RUN_ID  commit=$commit  branch=$OPI_NB_BRANCH"
echo "$jobid $RUN_ID $commit" > "$OPI_NB_ROOT/state/last_submission"

# Retention: keep the most recent NB_KEEP_RUNS run directories.
find "$OPI_NB_ROOT/runs" -mindepth 1 -maxdepth 1 -type d -print0 \
    | sort -z \
    | head -z -n "-${NB_KEEP_RUNS:-12}" \
    | xargs -0 -r rm -rf
