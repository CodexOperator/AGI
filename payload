"""T-022 tests: schemas as meta_nodes (schema-registry/R3)."""

from pathlib import Path

from schema_registry import (
    META_TYPE,
    diff_meta_nodes,
    load_schemas_from_dir,
    synthesize_meta_nodes,
)


def _seed(d: Path, names: list[str], active: list[str] | None = None) -> None:
    active = active or []
    for n in names:
        fname = f"[{n}].md" if n in active else f"{n}.md"
        (d / fname).write_text(
            f"---\nname: {n}\nfields:\n  title:\n    type: string\n---\n"
        )


def test_one_meta_node_per_schema(tmp_path: Path) -> None:
    """R3.1: one meta_node per registered schema."""
    _seed(tmp_path, ["idea", "hypothesis", "experiment"])
    reg = load_schemas_from_dir(tmp_path)
    meta = synthesize_meta_nodes(reg)
    assert set(meta.keys()) == {"idea", "hypothesis", "experiment"}
    assert all(n.type == META_TYPE for n in meta.values())


def test_meta_node_id_derived_from_schema_name(tmp_path: Path) -> None:
    """R3.1: id derived from schema name."""
    _seed(tmp_path, ["hypothesis"])
    reg = load_schemas_from_dir(tmp_path)
    meta = synthesize_meta_nodes(reg)
    n = meta["hypothesis"]
    assert "hypothesis" in n.id
    assert n.id.startswith("schema:")


def test_meta_node_payload_ref_points_to_schema_file(tmp_path: Path) -> None:
    _seed(tmp_path, ["idea"])
    reg = load_schemas_from_dir(tmp_path)
    meta = synthesize_meta_nodes(reg)
    n = meta["idea"]
    assert n.payload_ref is not None
    assert "idea" in n.payload_ref


def test_active_tag_on_bracketed(tmp_path: Path) -> None:
    """R3.2: active flag exposed in tags."""
    _seed(tmp_path, ["idea", "hypothesis"], active=["hypothesis"])
    reg = load_schemas_from_dir(tmp_path)
    meta = synthesize_meta_nodes(reg)
    assert "active" in meta["hypothesis"].tags
    assert "active" not in meta["idea"].tags


def test_diff_added_removed(tmp_path: Path) -> None:
    """R3.4: removing schema -> meta_node removed in next load."""
    _seed(tmp_path, ["idea", "hypothesis"])
    reg1 = load_schemas_from_dir(tmp_path)
    meta1 = synthesize_meta_nodes(reg1)
    (tmp_path / "hypothesis.md").unlink()
    (tmp_path / "experiment.md").write_text(
        "---\nname: experiment\n---\n"
    )
    reg2 = load_schemas_from_dir(tmp_path)
    meta2 = synthesize_meta_nodes(reg2)
    added, removed = diff_meta_nodes(meta1, meta2)
    assert added == {"experiment"}
    assert removed == {"hypothesis"}
