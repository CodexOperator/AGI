"""agi-brainstorm's JS return schema must agree with the manifest's declared
contract for the same stage — the brainstorm half of
`hypothesis:brainstorm-and-research-review-contracts-match-their-manifests`
(PASS 5/6 residue: "JS and manifest refute return contracts diverge";
research-review already pins this in `test_research_review_refute_contract.py`,
brainstorm did not).

`agi-brainstorm.js`'s prompts ask for the return in plain English (no
`RETURN CONTRACT: ... TOP-LEVEL keys are exactly: ...` sentence the way
research-review's do), so there is no prose to parse here — the
`agent(..., {schema: ...})` call's JS schema literal IS the JS-side return
contract (the runner validates the model's structured return against it),
and the manifest's own per-stage `schema` is the pi-route's copy of the same
contract. Comparing the two `required` lists directly is the faithful
version of "diff JS return keys against the manifest" for this workflow.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

WF_DIR = Path(__file__).resolve().parents[1] / "workflows"
WF = WF_DIR / "agi-brainstorm.js"
MANIFEST = WF_DIR / "brainstorm.json"

#: stage label (manifest) -> JS schema const name (agi-brainstorm.js)
STAGE_SCHEMA_CONSTS = {
    "brainstorm": "BRAINSTORM_SCHEMA",
    "refute": "REFUTE_SCHEMA",
}


def _js_schema(src: str, const_name: str) -> dict:
    m = re.search(rf"^const {const_name} = (\{{.*\}})\n", src, re.M)
    assert m, f"{const_name} not found in {WF.name}"
    return json.loads(m.group(1))


def _manifest_schema(manifest: dict, label: str) -> dict:
    stage = next(s for s in manifest["stages"] if s["label"] == label)
    return stage["schema"]


def test_every_manifest_stage_has_a_js_schema_counterpart():
    """The map above must cover every stage the manifest declares — a new
    stage added to one side with no counterpart on the other is exactly the
    silent-divergence failure this file exists to catch."""
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    labels = {s["label"] for s in manifest["stages"]}
    assert labels == set(STAGE_SCHEMA_CONSTS)


def test_js_and_manifest_schemas_declare_the_same_required_keys():
    src = WF.read_text(encoding="utf-8")
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    for label, const_name in STAGE_SCHEMA_CONSTS.items():
        js_schema = _js_schema(src, const_name)
        m_schema = _manifest_schema(manifest, label)
        assert js_schema["required"] == m_schema["required"], (
            label, js_schema["required"], m_schema["required"])


def test_js_and_manifest_schemas_declare_the_same_property_names():
    """`required` matching is not enough on its own — an optional field
    present in one schema and absent from the other is the same class of
    divergence one stage narrower than `required`."""
    src = WF.read_text(encoding="utf-8")
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    for label, const_name in STAGE_SCHEMA_CONSTS.items():
        js_schema = _js_schema(src, const_name)
        m_schema = _manifest_schema(manifest, label)
        assert set(js_schema["properties"]) == set(m_schema["properties"]), (
            label, sorted(js_schema["properties"]), sorted(m_schema["properties"]))
