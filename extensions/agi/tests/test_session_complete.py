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


# ---------------------------------------------------------------------------
# Director follow-up on the conflict rule: a MANIFEST is a document too, so a
# conflicting `manifest.json` is a UNION of complementary halves, not a pick
# by slug name (hypothesis:l4-a-manifest-is-a-document-too). An id held by
# one source is kept; an id held by TWO is resolved by the SAME
# `_AGENT_STATUS_RANK` as `agent.json` -- never a second ranking. `.manifest
# .lock` is NOT a document and is dropped from the migration entirely.
# ---------------------------------------------------------------------------


def _manifest_ids(target: Path) -> list:
    return [a["id"] for a in json.loads(
        (target / "manifest.json").read_text())["agents"]]


def test_conflicting_manifests_union_rather_than_slug_winner(graph, tmp_path):
    """(a/b) The two-round manifests are complementary halves, NOT versions.
    A conflict was previously decided by the alphabet (the slug), silently
    discarding one half's agents from the file a later reader opens first.
    Now the conflict is a UNION: three disjoint agents across the two trees
    all survive, and both verbatim manifests are kept recoverable."""
    cli = _load_cli()
    _make_linked_worktree(graph, "a00-04c03dd9", "L4.99",
                          [("a00-aaa", "done-unreported"), ("a00-bbb", "pending")])
    _make_linked_worktree(graph, "sanctuary-director", "L4.99",
                          [("a00-ccc", "done")])

    rc = cli._session_complete(graph, "L4.99", live_iters=set())
    assert rc == 0
    target = graph / "sessions" / "iter-L4.99"
    ids = _manifest_ids(target)
    assert sorted(ids) == ["a00-aaa", "a00-bbb", "a00-ccc"], (
        "the union must carry every agent from BOTH halves, not one source's")
    for slug in ["a00-04c03dd9", "sanctuary-director"]:
        loser = target / ".conflicts" / f"manifest.json.from-{slug}"
        assert loser.is_file(), "each verbatim manifest must stay recoverable"


def test_manifest_entry_sharing_an_id_uses_the_agent_status_rank(graph, tmp_path):
    """(c) An agent id present in BOTH manifests resolves by the SAME
    `_AGENT_STATUS_RANK` as the `agent.json` conflict -- `done` (the actor's
    own record) over `done-unreported` (the reaper's inference). Two rankings
    for one question is the defect this chain removes, so the merged entry
    must match what the `agent.json` rule itself picks."""
    cli = _load_cli()
    _make_linked_worktree(graph, "seat-dispatcher", "L4.99",
                          [("a00-aaa", "done-unreported"), ("a00-bbb", "pending")])
    _make_linked_worktree(graph, "seat-parent", "L4.99",
                          [("a00-aaa", "done")])

    rc = cli._session_complete(graph, "L4.99", live_iters=set())
    assert rc == 0
    target = graph / "sessions" / "iter-L4.99"
    merged = json.loads((target / "manifest.json").read_text())["agents"]
    aaa = next(a for a in merged if a["id"] == "a00-aaa")
    assert aaa["status"] == "done", (
        "a shared manifest id must use `_AGENT_STATUS_RANK`, so `done` beats "
        "`done-unreported` -- the same winner as the agent.json conflict")


def test_manifest_lock_is_not_a_document_and_is_dropped(graph, tmp_path):
    """(d) `.manifest.lock` is a LOCK FILE, not a document. Ranking or
    merging it is meaningless, so it is dropped from the migration entirely:
    never copied, never verified, never a conflict. A source that carries one
    still migrates and verifies, and no `.manifest.lock` reaches the target."""
    cli = _load_cli()
    wt = _make_linked_worktree(graph, "seat-a", "L4.99", COMPLETE)
    src = wt / ".agi" / "sessions" / "iter-L4.99"
    (src / ".manifest.lock").write_text("lock bytes\n")

    rc = cli._session_complete(graph, "L4.99", live_iters=set())
    assert rc == 0, "a lock file must not refuse a complete round"
    target = graph / "sessions" / "iter-L4.99"
    assert not (target / ".manifest.lock").exists(), (
        "a lock file is not data and must not land in main")
    assert (target / "manifest.json").is_file(), (
        "the real manifest still lands")


