---
name: opi-review
description: Cursory convention review of implemented changes in the OPI repo. Runs the read-only `nox -t pr_check` sessions (mypy, ruff, codespell, vulture) and reports their catches in plain language, then reads the diff for what those tools cannot check — CHANGELOG entries, numpydoc docstrings that match their signatures, docstring examples, docs/, and ambiguous naming. Use when asked to review, sanity-check, or pre-flight a diff, branch, or PR before pushing. `--recheck` re-verifies the findings of an earlier review instead of reviewing afresh. Never edits files and does NOT hunt for logic bugs.
---

# opi-review

A **convention reviewer** for changes in this repository. Two passes, in this order:

1. **Machine pass** — run `nox -t pr_check` and report what it caught. This is ground truth for
   formatting, lint, import order, typing, spelling in `src/opi`, and dead code.
2. **Reading pass** — review what no checker looks at: the CHANGELOG, docstring accuracy, prose
   docs, and naming.

With `--recheck` the same two passes run, but the output is a verdict on the findings of an
earlier review rather than a fresh review — see [Recheck mode](#recheck-mode---recheck).

## Hard boundaries

These are not preferences — they define the skill:

1. **Run only read-only checkers.** `nox -t pr_check` and read-only git plumbing (`git diff`,
   `git show`, `git log`, `git status`, `git merge-base`, `git ls-files`) are permitted. Nothing
   else — no `pytest`, no test sessions, no ad-hoc `python`, no installs, no `pip`/`uv` commands
   of your own.
2. **Never modify the working tree.** Report findings; do not fix them. This makes three nox tags
   and three sessions forbidden, because they **rewrite files in place**:

   | Never run | Why |
   |---|---|
   | `-t fix`, `-t style`, `-t static_check` | each includes at least one rewriting session |
   | `format_code`, `sort_imports`, `remove_unused_imports` | `ruff --fix` / reformat — they edit the diff under review |

   `-t pr_check` contains only `check_*`-style read-only sessions. It is the only tag you may use.
3. **Never predict a checker's output — run it and quote it.** If you did not see a rule code in
   real nox output, you may not claim a session will fail. Nothing turns "this import looks
   unused" into a blocker except `lint` actually printing `F401`. Reading-based findings go in
   the reading section, phrased as judgement, never as CI failure.
4. **Every finding quotes the file.** Before reporting, re-read the exact line and quote it. A
   finding you cannot quote is not a finding — delete it.
5. **Do not review logic, and do not report it either.** Correctness bugs, algorithmic problems,
   edge cases, performance, API design, test coverage — all out of scope, and out of scope means
   **absent from the report**. Do not investigate them, do not mention them in passing, do not add
   an aside, a footnote, a caveat, or a section for them. Noticing one is not a reason to write it
   down: drop it. The report contains convention findings and nothing else. If the user wants
   logic reviewed, that is `/code-review`, and one sentence pointing there — with no hint of what
   you saw — is the most you may say.
6. **Cursory, not exhaustive.** One pass. Do not go spelunking through the rest of the codebase —
   except the one lookup that *is* required: grepping for an established spelling before calling
   a new name inconsistent.

If the user wants logic review, point them at `/code-review`. If they want tests run, that is a
separate request — `pr_check` deliberately excludes them.

## Scope resolution

Work out what to review, in this order:


| Invocation | Scope |
|---|---|
| `/opi-review` (no args) | Uncommitted changes **plus** commits on the current branch not on `main` |
| `/opi-review --staged` | `git diff --cached` |
| `/opi-review --uncommitted` | `git diff HEAD` |
| `/opi-review <ref>` | `git diff <ref>...HEAD` |
| `/opi-review <path>...` | Restrict any of the above to those paths |
| `/opi-review --recheck [args]` | Re-resolve scope as above, but report only on an earlier review's findings — see [Recheck mode](#recheck-mode---recheck) |

Default scope:

```bash
git merge-base --fork-point main HEAD || git merge-base main HEAD   # base
git diff --stat <base>          # what changed — the file list, and nothing more
```


Resolve the scope **before** running nox — you need the changed-file list to attribute nox
findings (below). If `--stat` comes back empty, stop and say so rather than reviewing thin air;
the changes may have been committed since the user last looked.

**Do not run the full `git diff` yourself.** `--stat` is all you need to attribute nox findings
and to hand the scope over. The diff itself runs to tens of thousands of tokens on a real branch,
and the reviewing subagent fetches it from the base ref you give it — reading it in both contexts
doubles the cost of the review and adds no coverage. The only exception is
[reviewing inline](#running-the-review) instead of delegating.

The reviewing agent reads the diff with **wide context**, not the changed files in full:

```bash
git diff -U20 <base>                 # the changes, with enough context to judge them
git diff -U20 <base> -- src/         # narrow to this first when the diff is large
```

Twenty lines of context carries the enclosing docstring, the neighbouring names, and the nearby
`__all__` — which is what makes naming and docstring conventions judgeable. Reading every changed
file in full costs about twice as much and adds nothing the reading pass uses. Two carve-outs:

- **Prose in full.** `CHANGELOG.md`, `docs/contents/*.md`, `README.md` — small files, and no
  checker reads them at all, so read the whole thing rather than a hunk.
- **One source file at a time, on cause.** When a finding needs what the context window does not
  show — a signature that sits further up the file, say — open that one file and say why.

[//]: # ()
[//]: # (If the diff touches more than ~15 files, say so and review the most substantial ones, listing)

[//]: # (what you skipped.)

Always check whether `CHANGELOG.md` is in the changed-file list; its absence is itself a finding.

## The machine pass — running nox

```bash
.venv/bin/nox -t pr_check --no-stop-on-first-error
```

Three things about that command, each of which silently ruins the review if you skip it:

- **`--no-stop-on-first-error` is mandatory.** The noxfile sets
  `nox.options.stop_on_first_error = True`, so the default run aborts at the first failing
  session and you never see the other five. A review that reports one category because the rest
  never ran is worse than no review.
- **Do not pipe it through `head`/`tail`.** You get the pager's exit status, not nox's, and a
  clean-looking `exit 0` from a failing run will mislead you. If the output is long, redirect it
  to a file (`> $CLAUDE_JOB_DIR/tmp/nox.txt 2>&1`) and read the file.
- **Use `.venv/bin/nox`.** There is no system nox. First run may take minutes while `uv` builds
  the six session venvs; afterwards `.nox/` is reused and the whole thing takes about a second.
  Allow a generous timeout.

Skip the machine pass only when the diff touches no file any checker sees (see the coverage
table) — a CHANGELOG-only diff, for example. Say that you skipped it and why.

### What `-t pr_check` actually runs

Six sessions. Each has a **different scope**, which is what makes the reading pass necessary:

| Session | Tool | Paths it sees |
|---|---|---|
| `type_check` | `mypy --strict` (pydantic plugin) | `src/` |
| `check_sort_imports` | `ruff check --select I` | `pyproject.toml`, `src/`, `tests/`, `examples/` |
| `lint` | `ruff check` — default `E4,E7,E9,F`, `E203` ignored | same as above |
| `check_format_code` | `ruff format --check`, `line-length = 100` | same as above |
| `spell_check` | `codespell` | `src/opi` only |
| `dead_code` | `vulture`, `min_confidence = 70` | `src/` |

Two quirks worth knowing:

- **`check_unused_imports` is declared `default=False`, so `-t pr_check` skips it** — nox reports
  "Ran 6 sessions". Unused imports are still caught, by `lint` (F401 is part of `F`). Attribute
  an unused-import hit to `lint`, not to `check_unused_imports`.
- **`E501` (line too long) is not enabled.** The 100-column limit is enforced by
  `check_format_code`, and `ruff format` does not rewrap comments or string literals — so an
  over-long comment fails nothing. It is a nit, not a blocker.

### Nothing checks these

No `pr_check` session reads `CHANGELOG.md`, `docs/**`, `README.md`, or any `.md` prose.
`tests/` gets ruff but **no mypy and no codespell**. Docstring *examples* are never executed by
any session, so a sample that would now raise is invisible to CI. This is where the reading pass
earns its keep, and why a green nox run alone is not a clean review — do the reading pass before
calling it clean.

### Attributing nox findings

`pr_check` runs over the whole repository, not over the diff. So every nox finding is one of:

- **In the diff** — the file *and* line region appear in the diff you resolved. These fail CI
  because of this change: report each one individually.
- **Pre-existing** — anywhere else in the repo. Collapse these into a single count with a
  one-line note. Do not pad the review with them; they are not this diff's problem. Expand only
  if there are three or fewer, or if one sits in a file the diff touches.

If you cannot tell which, say so rather than guessing.

## Recheck mode (`--recheck`)

`--recheck` answers one question: **were the findings of the previous review addressed?** It is
not a fresh review. Same boundaries, same two passes, different output — a verdict per prior
finding.

### Which findings carry over

Only the **blockers, reading findings, and nits** of the previous report — everything under
*Will fail CI*, *From reading*, and *Nits*.

**Drop any logic observations the previous report carried.** Current reviews never produce them,
but an older report may have an *Out of scope, noticed anyway* section. Rechecking those would be
reviewing logic through the back door. Do not carry them over, do not verify them, do not list
them as unresolved, and do not mention that you dropped them — they are simply not part of the
recheck.

### Where the prior findings come from

In order:

1. The previous `opi-review` report **in this conversation** — the normal case.
2. A report the user pasted, or a file/PR-comment they point at.

If neither is available, **stop and ask** for the earlier report. Never silently fall back to a
full review — the user asked "did I fix these?", and a fresh review answers a different question.
Never reconstruct a prior finding from memory: a recheck against invented findings is worse than
no recheck.

### Method

Re-resolve the scope the same way (HEAD may have moved — the fixes were likely committed), then
run the same `nox -t pr_check` command. Nox output is the ground truth for the machine findings
and costs about a second on a warm `.nox/`.

Give each carried-over finding exactly one verdict, and **quote the current state of the file for
every one of them** — including the ones you call fixed. Boundary 4 applies unchanged: a verdict
you cannot quote is not a verdict.

| Verdict | Means | Evidence required |
|---|---|---|
| ✅ **Fixed** | the concern is gone | the rule code no longer appears in nox output, *or* the quoted line now reads correctly |
| ❌ **Open** | unchanged | the finding quoted from the current file, with its new line number |
| ⚠️ **Partial** | touched but not settled | what changed, and what still stands |
| ➖ **Moot** | the code it referred to is gone, or the file left the diff | the deletion, from `git diff` |
| ❓ **Unverifiable** | the old finding was too vague to check, or its file is unreadable | say which, and why |

Line numbers drift as fixes land — match findings by **content, not by line number**, and report
the current line number. A finding whose line number moved but whose text is unchanged is ❌ Open,
not ➖ Moot.

Two things `--recheck` does **not** do:

- **No new findings.** A convention problem you notice for the first time during a recheck is not
  reported — the user can run a plain `/opi-review` for that. The one exception: if a *fix itself*
  introduced a nox failure, note it in a single line under the affected finding, quoting the rule
  code. Cap that at what nox actually printed; do not go looking.
- **No re-litigating.** If a finding was addressed differently than suggested and the concern is
  genuinely gone, it is ✅ Fixed. Do not mark it open because you would have fixed it another way.

## Running the review

Delegate to a subagent so the review is a clean, isolated pass:

- `subagent_type: "opi-reviewer"` if that agent type is available, otherwise `"Explore"`.
- `run_in_background: false` — the user is waiting on this.
- In the prompt: the resolved base ref and the `--stat` file list — the agent fetches the diff
  itself, so never paste a diff into the prompt — the instruction to read
  `.claude/skills/opi-review/references/conventions.md` as the authoritative checklist, the hard
  boundaries above **verbatim** — especially the forbidden-session table and "never predict a
  checker's output" — the exact nox command, and the output format below.

For `--recheck`, the subagent gets the same prompt plus: the carried-over findings **verbatim,
one per line, numbered** (you hold the previous report, the agent does not), the instruction that
this is a recheck and not a fresh review, the verdict table, and the recheck output format. Strip
every logic observation — including an *Out of scope* section from an older report — before
handing the list over; do not make the agent decide what to drop.

Relay the agent's findings to the user in full; the agent's report is not shown to them. If the
agent reports a nox failure, relay the rule code and the quoted line, not a paraphrase.

For a diff of one or two small files, reviewing inline is fine: read it yourself with
`git diff -U20 <base>` and the boundaries apply identically.

## The checklist

The authoritative, OPI-specific convention catalogue lives in `references/conventions.md`.
**Read it before reporting anything.** With nox wired in, the two passes divide as follows:

**Machine-verified — report nox's output, do not re-derive it:** formatting, lint, import order,
unused imports, typing, spelling in `src/opi`, dead code.

**Reading pass — nox cannot see these:**

1. **CHANGELOG.md** — entry present, right section, `(#NNN)` issue number, identifiers in
   backticks, written for users. The most commonly missed item in this repo.
2. **Docstrings** — numpydoc sections spelled and underlined correctly, `Parameters` matching the
   signature after a rename, `Raises` matching the body, and **examples that still run** against
   the current signature.
3. **`__all__`** and the public surface.
4. **Prose docs** — `docs/contents/*.md`, `README.md`, new `examples/exmpNNN_<name>/`.
5. **`# >` comment house style.**
6. **Naming** — ambiguity between related names, names that contradict their type, shadowed
   builtins, consistency with the established spelling elsewhere in the repo.
7. **Spelling outside `src/opi`** — CHANGELOG, docs, tests, since codespell never reads them.
   Real misspellings only; British vs American variants are not findings.

## Output format

For `--recheck`, use the [recheck format](#recheck-output-format) instead of the one below.

Lead with the machine verdict — it answers "will CI pass?" without judgement. Then the reading
findings, clearly marked as judgement rather than CI failure.

```markdown
## opi-review — <base>..HEAD (<N> files)

### nox -t pr_check — ❌ 2 of 6 sessions failed
| session | verdict |
|---|---|
| `type_check` | ✅ |
| `check_sort_imports` | ❌ 1 |
| `lint` | ❌ 2 |
| `check_format_code` | ✅ |
| `spell_check` | ✅ |
| `dead_code` | ✅ |

**Will fail CI — from this diff**
- `src/opi/input/core.py:14` — **F401** `Optional` imported but unused → delete the import. `lint`
- `src/opi/input/core.py:12` — **I001** import block unsorted → `Any, ClassVar, Iterable`. `check_sort_imports`

**Pre-existing** — 3 further `lint` findings in files this diff does not touch; not caused by
this change.

### From reading — no nox session checks these
- `src/opi/input/core.py:628` — **docstring example**: `Block(d3s6=0.64)` would raise
  `TypeError`; `Block.__init__` requires `name`. Example is never executed by CI.
- `CHANGELOG.md` — **documentation**: `Input.get_blocks()` changed its return key, no
  `### Changed` entry.

### Nits
- `src/opi/input/core.py:636` — comment is 101 chars; nothing fails (`E501` off).
```

Render every nox finding as `path:line` — **rule code** — what is wrong → what to do, then the
session. The rule code and the quoted text come from real output; the "what to do" is yours.

The report has exactly these sections, and an empty section is left out, not written as "none".
**There is no section for logic observations** — if you find yourself opening one, or appending a
stray "worth noting" line about behaviour, delete it instead. There is no *Clean* line either: a
category with no finding is clean by omission, and listing clean categories is filler.

**When nothing is found**, the whole report is the heading plus one line:

```markdown
## opi-review — <base>..HEAD (<N> files)
✅ nox -t pr_check 6/6 passed; nothing to flag in CHANGELOG, docstrings, docs or naming.
```

No session table, no caveats, no summary of what was checked. The code is fine — say so and stop.

**Word budget.** Every word must carry a finding.

- One finding = one line (two if the quote is long), **≤ 30 words** plus the quote.
- The whole report stays **under ~200 words** outside quotes and the session table. More findings
  than that fits means the nits go first — cut them.
- Show the session table only when a session failed.
- No intros, no closing summary, no restating what the diff does (the user wrote it), no
  explanation of why a convention exists.

**Ignore small stuff.** British vs American spelling (`behaviour`/`behavior`,
`initialise`/`initialize`) is never a finding — both are correct. Nor are punctuation,
capitalisation, or unpolished-but-clear grammar in comments. If a nit would not change what a
reader understands or what CI does, drop it.

### Recheck output format

One line per prior finding, in the order the previous report listed them, each with its verdict
and the quoted current state. Lead with the tally so the answer to "am I done?" is the first thing
on screen.

```markdown
## opi-review --recheck — 5 prior findings: 3 fixed, 1 open, 1 partial

### nox -t pr_check — ✅ 6 of 6 sessions passed
(only the sessions that carried a prior finding need commenting on)

### Verdicts
1. ✅ **Fixed** — `src/opi/input/core.py` **F401** `Optional` unused → import removed; `lint`
   is clean on this file.
2. ❌ **Open** — `src/opi/input/core.py:631` (was :628) — docstring example still reads
   `Block(d3s6=0.64)`; `Block.__init__` still requires `name`.
3. ⚠️ **Partial** — `CHANGELOG.md:24` — entry added under `### Changed`, but no `(#NNN)` issue
   number: `- `Input.get_blocks()` now keys by block name`.
4. ➖ **Moot** — `src/opi/input/blocks/legacy.py` — file deleted in this diff.
5. ✅ **Fixed** — `src/opi/input/core.py:44` — `blk` renamed to `block`.
```

Say what is left, not what was done: if everything is ✅, that is the heading plus one line
(`✅ All N prior findings fixed; nox 6/6 passed.`) and no table. Each verdict ≤ 30 words plus
the quote. Do not
re-explain a finding the user has already read — the verdict plus the current quote is the whole
job.
