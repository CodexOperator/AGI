---
id: experiment:a00-200ebad9-7333f7
mint_id: 00dea4f716ae4264a8b87f6bb3d0c9cf
type: experiment
parents:
  - hypothesis:l4-create-refuses-a-genuinely-unknown-type-before-any-file-is-written
next_edges: []
confidence: 0.9
edited_by: a00-25d39101
evidence_runs:
  - experiment:a00-200ebad9-7333f7
line_ceiling: 40
loop: hypothesis:l4-create-refuses-a-genuinely-unknown-type-before-any-file-is-written@s2
model: ~deepseek/deepseek-v4-flash-latest
probes:
  - {"conjunct": 5, "class": "wire", "cmd": "parent probe_b.py P8: subprocess write.py create notown cli-sub --parent goal:g1 --root <fixture .agi graph>", "expected": "non-zero exit, refusal on stderr naming the type and the missing schema path, nodes dir set unchanged", "observed": "rc=2; stderr ERR: spawn rejected for notown:cli-sub: no active schema for type notown: a new notown node cannot be created because context/schemas/[notown].md does not exist; dirs before==after==[goal]", "result": "held"}
  - {"conjunct": 5, "class": "gate", "cmd": "parent probe_b.py P7: write.create(graph,notown,cli-payload,[goal:g1],payload=src/notown_payload.py)", "expected": "REJECTED, the payload file ensure_payload created before the gate must be cleaned up, no nodes/notown", "observed": "status=rejected, made=None, payload file absent, nodes dirs before==after==[goal]; CAVEAT the empty payload-location dir src/ remains, which I verified is pre-existing cleanup behaviour (identical on the rule-rejection path) and out of this round file scope", "result": "held"}
production_lines: 0
profile: balanced
role: kid
scaffold_hash: d394ef2aabb03f14
season: 2
title: "Clause 5: write.py create refuses an unknown type at the front end, pinned by four fixture-rooted tests"
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-200ebad9-7333f7

## Experiment

Clause 5 of `hypothesis:l4-create-refuses-a-genuinely-unknown-type-before-any-
file-is-written` plus the stray-directory sweep, landed as four committed tests
in `extensions/agi/tests/test_write.py` (test file only — no production line
changed; `git diff --numstat` over `node_writer.py`/`write.py`/`spawn_gate.py`
returns empty). Kid A's `write_node()` fix was already in the tree and is used
unmodified.

Reused the existing `project(tmp_path)` fixture (test_write.py:34) and the
existing `_schemas(graph)` helper (test_write.py:411) — no second fixture.
Added one tiny reader, `_seeded_node_dirs(graph)`, which returns the EXACT
set of directories under `nodes/` so the sweep asserts a set and not a diff.

Added tests:

1. `test_create_refuses_a_type_with_no_active_schema_by_name` — Python front
   end. `_schemas(project)` loads `[hypothesis].md`/`[experiment].md` and seeds
   `nodes/goal/g1.md` (so `rules.schemas` is non-empty and `notown` is
   genuinely unknown). `write.create(project, "notown", "cli-missing",
   ["goal:g1"])` → `res.rejected`, `made is None`, reason contains both
   `notown` and `context/schemas/[notown].md`; `nodes/notown` absent; the dir
   set equals `{"goal", "hypothesis"}` exactly, before and after.
2. `test_create_of_an_unknown_type_leaves_no_payload_file` — the sharpest
   clause-5 probe. With `payload="src/notown_payload.py"` the source file is
   created by `ensure_payload` before the gate runs; after the refusal it is
   gone and `nodes/notown` never appears. (write.py:~2240 cleanup verified,
   not assumed.)
3. `test_create_cli_refuses_an_unknown_type_and_stays_off_disk` — the real
   front end, `subprocess.run([sys.executable, BIN/"write.py", "create",
   "notown", "cli-sub", "--parent", "goal:g1", "--root", str(project)])`.
   Non-zero exit, refusal text naming `notown` and
   `context/schemas/[notown].md` on stderr, and the same exact unchanged
   `nodes/` dir set. This test did NOT need to be skipped: the fixture graph
   is sufficient, the CLI resolves the tmp root through
   `locations.find_project_root` and needs no seat/ring config.
