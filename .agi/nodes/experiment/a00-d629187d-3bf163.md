---
id: experiment:a00-d629187d-3bf163
mint_id: 0c1a144a1a504228a3361f555f94eb03
type: experiment
parents:
  - hypothesis:l4-create-refuses-a-genuinely-unknown-type-before-any-file-is-written
next_edges: []
confidence: 0.85
edited_by: a00-25d39101
evidence_runs:
  - experiment:a00-d629187d-3bf163
line_ceiling: 40
loop: hypothesis:l4-create-refuses-a-genuinely-unknown-type-before-any-file-is-written@s2
model: ~deepseek/deepseek-v4-flash-latest
probes:
  - {"conjunct": 1, "class": "gate", "cmd": "parent probe_a.py P4: pre-seed nodes/notown/existing.md then write_node(fixture,notown,existing,[idea:i1])", "expected": "SKIPPED, not the new REJECTED: an existing file must still take the old path", "observed": "status=skipped reason=<path> already exists; no rejection", "result": "held"}
  - {"conjunct": 2, "class": "gate", "cmd": "parent probe_a.py P1: fixture with [shape].md and [idea].md loaded, write_node(root,notown,missing-thing,[idea:i1])", "expected": "REJECTED by name, no nodes/notown dir created", "observed": "status=rejected; reason names notown and context/schemas/[notown].md; nodes dir set before==after==[idea]", "result": "held"}
  - {"conjunct": 3, "class": "gate", "cmd": "parent probe_a.py P3: [floating].md present but declares no spawn: block; write_node(root,floating,fl1,[idea:i1])", "expected": "WRITTEN, the other UNVERIFIED branch untouched", "observed": "status=written, gate=unverified, nodes/floating/fl1.md exists", "result": "held"}
  - {"conjunct": 4, "class": "gate", "cmd": "parent probe_a.py P11: write.create(fixture_graph,not-own,hyphen,[goal:g1])", "expected": "REJECTED naming the canonical type and the missing schema path", "observed": "status=rejected reason=no active schema for type not_own: a new not_own node cannot be created because context/schemas/[not_own].md does not exist", "result": "held"}
production_lines: 32
profile: balanced
role: kid
scaffold_hash: 1f6857181c811edd
season: 2
title: write_node refuses a brand-new node of a type with no active schema before the first mkdir
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-d629187d-3bf163

## Experiment

Kid A of the pair for `hypothesis:l4-create-refuses-a-genuinely-unknown-type-before-any-file-is-written`. Scope: clauses 1-4 (the `node_writer.write_node()` new-vs-existing distinction and the REJECTED-on-unknown-type refusal). Kid B owns clause 5 (the `write.py create` end-to-end proof) plus its own stray-directory sweep test.

### What the bytes did before the fix

Probe of the pre-fix tree (test-first, run before any edit):

```
$ python3 -m pytest extensions/agi/tests/test_node_writer.py -q \
    -k "unknown_type or without_a_spawn_block or existing_undeclared"
FAILED test_create_of_an_unknown_type_refuses_before_writing
       AssertionError: expected REJECTED, got written
FAILED test_unknown_type_refusal_leaves_no_stray_directory
       AssertionError: 'notown' != 'outcome'   (nodes/notown/ was created)
260 passed, 63 warnings
```

stderr from the pre-fix run: `SPAWN-GATE UNVERIFIED notown:another-missing ... The node is written.` — `spawn_gate.check_spawn` returns UNVERIFIED for a missing schema, `SpawnResult.ok` is `status != REJECTED`, and `write_node` sailed past the `not gate.ok` branch straight to `mkdir` + `write_text`. That is the L4.338 defect: `nodes/notown/missing-thing.md` in the live tree.

### The fix (clauses 1-4)

In `extensions/agi/bin/node_writer.py`, `write_node()` only:

1. `node_file = node_dir(root, ntype) / f"{slug}.md"` is computed **before** the gate is judged (moved up beside `gate = spawn_gate.check_spawn(...)`); the later duplicate line is removed. `node_dir()` is pure — a path, no side effect.
2. A second refusal, immediately after the existing `if not gate.ok:` branch, fires only when ALL of: the gate is `spawn_gate.UNVERIFIED`, its reason is exactly `f"no active schema for type '{ntype}'"`, at least one active schema was loaded (`rules.schemas` non-empty), and `not node_file.exists()`.
3. The refusal sets `res.status = REJECTED` with a named reason that names the type and says plainly `context/schemas/[<type>].md` does not exist, then returns — the same shape as the `not gate.ok` branch (no file, no directory). `res.gate` stays set.
4. Nothing else changed: `check_spawn()` and `SpawnResult.ok` are untouched, `bypass=True` still writes, the `rule_for()`-found-no-variant UNVERIFIED branch still writes, and a pre-existing file still takes the old path (`SKIPPED` under `on_exists=SKIP`).

### Judgement call (deviation, recorded per the delegated-authority rule)

The condition adds `rules.schemas` non-empty, which the brief did not spell out. Without it, `test_write.py::test_create_resolves_root_descend_only_to_dot_agi` — a fixture with a `.agi/` graph but NO `context/schemas/` directory at all — flipped from written to rejected. A project with no active schema loaded at all cannot tell an unknown type from an unconfigured one, and `check_spawn`'s own docstring says failing closed there means declining to approve, not rejecting. The genuinely-unknown case the round exists for is the OTHER one: schema set loaded, this type absent from it. Pinned explicitly by `test_a_project_with_no_schemas_loaded_still_writes`.

### Tests added (`extensions/agi/tests/test_node_writer.py`, fixture-rooted only)

