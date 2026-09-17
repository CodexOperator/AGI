# test_after_join_rename_boundary.py -- L5.15:
# hypothesis:l5-after-join-greps-the-old-post-name-at-a-rename-boundary.
# At a rotation boundary that also renames the post, the watch loop discovers
# seats by the seats ROW (which the boundary never renames) and so asks for the
# OLD name; the live successor window answers only to the NEW name (and the
# own window was carried aside to `<new>.prev`). The after_join `join` then
# misses, the join stays unresolved and the pin refuses. These tests prove the
# OLD bytes miss, that the record's OWN `applied_rename` fact resolves the
# renamed window's @id (never a guess), and that a genuine no-window case still
# refuses by name with no fabricated @id.
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from agi.bin import rotate  # noqa: E402


def _win(tmp_path, lines):
    p = tmp_path / "windows.txt"
    p.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return p


def test_boundary_candidates_are_the_new_name_then_its_prev():
    rec = {"applied_rename": {"old": "sextest", "new": "sextest-new"}}
    assert rotate._rename_boundary_names("sextest", rec) == [
        "sextest-new", "sextest-new.prev"]
    # no record fact -> no candidates (never a guessed name)
    assert rotate._rename_boundary_names("sextest", {}) == []
    # old == new is not a rename
    assert rotate._rename_boundary_names(
        "s", {"applied_rename": {"old": "s", "new": "s"}}) == []


def test_old_bytes_miss_the_renamed_window(tmp_path):
    win = _win(tmp_path, ["@7 sextest-new", "@8 sextest-new.prev"])
    # BEFORE: the pre-fix bytes resolve by the pre-rename name only -> None.
    assert rotate._successor_window_id("sextest", "t", str(win)) is None
    # AFTER: the renamed target resolves, and the alias list resolves it off
    # the pre-rename seat name with the renamed target preferred.
    assert rotate._successor_window_id("sextest-new", "t", str(win)) == "@7"
    assert rotate._successor_window_id(
        "sextest", "t", str(win),
        aliases=["sextest-new", "sextest-new.prev"]) == "@7"


def test_prev_window_is_the_fallback_when_only_it_is_live(tmp_path):
    win = _win(tmp_path, ["@9 sextest-new.prev"])
    assert rotate._successor_window_id(
        "sextest", "t", str(win),
        aliases=["sextest-new", "sextest-new.prev"]) == "@9"


def test_no_live_candidate_fabricates_no_id_and_names_the_miss(tmp_path):
    win = _win(tmp_path, ["@1 unrelated"])
    assert rotate._successor_window_id(
        "sextest", "t", str(win),
        aliases=["sextest-new", "sextest-new.prev"]) is None
    out = rotate._join_successor(
        root=tmp_path, seat="sextest", window_id=None,
        registry_dir=str(tmp_path / "reg"), poll_secs=0)
    assert out["found"] is False
    assert "window_id empty" in out["note"], out


def test_run_after_join_for_seat_joins_the_renamed_window(
        tmp_path, monkeypatch):
    """WIRE PROOF: the watch path is handed the OLD seat name (the row's) and
    the record's `applied_rename`; the join keys on the live renamed window's
    @id and the template `{succ_name}` grep names the renamed target."""
    rec = {"result": "success", "gen_after": 2,
           "recorded_at": "2000-01-01T00:00:00.000Z",
           "applied_rename": {"old": "sextest", "new": "sextest-new"}}
    rec_path = tmp_path / "rec.json"
    rec_path.write_text(json.dumps(rec), encoding="utf-8")
    win = _win(tmp_path, ["@7 sextest-new"])
    seen = {}

    def fake_join(*, root, seat, window_id, **kw):
        seen["window_id"] = window_id
        seen["seat"] = seat
        return {"found": True, "window_id": window_id, "pid": 4242,
                "session_id": "sess", "transcript": "/tmp/t.jsonl",
                "name": "sextest-new", "path": "/tmp/r.json", "note": "live"}

    captured = []
    tmpl = {"startup": {"after_join": [{"label": "join",
            "cmd": "tmux list-windows | grep {succ_name}"}],
            "after_join_delay_s": 0}}
    monkeypatch.setattr(
        rotate, "_latest_rotate_record",
        lambda root, seat: (json.loads(rec_path.read_text()), rec_path))
    monkeypatch.setattr(rotate, "_find_seat",
                        lambda root, name: {"role": "director", "pid": 1,
                                            "session_ref": "row-ref"})
    monkeypatch.setattr(
        rotate, "_resolve_template",
        lambda root, role, explicit=None, **kw: (tmpl, "director", "test"))
    monkeypatch.setattr(rotate, "_join_successor", fake_join)
    monkeypatch.setattr(
        rotate, "run_after_join",
        lambda *a, **kw: (captured.append(kw) or {
            "delay_s": 0, "results": [], "dm": "", "appended": True,
            "sent": True, "record_path": kw.get("record_path")}))
    out = rotate.run_after_join_for_seat(
        tmp_path, "sextest", performer="watch",
        tmux_session="t", window_path=str(win))
    assert out is not None
    assert seen["window_id"] == "@7", seen
    assert captured and captured[-1]["values"]["succ_name"] == "sextest-new", \
        captured
