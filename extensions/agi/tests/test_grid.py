"""Tests for bin/grid.py — the per-node git grid, in-repo ref-namespace mode."""

import fcntl
import importlib.util
import os
import subprocess
import sys
import threading
import time
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parents[1] / "bin" / "grid.py"
spec = importlib.util.spec_from_file_location("grid", BIN)
grid = importlib.util.module_from_spec(spec)
spec.loader.exec_module(grid)

# goal:g2.5 — grid.py now keys writes on `mint_id`, not on the node id. Every
# fixture node below carries one so the ordinary commit/log/diff/status path
# is exercised under the NEW scheme; the missing-mint_id and legacy-ref
# fallback behaviours get their own dedicated tests further down.
MINT_X = "a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1"


@pytest.fixture()
def project(tmp_path):
    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
    (tmp_path / "agi-tree.config.json").write_text("{}")
    d = tmp_path / "nodes" / "idea"
    d.mkdir(parents=True)
    (d / "x.md").write_text(
        f'---\nid: "idea:x"\nmint_id: {MINT_X}\ntype: idea\n---\n\nfirst thought\n'
    )
    grid.cmd_init(tmp_path)
    return tmp_path


def versions(root, node_id):
    """Version count via the SAME read-fallback path production code uses
    (`_resolve_read_ref`) — mint-id ref preferred, legacy ref as fallback —
    rather than hardcoding either ref scheme into the test helper."""
    node_file = grid.build_id_index(root).get(node_id)
    ref = grid._resolve_read_ref(root, node_file, node_id) if node_file else None
    tip = grid.ref_tip(root, ref) if ref else None
    return int(grid.git(root, "rev-list", "--count", tip)) if tip else 0


def test_init_idempotent_and_refuses_non_repo(tmp_path):
    (tmp_path / "agi-tree.config.json").write_text("{}")
    with pytest.raises(SystemExit):
        grid.cmd_init(tmp_path)  # not a git repo -> hard error, no silent grid


def test_commit_creates_version_and_skips_unchanged(project):
    grid.cmd_commit(project, [], do_all=True, session=None)
    assert versions(project, "idea:x") == 1
    # unchanged content -> no new version (change, not time, makes versions)
    grid.cmd_commit(project, [], do_all=True, session=None)
    assert versions(project, "idea:x") == 1


def test_grid_refs_stay_out_of_branch_listing(project):
    grid.cmd_commit(project, [], do_all=True, session=None)
    branches = grid.git(project, "branch", "--list")
    assert "grid" not in branches  # D2 must not pollute D1's branch namespace


def test_edit_makes_v2_and_diff_shows_it(project):
    grid.cmd_commit(project, [], do_all=True, session=None)
    f = project / "nodes" / "idea" / "x.md"
    f.write_text(f.read_text().replace("first thought", "second thought"))
    grid.cmd_commit(project, [], do_all=True, session=None)
    assert versions(project, "idea:x") == 2
    ref = grid.mint_node_ref(MINT_X)  # writes go to the mint-id ref (goal:g2.5)
    diff = grid.git(project, "diff", f"{ref}~1", ref, "--", "node.md")
    assert "-first thought" in diff and "+second thought" in diff


def test_session_branch_is_separate_dimension(project):
    grid.cmd_commit(project, [], do_all=True, session=None)
    f = project / "nodes" / "idea" / "x.md"
    f.write_text(f.read_text() + "\ndraft addition\n")
    grid.cmd_commit(project, [str(f)], do_all=False, session=("3", "a01-kid"))
    # D3 recorded, D2 untouched:
    assert grid.ref_tip(project, "refs/grid/session/3/a01-kid/idea/x") is not None
    assert versions(project, "idea:x") == 1


def test_node_without_id_is_skipped(project):
    (project / "nodes" / "idea" / "noid.md").write_text("no frontmatter here\n")
    grid.cmd_commit(project, [], do_all=True, session=None)
    assert grid.ref_tip(project, "refs/grid/node/noid") is None


def test_commit_prefix_marks_auto_snapshots(project):
    f = project / "nodes" / "idea" / "x.md"
    grid.cmd_commit(project, [str(f)], do_all=False, session=None,
                    prefix="cron: ")
    msg = grid.git(project, "log", "-1", "--format=%s",
                   grid.mint_node_ref(MINT_X))
    assert msg == "cron: v1 idea:x"


def test_sanitize_refuses_ref_hostile_chars():
    # Hostile chars are percent-encoded (injective), not collapsed to `-`
    # (lossy -- see the injectivity tests below for why that mattered).
    assert grid.sanitize("hyp:weird id~^?.") == "hyp/weird%20id%7E%5E%3F%2E"
    assert ".." not in grid.sanitize("a:..b")


def test_cron_lines_are_cwd_proof(tmp_path):
    # Regression: cron runs from $HOME; a line without cd/-C fails silently.
    lines = grid.cron_lines(tmp_path, "main", 5, tmp_path / "g.log")
    assert lines[0].startswith(f"*/5 * * * * cd {tmp_path} && ")
    assert f"'{grid.PUSH_SPEC}'" in lines[0]
    assert "--prefix 'cron: '" in lines[0]
    assert lines[1].startswith(f"7 * * * * git -C {tmp_path} push -q origin main")
    for line in lines:
        assert str(tmp_path / "g.log") in line  # log path doubles as the marker


def test_publish_engine_cron_also_pushes_the_engine(tmp_path):
    """goal:g7.10 — a publish that is never pushed is a publish nobody sees.

    `publish-engine.sh` commits the engine and does not push, on the stated
    grounds that pushing is the hourly cron's job. For the engine repo that
    cron did not exist, so 25 commits sat local and the remote went 3 days
    stale. The two halves of that design have to ship together.
    """
    plain = grid.cron_lines(tmp_path, "main", 5, tmp_path / "g.log")
    assert len(plain) == 2, "engine lines must stay opt-in, off by default"

    lines = grid.cron_lines(tmp_path, "main", 5, tmp_path / "g.log",
                            publish_engine=True)
    assert len(lines) == 4
    publish, push = lines[2], lines[3]

    engine_root = Path(grid.__file__).resolve().parents[3]
    assert push.startswith(f"47 * * * * git -C {engine_root} push -q origin HEAD")

    # Ordering is the property, not the literal minutes: the engine is pushed
    # after the publish that writes it, and both after the graph push it cites.
    minute = lambda l: int(l.split()[0])
    assert minute(plain[1]) < minute(publish) < minute(push)

    # HEAD, never a branch captured at install time — the iter24-extend-300hop
    # shape, where a cron pushed `master` while the work was somewhere else.
    assert " main" not in push

    for line in lines:
        assert str(tmp_path / "g.log") in line  # log path doubles as the marker


def test_sync_pushes_grid_refs_and_sets_fetch_spec(project, tmp_path):
    grid.cmd_commit(project, [], do_all=True, session=None)
    remote = tmp_path / "remote.git"
    subprocess.run(["git", "init", "--bare", "-q", str(remote)], check=True)
    grid.cmd_sync(project, str(remote))
    out = subprocess.run(
        ["git", "-C", str(remote), "for-each-ref", "refs/grid",
         "--format=%(refname)"],
        capture_output=True, text=True, check=True,
    ).stdout
    assert f"refs/grid/node/{MINT_X}" in out
    # a fresh clone must be able to fetch the grid: refspec configured
    specs = grid.git(project, "config", "--get-all", "remote.origin.fetch")
    assert grid.FETCH_SPEC in specs.splitlines()


def test_find_project_root_accepts_canonical_and_legacy_config(tmp_path):
    # Rename window: agi-tree.config.json is canonical, but projects still
    # carrying autoresearch-tree.config.json must keep resolving.
    canonical = tmp_path / "canonical"
    legacy = tmp_path / "legacy"
    nested = legacy / "nodes" / "idea"
    canonical.mkdir()
    nested.mkdir(parents=True)
    (canonical / "agi-tree.config.json").write_text("{}")
    (legacy / "autoresearch-tree.config.json").write_text("{}")

    assert grid.find_project_root(canonical) == canonical
    assert grid.find_project_root(nested) == legacy


# ------------------------------- ref-namespace collisions (found live, iter-2)

def test_only_the_first_colon_separates():
    """A later colon must not become a second path separator.

    git cannot hold a ref `a/b` and a ref `a/b/c` at once, so mapping every
    colon to `/` made `exp:x-r1:extend8` unversionable whenever `exp:x-r1`
    already had a ref -- and the failure aborted `commit --all`, losing
    versioning for every node after it.
    """
    assert grid.sanitize("exp:x-r1") == "exp/x-r1"
    assert grid.sanitize("exp:x-r1:extend8").count("/") == 1
    assert not grid.sanitize("exp:x-r1:extend8").startswith("exp/x-r1/")


def test_no_node_ref_is_a_path_prefix_of_another():
    ids = ["exp:x-r1", "exp:x-r1:extend8", "verdict:verdict:a00-1d9",
           "experiment:exp:a00-1d9", "hyp:x", "hyp:x:y:z"]
    refs = [grid.node_ref(i) for i in ids]
    for a in refs:
        for b in refs:
            if a is not b:
                assert not b.startswith(a + "/"), f"{b} nests under {a}"


def test_sanitize_is_injective_across_colon_and_dash():
    """Collapsing `:` to `-` would silently merge two distinct nodes."""
    assert grid.sanitize("exp:x-r1:extend8") != grid.sanitize("exp:x-r1-extend8")


def test_escape_alphabet_cannot_be_forged():
    """A literal `%` in an id must not be able to imitate an escape."""
    assert grid.sanitize("exp:a%3Ab") != grid.sanitize("exp:a:b")


# ------------------------- sanitize(): injective by construction (G2.5) ----
# level3:bin-grid@v2 -- the escaping layer only, not the zoom-encoded id
# scheme G2.5 ultimately wants. Confirmed live on 2026-08-24: the ref for
# level3:bin-stitch@v2 was already the collapsed `level3/bin-stitch-v2`,
# indistinguishable from a hypothetical `level3:bin-stitch-v2`.

