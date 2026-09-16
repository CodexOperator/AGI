"""goal:g15.25 SM.32 claim (3) — the row `town` cell is a declared vocabulary.

`town=all` is retired: a config-row write that CHANGES the `town` cell to a
value outside the accepted set (the ladder's declared `towns:` plus `core`)
is refused WHOLE, BY NAME. Judged on the NEW value only, so a row still
spelling `town: all` stays readable and an unrelated write is never refused.

The declaration is the `[config]` schema's `town_cell` block, read from the
LIVE schema bytes so this test pins what the tree ships. Fixture root only;
never touches the live `.agi/nodes/.geometry/posts.md`.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parent.parent / "bin"
SRC = Path(__file__).resolve().parent.parent / "src"
sys.path.insert(0, str(BIN))
sys.path.insert(0, str(SRC))

import write  # noqa: E402
import node_writer  # noqa: E402

# The LIVE schema file, so the test pins the real bytes the suite ships — a
# hand copy here would drift from the schema the prime reviews at merge-up.
LIVE_SCHEMA = (Path(__file__).resolve().parents[3] / ".agi" /
               "context" / "schemas" / "[config].md")

ROWS = [
    {"name": "belam", "role": "prime_director", "town": "all"},
    {"name": "sanctuary-director", "role": "director", "town": "core"},
    {"name": "sanctuary-helper", "role": "director", "town": "core"},
]


def _write_posts_node(project, rows):
    d = project / "nodes" / ".geometry"
    d.mkdir(parents=True, exist_ok=True)
    body = "\n".join(f"  - {json.dumps(r)}" for r in rows)
    (d / "posts.md").write_text(
        "---\nid: config:posts\nmint_id: 3e88873e3c204c5088f6ab81322a26de\n"
        "type: config\nparents:\n  - goal:g17\nposts:\n" + body +
        "\n---\n\n# config:posts\n\nfixture body\n", encoding="utf-8")


def _write_ladder(project):
    d = project / "nodes" / ".geometry"
    d.mkdir(parents=True, exist_ok=True)
    (d / "ladder.md").write_text(
        "---\nid: ladder:ladder\ncurrent_season: 2\ntowns:\n"
        "  - core\n  - sanctuary\n  - streaming-suite\n---\n\n# ladder\n",
        encoding="utf-8")


@pytest.fixture()
def project(tmp_path: Path) -> Path:
    root = tmp_path
    agi = root / ".agi"
    agi.mkdir(parents=True, exist_ok=True)
    (agi / "config.json").write_text("{}", encoding="utf-8")
    sd = agi / "context" / "schemas"
    sd.mkdir(parents=True)
    assert LIVE_SCHEMA.exists(), "the live [config].md schema must exist"
    (sd / "[config].md").write_text(LIVE_SCHEMA.read_text(encoding="utf-8"))
    _write_ladder(agi)
    _write_posts_node(agi, ROWS)
    return agi  # the graph root, what find_project_root returns


def _clone_rows():
    return [dict(r) for r in ROWS]


def _edit(rows):
    e = write.Edit("config:posts")
    write.verb_set(e, "posts", json.dumps(rows))
    return e


def _submit(project, rows, actor="belam-S1-L4-VII"):
    return write.submit(project, _edit(rows), actor=actor)


def test_accepted_set_is_ladder_towns_plus_core(project):
    """The vocabulary is DERIVED: ladder towns ∪ core, and `all` is never in it."""
    import towns
    accepted = towns.accepted_towns(project)
    assert accepted == {"core", "sanctuary", "streaming-suite"}
    assert "all" not in accepted


def test_change_town_to_all_refused_by_name(project):
    """`set town all` on a row whose cell differs is refused WHOLE, naming it."""
    new = _clone_rows()
    new[1]["town"] = "all"
    with pytest.raises(write.EditError) as ei:
        _submit(project, new)
    msg = str(ei.value)
    assert "'all'" in msg and "refused BY NAME" in msg
    # the accepted set is named too
    assert "sanctuary" in msg and "core" in msg
    # NOTHING was written: the row on disk still reads core
    assert "\"town\": \"core\"" in (project / "nodes/.geometry/posts.md").read_text()


def test_change_town_to_sanctuary_accepted(project):
    """`set town sanctuary` is accepted — the ladder declares it."""
    new = _clone_rows()
    new[1]["town"] = "sanctuary"
    res = _submit(project, new)
    assert res.status == node_writer.UPDATED
    assert "\"town\": \"sanctuary\"" in \
        (project / "nodes/.geometry/posts.md").read_text()


def test_change_town_to_core_accepted(project):
    """`set town core` is accepted — `core` is always in the accepted set."""
    new = _clone_rows()
    new[1]["town"] = "core"
    res = _submit(project, new)
    assert res.status in (node_writer.UPDATED, node_writer.UNCHANGED)


def test_change_town_to_bogus_refused_by_name(project):
    """`set town bogus` is refused by name."""
    new = _clone_rows()
    new[1]["town"] = "bogus"
    with pytest.raises(write.EditError) as ei:
        _submit(project, new)
    assert "'bogus'" in str(ei.value)


def test_untouched_all_cell_stays_readable_on_unrelated_write(project):
    """A row still spelling `town: all` is NEVER refused on an unrelated write.

    belam's cell stays `all`; only its `session_name` changes. The write is
    admitted and the `all` cell survives on disk — only the NEW value of a
    TOUCHED cell is judged.
    """
    new = _clone_rows()
    new[0]["session_name"] = "agi-54"
    res = _submit(project, new)
    assert res.status == node_writer.UPDATED
    text = (project / "nodes/.geometry/posts.md").read_text()
    assert "agi-54" in text
    assert "\"town\": \"all\"" in text
