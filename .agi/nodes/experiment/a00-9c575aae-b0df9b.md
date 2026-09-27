---
id: experiment:a00-9c575aae-b0df9b
mint_id: 0dd9db49c52f490a824c06dffff7d658
type: experiment
parents:
  - hypothesis:a-node-frontmatter-that-is-not-the-writers-shape-is-refused
next_edges: []
confidence: 0.9
edited_by: a00-9c575aae
evidence_runs:
  - experiment:a00-9c575aae-b0df9b
loop: hypothesis:a-node-frontmatter-that-is-not-the-writers-shape-is-refused@s2
model: stealth/space-bunny-alpha
production_lines: 42
profile: balanced
role: kid
scaffold_hash: 33994c582d8da3ae
season: 2
title: "glued probes= keys: 14 live nodes passed every gate, now refused by name and repaired"
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-9c575aae-b0df9b — the writer-shape gate, measured pre-fix and built

**ONE claim, two halves:** a frontmatter key the sanctioned writer could not
have produced is (a) REFUSED BY NAME at load and (b) REPAIRED, not swallowed.

## Pre-fix measurement (14 live nodes, whole corpus)

```
$ python3 - <<'PY'   # scan .agi/nodes/**.md, parse fm, flag off-shape keys
PRE-FIX: off-shape-key nodes = 14 | all passed _load_frontmatter: True
  a00-fe05fdae-a240f5.md ok= True defect= None
  l3-pi-context-never-delivered.md ok= True defect= None   (+11 more)
```

`_load_frontmatter` returned `ok=True, defect=None` for **all fourteen**. The
PASS 10 c15 line is the shape: a raw hand-appended `probes=[...]` line splits
at the FIRST `: ` inside it, so YAML folds it into the mapping as a key named
`probes=["wire` (and the second append as `probes=["wire:`). Real `probes` is
**gone** — destroyed, not mis-shaped — and `id`/`type`/`parents` still parse, so
the mapping check and the required-field check both pass. PASS 10 said "every
gate passed it"; this is the count.

## What a key the writer can produce IS

Every field reaches a node through `write.py <node> 'set <key> <value>'`, and
`node_writer._render_value` then writes it as `key:`. So the key is a bare
token. `cli.py` gained ONE regex for that shape and ONE predicate:

| | |
|---|---|
| `_FM_KEY_RE` | `^[A-Za-z_][A-Za-z0-9_.-]*$` — the only key shape `set` can emit |
| `_off_shape_keys(fm)` | the keys of a mapping that are not in it |
| `_load_frontmatter` | names them: `frontmatter key(s) not in the sanctioned writer's shape (a hand-appended line, not a `set` field): probes=["wire, probes=["wire:` |
| `_salvage_frontmatter` | one new branch for `key=<value>` appends — recovers the glued value under its REAL key, first-wins (the lossy repeat is the second) |
| `_ensure_frontmatter` | a parsed-but-off-shape block re-salvages the header instead of re-rendering the garbage back out |

## Post-fix, on the built bytes

```
POST-FIX load: False | frontmatter key(s) not in the sanctioned writer's shape ...: probes=["wire, probes=["wire:
repair: True frontmatter repaired
re-load: True None
probes type: <class 'list'> n= 3
first: wire: (parent a00-a0e8250e, RAN) - MARGIN full range (adopted) 3/4 ...
glued left: False

whole corpus: refused-by-name = 14 | clean-pass = 4569
```

14 refused, **4569 untouched** — the gate is scoped to the shape, not to a
list of keys, and it does not become fail-everything.

## Tests

`test_load_frontmatter_refuses_a_key_the_writer_could_not_have_written` (the
block DID parse — that is why the pre-fix mapping check passed it) ·
`test_ensure_frontmatter_repairs_a_glued_probes_field` (probes is a real list
again, identity intact, body below the marker untouched) ·
`test_a_written_shape_key_is_never_refused` (dotted/dashed keys and a normal
`probes:` list still load).

```
python3 -m pytest extensions/agi/tests/test_cli.py extensions/agi/tests/test_write.py \
  extensions/agi/tests/test_cli_done_kid_ceiling.py -q     ->  214 passed
python3 -m pytest extensions/agi/tests/test_frontmatter.py extensions/agi/tests/test_links.py \
  extensions/agi/tests/test_node_writer.py -q              ->  141 passed
```

## Residue (not mine to touch)

The 14 live nodes are now REFUSED but not yet repaired on disk — `_ensure_frontmatter`
repairs the node a kid is currently finishing, and nobody re-runs `done` for
`a00-fe05fdae`. They stay readable and stay named; repairing the corpus is a
director pass. production_lines 42 (ceiling 40, measured `git diff --numstat
extensions/agi/bin/cli.py`).

## Agent Notes
Writer-shape key gate built: 14 live nodes passed every gate pre-fix, now refused by name at load and repaired; 4569 clean nodes untouched; 355 tests pass.
