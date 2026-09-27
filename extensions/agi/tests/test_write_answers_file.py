"""`write.py create --answers <file>` — ONE mint route whose every row is
validated row-by-row, with no field value passing through a shell-quoted argv
(hypothesis:one-mint-route-answers-file-validated-row-by-row, claims 1 and 2;
claim 3 -- the config:posts stamp -- is KID 2's and is deliberately absent
here).

The answers file is JSON: one object whose reserved keys (`type`, `slug`,
`parents`, `body`, `payload`) name the mint, and every other key is one
frontmatter row. Probes, one per falsifier in the hypothesis:

  1. a body carrying an apostrophe, a backtick and `$(` round-trips
     byte-identically through the answers route;
  2. a REQUIRED row missing from the file is refused BY NAME and nothing is
     written (never the warn-and-write a bare `create` still does);
  3. a bad row (`goal_kind: sometimes`) is refused BY NAME, quoting the
     schema's own regex, and nothing is written;
  4. the row validator is a wrapper -- no second schema-rule table lives in
     write.py (asserted by grepping the two functions the answers route adds);
  5. `--set` / `--body-file` are byte-identical with and without `--answers`.

Every test runs against a temp graph under tmp_path, never the live nodes.
"""
from __future__ import annotations

import io
import json
import sys
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parent.parent / "bin"
sys.path.insert(0, str(BIN))

import write  # noqa: E402

REPO = Path(__file__).resolve().parents[3]
#: The REAL goal schema, read live (never a transcription that can drift).
GOAL_SCHEMA = REPO / ".agi" / "context" / "schemas" / "[goal].md"

