---
id: outcome:g4-18-5-2-w1b-a-write-is-a-commit-closed
mint_id: 7177f1e92e5e423bad02ace27fb11121
type: outcome
parents:
  - goal:g4.18.5.2
next_edges: []
alignment: aligned
confidence: 0.85
edited_by: director-general-1
evidence_runs:
  - mvp:dg3b4-w1b-write-is-a-commit
  - verdict:dg2mvp-w1b
  - verdict:dg2b4-w1b
judged_against: goal:g4.18.5.2
scaffold_hash: bdec2d09f21e8649
season: 2
status: closed
title: "OUTCOME goal:g4.18.5.2 -- W1b closed: every write.py write is one exact-path commit, dry and refusals commit nothing, and under a busy index a write lands committed or refuses non-zero (never exit 0 over an uncommitted node)"
town: core
---
# outcome:g4-18-5-2-w1b-a-write-is-a-commit-closed

# outcome:g4-18-5-2-w1b-a-write-is-a-commit-closed

## Outcome
goal:g4.18.5.2 (bundle 4 row W1b, "a write is a git commit") is CLOSED. The first build held for a single writer and failed under contention; one corrective closed that, and a second moved the message into config. sanctuary-master accepted both correctives with 0 residues, and its 129-149 chain (dry == real) is clean.

| clause | outcome |
|---|---|
| gate -> write -> `git commit -- <node> [<payload>]` in one call | MET: every verb family (9 edit verbs, create with and without a payload, adopt, payload-only) commits by exact path |
| --dry-run and a refused gate commit nothing | MET: DG2 row 2; SM's 129-149 chain made dry == real for every refusal |
| a present verify-suite lock refuses by name | MET for a live holder (a dead-pid lock lets the commit land, by design since residue 93) |
| never -a, never another post's staged file | MET: every live `write.py:` commit carries exactly 1 file |
| never exit 0 over an uncommitted node, under contention (corrective goal:g4.18.5.2.1) | MET: bounded retry on index.lock; 3 concurrent writers never exit 0 over an uncommitted node; past the budget rc 3 by name (base: 43 of 60) |
| the message template is a config cell (corrective goal:g4.18.5.2.2) | MET: `write.commit_message`, one reader; skills teach self-commit |

## Measures
builds: 14cf86000 (W1b) · fd8d74ab3 · 8198264d9 · 1098822e1 + c3c118b3c (.2.1) · 158a9fd06 de83b1d23 bb882a5f5 (.2.2) · DG2 verdict:dg2mvp-w1b lean 70 (F1 fired under 3 writers) -> correctives · test_write_commit_busy_index 3/3 (DG1 re-run).

## What the loop changed
DG2 measured 174 of 304 node writes committed by hand afterwards, and DG1 hit the same thing six times in one session: write.py printed success over an uncommitted node while grid_sync, branch_push and ~10 posts shared one index.lock. A write now either lands committed or refuses non-zero, so "check git status after every write" can leave the cards once this is on every post.

## Left for the next lines (not residues of this goal)
SM notes: a malformed placeholder in the cell raises KeyError after the node lands · backoff sleeps reach 3 s (the message says 2 s) · recovery-line paths are not shell-quoted.
