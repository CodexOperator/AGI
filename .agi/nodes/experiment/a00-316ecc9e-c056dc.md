---
id: experiment:a00-316ecc9e-c056dc
mint_id: 08163786dd8a4f14b77ed5a84b4fbf82
type: experiment
parents:
  - hypothesis:l4-the-facts-guard-covers-every-facts-label-and-facts-body-range-returns-all-ranges
next_edges: []
confidence: 0.9
edited_by: a00-efb03815
evidence_runs:
  - experiment:a00-316ecc9e-c056dc
line_ceiling: 30
loop: hypothesis:l4-the-facts-guard-covers-every-facts-label-and-facts-body-range-returns-all-ranges@s2
model: ~deepseek/deepseek-v4-flash-latest
probes:
  - {"conjunct": 1, "class": "gate", "cmd": "python3 parent_probes.py probe1a: _facts_cap_violations(live_templates(config:rotations), live_body_lines)", "expected": "live facts region (37:64, 7189 B) accepted under 90% of the 8000-B startup cap => no violation", "observed": "violations=[] on the live node; the guard is green on the shipped bytes", "result": "PASS"}
  - {"conjunct": 2, "class": "gate", "cmd": "python3 parent_probes.py probe1b/1c: fixture director{facts:1:3, facts-2:1:3 byte_cap:8}; run _facts_cap_violations AND a verbatim pre-fix label=='facts' gate", "expected": "facts-2 over ITS OWN byte_cap is REFUSED by name; the pre-fix gate lets the SAME fixture PASS", "observed": "post-fix violations=[\"template 'director' 'facts-2': ... 9 bytes, over ... 7 of byte_cap 8\"]; pre-fix violations=[] (fix is load-bearing)", "result": "PASS"}
  - {"conjunct": 2, "class": "gate", "cmd": "python3 parent_probes.py probe2a/2b: fixture director{facts:1:3 valid, facts-2:'true' no range}; _facts_body_range vs verbatim pre-fix reader", "expected": "widened reader REFUSES BY NAME (template+label); pre-fix silently skips the unresolvable facts-2", "observed": "post-fix AssertionError \"template 'director' 'facts-2' cmd does not name a body range\"; pre-fix returned (1,3)", "result": "PASS"}
  - {"conjunct": 3, "class": "wire", "cmd": "python3 parent_probes.py probe3a/3b: fixture with facts:2:2 and facts-2:4:4, 'by hand' only on line 4; call _facts_body_range then _region_hand_hits", "expected": "_facts_body_range returns BOTH ranges ordered; _region_hand_hits SCANS the facts-2 region (line 4) and finds the hit", "observed": "regions=[('facts',2,2),('facts-2',4,4)]; hits=[(4,18,'by hand','CITATION')]", "result": "PASS"}
  - {"conjunct": 3, "class": "wire", "cmd": "python3 parent_probes.py probe3c: spy _facts_cap_violations then run the LIVE guard test unmodified", "expected": "the live guard call site actually routes through the changed decision fn", "observed": "calls=1 and the guard test passed through the spy", "result": "PASS"}
production_lines: 0
profile: balanced
role: kid
scaffold_hash: 4c5caee5f809eaa7
season: 2
title: A00 316ecc9e c056dc
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-316ecc9e-c056dc

## Experiment

BUILD (code half, lands first so the template half has a green target).
File: `extensions/agi/tests/test_rotate_templates.py` (test-only; production
lines 0/30). No other file touched; `rotations.md` untouched.

Pre-fix state, measured (scratch `prefix_probe.py` / `pre_fix_falsifier.py`,
session dir, copy of the removed code — no `git stash`):

* `_facts_body_range` gated on `e.get("label") != "facts"` and returned ONE
  `(n, m)` pair. On `{facts: 1:3, facts-2: 1:3}` it returned `(1, 3)` — the
  facts-2 range was silently dropped.
* The byte-cap guard gated on `any(label == "facts")` and measured that one
  range, so the `facts-2`-over-its-own-cap fixture produced `violations []`:
the falsifier passed (the live defect).
* A `facts-2` entry with `cmd: true` was never refused by name while a `facts`
  entry existed (`NO REFUSAL`).

What was built:

1. `_facts_body_range(templates)` now returns the LIST of `(label, n, m)` for
   every first_turn label matching `facts(-\d+)?`, ordered `facts`, `facts-2`,
   `facts-3` … (numeric suffix). Same-label agreement across templates is
   kept; a facts* cmd naming no `read body N:M` fails by NAME (template +
   label), never as a bare "no facts entry"; the no-facts-at-all refusal stays.
2. All three callers take the list. `_region_hand_hits` range-scans EVERY
   range (deduped on line/pos/vocab so overlapping ranges do not double-hit);
   the F16-by-fact-id locator scans every range; the cap guard measures every
   facts* entry.