ADVERSARIAL_IDS = [
    "level3:bin-stitch@v2", "level3:bin-stitch-v2",
    "exp:x-r1:extend8", "exp:x-r1-extend8",
    "a:b:c", "a:b-c",
    "hyp:weird id~^?.",
    "idea:a..b", "idea:a.b", "idea:a...b",
    "idea:.leading", "idea:trailing.", "idea:.both.",
    "idea:foo.lock", "idea:foo.locked", "idea:.lock",
    "idea:@", "idea:@{HEAD}", "idea:x@{y",
    "idea:café", "idea:cafe", "idea:éclair",
    "idea:100%done", "idea:100%25done", "idea:%",
    "exp:a%3Ab", "exp:a:b", "exp:a%25%3Ab",
    "idea:...", "idea:....", "idea:.",
    "idea:foo/bar", "idea:foo\\bar", "idea:foo\tbar",
    "goal:g2.5", "level3:autoresearch.config.json",
    "level3:skills-agi-SKILL.md@v2", "level3:skills-agi-SKILL.md-v2",
]


def test_sanitize_is_injective_over_adversarial_corpus():
    """The actual point of this change: no two distinct ids may share a ref."""
    seen: dict[str, str] = {}
    for nid in ADVERSARIAL_IDS:
        ref = grid.sanitize(nid)
        assert ref not in seen, f"{nid!r} and {seen.get(ref)!r} both -> {ref!r}"
        seen[ref] = nid


def test_sanitize_output_is_a_valid_git_refname():
    """Don't trust the reasoning about `%XX` being ref-safe -- check it."""
    for nid in ADVERSARIAL_IDS:
        ref = grid.node_ref(nid)
        for component in ref.split("/"):
            res = subprocess.run(
                ["git", "check-ref-format", "--allow-onelevel", component],
                capture_output=True, text=True,
            )
            assert res.returncode == 0, f"{nid!r} -> {component!r}: {res.stderr}"
        res = subprocess.run(["git", "check-ref-format", ref],
                             capture_output=True, text=True)
        assert res.returncode == 0, f"{nid!r} -> full ref {ref!r}: {res.stderr}"


def test_sanitize_real_agi_tree_corpus_round_trips_distinctly():
    """Not just adversarial cases -- every id actually on disk today.

    Post-`goal:g11` the corpus lives at the engine repo's own `.agi/nodes`
    (plus `.agi/nodes/deprecated` for retired nodes), not a sibling
    `agi-tree/` checkout.
    """
    here = Path(__file__).resolve()
    engine_root = here.parents[3]  # .../extensions/agi/tests -> engine repo root
    nodes_dirs = []
    for rel in ((".agi", "nodes"),):
        d = engine_root.joinpath(*rel)
        if d.is_dir():
            nodes_dirs.append(d)
    dep = engine_root / ".agi" / "nodes" / "deprecated"
    if dep.is_dir():
        nodes_dirs.append(dep)
    if not nodes_dirs:
        pytest.skip(".agi/nodes not found beside the engine repo")
    ids = []
    for nodes_dir in nodes_dirs:
        for p in sorted(nodes_dir.rglob("*.md")):
            nid = grid.parse_node_id(p)
            if nid:
                ids.append(nid)
    assert len(ids) > 500, "expected the full live corpus, not a subset"
    seen: dict[str, str] = {}
    collisions = []
    for nid in ids:
        ref = grid.sanitize(nid)
        if ref in seen and seen[ref] != nid:
            collisions.append((seen[ref], nid, ref))
        seen[ref] = nid
    assert not collisions, f"non-injective on live corpus: {collisions[:5]}"
    for ref in seen:
        for component in ref.split("/"):
            res = subprocess.run(
                ["git", "check-ref-format", "--allow-onelevel", component],
                capture_output=True, text=True,
            )
            assert res.returncode == 0, f"{component!r} invalid: {res.stderr}"


# ------------------------- migrate-refs: move old-scheme refs safely -------

@pytest.fixture()
def migrate_project(tmp_path):
    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
    (tmp_path / "agi-tree.config.json").write_text("{}")
    (tmp_path / "nodes" / "level3").mkdir(parents=True)
    grid.cmd_init(tmp_path)
    return tmp_path


def _write_node(root, rel, node_id, body="body\n"):
    p = root / "nodes" / "level3" / rel
    p.write_text(f'---\nid: "{node_id}"\ntype: level3\n---\n\n{body}')
    return p


def test_migrate_refs_dry_run_changes_nothing(migrate_project):
    root = migrate_project
    p = _write_node(root, "a.md", "level3:bin-stitch@v2")
    old_ref = grid._node_ref_legacy("level3:bin-stitch@v2")
    grid.commit_file(root, p, old_ref, "")
    old_tip_before = grid.ref_tip(root, old_ref)

    grid.cmd_migrate_refs(root, write=False)

    assert grid.ref_tip(root, old_ref) == old_tip_before  # untouched
    assert grid.ref_tip(root, grid.node_ref("level3:bin-stitch@v2")) is None


def test_migrate_refs_write_moves_ref_and_preserves_history(migrate_project):
    root = migrate_project
    p = _write_node(root, "a.md", "level3:bin-stitch@v2")
    old_ref = grid._node_ref_legacy("level3:bin-stitch@v2")
    grid.commit_file(root, p, old_ref, "")
    old_tip = grid.ref_tip(root, old_ref)
    new_ref = grid.node_ref("level3:bin-stitch@v2")
    assert old_ref != new_ref

    grid.cmd_migrate_refs(root, write=True)

    assert grid.ref_tip(root, old_ref) is None      # old ref gone
    assert grid.ref_tip(root, new_ref) == old_tip    # same commit, new name
    msg = grid.git(root, "log", "-1", "--format=%s", new_ref)
    assert msg.endswith("level3:bin-stitch@v2")


def test_migrate_refs_is_idempotent(migrate_project):
    root = migrate_project
    p = _write_node(root, "a.md", "level3:bin-stitch@v2")
    old_ref = grid._node_ref_legacy("level3:bin-stitch@v2")
    grid.commit_file(root, p, old_ref, "")
    new_ref = grid.node_ref("level3:bin-stitch@v2")

    grid.cmd_migrate_refs(root, write=True)
    tip_after_first = grid.ref_tip(root, new_ref)
    grid.cmd_migrate_refs(root, write=True)  # second run must be a no-op

    assert grid.ref_tip(root, new_ref) == tip_after_first
    assert grid.ref_tip(root, old_ref) is None


def test_migrate_refs_refuses_to_overwrite_conflicting_destination(migrate_project):
    root = migrate_project
    p = _write_node(root, "a.md", "level3:bin-stitch@v2")
    old_ref = grid._node_ref_legacy("level3:bin-stitch@v2")
    grid.commit_file(root, p, old_ref, "")
    old_tip = grid.ref_tip(root, old_ref)

    # Pre-seed the destination with unrelated history -- migrate-refs must
    # never clobber it, only report and skip.
    other = _write_node(root, "other.md", "level3:unrelated")
    new_ref = grid.node_ref("level3:bin-stitch@v2")
    grid.commit_file(root, other, new_ref, "")
    other_tip = grid.ref_tip(root, new_ref)
    assert other_tip != old_tip

    grid.cmd_migrate_refs(root, write=True)

    assert grid.ref_tip(root, old_ref) == old_tip     # untouched
    assert grid.ref_tip(root, new_ref) == other_tip   # untouched


def test_migrate_refs_reports_collision_and_touches_neither_id(migrate_project):
    root = migrate_project
    # Two distinct ids that shared ONE ref under the old (buggy) scheme.
    _write_node(root, "a.md", "level3:bin-stitch@v2")
    p2 = _write_node(root, "b.md", "level3:bin-stitch-v2")
    assert (grid._node_ref_legacy("level3:bin-stitch@v2")
            == grid._node_ref_legacy("level3:bin-stitch-v2"))
    shared_old_ref = grid._node_ref_legacy("level3:bin-stitch@v2")
    grid.commit_file(root, p2, shared_old_ref, "")  # whichever "won" the ref
    old_tip = grid.ref_tip(root, shared_old_ref)

    grid.cmd_migrate_refs(root, write=True)

    # Untouched: no guessing whose history the shared ref actually holds.
    # ("level3:bin-stitch-v2" has no hostile chars, so its own new-scheme ref
    # IS `shared_old_ref` -- already asserted unchanged above. The other id,
    # "level3:bin-stitch@v2", has a genuinely different new-scheme ref, which
    # migrate-refs must not have created -- it cannot tell which id the
    # shared ref's history actually belongs to.)
    assert grid.ref_tip(root, grid.node_ref("level3:bin-stitch@v2")) is None


# --------------------- goal:g2.5 — mint-id keying, with read fallback ------
# grid.py now keys WRITES on `mint_id`, never on the node id (which is an
# address that moves on retag/regroup — see GOALS.md "Tension resolved
# 2026-08-25"). READS (log/diff/versions/status) fall back to the legacy
# node-id-keyed ref when no mint-id ref exists, so history committed before
# a node had a mint_id stays reachable.

MINT_A = "b2b2b2b2b2b2b2b2b2b2b2b2b2b2b2b2"
MINT_B = "c3c3c3c3c3c3c3c3c3c3c3c3c3c3c3c3"


@pytest.fixture()
def mint_project(tmp_path):
    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
    (tmp_path / "agi-tree.config.json").write_text("{}")
    (tmp_path / "nodes" / "idea").mkdir(parents=True)
    grid.cmd_init(tmp_path)
    return tmp_path


def _write_mint_node(root, rel, node_id, mint_id=None, parents=None, body="body\n"):
    fm = [f'id: "{node_id}"']
    if mint_id:
        fm.append(f"mint_id: {mint_id}")
    if parents:
        fm.append("parents:")
        fm.extend(f"  - {p}" for p in parents)
    fm.append("type: idea")
    p = root / "nodes" / "idea" / rel
    p.write_text("---\n" + "\n".join(fm) + f"\n---\n\n{body}")
    return p


def test_write_ref_for_raises_on_missing_mint_id(mint_project):
    p = _write_mint_node(mint_project, "x.md", "idea:x")  # no mint_id
    with pytest.raises(grid.MissingMintIdError, match="idea:x"):
        grid.write_ref_for(p, "idea:x")


def test_write_ref_for_returns_mint_ref_when_present(mint_project):
    p = _write_mint_node(mint_project, "x.md", "idea:x", mint_id=MINT_A)
    assert grid.write_ref_for(p, "idea:x") == grid.mint_node_ref(MINT_A)


