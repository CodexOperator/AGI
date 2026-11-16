"""goal:g7.16.1.11.46.37 (the owner's Q3, 11-15): an automatic hub fallback on a recorded QUOTA limit, and nothing else.

hub_move.py is the ENGINE half: it DECIDES from the host-written state and route files (the shape of goal .46.35) and says; belam's
host act applies. Rows 1-6 of the leaf's Falsifier, each with its MUTANT (a one-edit copy of hub_move.py that the row must catch);
row 7 (live) is belam's, on a scratch route. A fake state and route fixture, never a real hub: spend 0, no network, no root.

 f1 POSITIVE replay (hub B in quota, hub A's ok line DAYS older than the file's `written`): MOVE, ONE loud line with the post, the
    model, B, A, the reset, `quota` and the age of A's line; mutants: the line dropped, the age dropped, a per-line age check
 f2 NEGATIVE hub-down alone: no move; mutant: hub-down read as a trigger
 f3 NEGATIVE unread (stale / missing / malformed state or route): no move, rc 1; OFF-HUB (no route row, or `direct`): never unread,
    never moved; mutants: a stale state trusted, an off-hub post read as unread, an off-hub post moved
 f4 NEGATIVE the target hub is not ok (quota / down / no line): no move, ONE said refusal (once, not each run); mutant: a move into it
 f5 BOUND, one automatic move per post: the same cooldown again = no second move and the standing line once; a moved post that reads
    quota on its NEW hub (the other hub ok) = no move, ONE refusal naming the standing move; `clear` is the only way it moves again;
    mutants: a second move, the A -> B move on A's new cooldown, a move back after the first hub records a 200, the standing line
    repeating, the moved post's own-box line dropped
 f6 the two old no-move lines point at this leaf (the row's own grep, run on the repo's files); mutants: the old line left standing,
    a pointer missing
"""
from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[3]
BIN = ROOT / "extensions" / "agi" / "bin"
NOW = 1794774500                      # the live file's `written` on 11-15 (measured), a fixed clock
OPUS = "claude-opus-5-5"
RESET = NOW + 3600
DAYS_OLD = NOW - 193000               # hub A's last 200: days older than `written`, as measured (A opus T 1794581580)


def _state(tmp, lines, written=NOW):
    p = tmp / "state"
    p.write_text(f"written {written}\n" + "".join(l + "\n" for l in lines))
    return p


def _route(tmp, lines, written=NOW):
    p = tmp / "route"
    p.write_text(f"written {written}\n" + "".join(l + "\n" for l in lines))
    return p


B_QUOTA = f"B {OPUS} quota {RESET} {NOW - 5}"
A_OK = f"A {OPUS} ok {DAYS_OLD} {DAYS_OLD}"


def _copy(tmp, name, edit=None):
    """A bin dir with hub_move.py (edited by (old, new) when given), hub_quota.py and alarm_spool.py beside it."""
    d = tmp / name
    d.mkdir()
    for f in ("hub_quota.py", "alarm_spool.py"):
        shutil.copy(BIN / f, d / f)
    src = (BIN / "hub_move.py").read_text()
    if edit is not None:
        old, new = edit
        assert src.count(old) == 1, f"mutant anchor must match exactly once, got {src.count(old)}: {old[:60]!r}"
        src = src.replace(old, new)
    (d / "hub_move.py").write_text(src)
    return d / "hub_move.py"


def run(tmp, script=None, *, state=None, route=None, now=NOW, post=(), hubs=None, mem="mem", spool=True, said=True, extra=()):
    script = script or (BIN / "hub_move.py")
    cmd = [sys.executable, "-I", str(script), "decide", "--state", str(state or tmp / "state"), "--route", str(route or tmp / "route"),
           "--memory", str(tmp / mem), "--moves", str(tmp / "moves"), "--now", str(now)]
    if said:
        cmd += ["--said", str(tmp / "said")]
    if spool:
        cmd += ["--spool", str(tmp / "spool"), "--to", "sanctuary-master"]
    for n in post:
        cmd += ["--post", n]
    if hubs:
        cmd += ["--hubs", hubs]
    cmd += list(extra)
    return subprocess.run(cmd, capture_output=True, text=True, timeout=60)


