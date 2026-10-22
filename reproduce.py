#!/usr/bin/env python3
"""Reproduce the n=10 peak-location counterexample using Python >=3.10.

Three exact implementations use only the standard library.  With no options,
results are generated in a temporary directory and compared to the committed
baselines.  Use --output-dir artifacts to retain generated results, and
--max-n 32 to reproduce the optional coefficient scan through degree 32.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import time


ROOT = Path(__file__).resolve().parent
RUNTIME_KEYS = {"elapsed_seconds", "runtime_seconds", "python_version"}


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise AssertionError(detail)


def mathematical_data(value):
    """Exclude observational run metadata, while keeping all mathematical data."""
    if isinstance(value, dict):
        return {key: mathematical_data(item) for key, item in value.items()
                if key not in RUNTIME_KEYS}
    if isinstance(value, list):
        return [mathematical_data(item) for item in value]
    return value


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def read_csv(path: Path):
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def run_script(name: str, output_dir: Path, extra: list[str] | None = None) -> None:
    arguments = [sys.executable, "-B", str(ROOT/"scripts"/name),
                 "--output-dir", str(output_dir), *(extra or [])]
    result = subprocess.run(arguments, capture_output=True, text=True, encoding="utf-8")
    if result.returncode:
        if result.stdout:
            print(result.stdout, file=sys.stderr)
        if result.stderr:
            print(result.stderr, file=sys.stderr)
        raise RuntimeError(f"{name} exited with status {result.returncode}")


def verify_generated(output_dir: Path, max_n: int) -> dict:
    generated_coefficients = read_json(output_dir/"coefficients.json")
    baseline_coefficients = read_json(ROOT/"data"/"coefficients.json")
    require(baseline_coefficients["range"] == {"min_n": 2, "max_n": 32},
            "The committed coefficient baseline must cover n=2,...,32")
    expected_coefficients = dict(baseline_coefficients)
    expected_coefficients["range"] = {"min_n": 2, "max_n": max_n}
    expected_coefficients["rows"] = [row for row in baseline_coefficients["rows"] if row["n"] <= max_n]
    require(mathematical_data(generated_coefficients) == mathematical_data(expected_coefficients),
            "Hook-content results differ from the committed baseline")
    require([row["n"] for row in generated_coefficients["rows"]] == list(range(2, max_n + 1)),
            "Coefficient rows do not cover the requested range exactly")
    for row in generated_coefficients["rows"]:
        require(len(row["a"]) == len(row["b"]) == row["n"], "Misaligned binomial basis vectors")
        require(len(row["values_m_0_to_n"]) == row["n"] + 1, "Misaligned m-value vector")

    for name in ("counterexample_verification.json", "independent_tableau_check.json"):
        require(mathematical_data(read_json(output_dir/name))
                == mathematical_data(read_json(ROOT/"data"/name)),
                f"Generated mathematical data differ from baseline: {name}")

    certificate = read_csv(output_dir/"n10_tableau_certificate.csv")
    require(certificate == read_csv(ROOT/"data"/"n10_tableau_certificate.csv"),
            "The 42-shape certificate differs from baseline")
    certificate_by_shape = {tuple(map(int, row["shape"].split(","))): row for row in certificate}
    require(len(certificate) == len(certificate_by_shape) == 42, "Expected 42 distinct partitions of 10")

    hook_row = next(row for row in generated_coefficients["rows"] if row["n"] == 10)
    branching = read_json(output_dir/"counterexample_verification.json")
    direct = read_json(output_dir/"independent_tableau_check.json")
    direct_tableaux = direct["direct_tableau_enumeration"]
    determinants = direct["independent_polynomial_interpolation"]
    require(hook_row["a"] == branching["a"] == determinants["coefficients_a_0_through_9"],
            "The three independent coefficient vectors disagree")
    require(direct["direct_newton_coefficients_a_0_through_6"] == hook_row["a"][:7],
            "Direct Newton differences disagree with the binomial(m,k) coefficients")
    require(hook_row["values_m_0_to_n"] == branching["values_m_0_to_10"],
            "Hook-content and branching m-values disagree")
    require(hook_row["values_m_0_to_n"][:7] == direct_tableaux["c_n_m_for_m_0_through_6"],
            "Direct insertion counts disagree with the counting polynomial")
    require(determinants["interpolation_m_values"] == list(range(10, 20)),
            "Independent interpolation must use only m>=n")
    require(direct_tableaux["all_ssyt_enumerated"] == 239316
            and direct_tableaux["first_row_predicate_disagreements"] == 0,
            "The complete direct tableau enumeration did not pass")
    require(branching["direct_word_tests"] == 6684 and branching["certificate_partitions"] == 42,
            "The direct word/certificate checks did not pass")
    require(len(direct_tableaux["per_shape"]) == 42, "Missing direct-enumeration shapes")
    for shape in direct_tableaux["per_shape"]:
        key = tuple(shape["partition"])
        require(key in certificate_by_shape
                and shape["f_lambda"] == int(certificate_by_shape[key]["f_lambda"]),
                ("Independent standard-tableau weights disagree", key))
    for m in range(1, 11):
        require(sum(int(row["f_lambda"]) * int(row[f"ssyt_tail_alphabet_{m-1}"])
                    for row in certificate) == hook_row["values_m_0_to_n"][m],
                ("Shape certificate does not sum to c(10,m)", m))
    require(hook_row["a"][5] == 75095 and hook_row["a"][6] == 88704,
            "The stated counterexample did not reproduce")
    return {
        "status": "passed", "coefficient_range": {"min_n": 2, "max_n": max_n},
        "committed_coefficient_baseline_range": {"min_n": 2, "max_n": 32},
        "baseline_comparison": "All mathematical fields match; runtime metadata excluded.",
        "binomial_basis": "binomial(m,k), indexed by k=0,...,n-1",
        "n": 10, "a": hook_row["a"], "a_5": 75095, "a_6": 88704,
        "difference_a_6_minus_a_5": 13609, "predicted_peak": 5, "actual_unique_peak": 6,
        "certificate_partitions": 42, "direct_word_tests": 6684,
        "direct_ssyt_tests": 239316, "independent_algorithms_agree": True,
    }


def reproduce(output_dir: Path, max_n: int) -> dict:
    output_dir.mkdir(parents=True, exist_ok=True)
    print(f"[1/3] Hook-content computation, n=2,...,{max_n}", flush=True)
    run_script("coefficients.py", output_dir, ["--max-n", str(max_n)])
    print("[2/3] Corner/horizontal-strip recursion and 6,684 direct word tests", flush=True)
    run_script("verify_counterexample.py", output_dir,
               ["--coefficients", str(output_dir/"coefficients.json")])
    print("[3/3] All 239,316 tableaux and independent determinant interpolation", flush=True)
    run_script("independent_tableau_check.py", output_dir)
    summary = verify_generated(output_dir, max_n)
    (output_dir/"reproduction_summary.json").write_text(
        json.dumps(summary, indent=2)+"\n", encoding="utf-8")
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-n", type=int, default=10, choices=range(10, 33),
                        help="Coefficient scan upper bound, 10 through 32 (default: 10)")
    parser.add_argument("--output-dir", type=Path,
                        help="Keep generated results here; default uses a temporary directory")
    args = parser.parse_args()
    if sys.version_info < (3, 10):
        parser.error("Python 3.10 or newer is required")
    if not __debug__:
        parser.error("Run Python without -O or -OO so all verification assertions execute")
    started = time.perf_counter()
    if args.output_dir is None:
        with tempfile.TemporaryDirectory(prefix="plactic-peak-") as temporary:
            output_dir = Path(temporary).resolve()
            require(output_dir.parent == Path(tempfile.gettempdir()).resolve(), "Unexpected temporary path")
            summary = reproduce(output_dir, args.max_n)
        output_description = "Temporary output compared and removed."
    else:
        output_dir = args.output_dir.resolve()
        if output_dir == (ROOT/"data").resolve():
            parser.error("Choose a separate output directory, such as artifacts or data/generated")
        summary = reproduce(output_dir, args.max_n)
        output_description = f"Generated output retained in {output_dir}"
    print(f"PASS: a_5={summary['a_5']}, a_6={summary['a_6']}, "
          f"a_6-a_5={summary['difference_a_6_minus_a_5']}; "
          "42 partitions, 6,684 words and 239,316 tableaux checked.")
    print(f"All three methods match the committed baseline (n=2,...,{args.max_n}).")
    print(output_description)
    print(f"Elapsed: {time.perf_counter()-started:.3f} seconds")


if __name__ == "__main__":
    main()