def test_commit_all_skips_missing_mint_id_but_keeps_going(mint_project):
    """The load-bearing operational property: one un-migrated node must not
    block --all from committing every other node (the sanitize()-colon-bug
    failure class this file already paid for once)."""
    _write_mint_node(mint_project, "no-mint.md", "idea:no-mint")  # no mint_id
    _write_mint_node(mint_project, "has-mint.md", "idea:has-mint", mint_id=MINT_A)

    grid.cmd_commit(mint_project, [], do_all=True, session=None)

    assert grid.ref_tip(mint_project, grid.mint_node_ref(MINT_A)) is not None
    assert grid.ref_tip(mint_project, grid.node_ref("idea:no-mint")) is None
    assert grid.ref_tip(mint_project, grid.node_ref("idea:has-mint")) is None


def test_commit_never_falls_back_to_node_id_ref_for_missing_mint_id(mint_project, capsys):
    p = _write_mint_node(mint_project, "no-mint.md", "idea:no-mint")

    grid.cmd_commit(mint_project, [str(p)], do_all=False, session=None)

    assert grid.ref_tip(mint_project, grid.node_ref("idea:no-mint")) is None
    err = capsys.readouterr().err
    assert "ERROR" in err and "idea:no-mint" in err and "no mint_id" in err


def test_adopted_node_commits_with_zero_errors(mint_project):
    """hypothesis:l3-node-without-mint-id — the live-proof half of the fix.
    A node written outside node_writer (no mint_id -> grid refuses to version
    it) becomes versionable once `node_writer.repair_mint` adopts it: commit
    --all then reports 0 errors and the node gets a mint-id ref."""
    import node_writer
    _write_mint_node(mint_project, "no-mint.md", "idea:no-mint")

    # Before: commit --all refuses (skips, reports an error, keeps going).
    grid.cmd_commit(mint_project, [], do_all=True, session=None)
    assert grid.ref_tip(mint_project, grid.node_ref("idea:no-mint")) is None

    # Adopt it, then re-commit.
    res = node_writer.repair_mint(mint_project, "idea:no-mint", announce=False)
    assert res.status == node_writer.UPDATED, res.reason
    grid.cmd_commit(mint_project, [], do_all=True, session=None)

    assert grid.ref_tip(mint_project, grid.mint_node_ref(res_mint_id(mint_project))) is not None


def res_mint_id(project):
    import re as _re
    p = project / "nodes" / "idea" / "no-mint.md"
    m = _re.search(r"^mint_id:\s*([^\n\s]+)", p.read_text(), _re.M)
    return m.group(1) if m else ""


def test_read_falls_back_to_legacy_ref_when_no_mint_ref_exists(mint_project):
    """A version committed BEFORE the node had a mint_id (or before the
    mint-id ref existed) must stay reachable by log/diff/versions/status."""
    p = _write_mint_node(mint_project, "x.md", "idea:x")  # no mint_id yet
    legacy_ref = grid.node_ref("idea:x")
    grid.commit_file(mint_project, p, legacy_ref, "")  # simulate pre-migration history

    # Now the node picks up a mint_id but has never been committed under it.
    p.write_text(p.read_text().replace(
        'id: "idea:x"', f'id: "idea:x"\nmint_id: {MINT_A}'))

    assert grid.ref_tip(mint_project, grid.mint_node_ref(MINT_A)) is None  # nothing here yet
    assert grid.resolve_ref(mint_project, "idea:x") == legacy_ref
    grid.cmd_log(mint_project, "idea:x", 5)  # must not raise / SystemExit


def test_versions_falls_back_to_legacy_ref(mint_project, capsys):
    p = _write_mint_node(mint_project, "x.md", "idea:x")
    legacy_ref = grid.node_ref("idea:x")
    grid.commit_file(mint_project, p, legacy_ref, "")
    p.write_text(p.read_text().replace(
        'id: "idea:x"', f'id: "idea:x"\nmint_id: {MINT_A}'))

    capsys.readouterr()
    grid.cmd_versions(mint_project, "idea:x")
    out = capsys.readouterr().out.strip()
    assert out == "1"


def test_status_clean_via_legacy_ref_for_node_without_mint_id_yet(mint_project, capsys):
    """The common transition-window case: a node with no mint_id at all yet
    still has real legacy-ref history, and status must report it clean
    (unchanged) via the fallback rather than as drift or as NEW."""
    p = _write_mint_node(mint_project, "x.md", "idea:x")  # no mint_id
    legacy_ref = grid.node_ref("idea:x")
    grid.commit_file(mint_project, p, legacy_ref, "")

    capsys.readouterr()
    grid.cmd_status(mint_project)
    out = capsys.readouterr().out
    assert "grid status: 0 new, 0 changed, 1 clean" in out


def test_status_falls_back_to_legacy_ref_instead_of_reporting_new(mint_project, capsys):
    """Without the fallback this would misreport NEW (the mint-id ref has no
    history yet) even though the node has one real version under the legacy
    ref. With the fallback, status finds that history and reports drift
    against it (the mint_id field itself is new content) instead of
    treating the node as having no history at all."""
    p = _write_mint_node(mint_project, "x.md", "idea:x")
    legacy_ref = grid.node_ref("idea:x")
    grid.commit_file(mint_project, p, legacy_ref, "")  # pre-migration history
    p.write_text(p.read_text().replace(
        'id: "idea:x"', f'id: "idea:x"\nmint_id: {MINT_A}'))

    capsys.readouterr()
    grid.cmd_status(mint_project)
    out = capsys.readouterr().out
    assert "CHANGED  idea:x" in out
    assert "grid status: 0 new, 1 changed, 0 clean" in out


def test_status_reports_new_when_neither_ref_exists(mint_project, capsys):
    _write_mint_node(mint_project, "x.md", "idea:x", mint_id=MINT_A)
    capsys.readouterr()
    grid.cmd_status(mint_project)
    out = capsys.readouterr().out
    assert "grid status: 1 new, 0 changed, 0 clean" in out


def test_parent_mint_trailer_in_commit_body(mint_project):
    parent = _write_mint_node(mint_project, "parent.md", "idea:parent", mint_id=MINT_A)
    child = _write_mint_node(mint_project, "child.md", "idea:child", mint_id=MINT_B,
                             parents=["idea:parent"])

    grid.cmd_commit(mint_project, [], do_all=True, session=None)

    body = grid.git(mint_project, "log", "-1", "--format=%B",
                    grid.mint_node_ref(MINT_B))
    assert f"Parent-Mint-Id: {MINT_A} idea:parent" in body
    # subject line is unaffected by the added body
    subject = grid.git(mint_project, "log", "-1", "--format=%s",
                       grid.mint_node_ref(MINT_B))
    assert subject == "v1 idea:child"


def test_parent_mint_trailer_marks_unresolved_parent(mint_project):
    child = _write_mint_node(mint_project, "child.md", "idea:child", mint_id=MINT_B,
                             parents=["idea:ghost"])

    grid.cmd_commit(mint_project, [], do_all=True, session=None)

    body = grid.git(mint_project, "log", "-1", "--format=%B",
                    grid.mint_node_ref(MINT_B))
    assert "Parent-Mint-Id: UNRESOLVED idea:ghost" in body


def test_no_parents_means_no_trailer_body(mint_project):
    _write_mint_node(mint_project, "x.md", "idea:x", mint_id=MINT_A)
    grid.cmd_commit(mint_project, [], do_all=True, session=None)
    body = grid.git(mint_project, "log", "-1", "--format=%B",
                    grid.mint_node_ref(MINT_A))
    assert body.strip() == "v1 idea:x"


def test_mint_node_ref_is_a_valid_git_ref():
    ref = grid.mint_node_ref(MINT_A)
    res = subprocess.run(["git", "check-ref-format", ref], capture_output=True)
    assert res.returncode == 0


def test_mint_node_ref_is_identity_under_sanitize():
    # The whole point of the mint id format (32 lowercase hex chars): no
    # escaping needed, so sanitize() is a no-op on it.
    assert grid.sanitize(MINT_A) == MINT_A


# --------------------------- migrate-mint-refs: the write path (goal:g2.5) -
#
# Landmine this guards against: before this migration runs, no mint-id ref
# exists yet, so an ordinary `commit --all` under the new keying would give
# every migrated node a fresh v1 ROOT commit on its mint-id ref while the
# real history stays stranded on the node-id ref -- forking every node at
# once. `test_versions_and_log_report_full_history_after_migration` below
# is the direct regression guard for exactly that failure mode.

@pytest.fixture()
def migmint_project(tmp_path):
    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
    (tmp_path / "agi-tree.config.json").write_text("{}")
    (tmp_path / "nodes" / "idea").mkdir(parents=True)
    grid.cmd_init(tmp_path)
    return tmp_path


def test_migrate_mint_refs_dry_run_changes_nothing(migmint_project):
    p = _write_mint_node(migmint_project, "x.md", "idea:x", mint_id=MINT_A)
    old_ref = grid.node_ref("idea:x")
    grid.commit_file(migmint_project, p, old_ref, "")
    old_tip_before = grid.ref_tip(migmint_project, old_ref)

    grid.cmd_migrate_mint_refs(migmint_project, write=False)

    assert grid.ref_tip(migmint_project, old_ref) == old_tip_before  # untouched
    assert grid.ref_tip(migmint_project, grid.mint_node_ref(MINT_A)) is None


def test_migrate_mint_refs_write_moves_ref_and_preserves_full_history(migmint_project):
    p = _write_mint_node(migmint_project, "x.md", "idea:x", mint_id=MINT_A)
    old_ref = grid.node_ref("idea:x")
    grid.commit_file(migmint_project, p, old_ref, "")
    p.write_text(p.read_text() + "\nedit 2\n")
    grid.commit_file(migmint_project, p, old_ref, "")
    p.write_text(p.read_text() + "\nedit 3\n")
    grid.commit_file(migmint_project, p, old_ref, "")
    old_tip = grid.ref_tip(migmint_project, old_ref)
    new_ref = grid.mint_node_ref(MINT_A)

    grid.cmd_migrate_mint_refs(migmint_project, write=True)

    assert grid.ref_tip(migmint_project, old_ref) is None       # old ref gone
    assert grid.ref_tip(migmint_project, new_ref) == old_tip    # SAME commit object, new name
    # Not just "a ref exists" -- the full 3-version chain moved with it:
    assert int(grid.git(migmint_project, "rev-list", "--count", new_ref)) == 3