- `test_create_of_an_unknown_type_refuses_before_writing` — clauses 1-4: REJECTED, gate UNVERIFIED, reason names `notown` and `context/schemas/[notown].md`, `nodes/notown` absent.
- `test_unknown_type_refusal_leaves_no_stray_directory` — the L4.338 regression: `nodes/` maxdepth-1 dirs are unchanged after the refused create.
- `test_schema_without_a_spawn_block_still_writes` — regression pin: the OTHER UNVERIFIED branch (`[floating].md` exists, no `spawn:` block) is still WRITTEN.
- `test_existing_undeclared_type_file_is_still_skipped` — regression pin: an existing file of an undeclared type is SKIPPED, not REJECTED (`update_node` never calls `check_spawn`).
- `test_a_project_with_no_schemas_loaded_still_writes` — the carve-out above.

## Evidence

Test-first pre-fix run (2 failed, 2 passed) and post-fix run of the named suites:

```
$ python3 -m pytest extensions/agi/tests/test_node_writer.py \
      extensions/agi/tests/test_spawn_gate.py extensions/agi/tests/test_write.py \
      extensions/agi/tests/test_cli.py -q
332 passed, 164 warnings in 15.50s

$ python3 -m pytest extensions/agi/tests/test_post_wire.py \
      extensions/agi/tests/test_dispatch.py \
      extensions/agi/tests/test_dispatch_scaffold_unregistered.py -q
136 passed, 13 warnings in 49.96s
```

`test_spawn_gate.py` did not change colour — the gate's UNVERIFIED semantics are untouched.

End-to-end probe on a `tmp_path`-shaped fixture root (session scratch, NOT the live tree): schemas dir seeded with `[idea].md` + `[shape].md`, one `idea:i1` node, one ladder node.

```
$ python3 extensions/agi/bin/write.py create notown missing-thing \
      --parent idea:i1 --root <scratch>/probe-proj
exit=2
ERR: spawn rejected for notown:missing-thing: no active schema for type
'notown': a new notown node cannot be created because
context/schemas/[notown].md does not exist. ...

$ find <scratch>/probe-proj/.agi/nodes -maxdepth 1 -type d | sort
<root>/.agi/nodes
<root>/.agi/nodes/.geometry
<root>/.agi/nodes/idea
```

`nodes/notown` did not survive. Live invariant honoured: `ls /home/ubuntu/work/agi/.agi/nodes | grep -i notown` → no match, before and after; every probe ran under `.agi/sessions/iter-SD.10/a00-d629187d/` or pytest's `tmp_path`.

Production-line measurement (`git diff --numstat`, read-only): `extensions/agi/bin/node_writer.py` 33 added / 1 removed = net 32 lines, inside the 40-line ceiling. Tests: +85 lines, excluded from the measurement.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review version (a00-25d39101, SD.10). Kid A landed clauses 1-4 of hypothesis:l4-create-refuses-a-genuinely-unknown-type-before-any-file-is-written as a narrow edit inside node_writer.write_node: node_file is computed before the gate so the writer can tell a brand-new create from a pre-existing file, and a gate that is UNVERIFIED for exactly the no-active-schema reason plus a missing node file is turned into REJECTED with a reason naming the type and the missing context/schemas/[type].md. I read the bytes at 63f6bc83c rather than the result file, ran my own probes (probes field) and ran the touched suites (290 passed). What changed in this version is only the review: the kid account in the body stands, and I added the parent probes and this thought. THE PART WORTH KNOWING: the kid added a rules.schemas non-empty condition the brief did not ask for, which narrows clause 2 to the schema-set-loaded case. I treated that as a caveat rather than a disproval because it is forced by an existing pinned test (test_write.py:1542 creates a node into a .agi graph with no context/schemas) and because the real root loads 21 schemas, so the refusal still fires live; the degenerate unconfigured project keeps its previous fail-open behaviour.
<!-- THOUGHT:END -->

## Agent Notes
write_node() now refuses a brand-new node of a type with no active schema before any mkdir: node_file computed pre-gate, second REJECTED branch beside not-gate.ok (UNVERIFIED + exact no-active-schema reason + rules.schemas non-empty + file absent), reason names the type and context/schemas/[<type>].md. Regression pins green: rule_for-no-variant branch still writes, existing undeclared file still SKIPPED, bypass unchanged, no-schemas-loaded project unchanged (deviation recorded). 332 passed across test_node_writer/test_spawn_gate/test_write/test_cli; 136 passed across post_wire/dispatch suites; end-to-end write.py create on a scratch fixture root exits 2 and leaves no nodes/notown. Net 32 production lines vs 40 ceiling. Clause 5's formal test is kid B's.

parent review (a00-25d39101): ACCEPTED, verdict proved for clauses 1-4, confidence 0.85 kept. Read the diff at 63f6bc83c, not the result file: the new refusal sits at node_writer.py:687-717 and computes node_file before the gate so it can tell a new create from a pre-existing file. Parent probes held: schemas loaded + type absent -> REJECTED by name with no stray dir; no-spawn-block schema -> still WRITTEN; pre-existing undeclared file -> still SKIPPED; bypass -> still writes; hyphenated input names the canonical type. Touched suites green (290 passed across test_write.py + test_node_writer.py + test_spawn_gate.py). One caveat, recorded: the condition adds rules.schemas non-empty, which narrows clause 2 AND ONLY WHEN to the schema-set-loaded case. I verified the forcing test myself (test_write.py:1542 builds a .agi graph with no context/schemas and asserts res.written) and confirmed the real root loads 21 schemas, so the refusal fires live. Clause 5 is proven by experiment:a00-200ebad9-7333f7.
