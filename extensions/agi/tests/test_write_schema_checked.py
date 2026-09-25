"""goal:g7.33.10 round B — `write.py`'s `set` and `create --set` consult the
target's schema before writing a row (hypothesis:write-py-set-is-schema-
checked). Until this landed, `write.py <id> 'set <field> <value>'` admitted
an invented field name, a value failing the schema's regex, a value failing
its declared type, and a raw string into a list-typed field — all exit 0,
never coerced, never refused. Measured directly against goal:g7.33.9 (the
five probes this file pins four of) and independently reproduced twice more
the same session on `create --set` (goal:g7.33.12's `tags` landing as a raw
comma string).

The fifth probe from goal:g7.33.10's own "measured" row — a title with no
id-prefix format — is NOT pinned here: `[goal].md` declares no `title`
regex, and adding one is a schema-file change outside this hypothesis's
FILE SCOPE (`write.py` + `links.py` only). Left open for a follow-up round.
"""
from __future__ import annotations

import io
import sys
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parent.parent / "bin"
sys.path.insert(0, str(BIN))

import write  # noqa: E402


# A trimmed transcription of the real `.agi/context/schemas/[goal].md`
# frontmatter — the same fields/validation shape, none of the prose, so this
# test is grounded in the real rules without coupling to the doc's wording.
GOAL_SCHEMA = """---
name: goal
fields:
  title: {type: str}
  goal_id: {type: str}
  goal_kind: {type: str}
  status: {type: str}
  origin: {type: str}
  seeds: {type: list}
  parents: {type: list}
  confidence: {type: float}
  tags: {type: list}
validation:
  required: [id, type, mint_id, title, goal_id, goal_kind, status, origin, seeds, confidence, tags]
  types:
    seeds: list
    tags: list
    confidence: float
  regex:
    goal_id: '^[GS]\\d+(\\.\\d+)*$'
    goal_kind: '^(long-term|perpetual|short-term|subgoal)$'
    status: '^(active|horizon|retired|phasing-out|complete)$'
---

# goal
body
"""

GOAL_NODE = """---
id: "goal:g1"
type: goal
mint_id: "g1mint"
title: "G1: Sample goal"
goal_id: "G1"
goal_kind: perpetual
status: active
origin: goals-doc
seeds: []
parents: []
confidence: 0.9
tags: [sample]
---

# goal:g1

body
"""


@pytest.fixture()
def project(tmp_path: Path) -> Path:
    graph = tmp_path / ".agi"
    (graph / "nodes" / "goal").mkdir(parents=True)
    (graph / "context" / "schemas").mkdir(parents=True)
    (graph / "config.json").write_text("{}")
    (graph / "context" / "schemas" / "[goal].md").write_text(GOAL_SCHEMA)
    (graph / "nodes" / "goal" / "g1.md").write_text(GOAL_NODE)
    return graph


def _run(argv):
    """Run write.main, capturing stdout/stderr, returning (out, err, rc) —
    the exact helper test_write.py already uses for CLI-level assertions."""
    out, err = io.StringIO(), io.StringIO()
    with redirect_stdout(out), redirect_stderr(err):
        rc = write.main(argv)
    return out.getvalue(), err.getvalue(), rc


def _set(project, script):
    return _run(["goal:g1", script, "--root", str(project), "--actor", "test"])


# --------------------------------------------------------------------------
# The five probes from goal:g7.33.10's own "measured" row (four of five —
# see module docstring for the fifth)
# --------------------------------------------------------------------------

def test_an_invented_field_is_refused_by_name(project):
    before = (project / "nodes" / "goal" / "g1.md").read_text()
    out, err, rc = _set(project, "set invented_row somevalue")
    assert rc == 2, (out, err)
    assert "invented_row" in err
    assert "not a field" in err
    assert (project / "nodes" / "goal" / "g1.md").read_text() == before


def test_goal_id_out_of_regex_is_refused_by_name(project):
    before = (project / "nodes" / "goal" / "g1.md").read_text()
    out, err, rc = _set(project, "set goal_id X9")
    assert rc == 2, (out, err)
    assert "goal_id" in err and "X9" in err
    assert (project / "nodes" / "goal" / "g1.md").read_text() == before