def said(tmp):
    p = tmp / "said"
    return p.read_text().splitlines() if p.exists() else []


def spool(tmp):
    p = tmp / "spool"
    return [json.loads(l) for l in p.read_text().splitlines()] if p.exists() else []


def moves(tmp):
    p = tmp / "moves"
    return p.read_text().splitlines() if p.exists() else None


def moved_lines(tmp):
    return [l for l in said(tmp) if " -> " in l and " on quota (" in l]


def standing_lines(tmp):
    return [l for l in said(tmp) if ", moved from " in l]


# ---------- f1: the positive replay ----------
def _f1(tmp, script=None):
    _state(tmp, [A_OK, B_QUOTA])
    _route(tmp, [f"alpha B {OPUS}", f"beta A {OPUS}"])
    return run(tmp, script)


def test_f1_a_quota_post_moves_to_the_other_hub_and_says_so_once(tmp_path):
    r = _f1(tmp_path)
    assert r.returncode == 0, r.stderr
    loud = moved_lines(tmp_path)
    assert len(loud) == 1, said(tmp_path)
    line = loud[0].split(" ", 1)[1]
    assert line.startswith(f"post alpha ({OPUS}) DECIDED B -> A on quota (B until ")
    assert re.search(r"A ok as of \d\d-\d\d \d\d:\d\dZ, unconfirmed since$", line), line      # the AGE of the target line it trusted
    assert "11-13 14:51Z" in line                                                           # A's T, days before `written` (11-15 20:28Z)
    assert [l.split(" ", 1)[1] for l in standing_lines(tmp_path)] == ["post alpha decided onto hub A at 20:28Z, moved from B on quota, pending the host step"]
    assert moves(tmp_path) == [f"alpha A {OPUS}"]                                          # beta (on A, ok) is untouched
    sp = spool(tmp_path)
    assert [(s["to"], s["text"].startswith("[quota] post alpha")) for s in sp if s["to"] == "sanctuary-master"] == [("sanctuary-master", True)]
    assert len([s for s in sp if s["to"] == "alpha"]) == 1                                 # the moved post's OWN-box line


@pytest.mark.parametrize("name, edit", [
    ("line-dropped", ('out["said"].append((loud, True, aid(*did, kind="loud")))', "pass")),
    ("age-dropped", ('f"{other} ok as of {asof}, unconfirmed since")', 'f"{other}")')),
    ("per-line-age", ('        why = target_state(state, other, model)\n',
                      '        why = target_state(state, other, model)\n        if why == "ok" and now - state[(other, model)][1] > 180:\n            why = "stale"\n')),
])
def test_f1m_mutant_is_red(tmp_path, name, edit):
    r = _f1(tmp_path, _copy(tmp_path, "m", edit))
    loud = [l for l in moved_lines(tmp_path)]
    ok = (len(loud) == 1 and re.search(r"A ok as of \d\d-\d\d \d\d:\d\dZ, unconfirmed since$", loud[0]) is not None and r.returncode == 0)
    assert not ok, f"mutant {name} still reads green: {said(tmp_path)}"


# ---------- f2: hub-down alone never moves ----------
def _f2(tmp, script=None):
    _state(tmp, [A_OK, f"B - hub-down {NOW - 600} {NOW - 5}"])
    _route(tmp, [f"alpha B {OPUS}"])
    return run(tmp, script)


def test_f2_hub_down_alone_is_no_move(tmp_path):
    r = _f2(tmp_path)
    assert r.returncode == 0 and moved_lines(tmp_path) == [] and moves(tmp_path) == []
    assert "0 moved" in r.stdout


