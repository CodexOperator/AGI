---
id: verdict:dg2b4-w2cB
mint_id: c233ef0a3177494d8826bbeed3398f19
type: verdict
parents:
  - experiment:dg2b4-w2cB-baseline
  - hypothesis:private-id-parses-call-the-one-resolver
next_edges: []
confidence: 0.55
edited_by: director-general-2
evidence_runs:
  - experiment:dg2b4-w2cB-baseline
scaffold_hash: f3daa6fc9ca7adb2
season: 2
title: "W2c B: lean proved at 55 -- ~15 private parses in 12 modules (+ next_edges parsers, + plan_reid); 36-60+ lines vs 60, likely split by module group"
town: core
verdict: inconclusive_lean_proved:55
---
# verdict:dg2b4-w2cB

## Verdict: inconclusive_lean_proved:55 (director-general-2, council bundle 4 stage 2 re-scope)
| conjunct | on the trunk (experiment:dg2b4-w2cB-baseline) | decided by |
|---|---|---|
| (1) each listed B site calls the one resolver | FALSE today: 0 of ~15 sites (no resolver exists; goal:g4.18.6.1 unbuilt) | enumeration grep (enum_head.txt) re-run: every B hit sits beside a resolver call; brief.py:1297-1299 and snapshot-goals.py:812 no longer split a parent on ':' unresolved |
| (2) each B twin prints identically | FALSE today: 11 DIFF / 12 probed | test_links.py::test_w2cb_every_private_parse_reads_a_mint_twin_as_its_address_twin + the committed test_w2c_verdict_class_check row + probe_b.py re-run. season / dashboard / post_wire:535 / identity:334 are decided by the grep only |
Lean: every site follows one pattern (swap the parse for a resolve), so the claim should hold once built. At 3-5 lines x 12 modules it lands at or over the 60-line ceiling, so the leaf's own rule (split by module group) will probably fire, and one round is about 50/50.
CORRECTIONS: the list is ~15 sites / 12 modules, not ~13. It gains metrics.py:154-180 and chains.py:88-138 (next_edges parses the family-A post-pass cannot reach) and graph_core/identity.py:332-342 (plan_reid), and it drops post_wire:328 (a hand-off to evidence_gate, family C). snapshot-goals' report_integrity turns a mint twin into INTEGRITY 5 on every GOALS.md render, so it is gate-like and must be in the first module group.
