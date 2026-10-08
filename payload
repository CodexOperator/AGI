"""T-019 tests: schema files (schema-registry/R1)."""

import shutil
from pathlib import Path

from schema_registry import (
    Schema,
    SchemaRegistry,
    canonical_name,
    is_bracketed,
    load_schemas_from_dir,
)


FIXTURE_DIR = Path(__file__).parent.parent / "fixtures" / "schemas"


def test_load_existing_fixtures() -> None:
    """R1.1: schemas live at known path; R1.4: md+json accepted."""
    reg = load_schemas_from_dir(FIXTURE_DIR)
    names = reg.names()
    assert "experiment" in names
    assert "hypothesis" in names
    assert "idea" in names  # JSON schema also picked up
    assert len(reg.errors) == 0


def test_bracketed_means_active() -> None:
    """R2 hint (covered fully later): [hypothesis].md flags 'active'."""
    reg = load_schemas_from_dir(FIXTURE_DIR)
    hyp = reg.get("hypothesis")
    assert hyp is not None
    assert hyp.active is True
    exp = reg.get("experiment")
    assert exp is not None
    assert exp.active is False


def test_drop_in_new_schema_no_code_change(tmp_path: Path) -> None:
    """R1.2: dropping a new schema file makes it appear on next load — no restart."""
    # Copy fixtures to a tmp dir
    for src in FIXTURE_DIR.iterdir():
        shutil.copy(src, tmp_path / src.name)
    reg1 = load_schemas_from_dir(tmp_path)
    assert "newly_added" not in reg1.names()
    # Drop a brand new schema file in
    (tmp_path / "newly_added.md").write_text(
        "---\nname: newly_added\nfields:\n  title:\n    type: string\n---\nbody\n"
    )
    reg2 = load_schemas_from_dir(tmp_path)
    assert "newly_added" in reg2.names()


def test_json_schema_accepted(tmp_path: Path) -> None:
    """R1.4: pure JSON schema files load."""
    src = FIXTURE_DIR / "example.json"
    shutil.copy(src, tmp_path / "example.json")
    reg = load_schemas_from_dir(tmp_path)
    assert "idea" in reg.names()


def test_is_bracketed_helper() -> None:
    assert is_bracketed("[hypothesis]") is True
    assert is_bracketed("hypothesis") is False
    assert canonical_name("[hypothesis]") == "hypothesis"
    assert canonical_name("hypothesis") == "hypothesis"


def test_missing_dir_returns_empty_registry(tmp_path: Path) -> None:
    """Missing dir → empty registry, no error."""
    reg = load_schemas_from_dir(tmp_path / "nonexistent")
    assert len(reg.schemas) == 0