def test_f2m_mutant_hub_down_as_a_trigger_is_red(tmp_path):
    _f2(tmp_path, _copy(tmp_path, "m", ('return st if st is not None and st[0] == "quota" else None',
                                         'return st if st is not None and st[0] == "quota" else state.get((hub, "-"))')))
    assert moved_lines(tmp_path) != [], "the mutant moved nothing on hub-down: the row would not notice a hub-down trigger"


# ---------- f3: unread, and off-hub ----------
def test_f3_a_stale_or_malformed_or_missing_file_is_unread_and_moves_nothing(tmp_path):
    _route(tmp_path, [f"alpha B {OPUS}"])
    _state(tmp_path, [A_OK, B_QUOTA], written=NOW - 181)                                    # stale: 181 s >= 180
    r = run(tmp_path)
    assert r.returncode == 1 and "unread" in r.stderr and said(tmp_path) == [] and moves(tmp_path) is None
    _state(tmp_path, [A_OK, "B garbage"])                                                   # malformed state line
    assert run(tmp_path).returncode == 1
    _state(tmp_path, [A_OK, B_QUOTA])
    _route(tmp_path, [f"alpha B {OPUS}"], written=NOW - 500)                                # a stale route
    assert run(tmp_path).returncode == 1
    _route(tmp_path, ["alpha B"])                                                           # a hub route with no MODEL
    assert run(tmp_path).returncode == 1
    r = run(tmp_path, route=tmp_path / "no-such-route")                                     # a missing route
    assert r.returncode == 1 and said(tmp_path) == [] and moves(tmp_path) is None


def test_f3m_mutant_a_stale_state_trusted_is_red(tmp_path):
    _route(tmp_path, [f"alpha B {OPUS}"])
    _state(tmp_path, [A_OK, B_QUOTA], written=NOW - 5000)
    r = run(tmp_path, _copy(tmp_path, "m", ("state = hub_quota.read_state(a.state, now, a.max_age)", "state = hub_quota.read_state(a.state, now, 10**12)")))
    assert r.returncode == 0 and moved_lines(tmp_path) != [], "the mutant must move on a stale state (and the real one must not)"


def _f3_off(tmp, script=None):
    _state(tmp, [A_OK, B_QUOTA])
    _route(tmp, [f"alpha B {OPUS}", "gamma direct"])
    return run(tmp, script, post=["belam"])


def test_f3_off_hub_posts_are_never_unread_and_never_moved(tmp_path):
    r = _f3_off(tmp_path)
    assert r.returncode == 0, r.stderr
    assert "belam: off-hub, no move" in r.stdout and "gamma: off-hub (direct), no move" in r.stdout
    assert [l.split(" ", 2)[2].split(" ")[0] for l in moved_lines(tmp_path)] == ["alpha"]   # only alpha moved


def test_f3m_mutant_off_hub_read_as_unread_is_red(tmp_path):
    r = _f3_off(tmp_path, _copy(tmp_path, "m", ('print(f"{name}: off-hub, no move")', 'print(f"{name}: unread"); return 1')))
    assert r.returncode == 1


def test_f3m2_mutant_off_hub_moved_is_red(tmp_path):
    r = _f3_off(tmp_path, _copy(tmp_path, "m", ("        if hm is None:\n", "        if hm is None and False:\n")))
    assert r.returncode != 0 or "gamma" in " ".join(moved_lines(tmp_path))


