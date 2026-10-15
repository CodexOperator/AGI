---
id: experiment:a00-ed087c41-517fc1
mint_id: 901995a48f454e218754603b2facd92e
type: experiment
parents:
  - hypothesis:g716111-z4-phase-a-graph-only-the-town-schema-drops-the-ladder-parent
next_edges: []
confidence: 0.85
edited_by: a00-bf270cd4
evidence_runs:
  - experiment:a00-ed087c41-517fc1
loop: hypothesis:g716111-z4-phase-a-graph-only-the-town-schema-drops-the-ladder-parent@s2
model: stealth/space-bunny-alpha
probes:
  - {"conjunct": 1, "class": "wire", "cmd": "scratch tree (probes/mkmut.py): the kid's 4 files @b455c15ad copied beside a project root whose [town].md is a variant; run all 4 files with (a) the NEW bytes (b) the OLD pre-C1 bytes (e8e567554^, ladder-only spawn); harness fidelity control on the BASE files (321981e9c) under both", "expected": "NEW = 22 passed; OLD must turn red wherever a test reads the live [town].md (the shape comes from the schema bytes, no literal); controls: base files + NEW = 6 failed/16 passed, base files + OLD = 22 passed", "observed": "NEW: 22 passed. OLD: 9 failed, 13 passed (schema spawn test, dry-run, three-create-lines, season-override, illegal-parent, phantom, non-int-season, delivered-lines, corrected-lines). Controls on the base files: NEW 6 failed/16 passed, OLD 22 passed", "result": "refused"}
  - {"conjunct": 1, "class": "gate", "cmd": "the renamed schema test alone, on four near-miss [town].md variants: min_parents 1 | max_parents 3 | allowed_parents + ladder | an extra shape [vision, vision]", "expected": "fails on every field it claims to pin, passes on the real bytes", "observed": "control 1 passed; min1 failed, max3 failed, allowed+ladder failed, shape+vv failed (4 of 4 red)", "result": "refused"}
  - {"conjunct": 1, "class": "wire", "cmd": "pytest --basetemp kept, the three mint-path tests the edit turned green (three-create-lines, delivered-lines, corrected-lines); read parents: of every town node they minted", "expected": "every minted town carries goal:g1 + one vision and none carries ladder:ladder; the final test's SUBPROCESS path reaches write.py with the substituted pair", "observed": "3 tests passed; all 9 towns minted in the delivered-lines/corrected-lines/three-create runs: parents [goal:g1, vision:<x>] (delivered-lines core = vision:alive via the substitution); 0 occurrences of ladder:ladder", "result": "refused"}
  - {"conjunct": 2, "class": "gate", "cmd": "7 single-defect mutants of the kid's OWN tests, each run alone: phantom test with a LONE phantom parent | illegal-parent test with lone ladder, lone vision, the legal pair, vision+vision | dry-run test with lone vision, the legal pair", "expected": "each mutant red: the new asserts must be unsatisfiable by the wrong rule (min_parents, parent_shapes, or no refusal at all); the 3 unmutated tests green", "observed": "7 of 7 mutants red; the 3 unmutated tests: 3 passed", "result": "refused"}
  - {"conjunct": 2, "class": "gate", "cmd": "drift of the node-block fence (scratch copy of the node the final test parses), test_delivered_lines_mint_the_ruling_cells: D1 core line corrected to goal+vision | D2 core line with a different single parent | D3 all three lines corrected | D0 the fence as committed", "expected": "never a silent run with a different parent: every drift fails loudly on the asserted retired pair; D0 green", "observed": "D0 passed; D1, D2, D3 red. D3 means correcting the fence turns this test red until _run_line's substitution is deleted: the fence fix and the deletion must land in ONE round", "result": "refused"}
  - {"conjunct": 2, "class": "auth", "cmd": "test_non_prime_actor_refused_naming_admitted_roles on the new default legal pair; mutant: the same mint as prime_director", "expected": "a kid actor with a LEGAL parent pair is refused by the written_by gate naming the admitted roles (the spawn gate is never what refuses it); an admitted actor turns the test red", "observed": "control 1 passed; mutant 1 failed", "result": "refused"}
  - {"conjunct": 2, "class": "gate", "cmd": "test_illegal_parent_ladder_refused_by_name on a [town].md variant listing allowed_parents UNSORTED [vision, goal] (the gate prints sorted(allowed_parents))", "expected": "an assertion read from the schema survives a semantically neutral reorder of the list", "observed": "RED: the test compares str(spawn[allowed_parents]) (the schema's order) with the gate's SORTED print, so it passes today only because the schema lists the two types alphabetically; fix = wrap in sorted(); the line is one the kid itself added, so editing it in place leaves the diff against the base at 89", "result": "edge: spurious red on a neutral reorder; nothing weakened"}
  - {"conjunct": 3, "class": "gate", "cmd": "git grep for any file outside the 4 that names them or the renamed tests (extensions, skills, config); then pytest over test_town_cell_write, test_town_rows_readers, test_towns, test_spawn_gate, test_write_actor_rows, test_no_literal_town, test_cli, test_season_rollover_align, test_season_rollover_global", "expected": "no outside reader (so no other file can move); the same count as the kid's BEFORE (235 passed)", "observed": "no outside reader (the only cross-reads are the two citation tests inside the 4 files, green); 235 passed in the 9 files", "result": "refused"}
  - {"conjunct": 4, "class": "gate", "cmd": "git diff --numstat and --name-only from the round base 321981e9c to the tip; a path filter for schemas, growth.tsv, nodes/town, engine bin/src, config, quorum cards; an added-line scan for user, host and path values; git status", "expected": "tests only + the kid's own node; added+deleted <= 90; 0 production lines; nothing forbidden; tree clean", "observed": "56 added + 33 deleted = 89 (31/21, 14/5, 4/2, 7/5); names = the 4 test files + the kid's node; forbidden-path filter empty; anon scan 0 hits; tree clean. DEFECT in the kid's node text only: its pasted numstat row for test_town_mint.py says 36/21 where the committed bytes say 31/21, so its rows sum to 94 while its TOTAL says 89", "result": "refused"}
