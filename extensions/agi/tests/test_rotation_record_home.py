"""goal:g7.16.1.2.1 · hypothesis:rotation-records-carry-home-relative-paths-one-resolver.

The writer half, pinned through the existing `_write_rotation_record` (no new
interface): a record whose paths sit under HOME is written `~`-relative, so the
committed record never carries the box user's home path. A tmp graph and a
tmp HOME only; no live pane, seat or record is touched. RED on the trunk at
82d64ffe7 (council bundle 2, director-general-2); green since director-general-3's
build. The reader half is `_resolve_record_path`, pinned below.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "bin"))
import rotate  # noqa: E402

#: another box's home, joined at runtime: no literal home path is committed (R1 residue 36)
OTHER = "/" + "home/" + "abcdef" + "/"


def test_a_rotation_record_is_written_home_relative(tmp_path, monkeypatch):
    home = tmp_path / "home" / "someuser"
    (home / "proj").mkdir(parents=True)
    monkeypatch.setenv("HOME", str(home))
    root = tmp_path / ".agi"
    (root / "sessions").mkdir(parents=True)
    record = {"seat": "probe", "handover": {"join": {
        "transcript": str(home / "proj" / "t.jsonl"), "path": str(home / "proj")}},
        "after_join": {"results": [{"cmd": f"python3 x --session-log {home}/proj/t.jsonl"}]}}
    path = rotate._write_rotation_record(root, record)
    text = path.read_text(encoding="utf-8")
    assert str(home) not in text
    assert json.loads(text)["handover"]["join"]["transcript"] == "~/proj/t.jsonl"


def test_another_boxs_home_is_written_placeholder(tmp_path, monkeypatch):
    """Re-homed records carry ANOTHER box's home: it becomes `<home>/`."""
    monkeypatch.setenv("HOME", str(tmp_path / "h" / "me"))
    root = tmp_path / ".agi"
    (root / "sessions").mkdir(parents=True)
    path = rotate._write_rotation_record(root, {"seat": "probe", "ps": f"cwd={OTHER}w x"})
    assert json.loads(path.read_text(encoding="utf-8"))["ps"] == "cwd=<home>/w x"


def test_the_one_resolver_expands_tilde_and_passes_the_absolute_form(tmp_path, monkeypatch):
    home = tmp_path / "home" / "someuser"
    monkeypatch.setenv("HOME", str(home))
    assert rotate._resolve_record_path("~/proj/t.jsonl") == f"{home}/proj/t.jsonl"
    assert rotate._resolve_record_path(f"{home}/proj/t.jsonl") == f"{home}/proj/t.jsonl"
    assert rotate._resolve_record_path(None) == ""


# --- bundle 2 R1 residues 32-34 (sanctuary-master mur wf_8da5e93a-72f) ------
@pytest.fixture
def home(tmp_path, monkeypatch):
    h = tmp_path / "home" / "someuser"
    (h / "p").mkdir(parents=True)
    monkeypatch.setenv("HOME", str(h))
    return h


def test_a_tilde_record_resolves_to_a_transcript_that_exists(home):
    """Residues 32 + 34: rotate._record_join AND sensei._record_transcript read
    the ~-form through the ONE resolver, to a file that EXISTS."""
    import sensei
    (home / "p" / "t.jsonl").touch()
    rec = {"transcript_path": "~/p/other.jsonl",
           "handover": {"join": {"transcript": "~/p/t.jsonl"}}}
    assert Path(rotate._record_join(rec)["transcript"]).exists()
    assert sensei._record_transcript(rec).exists()


def _record(tmp_path, home, extra=None) -> Path:
    p = tmp_path / "r.json"
    p.write_text(json.dumps({"seat": "p", "result": "ok", **(extra or {})}, indent=2) + "\n", "utf-8")
    return p


@pytest.mark.parametrize("family", ["rotate", "heal", "sensei"])
def test_every_record_writer_family_writes_home_relative(tmp_path, home, family):
    """Residue 33: the writers outside _write_rotation_record re-dump through
    rotate._dump_record, so no HOME (this box's or another's) lands raw."""
    p, raw = _record(tmp_path, home), f"cwd={home}/p x {OTHER}w"
    if family == "rotate":
        rotate._record_closeout(p, [{"step": "s", "detail": raw}])
        rotate._record_swept_latches(p, [raw])
        rotate._record_s12_self_reap(p, {"chain": [{"ps_before": raw}]})
    elif family == "heal":
        import heal
        heal._close_late_reap_abandoned({}, str(p), 0.0, raw, 1.0, 2.0)
    else:
        import sensei
        sensei.write_audit_into_record(p, "left", {"transcript": raw})
    text = p.read_text("utf-8")
    assert str(home) not in text and OTHER not in text
    assert "cwd=~/p x <home>/w" in text
