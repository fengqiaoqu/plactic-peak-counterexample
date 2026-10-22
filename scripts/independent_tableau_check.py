#!/usr/bin/env python3
"""Independent exact review of Sagan--Wilson Conjecture 6.3(d), n=10.

Enumerate ALL SSYT of
size 10 over [6], without filtering the first row, then test commutation by
two direct row insertions.  Obtain the binomial(m,k) coefficients separately
by Jacobi--Trudi determinants evaluated at m=10,...,19 and exact interpolation.
The standard-tableau weights use a factorial-reciprocal determinant, not the
hook-content formula or corner recursion.
"""

from __future__ import annotations

import argparse
from bisect import bisect_right
from fractions import Fraction
from functools import cache
import json
from math import comb, factorial
from pathlib import Path
import time


Partition = tuple[int, ...]


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise AssertionError(detail)


@cache
def partitions(n: int, maximum: int | None = None) -> tuple[Partition, ...]:
    if n == 0:
        return ((),)
    maximum = n if maximum is None else min(n, maximum)
    return tuple((a,) + tail for a in range(maximum, 0, -1)
                 for tail in partitions(n - a, a))


def determinant(matrix: list[list[Fraction]]) -> Fraction:
    work = [row[:] for row in matrix]
    answer = Fraction(1)
    for col in range(len(work)):
        pivot = next((r for r in range(col, len(work)) if work[r][col]), None)
        if pivot is None:
            return Fraction(0)
        if pivot != col:
            work[col], work[pivot] = work[pivot], work[col]
            answer = -answer
        value = work[col][col]
        answer *= value
        for row in range(col + 1, len(work)):
            multiplier = work[row][col] / value
            for j in range(col + 1, len(work)):
                work[row][j] -= multiplier * work[col][j]
    return answer


@cache
def standard_tableau_count(shape: Partition) -> int:
    # f^lambda = n! det(1/(lambda_i-i+j)!).  A negative factorial means zero.
    matrix = [[Fraction(1, factorial(shape[i] - i + j))
               if shape[i] - i + j >= 0 else Fraction(0)
               for j in range(len(shape))] for i in range(len(shape))]
    result = factorial(sum(shape)) * determinant(matrix)
    require(result.denominator == 1 and result > 0, ("standard-tableau determinant", shape, result))
    return result.numerator


def row_insertion(word: tuple[int, ...]) -> tuple[tuple[int, ...], ...]:
    rows: list[list[int]] = []
    for letter in word:
        carry = letter
        for row in rows:
            position = bisect_right(row, carry)
            if position == len(row):
                row.append(carry)
                break
            row[position], carry = carry, row[position]
        else:
            rows.append([carry])
    return tuple(tuple(row) for row in rows)


