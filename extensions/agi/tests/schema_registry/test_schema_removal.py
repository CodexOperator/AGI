"""T-020 tests: schema removal + generic fallback (schema-registry/R1.3)."""

import warnings
from pathlib import Path

import pytest

from schema_registry import load_schemas_from_dir
from schema_registry.loader import GENERIC_SCHEMA_NAME, reload_schemas


def _seed(tmp: Path, names: list[str]) -> None:
    for n in names:
        (tmp / f"{n}.md").write_text(f"---\nname: {n}\nfields:\n  title:\n    type: string\n---\n\n{n}\n")


def test_resolve_falls_back_to_generic_when_missing(tmp_path: Path) -> None:
    """R1.3: nodes referencing a missing schema get the generic fallback + 1 warning."""
    _seed(tmp_path, ["idea", "hypothesis"])
    reg = load_schemas_from_dir(tmp_path)
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        s1 = reg.resolve("nonexistent")
        s2 = reg.resolve("nonexistent")  # second call — must NOT re-warn
    assert s1.name == GENERIC_SCHEMA_NAME
    assert s2.name == GENERIC_SCHEMA_NAME
    user_warnings = [item for item in w if issubclass(item.category, UserWarning)]
    assert len(user_warnings) == 1, "warning should be emitted exactly once per missing name"
    assert "nonexistent" in str(user_warnings[0].message)


def test_reload_after_removal_warns_once_per_missing(tmp_path: Path) -> None:
    """R1.3: after removing a previously-loaded schema, reload emits a single warning."""
    _seed(tmp_path, ["idea", "hypothesis"])
    reg1 = load_schemas_from_dir(tmp_path)
    assert "hypothesis" in reg1.names()
    # Remove hypothesis schema file
    (tmp_path / "hypothesis.md").unlink()
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        reg2 = reload_schemas(tmp_path, previous=reg1)
    assert "hypothesis" not in reg2.names()
    assert "hypothesis" in reg2.missing_warned
    user_warnings = [item for item in w if issubclass(item.category, UserWarning)]
    msgs = [str(x.message) for x in user_warnings]
    assert any("hypothesis" in m for m in msgs)


def test_carries_forward_warned_set(tmp_path: Path) -> None:
    """Warned-set survives reload so we don't spam logs."""
    _seed(tmp_path, ["idea"])
    reg1 = load_schemas_from_dir(tmp_path)
    # Trigger a warning by resolving a missing type
    with warnings.catch_warnings(record=True):
        warnings.simplefilter("always")
        reg1.resolve("ghost")
    assert "ghost" in reg1.missing_warned
    reg2 = reload_schemas(tmp_path, previous=reg1)
    assert "ghost" in reg2.missing_warned


def test_generic_fallback_is_active_and_empty_fields(tmp_path: Path) -> None:
    reg = load_schemas_from_dir(tmp_path)  # empty dir
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        gen = reg.resolve("anything")
    assert gen.name == GENERIC_SCHEMA_NAME
    assert gen.active is True
    assert gen.fields == {}
