"""goal:g7.16.1.2.1 · hypothesis:rotation-records-carry-home-relative-paths-one-resolver.

The writer half, pinned through the existing `_write_rotation_record` (no new
interface): a record whose paths sit under HOME is written `~`-relative, so the
committed record never carries the box user's home path. A tmp graph and a
tmp HOME only; no live pane, seat or record is touched. RED on the trunk at
ef73dec71 (council bundle 2, director-general-2); green since director-general-3's
build. The reader half is `_resolve_record_path`, pinned below.
"""
from __future__ import annotations

import json
import subprocess
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


def _late_reap(p, raw, tmp_path, monkeypatch):
    """heal._late_reap_for_skipped's REAP write (heal.py late-reap branch):
    a registry that now holds the successor, one older chain window."""
    import heal
    monkeypatch.setattr(rotate, "_reap_chain", lambda pids, **kw: {"chain": [{"ps_before": raw}]})
    rec = {"seat": "p", "result": "skipped", "refusal_reason": "no registry file for @6",
           "handover": {"own_window": {"name": "p-S1-L4-V", "id": "@5"},
                        "successor_window": {"name": "p-S1-L4-VI", "id": "@6"}}}
    p.write_text(json.dumps(rec, indent=2) + "\n", "utf-8")
    (tmp_path / "reg").mkdir()
    (tmp_path / "reg" / "1.json").write_text('{"window_id": "@6"}', "utf-8")
    (tmp_path / "win.txt").write_text("@5 p-S1-L4-V\n@6 p-S1-L4-VI\n", "utf-8")
    out = heal._late_reap_for_skipped(tmp_path, rec, record_path=str(p), rows=[{"name": "p", "role": "director"}],
                                      window_path=str(tmp_path / "win.txt"), registry_dir=str(tmp_path / "reg"),
                                      pids_for=lambda n: [1], rot=rotate, now=1234)
    assert out["action"] == "reaped", out


def _heal_abandoned(p, raw, *_):
    import heal
    heal._close_late_reap_abandoned({}, str(p), 0.0, raw, 1.0, 2.0)


def _sensei_audit(p, raw, *_):
    import sensei
    sensei.write_audit_into_record(p, "left", {"transcript": raw})


WRITERS = {
    "rotate._record_closeout": lambda p, raw, *_: rotate._record_closeout(p, [{"step": "s", "detail": raw}]),
    "rotate._record_swept_latches": lambda p, raw, *_: rotate._record_swept_latches(p, [raw]),
    "rotate._record_s12_self_reap": lambda p, raw, *_: rotate._record_s12_self_reap(p, {"chain": [{"ps_before": raw}]}),
    "heal._close_late_reap_abandoned": _heal_abandoned,
    "heal._late_reap_for_skipped": _late_reap,
    "sensei.write_audit_into_record": _sensei_audit,
}


@pytest.mark.parametrize("writer", sorted(WRITERS))
def test_every_record_writer_writes_home_relative(tmp_path, home, monkeypatch, writer):
    """Residues 33 + 45: EACH writer outside _write_rotation_record, alone on
    its own fresh record, re-dumps through rotate._dump_record -- no HOME
    (this box's or another's) lands raw, and no later writer can mask it."""
    p, raw = _record(tmp_path, home), f"cwd={home}/p x {OTHER}w"
    WRITERS[writer](p, raw, tmp_path, monkeypatch)
    text = p.read_text("utf-8")
    assert str(home) not in text and OTHER not in text
    assert "cwd=~/p x <home>/w" in text


# --- council bundle 3 (director-general-2, stage 2) -------------------------
_ROT = Path(__file__).resolve().parents[3] / ".agi" / "sessions" / "rotations"


def _committed_record() -> bytes:
    """The first COMMITTED record, read from HEAD (council CM2: never an
    untracked working-tree file)."""
    top = _ROT.parents[2]
    ls = subprocess.run(["git", "-C", str(top), "ls-tree", "--name-only", "HEAD", ".agi/sessions/rotations/"],
                        capture_output=True, text=True)
    recs = sorted(n for n in ls.stdout.split() if n.endswith(".json") and not n.endswith("/sequence.json"))
    if ls.returncode != 0 or not recs:
        pytest.skip("no committed rotation record in this checkout")
    return subprocess.run(["git", "-C", str(top), "show", f"HEAD:{recs[0]}"],
                          capture_output=True, check=True).stdout


def test_a_committed_record_round_trips_through_todays_serializer(home):
    """H4 p1 baseline: the bytes the move must preserve, today via rotate."""
    raw = _committed_record()
    assert rotate._dump_record(json.loads(raw)).encode("utf-8") == raw


def test_a_committed_record_round_trips_through_the_shared_module(home):
    import importlib
    shared = importlib.import_module("rotation_record")
    raw = _committed_record()
    assert shared.dump_record(json.loads(raw)).encode("utf-8") == raw
    assert shared.resolve_record_path("~/p") == f"{home}/p"


