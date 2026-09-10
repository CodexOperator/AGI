"""Tests for `cli.py session-complete` — the migration that brings a finished
round's session dir home (hypothesis:l4-session-dirs-come-home-when-the-round-
is-done).

The migration is deliberately built COPY-THEN-VERIFY and tested entirely on
FIxtures: it must never run against the live tree, other seats dispatch while
a round runs, and a live round's `manifest.json` is being written as a
migration would read it. These tests exercise the pure `_session_complete`
function against a synthetic main-graph + worktrees layout in `tmp_path`,
injecting the liveness signal directly so no process table is consulted.
"""
from __future__ import annotations

import filecmp
import importlib.util
import json
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parents[1] / "bin"


def _load_cli():
    spec = importlib.util.spec_from_file_location("agi_cli", BIN / "cli.py")
    cli = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cli)
    return cli


def _make_linked_worktree(main_graph: Path, slug: str, iter_n: str,
                          agents) -> Path:
    """A fake linked worktree under the main graph, holding one iter dir.

    `agents` is a list of `(id, status)` pairs; each gets an `agent.json` plus
    a manifest entry, and the iter dir also carries the round's other files
    (`output.log`, `context.md`). Returns the worktree root.
    """
    wt = main_graph / "worktrees" / slug
    sg = wt / ".agi"
    sg.mkdir(parents=True)
    (sg / "config.json").write_text("{}")
    iter_dir = sg / "sessions" / f"iter-{iter_n}"
    iter_dir.mkdir(parents=True)
    for aid, status in agents:
        d = iter_dir / aid
        d.mkdir()
        (d / "agent.json").write_text(
            json.dumps({"id": aid, "status": status, "victory": True}))
        (d / "scratch.txt").write_text(f"artifact of {aid}\n")
    (iter_dir / "manifest.json").write_text(json.dumps({
        "iter": iter_n,
        "agents": [{"id": aid, "status": status} for aid, status in agents],
    }))
    (iter_dir / "output.log").write_text("round output\n")
    (iter_dir / "context.md").write_text("# round context\n")
    return wt


def _snapshot(root: Path) -> dict:
    """A filesystem snapshot: relative path -> bytes, for every file under
    `root`. Used to prove a dry run writes nothing, and to compare trees."""
    out = {}
    if not root.exists():
        return out
    for p in root.rglob("*"):
        if not p.is_file():
            continue
        out[str(p.relative_to(root))] = p.read_bytes()
    return out


COMPLETE = [("a00-aaa", "done"), ("a00-bbb", "pending")]
RUNNING = [("a00-aaa", "done"), ("a00-ccc", "running")]


@pytest.fixture
def graph(tmp_path: Path):
    """A synthetic main checkout whose worktrees hold an L4.99 iter dir."""
    main = tmp_path / "main"
    main.mkdir(parents=True)
    (main / "config.json").write_text("{}")  # main is itself a graph dir
    return main


def test_complete_iteration_migrates_and_bytes_match(graph, tmp_path):
    """(c) A COMPLETE iteration migrates and its bytes match after."""
    cli = _load_cli()
    src_wt = _make_linked_worktree(graph, "seat-a", "L4.99", COMPLETE)
    src = src_wt / ".agi" / "sessions" / "iter-L4.99"
    before = _snapshot(src)

    rc = cli._session_complete(graph, "L4.99", live_iters=set())
    assert rc == 0
    target = graph / "sessions" / "iter-L4.99"
    assert target.is_dir(), "target iter dir must exist in main after migrate"
    assert not src.exists(), "source worktree dir must be removed after a verified copy"
    assert _snapshot(target) == before, "migrated bytes must equal the originals"


def test_incomplete_iteration_agent_records_are_refused(graph, tmp_path):
    """(d) An INCOMPLETE iteration -- one non-terminal agent record -- is
    REFUSED, not partially moved."""
    cli = _load_cli()
    src_wt = _make_linked_worktree(graph, "seat-a", "L4.99", RUNNING)
    src = src_wt / ".agi" / "sessions" / "iter-L4.99"
    before = _snapshot(src)

    rc = cli._session_complete(graph, "L4.99", live_iters=set())
    assert rc != 0, "an incomplete round must refuse"
    assert src.exists(), "the source must be left untouched"
    assert not (graph / "sessions" / "iter-L4.99").exists(), \
        "nothing may be migrated from an incomplete round"


