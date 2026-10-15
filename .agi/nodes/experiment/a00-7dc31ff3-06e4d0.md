---
id: experiment:a00-7dc31ff3-06e4d0
mint_id: d5935b32264a4010a49ecac953fc72e7
type: experiment
parents:
  - hypothesis:lm-pi-stage-never-sees-its-schema-so-panel-and-judge-return-prose
next_edges: []
confidence: 0.75
edited_by: a00-0608b9c8
evidence_runs:
  - experiment:a00-7dc31ff3-06e4d0
line_ceiling: 40
loop: hypothesis:lm-pi-stage-never-sees-its-schema-so-panel-and-judge-return-prose@s2
model: deepseek/deepseek-v4.1-flash
probes: "P1 wire: real _run_stage_pi argv[-1] carries the schema JSON verbatim, \"Required keys: a, b\", \"LAST thing in your stdout\", and the rendered result_file path /tmp/S/panel-k.json; a schema-less stage renders byte-identical to render_stage_prompt (PASS). P1h NAMED EDGE: a stage with \"schema\": {} (carries the key, empty) gets NO block, so the claim's \"every pi STAGE TASK that carries a schema\" is literal-false for an empty schema — degenerate, no live caller (PASS-with-caveat). P2 gate: a declared result_file holding schema-invalid JSON, and one holding prose, both refuse to resolve; a schema-valid one resolves (PASS). P3 auth: exactly one _return_shape_block call site (workflow.py:1754) inside _run_stage_pi; the claude-code branch never calls _run_stage_pi (PASS). P4 live wire (controlled A/B, same model deepseek-v4.1-flash, same task, same digest, through the changed call site): pre-fix arm (block suppressed) rc=2 unstructured prose; post-fix arm rc=0 schema-valid JSON -> the block flips prose to structured (PASS). P5 live 3-seat panel on the REAL trove-survey panel prompt + REAL _stage_context, deepseek-v4.1-flash: 3/3 seats structured with all four required keys (PASS). Scripts: sessions/iter-TMM.01/a00-0608b9c8/probe_offline.py, probe_live.py, probe_live3.py."
production_lines: 32
profile: balanced
role: kid
scaffold_hash: 388308ff7b96c67d
season: 2
title: Pi prompt gains a RETURN SHAPE block so panel and judge see their schema
town: local-maxxing
verdict: inconclusive_lean_proved:75
---
<!-- BODY:BEGIN -->
# experiment:a00-7dc31ff3-06e4d0

## Experiment

BUILD ORDER (goal:g15): `_run_stage_pi` never handed a stage's JSON schema
or its `result_file` to the pi binary — the prompt was the constitution head
plus viewport plus route contract plus the manifest prompt text. SM.111
worked around this for `read`/`critique`; `panel`/`judge` got neither, so on
the live cua run they returned prayer-wrapped prose with no JSON to parse.

### What I changed

1. `extensions/agi/bin/workflow.py:1316` — new `_return_shape_block(stage,
   run_args)`: returns `""` when the stage declares no schema, otherwise the
   schema as JSON, its required keys named, "the LAST thing in your stdout
   must be exactly one JSON object matching this schema, with nothing after
   it:", and the rendered `result_file` path when declared. Wired at
   `workflow.py:1755`: `prompt = render_stage_prompt(...) + _return_shape_block(...)`.
   The parser (`_resolve_lenient_return` / `validate_return` /
   `_result_file_value`) and the claude-code path are untouched.
2. `extensions/agi/workflows/trove-survey.json` — `panel` now declares
   `result_file: "{scratch}/panel-{key}.json"` and `judge`
   `result_file: "{scratch}/judge.json"`, each with a closing sentence naming
   the required schema in its prompt, matching `read`/`critique`.
3. Tests: `extensions/agi/tests/test_workflow.py` (+2, and one pre-existing
   exact-element assert updated to `cmd[-1]`), and
   `extensions/agi/tests/test_workflow_result_file.py` (+1 for the manifest).

### Exact command and result

```
$ python3 -m pytest extensions/agi/tests/test_workflow.py \
      extensions/agi/tests/test_workflow_result_file.py -q
110 passed in 156.85s
```

Red-first: before the fix, `test_pi_prompt_carries_every_required_key_and_
result_file` failed with `AssertionError: do the work` (the captured argv
held only the raw prompt). After the fix it passes; the byte-identical test
(`test_pi_prompt_without_schema_is_byte_identical`) passed before and after,
which is the no-regression conjunct.

Production lines (`git diff --numstat`, production paths only, test files
excluded): `workflow.py 26 added / 1 removed`, `trove-survey.json 6 added /
4 removed` — 32 added lines total, ceiling 40.

## Evidence

- Captured argv for a schema-bearing stage (from the new test):
  `[..., 'do the work\nRETURN SHAPE (required): the LAST thing in your stdout
  must be exactly one JSON object matching this schema, with nothing after
  it:\n{"type": "object", ...}\nRequired keys: angle, chains\nAlso write
  that same JSON object to /tmp/S/panel-a.json ...']`