4. `test_create_still_mints_a_declared_type_at_the_front_end` — regression
   pin: `write.create(project, "hypothesis", "still-fine", ["goal:g1"])` →
   `res.written`, file exists. The new refusal did not over-reach.

Pre-test probe (fixture root `/tmp/probe_root/.agi`, outside the repo; scratch
only) reproduced the CLI refusal by hand before writing the test: `rc=2`,
stderr `ERR: spawn rejected for notown:cli-missing: no active schema for type
'notown': ...`, and `find /tmp/probe_root/.agi/nodes -maxdepth 1 -type d`
showed only `nodes/`, `nodes/goal`, `nodes/hypothesis` both after the plain
create and after the payload create.

## Evidence

```
$ python3 -m pytest extensions/agi/tests/test_write.py \
    extensions/agi/tests/test_node_writer.py -q
209 passed, 137 warnings in 11.75s

$ python3 -m pytest extensions/agi/tests/test_write.py -q \
    -k "unknown or still_mints or stray or payload"
19 passed, 84 deselected, 21 warnings in 0.48s

$ git diff --numstat -- extensions/agi/bin/node_writer.py \
      extensions/agi/bin/write.py extensions/agi/bin/spawn_gate.py
(empty)

$ ls -d /home/ubuntu/work/agi/.agi/nodes/notown
ls: cannot access '/home/ubuntu/work/agi/.agi/nodes/notown': No such file or directory
```

LIVE INVARIANT held: every probe ran on `tmp_path` (the `project` fixture) or
`/tmp/probe_root`; no node under the real `/home/ubuntu/work/agi/.agi/nodes`
was created, touched or probed.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review version (a00-25d39101, SD.10). Kid B landed clause 5 plus the stray-directory sweep as four committed tests in test_write.py, with zero production lines changed. I read the diff at a23b7667d: 84 added lines, no deletions, so no existing test was weakened, and the tests reuse the project fixture and _schemas helper instead of minting a second fixture root. I ran my own probes (probes field): the CLI refusal end to end on a fixture, the payload cleanup on a refused create, bypass, and a declared-type mint. This version differs from the kid version only by that review. Two things I found and recorded instead of letting ride: an empty payload-location dir survives a refused create with --payload, which I confirmed is pre-existing cleanup behaviour on the rule-rejection path and out of scope here; and the whole refusal is narrowed by the parent-side rules.schemas carve-out, so a graph with no schema set at all still writes. Neither falsifies clause 5 as written, and both are named on the node so a later reader is not surprised.
<!-- THOUGHT:END -->

## Agent Notes
Clause 5 + stray-directory sweep landed as four tests in test_write.py; write.py create refuses an unknown type by name (rc=2, names context/schemas/[notown].md), leaves no node dir and no payload file, exact dir set {goal,hypothesis} unchanged; declared type still mints. 209 passed in test_write.py+test_node_writer.py. Zero production lines changed.

parent review (a00-25d39101): ACCEPTED, verdict proved for clause 5, confidence 0.9 kept. Read the diff at a23b7667d: test_write.py only, 84 added lines, zero deletions, so no existing test was weakened. Parent probes held on fixtures: the CLI exits 2 with the refusal naming context/schemas/[notown].md and leaves the nodes dir set unchanged; a refused create with a payload removes the source file ensure_payload made before the gate; bypass still writes; a declared type still mints. Touched suites green: 290 passed across test_write.py + test_node_writer.py + test_spawn_gate.py. Two caveats recorded: (a) an empty payload-location dir (src/) survives a refused create with payload, which I verified is pre-existing write.py cleanup behaviour on the rule-rejection path too, not introduced here; (b) the new refusal is narrowed by the rules.schemas non-empty carve-out, so a fixture whose graph has no schema set at all still writes an unknown type. No probe in this round ran against a real project root; the real tree has no nodes/notown.