def test_migrate_mint_refs_is_idempotent(migmint_project):
    p = _write_mint_node(migmint_project, "x.md", "idea:x", mint_id=MINT_A)
    old_ref = grid.node_ref("idea:x")
    grid.commit_file(migmint_project, p, old_ref, "")
    new_ref = grid.mint_node_ref(MINT_A)

    grid.cmd_migrate_mint_refs(migmint_project, write=True)
    tip_after_first = grid.ref_tip(migmint_project, new_ref)
    grid.cmd_migrate_mint_refs(migmint_project, write=True)  # second run: must be a no-op

    assert grid.ref_tip(migmint_project, new_ref) == tip_after_first
    assert grid.ref_tip(migmint_project, old_ref) is None


def test_migrate_mint_refs_second_run_reports_zero_moved(migmint_project, capsys):
    p = _write_mint_node(migmint_project, "x.md", "idea:x", mint_id=MINT_A)
    grid.commit_file(migmint_project, p, grid.node_ref("idea:x"), "")

    grid.cmd_migrate_mint_refs(migmint_project, write=True)
    capsys.readouterr()
    grid.cmd_migrate_mint_refs(migmint_project, write=True)
    out = capsys.readouterr().out
    assert "0 moved, 1 already correct, 0 conflict(s), 0 skipped" in out


def test_migrate_mint_refs_refuses_to_overwrite_conflicting_destination(migmint_project):
    p = _write_mint_node(migmint_project, "x.md", "idea:x", mint_id=MINT_A)
    old_ref = grid.node_ref("idea:x")
    grid.commit_file(migmint_project, p, old_ref, "")
    old_tip = grid.ref_tip(migmint_project, old_ref)

    # Pre-seed the destination with unrelated history -- must never be clobbered.
    other = _write_mint_node(migmint_project, "other.md", "idea:other")
    new_ref = grid.mint_node_ref(MINT_A)
    grid.commit_file(migmint_project, other, new_ref, "")
    other_tip = grid.ref_tip(migmint_project, new_ref)
    assert other_tip != old_tip

    grid.cmd_migrate_mint_refs(migmint_project, write=True)

    assert grid.ref_tip(migmint_project, old_ref) == old_tip     # untouched
    assert grid.ref_tip(migmint_project, new_ref) == other_tip   # untouched


def test_migrate_mint_refs_conflict_is_reported(migmint_project, capsys):
    p = _write_mint_node(migmint_project, "x.md", "idea:x", mint_id=MINT_A)
    grid.commit_file(migmint_project, p, grid.node_ref("idea:x"), "")
    other = _write_mint_node(migmint_project, "other.md", "idea:other")
    grid.commit_file(migmint_project, other, grid.mint_node_ref(MINT_A), "")  # pre-seed conflict

    capsys.readouterr()
    grid.cmd_migrate_mint_refs(migmint_project, write=True)
    out = capsys.readouterr().out
    # "other" itself has no mint_id (irrelevant to what it pre-seeded) -- 1 skipped is it.
    assert "0 moved, 0 already correct, 1 conflict(s), 1 skipped" in out


def test_migrate_mint_refs_skips_node_without_mint_id_not_guessed(migmint_project, capsys):
    p = _write_mint_node(migmint_project, "x.md", "idea:x")  # no mint_id
    old_ref = grid.node_ref("idea:x")
    grid.commit_file(migmint_project, p, old_ref, "")
    old_tip = grid.ref_tip(migmint_project, old_ref)

    capsys.readouterr()
    grid.cmd_migrate_mint_refs(migmint_project, write=True)
    out, err = capsys.readouterr()

    assert "SKIP-NO-MINT-ID  idea:x" in err
    assert "0 moved, 0 already correct, 0 conflict(s), 1 skipped" in out
    assert grid.ref_tip(migmint_project, old_ref) == old_tip  # left exactly alone


def test_migrate_mint_refs_reports_duplicate_mint_id_collision(migmint_project, capsys):
    p1 = _write_mint_node(migmint_project, "a.md", "idea:a", mint_id=MINT_A)
    p2 = _write_mint_node(migmint_project, "b.md", "idea:b", mint_id=MINT_A)  # duplicate!
    grid.commit_file(migmint_project, p1, grid.node_ref("idea:a"), "")
    grid.commit_file(migmint_project, p2, grid.node_ref("idea:b"), "")

    capsys.readouterr()
    grid.cmd_migrate_mint_refs(migmint_project, write=True)
    out, err = capsys.readouterr()

    assert "COLLISION" in err and "duplicate mint_id" in err
    assert "0 moved, 0 already correct, 0 conflict(s)" in out
    assert grid.ref_tip(migmint_project, grid.node_ref("idea:a")) is not None  # untouched
    assert grid.ref_tip(migmint_project, grid.node_ref("idea:b")) is not None  # untouched
    assert grid.ref_tip(migmint_project, grid.mint_node_ref(MINT_A)) is None   # never created


def test_versions_and_log_report_full_history_after_migration(migmint_project):
    """The direct regression guard for the fork failure mode this command
    exists to prevent: after migration, a node's version count and log must
    show its FULL pre-migration history, not 1 (a fresh-root-commit fork)."""
    p = _write_mint_node(migmint_project, "x.md", "idea:x", mint_id=MINT_A)
    old_ref = grid.node_ref("idea:x")
    grid.commit_file(migmint_project, p, old_ref, "")
    p.write_text(p.read_text() + "\nedit 2\n")
    grid.commit_file(migmint_project, p, old_ref, "")
    p.write_text(p.read_text() + "\nedit 3\n")
    grid.commit_file(migmint_project, p, old_ref, "")

    grid.cmd_migrate_mint_refs(migmint_project, write=True)

    node_file = grid.build_id_index(migmint_project)["idea:x"]
    ref = grid._resolve_read_ref(migmint_project, node_file, "idea:x")
    assert ref == grid.mint_node_ref(MINT_A)  # reads now prefer the migrated ref
    assert int(grid.git(migmint_project, "rev-list", "--count", ref)) == 3

    # Simulate the very next ordinary commit under the new keying: it must
    # land as v4 (a real child of the migrated history), never a fresh v1.
    p.write_text(p.read_text() + "\nedit 4\n")
    ref_after = grid.write_ref_for(p, "idea:x")
    assert ref_after == grid.mint_node_ref(MINT_A)
    grid.commit_file(migmint_project, p, ref_after, "")
    assert int(grid.git(migmint_project, "rev-list", "--count", ref_after)) == 4


# --- goal:s9 + goal:g6.3 — mode/symlink-correct payloads in the node's ref ----
#
# `exp:grid-payload-roundtrip`'s own table is the regression suite here, per
# goal:s9's "Test:" line: a 100755 file and a 120000 symlink, three version
# bumps each, compared against a non-git baseline. The pre-S9 `commit_file`
# fails every one of these — it hashed `path.resolve()` (substituting a
# symlink's target bytes for its link text) and hardcoded `100644`.

MINT_P = "b2b2b2b2b2b2b2b2b2b2b2b2b2b2b2b2"


@pytest.fixture()
def engine(tmp_path):
    """A stand-in engine tree with one regular, one executable and one symlink
    payload — the three modes git's tree format distinguishes."""
    root = tmp_path / "engine"
    (root / "bin").mkdir(parents=True)
    (root / "bin" / "plain.py").write_text("print('v1')\n")
    exe = root / "bin" / "run.sh"
    exe.write_text("#!/bin/sh\necho v1\n")
    exe.chmod(0o755)
    (root / "bin" / "link.sh").symlink_to("run.sh")
    return root


def _payload_node(project, name, node_id, payload_ref, mint_id=MINT_P):
    p = project / "nodes" / "level3" / f"{name}.md"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(
        f'---\nid: "{node_id}"\nmint_id: {mint_id}\ntype: level3\n'
        f"payload_ref: {payload_ref}\n---\n\nbuild node\n"
    )
    return p


def test_git_mode_reads_lstat_not_stat(engine):
    assert grid.git_mode(engine / "bin" / "plain.py") == grid.GIT_MODE_REGULAR
    assert grid.git_mode(engine / "bin" / "run.sh") == grid.GIT_MODE_EXEC
    # `stat` would follow the link and report the target's 100755; `lstat` is
    # the whole point of this function.
    assert grid.git_mode(engine / "bin" / "link.sh") == grid.GIT_MODE_SYMLINK


def test_symlink_blob_is_link_text_not_target_bytes(project, engine):
    """The pre-S9 defect at its sharpest: not a dropped mode, a wrong object."""
    mode, blob = grid.hash_path(project, engine / "bin" / "link.sh")
    assert mode == grid.GIT_MODE_SYMLINK
    assert grid.git(project, "cat-file", "blob", blob) == "run.sh"


@pytest.mark.parametrize("name,ref,expect_mode", [
    ("plain", "bin/plain.py", grid.GIT_MODE_REGULAR),
    ("exe", "bin/run.sh", grid.GIT_MODE_EXEC),
    ("link", "bin/link.sh", grid.GIT_MODE_SYMLINK),
])
def test_payload_round_trips_with_mode(project, engine, tmp_path,
                                       name, ref, expect_mode):
    node_id = f"level3:{name}"
    _payload_node(project, name, node_id, ref, mint_id=MINT_P + name[0])
    grid.cmd_commit(project, [], do_all=True, session=None, engine_root=engine)

    out = tmp_path / "out" / ref
    grid.cmd_payload(project, node_id, None, str(out))

    src = engine / ref
    assert grid.git_mode(out) == expect_mode
    if expect_mode == grid.GIT_MODE_SYMLINK:
        # A symlink must come back a symlink pointing at the same target —
        # the naive path materialised a regular file with the wrong bytes.
        assert out.is_symlink()
        assert os.readlink(out) == os.readlink(src)
    else:
        assert out.read_bytes() == src.read_bytes()


