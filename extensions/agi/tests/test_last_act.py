"""The ONE seat-scoped last-act clock (bin/last_act.py).

hypothesis:l4-the-card-age-captive-clocks-the-rotating-seat-own-last-act-never-
a-repo-wide-commit-and-merge-up-in-flight-means-a-real-merge

The falsifier of the OLD clock is test 1: another seat's commit must NOT stale
this seat's card. Tests 2/3 are the ok-unmeasurable rule and the stamp.
Fixtures only — no live hook, tmux or network.
"""
import os
import subprocess
import sys
import time
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[3]
BIN = Path(__file__).resolve().parents[1] / "bin"
sys.path.insert(0, str(BIN))
sys.path.insert(0, str(REPO / "extensions"))

import last_act  # noqa: E402


def _git(repo: Path, *args: str):
    subprocess.run(["git", "-C", str(repo), *args], check=True,
                   capture_output=True, text=True)


@pytest.fixture
def repo(tmp_path):
    """A real git repo whose graph root is `<repo>/.agi`."""
    r = tmp_path / "repo"
    r.mkdir(parents=True)
    _git(r, "init", "-q", "-b", "master")
    _git(r, "config", "user.email", "t@example.com")
    _git(r, "config", "user.name", "t")
    (r / "seed").write_text("x\n")
    _git(r, "add", "seed")
    _git(r, "commit", "-q", "-m", "seed")
    graph = r / ".agi"
    (graph / "nodes" / ".geometry").mkdir(parents=True)
    (graph / "config.json").write_text("{}")
    (graph / "nodes" / ".geometry" / "ladder.md").write_text("{}")
    return r, graph


def test_foreign_commit_never_stales_this_seats_card(repo):
    """THE falsifier: seat B commits a node; seat A's card check stays FRESH.

    Under the old repo-wide clock (`git log -1 --no-merges -- .`) seat B's
    commit was seat A's "last work commit" and re-staled A's card — the loop
    this node removes."""
    r, graph = repo
    card = graph / "sessions" / "quorum" / "seat-a.md"
    card.parent.mkdir(parents=True)
    card.write_text("# seat A card\n")
    _git(r, "add", "-A")
    _git(r, "commit", "-q", "-m", "seat A card")
    # seat B commits a node into the same checkout.
    (graph / "nodes" / "node-b.md").write_text("b\n")
    _git(r, "add", "-A")
    _git(r, "commit", "-q", "-m", "seat B node")
    os.utime(card, (1, 1))          # the card is OLDER than seat B's commit

    stale, act = last_act.card_stale(graph, "seat-a", card)
    assert stale is False, (stale, act)
    # the OLD clock read seat B's commit as newer than A's card -> stale.
    old = subprocess.run(
        ["git", "-C", str(r), "log", "-1", "--no-merges", "--format=%ct",
         "--", "."], capture_output=True, text=True, check=True)
    assert int(old.stdout.strip()) > card.stat().st_mtime


def test_no_stamp_and_no_own_card_commit_is_not_stale(tmp_path):
    """Unmeasurable reads NOT stale (P7): a card with no stamp and no own-card
    commit cannot be judged, and the hook must not hold the rotation on it."""
    graph = tmp_path / "proj" / ".agi"
    (graph / "nodes" / ".geometry").mkdir(parents=True)
    (graph / "config.json").write_text("{}")
    card = graph / "sessions" / "quorum" / "seat-a.md"
    card.parent.mkdir(parents=True)
    card.write_text("# seat A card\n")
    assert last_act.last_act_ts(graph, "seat-a", card) is None
    assert last_act.card_stale(graph, "seat-a", card) == (False, None)


def test_own_stamp_after_the_card_is_stale(tmp_path):
    """An act BY THE SEAT after its card write makes the card stale, and the
    hook's printed exit line names the act it needs (write card, rotate)."""
    graph = tmp_path / "proj" / ".agi"
    (graph / "nodes" / ".geometry").mkdir(parents=True)
    (graph / "config.json").write_text("{}")
    card = graph / "sessions" / "quorum" / "seat-a.md"
    card.parent.mkdir(parents=True)
    card.write_text("# seat A card\n")
    os.utime(card, (1, 1))                   # the card was written earlier
    last_act.touch(graph, "seat-a")          # the seat works AFTER the card
    stamp = last_act.stamp_path(graph, "seat-a")
    assert stamp == graph / "sessions" / "seats" / "seat-a.last-act"
    assert int(stamp.read_text().strip()) > card.stat().st_mtime
    stale, act = last_act.card_stale(graph, "seat-a", card)
    assert stale is True and act is not None
    # a SECOND seat's stamp is never this seat's clock (conjunct 1).
    last_act.touch(graph, "seat-b")
    assert last_act.last_act_ts(graph, "seat-a", card) == act


