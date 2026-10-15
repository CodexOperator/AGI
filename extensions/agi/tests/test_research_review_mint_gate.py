"""The mint gate: stages 3/4 are PROPOSE-ONLY unless run args set mint.

hypothesis:lm-research-review-why-brainstorm-mint-by-default. Before this
build, `why` and `brainstorm` ran `write.py create` (idea / hypothesis) on
EVERY run with no gate, so a review minted real graph nodes as a side effect
of reading. Now a `mint` run arg (default ABSENT) threads into the two stage
prompts as `{mint}`, and the create instruction is gated on it.

The gate rests on one mechanism: `render_stage_prompt` formats through
`_SafeDict`, so an ABSENT key renders as the EMPTY STRING, never a KeyError.
This test locks that fact, the empty-string = propose-only branch, the
`mint: true` branch that preserves the create instruction, and the proposal
fields the return contract/schema must always carry.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

BIN = Path(__file__).resolve().parents[1] / "bin"
REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(BIN))

import workflow  # noqa: E402

WF_DIR = Path(__file__).resolve().parents[1] / "workflows"
MANIFEST = WF_DIR / "research-review.json"
JS = WF_DIR / "agi-research-review.js"

BASE = {
    "targets": [
        {
            "key": "k1",
            "hypothesis": "hypothesis:x",
            "experiments": "experiment:y",
            "files": "none",
            "focus": "f",
            "verdict": "disproved",
        }
    ]
}


def _stages() -> dict:
    man = json.loads(MANIFEST.read_text(encoding="utf-8"))
    return {s["label"]: s for s in man["stages"]}


def _render(label: str, extra: dict | None = None) -> str:
    args = dict(BASE)
    if extra:
        args.update(extra)
    return workflow.render_stage_prompt(_stages()[label], args)


def test_absent_key_renders_to_the_empty_string():
    """The _SafeDict fact the gate depends on: absent == ''."""
    assert workflow._SafeDict({})["mint"] == ""
    # and a bare run's rendered gate value is the empty string, not "None"
    assert "MINT GATE: ``" in _render("why")
    assert "MINT GATE: ``" in _render("brainstorm")


def test_why_is_propose_only_when_mint_absent():
    prompt = _render("why")
    assert "run NO create" in prompt
    assert "PROPOSE-ONLY" in prompt
    # the empty gate value selects the propose-only branch, never the true one
    assert "MINT GATE: ``" in prompt
    assert "MINT GATE: `true`" not in prompt
    assert "MINT GATE: `True`" not in prompt


def test_why_fills_proposal_fields_on_the_propose_only_path():
    prompt = _render("why")
    assert "proposed_idea_title" in prompt
    assert "proposed_idea_body" in prompt


def test_brainstorm_is_propose_only_when_mint_absent():
    prompt = _render("brainstorm")
    assert "run NO create" in prompt
    assert "PROPOSE-ONLY" in prompt
    assert "MINT GATE: ``" in prompt
    assert "proposed_hypotheses" in prompt


def test_mint_true_keeps_the_create_instruction_on_both_stages():
    # a JSON `true` reaches the render context as a Python bool, which str()
    # renders as `True`. The stated condition is the AFFIRMATIVE LITERAL
    # (`true` or `True`), so True is ON. Both stages keep the original
    # write.py create text (mint:true reproduces today's behaviour).
    for label in ("why", "brainstorm"):
        prompt = _render(label, {"mint": True})
        assert "MINT GATE: `True`" in prompt
        assert "write.py create" in prompt
        assert "run NO create" in prompt  # the other branch is still stated


def test_gate_sentence_names_the_affirmative_literal():
    """The stated condition is `true`/`True`, never 'non-empty'.

    Regression guard: `str(False)` is `False`, which IS non-empty, so the old
    non-empty wording selected the mint branch for a `mint:false` run.
    """
    for label in ("why", "brainstorm"):
        prompt = _render(label)
        assert "exactly `true` or `True`" in prompt
        assert "non-empty" not in prompt


def test_mint_false_is_propose_only_on_both_stages():
    """The falsifier the previous build missed: `mint:false` must NOT mint.

    Both harnesses must agree on the same input: the pi/python renderer emits
    `False`, the js renderer emits `""`, and both are OFF under the stated
    affirmative-literal condition.
    """
    for label in ("why", "brainstorm"):
        prompt = _render(label, {"mint": False})
        assert "MINT GATE: `False`" in prompt
        assert "run NO create" in prompt
        assert "PROPOSE-ONLY" in prompt
        # the stated rule is the literal one, so `False` is off, not on
        assert "exactly `true` or `True`" in prompt
        assert "non-empty" not in prompt


def test_absent_and_false_are_both_off_by_the_stated_condition():
    """absent -> '' and mint:false -> 'False': both off, one rule."""
    def selects_mint(prompt: str, gate: str) -> bool:
        assert "exactly `true` or `True`" in prompt
        return gate in ("true", "True")

    for label in ("why", "brainstorm"):
        assert not selects_mint(_render(label), "")
        assert not selects_mint(_render(label, {"mint": False}), "False")
        assert selects_mint(_render(label, {"mint": True}), "True")


def test_manifest_schemas_declare_the_proposal_fields():
    stages = _stages()
    why = stages["why"]["schema"]
    assert "proposed_idea_title" in why["properties"]
    assert "proposed_idea_body" in why["properties"]
    assert "proposed_idea_title" in why["required"]
    assert "proposed_idea_body" in why["required"]
    bs = stages["brainstorm"]["schema"]
    assert "proposed_hypotheses" in bs["properties"]
    assert "proposed_hypotheses" in bs["required"]
    item_props = bs["properties"]["proposed_hypotheses"]["items"]["properties"]
    assert set(item_props) == {"title", "testable_claim", "cost", "falsifier"}


def test_js_half_carries_the_same_gate_and_declares_the_fields():
    src = JS.read_text(encoding="utf-8")
    assert "const MINT = (args && args.mint) ? \"true\" : \"\"" in src
    assert "k === 'mint' ? MINT :" in src
    # the js templates state the same affirmative-literal condition as the
    # manifest, so `false` (MINT "") and `true` (MINT "true") agree across
    # harnesses: the js half emits `true`, never `True`, which the literal
    # rule covers too.
    assert src.count("exactly `true` or `True`") == 4
    assert "non-empty" not in src
    for name in ("proposed_idea_title", "proposed_idea_body", "proposed_hypotheses"):
        assert name in src
