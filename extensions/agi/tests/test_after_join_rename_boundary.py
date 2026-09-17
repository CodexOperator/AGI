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


def test_boundary_candidates_license_prev_only_from_the_records_own_fact():
    """L5.15 (3): the renamed target is ALWAYS the first candidate; `<new>.prev`
    is a candidate ONLY when the record's OWN bytes name it the successor.
    Step (2) of the boundary carries the PREDECESSOR's window aside to
    `<new>.prev`, so an unlicensed `.prev` could only join the predecessor."""
    rec = {"applied_rename": {"old": "sextest", "new": "sextest-new"}}
    assert rotate._rename_boundary_names("sextest", rec) == ["sextest-new"]
    # rotate-self shape: handover.successor_window.name licenses it.
    named = dict(rec, handover={"successor_window":
                                {"name": "sextest-new.prev"}})
    assert rotate._rename_boundary_names("sextest", named) == [
        "sextest-new", "sextest-new.prev"]
    # crash-recovery shape: the same fact sits at the TOP level.
    top = _rename_rec("sextest", "sextest-new",
                      successor_window={"name": "sextest-new.prev"})
    assert rotate._rename_boundary_names("sextest", top) == [
        "sextest-new", "sextest-new.prev"]
    # a DIFFERENT successor name does not license `.prev`
    other = dict(rec, handover={"successor_window":
                                {"name": "sextest-new"}})
    assert rotate._rename_boundary_names("sextest", other) == [
        "sextest-new"]
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


def _rename_rec(old, new, **extra):
    return {"result": "success", "gen_after": 2,
            "recorded_at": "2000-01-01T00:00:00.000Z",
            "applied_rename": {"old": old, "new": new}, **extra}


def test_latest_record_falls_back_to_the_records_own_rename_fact(tmp_path):
    """L5.15 (2): the boundary names the record `<NEW>.<stamp>.json`, so a
    `<seat>.*.json` glob misses. The record's OWN `applied_rename.old` makes it
    discoverable from the OLD row seat -- and only from that seat."""
    rd = rotate._rotations_dir(tmp_path)
    rd.mkdir(parents=True)
    (rd / "sextest-new.20260101T000000Z.json").write_text(
        json.dumps(_rename_rec("sextest", "sextest-new")), encoding="utf-8")
    pair = rotate._latest_rotate_record(tmp_path, "sextest")
    assert pair is not None, "rename-boundary record is not discoverable"
    assert pair[1].name == "sextest-new.20260101T000000Z.json"
    # NEGATIVE: a foreign seat neither owns the record nor joins it.
    assert rotate._latest_rotate_record(tmp_path, "otherseat") is None
    # NEGATIVE: a no-rename record is not claimed by any old name.
    (rd / "plain.20260101T000000Z.json").write_text(
        json.dumps({"result": "success"}), encoding="utf-8")
    assert rotate._latest_rotate_record(tmp_path, "plain") is not None
    assert rotate._latest_rotate_record(tmp_path, "ghost") is None


def test_named_record_still_wins_over_the_rename_fallback(tmp_path):
    """A seat with its own `<seat>.*.json` record resolves exactly as before --
    the fallback never runs."""
    rd = rotate._rotations_dir(tmp_path)
    rd.mkdir(parents=True)
    (rd / "sextest.20250101T000000Z.json").write_text(
        json.dumps({"result": "success", "gen_after": 1}), encoding="utf-8")
    # A LATER rename record for the same old seat must not shadow the name hit.
    (rd / "sextest-new.20270101T000000Z.json").write_text(
        json.dumps(_rename_rec("sextest", "sextest-new")), encoding="utf-8")
    pair = rotate._latest_rotate_record(tmp_path, "sextest")
    assert pair is not None and pair[1].name == "sextest.20250101T000000Z.json"


def test_unaccepted_rename_record_is_not_returned_by_the_fallback(tmp_path):
    """The fallback inherits the acceptance rules: a `failed` rotation is not
    a rotation that happened, so it is not the after_join's record."""
    rd = rotate._rotations_dir(tmp_path)
    rd.mkdir(parents=True)
    rec = _rename_rec("sextest", "sextest-new")
    rec["result"] = "failed"
    (rd / "sextest-new.20260101T000000Z.json").write_text(
        json.dumps(rec), encoding="utf-8")
    assert rotate._latest_rotate_record(tmp_path, "sextest") is None


def test_run_after_join_for_seat_joins_the_renamed_window(
        tmp_path, monkeypatch):
    """WIRE PROOF: the watch path is handed the OLD seat name (the row's) and
    the record's `applied_rename`; the join keys on the live renamed window's
    @id and the template `{succ_name}` grep names the renamed target."""
    rec = _rename_rec("sextest", "sextest-new")
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


