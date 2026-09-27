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


#: A temp `config:posts` geometry with TWO posts, so "whose row" is testable:
#: post-a is the caller, post-b must never stamp. Plus the ladder cell the
#: `season` row is read from (config:ladder, never a literal here either).
POSTS_MD = """---
id: "config:posts"
type: config
posts:
  - name: post-a
    role: parent
    town: local-maxxing
    session_name: agi-a1
  - name: post-b
    role: council
    town: sanctuary
    session_name: agi-b1
---

# config:posts
"""

LADDER_MD = """---
id: "config:ladder"
type: config
current_season: 7
---

# config:ladder
"""


def _geometry(project: Path, season: int = 7) -> None:
    geo = project / "nodes" / ".geometry"
    geo.mkdir(parents=True, exist_ok=True)
    (geo / "posts.md").write_text(POSTS_MD, encoding="utf-8")
    (geo / "ladder.md").write_text(
        LADDER_MD.replace("current_season: 7",
                          f"current_season: {season}"), encoding="utf-8")


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

def _frontmatter_of(project: Path, name: str = "g9.9.9.md") -> str:
    return (project / "nodes" / "goal" / name).read_text(encoding="utf-8")


# --------------------------------------------------------------------------
# claim 3 — the CALLING post's config:posts row stamps the rows the file omits
# --------------------------------------------------------------------------

def test_the_calling_posts_row_stamps_the_rows_the_answers_file_omits(
        project, tmp_path):
    f = _write_answers(tmp_path, _answers())
    _geometry(project)
    out, err, rc = _mint(project, f, "--actor", "post-a")
    assert rc == 0, err
    node = _frontmatter_of(project)
    for row in ("edited_by: post-a", "role: parent", "town: local-maxxing",
                "season: 7", "thought_session: agi-a1"):
        assert row in node, f"the stamp is missing {row!r}:\n{node}"


def test_the_stamp_comes_from_the_CALLING_posts_row_only(project, tmp_path):
    """Falsifier 1: a post row that is not the caller's must not stamp — the
    stamp is the POST's, never the environment's, argv's, or last-row's."""
    f = _write_answers(tmp_path, _answers())
    _geometry(project)
    out, err, rc = _mint(project, f, "--actor", "post-a")
    assert rc == 0, err
    node = _frontmatter_of(project)
    for other in ("post-b", "council", "sanctuary", "agi-b1"):
        assert other not in node, f"another post's row stamped {other!r}"


def test_an_unseated_caller_stamps_nothing_rather_than_a_wrong_row(
        project, tmp_path):
    f = _write_answers(tmp_path, _answers())
    _geometry(project)
    out, err, rc = _mint(project, f, "--actor", "post-nobody")
    assert rc == 0, err
    node = _frontmatter_of(project)
    for row in ("role:", "thought_session:"):
        assert row not in node, f"an unseated caller stamped {row!r}"
    assert "town: core" in node, \
        "town here is node_writer's pre-existing DERIVED town (its own "\
        "setdefault), not the config:posts stamp"
    # `edited_by` here is create()'s OWN provenance stamp from --actor, which
    # every route has always carried -- not the config:posts row.
    assert "edited_by: post-nobody" in node


def test_a_row_the_answers_file_sets_wins_over_the_stamp(project, tmp_path):
    """Falsifier 2: the stamp fills what the file is SILENT on, never an
    authored row."""
    f = _write_answers(tmp_path, _answers(role="kid", town="streaming-suite",
                                          thought_session="authored-session"))
    _geometry(project)
    out, err, rc = _mint(project, f, "--actor", "post-a")
    assert rc == 0, err
    node = _frontmatter_of(project)
    assert "role: kid" in node and "role: parent" not in node
    assert "town: streaming-suite" in node and "local-maxxing" not in node
    assert "thought_session: authored-session" in node and "agi-a1" not in node


