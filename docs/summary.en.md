# A counterexample to the peak-location conjecture for plactic centralizers

For $n=10$, the binomial-basis coefficients of the plactic centralizer counting polynomial satisfy

$$
a_5=75095<88704=a_6.
$$

This disproves Conjecture 6.3(d) of Sagan and Wilson, [*Centralizers in the plactic monoid*, arXiv:2410.20460v1](https://arxiv.org/abs/2410.20460v1), numbered [Conjecture 7.3(d) in the published version](https://users.math.msu.edu/users/bsagan/Papers/Old/cpm-pub.pdf#page=19). Priority has not been established, and this material has not received external peer review.

Let $P(w)$ denote the RSK row-insertion tableau of a word. Knuth equivalence is characterized by $v\equiv w$ if and only if $P(v)=P(w)$. Define

$$
c_{n,m}(1)=\#\{w\in[m]^n:1w\equiv w1\}
=\sum_{k=0}^{n-1}a_k\binom{m}{k}.
$$

The conjecture predicts a maximum of $a_1,\ldots,a_{n-1}$ at $k=\lceil n/2\rceil$.

The authors' established centralizer criterion says that $w$ commutes with $1$ exactly when the first row of $P(w)$ consists entirely of $1$s. For $\lambda\vdash n$, write $\widehat\lambda=(\lambda_2,\lambda_3,\ldots)$ and let $f^\lambda$ count standard Young tableaux. Removing the first row and subtracting $1$ from the remaining entries gives

$$
c_{n,m}(1)=\sum_{\lambda\vdash n}f^\lambda
s_{\widehat\lambda}(1^{m-1}),\qquad m\ge1.
$$

RSK supplies the factor $f^\lambda$ through its standard recording tableaux. The hook-content formula makes the right-hand side a polynomial of degree at most $n-1$; for $n=10$, its degree is exactly $9$.

Summing over all $42$ partitions of $10$ gives the following values at $m=1,\ldots,10$:

$$
(1,252,5670,50820,275010,1086090,3456369,9398925,22677445,49807595).
$$

The degree-$9$ polynomial with binomial-basis coefficient vector

$$
(a_0,\ldots,a_9)
=(0,1,250,4917,29648,75095,88704,43414,4861,1)
$$

matches these ten values. Polynomial uniqueness therefore proves the identity. In particular, $a_6-a_5=13609>0$, contradicting the predicted maximum at $k=5$.

The repository includes a [42-row exact certificate](../data/n10_tableau_certificate.csv) and three standard-library Python verifiers: hook formulas; corner and horizontal-strip recurrences; and direct tableau enumeration together with determinant formulas. The last verifier enumerates all **239,316 semistandard tableaux** of size $10$ over an alphabet of size at most $6$, tests the insertion relation directly, and weights each accepted insertion tableau by its number of standard recording tableaux. It also independently recovers the coefficients using $m=10,\ldots,19$.

From the repository root, run:

```sh
python reproduce.py
```

The [complete Chinese proof](proof.zh-CN.md) explains the bijection, degree bound, exact arithmetic, and verification scope. This result refutes only the peak-location assertion; it does not refute the separate log-concavity conjecture or solve the general positive combinatorial rule problem for Kronecker coefficients.

The maintainer used Codex for exploration, writing, and code, with checks by separate AI subagents. Those checks are not external peer review.
