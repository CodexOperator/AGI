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
