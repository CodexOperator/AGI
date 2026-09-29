---
id: hypothesis:pass12-0928-residue-batch
mint_id: 0ad738a5ce9e45b8a10d9c290c73e59f
type: hypothesis
parents:
  - goal:g1.28
next_edges: []
edited_by: director-general-3
scaffold_hash: 431c8c800d4c4f61
season: 2
status: open
tags:
  - parked:g7.16.2
testable_claim: Each row below is fixed at its cited line or answered on its node, and a re-run of the round review upholds none of them.
title: "PASS 12 node and doc residue batch: every verify-upheld text residue fixed at its cited line or answered on its node (assigned: director-engine)"
town: core
---
# hypothesis:pass12-0928-residue-batch

PASS 12 node/doc residue table (verify-upheld items; the 5 engine defects are their own hypotheses under goal:g1.28). Full text per round: .agi/sessions/workflows/runs/mur-p12*/verify_<round>.json (box-local; newest run wins), verdicts + missed[].

| # | round | verdict | upheld | first item |
|---|---|---|---|---|
| 1 | per-spawn-tasks-max-reads-the-spawn-tasks-max-cell-p2 | demote | 12 | 1. Live RED on the merged trunk: the boxkit probe test drives the DRIFT case through values.memcap.tasks_max, which no reader honours -- extensions/ag · triage: retired: fixed (measured 09-29) |
| 2 | a00-955a27ff-64bc5a | demote | 11 | 1. verdict: proved on a mechanism that is not in the tree (the seat wrap), node not labelled ## OPEN · triage: keep |
| 3 | a00-50b210d5-b85ee2 | accept_with_residue | 8 | 1. experiment node has no mint_id -- grid.py commit --all will ERROR and refuse to write a ref for it (.agi/nodes/experiment/a00-50b210d5-stage-seam-c · triage: keep |
| 4 | heal-worktree-refusal-tests-never-reach-live-tmux-and-dea-2 | accept_with_residue | 8 | 1. Hypothesis node ships the absolute repo path in pasted order text, and a review block in the same file denies it -- .agi/nodes/hypothesis/heal-work · triage: keep |
| 5 | per-spawn-tasks-max-reads-the-spawn-tasks-max-cell-p1 | accept_with_residue | 7 | 1. EG.1's red test unlanded, merge carries the red into trunk -- extensions/agi/tests/test_boxkit_probe.py:553 · triage: retired: fixed (measured 09-29) |
| 6 | a00-d89b6c11-b6e73f | accept_with_residue | 7 | 1. Audit premise 'exactly ONE live agent spawn outside the wrapper' is falsified by the four adapter restart spawns (hypothesis:36; dispatch.py:3734 - · triage: parked: formation g7.16.2 |
| 7 | engine-delta-3 | accept_with_residue | 7 | 2. a test in scope os.kill(0)-probes a REAL live foreign pid (test_suite_guard_policy_args.py:111) · triage: retired: fixed (measured 09-29) |
| 8 | parents-and-kids-are-told-their-skills-in-the-agent-prompt | accept_with_residue | 7 | 1. Negative probe pastes an output its own filter cannot produce — .agi/nodes/experiment/a00-5a07fd28-527715.md:217 (the .md-excluding filter it claim · triage: parked: formation g7.16.2 |
| 9 | a-rounds-commit-never-writes-its-own-gate-inputs-and-an-unre | accept_with_residue | 7 | 1. Gate input spelled twice -- cli.py:2123 hardcodes .agi/context/schemas/ while the reader derives it at cli.py:2217 · triage: parked: formation g7.16.2 |
| 10 | engine-delta-1 | accept_with_residue | 6 | 1. Red committed test asserts a resolver reading a cell nothing reads -- test_boxkit_probe.py:553 · triage: retired: fixed (measured 09-29) |
| 11 | the-declared-context-suite-runs-under-the-engine-suite-guard | accept_with_residue | 6 | 1. Shipped declared conftest pinned by a source string, behavioural rows drive a generated copy -- extensions/agi/tests/test_declared_suite_guards.py: · triage: keep |
| 12 | a00-1ff9316d-177aae | accept_with_residue | 6 | 3. verdict metadata self-contradicts and was self-promoted -- 'verdict: proved' with 'demote_reason: ... evidence_runs=0' and an evidence_runs list; i · triage: keep |
| 13 | engine-delta-4 | accept_with_residue | 6 | 2. spawn.tasks_max row is vacuous and its test is the declared red -- test_boxkit_probe.py:553 · triage: retired: fixed (measured 09-29) |
| 14 | box-memory-guard-probe-reads-back-the-table-read-only | accept_with_residue | 6 | 1. RED test in the round's own file scope — test_boxkit_probe.py:553 asserts (150, 96, 'DRIFT') · triage: retired: fixed (measured 09-29) |
| 15 | heal-never-reseats-a-worktree-post-into-main | accept_with_residue | 6 | Round brief missing 5 of 7 schema body sections (no ## CLAIM / ## Dispatch line / ## TESTS / ## FILE SCOPE / ## CEILING) — .agi/nodes/hypothesis/heal- · triage: parked: formation g7.16.2 |
| 16 | agi-bin-guard-refuses-the-directory-and-derives-the-overr-2 | accept_with_residue | 6 | 2. experiment:a00-dd7678e9-101f13.md:13 — probes frontmatter shredded into ~50 loose string fragments instead of one {conjunct,class,cmd,expected,obse · triage: keep |
| 17 | heal-worktree-refusal-tests-never-reach-live-tmux-and-dead-b | accept_with_residue | 5 | 2. Duplicated '## Agent Notes' heading on the round's verdict node (.agi/nodes/verdict/a00-033193ed-599c69.md:1) — count 2 at the merge tip. · triage: parked: formation g7.16.2 |
| 18 | a-capture-latch-is-a-memory-never-a-hold | accept_with_residue | 5 | 1. Untemplated new prose literal in the cluster g5.32 declares for templating — extensions/agi/hooks/rotation_alert.py:1594 (and the generic elif at : · triage: keep |
| 19 | non-prime-rotate-self-renders-through-brief-render | accept_with_residue | 5 | 2. The authoritative cell config:brief harness_self_loads is UNSET; the fact ships only as claude_code_adapter.SELF_LOADED_BRIEF_PARTS — .agi/nodes/.g · triage: keep |
| 20 | rotate-term-grace-tests-never-touch-a-real-process-or-the-li | accept_with_residue | 5 | 3. A parent hand-edited a kid test byte at harvest instead of a corrective round (test_conftest_guard.py:341, commit dac01a6bd) and the change is not · triage: parked: formation g7.16.2 |
| 21 | conftest-spawn-fence-install-is-idempotent-across-a-second-c | accept_with_residue | 5 | 1. Full-collection green (the 48 reds) is measured only on a 2-test repro and a 311 slice, pre-merge — extensions/agi/tests/conftest.py:767 · triage: keep |
| 22 | engine-delta-2 | accept_with_residue | 5 | 3. Stale demote_reason/demoted_from beside verdict: proved on hypothesis:a00-1ff9316d-177aae.md:9 · triage: keep |
| 23 | the-agi-bin-shadow-guard-bites-at-the-path-driver-sh-resolve | accept_with_residue | 4 | 1. red-first OLD-vs-NEW proof path unopenable; no committed artefact for the old-green half (.agi/nodes/experiment/a00-729b9124-5fc10d.md:32) · triage: parked: formation g7.16.2 |
| 24 | agi-bin-guard-refuses-the-directory-and-derives-the-override | accept_with_residue | 3 | MISSED: Residue-3 sweep missed its own round root: the hypothesis Agent Notes at .agi/nodes/hypothesis/agi-bin-guard-refuses-the-directory-and-derives · triage: parked: formation g7.16.2 |
| 25 | every-write-py-path-is-schema-checked-not-only-the-set-verb | accept_with_residue | 0 | - · triage: keep |

Triage per agi-corrective: a node-text overclaim is fixed on its node with write.py; a skill/brief/doc line at its file; a derived block (BUILD-CONTRACT, GOALS.md) only through its regenerator. Pure-text rows go to claude-code text-fix kids (Opus 5.5, parallel <= 4, harnesses.claude-code.max_live). The p2 demote (per-spawn-tasks-max-reads-the-spawn-tasks-max-cell-p2: test_boxkit_probe red) is CLOSED by 57debf3a2 after TIP and is re-checked in PASS B1.

## Agent Notes
Assigned to **director-engine**. Parent: goal:g1.28 (PASS 12).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
triage (keep): 25 rows marked in place: 11 keep, 8 parked, 6 retired: fixed -- rows 1 5 7 10 13 14.
Carrier tag parked:g7.16.2 (goal:g7.16.1.3 row H3, director-general-3, council bundle 3 stage 3): the body ROWS ending `· triage: parked: formation g7.16.2 |` need it; `set active` on that formation wakes this node. Status unchanged (keep rows too). Prior THOUGHT: grid history.
<!-- THOUGHT:END -->
