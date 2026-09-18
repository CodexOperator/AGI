"""The generic `actor_rows:` write grant in write.py.

hypothesis:l4-the-formation-owner-writes-config-posts-rows-and-the-town-master-
cell-through-a-schema-declared-actor-row-grant-never-a-role-literal (g15 build
order). A schema declares, as a LIST, which RESOLVED seats may write which row
list or single field; a future grant is ONE schema line, never a new branch in
write.py. The identity is the resolved seat name, never a role literal or the
free-text `--actor` string.

Acceptance, all through the REAL entry point `write.submit` (and `write.main`
for the create side), on a FIXTURE root that never touches the live nodes:

  1. the `sanctuary-master` seat sets a posts row's `town` cell, CREATES a row
     and RETIRES a row -> each is written;
  2. `director-belam` and a kid actor on the same posts edit -> refused by name;
  3. `sanctuary-master` touching a field outside the grant -> refused by name;
  4. `sanctuary-master` sets the town `master` cell -> written; the town
     `branches` cell stays refused by name at mint and at read;
  5. the legacy `master_sensei_row` path still admits master-sensei and still
     refuses prime_director, in THIS file, so a regression is caught here as
     well as by test_write_master_sensei.py.
"""
from __future__ import annotations

import copy
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
import towns  # noqa: E402

ROOT = Path(__file__).resolve().parents[3]
LIVE_CONFIG = ROOT / ".agi" / "context" / "schemas" / "[config].md"
LIVE_TOWN = ROOT / ".agi" / "context" / "schemas" / "[town].md"

ROWS = [
    {"name": "sanctuary-master", "role": "director", "town": "sanctuary"},
    {"name": "master-sensei", "role": "director", "town": "sanctuary"},
    {"name": "director-belam", "role": "director", "town": "core"},
    {"name": "kid-worker", "role": "kid", "town": "core"},
    {"name": "council-core", "role": "council", "town": "core"},
]

TEMPLATES = {
    "director": {
        "brief_file": ".agi/sessions/quorum/{seat}.md",
        "steps": ["handoff", "spawn", "join", "authority", "release"],
        "telemetry": ["seed", "model"],
        "startup": {
            "first_turn": [
                {"label": "rotation-record", "cmd": "python3 extensions/agi/bin/rotate.py status --seat {seat} --record latest", "why": "x"},
            ],
            "after_join": [
                {"label": "ack", "cmd": "python3 extensions/agi/bin/rotate.py ack --seat {seat} --gen {gen} --ref {succ_ref} continue", "why": "y"},
            ],
        },
    },
    "prime_director": {
        "brief_file": "extensions/agi/briefs/prime-director-successor.md",
        "steps": ["handoff", "reap", "belam-cap"],
        "telemetry": ["seed", "model"],
        "startup": {"first_turn": [], "after_join": []},
    },
}


def _write(project: Path, rel: str, text: str) -> None:
    p = project / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")


def _posts_node(rows) -> str:
    body = "\n".join(f"  - {json.dumps(r)}" for r in rows)
    return ("---\nid: config:posts\nmint_id: 3e88873e3c204c5088f6ab81322a26de\n"
            "type: config\nparents:\n  - goal:g17\nposts:\n" + body +
            "\n---\n\n# config:posts\n\nfixture\n")


def _rotations_node() -> str:
    body = ("# config:rotations\n\npreamble\n\n## templates\n\nkeep me\n\n"
            "## facts\n\n- F1 probe one\n- F2 probe two\n\n"
            "## steps\n\nkeep me too\n")
    return ("---\nid: config:rotations\nmint_id: 4d469eed090b47a8bb039eb40d96f861\n"
            "type: config\nparents:\n  - hypothesis:x\n"
            "templates: " + json.dumps(TEMPLATES) + "\n---\n\n" + body + "\n")


@pytest.fixture()
def project(tmp_path: Path) -> Path:
    root = tmp_path
    agi = root / ".agi"
    agi.mkdir(parents=True, exist_ok=True)
    (agi / "config.json").write_text("{}", encoding="utf-8")
    assert LIVE_CONFIG.is_file() and LIVE_TOWN.is_file(), \
        "the live [config].md and [town].md schemas must exist"
    _write(agi, "context/schemas/[config].md", LIVE_CONFIG.read_text(encoding="utf-8"))
    _write(agi, "context/schemas/[town].md", LIVE_TOWN.read_text(encoding="utf-8"))
    _write(agi, "nodes/.geometry/ladder.md",
           "---\nid: ladder:ladder\ncurrent_season: 2\n"
           "towns: [core, sanctuary, streaming-suite]\n---\n\n# ladder\n")
    _write(agi, "nodes/.geometry/posts.md", _posts_node(ROWS))
    _write(agi, "nodes/.geometry/rotations.md", _rotations_node())
    _write(agi, "nodes/town/core.md",
           "---\nid: town:core\ntype: town\nvisions: [vision:a]\n"
           "council: council-core\nseason: 2\nmaster: ''\n---\n\n# town\n")
    _write(agi, "nodes/vision/a.md", "---\nid: vision:a\ntype: vision\n---\n\nv\n")
    return agi  # the graph root, what find_project_root returns