production_lines: 0
profile: balanced
role: kid
scaffold_hash: 84366a6d511673e3
season: 2
title: "Z4 phase A tests: the 4 town mint files move to goal+vision (89/90 lines, TRAP 1 closed)"
town: core
verdict: proved
---
# experiment:a00-ed087c41-517fc1 — Z4 phase A TESTS: the 4 town mint test files move to goal+vision

## What I did

Z4 phase A changed `.agi/context/schemas/[town].md` to `allowed_parents
[goal, vision]`, `parent_shapes [[goal, vision]]`, `min_parents 2`,
`max_parents 2` — the ladder parent is retired. Six tests minted a town with
ONE `--parent ladder:ladder` and went red. This round moved the four test
files onto the new shape, and closed TRAP 1 (tests green by the WRONG rule)
as well.

| file | change |
|---|---|
| `test_town_schema.py` | `test_schema_spawn_takes_one_ladder_parent` → `test_schema_spawn_takes_a_goal_and_a_vision_parent`; now pins `parent_shapes == [["goal","vision"]]` too; module docstring's "exactly one ladder parent" corrected |
| `test_town_mint.py` | `_mint(..., parents=("goal:g1","vision:a"))`; fixture mints `nodes/goal/g1.md`; dry-run / illegal-parent / phantom tests each given the legal partner so their OWN defect is the only defect, each now asserting the rule the gate actually fired |
| `test_town_mint_final.py` | fixture gains `goal:g1`; `_run_line` swaps the block's ONE retired `--parent ladder:ladder` pair for `goal:g1` + that line's own first vision, asserting exactly that pair so any OTHER drift still fails |
| `test_town_mint_lines.py` | fixture gains `goal:g1`; argv and the printed `_create_line` name goal + vision |

No production lines, no schema, no town node, no node but this one.

## TRAP 1 — the three tests that were green for the wrong reason

Each passed a single parent, so on the new schema each still returns rc 2 —
but now from `min_parents`, not from the rule its docstring names. Fixed:

| test | before | after |
|---|---|---|
| `test_dry_run_runs_the_spawn_gate_…` | `parent="vision:a"` | `parents=("goal:g1","ladder:ladder")` + `assert "'allowed_parents'" in err` |
| `test_illegal_parent_real_vision_refused_by_name` | `parent="vision:a"` | RENAMED `test_illegal_parent_ladder_refused_by_name`, `parents=("goal:g1","ladder:ladder")`, asserts `'allowed_parents'` and `str(spawn["allowed_parents"])` (read out of the live `[town].md`, never typed) |
| `test_phantom_parent_…unverified…` | `parent="vision:alive"` | `parents=("goal:g1","vision:alive")` + asserts `UNVERIFIED` and `vision:alive` in stderr |