3. New shared decision `_facts_cap_violations(templates, lines)`: each facts*
   entry against ITS OWN `byte_cap` (entry-level if present, else the template
   startup cap), same 90% headroom, violation naming template + label + cap.
   The live guard calls it, so a fixture cannot pass on a state the live
   assertion would refuse.

Command / result:

```
python3 -m pytest extensions/agi/tests/test_rotate_templates.py -q
29 passed, 1 warning in 3.69s
```

(26 before the change; 3 added: `test_facts_cap_guard_refuses_a_facts2_over_
its_own_byte_cap`, `test_facts_range_resolution_refuses_a_facts2_without_a_
body_range`, `test_facts_body_range_returns_every_facts_label_ordered`.) No
pre-existing assertion was weakened. The live node still carries only a
`facts` entry, so the live cap guard stays green (regions resolve to
`facts 37:64` under both templates' startup caps).

## Evidence

PRE-FIX vs POST-FIX on the SAME falsifier (scratch, verbatim copies of the
removed reader/guard):

```
PRE-FIX  reader           -> (1, 3)
PRE-FIX  facts-2-over-cap -> violations []   <-- RED FALSIFIER PASSES (defect)
POST-FIX reader           -> [('facts', 1, 3), ('facts-2', 1, 3)]
POST-FIX facts-2-over-cap -> violations ["template 'director' 'facts-2': facts
  region 1:3 renders to 9 bytes, over the 10%-headroom limit 7 of byte_cap 8 —
  the wake would receive a TRUNCATED facts section; compact it or add a
  facts-2 entry, never drop"]
PRE-FIX  facts-2-no-range -> NO REFUSAL
POST-FIX facts-2-no-range -> refused BY NAME: template 'director' 'facts-2'
  cmd does not name a body range: {'label': 'facts-2', 'cmd': 'true'}
```

Live-node assertion (unchanged, green): `test_live_facts_region_fits_under_
every_template_byte_cap_with_headroom` now reads every facts* entry through
`_facts_cap_violations`; with only `facts` present the set is identical to the
pre-fix one, and the live region still fits with headroom.

`git diff --numstat` (read-only measurement): test file +143/-50; production
(non-test) paths: none — 0 production lines against the 30-line ceiling.

## Agent Notes
Widened _facts_body_range to return (label,n,m) for every facts* label; all 3 callers take the list; new _facts_cap_violations measures each facts* entry against its OWN byte_cap (entry-level else startup, 90%); 3 falsifier tests added, 29 passed, live guard green; production lines 0/30; pre-fix red shown via verbatim-copy scratch probe (no git stash).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
(1) WHAT THE INSTRUCTION SAID: a tier parent reviews a kid by its DIFF (git diff merge-base..kid-branch), never its result file; one parent-run negative probe per claim conjunct, recorded as probes: in the kid node; a kid that passes its own suite but fails the parent probe is lean_disproved. (2) WHAT THE MACHINE ACTUALLY DOES: git diff d8ecdcbdf..3ed5b9ad2 moves _facts_body_range from a != "facts" one-pair reader to re.fullmatch(r"facts(-\d+)?") returning ordered (label,n,m), and adds _facts_cap_violations (test_rotate_templates.py:1117) reading each entry own byte_cap; parent_probes.py rebuilt the pre-fix gate verbatim and showed the facts-2-over-its-own-cap fixture yields violations=[] pre-fix and a named refusal post-fix, that a facts-2 cmd with no range is skipped pre-fix and refused by name post-fix, and that _region_hand_hits scans a facts-2 range while a spy shows the live guard makes exactly one call through the changed decision fn. All 8 probes PASS. (3) NEAR MISS: accepting the kid 29-passed line as evidence would miss that the entry-level byte_cap branch is exercised only on fixtures — the live rotations.md carries no facts-2 yet, so shipped-bytes coverage of the widened path waits on master-sensei template half; recorded as the kid caveat rather than a defect, since the node lands FIRST by design to give that edit a green target. (4) DEVIATION: none.
<!-- THOUGHT:END -->

ACCEPT :90 — parent read the DIFF d8ecdcbdf..3ed5b9ad2 (not the result file): _facts_body_range now returns [(label,n,m)] for every facts(-N)? label, all 3 callers take the list, and _facts_cap_violations measures each entry against its own byte_cap (entry-level else startup, 90%); 8 parent-run probes across all 3 claim conjuncts PASS, including the verbatim pre-fix gate passing the SAME facts-2-over-cap fixture (fix load-bearing) and a wire spy proving the live guard routes through the changed fn; 29 tests green; 1 kid accepted, 0 demoted.