def direct_tableau_counts(n: int = 10, max_m: int = 6) -> dict:
    exact_max_weighted = [0] * (max_m + 1)
    exact_max_all_tableaux = [0] * (max_m + 1)
    per_shape = []
    all_tableaux = first_row_predicate_disagreements = commuting_tableaux = 0
    for shape in partitions(n):
        if len(shape) > max_m:
            per_shape.append({"partition": list(shape), "f_lambda": standard_tableau_count(shape),
                              "all_ssyt": 0, "commuting_ssyt": 0})
            continue
        positions = tuple((row, col) for row, width in enumerate(shape) for col in range(width))
        cell_indices = {cell: index for index, cell in enumerate(positions)}
        above = [cell_indices.get((row - 1, col)) for row, col in positions]
        left = [cell_indices.get((row, col - 1)) for row, col in positions]
        reading_order = sorted(range(n), key=lambda k: (-positions[k][0], positions[k][1]))
        entries = [0] * n
        weight = standard_tableau_count(shape)
        shape_total = shape_commuting = 0

        def visit(index: int) -> None:
            nonlocal all_tableaux, first_row_predicate_disagreements, commuting_tableaux
            nonlocal shape_total, shape_commuting
            if index == n:
                all_tableaux += 1
                shape_total += 1
                maximum = max(entries)
                exact_max_all_tableaux[maximum] += 1
                word = tuple(entries[k] for k in reading_order)
                commutes = row_insertion((1,) + word) == row_insertion(word + (1,))
                first_row_ones = all(letter == 1 for letter in entries[:shape[0]])
                first_row_predicate_disagreements += commutes != first_row_ones
                if commutes:
                    commuting_tableaux += 1
                    shape_commuting += 1
                    exact_max_weighted[maximum] += weight
                return
            minimum = 1
            if left[index] is not None:
                minimum = max(minimum, entries[left[index]])
            if above[index] is not None:
                minimum = max(minimum, entries[above[index]] + 1)
            for letter in range(minimum, max_m + 1):
                entries[index] = letter
                visit(index + 1)

        visit(0)
        per_shape.append({"partition": list(shape), "f_lambda": weight,
                          "all_ssyt": shape_total, "commuting_ssyt": shape_commuting})
    require(first_row_predicate_disagreements == 0, "commutation/first-row predicate disagreement")
    # Independent total from sum_lambda s_lambda(1^m): coefficient of
    # (1-t)^(-m) (1-t^2)^(-m(m-1)/2).
    total_formula = sum(comb(max_m + n - 2 * j - 1, n - 2 * j)
                        * comb(max_m * (max_m - 1) // 2 + j - 1, j)
                        for j in range(n // 2 + 1))
    require(all_tableaux == total_formula, ("all SSYT total", all_tableaux, total_formula))
    values = [sum(exact_max_weighted[:m + 1]) for m in range(max_m + 1)]
    return {"n": n, "max_m": max_m, "all_ssyt_enumerated": all_tableaux,
            "independent_all_ssyt_total": total_formula,
            "commuting_ssyt_unweighted": commuting_tableaux,
            "first_row_predicate_disagreements": first_row_predicate_disagreements,
            "exact_max_tableaux_counts": exact_max_all_tableaux,
            "exact_max_commuting_word_counts": exact_max_weighted,
            "c_n_m_for_m_0_through_6": values, "per_shape": per_shape}


def h_specialization(degree: int, alphabet_size: int) -> Fraction:
    if degree < 0:
        return Fraction(0)
    if degree == 0:
        return Fraction(1)
    return Fraction(comb(alphabet_size + degree - 1, degree))


def jacobi_trudi_count(shape: Partition, alphabet_size: int) -> int:
    matrix = [[h_specialization(shape[i] - i + j, alphabet_size)
               for j in range(len(shape))] for i in range(len(shape))]
    result = determinant(matrix)
    require(result.denominator == 1 and result >= 0, ("Jacobi-Trudi", shape, alphabet_size, result))
    return result.numerator


def solve(matrix: list[list[Fraction]], values: list[int]) -> list[Fraction]:
    size = len(matrix)
    work = [row[:] + [Fraction(value)] for row, value in zip(matrix, values)]
    for col in range(size):
        pivot = next((r for r in range(col, size) if work[r][col]), None)
        require(pivot is not None, ("interpolation singular", col))
        work[col], work[pivot] = work[pivot], work[col]
        divisor = work[col][col]
        work[col] = [value / divisor for value in work[col]]
        for row in range(size):
            if row != col:
                multiplier = work[row][col]
                work[row] = [a - multiplier * b for a, b in zip(work[row], work[col])]
    answer = [row[-1] for row in work]
    require(all(sum(a * b for a, b in zip(row, answer)) == value
                for row, value in zip(matrix, values)), "interpolation reconstruction")
    return answer


def independent_polynomial(n: int = 10) -> dict:
    arguments = list(range(n, 2 * n))
    values = [sum(standard_tableau_count(shape)
                  * jacobi_trudi_count(shape[1:], m - 1) for shape in partitions(n))
              for m in arguments]
    matrix = [[Fraction(comb(m, k)) for k in range(n)] for m in arguments]
    coefficients = solve(matrix, values)
    require(all(value.denominator == 1 for value in coefficients), "nonintegral coefficient")
    return {"n": n, "interpolation_m_values": arguments,
            "c_n_m_at_interpolation_values": values,
            "basis": "binomial(m,k), k=0,...,9; NOT binomial(m-1,k)",
            "method": "Jacobi-Trudi determinant for s_tail(1^(m-1)); reciprocal-factorial determinant for f_lambda; interpolate only at m>=n.",
            "coefficients_a_0_through_9": [value.numerator for value in coefficients]}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path,
                        default=Path(__file__).resolve().parents[1]/"data"/"generated")
    args = parser.parse_args()
    started = time.perf_counter()
    direct = direct_tableau_counts()
    polynomial = independent_polynomial()
    coefficients = polynomial["coefficients_a_0_through_9"]
    low_values = direct["c_n_m_for_m_0_through_6"]
    for m, value in enumerate(low_values):
        reconstructed = sum(coefficients[k] * comb(m, k) for k in range(min(m, 9) + 1))
        require(reconstructed == value, ("direct/tableau-polynomial mismatch", m, reconstructed, value))
    # Newton differences of the DIRECT values are checked only after the
    # independently interpolated polynomial is shown to agree even at m=0.
    differences = low_values[:]
    first_differences = []
    while differences:
        first_differences.append(differences[0])
        differences = [b - a for a, b in zip(differences, differences[1:])]
    require(first_differences == coefficients[:7], "wrong binomial-basis conversion")
    require(coefficients[5] == 75095 and coefficients[6] == 88704 and coefficients[6] > coefficients[5],
            ("claimed counterexample not reproduced", coefficients))
    result = {"status": "passed", "independent_methods": True,
              "direct_tableau_enumeration": direct,
              "independent_polynomial_interpolation": polynomial,
              "direct_newton_coefficients_a_0_through_6": first_differences,
              "a_5": coefficients[5], "a_6": coefficients[6],
              "difference_a_6_minus_a_5": coefficients[6] - coefficients[5],
              "verdict": "The n=10 polynomial in the original binomial(m,k) basis violates Sagan-Wilson arXiv:2410.20460v1 Conjecture 6.3(d): ceil(10/2)=5 but a_6>a_5.",
              "scope": "Only the prescribed peak location is refuted; no log-concavity or first-discovery conclusion.",
              "elapsed_seconds": round(time.perf_counter() - started, 6)}
    args.output_dir.mkdir(parents=True, exist_ok=True)
    destination = args.output_dir / "independent_tableau_check.json"
    destination.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": result["status"], "all_ssyt_enumerated": direct["all_ssyt_enumerated"],
                      "c_10_m_for_m_0_through_6": low_values,
                      "a_0_through_9": coefficients, "a_6_minus_a_5": coefficients[6] - coefficients[5],
                      "elapsed_seconds": result["elapsed_seconds"], "output": str(destination.resolve())},
                     ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