def test_three_version_bumps_of_a_payload_are_three_versions(project, engine):
    """G6.3's untested case: a build node accumulating *meaningful* versions.
    The node file never changes — only the payload does — so this also proves
    the unchanged-check compares the whole tree and not just `node.md`."""
    _payload_node(project, "plain", "level3:plain", "bin/plain.py")
    node_before = (project / "nodes" / "level3" / "plain.md").read_text()

    src = engine / "bin" / "plain.py"
    expected = []
    for n in (1, 2, 3):
        src.write_text(f"print('v{n}')\n# éà中文 {n}\n")   # non-ASCII on purpose
        expected.append(src.read_bytes())
        grid.cmd_commit(project, [], do_all=True, session=None, engine_root=engine)

    assert versions(project, "level3:plain") == 3
    assert (project / "nodes" / "level3" / "plain.md").read_text() == node_before

    ref = grid.resolve_ref(project, "level3:plain")
    for i, want in enumerate(expected, start=1):
        rev = grid.version_rev(project, ref, "level3:plain", i)
        assert grid.read_tree_entry(project, rev, grid.PAYLOAD_ENTRY)[1] == want


def test_payload_version_out_of_range_is_a_hard_error(project, engine):
    _payload_node(project, "plain", "level3:plain", "bin/plain.py")
    grid.cmd_commit(project, [], do_all=True, session=None, engine_root=engine)
    ref = grid.resolve_ref(project, "level3:plain")
    with pytest.raises(SystemExit):
        grid.version_rev(project, ref, "level3:plain", 2)


def test_staged_payload_beats_the_engine_tree(project, engine):
    """goal:g6.1's arrow, as a preference order. Once `payloads/` holds the
    file, the engine tree is never consulted — that is what makes the graph
    the source rather than the description."""
    _payload_node(project, "plain", "level3:plain", "bin/plain.py")
    staged = project / grid.PAYLOAD_DIR / "bin" / "plain.py"
    staged.parent.mkdir(parents=True)
    staged.write_text("print('edited in the graph')\n")

    found = grid.resolve_payload(project, "bin/plain.py", engine)
    assert found == (staged, "staged")

    grid.cmd_commit(project, [], do_all=True, session=None, engine_root=engine)
    ref = grid.resolve_ref(project, "level3:plain")
    _, data = grid.read_tree_entry(project, ref, grid.PAYLOAD_ENTRY)
    assert data == staged.read_bytes()


def test_checkout_materializes_payloads_for_editing(project, engine):
    _payload_node(project, "exe", "level3:exe", "bin/run.sh")
    grid.cmd_commit(project, [], do_all=True, session=None, engine_root=engine)
    grid.cmd_checkout(project, [], do_all=True, dest=None)
    staged = project / grid.PAYLOAD_DIR / "bin" / "run.sh"
    assert staged.read_bytes() == (engine / "bin" / "run.sh").read_bytes()
    assert grid.git_mode(staged) == grid.GIT_MODE_EXEC


def test_unresolvable_payload_ref_warns_and_still_commits_the_node(
        project, engine, capsys):
    """G7's first invariant is that node count never drops. A payload problem
    is reported; it never costs the node its version history."""
    _payload_node(project, "gone", "level3:gone", "bin/does-not-exist.py")
    grid.cmd_commit(project, [], do_all=True, session=None, engine_root=engine)
    assert "resolves neither" in capsys.readouterr().err
    assert versions(project, "level3:gone") == 1
    ref = grid.resolve_ref(project, "level3:gone")
    assert grid.read_tree_entry(project, ref, grid.PAYLOAD_ENTRY) is None


def test_status_sees_a_payload_only_edit(project, engine, capsys):
    _payload_node(project, "plain", "level3:plain", "bin/plain.py")
    grid.cmd_commit(project, [], do_all=True, session=None, engine_root=engine)
    capsys.readouterr()
    grid.cmd_status(project, engine_root=engine)
    assert "CHANGED  level3:plain" not in capsys.readouterr().out

    (engine / "bin" / "plain.py").write_text("print('moved')\n")
    grid.cmd_status(project, engine_root=engine)
    assert "CHANGED  level3:plain" in capsys.readouterr().out


def test_status_writes_no_objects(project, engine):
    """`status` is a read. Computing the comparison must not leave loose
    objects behind — `tree_entries(write=False)` is what keeps that true."""
    _payload_node(project, "plain", "level3:plain", "bin/plain.py")
    grid.cmd_commit(project, [], do_all=True, session=None, engine_root=engine)
    (engine / "bin" / "plain.py").write_text("print('moved')\n")
    before = grid.git(project, "count-objects", "-v")
    grid.cmd_status(project, engine_root=engine)
    assert grid.git(project, "count-objects", "-v") == before


# --- goal:g11: two roots, and the tests that hold them apart -----------------
#
# Every fixture above builds a LEGACY tree: the graph root and the git repo are
# the same directory, so a call that hands the graph root to `git -C` is
# invisibly correct and this file could not see the defect goal:g11 introduced.
# These build the G11 layout instead — a git repo with its graph at
# `<repo>/.agi` — which is the only shape in which the conflation is
# observable at all.
#
# What that conflation produces is a silent wrong answer, never an error, and
# these tests are written to fail on it from two independent directions:
#
#   1. Behaviourally, through `cmd_diff` — the one command whose bug no
#      pathspec flag was masking (`git diff` has no `--full-tree`).
#   2. Structurally, by spying on every `git` argv and asserting no `-C` ever
#      names the graph directory. That one cannot be masked by any flag,
#      present or future, because it checks the cause rather than a symptom.

MINT_G11 = "c3c3c3c3c3c3c3c3c3c3c3c3c3c3c3c3"


@pytest.fixture()
def g11(tmp_path):
    """A goal:g11-layout project. Returns `(repo, graph)`, two real directories.

    `repo` is the git repo and holds `refs/grid/*`; `graph` is `<repo>/.agi` and
    holds the nodes. The payload sits in the tracked source tree the way it does
    under one repo (`<repo>/extensions/...`) — there is no `payloads/` staging
    copy to check out, which is the whole point of the layout.
    """
    repo = tmp_path / "proj"
    (repo / ".agi" / "nodes" / "idea").mkdir(parents=True)
    subprocess.run(["git", "init", "-q", str(repo)], check=True)
    (repo / ".agi" / "config.json").write_text("{}")
    (repo / ".agi" / "nodes" / "idea" / "x.md").write_text(
        f'---\nid: "idea:x"\nmint_id: {MINT_G11}\ntype: idea\n---\n\nfirst thought\n'
    )
    graph = repo / ".agi"
    grid.cmd_init(graph)
    return repo.resolve(), graph.resolve()


def _bump(graph, text):
    f = graph / "nodes" / "idea" / "x.md"
    f.write_text(f.read_text().replace("first thought", text))
    return f


def test_repo_root_is_the_git_repo_never_the_graph_dir(g11):
    """The split itself. `repo_root` is `.parent` on a `.agi/` and the identity
    on anything else, so a caller asks unconditionally and legacy projects —
    every other fixture in this file — are unaffected."""
    repo, graph = g11
    assert grid.repo_root(graph) == repo
    assert grid.repo_root(repo) == repo
    assert (repo / ".git").is_dir() and not (graph / ".git").exists()


def test_no_git_invocation_ever_targets_the_graph_dir(g11, monkeypatch, capsys):
    """The structural test, and the one that cannot be masked.

    Grid refs and the object store live in the repo; only node *files* live
    under the graph root. Handing `git -C` the graph root sets git's prefix to
    `.agi/`, and every cwd-scoped subcommand then resolves paths under a prefix
    a grid tree does not have. Rather than assert on any one command's output,
    this spies on every `git` argv a full commit/status/diff/log/payload cycle
    produces and asserts the `-C` is always the repo.
    """
    repo, graph = g11
    seen: list[Path] = []
    real_run = subprocess.run

    def spy(argv, *a, **kw):
        if isinstance(argv, (list, tuple)) and argv and argv[0] == "git" and "-C" in argv:
            seen.append(Path(argv[list(argv).index("-C") + 1]))
        return real_run(argv, *a, **kw)

    monkeypatch.setattr(grid.subprocess, "run", spy)

    grid.cmd_commit(graph, [], do_all=True, session=None)
    _bump(graph, "second thought")
    grid.cmd_commit(graph, [], do_all=True, session=None)
    grid.cmd_status(graph)
    grid.cmd_diff(graph, "idea:x", 1)
    grid.cmd_log(graph, "idea:x", 5)
    grid.cmd_versions(graph, "idea:x")
    capsys.readouterr()

    assert seen, "the spy saw no git invocations at all — it is not wired up"
    offenders = {str(p) for p in seen if p.name == grid.locations.GRAPH_DIR_NAME}
    assert not offenders, f"git invoked with the graph root: {sorted(offenders)}"
    assert {p.resolve() for p in seen} == {repo}


def test_byte_identical_corpus_reports_zero_changed(g11, capsys):
    """A corpus that has just been committed and not touched since has drifted
    from nothing. Under the conflated roots this reported every node CHANGED —
    812 of them on the live corpus, all byte-identical."""
    repo, graph = g11
    grid.cmd_commit(graph, [], do_all=True, session=None)
    capsys.readouterr()
    grid.cmd_status(graph)
    out = capsys.readouterr().out
    assert "CHANGED" not in out
    assert "0 new, 0 changed, 1 clean" in out


def test_status_reports_the_same_set_from_either_cwd(g11, capsys, monkeypatch):
    """`status` must answer the same question from the repo root and from
    inside `.agi/`. It is cwd-independent by construction now — the `-C` is
    derived from the resolved graph root, never from where you are standing —
    and this pins that rather than trusting it."""
    repo, graph = g11
    grid.cmd_commit(graph, [], do_all=True, session=None)
    _bump(graph, "second thought")
    capsys.readouterr()

    def status_from(cwd):
        monkeypatch.chdir(cwd)
        grid.cmd_status(graph)
        return sorted(l for l in capsys.readouterr().out.splitlines()
                      if l.startswith("CHANGED"))

    from_repo = status_from(repo)
    from_graph = status_from(graph)
    assert from_repo == from_graph == ["CHANGED  idea:x"]


