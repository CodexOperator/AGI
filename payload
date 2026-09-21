"""T-006 tests: frontmatter persistence (graph-core/R4)."""

from pathlib import Path

import pytest

from graph_core.persistence import load_node_file, save_node_file, FrontmatterError
from graph_core.persistence.frontmatter import NodeFile


FIXTURE_DIR = Path(__file__).parent.parent / "fixtures" / "nodes"


def test_md_round_trip_normalized(tmp_path: Path) -> None:
    """R4.2: load → save → load is identical (post normalization)."""
    src = FIXTURE_DIR / "sample.md"
    nf = load_node_file(src)
    out = tmp_path / "sample.md"
    save_node_file(out, nf)
    nf2 = load_node_file(out)
    assert nf.frontmatter == nf2.frontmatter
    assert nf.body == nf2.body


def test_md_round_trip_byte_equivalent_after_normalization(tmp_path: Path) -> None:
    """R4.2: writing normalizes; second write of same content matches first byte-for-byte."""
    src = FIXTURE_DIR / "sample.md"
    nf = load_node_file(src)
    a = tmp_path / "a.md"
    b = tmp_path / "b.md"
    save_node_file(a, nf)
    nf2 = load_node_file(a)
    save_node_file(b, nf2)
    assert a.read_bytes() == b.read_bytes()


def test_json_round_trip(tmp_path: Path) -> None:
    """R4.3: pure JSON node files round-trip."""
    src = FIXTURE_DIR / "sample.json"
    nf = load_node_file(src)
    out = tmp_path / "sample.json"
    save_node_file(out, nf)
    nf2 = load_node_file(out)
    assert nf.frontmatter == nf2.frontmatter
    assert nf.body == nf2.body


def test_md_lazy_body_skipped() -> None:
    """body=False yields empty body even when file has content."""
    src = FIXTURE_DIR / "sample.md"
    nf = load_node_file(src, body=False)
    assert nf.body == ""
    assert nf.frontmatter["id"] == "hyp:lru-saturates-warm-load"


def test_unknown_suffix_rejected(tmp_path: Path) -> None:
    """Unsupported file extensions raise FrontmatterError."""
    p = tmp_path / "node.txt"
    p.write_text("---\nid: x\n---\n")
    with pytest.raises(FrontmatterError):
        load_node_file(p)


def test_md_missing_closing_delim(tmp_path: Path) -> None:
    """Malformed md (missing closing '---') raises FrontmatterError."""
    p = tmp_path / "bad.md"
    p.write_text("---\nid: x\n")
    with pytest.raises(FrontmatterError):
        load_node_file(p)


def test_json_object_required(tmp_path: Path) -> None:
    """JSON node must be an object."""
    p = tmp_path / "bad.json"
    p.write_text("[]")
    with pytest.raises(FrontmatterError):
        load_node_file(p)