def test_manifest_lock_dropped_even_across_two_sources(graph, tmp_path):
    """(d2) Two sources that BOTH carry a `.manifest.lock` never conflict on
    it (a lock has no content semantics), the union still forms, and no lock
    file reaches the target."""
    cli = _load_cli()
    wa = _make_linked_worktree(graph, "seat-a", "L4.99",
                               [("a00-aaa", "done"), ("a00-bbb", "pending")])
    wb = _make_linked_worktree(graph, "seat-b", "L4.99", [("a00-ccc", "done")])
    for w in (wa, wb):
        (w / ".agi" / "sessions" / "iter-L4.99" / ".manifest.lock").write_text("x\n")

    rc = cli._session_complete(graph, "L4.99", live_iters=set())
    assert rc == 0
    target = graph / "sessions" / "iter-L4.99"
    assert not (target / ".manifest.lock").exists()
    assert sorted(_manifest_ids(target)) == ["a00-aaa", "a00-bbb", "a00-ccc"]


# ---------------------------------------------------------------------------
# A manifest-LESS partial source never vetoes a round's bring-home
# (hypothesis:l4-a-manifest-less-partial-source-never-vetoes-a-rounds-bring-
# home). An old TWO-worktree round can leave the kid's own tree holding an
# iter dir that carries NO manifest.json -- only its own agent subdir, or
# nothing at all -- while the parent tree holds the manifest and every record.
# Completeness is judged from the manifest-bearing (authority) half only; the
# manifest-less copy is a CONTRIBUTOR that rides into the merge and never
# refuses. Only no-authority-anywhere, or a truly non-terminal authority
# record, refuse.
# ---------------------------------------------------------------------------


def _make_partial_worktree(main_graph: Path, slug: str, iter_n: str,
                           files: dict) -> Path:
    """A fake linked worktree whose iter dir has NO manifest.json -- a
    partial copy of a round (a kid tree that only ever wrote its own agent
    subdir, or nothing). `files` maps relative paths to text content."""
    wt = main_graph / "worktrees" / slug
    sg = wt / ".agi"
    sg.mkdir(parents=True)
    (sg / "config.json").write_text("{}")
    iter_dir = sg / "sessions" / f"iter-{iter_n}"
    iter_dir.mkdir(parents=True)
    for rel, content in files.items():
        p = iter_dir / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content)
    return wt


def test_manifest_less_partial_merges_with_authority_and_never_vetoes(graph,
                                                                      tmp_path):
    """(a) A manifest-bearing all-terminal source + a manifest-LESS partial
    holding a kid's agent subdir: BOTH land in the union, both sources are
    removed, and the partial's bytes are not lost. This is the exact
    two-worktree shape that L4.254 measured refusing on the live tree."""
    cli = _load_cli()
    wa = _make_linked_worktree(graph, "seat-authority", "L4.99", COMPLETE)
    wp = _make_partial_worktree(graph, "seat-partial", "L4.99", {
        "a00-kid/agent.json": json.dumps({"id": "a00-kid", "status": "done"}),
        "a00-kid/scratch.txt": "kid artifact\n",
    })
    src_a = wa / ".agi" / "sessions" / "iter-L4.99"
    src_p = wp / ".agi" / "sessions" / "iter-L4.99"

    rc = cli._session_complete(graph, "L4.99", live_iters=set())
    assert rc == 0, "the partial must never veto a complete authority round"
    target = graph / "sessions" / "iter-L4.99"
    assert (target / "manifest.json").is_file(), "authority's manifest lands"
    assert (target / "a00-kid" / "agent.json").is_file(), \
        "the partial's agent record lands in the union"
    assert (target / "a00-kid" / "scratch.txt").is_file(), \
        "the partial's scratch artifact is not lost"
    assert not src_a.exists(), "authority source comes home"
    assert not src_p.exists(), "partial source comes home after its bytes verify"


def test_manifest_less_partial_dryrun_migrates_both_writes_nothing(graph,
                                                                   tmp_path,
                                                                   capsys):
    """(a2) `--dry-run` for the authority+partial shape prints WOULD migrate
    for BOTH sources, prints no REFUSE, and writes not a byte."""
    cli = _load_cli()
    _make_linked_worktree(graph, "seat-authority", "L4.99", COMPLETE)
    _make_partial_worktree(graph, "seat-partial", "L4.99", {
        "a00-kid/agent.json": '{"id": "a00-kid", "status": "done"}',
    })

    before = _snapshot(graph)
    rc = cli._session_complete(graph, "L4.99", live_iters=set(), dry_run=True)
    after = _snapshot(graph)
    assert rc == 0
    assert after == before, "a dry run must not write a single byte"
    out = capsys.readouterr().out
    assert out.count("WOULD migrate") == 2, \
        "the dry run must name BOTH the authority and the partial source"
    assert "REFUSE" not in out


