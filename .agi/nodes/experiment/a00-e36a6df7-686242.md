---
id: experiment:a00-e36a6df7-686242
mint_id: b774c70d07a44d35b8d770337f298f6d
type: experiment
parents:
  - hypothesis:a-rounds-named-node-set-is-its-dispatch-time-ids-never-a-kid-supplied-parent
next_edges: []
confidence: 0.8
edited_by: a00-564f21f5
evidence_runs:
  - experiment:a00-e36a6df7-686242
loop: hypothesis:a-rounds-named-node-set-is-its-dispatch-time-ids-never-a-kid-supplied-parent@s2
model: stealth/space-bunny-alpha
profile: balanced
role: kid
scaffold_hash: b2f3c8f062c3fa24
season: 2
title: "The round-commit policy must live in committed bytes: a per-type round_commit cell in .agi/context/schemas"
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-e36a6df7-686242

## Experiment
# experiment:a00-e36a6df7-686242 — the round-commit policy must live in COMMITTED bytes

## What I picked, and why: (a) a per-type `round_commit` cell in `.agi/context/schemas/[<type>].md`

The residual the last kid measured is a *reachability* defect, not a policy defect. The allowlist
(`grid.round_commit`) says the right thing, but it lives in `.agi/config.json`, and
`_round_scope_ok` (cli.py:2096) refuses that path for every round by design — so the cell is only
ever an uncommitted worktree modification, and in main and in every other checkout the gate is
fail-open for exactly `goal:*` and `doc:unified-*`. A gate that reads a file its own actor class may
never commit cannot be the gate.

| option | who can land the change | cost | why not |
|---|---|---|---|
| (a) schema cell | the round itself — `_round_scope_ok` only refuses config.json, quorum, foreign node files | one frontmatter key per type | **chosen** |
| (b) fail-closed in code | nobody (engine commit by a director) | every type must opt in; a missing cell blocks rounds | no code list of types (config-max), and the block lands on a round's own foreign-parent commit |
| (c) better | — | — | the cell IS (c): the per-type policy at the place the type is already defined, read by the same `schema_registry` reader `write.py` enforces `written_by` with |

The honest caveat, stated rather than papered over: an *undeclared* type is still fail-open
(config fallback retained, so a fixture tree behaves as it did). What changed is that closing a
family is now a one-line change a round can commit, and the two families the claim names are closed
today.

## The gate (cli.py `_round_committable`, third conjunct, 16 lines)

```
cell = sch.frontmatter.get("round_commit")
  False            -> refuse the type
  True             -> allow, skipping the config allowlist
  {allow: false}   -> refuse the type
  {never_node_ids: [...]} -> refuse those id prefixes inside the type
```
Precedence: schema `written_by` > schema `round_commit` cell > `grid.round_commit` in config.
An explicit cell wins either way, because it is the half that reaches main.

## The cells (committed)

- `.agi/context/schemas/[goal].md`: `round_commit: false`
- `.agi/context/schemas/[doc].md`: `round_commit: {never_node_ids: [doc:unified-]}` (doc of another
  family still committable — the id prefix, not the type, is what the claim names)

## Evidence — a test that reads only COMMITTED bytes

`test_round_commit_policy_lives_in_the_committed_schemas_not_in_config` copies the REAL
`.agi/context/schemas/` into a tmp root and writes `config.json = {}`:

```
root = tmp_path/".agi"  ; copytree(<repo>/.agi/context/schemas, root/"context"/"schemas")
(root/"config.json").write_text(json.dumps({}))
assert not _round_committable(root, "goal:g5")            # the pre-fix result was True
assert not _round_committable(root, "doc:unified-head")   # the pre-fix result was True
assert     _round_committable(root, "doc:goals-preamble")
assert     _round_committable(root, "hypothesis:tgt")
assert not _round_committable(root, "town:local-maxxing")  # written_by still refuses it
```
Run: `python3 -m pytest extensions/agi/tests/test_cli.py -q` -> **62 passed** (61 before, +1).
Schema readers unaffected by the new key: `test_spawn_gate.py test_hierarchy.py
test_node_writer.py test_frontier.py` -> **220 passed**.

Production lines (the only `git diff --numstat` I ran): cli.py 16 + `[doc].md` 5 + `[goal].md` 7 =
**28 / 40**. The 24-line `.agi/config.json` and 9-line
`nodes/experiment/a00-956f208a-1a6498.md` in that diff are the previous kid's uncommitted work; I
touched neither.

## Agent Notes
Chose (a): per-type round_commit cell in .agi/context/schemas/[<type>].md -- a file a round MAY commit, unlike .agi/config.json (_round_scope_ok:2096). goal:false, doc:{never_node_ids:[doc:unified-]}; new test copies the real schemas with config.json={} and proves both families refused; 62 test_cli + 220 schema-reader tests pass; 28/40 production lines.

parent review DH.390 (a00-564f21f5), on the DIFF 232b704e1. ACCEPTED at proved; the two families are closed in bytes a round can actually land. My probes, built by me, not read off the node: (GATE) a tmp root holding a copy of the REAL .agi/context/schemas with config.json={} -> goal:g5 False, doc:unified-head False, doc:unified-primer False, config:posts False, config:geometry-seats False, town:local-maxxing False, while doc:goals-preamble / hypothesis / experiment stay True; the pre-fix result on the same root was True for the first two, so the fix is measured, not asserted. (WIRE) the real call chain on the real worktree, done --parent goal:g5 threaded through cli.py:1739 -> _round_named_node_ids -> _round_own_node_paths: the set is the experiment node plus the dispatch target, the goal absent. (AUTH) --owns goal:g5 config:posts town:local-maxxing: none of the three reaches the commit set. NOT a demotion, but the claim's last clause is still open: a refused id is dropped by a bare `continue` in _round_own_node_paths (cli.py ~2205) with NOTHING on stderr, and the claim says "every refused path is named on stderr as before" — handed to kid 3. Residual, stated and not fatal: a root with no .agi/context/schemas (or an unreadable one) is fail-open for every type, since the cell lives in the schema. That is a fixture tree, not a town, but it is the one shape where the gate is off.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review DH.390, on the DIFF 232b704e1. Accepted, and the near miss it avoids is the whole round: (1) the brief said, quoted, "config-max: the round-editable node types as a declared cell or schema field, read .agi/context/schemas/ written_by first -- a type written_by owner/prime_director is never round-editable". Both available cells were legal by those words, and the first kid took the config one. (2) What the machine actually does: a gate reading .agi/config.json is unreachable for this actor class -- _round_scope_ok (cli.py:2096) refuses that path by design -- so the allowlist is an uncommitted worktree modification and in main goal:g5 and doc:unified-head are committable. I measured it: same root, cell present False/False, cell removed True/True. (3) The near miss: "the policy is DATA, not a literal, read at runtime" satisfies config-max word for word and loses the mechanism, because config-max assumes the data can be landed, and this data cannot. The second kid moved the same data one path over -- .agi/context/schemas/[<type>].md, which a round MAY commit -- and the fix is measurable on committed bytes alone: with config.json={} and the real schemas, both families are refused. (4) Deviation from a standing rule: none; I did not touch the schemas or the code, I read them.
<!-- THOUGHT:END -->
