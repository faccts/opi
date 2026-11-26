"""Check that a package index holds exactly the locally built files of an orca-pi release.

Used by .github/workflows/release.yml after uploading to TestPyPI and to PyPI. Waits a few
minutes for the release to show up, then compares the SHA-256 hashes of the files on the
index with those in the local dist directory. Exits non-zero on any mismatch.

Usage: python check_index_files.py {testpypi,pypi} VERSION DIST_DIR
"""

import argparse
import hashlib
import json
import pathlib
import sys
import time
import urllib.request

INDEXES = {"testpypi": "https://test.pypi.org", "pypi": "https://pypi.org"}
ATTEMPTS = 20
WAIT_SECONDS = 15


def fetch_remote_hashes(url: str, local: dict[str, str]) -> dict[str, str]:
    """Return {filename: sha256} of the release on the index, retrying until all are there."""
    remote: dict[str, str] = {}
    for attempt in range(1, ATTEMPTS + 1):
        try:
            with urllib.request.urlopen(url, timeout=30) as response:
                data = json.load(response)
        # > OSError covers HTTP errors (e.g. 404 before the release shows up), network errors
        # > and timeouts.
        except OSError as err:
            print(f"Attempt {attempt}: {err}")
        else:
            remote = {f["filename"]: f["digests"]["sha256"] for f in data["urls"]}
            if set(remote) >= set(local):
                return remote
            print(f"Attempt {attempt}: files so far {sorted(remote)}")
        time.sleep(WAIT_SECONDS)
    sys.exit(f"The release did not show up completely at {url}; files seen: {sorted(remote)}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("index", choices=sorted(INDEXES))
    parser.add_argument("version")
    parser.add_argument("dist", type=pathlib.Path)
    args = parser.parse_args()

    local = {
        p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(args.dist.iterdir())
    }
    if not local:
        sys.exit(f"No files in {args.dist}")

    url = f"{INDEXES[args.index]}/pypi/orca-pi/{args.version}/json"
    remote = fetch_remote_hashes(url, local)

    if remote != local:
        sys.exit(
            f"Files of orca-pi {args.version} on {args.index} differ from the files built in "
            "this run: this version was uploaded before from a different build (e.g. the tag "
            "was moved). The index never replaces files, so this release needs a new version "
            f"number.\n{args.index}: {remote}\nbuilt: {local}"
        )
    print(f"{args.index} holds exactly the built files: {sorted(local)}")


if __name__ == "__main__":
    main()