def test_wire_join_resolves_the_boundary_record_from_disk(
        tmp_path, monkeypatch):
    """END-TO-END WIRE PROOF (L5.15). A temp root holding ONLY
    `rotations/<NEW>.<stamp>.json`; the REAL `_latest_rotate_record` (no
    monkeypatch of discovery) must find it from the OLD row seat and the join
    must resolve to the renamed window's @id with `succ_name` the NEW name.
    FAILS on the pre-fix bytes, where the lookup returns None."""
    rd = rotate._rotations_dir(tmp_path)
    rd.mkdir(parents=True)
    (rd / "sextest-new.20260101T000000Z.json").write_text(
        json.dumps(_rename_rec("sextest", "sextest-new")), encoding="utf-8")
    win = _win(tmp_path, ["@7 sextest-new", "@9 sextest-new.prev"])
    seen = {}

    def fake_join(*, root, seat, window_id, **kw):
        seen["window_id"] = window_id
        return {"found": True, "window_id": window_id, "pid": 4242,
                "session_id": "sess", "transcript": "/tmp/t.jsonl",
                "name": "sextest-new", "path": "/tmp/r.json", "note": "live"}

    captured = []
    tmpl = {"startup": {"after_join": [{"label": "join",
            "cmd": "tmux list-windows | grep {succ_name}"}],
            "after_join_delay_s": 0}}
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
    assert out is not None, "boundary record not discovered from the OLD seat"
    assert seen["window_id"] == "@7", seen
    assert captured and captured[-1]["values"]["succ_name"] == "sextest-new", \
        captured


def _drive_watch(tmp_path, monkeypatch, win, rec, seen, captured, tmpl_cmd):
    rd = rotate._rotations_dir(tmp_path)
    rd.mkdir(parents=True)
    (rd / "sextest-new.20260101T000000Z.json").write_text(
        json.dumps(rec), encoding="utf-8")

    def fake_join(*, root, seat, window_id, **kw):
        seen.setdefault("calls", []).append(window_id)
        if not window_id:
            return {"found": False, "window_id": window_id,
                    "note": "no successor window @id captured "
                            "(window_id empty)"}
        seen["window_id"] = window_id
        return {"found": True, "window_id": window_id, "pid": 4242,
                "session_id": "sess", "transcript": "/tmp/t.jsonl",
                "name": "sextest-new", "path": "/tmp/r.json",
                "note": "live"}

    tmpl = {"startup": {"after_join": [{"label": "join",
            "cmd": tmpl_cmd}], "after_join_delay_s": 0}}
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
    return rotate.run_after_join_for_seat(
        tmp_path, "sextest", performer="watch",
        tmux_session="t", window_path=str(win))


def test_prev_only_window_is_refused_when_the_record_does_not_name_it(
        tmp_path, monkeypatch):
    """SAFE CASE (L5.15). With `.prev` the ONLY live window and a boundary
    record whose own bytes do NOT name it the successor, NO @id is fabricated
    and the predecessor is NEVER joined as the successor: the unlicensed
    `.prev` is not a candidate, so the join stays unresolved and takes the
    existing NAMED refusal path. This REPLACES the old test that asserted the
    predecessor-window join."""
    seen, captured = {}, []
    win = _win(tmp_path, ["@9 sextest-new.prev"])
    rec = _rename_rec("sextest", "sextest-new")
    out = _drive_watch(tmp_path, monkeypatch, win, rec, seen, captured,
                       "grep {succ_name}")
    # no alias resolved: `_join_successor` never saw a window @id.
    assert seen.get("calls", []) == [], seen
    assert "window_id" not in seen, seen
    assert out is not None
    vals = captured[-1]["values"]
    assert vals["pid"] is None and vals["session_id"] is None, vals
    # the refusal is the existing NAMED one, not a silent miss.
    assert captured[-1]["join_unresolved_wait_s"] is not None, captured[-1]
    miss = rotate._join_successor(
        root=tmp_path, seat="sextest", window_id=None,
        registry_dir=str(tmp_path / "reg"), poll_secs=0)
    assert miss["found"] is False and "window_id empty" in miss["note"]


def test_prev_only_window_resolves_when_the_record_names_it_successor(
        tmp_path, monkeypatch):
    """SAFE CASE (L5.15). When the record's OWN bytes name `<new>.prev` the
    successor (handover.successor_window.name), it IS a candidate and the
    join resolves @9 through the discovered boundary record."""
    seen, captured = {}, []
    win = _win(tmp_path, ["@9 sextest-new.prev"])
    rec = _rename_rec("sextest", "sextest-new",
                      handover={"successor_window":
                                {"name": "sextest-new.prev"}})
    out = _drive_watch(tmp_path, monkeypatch, win, rec, seen, captured,
                       "grep {succ_name}")
    assert out is not None
    assert seen["window_id"] == "@9", seen
    assert captured and captured[-1]["values"]["succ_name"] == "sextest-new"
