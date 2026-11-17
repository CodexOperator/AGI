---
id: doc:draft-paper-v0
mint_id: abc168ad2e814a0887d49794f678c79f
type: doc
parents:
  - goal:g5.4.3.2
next_edges: []
edited_by: meme-master
season: 3
tags:
  - draft
title: "DRAFT class paper v0.1 -- graph copy of the private draft, for thought-master's team and council (goal:g5.4.3.2)"
town: core
---
# DRAFT — class paper v0.1, graph copy

DRAFT. Every sentence is an agent's draft (meme-master, 11-17) for the owner to rewrite in his own words; the two lines marked '% OWNER' are the owner's. It is a MATH-class paper: the owner's rubric scores 15 each for topic depth, clarity (organization, grammar, notation), development (background, examples), support (definitions, theorems, examples), problem-solving process (definitions and theorems used correctly, logic), big picture; 5 for the abstract, 5 for the conclusion (total 100).

source sha256: ec794f9085bfc558182349013727b8795d3d98697ad5700475fa5e39b64835a0
copied: 2026-11-17T06:47:30Z
'% OWNER' lines: 2
removals: [elided: person] x1 line (author)
submitted bytes: none yet; the owner's final is his own rewrite, never this copy
numbers: measured by graphstats.py (below) at commit d7985199d4, 2026-11-17

## paper.tex (copy)
````latex
% DRAFT v0.1 (meme-master, 2026-11-17). Every sentence here is a DRAFT for the owner to rewrite in his own words.
% Numbers marked [measured 11-17] were read from the live graph by graphstats.py at commit d7985199d4.
% [TM: ...] = thought-master data still to come.
\documentclass[11pt]{article}
\usepackage[margin=1in]{geometry}
\usepackage{amsmath,amssymb,amsthm}
\usepackage{booktabs}
\usepackage{hyperref}
\usepackage{xcolor}
\usepackage{tikz}
\usetikzlibrary{arrows.meta,positioning}

\newtheorem{theorem}{Theorem}
\newtheorem{proposition}[theorem]{Proposition}
\newtheorem{lemma}[theorem]{Lemma}
\newtheorem{corollary}[theorem]{Corollary}
\theoremstyle{definition}
\newtheorem{definition}{Definition}
\newtheorem{example}{Example}
\theoremstyle{remark}
\newtheorem{remark}{Remark}

