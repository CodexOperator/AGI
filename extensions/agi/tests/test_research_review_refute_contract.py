"""REFUTE_TMPL's stated top-level key list must agree with REFUTE_SCHEMA.

hypothesis:lm-refute-tmpl-return-contract-omits-batch-empty. The template tells
the model to set `batch_empty` and the stage schema REQUIRES it, but the
RETURN CONTRACT sentence stated six keys and forbade adding others -- so a
contract-obeying model omitted batch_empty and failed validation. This test
locks the two lists together: change one and the other must follow.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

WF_DIR = Path(__file__).resolve().parents[1] / "workflows"
WF = WF_DIR / "agi-research-review.js"
MANIFEST = WF_DIR / "research-review.json"


def _js_string(src: str, name: str) -> str:
    m = re.search(rf'const {name} = "(.*)"\n', src)
    assert m, f"{name} not found in {WF.name}"
    return m.group(1).encode().decode("unicode_escape")


def _stated_top_level_keys(tmpl: str) -> list[str]:
    sentence = tmpl.split("TOP-LEVEL keys are exactly:", 1)[1].split(".", 1)[0]
    return re.findall(r"([a-z_]+)\s*\(", sentence)


def test_refute_template_key_list_matches_schema_required():
    src = WF.read_text(encoding="utf-8")
    stated = _stated_top_level_keys(_js_string(src, "REFUTE_TMPL"))
    schema = json.loads(re.search(r"const REFUTE_SCHEMA = (\{.*\})\n", src).group(1))
    assert stated == schema["required"], (stated, schema["required"])
    assert "batch_empty" in stated


def test_manifest_refute_prompt_and_schema_match_js_contract():
    """The manifest drives the Python/pi harness while the JS script drives
    Claude Code. Both must require and name the same refute return fields."""
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    refute = next(s for s in manifest["stages"] if s["label"] == "refute")
    stated = _stated_top_level_keys(refute["prompt"])
    required = refute["schema"]["required"]
    assert stated == required, (stated, required)
    assert "batch_empty" in stated
    assert refute["schema"]["properties"]["batch_empty"] == {"type": "boolean"}

    src = WF.read_text(encoding="utf-8")
    js_stated = _stated_top_level_keys(_js_string(src, "REFUTE_TMPL"))
    assert stated == js_stated