def test_empty_manifest_less_partial_is_carried_and_removed(graph, tmp_path):
    """(b) The manifest-less partial is an EMPTY dir (the L4.175 residue):
    the round still migrates, the empty source is removed, and the target
    byte-equals the authority's copy."""
    cli = _load_cli()
    wa = _make_linked_worktree(graph, "seat-authority", "L4.99", COMPLETE)
    wp = _make_partial_worktree(graph, "seat-partial", "L4.99", {})
    before = _snapshot(wa / ".agi" / "sessions" / "iter-L4.99")

    rc = cli._session_complete(graph, "L4.99", live_iters=set())
    assert rc == 0
    target = graph / "sessions" / "iter-L4.99"
    assert not (wp / ".agi" / "sessions" / "iter-L4.99").exists(), \
        "an empty partial source is removed after it contributes nothing"
    assert _snapshot(target) == before, \
        "target equals the authority's bytes when the partial is empty"


def test_authority_running_record_still_refuses_naming_agent_and_status(
        graph, tmp_path, capsys):
    """(c) The partial never vetoes, but an AUTHORITY carrying a `running`
    record still refuses the whole round -- and the refusal names the agent
    id and its status, not a vague 'not every agent record is terminal'."""
    cli = _load_cli()
    _make_linked_worktree(graph, "seat-authority", "L4.99", RUNNING)
    _make_partial_worktree(graph, "seat-partial", "L4.99", {
        "a00-kid/agent.json": '{"id": "a00-kid", "status": "done"}',
    })

    rc = cli._session_complete(graph, "L4.99", live_iters=set())
    assert rc != 0, "a non-terminal authority record must still refuse"
    out = capsys.readouterr().out
    assert "a00-ccc" in out and "running" in out, \
        "the refusal names the offending agent id and its status"
    assert "not every agent record" not in out, \
        "the misnaming message is gone"
    assert not (graph / "sessions" / "iter-L4.99").exists(), \
        "nothing moves from a round with a non-terminal authority"


def test_authority_with_empty_agents_list_still_refuses(graph, tmp_path, capsys):
    """(harvest L4.255) An AUTHORITY whose manifest lists NO agents is 'nothing
    to judge' -- the rule `_iteration_agents_complete` states -- and the round
    is refused fail-closed even though a manifest-less partial rides along."""
    cli = _load_cli()
    _make_linked_worktree(graph, "seat-authority", "L4.99", [])
    _make_partial_worktree(graph, "seat-partial", "L4.99", {
        "a00-kid/agent.json": '{"id": "a00-kid", "status": "done"}',
    })

    rc = cli._session_complete(graph, "L4.99", live_iters=set())
    assert rc != 0, "an authority with no agent records must refuse"
    out = capsys.readouterr().out
    assert "no agents in manifest" in out
    assert not (graph / "sessions" / "iter-L4.99").exists(), \
        "nothing moves when there is nothing to judge"


def test_no_authority_no_manifest_anywhere_refuses(graph, tmp_path, capsys):
    """(d) Two manifest-LESS sources and NO manifest-bearing authority: the
    round is refused `no manifest.json in any source`, and nothing moves --
    the 'nothing to judge' safety is unchanged."""
    cli = _load_cli()
    _make_partial_worktree(graph, "seat-p1", "L4.99",
                           {"x/agent.json": '{"id": "x", "status": "done"}'})
    _make_partial_worktree(graph, "seat-p2", "L4.99", {})

    rc = cli._session_complete(graph, "L4.99", live_iters=set())
    assert rc != 0
    out = capsys.readouterr().out
    assert "no manifest.json in any source" in out
    assert not (graph / "sessions" / "iter-L4.99").exists(), \
        "a round with no manifest anywhere must not move"


def test_live_lease_refused_before_partial_carry(graph, tmp_path):
    """(e) A LIVE spawn-budget lease refuses the iteration even when the only
    sources are manifest-less partials -- liveness is judged first."""
    cli = _load_cli()
    _make_partial_worktree(graph, "seat-partial", "L4.99", {})

    rc = cli._session_complete(graph, "L4.99", live_iters={"L4.99"})
    assert rc != 0
    assert not (graph / "sessions" / "iter-L4.99").exists(), \
        "a live lease must refuse before any partial is carried"
