---
id: hypothesis:g716111-aa2-the-ladder-retires-in-order-when-dispatch-has-no-users
mint_id: dda89eb4de0242e6830c107600cd8deb
type: hypothesis
parents:
  - goal:g7.16.1.11.12
  - goal:g7.16.1.11.15
next_edges: []
confidence: 0.6
edited_by: director-general-1
scaffold_hash: 22167c26ccbfcfbe
season: 2
testable_claim: "(1) v4 kids read the inherited `kid` cell now; (2) workflow.py resolves every stage via `kid-of <invoking post>` overridden by a per-stage `model` in the workflow's own manifest, with the ladder file ABSENT (AA2.25): only DIRECTOR stages change, claude-fable-5-1 -> the kid cell's model (Sonnet 5.5, by the owner's 'every subagent Sonnet 5.5'), a deliberate change not drift; a manifest that needs Fable names it per stage; (3) each old-setup post's move to v4 removes one dispatch.py / heal.py user; (4) when dispatch.py has 0 users and workflow.py reads 0 role rows, the ladder retires and nothing reads a role row while it stands (gate G4); season.py's rollover write of ladder:ladder and claude-code.toml's `source = 'ladder'` go into all-is-one's cell map BEFORE step (3); 0 ladder reads on the v4 path before and after (AA2.24, alive's count)."
title: "AA2.24/25: the ladder retires in four ordered steps -- v4 kids read the inherited cell, workflow.py resolves a stage as a kid of the invoking post BEFORE anything retires, each old-setup post's move to v4 removes a dispatch.py/heal.py user, then the two role readers are gone and the ladder retires -- with 0 ladder reads on the v4 path before and after"
town: core
---
# hypothesis:g716111-aa2-the-ladder-retires-in-order-when-dispatch-has-no-users

## Measured
- doc:radically-simple-engine AA2 'Retire ORDER' (posts/self-perpetuating 265eb2c25, corrected on alive's AA1.L count 05:0xZ; belam 04:43Z [decision]): Owner 03:1xZ, verbatim (via belam 04:43Z [decision]): "Oh okay yeah well we should be phasing out the ladder anyway in favor of post trees. The ladder doesn't need to exist since each post already linked to templates and other stuff via the matrix math."
- The 8 ladder rows have THREE spawning readers: dispatch.py and heal.py (which imports it), both old-setup, and workflow.py (`_resolve_pi_model`: each pi stage's model = the ladder row for its (tier, role)). Workflows run by NAME from any post, so workflow.py is NOT old-setup-only: without the ladder its DIRECTOR stages go claude-fable-5-1 -> stealth/space-bunny-alpha (kid and parent stages unchanged). Without the ladder dispatch.py's resolve_role_spec drifts on 5 of its 8 role rows (the config fallback defaults to pi-free); 16 reader files (5 new since Z3); season.py WRITES ladder:ladder at rollover; claude-code.toml declares source = 'ladder'. Nothing is re-encoded byte-equal into rows.
- Split (04:5xZ): all-is-one LEADS (Z3: cells -> homes, the one resolver, the retire order) and carries the cell map (not yet on posts/all-is-one when this leaf was written: place this leaf under its lead's goal shape when it lands); alive re-counts readers + dispatch's kid gate; AA2 = what a spawn reads instead. alive's count also proves dispatch.py's tier-3 gate has a successor before the ladder retires.
- NOTE: belam wrote the tier-3 claude-code PARENT ladder row = claude-sonnet-5-5 at d9d1cb7a1 (04:2xZ), so the OLD setup reads the ladder today; this hypothesis does not touch it until step (4).

## CLAIM
(1) v4 kids read the inherited `kid` cell now; (2) workflow.py resolves every stage via `kid-of <invoking post>` overridden by a per-stage `model` in the workflow's own manifest, with the ladder file ABSENT (AA2.25): only DIRECTOR stages change, claude-fable-5-1 -> the kid cell's model (Sonnet 5.5, by the owner's 'every subagent Sonnet 5.5'), a deliberate change not drift; a manifest that needs Fable names it per stage; (3) each old-setup post's move to v4 removes one dispatch.py / heal.py user; (4) when dispatch.py has 0 users and workflow.py reads 0 role rows, the ladder retires and nothing reads a role row while it stands (gate G4); season.py's rollover write of ladder:ladder and claude-code.toml's `source = "ladder"` go into all-is-one's cell map BEFORE step (3); 0 ladder reads on the v4 path before and after (AA2.24, alive's count).

## Dispatch line
config-max: the cell map (tier row cells and caps.director_kids -> kid.max; season.py's rollover write; claude-code.toml source) is all-is-one's, Prime-landed; a per-stage `model` key in a workflow manifest where a stage needs Fable / template-max: none / code: workflow.py's stage resolution via kid-of (step 2, a build); the retirement edits come last.

## FALSIFIERS
AA2.25 workflow.py resolves every stage via kid-of + manifest override with the ladder file ABSENT; only director stages change, and only to the kid cell's model · AA2.24 0 ladder reads on the v4 path before and after the retire (alive's count) · after step (4): `git grep -n 'ladder' -- <extensions/agi/bin>` shows 0 reader files and the season rollover does not recreate ladder:ladder · negative: while dispatch.py or heal.py has a user, the ladder file and its 8 rows are untouched.

## TESTS
workflow.py stage-resolution tests with the ladder file absent (kid / parent / director stages, with and without a manifest override); alive's reader count re-run at each step; a season-rollover dry run asserting no ladder write; the old setup's dispatch tests stay green until step (4).

## FILE SCOPE
workflow.py (stage resolution, step 2) · the cell map (all-is-one) · season.py rollover · claude-code.toml · dispatch.py / heal.py retirement (last). HORIZON: strictly ordered by the old setup's move to v4; the owner's season wrap is the deadline.

## CEILING
1 parent · kids <= 2 · regular review. Step (2) is buildable now; (3)-(4) are BLOCKED BY each old-setup post's move to v4 (belam, SM, DG3, old TM).
