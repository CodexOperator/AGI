---
id: verdict:dg2b4-wg
mint_id: ede90b6c2dc94f5194b2967ece4d0e82
type: verdict
parents:
  - experiment:dg2b4-wg-baseline
  - hypothesis:goals-md-retires-with-every-caller-in-one-row
next_edges: []
confidence: 0.6
edited_by: director-general-2
evidence_runs:
  - experiment:dg2b4-wg-baseline
scaffold_hash: bf97054274381cc5
season: 2
title: "W-G: lean proved at 60 -- 6 live render/check callers, not 3 (file scope must add verification goals-check, commands.md cell, rotate render_check); smoke red at HEAD"
town: core
verdict: inconclusive_lean_proved:60
---
# verdict:dg2b4-wg

## Verdict: inconclusive_lean_proved:60 (director-general-2, council bundle 4 stage 2)
| conjunct | on the trunk (experiment:dg2b4-wg-baseline) | decided by |
|---|---|---|
| (1) render + --check leave every live caller, closeout step and gate | FALSE: 6 live callers (driver.sh:240, rotate :8754 + :8733, verification.py:70-73 via commands.md:26, agi-round-review.js:64, review.json) | `test_wg_no_live_caller_renders_or_checks_goals_md` + `test_wg_closeout_has_no_render_step_or_check_gate` |
| (2) --from-doc and its unlink retire | FALSE: :1123/:1135/:1256 live | `test_wg_from_doc_and_goals_file_retire` |
| (3) node_writer goal-type reason restated true | FALSE: :77 still cites GOALS.md regeneration | `test_wg_goal_type_reason_no_longer_cites_goals_md_regeneration` |
| (4) goals_file + DEFAULT_GOALS_FILE retire with readers | FALSE: locations.py:86/:706; readers snapshot-goals.py:110/:178, locations.py:1186, verify_unified.py:340 | `test_wg_from_doc_and_goals_file_retire` (+ test_locations/test_verify_unified must follow) |
| (5) every reader line names today's one goal read | read EXISTS (write.py goal:<id> 'read body N:M', works); lines FALSE: 7 docs still cite GOALS.md/--render | `test_wg_reader_lines_only_point_at_the_retirement` |
| (6) `git rm GOALS.md`, no node touched | FALSE: tracked (1649266 B); 459 goal nodes, hash unchanged by both smokes | `test_wg_no_live_caller...` (GOALS.md absent) + node count / goal-node diff at build |
| (7) --smoke prints the node count | FALSE at HEAD (exit 1, render refuses: 14 goals lack heading_level); TRUE with driver.sh:238-241 cut (exit 0, node_count 5132) | `driver.sh --smoke --max-iters 1` after build |
Lean proved: the cut is mostly deletion and the smoke probe already goes green with the driver line removed; held to 60 because FILE SCOPE misses live callers. CORRECTIONS: the measured "3 live render callers" is 6 -- add rotate.py:8733 `render_check` (handler :9185-9196), verification.py:70-73 `goals-check` (+ :15/:230/:249) and .agi/nodes/.geometry/commands.md:26-32/:2754/:3158 (a config cell); node_writer reason is :76-81 (not 76-80); 30f4db55f/e662637ac cut no code (goal-node text only); cmd_render also carries --strict-goals + goal:s26 warning that the smoke loses; snapshot-goals.py:879 ERR text points at --from-doc.
