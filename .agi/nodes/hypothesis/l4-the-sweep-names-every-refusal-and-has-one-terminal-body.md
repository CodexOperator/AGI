---
id: hypothesis:l4-the-sweep-names-every-refusal-and-has-one-terminal-body
mint_id: d606c73962dd406099d81cd7ec5ce241
type: hypothesis
parents:
  - goal:g15
  - hypothesis:l4-a-manifest-less-partial-source-never-vetoes-a-rounds-bring-home
next_edges: []
edited_by: sanctuary-director
scaffold_hash: 7e17d111037fca5f
season: 2
testable_claim: "OWNER 2026-09-11 05:1xZ: bugfix/optimization findings are g15 hypothesis nodes fixed in-loop. FOUND by the mur-41 review (Prime XII, wf_71d90645-bb8, 21:5xZ), minted by sanctuary-director 214458Z as the Prime's g15 line E; IN the close cut-off (Prime 22:14Z). MEASURED by mur-41 in heal.py: `_sweep_refusal_reason` (heal.py:548) has NO needle for the newer `no manifest in any source` refusal (the `tags home failed` path from L4.255/257), so the sweep log maps it to the generic bucket; the old `not-every-agent-record-is-terminal` needle is DEAD (nothing prints that text any more -- grep); `_first_non_terminal` duplicates `_iteration_agents_complete` line for line (twin drift: a fix to one silently misses the other); and no fixture pins a status-less manifest entry refusing. CLAIM: (1) one needle per LIVE refusal text that cli.py session-complete / the sweep can print today (enumerate them by grep and list them in the experiment node with file:line), the dead needle removed; (2) `_first_non_terminal` and `_iteration_agents_complete` share ONE body (one calls the other or both call a shared helper) -- `grep -c` the duplicated lines reads 1; (3) a fixture with a manifest entry that has NO `status` key refuses through the same path and the sweep log names the reason; (4) the no-authority refusal (L4.255's residue: unmapped in the sweep log) gets its needle in the same table. CEILING: 1 kid. FILE SCOPE: `extensions/agi/bin/heal.py` (`_sweep_refusal_reason`, `_first_non_terminal`, `_iteration_agents_complete` only -- NOT the pin-reap region, which is next season's round 2) + `extensions/agi/tests/test_heal*.py`. Serial behind L4.292 (heal.py): cut only after its harvest. Run `env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_heal.py extensions/agi/tests/test_heal_sweep.py -q` (name the files that exist) and paste the needle table into the experiment node. The parent merges the kid branch into the round branch before `done:`."
title: "G15: heal.py _sweep_refusal_reason carries a needle for every live refusal (no-manifest-in-any-source), drops the dead one, and _first_non_terminal shares ONE body with _iteration_agents_complete"
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-the-sweep-names-every-refusal-and-has-one-terminal-body

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
