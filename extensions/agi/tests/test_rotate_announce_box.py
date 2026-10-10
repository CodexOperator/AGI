"""ROTATION ANNOUNCE OVER BOX (DG4's cut B, DG2 writes the rows FIRST, DG4 builds).

`rotate._announce_rotation`, NON-prime loop (rotate.py:6690-6705 on trunk 19327c2eb2): today it lands the [rotation-alert] block in each receiver's inbox (`send.send`) and in the pairwise dm log (`send.send_dm`). After the build `send.send_dm` is REPLACED by a `box send <recv>` subprocess (the text on STDIN, env AGI_POST=<seat>, a hard timeout of about 20 s, every exception caught). KEPT as today: the `send.send` inbox copy, `send.wake` once per delivered receiver, the whole PRIME branch, the `announced ...` line, the announced_to stamp.

  B1 the REAL `box` piece (`### box` of engine-post.md) mails each receiver: ref refs/box/<seat>/<recv>, signed 'for <seat>@agi', the receiver's `box n` lists the seat, the body IS the text send.send got
  B2 box FORCED TO FAIL three ways (absent from PATH · exits 1 · sleeps past the timeout): ONE warn line naming <recv> per failing receiver, the call RETURNS, delivered = every receiver whose inbox copy landed, elapsed <= timeout + 5 s
  B3 guard: AGI_POST unset, or != seat -> box is NOT called (a recording stub on PATH stays empty), ONE line, delivered unchanged
  B4 an off-matrix receiver (the real box prints [off-matrix], rc 1) = the B2 shape: one warn line, the inbox copy still landed, the matrix-reachable receiver still mailed
  B5 DIFF-SCOPE (AST vs BASE): every top-level def/class of BASE except `_announce_rotation` is identical (new top-level defs must carry `box` in their name); inside `_announce_rotation` the signature and everything before the non-prime `delivered = []` (the PRIME branch) and everything after the non-prime loop are identical
  B6 old route kept: send.send once per receiver (inbox copy), send.wake once per delivered, send.send_dm NOT called in the non-prime loop

Env ANNOUNCE_ROOT=<tree> runs the rows against a scratch tree (extensions/agi/{bin,src} and .agi/nodes/.geometry/engine*.md); default: the repo that holds this file. ANNOUNCE_BASE=<rev> is the BASE of B5 (default: the trunk the rows were cut on; ANNOUNCE_BASE_SRC=<file> gives BASE's rotate.py directly for a tree without .git). Hermetic: send.send / send.wake / send.send_dm and `_derive_receivers` are stubbed at the module seam; the box piece, git and the throwaway ssh keys are REAL, in a scratch repo.
"""
from __future__ import annotations

import ast
import os
import re
import stat
import subprocess
import sys
import time
from pathlib import Path

import pytest

HERE = Path(__file__).resolve()
ROOT = Path(os.environ.get("ANNOUNCE_ROOT") or HERE.parents[3])
EXT = ROOT / "extensions"
BIN = EXT / "agi" / "bin"
sys.path.insert(0, str(EXT))
sys.path.insert(0, str(BIN))
sys.path.insert(0, str(EXT / "agi" / "src"))

from agi.bin import rotate  # noqa: E402
import send  # noqa: E402

BASE_REV = os.environ.get("ANNOUNCE_BASE") or "19327c2eb2"
SEAT = "dg2"
TIMEOUT_CEIL_S = 25.0   # the order's ~20 s hard timeout + 5 s
POSTS = "\n".join([
    '  - {"name":"belam","parent":"owner","harness":"claude"}',
    '  - {"name":"keep","parent":"belam","members":["sm"]}',
    '  - {"name":"sm","parent":"keep","harness":"claude"}',
    '  - {"name":"dg1","parent":"sm","harness":"claude"}',
    '  - {"name":"dg2","parent":"sm","harness":"claude"}',
    '  - {"name":"dg3","parent":"sm","harness":"claude"}',
]) + "\n"
USERS = ["belam", "sm", "dg1", "dg2", "dg3"]


def _sect(name: str) -> str:
    """The body of the ~~~ fence under `### <name>` of the geometry engine*.md files (box-mail.t.sh's sed)."""
    out, hit, fence = [], False, False
    for f in sorted((ROOT / ".agi" / "nodes" / ".geometry").glob("engine*.md")):
        for line in f.read_text(encoding="utf-8").splitlines():
            if re.match(rf"^###* {re.escape(name)} ", line):
                hit, fence = True, False
                continue
            if hit and re.match(r"^###* ", line):
                hit = False
            if hit and line.startswith("~~~"):
                fence = not fence
                continue
            if hit and fence:
                out.append(line)
    return "\n".join(out) + "\n"


