#!/usr/bin/env python3
"""Dependency-free teaching validator for the DMAPRIME submission sandbox."""

from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODEL_ID_RE = re.compile(r"^[A-Za-z0-9_]+-[A-Za-z0-9_]+$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
OUTPUT_RE = re.compile(r"^(.+)-([A-Za-z0-9_]+-[A-Za-z0-9_]+)\.(csv|tsv|parquet|gz\.parquet)$", re.I)
FORECAST_COLUMNS = {
    "reference_date", "target", "horizon", "target_end_date", "location",
    "output_type", "output_type_id", "value",
}
SCENARIO_COLUMNS = {
    "origin_date", "scenario_id", "target", "horizon", "location", "age_group",
    "output_type", "output_type_id", "value", "run_grouping", "stochastic_run",
}


class Results:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.notes: list[str] = []

    def error(self, path: Path, message: str) -> None:
        self.errors.append(f"{path.as_posix()}: {message}")

    def note(self, path: Path, message: str) -> None:
        self.notes.append(f"{path.as_posix()}: {message}")


def relative(path: Path) -> Path:
    try:
        return path.resolve().relative_to(ROOT)
    except ValueError:
        return path


def simple_yaml(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8-sig").splitlines():
        if not line.strip() or line.lstrip().startswith("#") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        if key.strip() and not key.startswith((" ", "\t")):
            values[key.strip()] = value.strip().strip("'\"")
    return values


def validate_metadata(path: Path, results: Results) -> str | None:
    rel = relative(path)
    if path.suffix.lower() not in {".yml", ".yaml"}:
        results.error(rel, "practice metadata must use .yml or .yaml")
        return None
    model_id = path.stem
    if not MODEL_ID_RE.fullmatch(model_id):
        results.error(rel, "filename stem must be <team_abbr>-<model_abbr>")
        return None
    try:
        values = simple_yaml(path)
    except (OSError, UnicodeError) as exc:
        results.error(rel, f"could not read metadata: {exc}")
        return model_id
    required = {"team_abbr", "model_abbr", "model_id", "model_name", "model_type"}
    missing = sorted(required - values.keys())
    if missing:
        results.error(rel, f"missing top-level fields: {', '.join(missing)}")
    expected = f"{values.get('team_abbr', '')}-{values.get('model_abbr', '')}"
    if values.get("model_id") != model_id:
        results.error(rel, f"model_id must equal filename stem {model_id!r}")
    if expected != model_id:
        results.error(rel, f"team_abbr-model_abbr resolves to {expected!r}, not {model_id!r}")
    if values.get("model_type") not in {"forecast", "scenario"}:
        results.error(rel, "model_type must be forecast or scenario")
    return model_id


def read_table(path: Path, delimiter: str, results: Results) -> tuple[set[str], set[str], str | None]:
    rel = relative(path)
    try:
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle, delimiter=delimiter)
            if reader.fieldnames is None:
                results.error(rel, "file has no header row")
                return set(), set(), None
            columns = {name.strip() for name in reader.fieldnames if name is not None}
            if len(columns) != len(reader.fieldnames):
                results.error(rel, "column names are empty or duplicated")
            date_column = "reference_date" if "reference_date" in columns else "origin_date" if "origin_date" in columns else None
            dates: set[str] = set()
            rows = 0
            for row in reader:
                rows += 1
                if date_column and row.get(date_column, "").strip():
                    dates.add(row[date_column].strip())
            if rows == 0:
                results.error(rel, "file has a header but no data rows")
            return columns, dates, date_column
    except (OSError, UnicodeError, csv.Error) as exc:
        results.error(rel, f"could not read tabular file: {exc}")
        return set(), set(), None


def validate_output(path: Path, metadata_ids: set[str], results: Results) -> None:
    rel = relative(path)
    try:
        folder_id = path.parent.name
    except IndexError:
        results.error(rel, "output must be inside model-output/<model_id>/")
        return
    if not MODEL_ID_RE.fullmatch(folder_id):
        results.error(rel, "parent folder must be <team_abbr>-<model_abbr>")
    match = OUTPUT_RE.fullmatch(path.name)
    if not match:
        results.error(rel, "filename must be <round_id>-<team_abbr>-<model_abbr>.<extension>")
        return
    round_id, filename_model_id, extension = match.groups()
    extension = extension.lower()
    if filename_model_id != folder_id:
        results.error(rel, f"filename model ID {filename_model_id!r} does not match folder {folder_id!r}")
    if folder_id not in metadata_ids:
        results.error(rel, f"missing model-metadata/{folder_id}.yml (or .yaml)")
    if not re.fullmatch(r"(?:\d{4}-\d{2}-\d{2}|[A-Za-z0-9]+(?:_[A-Za-z0-9]+)*)", round_id):
        results.error(rel, "round_id must be an ISO date or alphanumeric parts separated by underscores")

    if extension in {"csv", "tsv"}:
        columns, dates, date_column = read_table(path, "," if extension == "csv" else "\t", results)
        if columns:
            if columns == FORECAST_COLUMNS:
                results.note(rel, "recognized the practice forecast schema")
            elif columns == SCENARIO_COLUMNS:
                results.note(rel, "recognized the practice scenario schema")
            else:
                missing_forecast = sorted(FORECAST_COLUMNS - columns)
                missing_scenario = sorted(SCENARIO_COLUMNS - columns)
                results.error(
                    rel,
                    "columns do not exactly match either practice schema; "
                    f"forecast missing [{', '.join(missing_forecast)}], "
                    f"scenario missing [{', '.join(missing_scenario)}]",
                )
            if len(dates) > 1:
                results.error(rel, f"{date_column} has more than one value: {', '.join(sorted(dates))}")
            if DATE_RE.fullmatch(round_id) and dates and dates != {round_id}:
                results.error(rel, f"filename date {round_id} does not match {date_column}: {', '.join(sorted(dates))}")
    elif extension == "parquet":
        try:
            with path.open("rb") as handle:
                if handle.read(4) != b"PAR1":
                    results.error(rel, "file does not have the expected Parquet signature")
                else:
                    results.note(rel, "Parquet signature found; full schema validation is intentionally not performed")
        except OSError as exc:
            results.error(rel, f"could not read Parquet file: {exc}")
    elif extension == "gz.parquet":
        try:
            with path.open("rb") as handle:
                if handle.read(4) != b"PAR1":
                    results.error(rel, "file does not have the expected Parquet container signature")
                else:
                    results.note(rel, "Parquet signature found; full schema validation is intentionally not performed")
        except OSError as exc:
            results.error(rel, f"could not read compressed Parquet file: {exc}")


def selected_paths(args: list[str]) -> tuple[list[Path], list[Path]]:
    if args:
        candidates = [(ROOT / arg).resolve() if not Path(arg).is_absolute() else Path(arg).resolve() for arg in args]
        metadata = [p for p in candidates if p.is_file() and "model-metadata" in p.parts]
        outputs = [p for p in candidates if p.is_file() and "model-output" in p.parts and p.name != "README.md"]
        return metadata, outputs
    metadata = sorted((ROOT / "model-metadata").glob("*.*"))
    metadata = [p for p in metadata if p.name != "README.md"]
    outputs = sorted(p for p in (ROOT / "model-output").glob("*/*") if p.is_file())
    return metadata, outputs


def main(args: list[str]) -> int:
    results = Results()
    metadata_paths, output_paths = selected_paths(args)
    if not metadata_paths:
        results.errors.append("No model metadata files were found.")
    if not output_paths:
        results.errors.append("No model output files were found.")

    metadata_ids = {model_id for p in metadata_paths if (model_id := validate_metadata(p, results))}
    for path in output_paths:
        validate_output(path, metadata_ids, results)

    for message in results.notes:
        print(f"INFO  {message}")
    if results.errors:
        for message in results.errors:
            print(f"ERROR {message}")
        print(f"\nPractice submission failed with {len(results.errors)} problem(s).")
        return 1
    print(f"\nPASS  Checked {len(metadata_paths)} metadata file(s) and {len(output_paths)} output file(s).")
    print("Remember: this is a teaching check, not operational hub validation.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
