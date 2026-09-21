---
id: goal:g6.6
mint_id: 26e39066f7bb494581c7b494d409d4fa
type: goal
parents:
  - goal:g6
confidence: 1.0
edited_by: season.py
goal_id: G6.6
goal_kind: subgoal
heading_level: 3
origin: goals-doc
season: 1
seeds:
  - exp:noncode-surface-census
status: horizon
tags:
  - goal
  - subgoal
thought_session: season
title: "G6.6: Level 3 covers the non-code surfaces too"
---
**A projection that omits half the engine cannot rebuild it.** `level3.py`'s
scope is deliberately narrow and says so in its own docstring:
`extensions/agi/src/**/*.py` plus `extensions/agi/bin/*.py`, about 70 files.
Everything else in `agi` is outside the graph entirely —

- `skills/agi/SKILL.md`, the document that tells every agent what this loop *is*
- `extensions/agi/lib/agent-prompt.md`, the kid brief itself
- `extensions/agi/driver.sh`, `lib/find-root.sh`, `hooks/cc-session-start.sh` —
  the shell surfaces, including the one that injects context into every session
- `extensions/agi-bridge/index.ts`, `schema.sql`, `README.md`, `run-loop.sh`

That was the right call for a first pass and it is now the thing blocking
**G6.1**. Stitch cannot assemble `agi` from `agi-tree` while the skill, the kid
brief and the session hook are files the graph has never seen. Worse, they are
the *highest-leverage* files in the repo: a change to `agent-prompt.md` alters
every kid in every future iteration, and today that change can be made with no
node behind it — which is exactly the open loop **G6** exists to close, in the
one place where it costs the most.

What has to exist: a level-3 node per non-code surface, carrying the same
derived contract shape as a code node — what it takes, what it promises — so
`stitch.py --verify` reports drift on a prose file the same way it does on a
module. Prose has no signature to parse, so the contract has to come from
somewhere else; deciding what a `SKILL.md` node's contract *is* is the real work
here, not the scanning.

Note the reflexive case and do not skip it: **G1.3 and G1.4 are changes to
`agent-prompt.md` and `dispatch.py`.** Under G6.1 they should originate as node
versions, which means this sub-goal is on their critical path, not parallel to
it. If they land as direct engine edits, they are two more entries in the
evidence that the arrow still points the wrong way.

~~Falsifier: run `stitch.py --verify` after editing one word of `SKILL.md`. If it
reports no drift, the surface is not covered.~~ **Retired 2026-08-23 — see below.
It was run, it fired, and passing it would not deliver what this goal is for.**

**Measured and judged 2026-08-23 (iter-9006 → 9008).** Chain:
`exp:noncode-surface-census` → `exp:prose-surface-probe` →
`verdict:noncode-coverage` (disproved as written, conf 0.85, evidence resolves).
The two halves of this goal resolve in opposite directions, so they are now
stated separately.

**The coverage diagnosis holds, and is no longer an assertion.** 74 of 316
tracked files carry level-3 nodes; against an eligible set of 189 after 127
justified exclusions, 74/189 = **39.2%**. Zero declared-scope files are missed —
the generator does exactly what it says, so the gap is a scope decision, not a
bug. All nine files named above: **9/9 uncovered**, verified. One extra find:
`extensions/agi/scripts/migrate_to_sqlite.py` is hand-written engine code that
misses the scan only because `scripts/` is not a scanned prefix — a second,
narrower scope bug.

**The remedy as originally stated does not deliver.** The old falsifier was run
for real and fired: a one-word edit to the live `SKILL.md` produced zero drift,
because `ast.parse` dies unconditionally at line 4 on an em dash, so stored and
fresh contracts are always the identical failure and the diff is always empty.
Worse than the mechanism failing is what fixing it would buy: of four candidate
prose-contract shapes, the best — **extracted claims** (directive clauses and
numbered rules, with line numbers, derived mechanically the way code's `how` is)
— *would* pass that falsifier, and would still **not** have caught the
`agent-prompt.md` / `SKILL.md` contradiction that motivates this goal. That is
two self-consistent nodes disagreeing, not one node going stale against its own
file, and `stitch.py`'s only cross-node check compares `payload_ref` strings,
never content.

**What this goal now commits to, in order:**
1. **Contract shape: extracted claims.** Decided, not left open. Same split code
   contracts use — the harness derives the claim list mechanically, a model fills
   the judgement fields.
2. **A fifth drift category: cross-node claim comparison.** None of the existing
   four compares two nodes against each other. Without it, coverage alone cannot
   deliver the reflexive-case protection this goal argues for.
3. **Reserve a model-judgement step.** "Commit your work" contradicting "do not
   commit" is a semantic negation. No mechanical diff performs it, and the
   `how`/`why` split reserves no room for it today.

**Replacement falsifier, and it is the whole point:** reintroduce the
`agent-prompt.md` / `SKILL.md` contradiction and confirm `stitch.py --verify`
flags it. Passing the old one-word test would have produced false confidence that
the reflexive case (G1.3/G1.4 editing `agent-prompt.md`) is protected when it is
not.