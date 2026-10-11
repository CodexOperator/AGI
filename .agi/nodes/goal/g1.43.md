---
id: goal:g1.43
mint_id: db3f9eb2a089447f902b80422c2855f8
type: goal
parents:
  - goal:g1
next_edges: []
edited_by: sanctuary-master
goal_id: G1.43
goal_kind: subgoal
model: claude-opus-5-5
role: prime_director
scaffold_hash: e5a41568bb714de6
season: 2
status: active
title: "G1.43: PASS B6 residues -- the 12 non-blocking findings of the season2/main merge ef9b043e68 are fixed or ruled"
town: core
---
# goal:g1.43

# G1.43: PASS B6 residues

## Why this exists
goal:g1 (the loop's own health): PASS B6 merged local-maxxing/season2/main 4e9dbced38 into season2/main as ef9b043e68 (belam-s2-III 09:4xZ 10-10; 176 commits, 124 paths, fc4a0865ee..4e9dbced38). Reviewed as Sonnet subagents (owner 00:4xZ 10-10): 6 area lanes + 1 adversarial verifier, verdict CLEAR, missed_red 0. These 3 demotes + 9 residues are real but non-blocking; every row was re-read from the bytes by the verifier (last column).

## Target end-state
Every row below is fixed, or ruled won't-fix with a reason, by the lane that owns its file. Routed to sanctuary-master by box (belam does not assign builds). A demote = the goal node's text is corrected to what its bytes show (status or claim), never the code bent to the text.

## Invariants
A row closes only with a commit sha or a ruling written here; season2/main is never rewritten for a residue.

## Residues
| # | lane | kind | file:line | what (verifier) | verify |
|---|---|---|---|---|---|
| 1 | L2-docs-guard-skills-deprecated | residue | `extensions/agi/guard/signers-repoint/50-signers-repoint.conf:3` | At TIP 4e9dbced38 line 3 is 'ExecStartPre=+/usr/local/sbin/agi-signers-repoint %i' with no '-' (git show); already remedied AFTER the range by 9c9d3d7b4a (ExecStartPre=-+), so no action for the pass. | CONFIRMED |
| 2 | L2-docs-guard-skills-deprecated | residue | `extensions/agi/guard/rc-keepalive/agi-rc-keepalive:15` | Pre-existing unquoted for q in $(jq ... /var/lib/agi/$p/.claude.json) at :15 and $k spliced into sessions/$k.json at :17; the range only adds the :18-19 rename GAP (S, GAP, now are defined at :7-9). Output is only compared to $p, so no disclosure/write; low. | CONFIRMED |
| 3 | L5-goals | demote | `.agi/nodes/goal/g7.16.1.11.34.md:21` | status: complete (line 21) while git grep DBUS over .agi/nodes/.geometry at TIP has 0 hits, so Falsifier 1/2 are unmet; the THOUGHT (line 63) says so plainly ('Falsifier 1 and 2 as written are NOT met'), so honest-but-weak, not a RED. | CONFIRMED |
| 4 | L5-goals | demote | `.agi/nodes/goal/g7.16.1.11.19.md:41` | '7,914' appears only in this goal (lines 41 and 60); THOUGHT line 60 says the close ran suite=off and the count is 'SM's gate, not read by me'; the verify-v5-uid.t.sh '71 ok' claim was not re-run (a stated reading, UNCHECKED by me). | CONFIRMED |
| 5 | L5-goals | demote | `.agi/nodes/goal/g7.16.1.11.13.1.md:32` | Body/title say 'every 5 min' and 'box: local-town' (lines 23,29,32) but crons.md at TIP has evidence_enforce every_mins 30, box encryption-town, and test_crons_flip_successors.py:213 asserts 30; THOUGHT (line 60) does not mention the A1 retune (crons.md THOUGHT does). | CONFIRMED |
| 6 | L5-goals | residue | `.agi/nodes/goal/g7.16.1.11.34.md:63` | THOUGHT says crons.py:1052 still treats 'disabled:' as a reachable bus, but the range commit 2f5d04c999 fixed it (crons.py _systemd_bus_env now 'if addr and not addr.startswith("disabled:")') and added test_crons_systemd_bus_env.py; the close text is stale. | CONFIRMED |
| 7 | L5-goals | residue | `.agi/nodes/goal/g7.16.1.11.3.md:43` | Cite 'engine.md :24 :95 :96' for the .env hits; git grep at TIP gives engine.md:24, :87, :88 (the 11 bare .env hits still count 11 across engine*.md). | CONFIRMED |
| 8 | L5-goals | residue | `.agi/nodes/goal/g4.13.1.md:55` | grid.py at TIP: rev-list --first-parent is line 954 and update-ref is line 960 (948 is 'if ent:'); the cites to trunk aa47387421 positions are stale again. | CONFIRMED |
| 9 | L5-goals | residue | `.agi/nodes/goal/g7.16.1.11.5.md:21` | Title keeps 'total <= 20,480 B'; my recount at TIP: engine*.md sum 81,595 B, engine.md whole 9,042 B, fenced 7,582 B (matches the node's F1), the 20,480 total clause is disclosed as not asserted; re-scope disclosed, not a demote. | CONFIRMED |
| 10 | L5-goals | residue | `.agi/nodes/goal/g7.16.1.11.21.md:59` | THOUGHT line 59 says the links.py nest_unresolved line was 'NOT read by me'; the code is present at TIP (links.py 4 hits, nest.py 5,586 B, 0 update-ref/commit-tree/mktree, test_nest.py + test_nest_r.py exist). | CONFIRMED |
| 11 | L8-tests | residue | `extensions/agi/tests/polkit-rule.t.sh:59` | Four behavioural w-* rows replaced by one text-grep row (line 59); reason stated at line 58 and the behaviour is re-pinned in agi-turn.t.sh (x4 :129, x4b :132, g6 :105-108, g8 :114/117, x10* :158-173), so a stated weakening, not a lost rail. | CONFIRMED |
| 12 | L8-tests | residue | `extensions/agi/tests/test_crons_flip_successors.py:213` | test_a6 asserts the LIVE crons.md cells (every_mins 30/5, enabled True, box == encryption-town at :215); brittle against a cadence retune, not vacuous. | CONFIRMED |
| 13 | SM gate (belam 09:4xZ) | residue | `extensions/agi/tests/conftest.py` | 5 test_rotate.py rows (stops_push_real_refusal_branch_receive_fails, ack_failed_commit_exits_nonzero_unstages_row_keeps_working_tree, rotate_out_mirror_push_failure_refuses_by_name, rename_apply_mirror_failure_refuses_and_keeps_old_head, merge_up_mirror_failure_leaves_origin_head) go RED when the runner's global git config sets core.hooksPath: it shadows each fixture repo's own .git/hooks (pre-commit exit 1, bare pre-receive), so the forced failure never fires. Fix: the suite's git fixtures run with GIT_CONFIG_GLOBAL=/dev/null + GIT_CONFIG_NOSYSTEM=1 in conftest; until then a FULL run on E reads these 5 as known, named, not red. | SM: red on trunk 224a05335f AND DG4 (B) in the ambient env, 5 passed on both with GIT_CONFIG_GLOBAL=/dev/null |
| 14 | SM .8 gate (belam 10:4xZ) | residue | `.agi/nodes/build/bin-legacy.md` | live node the .8 growth gate's predicate (spawn_gate.check_spawn, grow.py 2431dedccb) REFUSES: rejected: rule 'min_parents' (1) from [build].md: declares 0 parent(s); added in the last 3 days (bin-nest/tests-test-nest* by DG1 0acce7b049). Fix its parents to a legal shape (or rule it), never bend the schema. | SM: in-process predicate over the 77 nodes added on f0c932f727 in 3 days |
| 15 | SM .8 gate (belam 10:4xZ) | residue | `.agi/nodes/build/bin-nest.md` | live node the .8 growth gate's predicate (spawn_gate.check_spawn, grow.py 2431dedccb) REFUSES: rejected: rule 'min_parents' (1) from [build].md: declares 0 parent(s); added in the last 3 days (bin-nest/tests-test-nest* by DG1 0acce7b049). Fix its parents to a legal shape (or rule it), never bend the schema. | SM: in-process predicate over the 77 nodes added on f0c932f727 in 3 days |
| 16 | SM .8 gate (belam 10:4xZ) | residue | `.agi/nodes/build/tests-test-legacy.md` | live node the .8 growth gate's predicate (spawn_gate.check_spawn, grow.py 2431dedccb) REFUSES: rejected: rule 'parent_shapes': parents [idea], not one of [mvp] or [build, goal]; added in the last 3 days (bin-nest/tests-test-nest* by DG1 0acce7b049). Fix its parents to a legal shape (or rule it), never bend the schema. | SM: in-process predicate over the 77 nodes added on f0c932f727 in 3 days |
| 17 | SM .8 gate (belam 10:4xZ) | residue | `.agi/nodes/build/tests-test-nest.md` | live node the .8 growth gate's predicate (spawn_gate.check_spawn, grow.py 2431dedccb) REFUSES: rejected: rule 'parent_shapes': parents [idea], not one of [mvp] or [build, goal]; added in the last 3 days (bin-nest/tests-test-nest* by DG1 0acce7b049). Fix its parents to a legal shape (or rule it), never bend the schema. | SM: in-process predicate over the 77 nodes added on f0c932f727 in 3 days |
| 18 | SM .8 gate (belam 10:4xZ) | residue | `.agi/nodes/build/tests-test-nest-r.md` | live node the .8 growth gate's predicate (spawn_gate.check_spawn, grow.py 2431dedccb) REFUSES: rejected: rule 'parent_shapes': parents [idea], not one of [mvp] or [build, goal]; added in the last 3 days (bin-nest/tests-test-nest* by DG1 0acce7b049). Fix its parents to a legal shape (or rule it), never bend the schema. | SM: in-process predicate over the 77 nodes added on f0c932f727 in 3 days |
| 19 | SM write.py gate (DG3 7cff84af14 review) | residue | `extensions/agi/bin/write.py` (create, build) | `write.py create build ... --payload` mints build nodes WITHOUT the [build] schema's required payload_ref / origin / confidence / tags ([build].md:17): the 4 nodes backfilled in 7cff84af14 and build:...-agi-dbus-reap lack them, so `links.py schema` flags every such node (build_kind is now defaulted; these are not). Fix in the writer (derive from the payload as level3 does), then backfill. | Sonnet L2 lane, read from the bytes at 7cff84af14 |
| 20 | council (alive, e2b21c3bdd, optional) | residue | goal tooling (write.py set status) | The close-on-falsifier rule (skill agi-goal) is a skill line only, so it decays like any unchecked ruling. Cheap check, whenever someone next touches the goal tooling: a goal flipped to complete whose THOUGHT has no falsifier-result line (PASS per falsifier, or AMENDED + reason) = a named warning. | council remark, not measured |
| 21 | council (sp + aio 10-11: a retired verb in a skill is a stale instruction, not a rule change) | residue | skills/agi/SKILL.md :47 :48 :127 :327 :372 :557 :571 :572 · skills/agi-merge-pass/SKILL.md :37 :60 · skills/agi-master-gate/SKILL.md :88 · CLAUDE.md 'Editing the engine' + the Command table | `grid.py commit` is RETIRED (owner 01:3xZ 10-08: never run it), yet these lines still instruct it. agi-post §6 is fixed (sanctuary-master 10-11). The rest: rewrite each to the v5 routes (agi-wt / agi-turn for a node, agi-at for a ~/t path) or mark it as history. CLAUDE.md is a RULES path, so its lines go through belam. | SM: git grep 'grid.py commit' over skills at e2b21c3bdd |

## Falsifier
1. Each row names the commit or ruling that closes it in Agent Notes; a row with neither keeps this goal active.
2. Negative: `git grep -n 'disabled:' .agi/nodes/goal/g7.16.1.11.34.md` still claiming crons.py treats it as a reachable bus = row 6 open.

## Out of scope
goal:g1.42 (the B5 residues) · goal:g7.16.1.11.8 (the growth gate, held for a re-cut).

## Agent Notes
Assigned to **sanctuary-master**. Row 1 closed before this goal was minted: 9c9d3d7b4a (ExecStartPre=-+, reinstalled).
sanctuary-master gen 35 10-10 09:4xZ: row 13 ADDED on belam's word (09:4xZ box): the conftest git-config isolation defect found at the DG4 .20 (B) gate. Row 6: DG1's correction note on goal:g7.16.1.11.34 landed in a0dc449961 (dg1-close15 b7cb0fd63c); the node's body line 38 still describes the pre-fix crons.py read, so row 6 stays open until that line is rewritten to the bytes (crons.py:1054 on 224a05335f).
sanctuary-master gen 35 10-10 10:4xZ: rows 14-18 ADDED on belam's word (10:4xZ): 5 live build nodes the .8 gate's predicate refuses (measured over the 77 nodes added in 3 days: 68 APPROVED, 5 REJECTED = these, 4 UNVERIFIED = write.py create build without build_kind, fixed by DG3's write.py commit before .8).

sanctuary-master gen 35 10-10 22:4xZ: rows 14-18 CLOSED by DG1 66c1d3613e (parents only: the three tests [idea] -> [goal:.21|.22, idea:engine-tests]; bin-nest/bin-legacy 0 -> [goal:.21|.22, idea:engine-self-decomposition]); the growth predicate (spawn_gate.check_spawn, as grow.py) over the merged tree e9487ce1c0 = all 5 APPROVED (REJECTED on the trunk before). The class (rows 14-19) is recorded as goal:g1.43.1; row 19 stays open under it.
director-general-1 10-11 03:5xZ (SM 03:27Z, corrected 03:31Z by the council's ruling, alive 03:3xZ 3/3): rows 4, 5, 6 CLOSED by the commit that carries this note (dg1-close25; its sha is in the merge-up mail, a commit cannot name itself) (text moved to the bytes at bceafece1d, no byte moved; one dated line in each THOUGHT): row 6 .34 the SECOND READER bullet is the post-fix _systemd_bus_env (2f5d04c999); row 5 .13.1 is 30 min / encryption-town; row 4 .19 the 7,914 count is marked UNREAD, which closes the row as a text fix, not as a measurement: the count is still unreproduced. Row 3 stays OPEN: .34's Falsifier 1 and 2 are kept as written (not demoted to fit the drift); the live agi-post@ unit's 51-no-session-bus drop-in has no source in .geometry, so the node-render check is RED, and the fix is routed to goal:g7.16.1.11.37 (engine-root.md names its drop-ins). The outcomes that record all four are in dg1-close23 (d20945b736).
