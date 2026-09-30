"""goal:g7.16.1.7.1.3.1 -- ONE harness resolver.

`adapters.harness_block(cfg, name)` is the config.json harness read: a plain
block as itself, a pi TEMPLATE (shared cells + JSON `rows`) as its default
row, `<template>:<row>` as that row, an alias as its row. Every reader in
extensions/agi/bin goes through it, and on today's config every read is
byte-identical.
"""
import json
import re
import sys
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parents[1] / "bin"
sys.path.insert(0, str(BIN))

import adapters  # noqa: E402

TEMPLATE = {"harnesses": {
    "pi": {"adapter": "pi", "bin": "~/pi", "forward_env": ["K"],
           "rows": [
               {"name": "free", "default": True, "zero_usd": True,
                "provider": "openrouter", "models": {"kid": "m-free"}},
               {"name": "paid", "provider": "openrouter", "thinking": "medium",
                "models": {"kid": "m-paid"}},
               {"name": "local", "zero_usd": True, "provider": "town",
                "max_live": 1, "models": {"kid": "m-local"}}],
           "aliases": {"pi-free": "free", "pi-local": "local"}},
    "claude-code": {"adapter": "claude_code", "models": {"director": "c"}}}}


def test_a_template_answers_its_default_row():
    got = adapters.harness_block(TEMPLATE, "pi")
    assert got == {"adapter": "pi", "bin": "~/pi", "forward_env": ["K"],
                   "zero_usd": True, "provider": "openrouter",
                   "models": {"kid": "m-free"}, "row": "free"}


def test_a_named_row_and_an_alias_answer_their_row():
    assert adapters.harness_block(TEMPLATE, "pi:paid")["models"] == {"kid": "m-paid"}
    assert "zero_usd" not in adapters.harness_block(TEMPLATE, "pi:paid")
    assert adapters.harness_block(TEMPLATE, "pi-local")["max_live"] == 1
    assert adapters.harness_block(TEMPLATE, "pi-free")["row"] == "free"


def test_plain_blocks_and_unknown_names():
    assert adapters.harness_block(TEMPLATE, "claude-code") == \
        TEMPLATE["harnesses"]["claude-code"]
    for name in ("nope", "pi:nope", "claude-code:x", "", None):
        assert adapters.harness_block(TEMPLATE, name) == {}, name


def test_resolve_and_ids_speak_rows_and_aliases():
    assert adapters.harness_ids(TEMPLATE) == [
        "claude-code", "pi", "pi-free", "pi-local", "pi:free", "pi:local", "pi:paid"]
    name, block = adapters.resolve(TEMPLATE, "pi-local")
    assert name == "pi-local" and block["models"] == {"kid": "m-local"}
    with pytest.raises(adapters.AdapterError, match="pi:free"):
        adapters.resolve(TEMPLATE, "pi-typo")


def test_todays_config_reads_byte_identical():
    cfg = json.loads((BIN.parents[2] / ".agi" / "config.json").read_text())
    for hid, block in (cfg.get("harnesses") or {}).items():
        if "rows" not in block:
            assert adapters.harness_block(cfg, hid) == block, hid


def test_no_config_harness_read_outside_the_resolver():
    """Negative: no `get("harnesses")` on a config.json dict outside
    adapters/__init__.py (config:brief's own per-harness parts cell,
    `cell.get("harnesses")`, is a different node)."""
    hits = []
    for f in sorted(BIN.rglob("*.py")):
        if f.relative_to(BIN).as_posix() == "adapters/__init__.py":
            continue
        for n, line in enumerate(f.read_text(encoding="utf-8").splitlines(), 1):
            if re.search(r"""get\(["']harnesses["']\)""", line) and "cell.get(" not in line:
                hits.append(f"{f.name}:{n}")
    assert hits == []