def test_live_lease_iteration_is_refused(graph, tmp_path):
    """(d) A live spawn-budget lease for the iteration REFUSES it even if its
    agent records look terminal -- the lease is the primary liveness signal."""
    cli = _load_cli()
    src_wt = _make_linked_worktree(graph, "seat-a", "L4.99", COMPLETE)
    src = src_wt / ".agi" / "sessions" / "iter-L4.99"

    rc = cli._session_complete(graph, "L4.99", live_iters={"L4.99"})
    assert rc != 0
    assert src.exists(), "a live round must not be migrated"
    assert not (graph / "sessions" / "iter-L4.99").exists()


def test_dry_run_writes_nothing(graph, tmp_path, capsys):
    """(b) `--dry-run` is proven to write nothing by a filesystem snapshot
    before and after -- not by the absence of an error."""
    cli = _load_cli()
    _make_linked_worktree(graph, "seat-a", "L4.99", COMPLETE)

    before = _snapshot(graph)
    rc = cli._session_complete(graph, "L4.99", live_iters=set(), dry_run=True)
    after = _snapshot(graph)
    assert rc == 0
    assert after == before, "a dry run must not write a single byte"
    out = capsys.readouterr().out
    assert "WOULD migrate" in out
    assert "REFUSE" not in out


def test_failed_verify_leaves_both_sides_intact(graph, tmp_path, monkeypatch):
    """(e) The source is removed only after the copy verifies; a failed verify
    leaves BOTH sides intact."""
    cli = _load_cli()
    src_wt = _make_linked_worktree(graph, "seat-a", "L4.99", COMPLETE)
    src = src_wt / ".agi" / "sessions" / "iter-L4.99"
    before = _snapshot(src)

    monkeypatch.setattr(cli, "_trees_match", lambda s, d: False)
    rc = cli._session_complete(graph, "L4.99", live_iters=set())
    assert rc != 0
    assert src.exists(), "the source must remain when the copy fails to verify"
    assert _snapshot(src) == before, "the source must be byte-identical"
    assert not (graph / "sessions" / "iter-L4.99").exists(), \
        "a partial, unverified destination is removed, not left behind"


def test_target_collision_refuses_without_overwrite(graph, tmp_path):
    """A main checkout that already holds the iter dir is not overwritten --
    migration is a bring-home that never clobbers newer state."""
    cli = _load_cli()
    _make_linked_worktree(graph, "seat-a", "L4.99", COMPLETE)
    target = graph / "sessions" / "iter-L4.99"
    target.mkdir(parents=True)
    (target / "existing.txt").write_text("already here\n")

    rc = cli._session_complete(graph, "L4.99", live_iters=set())
    assert rc != 0
    assert (target / "existing.txt").read_text() == "already here\n", \
        "an existing main iter dir must be left untouched"


def test_worktree_filter_restricts_scope(graph, tmp_path):
    """`worktree=` narrows the scan to one slug; an iter dir in another tree
    is out of scope for that invocation."""
    cli = _load_cli()
    other = _make_linked_worktree(graph, "seat-b", "L4.99", COMPLETE)
    _make_linked_worktree(graph, "seat-a", "L4.99", COMPLETE)
    rc = cli._session_complete(graph, "L4.99", worktree="seat-a",
                               live_iters=set())
    assert rc == 0
    assert (graph / "sessions" / "iter-L4.99").is_dir()
    assert (other / ".agi" / "sessions" / "iter-L4.99").exists(), \
        "the filtered-out worktree must be left untouched"

# ---------------------------------------------------------------------------
# Director follow-up on the merge: `done-unreported` is terminal
# ---------------------------------------------------------------------------

REAPED = [("a00-aaa", "done-unreported")]


