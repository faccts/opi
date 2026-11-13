# OPI conventions checklist

This checklist is split between two passes.

**§2–§7 are machine-verified.** Run `.venv/bin/nox -t pr_check --no-stop-on-first-error` and
report what it printed. Those sections exist to help you *interpret* rule codes and to cover the
paths each tool cannot see — never to predict output. A rule code you did not read in real nox
output may not be reported as a CI failure.

**§1 and §8 are the reading pass** — the CHANGELOG, docstring accuracy, prose docs, and naming.
No `pr_check` session looks at any of it.

CI runs `uv run nox -t pr_check` (see `.github/workflows/pr_checks.yml`) on Python 3.11/3.12/3.13.
The tag selects **six** sessions: `type_check` (mypy), `check_sort_imports`, `lint`,
`check_format_code` (all ruff), `spell_check` (codespell), `dead_code` (vulture).
`check_unused_imports` is declared `default=False` and is therefore **skipped** by `-t pr_check`;
F401 is still covered by `lint`. Config lives in `pyproject.toml` under `[tool.mypy]`,
`[tool.ruff]`, `[tool.codespell]`, `[tool.vulture]`.

Never run `-t fix`, `-t style`, `-t static_check`, or the `format_code` / `sort_imports` /
`remove_unused_imports` sessions: they rewrite files in place and would edit the diff under review.

---

## 1. Documentation

### 1.1 CHANGELOG.md — the most commonly missed item

Every user-visible change needs a bullet under `## [Unreleased] - ReleaseDate`. Check:

- **Present at all.** New public class/method/argument, changed behaviour, changed return type,
  new exception, removed API → there must be an entry. Purely internal refactors that no user can
  observe do not need one; say so rather than demanding a bullet.
- **Correct section.** `### Added` / `### Changed` / `### Deprecated` / `### Removed` / `### Fixed`.
  The sections exist even when empty — do not add new ones or reorder them. A behaviour change
  dressed up as `### Added` is a finding.
- **Issue/PR number.** Every bullet ends with `(#NNN)` — e.g. `(#276)`. A bullet with no number,
  or a number that disagrees with the branch/PR being reviewed, is a finding. Recent entries
  place the number at the end of the sentence, with or without a trailing period; match the
  surrounding bullets rather than inventing a third variant.
- **Identifiers in backticks.** `` `Input.get_blocks()` ``, `` `BlockScf` ``, `` `ncores` `` —
  not bare words. Method names carry `()`.
- **Written for users, not for the diff.** "Added `Fcidump.from_arrays()` for constructing a
  `Fcidump` from numpy arrays" — states what a user can now do. "Refactored the block loop" is
  not a changelog entry.
- **Breaking changes** belong under a `### Breaking Changes` heading (see the `[2.0.0]` section
  for the format), and must spell out what existing code has to change.
