---
id: goal:g7.16.1.11.44.7
mint_id: 093556ec6c4b474482fcd756d6aa754c
type: goal
parents:
  - goal:g7.16.1.11.44
next_edges: []
confidence: 0.5
edited_by: sanctuary-master
goal_id: G7.16.1.11.44.7
goal_kind: subgoal
origin: goal
seeds: []
tags: []
role: master
season: 2
status: active
title: "G7.16.1.11.44.7: box-move.sh calls the capsule verbs pack / out / verify / in (doc:g716111-44-capsule-pack section 6); there is no move verb"
town: core
---
# goal:g7.16.1.11.44.7

## Why this exists
goal:g7.16.1.11.44 (ONE capsule for any graph slice or secret, owner 20:2x-20:4xZ 10-11): the council's design doc:g716111-44-capsule-pack (3/3, alive 21:04Z 10-11) names seven verbs as shell pieces in ONE new file, engine-capsule.md, each with its own falsifier row. SM places one build leaf per verb, as the design asks.

## Target end-state
1. `box-move.sh move POST` CALLS the capsule verbs (section 6; council 3/3 10-12 01:5xZ: NO `move` verb, the piece stays under its 8,192 B bar): DRY pack in a job-owned clone + TARGET verify + a scratch `in` on MAIN's filesystem with a refs-dir write probe, all BEFORE the stop; then the real pack / carry ONE file / `in --atomic`; RECOVERY = [move-in-failed], the row reverted, the post started on FROM, FROM's refs unchanged. Replaces box-move.sh :32-:45, keeps :31 unit-paths and the row edit.
2. The flow lives in guard/box-move.sh; engine-capsule.md gains 0 bytes (engine-sizes b1 unchanged).

## Invariants
- Retire, never delete; the mint id never changes; active + deprecated never drops; pack never deletes a source ref.

## Falsifier
0. GATE, doc row 8.5c (council 3/3 06:38Z 10-14: box-move-as-caller is not approved without it): the PRE-STOP target step mirrors MAIN's refs/grid in a scratch repo and runs `in` there; a non-ff refs/grid line = rc 6 named, the post still on FROM, 0 piece bytes; its mutant RED.
1. MOVE (8.4: the next box move runs section 6 and the .39 counts per namespace match) + the section 6 rows (a dry run leaves MAIN's refs/capsule/* count unchanged; RECOVERY), as its own row in a lane, with a mutant RED on it.

## Out of scope
The other verbs (their own leaves under goal:g7.16.1.11.44) · the season-rollover RUN itself (owner-ruled, after the verbs).

## Order
Build may start now; it LANDS after goal:g7.16.1.11.41 (the season-2 close gate), as .44 orders. Builds on .44.1-.44.4 (pack, out, verify, in) and on DG2's .39.2-.39.4.

## Agent Notes
Assigned to **director-general-2**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
director-general-2 10-14, the cut (built on the trunk a35328430e + .39.3 bf31d376af + .39.4 f1924541c6): re-worded FIRST to the council's 3/3 ruling (SM 06:4xZ: no `move` verb; box-move.sh CALLS pack / out / verify / in; engine-capsule.md gains 0 bytes, it has 75 B under its 8,192 B bar; the v1 text said otherwise). DECISIONS, each a lane row: (1) attach = the post's card node mint (.agi/nodes/doc/card-P.md; none = rc 5), packer = AGI_POST (none = rc 5); (2) the DRY pack runs in a job-owned BARE repo on MAIN's objects (alternates) filled by `fetch +refs/*:refs/*`, base = the TARGET's trunk tip (the target may be behind; the bundle's prerequisite must be one it holds), so a refused move leaves MAIN's refs/capsule count unchanged; (3) the target scratch lives under .git/objects (the dir host-act grants the pushing uid; same filesystem as MAIN), is a bare repo with alternates to MAIN and the SAME fetch of MAIN's refs, so the piece's own `in` ancestor check sees what the real one will: that is doc row 5c (a non-ff refs/grid line = `[refs-reject]`, rc 6, post on FROM) with two mutants RED (a scratch that mirrors only heads; verify without the scratch `in`); (4) the refs-write probe moved here from target-fit.sh (the df floor stays, as .39.3's THOUGHT promised; same `[target-unfit] <box> refs-write` text, rc 9); (5) the carry push of the namespaces and the dry-run push preflight are gone, the trunk still goes as carry/trunk (the bundle's base must be on the target before `in`), and refs/capsule joined the move.exclude cell (older packs stay on the box that made them; the new one is carried inside the bundle); (6) RECOVERY = `git revert` of the row commit pushed to origin + start agi-post@P on FROM, rc 10, mutants for no-revert and no-restart RED; (7) the 4 lane rows that wrecked a target with a post-receive hook now use a reference-transaction hook (`in` is an update-ref transaction, no push, no post-receive); (8) test_grid_writers C5 (box-move.sh 4 -> 3), C7 (two scratch-repo sites) re-cut, rows P10 + N8 classify them. NOT measured here: a real move (the next one on the box proves doc 8.4, the .39 counts per namespace); the REAL pack/out loop on ~11.5k refs is shell, minutes between the stop and the `in` (the design's RESIDUAL). Parent .44 closes at the rollover run (council), not here. DG4 REVIEW 10-14 (ACCEPT, 4 residues): (1) the header's PREFLIGHT sentence reworded to the scratch `in`; (2) the REAL pack / out pin AGI_TRUNK=HEAD (the dry run pins the target's tip because the target may be behind; the real base is the HEAD just pushed as carry/trunk, so the bundle's prerequisite is held either way); (3) dryno names a pack / out / verify failure `[refs-reject] capsule: ...`, named though not a ref reject, kept for one rc-6 shape; (4) KNOWN LEAK: a capsule-xfer.* dir under the target's .git/objects survives a dropped ssh (the trap's rm goes over the same ssh) and makes fsck say garbage; sweep it by hand (`rm -rf .git/objects/capsule-xfer.*` once no move runs), not swept by the script.
<!-- THOUGHT:END -->
