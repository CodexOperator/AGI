---
id: experiment:a00-2c00af23-3ea2ff
mint_id: e890b2c1eccd43cbbdbd0a0dbdd9fff0
type: experiment
parents:
  - hypothesis:l4-write-api-root-resolution
next_edges: []
confidence: 0.9
edited_by: a00-45bdb3cb
evidence_runs:
  - experiment:a00-2c00af23-3ea2ff
loop: hypothesis:l4-write-api-root-resolution@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 33955cff41c53dde
season: 2
title: A00 2c00af23 3ea2ff
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-2c00af23-3ea2ff

## Experiment

FIX-ONLY round (L4.95) against the proved hypothesis
(l4-write-api-root-resolution): write.py's Python API took `root` raw while
main()'s CLI resolved it, so `write.create(".")` from the repo root minted a
real node into `<root>/nodes/...` instead of `<root>/.agi/nodes/...` and
degraded the written_by spawn gate to unverified while returning success.

**Direction taken: (1) resolve root descend-only inside the API — BOTH
`create` and `submit`.** I deliberately did NOT take direction (2)
(refuse-on-missing-schemas-dir), because I found the permissive fallback IS
load-bearing: `_enforce_written_by`'s `if not schemas_dir.is_dir(): return`
is the exact branch the minimal-project/test-fixture pattern relies on — the
`project` fixture in test_write.py creates `.agi/config.json` + a nodes dir
but NO `context/schemas/`, and dozens of tests write through it. Making the
gate refuse on a missing schemas dir would force every minimal project to
ship a schemas dir and cascade fixture changes across test_node_writer.py /
test_spawn_gate.py (out of this round's scope). Direction (1) alone closes
the falsifier: a wrong root refuses before any write. The two directions
were not in tension, but (1) is the right round-scoped fix.

**Change** (`extensions/agi/bin/write.py`): added `_resolve_api_root(root)` —
a DESCEND-ONLY resolver. It looks at ONLY the given root
(`locations.config_path(d)` — the root already being a graph root, incl.
legacy config dirs) and the `.agi/` directly beneath it
(`locations.config_path(d / GRAPH_DIR_NAME)`); anything else raises
`EditError` naming the root. It never calls `find_project_root`, so it can
never walk UP into a real ancestor graph (the never-ascend hazard for a test
passing a bare tmp dir). Wired the call at the top of both `submit` and
`create`, BEFORE `_enforce_written_by` / any write. CLI paths unchanged:
main() still pre-resolves root with find_project_root and passes a valid
graph root, which the resolver accepts as identity.

**Tests** (`extensions/agi/tests/test_write.py`, +5):
- `test_create_resolves_root_descend_only_to_dot_agi` — repo root descends to
  `.agi/nodes/...`, no stray `<root>/nodes/`.
- `test_create_wrong_root_refuses_and_writes_nothing` — THE FALSIFIER: a
  bare root raises EditError and writes nothing (old behaviour wrote the
  node + returned success).
- `test_api_root_never_ascends_into_an_ancestor_graph` — a dir whose ANCESTOR
  is a real graph refuses rather than walking up into it.
- `test_submit_wrong_root_refuses_and_writes_nothing` — same falsifier for
  submit; file stays byte-identical.
- `test_submit_resolves_repo_root_descend_only` — submit descends `parent`
  the way the CLI does.

## Evidence

```
$ python3 -m pytest extensions/agi/tests/test_write.py -q
85 passed in 0.49s

$ python3 -m pytest extensions/agi/tests/test_write.py \
    extensions/agi/tests/test_node_writer.py extensions/agi/tests/test_spawn_gate.py -q
220 passed in 2.84s
```

Targeted suite grew from the 215-passed baseline to 220; the three targeted
files (the round's scope) all green. No full-suite run performed, per the
brief's standing constraint. No assertion was weakened; the written_by
fall-through for a genuinely schema-less project is unchanged.

**THOUGHT — why this version:** Fix-on-define sonnet-vetted: resolved root
inside the API (direction 1) not the gate (direction 2), because the gate's
permissive fallback is load-bearing for the minimal-project/test-fixture
pattern — the positive finding to report is that (2) is NOT free, not that
it was skipped. `_resolve_api_root` is a fresh public helper, never
`find_project_root`, so the never-ascend property is structural and asserted
directly by its own test.

## Agent Notes
FIX-ONLY: added descend-only _resolve_api_root to write.create/submit; wrong root now raises EditError and writes nothing; +5 targeted tests (incl. falsifier + never-ascend + submit), 220 passed across the three targeted files, up from 215; direction (1) chosen over (2) because the gate's permissive fallback is load-bearing for the minimal-project/test-fixture pattern.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (a00-45bdb3cb), L4.95: accepted as-is. Verified mechanism, not wording — (1) read _resolve_api_root end to end: it checks locations.config_path(d) then config_path(d/.agi) and raises EditError otherwise, never find_project_root, so never-ascend is structural; wired at the top of BOTH submit (write.py:738) and create (write.py:1175) before _enforce_written_by or any write. (2) ran the targeted three-file suite myself: 220 passed, up from the 215 baseline, no assertion touched. (3) ran the falsifier LIVE against the real code from /tmp, not from the kid's own fixture: write.create(<bare dir>) raised EditError and left zero files; write.create(<repo root>) minted into .agi/nodes/, no stray nodes/ root. Direction (2) refusal is correctly rejected with a named legitimate dependant (the minimal-project fixture pattern). BONUS: the live falsifier run incidentally pinned the message source the original brief could not grep — "SPAWN-GATE SCHEMA ERROR"/"SPAWN-GATE UNVERIFIED" print at runtime from write.py's own gate path, not node_writer.py; wording confirmed verbatim. Node stays proved.
<!-- THOUGHT:END -->

Review (parent a00-45bdb3cb): mechanism verified live — wrong root refuses with EditError and writes nothing, repo root descends to .agi; 220 targeted tests re-run by reviewer; direction (2) correctly declined with the load-bearing finding named. Bonus: pinned the SPAWN-GATE UNVERIFIED wording source to write.py runtime, resolving the brief's open question. ACCEPTED, verdict proved stands.