# ---------- f4: the target hub must be ok ----------
@pytest.mark.parametrize("why, lines", [
    ("quota", [f"A {OPUS} quota {RESET} {NOW - 9}", B_QUOTA]),
    ("hub-down", [f"A - hub-down {NOW - 900} {NOW - 5}", A_OK, B_QUOTA]),
    ("no-line", [B_QUOTA]),
])
def test_f4_a_target_that_is_not_ok_is_no_move_with_one_said_refusal(tmp_path, why, lines):
    _state(tmp_path, lines)
    _route(tmp_path, [f"alpha B {OPUS}", f"delta B {OPUS}"])
    r = run(tmp_path)
    assert r.returncode == 0 and moved_lines(tmp_path) == [] and moves(tmp_path) == []
    ref = [l for l in said(tmp_path) if "no move for alpha, delta" in l]
    assert len(ref) == 1, said(tmp_path)
    run(tmp_path, now=NOW + 60)                                                              # the next run: said ONCE, not each run
    assert len([l for l in said(tmp_path) if "no move for" in l]) == 1


def test_f4m_mutant_a_move_into_a_hub_in_quota_is_red(tmp_path):
    _state(tmp_path, [f"A {OPUS} quota {RESET} {NOW - 9}", B_QUOTA])
    _route(tmp_path, [f"alpha B {OPUS}"])
    run(tmp_path, _copy(tmp_path, "m", ('        if why != "ok":\n', "        if False:\n")))
    assert moved_lines(tmp_path) != [], "the mutant must move into a hub in quota"


# ---------- f5: the bound ----------
def _moved_once(tmp, script=None):
    _state(tmp, [A_OK, B_QUOTA])
    _route(tmp, [f"alpha B {OPUS}"])
    return run(tmp, script)


def test_f5_the_same_cooldown_again_is_no_second_move_and_the_standing_line_is_written_once(tmp_path):
    _moved_once(tmp_path)
    for k in (1, 2):                                                                         # the host has not applied it yet: the route still reads B
        r = run(tmp_path, now=NOW + 60 * k)
        assert r.returncode == 0 and "0 moved" in r.stdout
    assert len(moved_lines(tmp_path)) == 1 and len(standing_lines(tmp_path)) == 1 and moves(tmp_path) == [f"alpha A {OPUS}"]


def _on_a_quota_while_b_ok(tmp):
    _state(tmp, [f"A {OPUS} quota {RESET + 7200} {NOW + 100}", f"B {OPUS} ok {NOW + 90} {NOW + 90}"], written=NOW + 100)
    _route(tmp, [f"alpha A {OPUS}"], written=NOW + 100)                                      # the host applied the move: alpha is on A


def test_f5_a_moved_post_that_reads_quota_on_its_new_hub_is_not_moved_back(tmp_path):
    _moved_once(tmp_path)
    _on_a_quota_while_b_ok(tmp_path)
    r = run(tmp_path, now=NOW + 100)
    assert r.returncode == 0 and len(moved_lines(tmp_path)) == 1 and moves(tmp_path) == [f"alpha A {OPUS}"]
    ref = [l for l in said(tmp_path) if "stays on hub A" in l]
    assert len(ref) == 1 and "moved B -> A" in ref[0] and "hub_move.py clear alpha" in ref[0]
    run(tmp_path, now=NOW + 160)
    assert len([l for l in said(tmp_path) if "stays on hub A" in l]) == 1                    # the refusal is said ONCE


def test_f5_clear_is_the_only_way_a_post_moves_again(tmp_path):
    _moved_once(tmp_path)
    c = subprocess.run([sys.executable, "-I", str(BIN / "hub_move.py"), "clear", "alpha", "--memory", str(tmp_path / "mem"),
                        "--said", str(tmp_path / "said"), "--moves", str(tmp_path / "moves"), "--now", str(NOW + 30)], capture_output=True, text=True)
    assert c.returncode == 0 and "cleared" in c.stdout and moves(tmp_path) == []
    again = subprocess.run([sys.executable, "-I", str(BIN / "hub_move.py"), "clear", "alpha", "--memory", str(tmp_path / "mem")], capture_output=True, text=True)
    assert again.returncode == 1                                                              # nothing left to clear
    _on_a_quota_while_b_ok(tmp_path)
    run(tmp_path, now=NOW + 100)
    assert len(moved_lines(tmp_path)) == 2 and moves(tmp_path) == [f"alpha B {OPUS}"]         # cleared by a person: it may move again


