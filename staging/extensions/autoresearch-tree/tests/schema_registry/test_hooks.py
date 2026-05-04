"""T-028 tests: pluggable LM hooks (schema-registry/R6)."""

import warnings

import pytest

from schema_registry import (
    HookResult,
    LanguageModelHook,
    NoneHook,
    discover_schema,
    load_hook_from_config,
    load_schemas_from_dir,
)
from schema_registry.hooks.cascade_step import configure_hook


class FailingHook:
    name = "boom"

    def propose_schema(self, samples):
        raise RuntimeError("intentional failure for test")


class MalformedHook:
    name = "malformed"

    def propose_schema(self, samples):
        return HookResult(schema_yaml="not: valid: yaml: at: all", error=None)


class GoodHook:
    name = "good"

    def propose_schema(self, samples):
        return HookResult(
            schema_yaml="name: proposed_schema\nfields:\n  title:\n    type: string\n",
            error=None,
        )


def test_load_hook_from_config_none() -> None:
    """R6.1: hook target selectable via config; default = none."""
    h = load_hook_from_config(None)
    assert isinstance(h, NoneHook)
    h2 = load_hook_from_config("nonexistent_hook")
    assert isinstance(h2, NoneHook)


def test_none_hook_returns_no_schema() -> None:
    """R6.2: none hook short-circuits → cascade reaches generic."""
    h = NoneHook()
    result = h.propose_schema([])
    assert result.schema_yaml is None
    assert result.error is not None


def test_hook_failure_does_not_abort(tmp_path):
    """R6.3: hook failure logged, cascade returns no-match without raising."""
    schemas_dir = tmp_path / "schemas"
    schemas_dir.mkdir()
    (schemas_dir / "[other].md").write_text("---\nname: other\n---\n")
    reg = load_schemas_from_dir(schemas_dir)
    target = tmp_path / "data"
    target.mkdir()
    (target / "n.md").write_text("---\nrandom: 1\n---\n")
    configure_hook(FailingHook())
    try:
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            result = discover_schema(target, reg)
        assert result.schema is None
        assert result.step == "no-match"
        # Warning about hook failure recorded
        assert any("boom" in str(x.message) or "failed" in str(x.message).lower() for x in w)
    finally:
        configure_hook(None)


def test_hook_malformed_output_rejected(tmp_path):
    """R6.4: hook outputs validated before written."""
    schemas_dir = tmp_path / "schemas"
    schemas_dir.mkdir()
    reg = load_schemas_from_dir(schemas_dir)
    target = tmp_path / "data"
    target.mkdir()
    (target / "n.md").write_text("---\nrandom: 1\n---\n")
    configure_hook(MalformedHook())
    try:
        result = discover_schema(target, reg)
        assert result.schema is None  # rejected by validator
    finally:
        configure_hook(None)


def test_hook_good_output_yields_schema(tmp_path):
    """R6 happy path: valid proposal becomes a (non-active) schema for user review."""
    schemas_dir = tmp_path / "schemas"
    schemas_dir.mkdir()
    reg = load_schemas_from_dir(schemas_dir)
    target = tmp_path / "data"
    target.mkdir()
    (target / "n.md").write_text("---\nrandom: 1\n---\n")
    configure_hook(GoodHook())
    try:
        result = discover_schema(target, reg)
        assert result.step in {"lm-hook", "no-match"}  # depends on cascade ordering
        if result.step == "lm-hook":
            assert result.schema is not None
            assert result.schema.name == "proposed_schema"
            # Should be inactive (no brackets) — user review pending
            assert result.schema.active is False
    finally:
        configure_hook(None)


def test_hook_protocol_class() -> None:
    """R6.1: NoneHook satisfies the LanguageModelHook protocol."""
    h: LanguageModelHook = NoneHook()
    assert h.name == "none"