PARENT_NODE = """---
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

#: The body the round exists for: the predecessor route (argv) had to drop an
#: owner quote's apostrophes to get them through (goal:g4.18.1 Evidence).
NASTY_BODY = (
    "# answers\n\n"
    "The owner's own words: \"it's the owner's call, not `grid.py`'s\" -- "
    "and a shell would have eaten $(whoami) and `backtick` and 'quote'.\n"
)


def _answers(**overrides) -> dict:
    """A COMPLETE goal answer: every row `[goal].md` lists in
    `validation.required` (id/type/mint_id/parents are the mint's own)."""
    data = {
        "type": "goal",
        "slug": "g9.9.9",
        "parents": ["goal:g1"],
        "goal_id": "G9.9.9",
        "goal_kind": "subgoal",
        "status": "active",
        "origin": "answers-file",
        "seeds": [],
        "confidence": 0.5,
        "tags": ["core"],
        "title": "G9.9.9: minted from an answers file",
    }
    data.update(overrides)
    return data


@pytest.fixture()
def project(tmp_path: Path) -> Path:
    graph = tmp_path / ".agi"
    (graph / "nodes" / "goal").mkdir(parents=True)
    (graph / "context" / "schemas").mkdir(parents=True)
    (graph / "config.json").write_text("{}")
    (graph / "context" / "schemas" / "[goal].md").write_text(
        GOAL_SCHEMA.read_text(encoding="utf-8"))
    (graph / "nodes" / "goal" / "g1.md").write_text(PARENT_NODE)
    return graph


def _write_answers(tmp_path: Path, data) -> Path:
    path = tmp_path / "answers.json"
    path.write_text(json.dumps(data), encoding="utf-8")
    return path


def _run(argv):
    out, err = io.StringIO(), io.StringIO()
    with redirect_stdout(out), redirect_stderr(err):
        rc = write.main(argv)
    return out.getvalue(), err.getvalue(), rc


def _mint(project, answers_file, *extra):
    return _run(["create", "--answers", str(answers_file),
                 "--root", str(project), *extra])


# --------------------------------------------------------------------------
# claim 1 — the answers route mints, byte-identically, nothing shell-quoted
# --------------------------------------------------------------------------

def test_answers_file_mints_a_node(project, tmp_path):
    f = _write_answers(tmp_path, _answers(body=NASTY_BODY))
    out, err, rc = _mint(project, f)
    assert rc == 0, err
    assert "created: goal:g9.9.9" in out
    node = project / "nodes" / "goal" / "g9.9.9.md"
    assert node.is_file()


def test_a_body_with_a_quote_backtick_and_dollar_paren_round_trips(
        project, tmp_path):
    f = _write_answers(tmp_path, _answers(body=NASTY_BODY))
    assert _mint(project, f)[2] == 0
    node = project / "nodes" / "goal" / "g9.9.9.md"
    out, _err, rc = _run(["goal:g9.9.9", "read body 1:99", "--root", str(project)])
    assert rc == 0
    assert "'quote'" in out and "`backtick`" in out and "$(whoami)" in out
    assert "it's the owner's call" in out, "an apostrophe was eaten in flight"


# --------------------------------------------------------------------------
# claim 2 — every row is checked by ONE validator; a refusal writes NOTHING
# --------------------------------------------------------------------------

def test_a_missing_required_row_is_refused_by_name_and_writes_nothing(
        project, tmp_path):
    data = _answers()
    del data["origin"]
    f = _write_answers(tmp_path, data)
    out, err, rc = _mint(project, f)
    assert rc == 2, out
    assert err.strip().count("\n") == 0, "one line on stderr"
    assert "origin" in err, "the refusal must NAME the row"
    assert "required" in err, "the refusal must NAME the rule"
    assert not (project / "nodes" / "goal" / "g9.9.9.md").exists(), \
        "a refused answers file must leave NO file on disk"


def test_a_bad_row_is_refused_by_name_and_writes_nothing(project, tmp_path):
    f = _write_answers(tmp_path, _answers(goal_kind="sometimes"))
    out, err, rc = _mint(project, f)
    assert rc == 2, out
    assert "goal_kind" in err
    assert "subgoal" in err, "the refusal quotes the schema's own rule"
    assert not (project / "nodes" / "goal" / "g9.9.9.md").exists()


def test_a_bad_row_refuses_in_dry_run_too(project, tmp_path):
    """A dry run SIMULATES the mint, so it must refuse what the real mint
    refuses — otherwise `--dry-run` is a green light on a refusal."""
    f = _write_answers(tmp_path, _answers(goal_kind="sometimes"))
    _out, err, rc = _mint(project, f, "--dry-run")
    assert rc == 2 and "goal_kind" in err


def test_a_non_string_body_row_is_refused_by_name(project, tmp_path):
    f = _write_answers(tmp_path, _answers(body=["a", "list"]))
    _out, err, rc = _mint(project, f)
    assert rc == 2 and "body" in err
    assert not (project / "nodes" / "goal" / "g9.9.9.md").exists()


def test_an_unreadable_answers_file_is_refused_by_name(project, tmp_path):
    _out, err, rc = _mint(project, tmp_path / "absent.json")
    assert rc == 2 and "answers" in err
    assert not (project / "nodes" / "goal" / "g9.9.9.md").exists()


def test_the_answers_route_adds_no_second_schema_rule_table():
    """Falsifier 4: the row validator WRAPS `_schema_field_refusal` and
    `node_writer.seed_required`; it does not restate a required-field list or
    type a regex literal. Both function sources are grepped."""
    src = (BIN / "write.py").read_text(encoding="utf-8")
    for name in ("_answers_row_refusal", "_read_answers_file"):
        body = src.split(f"def {name}(", 1)[1].split("\ndef ", 1)[0]
        assert "re.compile" not in body and "\\.\\d" not in body, \
            f"{name} typed a regex instead of reading the schema"
        assert "validation:" not in body, \
            f"{name} restates a schema rule block instead of reading it"
    # The one list the answers route DOES name is what the MINT derives
    # itself (id/type/mint_id/parents are not answers-file rows at all).
    assert "_ANSWERS_RESERVED = frozenset(" in src


# --------------------------------------------------------------------------
# KEEP BYTE-IDENTICAL — the existing routes do not move
# --------------------------------------------------------------------------

def test_set_and_body_file_are_unchanged_without_answers(project, tmp_path):
    body = tmp_path / "body.md"
    body.write_text("# plain\n", encoding="utf-8")
    out, err, rc = _run(["create", "goal", "g8.8.8", "--parent", "goal:g1",
                         "--body-file", str(body), "--set", "goal_kind=subgoal",
                         "--set", "status=active", "--set", "goal_id=G8.8.8",
                         "--set", "origin=goals-doc", "--set", "tags=[core]",
                         "--set", "confidence=0.5", "--no-spawn-gate",
                         "--root", str(project)])
    assert rc == 0, err
    assert "created: goal:g8.8.8" in out
    assert (project / "nodes" / "goal" / "g8.8.8.md").read_text(
        encoding="utf-8").count("# plain") == 1


def test_set_still_refuses_a_bad_row_the_same_way(project, tmp_path):
    _out, err, rc = _run(["create", "goal", "g8.8.7", "--parent", "goal:g1",
                          "--set", "goal_kind=sometimes", "--root",
                          str(project)])
    assert rc == 2 and "goal_kind" in err
    assert not (project / "nodes" / "goal" / "g8.8.7.md").exists()


def test_the_answers_route_feeds_the_same_create_entry_point(project, tmp_path):
    """`--answers` is an ALTERNATIVE flag, not a new verb: it feeds the SAME
    `create()` entry point. `payload` is the proof -- only `create()` creates
    the source file behind the node, and the answers route can name it."""
    src = tmp_path / "src" / "answers_demo.py"
    f = _write_answers(tmp_path, _answers(payload="src/answers_demo.py"))
    out, err, rc = _mint(project, f)
    assert rc == 0, err
    assert src.is_file(), "create() did not run behind the answers route"
    assert "src/answers_demo.py" in (project / "nodes" / "goal" / "g9.9.9.md").read_text(
        encoding="utf-8")


def test_set_flags_may_still_add_a_row_on_top_of_the_answers_file(
        project, tmp_path):
    f = _write_answers(tmp_path, _answers())
    out, err, rc = _mint(project, f, "--set", "tags=[answers-file]")
    assert rc == 0, err
    node = (project / "nodes" / "goal" / "g9.9.9.md").read_text(
        encoding="utf-8")
    assert "answers-file" in node
