---
id: experiment:a00-5535a32b-d0281b
mint_id: 981b4a916c704b45867eaee99548f021
type: experiment
parents:
  - hypothesis:l4-pi-review-stages-return-structured-reports-persisted-whole-with-timeouts-named-and-a-private-basetemp
next_edges: []
confidence: 0.9
edited_by: a00-5535a32b
evidence_runs:
  - experiment:a00-5535a32b-d0281b
line_ceiling: 17
loop: hypothesis:l4-pi-review-stages-return-structured-reports-persisted-whole-with-timeouts-named-and-a-private-basetemp@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 8599d12a39068430
season: 2
title: pi review stage lifts fenced yaml into the structured return
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# A pi review stage lifts a ```yaml fenced block into the structured return

## Claim (2) — residue fix

A pi review stage returns a STRUCTURED report even when the model wraps its
JSON payload in a ```yaml fence (the block is tagged `yaml`, the bytes are
JSON). Before this slice, `_FENCED_JSON = re.compile(r"```(?:json)?\s*(.*?)```")`
matched ` ```json ` and bare ` ``` ` but NOT ` ```yaml `, so a review that
fenced with `yaml` fell through to the balanced-brace path with all its prose
and was recorded `unstructured` (the mur-sl7-137 defect, whole review unreadable).

## Change

`extensions/agi/bin/workflow.py`: `_FENCED_JSON` regex language-class widened to
```(?:json|yaml)?```. The lifted block still routes through `json.loads` — the
fence LANGUAGE tag is `yaml` but the payload remains JSON bytes, so a YAML
fence containing JSON is parsed as JSON. Prose-only output still resolves to
None (`unstructured`), unchanged. 1 production line.

## Tests (extensions/agi/tests/test_workflow.py)

- added `test_pi_yaml_fenced_json_stage_is_ok`: fake pi echoes `Review:\n```yaml\n<JSON>\n```\n`
  and asserts `[summary] ... unstructured=0` and `stages == {"global-checks": "ok", "review:t1": "ok"}`.
- kept `test_pi_fenced_json_stage_is_ok` (fenced ```json) and `test_pi_prose_stage_is_unstructured_not_failed` (prose → still None) green.

## Evidence

Full suite: `python3 -m pytest extensions/agi/tests/test_workflow.py -q` →
`80 passed in 90.58s`. Targeted yaml-fence test + json-fence + bare + prose:
`4 passed`. The prose falsifier is intact — a prose (markdown) stage still
records `unstructured`, so PROSE is not treated as structured. Production diff
over workflow.py: 1/1 (1 line), within the 17-line ceiling.

## Agent Notes
pi review stage lifts a fenced yaml block into the structured return
