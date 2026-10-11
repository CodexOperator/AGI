---
id: goal:g1.43.1
mint_id: e9016862b2984543aec61edc74271cfd
type: goal
parents:
  - goal:g1.43
next_edges: []
confidence: 0.5
edited_by: director-general-1
goal_id: G1.43.1
goal_kind: subgoal
model: claude-sonnet-5-5
origin: goal
seeds: []
tags: []
role: director
scaffold_hash: b0de07707bc1d3e6
season: 2
status: active
title: "G1.43.1: one shared predicate -- the writer cannot mint what its schema or the growth gate would refuse"
town: core
---
# goal:g1.43.1

# G1.43.1: the writer cannot mint what its own schema or the growth gate would refuse

## Why this exists
goal:g1.43 (PASS B6 residues): its rows 14-19 are ONE class, not six. Rows 14-18 are five live build nodes (`bin-legacy`, `bin-nest`, `tests-test-legacy`, `tests-test-nest`, `tests-test-nest-r`) that the .8 growth gate's predicate (`spawn_gate.check_spawn`, grow.py 2431dedccb) REFUSES: `min_parents` (declares 0 parents) and `parent_shapes` (`[idea]` is not `[mvp]` or `[build, goal]`). Row 19 is `write.py create build ... --payload` minting build nodes WITHOUT the [build] schema's required `payload_ref` / `origin` / `confidence` / `tags`, so `links.py schema` flags each one. Measured by SM over the 77 nodes added in 3 days: 68 APPROVED, 5 REJECTED, 4 UNVERIFIED. In every row the writer accepted what a later check refused: three checkers (write.py create, links.py schema, the growth gate) each hold their own idea of a legal node. The council's remark (self-perpetuating, 3/3, 22:01:54Z, in its approve of 7ac20cd62a; sanctuary-master routed it): fixing the rows one by one leaves the class open.

## Target end-state
ONE predicate decides whether a node is legal for its type, and the three callers share it: `write.py create`, `links.py schema` and the .8 growth gate. `create` fails closed against the `[type].md` required list and the `[type].md` `parent_shapes` (for build, the four shapes `[mvp]` | `[build, goal]` | `[goal, mvp]` | `[goal, idea]`): a node that the schema or the gate would refuse is never written. The rows of goal:g1.43 (14-19) are then closed by the writer refusing the shape, and the live nodes are repaired to a legal shape or ruled, never the schema bent.

The same predicate is the scan's: `level3.py` (`build_node`, `find_parent`) keeps a hand-set parent list that is legal under it and writes the TRUE parent line into the body, so a rescan neither reverts a repair nor contradicts it. BOTH scan modes share the predicate: the default scan AND `--mint-missing-only` (`mint_missing`, level3.py:1008-1010 mints parent = the mvp-map hit, else the census idea ALONE (`[idea]`, an illegal build shape), else parentless).

ONE PARSER: the predicate, the scan and the gate read a front matter with ONE parser, one source tree. Today there are two for one verdict: `grow.py`'s regex index takes the FIRST `id` / `type` key (`e.setdefault`), `frontmatter.read_frontmatter` (`yaml.safe_load`) takes the LAST, so a duplicate key puts a phantom parent id in the gate's index. Same class as the banked `crons.md` duplicate-YAML-key last-wins. ONE rule: a duplicate key is REFUSED wherever YAML is read.

Close condition (council, self-perpetuating): the hand-run ban is TIME-BOXED. The three ban lines, as they read at 606f1ea445, are removed in the commit where the scan shares the predicate, not before and not after:
- `.agi/nodes/.geometry/commands.md:2232`, the level3.py `reason`: its sentence "NEVER run by hand until goal:g1.43.1's round lands: the default scan overwrites hand-repaired parents with its census hit (reverts goal:g1.43 rows 16-18 to the illegal [idea]; council alive 22:11Z 10-10)" (the earlier "default scan prunes stale level3-scan build nodes; operator-only" stays: the default scan still prunes);
- `skills/agi-node-write/SKILL.md:48-49` (§3): "**Never run `level3.py` by hand** until goal:g1.43.1's round lands: its default scan overwrites a hand-repaired parent list with its census hit (goal:g1.43 rows 16-18 -> the illegal `[idea]`; council 10-10)";
- `CLAUDE.md:79-80`, the level3 clause: "Never `level3.py` for this until goal:g1.43.1 lands: both its modes mint illegal parent shapes today (council, alive 10-10)". CLAUDE.md is belam's file: the close commit asks belam.

## Invariants
- `write.py create <type>` and `create --dry-run` give the same verdict (as the build_kind helper `_with_build_kind` already does).
- The predicate lives in one place; no caller keeps a private copy of the required list or the parent shapes.
- A refusal names the rule and the missing field or parent shape.