def _clone_rows():
    return [dict(r) for r in ROWS]


def _posts_edit(rows):
    e = write.Edit("config:posts")
    write.verb_set(e, "posts", json.dumps(rows))
    return e


def _templates_edit(templates):
    e = write.Edit("config:rotations")
    write.verb_set(e, "templates", json.dumps(templates))
    return e


# --- 1. the declared seat writes ------------------------------------------

def test_sanctuary_master_sets_a_posts_row_town_cell(project):
    """`set town sanctuary` on a row, by the declared seat, is WRITTEN."""
    rows = _clone_rows()
    rows[2]["town"] = "sanctuary"
    res = write.submit(project, _posts_edit(rows), actor="sanctuary-master")
    assert res.status == node_writer.UPDATED
    assert "\"town\": \"sanctuary\"" in \
        (project / "nodes/.geometry/posts.md").read_text(encoding="utf-8")


def test_sanctuary_master_creates_a_posts_row(project):
    """`ops: [create]` — the declared seat adds a row -> WRITTEN."""
    rows = _clone_rows()
    rows.append({"name": "new-post", "role": "director", "town": "core"})
    res = write.submit(project, _posts_edit(rows), actor="sanctuary-master")
    assert res.status == node_writer.UPDATED
    assert "new-post" in \
        (project / "nodes/.geometry/posts.md").read_text(encoding="utf-8")


def test_sanctuary_master_retires_a_posts_row(project):
    """`ops: [retire]` — the declared seat drops a row -> WRITTEN."""
    rows = [r for r in _clone_rows() if r["name"] != "kid-worker"]
    res = write.submit(project, _posts_edit(rows), actor="sanctuary-master")
    assert res.status == node_writer.UPDATED
    assert "kid-worker" not in \
        (project / "nodes/.geometry/posts.md").read_text(encoding="utf-8")


# --- 2. every other seat is refused by name --------------------------------

def test_director_belam_refused_by_name(project):
    rows = _clone_rows()
    rows[2]["town"] = "sanctuary"
    with pytest.raises(write.EditError) as ei:
        write.submit(project, _posts_edit(rows), actor="director-belam")
    assert "seated role" in str(ei.value)


def test_kid_actor_refused_by_name(project):
    rows = _clone_rows()
    rows[2]["town"] = "sanctuary"
    with pytest.raises(write.EditError) as ei:
        write.submit(project, _posts_edit(rows), actor="kid-worker-1a")
    assert "seated role" in str(ei.value)


# --- 3. a field outside the grant is refused by name -----------------------

def test_sanctuary_master_field_outside_grant_refused(project):
    rows = _clone_rows()
    rows[2]["owning_goal"] = "goal:g99"
    with pytest.raises(write.EditError) as ei:
        write.submit(project, _posts_edit(rows), actor="sanctuary-master")
    msg = str(ei.value)
    assert "owning_goal" in msg and "actor_rows" in msg


# --- 4. the town master cell; branches stays refused -----------------------

def test_sanctuary_master_sets_town_master_cell(project):
    e = write.Edit("town:core")
    write.verb_set(e, "master", "sanctuary-master")
    res = write.submit(project, e, actor="sanctuary-master")
    assert res.status == node_writer.UPDATED
    assert "master: sanctuary-master" in \
        (project / "nodes/town/core.md").read_text(encoding="utf-8")


def test_sanctuary_master_other_town_field_refused(project):
    e = write.Edit("town:core")
    write.verb_set(e, "season", "9")
    with pytest.raises(write.EditError) as ei:
        write.submit(project, e, actor="sanctuary-master")
    assert "season" in str(ei.value)


