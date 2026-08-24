---
confidence: 1.0
goal_id: G5.1
goal_kind: subgoal
id: "goal:g5.1"
origin: goals-doc
parents:
  - goal:g5
seeds: []
status: horizon
tags:
  - goal
  - subgoal
title: "G5.1: A goal too saturated with intent gets broken up"
type: goal
---

**The failure this exists to catch is visible right now in this file.** Goals
accumulate intent: each session adds a clause, a falsifier, a dependency, a
recorded result, until a "goal" is really five goals sharing a heading. A
saturated goal cannot be finished, so it stays `active` forever, which is half
of why the rotation count reads 37 against a declared limit of 3. **G6.6 is the
worked example** — its verdict came back `disproved` specifically because it
bundled a coverage claim and a remedy claim that resolved in opposite
directions, and nobody noticed until an experiment forced the split.

What has to exist: **an error metric the engine computes per goal**, and a
mechanical decomposition when a goal fails it. Candidate signals, all cheap and
already derivable from the corpus:

- **Falsifier count.** More than one falsifier in a goal means more than one
  claim. This is the strongest signal and the easiest to compute.
- **Verdict split.** A goal whose descendant verdicts disagree — some
  supporting, some contradicting — is answering more than one question. G6.6
  exactly.
- **Age at `active`** with no descendant reaching an mvp. Intent accumulating
  without ever closing.
- **Length**, as a weak proxy for the others. Weak on purpose: a long goal that
  passes the first three signals is fine, and length alone would flag the good
  ones.

Decomposition should be **generated and then reviewed**, never automatic —
`snapshot-goals.py` already derives `nodes/goal/` from this file, so a proposed
split is a diff against `GOALS.md` a human accepts or rejects. Splitting a goal
by machine without review would break the one rule this file has that cannot
bend: **ids are permanent**, so a bad split is unrecoverable in the way a bad
node never is.

**The framing that decides how this is built:** with agents at their current
capability, *it is never an agent failure, always a harness failure*. An agent
that cannot finish a saturated goal is behaving correctly — the goal is
unfinishable. So this metric measures the goal, never the agent that worked it,
and its output is a proposed split rather than a performance signal. Any
version of this that scores agents is the wrong build.

Falsifier: run the metric over this file as it stands. It must flag **G6.6**
(known bundled, proved so by verdict) and must not flag **G3.1** or **S9**
(single claim, single falsifier, closed cleanly). If it cannot separate those,
the signal is length in disguise.
