"""hypothesis:l4-remote-thought-town-a-box-cell-one-guard-and-a-five-minute-
mail-poll-verified-on-a-stand-in-box.

One box-membership guard (`bin/boxes.py`) with three call sites (send whois +
nudge, heal watch, rotate status), a crons job-level `box` filter plus a
`mail_poll` job, and a service reader (`send.py read --box-local`).
"""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parents[1] / "bin"
sys.path.insert(0, str(BIN))

import boxes  # noqa: E402


def _graph(tmp: Path, default_box: str = "core-town",
           rows: list[dict] | None = None) -> Path:
    """A minimal graph root (the `.agi` dir) envfile/locations can resolve."""
    root = tmp / ".agi"
    (root / "nodes" / ".geometry").mkdir(parents=True, exist_ok=True)
    (root / "config.json").write_text("{}\n")
    body = "---\nid: config:posts\ntype: config\n"
    if default_box:
        body += f"default_box: {default_box}\n"
    body += "posts:\n"
    for r in rows or []:
        body += "  - " + __import__("json").dumps(r) + "\n"
    body += "---\n"
    (root / "nodes" / ".geometry" / "posts.md").write_text(body)
    return root


@pytest.fixture(autouse=True)
def _no_ambient_box(monkeypatch):
    monkeypatch.delenv("AGI_BOX", raising=False)


# (2) no cell = the default box, and the default box is local to itself.
def test_no_box_cell_is_default_box_and_local(tmp_path):
    root = _graph(tmp_path, "core-town",
                  rows=[{"name": "a", "pid": 1},
                        {"name": "b", "pid": 2, "box": "local-town"}])
    assert boxes.this_box(root) == "core-town"
    assert boxes.default_box(root) == "core-town"
    assert boxes.row_is_local(root, {"name": "a"})
    assert not boxes.row_is_local(root, {"name": "b", "box": "local-town"})


# (3) this box comes from AGI_BOX in the env; unset falls back to default.
def test_this_box_reads_agi_box_env(tmp_path, monkeypatch):
    root = _graph(tmp_path, "core-town")
    monkeypatch.setenv("AGI_BOX", "local-town")
    assert boxes.this_box(root) == "local-town"
    # A boxless row is the DEFAULT box, so it is now foreign to local-town.
    assert not boxes.row_is_local(root, {"name": "a"})
    monkeypatch.delenv("AGI_BOX")
    assert boxes.this_box(root) == "core-town"


# (1) whois never asserts a foreign row's window; heal and status skip it.
def test_foreign_rows_skipped_by_name_at_every_call_site(tmp_path, monkeypatch):
    root = _graph(tmp_path, "core-town")
    foreign = {"name": "foreign-seat", "role": "director",
               "pid": 222, "window": "@999", "box": "local-town"}
    local = {"name": "local-seat", "role": "director", "pid": 111,
             "window": "@111"}

    import send
    code, text = send._whois_answer(foreign, "by name: foreign-seat", None, root)
    assert code == send.WHOIS_OK
    assert "foreign: window @999 not this box's" in text
    assert "box local-town" in text
    _c, ltext = send._whois_answer(local, "by name: local-seat", None, root)
    assert "window @111" in ltext

    monkeypatch.setattr(send, "_locally_loaded_rows", lambda r: [foreign, local])
    monkeypatch.setattr(send, "_window_id_listed", lambda *a, **k: True)
    assert send._nudge_target(root, "foreign-seat", None) is None
    assert send._nudge_target(root, "local-seat", None) is not None

    import heal
    import rotate
    monkeypatch.setattr(rotate, "_load_seats", lambda r: [local, foreign])
    monkeypatch.setattr(heal, "_all_windows", lambda p=None: [])
    monkeypatch.setattr(heal, "_load_launcher", lambda l: None)
    monkeypatch.setattr(heal, "_pin_table", lambda r, rows: ({}, []))
    acted, logs = [], []
    monkeypatch.setattr(heal, "_watch_one_seat",
                        lambda *a, **k: acted.append(a[1]["name"]) or {})
    monkeypatch.setattr(heal, "_watch_log", lambda line: logs.append(line))
    heal._watch_seats(root)
    assert acted == ["local-seat"]
    assert any("foreign-seat" in ln for ln in logs)

    import argparse
    monkeypatch.setattr(rotate, "_load_seats", lambda r: [local, foreign])
    monkeypatch.setattr(rotate, "_read_generation", lambda r, s: 0)
    monkeypatch.setattr(rotate, "_seat_fraction", lambda r, row: 0.0)
    monkeypatch.setattr(rotate, "find_pin_log", lambda r, s: None)
    rc = rotate.cmd_status(argparse.Namespace(seats=True, record=None), root)
    assert rc == 0


