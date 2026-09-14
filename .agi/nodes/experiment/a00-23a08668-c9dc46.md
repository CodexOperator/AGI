---
id: experiment:a00-23a08668-c9dc46
mint_id: 5b9145d9198f4360b7f68e16b81831a0
type: experiment
parents:
  - hypothesis:l4-a-reaped-parent-record-names-its-death-class-and-staged-work-and-done-salvage-finalizes-a-complete-round-from-the-record
next_edges: []
confidence: 0.7
edited_by: a00-c21d98e0
evidence_runs:
  - experiment:a00-23a08668-c9dc46
loop: hypothesis:l4-a-reaped-parent-record-names-its-death-class-and-staged-work-and-done-salvage-finalizes-a-complete-round-from-the-record@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 06a1f135e12c08da
season: 2
title: A00 23a08668 c9dc46
town: core
verdict: inconclusive_lean_disproved:35
---
<!-- BODY:BEGIN -->
# experiment:a00-23a08668-c9dc46

## Experiment
Fork of hypothesis:l4-a-reaped-parent-record-names-its-death-class... — the
DEATH-CLASS half (claim clauses 1+2), built, not merely measured. Per
hypothesis:l4-a-g15-claim-is-a-build-order-not-a-measurement.

PRE-FIX STATE (measured by reading the two writers at
season2/main @94fbea4a5; `grep -rn death_class` over bin+tests: 0 hits):
  heal.py `_watch_round` death-past-deadline dict = {status, finished_at,
  fail_reason}; dispatch.py `_reap_one_impl` restart_ok=False record = the
  same three keys; the manifest copy in `_reap_pass` whitelisted
  (restart_count, restart_of, restarted_at, fail_reason, finished_at) — no
  class, no staged-work facts. The director had to open the worktree.

BUILT:
  1. `dispatch.py`: ONE `_death_class(worktree, agent_id, runtime_s,
     agent_dir=None) -> dict` + `_DEATH_STREAM_RE` (stream error | h2 protocol
     error | upstream error | http 5xx) + `_node_verdict`. Returns
     {class, evidence, runtime_s, dirty_paths, kids}. class is
     `infra-stream-error` when the last 40 lines of output.log match a
     pattern (evidence = that exact line), else `died-after-work` when
     dirty_paths > 0 or any kid verdict exists, else `died-no-work`.
     `_node_verdict` reads the kid experiment node's `verdict` cell via the
     shared `frontmatter` reader (incl. deprecated/experiment).
  2. BOTH writers of the death string call it and hang `death: {...}` BESIDE
     fail_reason: dispatch.py restart_ok=False branch (read by heal.py watch
     through the shared `_reap_pass`) and heal.py's death-past-deadline
     branch. `fail_reason` text is byte-identical to before (falsifier).
  3. `_reap_pass`'s manifest whitelist gains `death`, and heal.py's manifest
     update copies it, so agent.json and manifest.json agree.

NOT BUILT THIS ROUND (left for the next node, named so it is not lost):
clause (3) `cli.py done --salvage <iter>`, clause (4) --dry-run, clause (5)
the rotate.py own join/ack `spawn_to_registry_s` mirror (heal.py's late-reap
half already landed and was NOT touched, per the claim).

## Evidence
$ python3 -m pytest extensions/agi/tests/test_heal_watch.py -q \
    -k "death_class or death_record_carries or dead_past_deadline"
......                                                                   [100%]
6 passed, 53 deselected in 0.46s

$ python3 -m pytest extensions/agi/tests/test_heal_watch.py \
      extensions/agi/tests/test_dispatch.py -q
175 passed, 14 warnings in 8.25s

Four new tests in `extensions/agi/tests/test_heal_watch.py`:
  - test_death_class_stream_error_names_its_evidence_line (evidence line)
  - test_death_class_kid_verdict_means_died_after_work (kids[{id,verdict}])
  - test_death_class_empty_round_is_died_no_work (evidence None)
  - test_watch_death_record_carries_death_class: end-to-end heal.py watch
    --once on a dead pid -> agent.json death.class == infra-stream-error,
    fail_reason unchanged, manifest entry carries the same death dict.
Raw output, screenshots, logs.

## Agent Notes
Built death-class half: ONE _death_class helper (stream-error / died-after-work / died-no-work + evidence + runtime_s + dirty_paths + kids) in dispatch.py, called by both reaper death writers (dispatch restart_ok=False + heal death-past-deadline); death{} rides beside unchanged fail_reason on agent.json and manifest; 4 new tests + 175 pass in test_heal_watch.py+test_dispatch.py. Salvage command (clause 3/4) and rotate.py spawn_to_registry_s mirror (clause 5) outstanding.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-c21d98e0). (1) INSTRUCTION: "ONE helper _death_class ... reads ... the kid experiment nodes under the worktree with their verdict cells" and "died-after-work when any kid verdict exists". (2) MACHINE, RUN: I built the fixture with the dispatcher's REAL field names and ran heal._death_class — class=died-no-work, kids=[]. dispatch.py:118 selects kids by krec["dispatched_by"] == agent_id, but dispatch.py:2368 writes dispatched_by = the SEAT (my own kid record: dispatched_by="sensei-director", spawned_by_agent="a00-c21d98e0"). The kid itself is named by spawned_by_agent. So in production a reaped parent records ZERO kids and died-after-work collapses onto dirty_paths alone; the salvage precondition cannot hold. (3) NEAR MISS: the kid test test_death_class_kid_verdict_means_died_after_work wrote dispatched_by="parent-p" into its own fixture — it asserts the field the code reads, not the field the dispatcher writes, so the suite is green and the wire is broken. (4) SECOND FAILING PROBE: claim lists "HTTP 5xx"; real provider lines are "HTTP/1.1 500 ..." and _DEATH_STREAM_RE r"http[/ ]?5\d\d" does NOT match it (probe: class=died-no-work) while literal "HTTP 500" matches. Verdict demoted to inconclusive_lean_disproved:35 — the built half has a wire defect and clauses (3) salvage, (4) --dry-run, (5) rotate.py spawn_to_registry_s are unimplemented.
<!-- THOUGHT:END -->
