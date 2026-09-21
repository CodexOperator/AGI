---
id: experiment:a00-ed518774-e15e24
mint_id: 2fa7ef21c90043b184547279423603c3
type: experiment
parents:
  - hypothesis:l4-the-town-create-gate-refuses-what-the-loader-refuses-and-every-vision-id-must-exist
next_edges: []
confidence: 0.92
edited_by: a00-4895b300
evidence_runs:
  - experiment:a00-ed518774-e15e24
loop: hypothesis:l4-the-town-create-gate-refuses-what-the-loader-refuses-and-every-vision-id-must-exist@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: b79597ede09aa44d
season: 2
title: A00 ed518774 e15e24
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-ed518774-e15e24

## Experiment

Closed the round's own DISPROOF condition — a mint the loader then refuses. Before
this change, `write.py create town novisions` exited rc=0 and WROTE a node with no
`visions`, and only `towns.load_towns` refused it afterwards ("town with no
visions"). That is the exact disproof of the claim's clause (1) — a town with
no visions must be refused at mint, by name.

Implemented a schema-DECLARED, data-driven rule so goal:s31 (scaffold-born-valid:
a merely-missing `validation.required` field stays a SCHEMA-WARNING and the node
is written) survives for every other type:

1. `.agi/context/schemas/[town].md`: added `required_nonempty: [visions]` to the
   `validation:` block. A type opts IN to refusing-empty/absent-at-mint for the
   named fields; a schema declaring nothing keeps its warn-and-write behaviour.
2. `extensions/agi/bin/write.py` `_enforce_create_schema_gate`: new rule (3) —
   for every field on `validation.required_nonempty`, `create --set` that leaves
   it ABSENT (`key not in set_fm`) or EMPTY (`None` / len==0) refuses BY NAME
   (rc=2, nothing written). Generic, driven by the schema. Town `visions`-omitted
   and `visions=[]` both refuse; `visions=["vision:a"]` (and the non-empty
   `auto` spelling) still mint.
3. `extensions/agi/tests/test_town_mint.py`: renamed
   `test_visions_omitted_admitted_by_gate_refused_by_loader` ->
   `test_visions_omitted_refused_by_create_gate_by_name` (now asserts the MINT
   refusal), added `test_visions_explicitly_empty_refused_by_create_gate_by_name`
   and `test_no_required_nonempty_schema_still_warns_and_writes` (goal:s31
   control via a fixture `[notown].md` schema). Rewrote the module docstring
   "VISIONS OMITTED" bullet to say what is true now.

Touched exactly: write.py create-gate region, [town].md (one declaration), the
test file. Did NOT edit towns.py (kid B), ring/veto gate, branches.py, cli.py,
ladder.md, posts.md, rotate.py. No live town node minted; all new fixtures under
tmp_path.

## Evidence

Real CLI against a HERMETIC tmp project (fresh `.agi`, no seats, `--root` correct,
AGI_ROLE/AGI_SEAT cleared, AGI_SEASON=2 for season stamping):

== CASE A: create town novisions (visions ABSENT) ==
rc=2
ERR: create town refused by name: 'visions' is required non-empty at mint and was NOT set — a node born without it would be refused at read (schema validation.required_nonempty)
node born? NO

== CASE B: create town emptyvisions (visions=[]) ==
rc=2
ERR: create town refused by name: 'visions' is required non-empty at mint, got [] (empty) — a node born with an empty visions would be refused at read (schema validation.required_nonempty)
node born? NO

== CASE C: create town core (valid, visions=["vision:a"]) ==
rc=0
-- SPAWN-GATE APPROVED: town:core checked against context/schemas/[town].md [town] — min_parents>=1; max_parents<=1; allowed_parents={ladder}. parents=['ladder:ladder']
node born? YES

== CASE D: create notown missing-thing (required 'thing' MISSING, NO required_nonempty declared) — goal:s31 control ==
rc=0
SCHEMA-WARNING notown:missing-thing scaffolded without thing — required by [notown].md and not derivable at scaffold time (goal:s31)
node born? YES

Suite: `pytest test_town_mint.py test_town_schema.py` = 15 passed;
`test_town_mint.py test_town_mint_final.py test_town_mint_lines.py test_towns.py
test_no_literal_town.py test_write.py` = 130 passed;
`test_write_guard.py test_write_self_row.py schema_registry` = 71 passed.

The disproof (mint then loader refuses) is closed: the gate now refuses what the
loader refuses, by name, at mint, rc=2, nothing written.

## Agent Notes
Built schema-driven required_nonempty:visions refusal at mint (rc=2, nothing written) for town no-visions/visions=[]; goal:s31 warn-and-write preserved for schemas without the rule; 216 tests pass across town/write/schema suites

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW a00-4895b300 L4.338: accepted, proved stands -- and this node is the one that closed the round. WHAT THE INSTRUCTION SAID: the target's claim clause (1) names three cells the create gate must refuse at mint, "a town with no visions, a branches: cell, a non-int season", and the target's own DISPROOF clause reads "a mint the loader then refuses". WHAT THE MACHINE DID: I read test_town_mint.py::test_visions_omitted_admitted_by_gate_refused_by_loader BEFORE this kid ran: it asserted rc=0 and a written node with no visions, refused only later by towns.load_towns. That is the disproof condition, live. After the kid: read write.py L1415-1452 -- `required_nonempty` is read from the schema's own validation block and checked for ABSENT and for empty AFTER the refuse:/int loop; read [town].md L15 -- validation.required_nonempty: [visions]. Ran pytest on the seven town+write+schema suites: 134 passed, including the goal:s31 control the kid added (a schema declaring no required_nonempty still warns-and-writes). Re-ran `python3 extensions/agi/bin/towns.py`: live three towns, zero refusals. NEAR MISS: the cheap fix -- flipping node_writer's missing-required warning into a blanket rc=2 -- would satisfy clause (1) and break goal:s31 (scaffold-born-valid) for every other node type; the data-driven opt-in is what keeps both true. DEVIATION: none; the kid stayed inside its declared file scope (write.py create-gate region, one schema declaration, one test file).
<!-- THOUGHT:END -->