# (4) crons box filter: core byte-identical with no box fields; the live node
# renders core = grid_sync + mirror + branch_push and local = branch_push + mail.
def test_crons_box_filter_core_unchanged_and_local_mail_only(tmp_path):
    import crons
    root = _graph(tmp_path, "core-town")
    repo = tmp_path
    subprocess.run(["git", "init", "-q", str(repo)], check=True)
    subprocess.run(["git", "-C", str(repo), "config", "user.email", "t@t"],
                   check=True)
    subprocess.run(["git", "-C", str(repo), "config", "user.name", "t"],
                   check=True)
    (repo / "f").write_text("x")
    subprocess.run(["git", "-C", str(repo), "add", "f"], check=True)
    subprocess.run(["git", "-C", str(repo), "commit", "-qm", "i"], check=True)

    def job(**kw):
        return {"enabled": True, "every_mins": 5, "schedule": None, **kw}

    no_box = {"crons_live": True, "jobs": {"grid_sync": job(),
              "branch_push": {"enabled": True, "every_mins": None,
                              "schedule": "7 * * * *"}}}
    core = crons.render_managed_lines(root, repo, repo, no_box,
                                      box_name="core-town")
    local = crons.render_managed_lines(root, repo, repo, no_box,
                                       box_name="local-town")
    assert core == local  # no box fields at all -> every box, unchanged

    with_box = {"crons_live": True, "jobs": {
        "grid_sync": job(box="core-town"),
        "branch_push": {"enabled": True, "every_mins": None,
                        "schedule": "7 * * * *"},
        "mail_poll": job(box="local-town")}}
    core2 = crons.render_managed_lines(root, repo, repo, with_box,
                                       box_name="core-town")
    local2 = crons.render_managed_lines(root, repo, repo, with_box,
                                        box_name="local-town")
    assert core2 == core  # core-town crontab byte-identical to today
    assert len(local2) == 2
    assert any("--box-local" in ln for ln in local2)
    # SM.123 conjunct 2: the SAME tick receives the migrate record.
    assert any("migrate --receive" in ln for ln in local2)
    assert any("push" in ln for ln in local2)
    assert not any("grid.py commit" in ln for ln in local2)


# (6) no RUNABLE literal box alias in any engine script (comments/docstrings
# are prose, matching test_no_literal_town.py's AST rule; season.py carries
# 'core-town' in a comment and is not an offender).
def test_no_literal_box_alias_in_bin():
    import ast
    offenders = []
    for f in sorted(BIN.glob("*.py")):
        tree = ast.parse(f.read_text(encoding="utf-8"))
        for n in ast.walk(tree):
            if (isinstance(n, ast.Constant) and isinstance(n.value, str)
                    and n.value in ("core-town", "local-town")):
                offenders.append(f"{f.name}: literal {n.value!r}")
    assert not offenders, "\n".join(offenders)


# (5) one mail_poll tick through a bare hub: a dm committed on the core side
# is read on the stand-in within one fetch, and a foreign row is skipped.
def test_mail_poll_one_tick_through_bare_hub(tmp_path, monkeypatch, capsys):
    hub = tmp_path / "hub.git"
    subprocess.run(["git", "init", "-q", "--bare", str(hub)], check=True)
    core = tmp_path / "core"
    core.mkdir()
    _graph(core, "core-town", rows=[
        {"name": "core-seat", "pid": 1},
        {"name": "far-seat", "pid": 2, "box": "local-town"}])
    subprocess.run(["git", "init", "-q", str(core)], check=True)
    subprocess.run(["git", "-C", str(core), "config", "user.email", "t@t"],
                   check=True)
    subprocess.run(["git", "-C", str(core), "config", "user.name", "t"],
                   check=True)
    sessions = core / ".agi" / "sessions" / "inbox"
    sessions.mkdir(parents=True)
    sessions.joinpath("far-seat.md").write_text(
        "---\nts: 2026-09-18T00:00:00Z\nfrom: core-seat\nto: far-seat\n"
        "text: hello across boxes\n---\n")
    subprocess.run(["git", "-C", str(core), "add", "-A"], check=True)
    subprocess.run(["git", "-C", str(core), "commit", "-qm", "dm"], check=True)
    subprocess.run(["git", "-C", str(core), "remote", "add", "origin",
                    str(hub)], check=True)
    subprocess.run(["git", "-C", str(core), "push", "-q", "origin", "HEAD"],
                   check=True)

    standin = tmp_path / "standin"
    subprocess.run(["git", "clone", "-q", str(hub), str(standin)], check=True)
    # The stand-in declares itself local-town via AGI_BOX (env seam).
    monkeypatch.setenv("AGI_BOX", "local-town")
    monkeypatch.chdir(standin)
    (standin / ".env").write_text("AGI_BOX=local-town\n")
    subprocess.run(["git", "-C", str(standin), "fetch", "-q", "origin"],
                   check=True)
    import send
    rc = send.main(["read", "--box-local"])
    out = capsys.readouterr()
    assert rc == 0
    assert "hello across boxes" in out.out
    assert "core-seat" in out.err and "foreign-box" in out.err
