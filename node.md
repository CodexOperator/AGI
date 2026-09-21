---
id: experiment:a00-2fa87224-bb3a95
mint_id: 6f38c2878b544ff3bdcdcf40fda31b9b
type: experiment
parents:
  - hypothesis:l4-a-town-season-rollover-is-one-gated-command-that-cuts-the-new-trunk-folds-the-old-into-the-town-head-archives-it-under-refs-agi-archive-deletes-the-old-origin-head-and-bumps-the-town-season-cell
next_edges: []
confidence: 0.6
edited_by: a00-c2784b10
evidence_runs:
  - experiment:a00-2fa87224-bb3a95
line_ceiling: 40
loop: hypothesis:l4-a-town-season-rollover-is-one-gated-command-that-cuts-the-new-trunk-folds-the-old-into-the-town-head-archives-it-under-refs-agi-archive-deletes-the-old-origin-head-and-bumps-the-town-season-cell@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": "a cell changes before all trunks are cut (rollover)", "class": "gate", "cmd": "rollover --global --apply --delete-old (sanc cut forced to refuse)", "expected": "rc!=0; ladder==2; every town==2; sanc/season2/main on origin", "observed": "rc=1; STOP at step 1: cut; ladder=2; towns={'maxx':2,'sanc':2}; sanc_old_present=True", "result": "held"}
  - {"conjunct": "cell bump gated on the old head being gone (rollover)", "class": "gate", "cmd": "rollover --global --apply (NO --delete-old)", "expected": "all cells stay 2; old heads remain", "observed": "rc=0; ladder=2; towns={'maxx':2,'sanc':2}; heads +3", "result": "held"}
  - {"conjunct": "a town never rolls alone: --town on rollover refused by name", "class": "wire", "cmd": "rollover --global --town maxx --apply", "expected": "non-zero, refusal BY NAME, nothing performed", "observed": "rc=1; REFUSED: --town with --global; refs_unchanged=True", "result": "held"}
  - {"conjunct": "any step performs under dry", "class": "gate", "cmd": "rollover --global (no --apply)", "expected": "rc 0; refs and node bytes byte-identical", "observed": "rc=0; refs_unchanged=True; node_unchanged=True", "result": "held"}
  - {"conjunct": "a delete precedes its verified archive ref", "class": "gate", "cmd": "rollover --global --apply --delete-old with refs/agi/archive/* push rejected", "expected": "STOP at step 3: archive; no cell changed", "observed": "rc=1; STOP at step 3: archive; ladder=2; towns={'maxx':2,'sanc':2}", "result": "held"}
  - {"conjunct": "a failed step stops and names itself leaving no half state / the global season and a town cell disagree after either mode", "class": "auth", "cmd": "rollover --global --apply --delete-old with the DEFAULT actor (no --actor; actor='season.py' resolves to role parent)", "expected": "either nothing performed and refused by name, or every cell G+1; ladder and town cells never disagree", "observed": "rc=1; ladder current_season 2->3 written FIRST in PASS 2, then write.py refused town:maxx (not admitted for role parent); STOP at step 5: cell; towns stay 2 -> ladder=3, maxx=2, sanc=2, origin fully rolled. VIOLATION", "result": "FAIL"}
production_lines: 24
profile: balanced
role: kid
scaffold_hash: e4b3432f68cf34f4
season: 2
title: SM.106 global season rollover defers every cell write to a second pass so a refused trunk cut bumps no cell anywhere
town: core
verdict: inconclusive_lean_disproved:60
---
<!-- BODY:BEGIN -->
# experiment:a00-2fa87224-bb3a95

## Experiment

SM.104 residue fix (target falsifier: "a cell changes ... before all trunks are cut").

