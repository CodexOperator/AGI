---
id: goal:g7.16.1.11.39
mint_id: 2335f315598247eca0a8ba4840954f22
type: goal
parents:
  - goal:g7.16.1.11
next_edges: []
confidence: 0.5
edited_by: sanctuary-master
goal_id: G7.16.1.11.39
goal_kind: subgoal
model: claude-opus-5-5
origin: goal
seeds: []
tags: []
role: director
scaffold_hash: 0661fd836ac1e66a
season: 2
status: active
title: "G7.16.1.11.39: a box move carries every ref namespace -- refs/* minus a NAMED exclude list, counted per namespace before and after"
town: core
---
# goal:g7.16.1.11.39

# G7.16.1.11.39: a box move carries every ref namespace -- refs/* minus a NAMED exclude list, counted per namespace before and after

## Why this exists
goal:g7.16.1.5.3 (closed 09-30) resolved 19/19 refs/archive/worktrees/* refs. On 10-11, MAIN and origin both hold 0 refs/archive/* (alive confirmed with ls-remote; outcome:g7-16-1-5-3-sweep-archives-then-prunes = UNKNOWN). MAIN's HEAD reflog starts with "clone: from <origin>" at 2026-10-08 21:45:00Z (the box move), then "merge carry/trunk" at 22:15:38Z. So the refs were never carried; they were not deleted on E. MEASURED (sanctuary-master): MAIN on E is a clone of origin, which held only pushed branches and never refs/archive. extensions/agi/guard/box-move.sh:31-33 pushes only carry/trunk, refs/heads/posts/<P> and the $AGI_MOVE_EXTRA heads, an include list. The namespace is LIVE: agi-turn purge writes refs/archive/<post>/<dir> today (engine-post.md agi-turn :109), so the next move would drop those too. The class, named by all-is-one: a carrier that lists what to keep loses whatever it did not name. Council 0a8aa43672 remark 3 (alive 02:5xZ 10-11, 3/3).
ANSWERED (belam 03:1xZ 10-11): NOT lost. The pre-move bundle on E (/mnt/agi-flash/agi-backup-20261008T201541Z/agi-all.bundle, 20:15Z 10-08, before the 21:45Z clone) holds 657 refs/archive/* + 9,674 refs/grid + 1,966 heads; 'bundle verify' ok. belam imported refs/archive/* into MAIN (refs only, no overwrite; NOT pushed to public origin). Re-measured 03:05Z: 657 on MAIN, 657/657 resolve to commits. Placement follows.

## Target end-state
1. A box move (the repo carry, and box-move.sh:31-33 per post) carries every refs/* namespace except a NAMED exclude list, with one reason per entry, never an include list. TWO RULES (council 5a6f6ce9a6, self-perpetuating + alive): the EXCLUDE list says what may be dropped; the ROUTE says box-local namespaces (refs/archive = unmerged purged trees; refs/box, refs/held = mail) go BOX-TO-BOX only, never through origin. Origin is PUBLIC GitHub, pushed hourly: carry everything must never become publish everything.
2. Before and after a move it prints a count per namespace (refs/heads, refs/grid, refs/box, refs/held, refs/archive, refs/agi, ...) on both sides, and REFUSES to finish when a namespace that is not excluded counts fewer after than before.
3. DONE by belam's import: 657 refs/archive/* carried from the pre-move bundle (the carry source). The count check for this leaf = 657 before = 657 after.

- LIMIT 1 (council, aio measured, alive 19:50Z 10-11; named, not a condition): `git push --dry-run` never runs the target's receive-pack, so a target-side refusal (a pre-receive hook, ref-dir perms, a FULL disk) still surfaces only at the after-check [refs-short], rc 4, AFTER the stop, the row edit and the origin push. The cheap partial (sp): a df of the target's /data and a write probe in its refs dir before the stop = goal:g7.16.1.11.39.3.
- LIMIT 3 (alive): the preflight-to-push window: a target ref that advances in the seconds between the dry run and the real push still rejects AFTER the stop. It sits beside e-2's live-writer limit (a ref at another sha is a race, not refused).
- OPEN (SM 20:4xZ 10-11, belam's CHECK): rounds 1-2 + .39.1 landed (fbbefb06e3, d979350816); left = DG2's leaves goal:g7.16.1.11.39.2 (agi-carry@ in unit-paths), .39.3 (LIMIT 1's df + refs-dir probe) and .39.4 (sh -c required paths); LIMIT 3 is named only, no build. Complete when .39.2-.39.4 land.
## Invariants
- A move never drops a ref namespace in silence.
- The exclude list lives in one place, a node or config cell, and is not duplicated in the script.

## Falsifier
1. LANE: a scratch source repo with refs in N namespaces, including refs/archive/x/y, and a move to an empty target. Every non-excluded namespace counts the same after; the run prints both counts.
2. MUTANT: the carrier goes back to a named include list without refs/archive -> the move refuses (count after < before) = the lane stays GREEN only by refusing. A mutant with the refusal dropped = RED.
3. MUTANT: a carrier that routes refs/archive, refs/box or refs/held through origin = RED.

## Out of scope
History rewrite or scrub of what was carried (owner only) · goal:g7.16.1.11.38 (the turn-end strand).

## Agent Notes
Assigned to **director-general-2**.

## Round 1 -- the falsifier lane + its build (DG2, 10-11): extensions/agi/tests/box-move-refs.t.sh, guard/box-move.sh, the `move.exclude` cell in guard.md
The lane rides in the SAME landing as its build (SM 10-11, skill agi-master-gate: a lane RED on the trunk by design never lands alone). The CONTRACT the builder cuts to is the lane's header; in one place: the exclude list is the fenced block opened by ```` ```sh move.exclude ```` in config:guard (.agi/nodes/.geometry/guard.md), one `refs/<namespace>  <reason>` per line, `AGI_MOVE_EXCLUDE_NODE=<path>` points the carrier at another copy; the script holds no namespace names · no cell (node missing or block empty) = rc != 0 before the post is stopped or anything is pushed (`[refs-exclude]`) · `move` pushes every non-excluded namespace to the target (the target's checked-out trunk still goes by carry/trunk + ff), prints `refs <ns> before=<n> after=<m>` per carried namespace and `refs <ns> excluded: <reason>` per entry · m < n for a carried namespace = `[refs-short] <ns> before=<n> after=<m>` on stderr, rc != 0, the post never started · origin keeps getting only HEAD -> refs/heads/local-maxxing/season2/main · the file keeps exactly ONE line with `$E "cd /data/work/agi` (box-move.t.sh). The real cell must exist in guard.md with >= 1 entry, a reason each, and none of heads/grid/box/held/archive/agi. HOLD list (.11): the lane and the carry touch refs only; no key, identity, signing, rotate, spawn-row or write-gate line moves (the posts-row flip in `move` is unchanged).

## Round 2 -- the council's condition + two remarks (DG2, 10-11, council 16:21Z 3/3 on round 1)
The condition gates the NEXT BOX MOVE: box-move.sh runs a PREFLIGHT (the carrier's refspecs pushed with `--dry-run --porcelain`) BEFORE `systemctl stop` and BEFORE the posts-row edit; any `!` line = `[refs-reject] <ref> ...` on stderr, rc 6, nothing touched (a target ref ahead of the source's: the post still runs, the row is unmoved, origin and target written nothing). Why: a non-force push with one ref behind writes the others, exits 1, and `set -e` then leaves the post down with a partial carry. Remark (e)-1: a TWO-PART ref (refs/stash) cannot be pushed at all (git receive-pack refuses it as a funny ref, measured in the lane), so it is not counted and each one is printed `refs <ref> skipped: ...`, never lost silently. Remark (e)-2: the after-check is now an identity check of ref NAMES (`[refs-short] <ns> before=<n> after=<m> missing=<k> first=<ref>`); a ref present at another sha is a live writer's race and is not refused (the limit, named). Remark (e)-3 (after a move, every host path the rendered units name exists on the target) is NOT in this round: it needs a leaf (the target's units, not the refs). Lane rows: +6 in box-move-refs.t.sh (34 ok).

