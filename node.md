---
id: experiment:a00-3ddb5d1b-989253
mint_id: f6b781881ec443da93c7c460708d1ae3
type: experiment
parents:
  - hypothesis:l4-the-carve-out-refuses-a-non-dict-template-and-keys-on-the-resolved-seat
next_edges: []
confidence: 0.95
edited_by: a00-6c0bf498
evidence_runs:
  - experiment:a00-3ddb5d1b-989253
loop: hypothesis:l4-the-carve-out-refuses-a-non-dict-template-and-keys-on-the-resolved-seat@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 89b582c6952c9dea
season: 2
title: A00 3ddb5d1b 989253
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-3ddb5d1b-989253

## Experiment

A g15 build order (hypothesis:l4-the-carve-out-refuses-a-non-dict-template-and-keys-on-the-resolved-seat): the master-sensei templates carve-out in `write.py` shipped four defects; this round IMPLEMENTED the four claims and PROVED them on built bytes.

Scope: `extensions/agi/bin/write.py` + `extensions/agi/tests/test_write_master_sensei.py`. Repo suite **134 passed** (test_write.py, test_write_guard.py, test_write_self_row.py, test_write_master_sensei.py).

**Fix (1) — non-dict template value refused by name.** In `_master_sensei_templates_refusal`, `templates.director = 'garbage'` (a str) used to slip the field check because it is gated on `isinstance(old_r, dict) and isinstance(new_r, dict)` — the `is_ms` arm chose the free-text actor and the writer silently dropped brief_file + steps. Added, before the field loop: `if role in new_val and not isinstance(new_val[role], dict): return "template {role!r} must be a dict of fields, got {type}"`. Tests `test_master_sensei_refused_non_dict_template_value` (str) and `..._list_value` (list) both `EditError` naming role + `must be a dict` + the actual type, and the drop does not land.

**Fix (2) — facts-body gate scoped to the list_key node.** In `_enforce_written_by` the body-only master-sensei branch returned (admitted) for ANY config node; a config:seats body probe was admitted. It now returns only when `_read_node_fm(where).get(list_key)` is truthy; otherwise it falls through to the self_row/written_by refusal. `_enforce_master_sensei_facts_body` independently raises when the node's frontmatter lacks `list_key`. Test `test_master_sensei_refused_config_seats_body_edit` (a config:seats body-only `## facts` delta) is refused.

**Fix (3) — identity is the RESOLVED SEAT, not the `--actor` string.** All three `is_ms` sites (`_master_sensei_templates_refusal`, `_enforce_master_sensei_facts_body`, `_enforce_written_by`) replaced `str(actor)==actor_row or startswith(actor_row+'-')` with `_resolve_seat(root, actor) == str(actor_row)` — the same identity L4.110's self_row rule keys on. The fixture gained a longer-prefix collision seat `master-sensei-impostor`; `test_master_sensei_impostor_resolves_to_other_seat_refused` proves `master-sensei-impostor-9f` (longest-prefix -> impostor seat, not master-sensei) is refused a templates write even though its STRING starts with `master-sensei-`.

**Fix (4) — the `-h` epilog example parses.** Moved `VERB_EXAMPLES` to module level (next to `ARITY`), changed `"set": "set k=v"` (one token, arity-2 verb, refused) to `"set": "set key value"`. Two new tests: `test_verb_examples_parse_as_their_arity` asserts EVERY example parses via the shared `parse_script` to exactly `ARITY[name]` args; `test_set_epilog_example_is_two_arg` pins the regression. `write.py -h` now prints `set  2 arg(s)  set key value`.

## Evidence

- `python3 -m pytest extensions/agi/tests/test_write_master_sensei.py -q` -> **17 passed** (11 prior + 4 fixed-blocks + 2 epilog). All 4 defect-probing tests are NEW.
- Full suite on touched files: **134 passed**.
- `python3 extensions/agi/bin/write.py -h` -> `set\t2 arg(s)\tset key value`.
- Pre-fix falsification confirmed by construction: (1) non-dict new_r skipped the dict-gated field check; (2) the body branch returned before self_row; (3) `startswith('master-sensei-')` admitted the impostor string; (4) the drift guard checked presence but not parseability.
- Commentary deviation: the hypothesis's claim (3) wording said identity is `_resolve_role(root, actor,'') == the declared actor`, but `_resolve_role` returns the seat's ROLE (e.g. `director`), not the seat NAME (`master-sensei`), so that literal compare would never match. The correct identity is the seat NAME via `_resolve_seat`, which IS the codebase's established L4.110 identity — used here.

## Agent Notes
Implemented all 4 g15 claims in write.py + test_write_master_sensei.py: (1) non-dict template value refused by name, (2) facts-body gate scoped to the list_key node, (3) is_ms keyed on _resolve_seat not the --actor string, (4) -h epilog set example 'set key value'; 134 tests pass, all 4 falsifier probes refused.

PARENT REVIEW (a00-6c0bf498, L4.248): accepted, proved at 0.95. Independent verification beyond the kid report: (1) read the four code sites in write.py -- is_ms now `_resolve_seat(root, actor) == str(actor_row)` at 794/941/1046; the non-dict template refusal sits INSIDE the role loop before the dict-gated field check (write.py 832-840); the facts-body gate requires `_read_node_fm(...).get(list_key)` (946-957); VERB_EXAMPLES is module level with set -> "set key value" (1631). (2) Ran the kid four falsifier tests cold: 6 passed. (3) `write.py -h` prints set 2 arg(s) set key value; the old form `set k=v` still errors `set: wrong arguments` on the live script. (4) Ran the full engine suite: 2657 passed, 6 skipped, 1 failed -- test_stream_master_semantic_screen.py::test_zero_novel_escapes, a live ModelJudge/OPENROUTER_API_KEY measurement unrelated to write.py (same file documents it as an environment-gated model call); not a regression from this round. Residual NOT in this node scope: the live config:rotations still carries judge-dirty after_join entries, so the master-sensei cannot form a write on the live tree -- that is the prime/owner decision recorded in the parent harvest.
