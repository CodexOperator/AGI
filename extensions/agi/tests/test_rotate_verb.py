# test_rotate_verb.py -- SL7.115 `rotate` (the bare verb).
#
# `rotate` IS `rotate-self` for the post whose key the caller holds, with
# every default (name/timeout/force/stops/trigger) derived through the
# SL7.114 resolvers, every rotate-self flag an override, --post rank-gated
# downward only, closeout from the ONE top-level rotate_defaults map. These
# tests monkeypatch
# `rotate.cmd_rotate_self` to CAPTURE the delegated Namespace and return 0, so
# they assert the RESOLUTION + the delegation contract without a real spawn.
# The falsifier "a hand-built Namespace missing a rotate-self attribute" is
# killed by construction: both subparsers declare the SAME flag set through
# `_add_rotate_self_flags` (asserted by the parity test), so the delegated
# namespace carries every attribute the built bytes read.
import argparse
import json
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from agi.bin import rotate
from agi.bin import send


def _write_geo(tmp_path, rows, rotations=None):
    """Fixture root: tmp_path IS the graph dir, seats at
    <root>/nodes/.geometry/posts.md (post-first). A row carries
    name/role/worktree/pubkey."""
    geo = tmp_path / "nodes" / ".geometry"
    geo.mkdir(parents=True, exist_ok=True)
    lines = ["---", "id: config:posts", "posts:"]
    for r in rows:
        lines.append(f"  - name: {r['name']}")
        lines.append(f"    role: {r['role']}")
        if r.get("worktree"):
            lines.append(f"    worktree: {r['worktree']}")
        if r.get("pubkey"):
            lines.append(f"    pubkey: {r['pubkey']}")
    lines.append("---")
    (geo / "posts.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    if rotations is not None:
        (geo / "rotations.md").write_text(rotations, encoding="utf-8")


def _mint(root, seat):
    path, pub = send._mint_seat_key(root, seat, "ed25519")
    assert path is not None
    return path, pub.hex()


def _keyed_posts(root, spec):
    """Rows for `spec` = [(name, role), ...]; every row minted a key and the
    committed row's pubkey set from it (the holds-the-key requirement)."""
    rows = []
    for name, role in spec:
        _p, pubhex = _mint(root, name)
        rows.append({"name": name, "role": role, "pubkey": pubhex})
    return rows


def _parse(argv):
    """Build the `rotate` subparser (flag set + --post) and parse `argv`."""
    sp = argparse.ArgumentParser()
    rotate._add_rotate_self_flags(sp, name_required=False,
                                  timeout_default=None, trigger_default="rotate")
    sp.add_argument("--post", default=None)
    return sp.parse_args(argv)


def _stops_card(root, seat, text):
    """A card for `seat` whose where-it-stops slot carries `text`."""
    card = root / "sessions" / "quorum" / f"{seat}.md"
    card.parent.mkdir(parents=True, exist_ok=True)
    card.write_text(f"# card\n\nlead\n\n## 🔴 Where it stops\n{text}\n",
                    encoding="utf-8")


# --- (1) bare rotate resolves and delegates --------------------------------
def test_bare_rotate_resolves_and_delegates(tmp_path, monkeypatch):
    rows = _keyed_posts(tmp_path, [("prime", "prime_director")])
    _write_geo(tmp_path, rows)
    _stops_card(tmp_path, "prime", "run the suite and report")
    monkeypatch.setenv("AGI_POST", "prime")
    monkeypatch.delenv("AGI_SEAT", raising=False)
    captured = {}
    monkeypatch.setattr(
        rotate, "cmd_rotate_self",
        lambda ns, root: (captured.update(ns=ns), 0)[1])
    code = rotate.cmd_rotate(_parse([]), tmp_path)
    assert code == 0
    ns = captured["ns"]                    # every rotate-self attribute present
    assert ns.name == "prime"              # = the caller's held-key post
    assert ns.timeout == 600               # role default (no template cell)
    assert ns.force is True                # the held key implies it
    assert ns.stops == "run the suite and report"  # the card's slot
    assert ns.trigger == "rotate"          # the rotation record names the verb


# --- (2) no identity -> exit 3, NOTHING delegated ---------------------------
def test_no_identity_refuses_not_delegated(tmp_path, monkeypatch):
    rows = _keyed_posts(tmp_path, [("prime", "prime_director")])
    _write_geo(tmp_path, rows)
    monkeypatch.delenv("AGI_POST", raising=False)
    monkeypatch.delenv("AGI_SEAT", raising=False)
    monkeypatch.setattr(rotate, "_git_toplevel", lambda _c: None)
    called = []
    monkeypatch.setattr(rotate, "cmd_rotate_self",
                        lambda ns, root: (called.append(ns), 0)[1])
    code = rotate.cmd_rotate(_parse([]), tmp_path)
    assert code == 3
    assert called == []                    # NOTHING delegated


# --- (3) --post lower rank -> delegates with name=target --------------------
def test_post_lower_rank_delegates_with_name_target(tmp_path, monkeypatch):
    rows = _keyed_posts(tmp_path, [("prime", "prime_director"),
                                   ("director", "director")])
    _write_geo(tmp_path, rows)
    _stops_card(tmp_path, "director", "close out the round")
    monkeypatch.setenv("AGI_POST", "prime")
    monkeypatch.delenv("AGI_SEAT", raising=False)
    captured = {}
    monkeypatch.setattr(
        rotate, "cmd_rotate_self",
        lambda ns, root: (captured.update(ns=ns), 0)[1])
    code = rotate.cmd_rotate(_parse(["--post", "director"]), tmp_path)
    assert code == 0
    assert captured["ns"].name == "director"   # target == --post
    assert captured["ns"].stops == "close out the round"


# --- (4) --post equal/upward rank -> exit 3, NOTHING delegated --------------
def test_post_equal_rank_refused_not_delegated(tmp_path, monkeypatch):
    rows = _keyed_posts(tmp_path, [("d1", "director"), ("d2", "director")])
    _write_geo(tmp_path, rows)
    monkeypatch.setenv("AGI_POST", "d1")
    monkeypatch.delenv("AGI_SEAT", raising=False)
    called = []
    monkeypatch.setattr(rotate, "cmd_rotate_self",
                        lambda ns, root: (called.append(ns), 0)[1])
    code = rotate.cmd_rotate(_parse(["--post", "d2"]), tmp_path)
    assert code == 3
    assert called == []


# --- (5) explicit --timeout/--stops win (no derivation) ---------------------
def test_explicit_timeout_and_stops_win(tmp_path, monkeypatch):
    rows = _keyed_posts(tmp_path, [("prime", "prime_director")])
    _write_geo(tmp_path, rows)             # NO card: derivation would refuse
    monkeypatch.setenv("AGI_POST", "prime")
    monkeypatch.delenv("AGI_SEAT", raising=False)
    captured = {}
    monkeypatch.setattr(
        rotate, "cmd_rotate_self",
        lambda ns, root: (captured.update(ns=ns), 0)[1])
    code = rotate.cmd_rotate(_parse(["--stops", "hand handoff",
                                     "--timeout", "99"]), tmp_path)
    assert code == 0
    assert captured["ns"].stops == "hand handoff"
    assert captured["ns"].timeout == 99    # the override, never the role default


# --- (6) empty stops slot -> exit 2, NOTHING delegated ----------------------
def test_empty_slot_refuses_exit2_not_delegated(tmp_path, monkeypatch):
    rows = _keyed_posts(tmp_path, [("prime", "prime_director")])
    _write_geo(tmp_path, rows)
    _stops_card(tmp_path, "prime", "")     # slot present but EMPTY
    monkeypatch.setenv("AGI_POST", "prime")
    monkeypatch.delenv("AGI_SEAT", raising=False)
    called = []
    monkeypatch.setattr(rotate, "cmd_rotate_self",
                        lambda ns, root: (called.append(ns), 0)[1])
    code = rotate.cmd_rotate(_parse([]), tmp_path)
    assert code == 2
    assert called == []


# --- (7) --dry-run prints the ONE resolved line, then delegates -------------
def test_dry_run_prints_resolved_line_and_delegates(tmp_path, monkeypatch,
                                                    capsys):
    rows = _keyed_posts(tmp_path, [("prime", "prime_director")])
    _write_geo(tmp_path, rows)
    _stops_card(tmp_path, "prime", "run the suite")
    monkeypatch.setenv("AGI_POST", "prime")
    monkeypatch.delenv("AGI_SEAT", raising=False)
    captured = {}
    monkeypatch.setattr(
        rotate, "cmd_rotate_self",
        lambda ns, root: (captured.update(ns=ns), 0)[1])
    code = rotate.cmd_rotate(_parse(["--dry-run"]), tmp_path)
    assert code == 0
    out = capsys.readouterr().out
    assert "rotate: resolved -> rotate-self --name prime --timeout 600 " \
           "--force --stops 13 chars (from: env; rank: self)" in out
    assert captured["ns"].dry_run is True  # rotate-self's dry-run does the rest


# --- (8) flag parity: rotate accepts EVERY rotate-self flag (+ --post) ------
def test_flag_parity_rotate_is_rotate_self_superset():
    def _opts(parser):
        return set(s for a in parser._actions for s in a.option_strings)
    base = argparse.ArgumentParser()
    sub = base.add_subparsers()
    rs = sub.add_parser("rs")
    rotate._add_rotate_self_flags(rs, name_required=True, timeout_default=600)
    ro = sub.add_parser("ro")
    rotate._add_rotate_self_flags(ro, name_required=False, timeout_default=None,
                                  trigger_default="rotate")
    ro.add_argument("--post", default=None)
    rs_opts, ro_opts = _opts(rs), _opts(ro)
    assert rs_opts <= ro_opts              # every rotate-self flag reaches rotate
    assert "--post" in ro_opts             # the ONE extra (rank-gated target)
    # --name is REQUIRED on rotate-self, OPTIONAL (target default) on rotate:
    assert rs._actions and any(
        a.dest == "name" and a.required for a in rs._actions)
    assert not any(a.dest == "name" and a.required for a in ro._actions)

# --- (10) closeout default from the ONE rotate_defaults map (SL7.117) ----
def test_closeout_default_from_rotate_defaults_map(tmp_path, monkeypatch):
    """cmd_rotate reads the closeout boolean PER ROLE from the top-level
    rotate_defaults.closeout map -- true, false, or absent -- never from
    templates.<role>.rotate_defaults (the per-template cell write.py cannot
    nest on config:rotations)."""
    rows = _keyed_posts(tmp_path, [("prime", "prime_director")])
    _stops_card(tmp_path, "prime", "close out the round")
    monkeypatch.setenv("AGI_POST", "prime")
    monkeypatch.delenv("AGI_SEAT", raising=False)

    def _run(rotations, want):
        _write_geo(tmp_path, rows, rotations=rotations)
        captured = {}
        monkeypatch.setattr(
            rotate, "cmd_rotate_self",
            lambda ns, root: (captured.update(ns=ns), 0)[1])
        code = rotate.cmd_rotate(_parse([]), tmp_path)
        assert code == 0
        assert getattr(captured["ns"], "closeout") is want

    # true -> closeout; false -> not; absent role -> not
    _run("---\nid: config:rotations\nrotate_defaults:\n"
         "  closeout:\n    prime_director: true\n---\n", True)
    _run("---\nid: config:rotations\nrotate_defaults:\n"
         "  closeout:\n    prime_director: false\n---\n", False)
    _run("---\nid: config:rotations\nrotate_defaults:\n  closeout: {}\n---\n",
         False)   # absent role -> False, never a fallback to templates

# --- (9) --dry-run never len(None): --stops-file / --closeout (SL7.115) -----
def test_dry_run_stops_file_and_closeout_no_traceback(tmp_path, monkeypatch,
                                                      capsys):
    rows = _keyed_posts(tmp_path, [("prime", "prime_director")])
    _write_geo(tmp_path, rows)             # no card: derivation would refuse,
    monkeypatch.setenv("AGI_POST", "prime")   # but --stops-file/--closeout
    monkeypatch.delenv("AGI_SEAT", raising=False)  # skip the derivation
    for argv, tok, field, value in (
            (["--dry-run", "--stops-file", "F"], "--stops-file F",
             "stops_file", "F"),
            (["--dry-run", "--closeout"], "--closeout", "closeout", True)):
        captured = {}
        monkeypatch.setattr(
            rotate, "cmd_rotate_self",
            lambda ns, root: (captured.update(ns=ns), 0)[1])
        code = rotate.cmd_rotate(_parse(argv), tmp_path)
        assert code == 0
        out = capsys.readouterr().out
        assert "rotate: resolved -> rotate-self --name prime " \
               "--timeout 600 --force" in out
        assert tok in out                # truthful token, not len(None)
        assert captured["ns"].dry_run is True
        assert getattr(captured["ns"], field) == value   # carried unchanged


# --- SL7.116 stale where-it-stops gate -------------------------------------
# goal:g15.25 residue (SL7.115): a DERIVED default that is byte-identical to
# the slot at the seat's most recent rotate-out commit is a STALE predecessor
# block, refused BY NAME (exit 2) -- NOT handed to the successor as fresh.
# These tests run cmd_rotate against a tmp GIT repo whose card is committed
# under the exact `_commit_stops_row` message shape, so the gate's
# `git log --grep='^<seat> rotate-out gen '` finds it.

def _git_init(tmp_path):
    subprocess.run(["git", "-C", str(tmp_path), "init", "-q"],
                   check=True, capture_output=True)
    subprocess.run(["git", "-C", str(tmp_path), "config", "user.email", "t@t"],
                   check=True, capture_output=True)
    subprocess.run(["git", "-C", str(tmp_path), "config", "user.name", "t"],
                   check=True, capture_output=True)


def _commit_all(tmp_path, msg):
    subprocess.run(["git", "-C", str(tmp_path), "add", "-A"],
                   check=True, capture_output=True)
    subprocess.run(["git", "-C", str(tmp_path), "commit", "-q", "-m", msg],
                   check=True, capture_output=True)


# --- (10) unchanged slot since the predecessor's rotate-out -> exit 2 ------
def test_stale_stops_slot_refuses_by_name_not_delegated(tmp_path, monkeypatch,
                                                        capsys):
    rows = _keyed_posts(tmp_path, [("prime", "prime_director")])
    _write_geo(tmp_path, rows)
    _git_init(tmp_path)
    _stops_card(tmp_path, "prime", "run the suite and report")  # predecessor text
    _commit_all(tmp_path, "prime rotate-out gen 4->5: run the suite")
    # the current card is UNCHANGED (same slot text): STALE, refuse by name.
    monkeypatch.setenv("AGI_POST", "prime")
    monkeypatch.delenv("AGI_SEAT", raising=False)
    called = []
    monkeypatch.setattr(rotate, "cmd_rotate_self",
                        lambda ns, root: (called.append(ns), 0)[1])
    code = rotate.cmd_rotate(_parse([]), tmp_path)
    assert code == 2
    err = capsys.readouterr().err
    assert "STALE" in err
    assert "rotate-out gen 4->5" in err        # the gen pair is named
    assert "write the card where-it-stops section or pass --stops" in err
    assert called == []                         # NOTHING delegated


# --- (11) rewritten slot during this generation -> delegated ---------------
def test_rewritten_slot_delegates(tmp_path, monkeypatch):
    rows = _keyed_posts(tmp_path, [("prime", "prime_director")])
    _write_geo(tmp_path, rows)
    _git_init(tmp_path)
    _stops_card(tmp_path, "prime", "run the suite and report")  # predecessor text
    _commit_all(tmp_path, "prime rotate-out gen 4->5: run the suite")
    _stops_card(tmp_path, "prime", "hand off the round")         # REWRITTEN
    monkeypatch.setenv("AGI_POST", "prime")
    monkeypatch.delenv("AGI_SEAT", raising=False)
    captured = {}
    monkeypatch.setattr(rotate, "cmd_rotate_self",
                        lambda ns, root: (captured.update(ns=ns), 0)[1])
    code = rotate.cmd_rotate(_parse([]), tmp_path)
    assert code == 0
    assert captured["ns"].stops == "hand off the round"
    # the geared sha256 rides the delegated namespace for the started record.
    import hashlib
    assert captured["ns"].stops_sha256 == hashlib.sha256(
        "hand off the round".encode()).hexdigest()


# --- (12) no rotate-out commit (a first seating) -> delegated --------------
def test_no_rotate_out_commit_delegates(tmp_path, monkeypatch):
    rows = _keyed_posts(tmp_path, [("prime", "prime_director")])
    _write_geo(tmp_path, rows)
    _git_init(tmp_path)
    _stops_card(tmp_path, "prime", "run the suite and report")
    _commit_all(tmp_path, "init")              # NOT a rotate-out message
    monkeypatch.setenv("AGI_POST", "prime")
    monkeypatch.delenv("AGI_SEAT", raising=False)
    captured = {}
    monkeypatch.setattr(rotate, "cmd_rotate_self",
                        lambda ns, root: (captured.update(ns=ns), 0)[1])
    code = rotate.cmd_rotate(_parse([]), tmp_path)
    assert code == 0                            # no rotate-out commit -> None
    assert captured["ns"].stops == "run the suite and report"


# --- (13) explicit --stops with a STALE slot -> delegated (gate skipped) ----
def test_explicit_stops_with_stale_slot_delegates(tmp_path, monkeypatch):
    rows = _keyed_posts(tmp_path, [("prime", "prime_director")])
    _write_geo(tmp_path, rows)
    _git_init(tmp_path)
    _stops_card(tmp_path, "prime", "run the suite and report")  # stale slot
    _commit_all(tmp_path, "prime rotate-out gen 4->5: run the suite")
    monkeypatch.setenv("AGI_POST", "prime")
    monkeypatch.delenv("AGI_SEAT", raising=False)
    captured = {}
    monkeypatch.setattr(rotate, "cmd_rotate_self",
                        lambda ns, root: (captured.update(ns=ns), 0)[1])
    code = rotate.cmd_rotate(_parse(["--stops", "fresh handoff"]), tmp_path)
    assert code == 0                            # explicit --stops never gated
    assert captured["ns"].stops == "fresh handoff"


# --- (14) the started record seals stops_sha256 and a rewrite keeps it -----
def test_started_record_seals_stops_sha256(tmp_path):
    import hashlib
    stops = "run the suite and report"
    target = hashlib.sha256(stops.encode()).hexdigest()
    path = tmp_path / "rec.json"
    rotate._write_rotate_self_started(path, seat="prime", steps=["handoff"],
                                      stops_sha256=target)
    rec = json.loads(path.read_text(encoding="utf-8"))
    assert rec["stops_sha256"] == target
    # a LATER rebuild of the SAME file (no arg) must not drop it (preserve):
    rotate._write_rotate_self_started(path, seat="prime",
                                      steps=["handoff", "spawn"])
    rec2 = json.loads(path.read_text(encoding="utf-8"))
    assert rec2["stops_sha256"] == target
