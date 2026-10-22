# Sources and status of the cited conjecture

Source and literature-status checks were performed on 2026-10-22. The main result in this package concerns the coefficients of $\binom{m}{k}$ in $c_{n,m}(1)$. Its precise target is Sagan--Wilson Conjecture 7.3(d) in the published article below, equivalently Conjecture 6.3(d) in the specified preprint version. Bibliographic entries are provided in [references.bib](references.bib).

## Primary source: the published assertion

**Bruce E. Sagan and Alexander N. Wilson.** *Centralizers in the plactic monoid.* Semigroup Forum **110**(3), 724--744 (2025). Published online 2025-05-15. DOI: [10.1007/s00233-025-10535-0](https://doi.org/10.1007/s00233-025-10535-0).

- **Exact target:** Section 7, Conjecture 7.3(d), printed p. 742. The preceding display uses $c_{n,m}(1)=\sum_{k=0}^{n-1}a_k\binom{m}{k}$; clause (d) specifies a maximum at $k=\lceil n/2\rceil$.
- **Counting criterion used in the proof:** Theorem 4.2 and Corollary 4.3(a)--(b) characterize membership in $C(1)$ by the first row of the insertion tableau consisting entirely of ones.
- **Connection to the original research direction:** Section 1, printed p. 725, and Section 2 describe the motivation from commuting crystal structures on lexicographic bitableaux.
- **Access:** [publisher record](https://link.springer.com/article/10.1007/s00233-025-10535-0); [author-hosted published text](https://users.math.msu.edu/users/bsagan/Papers/Old/cpm-pub.pdf). These are external links; the package does not redistribute either text.

The exact arithmetic in this package gives $a_5=75095<a_6=88704$ for $n=10$, contradicting the specified peak position. The counterexample does not address clause (c), which asserts log-concavity.

## Earlier numbering: the fixed preprint version

**Bruce E. Sagan and Alexander N. Wilson.** *Centralizers in the plactic monoid.* [arXiv:2410.20460v1](https://arxiv.org/abs/2410.20460v1), submitted 2024-10-27.

- Section 6, Conjecture 6.3(d), printed p. 16, is the same peak-location assertion in the $\binom{m}{k}$ basis.
- Theorem 3.2 and Corollary 3.3 give the single-letter criterion corresponding to the published Theorem 4.2 and Corollary 4.3.
- The [arXiv history](https://arxiv.org/abs/2410.20460) listed only v1 when checked. The published article adds a section and changes the relevant conjecture numbers from 6.x to 7.x; both identifiers are stated explicitly here.

## Subsequent work checked to avoid claiming an already settled result

**Bruce E. Sagan and Chenchen Zhao.** *Properties of plactic monoid centralizers.* Semigroup Forum **113**, 242--262 (2026), published online 2026-06-24. DOI: [10.1007/s00233-026-10652-4](https://doi.org/10.1007/s00233-026-10652-4). Earlier version: [arXiv:2512.21401v1](https://arxiv.org/abs/2512.21401v1), submitted 2025-12-24.

- Proposition 4.1, printed p. 257, allows $m\ge0$ in the counting-polynomial statement for $n\ge2$.
- Theorem 4.2(a), (b), and (e), printed pp. 257--259, prove the zero constant term, $a_1=1$, and positivity of the remaining $a_i$. These are prior results, not contributions of this package.
- Corollary 4.4 and Conjecture 4.6, printed pp. 260--261, use a different basis, $\binom{m-1}{k-1}$, with coefficients $b_{n,k}$. The computation through $n\le20$ preceding Conjecture 4.6 concerns log-concavity of those $b_{n,k}$, not the peak-location assertion about the $a_k$ considered here.

**Colin Defant.** *Short Proofs in Algebraic and Enumerative Combinatorics.* [arXiv:2605.19979v3](https://arxiv.org/abs/2605.19979v3), version dated 2026-05-25.

- Section 4, Theorems 4.3 and 4.7, prove the entry-bound and evacuation assertions of Sagan--Wilson, respectively. They correspond to preprint Conjectures 6.1 and 6.5, or published Conjectures 7.1 and 7.5.
- Those results are excluded from the new claim here. This package does not claim to re-solve them.

## Relation to Kronecker coefficients

**Nate Harman and Alexander N. Wilson.** *Kronecker Coefficients, Crystals, and Bitableaux.* [arXiv:2507.14026v1](https://arxiv.org/abs/2507.14026v1), submitted 2025-07-18.

The introduction and Conjecture 1 set out the commuting-crystal program; Theorem 2 gives a positive expansion in the monomial basis. This source explains the surrounding research motivation. The present peak-location counterexample does not provide a general positive combinatorial rule for Kronecker coefficients or settle that broader problem.

## Scope of the prior-report search

The 2026-10-22 check covered the primary versions above, the authors' [Wilson research page](https://alexandernwilson.com/research.html) and [Sagan paper list](https://users.math.msu.edu/users/bsagan/Papers/Old/1list.html), and the public [Sagan--Wilson code repository](https://github.com/wilsoa/Centralizers-in-the-Plactic-Monoid). Targeted web searches combined the paper titles, conjecture identifiers 6.3(d) and 7.3(d), the integers 75095, 88704, and 4861, and terms such as counterexample, correction, and erratum. The cited code repository and its issue search were also inspected.

No earlier public report of this particular peak-location counterexample was found in that search. This is a bounded search statement, not proof of first discovery: unindexed material, private knowledge, and sources outside the search scope may exist. No author endorsement or external referee approval is asserted.
