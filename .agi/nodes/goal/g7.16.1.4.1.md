---
id: goal:g7.16.1.4.1
mint_id: f32967f231364c1ba2b30a79bbcf0b5a
type: goal
parents:
  - goal:g7.16.1.4
next_edges: []
confidence: 0.6
edited_by: belam
goal_id: G7.16.1.4.1
goal_kind: subgoal
heading_level: 5
origin: goals-doc
scaffold_hash: 9fd181800bc6f0da
season: 2
seeds: []
status: active
tags:
  - council-loop
  - bundle-4
  - local-maxxing
title: "G7.16.1.4.1: GOALS.md is retired in ONE row -- the render and its check leave every live caller, the only GOALS.md-to-node deletion path goes, the smoke keeps its node count, every reader names the one goal read (row W-G; assigned: director-general-1)"
town: core
---
# goal:g7.16.1.4.1

## Why this exists
goal:g7.16.1.4 row W-G, moved UNBUILT from goal:g7.16.1.3 row G (council 20:2xZ; the OWNER 17:3xZ order is verbatim on goal:g7.16.1). Measured 20:3xZ 09-29 at ddea3a61f (the bundle's SM-clean base): GOALS.md is tracked; the live render callers are driver.sh:240 (every --smoke), the rotation closeout step "render" (rotate.py:8754, handler :9370-9386, whose --check verdict refuses the closeout) and workflows/agi-round-review.js:64; `--from-doc` (snapshot-goals.py:1123/:1135) with its unlink (:1256) is the only code that turns GOALS.md into goal-node deletions; node_writer.py:76-80 keeps `goal` out of CANONICAL_NODE_TYPES on the regenerate-from-GOALS.md reason; locations.py:86 DEFAULT_GOALS_FILE + the goals_file cell (:706). GOALS.md is named in 16 code files, 12 test files, 5 skills, CLAUDE.md and QUICKSTART.md.

## Target end-state
- No live code path renders or checks GOALS.md (6 callers): `driver.sh --smoke` keeps snapshot + metrics and still prints the node count (the Prime's [red] 18:00Z: the node-count floor never goes blind); the rotation closeout drops its render step AND its --check gate together (with their row in test_rotate_closeout_steps.py); agi-round-review.js and review.json drop the item; the WORKTREE closeout step `render_check` (rotate.py:8733, handler :9185-9196) drops with the Prime step; verification.py's `goals-check` leaves LEVELS quick/rotation/full (:70-73), which the closeout reaches through post_verify / suite / verify_stamp. Six live callers in all (experiment:dg2b4-wg-baseline, 20:4xZ), not the three this leaf first named.
- `snapshot-goals.py --from-doc` and its unlink retire; node_writer's reason for keeping `goal` out of CANONICAL_NODE_TYPES is restated true or `goal` is admitted; the goals_file cell and DEFAULT_GOALS_FILE retire with their readers.
- GOALS.md leaves by `git rm` of the DERIVED file only; no goal node is touched.
- Built in two commits: W-G.1 41107692f (every caller, the gate, the readers, git rm GOALS.md) and W-G.2 254f58ef7 (the unreachable renderer, the doc import, goals_path); mvp:dg3b4-wg1-goals-md-retired + mvp:dg3b4-wg2-dead-renderer-retired. The 5 W-G strict-xfail rows are green at 254f58ef7; residues 81-85 closed at 9eaf5992f. The leaf stays active until SM's re-review is clean.
- Every reader line (CLAUDE.md, QUICKSTART.md, skills agi, agi-goal, agi-master-gate, agi-node-write, agi-verify) names the ONE goal read that exists when this row lands (today `write.py goal:<id> 'read body N:M'`). goal:g4.18.7.3 moves that same line with every other teacher, so there is never a second read surface.

## Invariants
- No half-retire: until this row lands the render and --check stay live, and a red --check is this row's by name, never waived.
- active + deprecated node count never drops; no goal node is deleted.

## Falsifier
1. `git ls-files GOALS.md` prints nothing · `git grep -n 'snapshot-goals.py --render' -- extensions ':!extensions/agi/tests'` prints 0 · `bash extensions/agi/driver.sh --smoke --max-iters 1` exits 0 and prints a node count · one rotation closeout runs clean.
2. Negative: `git grep -n 'GOALS.md' -- CLAUDE.md QUICKSTART.md skills extensions/agi/bin extensions/agi/driver.sh` prints only retirement pointers (no exclusion: goal:g7.16.1.4.1.1 retired the three one-repo migration tools and closed) · `git grep -n -e '--from-doc' -e 'from_doc' -- extensions/agi/bin/snapshot-goals.py` prints 0.

## Out of scope
goal:g4.18.7.3 (the read cut) · goal:g7.16.1.3.5 and its .1 .2 (the bundle-3 leaves this row supersedes)

## Agent Notes
Assigned to **director-general-1**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Falsifier 2 exclusion dropped by director-general-1 at 00:5xZ 09-30, as goal:g7.16.1.4.1.1's end-state asks: that leaf closed on DG2 verdict:dg2mvp-l2a PROVED 0.9 (unify.py + verify_unified.py b8d232fc6, publish-engine.sh de5507a17). F2 without the exclusion, run by DG1 at HEAD: 17 GOALS.md hits, every one a retirement pointer; --from-doc/from_doc 0; F1 greps: GOALS.md untracked, --render outside tests 0. Status stays active: the end-state holds this leaf until SM's re-review is clean (the smoke run and one clean rotation closeout are SM's to read). DG2's W-G corrective verdict:dg2mvp-wgR PROVED 0.9 closed the schema half (hypothesis:node-type-schemas-name-a-thought-reader-that-exists).
<!-- THOUGHT:END -->
