"""T-008 tests: directory-level error isolation (graph-core/R4.4)."""

from pathlib import Path

from graph_core.persistence import load_node_dir, FrontmatterError


def test_dir_load_isolates_bad_file(tmp_path: Path) -> None:
    """One valid + one malformed → 1 node + 1 error, both reported."""
    good = tmp_path / "good.md"
    good.write_text("---\nid: hyp:ok\ntype: hypothesis\n---\n\nbody\n")
    bad = tmp_path / "bad.md"
    bad.write_text("---\nid: hyp:bad\n")  # missing closing ---
    result = load_node_dir(tmp_path)
    assert len(result.nodes) == 1
    assert result.nodes[0].frontmatter["id"] == "hyp:ok"
    assert len(result.errors) == 1
    assert result.errors[0].path == bad
    assert "closing" in result.errors[0].reason.lower() or "---" in result.errors[0].reason


def test_dir_load_skips_non_node_files(tmp_path: Path) -> None:
    """Files that aren't .md/.json are silently ignored."""
    (tmp_path / "node.md").write_text("---\nid: a\n---\nb\n")
    (tmp_path / "README.txt").write_text("not a node")
    (tmp_path / "data.csv").write_text("a,b\n1,2\n")
    result = load_node_dir(tmp_path)
    assert len(result.nodes) == 1
    assert len(result.errors) == 0


def test_dir_load_mixed_md_and_json(tmp_path: Path) -> None:
    """Both .md and .json node files are picked up."""
    (tmp_path / "a.md").write_text("---\nid: a\n---\nbody-a\n")
    (tmp_path / "b.json").write_text('{"frontmatter": {"id": "b"}, "body": "body-b"}\n')
    result = load_node_dir(tmp_path)
    assert len(result.nodes) == 2
    assert len(result.errors) == 0


def test_dir_load_not_a_directory(tmp_path: Path) -> None:
    """Pointing at a file rather than a dir raises FrontmatterError."""
    f = tmp_path / "x.md"
    f.write_text("---\nid: x\n---\n")
    import pytest

    with pytest.raises(FrontmatterError):
        load_node_dir(f)


def test_dir_load_continues_after_multiple_errors(tmp_path: Path) -> None:
    """Multiple bad files → multiple LoadErrors, all good files load."""
    (tmp_path / "good1.md").write_text("---\nid: a\n---\n")
    (tmp_path / "good2.md").write_text("---\nid: b\n---\n")
    (tmp_path / "bad1.md").write_text("no frontmatter at all")
    (tmp_path / "bad2.json").write_text("{not json")
    result = load_node_dir(tmp_path)
    assert len(result.nodes) == 2
    assert len(result.errors) == 2
    assert {e.path.name for e in result.errors} == {"bad1.md", "bad2.json"}


# ---------------------------------------------------------------------------
# goal:g13 — one failure class, both entry points.
#
# `FrontmatterError` is documented as "Raised when a node file cannot be
# parsed". Before this, malformed YAML escaped as `yaml.parser.ParserError`
# and malformed JSON as `json.JSONDecodeError`, so the single `except
# FrontmatterError` this module's contract offers did not hold. Measured
# 2026-09-02 across six independent parsers in this tree: four different
# failure semantics, and this was the only one that contradicted its OWN
# documented contract rather than merely differing from its neighbours.
# ---------------------------------------------------------------------------

import json as _json          # noqa: E402
import pytest as _pytest      # noqa: E402
import yaml as _yaml          # noqa: E402

from graph_core.persistence.frontmatter import (  # noqa: E402
    FrontmatterError,
    load_node_file,
)


@_pytest.mark.parametrize("bad_yaml", [
    "---\nid: [unclosed\n---\nbody\n",
    "---\nid: 'unterminated\n---\nbody\n",
    "---\na: b\n c: d\n---\nbody\n",
])
def test_malformed_yaml_raises_frontmatter_error_not_a_yaml_error(tmp_path, bad_yaml):
    p = tmp_path / "n.md"
    p.write_text(bad_yaml)
    with _pytest.raises(FrontmatterError):
        load_node_file(p)


def test_malformed_json_raises_frontmatter_error_not_a_decode_error(tmp_path):
    p = tmp_path / "n.json"
    p.write_text("{not json")
    with _pytest.raises(FrontmatterError):
        load_node_file(p)


def test_the_underlying_cause_is_preserved_for_debugging(tmp_path):
    """One class to catch, but the original error is still reachable via
    `__cause__` -- collapsing the taxonomy must not destroy the diagnosis."""
    p = tmp_path / "n.md"
    p.write_text("---\nid: [unclosed\n---\nbody\n")
    with _pytest.raises(FrontmatterError) as ei:
        load_node_file(p)
    assert isinstance(ei.value.__cause__, _yaml.YAMLError)

    j = tmp_path / "n.json"
    j.write_text("{not json")
    with _pytest.raises(FrontmatterError) as ej:
        load_node_file(j)
    assert isinstance(ej.value.__cause__, _json.JSONDecodeError)


def test_every_malformed_shape_fails_in_exactly_one_class(tmp_path):
    """The contract, stated as a single assertion: nothing a caller can put in
    this file escapes `except FrontmatterError`."""
    shapes = {
        "no frontmatter":   ("n1.md", "just a body\n"),
        "unterminated":     ("n2.md", "---\nid: x\nno close\n"),
        "malformed YAML":   ("n3.md", "---\nid: [unclosed\n---\nb\n"),
        "list not mapping": ("n4.md", "---\n- a\n- b\n---\nb\n"),
        "empty":            ("n5.md", ""),
        "bad json":         ("n6.json", "{nope"),
        "json not object":  ("n7.json", "[1,2]"),
    }
    for label, (name, text) in shapes.items():
        p = tmp_path / name
        p.write_text(text)
        try:
            load_node_file(p)
        except FrontmatterError:
            pass
        except Exception as e:                      # noqa: BLE001
            raise AssertionError(
                f"{label}: leaked {type(e).__module__}.{type(e).__name__} "
                f"past FrontmatterError"
            ) from e
