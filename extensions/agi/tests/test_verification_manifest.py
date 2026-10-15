"""Experiment for hypothesis:l4-the-never-lower-baseline-counts-committed-
node-files-and-records-the-manifest-so-a-drop-names-the-file.

THE CLAIM (four conjuncts):

1. the stamped count is a COMMITTED count — a stamp taken while the stamping
   checkout holds an untracked/modified node REFUSES BY NAME and writes
   nothing (never a working-tree count);
2. the stamp records the committed FILE MANIFEST beside the numbers;
3. a real drop NAMES THE MISSING FILES, not `2841 vs 2840`;
4. both sides of a comparison are committed manifests, so an untracked file on
   either side never enters either set.

FALSIFIERS: a stamp taken with an untracked node present that does not refuse;
a drop report with no file name; a worktree read that counts an untracked file.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

BIN = Path(__file__).resolve().parent.parent / "bin"
SRC = Path(__file__).resolve().parent.parent / "src"
sys.path.insert(0, str(BIN))
sys.path.insert(0, str(SRC))

import verification  # noqa: E402

BRANCH = "season2/main"


def _sp(*args, **kw):
    return subprocess.run(*args, check=True, capture_output=True, text=True, **kw)


def _init_fixture(tmp_path: Path) -> Path:
    """A git repo on the integration branch with a bare origin, HEAD pushed,
    and two COMMITTED node files."""
    root = tmp_path / "repo"
    nd = root / ".agi" / "nodes" / "hypothesis"
    nd.mkdir(parents=True)
    (root / ".agi" / "nodes" / ".geometry").mkdir(parents=True)
    (root / ".agi" / "nodes" / ".geometry" / "ladder.md").write_text(
        f"---\nid: ladder:ladder\ntype: ladder\ntown_branches:\n"
        f"  core: {BRANCH}\n---\n# ladder\n\n")
    for name in ("a", "b"):
        (nd / f"{name}.md").write_text(
            f"---\nid: hypothesis:{name}\ntype: hypothesis\nstatus: active\n"
            f"---\n# {name}\n")
    _sp(["git", "init", "-b", BRANCH], cwd=root)
    _sp(["git", "config", "user.email", "t@t"], cwd=root)
    _sp(["git", "config", "user.name", "t"], cwd=root)
    _sp(["git", "add", "-A"], cwd=root)
    _sp(["git", "commit", "-m", "init"], cwd=root)
    _sp(["git", "init", "--bare", str(tmp_path / "origin.git")], cwd=tmp_path)
    _sp(["git", "remote", "add", "origin", str(tmp_path / "origin.git")],
        cwd=root)
    _sp(["git", "push", "-u", "origin", BRANCH], cwd=root)
    return root


CURRENT = {"active": 3, "deprecated": 0, "total": 3}


def test_untracked_node_makes_the_stamp_refuse_by_name(tmp_path):
    """The measured SM.33 defect: MAIN mid-mint of an untracked node stamped
    an inflated baseline. The stamp must now REFUSE and name the file, leaving
    no baseline behind."""
    root = _init_fixture(tmp_path)
    groot = root / ".agi"
    untracked = groot / "nodes" / "hypothesis" / "untracked-mint.md"
    untracked.write_text("---\nid: hypothesis:untracked\ntype: hypothesis\n"
                         "status: active\n---\n# untracked\n")
    r = verification.compare_count(groot, CURRENT)
    assert r.status == "PASS", r.note
    assert "refused by name" in r.note, r.note
    assert "untracked-mint.md" in r.note, r.note
    assert not (groot / "sessions" / verification.STATE_FILE).exists(), (
        "a stamp over an uncommitted node must never be recorded")


def test_stamped_manifest_is_committed_only_and_matches_head_tree(tmp_path):
    """The recorded manifest is the COMMITTED node set — byte-for-byte the
    `git ls-tree -r HEAD -- nodes` answer — and an untracked node in the same
    checkout never enters it. `_node_manifest` must read HEAD, not the INDEX:
    `git ls-files` would admit a staged-but-uncommitted node (SM.34
    conjunct 2)."""
    root = _init_fixture(tmp_path)
    groot = root / ".agi"
    r = verification.compare_count(groot, CURRENT)
    assert "baseline recorded" in r.note, r.note
    committed = _sp(["git", "-C", str(groot), "ls-tree", "-r", "--name-only",
                     "HEAD", "--", "nodes"]).stdout.split()
    manifest = verification._node_manifest(groot)
    assert manifest == sorted(committed), (manifest, committed)
    assert all(p.endswith(".md") or "/.geometry/" in p for p in manifest)
    # a STAGED-but-uncommitted node never enters the committed manifest either
    staged = groot / "nodes" / "hypothesis" / "staged-only.md"
    staged.write_text("---\nid: hypothesis:staged\ntype: hypothesis\n"
                      "status: active\n---\n# staged\n")
    _sp(["git", "add", ".agi/nodes/hypothesis/staged-only.md"], cwd=root)
    index = _sp(["git", "-C", str(groot), "ls-files", "--", "nodes"]
                ).stdout.split()
    assert any("staged-only" in p for p in index), "fixture: staged node"
    fresh = verification._node_manifest(groot)
    assert not any("staged-only" in p for p in fresh), (
        "the INDEX is not a commit: a staged node entered the manifest", fresh)
    # an untracked node minted AFTER the stamp never enters the recorded set
    (groot / "nodes" / "hypothesis" / "untracked-only.md").write_text(
        "---\nid: hypothesis:x\ntype: hypothesis\nstatus: active\n---\n# x\n")
    assert not any("untracked-only" in p
                   for p in verification._node_manifest(groot))
    doc = json.loads((groot / "sessions" / verification.STATE_FILE).read_text())
    # kid 1's `_stamped_manifest` records `{path: mint_id}`; the KEYS are the
    # committed manifest. This assertion still says "committed only".
    assert isinstance(doc["manifest"], dict)
    assert sorted(doc["manifest"]) == manifest and doc["manifest_sha256"]


def test_parent_probe_inflated_worktree_count_cannot_mask_a_drop(tmp_path):
    """THE parent probe (SM.34): stamp on MAIN; a worktree COMMITS the loss of
    a committed node and mints an untracked filler so the working-tree count
    is restored to 3. The gate must FAIL on the COMMITTED count (2) and name
    `b.md`, never PASS on `current['active']=3`."""
    root = _init_fixture(tmp_path)
    groot = root / ".agi"
    assert "baseline recorded" in verification.compare_count(groot, CURRENT).note
    wt = tmp_path / "wt"
    _sp(["git", "worktree", "add", "--detach", str(wt), "HEAD"], cwd=root)
    _sp(["git", "rm", ".agi/nodes/hypothesis/b.md"], cwd=wt)
    _sp(["git", "-c", "user.email=t@t", "-c", "user.name=t", "commit",
         "--no-verify", "-m", "lost b"], cwd=wt)
    (wt / ".agi" / "nodes" / "hypothesis" / "untracked-filler.md").write_text(
        "---\nid: hypothesis:f\ntype: hypothesis\nstatus: active\n---\n# f\n")
    # the baseline the worktree reads: `_read_state` looks in the local
    # sessions dir, so the position MAIN stamped is copied there
    wss = wt / ".agi" / "sessions"
    wss.mkdir(parents=True, exist_ok=True)
    (wss / verification.STATE_FILE).write_bytes(
        (groot / "sessions" / verification.STATE_FILE).read_bytes())
    r = verification.compare_count(wt / ".agi",
                                   {"active": 3, "deprecated": 0, "total": 3})
    assert r.status == "FAIL", (
        "an untracked filler masked a committed drop: " + r.note)
    assert "missing committed file(s)" in r.note and "b.md" in r.note, r.note
    assert "committed total=2" in r.note, r.note


def test_a_drop_names_the_missing_committed_file(tmp_path):
    """Conjunct 3: `current.active < state.active` prints the SET DIFFERENCE of
    the stamped manifest against the current one — the lost file's name."""
    root = _init_fixture(tmp_path)
    groot = root / ".agi"
    assert "baseline recorded" in verification.compare_count(
        groot, CURRENT).note
    # a committed node disappears (deleted and committed)
    _sp(["git", "rm", ".agi/nodes/hypothesis/b.md"], cwd=root)
    _sp(["git", "commit", "-m", "delete b"], cwd=root)
    r = verification.compare_count(groot, {"active": 2, "deprecated": 0,
                                           "total": 2})
    assert r.status == "FAIL", r.note
    assert "missing committed file(s)" in r.note, r.note
    assert "b.md" in r.note, r.note


