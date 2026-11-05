"""goal:g7.16.1.11.46.23 V8a tip 2b: config_rows.write_rows, the narrow writer that replaced write.submit
at the six config:posts write shapes (doc:v8a-submit-guard-census section 1).

Each row of the census that is KEPT has a case that is ADMITTED and a MUTANT that is REFUSED, on a
fixture graph built here (never the live tree): the keygen own-row write, --all-live, the spawn-mint
create, the countersign promotion, the session cells, and the migrate tick's seating cells.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parents[1] / "bin"
sys.path.insert(0, str(BIN))
sys.path.insert(0, str(BIN.parent / "src"))

import config_rows  # noqa: E402
import geometry_config  # noqa: E402

SCHEMA = """---
name: config
written_by: [owner, prime_director]
self_row: {list_key: seats, match_key: name, fields: [session_ref, session_name, session_id, generation, window, pid, pubkey, sig_scheme, enc_scheme, key_history]}
actor_rows:
  - {actor: master, list_key: posts, match_key: name, fields: [town, quiet, status, box, worktree], ops: [create, set, retire], deny_roles: [kid, parent]}
---
# config
"""

ROWS = [
    {"name": "prime", "role": "prime_director", "tier": 1, "model": "m", "pid": 1},
    {"name": "master", "role": "director", "tier": 1, "model": "m", "box": "a", "worktree": "w/master"},
    {"name": "dg1", "role": "director", "tier": 1, "model": "m", "pid": 2},
    {"name": "dg2", "role": "director", "tier": 1, "model": "m", "pid": 3},
    {"name": "kidx", "role": "kid", "tier": "untrusted", "model": "m"},
    {"name": "parent", "role": "parent", "tier": 1, "model": "m"},  # a row NAMED in the grant's deny_roles
]


def _rows_md(rows):
    out = ["---", "id: config:posts", "mint_id: 22222222222222222222222222222222", "type: config",
           "parents: []", "posts:"]
    for r in rows:
        out.append("  - " + "{" + ", ".join(f"{k}: {_v(v)}" for k, v in r.items()) + "}")
    out += ["---", "# posts", ""]
    return "\n".join(out)


def _v(v):
    return '"%s"' % v if isinstance(v, str) else str(v)


@pytest.fixture()
def g(tmp_path):
    root = tmp_path / ".agi"
    (root / "nodes" / ".geometry").mkdir(parents=True)
    (root / "context" / "schemas").mkdir(parents=True)
    (root / "context" / "schemas" / "[config].md").write_text(SCHEMA, encoding="utf-8")
    (root / "config.json").write_text("{}", encoding="utf-8")
    (root / "nodes" / ".geometry" / "posts.md").write_text(_rows_md(ROWS), encoding="utf-8")
    return root


def _rows(root):
    return geometry_config.load_rows(root)


def _with(root, name, **cells):
    rows = [dict(r) for r in _rows(root)]
    for r in rows:
        if r["name"] == name:
            r.update(cells)
    return rows


def _unchanged(root):
    return (root / "nodes" / ".geometry" / "posts.md").read_text(encoding="utf-8")


# ---- (S) own row: keygen and the session cells ------------------------------------------------
def test_keygen_own_row_admitted(g):
    config_rows.write_rows(g, _with(g, "dg1", pubkey="ab", sig_scheme="s", enc_scheme="none", key_history=[]),
                           actor="dg1", declare={"dg1": ("set", config_rows.KEYGEN_KEYS)})
    assert next(r for r in _rows(g) if r["name"] == "dg1")["pubkey"] == "ab"


def test_mutant_keygen_writing_another_posts_row_is_refused(g):
    before = _unchanged(g)
    with pytest.raises(config_rows.RowWriteRefused):
        config_rows.write_rows(g, _with(g, "dg2", pubkey="cd"), actor="dg1",
                               declare={"dg2": ("set", config_rows.KEYGEN_KEYS)})
    assert _unchanged(g) == before


def test_mutant_own_row_protected_cell_is_refused(g):
    before = _unchanged(g)
    with pytest.raises(config_rows.RowWriteRefused):
        config_rows.write_rows(g, _with(g, "dg1", model="x/y"), actor="dg1", declare={"dg1": ("set", {"model"})})
    assert _unchanged(g) == before


def test_mutant_site_declares_one_row_but_the_write_changes_two(g):
    rows = _with(g, "dg1", pubkey="ab")
    rows = [dict(r, pubkey="zz") if r["name"] == "dg2" else r for r in rows]
    with pytest.raises(config_rows.RowWriteRefused, match="did not declare"):
        config_rows.write_rows(g, rows, actor="dg1", declare={"dg1": ("set", config_rows.KEYGEN_KEYS)})


def test_mutant_site_declares_pubkey_but_the_write_changes_a_cell_outside_it(g):
    with pytest.raises(config_rows.RowWriteRefused, match="outside"):
        config_rows.write_rows(g, _with(g, "dg1", pubkey="ab", pid=99), actor="dg1",
                               declare={"dg1": ("set", {"pubkey"})})


def test_session_cells_own_row_admitted(g):
    config_rows.write_rows(g, _with(g, "dg1", pid=77, window="@3"), actor="dg1",
                           declare={"dg1": ("set", {"pid", "window"})})
    assert next(r for r in _rows(g) if r["name"] == "dg1")["pid"] == 77


# ---- (W) written_by: --all-live, spawn-mint, countersign ---------------------------------------
def test_all_live_by_a_prime_admitted_many_rows(g):
    rows = _with(g, "dg1", pubkey="a1")
    rows = [dict(r, pubkey="a2") if r["name"] == "dg2" else r for r in rows]
    config_rows.write_rows(g, rows, actor="prime",
                           declare={n: ("set", config_rows.KEYGEN_KEYS) for n in ("dg1", "dg2")})
    assert {r["name"]: r.get("pubkey") for r in _rows(g)}["dg2"] == "a2"


def test_mutant_all_live_by_a_non_prime_is_refused(g):
    with pytest.raises(config_rows.RowWriteRefused):
        config_rows.write_rows(g, _with(g, "dg2", pubkey="a2"), actor="dg1",
                               declare={"dg2": ("set", config_rows.KEYGEN_KEYS)})


def test_countersign_promotion_by_the_prime_admitted(g):
    config_rows.write_rows(g, _with(g, "kidx", tier=0, promoted_by="prime"), actor="prime",
                           declare={"kidx": ("set", {"tier", "promoted_by"})})
    assert next(r for r in _rows(g) if r["name"] == "kidx")["tier"] == 0


def test_mutant_countersign_promotion_that_also_changes_model_is_refused(g):
    with pytest.raises(config_rows.RowWriteRefused, match="outside"):
        config_rows.write_rows(g, _with(g, "kidx", tier=0, promoted_by="prime", model="z"), actor="prime",
                               declare={"kidx": ("set", {"tier", "promoted_by"})})


def test_mutant_a_post_promoting_itself_is_refused(g):
    with pytest.raises(config_rows.RowWriteRefused):
        config_rows.write_rows(g, _with(g, "dg1", tier=0, promoted_by="dg1"), actor="dg1",
                               declare={"dg1": ("set", {"tier", "promoted_by"})})


def test_spawn_mint_create_by_the_prime_admitted(g):
    rows = [dict(r) for r in _rows(g)] + [{"name": "newkid", "role": "kid", "tier": "untrusted"}]
    config_rows.write_rows(g, rows, actor="prime", declare={"newkid": ("create", None)})
    assert any(r["name"] == "newkid" for r in _rows(g))


def test_mutant_a_post_minting_its_own_row_is_refused(g):
    rows = [dict(r) for r in _rows(g)] + [{"name": "sneaky", "role": "kid"}]
    with pytest.raises(config_rows.RowWriteRefused):
        config_rows.write_rows(g, rows, actor="sneaky", declare={"sneaky": ("create", None)})


# ---- (A) actor_rows: the migrate tick's seating cells ------------------------------------------
def test_seating_cells_by_the_granted_master_admitted(g):
    config_rows.write_rows(g, _with(g, "dg1", box="b", worktree="w/dg1"), actor="master",
                           declare={"dg1": ("set", {"box", "worktree"})})
    assert next(r for r in _rows(g) if r["name"] == "dg1")["box"] == "b"


def test_mutant_seating_cells_by_a_non_master_are_refused(g):
    with pytest.raises(config_rows.RowWriteRefused):
        config_rows.write_rows(g, _with(g, "dg2", box="b"), actor="dg1", declare={"dg2": ("set", {"box"})})


def test_mutant_the_master_writing_a_cell_outside_its_grant_is_refused(g):
    with pytest.raises(config_rows.RowWriteRefused):
        config_rows.write_rows(g, _with(g, "dg1", pubkey="zz"), actor="master", declare={"dg1": ("set", {"pubkey"})})


def test_mutant_the_master_on_a_denied_row_is_refused(g):
    with pytest.raises(config_rows.RowWriteRefused):
        config_rows.write_rows(g, _with(g, "parent", box="b"), actor="master", declare={"parent": ("set", {"box"})})


# ---- identity ------------------------------------------------------------------------------------
def test_mutant_an_unresolved_actor_is_refused(g):
    with pytest.raises(config_rows.RowWriteRefused, match="UNRESOLVED"):
        config_rows.write_rows(g, _with(g, "dg2", pid=5), actor="nobody", declare={"dg2": ("set", {"pid"})})


def test_the_literal_owner_is_role_owner(g):
    config_rows.write_rows(g, _with(g, "dg2", model="o/p"), actor="owner", declare={"dg2": ("set", {"model"})})
    assert next(r for r in _rows(g) if r["name"] == "dg2")["model"] == "o/p"


def test_a_generation_suffixed_actor_resolves_to_its_seat(g):
    config_rows.write_rows(g, _with(g, "dg1", pid=8), actor="dg1-S1-L4-3", declare={"dg1": ("set", {"pid"})})
    assert next(r for r in _rows(g) if r["name"] == "dg1")["pid"] == 8


def test_mutant_a_caller_passed_role_is_not_a_parameter(g):
    with pytest.raises(TypeError):
        config_rows.write_rows(g, _with(g, "dg2", model="x"), actor="dg1", role="prime_director",
                               declare={"dg2": ("set", {"model"})})


# ---- shape ---------------------------------------------------------------------------------------
def test_mutant_posts_not_a_list_of_named_rows_is_refused(g):
    with pytest.raises(config_rows.RowWriteRefused):
        config_rows.write_rows(g, "notalist", actor="prime", declare={})
    with pytest.raises(config_rows.RowWriteRefused):
        config_rows.write_rows(g, [{"role": "kid"}], actor="prime", declare={})


def test_mutant_a_root_with_no_config_node_is_refused(tmp_path):
    (tmp_path / ".agi").mkdir()
    (tmp_path / ".agi" / "config.json").write_text("{}", encoding="utf-8")
    with pytest.raises(config_rows.RowWriteRefused, match="no config:posts / config:seats node"):
        config_rows.write_rows(tmp_path / ".agi", [], actor="prime", declare={})


def test_a_noop_write_changes_nothing(g):
    before = _unchanged(g)
    config_rows.write_rows(g, [dict(r) for r in _rows(g)], actor="dg1", declare={})
    assert [r["name"] for r in _rows(g)] == [r["name"] for r in ROWS]
    assert "dg1" in before


def test_a_graph_with_no_config_schema_gates_nothing_but_the_declared_diff_still_binds(g):
    (g / "context" / "schemas" / "[config].md").unlink()
    config_rows.write_rows(g, _with(g, "dg2", pid=5), actor="nobody", declare={"dg2": ("set", {"pid"})})
    with pytest.raises(config_rows.RowWriteRefused, match="did not declare"):
        config_rows.write_rows(g, _with(g, "dg1", pid=6), actor="nobody", declare={"dg2": ("set", {"pid"})})


def test_mutant_a_schema_that_exists_but_cannot_be_read_refuses(g, monkeypatch):
    import schema_registry

    def boom(*a, **k):
        raise OSError("unreadable")

    monkeypatch.setattr(schema_registry, "load_schemas_from_dir", boom)
    with pytest.raises(config_rows.RowWriteRefused, match="cannot read"):
        config_rows.write_rows(g, _with(g, "dg2", pid=5), actor="prime", declare={"dg2": ("set", {"pid"})})


def test_mutant_a_root_with_no_project_marker_is_refused_and_nothing_is_written(tmp_path):
    root = tmp_path / "bare"
    (root / "nodes" / ".geometry").mkdir(parents=True)
    posts = root / "nodes" / ".geometry" / "posts.md"
    posts.write_text(_rows_md(ROWS), encoding="utf-8")
    before = posts.read_text(encoding="utf-8")
    with pytest.raises(config_rows.RowWriteRefused, match="not an agi project graph root"):
        config_rows.write_rows(root, _with_rows(ROWS, "dg1", pid=9), actor="dg1", declare={"dg1": ("set", {"pid"})})
    assert posts.read_text(encoding="utf-8") == before


def _with_rows(rows, name, **cells):
    return [dict(r, **cells) if r["name"] == name else dict(r) for r in rows]


def test_the_project_root_resolves_down_to_its_dot_agi(g):
    config_rows.write_rows(g.parent, _with(g, "dg1", pid=11), actor="dg1", declare={"dg1": ("set", {"pid"})})
    assert next(r for r in _rows(g) if r["name"] == "dg1")["pid"] == 11


def test_mutant_a_node_writer_rejection_is_a_refusal_not_a_silent_success(g, monkeypatch):
    """The old submit path returned success when node_writer REJECTED the write (the row never
    landed and the caller went on). A rejection now refuses by name."""
    import node_writer

    monkeypatch.setattr(node_writer, "update_node",
                        lambda *a, **k: node_writer.NodeWrite(status=node_writer.REJECTED, node_id="config:posts",
                                                              reason="no node file for config:posts"))
    with pytest.raises(config_rows.RowWriteRefused, match="rejected the write: no node file"):
        config_rows.write_rows(g, _with(g, "dg2", pid=5), actor="prime", declare={"dg2": ("set", {"pid"})})


def test_help_prints_and_exits_zero():
    import subprocess

    r = subprocess.run([sys.executable, str(BIN / "config_rows.py"), "--help"], capture_output=True, text=True)
    assert r.returncode == 0 and "write_rows" in r.stdout


def test_c2_mutant_a_config_file_resolve_finds_but_with_no_id_is_refused_by_name(tmp_path):
    """geometry_config.resolve finds posts.md by FILENAME; node_writer resolves by `id:`. A posts.md
    with no `id: config:posts` is no config node: the write is refused naming node_writer, nothing is
    written (the old path reported success and printed 'wrote identity cells' for a row never written)."""
    root = tmp_path / ".agi"
    (root / "nodes" / ".geometry").mkdir(parents=True)
    (root / "config.json").write_text("{}", encoding="utf-8")
    posts = root / "nodes" / ".geometry" / "posts.md"
    posts.write_text("---\ntype: config\nposts:\n  - {\"name\": \"dg1\", \"role\": \"director\", \"pid\": 1}\n---\n",
                     encoding="utf-8")
    before = posts.read_text(encoding="utf-8")
    with pytest.raises(config_rows.RowWriteRefused, match="carries id none, not config:posts"):
        config_rows.write_rows(root, [{"name": "dg1", "role": "director", "pid": 2}], actor="dg1",
                               declare={"dg1": ("set", {"pid"})})
    assert posts.read_text(encoding="utf-8") == before


def _seats_graph(tmp_path, head):
    root = tmp_path / ".agi"
    (root / "nodes" / ".geometry").mkdir(parents=True)
    (root / "config.json").write_text("{}", encoding="utf-8")
    f = root / "nodes" / ".geometry" / "seats.md"
    f.write_text(head + 'type: config\nseats:\n  - {"name": "dg1", "role": "director", "pid": 1}\n---\n',
                 encoding="utf-8")
    return root, f


def test_c1_seats_md_with_id_config_seats_is_written_and_read_back(tmp_path):
    root, f = _seats_graph(tmp_path, "---\nid: config:seats\n")
    config_rows.write_rows(root, [{"name": "dg1", "role": "director", "pid": 5}], actor="dg1",
                           declare={"dg1": ("set", {"pid"})})
    assert geometry_config.load_rows(root)[0]["pid"] == 5          # read back, not rc alone


def test_c3_mutant_a_file_whose_id_is_foreign_is_refused_by_name(tmp_path):
    root, f = _seats_graph(tmp_path, "---\nid: config:rotations\n")
    before = f.read_text(encoding="utf-8")
    with pytest.raises(config_rows.RowWriteRefused, match="carries id config:rotations, not config:posts"):
        config_rows.write_rows(root, [{"name": "dg1", "role": "director", "pid": 5}], actor="dg1",
                               declare={"dg1": ("set", {"pid"})})
    assert f.read_text(encoding="utf-8") == before


def test_c4_mutant_neither_posts_nor_seats_is_refused(tmp_path):
    root = tmp_path / ".agi"
    (root / "nodes" / ".geometry").mkdir(parents=True)
    (root / "config.json").write_text("{}", encoding="utf-8")
    with pytest.raises(config_rows.RowWriteRefused, match="no config:posts / config:seats node"):
        config_rows.write_rows(root, [{"name": "dg1"}], actor="dg1", declare={})
