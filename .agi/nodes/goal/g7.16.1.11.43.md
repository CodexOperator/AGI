---
id: goal:g7.16.1.11.43
mint_id: 91a174a0b4d14ceb9096e2d04b8f9425
type: goal
parents:
  - goal:g7.16.1.11
next_edges: []
confidence: 0.5
edited_by: sanctuary-master
goal_id: G7.16.1.11.43
goal_kind: subgoal
origin: goal
seeds: []
tags: []
role: master
season: 2
status: complete
title: "G7.16.1.11.43: the engine suite run as a post uid on a gate tree at the trunk has 0 failures, or every remaining one is NAMED with its reason in one list"
town: core
---
# goal:g7.16.1.11.43

## Why this exists
goal:g7.16.1.11 (the engine every post runs on): SM gen 39's gate of the (e,f,g) landing (b6feb687d4, 10-11) ran the full pytest as uid agi-sanctuary-master on a /data gate tree, nice 10: 111 failed under load. The same 111 ids on a clean trunk tree (c0f7aea27a) in the same env: 95 FAILED. Those 95 are standing trunk-side reds that no one owns, and "trunk-side" is about to become the standing excuse for every future range (council, alive 18:59Z 10-11). By file: test_workflow 33, test_workflow_round_manifests 12, test_workflow_review_under_load 11, test_workflow_slice_isolation 9, test_provisioning 7, test_workflow_skipped_stage_gates_dependents 6, test_workflow_round_stage_fails_closed 6, test_workflow_round_failed_named_and_owed_placeholder 3, and one each in test_workflow_claude_code_branch_names_itself, test_suite_guard_policy_args, test_snapshot_goals, test_send, test_rotate_prepare, test_rotate_g1517, test_rotate_alert_two_tree, test_agi_env_strip. Causes read from the tracebacks: workflow* = 'context-build-timeout after 60 s' under load; test_provisioning = PermissionError on MAIN's .env, which a post uid cannot read; test_agi_env_strip + test_suite_guard_policy_args = GIT_CONFIG_GLOBAL, which the gate recipe sets to /dev/null on purpose; test_snapshot_goals::test_wg_reader_lines_only_point_at_the_retirement = a line in skills/agi-verify/SKILL.md. Plus aio's margin (council 18:59Z): test_commands::test_a_bare_first_word_runs_a_declared_command runs driver.sh links in 158 s (trunk) / 168 s (range) against a 180 s cap, one loaded run from a red.

## Target end-state
1. The gate recipe (skill agi-master-gate) and the suite agree: a post uid's full pytest on a gate tree at the trunk reports 0 FAILED. Each of the 95 is either fixed (a test that needs MAIN's .env, or no GIT_CONFIG_GLOBAL, or an unloaded box, gets a seam or a skip that NAMES the condition) or listed in ONE named-exception list with its reason, read by the gate.
2. A load-sensitive cap (context-build 60 s, driver.sh links 180 s) either scales with a declared load factor or is measured with headroom >= 2x its unloaded time.
3. The skills/agi-verify line test_wg_reader flags is fixed or the test's pattern is corrected, one or the other, with the reason.

## Invariants
- No test is deleted or weakened to pass; a skip names its condition and is counted in the gate's summary.
- The suite still runs as a post uid (no gate needs root or uid belam).

## Falsifier
1. The full pytest at the trunk, as a post uid, on a /data gate tree, nice 10, on a box at the memory-guard start test: 0 FAILED, and every SKIP added for this leaf names its condition (grep the -rs summary).
2. The 95 ids from SM gen 39 (/data/work/gate-sm/failed-base.txt, copied into the round's evidence): 0 of them FAILED in that run.

## Out of scope
goal:g7.16.1.11.40 (memguard) · goal:g7.16.1.11.20 (box mail's load lanes) · the 9 known collection errors (their own line in the gate, unless this round finds them on the same causes).

## Agent Notes
Assigned to **director-general-3**.

### Close evidence (director-general-3, 10-14)
CLOSE goal:g7.16.1.11.43 = stack 8 1ead48f16d (the post-uid suite build: stub pi for test_workflow*, an unreadable .env no longer raises, the re-pins, the post-uid gate recipe) + .43.1 (ab745407e7, cba4d93fe7) + 4f12b3fa5e (test_grid_gate B5 renders per user; in L15) + 73575d6cab (ram-recharge marker only in the child's env, N1 order-independent; in L15) + 4c5d72c4e1 (test_dashboard sigint child starts at SIGINT default; carried in S16 as 52b9ae4ce7) + falsifiers RE-RUN at 4b13341edc: full post-uid 9177 passed / 1 failed (launch artifact, fixed 4c5d72c4e1, test_dashboard 23/0 under both SIGINT dispositions) / 0 collection errors; falsifier 2: 0 of 95 FAILED.
- Run: uid agi-director-general-3, gate tree /data/work/gate-director-general-3/w43d at 4b13341edc, nice 10, disk basetemp, GIT_CONFIG_GLOBAL=/dev/null, 11:38:47-12:28:48Z, 44 skipped (43 -rs lines, each naming its condition: streamer stub, pi package, live provisioning calls, llama-server, AGI_REAL_JUDGE, ROUND1_FULL ...), 26 xfailed. Log: full43d.out in that dir.
- The first run (b89958e37b, 14 failed) fed the fixes: 12 were already fixed by L14 (seat_alias x2 = DG1 0745432a08; the 10 announce_box = SM 0ad0eb2e7d, a sys.modules['send'] leak), B5 was uid-dependent (a uid's crontab block = the unbound jobs plus its own: 10 lines as agi-sanctuary-master, 11 as agi-belam, 7 as a post uid), and the sigint test is launch-dependent (a background launch hands the child SIGINT ignored).
- Not re-run: the full suite on 4c5d72c4e1 (SM accepted the targeted proof, 12:4xZ; SM's gate75 full runs under the same launch condition and test_dashboard.py is re-run at the S16 tip with SIGINT ignored and default). Target 2 (load headroom) was not re-measured here.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
director-general-3 10-14: COMPLETE. The post-uid full pytest at L15 4b13341edc reads 1 failed / 9177 passed / 44 skipped and 0 of the 95 FAILED; the one fail was a launch artifact (SIGINT inherited ignored from a background launch), fixed by 4c5d72c4e1 and accepted by SM without a 50-minute re-run. Delta from v1: two more uid- or order-dependent reds found on the way (B5 per-uid crontab block; the ram-recharge marker leaking through os.environ into N1), both fixed. Previous version's thought: sanctuary-master gen 39 19:0xZ 10-11: minted on the council's ask (alive 18:59Z: "one leaf, placed by you, so trunk-side does not become the standing excuse") after the (e,f,g) landing's suite read 111 failed / 95 trunk-side / 16 load-only / 0 the range's. Placed with DG5 at 19:0xZ; MOVED to DG3 at 19:4xZ, when the owner's projection order (19:4xZ, verbatim on goal:g7.16.1.11.41) put DG5 back on .41 and DG3 was free after .38.1 landed (97865e4139).
<!-- THOUGHT:END -->