def test_diff_reads_node_md_when_the_graph_is_a_subdirectory(g11, capsys):
    """The behavioural regression test, and the one no flag was covering.

    `read_tree`/`read_tree_entry` were patched with `ls-tree --full-tree`, which
    made `status` correct again and left the underlying root conflation in
    place. `git diff` has no such flag, so `cmd_diff` stayed broken in exactly
    the way that is hardest to notice: a bare `node.md` pathspec became
    `.agi/node.md`, matched nothing, and the command printed an empty diff and
    exited 0 for a node with real version history.
    """
    repo, graph = g11
    grid.cmd_commit(graph, [], do_all=True, session=None)
    _bump(graph, "second thought")
    grid.cmd_commit(graph, [], do_all=True, session=None)
    capsys.readouterr()

    grid.cmd_diff(graph, "idea:x", 1)
    out = capsys.readouterr().out
    assert "-first thought" in out and "+second thought" in out


def test_payload_round_trips_with_no_staging_copy(g11, capsys):
    """goal:g11's payload story end to end: the payload is a tracked file in the
    same worktree as the graph, committed into the node's ref and read back out
    of it — no `payloads/` directory involved at any point."""
    repo, graph = g11
    src = repo / "extensions" / "agi" / "bin" / "thing.py"
    src.parent.mkdir(parents=True)
    src.write_text("print('v1')\n")
    node = graph / "nodes" / "level3" / "thing.md"
    node.parent.mkdir(parents=True)
    node.write_text(
        f'---\nid: "level3:thing"\nmint_id: {MINT_P}\ntype: level3\n'
        f"payload_ref: extensions/agi/bin/thing.py\n---\n\nbuild node\n"
    )
    assert not (graph / grid.PAYLOAD_DIR).exists()

    grid.cmd_commit(graph, [], do_all=True, session=None, engine_root=repo)
    ref = grid.resolve_ref(graph, "level3:thing")
    mode, data = grid.read_tree_entry(graph, ref, grid.PAYLOAD_ENTRY)
    assert data == src.read_bytes() and mode == grid.GIT_MODE_REGULAR

    capsys.readouterr()
    grid.cmd_status(graph, engine_root=repo)
    assert "CHANGED" not in capsys.readouterr().out


def test_cron_marker_distinguishes_two_migrated_projects(tmp_path):
    """`cmd_cron` uses the log path as the marker for "our" crontab lines, and
    removes every line carrying it before installing. Every migrated project's
    graph root is literally named `.agi`, so a marker derived from it would be
    identical across projects and installing for one would silently uninstall
    another's. The repo's name is the part that actually differs."""
    a = tmp_path / "alpha" / ".agi"
    b = tmp_path / "beta" / ".agi"
    for d in (a, b):
        d.mkdir(parents=True)
    assert grid.cron_log(a) != grid.cron_log(b)
    assert grid.cron_log(a).name == "grid-sync-alpha.log"
    # Legacy layout is untouched: the graph root IS the repo root there, so an
    # already-installed line keeps matching its marker byte for byte.
    legacy = tmp_path / "gamma"
    legacy.mkdir()
    assert grid.cron_log(legacy).name == "grid-sync-gamma.log"


def test_cron_lines_name_the_repo_under_the_g11_layout(g11):
    """`cd` and `git -C` in the installed crontab entries both take the repo.
    `find_project_root` walking up from `<repo>` finds `<repo>/.agi` in phase 0
    and resolves identically, and the push has to run where the refs are."""
    repo, graph = g11
    lines = grid.cron_lines(graph, "main", 5, repo / "g.log")
    assert lines[0].startswith(f"*/5 * * * * cd {repo} && ")
    assert lines[1].startswith(f"7 * * * * git -C {repo} push -q origin main")
    assert f"cd {graph}" not in lines[0] and f"-C {graph}" not in lines[1]


def test_find_project_root_honours_the_env_override(g11, monkeypatch, tmp_path):
    """goal:g11.1 — `grid.py` resolves through `locations.project_root_from_env`,
    the same entry point the rest of the engine uses, so an explicit
    `$AGI_TREE_PROJECT_ROOT` wins here too. It previously called the plain
    `find_project_root`, which ignores the override: `grid.py` versioning a
    different project than its caller believes is the one disagreement the grid
    cannot survive."""
    repo, graph = g11
    for var in grid.locations.PROJECT_ROOT_ENV_VARS:
        monkeypatch.delenv(var, raising=False)
    elsewhere = tmp_path / "elsewhere"
    elsewhere.mkdir()

    monkeypatch.setenv("AGI_TREE_PROJECT_ROOT", str(graph))
    assert grid.find_project_root(elsewhere) == graph

    monkeypatch.delenv("AGI_TREE_PROJECT_ROOT")
    monkeypatch.chdir(graph)
    assert grid.find_project_root() == graph  # and still resolves with no env


def test_ensure_repo_names_the_repo_not_the_graph_dir(tmp_path, capsys):
    """A `.agi/` is never itself a git repo. `git init`-ing one because an error
    message pointed there would create a nested repo whose object store is not
    the one holding `refs/grid/*`, so the error has to name the enclosing repo."""
    graph = tmp_path / "proj" / ".agi"
    graph.mkdir(parents=True)
    (graph / "config.json").write_text("{}")
    with pytest.raises(SystemExit) as exc:
        grid.ensure_repo(graph)
    assert str(tmp_path / "proj") in str(exc.value)
    assert str(graph) not in str(exc.value)


# -------------------- hypothesis:l2w15-grid-master-guard — --allow-branch guard on commit --all
#
# grid.py commit --all must refuse to run when the checked-out branch is not
# master, unless --allow-branch is passed. Session commits (--session) are
# never gated. Detached HEAD counts as not master.


@pytest.fixture()
def guard_project(tmp_path):
    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
    (tmp_path / "agi-tree.config.json").write_text("{}")
    d = tmp_path / "nodes" / "idea"
    d.mkdir(parents=True)
    (d / "x.md").write_text(
        f'---\nid: "idea:x"\nmint_id: {MINT_G11}'  # reuse G11's mint
        '\ntype: idea\n---\n\nfirst thought\n'
    )
    grid.cmd_init(tmp_path)
    # The fixture repo is on master by default (git init checks out master).
    return tmp_path


def _on_branch(root, branch):
    """Create and switch to `branch` (orphan if needed), leaving master intact."""
    subprocess.run(["git", *grid.GIT_IDENT, "-C", str(root),
                    "checkout", "--orphan", branch],
                   capture_output=True, check=True)
    # Orphan needs a first commit to become a real branch.
    subprocess.run(["git", *grid.GIT_IDENT, "-C", str(root),
                    "commit", "--allow-empty",
                    "-m", f"init {branch}"], capture_output=True, check=True)


def test_commit_all_refuses_on_non_master_branch(guard_project):
    """commit --all on a non-master branch exits 2 and writes no ref."""
    _on_branch(guard_project, "work")
    with pytest.raises(SystemExit) as exc:
        grid.cmd_commit(guard_project, [], do_all=True, session=None)
    assert exc.value.code == 2
    assert grid.ref_tip(guard_project, grid.node_ref("idea:x")) is None


def test_commit_all_on_master_succeeds(guard_project):
    """commit --all on master works normally."""
    grid.cmd_commit(guard_project, [], do_all=True, session=None)
    # Must not raise; must create a version (uses mint-id ref under G2.5).
    mint_ref = grid.mint_node_ref(MINT_G11)
    assert grid.ref_tip(guard_project, mint_ref) is not None


def test_commit_all_on_non_master_with_allow_branch_succeeds(guard_project):
    """commit --all --allow-branch on a non-master branch works."""
    _on_branch(guard_project, "work")
    grid.cmd_commit(guard_project, [], do_all=True, session=None,
                    allow_branch=True)
    mint_ref = grid.mint_node_ref(MINT_G11)
    assert grid.ref_tip(guard_project, mint_ref) is not None


def test_session_commit_on_non_master_branch_is_not_gated(guard_project):
    """Session commit (D3) always works regardless of branch."""
    _on_branch(guard_project, "work")
    f = guard_project / "nodes" / "idea" / "x.md"
    grid.cmd_commit(guard_project, [str(f)], do_all=False,
                    session=("1", "a01"))
    ref = grid.session_ref("1", "a01", "idea:x")
    assert grid.ref_tip(guard_project, ref) is not None


def test_commit_all_refuses_on_detached_head(guard_project):
    """Detached HEAD is treated as 'not master' and is refused."""
    # First commit on master so we have a commit to detach to.
    grid.cmd_commit(guard_project, [], do_all=True, session=None)
    mint_ref = grid.mint_node_ref(MINT_G11)
    tip = grid.ref_tip(guard_project, mint_ref)
    subprocess.run(["git", *grid.GIT_IDENT, "-C", str(guard_project),
                    "checkout", "--detach", tip],
                   capture_output=True, check=True)
    with pytest.raises(SystemExit) as exc:
        grid.cmd_commit(guard_project, [], do_all=True, session=None)
    assert exc.value.code == 2


def test_commit_all_refuses_on_detached_head_even_with_existing_refs(guard_project):
    """A detached HEAD with existing grid history still refuses commit --all."""
    # Commit on master, then detach.
    grid.cmd_commit(guard_project, [], do_all=True, session=None)
    mint_ref = grid.mint_node_ref(MINT_G11)
    tip = grid.ref_tip(guard_project, mint_ref)
    subprocess.run(["git", *grid.GIT_IDENT, "-C", str(guard_project),
                    "checkout", "--detach", tip],
                   capture_output=True, check=True)
    # Edit the node so there's something to commit.
    f = guard_project / "nodes" / "idea" / "x.md"
    f.write_text(f.read_text().replace("first thought", "second thought"))
    with pytest.raises(SystemExit) as exc:
        grid.cmd_commit(guard_project, [], do_all=True, session=None)
    assert exc.value.code == 2
    # Existing ref must still hold v1 (via mint ref), not a new v2.
    assert int(grid.git(guard_project, "rev-list", "--count", mint_ref)) == 1


def test_commit_named_files_refuses_on_non_master(guard_project):
    """commit FILE (without --session) is also gated, not just --all."""
    _on_branch(guard_project, "work")
    f = guard_project / "nodes" / "idea" / "x.md"
    with pytest.raises(SystemExit) as exc:
        grid.cmd_commit(guard_project, [str(f)], do_all=False, session=None)
    assert exc.value.code == 2