def test_worktree_manifest_matches_main_and_excludes_untracked(tmp_path):
    """Conjunct 4: an untracked file on EITHER side never enters either set,
    so a worktree holding the same commits reads the same manifest as MAIN."""
    root = _init_fixture(tmp_path)
    groot = root / ".agi"
    wt = tmp_path / "wt"
    _sp(["git", "worktree", "add", "--detach", str(wt), "HEAD"], cwd=root)
    (groot / "nodes" / "hypothesis" / "main-untracked.md").write_text(
        "---\nid: hypothesis:y\ntype: hypothesis\nstatus: active\n---\n# y\n")
    main_manifest = verification._node_manifest(groot)
    wt_manifest = verification._node_manifest(wt / ".agi")
    assert main_manifest == wt_manifest, (main_manifest, wt_manifest)
    assert not any("main-untracked" in p for p in wt_manifest)
    assert not any("main-untracked" in p for p in main_manifest)


import metrics  # noqa: E402

FILLER_PY = "# a scratch script, not a node\n"


def _add_third_node(root: Path, groot: Path) -> None:
    """Commit a third active node and a NON-`.md` file under `nodes/`, so the
    committed FILE set is one larger than the smoke metric (SM.34 kid 3's
    probe fixture). The metric is `rglob("*.md")`, which also counts
    `.geometry/ladder.md`: ladder + a + b + c = 4 nodes, 5 committed files."""
    (groot / "nodes" / "hypothesis" / "c.md").write_text(
        "---\nid: hypothesis:c\ntype: hypothesis\nstatus: active\n---\n# c\n")
    (groot / "nodes" / "scratch_notes.py").write_text(FILLER_PY)
    _sp(["git", "add", "-A"], cwd=root)
    _sp(["git", "-c", "user.email=t@t", "-c", "user.name=t", "commit",
         "--no-verify", "-m", "third node + scratch"], cwd=root)
    _sp(["git", "push", "origin", BRANCH], cwd=root)


