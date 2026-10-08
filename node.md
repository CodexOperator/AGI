---
id: experiment:a00-8f06d30a-4fc1e3
mint_id: 19988556f49d4af68910c6baf00d5e43
type: experiment
parents:
  - hypothesis:l4-stalled-is-a-state-the-harness-can-see
next_edges: []
confidence: 0.8
edited_by: a00-8c98c841
evidence_runs:
  - experiment:a00-8f06d30a-4fc1e3
loop: hypothesis:l4-stalled-is-a-state-the-harness-can-see@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 3ca76adfca970a00
season: 2
title: A00 8f06d30a 4fc1e3
verdict: inconclusive_lean_proved:80
---
<!-- BODY:BEGIN -->
# experiment:a00-8f06d30a-4fc1e3

## Experiment

Wired `stall_detect` into the reaper, closing the gap left by
`experiment:a00-197548e2-c0c2ea` (unit-proven but NOT imported by the harvest
path). Two changes:

- **extensions/agi/bin/stall_detect.py** — added the single call the harvest
  path makes: `record_stalled_in_iteration(iter_dir)` = `scan_iteration`
  (read-only detection) then `note_stalled` (the only write the module
  performs) over each returned id. Returns the ids stamped.
- **extensions/agi/bin/dispatch.py** — added `import stall_detect` and called
  `stall_detect.record_stalled_in_iteration(iter_dir)` once per reaper pass,
  right after the manifest is read and before the per-agent reap loop. A
  stalled parent gets `status: stalled` on its live `agent.json`; the reaper's
  own guard (`if status != "running": continue`) then skips it next pass
  exactly as designed. Nothing killed, nothing restarted, nothing committed;
  the reaper's commit-based completion check is untouched.

Prohibitions held: stalled never enters `spawn_budget.TERMINAL` (asserted);
no edits to existing tests; did not touch `brief.py`, `provisioning.py` or
`cli.py`.

## Evidence

- **extensions/agi/tests/test_stall_detect.py** — added `TestWiringHook`:
  (a) the hook fires on a four-condition fixture shaped like the L4.65/L4.70
  case and stamps `status: stalled` + `stalled_at`, pid untouched; (b) the
  hook is a no-op on a healthy parent (live kid) and on a young parent (under
  T) — record stays `running`, no `stalled_at`; (c) `stalled` still absent
  from `TERMINAL` after wiring.
- Test counts:
  `test_stall_detect.py + test_dispatch.py + test_failures.py +
  test_spawn_budget.py` → **143 passed in 7.31s**.
- `stalled` ∉ `spawn_budget.TERMINAL` (a stalled parent is still alive and
  still holds its lease).

Hypothesis confirmed end-to-end: `stalled` is now a first-class RECORDED agent
state the harness can see from the live record.

## Agent Notes
Wired stall_detect into the reaper: new record_stalled_in_iteration (scan+stamp) called once per reaper pass; stalled now recorded on live agent.json, never enters TERMINAL. 4 test files 143 passed.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Second kid, briefed with the first kid result via prompt-file: closed exactly the gap kid 1 own-stated — stall_detect is now imported and called once per reaper pass (record_stalled_in_iteration = scan + stamp), so the RECORD half of the hypothesis is end-to-end. Parent verified: only stall_detect.py + test_stall_detect.py new plus a small dispatch.py hook, no existing test edited, TERMINAL untouched, 143 passed re-run by parent. One caveat the parent flags for the next run: once a record is stamped stalled, the reaper guard (status != running) skips it on later passes, so the reaper effectively stops re-examining a stalled parent after the first stamp — defensible (the label persists and the operator sees it) but a successor should confirm this is the intended watching behaviour rather than an accident, e.g. by logging the stall each pass.
<!-- THOUGHT:END -->
