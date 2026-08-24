"""Tests for bin/grid.py — the per-node git grid, in-repo ref-namespace mode."""

import importlib.util
import subprocess
import sys
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parents[1] / "bin" / "grid.py"
spec = importlib.util.spec_from_file_location("grid", BIN)
grid = importlib.util.module_from_spec(spec)
spec.loader.exec_module(grid)


@pytest.fixture()
def project(tmp_path):
    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
    (tmp_path / "agi-tree.config.json").write_text("{}")
    d = tmp_path / "nodes" / "idea"
    d.mkdir(parents=True)
    (d / "x.md").write_text(
        '---\nid: "idea:x"\ntype: idea\n---\n\nfirst thought\n'
    )
    grid.cmd_init(tmp_path)
    return tmp_path


def versions(root, node_id):
    tip = grid.ref_tip(root, grid.node_ref(node_id))
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
    ref = grid.node_ref("idea:x")
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
    msg = grid.git(project, "log", "-1", "--format=%s", grid.node_ref("idea:x"))
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
    assert "refs/grid/node/idea/x" in out
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
    """Not just adversarial cases -- every id actually on disk today."""
    agi_tree = Path(__file__).resolve().parents[4] / "agi-tree"
    nodes_dir = agi_tree / "nodes"
    if not nodes_dir.is_dir():
        pytest.skip("agi-tree checkout not found beside the engine repo")
    ids = []
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
