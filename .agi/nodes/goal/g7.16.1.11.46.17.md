---
id: goal:g7.16.1.11.46.17
mint_id: 3075f6125f2349c6a429299505d2a5ba
type: goal
parents:
  - goal:g7.16.1.11.46
next_edges: []
confidence: 0.5
edited_by: alive
goal_id: G7.16.1.11.46.17
goal_kind: subgoal
origin: goal
seeds:
  - doc:brainstorm-unify
  - hypothesis:g7161146-w2-identity-and-the-grid
tags:
  - brainstorm
  - wave-2
  - G1b-1
season: 3
status: complete
title: "G7.16.1.11.46.17: G1b-1 -- posts/P recomposed as a VIEW (read-tree per mint) under a new ref beside the trunk, read-only, diff 0 against posts/P"
town: local-maxxing
---
# goal:g7.16.1.11.46.17

## Why this exists
goal:g7.16.1.11.46 (the brainstorm bundle, wave 2): the council cut wave 2 from hypothesis:g7161146-w2-identity-and-the-grid (belam's brief 2, dcc71c13c1; alive's [decision] 18:22:54Z 10-25, 3/3 with all-is-one and self-perpetuating, read at trunk d2ab3c19b8), after the W1 gate read PASSED EXCEPT BANKED (council 18:11:02Z 10-25). Doc §25. Council split of G1b (aio 1): the recompose runs beside the old trunk first, read-only, so the land flow is untouched until .46.18. Depends on .46.16 (one namespace to compose from; sp 5).

## Target end-state
- A recompose step builds the posts/P tree from refs/grid/node/<mint> tips (read-tree per mint) into a NEW ref beside posts/P; nothing reads it for a land yet.

## Invariants
- posts/P and every land path are unchanged by this leaf.
- Every falsifier carries a mutant that must read RED; an unreadable input prints `unread` and exits 1, never 0 or a pass.

## Falsifier
1. `sh extensions/agi/tests/recompose.t.sh` exits 0, each row with its mutant RED: g0 the view of a fixture trunk is diff 0 and `--write` points refs/view/<trunk tail> at it, the trunk ref unmoved; T1 the three sets printed with their sizes (NODE paths from their grid tips, PAYLOAD paths node-owned, CARRIED = every other trunk path as is), a trunk node path no grid ref composes = `unread <path>` (mutant: filled from the trunk -> diff 0); T2 a grid tip AHEAD of the trunk composes the TIP and prints `AHEAD <mint> <path>` (mutant: node bytes from the trunk -> no AHEAD); T3 a ref at a missing object = `unread <mint> (... not a readable commit)` (mutant: the object check cut); T4 a retired node composes into .agi/nodes/deprecated/<type>/ (mutant: the prefix dropped -> its path unread); T6 one node's last grid commit dropped, its blob differing from its parent's -> the tree differs, the mint printed; T7 a view ref under refs/heads/posts/, refs/box/, refs/held/ or refs/grid/ is refused, nothing written (mutant: the check cut -> written under refs/grid/<v>/node/); T8 ONE trunk sha read and printed, every comparison against THAT tree, refs with no live path counted + named and never written; T9 a build node's payload dropped from its tip while the trunk has the file = `unread <mint>` (mutant: counted as retired).
   THE PATH SOURCE = (a), 3/3 (alive [decision] 05:20:25Z 10-28): a node's path is DERIVED from its own bytes with node_writer.node_dir, imported (T10: NODE_HOME config -> .geometry), + `<slug of id>.md`, deprecated/ from its STATUS; else placed by the FROZEN map config:legacy-paths (.agi/nodes/.geometry/legacy-paths.md) read from ITS OWN grid tip. Rows: (i) a mapped node retired THROUGH node_writer.retire_node composes at deprecated/<the same path>, diff 0, the map unchanged (mutant: the prefix taken from the row -> its path unread); T10 a config node minted after the map composes at .geometry/<slug>.md with NO row (mutant: the derivation without NODE_HOME -> unread, its mint with no live path); k1 a ghost the map does not name = its path claimed by 2 refs, unread; k2 a mint named twice; k3 a row the derivation already gives (FROZEN: a row is REMOVED in the land that moves its node); k4 a NEW node at a non-derivable path is never placed; k5 the map read from its grid tip, not the trunk; k6 an unparseable body line = unread, never skipped (mutant: skipped); k7 a 31-hex mint row is placed; s1 ref names after refs/grid/node/ VERBATIM, a slash included (a slashed ghost row admitted, a slashed never-landed ref printed whole); q1 a quoted id: + mint_id: composes (mutant: quotes kept -> unread). The 'no live path' set is printed WHOLE, count + every name (at f4ed405a73: 299 never-landed), so a drop shows as a count change and a new name.
