---
id: experiment:a00-1ad5908f-7981ba
mint_id: a92a05dd05734a478281c77c0ec602fb
type: experiment
parents:
  - hypothesis:every-write-py-path-is-schema-checked-not-only-the-set-verb
next_edges: []
confidence: 0.9
edited_by: a00-e017cdf8
evidence_runs:
  - experiment:a00-1ad5908f-7981ba
loop: hypothesis:every-write-py-path-is-schema-checked-not-only-the-set-verb@s2
model: stealth/space-bunny-alpha
production_lines: 16
profile: balanced
role: kid
scaffold_hash: 8aa6eeec91593f13
season: 2
title: submit() runs the same schema gate as the CLI set verb
town: core
verdict: proved
---
# experiment:a00-1ad5908f-7981ba — every write.py path is schema-checked, not only `set`

## Falsifier, run first (pre-fix bytes)

`submit()` is the only writer in the module and the path every engine caller
(rotate.py:9518's list cells among them) writes through. On a tmp fixture
carrying a trimmed `[goal].md` schema, three edits the CLI's `set` refuses:

```
raw scalar into list: WROTE status=updated changed=True
out of regex:         WROTE status=updated changed=True
bad type:             WROTE status=updated changed=True
```

Falsifier fires. The hypothesis's defect-3 measurement holds on the bytes.

## Fix (16 production lines, `extensions/agi/bin/write.py`, in `submit()`)

`submit()` now runs the SAME `_enforce_set_schema_gate(root, node_type,
edit.set_fm)` that `main()` runs on the CLI, after the replace/diff
resolution and before `update_node` / `replace_payload`, and raises
`EditError(refusal)`. Only the CALLER's `set_fm` is judged — exactly as on
the CLI — so the provenance/ring cells `submit()` stamps on itself are not
gated.

## Post-fix, same three edits

```
raw scalar into list: REFUSED set goal refused by name: 'tags' must be a list value, got 'a,b,c' (schema declares tags: list)
out of regex:         REFUSED set goal refused by name: 'goal_id' must match '^[GS]\\d+(\\.\\d+)*$', got 'X9' (schema validation.regex)
bad type:             REFUSED set goal refused by name: 'confidence' must be a float value, got 'notafloat' (schema declares confidence: float)
```

One line each, naming the row and the rule, identical to the CLI's text.

## Tests — `extensions/agi/tests/test_write_schema_checked.py`

- `test_submit_refuses_what_the_cli_set_refuses` (parametrized x3) — raises
  `EditError`, single line, names key + rule, node bytes unchanged.
- `test_submit_still_writes_a_schema_valid_row` — a real list lands, no
  regression on the happy path.
- `test_submit_on_a_schema_less_type_gates_nothing` — a type with no schema
  gates nothing, as on the CLI.

`python3 -m pytest extensions/agi/tests/test_write_schema_checked.py -q`
→ 15 passed. The 11 write/node_writer/town/rotate-adjacent write suites
→ 360 passed. Full `extensions/agi/tests/test_*.py` (270 files) → 6560 passed,
29 skipped, 1 xfailed, 1 failed: `test_dispatch_forward_env.py::
test_listed_name_reaches_the_child_when_the_shell_never_sourced_env`, which
asserts `TYPESAFE_KEY not in os.environ` and fails because this session's
shell exports it — pre-existing and environment-borne, unrelated to write.py.

## Note left forward

The gate is per-node-id prefix (`goal:g1` → schema `goal`), the same shortcut
the CLI already used; a node whose id prefix differs from its `type:` still
gates nothing. Left as-is — fixing it is a separate, wider change.

## Agent Notes
submit() now runs the same _enforce_set_schema_gate the CLI set verb runs; falsifier reproduced pre-fix (3/3 wrote) and refused post-fix; 15 schema tests + full 270-file suite green except one pre-existing TYPESAFE_KEY env failure

PARENT REVIEW (a00-e017cdf8, DH.420) — probes run BY THE PARENT on TMP graphs (my session dir, never the live .agi), scripts probe_submit_gate.py / probe_wire.py / probe_refuse.py in this session dir.

probes:
- gate: write.submit(root, Edit(node_id="goal:g1", set_fm={"tags": "a,b,c"})) on a tmp graph carrying the REAL context/schemas -> EditError: "set goal refused by name: 'tags' must be a list value, got 'a,b,c' (schema declares tags: list)". Node bytes unchanged.
- gate: same path, set_fm={"goal_id": "X9"} -> EditError: "... must match '^[GS]\d+(\.\d+)*$' ... (schema validation.regex)".
- gate: a schema field carrying a field-level `refuse:` (added to the tmp copy of [goal].md, the declaration shaped exactly as the town `branches:` cell at [town].md:19) -> EditError: "set goal refused by name: 'derived_cell' is not a settable cell - DERIVED, never a cell (schema field-level `refuse:`, enforced generically)"; one line; node bytes unchanged.
- gate (CLI parity): the SAME case through the CLI prints byte-identically - "ERR: set goal refused by name: 'tags' must be a list value, got 'a,b,c' (schema declares tags: list)". The API line == the CLI line minus the "ERR: " prefix.
- wire: with write._enforce_set_schema_gate wrapped in a spy, submit() carrying the ROTATE-SHAPED payload (a LIST of row dicts - the shape rotate.py:9518-9519 builds, edit.set_fm[list_key] = new_rows) shows the gate ENTERED LIVE: node_type "goal", keys ["tags"], types {"tags": "list"}, refusal None, and the write lands (status=updated). The same call with a scalar for that list-typed cell is refused by the same line. No stub refusal was involved: the changed bytes were reached.

accepted: every conjunct of hypothesis:every-write-py-path-is-schema-checked-not-only-the-set-verb holds on the DIFF's bytes (write.py:2202-2215, the +16 lines in 2af9a2085), not on the kid's report. No demotion.

caveats I could not close: (1) I did not execute rotate.py:9477 _write_identity_cells itself - in a bare tmp graph the config schema's self_row/actor_rows grant refuses first (goal:g12, L4.110 ruling B), so the rotate evidence is payload SHAPE + [config].md "seats: {type: list}" + a live gate call on that shape, not the real function; (2) the gate derives node_type from the node-id PREFIX, not from the node's `type:` (the kid's own forward note) - a node whose id prefix differs from its type gates nothing, exactly as on the CLI, so this is parity, not coverage; (3) only the CALLER's own set_fm is gated, so the provenance/ring cells submit() stamps on itself are ungated by design (stated in the diff comment).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW — the kid's DIFF, not its result file, is the evidence. (1) INSTRUCTION: the hypothesis claims write.submit() "runs the SAME _schema_field_refusal check the CLI's set and create verbs run", so a refuse: annotation, a value failing the schema regex/type, and a raw scalar for a list-typed field are each refused through submit() with one line naming the row and the rule, exactly as through the CLI. (2) MACHINE: the diff (commit 2af9a2085; extensions/agi/bin/write.py +16 at 2202-2215) calls _enforce_set_schema_gate(root, edit.node_id.split(":", 1)[0], edit.set_fm) inside submit(), after the replace/diff resolution and before the location move and update_node, raising EditError on a refusal; _enforce_set_schema_gate -> _schema_field_refusal (write.py:1800) is the same predicate main() calls at write.py:3137, so the two surfaces are one implementation, not two hand-kept copies. My own probes (the `probes:` block in this version) confirmed each conjunct on TMP graphs carrying the REAL context/schemas, and the wire probe showed the gate entered live on rotate's payload shape rather than trusting the kid's suite. (3) NEAR MISS: a version that gated only from main() (prose satisfied, library path still open); or one that gated submit()'s POST-STAMP frontmatter, so the provenance/ring cells submit() adds itself would be judged and routine protocol writes would start refusing; or one that read the node's `type:` off disk instead of the id prefix, silently widening coverage the CLI does not have. Each satisfies "submit() runs the check" in words and loses the mechanism. The kid gated the caller's own set_fm by the id prefix - exactly CLI parity, nothing more. (4) DEVIATION: none from a standing rule. Verdict left at the kid's proved; no demotion, no re-brief, no second kid (the target's falsifier is now closed and the remaining note - id-prefix vs type - is a wider, separately-scoped change).
<!-- THOUGHT:END -->
