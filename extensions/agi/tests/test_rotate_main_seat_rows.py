"""hypothesis:rotate-verbs-read-the-main-seat-rows -- rotate's seat-row
READERS resolve through `_seat_read_root` (the MAIN graph copy), never the
caller's lagging worktree copy, exactly as `cmd_rotate` already does.

Fixture: a real MAIN checkout + a linked git worktree, each carrying its own
`.agi/nodes/.geometry/seats.md`. No live seats row, no tmux, no real seat key
outside the fixture.

Conjuncts:
  (a) `cmd_merge_up --post` picks a NON-caller target row from MAIN; a
      worktree copy that names the seat at a rank the caller may NOT rotate
      must not win.
  (b) `rotate-self --prepare`'s registry gate sees a seat that exists in
      MAIN but not in the worktree copy; and the documented fallback (MAIN
      has no row for the seat) still reads the worktree copy.
  (c) `cmd_rotate`'s target lookup reads MAIN (the missing test).
  (d) `_caller_post`'s `$AGI_POST` path from a worktree root reads MAIN's
      row (the missing test).
"""
import json
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
import rotate  # noqa: E402
import send  # noqa: E402


def _write_seats(root, rows):
    gp = root / "nodes" / ".geometry"
    gp.mkdir(parents=True, exist_ok=True)
    body = "---\nid: config:seats\ntype: config\nseats:\n"
    for r in rows:
        body += "  - " + json.dumps(r) + "\n"
    body += "---\n"
    (gp / "seats.md").write_text(body, encoding="utf-8")


def _make(tmp_path):
    """A MAIN checkout + one linked worktree, both with a real `.agi` graph.
    Returns (main_graph, wt_graph, seat) where the graphs are `.agi` roots."""
    repo = tmp_path / "main"
    repo.mkdir(parents=True)
    subprocess.run(["git", "-C", str(repo), "init", "-b", "season/s1"],
                   check=True, capture_output=True)
    for cfg in ("user.email", "user.name"):
        subprocess.run(["git", "-C", str(repo), "config", cfg, "t"],
                       check=True, capture_output=True)
    (repo / ".agi" / "nodes").mkdir(parents=True)
    (repo / ".agi" / "config.json").write_text('{"metric_primary": "x"}')
    seat = "s-director"
    wt = tmp_path / "wt"
    _write_seats(repo / ".agi", [{"name": seat, "role": "director",
                                  "window": "@OLD", "pid": 100,
                                  "generation": 3}])
    subprocess.run(["git", "-C", str(repo), "add", "-A"], check=True,
                   capture_output=True)
    subprocess.run(["git", "-C", str(repo), "commit", "-m", "init"],
                   check=True, capture_output=True)
    subprocess.run(["git", "-C", str(repo), "worktree", "add",
                    "-b", "loop/x-a@s1", str(wt), "season/s1"],
                   check=True, capture_output=True)
    return repo / ".agi", wt / ".agi", seat


def _make_keyed(tmp_path):
    """Same two-tree fixture, plus a real held key for `seat` minted in MAIN.
    Returns (main_graph, wt_graph, seat, pub_a, pub_b); the seat's `.key`
    holds pub_b, an unrelated keypair gives pub_a."""
    repo = tmp_path / "main"
    repo.mkdir(parents=True)
    subprocess.run(["git", "-C", str(repo), "init", "-b", "season/s1"],
                   check=True, capture_output=True)
    for cfg in ("user.email", "user.name"):
        subprocess.run(["git", "-C", str(repo), "config", cfg, "t"],
                       check=True, capture_output=True)
    (repo / ".agi" / "nodes").mkdir(parents=True)
    (repo / ".agi" / "config.json").write_text('{"metric_primary": "x"}')
    seat = "s-director"
    _p_b, pub_b = send._mint_seat_key(repo / ".agi", seat, "ed25519")
    _p_a, pub_a = send._mint_seat_key(repo / ".agi", "unrelated", "ed25519")
    wt = tmp_path / "wt"
    _write_seats(repo / ".agi", [{"name": seat, "role": "director",
                                  "window": "@OLD", "pid": 100,
                                  "generation": 3, "worktree": str(wt),
                                  "pubkey": pub_b.hex()}])
    subprocess.run(["git", "-C", str(repo), "add", "-A"], check=True,
                   capture_output=True)
    subprocess.run(["git", "-C", str(repo), "commit", "-m", "init"],
                   check=True, capture_output=True)
    subprocess.run(["git", "-C", str(repo), "worktree", "add",
                    "-b", "loop/x-a@s1", str(wt), "season/s1"],
                   check=True, capture_output=True)
    return repo / ".agi", wt / ".agi", seat, pub_a.hex(), pub_b.hex()