def test_a_reaped_round_is_complete(graph, tmp_path):
    """🔴 `done-unreported` is the MOST COMMON ending for a --branch parent.

    Built from a real artefact, not from what the status set happened to
    list: `.agi/sessions/iter-L4.56/manifest.json` on this seat records
    exactly `['done-unreported']`, and so did L4.57's and L4.58's. It is what
    the reaper writes when a round landed and only the report was lost — a
    parent authors no node, and its `cli.py done` reaches its own worktree
    rather than the dispatcher's, so the dispatcher's record never moves off
    it.

    Running `session-complete L4.56 --dry-run` against the live tree
    immediately after this command merged returned "not every agent record is
    terminal; round still running" for a round that had finished hours
    earlier. A refusal wearing a safety message, on precisely the case the
    command exists for.

    `dispatch.py:1738` carries the same four-name set and survives it by
    accident — its reaper loop's second guard (`if status != "running":
    continue`) skips the status the set forgot. Copying the set without the
    guard is what produced the refusal, so this asserts the property on the
    set rather than on any caller's control flow.
    """
    cli = _load_cli()
    wt = _make_linked_worktree(graph, "seat-reaped", "L4.99", REAPED)
    assert "done-unreported" in cli.TERMINAL_STATUSES

    rc = cli._session_complete(graph, "L4.99", live_iters=set())
    assert rc == 0
    assert (graph / "sessions" / "iter-L4.99").is_dir(), (
        "a reaped round must migrate; refusing it makes the command a no-op "
        "for every seat-dispatched parent")
    assert not (wt / ".agi" / "sessions" / "iter-L4.99").exists(), (
        "and the source is gone, because the copy verified")


def test_an_empty_placeholder_target_is_not_a_collision(graph, tmp_path):
    """🔴 dispatch PRE-CREATES `sessions/iter-<id>/` in the main checkout.

    Measured on the live tree the moment this command merged: iter-L4.56,
    .57, .58, .65 and .66 all existed in main with ZERO entries. A guard on
    `target.exists()` therefore refused every round ever dispatched, and the
    command was a complete no-op wearing a safety message.

    The property worth keeping is "never overwrite real data". An empty
    placeholder is not data, and the test below still holds the other half:
    a target with content refuses. The clearing uses `rmdir`, which refuses a
    non-empty directory, so loosening the guard above cannot silently turn
    this into a merge.
    """
    cli = _load_cli()
    wt = _make_linked_worktree(graph, "seat-placeholder", "L4.99", COMPLETE)
    placeholder = graph / "sessions" / "iter-L4.99"
    placeholder.mkdir(parents=True)
    assert not any(placeholder.iterdir()), "sanity: the placeholder is empty"

    rc = cli._session_complete(graph, "L4.99", live_iters=set())
    assert rc == 0
    assert (graph / "sessions" / "iter-L4.99" / "manifest.json").is_file(), (
        "the round must land through an empty placeholder")
    assert not (wt / ".agi" / "sessions" / "iter-L4.99").exists()

# ---------------------------------------------------------------------------
# The merge. A --branch round lives in TWO trees at once, so bringing it home
# is a merge of complementary subtrees, not a copy of one
# (hypothesis:l4-a-round-lives-in-two-trees-so-coming-home-is-a-merge). The
# fixed rules: (1) a file in one source is copied; (2) a path in BOTH sources
# is the interesting case and is decided by content semantics -- never by scan
# or iteration order -- with the LOSER kept recoverable, not deleted;
# (3) verify every byte from every source before removing a source, and remove
# each source only when ITS OWN contribution verifies.
# ---------------------------------------------------------------------------


def test_two_disjoint_sources_merge_into_union(graph, tmp_path):
    """(b) Two source trees with DISJOINT files both land, and the target
    holds the union. This is the whole reason the bring-home became a merge:
    the dispatcher's tree and the child's worktree carry different halves of
    one round, and both must arrive in the same target."""
    cli = _load_cli()
    wa = _make_linked_worktree(graph, "seat-a", "L4.99",
                               [("a00-aaa", "done"), ("a00-bbb", "pending")])
    wb = _make_linked_worktree(graph, "seat-b", "L4.99",
                               [("a00-ccc", "done")])
    (wa / ".agi" / "sessions" / "iter-L4.99" / "a-only.txt").write_text(
        "only A\n")
    (wb / ".agi" / "sessions" / "iter-L4.99" / "b-only.txt").write_text(
        "only B\n")

    rc = cli._session_complete(graph, "L4.99", live_iters=set())
    assert rc == 0
    target = graph / "sessions" / "iter-L4.99"
    for f in ["a-only.txt", "b-only.txt", "manifest.json",
              "output.log", "context.md",
              "a00-aaa/agent.json", "a00-aaa/scratch.txt",
              "a00-ccc/agent.json", "a00-ccc/scratch.txt"]:
        assert (target / f).is_file(), f"{f} must be present in the union"
    # both sources verified their own contribution and were removed
    assert not (wa / ".agi" / "sessions" / "iter-L4.99").exists(), \
        "the disjoint seat-a source verifies and is removed"
    assert not (wb / ".agi" / "sessions" / "iter-L4.99").exists(), \
        "the disjoint seat-b source verifies and is removed"