@pytest.mark.parametrize("name, edit", [
    ("second-move", ("        s = standing.get(post)\n", "        s = None\n")),
    ("repeating-standing-line", ("            continue                                 # the same cooldown seen again: no second move, nothing said\n",
                                 "            out[\"said\"].append((f\"post {post} decided onto hub {s['to']} at {hhmm(s['since'])}, moved from {s['from']} on quota\", False, None))\n            continue\n")),
])
def test_f5m_bound_mutants_are_red(tmp_path, name, edit):
    script = _copy(tmp_path, "m", edit)
    _moved_once(tmp_path, script)
    run(tmp_path, script, now=NOW + 60)                                                      # the same cooldown, seen again
    ok = len(moved_lines(tmp_path)) == 1 and len(standing_lines(tmp_path)) == 1
    if name == "second-move":
        _on_a_quota_while_b_ok(tmp_path)                                                     # and A's new cooldown: the A -> B move
        run(tmp_path, script, now=NOW + 100)
        ok = ok and len(moved_lines(tmp_path)) == 1
    assert not ok, f"mutant {name} still reads green"


def test_f5m_mutant_a_move_back_after_the_first_hub_records_a_200_is_red(tmp_path):
    script = _copy(tmp_path, "m", ("        s = standing.get(post)\n",
                                   "        s = standing.get(post)\n        if s and state.get((s['from'], s['model']), ('',))[0] == 'ok':\n            standing.pop(post)\n            s = None\n"))
    _moved_once(tmp_path, script)
    _state(tmp_path, [f"A {OPUS} ok {NOW + 40} {NOW + 40}", f"B {OPUS} ok {NOW + 40} {NOW + 40}"], written=NOW + 50)    # B records a 200, A fine
    _route(tmp_path, [f"alpha A {OPUS}"], written=NOW + 50)
    run(tmp_path, script, now=NOW + 50)
    _on_a_quota_while_b_ok(tmp_path)
    run(tmp_path, script, now=NOW + 100)
    assert len(moved_lines(tmp_path)) == 2, "the mutant must move the post back; the real one never does (the standing line is not cleared by a 200)"
    # the real mover, same sequence: never moves it back
    t2 = tmp_path / "real"
    t2.mkdir()
    _moved_once(t2)
    _state(t2, [f"A {OPUS} ok {NOW + 40} {NOW + 40}", f"B {OPUS} ok {NOW + 40} {NOW + 40}"], written=NOW + 50)
    _route(t2, [f"alpha A {OPUS}"], written=NOW + 50)
    run(t2, now=NOW + 50)
    _on_a_quota_while_b_ok(t2)
    run(t2, now=NOW + 100)
    assert len(moved_lines(t2)) == 1 and moves(t2) == [f"alpha A {OPUS}"]


def test_f5m_mutant_the_moved_posts_own_box_line_dropped_is_red(tmp_path):
    script = _copy(tmp_path, "m", ('out["tell"].append((post, aid(*did, kind="tell"), f"[hub-move] you are decided onto hub', '_drop = ((post, aid(*did, kind="tell"), f"[hub-move] you are decided onto hub'))
    _moved_once(tmp_path, script)
    assert [s for s in spool(tmp_path) if s["to"] == "alpha"] == [], "the mutant must drop the post's own line"
    t2 = tmp_path / "real"
    t2.mkdir()
    _moved_once(t2)
    own = [s for s in spool(t2) if s["to"] == "alpha"]
    assert len(own) == 1 and "hub A" in own[0]["text"] and "never moves you back" in own[0]["text"]


