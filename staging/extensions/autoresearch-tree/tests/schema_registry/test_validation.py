"""T-024 tests: validation engine (schema-registry/R4)."""

from pathlib import Path

from schema_registry import (
    ValidationResult,
    load_schemas_from_dir,
    validate_nodes_against_registry,
)


def _write_schema_with_rules(d: Path) -> None:
    (d / "hypothesis.md").write_text(
        """---
name: hypothesis
fields:
  title: {type: string}
  confidence: {type: float}
validation:
  required: [title]
  types:
    confidence: float
  regex:
    title: '^[A-Z]'
---
"""
    )


def _write_schema_no_rules(d: Path) -> None:
    (d / "idea.md").write_text("---\nname: idea\n---\n")


def test_no_rules_no_checks(tmp_path: Path) -> None:
    """R4.1: no validation block → no per-field checks."""
    _write_schema_no_rules(tmp_path)
    reg = load_schemas_from_dir(tmp_path)
    nodes = [("idea:abc", "idea", {})]
    result = validate_nodes_against_registry(nodes, reg)
    assert result.errors == []


def test_required_field_missing(tmp_path: Path) -> None:
    """R4.2: violators produce structured errors."""
    _write_schema_with_rules(tmp_path)
    reg = load_schemas_from_dir(tmp_path)
    nodes = [("hyp:bad", "hypothesis", {})]
    result = validate_nodes_against_registry(nodes, reg)
    assert any(
        e.rule == "required" and e.field == "title" for e in result.errors
    )


def test_type_check_fails(tmp_path: Path) -> None:
    _write_schema_with_rules(tmp_path)
    reg = load_schemas_from_dir(tmp_path)
    nodes = [
        (
            "hyp:wrong-type",
            "hypothesis",
            {"title": "Tested", "confidence": "high"},
        )
    ]
    result = validate_nodes_against_registry(nodes, reg)
    assert any(
        e.rule == "types" and e.field == "confidence" for e in result.errors
    )


def test_regex_check_fails(tmp_path: Path) -> None:
    _write_schema_with_rules(tmp_path)
    reg = load_schemas_from_dir(tmp_path)
    nodes = [
        ("hyp:lower", "hypothesis", {"title": "lowercase", "confidence": 0.5})
    ]
    result = validate_nodes_against_registry(nodes, reg)
    assert any(e.rule == "regex" and e.field == "title" for e in result.errors)


def test_valid_node_passes(tmp_path: Path) -> None:
    _write_schema_with_rules(tmp_path)
    reg = load_schemas_from_dir(tmp_path)
    nodes = [("hyp:ok", "hypothesis", {"title": "Tested", "confidence": 0.5})]
    result = validate_nodes_against_registry(nodes, reg)
    assert result.errors == []


def test_failures_by_schema_query(tmp_path: Path) -> None:
    """R4.4: failure counts per schema."""
    _write_schema_with_rules(tmp_path)
    _write_schema_no_rules(tmp_path)
    reg = load_schemas_from_dir(tmp_path)
    nodes = [
        ("hyp:a", "hypothesis", {}),
        ("hyp:b", "hypothesis", {"title": "lowercase", "confidence": "x"}),
        ("idea:c", "idea", {}),
    ]
    result = validate_nodes_against_registry(nodes, reg)
    counts = result.failures_by_schema()
    assert counts.get("hypothesis", 0) >= 2
    assert "idea" not in counts


def test_errors_do_not_abort(tmp_path: Path) -> None:
    """R4.3: a violator does not stop other nodes from being checked."""
    _write_schema_with_rules(tmp_path)
    reg = load_schemas_from_dir(tmp_path)
    nodes = [
        ("hyp:bad1", "hypothesis", {}),
        ("hyp:ok", "hypothesis", {"title": "Tested", "confidence": 0.5}),
        ("hyp:bad2", "hypothesis", {"title": "lowercase", "confidence": 0.5}),
    ]
    result = validate_nodes_against_registry(nodes, reg)
    failed_ids = {e.node_id for e in result.errors}
    assert "hyp:bad1" in failed_ids
    assert "hyp:bad2" in failed_ids
    assert "hyp:ok" not in failed_ids
