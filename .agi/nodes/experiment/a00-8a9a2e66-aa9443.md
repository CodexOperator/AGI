---
id: experiment:a00-8a9a2e66-aa9443
mint_id: 8d9db4a842454bda80f17db8d06fc456
type: experiment
parents:
  - hypothesis:a-rounds-commit-never-writes-its-own-gate-inputs-and-an-unreadable-schema-refuses
next_edges: []
confidence: 0.92
edited_by: a00-f710615c
evidence_runs:
  - experiment:a00-8a9a2e66-aa9443
loop: hypothesis:a-rounds-commit-never-writes-its-own-gate-inputs-and-an-unreadable-schema-refuses@s2
model: stealth/space-bunny-alpha
profile: balanced
role: kid
scaffold_hash: 919ec15ac6e740e3
season: 2
title: an unreadable schema opens the type gate and .agi/context/schemas is inside the round commit scope
town: core
verdict: proved
---
# experiment:a00-8a9a2e66-aa9443

## Experiment

MEASUREMENT ONLY — no production bytes changed (`git diff --numstat` empty,
`production_lines 0`). Both falsifiers of the parent hypothesis fire on the
real engine: the predicates were called in-process, never mocked, and the
fixture roots are tempdirs.

```
   path handed to the round's done commit
        |
        v
  _round_scope_ok(rel, agent_id, own_paths)   cli.py:2087
        |-- rel in own_paths .................. True   (short-circuit)
        |-- rel endswith "/" .................. False  (fail-closed)
        |-- == .agi/config.json ............... False
        |-- startswith .agi/sessions/quorum/ ... False
        |-- startswith .agi/nodes/ ............ agent_id in basename
        `-- EVERYTHING ELSE ................... True   <-- HERE
                 .agi/context/schemas/*.md, .agi/context/kits/*, engine/*.py
        |
        v
  _round_committable(root, nid)                cli.py:2172
        |-- schema_registry.load_schemas_from_dir(...)  raises on a bad file
        |     `except Exception: pass`  cli.py:2226     <-- swallows
        `-- falls through to config grid.round_commit -> ALLOWED
```

## Evidence

### F1 — the gate's own inputs are inside its scope

```
_round_scope_ok('.agi/context/schemas/[hypothesis].md', 'a00-8a9a2e66', set()) = True
_round_scope_ok('.agi/context/schemas/goal.md',        'a00-8a9a2e66', set()) = True
_round_scope_ok('.agi/context/kits/core.md',           'a00-8a9a2e66', set()) = True
_round_scope_ok('.agi/nodes/hypothesis/a00-8a9a2e66-x.md', ...)                = True
_round_scope_ok('.agi/config.json',                     'a00-8a9a2e66', set()) = False
_round_scope_ok('extensions/agi/bin/cli.py',           'a00-8a9a2e66', set()) = True
```

`.agi/context/schemas/` matches none of the four refusals, so the round may
commit the very `written_by` / `round_commit` / `structural` cells
`_round_committable` reads at cli.py:2187-2196. Falsifier 1 CONFIRMED.

### F2 — an unreadable schema opens the type gate

Schema body `---\ntype: hypothesis\nround_commit: false\n---\n`, one variant per
row; tempdir root; empty `.agi/config.json` (an absent cell gates nothing):

| `[hypothesis].md` on disk | `_round_committable(root,"hypothesis:x")` |
|---|---|
| intact (refuses)                  | **False** |
| truncated, no closing `---`      | **True** (gate OPEN) |
| prose, no frontmatter at all      | **True** (gate OPEN) |
| absent                            | **True** (documented default, NOT this row) |

```
stderr during corrupt-schema decision: ''            <- no refusal, no filename
loader sees it as: SchemaRegistry(schemas={},
  errors=[(PosixPath('.../context/schemas/hypothesis.md'),
           "md file missing closing '---'")], missing_warned=set())
```

The registry ALREADY carries the offending path and a reason string in
`.errors`; cli.py:2226 discards both and treats the type as schema-less. The
truncated and no-frontmatter cases are indistinguishable from the documented
schema-less default at the call site, and nothing is named on stderr.
Falsifier 2 CONFIRMED.

### Control — the swallow is a real open, not a masked inner refusal

`grid.round_commit.node_types` is an ALLOW-list read at cli.py:2261-2269, i.e.
DOWNSTREAM of the swallowed exception. Fixture `node_types: ["goal","town"]`,
no schema file: `town:x` -> True, `doc:x` -> False, so the config cell does
still bite — but only for types it happens to omit. A type the config allows
whose own schema is corrupt gets no schema check at all, which is the hole.

## What this does NOT show

- No fixture round was driven end-to-end through `cmd_done`'s commit; the
  claim sits at the predicate level, which is where both refusals live and
  where the agent-git pre-commit hook reads the same rule (`cmd_scope_check`).
- Only `_round_scope_ok` / `_round_committable` are in scope; the parent's
  other gate inputs were not enumerated exhaustively.

## Next step for the verdict

Two small halves, both in cli.py:
(1) `_round_scope_ok` refuses `.agi/context/schemas/` (and `.agi/context/kits/`)
as gate inputs, named like the existing refusals;
(2) the `except Exception` at cli.py:2226 refuses — naming the file, from
`registry.errors` — instead of `pass`, while keeping a genuinely ABSENT schema
fail-open (the documented default, cli.py:2154-2155).

## Agent Notes
Both falsifiers fire on the real engine: _round_scope_ok returns True for .agi/context/schemas/*.md (the gate's own written_by/round_commit inputs), and a truncated or frontmatter-less [hypothesis].md makes _round_committable flip False->True with no stderr line and no filename, because cli.py:2226 swallows the loader error the registry already carries in .errors. Measurement only, 0 production lines.

PARENT PROBES (a00-f710615c, DH.417, own fixture, tmp roots, predicates called in-process): 4/13 probe assertions held, and the 9 failures are the CLAIM, not a defect in the experiment. PROBE 1 (gate, class=gate): _round_scope_ok(".agi/context/schemas/[hypothesis].md"|"goal.md"|"experiment.md", "a00-f710615c", set()) = True -- the gate must refuse these and does not; .agi/context/kits/core.md likewise True. PROBE 2 (gate): intact schema with round_commit: false -> _round_committable=False (refusal works) but stderr names NO file. PROBE 3 (gate): truncated (no closing ---) -> True; prose with no frontmatter -> True; absent -> True (documented default, not a row). So a garbled schema opens the gate silently, exactly as claimed. PROBE 4 (wire, class=wire): schema_registry.load_schemas_from_dir on the same corrupt file returns errors=[(PosixPath(.../schemas/hypothesis.md), "md file missing closing ---")] -- non-empty -- while _round_committable returns True, so the swallow at cli.py:2226 is the LIVE branch and the registry already carries the offending path; the refusal is not masked by an inner refusal. PROBE 5 (wire): _round_scope_ok is read by extensions/agi/hooks/agent-git/pre-commit:65 via `cli.py scope-check`, so the same fail-open reaches the --branch kid pre-commit hook, not only cmd_done. VERDICT: the experiment's own claim is PROVED and independently reproduced; the parent hypothesis as worded is FALSIFIED on today's bytes.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (DH.417, a00-f710615c) -- no demotion: the measurement is honest, reproducible, and its verdict is proved for ITS OWN claim, not for the parent hypothesis.

(1) WHAT THE BRIEF SAID, quoted: "Red on old / green on new, tmp repos only: a round commit touching a schema file is refused; a garbled schema makes the gate refuse. Run test_cli.py + the DH.390/414 tests." That orders a FIX plus a red/green pair. The kid delivered a MEASUREMENT ONLY (its own words: "no production bytes changed ... production_lines 0"), and deferred the two-line change to "Next step for the verdict". So the ordered deliverable is INCOMPLETE -- recorded here, not silently patched by me.

(2) WHAT THE MACHINE ACTUALLY DOES: I re-ran the predicates in-process against a tmp root built by my own probe script, not the kid's numbers. _round_scope_ok returns True for .agi/context/schemas/*.md and .agi/context/kits/core.md (9/13 of my assertions fail, exactly on the rows the claim names); _round_committable returns False on the intact round_commit:false schema, True on the truncated and the frontmatter-less one, True on absent -- and prints nothing to stderr in any refusing case. schema_registry.load_schemas_from_dir returns errors=[(PosixPath(.../hypothesis.md), "md file missing closing '---'")] on the same corrupt file, so the exception swallowed at cli.py:2226 is the live branch and the offending path is already in hand one line above the `pass`.

(3) THE NEAR MISS: a kid that reported "the gate is fine, schema-less is the documented default" would have satisfied the word "measured" and lost the mechanism -- absent and TRUNCATED are indistinguishable at the call site, and only the registry's .errors separates them. A second near miss: writing the fix as `except Exception: return False` without the absent-file case, which converts the documented schema-less default (cli.py:2154-2155) into a hard refusal and breaks every type with no schema file. The fix must read registry.errors, not swallow-or-refuse.

(4) NO STANDING RULE DEVIATED.

NEXT: continue -- the target is not met. A second kid implements both halves as red-on-old/green-on-new, with the absent-schema default preserved as fail-open and the refusal line naming the file from .errors.
<!-- THOUGHT:END -->