def _caller(name, role):
    return (name, {"name": name, "role": role}, "env")


# --- (a) cmd_merge_up's target-row lookup reads MAIN ----------------------

def test_merge_up_target_row_reads_main(tmp_path, monkeypatch):
    """(a) the caller (helper) may rotate MAIN's `director` row; the worktree
    copy names the same seat `prime_director` (caller may NOT rotate). The
    target row handed to `_rank_gate` must be MAIN's -- role `director`."""
    main, wt, seat = _make(tmp_path)
    _write_seats(main, [{"name": "s-helper", "role": "helper"},
                        {"name": seat, "role": "director"}])
    _write_seats(wt, [{"name": "s-helper", "role": "helper"},
                      {"name": seat, "role": "prime_director"}])
    monkeypatch.setattr(rotate, "_caller_post", lambda _r: _caller("s-helper",
                                                                   "helper"))
    seen = {}

    def fake_gate(crow, trow, ranks):
        seen["role"] = trow.get("role")
        return None

    monkeypatch.setattr(rotate, "_rank_gate", fake_gate)
    monkeypatch.setattr(rotate, "merge_up_plan",
                        lambda r, p: (_ for _ in ()).throw(ValueError("stub")))
    rc = rotate.cmd_merge_up(SimpleNamespace(post=seat, name=None,
                                             dry_run=False), wt)
    assert seen.get("role") == "director", (
        "cmd_merge_up must read the target row from MAIN, not the worktree")
    assert rc == 3  # the stubbed plan refuses; the gate was reached


def test_merge_up_stale_worktree_row_never_authorizes(tmp_path, monkeypatch,
                                                      capsys):
    """(a) vice versa: MAIN's row is `prime_director` (the caller must be
    refused), the worktree copy is a stale permissive `director`. The real
    rank gate must refuse BY NAME and never reach the plan."""
    main, wt, seat = _make(tmp_path)
    _write_seats(main, [{"name": "s-helper", "role": "helper"},
                        {"name": seat, "role": "prime_director"}])
    _write_seats(wt, [{"name": "s-helper", "role": "helper"},
                      {"name": seat, "role": "director"}])
    monkeypatch.setattr(rotate, "_caller_post", lambda _r: _caller("s-helper",
                                                                   "helper"))
    reached = {}
    monkeypatch.setattr(
        rotate, "merge_up_plan",
        lambda r, p: (reached.__setitem__("plan", True),
                      (_ for _ in ()).throw(ValueError("stub")))[1])
    rc = rotate.cmd_merge_up(SimpleNamespace(post=seat, name=None,
                                             dry_run=False), wt)
    err = capsys.readouterr().err
    assert "refuse upward" in err, (
        "MAIN's prime_director row must gate the helper, not the worktree's "
        f"stale row: {err}")
    assert "plan" not in reached, "the plan must not be reached"
    assert rc == 3


# --- (b) rotate-self --prepare's registry gate reads MAIN -----------------