def _git(*a, cwd, env=None):
    e = dict(os.environ)
    e.update({"GIT_CONFIG_GLOBAL": "/dev/null", "GIT_CONFIG_SYSTEM": "/dev/null"})
    e.update(env or {})
    return subprocess.run(["git", *a], cwd=str(cwd), env=e, capture_output=True, text=True)


@pytest.fixture
def world(tmp_path, monkeypatch):
    """A scratch git repo with the fixture matrix, a signing config per post, the REAL box piece on PATH as `box`, and a graph root inside the repo (<repo>/.agi) so any cwd the build picks finds the repo."""
    repo = tmp_path / "repo"
    keys, cfg = tmp_path / "k", tmp_path / "c"
    keys.mkdir(), cfg.mkdir()
    signers = tmp_path / "signers"
    signers.write_text("")
    for u in USERS:
        subprocess.run(["ssh-keygen", "-q", "-t", "ed25519", "-N", "", "-f", str(keys / u), "-C", u],
                       check=True, capture_output=True)
        pub = (keys / f"{u}.pub").read_text().split()[:2]
        with open(signers, "a") as fh:
            fh.write(f'{u}@agi namespaces="git" {pub[0]} {pub[1]}\n')
        (cfg / u).write_text(
            f"[user]\n\tname={u}\n\temail={u}@agi\n\tsigningkey={keys / u}\n[gpg]\n\tformat=ssh\n"
            f'[gpg "ssh"]\n\tallowedSignersFile={signers}\n[commit]\n\tgpgsign=false\n')
    geo = repo / ".agi" / "nodes" / ".geometry"
    geo.mkdir(parents=True)
    _git("init", "-q", ".", cwd=repo)
    (geo / "posts.md").write_text(POSTS)
    _git("add", "-A", cwd=repo)
    _git("-c", "user.name=x", "-c", "user.email=x@x", "commit", "-qm", "fixture", cwd=repo)
    # the graph root the announce reads: <repo>/.agi, with a seats sheet (nodes/.geometry/seats.md)
    (repo / ".agi" / "sessions").mkdir(parents=True, exist_ok=True)
    body = "---\nid: config:seats\ntype: config\nseats:\n" + "".join(
        '  - {"name": "%s", "role": "director"}\n' % u for u in USERS) + "---\n"
    (geo / "seats.md").write_text(body, encoding="utf-8")
    bindir = tmp_path / "bin"
    bindir.mkdir()
    box = bindir / "box"
    box.write_text(_sect("box"))
    box.chmod(box.stat().st_mode | stat.S_IXUSR)
    assert box.stat().st_size > 1000, "the box piece did not extract from engine*.md"
    w = type("W", (), {})()
    w.repo, w.root, w.cfg, w.bindir, w.tmp = repo, repo / ".agi", cfg, bindir, tmp_path
    monkeypatch.chdir(repo)
    monkeypatch.setenv("PATH", f"{bindir}:{os.environ['PATH']}")
    monkeypatch.setenv("GIT_CONFIG_GLOBAL", str(cfg / SEAT))
    monkeypatch.setenv("GIT_CONFIG_SYSTEM", "/dev/null")
    monkeypatch.setenv("AGI_POST", SEAT)
    monkeypatch.delenv("AGI_TRUNK", raising=False)
    return w


def _install_box(w, script: str | None):
    """Replace the box on PATH with a stub script (None = remove it: absent from PATH)."""
    b = w.bindir / "box"
    if b.exists():
        b.unlink()
    if script is not None:
        b.write_text(script)
        b.chmod(b.stat().st_mode | stat.S_IXUSR)


class Seams:
    def __init__(self):
        self.sent, self.woke, self.dms = [], [], []


@pytest.fixture
def seams(monkeypatch):
    s = Seams()

    def fake_send(root, to, text, sender=None, *a, **k):
        if to in getattr(s, "inbox_fail", ()):
            raise SystemExit(f"inbox for {to} unwritable")
        s.sent.append((to, text, sender))

    monkeypatch.setattr(send, "send", fake_send)
    monkeypatch.setattr(send, "wake", lambda root, to, *a, **k: s.woke.append(to) or True)
    monkeypatch.setattr(send, "send_dm", lambda *a, **k: s.dms.append((a, k)))
    return s


