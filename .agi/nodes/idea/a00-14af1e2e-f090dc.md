---
id: idea:a00-14af1e2e-f090dc
mint_id: 636e7347e01449c68fc71e412f2fa9ce
type: idea
parents: []
confidence: 0.5
evidence_runs: 0
title: A00 14af1e2e f090dc
verdict: pending
wired_at: 1788198005
wired_from: a00-14af1e2e
---


<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Seeded at BIG zoom (iteration 1, agent a00-14af1e2e). No existing domain
covers concurrent multi-agent writes to one graph — yet the 2026-08-31
live run already produced this failure class once (goal:g4.1: parallel
kids share one tree, `git commit -A` from one kid swept another kid's
half-written node plus a human's uncommitted engine edits into a commit
labelled with the wrong node id). The graph runs parallel agents by
design (spawn gates, parallel chain steps), so write contention is
structural, not incidental. Fresh chain; scale: big.
<!-- THOUGHT:END -->

# idea:a00-14af1e2e-f090dc

## Idea

`scale:` big (new chain) — **domain: concurrent graph writes / multi-agent write isolation.**

The engine runs multiple agents against one thoughtgraph (parallel chain
steps, spawned kids, crons). Today safety comes from convention: kids are
told "do not run git at all", the loop owns commits, `grid.py commit
--all` snapshots after the fact. goal:g41 proved convention fails under
parallelism — one agent's bulk commit swallowed another's in-flight work.

The idea: make write isolation a graph-level property, not a prompt rule.
Candidate shapes to explore downstream:

1. **Agent-scoped staging** — each agent writes only under a per-agent
   session dir (`.agi/sessions/<iter>/<agent>/`); the loop is the single
   writer that promotes files into `nodes/` at commit time.
2. **Claim-based node locking** — a node must carry a `claimed_by:`
   frontmatter line before an agent edits it; the claim is the
   coordination record, inspectable by `grid.py status`.
3. **Commit attribution contract** — commits are made per-agent-session
   with an explicit path list (never `-A`), so a commit's provenance is
   mechanical, not inferred.

Each is a testable hypothesis: inject two concurrent writers and assert
no commit contains bytes neither writer authored.

## Why

- goal:g4.1 already happened; nothing in the graph records the fix.
- Convention-based safety scales badly — the cost of every future agent
  prompt growing another "do not do X" clause.
- Graph data (nodes, claims, commits) is machine-checkable; prompt data
  is not.

## Next

Spawn a hypothesis (prefer shape 1 or 3 — lock-based schemes risk
deadlock the same way `grid.py checkout --all` did pre-goal:g11).

Big: seeded fresh domain idea 'concurrent graph writes / multi-agent write isolation', motivated by goal:g4.1; hypotheses to follow.