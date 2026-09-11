---
id: hypothesis:l4-heal-death-past-deadline-branch-has-a-test
mint_id: 56638e0e11604d4394a765c08625d1c4
type: hypothesis
parents:
  - goal:g15
  - hypothesis:l4-the-reaper-is-one-persistent-service
next_edges: []
edited_by: sanctuary-director
scaffold_hash: dd653938f7c67fd1
season: 2
testable_claim: "OWNER 2026-09-11 05:1xZ: bugfix findings are g15 hypothesis nodes fixed in-loop. Re-filed from goal:g17.1 (merge-up 26 residue (b), L4.123 = hypothesis:l4-the-reaper-is-one-persistent-service). CLAIM: heal.py's death-past-deadline branch (`extensions/agi/bin/heal.py:317-336` on db9b3d573 -- inside `for agent_id in outcome[\"still\"]`, the `if pid > 0 and not adapter.is_alive(pid)` death record + manifest update + ONE `death` dm + the `marked DEAD past deadline` watch line) is UNTESTED: the existing `test_watch_dead_pid_past_deadline_is_a_death_not_timeout` (test_heal_watch.py:219) uses a pid dead from the start, which `_reap_pass` reaps into `outcome[\"died\"]` (heal.py:275-287), so :320 is never reached. A test that exercises EXACTLY the transition -- the pid ALIVE at the reap pass (left in `still`) and DEAD by the timeout check -- lands in extensions/agi/tests/test_heal_watch.py: an adapter (or monkeypatched `is_alive`) that returns True on the first call for that pid and False afterwards, a round past its `timeout_seconds` (started_ago > timeout_s); ASSERT agent.json status=failed + fail_reason `pid N died (detected by reaper)` + finished_at set, the manifest entry status/finished_at/fail_reason updated, EXACTLY ONE dm to the dispatcher with reason=death and NO reason=timeout, the watch log line contains `marked DEAD past deadline`, and a SECOND pass does not re-dm (the L4.123 double-dm guard). Also assert the sibling path is untouched: the same setup with the pid alive at BOTH checks still records the timeout (not a death). FALSIFIER: the new test passes with :320-336 deleted (prove it fails on a mutated copy, paste the run). heal.py is edited ONLY if the new test exposes a defect in that branch -- say so in the experiment with the failing run; otherwise heal.py is byte-identical. CEILING: 1 kid. FILE SCOPE: extensions/agi/tests/test_heal_watch.py (+ heal.py:317-336 only on a proven defect). EXCLUDED: dispatch.py, rotate.py, crons.py, the live reaper unit (agi-agi-reaper-2f118e6f.service is the prime's; never `heal.py watch` against the live sessions dir -- fixtures only). Disjoint from the rotate.py and crons.py g15 rounds; runs in PARALLEL with them."
title: heal.py death-past-deadline branch (alive at the reap pass, dead by the timeout check) is covered by a test
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-heal-death-past-deadline-branch-has-a-test

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