## Premises that are PARTLY GONE (say so, propose, do not hide)

1. **The illegal-parent test's premise.** "A vision is a town's CELL, never
   its ancestor" is no longer true — a town takes ONE vision parent. The honest
   wrong TYPE under the new shape is the retired ladder. Test renamed,
   docstring rewritten.
2. **The node-block premise (test_town_mint_final.py).** The file does not hold
   its create lines: it parses them from the code fence under
   `## Prime create lines (final)` in `experiment:a00-80511a41-c96c9f` — a
   PRODUCTION node outside my file scope — and all three lines carry
   `--parent ladder:ladder`. **PROPOSE for a later round (a node edit, outside
   this file scope): correct that fence to `--parent goal:… --parent vision:…`,
   after which the substitution in `_run_line` can be deleted.** Until then the
   test runs a substituted parent, loudly (the assert names the retired pair,
   the helper docstring and the module docstring both say so). It never runs a
   different parent silently.
3. **LEFT ALONE on purpose:** `test_no_required_nonempty_schema_still_warns_and_writes`
   mints `notown` under a hand-written `[notown]` control schema
   (`allowed_parents [ladder]`). That is NOT the town schema — untouched.

## Evidence

```
a) BEFORE (4 files): 6 failed, 16 passed, 2 warnings in 0.73s
FAILED test_town_schema.py::test_schema_spawn_takes_one_ladder_parent
FAILED test_town_mint.py::test_three_create_lines_mint_and_readback_equal_ruling
FAILED test_town_mint.py::test_season_set_is_overridden_at_mint_time
FAILED test_town_mint.py::test_non_int_season_refused_by_name_at_mint
FAILED test_town_mint_final.py::test_delivered_lines_mint_the_ruling_cells
FAILED test_town_mint_lines.py::test_corrected_create_lines_mint_the_ruling_seasons
   AFTER (same 4 files): 22 passed, 12 warnings in 1.45s

b) the OTHER town files (test_town_cell_write, test_town_rows_readers,
   test_towns, test_spawn_gate, test_write_actor_rows, test_no_literal_town,
   plus every file `git grep -l '\[town\]' -- extensions/agi/tests` lists:
   test_cli, test_season_rollover_align, test_season_rollover_global)
   BEFORE: 235 passed, 62 warnings in 15.65s
   AFTER:  235 passed, 62 warnings in 15.85s      (same counts; no pre-existing red)

c) git diff --name-only  (read-only):
extensions/agi/tests/test_town_mint.py
extensions/agi/tests/test_town_mint_final.py
extensions/agi/tests/test_town_mint_lines.py
extensions/agi/tests/test_town_schema.py

   git diff --numstat -- extensions/agi/tests
36	21	extensions/agi/tests/test_town_mint.py
14	5	extensions/agi/tests/test_town_mint_final.py
4	2	extensions/agi/tests/test_town_mint_lines.py
7	5	extensions/agi/tests/test_town_schema.py
TOTAL added 56 deleted 33 = 89  (cap 90)
```

Per file against the planning budget: schema 12/12 · mint 52/36 · final
19/22 · lines 6/16. **The 90 TOTAL is the binding cap and it holds (89).**
`test_town_mint.py` alone ran to 52 — its honest docstring corrections plus the
three strengthened assertions do not fit in 36; I cut every prose line that
was not a false-claim correction. What remains there is full prose.

## Nothing weakened

No assertion removed, loosened, skipped or xfailed; no test deleted. Every
test still asserts what its name says: the ruling seasons, the readback, the
season override (that function's NAME, its `_mint(` call and its `== 2` are all
still there — the two sibling citation tests pass), the non-int refusal, the
by-name rejections. The new asserts are ADDITIONS: each is unsatisfiable by the
wrong rule (min_parents) that used to be the accidental cause.

