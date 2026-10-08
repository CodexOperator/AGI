"""T-025 tests: cascade step 1 (schema-registry/R5.1)."""

from pathlib import Path

from schema_registry import cascade_step_1, discover_schema, load_schemas_from_dir


def test_bracket_match_short_circuits(tmp_path: Path) -> None:
    """R5.1: directory named 'idea' matches [idea].md in active set."""
    schemas_dir = tmp_path / "schemas"
    schemas_dir.mkdir()
    (schemas_dir / "[idea].md").write_text("---\nname: idea\nfields:\n  title: {type: string}\n---\n")
    reg = load_schemas_from_dir(schemas_dir)
    target_dir = tmp_path / "idea"
    target_dir.mkdir()
    result = cascade_step_1(target_dir, reg)
    assert result.schema is not None
    assert result.schema.name == "idea"
    assert result.step == "bracket"


def test_no_match_returns_step_no_match(tmp_path: Path) -> None:
    schemas_dir = tmp_path / "schemas"
    schemas_dir.mkdir()
    (schemas_dir / "[hypothesis].md").write_text("---\nname: hypothesis\n---\n")
    reg = load_schemas_from_dir(schemas_dir)
    target_dir = tmp_path / "experiment"
    target_dir.mkdir()
    result = cascade_step_1(target_dir, reg)
    assert result.schema is None
    assert result.step == "no-match"


def test_inactive_schema_not_matched(tmp_path: Path) -> None:
    """R5.1 strict: only ACTIVE (bracketed) schemas match."""
    schemas_dir = tmp_path / "schemas"
    schemas_dir.mkdir()
    # No brackets → inactive
    (schemas_dir / "idea.md").write_text("---\nname: idea\n---\n")
    reg = load_schemas_from_dir(schemas_dir)
    target_dir = tmp_path / "idea"
    target_dir.mkdir()
    result = cascade_step_1(target_dir, reg)
    assert result.schema is None
    assert result.step == "no-match"


def test_discover_schema_calls_step_1(tmp_path: Path) -> None:
    schemas_dir = tmp_path / "schemas"
    schemas_dir.mkdir()
    (schemas_dir / "[idea].md").write_text("---\nname: idea\n---\n")
    reg = load_schemas_from_dir(schemas_dir)
    target_dir = tmp_path / "idea"
    target_dir.mkdir()
    result = discover_schema(target_dir, reg)
    assert result.step == "bracket"
    assert result.schema is not None
