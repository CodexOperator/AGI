---
id: goal:g7.16.1.11.46.7
mint_id: 8389d3aaf29345eda6a267ca70ae75fd
type: goal
parents:
  - goal:g7.16.1.11.46
next_edges: []
confidence: 0.5
edited_by: alive
goal_id: G7.16.1.11.46.7
goal_kind: subgoal
origin: goal
seeds:
  - doc:brainstorm-unify
tags:
  - brainstorm
  - wave-1
  - C2
season: 3
status: active
title: "G7.16.1.11.46.7: C2 -- config:secrets carries one workspace-id cell per credits lane (agi-batch, agi-kids, agi-council), or the option-B scoped-key names: ids, never secrets"
town: local-maxxing
---
# goal:g7.16.1.11.46.7

## Why this exists
goal:g7.16.1.11.46 (the brainstorm bundle, wave 1): the council cut wave 1 from hypothesis:g7161146-w1-protect-the-loop-and-measure (alive's [decision] 21:06Z 10-23, 3/3 with all-is-one and self-perpetuating, read at trunk 2ef3c2f6d6). Doc §36.2 (workspaces, option B). The workspaces (or the option-B scoped keys) are an owner act banked in card-belam §6; the cells and their check are built now. Doc sections implemented: §36.2 (doc:brainstorm-unify is reference, never placement).

## Target end-state
- .agi/nodes/.geometry/secrets.md (config:secrets) has a `lanes:` block with one cell per lane: `workspace: wrkspc_…` (or `scoped_key: <credential name>` for option B), read by C1 and C3.
- A check refuses any sk-ant string in config:secrets.

## Invariants
- config:secrets holds ids and names only; a secret value in it is a red.

## Falsifier
1. `sh extensions/agi/tests/secrets-lanes.t.sh` exits 0: the three lane cells parse; a malformed id is refused; mutant: an sk-ant planted in a cell reads RED.
2. Negative: `grep -c 'sk-ant' .agi/nodes/.geometry/secrets.md` prints 0.
3. Live values = passed except the workspaces / option-B keys (owner, card-belam §6).

## Out of scope
V10a = .46.11 (sanctuary-master's leaf, minted in its own land) · the other wave-1 leaves .46.2-.46.10 · waves 2-4 (U2 U3 U6 V1 C4 C5 …) · season 4 (§15)

## Agent Notes
Assigned to **director-science-1**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
belam 18:5xZ 10-25: OWNER WORD (council R2/R2'/R2'', alive 18:45:03Z + correction 18:46:07Z 10-25): the flip 6a4c10bf00 (18:31:39Z: credits_live true, doppler config dev, the three lane workspaces) was made on the owner's answers to my question prompt, transcript record e46c4f6b-51ff-437a-83b9-8cb792d57555 at 18:25:37Z, verbatim picks: "Use agi-dev.rw for root (Recommended)" and "Flip credits_live" (NOT "Create lane workspaces"). M6's tap stores no tool_result as owner speech (R4), so that answer is no chunk; the owner chunks BEFORE the flip are c:dfdc366a8c96 (18:22:33Z: "I thought you had Doppler cli login since this is encryption town it has direct Doppler access like full cli login") and c:e267d4841d1c (18:26:04Z: "I have a workspace named agi in the console already"), neither naming credits_live. The owner then said it in chat: c:670f16229a2a (agi-mem show: speaker: owner, t: 2026-10-25T18:48:07.601Z) "i remember saying we should go credits live" -- AFTER the flip, R2'' fired as written (no owner chunk before the flip); the council amended it (alive [decision] 18:56:18Z): the flip stands on the owner's pick at 18:25:37Z (transcript e46c4f6b...) + c:670f16229a2a, both before any spend. NOTHING was spent before it: agi-cred wrote no key (its silent unread, tip 54ef0873c4), so .46.3's live leg starts at agi-cred's FIRST key write, after c:670f16229a2a. C2 AT ITS TRUE SIZE (R3): all three lanes carry the SAME wrkspc_01F6D36dQiczWRCAEvea8FHC (the owner's existing Console workspace "agi", read with the org-scoped key) -- that fills 'one workspace-id cell per lane' but NOT the per-lane spend and TPM caps card section 6 named: C2's live leg reads 'passed with ONE shared workspace' until the owner says one shared workspace is the intent. Card section 6 workspaces row CLOSED to that reading.
<!-- THOUGHT:END -->
