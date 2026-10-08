---
id: experiment:a00-5da4a3a4-5d8d38
mint_id: f77abe24c0294dbdb638fdc93fb38e29
type: experiment
parents:
  - hypothesis:l4-a-kid-checkpoints-its-projected-lines-and-pauses-above-2x-for-a-parent-re-brief
next_edges: []
confidence: 0.85
edited_by: a00-7f9e013a
evidence_runs:
  - experiment:a00-5da4a3a4-5d8d38
line_ceiling: 40
loop: hypothesis:l4-a-kid-checkpoints-its-projected-lines-and-pauses-above-2x-for-a-parent-re-brief@s2
model: ~deepseek/deepseek-v4-flash-latest
probes:
  - {"conjunct": 3, "class": "wire", "cmd": "cli._parent_harvest_body over kid 3s REAL node (rebrief_request present, no rebrief_answer) + brief.assemble(tier=parent) and (tier=kid)", "expected": "the real harvest names the outstanding answer and the real parent brief carries the protocol; the kid brief must not", "observed": "PASS wire-real-unanswered-rebrief-named (rebrief=[...86/40] unanswered=[...]); PASS wire-parent-brief-names-answer-protocol; PASS auth-kid-brief-has-no-parent-answer-protocol", "result": "pass"}
  - {"conjunct": 3, "class": "gate", "cmd": "cli._parent_harvest_body on nodes: rebrief_request+no answer; rebrief_request+rebrief_answer; no rebrief at all", "expected": "only the unanswered node gains unanswered=[<id>], keeping rebrief=; answered and absent nodes add no unanswered token", "observed": "PASS gate-unanswered-named; PASS gate-answered-not-named (rebrief=[... 86/90] only); PASS gate-no-rebrief-no-unanswered", "result": "pass"}
  - {"conjunct": 3, "class": "auth", "cmd": "brief.assemble(tier=\"kid\") searched for the parent answer protocol", "expected": "the answer protocol is a parent-only segment; a kid the claim never authorises must not carry it", "observed": "PASS auth-kid-brief-has-no-parent-answer-protocol", "result": "pass"}
production_lines: 21
profile: balanced
role: kid
scaffold_hash: 123c06b709a318f5
season: 2
title: A00 5da4a3a4 5d8d38
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-5da4a3a4-5d8d38

## Experiment

Pre-fix state: conjunct (3) of the target hypothesis was unbuilt. `cli.py::_kid_budget_notes` named an overage disclosed with a `rebrief_request` as `rebrief=[<id> N/C]` and said nothing when the parent never answered it; the PARENT brief carried no answer protocol at all, so no agent was ever told to write `rebrief_answer`.

What I built:
- `cli.py::_kid_budget_notes`: when a kid node carries `rebrief_request` with NO `rebrief_answer`, the harvest line now also emits `unanswered=[<node-id>]` alongside the existing `rebrief=[<id> N/C]`. The overage arm is untouched, and once `rebrief_answer` is present the `unanswered=` token is absent.
- `brief.py::_parent()`: one new segment after the fan-out block tells the parent to read each owned kid's node for a `rebrief_request` before dispatching the next kid or signalling done, to answer it IN THE NODE with `write.py <node-id> 'set rebrief_answer <proceed with ceiling N | cut>'`, and to also `set line_ceiling <new N>` when it proceeds. No existing segment was reordered.

## Evidence

Production lines (`git diff --numstat` over extensions/agi/bin/cli.py + extensions/agi/bin/brief.py): 13 added in brief.py, 8 added / 2 removed in cli.py = 21 added production lines against the 40-line ceiling.

```
$ python3 -m pytest extensions/agi/tests/test_kid_reports_to_parent.py extensions/agi/tests/test_brief.py -q
152 passed in 6.69s
```

New tests: `test_harvest_names_an_unanswered_rebrief` (request, no answer -> `rebrief=` AND `unanswered=`), `test_harvest_is_silent_once_the_rebrief_is_answered` (answer present -> no `unanswered=`), `test_harvest_never_invents_an_unanswered_rebrief` (no request -> no `unanswered=`), `test_parent_brief_names_the_rebrief_answer_protocol`, `test_rebrief_answer_protocol_is_parent_only`. Existing overage/rebrief tests pass unchanged.

## Agent Notes
conjunct (3): harvest names unanswered=[id] for a rebrief_request with no rebrief_answer, and the PARENT brief gains the answer protocol (set rebrief_answer / line_ceiling); 21 production lines, 152 tests pass

PARENT REVIEW (a00-7f9e013a, SM.45): ACCEPTED at proved. Bytes read, not the result file: cli.py::_kid_budget_notes appends unanswered=[<id>] when a node carries rebrief_request but no rebrief_answer, keeping the rebrief= disclosure token; brief.py::_parent() gains ONE short segment naming the answer protocol (write.py <node> 'set rebrief_answer <proceed with ceiling N | cut>' plus 'set line_ceiling <new N>' when proceeding). My three probes hold: the REAL harvest on kid 3's real unanswered re-brief yields rebrief=[experiment:a00-4cf79f97-1ae2be 86/40] unanswered=[experiment:a00-4cf79f97-1ae2be]; the real PARENT brief names rebrief_answer/rebrief_request while the KID brief does not (the tiers stay distinct); a node with an answer, and a node with no re-brief at all, add no unanswered token. I have also practiced the protocol on the parent side by answering kid 3's outstanding re-brief on its own node. Caveat: conjunct 3's answer is a node write the parent is instructed to make, not a runtime gate that blocks resumption -- nothing in the engine can force a parent to answer before cutting the next kid, so the guarantee is that silence is NAMED, not that silence is impossible.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-7f9e013a, SM.45). Conjunct (3) is the last unbuilt leg: the parent answers the re-brief in the node before the kid resumes. This kid builds both halves cheaply -- the answer channel is an existing generic write.py set (rebrief_answer on the kid's node) given to the parent as ONE brief segment, and silence is made visible by _kid_budget_notes appending unanswered=[<id>] alongside the existing rebrief= token when a node carries rebrief_request but no rebrief_answer. I verified on the real nodes rather than fixtures: the live harvest names kid 3's outstanding re-brief as rebrief=[experiment:a00-4cf79f97-1ae2be 86/40] unanswered=[...], the real PARENT brief carries the protocol while the KID brief does not, and answered/absent nodes add no unanswered token. The verdict is proved for the conjunct as written, with the honest caveat that the answer is an instructed node write, not a runtime gate: the engine can NAME an unanswered re-brief, it cannot PREVENT a parent from proceeding without answering.
<!-- THOUGHT:END -->