def test_prepare_gate_sees_main_only_seat(tmp_path, monkeypatch):
    """(b) the seat exists in MAIN and NOT in the worktree copy. The prepare
    gate must see it and reach `cmd_prepare`."""
    main, wt, seat = _make(tmp_path)
    _write_seats(main, [{"name": seat, "role": "director"}])
    _write_seats(wt, [{"name": "someone-else", "role": "director"}])
    reached = {}
    monkeypatch.setattr(rotate, "cmd_prepare",
                        lambda a, r: (reached.__setitem__("ok", True), 0)[1])
    ns = SimpleNamespace(name=seat, seat=seat, throwaway=False, dry_run=True,
                         prepare=True)
    rc = rotate.cmd_rotate_self(ns, wt)
    assert reached.get("ok"), (
        "rotate-self --prepare must find the seat in MAIN and reach the "
        "prepare path")
    assert rc == 0


def test_prepare_gate_falls_back_when_main_lacks_the_seat(tmp_path,
                                                          monkeypatch):
    """(b) documented fallback: when MAIN has NO row for the seat, the
    worktree copy is read (this is the same per-seat fallback
    `test_rotate_caller_post.test_seat_absent_from_main_falls_back_to_worktree`
    locks in)."""
    main, wt, seat = _make(tmp_path)
    _write_seats(main, [{"name": "someone-else", "role": "director"}])
    _write_seats(wt, [{"name": seat, "role": "director"}])
    reached = {}
    monkeypatch.setattr(rotate, "cmd_prepare",
                        lambda a, r: (reached.__setitem__("ok", True), 0)[1])
    ns = SimpleNamespace(name=seat, seat=seat, throwaway=False, dry_run=True,
                         prepare=True)
    rc = rotate.cmd_rotate_self(ns, wt)
    assert reached.get("ok"), "the per-seat fallback must still reach prepare"
    assert rc == 0


# --- (c) cmd_rotate's target-row lookup reads MAIN ------------------------

def test_cmd_rotate_target_row_reads_main(tmp_path, monkeypatch):
    """(c) the missing test: `cmd_rotate`'s non-self target lookup resolves
    MAIN's row. The worktree copy is stale at another role, and the row handed
    to the rank gate must be MAIN's."""
    main, wt, seat = _make(tmp_path)
    _write_seats(main, [{"name": "s-helper", "role": "helper"},
                        {"name": seat, "role": "director"}])
    _write_seats(wt, [{"name": "s-helper", "role": "helper"},
                      {"name": seat, "role": "prime_director"}])
    monkeypatch.setattr(rotate, "_caller_post", lambda _r: _caller("s-helper",
                                                                   "helper"))
    seen = {}

    def fake_gate(crow, trow, ranks):
        seen["role"] = trow.get("role")
        return "TEST-STOP"

    monkeypatch.setattr(rotate, "_rank_gate", fake_gate)
    rc = rotate.cmd_rotate(SimpleNamespace(post=seat, name=None), wt)
    assert seen.get("role") == "director", (
        "cmd_rotate must read the target row from MAIN, not the worktree")
    assert rc == 3


# --- (d) _caller_post's $AGI_POST path reads MAIN -------------------------

def test_caller_post_env_reads_main_row_from_worktree(tmp_path, monkeypatch):
    """(d) the missing test: from a worktree root, `$AGI_POST` resolves the
    seat's row from MAIN. Held key is B (MAIN's row); the worktree copy names
    stale key A -- pre-fix the env path already used `_seat_read_root`, this
    locks that in."""
    main, wt, seat, pub_a, pub_b = _make_keyed(tmp_path)
    _write_seats(main, [{"name": seat, "role": "director", "window": "@OLD",
                         "pid": 100, "generation": 3, "pubkey": pub_b}])
    _write_seats(wt, [{"name": seat, "role": "director", "window": "@OLD",
                       "pid": 100, "generation": 3, "pubkey": pub_a}])
    monkeypatch.setenv("AGI_POST", seat)
    monkeypatch.delenv("AGI_SEAT", raising=False)
    post, row, how = rotate._caller_post(wt)
    assert (post, how) == (seat, "env"), (post, how)
    assert row["pubkey"] == pub_b, (
        "the $AGI_POST row must come from MAIN, not the worktree copy")