def test_committed_triple_is_count_preserving_with_the_metric(tmp_path):
    """THE acceptance criterion: on a CLEAN checkout the committed triple must
    EQUAL `metrics.node_lifecycle_stats(nodes_dir, len(rglob('*.md')))`. A
    committed non-`.md` file under `nodes/` is not a node and must not offset
    the committed count upward."""
    root = _init_fixture(tmp_path)
    groot = root / ".agi"
    _add_third_node(root, groot)
    dep_dir = groot / "nodes" / "deprecated" / "hypothesis"
    dep_dir.mkdir(parents=True)
    (dep_dir / "d.md").write_text(
        "---\nid: hypothesis:d\ntype: hypothesis\nstatus: deprecated\n"
        "---\n# d\n")
    _sp(["git", "add", "-A"], cwd=root)
    _sp(["git", "-c", "user.email=t@t", "-c", "user.name=t", "commit",
         "--no-verify", "-m", "deprecated node"], cwd=root)
    committed = verification._committed_counts(groot)
    nd = groot / "nodes"
    total = len(list(nd.rglob("*.md")))
    metric = metrics.node_lifecycle_stats(nd, total)
    assert committed == {"active": metric["active_node_count"],
                         "deprecated": metric["deprecated_node_count"],
                         "total": total}, (committed, metric, total)
    assert all(p.endswith(".md")
               for p in verification._node_manifest(groot))
    assert "scratch_notes.py" not in json.dumps(
        verification._node_manifest(groot)), "a .py is not a node"


def test_committed_non_md_file_cannot_offset_the_count_and_mask_a_drop(
        tmp_path):
    """THE parent probe (SM.34 kid 3): a committed non-`.md` file under
    `nodes/` must NOT offset the committed active count. Worktree deletes a
    committed `.md` node, commits the loss, and mints an untracked filler so
    the working-tree metric reads 4 again. The gate must FAIL on the committed
    count and name `b.md`."""
    root = _init_fixture(tmp_path)
    groot = root / ".agi"
    _add_third_node(root, groot)          # metric 4, committed files 5
    assert "baseline recorded" in verification.compare_count(
        groot, {"active": 4, "deprecated": 0, "total": 4}).note
    wt = tmp_path / "wt"
    _sp(["git", "worktree", "add", "--detach", str(wt), "HEAD"], cwd=root)
    _sp(["git", "rm", ".agi/nodes/hypothesis/b.md"], cwd=wt)
    _sp(["git", "-c", "user.email=t@t", "-c", "user.name=t", "commit",
         "--no-verify", "-m", "lost b"], cwd=wt)
    (wt / ".agi" / "nodes" / "hypothesis" / "untracked-filler.md").write_text(
        "---\nid: hypothesis:f\ntype: hypothesis\nstatus: active\n---\n# f\n")
    wss = wt / ".agi" / "sessions"
    wss.mkdir(parents=True, exist_ok=True)
    (wss / verification.STATE_FILE).write_bytes(
        (groot / "sessions" / verification.STATE_FILE).read_bytes())
    r = verification.compare_count(wt / ".agi",
                                   {"active": 4, "deprecated": 0, "total": 4})
    assert r.status == "FAIL", (
        "a committed non-.md file offset the count and masked the drop: "
        + r.note)
    assert "committed total=3" in r.note, r.note
    assert "b.md" in r.note, r.note
    assert "scratch_notes.py" not in r.note.split("missing committed")[-1], (
        "the report must not name a non-node as a lost node: " + r.note)


