import shutil
from dataclasses import dataclass
from pathlib import Path


def _is_separator(line: str) -> bool:
    """Return True if the line contains only dashes, equals signs, and spaces (ORCA separator line)."""
    stripped = line.strip()
    return bool(stripped) and all(c in "-= " for c in stripped)


@dataclass(frozen=True)
class JsonFilesExporter:
    json_files_dir: Path
    prefix: str
    enabled: bool

    def export_jsons_from(
        self,
        src_dir: Path,
        *,
        recursive: bool = False,
        overwrite: bool = True,
        gbw_subdir: str = "gbw",
        property_subdir: str = "property",
    ) -> tuple[list[Path], list[Path]]:
        """
        Copy JSON files from src_dir into tests/json_files/<plain_subdir|property_subdir>.

        - plain:     *.json excluding *.property.json
        - property:  *.property.json

        Destination filenames are prefixed:
            <prefix>__<original_filename>

        Returns: (plain_dests, property_dests)
        """
        pattern = "**/*.json" if recursive else "*.json"
        sources = sorted(p for p in src_dir.glob(pattern) if p.is_file())

        plain_out = self.json_files_dir / gbw_subdir
        prop_out = self.json_files_dir / property_subdir
        plain_out.mkdir(parents=True, exist_ok=True)
        prop_out.mkdir(parents=True, exist_ok=True)

        plain_dests: list[Path] = []
        prop_dests: list[Path] = []

        for src in sources:
            name = src.name

            is_property = name.endswith(".property.json")
            if is_property:
                dst = prop_out / f"{self.prefix}_{name}"
                prop_dests.append(dst)
            else:
                # it's a .json from the glob, but not a .property.json
                dst = plain_out / f"{self.prefix}_{name}"
                plain_dests.append(dst)

            if not self.enabled:
                continue

            if dst.exists() and not overwrite:
                raise FileExistsError(f"JSON file exists (overwrite disabled): {dst}")

            shutil.copy2(src, dst)

        if self.enabled and not (plain_dests or prop_dests):
            raise FileNotFoundError(f"No JSON files found in {src_dir} (pattern={pattern!r})")

        return plain_dests, prop_dests


@dataclass(frozen=True)
class OutFileExporter:
    out_file: Path
    enabled: bool

    @staticmethod
    def _extract_orca_blocks(src: Path) -> str:
        """
        Extract only the `Grepper`-relevant blocks from a full ORCA .out file.

        Strips all system-specific info (paths, hostnames, timings) and keeps only:
          - Total Charge / Multiplicity lines (once each)
          - Each CARTESIAN COORDINATES (ANGSTROEM) block
          - Each FINAL SINGLE POINT ENERGY line (with surrounding separator lines)
          - Each CARTESIAN GRADIENT block
        """
        result: list[str] = []
        charge_done = False
        mult_done = False
        prev_line = ""

        with src.open() as f:
            it = (raw.rstrip("\n") for raw in f)
            # pending holds the already-fetched next line, giving one line of lookahead
            pending: str | None = next(it, None)

            while pending is not None:
                line = pending
                pending = next(it, None)

                # Charge line (emit once)
                if (
                    not charge_done
                    and "Total Charge" in line
                    and "Charge" in line
                    and "...." in line
                ):
                    result.append(line)
                    charge_done = True
                    prev_line = line
                    continue

                # Mult line (emit once)
                if not mult_done and "Multiplicity" in line and "Mult" in line and "...." in line:
                    result.append(line)
                    mult_done = True
                    prev_line = line
                    continue

                # CARTESIAN COORDINATES block
                if "CARTESIAN COORDINATES (ANGSTROEM)" in line:
                    result.append("")
                    if _is_separator(prev_line):
                        result.append(prev_line)
                    result.append(line)
                    if pending is not None:
                        result.append(pending)  # separator after header
                        pending = next(it, None)
                    while pending is not None and pending.strip():
                        result.append(pending)
                        pending = next(it, None)
                    result.append("")
                    continue

                # FINAL SINGLE POINT ENERGY line (with surrounding separators)
                if "FINAL SINGLE POINT ENERGY" in line:
                    result.append("")
                    if _is_separator(prev_line):
                        result.append(prev_line)
                    result.append(line)
                    if pending is not None and _is_separator(pending):
                        result.append(pending)
                        prev_line = pending
                        pending = next(it, None)
                    else:
                        prev_line = line
                    result.append("")
                    continue

                # CARTESIAN GRADIENT block (match exact header, not "CARTESIAN GRADIENT NORMS")
                if line.strip() == "CARTESIAN GRADIENT":
                    result.append("")
                    if _is_separator(prev_line):
                        result.append(prev_line)
                    result.append(line)
                    if pending is not None:
                        result.append(pending)  # separator after header
                        pending = next(it, None)
                    if pending is not None:
                        result.append(pending)  # blank line between separator and data
                        pending = next(it, None)
                    while pending is not None and pending.strip():
                        result.append(pending)
                        pending = next(it, None)
                    result.append("")
                    continue

                prev_line = line

        # Collapse consecutive blank lines into one
        cleaned: list[str] = []
        prev_blank = False
        for ln in result:
            if not ln.strip():
                if not prev_blank:
                    cleaned.append(ln)
                prev_blank = True
            else:
                cleaned.append(ln)
                prev_blank = False

        return "\n".join(cleaned).rstrip() + "\n"

    def export_from(self, src: Path) -> None:
        """Extract grepper-relevant blocks from src and write to self.out_file."""
        if not self.enabled:
            return
        content = self._extract_orca_blocks(src)
        self.out_file.write_text(content)