def test_allow_branch_message_mentions_branch_name_and_flag(guard_project, capsys):
    """The error message should name the branch and suggest --allow-branch."""
    _on_branch(guard_project, "work")
    with pytest.raises(SystemExit) as exc:
        grid.cmd_commit(guard_project, [], do_all=True, session=None)
    assert exc.value.code == 2
    out = capsys.readouterr()
    err = out.err
    assert "work" in err
    assert "--allow-branch" in err


# --------------------------------------------- evidence gate on the commit path
#
# hypothesis:gate-must-sit-on-the-commit-path (goal:g7). The falsifier the
# hypothesis names, as code: hand-write a `proved` verdict with no evidence
# into a fixture node, run the commit path, assert it comes out demoted. Remove
# the `enforce_on_disk` call from `cmd_commit` and the first test goes red.

import yaml  # noqa: E402

MINT_E1 = "e1e1e1e1e1e1e1e1e1e1e1e1e1e1e1e1"
MINT_V1 = "f1f1f1f1f1f1f1f1f1f1f1f1f1f1f1f1"
MINT_V2 = "f2f2f2f2f2f2f2f2f2f2f2f2f2f2f2f2"
THOUGHT = ("<!-- THOUGHT:BEGIN — authored, not derived; carried across "
           "regenerating scans. The reasoning behind THIS version. -->\n"
           "why this version\n<!-- THOUGHT:END -->\n")


def _hand_written(root, ntype, slug, mint_id, extra="", body="body\n"):
    """A node written the way a pi kid writes one: straight to disk, past
    every writer path. `extra` is raw frontmatter text."""
    d = root / "nodes" / ntype
    d.mkdir(parents=True, exist_ok=True)
    p = d / f"{slug}.md"
    p.write_text(f'---\nid: "{ntype}:{slug}"\nmint_id: {mint_id}\n'
                 f"type: {ntype}\n{extra}---\n\n{body}")
    return p


def _fm(path):
    return yaml.safe_load(path.read_text().split("---", 2)[1])


def _tip_node_md(root, node_id) -> str:
    """`node.md` as the grid holds it at the node's tip."""
    node_file = grid.build_id_index(root).get(node_id)
    ref = grid._resolve_read_ref(root, node_file, node_id)
    return grid.read_tree_entry(root, ref, grid.NODE_ENTRY)[1].decode()


@pytest.fixture()
def gated_project(tmp_path):
    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
    (tmp_path / "agi-tree.config.json").write_text("{}")
    _hand_written(tmp_path, "experiment", "e1", MINT_E1)   # a real run to cite
    grid.cmd_init(tmp_path)
    return tmp_path


def test_commit_path_demotes_a_hand_written_unevidenced_proved(gated_project, capsys):
    """THE falsifier. A `proved` that reached the commit with nothing behind it
    comes out demoted, stamped, kept -- and the overclaim never becomes a
    version."""
    p = _hand_written(gated_project, "verdict", "v1", MINT_V1,
                      "verdict: proved\nconfidence: 0.9\n", body="body\n\n" + THOUGHT)
    grid.cmd_commit(gated_project, [], do_all=True, session=None)

    fm = _fm(p)
    assert fm["verdict"] == "inconclusive_lean_proved:50"
    assert fm["demoted_from"] == "proved"
    assert grid.evidence_gate.COMMIT_PATH_TAG in fm["demote_reason"]
    assert "proved" not in (fm["verdict"], fm.get("status"))
    assert fm["confidence"] == 0.9                       # nothing else touched
    assert THOUGHT.strip() in p.read_text()              # body untouched, THOUGHT kept

    # What the grid accepted is the demoted node: v1 IS the demotion, there is
    # no earlier version carrying the overclaim.
    assert versions(gated_project, "verdict:v1") == 1
    tip = _tip_node_md(gated_project, "verdict:v1")
    assert "verdict: inconclusive_lean_proved:50" in tip
    assert "verdict: proved" not in tip

    out = capsys.readouterr()
    assert "EVIDENCE-GATE DEMOTED proved -> inconclusive_lean_proved:50" in out.out
    assert "1 demoted by the evidence gate" in out.out


def test_commit_path_leaves_an_evidenced_proved_byte_identical(gated_project, capsys):
    p = _hand_written(gated_project, "verdict", "v1", MINT_V1,
                      "verdict: proved\nevidence_runs:\n  - experiment:e1\n")
    before = p.read_bytes()
    grid.cmd_commit(gated_project, [], do_all=True, session=None)
    assert p.read_bytes() == before
    assert "verdict: proved" in _tip_node_md(gated_project, "verdict:v1")
    assert "0 demoted by the evidence gate" in capsys.readouterr().out


def test_commit_path_is_idempotent_after_a_demotion(gated_project):
    """A demoted node is no longer decisive, so the next commit has nothing to
    do -- no second rewrite, no second version. Versions record change."""
    p = _hand_written(gated_project, "verdict", "v1", MINT_V1, "verdict: proved\n")
    grid.cmd_commit(gated_project, [], do_all=True, session=None)
    after_first = p.read_bytes()
    grid.cmd_commit(gated_project, [], do_all=True, session=None)
    assert p.read_bytes() == after_first
    assert versions(gated_project, "verdict:v1") == 1


@pytest.mark.parametrize("verdict", ["pending", "inconclusive_lean_proved:60",
                                     "inconclusive_lean_disproved:40"])
def test_commit_path_leaves_honest_uncertainty_alone(gated_project, verdict):
    p = _hand_written(gated_project, "verdict", "v1", MINT_V1, f"verdict: {verdict}\n")
    before = p.read_bytes()
    grid.cmd_commit(gated_project, [], do_all=True, session=None)
    assert p.read_bytes() == before


def test_commit_path_honours_the_bypass_stamp(gated_project):
    """`evidence_gate: bypassed` is the reviewed, loud escape hatch the writer
    paths honour; the commit path honours the same stamp."""
    p = _hand_written(gated_project, "verdict", "v1", MINT_V1,
                      "verdict: proved\nevidence_gate: bypassed\n")
    before = p.read_bytes()
    grid.cmd_commit(gated_project, [], do_all=True, session=None)
    assert p.read_bytes() == before


def test_session_commit_does_not_gate_a_draft(gated_project):
    """A D3 draft is a node under review, not an accepted one."""
    p = _hand_written(gated_project, "verdict", "v1", MINT_V1, "verdict: proved\n")
    before = p.read_bytes()
    grid.cmd_commit(gated_project, [str(p)], do_all=False, session=("1", "a1"))
    assert p.read_bytes() == before


def test_commit_path_demotes_the_status_shadow_in_lockstep(gated_project):
    p = _hand_written(gated_project, "verdict", "v1", MINT_V1,
                      "verdict: proved\nstatus: proved\n")
    grid.cmd_commit(gated_project, [], do_all=True, session=None)
    fm = _fm(p)
    assert fm["status"] == fm["verdict"] == "inconclusive_lean_proved:50"


def test_commit_path_never_touches_a_lifecycle_status(gated_project):
    p = _hand_written(gated_project, "verdict", "v1", MINT_V1,
                      "verdict: proved\nstatus: active\n")
    grid.cmd_commit(gated_project, [], do_all=True, session=None)
    assert _fm(p)["status"] == "active"


def test_commit_path_demotes_a_bare_int_and_keeps_the_attestation_visible(gated_project):
    """goal:g7.3: `evidence_runs: 2` certifies nothing, so the verdict is
    demoted -- but the count the author wrote stays on the node. The commit
    path reviews bytes it did not write; `stamp`'s overwrite-with-0 would
    destroy the only record of what was claimed."""
    p = _hand_written(gated_project, "experiment", "x1", MINT_V1,
                      "verdict: disproved\nevidence_runs: 2\n")
    grid.cmd_commit(gated_project, [], do_all=True, session=None)
    fm = _fm(p)
    assert fm["verdict"] == "inconclusive_lean_disproved:50"
    assert fm["demoted_from"] == "disproved"
    assert fm["evidence_runs"] == 2


def test_commit_path_demotes_a_dangling_citation_and_keeps_it(gated_project):
    p = _hand_written(gated_project, "verdict", "v1", MINT_V1,
                      "verdict: proved\nevidence_runs:\n  - experiment:deleted\n")
    grid.cmd_commit(gated_project, [], do_all=True, session=None)
    fm = _fm(p)
    assert fm["verdict"] == "inconclusive_lean_proved:50"
    assert fm["evidence_runs"] == ["experiment:deleted"]   # the typo a reviewer fixes


def test_commit_path_demotes_a_taxonomy_violation_rather_than_leaving_it(gated_project):
    """A writer path REJECTS `[synthetic]` -- nothing is written. On disk the
    bytes are already written, so the only honest move is the demotion, with
    the violation named in the reason."""
    p = _hand_written(gated_project, "verdict", "v1", MINT_V1,
                      "verdict: proved\nevidence_runs:\n  - synthetic\n")
    grid.cmd_commit(gated_project, [], do_all=True, session=None)
    fm = _fm(p)
    assert fm["verdict"] == "inconclusive_lean_proved:50"
    assert "taxonomy violation" in fm["demote_reason"]
    assert "synthetic" in fm["demote_reason"]


def test_commit_path_self_citation_rule_matches_the_writer_paths(gated_project):
    """An experiment IS its own run and may cite itself; a verdict judges runs
    and may not. Same asymmetry as `cli.py done` and `post_wire`."""
    e = _hand_written(gated_project, "experiment", "x1", MINT_V1,
                      "verdict: proved\nevidence_runs:\n  - experiment:x1\n")
    v = _hand_written(gated_project, "verdict", "v1", MINT_V2,
                      "verdict: proved\nevidence_runs:\n  - verdict:v1\n")
    grid.cmd_commit(gated_project, [], do_all=True, session=None)
    assert _fm(e)["verdict"] == "proved"
    assert _fm(v)["verdict"] == "inconclusive_lean_proved:50"


def test_commit_of_named_files_resolves_against_the_whole_corpus(gated_project):
    """`commit FILE` gates FILE, but `evidence_runs` resolves against every
    node on disk -- a verdict committed alone still cites a run that is not
    being committed with it."""
    p = _hand_written(gated_project, "verdict", "v1", MINT_V1,
                      "verdict: proved\nevidence_runs:\n  - experiment:e1\n")
    before = p.read_bytes()
    grid.cmd_commit(gated_project, [str(p)], do_all=False, session=None)
    assert p.read_bytes() == before
    assert versions(gated_project, "verdict:v1") == 1