def _announce(w, monkeypatch, recvs, seat=SEAT):
    monkeypatch.setattr(rotate, "_derive_receivers", lambda root, **kw: list(recvs))
    return rotate._announce_rotation(
        root=w.root, croot=w.tmp / "comms", seat=seat, successor=seat, gen_before=1, gen_after=2,
        trigger="rotate-self", handoff_path=f".agi/sessions/{seat}.md", in_flight="none",
        live_names=[seat, *recvs])


def _as(w, user, *args):
    e = dict(os.environ)
    e.update({"AGI_POST": user, "GIT_CONFIG_GLOBAL": str(w.cfg / user), "GIT_CONFIG_SYSTEM": "/dev/null",
              "AGI_TRUNK": "HEAD"})
    return subprocess.run(["sh", str(w.bindir / "box"), *args], cwd=str(w.repo), env=e, capture_output=True, text=True)


def _warn_lines(err: str, recv: str):
    return [ln for ln in err.splitlines() if recv in ln and not ln.startswith("announced")]


# ---------------------------------------------------------------- B1
def test_b1_real_box_mails_each_receiver(world, seams, monkeypatch, capsys):
    delivered = _announce(world, monkeypatch, ["sm", "dg1"])
    err = capsys.readouterr().err
    assert delivered == ["sm", "dg1"]
    text = seams.sent[0][1]
    assert "[rotation-alert]" in text
    for recv in ("sm", "dg1"):
        ref = f"refs/box/{SEAT}/{recv}"
        assert _git("rev-parse", "-q", "--verify", ref, cwd=world.repo).returncode == 0, f"{ref} missing: {err}"
        v = _git("verify-commit", "--raw", ref, cwd=world.repo, env={"GIT_CONFIG_GLOBAL": str(world.cfg / recv)})
        assert f"for {SEAT}@agi with" in (v.stdout + v.stderr)
        body = _git("log", "-1", "--format=%B", ref, cwd=world.repo).stdout
        assert body.rstrip() == text.rstrip()
        n = _as(world, recv, "n")
        assert SEAT in n.stdout.split(), n.stdout + n.stderr
    assert not [ln for ln in err.splitlines() if ln.startswith("warn")], err


# ---------------------------------------------------------------- B2
FAILS = {
    "absent": None,
    "exit1": "#!/bin/sh\ncat >/dev/null\nexit 1\n",
    "sleeps": "#!/bin/sh\nexec sleep 60\n",
}


@pytest.mark.parametrize("how", ["absent", "exit1", "sleeps"])
def test_b2_box_forced_to_fail(world, seams, monkeypatch, capsys, how):
    _install_box(world, FAILS[how])
    if how == "absent":
        empty = world.tmp / "nopath"
        empty.mkdir()
        monkeypatch.setenv("PATH", str(empty))
    seams.inbox_fail = {"dg3"}
    recvs = ["sm"] if how == "sleeps" else ["sm", "dg1", "dg3"]
    t0 = time.monotonic()
    delivered = _announce(world, monkeypatch, recvs)
    elapsed = time.monotonic() - t0
    err = capsys.readouterr().err
    assert elapsed <= TIMEOUT_CEIL_S, f"{how}: {elapsed:.1f}s"
    want = [r for r in recvs if r != "dg3"]
    assert delivered == want, f"delivered = every receiver whose inbox copy landed: {delivered} {err}"
    for recv in want:
        lines = _warn_lines(err, recv)
        assert len(lines) == 1, f"{how}: ONE warn line naming {recv}: {lines}"
        assert "box" in lines[0].lower(), lines[0]
    assert sorted(t for t, _, _ in seams.sent) == sorted(want)


# ---------------------------------------------------------------- B3
@pytest.mark.parametrize("ambient", [None, "dg1"])
def test_b3_guard_ambient_post_must_be_the_seat(world, seams, monkeypatch, capsys, ambient):
    rec = world.tmp / "box-called"
    _install_box(world, f"#!/bin/sh\necho \"$@\" >> {rec}\ncat >/dev/null\n")
    if ambient is None:
        monkeypatch.delenv("AGI_POST", raising=False)
    else:
        monkeypatch.setenv("AGI_POST", ambient)
    delivered = _announce(world, monkeypatch, ["sm", "dg1"])
    err = capsys.readouterr().err
    assert not rec.exists() or rec.read_text() == "", f"box was called: {rec.read_text()}"
    boxlines = [ln for ln in err.splitlines() if "box" in ln.lower()]
    assert len(boxlines) == 1, f"ONE line: {boxlines}"
    assert delivered == ["sm", "dg1"]
    assert _git("for-each-ref", "refs/box", cwd=world.repo).stdout == ""