def _commit_node(root: Path, groot: Path, name: str, text: str) -> None:
    """Commit one node file and push, so the fixture is clean again."""
    (groot / "nodes" / "hypothesis" / name).write_text(text)
    _sp(["git", "add", "-A"], cwd=root)
    _sp(["git", "-c", "user.email=t@t", "-c", "user.name=t", "commit",
         "--no-verify", "-m", name], cwd=root)
    _sp(["git", "push", "origin", BRANCH], cwd=root)


def _metric_triple(groot: Path) -> dict:
    """`metrics.node_lifecycle_stats` over the working tree — the number the
    committed triple must stand in for."""
    nd = groot / "nodes"
    total = len(list(nd.rglob("*.md")))
    m = metrics.node_lifecycle_stats(nd, total)
    return {"active": m["active_node_count"],
            "deprecated": m["deprecated_node_count"], "total": total}


def test_quoted_deprecated_spelling_agrees_with_the_metric(tmp_path):
    """THE parent probe (SM.34 kid 4), first direction: a node whose
    frontmatter says `status: "deprecated"` is deprecated to the PARSER the
    metric uses and invisible to the `^status: deprecated` line anchor, so the
    anchor read the committed active count one HIGH and masked a real drop.

    Falsifier: `_committed_counts` != `_metric_triple` on a clean tree."""
    root = _init_fixture(tmp_path)
    groot = root / ".agi"
    _commit_node(root, groot, "q.md",
                 '---\nid: hypothesis:q\ntype: hypothesis\n'
                 'status: "deprecated"\n---\n# q\n')
    committed = verification._committed_counts(groot)
    metric = _metric_triple(groot)
    assert committed == metric, (
        "a quoted `status: deprecated` is deprecated to the parser and must "
        "count as deprecated here too: " + repr((committed, metric)))
    assert committed["deprecated"] == 1, committed
    # and the drop the inflated count used to mask is still caught
    assert "baseline recorded" in verification.compare_count(
        groot, metric).note
    wt = tmp_path / "wt"
    _sp(["git", "worktree", "add", "--detach", str(wt), "HEAD"], cwd=root)
    _sp(["git", "rm", ".agi/nodes/hypothesis/b.md"], cwd=wt)
    _sp(["git", "-c", "user.email=t@t", "-c", "user.name=t", "commit",
         "--no-verify", "-m", "lost b"], cwd=wt)
    (wt / ".agi" / "nodes" / "hypothesis" / "filler.md").write_text(
        "---\nid: hypothesis:f\nstatus: active\n---\n# f\n")
    wss = wt / ".agi" / "sessions"
    wss.mkdir(parents=True, exist_ok=True)
    (wss / verification.STATE_FILE).write_bytes(
        (groot / "sessions" / verification.STATE_FILE).read_bytes())
    r = verification.compare_count(wt / ".agi", metric)
    assert r.status == "FAIL", ("a quoted deprecation masked the drop: "
                               + r.note)
    assert "b.md" in r.note, r.note


