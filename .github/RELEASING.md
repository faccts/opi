# Releasing OPI

Releases are built and uploaded by the GitHub Actions workflow
[`.github/workflows/release.yml`](workflows/release.yml). It runs only when started by
hand: on GitHub, *Actions* → *Release* → *Run workflow*, or `gh workflow run release.yml`.
Pushing a tag does not start it.

When starting it, choose where it runs (*Use workflow from*: a branch or a tag) and a target:

| Target       | What happens                                                     | Allowed on      |
|--------------|------------------------------------------------------------------|-----------------|
| `build-only` | build and verify, upload nothing                                 | branch or tag   |
| `testpypi`   | additionally upload to TestPyPI and verify the upload            | branch or tag   |
| `pypi`       | build → TestPyPI → verify → upload the *same* files to PyPI       | `v*` tag only   |

On a `v*` tag the built version must match the tag (`v3.0.0-alpha.1` → `3.0.0a1`); otherwise
the run stops before uploading anything. On a branch the build gets a unique dev version
(e.g. `3.0.0a1.post64.dev17`), so rehearsals never take a real version number.

The steps of a run:

1. **Build and verify**: builds sdist and wheel once, checks the version, runs `twine check`,
   and installs and imports the wheel.
2. **TestPyPI**: uploads these files to [TestPyPI](https://test.pypi.org/project/orca-pi/).
3. **Verify TestPyPI**: checks that TestPyPI holds exactly the built files (SHA-256) and that
   `orca-pi` installs from there.
4. **PyPI**: uploads the same files to [PyPI](https://pypi.org/project/orca-pi/).

The workflow only runs on GitHub (`faccts/opi`), never on a Forgejo mirror.

## Release steps

1. Rehearse (optional, recommended): run the workflow on `main` with target `testpypi`.
2. Prepare the release in a PR: in `CHANGELOG.md`, turn `## [Unreleased] - ReleaseDate` into
   `## [X.Y.Z] - YYYY-MM-DD` and add a new empty `Unreleased` section. Merge it.
3. Tag the merge commit on `main` and push the tag to GitHub:

   ```bash
   git switch main && git pull
   git tag -a vX.Y.Z -m "OPI X.Y.Z"
   git push origin vX.Y.Z
   ```

   Tags follow the existing scheme, e.g. `v3.0.0` or `v3.0.0-alpha.1`.
4. Run the workflow on the tag `vX.Y.Z` with target `pypi`:

   ```bash
   gh workflow run release.yml --ref vX.Y.Z -f target=pypi
   ```

   To look at TestPyPI before anything goes to PyPI, first run it on the tag with target
   `testpypi`, then again with target `pypi`; the second run builds identical files (the
   build tools are pinned in `.github/build-constraints.txt`), finds them on TestPyPI and
   continues. Do this only right before the release: once `testpypi` ran on the tag, that
   version number is used up on TestPyPI (see below). Rehearse on `main` instead.
5. Optionally create a GitHub release for the tag with the changelog section.
6. conda-forge: the autotick bot opens a PR on `conda-forge/orca-pi-feedstock` a few hours
   later. Check that the recipe's dependencies still match `pyproject.toml` before merging.

A version number can be uploaded to PyPI only once, even after deleting it. If a broken
release slips through, yank it on PyPI and release a new patch version.

TestPyPI behaves the same way. Once files of a version are on TestPyPI, only that exact build
can go on to PyPI through this workflow. So a tag may only be moved as long as no `testpypi`
or `pypi` run on it got past the build job: if the version does not match the tag, the tag
points to the wrong commit; delete it (`git push origin :refs/tags/vX.Y.Z`,
`git tag -d vX.Y.Z`) and tag again, nothing has been uploaded at that point. If a bug turns
up after the TestPyPI upload, release under a new version number instead.

Do not change the pinned build tools between a `testpypi` and a `pypi` run of the same tag:
`.github/build-constraints.txt` and the uv `version:` in `release.yml` (uv also decides which
Python build compresses the files). Otherwise the rebuilt files differ from those on TestPyPI.
Update the pins in a normal PR between releases (`build-constraints.txt` explains how).

Wait until a run has finished before starting the next one on the same tag or branch. GitHub
keeps only one waiting run per tag or branch and cancels an older waiting one.

GitHub runs the `release.yml` contained in the selected tag or branch, so a tag must point to
a commit that already contains the workflow.

## One-time setup

Uploads use [trusted publishing](https://docs.pypi.org/trusted-publishers/), so no API tokens
are stored on GitHub.

- **GitHub environments** (*Settings* → *Environments*): an environment is a named gate that a
  job can be assigned to; PyPI can be told to accept uploads only from jobs in it.
  - `pypi`: restrict deployments to tags matching `v*`. Required reviewers are optional; if
    set, the run additionally waits for an approval before the PyPI upload.
  - `testpypi`: no restrictions needed.
- **PyPI** (needs an owner of `orca-pi`): *Manage project* → *Publishing* → add a GitHub
  publisher with owner `faccts`, repository `opi`, workflow `release.yml`, environment `pypi`.
- **TestPyPI**: the same on <https://test.pypi.org> with environment `testpypi`. If `orca-pi`
  does not exist there yet, add it as a *pending publisher* in the account settings; the first
  upload then creates the project.
- **Allowed actions** (*Settings* → *Actions* → *General*, or the organization settings): the
  workflow uses `astral-sh/setup-uv` and `pypa/gh-action-pypi-publish` next to GitHub's own
  actions; both must be allowed.
