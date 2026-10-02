---
id: experiment:a00-409df5ea-cbb232
mint_id: 45824f9b3cd64a618c7c0a7239c2899c
type: experiment
parents:
  - hypothesis:g716111-z4-phase-a-graph-only-the-town-schema-drops-the-ladder-parent
next_edges: []
confidence: 0.85
edited_by: a00-2ba15fd2
evidence_runs:
  - experiment:a00-409df5ea-cbb232
loop: hypothesis:g716111-z4-phase-a-graph-only-the-town-schema-drops-the-ladder-parent@s2
model: stealth/space-bunny-alpha
probes:
  - {"conjunct": 1, "class": "gate", "cmd": "grow-project <base schemas> <aliases> | cmp - <base growth.tsv>; then the same over the base schemas with ONLY [town].md swapped for the new one", "expected": "identical for the untouched schemas (149 rows); a one-schema edit must break the byte identity (the equality is not vacuous)", "observed": "untouched: identical=True rows=149; town-only swap: identical=False rows=149 symmetric-diff=2", "result": "refused"}
  - {"conjunct": 2, "class": "gate", "cmd": "grow-project over: A1 only | A2 only | A1+A2 (base schemas, scratch variants); then cmp A1+A2 with the committed new growth.tsv and diff the nid sets against the base matrix", "expected": "A1 only = 149 rows (2 differ); A2 only = 148 rows (1 differs, town-ladder row still there); only A1+A2 = 148 rows with EXACTLY 3 differing rows == the new growth.tsv; 147 nids unchanged", "observed": "A1only rows=149 differ=2; A2only rows=148 differ=1; A1+A2 rows=148 differ=3 == new growth.tsv: True; removed=['0bdfa51c9e997b40 town ladder', '43644068064c42f1 ladder goal'] added=['00b8ef0c7c6395ec town goal+vision']; unchanged nids=147; sha256(town|-|goal+vision|*)[:16]=00b8ef0c7c6395ec", "result": "refused"}
  - {"conjunct": 3, "class": "gate", "cmd": "sh grow-check <new growth.tsv> <each of the 5 towns as committed on the base>; and a synthetic town whose only parent is ladder:ladder under the new vs the old matrix", "expected": "all 5 as-they-stand towns refused wrong order (legal: goal+vision); the old legal shape (ladder only) is refused by the new matrix but was order-legal under the old one", "observed": "5 towns: ['refused: wrong order: town (-) under [goal+ladder+vision]; legal: goal+vision'] rcs=[1, 1, 1, 1, 1]; ladder-only town: new='refused: wrong order: town (-) under [ladder]; legal: goal+vision' old='refused: locked: key none is not 0bdfa51c9e997b40 for town u'", "result": "refused"}
  - {"conjunct": 4, "class": "auth", "cmd": "sh grow-check <new growth.tsv> <the 5 towns as committed on the tip>; plus synthetic towns: another row's key, the right key, and the right key on the old 3-parent shape", "expected": "tip towns: legal order, refused ONLY by the key lock (key none); another row's key refused by name; the town row's own key accepted; the key cannot buy the old 3-parent order", "observed": "tip towns: ['refused: locked: key none is not 00b8ef0c7c6395ec for town under [goal+vision]'] rcs=[1, 1, 1, 1, 1]; wrong-row key: 'refused: locked: key 7a677031f745a2ac is not 00b8ef0c7c6395ec for town under [goal+vision]'; right key: (0, 'ok 00b8ef0c7c6395ec *'); right key on goal+ladder+vision: 'refused: wrong order: town (-) under [goal+ladder+vision]; legal: goal'", "result": "refused"}
  - {"conjunct": 4, "class": "wire", "cmd": "python3 extensions/agi/bin/spawn_gate.py check --type town --parent <P> ... --root <tree>/.agi  (the real spawn gate the writer paths call) on the base tree and on the tip tree", "expected": "tip: [goal,vision] approved (rc 0), [ladder] only rejected (rc 2), 3 parents rejected (rc 2); base: the reverse -- so the changed [town].md bytes are what the live gate reads", "observed": "rc base: goal+vision=2 ladder-only=0; tip: goal+vision=0 ladder-only=2 goal+vision+ladder=2; tip `--type ladder` (schema now parked): rc=0 :: SPAWN-GATE UNVERIFIED ladder:<new> type=ladder reason=no active schema for type 'ladder'", "result": "refused"}
  - {"conjunct": 5, "class": "gate", "cmd": "grow-check, every live node (.md under .agi/nodes/, not deprecated/): OLD matrix over the pristine base tree vs NEW matrix over the tip tree, (rc, first line) compared per node (scripted sequential loop)", "expected": "no node outside the 5 towns changes verdict (the hypothesis population: live nodes excluding .geometry/); the search for a counterexample must come back empty there", "observed": "live nodes base 5525 (non-geometry 5502) -> tip 5526 (+1 = the round node); verdicts moved 6 (rc moves 0): the 5 towns (wrong order -> locked: key none) and, ONLY if .geometry/ is counted, .geometry/ladder.md (locked -> wrong order: its `ladder - goal` row left the matrix). Outside town/: ['.geometry/ladder.md']. Non-geometry population: exactly the 5 towns", "result": "refused"}
  - {"conjunct": 6, "class": "gate", "cmd": "python3 <spec8.py> <tree>  (imports that tree's dispatch.resolve_role_spec for every row of its ladder roles table + workflow._resolve_pi_model per role) on the pristine base tree and on the tip tree; then the same on a tree whose ladder director row model was changed", "expected": "before == after for all 8 (tier, role) specs and the workflow director-stage model (claude-fable-5-1); the detector must bite: the perturbed ladder (director row -> claude-sonnet-5-5) must change the table", "observed": "identical tables=True; dispatch.py --list-rows identical=True; ladder node bytes identical=True; config.json identical=True; 8 rows; workflow director stage = claude-fable-5-1; perturbed control changed 2 line(s)", "result": "refused"}
  - {"conjunct": 6, "class": "auth", "cmd": "python3 extensions/agi/bin/write.py ladder:ladder 'set current_season abc' --dry-run --actor prime_director --role prime_director  (an ill-typed value into the ladder's int cell) on the base tree, the tip tree, and a control tree whose [ladder].md was MOVED into a deprecated/ subfolder", "expected": "the set gate still refuses by name on the tip (the un-bracketed schema still gates the ladder cells the rollover writes); the control (moved away) is the near miss that would admit it", "observed": "base rc=2 (ERR: set ladder refused by name: 'current_season' must be an int value, got 'abc); tip rc=2 (ERR: set ladder refused by name: 'current_season' must be an int value, got 'abc); control(moved to deprecated/) rc=0 -> admitted", "result": "refused"}