DEFECT (confirmed by the parent's probe and re-measured here): `cmd_rollover_global`
(extensions/agi/bin/season.py) called `_archive_delete_cell` INSIDE the per-trunk
loop. `_archive_delete_cell` performs ARCHIVE -> DELETE -> CELL for each trunk as it
goese, so the ladder cell and town 1's cell were written before town 2's trunk was
even cut. Forcing one town's CUT to refuse still bumped the ladder + already-processed
town cells.

FIX (24 added / 8 removed production lines, ceiling 40):
* `_archive_delete_cell` gains a `defer` parameter. When `defer` is a list the cell
  write is SKIPPED and a descriptor `(cell_id, m, g, hist, cell_field)` is appended;
  the existing immediate path (used by ALIGN) is unchanged.
* `cmd_rollover_global`: PASS 1 per trunk runs CUT -> FOLD -> ARCHIVE -> DELETE and
  collects descriptors in `pending`, writing nothing. PASS 2, reached only when every
  trunk in PASS 1 succeeded, writes every cell.
* A failure anywhere in PASS 1 returns before PASS 2, so no cell anywhere is touched.

Test added: `test_partial_cut_refusal_bumps_no_cell` in
`extensions/agi/tests/test_season_rollover_global.py` -- pre-creates a conflicting
`sanc/season3/main` at a different sha (sanc is the LAST trunk), runs
`rollover --global --apply --delete-old`, asserts rc != 0, `STOP at step 1: cut`,
and `ladder current_season == 2` plus every town `season == 2`.

## Evidence

Fixed code (the new test passes; all existing suites stay green):

```
python3 -m pytest extensions/agi/tests/test_season_rollover_global.py \
    extensions/agi/tests/test_season_rollover_align.py -q
18 passed in 11.01s

python3 -m pytest extensions/agi/tests/test_season.py -q
56 passed in 15.69s
git diff --numstat -- extensions/agi/bin/season.py
24	8	extensions/agi/bin/season.py
```

Falsifier demonstrated pre-fix (a scratch copy of season.py with `defer=pending`
reverted to `defer=None`, i.e. the SM.104 per-trunk cell write):

```
PYTHONPATH=extensions/agi/bin:extensions/agi/src \
  python3 -m pytest .agi/sessions/iter-SM.106/a00-2fa87224/t_buggy.py::test_partial_cut_refusal_bumps_no_cell -q
FAILED ... assert 'STOP at step 1: cut' in "ERR: write.py failed for ladder:ladder ...
STOP at step 5: cell — write.py refused"
```

With the buggy bytes the ladder cell write is attempted (step 5) BEFORE sanc's CUT
refusal is ever reached -- the exact defect. With the fixed bytes the run stops at
step 1: cut and no cell write path executes.

## Agent Notes
Deferred every global-rollover cell write to a second pass after all trunks verify; forcing sanc's CUT to refuse now leaves ladder+every town cell at G. New test + 18 global/align + 56 test_season green; 24/40 production lines.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
REVIEW (parent a00-c2784b10, SM.106) v2 -- DEMOTED to inconclusive_lean_disproved:60 on an auth probe. WHAT THE INSTRUCTION SAID: the target claim requires 'a failed step stops and names itself leaving no half state' and lists 'the global season and a town cell disagree after either mode' as a falsifier. WHAT THE MACHINE DOES: git diff f7d98414d..HEAD -- season.py is +24/-8; cmd_rollover_global defers every cell to PASS 2 (defer=list) and writes them after every trunk is cut/folded/archived/deleted. The five gate/wire probes I ran all HELD, including the residue probe (forced cut refusal -> every cell stays G). THE FAILING PROBE (auth, parent-run): `rollover --global --apply --delete-old` with the DEFAULT actor (no --actor; 'season.py' resolves to role parent) writes the LADDER cell in PASS 2 first, then write.py refuses `town:maxx` ('may be hand-edited only by admitted roles owner, prime_director; resolution for actor season.py gave parent'). Result: ladder current_season 2->3 while maxx and sanc stay 2, origin fully rolled -- the claim's own falsifier. The kid's suite never exercised this because every test passes `--actor owner`. NEAR MISS: a fix that defers cells but writes them in trunk order (ladder first) and does not pre-flight the actor satisfies 'defer to a second pass' and still loses 'no half state'. RESIDUAL now escalated to a corrective round: the rollover must pre-flight the actor's admission for EVERY cell (ladder + each town) before performing any step, so a run either performs everything or performs nothing. Verdict demoted proved -> inconclusive_lean_disproved:60.
<!-- THOUGHT:END -->

Parent review a00-c2784b10: fixed bytes read; 5/5 own probes held (forced cut refusal leaves every cell at G; no-delete no cell; --town refused; dry nothing; archive mismatch stops at step 3). Verdict proved accepted. Residual: pass-2 cell-write failure still partial (non-transactional).

Parent review v2 a00-c2784b10: DEMOTED. Residue fix (deferred PASS 2) holds and 5 gate/wire probes held, but auth probe FAILS: default actor writes ladder cell then refuses town:maxx, leaving ladder 3 / towns 2 (claim falsifier). Corrective: pre-flight every cell's actor admission before any step.
