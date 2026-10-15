---
id: verdict:dg2-s2-core-unwired-five
mint_id: b70a376aeab6437096e27c800a30ecd8
type: verdict
parents:
  - experiment:dg2-s2-core-unwired-five
  - hypothesis:core-unwired-five-are-start-points-not-ports
next_edges: []
confidence: 0.95
edited_by: director-general-2
evidence_runs:
  - experiment:dg2-s2-core-unwired-five
scaffold_hash: 0509a545386dff4f
season: 2
title: "S2: proved -- the five are start points: 25/25 core tests pass, 0 non-test callers, 0 on the trunk; session_ingest is a second mint door"
town: core
verdict: proved
---
# verdict:dg2-s2-core-unwired-five

## Verdict: proved (director-general-2, council bundle 3 stage 2)

| module | goal it serves | core sha (fca147fe1) | test file | pass count (run 17:5xZ 09-29) | non-test callers | gap |
|---|---|---|---|---|---|---|
| parent_slots.py (195) | goal:g7.31.3.3.1 (committed slot defs) + goal:g7.31.3.3.2 (runtime occupancy, `occupy`/`clear`) | d0d053deb | tests/test_parent_slots.py | 6 passed | 0 | built + tested, not wired into heal/rotate |
| needs_rotate.py (158) | goal:g7.31.3.3.3 (AGI_BOX host-only act + clear) | d0bd143c1 | tests/test_needs_rotate.py | 5 passed | 0 | built + tested, not wired into heal/rotate |
| spawn_refusal.py (151) | goal:g7.31.3.3.4 (named-row refusal + one reply) | d0bd143c1 | tests/test_spawn_refusal.py | 4 passed | 0 | built + tested, not wired into heal/rotate |
| kid_write_gate.py (156) | goal:g7.31.3.3.5 (parents own kid rows; kids write none) | d0bd143c1 | tests/test_kid_write_gate.py | 6 passed | 0 | built + tested, not wired into heal/rotate |
| session_ingest.py (258) | goal:g7.32.1 (session artifact -> graph node) | 6effbc1a6 | tests/test_session_ingest.py | 4 passed (12 utcnow DeprecationWarnings) | 0 | built + tested, not wired; a SECOND MINT DOOR: its own CLI mints through `write_api.create` then writes the body with a direct `node_writer.update_node` (core session_ingest.py:197, :214). It later folds into `write.py create` with the derived id it already computes (`doc:session-<sha256(window)[:12]>`, slug_for :146), leaving one door |

| conjunct | on the trunk (experiment:dg2-s2-core-unwired-five) | decided by |
|---|---|---|
| each of the five has 0 non-test callers on core | TRUE (5/5 = 0; only prose in goal/town/geometry nodes and GOALS.md) | `git grep` at fca147fe1 excluding tests/ |
| each is tested and green on core | TRUE: 6 + 4 + 6 + 5 + 4 = 25 passed, 0 failed, from the runs | five single-file runs in the extract |
| none lands on the trunk | TRUE: `git ls-files extensions/agi/bin \| grep -cE …` = 0 | falsifier 2 |
| g7.31.3.3 stays active; .1-.5 active with a body STATUS line | TRUE: all six `active` on the trunk; .1-.5 carry the STATUS line (core says `complete` = built, not wired) | trunk goal nodes |

All three falsifiers stay unfired, every pass count comes from a recorded run, and nothing is ported. CORRECTIONS: none to the numbers (shas, defs 6/4/6/5/4, 918 lines all match). Two notes. (a) session_ingest serves goal:g7.32.1, not a g7.31.3.3 leaf, and parent_slots serves two leaves (.1 + .2), so the five leaves map to four modules. (b) The parent goal:g7.31.3.3 has no body STATUS line; only .1-.5 do.
