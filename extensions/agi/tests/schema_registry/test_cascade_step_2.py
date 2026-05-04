"""T-026 tests: cascade step 2 (schema-registry/R5.2)."""

from pathlib import Path

from schema_registry import (
    cascade_step_2,
    collect_fingerprint,
    discover_schema,
    jaccard,
    load_schemas_from_dir,
)


def test_jaccard_basics() -> None:
    assert jaccard({"a", "b"}, {"a", "b"}) == 1.0
    assert jaccard({"a"}, {"b"}) == 0.0
    assert jaccard({"a", "b", "c"}, {"a", "b"}) == 2 / 3


def test_collect_fingerprint(tmp_path: Path) -> None:
    (tmp_path / "n1.md").write_text("---\nid: a\ntitle: x\n---\n")
    (tmp_path / "n2.md").write_text("---\nid: b\nverdict: pending\n---\n")
    fp = collect_fingerprint(tmp_path)
    assert {"id", "title", "verdict"}.issubset(fp)


def test_step_2_high_similarity_match(tmp_path: Path) -> None:
    """R5.2: 70% field overlap → schema is selected."""
    schemas_dir = tmp_path / "schemas"
    schemas_dir.mkdir()
    (schemas_dir / "[experiment].md").write_text(
        "---\nname: experiment\nfields:\n  id: {type: string}\n  verdict: {type: string}\n  evidence_runs: {type: list}\n---\n"
    )
    reg = load_schemas_from_dir(schemas_dir)
    target = tmp_path / "data"
    target.mkdir()
    # Files with 2/3 of the schema's fields → ~0.66 overlap
    (target / "node1.md").write_text("---\nid: e1\nverdict: proved\nevidence_runs: []\n---\n")
    (target / "node2.md").write_text("---\nid: e2\nverdict: pending\nevidence_runs: []\n---\n")
    result = cascade_step_2(target, reg, threshold=0.5)
    assert result.schema is not None
    assert result.schema.name == "experiment"
    assert result.step == "fingerprint"


def test_step_2_below_threshold_no_match(tmp_path: Path) -> None:
    """R5.2: similarity < threshold → no match."""
    schemas_dir = tmp_path / "schemas"
    schemas_dir.mkdir()
    (schemas_dir / "[experiment].md").write_text(
        "---\nname: experiment\nfields:\n  verdict: {type: string}\n  evidence_runs: {type: list}\n---\n"
    )
    reg = load_schemas_from_dir(schemas_dir)
    target = tmp_path / "data"
    target.mkdir()
    (target / "totally_unrelated.md").write_text("---\nrandom_field: 1\nother: 2\n---\n")
    result = cascade_step_2(target, reg, threshold=0.7)
    assert result.schema is None


def test_discover_schema_uses_step_2_after_step_1(tmp_path: Path) -> None:
    """End-to-end: bracket miss → fingerprint match."""
    schemas_dir = tmp_path / "schemas"
    schemas_dir.mkdir()
    (schemas_dir / "[experiment].md").write_text(
        "---\nname: experiment\nfields:\n  id: {type: string}\n  verdict: {type: string}\n---\n"
    )
    reg = load_schemas_from_dir(schemas_dir)
    # Directory name doesn't match — bracket step misses
    target = tmp_path / "weird_name"
    target.mkdir()
    (target / "x.md").write_text("---\nid: e1\nverdict: proved\n---\n")
    result = discover_schema(target, reg)
    assert result.step == "fingerprint"
    assert result.schema is not None
    assert result.schema.name == "experiment"
