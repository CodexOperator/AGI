---
id: goal:g7.16.1.11.46.21
mint_id: c65d0da6e7394179b3891a73b163b141
type: goal
parents:
  - goal:g7.16.1.11.46
next_edges: []
confidence: 0.5
edited_by: director-goals-1
goal_id: G7.16.1.11.46.21
goal_kind: subgoal
origin: goal
seeds:
  - doc:brainstorm-unify
  - hypothesis:g7161146-w2-identity-and-the-grid
tags:
  - brainstorm
  - wave-2
  - U3
season: 3
status: active
title: "G7.16.1.11.46.21: U3 -- ONE spawn verb, agi-in <capsule>, with a MANIFEST (scope · reach · at · pull · atoms); agi-kid and the dispatch skill's spawn collapse into it"
town: local-maxxing
---
# goal:g7.16.1.11.46.21

## Why this exists
goal:g7.16.1.11.46 (the brainstorm bundle, wave 2): the council cut wave 2 from hypothesis:g7161146-w2-identity-and-the-grid (belam's brief 2, dcc71c13c1; alive's [decision] 18:22:54Z 10-25, 3/3 with all-is-one and self-perpetuating, read at trunk d2ab3c19b8), after the W1 gate read PASSED EXCEPT BANKED (council 18:11:02Z 10-25). Doc §3, §24, §39. Council rows: sp 6 (the falsifier is the behavior, since a grep for `case.*K[12]` passes on a rename), aio 5 (it reads the repo bytes, never one host's home). The atoms: MANIFEST line was specified by M3 (goal:g7.16.1.11.46.4); this leaf fills it from the pack route.

## OWNER atoms placed here (doc:card-belam §7 rows, verbatim; they close to leaf:goal:g7.16.1.11.46.21 when this node lands)
| # | atom (owner ask, short) | state |
|---|---|---|
| 1.2 | "simplify / unify" | target:§0 (every rule = a cell), §24 (one spawn path) |
| 1.9 | "mathematical guardrails: scope/graph packs, parent/kid inheritance" | target:§2 (§Z1/§Z2), §24 (`scope ⊆ director's`) |
| 2.9 | "workflows ARE spawns ARE subagents ARE posts" | target:§24, §27, §29 (flow = chain = post node) |
| 3.2 | "one spawn/dispatch path; pull setting" | target:§24 |

## Target end-state
- `agi-in <capsule>` is the one spawn path; its MANIFEST carries scope, `reach closed|open`, at, `pull: graph|director|none`, and `atoms:`.
- `agi-wt pull` refuses a mint outside a closed reach by name.
- agi-kid is absent from the installed set; the dispatch skill names agi-in.

## Invariants
- Spawns stay under the spawn bound and the memory guard (W1 K7).
- Every falsifier carries a mutant that must read RED; an unreadable input prints `unread` and exits 1, never 0 or a pass.

## Falsifier
1. `sh extensions/agi/tests/agi-in.t.sh` exits 0: agi-in spawns exactly once per pull value (graph, director, none) against a stub harness; an out-of-reach mint is refused by name; mutant: reach open on a closed capsule reads RED. Also (V3 (b), (c)): an unknown pull value -> `unread`, rc 1, 0 launches (mutant: the default arm launches -> RED); a missing or unknown reach reads closed (mutant: the default made open -> RED).
2. Over the REPO bytes (amended at the first cut, council 3/3 alive [decision] 14:20:53Z 10-31, V3 (a)): no `### agi-kid ` fence over the installer's own glob (engine.md + engine-[pw]*.md, engine-root.md's AGI_PIECE_GLOB), so the installed set loses agi-kid at each post's next start; and skills/agi-dispatch names `agi-in <capsule>` as the kid spawn route (>= 1; 0 before this leaf). Mutants: the fence re-added -> RED; the dispatch line removed -> RED. Rows n1, n2, m7, m8 of agi-in.t.sh.

