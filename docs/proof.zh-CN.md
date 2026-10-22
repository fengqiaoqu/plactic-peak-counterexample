# Sagan–Wilson 峰位猜想的 $n=10$ 反例

本文证明 Sagan–Wilson《Centralizers in the plactic monoid》中的一个具体断言为假：其计数多项式在二项式基下的系数，不总是在 $k=\lceil n/2\rceil$ 取得最大值。反例是

$$
n=10,\qquad a_5=75095<88704=a_6.
$$

这是对该峰位断言的否定结果。本文不主张首次发现，也不声称解决系数对数凹性或一般 Kronecker 正组合规则问题；本材料尚未经过外部同行审阅。

## 1. 原问题和记号

直接核查的来源是 Bruce E. Sagan 与 Alexander N. Wilson 的 [arXiv:2410.20460v1](https://arxiv.org/abs/2410.20460v1)，§6，Conjecture 6.3(d)。论文发表于 *Semigroup Forum* 110(3), 724–744 (2025)；正式版对应 [Conjecture 7.3(d)](https://users.math.msu.edu/users/bsagan/Papers/Old/cpm-pub.pdf#page=19)。

令 $[m]=\{1,\ldots,m\}$。对词 $w$，记 $P(w)$ 为通常 RSK 行插入算法的插入表。两个词 Knuth 等价，当且仅当它们的插入表相同，记作

$$
v\equiv w\quad\Longleftrightarrow\quad P(v)=P(w).
$$

词关于这一等价关系取商，得到 plactic monoid。定义

$$
C(1)=\{w:1w\equiv w1\},\qquad
c_{n,m}(1)=\#\{w\in[m]^n:1w\equiv w1\}.
$$

固定 $n$，将关于 $m$ 的计数多项式写成

$$
c_{n,m}(1)=\sum_{k=0}^{n-1}a_k\binom{m}{k}.
\tag{1}
$$

原猜想的 (d) 断言：$a_1,\ldots,a_{n-1}$ 在 $k=\lceil n/2\rceil$ 取得最大值。这里的基底明确为 $\binom{m}{k}$；换成其他二项式基会改变系数，不能混用。

## 2. 一个精确计数式

分拆 $\lambda=(\lambda_1,\lambda_2,\ldots)\vdash n$ 用来描述大小为 $n$ 的 Young 图。标准 Young 表使用 $1,\ldots,n$ 各一次，行和列均严格递增；半标准 Young 表允许重复，行弱增、列严增。记

$$
f^\lambda=\#\operatorname{SYT}(\lambda),\qquad
\widehat\lambda=(\lambda_2,\lambda_3,\ldots),
$$

并令 $N(\eta,q)$ 表示形状 $\eta$、字母在 $[q]$ 中的半标准表数。约定 $N(\varnothing,q)=1$；当 $q=0$ 且 $\eta\ne\varnothing$ 时，$N(\eta,0)=0$。

Sagan–Wilson 已证明的单字母 centralizer 判据（arXiv v1，Theorem 3.2 和 Corollary 3.3）说明：

$$
w\in C(1)
\quad\Longleftrightarrow\quad
P(w)\text{ 每一列含有 }1
\quad\Longleftrightarrow\quad
P(w)\text{ 的首行全部为 }1.
\tag{2}
$$

最后一个等价来自列严增：字母 $1$ 只能位于其所在列的最上方。

**引理。** 对每个 $n\ge1$ 和 $m\ge1$，

$$
c_{n,m}(1)=\sum_{\lambda\vdash n}
f^\lambda N(\widehat\lambda,m-1).
\tag{3}
$$

**证明。** 固定插入表的形状 $\lambda$。根据 (2)，合法插入表的首行必须全部为 $1$。删去首行，并把剩余的数值都减去 $1$，得到形状 $\widehat\lambda$、字母在 $[m-1]$ 中的半标准表。

反过来，将任意这样的半标准表各项加 $1$，再放回长度为 $\lambda_1$ 的全 $1$ 首行，就得到合法插入表。剩余各项原值均至少为 $2$，因此补回首行自动满足列严增，不增加其他限制。这两个操作互逆。

RSK 将词双射到一对同形状的表：半标准插入表 $P$ 和标准记录表 $Q$。每张合法的 $P$ 恰配有 $f^\lambda$ 张 $Q$。对所有形状求和，即得 (3)。证毕。

这个双射直接证明 (3) 对全部正整数 $m$ 成立。尽管原论文的某些多项式陈述采用 $m\ge n$，这里无需将低 $m$ 的计数当作未经证明的外推。

## 3. 为什么十个精确值足够

对格子 $x=(i,j)$，其钩长为同一行右侧格数、同一列下方格数再加 $1$，记为 $h_\eta(i,j)$。钩长公式和钩内容公式给出

$$
f^\lambda=\frac{n!}{\prod_{x\in\lambda}h_\lambda(x)},
\qquad
N(\eta,m-1)=
\prod_{(i,j)\in\eta}
\frac{m-1+j-i}{h_\eta(i,j)}.
\tag{4}
$$

右式是关于 $m$ 的有理系数多项式，次数为 $|\eta|$。因此在 $n=10$ 时，(3) 是次数至多 $9$ 的显式多项式。

实际上次数恰为 $9$：只有 $\lambda=(1^{10})$ 的 $\widehat\lambda$ 有 $9$ 格，该项是

$$
f^{(1^{10})}N((1^9),m-1)=\binom{m-1}{9},
$$

其最高次系数为 $1/9!$；其余项次数均至多 $8$。

设用 (3)–(4) 得到的多项式为 $F(m)$。若另一个次数至多 $9$ 的多项式 $Q(m)$ 在十个不同点与 $F(m)$ 相同，则 $F-Q$ 有十个根，因而恒为零。这是下文十点证书的逻辑依据；它不依赖对任意 $n$ 的数值归纳。

## 4. $n=10$ 的逐项证书

$10$ 恰有 $42$ 个分拆。[n10_tableau_certificate.csv](../data/n10_tableau_certificate.csv) 为每个分拆列出 $f^\lambda$，以及 $q=0,\ldots,9$ 时的 $N(\widehat\lambda,q)$。逐列按 (3) 加权求和，得到：

| $m$ | $c_{10,m}(1)$ |
|---:|---:|
| 1 | 1 |
| 2 | 252 |
| 3 | 5670 |
| 4 | 50820 |
| 5 | 275010 |
| 6 | 1086090 |
| 7 | 3456369 |
| 8 | 9398925 |
| 9 | 22677445 |
| 10 | 49807595 |

定义

$$
\begin{aligned}
Q(m)={}&\binom m1+250\binom m2+4917\binom m3
+29648\binom m4\\
&+75095\binom m5+88704\binom m6
+43414\binom m7+4861\binom m8+\binom m9.
\end{aligned}
\tag{5}
$$

将 $m=1,\ldots,10$ 代入 (5)，恰好逐项得到上表。$F,Q$ 的次数均至多 $9$，所以根据第 3 节，

$$
c_{10,m}(1)=Q(m)
$$

是多项式恒等式。二项式多项式 $\binom m0,\ldots,\binom m9$ 构成次数至多 $9$ 的多项式空间的一组基，因此 (1) 的系数唯一，且

$$
(a_0,\ldots,a_9)
=(0,1,250,4917,29648,75095,88704,43414,4861,1).
\tag{6}
$$

于是

$$
a_6-a_5=88704-75095=13609>0.
$$

猜想要求 $k=\lceil10/2\rceil=5$ 处取得最大值，而 $a_6>a_5$。因此 Conjecture 6.3(d)，即正式发表版的 Conjecture 7.3(d)，为假。**证毕。**

完整向量还说明该例的唯一最大值位于 $k=6$；但仅 $a_6>a_5$ 就已足以反驳猜想。

## 5. 独立计算如何核对有限算术

证明的依据是上述双射、次数界和精确证书。程序用于复核有限算术，三条路线分别为：

1. **钩公式。** [coefficients.py](../scripts/coefficients.py) 使用 (3)–(4) 和精确有理数，生成二项式基系数。
2. **分支递推。** [verify_counterexample.py](../scripts/verify_counterexample.py) 以删角递推标准表数，以水平条分支递推半标准表数，不使用钩长或钩内容公式。所得 $42$ 行证书及十个加权计数与第 4 节一致。
3. **直接枚举及行列式。** [independent_tableau_check.py](../scripts/independent_tableau_check.py) 枚举 $n=10$、字母不超过 $6$ 的全部 **239,316 张半标准表**，不预先用“首行全为 $1$”筛选。对每张表的标准 row word $w$，直接比较 $P(1w)$ 与 $P(w1)$，再乘同形标准记录表数，得到相同的 $c_{10,m}(1)$，$1\le m\le6$。这枚举的是插入表，而非全部词。该程序另外使用 Jacobi–Trudi 公式及标准表数的行列式，在 $m=10,\ldots,19$ 上精确求解二项式基系数，重新得到 (6)。

第三条路线中按记录表数加权是合法的：若 $w\equiv w'$，则由 Knuth 等价关于词连接的相容性，有 $1w\equiv1w'$、$w1\equiv w'1$，所以是否属于 $C(1)$ 只取决于插入表。

在仓库根目录运行

```sh
python reproduce.py
```

即可运行全部核验。程序仅使用 Python 标准库；默认在临时目录重新计算，再与已保存的 [coefficients.json](../data/coefficients.json)、[counterexample_verification.json](../data/counterexample_verification.json) 和 [independent_tableau_check.json](../data/independent_tableau_check.json) 基线比较。需要保留本次输出时，可运行 `python reproduce.py --output-dir artifacts`。

## 6. 成果范围与归属

原猜想及单字母 centralizer 判据来自 Sagan–Wilson 的论文。本仓库提供的是一个固定 $n=10$ 的反例及其证明和复现材料。

本反例只否定峰位断言 (d)，没有否定同组猜想中的正性、整性或对数凹性，也没有解决一般 Kronecker 系数的正组合规则问题。

公开检索未确认这一反例的优先权；不能由“未找到已有报告”推断首次发现。本材料使用了 Codex 辅助探索、写作与编码，并由不同 AI 子代理交叉核验；这些过程不等同于外部同行审阅。