def test_touch_never_raises_on_an_unwritable_root():
    """P7 fail-open: a stamp that cannot be written returns quietly."""
    last_act.touch("/proc/definitely-not-writable", "seat-a")


# ── the VERB stamps + THE CLOSEOUT HAZARD (conjunct 1) ────────────────────

def _closeout_fixture(tmp_path):
    """A real git repo whose graph root holds a COMMITTED card (so its own
    commit time is measurable) plus the g17.1 node the closeout note writes."""
    r = tmp_path / "repo"
    graph = r / ".agi"
    (graph / "nodes" / "goal").mkdir(parents=True)
    (graph / "nodes" / ".geometry").mkdir(parents=True)
    (graph / "sessions" / "quorum").mkdir(parents=True)
    (graph / "config.json").write_text("{}")
    (graph / "nodes" / "goal" / "g17.1.md").write_text(
        "---\nid: goal:g17.1\ntype: goal\ntitle: g17.1\n---\n\nbody\n")
    card = graph / "sessions" / "quorum" / "seat-a.md"
    card.write_text("# seat A card\n")
    _git(r, "init", "-q", "-b", "master")
    _git(r, "config", "user.email", "t@example.com")
    _git(r, "config", "user.name", "t")
    _git(r, "add", "-A")
    _git(r, "commit", "-q", "-m", "card + node")
    return r, graph, card


def test_rotate_closeout_note_never_restales_the_card_it_just_wrote(
        tmp_path, monkeypatch):
    """THE HAZARD (conjunct 1, measured): the closeout's OWN `write.py
    goal:g17.1 note ...` runs AFTER the rotation wrote the card. Without an
    engine-internal marker its stamp is a FRESH act, so the card the rotation
    just produced reads STALE on the next check -- the loop this node removes.

    Both halves on ONE fixture: the same write.py call WITHOUT the marker
    stales the card; the REAL `_g17_1_note` closeout seam leaves it FRESH."""
    from agi.bin import rotate as _rotate  # noqa: PLC0415
    r, graph, card = _closeout_fixture(tmp_path)
    # the seat resolver: the explicit flag first, then AGI_SEAT; and the
    # engine-internal marker SKIPS the stamp entirely (the closeout's own call).
    monkeypatch.setenv("AGI_SEAT", "seat-env")
    assert last_act.touch_env(graph, "seat-flag") == "seat-flag"
    assert not last_act.stamp_path(graph, "seat-env").exists()
    assert last_act.touch_env(graph) == "seat-env"
    last_act.stamp_path(graph, "seat-flag").unlink()
    monkeypatch.setenv(last_act.INTERNAL_ENV, "1")
    assert last_act.touch_env(graph, "seat-a") == ""
    assert not last_act.stamp_path(graph, "seat-a").exists()
    last_act.stamp_path(graph, "seat-env").unlink()
    monkeypatch.delenv(last_act.INTERNAL_ENV)
    own = last_act.card_commit_ts(graph, card)
    assert own is not None
    # the note runs in a LATER whole second than the card's own commit -- what
    # makes `act > own` true and the hazard real.
    time.sleep(max(0.0, own + 2 - time.time()))

    # (b) FALSIFIER, same fixture: an ordinary write.py call stamps the seat.
    plain = subprocess.run(
        [sys.executable, str(BIN / "write.py"), "goal:g17.1", "note plain",
         "--root", str(graph), "--actor", "seat-a"],
        capture_output=True, text=True, cwd=str(r))
    assert plain.returncode == 0, plain.stderr
    assert last_act.stamp_path(graph, "seat-a").exists()
    assert last_act.card_stale(graph, "seat-a", card)[0] is True
    last_act.stamp_path(graph, "seat-a").unlink()

    # the REAL closeout runner: writes the note, never stamps.
    seams = _rotate._make_closeout_seams(
        graph, {"commit": "abc1234", "facts": ["42"]}, seat="seat-a")
    ok, result, detail = seams["g17_1_note"]()
    assert ok is True, detail
    assert "42 | abc1234" in (graph / "nodes" / "goal" / "g17.1.md").read_text()
    assert not last_act.stamp_path(graph, "seat-a").exists()
    assert last_act.card_stale(graph, "seat-a", card)[0] is False