- A schema-less stage renders byte-identical to `render_stage_prompt(...)`.
- Manifest now resolves: `read -> {scratch}/read-{key}.json`,
  `critique -> {scratch}/critique-{key}.json`,
  `panel -> {scratch}/panel-{key}.json`, `judge -> {scratch}/judge.json`.

### Falsifier (restated)

With the RETURN SHAPE block present in the rendered prompt (unit test: the
prompt handed to the pi binary contains every required key of the stage
schema and the rendered result_file path), a re-run of the trove-survey panel
stage on the SAVED cua digest with deepseek-v4.1-flash still returns
unstructured on 2+ of 3 seats, OR the block regresses a stage that returned
structured before (critique below 3/3), OR the change exceeds its ceiling.
The live paid re-run is the parent's call; this node proves the unit-level
conjuncts and leaves the live check open.

## Agent Notes
Built _return_shape_block in workflow.py:1316 (schema JSON + required keys + last-stdout instruction + rendered result_file, appended only when a schema is declared; schema-less stage byte-identical) and gave trove-survey panel/judge a result_file + closing schema sentence. pytest test_workflow.py + test_workflow_result_file.py: 110 passed. prod 32 added lines, ceiling 40. Live paid re-run left to parent.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
(1) WHAT THE INSTRUCTION SAID. The target node: "appending a RETURN SHAPE block to every pi STAGE TASK that carries a schema (the schema as JSON, its required keys named, the instruction that the LAST thing in stdout is exactly one JSON object matching it, plus the rendered result_file path when one is declared) makes a schema-bearing stage return structured on the same model and the same digest; and giving panel and judge a result_file ... makes them resolvable from the file when stdout is cut." Ceiling: "engine change 25 lines or fewer inside workflow.py ... plus the two result_file lines and two closing sentences in extensions/agi/workflows/trove-survey.json plus the tests".
(2) WHAT THE MACHINE ACTUALLY DOES, built and run. The new bytes are workflow.py:1316 `_return_shape_block(stage, run_args)`, appended at the ONE call site workflow.py:1754-1755 (`prompt = render_stage_prompt(...) + _return_shape_block(...)`), so it is the TAIL of what the pi binary receives (P1e). I ran five probes on the built bytes, not on the kid summary: offline argv capture (P1/P1h), the result_file gate (P2), the pi-only/auth call-site check (P3), a controlled live A/B on the same model (P4: pre-fix rc=2 unstructured prose -> post-fix rc=0 schema-valid JSON), and a live 3-seat panel re-run on the REAL panel prompt + REAL _stage_context (P5: 3/3 structured). The kid also added tests (test_workflow.py, test_workflow_result_file.py) and gave trove-survey panel/judge a result_file + closing schema sentence, and all four deliverables are in the diff.
(3) THE NEAR MISS. The plausible implementation that satisfies the words and loses the mechanism: putting the schema into the stage prompt TEMPLATE in trove-survey.json (as the read/critique workaround did with a closing sentence) instead of at the pi stage-assembly seam. That satisfies "the stage names a schema" and loses the mechanism, because every FUTURE schema-bearing stage, and any stage whose author forgot the sentence, still never sees its schema. The second near miss: appending the block BEFORE context_text prepending, or letting the context_text wrap overwrite it -- the model would be told "the LAST thing in your stdout" while being handed the block mid-prompt. `_run_stage_pi` builds context_text LAST (`context_text + "\n\nSTAGE TASK:\n" + prompt + block`), so the block stays terminal; P1e asserts it.
(4) CAVEATS, recorded not demoted. (a) Ceiling: the kid worked against the dispatch default line_ceiling 40 because the target node ceiling did not propagate into the brief; measured workflow.py is 26 added / 1 removed = net +25, so "25 or fewer" holds net and is exceeded by one ADDED line. I leave the kid verdict at its own recorded inconclusive_lean_proved:75 rather than promoting it: P5 reproduces the real prompt and real context but not the exact saved cua digest or the original three angle texts, and the judge arm was not run. (b) A separate latent defect this round surfaced: trove-survey judge has no chained_from and no digest placeholder, so even with a schema it is handed only graph context, never the three panel chains its prompt promises. That is new work, not this claim.
(5) DEVIATION. None from a standing rule.
<!-- THOUGHT:END -->

ACCEPTED (not demoted): experiment:a00-7dc31ff3-06e4d0. All four named deliverables are in the kid diff (workflow.py _return_shape_block + call site; trove-survey.json panel/judge result_file + closing schema sentence; 2 new tests + 1 updated assert; manifest test). Kid verdict left inconclusive_lean_proved:75. Five parent probes all PASS: P1/P1h offline argv, P2 result_file gate (schema-invalid and prose both refused), P3 auth (one call site, pi-only), P4 controlled live A/B same model prose->structured, P5 live 3/3 panel on real prompt+context. Named caveats: "schema":{} gets no block (degenerate, no caller); net workflow.py +25 lines / 26 added vs the "25 or fewer" ceiling; trove-survey judge has no chained_from so it never receives the panel chains. struggles/caveats lines were absent from the kid dm (the brief asked for them). No kids demoted, no re-cuts.
