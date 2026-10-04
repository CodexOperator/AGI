---
id: goal:g7.16.1.11.12
mint_id: bf6507f5deb94d71ad93afd259c78cc7
type: goal
parents:
  - goal:g7.16.1.11
next_edges: []
confidence: 0.6
edited_by: director-general-1
goal_id: G7.16.1.11.12
goal_kind: subgoal
origin: goal
scaffold_hash: 4c4a8cdf0ba4c1c6
season: 2
seeds:
  - goal:g7.16.1.11
status: active
tags:
  - council
  - design
  - g7.16.1.11
  - aa2
  - lap
  - keys
  - budget
title: "G7.16.1.11.12: AA2 rotations -- the lap is one permutation cycle on the post tree projected from the parent cells; a key is fresh per generation on root's ring; the base stays under 8 KB with 0 new pieces"
town: core
---
# goal:g7.16.1.11.12

## Why this exists
goal:g7.16.1.11: the council's AA2 section (doc:radically-simple-engine §AA2 on posts/self-perpetuating, 2033-2088) answers the owner's 23:2xZ line that protocol is a matrix rotation or projection, so things go only where they must go, and that the in-session rotation handoff for the figure 8 can be built into the other pieces. What it measured: today's cells give a BROKEN tour (the owner cycle covers 8 of 16 darts: council was a parent value, not a row); the signers ring cannot come from a post-writable tree; and config:engine is 8,298 B, 106 over the 8 KB bar. belam's ruling ec5daa28a made `council` a real inert row, which is the one cell change AA2 asked for.

## OWNER 2026-10-01 23:0xZ + 23:2xZ, verbatim (via the council bundle)
"We just need to allow each post to have a will box which they already do, an inbox and a holding box or an outbox or something."
"This is why protocol needs to be a mathematical matrix rotation or projection. So things could only go where they must go."
"Remember the graph can hold as much as you want just the engine itself needs to be tiny. It can lead on the graph via templates we have so much recursion and linking built in."
Skills line (owner 23:4xZ via belam 23:49Z): "update the other skills to reflect the way the new system works"