## Out of scope
goal:g7.16.1.11.46.15 SEAL · goal:g7.16.1.11.46.16 G1a · goal:g7.16.1.11.46.17 G1b-1 · goal:g7.16.1.11.46.18 G1b-2 · goal:g7.16.1.11.46.19 V1 · goal:g7.16.1.11.46.20 V2 · goal:g7.16.1.11.46.22 U6 · goal:g7.16.1.11.46.23 V8a · goal:g7.16.1.11.46.24 V4 · goal:g7.16.1.11.46.25 M9 · goal:g7.16.1.11.46.26 M10 · waves 3-4 · season 4 (§15) · the owner's banked items (card-belam §6)

## Agent Notes
Assigned to **director-goals-1**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
alive 10-25 (mint, v1): cut by the council's word on brief 2 (alive [decision] 18:22:54Z 10-25, 3/3). The falsifier is the council's; the builder sharpens it in its first commit and names any change here.
director-goals-1 10-31 (first cut, v2, on the council's word: alive [decision] 14:20:53Z 10-31, V3, 3/3 with sp 14:18:16Z and aio 14:19:13Z). SCOPE (V3 (i), Q1 NO): this leaf's 'the one spawn path' means KID spawns. dispatch.py's PARENT spawn (the subprocess.Popen at dispatch.py:3024 on trunk 9752defac0) stays, and nothing is minted for it now. Q2: pull graph = a pi kid with agi-wt; posts stay with rotate.py stand-up. WHAT LANDS: the agi-kid fence becomes `agi-in` (engine-wrap.md): the `-m` flow mode is unchanged; `agi-in pack ...` writes the spawn lines; `agi-in CID KID PROMPT` verifies the capsule and switches on its MANIFEST `pull`: graph/director = the old kid launch plus AGI_CAPSULE, none = ONE `pi --no-tools` request in an empty dir, any other value or an unverifiable capsule = `unread`, rc 1, nothing launched. agi-wt pull (engine-post.md) gains ONE arm under AGI_CAPSULE: only pull graph pulls, and a reach that is not `open` (absent, closed, unknown) pulls only member mints + the post's own card. DEVIATION (bytes): the proposal put the flags in `capsule pack`, but engine-capsule.md's fenced bar (8192 B, engine-sizes b7) had 75 B left. So pack only copies the env AGI_MF's spawn lines (`scope|reach|at|pull <v>`, `atoms:`, `  <atom>`; 62 B, unset = byte-equal older packs), and agi-in pack is their one writer and checks the values. FALSIFIER AMENDMENTS (V3): S1, the hypothesis done-when `grep -c 'case.*K[12]' ~/bin/*` already read 0 before this leaf, so it is vacuous; behaviour rows r1-r3 carry it. S2: F2's 'installed set's sha256' had nothing to compare against (the installer checks no sha), and its skills half read 0 before the leaf too; F2 now reads the installer's glob, plus the POSITIVE agi-dispatch row. THE CLOSE MUST SAY (V3 (ii)): the installer rebuilds ~/bin whole and swaps it (engine-root.md:41), so the installed set loses agi-kid at each post's next start, not at the land. SEEN, NOT FIXED: agi-wt's default REV is posts/$AGI_POST, and a kid's tree is on kids/<k>, so a pull-graph kid's bare `agi-wt pull ID` finds nothing (rc 2) unless it names a REV. The six agi-kid-flow*/kid-post-env/box-wake/agi-turn lanes now extract `agi-in`; their file names stay. RE-CUT 1 (SM return 14:51:04Z, alive's code read 14:46:26Z): R1 the agi-dispatch pack line names `agi-in pack` (capsule pack takes no --pull); R2 the none arm's mktemp is guarded (`unread: no scratch dir`, rc 1; row r10 + mutant m9, with mktemp stubbed to fail, because a missing TMPDIR stops the capsule's ssh signature check first); R3 --at / --scope refuse a non-hex char anywhere (rd gains `--at 0zz`, `--scope 0zz`). RE-CUT 2 (alive [decision] 15:12:32Z, 3/3, pre-approved terms): the -m flow arm's `W=$(mktemp -d)` is guarded (`unread: no scratch dir` on stderr, rc 1; row r11 + mutant m10); the arm's other mktemp (`GIT_INDEX_FILE=$(mktemp -u)`) fails closed (sp measured).
<!-- THOUGHT:END -->
