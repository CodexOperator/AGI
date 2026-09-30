"""goal:g7.16.1.7.1.1.4 -- ONE stand-up verb.

`rotate.stand_up` (lock -> resolve -> launch -> row write) is the one code
path under all four modes: a seated spawn, a rotate-self successor, a heal
recovery and a hand restart (`rotate.py stand-up --post <p>`). Each mode is
driven for a dummy post and the verb's core is counted. Negative: no
`launch_in_window` / `post_launch_lock` caller outside the verb's core.
Every launch goes to a fake launcher or stops at a sentinel; no tmux.
"""
from __future__ import annotations

import ast
import json
import os
import sys
from pathlib import Path
from types import SimpleNamespace as NS

import pytest

_TS = str(Path(__file__).resolve().parent)
if _TS not in sys.path:
    sys.path.insert(0, _TS)

import heal  # noqa: E402
import rotate  # noqa: E402
from test_rotate_handover import (  # noqa: E402,F401
    _fix, _rotate_self_args, _write_seats_sheet)

BIN = Path(rotate.__file__).resolve().parent
DEAD_PID = 99_999_999  # above any pid_max: never a live process


@pytest.fixture
def calls(monkeypatch):
    seen: list = []
    real = rotate.stand_up

    def counting(root, post, body, *, mode, **kw):
        seen.append((post, mode))
        return real(root, post, body, mode=mode, **kw)

    monkeypatch.setattr(rotate, "stand_up", counting)
    return seen


@pytest.fixture
def graph(tmp_path: Path) -> Path:
    g = tmp_path / "repo" / ".agi"
    (g / "sessions").mkdir(parents=True)
    (g / "config.json").write_text(json.dumps({"metric_primary": "x"}))
    p = g / "nodes" / ".geometry" / "seats.md"
    p.parent.mkdir(parents=True)
    row = {"name": "seat-a", "role": "director", "pid": DEAD_PID,
           "window": "@50", "generation": 2, "model": "m-1"}
    p.write_text("---\nid: config:seats\nseats:\n  - " + json.dumps(row)
                 + "\n---\n", encoding="utf-8")
    (g / "windows.txt").write_text("\n@1 other\n", encoding="utf-8")
    return g


def _launcher(seen: list):
    def launch(root, name, shell_cmd, window_path=None, cwd=None):
        seen.append(name)
        return 424243, "@556"
    return launch


def test_spawn_is_a_stand_up(tmp_path, calls, monkeypatch):
    monkeypatch.setattr(rotate, "_cmd_spawn", lambda args, root: 0)
    assert rotate.cmd_spawn(NS(seat="p1", dry_run=False), tmp_path) == 0
    assert calls == [("p1", "spawn")]


def test_recover_is_a_stand_up(graph, calls):
    launched: list = []
    heal._watch_seats(graph, pid_alive=lambda pid: False,
                      window_path=str(graph / "windows.txt"),
                      launcher=_launcher(launched))
    assert calls == [("seat-a", "recover")] and launched, (calls, launched)


def test_hand_restart_is_a_stand_up(graph, calls, capsys):
    launched: list = []
    rc = rotate.cmd_stand_up(
        NS(post="seat-a", window_path=str(graph / "windows.txt")), graph,
        launcher=_launcher(launched))
    assert rc == 0 and calls == [("seat-a", "restart")], capsys.readouterr()
    assert len(launched) == 1, launched
    recs = sorted((graph / "sessions" / "rotations").glob("seat-a.*.json"))
    rec = json.loads(recs[-1].read_text())
    assert rec["result"] == "respawned" and rec["probable_cause"] == "hand-restart"
    assert "stood up seat-a (fresh)" in capsys.readouterr().out


def test_hand_restart_refuses_a_live_post(graph, calls, capsys):
    p = graph / "nodes" / ".geometry" / "seats.md"
    p.write_text(p.read_text().replace(str(DEAD_PID), str(os.getpid())))
    launched: list = []
    rc = rotate.cmd_stand_up(
        NS(post="seat-a", window_path=str(graph / "windows.txt")), graph,
        launcher=_launcher(launched))
    assert rc == 1 and calls == [] and launched == []
    assert "is alive" in capsys.readouterr().err


