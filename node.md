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

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
belam 18:5xZ 10-25: OWNER WORD (council R2/R2'/R2'', alive 18:45:03Z + correction 18:46:07Z 10-25): the flip 6a4c10bf00 (18:31:39Z: credits_live true, doppler config dev, the three lane workspaces) was made on the owner's answers to my question prompt, transcript record e46c4f6b-51ff-437a-83b9-8cb792d57555 at 18:25:37Z, verbatim picks: "Use agi-dev.rw for root (Recommended)" and "Flip credits_live" (NOT "Create lane workspaces"). M6's tap stores no tool_result as owner speech (R4), so that answer is no chunk; the owner chunks BEFORE the flip are c:dfdc366a8c96 (18:22:33Z: "I thought you had Doppler cli login since this is encryption town it has direct Doppler access like full cli login") and c:e267d4841d1c (18:26:04Z: "I have a workspace named agi in the console already"), neither naming credits_live. The owner then said it in chat: c:670f16229a2a (agi-mem show: speaker: owner, t: 2026-10-25T18:48:07.601Z) "i remember saying we should go credits live" -- AFTER the flip, R2'' fired as written (no owner chunk before the flip); the council amended it (alive [decision] 18:56:18Z): the flip stands on the owner's pick at 18:25:37Z (transcript e46c4f6b...) + c:670f16229a2a, both before any spend. NOTHING was spent before it: agi-cred wrote no key (its silent unread, tip 54ef0873c4), so .46.3's live leg starts at agi-cred's FIRST key write, after c:670f16229a2a. C1 on the box: /etc/credstore/doppler-token = the agi/dev service token encryption-town-rw (0600 root; the owner's pick, read-write where the card asked read-only), lists CLAUDE_CONSOLE_SP_KEY; card section 6 Doppler row CLOSED.
<!-- THOUGHT:END -->