## Target end-state
- The lap = PHI on the tree's darts (u->v maps to v->w, w the next neighbour after u in ring(v) = [parent, children in row order]); on a tree ONE cycle of 2(n-1) darts = the Euler tour = the figure eight of council-loop. It is projected into .geometry/lap.tsv (one row `u v w` per dart) by 268 B of awk FOLDED INTO grow-project (no new piece).
- A `[lap]` mail names no recipient: agi-send in lap mode looks up the ONE row `F me T`; the gate (grow-gate, existing) refuses a `[lap]` commit on refs/box/P/T unless row `F P T` exists. A misrouted baton is refused, not delivered late. A subtree lap is 2|T| darts (nesting, no new cell).
- LAP and GENERATION are two rotations that commute: a baton is an unread ref, so it survives any number of generations.
- KEYS: root owns the ring; at unit start ExecStartPre=+ appends `<post>@agi namespaces="git" valid-after=<now> <pubkey>` to a root-owned allowed-signers; a key is FRESH PER GENERATION (`.fresh`, not a unit start); a crash restart appends 0 lines; a retired generation's commits still verify at their own dates.
- BUDGET: config:engine <= 8,192 B (agi-project's pi-path resolution moves to engine-wrap, -332 B; + the three matrix rows ~110 B; + one map line ~70 B), the seed unchanged at 1,023 B.
- The council row exists (ec5daa28a) and every member sits under it, so the owner cycle covers all 18 darts.
- VERSIONING (AA2, self-perpetuating 370cd4433): PHI's 18 darts read as branch moves (9 DOWN = branch off the parent's tip, 9 UP = the parent may fast-forward, masked by the `lands` cell; the council row carries lands: [sanctuary-master]); a child's tip moves only on its parent's handoff mail; trees live one generation (commit always, purge only at ~/.fresh; agi-turn -129 B, agi-flush +17 B, the per-stop trunk merge -61 B); READ is open on one box and hidden by the hub's `hide` (331 B) across boxes (banked to belam). Falsifiers AA2.9-AA2.17.
- ONE-BOX READ (AA2 'READ, RULING 2', belam accepted (b) 04:45Z): one git object store per post user (alternates -> a trunk-only commons, never MAIN), root's agi-carry moves only a lap dart's tip; ~1,059 B expansion; limits: privacy after the switch only, the commons never pruned, the uid barrier is the build check.
- LADDER OUT (AA2, belam 04:43Z [decision]): tier = projected depth; a kid's spec = the nearest ancestor-or-self row's `engine.kid` cell (kid-of, ~+360 B in agi-kid, AGI_KID_MODEL is EMPTY on every v4 row today); the ladder retires in order with dispatch.py. Falsifiers AA2.18-AA2.25.
- THE RING IS THE TREE (doc:radically-simple-engine section AB + AB.5 + AB.6 + AGI_SEAL_ID, landed at trunk 1c0edcf20; belam [decision] 03:07Z releases it, owner 02:3xZ 'Is the design finished and looks sound? If so send on'): ONE ring node at .agi/nodes/.geometry/ring, one line per post x algorithm column; may(s, x) <=> s is ancestor-or-self of ruler(x) read at the RECEIVING tip; no date is read; layered blocks under refs/agi/block/* are the calendar; ONE GENERATION = three keys (SIGN published once sealed, PQ inner, SEAL never published); a retired SIGN key goes to refs/revoked (never pushed); the outward sealer is a scheduled GitHub sweep on master. This SUPERSEDES the KEYS bullet above where they differ (root no longer owns a post-side ring: the post writes its own next line, signed by its current key; agi-signers retires after AA2.64). Falsifiers AA2.54-AA2.80 are carried by the hypotheses named g716111-ab-* and g716111-aa2-the-trunk-refuses-... (the leaves, in build order: key-gate, ring, out-line, ckpt, pq, revoke, flow-rotation, agi-signers retires, outward sealer). HELD: AA2.55 (two boxes), AA2.61 (a real PQ verifier), AA2.75/76/78 (outward, belam's GO), AA2.62 RETIRED (AB.5: the nest is in the block blob).

## Invariants
- Row order IS sibling order: reordering config:posts reorders the lap (intended, now load-bearing).
- A group vertex has no key: who issues SM's cert (council -> SM) is the §O ring, banked to the council.
- agi-gate HEAD rc 0 after every move; boxes and the lap are EXPANSION, never in the zygote.
- SIZE BAR (the bundle's statement of the owner's line): the base install stays under 8 KB (config:engine <= 8,192 B), unfolded from a 1 KB seed (1,023 B); boxes, the lap and the land check are EXPANSION read by `sect`, 0 B in the zygote; nothing model-manual that could be automated; reuse an existing piece before adding one.

## Falsifier
1. `awk` over `.geometry/lap.tsv` shows 18 rows, every image unique, and the cycle from (owner, belam) has length 18 (AA2.1) on today's cells; `wc -c` of config:engine <= 8192 and `agi-gate HEAD` rc 0 (AA2.4).
2. (SUPERSEDED by section AB where it conflicts: the ring is a trunk node ruled by grow-gate, and ckpt, revoke and pq are new pieces; falsifier AA2.63 is the size gate.) Negative: `git grep -n 'valid-after' -- <any post-writable path>` returns zero hits (the ring is root-owned only), and no new engine PIECE is added (the piece list of config:engine is unchanged).

## Out of scope
goal:g7.16.1.11.11 (boxes) · goal:g7.16.1.11.13 (land) · goal:g7.16.1.11.14 (skill deltas, incl. the load matrix) · the group vertex's own key (banked to the council) · who owns KEYS if not AA2 (open: AA2 or AA3, the bundle proposes AA2).

## Agent Notes
Assigned to **director-general-1**.
