#!/usr/bin/env python3
"""Dependency-free smoke tests for the classroom submission validator."""

from __future__ import annotations

import tempfile
from pathlib import Path

import validate_submission as validator


HEADER = "reference_date,target,horizon,target_end_date,location,output_type,output_type_id,value\n"
ROW = "2026-09-10,wk ahead practice value,1,2026-09-17,US,quantile,0.5,12\n"


def check_output(path: Path) -> list[str]:
    results = validator.Results()
    validator.validate_output(path, {"capture-demo"}, results)
    return results.errors


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="hubverse-validator-") as temp_dir:
        output_dir = Path(temp_dir) / "model-output" / "capture-demo"
        output_dir.mkdir(parents=True)

        passing = output_dir / "2026-09-10-capture-demo.csv"
        passing.write_text(HEADER + ROW, encoding="utf-8")
        passing_errors = check_output(passing)
        if passing_errors:
            raise AssertionError(f"expected matching dates to pass: {passing_errors}")

        failing = output_dir / "2026-09-11-capture-demo.csv"
        passing.rename(failing)
        failing_errors = check_output(failing)
        expected = "filename date 2026-09-11 does not match reference_date: 2026-09-10"
        if not any(expected in message for message in failing_errors):
            raise AssertionError(f"expected the date mismatch error, found: {failing_errors}")

    print("PASS  Validator accepts matching dates and rejects an intentional date mismatch.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
