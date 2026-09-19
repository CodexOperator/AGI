"""SM.125 -- config_max / template_max are REQUIRED merge-up-review fields.

hypothesis:l4-config-max-and-template-max-are-required-verdict-fields-of-
every-merge-up-review-and-a-named-line-of-every-dispatch-order.

The round declares schema DATA, not validation code: workflow.validate_return
already calls real jsonschema.validate and names a missing required field /
an invalid enum value (extensions/agi/bin/workflow.py:937). These tests pin
that the live manifest carries the fields, that a return missing either is
refused BY NAME, that a bad enum value is refused (kid-2's regression: the
shape was silently widened to {"type": "string"}), and that the director
brief carries the one-named-line dispatch shape.

No test here touches a real pane, unit, crontab or process.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

BIN = Path(__file__).resolve().parents[1] / "bin"
REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(BIN))

from workflow import validate_return  # noqa: E402

WF = REPO / "extensions" / "agi" / "workflows" / "merge-up-review.json"
BRIEF = REPO / ".agi" / "nodes" / "doc" / "unified-director-brief.md"

ANSWER_ENUM = {"enum": ["yes", "no"]}


def _stages() -> dict:
    return {s["label"]: s for s in json.loads(WF.read_text())["stages"]}


def _review_return(**over):
    r = {
        "round": "r1",
        "verdict_recommendation": "accept",
        "conjuncts": [],
        "defects": [],
        "defects_summary": "NONE",
        "tests_run": "1 passed",
        "node_checks": "n",
        "prime_step": "p",
        "config_max": {"answer": "no", "where": ""},
        "template_max": {"answer": "no", "where": ""},
    }
    r.update(over)
    return r


def _verify_return(**over):
    r = {
        "round": "r1",
        "verdicts": [],
        "missed": [],
        "final_recommendation": "accept",
        "summary": "s",
        "config_max": {"answer": "no", "where": ""},
        "template_max": {"answer": "no", "where": ""},
    }
    r.update(over)
    return r


# (a) both live stages require the two fields, with the yes|no enum ----------
def test_both_stages_require_config_and_template_max():
    for label, factory in (("review", _review_return),
                           ("verify", _verify_return)):
        schema = _stages()[label]["schema"]
        assert "config_max" in schema["required"], label
        assert "template_max" in schema["required"], label
        for field in ("config_max", "template_max"):
            shape = schema["properties"][field]
            assert shape["type"] == "object", (label, field)
            assert shape["required"] == ["answer", "where"], (label, field)
            assert shape["properties"]["answer"] == ANSWER_ENUM, (
                label, field, shape["properties"]["answer"])
            assert factory()  # the factory matches that stage


def test_verify_holds_the_fields_at_top_level_not_inside_verdict_items():
    verify = _stages()["verify"]["schema"]
    assert "config_max" in verify["properties"]
    assert "template_max" in verify["properties"]
    item = verify["properties"]["verdicts"]["items"]
    assert "config_max" not in item.get("properties", {})
    assert "template_max" not in item.get("properties", {})


# (b) missing either field is refused AND the violation names it -------------
def test_missing_each_field_is_refused_by_name():
    for label, factory in (("review", _review_return),
                           ("verify", _verify_return)):
        schema = _stages()[label]["schema"]
        for field in ("config_max", "template_max"):
            bad = factory()
            del bad[field]
            errs = validate_return(schema, bad)
            assert errs, (label, field)
            assert any(field in e for e in errs), (label, field, errs)


# (c) a well-formed return validates with zero violations --------------------
def test_well_formed_returns_validate_clean():
    stages = _stages()
    assert validate_return(stages["review"]["schema"], _review_return()) == []
    assert validate_return(stages["verify"]["schema"], _verify_return()) == []


# (d) an out-of-enum answer is refused -- the kid-2 regression ---------------
def test_bad_enum_value_is_refused_for_both_stages():
    for label, factory in (("review", _review_return),
                           ("verify", _verify_return)):
        schema = _stages()[label]["schema"]
        for field in ("config_max", "template_max"):
            bad = factory(**{field: {"answer": "maybe", "where": ""}})
            errs = validate_return(schema, bad)
            assert errs, (label, field)
            assert "maybe" in " ".join(errs) or "enum" in " ".join(
                errs).lower(), (label, field, errs)


def test_answer_shape_is_literally_the_enum():
    """The one thing both prior kids got wrong: assert the committed bytes."""
    for label in ("review", "verify"):
        props = _stages()[label]["schema"]["properties"]
        assert props["config_max"]["properties"]["answer"] == ANSWER_ENUM
        assert props["template_max"]["properties"]["answer"] == ANSWER_ENUM


# (e) the brief carries exactly one named dispatch line ----------------------
def test_brief_carries_exactly_one_config_max_template_max_code_line():
    lines = BRIEF.read_text().splitlines()
    hits = [ln for ln in lines if all(
        tok in ln for tok in ("config-max:", "template-max:", "code:"))]
    assert len(hits) == 1, hits
