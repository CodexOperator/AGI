"""model_fence's cap cell fails CLOSED, never at import (TMM.256).

`_cap_from_config` indexed `["values"]["core"][...]` on the nearest config, so a
tree whose config.json lacks the cell raised KeyError at IMPORT -- every context
test in that tree errored at collection, though the docstring promised cap 0.
"""
import importlib.util
import json
import shutil
from pathlib import Path

import pytest

FENCE = Path(__file__).resolve().parents[1] / "model_fence.py"


def _load_in(tree: Path, cfg, monkeypatch):
    """Import a COPY of model_fence.py that lives under `tree`, whose nearest
    config is `cfg` (a dict, raw text, or None for no config at all)."""
    monkeypatch.delenv("AGI_MODEL_FENCE_MAX_BYTES", raising=False)
    dst = tree / "extensions" / "agi" / "model_fence.py"
    dst.parent.mkdir(parents=True)
    shutil.copy(FENCE, dst)
    if cfg is not None:
        (tree / ".agi").mkdir()
        (tree / ".agi" / "config.json").write_text(
            cfg if isinstance(cfg, str) else json.dumps(cfg))
    spec = importlib.util.spec_from_file_location(f"mf_{tree.name}", dst)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@pytest.mark.parametrize("cfg", [
    {"values": {"local_maxxing": {}}},     # the cell's section is absent
    {"paths": {}},                         # no values at all
    "{not json",                           # unparseable
    {"values": {"core": {"model_load_allowed_max_bytes": "64MiB"}}},  # not a number
])
def test_a_config_without_a_usable_cell_is_cap_zero_not_an_import_error(
        tmp_path, cfg, monkeypatch):
    assert _load_in(tmp_path / "t", cfg, monkeypatch).MAX_ALLOWED_LOAD_BYTES == 0


def test_the_declared_cell_is_still_read(tmp_path, monkeypatch):
    cfg = {"values": {"core": {"model_load_allowed_max_bytes": 1234}}}
    assert _load_in(tmp_path / "t", cfg, monkeypatch).MAX_ALLOWED_LOAD_BYTES == 1234


def test_the_refusal_names_the_sanctioned_path(tmp_path, monkeypatch):
    mod = _load_in(tmp_path / "t", {"paths": {}}, monkeypatch)
    why = mod._why("transformers", "from_pretrained")
    assert "model_slot.py" in why and "asserts on bytes" not in why