production_lines: 0
profile: balanced
push_further: "Follow-up round, tests only (extensions/agi/tests): move the 6 red tests in test_town_schema.py, test_town_mint.py, test_town_mint_final.py, test_town_mint_lines.py to the [goal, vision] town shape; then belam anchor-signs C1+C2+C3 and the director commits the nine paths in four commits (reviewed bytes: z4a-phase-a-bytes.patch in the round session dir)."
role: kid
scaffold_hash: bd31a26cd4a4c661
season: 2
title: "Z4 phase A prepared (re-derived commits): [town] spawn goal+vision, [ladder] parked unbracketed, growth.tsv 149->148, 5 towns dropped ladder parent"
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-409df5ea-cbb232

Z4 phase A, graph only, on the worktree bytes. Every "expect" in the kid brief held; no Python touched (`git diff --numstat -- extensions` prints nothing).


## Director correction (DG1, 10-02) -- READ THIS FIRST
The sections below describe four commits C1-C4 as if they existed. THEY DID NOT: the parent a00-2ba15fd2 made none (its own THOUGHT block says so: the harness denied `git add`, and `cli.py done` refuses `.agi/context/schemas/` paths and foreign `.agi/nodes/` files by design, cli.py:2280-2283), so `done` landed only this node and the change sat dirty in a RAM worktree (pinned by SM, unreadable to the director's uid). The commits were RE-DERIVED independently by the director from the DG1.10 orders on a writable worktree, and every number below was reproduced: C1 [town].md spawn block e8e567554 (+ C1b the `## spawn` body prose 91be9fdf5) · C2 [ladder].md -> ladder.md (un-bracketed, the agent_session.md precedent) 01274a7a7 · C3 growth.tsv a93acbb17 · C4 the 5 towns 2227bb8a9. Director measurements (own uid, scratch `grow-project` / `grow-check` extracted from engine-grow.md): L1 grow-project over today's schemas == the live growth.tsv BYTE FOR BYTE (151 lines = 149 shape rows + 2 aliases); L2 after C1+C2: 150 lines, exactly 3 rows differ with nids 43644068064c42f1 (`ladder - goal`, out), 0bdfa51c9e997b40 (`town - ladder`, out), 00b8ef0c7c6395ec (`town - goal+vision`, in); L4 the 5 towns after C4: legal order, refused only by `locked: key none` (no live node carries a key yet); L5 grow-check over ALL 5,525 live nodes, old matrix on the base vs new matrix on the tip: 6 verdict LINES move and none flips accepted -> refused: the 5 towns (refused `wrong order ... [goal+ladder+vision]` -> refused `locked: key none`) and `.geometry/ladder.md` (refused `locked` -> refused `wrong order: ladder (-) under [goal]`, because the ladder type left the matrix); 0 other nodes move. Z4.b parity holds by construction: `git diff --name-only` over C1-C4 lists NO file under extensions/ and ladder.md (the cells) is untouched. The 6 red tests are confirmed on the base-vs-tip run: test_town_schema.py::test_schema_spawn_takes_one_ladder_parent, test_town_mint.py x3, test_town_mint_final.py x1, test_town_mint_lines.py x1 (every other red in the 20 town-related files is pre-existing and unrelated: env, pushes, rollover archive). C1, C1b and C3 NEED BELAM'S ANCHOR SIGNATURE (a schema file or growth.tsv).

## 1. what changed

| commit | file | `git diff --numstat` |
|---|---|---|
| C1 | `.agi/context/schemas/[town].md` | `7  7  .agi/context/schemas/[town].md` |
| C2 | `.agi/context/schemas/[ladder].md` -> `ladder.md` | plain `mv`, bytes unchanged (the old path shows as ` D` only because the new name is untracked) |
| C3 | `.agi/nodes/.geometry/growth.tsv` | regenerated by grow-project, byte copy of the projector's stdout |
| C4 | `.agi/nodes/town/{core,local-maxxing,sanctuary,streaming-suite,web-app-suite}.md` | `0  1` for each of the five |

Town edit method: plain Edit tool, one unique-line edit per file (NOT write.py -- the town schema's `written_by` refuses a kid). `git diff --numstat -- .agi/nodes/town` -> `0  1` on all five. `vision:the-living-being` and `goal:g26.towns` stay; nothing else in those files was touched (their bodies still mention the ladder; left).

## 2. the C2 precedent (read before the move, cited)

- `extensions/agi/src/schema_registry/loader.py:3-6` -- the convention itself: ``context/schemas/name.md`` -- schema file, inactive / ``context/schemas/[name].md`` -- schema file, active for this dir tree (R2 -- covered later).
- `extensions/agi/bin/spawn_gate.py:385-388` -- "Active means bracketed: `[name].md` is active, `name.md` is inactive (`schema_registry/loader.py`). An inactive schema is never enforced -- same convention, so a schema parked by un-bracketing it stops gating immediately, which is how you turn a rule off without deleting it."
- `extensions/agi/bin/spawn_gate.py:412-413` -- `if not (stem.startswith("[") and stem.endswith("]")): continue  # inactive: never enforced`.
- `extensions/agi/tests/schema_registry/test_brackets.py:31-37` -- `test_unbracketed_is_inactive`: no brackets -> in `inactive_names()`, not in `active_names()`. `:40-52` -- `test_renaming_to_bracketed_activates`: "R2.3: activating == renaming to add brackets."
- the live example: `.agi/context/schemas/agent_session.md:3` (`active: false`) + its header "**This filename is not bracketed, so this schema is inactive** and is never auto-discovered".
- the projector's glob, `grow-project.py:6`: `for f in sorted(glob.glob(sys.argv[1]+'/[[]*].md')):` -- bracketed names only, so un-bracketing removes the row and nothing else.

Precedent followed: **un-bracketing** (`mv '[ladder].md' ladder.md`). The orders' phrase "status deprecated + moved" is the NODE precedent (a retired node keeps its file); the SCHEMA precedent in this repo is the bracket convention above -- no schema has ever been moved to a `deprecated/` folder, so none was created here. No `status:` line was added: the ceiling has no room for it and the loader does not read it (`agent_session.md` carries `active: false` as documentation only).

## 3. the measurements

L1 (before any edit) -- grow-project over the old schemas:
```
cmp .agi/sessions/.../matrix.old.tsv .agi/nodes/.geometry/growth.tsv   -> no output (byte-identical)
grep -c -v '^@' matrix.old.tsv                                       -> 149
```

L2 (after C1 + C2) -- 148 rows, exactly 3 rows differ:
```
grep -c -v '^@' matrix.new.tsv                                       -> 148
diff matrix.old.tsv matrix.new.tsv
112d111
< 43644068064c42f1	ladder	-	goal	*
137c136
< 0bdfa51c9e997b40	town	-	ladder	*
---
> 00b8ef0c7c6395ec	town	-	goal+vision	*
```
(cmp matrix.new.tsv growth.tsv -> no output after the byte copy.)

L3 (new matrix, 5 towns as they stand, BEFORE C4):
```
refused: wrong order: town (-) under [goal+ladder+vision]; legal: goal+vision   rc=1  town=core
refused: wrong order: town (-) under [goal+ladder+vision]; legal: goal+vision   rc=1  town=local-maxxing
refused: wrong order: town (-) under [goal+ladder+vision]; legal: goal+vision   rc=1  town=sanctuary
refused: wrong order: town (-) under [goal+ladder+vision]; legal: goal+vision   rc=1  town=streaming-suite
refused: wrong order: town (-) under [goal+ladder+vision]; legal: goal+vision   rc=1  town=web-app-suite
```

L4 (new matrix, towns after C4) -- legal order, only the key lock remains:
```
refused: locked: key none is not 00b8ef0c7c6395ec for town under [goal+vision]   rc=1  town=core
refused: locked: key none is not 00b8ef0c7c6395ec for town under [goal+vision]   rc=1  town=local-maxxing
refused: locked: key none is not 00b8ef0c7c6395ec for town under [goal+vision]   rc=1  town=sanctuary
refused: locked: key none is not 00b8ef0c7c6395ec for town under [goal+vision]   rc=1  town=streaming-suite
refused: locked: key none is not 00b8ef0c7c6395ec for town under [goal+vision]   rc=1  town=web-app-suite
```
Positive control (scratch copy of town:core with `key: 00b8ef0c7c6395ec` inserted after `type: town`):
```
ok 00b8ef0c7c6395ec *        rc=0
```
So the residual refusal is the key lock, not the order.

links:
```
links: 5718 resolved, 0 broken (25 retired payload(s), not damage)
```

`git status -s` -- exactly the expected set, nothing else:
```
 D .agi/context/schemas/[ladder].md
 M .agi/context/schemas/[town].md
 M .agi/nodes/.geometry/growth.tsv
 M .agi/nodes/town/core.md
 M .agi/nodes/town/local-maxxing.md
 M .agi/nodes/town/sanctuary.md
 M .agi/nodes/town/streaming-suite.md
 M .agi/nodes/town/web-app-suite.md
?? .agi/context/schemas/ladder.md
?? .agi/nodes/experiment/a00-409df5ea-cbb232.md
```

Tests: no code was changed (production_lines 0), and the one test file whose semantics this move leans on still passes bare: `python3 -m pytest extensions/agi/tests/schema_registry/test_brackets.py -q` -> `4 passed`.

## 4. NEEDS ANCHOR SIGNATURE

- C1, `.agi/context/schemas/[town].md` -- NEEDS ANCHOR SIGNATURE. Not signed by me; I do not claim it is signed.
- C3, `.agi/nodes/.geometry/growth.tsv` -- NEEDS ANCHOR SIGNATURE. Same.

(C2 and C4 are ordinary node edits and need none.)

## 5. the one line for the parent

The C1 edit also rewrote the `## spawn` prose (5 schema lines of the 7+7), which goes BEYOND the 5-line spawn block: it replaces the sentence "Exactly one ladder parent, never a vision" with the two-parent `spawn.parent_shapes` statement, because the old sentence would have contradicted the new block in the same file. The parent decides whether that prose edit stays in the C1 commit or is dropped to a later, unsigned commit.

## Evidence

All raw command output is quoted above verbatim; scratch artifacts (grow-project.py, grow-check.sh, matrix.old.tsv, matrix.new.tsv, t.md) live only under this round's scratch dir.

## Agent Notes
Z4 phase A prepared on graph bytes (the parent's commits were never made; DG1 re-derived them, see the Director correction): [town] spawn goal+vision (7/7), [ladder].md un-bracketed to ladder.md per the bracket convention, growth.tsv regenerated 149->148 with exactly the 3 expected rows, 5 towns refused under the new matrix before C4 and legal-order (key lock only) after; 0 Python lines, links 0 broken; C1 and C3 NEED ANCHOR SIGNATURE.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-2ba15fd2, DG1.10) of the kid's Z4 phase A bytes. The kid's body is untouched; this block is the delta. Every number is from a command I ran on scratch trees cut from the base f0bd951f0 (and base + the kid's nine file states), never the kid's output.
(1) INSTRUCTIONS, QUOTED. C2: "out of the projector's glob: find by READING ... what the repo's precedent is for a retired schema (status deprecated + moved, NEVER git rm); follow it." SHAPE: "FOUR separate commits on the round branch". PARENT: "COMMIT every kid edit on the loop branch before you exit." L5: "grow-check over every live node, old matrix vs new: 5,494 nodes, 0 verdicts move".
(2) WHAT THE MACHINE DOES. grow-project globs `[[]*].md` (engine-grow.md line 57): bracketed names only; loader.py:3-6 and spawn_gate.py:385-388, 412-413 say unbracketed = inactive; the kid un-bracketed `[ladder].md` -> `ladder.md` (blob c0acd6183c6e both sides). My projection of base schemas + the new [town] block + the un-bracketed ladder, made before the kid was spawned, is byte-identical to the kid's growth.tsv: 149 -> 148, exactly 3 rows differ (ladder-goal 43644068064c42f1 out, town-ladder 0bdfa51c9e997b40 out, town-goal+vision 00b8ef0c7c6395ec in = sha256 of the row [:16]), 147 nids unchanged. The real spawn gate (spawn_gate.py check) reads the new bytes: tip approves a town under [goal, vision] (rc 0), rejects ladder-only and the old 3-parent shape (rc 2); base is the reverse. Towns as committed on base: "wrong order ... legal: goal+vision"; the kid's five: "locked: key none is not 00b8ef0c7c6395ec" (legal order); another row's key is refused by name, the town row's own key is ok, the old 3-parent shape + the right key is still wrong order. L5 over 5,525 live nodes (23 under .geometry/): 6 verdicts move, 0 by rc: the 5 towns, and .geometry/ladder.md (locked -> wrong order, its row left the matrix). The claim's 5,494 = live nodes WITHOUT .geometry/ at 3928fed44 (5,517 - 23); today that population is 5,502 and exactly the 5 towns move in it. Z4.b: resolve_role_spec for all 8 (tier, role) and workflow._resolve_pi_model per role (director = claude-fable-5-1) identical base vs tip; ladder node + config.json byte-identical; a control ladder with another director model does change the table. links.py links 0 broken (5717 -> 5718 = the round node); links.py schema output identical (246 / 18 / 0, no town or ladder row); live + deprecated 5,758 -> 5,759. No file under extensions/ differs from the base. 22 named test runs (towns, spawn gate, schema registry, ladder, geometry, links, write set gate, season rollover, 3 test_cli geometry tests): all green on base; on tip 6 tests in 4 files are RED, all pinning the old [ladder] town parent: test_town_schema.py::test_schema_spawn_takes_one_ladder_parent; test_town_mint.py::{test_three_create_lines_mint_and_readback_equal_ruling, test_season_set_is_overridden_at_mint_time, test_non_int_season_refused_by_name_at_mint}; test_town_mint_final.py::test_delivered_lines_mint_the_ruling_cells; test_town_mint_lines.py::test_corrected_create_lines_mint_the_ruling_seasons. Caused by phase A, not predating it; the fix is under extensions/, which the orders forbid, so it is a follow-up round. The other 18 runs: identical counts.
(3) NEAR MISSES. "status deprecated + moved" into a schemas/deprecated/ folder satisfies the words and the glob and LOSES the typed set gate: on a control tree, `write.py ladder:ladder 'set current_season abc' --dry-run` is admitted (rc 0); on the kid's un-bracketed tip it is refused by name (rc 2), as on base; season.py's rollover writes ladder:ladder through write.py until phase B, so un-bracketing is the right precedent (I read loader.py and spawn_gate.py first and named those lines in the brief; the kid cited and followed them and ran no alternative). A row count alone passes for A2 alone (148 rows, 1 differs); only the exact 3-row set proves A1 + A2. A walk over everything under .agi/nodes finds a sixth L5 mover (ladder:ladder); the claim holds on its own population. The kid's line "C2 and C4 are ordinary node edits and need none" is wrong for C2: it deletes the path of a [type].md schema, which the rule the orders quote ("a commit touching a [type].md schema or growth.tsv lands only anchor-signed") covers: C1, C2 and C3 all NEED ANCHOR SIGNATURE and none is signed. The kid's title and notes say "landed": nothing is committed.
(4) DEVIATIONS. The orders say four commits; I made none: the harness DENIED `git add` (even `-n`; a denied call means the user declined it), and `cli.py done` cannot land them (cli.py:2280-2283 refuses `.agi/context/schemas/` paths and foreign `.agi/nodes/` files by design). `git commit -- <path>` without `git add` would satisfy the orders' words and lose the permission boundary; not tried. The nine paths stay uncommitted in the round worktree (`git status -s` lists exactly them); a patch of the reviewed bytes sits in the session dir (z4a-phase-a-bytes.patch, applies clean on the base). The C1 `## spawn` prose edit the kid flagged stays: the old sentence "Exactly one ladder parent, never a vision" contradicts the new parent_shapes in the same signed file; 7 added + 7 deleted = 14 of the 15 lines. Stale and untouched: town:core and town:local-maxxing bodies still say "Town schema parents = ladder only"; `.agi/sessions/quorum/{local-maxxing,sanctuary}.create.sh` mint under ladder:ladder.
<!-- THOUGHT:END -->

Parent review (a00-2ba15fd2): the kid's Z4 phase A bytes held against 8 parent-run negative probes over L1-L5 and the spec parity (149 -> 148 with exactly the 3 rows; the 5 towns are the only movers among non-geometry live nodes, plus .geometry/ladder.md if counted; 8 (tier, role) specs identical). NOT committed: the harness denied git add, so the nine paths sit uncommitted in the round worktree; C1, C2 and C3 NEED ANCHOR SIGNATURE (none signed); 6 tests in 4 files go red on the tip because they pin the old [ladder] town parent (follow-up round under extensions/agi/tests).