- **Mechanical slips:** unbalanced backticks (there is already a `` Add `functions to clean up ``
  in the file — do not add another), trailing whitespace at end of bullet, duplicate entry for a
  change already listed, entry added under a released version instead of `[Unreleased]`.

### 1.2 Docstrings — numpydoc

Rendered by Sphinx AutoAPI + Napoleon, so malformed sections silently produce broken API docs.
Style is [numpydoc](https://numpydoc.readthedocs.io/en/latest/format.html).

- **Present** on every public module, class, and method/function. Private helpers (`_name`) should
  have one when non-obvious.
- **Sections spelled and underlined exactly:** `Parameters`, `Returns`, `Raises`, `Attributes`,
  `Examples` — each followed by a line of dashes of matching length. A missing or short underline
  breaks the render.
- **`Parameters` matches the signature**: same names, same order, none missing, none left over
  after a rename. This is the single most common docstring defect in a refactor — when an argument
  is renamed, the docstring is usually forgotten.
- **Types given** in numpydoc form: `name : type`, e.g. `**data : Any`, `block : BlockABC | str`.
  Use modern syntax (`X | None`, `list[str]`), never `Optional[X]` / `List[x]`.
- **`Returns`** present whenever the function returns something; describe what, not just the type.
- **`Raises`** lists the exceptions actually raised in the body — and only those. A new `raise`
  added without a matching `Raises` entry is a finding; a `Raises` entry for an exception that was
  removed is equally one.
- **`Attributes`** on classes documents the pydantic fields including the private ones the class
  relies on (see `BlockABC` for the house style, which documents `_name`, `_arbitrary`, `_registry`).
- **Error messages and docstrings agree** with the actual behaviour after the change.

### 1.3 In-code comments

- The house style is the **`# >` prefix** — ~390 uses in `src/opi` versus a handful of plain `#`.
  New explanatory comments should use `# >`. Flag plain `#` comments added in the diff.
- Banner/section comments use the `# ////` and `# %%%%` box styles (`noxfile.py`,
  `pyproject.toml`, `src/opi/core.py`). Match the surrounding file; do not introduce a new style.
- Comments explain **why**, not what. A comment restating the line below it is a nit.
- No commented-out code, no `TODO`/`FIXME`/`XXX` left in a diff meant for merge, no leftover
  debugging comments.

### 1.4 `__all__` and public surface

Modules in `src/opi` declare `__all__` (e.g. `__all__ = ["BlockABC"]`). A new public class or
function added to such a module must be added to its `__all__`, and a renamed one updated — this
is what makes it importable from the package and visible to AutoAPI. Also check the package
`__init__.py` re-exports if the module's siblings are re-exported there.

### 1.5 Prose docs

- `docs/contents/*.md` — update if the change contradicts something written there
  (`dev_guide.md` describes tooling and style; `install.md`, `how_to_contribute.md`).
- `README.md` — only if it shows the changed API.
- `examples/` — new example directories follow the existing `exmpNNN_<name>/job.py` naming;
  examples are covered by ruff (`[tool.ruff] include`), so they must be formatted too.
- Docstring/markdown code samples must reflect the post-change API. A sample that would now raise
  is a finding.

---

## 2. Formatting — `ruff format` (`check_format_code`)

Black-compatible, `line-length = 100`, applied to `src/**/*.py`, `tests/**/*.py`,
`examples/**/*.py`, `pyproject.toml`. **Machine-verified** — `check_format_code` reports the hits.
Use the list below to explain what the formatter wants, not to predict it:

- **Lines over 100 characters** — count them; this is the most frequent real hit. Long string
  literals and long `raise ... (` messages are the usual culprits.
- **Quotes**: double quotes everywhere (formatter normalizes `'x'` → `"x"`).
- **Magic trailing comma**: a trailing comma in a collection/call forces one element per line;
  its absence lets the formatter join them. Mixed hand-wrapping that the formatter would undo
  (e.g. an argument list split across lines that fits in 100 cols with no trailing comma) is a hit.
- **Blank lines**: two between top-level definitions, one between methods, none at the start of a
  block, exactly one at end of file.
- **Whitespace**: no trailing whitespace, 4-space indent (never tabs), single space around binary
  operators, no alignment padding, no space before `:` or `,`.
- **Line breaks around operators**, implicit string concatenation, and parenthesized returns —
  match how the rest of the file reads.
- `E203` is explicitly ignored (`[tool.ruff.lint] ignore`), so whitespace-before-colon in slices
  is not a finding.

## 3. Lint — `ruff check` (`lint`)

Default rule set (`E4`, `E7`, `E9`, `F`), `E203` ignored. **Machine-verified** — `lint` reports
these. Note `E501` (line too long) is **not** in the default set, so an over-long comment or
string fails nothing. Common codes and what they mean:

- `F401` unused import. Caught here by `lint`, **not** by `check_unused_imports` — that session is
  skipped by `-t pr_check`.
- `F841` local variable assigned but never used.
- `F811` redefinition of an unused name (a duplicated method in a class is the classic).
- `F403`/`F405` star imports.
- `F821` undefined name (typo'd identifier, name used before definition).
- `F541` f-string with no placeholders.
- `E711`/`E712` `== None` / `== True` instead of `is None` / `if x`.
- `E721` `type(a) == type(b)` instead of `isinstance` — note `type(self) is X` is fine.
- `E722` bare `except:`.
- `E731` lambda assigned to a name.
- `E741` ambiguous names `l`, `O`, `I`.

## 4. Imports — `ruff check --select I` (`check_sort_imports`)

**Machine-verified** — `check_sort_imports` reports the hits as `I001`.

isort ordering: `__future__`, stdlib, third-party, first-party (`opi`), local — separated by one
blank line, alphabetized within each group, `import x` before `from x import y`. A new import
dropped at the end of a block, or into the wrong group (`opi` under third-party), is a finding.
The repo annotates groups with `# >` comments in some files (`noxfile.py`); match locally.

## 5. Spelling — `codespell` (`spell_check`)

**Partly machine-verified.** `spell_check` runs codespell over `src/opi` only, so nothing else in
the diff is covered — review prose everywhere: CHANGELOG, docs, tests, comments, docstrings,
error messages, and identifier names.

Two limits to respect. Codespell's dictionary is narrow: a green `spell_check` does **not** mean
`src/opi` is typo-free, so reading it is still worthwhile — but report anything codespell did not
print as *should fix*, never as a CI failure. And check that the misspelling is really on the
line before reporting it: quote the word from the file.

- **British vs American spelling is not a finding.** `initialise`/`initialize`,
  `behaviour`/`behavior`, `colour`/`color` — both are correct; never report either. The same goes
  for other trivial prose slips with no reader consequence: a comma, capitalisation, a minor
  grammar wobble in a comment. Report a typo only when it is an actual misspelling.
- Typos in **error messages** and **docstrings** are the ones users actually see — weight them
  higher than a typo in a comment.
- **Misspelled identifiers** are worse than misspelled prose: they are load-bearing and expensive
  to fix later. `recieve_blocks`, `seperator`, `arbitary` in a public name is a blocker.
- Real domain terms that codespell would false-positive on belong in `.codespellignore`
  (one term per line, trailing newline). Current entries: `XTB`, `Te`, `Nd`, `hav`, `TE`, `ND`,
  `ABD`, `ist`. If the diff adds a chemistry/ORCA term codespell would reject (e.g. an element
  symbol or ORCA keyword that collides with an English typo), flag that `.codespellignore` needs
  the term — and conversely, flag an addition to `.codespellignore` that is just papering over a
  genuine typo.
- Grammar in user-facing prose (changelog, docstrings) is worth a line only when it misleads or
  reads as broken, not when it is merely unpolished.

## 6. Typing — `mypy --strict` (`type_check`)

`[tool.mypy] strict = true`, `files = "src/"`, with the pydantic plugin. **Machine-verified** —
`type_check` reports the hits with their error codes. What it enforces:

- **Any missing annotation** — strict mode requires every parameter and every return annotated,
  including `-> None` on `__init__` and on functions that return nothing.
- `**kwargs: Any` / `*args: Any` must still be annotated.
- **Modern syntax only** (Python ≥ 3.11): `list[str]`, `dict[str, int]`, `X | None`,
  `type[Block]`. Not `List`, `Dict`, `Optional`, `Union` — the changelog records this migration
  (`Updated deprecated typing types to be compliant with Python >=3.11 guidelines (#216)`), so a
  reintroduction is a regression.
- **No implicit Optional**: a parameter defaulting to `None` must be typed `X | None`.
- `Any` used where a real type is known; a new `# type: ignore` without a narrow error code and a
  `# >` comment explaining it.
- `ClassVar[...]` on class-level mutable state (see `BlockABC._registry`).
- Forward references quoted (`type["BlockABC"]`) where needed.
- Note: mypy covers `src/` only. Missing annotations in `tests/` are not CI failures — mention
  them as nits at most.

## 7. Dead code — `vulture` (`dead_code`)

`paths = ["src/"]`, `min_confidence = 70`, `ignore_names = ["RdkitMol"]`. **Machine-verified** —
`dead_code` reports the hits with a confidence percentage.

- A newly added function, method, class, attribute, or import in `src/` that nothing references.
- Code left behind by the change: the old helper that the new implementation replaced, an
  attribute no longer read, a branch made unreachable by an earlier `return`/`raise`.
- Legitimately unused-but-required names (pydantic validators, protocol methods, public API not
  yet called internally) belong in `ignore_names` — or should just be flagged as intentional.

## 8. Naming — clarity and consistency

PEP 8 baseline: `snake_case` for functions/variables/arguments/modules, `PascalCase` for classes,
`UPPER_CASE` for constants, single leading `_` for private. Files are `snake_case.py`
(`docs/contents/dev_guide.md` § File Names). Beyond that, judge for **confusion**:

- **Ambiguity between related names.** The strongest check in this skill. When a diff introduces
  a name that sits next to an existing one, ask whether a reader could tell them apart at a
  glance: `Block` vs `BlockABC` vs `ORCABlock`; `block` vs `blocks` vs `block_name` vs `name`.
  If two names in the same module could plausibly be swapped by a reader without noticing, that
  is a finding — say which two and propose a disambiguating pair.
- **Name contradicts its type.** A plural name holding one object, a singular name holding a
  collection, `*_list` that is a dict, `get_*` that mutates, `is_*`/`has_*` that returns a
  non-boolean, a `*_name` parameter that also accepts a class.
- **Overloaded parameters.** A parameter accepting several unrelated types (`str | type | Block`)
  needs a name and a docstring that say so; a bare `block` that also takes a name string is
  exactly the kind of thing to flag.
- **Shadowed builtins**: `input`, `type`, `id`, `list`, `dict`, `format`, `next`, `object`,
  `str`. Note the codebase legitimately uses `input` as an *attribute* (`calc.input`) — that is
  established API, not a finding; a *local variable* named `input` is.
- **Single-letter and abbreviated names** outside tight loops and established math notation. This
  is a quantum-chemistry codebase: `mo`, `scf`, `mdci`, `s2`, `nprocs` are domain vocabulary and
  fine; `b`, `tmp`, `res`, `val`, `data2`, `flag` are not.
- **Consistency with the codebase.** The same concept must carry the same name everywhere. If the
  repo says `ncores`, a new `n_cores` is a finding; if it says `basename`, do not add `base_name`.
  Grep for the existing spelling before flagging — and cite where the established name lives.
- **Docstring name ≠ signature name** after a rename (also § 1.2).
- **Boolean parameters** read as predicates (`strict`, `create_missing`, `aftercoord` are the
  house style) and default to the conservative value.
- **Negated names** (`not_disabled`, `skip_no_check`) that force double-negative reasoning.
- **Test names** describe the behaviour asserted (`test_<unit>_<condition>_<expectation>`), not
  `test_1`, `test_new`, `test_it_works`.

---

## Severity

- **Blocker** — a session in your `nox -t pr_check` output actually failed, and the hit falls in
  a file and line region this diff touched. Quote the rule code. Nothing else in §2–§7 is a
  blocker, however confident you feel about it. Two reading-pass items also count: a missing
  CHANGELOG entry for a user-visible change, and a misspelled or genuinely confusing **public**
  name — both are expensive to fix after release.
- **Pre-existing** — a real nox failure somewhere the diff does not touch. Collapse to a count;
  it is not this diff's problem.
- **Should fix** — reviewers will ask for it: docstring/signature mismatch, missing `Raises`,
  off-convention changelog wording, `__all__` not updated, an internal name that reads ambiguously.
- **Nit** — style preference with no CI or reader consequence. Keep these few; a long nit list
  buries the blockers.