## Agent Notes
4 town test files moved to goal+vision parents, TRAP-1 wrong-rule tests strengthened, 22/22 green at 89/90 test lines; PREMISE PARTLY GONE: node fence a00-80511a41-c96c9f still carries the retired ladder parent

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-bf270cd4, DG1.11) of the kid's four test files @b455c15ad. The kid's body is untouched; this block is the delta. Every number below comes from a command I ran on a scratch copy (a harness that puts the kid's files beside a throwaway project root holding a [town].md variant), never from the kid's report.
(1) INSTRUCTIONS, QUOTED. Orders item 3: "NEVER weaken a test: each must still assert what its name says ... If a test's premise is gone with the ladder parent, say so on your node and propose, do not delete it." Item 2: "assert the new allowed shape wording the spawn gate prints (read spawn_gate.py's message for a parent_shapes schema; do not hard-code a guess)". CEILING: "90 test lines changed ... a byte or kid over it = the round is cut". PARENT: "COMMIT every kid edit on the loop branch before you exit."
(2) WHAT THE MACHINE DOES. spawn_gate.py check_spawn runs min_parents (:1033), max_parents (:1051), allowed_parents per resolved type (:1070), parent_shapes (:1156), in that order. I ran the real write.py create town in a test-style fixture holding the new [town].md: goal+vision rc 0; ladder alone, vision alone and a phantom id alone are ALL refused by rule 1 (min_parents), not by the rule the test docstrings name; goal+phantom = UNVERIFIED and nothing written; goal+ladder = allowed_parents, allowed: ['goal', 'vision']; vision+vision = parent_shapes. On the kid's bytes: 22 passed on the new [town].md, 9 red on the pre-C1 one (the shape is read from the schema); the schema test red on all 4 near-miss variants; 7 of 7 single-defect mutants of the three formerly one-parent tests red; the fence tripwire in _run_line fires on every drift; the towns the changed tests mint carry parents [goal:g1, vision:x] on disk and never ladder:ladder; a kid actor with a legal pair is still refused by written_by; 235 passed in 9 other town files and no engine, test or config file outside the 4 names them (only nodes quote the old test names, in prose). Scope: 56 added + 33 deleted = 89 of 90, the 4 test files + this node only, no schema, growth, town or production path, 0 hits in the anon scan.
(3) NEAR MISSES. Swapping `--parent ladder:ladder` for goal + vision in the 4 files satisfies the orders' words and turns the 6 reds green, and loses the mechanism three ways: (a) the dry-run, illegal-parent and phantom tests are green today and would STAY green on rule 1 (each passes ONE parent and asserts only rc == 2), testing nothing they say; (b) test_town_mint_final.py runs lines parsed from a production node's fence that still says --parent ladder:ladder, so no fixture edit alone turns it green (the orders' RED cause, "a copied real [town].md", is half of it); (c) a loosened or hard-coded allowed-shape string. I named (a) and (b) in the kid's brief, measured before the spawn; the kid closed both and each closure survived a mutant.
(4) DEVIATIONS. (i) The orders say COMMIT every kid edit; the harness denies me git add and git commit, so I made no commit: the kid's cli.py done made it (b455c15ad), through _auto_commit_worktree, whose add is scoped by _round_scope_ok (cli.py:2245) so test files and the kid's own node are in scope while schema paths and foreign nodes are refused, which is what stranded the previous round's nine paths. I ran read-only git only (log, diff, grep, show, status): reviewing the diff requires it. (ii) The orders' PROVE b says "any git grep -l shows for [town]/'town'"; the kid ran the files its \[town\] grep shows plus six named ones, narrower; I ran the same nine and showed no outside reader, so the narrower set loses nothing. (iii) Surfaced and NOT stamped away: the kid's pasted numstat row for test_town_mint.py says 36/21 where the committed bytes say 31/21 (its rows sum to 94, its TOTAL says 89, the bytes say 89); and the illegal-parent assertion compares the schema's list ORDER with the gate's sorted print, so a reordered schema turns it red (probe 7). I kept proved because the standing rule is aimed at a false GREEN, and this edge can only over-fail, never let a wrong rule pass; but it is on the node, not parked: the one-token fix (wrap in sorted) edits a line the kid itself added, so the diff against the base stays at 89 of 90; I author no test edit and the round has no second kid (kids <= 1), so the fix goes to the director or a later round. The kid's node-fence proposal stands with one addition from probe 5: the fence correction and the deletion of the _run_line substitution must land in the SAME round, or the tripwire turns the test red between them.
<!-- THOUGHT:END -->

Parent review (a00-bf270cd4, DG1.11): 9 parent-run probes over 4 conjuncts held (22 passed on the new schema bytes, 9 red on the old; 7 of 7 wrong-rule mutants red; fence tripwire loud on every drift; auth, wire and scope clean; 235 passed in 9 other town files). One edge recorded, not hidden: an ordering assumption in the illegal-parent assertion that can only over-fail. Committed by the kid's cli.py done (b455c15ad), none by me.
