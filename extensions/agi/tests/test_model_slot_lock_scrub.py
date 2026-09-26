"""A spawned round never inherits a model-slot lock override.

hypothesis:a-spawned-round-never-inherits-a-model-slot-lock-override --
`AGI_MODEL_SLOT_LOCK` is model_slot.py's test seam for lock_path(). Inherited
silently, it would move every spawned parent AND kid OFF the box-wide flock the
memory guard relies on. The explicit `--lock` flag is untouched: a deliberate
test still has its seam, in argv where it is visible.
"""
import importlib.util
import json
import os
from pathlib import Path

BIN = Path(__file__).resolve().parents[1] / "bin"
CTX = Path(__file__).resolve().parents[3] / ".agi" / "context" / "local-maxxing"


def _dispatch():
    spec = importlib.util.spec_from_file_location("d_scrub", BIN / "dispatch.py")
    d = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(d)
    return d


def _model_slot():
    spec = importlib.util.spec_from_file_location("ms_scrub", CTX / "model_slot.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def test_a_spawned_round_inherits_no_model_slot_lock_override(monkeypatch):
    monkeypatch.setenv("AGI_MODEL_SLOT_LOCK", "/tmp/a-squatted-lock")
    env = _dispatch().scrubbed_env()
    assert "AGI_MODEL_SLOT_LOCK" not in env
    assert "/tmp/a-squatted-lock" not in json.dumps(env)
    # a sibling key must still survive -- the scrub is narrow
    monkeypatch.setenv("AGI_ROUNDS", "3")
    assert _dispatch().scrubbed_env().get("AGI_ROUNDS") == "3"


def test_no_injection_means_the_production_cell_still(monkeypatch):
    monkeypatch.delenv("AGI_MODEL_SLOT_LOCK", raising=False)
    m = _model_slot()
    m.lock_path.injected = None
    try:
        rel = json.load(open(m.paths.config_path()))[
            "paths"]["local_maxxing"]["model_slot_lock"]
        assert m.lock_path() == os.path.join(m.paths.main_checkout_root(), rel)
    finally:
        m.lock_path.injected = None
