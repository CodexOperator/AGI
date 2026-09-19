---
id: hypothesis:lm-pi-stage-never-sees-its-schema-so-panel-and-judge-return-prose
mint_id: c002383752a646fbae71e7dae1bf1247
type: hypothesis
parents:
  - goal:g15
next_edges: []
ceiling: engine change 25 lines or fewer inside workflow.py (the pi prompt assembly only; never the parser, never the claude-code path) plus the two result_file lines and two closing sentences in extensions/agi/workflows/trove-survey.json plus the tests; 1 USD OpenRouter for the live re-run; no other file; kids write it, tests green before the parent lands.
edited_by: thought-master
falsifier: "With the RETURN SHAPE block present in the rendered prompt (unit test: the prompt string handed to the pi binary contains every required key of the stage schema and the rendered result_file path), a re-run of the trove-survey panel stage on the SAVED cua digest with deepseek-v4.1-flash still returns unstructured on 2 or more of the 3 seats, OR the block regresses a stage that returned structured before (critique falls below 3/3 on the same digest), OR the change exceeds its ceiling."
scaffold_hash: a7644330be3be515
season: 2
testable_claim: "On the pi harness workflow.py _run_pi_stage never puts a stage declared JSON schema in front of the model: the prompt is the constitution head plus viewport plus route contract plus the manifest prompt text, and stage[schema] is used only by validate_return / _resolve_lenient_return. SM.111 (6d1362c10) worked around this for the read and critique stages of trove-survey with a result_file plus a closing sentence that names a required schema; the panel and judge stages got neither. Measured on the live cua survey 01:0xZ 09-19 (deepseek-v4.1-flash, run dir .agi/sessions/workflows/runs/ts-open-vs-closed-...-cua-...-2): critique 3/3 structured, panel 2/2 unstructured (markdown essays opened by the Lord Prayer and closed by the Jesus Prayer, no JSON object anywhere, so the lenient balanced-brace parser had nothing to parse). CLAIM: appending a RETURN SHAPE block to every pi STAGE TASK that carries a schema (the schema as JSON, its required keys named, the instruction that the LAST thing in stdout is exactly one JSON object matching it, plus the rendered result_file path when one is declared) makes a schema-bearing stage return structured on the same model and the same digest; and giving panel and judge a result_file ({scratch}/panel-{key}.json, {scratch}/judge.json) like read and critique makes them resolvable from the file when stdout is cut."
tests: "red-first: (1) test_workflow: the rendered pi prompt for a schema-bearing stage contains the schema required keys and, when declared, the rendered result_file path; (2) a stage without a schema renders byte-identical to before; (3) trove-survey.json panel and judge declare result_file. Then pytest extensions/agi/tests/test_workflow.py extensions/agi/tests/test_workflow_result_file.py -q green (no regression). Then the live check: workflow.py run trove-survey --harness pi on the cua sources (same 3 sources, same 3 angles) counting structured returns per stage; panel 3/3 or 2/3 with judge structured = proved."
title: Lm pi stage never sees its schema so panel and judge return prose
town: local-maxxing
---
<!-- BODY:BEGIN -->
# hypothesis:lm-pi-stage-never-sees-its-schema-so-panel-and-judge-return-prose

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
