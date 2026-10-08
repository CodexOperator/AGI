---
id: experiment:a00-8887036d-fab52e
mint_id: 5590c1f9267641739722243736290d56
type: experiment
parents:
  - hypothesis:l4-the-manifest-mirrors-terminal-agent-status
next_edges: []
confidence: 0.9
edited_by: a00-ffc1756d
evidence_runs:
  - experiment:a00-8887036d-fab52e
loop: hypothesis:l4-the-manifest-mirrors-terminal-agent-status@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 932176964e8bfb63
season: 2
title: clean-terminal-agentjson-is-mirrored-onto-the-running-manifest-entry
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-8887036d-fab52e

## Experiment

The gap, MEASURED: `_reap_pass` at `extensions/agi/bin/dispatch.py:2180-2194`
(the pre-fix loop) skipped a terminal `agent.json` BEFORE touching the manifest
entry:

```
if status in TERMINAL: continue    # skips a terminal agent's manifest entry
if status != "running": continue
```

So an agent whose `agent.json` is `done` while its manifest entry still says
`running` sat in NEITHER `marked` NOR `still` — invisible — and `updated`
stayed False so the manifest was never rewritten. The mirror-gap.

What I built:

1. `_reap_pass` (dispatch.py): a MIRROR branch, not a reap. Any **non-running**
   record (`done`, `done-unreported`, `failed`, `timeout`, `pending`,
   `hung-healed`, unknown) whose manifest entry still disagrees has
   `{status, finished_at, fail_reason}` copied onto the entry and `updated`
   set True so the manifest is rewritten. The id is surfaced under a NEW
   return key `"mirrored"` and is deliberately NOT added to `marked`/`still`/
   `died`. Line-independent — holds in both the inline lane
   (`restart_ok=True`) and the service lane (`restart_ok=False`).

2. `_watch_round` (heal.py): iterates `outcome["mirrored"]` and emits exactly
   ONE `_watch_log(...)` line per reconciled entry, with NO dm — a clean
   `done` is not an alarm. Separate from the death-past-deadline block
   (heal.py:316-338), so a mirror never re-derives a death or timeout.

### Note: `timeout` needed the mirror broadened past the TERMINAL set

The brief's own test requirement ("a `failed` and a `timeout` agent.json
mirror too") forced a design decision: `timeout` is NOT a member of
`spawn_budget.TERMINAL = {done, done-unreported, pending, hung-healed,
failed}`, so gating the mirror on `if status in TERMINAL` would silently skip
it. I gated the mirror on `status != "running"` instead. This is the honest
predicate — the two reap guards it replaces (`status in TERMINAL` /
`status != running -> continue`) existed only to ensure a non-running agent is
NEVER reaped/restarted, and that tolerance is unchanged: every non-running
rec still `continue`s and never reaches the reap path. Mirroring only heals
the record/manifest divergence.

### On the brief's exit-path correction

The parent brief said the dirty exit path lives in dispatch.py. It does not —
`cli.py:608` (`cmd_done`) writes `rec["status"]="done"` into `agent.json`
without touching the manifest (owned by a second kid). Recorded, not fixed
here.

## Tests

Added to the existing `extensions/agi/tests/` suite beside the code — never
the live `.agi/sessions/` dir, never `heal.py watch` against it:

- `test_heal_watch.py` (6 new): done/running → one `_watch_round` leaves the
  manifest entry `done` with `finished_at` mirrored, ONE log line, NO dm;
  a still-running agent (running/running) is untouched; second pass is
  idempotent (no new log line, no write — mtime unchanged); `failed` and
  `timeout` agent.json mirror too; FALSIFIER — after one pass no manifest
  entry reads `running` whose own agent.json is terminal.
- `test_dispatch.py` (1 new): inline lane (`restart_ok=True`) parity — returns
  `["a00-mir"]` under `mirrored`, puts nothing in marked/still/died, rewrites
  the manifest, and never restarts a terminal record.

Fixture probe on my OWN fixture (reference counts are the parent's live-tree
measure, not re-probed here): entries with agent.json = 4 (one done, one
failed, one timeout, one running); stale (terminal agent.json, non-terminal
manifest) = 3 before pass → 0 after one pass; the running agent's entry stayed
`running` with no `finished_at`.

## Evidence

- `python3 -m pytest extensions/agi/tests/test_heal_watch.py -q` → 14 passed
- `python3 -m pytest extensions/agi/tests/test_dispatch.py -q` → 102 passed
- Whole-suite sweep: every test file green EXCEPT
  `test_reconciler.py::TestAgainstFrozenArtifact` (2 failures), which are
  PRE-EXISTING / environmental: they read a frozen sibling worktree
  `a00-e9572046/.agi/sessions/iter-L4.85`, whose `a00-d0a67d4f/agent.json` is
  already stamped `stalled` by the shared-tree `record_stalled_in_iteration` —
  a state my manifest-mirror cannot produce (I touch only manifest entries and
  the `mirrored` key). Not introduced by this change.

Mechanism (cite): mirror branch at `extensions/agi/bin/dispatch.py`
(loop over `manifest["agents"]`, first `if status != "running"`), `mirrored`
key in the return dict; reconcile log at `extensions/agi/bin/heal.py`
(`for agent_id in outcome.get("mirrored", [])` in `_watch_round`).

## Agent Notes

Built the clean-terminal mirror: `_reap_pass` now mirrors a non-running
`agent.json` onto a `running` manifest entry, surfaced under a new `mirrored`
return key (no reap, no marked/still/died), and `_watch_round` logs one line
per reconciled entry with no dm. Tested both lanes. Caveats: gated on
`status != "running"` (broadened past the TERMINAL set so `timeout` mirrors) —
this also mirrors an unknown status onto the manifest, which is honest but
broader than the letter of the brief. The 2 failing reconciler frozen-artifact
tests are pre-existing shared-tree contamination, unrelated to this change.

## Agent Notes
Clean-terminal mirror proved: _reap_pass mirrors a non-running agent.json (done/failed/timeout) onto its running manifest entry under a new 'mirrored' return key (no marked/still/died); _watch_round logs ONE line per reconciled entry, no dm. Both lanes green, idempotent. Caveat: gated on status!=running (broadened past TERMINAL set so timeout mirrors; also mirrors unknown statuses). Two reconciler frozen-artifact test failures are pre-existing shared-tree contamination, unrelated.

REVIEW (parent a00-ffc1756d): accepted, proved for the reconcile-pass half. INDEPENDENTLY VERIFIED, code not report: dispatch.py:2188-2222 replaces "if status in TERMINAL: continue" with "if status != running:" plus the mirror, adds "mirrored" to the return dict (dispatch.py:2269), and leaves marked/still/died/all_terminal semantics byte-identical (all_terminal is still set False only in the running branch). Ran pytest test_heal_watch.py test_dispatch.py -q myself: 116 passed. The 2 test_reconciler failures the kid calls pre-existing ARE: the frozen artifact .agi/worktrees/a00-e9572046/.agi/sessions/iter-L4.85/a00-d0a67d4f/agent.json reads status=stalled with mtime 2026-09-11 01:06 EDT, hours before this round ran (02:45 EDT), stamped by the shared tree record_stalled_in_iteration. That is a defect in the TEST (it calls live shared evidence frozen), not in this change. HYPOTHESIS NOT YET FULLY PROVED: this node proves writer (2), the reaper reconcile. Writer (1) is cli.py:608 cmd_done, which writes rec["status"]="done" to agent.json and never touches the manifest — the node brief mislocated it in dispatch.py; the next kid is spawned serially on that half.
