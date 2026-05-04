"""T-021 tests: bracket convention (schema-registry/R2)."""

import shutil
from pathlib import Path

import pytest

from schema_registry import (
    DuplicateActiveSchemaError,
    build_active_set,
    load_schemas_from_dir,
)


def _seed(d: Path, files: dict[str, str]) -> None:
    d.mkdir(parents=True, exist_ok=True)
    for name, fields in files.items():
        (d / name).write_text(
            f"---\nfields:\n  {fields}:\n    type: string\nname: {Path(name).stem.strip('[]')}\n---\n"
        )


def test_bracketed_is_in_active_set(tmp_path: Path) -> None:
    """R2.1: bracketed file is in active set."""
    _seed(tmp_path, {"[hypothesis].md": "title"})
    reg = load_schemas_from_dir(tmp_path)
    aset = build_active_set(reg)
    assert "hypothesis" in aset.active_names()


def test_unbracketed_is_inactive(tmp_path: Path) -> None:
    """R2.2: no brackets → loaded but inactive, excluded from auto-discovery."""
    _seed(tmp_path, {"experiment.md": "verdict"})
    reg = load_schemas_from_dir(tmp_path)
    aset = build_active_set(reg)
    assert "experiment" in aset.inactive_names()
    assert "experiment" not in aset.active_names()


def test_renaming_to_bracketed_activates(tmp_path: Path) -> None:
    """R2.3: activating == renaming to add brackets."""
    src = tmp_path / "idea.md"
    src.write_text("---\nname: idea\nfields:\n  title:\n    type: string\n---\n")
    reg1 = load_schemas_from_dir(tmp_path)
    aset1 = build_active_set(reg1)
    assert "idea" in aset1.inactive_names()
    # Rename
    new = tmp_path / "[idea].md"
    src.rename(new)
    reg2 = load_schemas_from_dir(tmp_path)
    aset2 = build_active_set(reg2)
    assert "idea" in aset2.active_names()


def test_two_bracketed_same_name_raises(tmp_path: Path) -> None:
    """R2.4: two bracketed schemas claiming same name → DuplicateActiveSchemaError naming both."""
    a = tmp_path / "[hypothesis].md"
    a.write_text("---\nname: hypothesis\n---\n")
    b = tmp_path / "subdir"
    b.mkdir()
    # Same dir, second bracketed file with same canonical name. To cleanly trigger,
    # use a single dir with both .md and .json variants:
    c = tmp_path / "[hypothesis].json"
    c.write_text('{"frontmatter": {"name": "hypothesis"}, "body": ""}')
    reg = load_schemas_from_dir(tmp_path)
    with pytest.raises(DuplicateActiveSchemaError) as exc:
        build_active_set(reg)
    assert exc.value.name == "hypothesis"
    assert len(exc.value.paths) == 2