def test_a_body_line_is_not_a_deprecation_and_raises_no_spurious_fail(
        tmp_path):
    """THE parent probe (SM.34 kid 4), second direction: the literal line
    `status: deprecated` inside a BODY is not a deprecation to the parser and
    WAS one to the anchor, so the committed active count read one LOW and
    could raise a spurious FAIL — the SM.33 pathology this exists to kill.

    Falsifier: a spurious FAIL on a clean tree, or a triple below the metric."""
    root = _init_fixture(tmp_path)
    groot = root / ".agi"
    _commit_node(root, groot, "body.md",
                 "---\nid: hypothesis:body\ntype: hypothesis\n"
                 "status: active\n---\n# body\n\nprose follows\n\n"
                 "```\nstatus: deprecated\n```\n")
    committed = verification._committed_counts(groot)
    metric = _metric_triple(groot)
    assert committed == metric, (committed, metric)
    assert committed["deprecated"] == 0, committed
    # a CLEAN tree stamps (no spurious FAIL) and then compares steady — the
    # exact shape the anchor's low count used to break
    assert "baseline recorded" in verification.compare_count(
        groot, metric).note
    second = verification.compare_count(groot, metric)
    assert second.status == "PASS", second.note
    assert "FAIL" not in second.note and "DROPPED" not in second.note


def test_a_missing_blob_yields_none_never_a_truncated_count(tmp_path):
    """THE parent probe (SM.34 kid 5): `git cat-file --batch` answers
    `<path> missing` — TWO fields, not three — for a manifest entry with no
    blob behind it, and `_committed_deprecated` used to `break`, returning the
    PARTIAL count as if it were complete.

    A truncated DEPRECATED count is LOW, so `_committed_counts` reported
    committed active HIGH by the number of lost deprecations and a real drop
    was masked SILENTLY — the exact class of failure this hypothesis exists to
    kill. The input is reachable, not malformed: `_node_manifest` and
    `_committed_deprecated` are two separate git invocations and `grid.py
    commit --all` moves HEAD between them in a shared tree.

    Falsifier: a missing blob returns a number instead of None — first in the
    manifest (nothing counted) or mid-manifest (the parse desyncs)."""
    root = _init_fixture(tmp_path)
    groot = root / ".agi"
    (groot / "nodes" / "hypothesis" / "c.md").write_text(
        "---\nid: hypothesis:c\ntype: hypothesis\nstatus: deprecated\n"
        "---\n# c\n")
    _sp(["git", "add", "-A"], cwd=root)
    _sp(["git", "-c", "user.email=t@t", "-c", "user.name=t", "commit",
         "--no-verify", "-m", "c"], cwd=root)
    manifest = verification._node_manifest(groot)
    assert verification._committed_deprecated(groot, manifest) == 1
    for label, broken in (("first", ["nodes/gone.md"] + manifest),
                          ("mid", manifest + ["nodes/gone.md"])):
        dep = verification._committed_deprecated(groot, broken)
        assert dep is None, (
            f"a missing blob {label} in the manifest returned {dep!r} instead "
            "of None: a truncated deprecated count reads LOW, committed "
            "active reads HIGH, and drops are masked silently")
        assert verification._committed_counts(groot, broken) is None, (
            f"_committed_counts did not fall back to None on a {label} "
            "missing blob")


def test_a_stale_manifest_yields_no_drop_verdict_rather_than_a_wrong_one(
        tmp_path, monkeypatch):
    """The consequence, driven through the real gate: `_node_manifest` and
    `_committed_deprecated` are two separate git invocations, so HEAD can move
    between them (`grid.py commit --all`, 5 minutes, shared tree) and the
    second answers `missing` for a path the first listed. With the old
    `break`, the committed count came back truncated — deprecated LOW, active
    HIGH — and a real drop was masked. Now `_committed_counts` is None, so the
    gate never gates on that number: it falls back to the working-tree metric,
    which still catches the drop.

    Falsifier: a note that says `committed active=` while git could not answer
    for the manifest — the gate comparing a silently short count."""
    root = _init_fixture(tmp_path)
    groot = root / ".agi"
    _commit_node(root, groot, "c.md",
                 "---\nid: hypothesis:c\ntype: hypothesis\nstatus: deprecated\n"
                 "---\n# c\n")
    metric = {"active": 3, "deprecated": 1, "total": 4}
    assert verification._committed_counts(groot) == metric
    assert "baseline recorded" in verification.compare_count(
        groot, metric).note
    # the race, injected: the manifest lists a path whose blob is gone
    stale = ["nodes/gone.md"] + verification._node_manifest(groot)
    assert verification._committed_counts(groot, stale) is None
    monkeypatch.setattr(verification, "_node_manifest", lambda g: stale)
    r = verification.compare_count(groot, {"active": 2, "deprecated": 1,
                                           "total": 3})
    assert r.status == "FAIL", r.note
    assert "committed total=" not in r.note, (
        "the gate compared a truncated committed count: " + r.note)
    assert "total=3 below baseline=4" in r.note, r.note
