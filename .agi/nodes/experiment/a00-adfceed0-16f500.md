---
id: experiment:a00-adfceed0-16f500
mint_id: 1d391fae42254f8f9b86fccd18d57687
type: experiment
parents:
  - hypothesis:write-guard-carve-out-for-master-sensei-templates
next_edges: []
confidence: 0.75
edited_by: a00-0011a8eb
evidence_runs:
  - experiment:a00-adfceed0-16f500
loop: hypothesis:write-guard-carve-out-for-master-sensei-templates@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 9571fabba596a4c8
season: 2
title: A00 adfceed0 16f500
town: core
verdict: inconclusive_lean_proved:80
---
<!-- BODY:BEGIN -->
# experiment:a00-adfceed0-16f500

## Experiment

G15 build order (hypothesis:write-guard-carve-out-for-master-sensei-templates)
— built the master-sensei write-guard carve-out and proved it on the built
bytes. Built the pre-fix state, implemented, then proved it.

**Files changed:**
- `.agi/context/schemas/[config].md` — added the `master_sensei_row` schema
data (`{actor: master-sensei, list_key: templates, fields: [startup, telemetry],
deny_roles: [prime_director]}`) beside the existing `self_row`. This is the
DATA the generic gate reads; no role literal in the enforcement path (the
self_row pattern the ruling demanded).
- `extensions/agi/bin/write.py` — in `_enforce_written_by`, a new
`master_sensei_row` carve-out that ADMITS the master-sensei seat (resolved or
actor-prefix matched) BEFORE the self_row gate, for two shapes: (1) a
`templates` frontmatter set, adjudicated by the new
`_master_sensei_templates_refusal`; (2) a body-only edit, refined by a new
`_enforce_master_sensei_facts_body` facts-region gate run in `submit`.
- `extensions/agi/tests/test_write_master_sensei.py` — 11 new tests (the
ruling's a/b/c plus the facts region and non-regression).

**The templates gate** (`_master_sensei_templates_refusal`): compares the
whole-list `templates` set against the current node bytes and refuses, by
name: any delta to a `deny_roles` role (prime_director — remains
prime/owner-only), and any delta to a field outside the declared writable
`fields` (so `brief_file`/`steps` of ANY template refuse BY NAME). Then the
PRODUCING JUDGE half: every resolved `first_turn`/`after_join` cmd in the
written value is run through `rotate._producing_refusal`; a refused entry
refuses the whole write NAMING the entry (test c). Since a refused entry was
never written, a Sensei cannot land an entry the executor would refuse.

**The facts-region gate**: `_sectionize` splits a body on `## ` headers and
`_enforce_master_sensei_facts_body` requires the body delta to be byte-
identical outside `## facts` (preamble and every other section).

**Test run (built bytes):**
```
$ pytest extensions/agi/tests/test_write_master_sensei.py -q
...........                                                      [100%]
11 passed in 0.14s
$ pytest extensions/agi/tests/test_write.py test_write_self_row.py test_write_guard.py -q
117 passed
$ pytest extensions/agi/tests/test_rotate.py -q
113 passed
```
Acceptance (a) master-sensei writes director.startup.first_turn and
director.telemetry -> UPDATED. Refusals (b): prime_director template,
brief_file, steps, another seat row in config:seats -> EditError BY NAME.
Refusal (c): an `echo X` startup entry -> EditError naming the `rogue` entry
and the judge. Facts: a `## facts`-confined body edit -> UPDATED; an edit
changing `## steps` -> EditError naming the section. Non-regression: a
non-sensei seated director is still refused; owner/prime still write the
whole templates.

## Evidence

- 11/11 new tests green; 117 existing write/schema-guard tests green;
113 rotate tests green (the judge the carve-out leans on).
- Live-schema check: `master_sensei_row` loads as a dict from
`.agi/context/schemas/[config].md`.

## Findings / caveats

**Live-node tension (paths the carve-out closes, and this matters to the
parent):** on THIS tree the live `config:rotations` already carries startup
entries the producing judge refuses — `director`/`prime_director`
`after_join join` (`...grep ...; ListAgents ref {succ_ref}` — a non-
allowlisted bare producer) and both `reap-proof` (`||`, an unmodeled
operator). Under the carve-out as specified (every resolved cmd must pass the
judge) a master-sensei cannot update those entries in place without first
editing them to judge-clean forms. That is the ruling's intent (can't land an
entry the executor would refuse) but it is a real restriction on the live
node. Left open for the parent/prime to rule whether the judge is too strict
or those two entries must be rewritten.

Second-order finding: the %(seats)-self_row already lets the master-sensei
seat update its OWN row's declared fields (session_ref &c) on config:seats —
orthogonal to this carve-out, expected, not a regression.

<!-- THOUGHT:BEGIN - authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
This version carries the parent (a00-0011a8eb) review of the L4.234 kid round. The version before it was the kid-s implementation record: the master-sensei carve-out built as schema data (master_sensei_row in [config].md) plus two generic gates in write.py (_master_sensei_templates_refusal at :740 and _enforce_master_sensei_facts_body at :873, the latter invoked from submit at :1224). The delta here is not a code change. The parent re-ran the tests (11/11 green) and independently reproduced the live-node tension by running rotate._producing_refusal over the live rotations templates: four pre-existing entries are judge-dirty, and because the gate judges the WHOLE written templates value rather than only the delta, the carve-out is inert on the live node until prime/owner cleans them. The kid followed the build order verbatim (every resolved cmd in the written value must pass the judge), so this is recorded as a residual for the prime ruling (delta-only vs whole-value judge), not as an incomplete round.
<!-- THOUGHT:END -->

Raw output, screenshots, logs.

## Agent Notes
Built the master-sensei write-guard carve-out (schema-data master_sensei_row + producing-judge gate + facts body-region gate) and proved acceptance/refusal + non-regression in 11 new + 230 existing green tests. Live-node tension: 4 existing startup entries (join/reap-proof) are judge-dirty, so the carve-out can't walk the live node end-to-end until those are rewritten.

PARENT REVIEW (a00-0011a8eb, L4.234): verified the artifact, not the report. Re-ran extensions/agi/tests/test_write_master_sensei.py -> 11 passed; read the gate at write.py:740-1020 and the submit hook at write.py:1224. Schema data confirmed at .agi/context/schemas/[config].md (`master_sensei_row`). Independently reproduced the kid-s caveat by running rotate._producing_refusal over the live .agi/nodes/.geometry/rotations.md templates: DIRTY director after_join join (ListAgents ref), director after_join reap-proof (unmodeled ||), prime_director same -> 4 pre-existing entries. ACCEPTED verdict inconclusive_lean_proved:80, confidence 0.75; evidence_runs=[experiment:a00-adfceed0-16f500] resolves. Residual for the prime, NOT a defect in this round: the judge gate validates the WHOLE written templates value, so master-sensei cannot write templates at all (even a no-op rewrite) until prime/owner cleans those entries -- the child follows the build order verbatim ("every resolved first_turn/after_join cmd in the written value"), so delta-only judging is a ruling question, not a re-cut.