def test_f5_a_line_not_delivered_is_decided_and_said_again_never_lost(tmp_path):
    _state(tmp_path, [A_OK, B_QUOTA])
    _route(tmp_path, [f"alpha B {OPUS}"])
    bad = tmp_path / "no-such-dir" / "said"
    r = subprocess.run([sys.executable, "-I", str(BIN / "hub_move.py"), "decide", "--state", str(tmp_path / "state"), "--route", str(tmp_path / "route"),
                        "--memory", str(tmp_path / "mem"), "--said", str(bad), "--now", str(NOW)], capture_output=True, text=True)
    assert r.returncode == 1 and not (tmp_path / "mem").exists()                              # nothing remembered, nothing applied
    r = run(tmp_path)
    assert r.returncode == 0 and len(moved_lines(tmp_path)) == 1 and moves(tmp_path) == [f"alpha A {OPUS}"]


# ---------- f6: the two old no-move lines point here ----------
POINT = "g7.16.1.11.46.37"


def _row6(files: dict) -> bool:
    """The row's own command, over {path: text}: the .46.35 pointer, BOTH of hub_quota.py and its build node name this leaf, and the old line is gone."""
    return (POINT in files[".agi/nodes/goal/g7.16.1.11.46.35.md"]
            and sum(POINT in files[p] for p in ("extensions/agi/bin/hub_quota.py", ".agi/nodes/build/bin-hub-quota.md")) == 2
            and "moves no post between hubs" not in files["extensions/agi/bin/hub_quota.py"])


def _files():
    return {p: (ROOT / p).read_text() for p in (".agi/nodes/goal/g7.16.1.11.46.35.md", "extensions/agi/bin/hub_quota.py", ".agi/nodes/build/bin-hub-quota.md")}


def test_f6_the_old_no_move_lines_point_at_this_leaf():
    assert _row6(_files())


def test_f6m_mutants_are_red():
    f = _files()
    old = dict(f, **{"extensions/agi/bin/hub_quota.py": f["extensions/agi/bin/hub_quota.py"] + "\nIt moves no post between hubs.\n"})
    assert not _row6(old)                                                                    # the old line left standing
    for p in f:
        gone = dict(f, **{p: f[p].replace(POINT, "g7.16.1.11.46.XX")})
        assert not _row6(gone), f"pointer missing from {p} must be RED"


# ---------- f7 (child of 269cd97451, sp + alive 11-16): the decide-vs-apply seam ----------
def test_f7_decide_with_no_apply_never_says_on_hub_since(tmp_path):
    _moved_once(tmp_path)
    assert not [l for l in said(tmp_path) if "on hub A since" in l]
    assert any("pending the host step" in l for l in said(tmp_path))


def test_f7m_mutant_old_standing_wording_is_red(tmp_path):
    script = _copy(tmp_path, "m", ('mine = f"post {post} decided onto hub {other} at {hhmm(now)}, moved from {hub} on quota, pending the host step"',
                                   'mine = f"post {post} on hub {other} since {hhmm(now)}, moved from {hub} on quota"'))
    _moved_once(tmp_path, script)
    assert any("on hub A since" in l for l in said(tmp_path))                                 # the mutant says it: f7 is RED on it


def _back_on_b_by_hand(tmp, script=None):
    _moved_once(tmp, script)
    _state(tmp, [f"A {OPUS} ok {NOW + 90} {NOW + 90}", f"B {OPUS} ok {NOW + 90} {NOW + 90}"], written=NOW + 100)
    _route(tmp, [f"alpha A {OPUS}"], written=NOW + 100)                                      # applied: seen on its `to` hub
    run(tmp, script, now=NOW + 100)
    _route(tmp, [f"alpha B {OPUS}"], written=NOW + 200)                                      # then moved back by a route edit, no `clear`
    return run(tmp, script, now=NOW + 200)


