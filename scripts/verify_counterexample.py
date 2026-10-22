"""Independent exact certificate for the n=10 peak-position counterexample.

No hook-length or hook-content formula is used here. Standard tableaux are
counted by corner removal; semistandard tableaux by horizontal-strip branching.
A further direct word-insertion check covers small cases.
"""
from __future__ import annotations

import argparse
from functools import cache
from itertools import product
import csv
import json
from math import comb
from pathlib import Path


def partitions(n, maximum=None):
    if n == 0:
        yield ()
    else:
        maximum = n if maximum is None else min(maximum, n)
        for first in range(maximum, 0, -1):
            for tail in partitions(n-first, first):
                yield (first,) + tail


@cache
def standard_count(shape):
    if not shape:
        return 1
    total = 0
    for i, width in enumerate(shape):
        if i+1 == len(shape) or width > shape[i+1]:
            predecessor = list(shape)
            predecessor[i] -= 1
            total += standard_count(tuple(x for x in predecessor if x))
    return total


@cache
def horizontal_predecessors(shape):
    """All mu with shape/mu a horizontal strip, including the empty strip."""
    ranges = [range(shape[i+1] if i+1 < len(shape) else 0, width+1)
              for i, width in enumerate(shape)]
    return tuple(tuple(x for x in parts if x) for parts in product(*ranges))


@cache
def semistandard_count(shape, alphabet):
    if alphabet == 0:
        return int(not shape)
    return sum(semistandard_count(mu, alphabet-1)
               for mu in horizontal_predecessors(shape))


def c(n, m):
    assert m >= 1
    return sum(standard_count(shape)*semistandard_count(shape[1:], m-1)
               for shape in partitions(n))


def insertion(word):
    rows = []
    for value in word:
        for row in rows:
            for j, old in enumerate(row):
                if old > value:
                    row[j], value = value, old
                    break
            else:
                row.append(value)
                break
        else:
            rows.append([value])
    return tuple(tuple(row) for row in rows)


def coefficient(values, k):
    return sum((-1)**(k-j)*comb(k, j)*values[j] for j in range(k+1))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path,
                        default=Path(__file__).resolve().parents[1]/"data"/"generated")
    parser.add_argument("--coefficients", type=Path,
                        default=Path(__file__).resolve().parents[1]/"data"/"coefficients.json")
    args = parser.parse_args()
    if not __debug__:
        parser.error("Run Python without -O or -OO so all verification assertions execute")
    root = args.output_dir
    root.mkdir(parents=True, exist_ok=True)
    previous = json.loads(args.coefficients.read_text(encoding="utf-8"))
    rows_by_n = {row["n"]: row for row in previous["rows"]}
    branch_checks = 0
    for n in range(2, 11):
        values = [0] + [c(n, m) for m in range(1, n+1)]
        assert values == rows_by_n[n]["values_m_0_to_n"], (n, values)
        a = [coefficient(values, k) for k in range(n)]
        assert a == rows_by_n[n]["a"]
        branch_checks += n

    word_checks = []
    total_words = 0
    for n in range(1, 7):
        for m in range(1, 5):
            actual = 0
            characterization_count = 0
            for word in product(range(1, m+1), repeat=n):
                total_words += 1
                left, right = insertion((1,)+word), insertion(word+(1,))
                commutes = left == right
                tableau = insertion(word)
                first_row_ones = all(letter == 1 for letter in tableau[0])
                assert commutes == first_row_ones, (word, left, right)
                actual += commutes
                characterization_count += first_row_ones
            predicted = c(n, m)
            assert actual == characterization_count == predicted
            word_checks.append(dict(n=n, m=m, c=actual))

    values = [0] + [c(10, m) for m in range(1, 11)]
    a = [coefficient(values, k) for k in range(10)]
    assert a == [0, 1, 250, 4917, 29648, 75095, 88704, 43414, 4861, 1]
    assert a[6] > a[5] and a.index(max(a)) == 6
    assert coefficient(values, 10) == 0

    # Forty-two individual tableau-shape contributions certify every value
    # c(10,m), m=1,...,10, without invoking either hook formula.
    certificate = []
    for shape in partitions(10):
        f = standard_count(shape)
        counts = [semistandard_count(shape[1:], q) for q in range(10)]
        row = {"shape": ",".join(map(str, shape)), "f_lambda": f}
        row.update({f"ssyt_tail_alphabet_{q}": count
                    for q, count in enumerate(counts)})
        certificate.append(row)
    with (root/"n10_tableau_certificate.csv").open("w", encoding="utf-8",
                                                  newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(certificate[0]))
        writer.writeheader()
        writer.writerows(certificate)
    for m in range(1, 11):
        assert sum(r["f_lambda"]*r[f"ssyt_tail_alphabet_{m-1}"]
                   for r in certificate) == values[m]

    # Degree <=9 follows from |tail(lambda)|<=9. Zero constant term follows
    # from the hook-shape alternating binomial identity, explained in the proof.
    result = dict(
        status="passed",
        conjecture="Sagan-Wilson arXiv:2410.20460 Conjecture 6.3(d); journal 7.3(d)",
        n=10, predicted_peak=5, actual_unique_peak=6, a=a,
        difference_a6_minus_a5=a[6]-a[5],
        values_m_0_to_10=values,
        independent_method="Corner recursion for f; horizontal-strip recursion for SSYT; no hook formulas",
        matched_values_n2_to_10=branch_checks,
        certificate_partitions=len(certificate),
        direct_word_tests=total_words,
        direct_word_cases=word_checks,
        polynomial_degree_upper_bound=9,
        novelty="No priority conclusion is established by this program.",
        scope="Only the prescribed peak location is refuted; no log-concavity or first-discovery conclusion.",
    )
    (root/"counterexample_verification.json").write_text(
        json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps({k: result[k] for k in ["status", "n", "a",
                     "predicted_peak", "actual_unique_peak",
                     "difference_a6_minus_a5", "certificate_partitions",
                     "direct_word_tests"]}, indent=2))


if __name__ == "__main__":
    main()