\newcommand{\TM}[1]{\textcolor{orange}{[TM: #1]}}
\newcommand{\draftnote}[1]{\textcolor{gray}{\emph{[#1]}}}

\title{Context Management for Many AI Agents:\\ The Mathematics of a Thoughtgraph\\[4pt]
\large\textcolor{red}{DRAFT for rewriting --- not the author's final words}}
\author{[elided: person]}
\date{November 2026}

\begin{document}
\maketitle

\begin{abstract}
Large language model (LLM) agents can now write and change software, but two limits appear as soon as
several of them work together: each agent sees only a bounded \emph{context window}, and the agents must
coordinate without overwriting one another. This paper models a working system that addresses both
limits, a \emph{thoughtgraph}, as a typed directed acyclic graph whose nodes are goals, ideas,
hypotheses, experiments and verdicts. We prove four results that justify its design: a tree of $n$
agents needs only $n-1$ communication channels instead of $\binom{n}{2}$; a well-formed graph always
admits a parents-first processing order; independent per-step errors compound geometrically, which
fixes how long an unchecked chain of work may be; and majority voting over three independent versions
improves reliability exactly when each version is right more than half the time. We then measure the
live graph (5{,}889 nodes, longest chain 20, mean ancestor set 9.4 nodes) and show that an agent reading
only a node's ancestors reads about $1/600$ of the graph. Finally we state a sign test that decides,
in advance, what would count as evidence that the graph treatment improved a piece of work.
\end{abstract}

\section{Introduction}
\draftnote{Owner's hook, verbatim from the talk:} \textbf{``Can you prove to me you achieved anything?''} % OWNER c:2763ec818294

A progress bar that crosses 80\% looks like an achievement until someone asks three questions: who
wrote the formula, what measured the quantity, and who checks the instrument. The same questions apply
to AI agents. A single agent can report that a task is done; a team of agents can report it many times
over, and the reports can contradict each other.

This project began as an attempt to answer those questions with structure rather than trust. Every unit
of thinking an agent does is written down as a node in a graph, linked to the reason it exists (its
parents), and closed by a verdict that can be checked. The graph is version-controlled, so every change
is recorded. The question this paper asks is mathematical: \emph{what properties does such a structure
have, and which of them actually explain why it helps?}

\paragraph{Outline.} Section~\ref{sec:background} gives the background on context windows and
multi-agent failures. Section~\ref{sec:defs} defines the thoughtgraph formally. Section~\ref{sec:results}
proves the main results. Section~\ref{sec:data} measures the live graph. Section~\ref{sec:measure}
states the test that decides whether the approach improved real work. Section~\ref{sec:conclusion}
concludes.

\section{Background}\label{sec:background}
\subsection{The context window}
An LLM reads a bounded sequence of tokens, its \emph{context window}, and nothing else. Even within
that bound, use is uneven: Liu et al.\ found that GPT-3.5-Turbo answered 56.1\% of questions correctly
with no documents at all, but only 53.8\% when the one relevant document sat in the middle of
twenty~\cite{liu2023lost}. Hong et al.\ report the same degradation across eighteen models as input
grows~\cite{hong2025rot}. More context is therefore not free: what an agent is shown must be chosen.

\subsection{Long tasks and compounding errors}
Kwa et al.\ measure the length of task an agent completes half the time, and find it doubling about
every seven months, near fifty minutes for one 2025 model~\cite{kwa2025metr}. Sinha et al.\ show that
when a plan is supplied, long-task failures are mostly execution slips that accumulate step by
step~\cite{sinha2026illusion}. Section~\ref{sec:compound} turns this into a formula.

\subsection{Many agents}
Cemri et al.\ classify failures of multi-agent LLM systems and find that a large share come from
specification and system design rather than from the models themselves~\cite{cemri2025mast}.
The human version of this problem is old: Brooks observed that adding people to a late software project
makes it later, partly because communication paths multiply~\cite{brooks1975}. Section~\ref{sec:channels}
makes that count precise.

\subsection{Redundancy}
Repeating work on purpose can raise reliability. Sampling several answers and voting improves reasoning
accuracy~\cite{wang2023sc}; sampling 250 attempts instead of one raised the share of solved software
issues from 15.9\% to 56\%, provided a test can recognise the right one~\cite{brown2024monkeys}.
But Knight and Leveson showed in 1986 that independently written program versions fail together far more
often than independence predicts~\cite{knight1986}, and Ron et al.\ see the same with coding agents:
three-version voting cut mean failures from 387.44 to 130.99, with residual failures concentrated on
ambiguous parts of the specification~\cite{ron2026nversion}. Sections~\ref{sec:vote}
and~\ref{sec:bestofk} explain both effects with one model.

\section{Definitions}\label{sec:defs}

\begin{definition}[Node types]
Let
\[T = \{\textsf{moral}, \textsf{vision}, \textsf{goal}, \textsf{idea}, \textsf{hypothesis},
\textsf{experiment}, \textsf{verdict}, \textsf{mvp}, \textsf{outcome}\}\]
be the \emph{chain types},
totally ordered in the order listed. (The live system has a few further types, such as \textsf{doc} and
\textsf{build}, which we set aside.)
\end{definition}

\begin{definition}[Thoughtgraph]
A \emph{thoughtgraph} is a triple $G=(V,E,\tau)$ where $V$ is a finite set of nodes,
$E \subseteq V\times V$ is a set of directed edges, and $\tau : V \to T$ assigns each node a type.
An edge $(u,v)\in E$ means \emph{$u$ is a parent of $v$}: $v$ exists because of $u$.
For $v\in V$ write $P(v)=\{u : (u,v)\in E\}$ for its parents.
\end{definition}

\begin{definition}[Well-formed]\label{def:wf}
$G$ is \emph{well-formed} if
\begin{enumerate}
  \item[(W1)] $G$ has no directed cycle;
  \item[(W2)] $P(v)=\varnothing$ if and only if $\tau(v)=\textsf{moral}$ (only morals are parentless);
  \item[(W3)] every edge respects the order of types: $(u,v)\in E \Rightarrow \tau(u)\le\tau(v)$.
\end{enumerate}
\end{definition}

\begin{definition}[Ancestors and depth]
The \emph{ancestor set} $A(v)$ is the set of nodes from which there is a directed path to $v$.
The \emph{depth} $d(v)$ is the number of edges on the longest directed path ending at $v$.
\end{definition}

\begin{definition}[Context budget]
An agent with context budget $C$ (in tokens) may read a set $S\subseteq V$ only if
$\sum_{u\in S} s(u)\le C$, where $s(u)$ is the size of node $u$ in tokens.
\end{definition}

\begin{example}
This paper is itself a path in a thoughtgraph:
$\textsf{goal:g5.4} \to \textsf{goal:g5.4.3} \to \textsf{goal:g5.4.3.2}$, the last being ``the class
paper after the presentation''. An agent asked to draft it reads exactly the ancestors of
\textsf{goal:g5.4.3.2}, not the rest of the graph.
\end{example}

\begin{figure}[h]\centering
\begin{tikzpicture}[node distance=7mm and 4mm, every node/.style={draw, rounded corners, font=\small, inner sep=3pt}, >=Stealth]
\node (m) {moral};
\node[right=of m] (vi) {vision};
\node[right=of vi] (g) {goal};
\node[right=of g] (i) {idea};
\node[right=of i] (h) {hypothesis};
\node[below=of h] (e) {experiment};
\node[left=of e] (ve) {verdict};
\node[left=of ve] (mv) {mvp};
\node[left=of mv] (o) {outcome};
\draw[->] (m)--(vi); \draw[->] (vi)--(g); \draw[->] (g)--(i); \draw[->] (i)--(h);
\draw[->] (h)--(e); \draw[->] (e)--(ve); \draw[->] (ve)--(mv); \draw[->] (mv)--(o);
\end{tikzpicture}
\caption{The chain of types. Every arrow points from parent to child. Only morals have no parent;
the owner writes them, agents never do.}
\end{figure}

\section{Results}\label{sec:results}

\subsection{Communication channels}\label{sec:channels}
\begin{theorem}\label{thm:channels}
Among $n$ agents, letting every pair communicate directly requires $\binom{n}{2}=\frac{n(n-1)}{2}$
channels, while the fewest channels that still connect all $n$ agents is $n-1$, achieved exactly by
trees.
\end{theorem}
\begin{proof}
The complete graph $K_n$ has one edge per unordered pair, hence $\binom{n}{2}$ edges.
For the lower bound, we show by induction on $n$ that a connected graph on $n$ vertices has at least
$n-1$ edges. For $n=1$ this is trivial. Suppose it holds for fewer than $n$ vertices and let $H$ be
connected on $n\ge 2$ vertices. If $H$ has a vertex of degree~1, delete it and its edge: the rest is
connected on $n-1$ vertices, so has at least $n-2$ edges, and $H$ has at least $n-1$. Otherwise every
vertex has degree at least~2 (degree~0 is impossible in a connected graph with $n\ge2$), so
$2|E|=\sum \deg \ge 2n$ and $|E|\ge n>n-1$. A tree on $n$ vertices has exactly $n-1$ edges (the same
induction, removing a leaf), so the bound is attained.
\end{proof}

\begin{example}
$n=5$ gives $10$ channels against $4$; $n=10$ gives $45$ against $9$; $n=50$ gives $1{,}225$ against
$49$. The project runs about twenty agent posts arranged in a hierarchy
(prime $\to$ masters $\to$ directors $\to$ workers): $190$ possible pairs, but $19$ channels in the tree.
\end{example}

\begin{remark}
A tree is fragile: removing one internal node disconnects it. The project adds a few cross-links on
purpose (a three-member council, a mail system), trading a handful of extra channels for robustness.
\end{remark}

\subsection{A parents-first order always exists}
\begin{theorem}\label{thm:topo}
A finite directed graph has an ordering $v_1,\dots,v_n$ of its vertices with every edge going forward
($(v_i,v_j)\in E\Rightarrow i<j$) if and only if it has no directed cycle.
\end{theorem}
\begin{proof}
($\Rightarrow$) A cycle $v_{i_1}\to\cdots\to v_{i_k}\to v_{i_1}$ would need $i_1<i_2<\cdots<i_k<i_1$.
($\Leftarrow$) First, a finite acyclic graph has a vertex with no incoming edge: otherwise, walking
backwards along incoming edges from any vertex never stops, and after more than $n$ steps some vertex
repeats, giving a cycle. Put such a vertex first, delete it, and repeat; deleting vertices cannot create
a cycle, so the process continues until every vertex is placed, and each edge goes from an earlier
vertex to a later one.
\end{proof}

\begin{corollary}
In a well-formed thoughtgraph every node can be processed after all of its parents. In particular a
verdict is never asked to judge an experiment that has not been written yet.
\end{corollary}

\begin{remark}
The proof of Theorem~\ref{thm:topo} is an algorithm (Kahn's algorithm); if it stops early, the vertices
left over contain a cycle. Section~\ref{sec:data} reports that the live graph contains exactly one.
\end{remark}

\subsection{Errors compound}\label{sec:compound}
\begin{proposition}\label{prop:compound}
If each step of a task succeeds independently with probability $p$, a chain of $k$ steps succeeds with
probability $p^k$, and it succeeds at least half the time if and only if
\[
k \;\le\; k_{1/2}(p) \;=\; \frac{\ln(1/2)}{\ln p}.
\]
\end{proposition}
\begin{proof}
Independence gives $\Pr[\text{all }k\text{ succeed}]=p^k$. Since $0<p<1$, $\ln p<0$, so
$p^k\ge \tfrac12 \iff k\ln p\ge \ln\tfrac12 \iff k\le \ln\tfrac12/\ln p$.
\end{proof}

\begin{example}
$p=0.99$ gives $k_{1/2}\approx 69$ steps; $p=0.95$ gives about $13.5$; $p=0.90$ about $6.6$.
A model that is only slightly less reliable per step can only be trusted with a far shorter chain.
\end{example}

\begin{proposition}[Checkpoints]\label{prop:checkpoint}
Split a $k$-step task into $m$ segments of $k/m$ steps, each followed by a check that detects any failure
in its segment and allows the segment to be retried up to $r$ times. The segment succeeds with probability
$1-(1-p^{k/m})^{r+1}$, and the whole task with probability
\[
\Bigl(1-\bigl(1-p^{k/m}\bigr)^{r+1}\Bigr)^{m}.
\]
\end{proposition}
\begin{proof}
A segment fails only if all $r+1$ independent attempts fail, each with probability $1-p^{k/m}$.
Segments are independent, so their success probabilities multiply.
\end{proof}

\begin{example}
Take $p=0.95$ and $k=60$. Unchecked: $0.95^{60}\approx 0.046$. Split into $m=6$ segments of 10 steps
($p^{10}\approx0.599$) with one retry each ($r=1$): each segment succeeds with probability
$1-0.401^2\approx 0.839$, and the task with $0.839^6\approx 0.35$, about eight times better. In the
thoughtgraph the check is the \emph{verdict} node, and the segment is a hypothesis with its experiments.
This is the mathematical reason for the ``convoluted'' path: weaker or local models have smaller $p$, so
they need shorter segments.
\end{example}

\subsection{Majority voting}\label{sec:vote}
\begin{theorem}\label{thm:vote}
Three versions are built independently, each correct with probability $p$. The majority is correct with
probability $q(p)=p^3+3p^2(1-p)$, and
\[
q(p)-p \;=\; p(1-p)(2p-1).
\]
Hence voting helps when $p>\tfrac12$, hurts when $p<\tfrac12$, and changes nothing at $p\in\{0,\tfrac12,1\}$.
\end{theorem}
\begin{proof}
The majority is right when all three are right ($p^3$) or exactly two are ($\binom32p^2(1-p)$). Then
$q(p)-p=3p^2-2p^3-p=-p(2p^2-3p+1)=-p(2p-1)(p-1)=p(1-p)(2p-1)$, whose sign is the sign of $2p-1$
for $0<p<1$.
\end{proof}

\begin{example}
$p=0.8$ gives $q=0.896$: the failure rate falls from $20\%$ to $10.4\%$.
\end{example}

\begin{remark}[When independence fails]
If the three versions share a misreading of the specification, they fail together and the vote cannot
correct them. In the extreme where failures always coincide, $q(p)=p$. Knight and Leveson's experiment
and Ron et al.'s agent study both land between the extremes: real gains, smaller than independence
predicts~\cite{knight1986,ron2026nversion}. This is why the thoughtgraph puts the \emph{hypothesis},
the shared specification, under review before any version is built.
\end{remark}

\subsection{Best of $k$ with a checker}\label{sec:bestofk}
\begin{proposition}\label{prop:bestofk}
Suppose a problem $i$ is solved by one attempt with probability $p_i$, attempts are independent given
the problem, and a perfect checker recognises a correct attempt. Over a set of problems with $p_i$ drawn
from a distribution $\mu$, the fraction solved by the best of $k$ attempts is
\[
c(k)=\mathbb{E}_{p\sim\mu}\bigl[1-(1-p)^k\bigr],\qquad
\lim_{k\to\infty}c(k)=\mu\bigl(\{p>0\}\bigr).
\]
\end{proposition}
\begin{proof}
For one problem the chance that all $k$ attempts fail is $(1-p_i)^k$; averaging over problems gives
$c(k)$. For each fixed $p$, $1-(1-p)^k$ increases to $1$ if $p>0$ and stays $0$ if $p=0$; it is bounded
by $1$, so by monotone convergence $c(k)\to\mu(\{p>0\})$.
\end{proof}

\begin{example}
If all problems were alike with $p=0.159$, then $c(250)=1-0.841^{250}\approx 1$. Brown et al.\ observed
$56\%$~\cite{brown2024monkeys}. The proposition explains the gap: problems differ, and some are never
solved ($p_i=0$) however often they are tried. Repetition raises coverage only up to the share of
problems the agents can solve at all. Past that point the remedy is a better decomposition, which is
what the graph supplies, not more samples.
\end{example}

\subsection{Reading ancestors instead of everything}
\begin{proposition}\label{prop:context}
If every node has size at most $s$ tokens, an agent working on $v$ that reads $A(v)\cup\{v\}$ needs at
most $s\,(|A(v)|+1)$ tokens, independent of $|V|$. If every node has at most one parent, then
$|A(v)|=d(v)$.
\end{proposition}
\begin{proof}
The first claim is a sum of at most $|A(v)|+1$ terms each at most $s$. With one parent per node, the
ancestors of $v$ are exactly the vertices on the unique path from its root to $v$, of which there are
$d(v)$.
\end{proof}

\section{Measuring the live graph}\label{sec:data}
The numbers below were read from the project's repository on 17 November 2026 \draftnote{measured
11-17 at commit d7985199d4; refresh before submission}.

\begin{table}[h]\centering
\begin{tabular}{lr}
\toprule
Quantity & Value\\
\midrule
Nodes (live / retired) & 5{,}889 / 255\\
Parent edges & 6{,}797\\
Commits since 30 April 2026 & 26{,}417\\
Live goals (complete / active / horizon / retired) & 284 / 247 / 224 / 60\\
Experiments / hypotheses / verdicts & 2{,}393 / 1{,}529 / 304\\
Nodes with 1 parent / 2 parents / 3 or more & 5{,}076 / 690 / 22\\
Longest chain $\max d(v)$ & 20\\
Mean depth $\bar d$ & 5.47\\
Ancestor set $|A(v)|$: mean / median / 95th pct / max & 9.38 / 9 / 16 / 41\\
\bottomrule
\end{tabular}
\caption{The live thoughtgraph.}
\end{table}

\paragraph{Context saving.} By Proposition~\ref{prop:context}, an agent reading a typical node's
ancestors reads about $9.4$ nodes instead of $5{,}889$, a factor of roughly $600$. Even the worst case,
41 ancestors, is under 1\% of the graph. Because 86\% of nodes have exactly one parent, the ancestor
set is close to the depth, as the proposition predicts for trees ($9.38$ against $5.47$; the difference
is the 12\% of nodes with two or more parents).

\paragraph{Shape.} Most nodes are leaves (3{,}683 of 5{,}889): the graph is wide and shallow, as
expected when each hypothesis spawns several experiments that end there. Internal nodes have
$2.9$ children on average.

\paragraph{Where the real graph is not well-formed.} Checking Definition~\ref{def:wf} against the data
is itself an exercise in the problem-solving process:
\begin{itemize}
  \item (W1) fails once: one hypothesis and one of its experiments list each other as parents. Kahn's
  algorithm (Theorem~\ref{thm:topo}) finds exactly this pair.
  \item (W2) fails for 95 older nodes that have no parent although they are not morals; they predate the
  rule. 66 parent references point to nodes that no longer exist.
  \item These defects are small (under 2\% of nodes) and are exactly the kind the verification step is
  meant to catch; the rule was introduced after they were written.
\end{itemize}

\TM{lands per day; the benchmark of small local models against the reference model; per-node token
sizes $s(u)$, which would turn the factor of 600 into a token count.}

\section{How we will know it helped}\label{sec:measure}
The presentation that accompanies this paper was produced twice: once directly (arm~A) and once through
the full graph treatment (arm~B). Reviewers score each slide blind to which arm produced it.

\begin{definition}[Sign test]
For the $n$ slides on which the two arms' scores differ, let $X$ be the number where arm~B scored higher.
Under the null hypothesis that the treatment makes no difference, $X\sim\mathrm{Binomial}(n,\tfrac12)$ and
\[
\Pr[X\ge x]=\frac{1}{2^n}\sum_{j=x}^{n}\binom{n}{j}.
\]
\end{definition}

\begin{example}
The deck has 13 labelled slides; the last reports this test and cannot be scored, leaving at most
$n=12$. Then $\Pr[X\ge10]=(66+12+1)/4096\approx0.019$, so ten or more wins for arm~B would be significant
at the 5\% level (one-sided). Ties carry no information and are left out, which shrinks $n$, and the test
has a floor: with $n\le5$ differing slides even a clean sweep has two-sided $p\ge 2/2^5=0.0625$, so it can
never pass, and for $6\le n\le 8$ only a clean sweep passes.
\end{example}

\TM{the measured result of the A/B, once the council's scorers return their sheets.}

\section{Conclusion}\label{sec:conclusion}
The thoughtgraph is a simple object, a typed acyclic graph, but its design choices follow from
elementary results. A hierarchy keeps communication linear in the number of agents
(Theorem~\ref{thm:channels}); acyclicity guarantees that work can be done parents first
(Theorem~\ref{thm:topo}); geometric error growth sets how long a chain may run between verdicts
(Propositions~\ref{prop:compound} and~\ref{prop:checkpoint}); and voting helps only when versions are
better than chance and fail independently, which is why the shared specification is reviewed first
(Theorem~\ref{thm:vote}). On the live graph, reading only a node's ancestors cuts what an agent must read
by a factor of about 600. Whether this structure produces \emph{better} work, and not only tidier work,
is a question the sign test of Section~\ref{sec:measure} will answer with data rather than with
confidence.

\draftnote{Owner's closing question from the talk:} \textbf{``How do we measure success?''} % OWNER (board, v1 slide 8)

\section*{A note on how this paper was made}
\draftnote{Draft by the agent meme-master from the graph and the presentation's research; the author
rewrites every sentence in his own words. Numbers measured by script; citations from the presentation's
evidence file, where each was checked against its source.}

\begin{thebibliography}{99}
\bibitem{brooks1975} F.~P.~Brooks Jr., \emph{The Mythical Man-Month}, Addison-Wesley, 1975.
\bibitem{brown2024monkeys} B.~Brown, J.~Juravsky, R.~Ehrlich, R.~Clark, Q.~V.~Le, C.~R\'e, A.~Mirhoseini,
``Large Language Monkeys: Scaling Inference Compute with Repeated Sampling,'' arXiv:2407.21787, 2024.
\bibitem{cemri2025mast} M.~Cemri et al., ``Why Do Multi-Agent LLM Systems Fail?'' arXiv:2503.13657, 2025.
\bibitem{hong2025rot} K.~Hong, A.~Troynikov, J.~Huber, ``Context Rot: How Increasing Input Tokens Impacts
LLM Performance,'' Chroma technical report, 2025.
\bibitem{knight1986} J.~C.~Knight, N.~G.~Leveson, ``An Experimental Evaluation of the Assumption of
Independence in Multiversion Programming,'' \emph{IEEE Trans.\ Software Engineering} 12(1):96--109, 1986.
\bibitem{kwa2025metr} T.~Kwa et al., ``Measuring AI Ability to Complete Long Software Tasks,''
arXiv:2503.14499, 2025.
\bibitem{liu2023lost} N.~F.~Liu, K.~Lin, J.~Hewitt, A.~Paranjape, M.~Bevilacqua, F.~Petroni, P.~Liang,
``Lost in the Middle: How Language Models Use Long Contexts,'' \emph{TACL}, 2023.
\bibitem{ron2026nversion} J.~Ron, B.~Baudry, M.~Monperrus, ``N-Version Programming with Coding Agents,''
arXiv:2606.20158, 2026.
\bibitem{sinha2026illusion} A.~Sinha, A.~Arun, S.~Goel, S.~Staab, J.~Geiping, ``The Illusion of
Diminishing Returns: Measuring Long Horizon Execution in LLMs,'' ICLR, 2026.
\bibitem{wang2023sc} X.~Wang et al., ``Self-Consistency Improves Chain of Thought Reasoning in Language
Models,'' ICLR, 2023.
\end{thebibliography}
\end{document}
````

## graphstats.py (the measurement behind the data table)
Run from the repo root: `python3 -I graphstats.py`.
````python
import os,re,collections,statistics,json
R='.agi/nodes'
nodes={};dep=0
for d,_,fs in os.walk(R):
    if '/.' in d: continue
    for f in fs:
        if not f.endswith('.md'): continue
        p=os.path.join(d,f); t=open(p,errors='ignore').read(4000)
        if not t.startswith('---'): continue
        fm=t.split('---',2)[1]
        m=re.search(r'^id:\s*(\S+)',fm,re.M)
        if not m: continue
        ps=re.findall(r'^\s+-\s+(\S+)',fm.split('parents:',1)[1].split('\n',1)[1]) if 'parents:' in fm and not re.search(r'parents:\s*\[\]',fm) else []
        # stop parents list at next key
        if 'parents:' in fm:
            blk=fm.split('parents:',1)[1]
            lines=blk.split('\n')[1:]; ps=[]
            for l in lines:
                mm=re.match(r'\s+-\s+(\S+)',l)
                if mm: ps.append(mm.group(1).strip('"\''))
                else: break
        st=re.search(r'^status:\s*(\S+)',fm,re.M)
        nodes[m.group(1)]={'type':m.group(1).split(':')[0],'parents':ps,'dep':'/deprecated/' in p,'status':st.group(1) if st else ''}
live={k:v for k,v in nodes.items() if not v['dep']}
print('total',len(nodes),'live',len(live),'deprecated',len(nodes)-len(live))
print('live by type',collections.Counter(v['type'] for v in live.values()).most_common())
E=sum(len(v['parents']) for v in nodes.values()); print('parent edges (all)',E)
pc=collections.Counter(len(v['parents']) for v in live.values()); print('live parent-count dist',sorted(pc.items()))
roots=[k for k,v in live.items() if not v['parents']]; print('live roots by type',collections.Counter(nodes[k]['type'] for k in roots))
dangling=sum(1 for v in nodes.values() for p in v['parents'] if p not in nodes); print('dangling parent refs',dangling)
# cycle check + depth from roots (longest path via memo)
import sys; sys.setrecursionlimit(100000)
memo={};state={}
cyc=[0]
def depth(k):
    if k in memo: return memo[k]
    if state.get(k)==1: cyc[0]+=1; return 0
    state[k]=1
    ps=[p for p in nodes.get(k,{'parents':[]})['parents'] if p in nodes]
    d=0 if not ps else 1+max(depth(p) for p in ps)
    state[k]=2; memo[k]=d; return d
ds=[depth(k) for k in live]; print('cycles hit',cyc[0],'max depth',max(ds),'mean depth',round(statistics.mean(ds),2))
print('depth dist',sorted(collections.Counter(ds).items())[:25])
ch=collections.Counter(p for v in live.values() for p in v['parents'])
vals=[ch.get(k,0) for k in live]; inner=[x for x in vals if x>0]
print('children per live node: mean',round(statistics.mean(vals),2),'leaves',vals.count(0),'internal mean',round(statistics.mean(inner),2),'max',max(vals))
print('goal status',collections.Counter(v['status'] for v in live.values() if v['type']=='goal'))
print('hyp/verdict', {t:sum(1 for v in nodes.values() if v['type']==t) for t in ['hypothesis','experiment','verdict','mvp','outcome','idea']})
amemo={}
def anc(k,seen=None):
    if k in amemo: return amemo[k]
    out=set(); stack=[p for p in nodes[k]['parents'] if p in nodes]
    while stack:
        x=stack.pop()
        if x in out: continue
        out.add(x); stack+= [p for p in nodes[x]['parents'] if p in nodes]
    amemo[k]=out; return out
A=[len(anc(k)) for k in live]
print('ancestor set: mean',round(statistics.mean(A),2),'median',statistics.median(A),'max',max(A),'p95',sorted(A)[int(.95*len(A))])
norm=lambda t:{'exp':'experiment','hyp':'hypothesis'}.get(t.strip('"'),t.strip('"'))
print('live by type (normalized)',collections.Counter(norm(v['type']) for v in live.values()).most_common())
cyc=[]
for k in nodes:
    if k in anc(k): cyc.append(k)
print('nodes on a cycle',cyc[:6])
print('non-moral live roots',sum(1 for k in roots if norm(nodes[k]['type'])!='moral'))
````

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
v0.1, meme-master 11-17: owner 06:5xZ "Use the graph route for it" + SM [decision] 06:4xZ (B): the private draft is copied here so thought-master's team and council can read it; author name elided, the two owner lines marked, nothing else changed.
<!-- THOUGHT:END -->
