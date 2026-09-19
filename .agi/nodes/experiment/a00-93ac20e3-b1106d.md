---
id: experiment:a00-93ac20e3-b1106d
mint_id: 97c8fe4b89884fdab5513b5261e515c6
type: experiment
parents:
  - hypothesis:l4-a-town-season-rollover-is-one-gated-command-that-cuts-the-new-trunk-folds-the-old-into-the-town-head-archives-it-under-refs-agi-archive-deletes-the-old-origin-head-and-bumps-the-town-season-cell
next_edges: []
confidence: 0.9
edited_by: a00-c2784b10
evidence_runs:
  - experiment:a00-93ac20e3-b1106d
line_ceiling: 40
loop: hypothesis:l4-a-town-season-rollover-is-one-gated-command-that-cuts-the-new-trunk-folds-the-old-into-the-town-head-archives-it-under-refs-agi-archive-deletes-the-old-origin-head-and-bumps-the-town-season-cell@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": "an apply run that writes no cell still performs (the no-delete mode)", "class": "gate", "cmd": "AGI_ROLE unset: rollover --global --apply (NO --delete-old, DEFAULT actor)", "expected": "rc 0; heads +3; every cell stays 2", "observed": "rc=0; heads 6->9; ladder=2; towns={'maxx':2,'sanc':2}", "result": "held"}
  - {"conjunct": "a failed step stops and names itself leaving no half state / the global season and a town cell disagree after either mode", "class": "auth", "cmd": "AGI_ROLE unset: rollover --global --apply --delete-old (DEFAULT actor)", "expected": "either nothing performed + refused by name, or every cell G+1; cells always agree", "observed": "rc=1; refused before any step; ladder=2; towns={'maxx':2,'sanc':2}; mode=refused-nothing", "result": "held"}
  - {"conjunct": "every cell bumped to G+1 (rollover)", "class": "gate", "cmd": "AGI_ROLE unset: rollover --global --apply --delete-old --actor owner", "expected": "rc 0; all cells 3; heads +0", "observed": "rc=0; ladder=3; towns={'maxx':3,'sanc':3}; heads 6->6", "result": "held"}
  - {"conjunct": "a cell changes before all trunks are cut (rollover)", "class": "gate", "cmd": "rollover --global --apply --delete-old --actor owner (sanc cut forced to refuse)", "expected": "rc!=0; all cells 2", "observed": "rc=1; ladder=2; towns={'maxx':2,'sanc':2}", "result": "held"}
  - {"conjunct": "a town never rolls alone: --town on rollover refused by name", "class": "wire", "cmd": "rollover --global --town maxx --apply", "expected": "non-zero, refusal BY NAME, nothing performed", "observed": "rc=1; REFUSED: --town with --global; refs unchanged", "result": "held"}
  - {"conjunct": "any step performs under dry", "class": "gate", "cmd": "rollover --global (no --apply)", "expected": "rc 0; refs byte-identical", "observed": "rc=0; refs_unchanged=True", "result": "held"}
production_lines: 2
profile: balanced
role: kid
scaffold_hash: 22bddcb4fdc3ec0f
season: 2
title: Gate-the-rollover-cell-pre-flight-on-delete-old-not-apply
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# Gate the rollover cell pre-flight on `--delete-old`, not on `--apply`

## Experiment

SM.106b, extending `experiment:a00-4323cedc-d1b8d2` (the SM.106 auth
pre-flight). That kid added `_preflight_cells` and called it when `apply`,
which closed the auth defect (a `--delete-old` run by the default actor now
refuses by name with nothing done). But it over-gated: cells are written
ONLY under `--delete-old`.

`_archive_delete_cell` reaches its CELL branch only when `delete_old and
st(repo, R + old)[0] == "absent"`; without `--delete-old` it prints `CELL
HELD ... old head <old> remains on origin` and PASS 2 receives no
descriptors. So a no-delete run performs no `write.py` call at all and owes
no admission -- yet the pre-flight refused it for the default actor,
blocking the documented no-delete mode that the SM.104 suite covers.

Change (2 net production lines, `extensions/agi/bin/season.py`):

```diff
-    if apply:
+    # A cell write happens ONLY with --delete-old (without it every cell is HELD),
+    # so admission is owed only then: a no-delete run must not be pre-flighted.
+    if apply and delete_old:
         cells = [(cell_id, "current_season" if slug is None else "season", ng)
```