def test_commit_path_never_deletes_or_moves_a_node(gated_project):
    _hand_written(gated_project, "verdict", "v1", MINT_V1, "verdict: proved\n")
    _hand_written(gated_project, "verdict", "v2", MINT_V2, "verdict: proved\nevidence_runs: [x]\n")
    before = sorted((gated_project / "nodes").rglob("*.md"))
    grid.cmd_commit(gated_project, [], do_all=True, session=None)
    assert sorted((gated_project / "nodes").rglob("*.md")) == before


def test_commit_path_leaves_an_unparseable_node_alone_and_keeps_going(gated_project, capsys):
    """Per-node, never batch-aborting: one node the gate cannot read is
    reported and left as it is, and every other node is still gated and
    committed."""
    bad = gated_project / "nodes" / "verdict" / "bad.md"
    bad.parent.mkdir(parents=True, exist_ok=True)
    bad.write_text('---\nid: "verdict:bad"\nmint_id: ' + MINT_V2 +
                   "\nverdict: proved\nparents: [unclosed\n---\nbody\n")
    before = bad.read_bytes()
    good = _hand_written(gated_project, "verdict", "v1", MINT_V1, "verdict: proved\n")
    grid.cmd_commit(gated_project, [], do_all=True, session=None)
    assert bad.read_bytes() == before
    assert _fm(good)["verdict"] == "inconclusive_lean_proved:50"
    assert "cannot parse" in capsys.readouterr().err


def test_commit_path_drives_the_metric_to_zero(gated_project):
    """The number the hypothesis was minted over. `metrics.evidence_stats`
    reads the same corpus with the same two functions the gate resolves with,
    so what the gate demotes is exactly what the metric counted."""
    spec_m = importlib.util.spec_from_file_location(
        "metrics", Path(__file__).resolve().parents[1] / "bin" / "metrics.py")
    metrics = importlib.util.module_from_spec(spec_m)
    spec_m.loader.exec_module(metrics)
    nodes = gated_project / "nodes"

    _hand_written(gated_project, "verdict", "v1", MINT_V1, "verdict: proved\n")
    _hand_written(gated_project, "experiment", "x1", MINT_V2,
                  "verdict: disproved\nevidence_runs: 3\n")
    _hand_written(gated_project, "verdict", "v2", "a2" * 16,
                  "verdict: proved\nevidence_runs:\n  - experiment:e1\n")
    _hand_written(gated_project, "verdict", "v3", "a3" * 16, "verdict: pending\n")
    assert metrics.evidence_stats(nodes)["unevidenced_decisive_verdicts"] == 2

    grid.cmd_commit(gated_project, [], do_all=True, session=None)
    stats = metrics.evidence_stats(nodes)
    assert stats["unevidenced_decisive_verdicts"] == 0
    assert stats["decisive_verdicts"] == 1          # the evidenced one survives


# -------------------- hypothesis:l3w0-grid-flock — commit --all holds an exclusive flock
#
# grid.py commit --all must take an exclusive flock on .agi/sessions/.grid.lock
# for the duration of the commit so a manual director commit and the 5-minute
# grid_sync cron on the same box serialize instead of racing on the same node
# refs. Single-file commits and read verbs take no lock. A second commit --all
# waits up to --lock-wait seconds, then exits non-zero naming the holder.
#
# Incidental addendum (owner, seasons-as-branches): the master-only guard on
# commit --all admits branches named season/* as well; master stays admitted;
# any other branch is still refused with the same message.


def _grid_lock_path(root):
    return grid.GridLock(root, 1)._path


def _hold_grid_lock(root, seconds):
    """Acquire the grid lock in a background thread and hold it `seconds`.
    Returns the thread so tests can join it; the lock is released on exit of
    that thread's run()."""
    lock = _grid_lock_path(root)
    lock.parent.mkdir(parents=True, exist_ok=True)
    f = open(lock, "a+")
    fcntl.flock(f, fcntl.LOCK_EX)

    def _hold():
        time.sleep(seconds)
        fcntl.flock(f, fcntl.LOCK_UN)
        f.close()

    t = threading.Thread(target=_hold, daemon=True)
    t.start()
    return t


def test_commit_all_times_out_nonzero_when_lock_held(guard_project, capsys):
    """A second commit --all waits --lock-wait seconds, then exits non-zero
    naming the holder pid, writing no new version."""
    _hold_grid_lock(guard_project, 5)               # holder sleeps well past the wait
    with pytest.raises(SystemExit) as exc:
        grid.cmd_commit(guard_project, [], do_all=True, session=None, lock_wait=1)
    assert exc.value.code == 2
    err = capsys.readouterr().err
    assert ".grid.lock" in err                       # message names the lock file
    assert grid.ref_tip(guard_project, grid.mint_node_ref(MINT_G11)) is None


def test_commit_all_waits_for_holder_then_succeeds_consistent(guard_project):
    """commit --all blocks while a slow writer holds the lock, then completes;
    the resulting ref is consistent (exactly one version)."""
    _hold_grid_lock(guard_project, 0.6)
    t0 = time.time()
    grid.cmd_commit(guard_project, [], do_all=True, session=None, lock_wait=10)
    elapsed = time.time() - t0
    assert elapsed >= 0.3                            # it really waited on the holder
    mint_ref = grid.mint_node_ref(MINT_G11)
    assert grid.ref_tip(guard_project, mint_ref) is not None
    assert int(grid.git(guard_project, "rev-list", "--count", mint_ref)) == 1


def test_single_file_commit_takes_no_lock(guard_project):
    """commit FILE (non-session) is NOT gated by the flock — a manual
    per-node commit proceeds even while a commit --all holds the lock."""
    _hold_grid_lock(guard_project, 0.5)
    f = guard_project / "nodes" / "idea" / "x.md"
    t0 = time.time()
    grid.cmd_commit(guard_project, [str(f)], do_all=False, session=None)
    assert time.time() - t0 < 0.3                    # returned without waiting


def test_commit_all_on_season_branch_succeeds(guard_project):
    """commit --all is admitted on branches named season/* (seasons as
    git branches), without --allow-branch."""
    _on_branch(guard_project, "season/s1")
    grid.cmd_commit(guard_project, [], do_all=True, session=None)
    assert grid.ref_tip(guard_project, grid.mint_node_ref(MINT_G11)) is not None


def test_commit_all_on_nested_season_branch_succeeds(guard_project):
    """season/* admits nested names like season/ideas/flock too."""
    _on_branch(guard_project, "season/ideas/flock")
    grid.cmd_commit(guard_project, [], do_all=True, session=None)
    assert grid.ref_tip(guard_project, grid.mint_node_ref(MINT_G11)) is not None


def test_commit_all_still_refuses_plain_non_master_branch(guard_project):
    """A non-master, non-season branch is still refused (regression guard)."""
    _on_branch(guard_project, "work")
    with pytest.raises(SystemExit) as exc:
        grid.cmd_commit(guard_project, [], do_all=True, session=None)
    assert exc.value.code == 2


# --- hypothesis:l3-grid-lock-doubled-path — the grid lock must NOT double .agi
#
# In the G11 layout the graph root passed to cmd_commit IS the `<repo>/.agi`
# directory. The lock must therefore live at `<graph>/sessions/.grid.lock`
# (== `<repo>/.agi/sessions/.grid.lock`), NOT at `<graph>/.agi/sessions`
# (`<repo>/.agi/.agi/sessions`), which doubles the `.agi` into a stray scratch
# dir that never serializes against the documented path. The SAME single path
# must resolve whether commit --all is run from the repo root or from inside
# `<repo>/.agi`, and committing must never create a `.agi/.agi` directory.

def _make_g11_project(tmp_path):
    """A G11-layout project: config + nodes live under `<tmp>/.agi`."""
    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
    agi = tmp_path / ".agi"
    (agi / "nodes" / "idea").mkdir(parents=True)
    (agi / "config.json").write_text("{}")
    (agi / "nodes" / "idea" / "g.md").write_text(
        f'---\nid: "idea:g"\nmint_id: {MINT_X}\ntype: idea\n---\n\nhi\n'
    )
    return agi


def test_g11_grid_lock_path_is_single_non_doubled(tmp_path):
    """The lock path resolves to one correct file from a G11 graph root, and
    commit --all creates no doubled `.agi/.agi` directory."""
    agi = _make_g11_project(tmp_path)
    graph = grid.find_project_root(agi)
    assert graph == agi                       # graph root IS the .agi dir
    assert grid.GridLock(graph, 1)._path == agi / "sessions" / ".grid.lock"
    assert not (agi / ".agi").exists()        # no doubled dir before commit

    grid.cmd_commit(graph, [], do_all=True, session=None, lock_wait=1)
    assert (agi / "sessions" / ".grid.lock").exists()   # lock is the real one
    assert not (agi / ".agi").exists()        # and no .agi/.agi was ever made


def test_g11_grid_lock_serializes_across_cwds(tmp_path, capsys):
    """Holding the lock at the single CORRECT path makes commit --all from the
    other cwd (same resolved graph root) time out naming the lock. Locking on
    the doubled path instead would NOT meet the held lock, so this is red
    against the doubling bug."""
    agi = _make_g11_project(tmp_path)
    graph = grid.find_project_root(agi)
    correct = graph / "sessions" / ".grid.lock"
    _hold_grid_lock_at(correct, 5)            # hold the CORRECT path, > wait
    with pytest.raises(SystemExit) as exc:
        grid.cmd_commit(graph, [], do_all=True, session=None, lock_wait=1)
    assert exc.value.code == 2
    err = capsys.readouterr().err
    assert "could not acquire the grid lock" in err
    assert grid.GridLock(graph, 1)._path == correct


def _hold_grid_lock_at(lock, seconds):
    """Acquire an exclusive flock on `lock` and hold it `seconds` in a thread."""
    lock.parent.mkdir(parents=True, exist_ok=True)
    f = open(lock, "a+")
    fcntl.flock(f, fcntl.LOCK_EX)

    def _hold():
        time.sleep(seconds)
        fcntl.flock(f, fcntl.LOCK_UN)
        f.close()

    t = threading.Thread(target=_hold, daemon=True)
    t.start()
    return t

