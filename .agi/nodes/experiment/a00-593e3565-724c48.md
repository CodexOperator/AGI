---
id: experiment:a00-593e3565-724c48
mint_id: c8349ebb003946d8b1f244f1779d66ea
type: experiment
parents:
  - hypothesis:l4-moral-written-by-carrier
next_edges: []
confidence: 0.85
edited_by: a00-97e79d50
evidence_runs:
  - experiment:a00-593e3565-724c48
loop: hypothesis:l4-moral-written-by-carrier@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 55f04a925b67cc7a
season: 2
title: A00 593e3565 724c48
verdict: inconclusive_lean_proved:85
---
<!-- BODY:BEGIN -->
# experiment:a00-593e3565-724c48

## Experiment

Implemented the schema-carried owner rule end to end (hypothesis:l4-moral-written-by-carrier).

**1. Rule as DATA** — `.agi/context/schemas/[moral].md` gained one top-level
frontmatter field: `written_by: owner` (verified the loader reads it back:
`load_schemas_from_dir(.agi/context/schemas).get('moral').frontmatter['written_by']
== 'owner'`).

**2. Both code literals deleted in `extensions/agi/bin/write.py`** — added a
single helper `_enforce_written_by(root, node_type, actor, where)` that loads the
node type's schema via `schema_registry.load_schemas_from_dir` and refuses the
write iff the schema's own frontmatter declares `written_by` and `written_by !=
actor`. Both hardcoded conditions — L524 `edit.node_id.startswith("moral:") and
actor != "owner"` and L926 `node_type == "moral" and actor != "owner"` — were
replaced by a call to that helper.

**3. Test fixture** — `test_write._moral_schema()` gained EXACTLY one data line,
`written_by: owner` in the `[moral].md` it writes. No assertion in the file was
weakened, removed or retargeted.

## Evidence

- `pytest extensions/agi/tests/test_write.py -q` → **64 passed** (ran ONLY this
  file, as the ceiling requires — the full suite was not run).
- Both `startswith("moral:")` / `== "moral"` condition literals are gone from
  `write.py`; remaining `moral` hits are the SAME-message string and helper
  docstring prose, not rule literals.
- Same message preserved: a moral edit without `--actor owner` raises
  `EditError: moral nodes (moral:faith) are hand-edited by the owner only. Pass
  --actor owner (goal:g12).` — byte-identical to today's text.
- No other type's write rule changes: with root `.agi`, a `hypothesis` write
  with actor `director` still passes (no `written_by` declared in its schema).

**🔴 ONE DEVIATION FROM THE CLAIM'S BOUND:** "green with ONLY that one fixture
line changed" is FALSE. `test_submit_moral_without_owner_is_refused` exercises
the submit path but never installed the schema, so a data-driven gate had no
rule to read → it failed `DID NOT RAISE`. Fix was one second, non-assertion
setup line (`_moral_schema(project)` in that test) so the schema-driven gate can
see `written_by`. Mechanism PROVED; the exact "exactly one line" bound in the
claim is a misfiled estimate (red-herring, not a behavioural gap).

## Agent Notes
Rule moved to data: [moral].md carries written_by: owner; both literals in write.py replaced by schema-driven _enforce_written_by; message byte-identical; test_write 64 passed (only file run). Mechanism PROVED. One claim bound FALSE: green needed a 2nd non-assertion line (_moral_schema call) because the submitting test never installed the schema.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (a00-97e79d50, L4.32): ACCEPTED as written, verdict held at inconclusive_lean_proved:85. Independently re-verified: both rule literals gone from write.py; [moral].md carries written_by: owner; _enforce_written_by reads the schema via schema_registry and refuses only when written_by is declared and != actor; pytest test_write.py -q -> 64 passed in my own run; same EditError message text preserved; a schema with no written_by gates nothing, so other node types are untouched. The kid is honest about the ONE deviation: test_submit_moral_without_owner_is_refused needed a setup call to _moral_schema(project) because it never installed the schema — a non-assertion setup line, not a weakened assertion, and the exact one-line bound in the claim was a director misestimate. Not a demotion reason; it is why the verdict stays lean rather than proved: the claimed bound was not met verbatim.
<!-- THOUGHT:END -->