def test_status_out_of_regex_is_refused_by_name(project):
    before = (project / "nodes" / "goal" / "g1.md").read_text()
    out, err, rc = _set(project, "set status bogus")
    assert rc == 2, (out, err)
    assert "status" in err and "bogus" in err
    assert (project / "nodes" / "goal" / "g1.md").read_text() == before


def test_confidence_failing_its_declared_type_is_refused_by_name(project):
    before = (project / "nodes" / "goal" / "g1.md").read_text()
    out, err, rc = _set(project, "set confidence notafloat")
    assert rc == 2, (out, err)
    assert "confidence" in err and "float" in err
    assert (project / "nodes" / "goal" / "g1.md").read_text() == before


# --------------------------------------------------------------------------
# This session's own repro: a raw scalar into a list-typed field
# --------------------------------------------------------------------------

def test_a_raw_scalar_into_a_list_typed_field_is_refused(project):
    """goal:g7.33.12's own bug, reproduced independently here: `tags` given
    as a bare comma string (no brackets) coerces to a plain string, not a
    list — `[goal].md` declares `tags: list`, so this must refuse, not land
    a string where every reader expects a list."""
    before = (project / "nodes" / "goal" / "g1.md").read_text()
    out, err, rc = _set(project, "set tags local-maxxing,engine,research-review")
    assert rc == 2, (out, err)
    assert "tags" in err and "list" in err
    assert (project / "nodes" / "goal" / "g1.md").read_text() == before


def test_create_set_refuses_the_same_raw_scalar_into_a_list_field(project):
    """The `create --set` sibling path shares the same predicate — the exact
    class of bug that landed `hypothesis:parent-orders-line-names-a-real-
    path-not-prose`'s sibling defect on goal:g7.33.12 at create time."""
    out, err, rc = _run(["create", "goal", "g2",
                         "--set", "tags=a,b,c",
                         "--set", "goal_id=G2",
                         "--set", "goal_kind=perpetual",
                         "--set", "status=active",
                         "--root", str(project)])
    assert rc == 2, (out, err)
    assert "tags" in err and "list" in err
    assert not (project / "nodes" / "goal" / "g2.md").exists()


# --------------------------------------------------------------------------
# A schema-valid row still writes, byte-for-byte the same shape as before
# this round — no regression on the happy path.
# --------------------------------------------------------------------------

def test_a_valid_scalar_set_still_succeeds(project):
    out, err, rc = _set(project, "set confidence 0.42")
    assert rc == 0, (out, err)
    text = (project / "nodes" / "goal" / "g1.md").read_text()
    assert "confidence: 0.42" in text


def test_a_valid_list_set_still_succeeds(project):
    out, err, rc = _set(project, "set tags [sample, other]")
    assert rc == 0, (out, err)
    text = (project / "nodes" / "goal" / "g1.md").read_text()
    assert "sample" in text and "other" in text


def test_a_valid_goal_retitle_is_one_verb(project):
    """goal:g7.33.10's own "done" bar: a valid goal re-title is ONE verb."""
    out, err, rc = _set(project, 'set title "G1: Renamed sample goal"')
    assert rc == 0, (out, err)
    text = (project / "nodes" / "goal" / "g1.md").read_text()
    assert "Renamed sample goal" in text


def test_an_undeclared_key_on_a_schema_less_type_gates_nothing(project):
    """A node type with no active schema file (or none matching) gates
    nothing — falls through to today's behaviour, exactly like the create
    gate already did before this round."""
    (project / "nodes" / "doc").mkdir(parents=True)
    (project / "nodes" / "doc" / "d1.md").write_text(
        '---\nid: "doc:d1"\ntype: doc\nmint_id: "d1mint"\ntitle: "D"\n---\n\nbody\n')
    out, err, rc = _run(["doc:d1", "set anything_at_all 1",
                         "--root", str(project), "--actor", "test"])
    assert rc == 0, (out, err)