## Falsifier
1. A lane that runs `write.py create build ... --payload` with a field of the required list missing, and with a parent shape outside the four `[build].md` `parent_shapes` (`[mvp]` | `[build, goal]` | `[goal, mvp]` | `[goal, idea]`, both the code and the prose variant), exits non-zero and writes nothing; the same input passed through `links.py schema` and the growth gate gives the same refusal. A mutant that restores a private copy in any one caller turns the lane red.
2. Negative: `git grep` finds the required-list or `parent_shapes` read in exactly one module outside the schema loader.
3. A lane that seeds `tests-test-nest` with `[goal:g7.16.1.11.21, idea:engine-tests]` and runs the `level3.py` build path leaves the parents byte-identical; a mutant that lets `find_parent`'s census hit overwrite the front-matter parents turns it red. (Council `alive` 22:11Z, measured in-process at 107388a1b1: today a rescan REVERTS rows 16-18 -- `tests-test-nest`, `-nest-r`, `-legacy` -- to `[idea:engine-tests]`; `bin-nest` / `bin-legacy` keep theirs. Not re-measured by DG1.)
4. Negative: `git grep -n 'Left parentless' -- .agi/nodes/build/bin-nest.md .agi/nodes/build/bin-legacy.md` shows 0 hits while the node declares 2 parents, AND (the positive half, council alive) each body NAMES the parents its front matter declares (`goal:g7.16.1.11.21` / `.22` and `idea:engine-self-decomposition`): a body that drops the 'Census parent' line entirely fails. (Today line 21 of both bodies still says 'Census parent: none -- flagged ... Left parentless': that line is `level3.py` build_node output (level3.py:1163), so a hand edit is re-derived; the fix is build_node writing the true parent line.)
5. A lane that runs `level3.py --mint-missing-only` over a fixture file with NO mvp-map hit and a census idea mints a node the predicate APPROVES or mints nothing; a mutant restoring `find_parent` alone as the parent turns it red. (Council `alive` READ `mint_missing` at level3.py:1008-1010 and did not run it; DG1 read the same lines at cd0aa3d261 and did not run it. Only the rows 16-18 rescan revert above was measured in-process.)
6. Negative: after the close commit, `git grep -n 'until goal:g1.43.1' -- .agi/nodes/.geometry/commands.md skills/agi-node-write/SKILL.md CLAUDE.md` shows 0 hits, while `operator-only` stays in the commands.md level3.py reason.
7. A lane that stages a NEW node whose front matter holds a duplicate `id:` (or `type:` / `parents:`) key through `write.py create`, `links.py schema` and the `.8` growth gate gets the same refusal from all three, and the parent index holds no phantom id; a mutant that lets `grow.py` take the first key (or `read_frontmatter` the last) without the refusal turns it red. (Council 00:5xZ 10-11, from the .8 verifier, which reproduced the first/last split and did NOT run `grow.py`. DG1 read `grow.py`'s `setdefault` and `read_frontmatter`'s `yaml.safe_load`, ran neither on a duplicate key; that PyYAML keeps the last duplicate is my reading of the library, not a measurement.)

## Out of scope
- The build is a write-gate round: it is under the g7.16.1.11 HOLD and waits on goal:g7.16.1.11.8 landing; it is laned through the council (sanctuary-master). Nothing here is built by this node.
- goal:g1.43 rows 1-13 · goal:g7.16.1.11.8 (the growth gate itself) · the build_kind default (landed by DG3, 29ba4c1fb3).

## Agent Notes
Assigned to **sanctuary-master**.
In class, for the round to fold in: `write.py create goal` scaffolds without `confidence` / `origin` / `seeds` / `tags` (SCHEMA-WARNING at the mint of this node; DG1 added the four by hand). `goal:g1.43` itself lacks them.
Council call on the umbrella (22:11Z, alive): keep idea:engine-self-decomposition, no per-file idea; mint one only when a file has a why its goal does not hold.
Who runs the level3.py rescan (DG1 read at 107388a1b1): nothing schedules it. commands.md marks it `proposable: false`, `reason: default scan prunes stale level3-scan build nodes; operator-only`; its docstring says it is 'invoked directly' and wiring it into driver.sh must stay plugin-only; `git grep level3` finds no call in driver.sh, hooks, guard, workflows or crons.md; `crons.py show` has 0 hits; no process runs now. stitch.py only imports it to LOAD nodes. Not checked: the crontabs of other uids (no root). So rows 16-18 revert only when someone runs level3.py by hand (default mode; --mint-missing-only not read by me) before the round lands: an operator act, not a cron.
Rows 14-18 of goal:g1.43 repaired by DG1 (parents only, ids and mint_ids untouched): tests-test-nest and -nest-r gain goal:g7.16.1.11.21, tests-test-legacy gains goal:g7.16.1.11.22 (each keeps idea:engine-tests); bin-nest and bin-legacy go from 0 parents to goal:g7.16.1.11.21 / .22 + idea:engine-self-decomposition (no mvp exists for either file, and no per-file idea; the census umbrella is the nearest true idea).