def test_f7_a_hand_move_back_without_clear_is_said_once_and_the_row_stays(tmp_path):
    r = _back_on_b_by_hand(tmp_path)
    assert r.returncode == 0, r.stderr
    back = [l for l in said(tmp_path) if "is back on hub B by hand" in l]
    assert len(back) == 1 and "hub_move.py clear alpha" in back[0], said(tmp_path)
    assert moves(tmp_path) == [f"alpha A {OPUS}"]
    run(tmp_path, now=NOW + 260)
    assert len([l for l in said(tmp_path) if "is back on hub B by hand" in l]) == 1           # ONCE, not every run


def test_f7_no_back_line_before_the_host_ever_applied(tmp_path):
    _moved_once(tmp_path)
    run(tmp_path, now=NOW + 60)                                                              # route still reads B: not seen on A, so not 'back'
    assert not [l for l in said(tmp_path) if "by hand" in l]


def test_f7m_mutant_silence_is_red(tmp_path):
    script = _copy(tmp_path, "m", ('            key = f"standing {post} back {hub}"\n', '            continue\n            key = f"standing {post} back {hub}"\n'))
    _back_on_b_by_hand(tmp_path, script)
    assert not [l for l in said(tmp_path) if "is back on hub B by hand" in l]                 # the mutant is silent: f7 above is RED on it


# ---------- f8 (all-is-one 11-16): a replayed decision keeps ONE alarm id ----------
def test_f8_a_partial_delivery_replays_the_loud_line_under_one_id(tmp_path):
    _state(tmp_path, [A_OK, B_QUOTA]); _route(tmp_path, [f"alpha B {OPUS}"])
    (tmp_path / "spool").write_text("".join(json.dumps({"id": f"x{i}", "job": "j", "to": "z", "text": "t", "ts": 1}) + "\n" for i in range(4)))
    r1 = run(tmp_path, extra=["--max-lines", "5"])                                           # the loud line fits (5), the tell is refused: rc 1, memory unsaved
    assert r1.returncode == 1, r1.stdout
    (tmp_path / "spool").write_text("".join(l + "\n" for l in (tmp_path / "spool").read_text().splitlines() if '"to": "z"' not in l))   # the drain
    r2 = run(tmp_path, extra=["--max-lines", "5"])
    assert r2.returncode == 0, r2.stderr
    ids = [x["id"] for x in spool(tmp_path) if x["to"] == "sanctuary-master"]
    assert len(ids) == 2 and len(set(ids)) == 1 and ids[0].startswith("hm-loud-"), ids      # two copies, ONE id: the drain sends it once


def test_f8m_mutant_id_dropped_is_red(tmp_path):
    script = _copy(tmp_path, "m", ("now=now, alarm_id=lid)", "now=now)"))
    _state(tmp_path, [A_OK, B_QUOTA]); _route(tmp_path, [f"alpha B {OPUS}"])
    (tmp_path / "spool").write_text("".join(json.dumps({"id": f"x{i}", "job": "j", "to": "z", "text": "t", "ts": 1}) + "\n" for i in range(4)))
    run(tmp_path, script, extra=["--max-lines", "5"])
    (tmp_path / "spool").write_text("".join(l + "\n" for l in (tmp_path / "spool").read_text().splitlines() if '"to": "z"' not in l))
    run(tmp_path, script, extra=["--max-lines", "5"])
    ids = [x["id"] for x in spool(tmp_path) if x["to"] == "sanctuary-master"]
    assert len(set(ids)) != 1, "mutant still reads one id: f8 is RED on it"


# ---------- f9 (sp + all-is-one 11-16): move, clear, move again in ONE window = two ids, two tells ----------
def _clear(tmp, now):
    return subprocess.run([sys.executable, "-I", str(BIN / "hub_move.py"), "clear", "alpha", "--memory", str(tmp / "mem"),
                           "--said", str(tmp / "said"), "--moves", str(tmp / "moves"), "--now", str(now)], capture_output=True, text=True)