def test_season_is_owned_by_the_writers_env_stamp_on_both_routes(
        project, tmp_path, monkeypatch):
    """MEASURED, pre-existing, and the reason the post-row stamp is re-applied
    after the mint: `node_writer._stamp_env_fields` OWNS `season` at mint and
    overwrites whatever the mint carried with `AGI_SEASON`. The CONTROL below
    is the pre-existing `--set` route, which loses its `season` row the same
    way — so this is create()'s behaviour, not this round's."""
    monkeypatch.setenv("AGI_SEASON", "5")
    f = _write_answers(tmp_path, _answers())
    _geometry(project)
    out, err, rc = _mint(project, f, "--actor", "post-a")
    assert rc == 0, err
    node = _frontmatter_of(project)
    assert "season: 7" in node and "season: 5" not in node, \
        "the post row is the authority the claim names, so it lands LAST"
    control = _run(["create", "goal", "g8.8.6", "--parent", "goal:g1",
                    "--set", "goal_kind=subgoal", "--set", "status=active",
                    "--set", "goal_id=G8.8.6", "--set", "origin=goals-doc",
                    "--set", "tags=[core]", "--set", "confidence=0.5",
                    "--set", "season=1", "--no-spawn-gate", "--root",
                    str(project)])
    assert control[2] == 0, control[1]
    assert "season: 5" in (project / "nodes" / "goal" / "g8.8.6.md").read_text(
        encoding="utf-8"), "the argv route already behaved this way"


def test_the_stamp_lands_BEFORE_the_required_row_check(project, tmp_path):
    """Falsifier 3: a stamp landing after `seed_required` would refuse a
    required row the stamp was about to supply. The temp schema copy (the
    LIVE [goal].md, read not transcribed) declares `town` required, and the
    answers file omits it."""
    schema = project / "context" / "schemas" / "[goal].md"
    schema.write_text(
        schema.read_text(encoding="utf-8").replace(
            "  required: [id, type, mint_id, title, goal_id, goal_kind, "
            "status, origin, seeds, confidence, tags]",
            "  required: [id, type, mint_id, title, goal_id, goal_kind, "
            "status, origin, seeds, confidence, tags, town]"),
        encoding="utf-8")
    f = _write_answers(tmp_path, _answers())
    _geometry(project)
    out, err, rc = _mint(project, f, "--actor", "post-a")
    assert rc == 0, f"the stamp was refused as a missing required row: {err}"
    assert "town: local-maxxing" in _frontmatter_of(project)


def test_a_stamp_value_is_validated_by_the_SAME_row_validator(project,
                                                               tmp_path):
    """Falsifier 4: the stamp must go THROUGH the row validator, not around
    it. The temp schema copy declares `town` a bool, so the post row's own
    string value is a bad row and must be refused BY NAME."""
    schema = project / "context" / "schemas" / "[goal].md"
    text = schema.read_text(encoding="utf-8")
    text = text.replace("  tags: {type: list}",
                        "  tags: {type: list}\n  town: {type: str}")
    text = text.replace("  types:\n    seeds: list",
                        "  types:\n    seeds: list\n    town: bool")
    schema.write_text(text, encoding="utf-8")
    f = _write_answers(tmp_path, _answers())
    _geometry(project)
    out, err, rc = _mint(project, f, "--actor", "post-a")
    assert rc == 2, out
    assert "town" in err
    assert not (project / "nodes" / "goal" / "g9.9.9.md").exists(), \
        "an unvalidated stamp value must not reach disk"


def test_a_corrupt_ladder_cell_stamps_no_season_row(project, tmp_path):
    f = _write_answers(tmp_path, _answers())
    _geometry(project)
    (project / "nodes" / ".geometry" / "ladder.md").write_text(
        LADDER_MD.replace("current_season: 7", 'current_season: "seven"'),
        encoding="utf-8")
    out, err, rc = _mint(project, f, "--actor", "post-a")
    assert rc == 0, err
    assert "seven" not in _frontmatter_of(project), \
        "a non-int ladder cell must stamp nothing, not a bad row"


def test_the_answers_route_mentions_no_transcribed_stamp_value():
    """Every stamped value is READ from `config:posts` / `config:ladder`;
    none of a row's own values is typed into write.py."""
    src = (BIN / "write.py").read_text(encoding="utf-8")
    body = src.split("def _post_stamp(", 1)[1].split("\ndef ", 1)[0]
    for literal in ("local-maxxing", "sanctuary", "agi-", "current_season:"):
        assert literal not in body, \
            f"_post_stamp transcribed {literal!r} instead of reading the cell"


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