def test_rotate_self_successor_is_a_stand_up(_fix, tmp_path, monkeypatch):
    class _Stop(Exception):
        pass

    seen: list = []

    def stop(root, post, body, *, mode, **kw):
        seen.append((post, mode))
        raise _Stop

    _write_seats_sheet(tmp_path, [{"name": "adv-alive", "role": "parent",
                                   "model": "x", "effort": "max",
                                   "settings": ""}])
    win = tmp_path / "windows.txt"
    win.write_text("adv-alive\n", encoding="utf-8")
    monkeypatch.setattr(rotate, "stand_up", stop)
    with pytest.raises(_Stop):
        rotate.cmd_rotate_self(_rotate_self_args(tmp_path, window_path=str(win)),
                               tmp_path)
    assert seen == [("adv-alive", "rotate")]


def _callers(fn_name: str) -> set:
    out = set()
    for f in sorted(BIN.glob("*.py")):
        tree = ast.parse(f.read_text(encoding="utf-8"))
        for fn in ast.walk(tree):
            if not isinstance(fn, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            for node in ast.walk(fn):
                if isinstance(node, ast.Call):
                    c = node.func
                    name = getattr(c, "attr", None) or getattr(c, "id", None)
                    if name == fn_name:
                        out.add((f.name, fn.name))
    return out


def test_no_launch_or_lock_outside_the_verbs_core():
    assert _callers("launch_in_window") == {
        ("rotate.py", "_launch_window"), ("rotate.py", "stand_up_launch")}
    assert _callers("post_launch_lock") == {("rotate.py", "stand_up")}


# ---------- goal:g7.16.1.7.1.4: a stand-up keys its post from the template ----

def _row(graph: Path, name: str) -> dict:
    import write
    return next(r for r in write._load_seats(graph) if r.get("name") == name)


def _verifies(graph: Path, seat: str) -> str:
    """The label send gives a line the seat signs now (whois's verifier)."""
    import send
    ts, to, text = "2026-09-30T00:00:00Z", "belam", "hello"
    sig = send._sign_line(graph, seat, ts, to, text)
    meta = {"sig": sig.split("sig: ", 1)[1], "from": seat, "ts": ts, "to": to}
    import write
    return send._verify_block(graph, list(write._load_seats(graph)), meta, text)


def test_a_stand_up_mints_an_unkeyed_posts_key(graph, capsys):
    assert "pubkey" not in _row(graph, "seat-a")
    held, out = rotate.stand_up(graph, "seat-a", lambda: "launched", mode="restart")
    assert (held, out) == (True, "launched")
    assert "minted its first key" in capsys.readouterr().err
    row = _row(graph, "seat-a")
    assert row["pubkey"] and row["sig_scheme"]
    assert _verifies(graph, "seat-a").startswith("VERIFIED seat-a")


def test_an_existing_key_file_is_adopted_not_left_unkeyed(graph):
    import send
    _path, pub = send._mint_seat_key(graph, "seat-a", send.seatsig.DEFAULT_SCHEME)
    note = rotate.ensure_post_key(graph, "seat-a")
    assert "adopted its existing key" in note, note
    assert _row(graph, "seat-a")["pubkey"] == pub.hex()
    assert _verifies(graph, "seat-a").startswith("VERIFIED seat-a")
    assert rotate.ensure_post_key(graph, "seat-a") == ""  # keyed: nothing to do


def test_the_template_cell_can_leave_an_existing_key(graph, monkeypatch):
    import send
    send._mint_seat_key(graph, "seat-a", send.seatsig.DEFAULT_SCHEME)
    monkeypatch.setattr(rotate, "key_template",
                        lambda root: {"scheme": "", "existing_key": "leave"})
    assert rotate.ensure_post_key(graph, "seat-a") == ""
    assert "pubkey" not in _row(graph, "seat-a")


def test_key_template_defaults_forgiving_and_reads_the_node(graph, tmp_path):
    # the default on a graph that never carries the node (node_writer indexes
    # a root once, so the node-read case below gets a root of its own)
    bare = tmp_path / "bare" / ".agi"
    (bare / "nodes").mkdir(parents=True)
    (bare / "config.json").write_text("{}")
    assert rotate.key_template(bare) == rotate.KEY_TEMPLATE_DEFAULT
    p = graph / "nodes" / ".geometry" / "key-authority.md"
    p.write_text('---\nid: config:key-authority\ntype: config\nkey_template: '
                 '{"existing_key": "leave", "junk": 1}\n---\n', encoding="utf-8")
    assert rotate.key_template(graph) == dict(rotate.KEY_TEMPLATE_DEFAULT,
                                              existing_key="leave")


@pytest.mark.parametrize("mode", rotate.STAND_UP_MODES)
def test_every_stand_up_mode_keys_an_unkeyed_row(graph, mode):
    """hypothesis:stand-up-verb-keys-every-mode-through-key-template: spawn
    (cmd_seats_launch), rotate (cmd_loop, rotate-self), recover and restart
    all key an unkeyed row through key_template before the body runs."""
    seen: list = []
    held, _ = rotate.stand_up(graph, "seat-a",
                              lambda: seen.append(_row(graph, "seat-a")),
                              mode=mode)
    assert held and seen[0].get("pubkey"), seen
    assert _verifies(graph, "seat-a").startswith("VERIFIED seat-a")


def test_a_body_that_keys_itself_is_not_keyed_twice(graph):
    rotate.stand_up(graph, "seat-a", lambda: None, mode="spawn",
                    keyed_in_body=True)
    assert "pubkey" not in _row(graph, "seat-a")


def _stand_up_calls() -> dict:
    """{caller function: [keyed_in_body value]} for every stand_up call."""
    out: dict = {}
    tree = ast.parse((BIN / "rotate.py").read_text(encoding="utf-8"))
    for fn in ast.walk(tree):
        if not isinstance(fn, ast.FunctionDef):
            continue
        for node in ast.walk(fn):
            if (isinstance(node, ast.Call)
                    and getattr(node.func, "id", None) == "stand_up"):
                kib = [k.value.value for k in node.keywords
                       if k.arg == "keyed_in_body"]
                out.setdefault(fn.name, []).extend(kib or [False])
    return out


def test_only_the_seating_spawn_keys_in_its_body():
    """seats-launch and loop go through stand_up's key step; only cmd_spawn
    (its ONE seating commit) keys in its body, via the same template step."""
    calls = _stand_up_calls()
    assert calls["cmd_spawn"] == [True]
    for fn in ("cmd_seats_launch", "cmd_loop", "cmd_rotate_self", "cmd_stand_up"):
        assert calls.get(fn) == [False], (fn, calls)
    fn = ast.parse(inspect.getsource(rotate._first_seating_key).lstrip())
    called = {getattr(n.func, "attr", None) or getattr(n.func, "id", None)
              for n in ast.walk(fn) if isinstance(n, ast.Call)}
    assert "_mint_seat_key" not in called and "_template_key" in called


@pytest.mark.parametrize("pre_key", [False, True])
def test_dry_stand_up_names_the_real_decision(graph, pre_key, capsys):
    """dry == real on the decision: mint or adopt."""
    import send
    if pre_key:
        send._mint_seat_key(graph, "seat-a", send.seatsig.DEFAULT_SCHEME)
    dry = rotate._stand_up_key_plan(graph, "seat-a")
    assert "pubkey" not in _row(graph, "seat-a")
    assert dry in capsys.readouterr().err
    real = rotate.ensure_post_key(graph, "seat-a")
    word = "adopt" if pre_key else "mint"
    assert f"would {word}" in dry and f"{word}ed its" in real, (dry, real)


def test_a_post_with_no_row_is_never_keyed(graph):
    import send
    assert rotate.ensure_post_key(graph, "nobody") == ""
    assert not send._seat_key_path(graph, "nobody").exists()


# ---------- council ruling 09-30: a keyed row with NO key file ---------------

import inspect  # noqa: E402
import subprocess  # noqa: E402


def _keyed_repo(graph: Path, box: str, monkeypatch) -> tuple[list, str]:
    """seat-a KEYED on `box` (its key file absent), a prime row, in a git
    repo whose one commit seats the row there. Returns (sent, witness sha)."""
    import send
    _priv, pub = send.seatsig.get(send.seatsig.DEFAULT_SCHEME).keygen()
    rows = [{"name": "seat-a", "role": "director", "pid": DEAD_PID,
             "window": "@50", "generation": 2, "box": box, "pubkey": pub.hex(),
             "sig_scheme": send.seatsig.DEFAULT_SCHEME, "key_history": []},
            {"name": "prime", "role": "prime_director", "box": box}]
    (graph / "nodes" / ".geometry" / "seats.md").write_text(
        "---\nid: config:seats\nseats:\n" + "".join(
            f"  - {json.dumps(r)}\n" for r in rows) + "---\n", encoding="utf-8")
    top = graph.parent
    for cmd in (["init", "-q"], ["add", "-A"],
                ["-c", "user.name=t", "-c", "user.email=t@t", "commit", "-q",
                 "-m", "seat seat-a on its box"]):
        subprocess.run(["git", "-C", str(top)] + cmd, check=True, capture_output=True)
    sha = subprocess.run(["git", "-C", str(top), "rev-parse", "--short", "HEAD"],
                         capture_output=True, text=True).stdout.strip()
    sent: list = []
    monkeypatch.setattr(send, "send", lambda root, to, text, frm: sent.append((to, text)))
    return sent, sha


def test_own_box_remint_is_unsigned_witnessed_and_found_once(graph, monkeypatch):
    sent, sha = _keyed_repo(graph, "town-x", monkeypatch)
    monkeypatch.setenv("AGI_BOX", "town-x")
    old = _row(graph, "seat-a")["pubkey"]
    note = rotate.ensure_post_key(graph, "seat-a")
    assert "reminted" in note and "UNSIGNED" in note, note
    row = _row(graph, "seat-a")
    assert row["pubkey"] != old
    last = row["key_history"][-1]
    assert (last["pub"], last["signed"], last["box"], last["witness"]) == (
        old, False, "town-x", sha)
    assert last["reason"] == "key file absent on own box" and last["at"].endswith("Z")
    assert _verifies(graph, "seat-a").startswith("VERIFIED seat-a")
    assert [to for to, _ in sent] == ["prime"]  # ONE finding
    assert rotate.ensure_post_key(graph, "seat-a") == ""  # keyed + key: done


def test_foreign_box_refuses_with_one_finding_and_no_keygen_hint(graph, monkeypatch):
    import send
    sent, _sha = _keyed_repo(graph, "town-far", monkeypatch)
    monkeypatch.setenv("AGI_BOX", "town-x")
    old = _row(graph, "seat-a")["pubkey"]
    for _ in range(2):
        note = rotate.ensure_post_key(graph, "seat-a")
        assert "REFUSED" in note and "town-far" in note, note
    assert len(sent) == 1 and "keygen" not in sent[0][1]
    assert _row(graph, "seat-a")["pubkey"] == old
    assert not send._seat_key_path(graph, "seat-a").exists()


def test_no_override_makes_a_foreign_box_the_rows_own(graph, monkeypatch):
    """Condition 4: "this box" is boxes.this_box (AGI_BOX), never a caller
    value -- no box argument exists, a forged row dict naming this box is not
    believed (the node's row is read), and an undeclared box is never own."""
    import send
    for fn in (rotate.ensure_post_key, rotate._rotate_first_key):
        assert "box" not in inspect.signature(fn).parameters
    sent, _sha = _keyed_repo(graph, "town-far", monkeypatch)
    monkeypatch.setenv("AGI_BOX", "town-x")
    forged = dict(_row(graph, "seat-a"), box="town-x")
    assert "REFUSED" in rotate._rotate_first_key(graph, None, "seat-a", forged)
    monkeypatch.delenv("AGI_BOX")
    monkeypatch.setattr("boxes.this_box", lambda root: (_ for _ in ()).throw(
        RuntimeError("undeclared")))
    assert "(undeclared)" in rotate.ensure_post_key(graph, "seat-a")
    assert not send._seat_key_path(graph, "seat-a").exists()


def test_the_missing_key_row_can_refuse(graph, monkeypatch):
    _sent, _sha = _keyed_repo(graph, "town-x", monkeypatch)
    monkeypatch.setenv("AGI_BOX", "town-x")
    monkeypatch.setattr(rotate, "key_template", lambda root: dict(
        rotate.KEY_TEMPLATE_DEFAULT, missing_key="refuse"))
    assert rotate.ensure_post_key(graph, "seat-a") == ""


def test_no_template_skill_or_card_instructs_keygen():
    """goal:g7.16.1.7.1.4 falsifier 2 (negative): no role template, skill,
    card or root doc tells a post to RUN `send.py ... keygen` -- the stand-up
    and rotate-self key the row from key_template. A file:line citation of
    the code (`send.py:796 keygen`) is not an invocation."""
    repo = BIN.parents[2]
    call = __import__("re").compile(r"send\.py\s+(?:--\S+\s+\S+\s+)*keygen\b")
    files = [*repo.glob("skills/**/SKILL.md"), repo / "CLAUDE.md",
             repo / "QUICKSTART.md",
             *repo.glob(".agi/nodes/doc/unified-*.md"),
             *repo.glob(".agi/nodes/doc/card-*.md"),
             *(repo / ".agi" / "nodes" / ".geometry" / f for f in
               ("rotations.md", "brief.md", "posts.md"))]
    hits = [f"{f.relative_to(repo)}:{n}"
            for f in files if f.is_file()
            for n, line in enumerate(f.read_text(encoding="utf-8").splitlines(), 1)
            if call.search(line)]
    assert hits == []


# ---------- run-27 residues 158-161 ------------------------------------------

def test_a_refused_row_write_leaves_no_key_file_and_retries(graph, monkeypatch):
    """158: the remint key file lands only after the row names it."""
    import send
    _sent, _sha = _keyed_repo(graph, "town-x", monkeypatch)
    monkeypatch.setenv("AGI_BOX", "town-x")
    real = rotate._write_identity_cells
    monkeypatch.setattr(rotate, "_write_identity_cells", lambda *a, **k: False)
    assert "remint held" in rotate.ensure_post_key(graph, "seat-a")
    assert not send._seat_key_path(graph, "seat-a").exists()
    monkeypatch.setattr(rotate, "_write_identity_cells", real)
    assert "reminted" in rotate.ensure_post_key(graph, "seat-a")
    assert _verifies(graph, "seat-a").startswith("VERIFIED seat-a")


def test_a_dry_run_remint_sends_nothing_and_writes_nothing(graph, monkeypatch):
    """160: a dry run reports the plan; no finding, no mark, no key file."""
    import send
    sent, _sha = _keyed_repo(graph, "town-far", monkeypatch)
    monkeypatch.setenv("AGI_BOX", "town-x")
    row = _row(graph, "seat-a")
    note = rotate._rotate_first_key(graph, None, "seat-a", row, dry_run=True)
    assert note.startswith("(dry-run)") and "REFUSED" in note, note
    monkeypatch.setenv("AGI_BOX", "town-far")
    note = rotate._rotate_first_key(graph, None, "seat-a", row, dry_run=True)
    assert "would remint" in note, note
    assert sent == [] and not send._seat_key_path(graph, "seat-a").exists()
    assert not list((graph / "sessions").rglob("*.key-finding"))


def test_own_box_without_a_witness_refuses(graph, monkeypatch):
    """161: the own box alone is not enough -- no commit shows the box cell."""
    import send
    sent, _sha = _keyed_repo(graph, "town-x", monkeypatch)
    monkeypatch.setenv("AGI_BOX", "town-x")
    monkeypatch.setattr(rotate, "_box_cell_witness", lambda root, seat, box: "")
    pub_before = _row(graph, "seat-a").get("pubkey")
    note = rotate.ensure_post_key(graph, "seat-a")
    assert "no commit witnesses" in note and "REFUSED" in note, note
    assert len(sent) == 1 and not send._seat_key_path(graph, "seat-a").exists()
    assert _row(graph, "seat-a").get("pubkey") == pub_before


def test_a_failed_rename_leaves_no_row_naming_a_lost_key(graph, monkeypatch):
    """158b: the key is staged before the row write and renamed after; a
    failed rename restores the row and leaves no temp file behind, and a
    same-process retry then remints cleanly."""
    import send
    _sent, _sha = _keyed_repo(graph, "town-x", monkeypatch)
    monkeypatch.setenv("AGI_BOX", "town-x")
    pub_before = _row(graph, "seat-a").get("pubkey")
    real = rotate._place_seat_key

    def boom(src, dst):
        raise OSError("rename refused")
    monkeypatch.setattr(rotate, "_place_seat_key", boom)
    note = rotate.ensure_post_key(graph, "seat-a")
    assert "remint held" in note and "row restored" in note, note
    key = send._seat_key_path(graph, "seat-a")
    assert not key.exists()
    assert not list(key.parent.glob(f".{key.name}.*"))
    assert _row(graph, "seat-a").get("pubkey") == pub_before
    monkeypatch.setattr(rotate, "_place_seat_key", real)
    assert "reminted" in rotate.ensure_post_key(graph, "seat-a")
    assert _verifies(graph, "seat-a").startswith("VERIFIED seat-a")
    assert not list(key.parent.glob(f".{key.name}.*"))


def test_a_refused_row_unlinks_the_staged_key(graph, monkeypatch):
    """158b: a refused row write unlinks the staged temp -- nothing left."""
    import send
    _sent, _sha = _keyed_repo(graph, "town-x", monkeypatch)
    monkeypatch.setenv("AGI_BOX", "town-x")
    monkeypatch.setattr(rotate, "_write_identity_cells", lambda *a, **k: False)
    assert "remint held" in rotate.ensure_post_key(graph, "seat-a")
    key = send._seat_key_path(graph, "seat-a")
    assert not key.exists() and not list(key.parent.glob(f".{key.name}.*"))


def _stage_orphan(graph: Path, seat: str, priv: bytes) -> Path:
    import send
    return rotate._stage_seat_key(send, graph, seat,
                                  send.seatsig.DEFAULT_SCHEME, priv)


def _a_new_key() -> tuple[bytes, str]:
    import send
    priv, pub = send.seatsig.get(send.seatsig.DEFAULT_SCHEME).keygen()
    return priv, pub.hex()


def _age_orphan(tmp: Path) -> Path:
    """age a staged temp past the grace window -- an ORPHAN, not another
    process's in-flight stage (hypothesis:...-orphan-staged-key, D2)."""
    import os
    import time
    when = time.time() - rotate.ORPHAN_TEMP_GRACE_S - 1
    os.utime(tmp, (when, when))
    return tmp


def _seats_dirty(graph: Path) -> str:
    return subprocess.run(["git", "-C", str(graph.parent), "status", "--porcelain",
                           "--", ".agi/nodes/.geometry/seats.md"],
                          capture_output=True, text=True).stdout.strip()


def test_the_remint_adopts_its_own_orphan_staged_key(graph, monkeypatch):
    """158c: the kill between the row write and the rename -- the next run
    ADOPTS the temp (no remint, no key_history entry) and sweeps every other
    orphan temp for the seat."""
    import send
    _sent, _sha = _keyed_repo(graph, "town-x", monkeypatch)
    monkeypatch.setenv("AGI_BOX", "town-x")
    priv, pub = _a_new_key()
    seats = graph / "nodes" / ".geometry" / "seats.md"
    # the row write landed naming the new pub; the rename never did
    seats.write_text(seats.read_text().replace(_row(graph, "seat-a")["pubkey"], pub),
                     encoding="utf-8")
    key = send._seat_key_path(graph, "seat-a")
    _stage_orphan(graph, "seat-a", priv)
    _age_orphan(_stage_orphan(graph, "seat-a", _a_new_key()[0]))  # an old orphan
    assert _seats_dirty(graph), "the pre-crash row write is uncommitted"
    note = rotate.ensure_post_key(graph, "seat-a")
    assert "ADOPTED" in note and "remint held" not in note, note
    assert json.loads(key.read_text())["priv_hex"] == priv.hex()
    assert _row(graph, "seat-a")["pubkey"] == pub
    assert _row(graph, "seat-a")["key_history"] == []
    assert _verifies(graph, "seat-a").startswith("VERIFIED seat-a")
    assert list(key.parent.glob(f".{key.name}.*")) == []
    # 3/4: the adopt COMMITS the row (as the remint twin does) and its ONE
    # finding names the box and the witness, like the twin's.
    assert _seats_dirty(graph) == "", "the adopt left the adopted row uncommitted"
    assert "town-x" in note and "witness" in note and _sha in note, note


def test_a_stale_orphan_temp_is_swept_and_the_remint_still_runs(graph, monkeypatch):
    """158c falsifier 2: a temp whose key the row does NOT name is unlinked
    once it is an ORPHAN (past the grace window) and the normal remint path
    runs (key_history grows by one)."""
    import send
    _sent, _sha = _keyed_repo(graph, "town-x", monkeypatch)
    monkeypatch.setenv("AGI_BOX", "town-x")
    old = _row(graph, "seat-a")["pubkey"]
    key = send._seat_key_path(graph, "seat-a")
    _age_orphan(_stage_orphan(graph, "seat-a", _a_new_key()[0]))
    note = rotate.ensure_post_key(graph, "seat-a")
    assert "reminted" in note and "ADOPTED" not in note, note
    assert _row(graph, "seat-a")["pubkey"] != old
    assert len(_row(graph, "seat-a")["key_history"]) == 1
    assert list(key.parent.glob(f".{key.name}.*")) == []


def test_a_fresh_non_matching_temp_is_a_concurrent_mint_and_is_left_alone(
        graph, monkeypatch):
    """D2: the sweep never unlinks a temp younger than ORPHAN_TEMP_GRACE_S
    -- that is another process's in-flight stage, a LIVE private key between
    its keygen and its rename. The dry run says it would sweep 0 (D3)."""
    import send
    sent, _sha = _keyed_repo(graph, "town-x", monkeypatch)
    monkeypatch.setenv("AGI_BOX", "town-x")
    key = send._seat_key_path(graph, "seat-a")
    row = _row(graph, "seat-a")
    _stage_orphan(graph, "seat-a", _a_new_key()[0])   # written microseconds ago
    dry = rotate._rotate_first_key(graph, None, "seat-a", row, dry_run=True)
    assert "would remint" in dry and "sweep 0" in dry, dry
    note = rotate.ensure_post_key(graph, "seat-a")
    assert "reminted" in note, note
    assert [p.name for p in key.parent.glob(f".{key.name}.*")] != [], \
        "a concurrent mint's live private key was swept mid-mint"


def test_the_dry_run_names_the_adopt_and_changes_nothing(graph, monkeypatch):
    """158c falsifier 3 (mechanism, not prose): the dry run reports the
    adopt AND the sweep count, and unlinks/renames/finds nothing."""
    import send
    _sent, _sha = _keyed_repo(graph, "town-x", monkeypatch)
    monkeypatch.setenv("AGI_BOX", "town-x")
    priv, pub = _a_new_key()
    seats = graph / "nodes" / ".geometry" / "seats.md"
    seats.write_text(seats.read_text().replace(_row(graph, "seat-a")["pubkey"], pub),
                     encoding="utf-8")
    _stage_orphan(graph, "seat-a", priv)       # the key the row already names
    _age_orphan(_stage_orphan(graph, "seat-a", _a_new_key()[0]))  # an old orphan
    row = _row(graph, "seat-a")
    dry = rotate._rotate_first_key(graph, None, "seat-a", row, dry_run=True)
    assert "would ADOPT its orphan staged key and sweep 1" in dry, dry
    key = send._seat_key_path(graph, "seat-a")
    assert not key.exists() and len(list(key.parent.glob(f".{key.name}.*"))) == 2
    assert _sent == [] and not list((graph / "sessions").rglob("*.key-finding"))


def test_the_seating_keys_from_the_template_too(graph, monkeypatch):
    """159: spawn's _first_seating_key adopts an existing key file and sends
    a keyed row with no key file to the own-box rule."""
    import send
    _p, pub = send._mint_seat_key(graph, "seat-a", send.seatsig.DEFAULT_SCHEME)
    cells, note = rotate._first_seating_key(graph, "seat-a")
    assert cells["pubkey"] == pub.hex() and "adopted its existing key" in note
    sent, _sha = _keyed_repo(graph, "town-far", monkeypatch)
    send._seat_key_path(graph, "seat-a").unlink()
    monkeypatch.setenv("AGI_BOX", "town-x")
    cells, note = rotate._first_seating_key(graph, "seat-a")
    assert cells == {} and "REFUSED" in note, note
