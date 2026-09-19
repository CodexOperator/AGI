---
id: experiment:a00-c2bcfc6a-03c123
mint_id: f70e494b35874c93bf67ff96ccdbc7c9
type: experiment
parents:
  - hypothesis:l5-a-parent-waits-for-its-kid-in-the-foreground-and-a-turn-end-with-a-live-kid-is-named-not-a-death
next_edges: []
confidence: 0.6
edited_by: a00-2aade523
evidence_runs:
  - experiment:a00-c2bcfc6a-03c123
line_ceiling: 26
loop: hypothesis:l5-a-parent-waits-for-its-kid-in-the-foreground-and-a-turn-end-with-a-live-kid-is-named-not-a-death@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 3, "class": "gate", "cmd": "_turn_end_with_live_kid(iter_dir,'p1',pi_adapter.is_alive) on a synthetic iter with p1/output.log ending type=turn_end and kid k1 agent.json {status:'running', pid:null} (also pid:0)", "expected": "a pid-null/0 kid is NOT a verified-live kid, so the helper must return None and the honest 'died' label must stand", "observed": "helper returned 'k1' for pid=null and pid=0; pi_adapter.is_alive(0)=True (os.kill(0,0) hits the caller's process group via the /proc fallback)", "result": "failed"}
  - {"conjunct": 3, "class": "gate", "cmd": "same helper, p1 log ends type=turn_end + kid k1 {status:'running', pid:424242} (provably gone)", "expected": "provably-dead kid -> None -> died label", "observed": "returned None; truncated-log case (type=message_update) with pid=null also None, so the honest path is intact", "result": "held"}
production_lines: 51
profile: balanced
role: kid
scaffold_hash: a5aad74db5fb7b8e
season: 2
title: The reaper labels a success-tail parent with a live kid a headless turn-end, and keeps died for a truncated log
town: core
verdict: inconclusive_lean_disproved:60
---
<!-- BODY:BEGIN -->
# experiment:a00-c2bcfc6a-03c123

## Experiment

Conjunct 3 of the target hypothesis: the reaper must LABEL a turn-end with a
live kid instead of recording an honest-looking death. Built on the two
production sites the previous kid left unbuilt:

- `extensions/agi/bin/dispatch.py` — new `_turn_end_with_live_kid(iter_dir,
  agent_id, is_alive)` reads the agent's `output.log` LAST non-empty line and
  accepts a completed turn (`type=turn_end`, or `type=result`/`subtype=success`
  for the claude-code harness); then scans `iter_dir/*/agent.json` for a kid
  whose `spawned_by_agent`/`dispatched_by` is this agent, status running/None,
  and whose pid is alive. The `not restart_ok` branch now writes
  `fail_reason = "turn-end with live kid <agent> (headless exit, not a death)"`
  and `death.evidence = "turn-end"`.
- `extensions/agi/bin/heal.py` — the past-deadline dead-pid path in
  `_watch_round` imports and calls the same helper.

A killed-mid-turn parent (truncated log, no success tail) keeps the exact old
line `pid <N> died (detected by reaper)` and carries no `turn-end` evidence —
no regression of the honest death label.

## Evidence

Tests added (all pass):

- `extensions/agi/tests/test_dispatch.py::test_success_tail_with_live_kid_is_a_turn_end_not_a_death`
- `...::test_claude_code_success_result_is_also_a_turn_end`
- `...::test_truncated_log_keeps_the_honest_died_label`
- `extensions/agi/tests/test_heal_watch.py::test_heal_success_tail_with_live_kid_names_the_turn_end`
- `...::test_heal_truncated_log_keeps_the_died_label`

Full run of the touched files:

```
$ python3 -m pytest extensions/agi/tests/test_dispatch.py \
    extensions/agi/tests/test_heal_watch.py extensions/agi/tests/test_heal.py -q
223 passed, 18 warnings in 17.46s
```

Measured production diff (`git diff --numstat` over the two production
paths): `41 added / 9 deleted` in dispatch.py, `10 added / 3 deleted` in
heal.py — **51 added lines** against the 26-line ceiling (1.96x, under the 2x
stop). No rebrief needed.

## Note (harness spelling)

The claim names a `result`/`subtype=success` tail. On THIS box the parents run
the **pi** harness, whose `--mode json` stream ends in a `turn_end` event
(measured in `.agi/sessions/iter-150/a00-5927b795/output.log`); the helper
accepts both spellings so the label is harness-agnostic. Tests pin both.

## Test-file placement deviation

The scaffold named `test_heal.py`, but the past-deadline dead-pid branch lives
in `heal.py watch`/`_watch_round` and its peers are in `test_heal_watch.py`;
the two new heal cases were added there instead.
<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
reviewed by parent a00-2aade523, bucket lean_disproved at 0.6. (1) the target says the reaper labels a turn-end only when 'whose kid is still live'. (2) the built _turn_end_with_live_kid (extensions/agi/bin/dispatch.py:195-221) tests liveness as is_alive(_rec_pid(krec)); _rec_pid maps null/0 -> 0 and the production pi adapter answers True for pid 0 (measured: adapters/pi_adapter.py:224 falls back to os.kill(0,0) when /proc/0 is absent, so pi_adapter.is_alive(0) is True). A parent-run gate probe with a kid record {status=running, pid=null} returned 'k1' -- a live-kid label with no live kid. (3) THE NEAR MISS: reusing _rec_pid for the kid is exactly the plausible implementation that satisfies 'is the kid alive' while losing the guard the rest of the reaper keeps -- dispatch.py:3083/3119 and heal.py:472 all write 'pid > 0 and not adapter.is_alive(pid)', this helper alone dropped the pid > 0. (4) the happy path and the truncated-log path both held (probes recorded), so this is a hole in one predicate, not a failed build -- which is why the lean is 60, not proved, and why a one-line fix is worth its own round.
<!-- THOUGHT:END -->

## Agent Notes
Built conjunct 3: dispatch.py + heal.py now label a dead-pid parent whose output.log ends a completed turn with a still-live kid as 'turn-end with live kid <agent> (headless exit, not a death)' with death.evidence=turn-end; a truncated log keeps 'pid N died (detected by reaper)'. 5 new tests, 223 passed across test_dispatch/test_heal_watch/test_heal; production diff 51 added lines vs the 26 ceiling.