# --------------------------------------------------------------------------
# KID 1 (DH.502) — the three holes: identity rows, `--set` vs the post stamp,
# and the precedence stated ONCE
# --------------------------------------------------------------------------

@pytest.mark.parametrize("row", ["id", "mint_id", "next_edges", "scaffold_hash"])
def test_an_answers_row_naming_a_MINTED_row_refuses_by_name(project, tmp_path,
                                                             row):
    """Hole 1. `node_writer.write_node` builds id/mint_id/next_edges/
    scaffold_hash and only THEN runs `fm.update(extra_fm)`, so an answers row
    naming one used to overwrite the node's own identity silently."""
    f = _write_answers(tmp_path, _answers(**{row: "goal:g-stolen"
                                             if row == "id" else "x"}))
    out, err, rc = _mint(project, f)
    assert rc == 2, out
    assert row in err and "MINTED" in err
    assert not (project / "nodes" / "goal" / "g9.9.9.md").exists()


def test_the_argv_set_route_refuses_a_MINTED_row_by_the_same_check(project,
                                                                   tmp_path):
    """Hole 1, the second copy of the hole: the argv `--set` route had it too.
    ONE shared check, so the two routes cannot drift apart."""
    _out, err, rc = _run(["create", "goal", "g8.8.5", "--parent", "goal:g1",
                          "--set", "mint_id=0000", "--root", str(project)])
    assert rc == 2 and "mint_id" in err and "MINTED" in err
    assert not (project / "nodes" / "goal" / "g8.8.5.md").exists()


def test_an_explicit_set_BEATS_the_calling_posts_stamp(project, tmp_path):
    """Hole 2. `post_rows` was filtered on `answers` alone, so an explicit
    `--set role=...` was overwritten by the post's row. THE RULE CHOSEN: the
    explicit `--set` WINS (rank 1 of the precedence)."""
    f = _write_answers(tmp_path, _answers())
    _geometry(project)
    out, err, rc = _mint(project, f, "--actor", "post-a",
                         "--set", "role=council")
    assert rc == 0, err
    node = _frontmatter_of(project)
    assert "role: council" in node and "role: parent" not in node, \
        "an explicit --set outranks the calling post's row"


def test_an_explicit_set_BEATS_the_answers_file_row_too(project, tmp_path):
    """Rank 1 over rank 2, same rule, no second copy of the check."""
    f = _write_answers(tmp_path, _answers(role="kid"))
    _geometry(project)
    out, err, rc = _mint(project, f, "--actor", "post-a",
                         "--set", "role=council")
    assert rc == 0, err
    assert "role: council" in _frontmatter_of(project)


def test_the_answers_files_own_row_beats_the_ENVIRONMENT(project, tmp_path,
                                                          monkeypatch):
    """Ranks 2 and 4 of the precedence, executed: the mint's environment stamp
    (`node_writer._stamp_env_fields`) must not silently replace what the file
    asked for. Without a matching post row, too — the re-stamp is not gated
    on the post stamp existing."""
    monkeypatch.setenv("AGI_ROLE", "director")
    monkeypatch.setenv("AGI_SEASON", "5")
    f = _write_answers(tmp_path, _answers(role="kid", season=7))
    out, err, rc = _mint(project, f)
    assert rc == 0, err
    node = _frontmatter_of(project)
    assert "role: kid" in node and "role: director" not in node
    assert "season: 7" in node and "season: 5" not in node


def test_the_precedence_is_STATED_ONCE_and_the_routes_follow_it():
    """Hole 3. The order lives in ONE place (`_STAMP_ROWS` + the answers-file
    docstring), and the argv route is untouched by it: without `--answers`
    nothing is re-stamped, so `--set season` still loses to `AGI_SEASON`."""
    src = (BIN / "write.py").read_text(encoding="utf-8")
    assert src.count("_STAMP_ROWS = (") == 1, "one source for the order"
    doc = src.split("def _read_answers_file(", 1)[1].split('"""', 2)[2]
    assert "`--set`" in doc and "answers file" in doc and "environment" in doc