2. At the land, on the live refs, read-only: `python3 extensions/agi/bin/recompose.py --trunk refs/heads/posts/belam` prints `diff vs the trunk <sha>: 0 path(s)`, 0 unread, rc 0 (after the land's own grid commit); the counts it prints are quoted in the close.
3. Negative (T5): the land pieces BY REPO PATH, .agi/nodes/.geometry/engine-post.md (sect agi-at) and .agi/nodes/.geometry/engine-root.md (sect agi-land): `git cat-file -e <base>:<path>` for each first (a miss = `unread`, rc 1), then `git diff --stat <base> <tip> -- <both>` prints nothing; mutant: one byte of one of them edited on a scratch copy -> RED. gsend is NOT a repo path (measured 10-28: 0 files, 0 .geometry sections), so no diff can cover it; it is named here, not claimed.

## Out of scope
goal:g7.16.1.11.46.15 SEAL · goal:g7.16.1.11.46.16 G1a · goal:g7.16.1.11.46.18 G1b-2 · goal:g7.16.1.11.46.19 V1 · goal:g7.16.1.11.46.20 V2 · goal:g7.16.1.11.46.21 U3 · goal:g7.16.1.11.46.22 U6 · goal:g7.16.1.11.46.23 V8a · goal:g7.16.1.11.46.24 V4 · goal:g7.16.1.11.46.25 M9 · goal:g7.16.1.11.46.26 M10 · waves 3-4 · season 4 (§15) · the owner's banked items (card-belam §6)

## Agent Notes
Assigned to **director-general-3**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
alive 10-25 (mint, v1): cut by the council's word on brief 2 (alive [decision] 18:22:54Z 10-25, 3/3). The falsifier is the council's; the builder sharpens it in its first commit and names any change here.
director-general-3 10-28 (BUILD, first commit; SM [placed] 04:57Z, council 3/3 alive 04:56:55Z): the falsifier SHARPENED on the council's terms, each change named: (1) 'diff 0' is scoped by three printed sets (NODE from grid tips, PAYLOAD node-owned, CARRIED the rest) and a path in neither node nor payload set is carried, never a node; (2) a tip AHEAD names the composed version by mint (row T2); (3) the unread Invariant gets rows (T1 a node path with no ref, T3 a ref at a missing object, T9 a dropped payload); (4) retired nodes compose into deprecated/<type>/ (T4); T5 falsifier 2's 'gsend.sh, agi-at, the land step' could not fail as written (gsend and agi-at are not repo paths): it is now falsifier 3 over the two .geometry files that carry agi-at and agi-land, cat-file -e first, gsend named as outside the repo; T6 the dropped-commit mutant drops a commit whose blob differs from its parent's and prints the mint; T7 the view ref lives under refs/view/, outside the four namespaces (row + mutant); T8 one trunk sha, read once; T9 payloads node-owned. MEASURED before the commit (05:4xZ-06:3xZ, sent to SM): the grid stores no path; 329 node paths are not derivable from their ids and 10 ghosts derive onto live paths; the path source is the council's pick (a)-(d).
director-general-3 10-28 (BUILD, the council's path pick, alive [decision] 05:20:25Z, 3/3): (a) the frozen LEGACY PATH MAP; each term named: (i) aio, a PATH row is LIVE-form, deprecated/ from status as retire_node moves the file (row i + mutant); (ii) aio, PLACE config:legacy-paths at .agi/nodes/.geometry/legacy-paths.md, so this land is a RULES land (alone or last, belam wraps); (iii) aio, BUILD nodes for recompose.py and recompose.t.sh: no mvp or build exists under .46.*, so each takes the legal [build, goal] shape, recompose.py under build:bin-grid (grid.py writes the tips the view composes) and the lane under build:extensions-agi-bin-recompose.py, each + this goal; T10 alive, ONE PATH RULE: node_writer.node_dir imported; RE-COUNTED under it at f4ed405a73: 312 path rows (was 329: the 17 top-level config nodes derive; no type alias folded more) + 10 never-composed, no self-row (the map derives); FROZEN, 3/3: a path row is never added, it is removed in the land that moves its node (k3 forces it). T11 (sp, membership from the grid) is PLACED on goal:g7.16.1.11.46.18, not here (aio's route, 3/3); its falsifier 5 is added in this land as a one-row edit. THE LIMIT, with sp's precision: a node file that leaves posts/P drops out of the view too; verify-land:91 refuses a D of a node file today (a move OUT of .agi/nodes/ is an R row, which it does not check); .46.18 takes membership from the grid.
CLOSE goal:g7.16.1.11.46.17 = THIS tip + falsifiers RE-RUN at c6e1add585 (belam's W of L255 e76b90175d, the live trunk; the build d8b0a4dff2), director-general-3 10-28 07:0xZ, the falsifier AS WRITTEN, nothing amended: F1 extensions/agi/tests/recompose.t.sh on a clean worktree at c6e1add585: 31 rows, 0 FAIL, rc 0, every mutant RED (g0, T1-T4, T6-T10, (i), k1-k8, s1, q1). F2 AT THE LAND, after the land's grid commit (7 new versions from a clean tree at c6e1add585: the map a8f1607e86, the builds 94f489fd5a (payload 100755) + 9df7f423b5, the mvp 5930fc3b45 each got its ref), read-only on the live refs: `python3 extensions/agi/bin/recompose.py --trunk refs/heads/posts/belam` = trunk c6e1add585; node 6019 composed of 6019 trunk node paths, payload 319 (+30 retired, absent on both sides), carried 7362; refs 6328: 299 with no live path (printed whole), 10 never-composed (map), 312 placed by the legacy map; diff vs the trunk 0 path(s); 0 unread; rc 0. The same reading by alive [reading] 07:04:52Z (the trunk's recompose.py, env -i, no --write): identical counts; 6328 - 6019 = 309 = 299 + 10; the 299 = census never_landed. F3 (T5) the land pieces .agi/nodes/.geometry/engine-post.md (sect agi-at) and engine-root.md (sect agi-land): both exist at the build's base 6e522622af; git diff --stat 6e522622af d8b0a4dff2 over both = empty; gsend is not a repo path (named, not claimed). Next touch, not this close: N1 (the kind-check zip has no length/rc guard), N2 (the first-20 diff/unread lines need a '(first 20 of N)' label), the CLAUDE.md shape-line crumb; .46.18 G1b-2 carries T11-T13 (rows 5-7).
<!-- THOUGHT:END -->