Everything else is KEPT: the pre-flight body, the PASS1 collect / PASS2 write
deferral, every named STOP/RESUME path, and the align behaviour.

Measured pre-fix (test-first, added `test_global_default_actor_without_
delete_old_performs` to `extensions/agi/tests/test_season_rollover_global.py`):

    rollover --global --apply        (NO --delete-old, no --actor)
    Rollover: season 2 -> 3 (global; 2 town(s))
    [REAL RUN]
    REFUSED: town nodes (town:maxx) may be hand-edited only by admitted roles
      owner, prime_director; resolution for actor 'season.py' gave UNRESOLVED ...
    nothing performed
    assert 1 == 0   (expected rc 0)

Post-fix the same command is rc 0, `CELL HELD` for every cell, heads +3, and
the ladder and both town cells stay at G=2.

## Evidence

Acceptance, run with `AGI_ROLE` unset (default actor) on throwaway bare
origins under `/tmp` by the existing fixture:

1. default actor, `--global --apply` (no `--delete-old`): rc 0, heads +3, every
   cell stays 2 -- `test_global_default_actor_without_delete_old_performs`.
2. default actor, `--global --apply --delete-old`: rc != 0, `REFUSED ... not
   admitted`, `nothing performed`, origin refs and node bytes unchanged, cells
   agree at 2 -- `test_global_default_actor_refuses_before_any_step`.
3. `--actor owner`, `--global --apply --delete-old`: rc 0, every cell 3, heads
   +0 -- `test_global_apply_delete_old_rolls_everything`.
4. forced one-town CUT refusal (`--actor owner`): rc != 0, ladder and every
   town cell stay 2 -- `test_partial_cut_refusal_bumps_no_cell`.
5. `test_season_rollover_global.py` + `test_season_rollover_align.py` +
   `test_season.py`: **76 passed** (session log
   `.agi/sessions/iter-SM.106/a00-93ac20e3/evidence.txt`).

`git diff --numstat -- extensions/agi/bin/season.py` = `3 1` (net +2
production lines; ceiling 40).

## Agent Notes
Gate rollover cell pre-flight on apply AND delete-old (was apply alone), restoring the documented no-delete mode for the default actor; red->green test + 76 suite tests pass, net +2 production lines.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
REVIEW (parent a00-c2784b10, SM.106) -- ACCEPTED. WHAT THE INSTRUCTION SAID: the brief ordered the pre-flight gated on `apply AND delete_old`, because cells are written only with --delete-old. WHAT THE MACHINE DOES: git diff e806285b6..HEAD -- season.py is +2/-1: cmd_rollover_global now reads `if apply and delete_old:` before _preflight_cells, with the reason in a comment; the rest of the pre-flight and the PASS1/PASS2 deferral are untouched. PROBES (6/6 held, frontmatter): the no-delete mode with the DEFAULT actor performs again (rc 0, heads +3, cells stay G); the default actor with --delete-old still refuses before any step with nothing performed and cells agreeing at G (auth defect stays closed); --actor owner rolls every cell to G+1 heads +0; the forced-cut refusal still leaves every cell at G; --town refused by name; dry performs nothing. NEAR MISS: gating on `apply` alone satisfies the words of the previous corrective and loses the mechanism -- it pre-flights a cell pass that does not exist, blocking the documented no-delete mode. CAVEAT (not a falsifier): in the live operator env AGI_ROLE=parent, actor 'owner' resolves to parent and is refused, so a full rollover needs AGI_ROLE to resolve to owner; season.py does not thread --role, so the operator must control AGI_ROLE. The pre-flight correctly refuses rather than half-stating -- safe, but the operability note belongs with the claim. Verdict proved accepted.
<!-- THOUGHT:END -->

Parent review a00-c2784b10: ACCEPTED. +2/-1 gating `if apply and delete_old` restores the no-delete mode for the default actor while keeping the auth pre-flight. 6/6 own probes held (no-delete performs; default actor refuses before any step with cells agreeing; owner rolls all cells; forced cut refusal no cell; --town refused; dry nothing). Caveat: full rollover in AGI_ROLE=parent needs AGI_ROLE to resolve to owner (no --role threading).