def test_conflicting_agent_record_status_rule_and_loser_recoverable(graph, tmp_path):
    """(c) The CONFLICTING PATH. A `--branch` round's two trees hold the SAME
    parent `agent.json` and they are two genuinely different documents: the
    dispatcher's reads `done-unreported` (the reaper's view) and the parent's
    own reads `done` (its own, through `cli.py done`). The rule: the more
    authoritative completion status wins -- `done` beats `done-unreported` --
    and the LOSER is preserved recoverably, never deleted. Resolving by scan
    or iteration order would disprove the hypothesis on construction."""
    cli = _load_cli()
    wa = _make_linked_worktree(graph, "seat-dispatcher", "L4.99",
                               [("a00-aaa", "done-unreported")])
    wb = _make_linked_worktree(graph, "seat-parent", "L4.99",
                               [("a00-aaa", "done")])

    rc = cli._session_complete(graph, "L4.99", live_iters=set())
    assert rc == 0
    target = graph / "sessions" / "iter-L4.99"
    winner = json.loads((target / "a00-aaa" / "agent.json").read_text())
    assert winner["status"] == "done", \
        "the agent's own `done` must out-rank the reaper's `done-unreported`"
    # the loser is not deleted -- it is recoverable under .conflicts
    loser = target / ".conflicts" / "a00-aaa" / "agent.json.from-seat-dispatcher"
    assert loser.is_file(), "the losing `done-unreported` record must survive"
    assert json.loads(loser.read_text())["status"] == "done-unreported"
    assert not (wa / ".agi" / "sessions" / "iter-L4.99").exists(), \
        "a losing-but-verifying source still comes home"
    assert not (wb / ".agi" / "sessions" / "iter-L4.99").exists()


def test_source_whose_contribution_fails_verify_is_not_removed(graph, tmp_path,
                                                               monkeypatch):
    """(d) A source is removed only when ITS OWN contribution verifies -- not
    because the target exists and not because a sibling verified. When one
    source's own copy can't be confirmed it stays in its worktree, intact and
    recoverable."""
    cli = _load_cli()
    wa = _make_linked_worktree(graph, "seat-a", "L4.99",
                               [("a00-aaa", "done")])
    wb = _make_linked_worktree(graph, "seat-b", "L4.99",
                               [("a00-bbb", "done")])
    real = cli._source_landed

    def fake_landed(src, target, win, lose):
        if "seat-b" in str(src):
            return False
        return real(src, target, win, lose)

    monkeypatch.setattr(cli, "_source_landed", fake_landed)
    rc = cli._session_complete(graph, "L4.99", live_iters=set())
    assert rc == 0, "the round still lands; only the unverified source stays"
    assert not (wa / ".agi" / "sessions" / "iter-L4.99").exists(), \
        "seat-a's own contribution verified, so it is removed"
    assert (wb / ".agi" / "sessions" / "iter-L4.99").exists(), \
        "a source whose own contribution did not verify must NOT be removed"
    # and the merged target still holds seat-b's disjoint bytes
    assert (graph / "sessions" / "iter-L4.99" / "a00-bbb" / "agent.json").is_file()


def test_dry_run_shows_merge_plan_and_writes_nothing(graph, tmp_path, capsys):
    """(e) `--dry-run` prints the merge plan -- including which source wins
    each conflicting path -- and writes nothing, proven by a filesystem
    snapshot before and after."""
    cli = _load_cli()
    _make_linked_worktree(graph, "seat-dispatcher", "L4.99",
                          [("a00-aaa", "done-unreported")])
    _make_linked_worktree(graph, "seat-parent", "L4.99",
                          [("a00-aaa", "done")])

    before = _snapshot(graph)
    rc = cli._session_complete(graph, "L4.99", live_iters=set(), dry_run=True)
    after = _snapshot(graph)
    assert rc == 0
    assert after == before, "a dry run must not write a single byte"
    out = capsys.readouterr().out
    assert "WOULD migrate" in out
    assert "CONFLICT" in out and "wins over" in out, \
        "the dry run must name each conflicting path and its winner"
    assert "REFUSE" not in out