def test_town_branches_refused_at_mint(project, capsys):
    rc = write.main(["create", "town", "with-branches", "--parent", "ladder:ladder",
                     "--root", str(project.parent), "--actor", "owner",
                     "--set", 'visions=["vision:a"]',
                     "--set", "council=council-core", "--set", "season=2",
                     "--set", "branches=[core/main]"])
    assert rc == 2
    err = capsys.readouterr().err
    assert "branches" in err, err
    assert not (project / "nodes/town/with-branches.md").exists()


def test_town_branches_refused_at_read(project):
    _write(project, "nodes/town/bad.md",
           "---\nid: town:bad\ntype: town\nvisions: [vision:a]\n"
           "council: council-core\nseason: 1\nbranches: [core/main]\n---\n\n# badly born\n")
    with pytest.raises(towns.TownError) as ei:
        towns.load_towns(project)
    assert "branches" in str(ei.value)


# --- 5. the legacy master_sensei_row path, in THIS file ---------------------

def test_legacy_master_sensei_row_still_admits(project):
    new = copy.deepcopy(TEMPLATES)
    new["director"]["telemetry"] = ["seed", "model", "ack"]
    res = write.submit(project, _templates_edit(new), actor="master-sensei")
    assert res.status == node_writer.UPDATED


def test_legacy_master_sensei_row_still_refuses_prime_director(project):
    new = copy.deepcopy(TEMPLATES)
    new["prime_director"]["telemetry"] = ["seed", "model", "window"]
    with pytest.raises(write.EditError) as ei:
        write.submit(project, _templates_edit(new), actor="master-sensei")
    assert "prime_director" in str(ei.value)


# --- 6. SM.108 corrective: the three residues, each with its twin -----------

def test_chained_list_edit_plus_ungranted_top_level_key_refused(project):
    """Defect (2): a legal posts-list edit that ALSO sets a top-level key
    outside the grant (`owning_goal`) is refused BY NAME."""
    rows = _clone_rows()
    rows[2]["town"] = "sanctuary"          # a legal row edit on its own
    e = _posts_edit(rows)
    write.verb_set(e, "owning_goal", "goal:g99")   # the smuggled top-level key
    with pytest.raises(write.EditError) as ei:
        write.submit(project, e, actor="sanctuary-master")
    msg = str(ei.value)
    assert "owning_goal" in msg and "actor_rows" in msg
    assert "owning_goal" not in \
        (project / "nodes/.geometry/posts.md").read_text(encoding="utf-8")


def test_chained_list_edit_alone_still_written(project):
    """Twin of defect (2): the SAME legal list edit without the smuggled
    top-level key is still written."""
    rows = _clone_rows()
    rows[2]["town"] = "sanctuary"
    res = write.submit(project, _posts_edit(rows), actor="sanctuary-master")
    assert res.status == node_writer.UPDATED


def test_create_row_with_ungranted_field_refused(project):
    """Defect (4): a `create` row carrying `pubkey` (outside the grant's
    fields) is refused BY NAME, not silently admitted."""
    rows = _clone_rows()
    rows.append({"name": "new-post", "role": "director", "town": "core",
                 "pubkey": "deadbeef" * 8})
    with pytest.raises(write.EditError) as ei:
        write.submit(project, _posts_edit(rows), actor="sanctuary-master")
    msg = str(ei.value)
    assert "pubkey" in msg and "actor_rows" in msg
    assert "pubkey" not in \
        (project / "nodes/.geometry/posts.md").read_text(encoding="utf-8")


def test_create_row_with_only_granted_fields_still_written(project):
    """Twin of defect (4): a `create` row using only granted fields stands."""
    rows = _clone_rows()
    rows.append({"name": "new-post", "role": "director", "town": "core"})
    res = write.submit(project, _posts_edit(rows), actor="sanctuary-master")
    assert res.status == node_writer.UPDATED


def test_unrecognised_actor_rows_entry_refused_by_name(project):
    """Defect (3b): the live `[config].md` declares the master-sensei entry
    with `role_field` and no `match_key`; a master-sensei write that reaches
    the generic resolver is refused BY NAME, never silently falls through."""
    with pytest.raises(write.EditError) as ei:
        write.submit(project, _posts_edit(_clone_rows()), actor="master-sensei")
    msg = str(ei.value)
    assert "actor_rows" in msg and "no shape" in msg


def test_well_formed_entry_unaffected(project):
    """Twin of defect (3b): the well-formed sanctuary-master entry on the
    same schema is unaffected by the unrecognised-shape refusal."""
    rows = _clone_rows()
    rows[2]["town"] = "sanctuary"
    res = write.submit(project, _posts_edit(rows), actor="sanctuary-master")
    assert res.status == node_writer.UPDATED