@pytest.mark.parametrize("base", ["/" + "home/" + "abcdef/", "/" + "Users/" + "abcdef/"])
def test_the_seating_announcement_carries_a_home_relative_transcript(home, base):
    text = rotate._compose_seating_announcement(seat="probe", transcript_path=base + "p/t.jsonl")
    assert base not in text and "transcript: <home>/p/t.jsonl |" in text


# --- bundle 4 W3 B3 (director-general-2) ------------------------------------
# hypothesis:node-search-lives-beside-node-writer (goal:g4.18.7.2), CLAIM (3).
@pytest.mark.xfail(strict=True, reason="bundle 4 W3 B3: RED until DG3 moves the node search beside node_writer")
def test_b3_rotation_record_keeps_only_the_record_helpers():
    import rotation_record
    assert not {"grep_live", "parked_carriers", "GrepError"} & set(vars(rotation_record))
    assert all(callable(getattr(rotation_record, n)) for n in ("home_rel", "dump_record", "resolve_record_path"))


def test_the_sanctioned_writer_applies_the_user_root_remedy(tmp_path, monkeypatch):
    """dg6-04 residue 3, dh347 item 2: the refusal names `home_relative(text,
    root=ROOT)` for the `user` class, but the ONE writer rotate calls passed no
    root, so the remedy the guard advertises was unreachable from it. This row
    goes through the REAL caller -- rotate._write_rotation_record, the writer
    rotate/heal/sensei all share -- and drives the DEFAULT branch of
    `_cell_root`: NOTHING is stubbed, the cell read is the LIVE one, so the row
    goes red the moment the writer stops resolving from its own path."""
    import rotation_record
    monkeypatch.setenv("HOME", str(tmp_path / "h" / "me"))
    root = tmp_path / "proj"
    (root / ".agi" / "sessions").mkdir(parents=True)
    text = "basetemp " + "/" + "tmp/pytest-of-" + "fixtureuser/pytest-3"
    path = rotate._write_rotation_record(root / ".agi", {"seat": "probe", "cmd": text})
    written = json.loads(path.read_text(encoding="utf-8"))["cmd"]
    assert "fixtureuser" not in written, "the user segment survived the writer"
    assert written.endswith("<user>/pytest-3")
    assert rotation_record.dump_record({"cmd": text}) == json.dumps(
        {"cmd": written}, indent=2) + "\n"


def test_the_writer_resolves_its_own_project_once_per_record(tmp_path, monkeypatch):
    """dh347 items 2 and 3, the two halves a stub could not see. (a) From a
    DIFFERENT project's directory -- one holding its own competing cell -- the
    writer still honours the cell of the project it lives in: a CWD-derived
    root would read the other project's `anonymize` and rewrite nothing.
    (b) ONE resolution per record, not one per string leaf: two records of the
    same shape, one 8x longer, must resolve the root the SAME number of times
    (the record still reads the LIVE cell -- only the PATH lookup is cached)."""
    import anonymize, locations, rotation_record
    elsewhere = tmp_path / "elsewhere"
    (elsewhere / ".agi").mkdir(parents=True)
    (elsewhere / ".agi" / "config.json").write_text(
        json.dumps({"anonymize": {"user_roots": ["/" + "opt/other/"]}}),
        encoding="utf-8")
    # dg352 item 1: COLD before the chdir assert; and `find_project_root` answers with the `.agi` DIR, so `!= elsewhere` held for a CWD root too.
    rotation_record._CELL_ROOT.clear()
    anonymize._project.cache_clear()   # the PATH cache, cold for this row
    monkeypatch.chdir(elsewhere)
    assert Path(str(rotation_record._cell_root())).resolve() != (
        elsewhere / ".agi").resolve(), "the root came from the CWD"
    calls = []
    real = locations.find_project_root
    monkeypatch.setattr(locations, "find_project_root",
                        lambda start=None: (calls.append(start), real(start))[1])
    rotation_record.dump_record({"log": [{"cmd": "x " * 6} for _ in range(5)]})
    first = len(calls)
    assert first <= 3, "the project root was resolved %d times for one small record" % first
    rotation_record.dump_record({"log": [{"cmd": "x " * 6} for _ in range(40)]})
    assert len(calls) == first, \
        "the resolution scales with the record: %d -> %d" % (first, len(calls))


def test_a_project_less_caller_reads_no_cell(monkeypatch):
    """dg352 item 2: no project, no cell, no `user` class; the seam patched is `find_project_root`."""
    import anonymize, locations, rotation_record
    monkeypatch.setattr(locations, "find_project_root", lambda *a, **k: None)
    rotation_record._CELL_ROOT.clear()
    assert rotation_record._cell_root() is None
    hits = anonymize.scan("basetemp /" + "tmp/pytest-of-" + "fixtureuser/pytest-3",
                          [], root=None)
    assert "user" not in hits, "no project, no cell, yet user fired: %r" % (hits,)
