# Plactic centralizer 峰位猜想的反例：$n=10$

本仓库给出 Sagan–Wilson《Centralizers in the plactic monoid》中峰位猜想的一个精确反例。猜想编号为 [arXiv v1 的 Conjecture 6.3(d)](https://arxiv.org/abs/2410.20460v1)，正式发表版对应 [Conjecture 7.3(d)](https://users.math.msu.edu/users/bsagan/Papers/Old/cpm-pub.pdf#page=19)。

**当 $n=10$ 时，猜想指定的第 $5$ 项并非最大项：**

$$
a_5=75095<88704=a_6.
$$

这里的 $a_k$ 是计数多项式在 $\binom{m}{k}$ 基下的系数。完整向量是

$$
(a_0,\ldots,a_9)
=(0,1,250,4917,29648,75095,88704,43414,4861,1).
$$

该反例否定的是上述猜想的 **(d) 峰位断言**。它没有否定系数的对数凹性，也没有解决一般 Kronecker 系数的正组合规则问题。优先权尚未确认；本材料尚未经过外部同行审阅。

## 这个问题在数什么

把正整数排成一个词，用 RSK 行插入算法得到一张 Young 表。两个词得到同一张插入表，就称它们 Knuth 等价；按这种等价关系合并词，便得到 plactic monoid。

考察在词的前面或后面加一个 $1$，插入表仍相同的词：

$$
C(1)=\{w:1w\equiv w1\},\qquad
c_{n,m}(1)=\#\{w\in[m]^n:1w\equiv w1\}.
$$

对固定的 $n$，这个计数是关于字母上界 $m$ 的多项式。原猜想将它写成

$$
c_{n,m}(1)=\sum_{k=0}^{n-1}a_k\binom{m}{k},
$$

并预测 $a_1,\ldots,a_{n-1}$ 在 $k=\lceil n/2\rceil$ 取得最大值。$n=10$ 的反例由此只需证明 $a_6>a_5$。

## 证明与核验

[中文完整证明](docs/proof.zh-CN.md) 从已发表的 centralizer 判据和 RSK 双射推导精确计数式，再利用次数上界与十个精确取值确定多项式。全部 $42$ 个分拆的逐项数据保存在 [计数证书](data/n10_tableau_certificate.csv) 中。

三套程序分别使用钩公式、删角与水平条递推，以及直接半标准表枚举与行列式计算。直接枚举覆盖 $n=10$、字母不超过 $6$ 的 **239,316 张半标准表**，对每张表检验插入关系，并按同形标准记录表数加权。这里枚举的是表，而非全部 $6^{10}$ 个词。

也可阅读 [English summary](docs/summary.en.md)。

## 复现

需要 Python 3.10 或更新版本；程序仅使用 Python 标准库。

1. 下载或克隆本仓库。
2. 在仓库根目录打开终端，运行：

   ```sh
   python reproduce.py
   ```

3. 查看运行输出，并核对 `data/` 中的精确系数、计数证书和独立核验记录。

默认运行使用临时目录，不改动 `data/` 中的基线。保留本次输出可运行 `python reproduce.py --output-dir artifacts`；完整复算已保存的 n=2 至 32 扫描可运行 `python reproduce.py --max-n 32`。仓库文件的校验值列于 [SHA256SUMS](SHA256SUMS)。

## 文件结构

```text
README.md
reproduce.py
docs/
  proof.zh-CN.md                 中文完整证明
  summary.en.md                 英文摘要
scripts/
  coefficients.py               钩长、钩内容公式路线
  verify_counterexample.py      删角、水平条递推路线
  independent_tableau_check.py  直接表枚举、行列式路线
data/
  n10_tableau_certificate.csv    42 个分拆的逐项证书
  coefficients.json
  counterexample_verification.json
  independent_tableau_check.json
```

## 归属与 AI 使用说明

原问题、记号和已有判据归属于 Sagan–Wilson 的论文；本仓库的具体内容是 $n=10$ 的反例及可检查的证明和计算材料。定向公开检索尚未确认是否已有相同反例，因而本仓库不主张首次发现。

维护者使用 Codex 辅助探索、整理文稿和编写代码，不同 AI 子代理参与独立核验。这些核验不等同于外部同行审阅。读者可以从完整证明和逐项证书检查结论，也可运行 `python reproduce.py` 重新计算。

原始文献与后续状态见 [references.md](references.md)，BibTeX 见 [references.bib](references.bib)。AI 使用及材料声明见 [NOTICE.md](NOTICE.md)，引用本仓库的方法见 [CITATION.md](CITATION.md)。本次发布尚未指定新材料的开放许可证。
