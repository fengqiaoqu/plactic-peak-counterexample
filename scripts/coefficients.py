"""Exact tableau computation of c_{n,m}(1) and its two binomial expansions.

The input theorem is Sagan--Wilson's characterization: every column of P(w)
contains 1. Thus the first row consists entirely of ones and all other entries
are >1. RSK gives c = sum_{lambda|-n} f^lambda s_{tail(lambda)}(1^(m-1)).
This is an oracle for experiments, not a proof of any log-concavity conjecture.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
import json
from math import comb, factorial
from pathlib import Path
import time


BASIS = {
    "a": "c_n(m) = sum(a[k] * binomial(m,k), k=0,...,n-1)",
    "b": "c_n(m) = sum(b[k] * binomial(m-1,k), k=0,...,n-1)",
}


def require(condition, detail):
    if not condition:
        raise AssertionError(detail)


def partitions(n, maximum=None):
    if n == 0:
        yield ()
        return
    maximum = n if maximum is None else min(maximum, n)
    for first in range(maximum, 0, -1):
        for tail in partitions(n - first, first):
            yield (first,) + tail


def hook_product(shape):
    result = 1
    for i, width in enumerate(shape):
        for j in range(width):
            result *= width-j + sum(row > j for row in shape)-i-1
    return result


def differences(values):
    answer = []
    while values:
        answer.append(values[0])
        values = [b-a for a, b in zip(values, values[1:])]
    return answer


def compute(n):
    values = [Fraction(0)] * (n+1)
    ftotal = factorial(n)
    shape_count = 0
    for shape in partitions(n):
        shape_count += 1
        dimension = Fraction(ftotal, hook_product(shape))
        require(dimension.denominator == 1, ("nonintegral dimension", shape))
        dim = dimension.numerator
        tail = shape[1:]
        denominator = hook_product(tail)
        contents = [j-i for i, width in enumerate(tail) for j in range(width)]
        for m in range(n+1):
            numerator = dim
            for content in contents:
                numerator *= m-1+content
                if numerator == 0:
                    break
            values[m] += Fraction(numerator, denominator)
    require(all(v.denominator == 1 for v in values), ("nonintegral counts", n))
    vals = [v.numerator for v in values]
    a = differences(vals)
    b = differences(vals[1:])
    require(a[-1] == 0 and a[0] == 0 and a[1] == 1, ("degree/constant/linear checks", n))
    a = a[:-1]
    require(a[-1] == 1, ("leading binomial coefficient", n))
    require(all(x > 0 for x in a[1:]), ("nonpositive a", n))
    require(all(x >= 0 for x in b), ("negative b", n))
    require(len(a) == len(b) == n, ("basis vector lengths", n))
    for m, value in enumerate(vals):
        require(sum(a[k] * comb(m, k) for k in range(n) if k <= m) == value,
                ("binomial(m,k) reconstruction", n, m))
        if m >= 1:
            require(sum(b[k] * comb(m-1, k) for k in range(n) if k < m) == value,
                    ("binomial(m-1,k) reconstruction", n, m))
    a_failures = [k for k in range(2, len(a)-1)
                  if a[k]**2 < a[k-1]*a[k+1]]
    b_failures = [k for k in range(1, len(b)-1)
                  if b[k]**2 < b[k-1]*b[k+1]]
    peak = max(a)
    peaks = [k for k, value in enumerate(a) if value == peak]
    return dict(n=n, partitions=shape_count, a=a, b=b,
                a_log_concavity_failures=a_failures,
                b_log_concavity_failures=b_failures,
                a_peak_indices=peaks,
                expected_peak_attained=(n+1)//2 in peaks,
                values_m_0_to_n=vals)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-n", type=int, default=10, choices=range(2, 33))
    parser.add_argument("--output-dir", type=Path,
                        default=Path(__file__).resolve().parents[1]/"data"/"generated")
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    started = time.perf_counter()
    rows = []
    for n in range(2, args.max_n+1):
        row = compute(n)
        rows.append(row)
        print(json.dumps({k: row[k] for k in
                          ["n", "partitions", "a_log_concavity_failures",
                           "b_log_concavity_failures", "a_peak_indices",
                           "expected_peak_attained"]}), flush=True)
    result = dict(schema_version=1, range=dict(min_n=2, max_n=args.max_n),
                  basis=BASIS, rows=rows, elapsed_seconds=time.perf_counter()-started)
    (args.output_dir/"coefficients.json").write_text(
        json.dumps(result, indent=2)+"\n", encoding="utf-8")


if __name__ == "__main__":
    main()