# ---------------------------------------------------------------- B4
def test_b4_off_matrix_receiver_is_the_b2_shape(world, seams, monkeypatch, capsys):
    delivered = _announce(world, monkeypatch, ["belam", "sm"])
    err = capsys.readouterr().err
    assert delivered == ["belam", "sm"]
    assert sorted(t for t, _, _ in seams.sent) == ["belam", "sm"]
    lines = _warn_lines(err, "belam")
    assert len(lines) == 1 and "box" in lines[0].lower(), lines
    assert _git("rev-parse", "-q", "--verify", f"refs/box/{SEAT}/belam", cwd=world.repo).returncode != 0
    assert _git("rev-parse", "-q", "--verify", f"refs/box/{SEAT}/sm", cwd=world.repo).returncode == 0
    assert not _warn_lines(err, "sm")


# ---------------------------------------------------------------- B5
def _base_src() -> str:
    if os.environ.get("ANNOUNCE_BASE_SRC"):   # a scratch tree without .git: BASE's rotate.py as a file
        return Path(os.environ["ANNOUNCE_BASE_SRC"]).read_text(encoding="utf-8")
    r = subprocess.run(["git", "show", f"{BASE_REV}:extensions/agi/bin/rotate.py"], cwd=str(HERE.parent),
                       capture_output=True, text=True)
    assert r.returncode == 0, f"BASE {BASE_REV} unreadable: {r.stderr}"
    return r.stdout


def _defs(tree):
    return {n.name: n for n in tree.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))}


def _dump(nodes):
    return [ast.dump(n) for n in nodes]


def _split_announce(fn):
    """(signature, prime preamble = body before the non-prime `delivered = []`, loop, tail after the loop)."""
    body = list(fn.body)
    if body and isinstance(body[0], ast.Expr) and isinstance(getattr(body[0], "value", None), ast.Constant) \
            and isinstance(body[0].value.value, str):
        body = body[1:]   # the docstring may be updated
    loops = [i for i, n in enumerate(body) if isinstance(n, ast.For)
             and isinstance(n.iter, ast.Name) and n.iter.id == "receivers"]
    assert loops, "no top-level `for ... in receivers` loop in _announce_rotation"
    li = loops[-1]
    di = max(i for i in range(li) if isinstance(body[i], ast.Assign)
             and any(isinstance(t, ast.Name) and t.id == "delivered" for t in body[i].targets))
    sig = ast.dump(fn.args) + ast.dump(fn.returns) if fn.returns else ast.dump(fn.args)
    return sig, _dump(body[:di]), body[li], _dump(body[li + 1:])


def test_b5_diff_scope_only_the_nonprime_loop_changes():
    base = ast.parse(_base_src())
    new = ast.parse((BIN / "rotate.py").read_text(encoding="utf-8"))
    bd, nd = _defs(base), _defs(new)
    for name, node in bd.items():
        if name == "_announce_rotation":
            continue
        assert name in nd, f"{name} vanished"
        assert ast.dump(node) == ast.dump(nd[name]), f"{name} changed outside _announce_rotation"
    added = set(nd) - set(bd)
    assert all("box" in n.lower() for n in added), f"new top-level defs without 'box' in the name: {sorted(added)}"
    bs, bpre, _bl, btail = _split_announce(bd["_announce_rotation"])
    ns, npre, _nl, ntail = _split_announce(nd["_announce_rotation"])
    assert bs == ns, "the _announce_rotation signature changed"
    assert bpre == npre, "the prime branch / preamble of _announce_rotation changed"
    assert btail == ntail, "the tail after the non-prime loop (announced line, wake loop, stamp, return) changed"


# ---------------------------------------------------------------- B6
def test_b6_old_route_kept(world, seams, monkeypatch, capsys):
    delivered = _announce(world, monkeypatch, ["sm", "dg1"])
    assert delivered == ["sm", "dg1"]
    assert [(t, s) for t, _, s in seams.sent] == [("sm", SEAT), ("dg1", SEAT)]
    assert seams.woke == ["sm", "dg1"]
    assert seams.dms == [], "send.send_dm is called in the non-prime loop"
    assert "announced rotation -> 2 recipient(s)" in capsys.readouterr().err
