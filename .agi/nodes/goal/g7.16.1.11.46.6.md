---
id: goal:g7.16.1.11.46.6
mint_id: d41dd1921acf4ee6be54f343aa20602c
type: goal
parents:
  - goal:g7.16.1.11.46
next_edges: []
confidence: 0.5
edited_by: alive
goal_id: G7.16.1.11.46.6
goal_kind: subgoal
origin: goal
seeds:
  - doc:brainstorm-unify
tags:
  - brainstorm
  - wave-1
  - C1
season: 3
status: active
title: "G7.16.1.11.46.6: C1 -- agi-cred: a root timer puts the Console service-account key from Doppler into /etc/credstore/claude-sp (0600) for the lane units only (LoadCredential), with a credits_live kill cell; no post process environment holds an sk-ant key"
town: local-maxxing
---
# goal:g7.16.1.11.46.6

## Why this exists
goal:g7.16.1.11.46 (the brainstorm bundle, wave 1): the council cut wave 1 from hypothesis:g7161146-w1-protect-the-loop-and-measure (alive's [decision] 21:06Z 10-23, 3/3 with all-is-one and self-perpetuating, read at trunk 2ef3c2f6d6). Doc §36.2/§36.4 (C1), §33. Box readings: doppler v3.76.5 installed; /etc/credstore exists (root 700, empty); systemd 255 (LoadCredential). (K5) As a post, another post's /proc/<pid>/environ is Permission denied, so an "empty grep" passes on nothing: the check runs as root and counts what it read. Doc sections implemented: §36.2, §36.4 C1, §33 (doc:brainstorm-unify is reference, never placement).

## OWNER atoms placed here (doc:card-belam §7 rows, verbatim; they close to leaf:goal:g7.16.1.11.46.6 when this node lands)
| # | atom (owner ask, short) | state |
|---|---|---|
| 6.1 | service-account key in Doppler; workload identity later?; needed for batching? | target:§36 (cannot mint keys; WIF = season 4; not needed for batching) |
| 3.11 | run autonomously; provide keys | target:§33, §36 |

## Target end-state
- A root timer `agi-cred` runs `doppler secrets get CLAUDE_CONSOLE_SP_KEY --plain --project agi --config <cfg>` with a read-only Doppler service token from /etc/credstore/doppler-token and writes /etc/credstore/claude-sp (0600 root).
- Lane units only carry LoadCredential=claude-sp:/etc/credstore/claude-sp; never Environment=, never a post's env, never the repo.
- `credits_live: false` in config:secrets → agi-cred removes /etc/credstore/claude-sp and restarts the lane units at the next tick.
- A root check unit `agi-cred check`: pids read == the live agi-post@ process count, that count > 0, and `grep -c sk-ant` over each environ = 0 (counts only, never a matched line).
- The install is a root act by belam after the stub test passes; live = passed except the Doppler token (owner, card-belam §6) + the root install.

## Invariants
- The org-wide key is root's only; no post and no kid environment holds it.
- The check never prints a key byte.

## Falsifier
1. `sh extensions/agi/tests/agi-cred.t.sh` exits 0 as a post, with a stub doppler on PATH and a temp credstore: the file is written 0600; credits_live false removes it; a unit text without LoadCredential gets nothing; mutant m (agi-cred check that skips the count) reads RED on an empty selector.
2. Root leg at install (belam): `agi-cred check` exits 0; a stub post started with ANTHROPIC_API_KEY=sk-ant-test makes it exit non-zero.
3. Negative: `git grep -n -e 'Environment=.*ANTHROPIC_API_KEY' -e 'sk-ant-' -- .agi/nodes/.geometry extensions/agi/bin` prints nothing.

## Out of scope
V10a = .46.11 (sanctuary-master's leaf, minted in its own land) · the other wave-1 leaves .46.2-.46.10 · waves 2-4 (U2 U3 U6 V1 C4 C5 …) · season 4 (§15)

## Agent Notes
Assigned to **director-science-1**.
