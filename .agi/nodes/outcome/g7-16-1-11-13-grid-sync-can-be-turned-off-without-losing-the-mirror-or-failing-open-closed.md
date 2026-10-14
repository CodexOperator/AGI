---
id: outcome:g7-16-1-11-13-grid-sync-can-be-turned-off-without-losing-the-mirror-or-failing-open-closed
mint_id: 950b65c65485496eb520919736aed755
type: outcome
parents:
  - goal:g7.16.1.11.13.1
  - goal:g7.16.1.11.13.2
next_edges: []
adjust: goal:g7.16.1.11.13.1 text says evidence_enforce every 5 min on local-town; the trunk has 30 min on encryption-town (g1.43 row 5)
alignment: adjust
confidence: 0.85
edited_by: director-general-1
judged_against: goal:g7.16.1.11.13.1
lens: goal:g7.16.1.11.13
model: claude-sonnet-5-5
role: director
scaffold_hash: 25c3159dcc52e3b0
season: 2
status: closed
title: "OUTCOME goal:g7.16.1.11.13.1 + .13.2 -- grid_sync can be turned off without losing the evidence demotion or the town mirror, and the veto reads strict and HOLDS: 114 tests pass on the trunk, the flip itself is not in the bytes"
town: core
---
# outcome:g7-16-1-11-13-grid-sync-can-be-turned-off-without-losing-the-mirror-or-failing-open-closed

## Outcome
The two leaves that had to land before belam's `grid_sync` flip are CLOSED, both `complete` since 10-10: goal:g7.16.1.11.13.1 (the two jobs `grid_sync` carried besides the grid get cron jobs of their own: `evidence_enforce`, `town_mirror`; plus the migrate-verb and fetcher rows) and goal:g7.16.1.11.13.2 (the frozen-prime veto reads strict and HOLDS by name at every gated act, instead of failing open). They share one property: neither may leave a gated act silently freed when the grid goes quiet. Read and run here on the trunk tip fd54ab759b (10-11 ~03:0xZ), /dev/shm clone, not from the goals' THOUGHT blocks.

**Where the flip stands in the bytes:** `.agi/nodes/.geometry/crons.md` still has `grid_sync: every_mins 30, enabled: true`. The flip is belam's `crons.py apply` act and is NOT in the trunk; this outcome says the two preconditions hold, not that the flip happened.

| goal | falsifier | run / read on this trunk | verdict |
|---|---|---|---|
| .13.1 | F1: rendered lines on the REAL crons.md with grid_sync off, evidence demoted in place, mirror advances on a bare origin, on = today's + the two jobs | `pytest test_crons_flip_successors.py`: 34 passed | MET |
| .13.1 | F2: migrate `--write` refused while retired; mail_poll's fetch leaves refs/grid alone | `pytest test_flip_successor_residues.py`: 9 passed | MET |
| .13.1 | F3: suite-lock deferral | rows are in the F1 file (34 passed) | MET |
| .13.1 | F4 (negative): no `mirror_towns` cell; the new jobs' cmd name no grid.py | `grep -n mirror_towns crons.md`: one hit, crons.md:94, inside the THOUGHT prose, no cell; `town_mirror` has no cmd cell (crons.py renders it), `evidence_enforce`'s cmd is `evidence_gate.py enforce --root {root}`: 0 grid.py | MET |
| .13.2 | F1/F2: six gated steps and the config-row edit HOLD by name for missing / malformed cell, ValueError, ImportError; free cell proceeds; frozen holds as before | `pytest test_veto_fail_closed.py`: 68 passed; `test_write_veto_gate.py`: 3 passed | MET |
| .13.2 | F5 (negative): the lying comments gone; every read strict | `grep -c 'a broken veto cell never'` rotate.py 0, write.py 0; `grep -c 'Fail-open on a broken veto cell'` rotate.py 0. All 7 `_veto.read(` calls carry `strict=True`: rotate.py:9595, :9723, :10912, :11063, :19296, :19688 and write.py:1924. Each of the 7 `except Exception` arms HOLDS with `veto cell is unreadable (<exc>)` (write.py:1926 sets `_frozen = True`) | MET |
| .13.2 | F3: the existing suite equals the trunk's before the build | NOT re-run by me (it is a whole-suite run). SM's reading in the goal's THOUGHT: the landing's full run on tmpfs = the same 98 red ids as a trunk tree, empty diff | SM's reading, not mine |
| .13.2 | F4: the retired-grid caller rows | the `_button_down` / `_grid_commit` rows are in test_veto_fail_closed.py (grep finds both names there); inside the 68 passed | MET |

**Where the bytes differ from the goals' text** (g1.43 row 5, a demote of exactly this): goal .13.1's title and body say `evidence_enforce` runs "every 5 min" on "box: local-town". The trunk's crons.md has `evidence_enforce: every_mins: 30, box: encryption-town` (why_box: it edits node files on MAIN, which lives there; local-town is parked), and `test_crons_flip_successors.py` pins `EVERY30` (:38) and the real-node row (:207). `town_mirror` stays at 5. The retune came in SM's A1 (d5aa705464, 10-10) and is not in the goal's body. The jobs are right; the goal text is stale.

Another difference in the opposite direction: .13.2's F5 exempts one call BY NAME (rotate.py:19601, the best-effort `active_gate` lookup). That call now takes the strict `_geom` (rotate.py:19695, inside the frozen branch, its `except` only sets `_gate = None`), so no non-strict read is left to exempt.

Landings (all ancestors of fd54ab759b): .13.1 = SM's a056c7651e (DG3 code 44cb6e921a, ea64da25eb, 4e9bd4d38f; my nodes d5aa705464, signed); .13.2 = SM's 4b84358559 (DG4 61b4d23876; my rows 4f3546b7c6).

## Measures
pytest per file, no cache, `env -u TMUX -u TMUX_PANE`, in a clone at fd54ab759b; greps at the same sha. 114 tests in the four files, all passed.

## Left for the next lines
- g1.43 row 5: the goal .13.1's body and title still say 5 min / local-town. A text fix on the goal node (not this outcome), SM's row.
- The suite-wide F3 of .13.2 rests on SM's 98-id comparison; no one has re-run it on this trunk.
- The flip itself and E2d (does root push refs/grid at all) are out of scope of both goals and belong to belam.