def _move_clear_move(tmp, reset, script=None):
    _state(tmp, [A_OK, f"B {OPUS} quota {reset} {NOW - 5}"])
    _route(tmp, [f"alpha B {OPUS}"])
    run(tmp, script)
    assert _clear(tmp, NOW + 30).returncode == 0
    run(tmp, script, now=NOW + 60)                                                           # the route reads B again, B still in the SAME window
    return ([x["id"] for x in spool(tmp) if x["to"] == "sanctuary-master"], [x["id"] for x in spool(tmp) if x["to"] == "alpha"])


@pytest.mark.parametrize("reset", [0, RESET])
def test_f9_move_clear_move_in_one_window_is_two_loud_ids_and_two_tells(tmp_path, reset):
    loud, tell = _move_clear_move(tmp_path, reset)
    assert len(loud) == 2 and len(set(loud)) == 2 and len(tell) == 2 and len(set(tell)) == 2, (loud, tell)


@pytest.mark.parametrize("reset", [0, RESET])
def test_f9m_mutant_counter_dropped_is_red(tmp_path, reset):
    script = _copy(tmp_path, "m", ('q[1], mem.get("cleared", {}).get(post, 0))', 'q[1])'))
    loud, tell = _move_clear_move(tmp_path, reset, script)
    assert len(set(loud)) == 1 and len(set(tell)) == 1, "the mutant must repeat the ids: f9 is RED on it"


# ---------- f10 (SM + aio + sp 11-16): the words say what the HOST does, and the stay id counts clears ----------
def test_f10_the_back_line_says_the_host_does_not_reapply(tmp_path):
    _back_on_b_by_hand(tmp_path)
    back = [l for l in said(tmp_path) if "is back on hub B by hand" in l]
    assert len(back) == 1 and "does NOT re-apply" in back[0] and "re-applies" not in back[0] and "clear alpha" in back[0], back
    doc = (BIN / "hub_move.py").read_text()
    assert "is re-applied" not in doc and "re-applies the row" not in doc


def test_f10m_mutant_old_back_wording_is_red(tmp_path):
    script = _copy(tmp_path, "m", ("the host does NOT re-apply it; \"", "or the host re-applies it; \""))
    _back_on_b_by_hand(tmp_path, script)
    back = [l for l in said(tmp_path) if "is back on hub B by hand" in l]
    assert back and "does NOT re-apply" not in back[0], "the mutant says the false line: f10 is RED on it"


def _stay_after_clear(tmp, script=None):
    """move B -> A, A hits quota (stay said), clear, move B -> A again, A hits quota with the SAME reset: the stay ids."""
    _moved_once(tmp, script)
    _on_a_quota_while_b_ok(tmp)
    run(tmp, script, now=NOW + 100)
    assert _clear(tmp, NOW + 110).returncode == 0
    _state(tmp, [A_OK, f"B {OPUS} quota {RESET} {NOW + 120}"], written=NOW + 130)
    _route(tmp, [f"alpha B {OPUS}"], written=NOW + 130)
    run(tmp, script, now=NOW + 130)                                                          # the second real move
    _on_a_quota_while_b_ok(tmp)
    run(tmp, script, now=NOW + 200)                                                          # A in quota AGAIN, same reset: a second stay
    return [x["id"] for x in spool(tmp) if x["to"] == "sanctuary-master" and "stays on hub" in x["text"]]


def test_f10_the_stay_id_counts_clears(tmp_path):
    ids = _stay_after_clear(tmp_path)
    assert len(ids) == 2 and len(set(ids)) == 2, ids


def test_f10m_mutant_stay_counter_dropped_is_red(tmp_path):
    script = _copy(tmp_path, "m", ('model, q[1], mem.get("cleared", {}).get(post, 0), kind="stay")', 'model, q[1], kind="stay")'))
    ids = _stay_after_clear(tmp_path, script)
    assert len(set(ids)) < 2, "the mutant repeats the stay id: f10 is RED on it"
