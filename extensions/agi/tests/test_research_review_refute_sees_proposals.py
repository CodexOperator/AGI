"""REFUTE must see propose-only content, not just minted content.

hypothesis:a-round-stage-spawns-the-parent-and-chains-its-review-in-one-workflow
found this live (run rr-lm-qk-norm-model-wall-parent): brainstorm proposed 3
hypotheses in propose-only mode (mint absent), but REFUTE_TMPL only ever
referenced `{hypotheses}` -- the MINTED list, `[]` by design on a propose-only
run. The adversarial filter never ran on the proposals at all; the refuter's
own output said "No hypotheses were supplied by the brainstorm stage".

This locks: (1) the manifest's refute prompt renders real proposal content
when chained from a propose-only brainstorm return, (2) it renders real
minted content when chained from a mint:true return, (3) the js half routes
to whichever list is populated and does not leak "[object Object]" (the
naive JS string-coercion bug found alongside the routing bug, fixed at the
same call site since a routed-but-unstringified list is equally unusable).
"""
from __future__ import annotations

import re
from pathlib import Path

import workflow

WF_DIR = Path(__file__).resolve().parents[1] / "workflows"
MANIFEST = WF_DIR / "research-review.json"
JS = WF_DIR / "agi-research-review.js"

RUN_ARGS = {"project_root": "."}

PROPOSED = [
    {"title": "qk-norm cuts the model wall", "testable_claim": "qk-norm reduces peak memory by 10pct",
     "cost": "0 USD", "falsifier": "peak memory unchanged"},
]
MINTED = [
    {"id": "hypothesis:qk-norm-cuts-the-model-wall", "title": "qk-norm cuts the model wall",
     "testable_claim": "qk-norm reduces peak memory by 10pct", "cost": "0 USD"},
]


def _refute_stage() -> dict:
    import json
    man = json.loads(MANIFEST.read_text(encoding="utf-8"))
    return next(s for s in man["stages"] if s["label"] == "refute")


def test_propose_only_brainstorm_output_reaches_the_refute_prompt():
    prior = {"idea": "idea:x", "refined_question": "q", "hypotheses": [],
             "proposed_hypotheses": PROPOSED}
    prompt = workflow.render_stage_prompt(_refute_stage(), RUN_ARGS, prior=prior)
    assert "qk-norm cuts the model wall" in prompt
    assert "qk-norm reduces peak memory by 10pct" in prompt


def test_mint_true_brainstorm_output_still_reaches_the_refute_prompt():
    prior = {"idea": "idea:x", "refined_question": "q", "hypotheses": MINTED,
             "proposed_hypotheses": []}
    prompt = workflow.render_stage_prompt(_refute_stage(), RUN_ARGS, prior=prior)
    assert "hypothesis:qk-norm-cuts-the-model-wall" in prompt
    assert "qk-norm cuts the model wall" in prompt


def test_refute_manifest_prompt_names_both_lists_and_id_branching():
    prompt = _refute_stage()["prompt"]
    assert "{hypotheses}" in prompt
    assert "{proposed_hypotheses}" in prompt
    assert "no id (a proposal)" in prompt


def _js_string(src: str, name: str) -> str:
    m = re.search(rf'const {name} = "(.*)"\n', src)
    assert m, f"{name} not found"
    return m.group(1).encode().decode("unicode_escape")


def test_js_refute_template_names_both_lists_and_id_branching():
    src = JS.read_text(encoding="utf-8")
    tmpl = _js_string(src, "REFUTE_TMPL")
    assert "{hypotheses}" in tmpl
    assert "{proposed_hypotheses}" in tmpl
    assert "no id (a proposal)" in tmpl


def test_js_pipeline_routes_to_whichever_list_is_populated_and_serializes_it():
    src = JS.read_text(encoding="utf-8")
    # the routing: minted wins when non-empty, else the proposed list
    assert "brainstorm.hypotheses && brainstorm.hypotheses.length" in src
    assert "brainstorm.proposed_hypotheses" in src
    # serialized, not left to naive String() coercion (which renders an
    # array of objects as "[object Object]" -- unusable for the model)
    assert "JSON.stringify(mintedHyps)" in src
    assert "JSON.stringify(proposedHyps)" in src


def test_refute_template_key_list_still_matches_schema_required_after_the_fix():
    """Guard against the routing fix accidentally touching the return
    contract this file's sibling test (test_research_review_refute_contract)
    already locks -- batch_empty stays required on the js half."""
    import json as _json
    src = JS.read_text(encoding="utf-8")
    tmpl = _js_string(src, "REFUTE_TMPL")
    sentence = tmpl.split("TOP-LEVEL keys are exactly:", 1)[1].split(".", 1)[0]
    stated = re.findall(r"([a-z_]+)\s*\(", sentence)
    schema = _json.loads(re.search(r"const REFUTE_SCHEMA = (\{.*\})\n", src).group(1))
    assert stated == schema["required"]
    assert "batch_empty" in stated
