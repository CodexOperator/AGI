"""Tests for bin/snapshot-build-site.py.

Scope is deliberately narrow: the `preserve` contract on `write_frontmatter`.
That function rebuilt node frontmatter from `build-site.md` on every run, so any
field a later writer had added was silently dropped. On the live agi-tree corpus
that severed `next_edges` — chain structure — on 15 nodes, as a side effect of a
render pass that reports itself as successful.
"""

import importlib.util
from pathlib import Path

import pytest
import yaml

BIN = Path(__file__).resolve().parents[1] / "bin" / "snapshot-build-site.py"
spec = importlib.util.spec_from_file_location("snapshot_build_site", BIN)
sbs = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sbs)


def fm_of(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8").split("---", 2)[1])


@pytest.fixture()
def node(tmp_path):
    return tmp_path / "n.md"


def test_unowned_fields_survive_a_rewrite(node):
    sbs.write_frontmatter(
        node,
        {"id": "hyp:x", "type": "hypothesis", "title": "first"},
        "body",
        origin="build-site",
    )
    # post_wire.py adds chain structure after the snapshot has run.
    existing = fm_of(node)
    existing["next_edges"] = ["exp:x"]

    sbs.write_frontmatter(
        node,
        {"id": "hyp:x", "type": "hypothesis", "title": "second"},
        "body",
        origin="build-site",
        preserve=existing,
    )

    fm = fm_of(node)
    assert fm["next_edges"] == ["exp:x"]   # the field we do not own
    assert fm["title"] == "second"          # the field we do


def test_snapshot_owned_fields_always_win(node):
    sbs.write_frontmatter(
        node,
        {"id": "task:t-001", "type": "task", "status": "done"},
        "body",
        preserve={"id": "task:t-001", "type": "task", "status": "pending",
                  "tier": 2},
    )
    fm = fm_of(node)
    assert fm["status"] == "done"  # build-site.md is the source of truth
    assert fm["tier"] == 2         # nothing else is touched


def test_preserve_absent_is_the_old_behaviour(node):
    sbs.write_frontmatter(node, {"id": "idea:x", "type": "idea"}, "body")
    assert set(fm_of(node)) == {"id", "type"}


def test_preserve_does_not_mutate_the_callers_dict(node):
    owned = {"id": "idea:x", "type": "idea"}
    carried = {"next_edges": ["hyp:x"]}
    sbs.write_frontmatter(node, owned, "body", origin="build-site",
                          preserve=carried)
    assert owned == {"id": "idea:x", "type": "idea"}
    assert carried == {"next_edges": ["hyp:x"]}


# ------------------------------------------- goals-only projects (goal:g5/L18)


def test_missing_build_site_returns_zero_and_prunes_nothing(tmp_path, monkeypatch, capsys):
    """A goals-only project is a valid state, not a broken one.

    Two defects in one assertion. `parse_tasks` used to `sys.exit(1)`, which
    under driver.sh's `set -euo pipefail` aborted the entire loop — a project
    without a build site could not run at all. And falling through with zero
    parsed tasks would reach the stale-prune, which unlinks every
    `origin: build-site` node not rewritten this run; with nothing parsed that
    is the whole build-site corpus (H0i, 159 of 661 nodes on the live tree).
    """
    nodes = tmp_path / "nodes" / "task"
    nodes.mkdir(parents=True)
    survivor = nodes / "t-001.md"
    survivor.write_text(
        '---\nid: "task:t-001"\ntype: task\norigin: build-site\n---\n\nbody\n',
        encoding="utf-8",
    )
    monkeypatch.setattr(sbs, "BUILD_SITE", tmp_path / "context" / "plans" / "build-site.md")
    monkeypatch.setattr(sbs, "NODES_DIR", tmp_path / "nodes")

    assert sbs.main() == 0
    assert survivor.exists(), "a missing build site must never prune existing nodes"
    assert "goals-only" in capsys.readouterr().out
