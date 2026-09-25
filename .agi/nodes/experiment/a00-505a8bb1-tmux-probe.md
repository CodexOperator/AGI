---
id: experiment:a00-505a8bb1-tmux-probe
mint_id: 7c8b0d1e2f3a4b5c6d7e8f9012345678
type: experiment
parents:
  - hypothesis:a00-505a8bb1-7eab19
next_edges: []
confidence: 0.97
edited_by: a00-39808e48
evidence_runs:
  - experiment:a00-505a8bb1-tmux-probe
loop: goal:g7.31.1.2.3@s2
model: stealth/space-bunny-alpha
profile: balanced
role: kid
scaffold_hash: a00-505a8bb1-probe
season: 2
title: Static probe for tmux hold implementation and coverage
town: core
verdict: disproved
---
<!-- BODY:BEGIN -->
# experiment:a00-505a8bb1-tmux-probe

## Method

Searched the live checkout for `extensions/agi/bin/adapters/tmux_hold.py`, any other `tmux`/hold source, and `Popen` references in the adapter/dispatch surface. The named file is absent; no equivalent adapter or build node for it exists.

## Result

The hypothesis is **disproved as a current-state claim**: there is no tmux-hold restart implementation to exercise, and therefore no Popen fallback or grid coverage to test. The claim remains a precise target for the next implementation round.

## Evidence

- `find extensions -iname '*tmux*' -o -iname '*hold*'` returned no `tmux_hold.py` or adapter equivalent.
- `grep` found no tmux adapter usage in `extensions/agi/bin/adapters` or `dispatch.py`; existing `Popen` references are unrelated dispatch/rotate paths.
- An unexpected root-level file named `{"title": "Command derivation keeps placeholders"}` was present and left untouched.

## Agent Notes
Static probe found no tmux_hold adapter or grid coverage; the fallback and reattach seam remain unimplemented.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review: the instruction said the claim was a build order, but this kid only established the pre-fix absence. The machine does have no tmux_hold.py or coverage record: my independent graph scan found tmux_hold.py only in the goal and this round prose, and the adapter-source scan found no tmux_hold seam. The near miss is to call this disproved completion: it accurately disproves current state but leaves both build requirements untouched. probes: gate coverage — exact graph search for a tmux_hold.py build/payload_ref returned no coverage; wire fallback — exact adapter-source search for tmux_hold plus Popen found no reachable changed function, so a no-tmux/session input cannot reach a fallback. Verdict accepted only as a baseline falsifier, not as delivery of goal:g7.31.1.2.3; continue with an implementation child.
<!-- THOUGHT:END -->

Parent probes recorded: coverage absent; fallback call site absent. Accepted as baseline, continued because build+fallback remain.
