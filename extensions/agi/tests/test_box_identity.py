"""A live row carries its OWN box; an unset or unknown box is REFUSED.

hypothesis:every-live-row-carries-its-own-box-and-an-unset-box-is-refused
(belam 00:35Z 09-27). Two claims, each with its falsifiers:

  (1) seating stamps the live row's `box` cell from AGI_BOX -- through the ONE
      seat-row writer (`rotate._write_identity_cells`) under the schema's
      SEATING actor, because `box` is the master's cell, never a post's own.
  (2) `boxes.this_box` REFUSES an unset AGI_BOX (no `default_box` fallback)
      and `boxes.row_is_local` never calls an EMPTY or UNKNOWN row box local,
      on any box -- `'(default)'` is never a match.

Temp graphs + monkeypatched env only; never the live .env, never a live pane.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parent.parent / "bin"
sys.path.insert(0, str(BIN))

import boxes  # noqa: E402
import rotate  # noqa: E402
import write  # noqa: E402

# The LIVE schema bytes, so the grant under test is the real one, not a copy.
LIVE_SCHEMA = (Path(__file__).resolve().parents[3] / ".agi" /
               "context" / "schemas" / "[config].md")

ROWS = [
    {"name": "sanctuary-master", "role": "prime_director", "model": "m",
     "session_ref": "", "generation": 0, "window": ""},
    {"name": "director-belam", "role": "director", "model": "m",
     "session_ref": "", "generation": 3, "window": "@1"},
]


def _graph(tmp_path: Path, *, env_box: str | None = "local-town",
           default_box: str | None = "core-town") -> Path:
    """A temp project root (.agi) with the schema, a posts list and an env."""
    agi = tmp_path / ".agi"
    (agi / "nodes" / ".geometry").mkdir(parents=True, exist_ok=True)
    (agi / "context" / "schemas").mkdir(parents=True, exist_ok=True)
    (agi / "config.json").write_text("{}")
    assert LIVE_SCHEMA.is_file()
    (agi / "context" / "schemas" / "[config].md").write_text(
        LIVE_SCHEMA.read_text(encoding="utf-8"))
    head = ("---\nid: config:posts\nmint_id: 3e88873e3c204c5088f6ab81322a26de\n"
            "type: config\nparents:\n  - goal:g17\n")
    if default_box is not None:
        head += f"default_box: {default_box}\n"
    body = "\n".join("  - " + json.dumps(r) for r in ROWS)
    (agi / "nodes" / ".geometry" / "posts.md").write_text(
        head + "posts:\n" + body + "\n---\n\n# config:posts\n\nfixture\n")
    if env_box is not None:
        (tmp_path / ".env").write_text(f"AGI_BOX={env_box}\n")
    return agi


@pytest.fixture(autouse=True)
def _no_inherited_box(monkeypatch):
    monkeypatch.delenv("AGI_BOX", raising=False)


# --------------------------------------------------------------- claim (2)

def test_this_box_reads_the_env_file(tmp_path, monkeypatch):
    assert boxes.this_box(_graph(tmp_path)) == "local-town"


def test_this_box_env_beats_the_env_file(tmp_path, monkeypatch):
    monkeypatch.setenv("AGI_BOX", "sanctuary")
    assert boxes.this_box(_graph(tmp_path)) == "sanctuary"


def test_falsifier_unset_agi_box_refuses_instead_of_defaulting(tmp_path):
    """FALSIFIER 1: an unset AGI_BOX (env AND env file) must REFUSE.

    Pre-fix this returned the posts node's `default_box` ('core-town'), which
    is what made every boxless row read as foreign on a non-core box.
    """
    root = _graph(tmp_path, env_box=None)
    with pytest.raises(RuntimeError) as ei:
        boxes.this_box(root)
    assert "AGI_BOX" in str(ei.value)
    assert "default_box" in str(ei.value)  # named as documentation, not a fallback


def test_default_box_still_reads_as_documentation(tmp_path):
    assert boxes.default_box(_graph(tmp_path)) == "core-town"


def test_row_with_its_own_box_is_local(tmp_path):
    root = _graph(tmp_path)
    assert boxes.row_is_local(root, {"name": "x", "box": "local-town"})
    assert not boxes.row_is_local(root, {"name": "x", "box": "sanctuary"})


def test_falsifier_empty_row_box_is_never_local(tmp_path):
    """FALSIFIER 2: `box: ''` is not local, even where default_box == here."""
    root = _graph(tmp_path, default_box="local-town")
    assert not boxes.row_is_local(root, {"name": "x"})
    assert not boxes.row_is_local(root, {"name": "x", "box": ""})
    assert not boxes.row_is_local(root, {"name": "x", "box": "   "})


def test_falsifier_default_string_is_never_a_match(tmp_path):
    """FALSIFIER 3: a row literally labelled '(default)' matches nothing."""
    root = _graph(tmp_path)
    assert not boxes.row_is_local(root, {"name": "x", "box": "(default)"})


def test_falsifier_unknown_row_box_is_not_local_on_any_box(tmp_path, monkeypatch):
    for label in ("local-town", "core-town", "sanctuary", "streaming-suite"):
        monkeypatch.setenv("AGI_BOX", label)
        root = _graph(tmp_path, env_box=None)
        assert not boxes.row_is_local(root, {"name": "x", "box": "nonesuch"})


def test_graph_that_declares_no_box_is_the_one_retained_fail_open(tmp_path):
    """No AGI_BOX anywhere: a SINGLE-BOX dev graph keeps working (unchanged),
    but a row that names a box is still foreign -- nothing confirms it."""
    root = _graph(tmp_path, env_box=None)
    assert boxes.row_is_local(root, {"name": "x"})
    assert not boxes.row_is_local(root, {"name": "x", "box": "sanctuary"})
    assert not boxes.row_is_local(root, {"name": "x", "box": "local-town"})


# --------------------------------------------------------------- claim (1)

def test_seating_stamps_the_live_row_box(tmp_path, monkeypatch):
    """A fresh seat on a temp graph lands its OWN `box` cell from AGI_BOX."""
    monkeypatch.setenv("AGI_BOX", "local-town")
    root = _graph(tmp_path)
    out = rotate._stamp_row_box(root, seat="director-belam",
                                row={"name": "director-belam"})
    assert "box=local-town" in out
    rows = write._load_seats(root)
    stamped = next(r for r in rows if r["name"] == "director-belam")
    assert stamped["box"] == "local-town"


def test_seating_never_rewrites_a_row_that_names_its_box(tmp_path, monkeypatch):
    """A row already carrying its own box is left exactly as it is."""
    monkeypatch.setenv("AGI_BOX", "local-town")
    root = _graph(tmp_path)
    before = write._load_seats(root)
    assert rotate._stamp_row_box(root, seat="director-belam",
                                 row={"name": "director-belam",
                                      "box": "sanctuary"}) == ""
    assert write._load_seats(root) == before  # untouched, never relabelled


def test_seating_writes_no_box_when_the_graph_names_none(tmp_path):
    root = _graph(tmp_path, env_box=None)
    out = rotate._stamp_row_box(root, seat="director-belam",
                                row={"name": "director-belam"})
    assert "undeclared" in out
    assert all("box" not in r for r in write._load_seats(root))
