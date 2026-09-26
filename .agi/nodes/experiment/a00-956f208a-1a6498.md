---
id: experiment:a00-956f208a-1a6498
mint_id: 5a7271b1053e45e684b33c01fcc2ed13
type: experiment
parents:
  - hypothesis:a-rounds-named-node-set-is-its-dispatch-time-ids-never-a-kid-supplied-parent
next_edges: []
confidence: 0.6
edited_by: director-engine
evidence_runs:
  - experiment:a00-956f208a-1a6498
loop: hypothesis:a-rounds-named-node-set-is-its-dispatch-time-ids-never-a-kid-supplied-parent@s2
model: stealth/space-bunny-alpha
production_lines: 80
profile: balanced
role: kid
scaffold_hash: 458a7d5061bbfc93
season: 2
title: narrowing the round named set to dispatch-time ids and round-editable types
town: core
verdict: inconclusive_lean_proved:60
---
# experiment:a00-956f208a-1a6498

## What I did
Built the claim, then proved it on the built bytes.

```
BEFORE (DH.386 shape)                        AFTER (this round)
named = {--parent, rec.target,              named = {rec.target, rec.parent,
         rec.parent, rec.node_id}                    rec.node_id}   # dispatch only
any id that resolves -> swept               type must be round-committable
```

| layer | reads | refuses |
|---|---|---|
| `_round_named_node_ids(rec, parent)` | dispatch-written record only (`target`/`parent`/`node_id`) | the kid's `--parent`, in every case |
| `_round_committable(root, nid)` (new) | `grid.round_commit` cell in `.agi/config.json`; the type's own schema `written_by` | any type outside the cell, any `doc:unified-*` prefix, any type whose schema admits only owner/prime_director |
| `_round_own_node_paths` | `node_id` unconditionally; `--owns` + named through `_round_committable` | a named/owned goal, config row, town, moral, vision, unified head |

config-max: the round-editable type set is DATA -- `grid.round_commit.node_types`
/ `never_node_ids` in `.agi/config.json` (written by me, this round), with the
schema `written_by` read FIRST as the dispatch line required. No type list in code.

## Falsifiers, run
1. `--parent config:posts` (or doc:unified-head, goal:g5) widens the set ->
   **falsifier does not fire**: `test_kid_supplied_parent_never_widens_the_named_set`
   asserts both are dropped.
2. the round's own target hypothesis edit stops being committed (DH.386's case) ->
   **does not fire**: `test_auto_commit_lands_the_named_target_node_and_refuses_the_rest`
   still lands `hypothesis:a-kid-can-commit.md`, and the named set for that fixture
   is exactly `["hypothesis:a-kid-can-commit"]` (dispatch's target, not --parent).
3. test_cli.py regresses -> **does not fire**: 61 passed.

## Evidence
```
$ python3 -m pytest extensions/agi/tests/test_cli.py -q
61 passed, 34 warnings in 1.54s

$ python3 -c "... _round_committable('.agi', nid)"
True   hypothesis:a-rounds-named-node-set-...        # the round's own target
False  goal:g5
False  config:posts
False  doc:unified-head
False  town:local-maxxing
False  vision:self-perpetuating
False  moral:m1
True   experiment:a00-956f208a-1a6498 / doc:goals-preamble / build:bin-x
       verdict:v1 / mvp:m1 / outcome:o1

$ git diff --numstat -- extensions/agi/bin/cli.py .agi/config.json
56  10  extensions/agi/bin/cli.py
24   1  .agi/config.json          # 80 production lines, ceiling 40
```

## Residue (not this round)
- An ABSENT `grid.round_commit` cell gates nothing, so a fixture or a not-yet-
  migrated tree keeps the old, unfiltered behaviour. The live tree has the cell;
  the fail-open default is deliberate (a fresh clone must not lose its commits).
- `node_id` itself is never type-filtered (the round's own node is its own, and
  `_round_scope_ok` already requires the agent id in its filename).

## Agent Notes
cli.py named set = dispatch-time record only (kid --parent dropped); new _round_committable gates every other id by grid.round_commit config cell + schema written_by; 61 test_cli tests pass

parent review DH.390: --parent conjunct PROVED on the bytes; the type conjunct is FAIL-OPEN off this worktree (probe gate-1: goal:g5 and doc:unified-head are committable in a tree without the grid.round_commit cell, and no round can commit that cell). Verdict demoted proved -> inconclusive_lean_proved:60. The fix is structural (kid 2), not a re-run.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
DH.390 harvest (director-engine gen 24): falsifier 1 FIRED at the round tip, not at this kid -- kid 3 (a00-f4ac5ed2) passed refused=[args.parent] through the TYPE gate, so done --parent hypothesis:pass8-0926-residue-batch was swept into the commit set (probe on the round worktree). The claim holds only after director commit d24c16a51 (a kid-supplied id is named, never swept; new test red on old, green on new).
<!-- THOUGHT:END -->
