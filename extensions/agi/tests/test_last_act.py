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
    # HERMETIC: this agent's own env carries AGI_AGENT_ID/AGI_ACTOR (a spawned
    # kid has both), and after the resolver reorder they would otherwise beat
    # the AGI_SEAT these assertions are about.
    monkeypatch.delenv("AGI_AGENT_ID", raising=False)
    monkeypatch.delenv("AGI_ACTOR", raising=False)
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


# ── the SPAWNED AGENT'S OWN ID, never the inherited seat (SM.48b) ─────────

def _seat_graph(tmp_path) -> Path:
    """A bare graph root the stamp resolves `<root>/sessions/seats/` under."""
    graph = tmp_path / "proj" / ".agi"
    (graph / "nodes" / ".geometry").mkdir(parents=True)
    (graph / "config.json").write_text("{}")
    return graph


def test_spawned_agent_stamps_its_own_id_never_the_inherited_seat(
        tmp_path, monkeypatch):
    """THE HAZARD (measured at the tip): a spawned kid's env carries BOTH
    `AGI_AGENT_ID=a00-x` and the dispatching seat's inherited `AGI_SEAT`
    (dispatch.py survives it through scrubbed_env). Before the reorder the kid
    stamped the DIRECTOR, the director's card read stale although the director
    did nothing -- the rotation loop. Also folds in conjunct 4: a stray USER
    names no seat at all."""
    graph = _seat_graph(tmp_path)
    for k in ("AGI_ACTOR", "AGI_TIER"):
        monkeypatch.delenv(k, raising=False)
    monkeypatch.setenv("AGI_AGENT_ID", "a00-x")
    monkeypatch.setenv("AGI_SEAT", "sensei-director")

    assert last_act.env_seat() == "a00-x"
    assert last_act.touch_env(graph) == "a00-x"
    assert last_act.stamp_path(graph, "a00-x").exists()
    assert not last_act.stamp_path(graph, "sensei-director").exists()

    # conjunct 4: USER alone (no agent id, no seat, no actor) is NOT a seat.
    monkeypatch.delenv("AGI_AGENT_ID")
    monkeypatch.delenv("AGI_SEAT")
    monkeypatch.setenv("USER", "sensei-director")
    assert last_act.env_seat() == ""
    assert last_act.touch_env(graph) == ""
    assert not last_act.stamp_path(graph, "sensei-director").exists()


def test_only_a_seat_env_stamps_that_seat_itself(tmp_path, monkeypatch):
    """A director's OWN acts (its harvest, its sends, its notes) still stale
    its own card: with only AGI_SEAT set the seat is stamped, and it is that
    seat's stamp, not anyone else's."""
    graph = _seat_graph(tmp_path)
    monkeypatch.delenv("AGI_AGENT_ID", raising=False)
    monkeypatch.delenv("AGI_ACTOR", raising=False)
    monkeypatch.delenv("AGI_TIER", raising=False)
    monkeypatch.setenv("AGI_SEAT", "sensei-director")

    assert last_act.env_seat() == "sensei-director"
    assert last_act.touch_env(graph) == "sensei-director"
    assert last_act.stamp_path(graph, "sensei-director").exists()
    assert not last_act.stamp_path(graph, "a00-x").exists()


def test_explicit_actor_beats_the_agent_id_env(tmp_path, monkeypatch):
    """A post acting AS ITSELF passes `--actor <post>`; the flag wins over the
    agent id its own spawn put in env (write.py --actor <post> must still
    stamp the post, not the agent)."""
    graph = _seat_graph(tmp_path)
    monkeypatch.setenv("AGI_AGENT_ID", "a00-x")
    monkeypatch.setenv("AGI_SEAT", "sensei-director")

    assert last_act.env_seat("master-sensei") == "master-sensei"
    assert last_act.touch_env(graph, "master-sensei") == "master-sensei"
    assert last_act.stamp_path(graph, "master-sensei").exists()
    assert not last_act.stamp_path(graph, "a00-x").exists()
    assert not last_act.stamp_path(graph, "sensei-director").exists()


# ── a seat that OWNS ITSELF stales its OWN card (SM.49 conjunct 2) ────────

def test_director_tier_stamps_the_seat_it_owns(tmp_path, monkeypatch):
    """conjunct 2: a DIRECTOR is itself a spawned agent -- dispatch.py exports
    AGI_AGENT_ID, AGI_ACTOR AND AGI_SEAT together (measured from the real
    `dispatch.py --tier director --seat sensei-director --dry-run`) -- so
    keying AGI_AGENT_ID first for everyone re-pointed the director's own clock
    at its agent id and its card never went stale. AGI_TIER=director says the
    actor IS the seat: the seat stamps `<post>.last-act` and the card reads
    STALE, while the agent id is never stamped."""
    graph = _seat_graph(tmp_path)
    monkeypatch.setenv("AGI_TIER", "director")
    monkeypatch.setenv("AGI_AGENT_ID", "dry00-x")
    monkeypatch.setenv("AGI_ACTOR", "dry00-x")
    monkeypatch.setenv("AGI_SEAT", "sensei-director")
    card = graph / "sessions" / "quorum" / "sensei-director.md"
    card.parent.mkdir(parents=True, exist_ok=True)
    card.write_text("card\n")
    # back-date the card so `mtime < act` is decidable inside one test second
    # (git is absent here, so the card's own commit is unmeasurable = None).
    past = time.time() - 10
    os.utime(card, (past, past))

    assert last_act.env_seat() == "sensei-director"
    assert last_act.touch_env(graph) == "sensei-director"
    assert last_act.stamp_path(graph, "sensei-director").exists()
    assert not last_act.stamp_path(graph, "dry00-x").exists()
    assert last_act.card_stale(graph, "sensei-director", card)[0] is True
