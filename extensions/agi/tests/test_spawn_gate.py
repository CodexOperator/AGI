"""Tests for the S17 spawn gate — bin/spawn_gate.py + both writer paths.

Rule under test: a node's `type:` and `parents:` must satisfy the `spawn:`
block of `context/schemas/[<type>].md`. Exactly three shapes may be
parentless (`goal:long-term`, `goal:short-term`, `idea`); every other type
needs >= 1 parent; max-parents is per type and capped by `[shape].md`.

The three behaviours that matter, in order of how easy they are to get wrong:

1. **Rejection names the rule AND the schema file.** A gate that says "no"
   without saying which rule or where it is written is a worse prose control
   than none, because it looks like a code control.
2. **Approval is announced.** An agent cannot distinguish "approved" from
   "not checked" if only failure speaks.
3. **Undecidable is unverified, not approved and not rejected.** Missing
   schema, missing `spawn:` block, unresolvable parent id — all fail OPEN and
   say so. Inferring the missing parent is inventing one (G7.1).
"""

import importlib.util
import json
import subprocess
import sys
import textwrap
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parents[1] / "bin"


def _load(name, filename=None):
    path = BIN / (filename or f"{name}.py")
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


sg = _load("spawn_gate")


# --------------------------------------------------------------------------
# fixtures — a minimal project: schemas + a couple of real nodes
# --------------------------------------------------------------------------

SHAPE = """\
---
name: shape
structural: true
parentless_types:
  - goal:long-term
  - goal:short-term
  - idea
max_parents_ceiling: 2
---
shape
"""

VERDICT = """\
---
name: verdict
spawn:
  allowed_parents: [experiment, verdict, hypothesis]
  min_parents: 1
  max_parents: 2
---
verdict
"""

TASK = """\
---
name: task
spawn:
  allowed_parents: [hypothesis]
  min_parents: 1
  max_parents: 1
---
task
"""

IDEA = """\
---
name: idea
spawn:
  allowed_parents: [goal]
  min_parents: 0
  max_parents: 1
---
idea
"""

GOAL = """\
---
name: goal
spawn:
  discriminator: goal_kind
  variants:
    long-term:  {allowed_parents: [], min_parents: 0, max_parents: 0}
    short-term: {allowed_parents: [], min_parents: 0, max_parents: 0}
    subgoal:    {allowed_parents: [goal], min_parents: 1, max_parents: 1}
---
goal
"""

CONFIG = """\
---
name: config
structural: true
locations:
  nodes_root:
    role: the graph itself
    path: "<graph_root>/nodes"
---
config
"""

NO_SPAWN = """\
---
name: outcome
fields:
  title: {type: str}
---
outcome, with no spawn block
"""


@pytest.fixture
def project(tmp_path):
    """A throwaway graph repo with schemas and four real nodes."""
    (tmp_path / "agi-tree.config.json").write_text("{}")
    sd = tmp_path / "context" / "schemas"
    sd.mkdir(parents=True)
    for fname, body in [
        ("[shape].md", SHAPE), ("[verdict].md", VERDICT), ("[task].md", TASK),
        ("[idea].md", IDEA), ("[goal].md", GOAL), ("[config].md", CONFIG),
        ("[outcome].md", NO_SPAWN),
    ]:
        (sd / fname).write_text(body)
    # An inactive copy that must never be enforced.
    (sd / "mvp.md").write_text(
        "---\nname: mvp\nspawn:\n  allowed_parents: []\n"
        "  min_parents: 0\n  max_parents: 9\n---\ninactive\n"
    )
    nd = tmp_path / "nodes"
    for ntype, slug in [("goal", "s17"), ("idea", "seed"),
                        ("hypothesis", "h1"), ("experiment", "e1")]:
        d = nd / ntype
        d.mkdir(parents=True, exist_ok=True)
        (d / f"{slug}.md").write_text(
            f"---\nid: {ntype}:{slug}\ntype: {ntype}\n---\n\nbody\n"
        )
    return tmp_path


@pytest.fixture
def gate(project):
    rules, index = sg.gate_for_root(project)
    return rules, index


# --------------------------------------------------------------------------
# loading
# --------------------------------------------------------------------------

def test_loads_every_active_schema_and_no_inactive_one(gate):
    rules, _ = gate
    assert rules.schema_errors == []
    assert set(rules.schemas) >= {"verdict", "task", "idea", "goal", "outcome"}
    # `mvp.md` is unbracketed: inactive, never enforced. Its absurd
    # max_parents: 9 would have tripped the ceiling check had it been read.
    assert "mvp" not in rules.schemas


def test_geometry_comes_from_shape_md(gate):
    rules, _ = gate
    assert rules.geometry.max_parents_ceiling == 2
    assert rules.geometry.parentless_types == frozenset(
        {"goal:long-term", "goal:short-term", "idea"}
    )


def test_shape_key_canonicalises_type_half_only():
    # `goal_kind: long-term` legitimately contains a hyphen. Canonicalising
    # the whole key turned it into `goal:long_term`, which matched no shape
    # and silently disabled the entire [goal].md schema.
    assert sg.canonical_shape_key("goal:long-term") == "goal:long-term"
    assert sg.canonical_shape_key("bigger-outcome") == "bigger_outcome"
    assert sg.canonical_shape_key("app-purpose:x-y") == "app_purpose:x-y"


def test_config_md_is_actually_read_for_nodes_root(project):
    # G10.2: a geometry declaration no code path consults is prose with a
    # directory name. This is that consultation.
    assert sg.resolve_nodes_root(project) == project / "nodes"
    (project / "context" / "schemas" / "[config].md").write_text(
        CONFIG.replace("<graph_root>/nodes", "<graph_root>/elsewhere")
    )
    assert sg.resolve_nodes_root(project) == project / "elsewhere"


def test_missing_config_falls_back_to_nodes(project):
    (project / "context" / "schemas" / "[config].md").unlink()
    assert sg.resolve_nodes_root(project) == project / "nodes"


# --------------------------------------------------------------------------
# schema-level invariants: a broken schema is refused, not obeyed
# --------------------------------------------------------------------------

def test_min_parents_zero_outside_the_whitelist_is_a_schema_error(project):
    (project / "context" / "schemas" / "[task].md").write_text(
        TASK.replace("min_parents: 1", "min_parents: 0")
    )
    rules = sg.load_spawn_rules(project / "context" / "schemas", root=project)
    assert any("parentless_types" in msg for _, msg in rules.schema_errors)
    # Refused, not obeyed: the type falls back to unverified.
    res = sg.check_spawn("task", [], rules=rules, type_index={})
    assert res.status == sg.UNVERIFIED
    assert res.ok


def test_max_parents_above_the_ceiling_is_a_schema_error(project):
    (project / "context" / "schemas" / "[task].md").write_text(
        TASK.replace("max_parents: 1", "max_parents: 5")
    )
    rules = sg.load_spawn_rules(project / "context" / "schemas", root=project)
    assert any("ceiling" in msg for _, msg in rules.schema_errors)
    res = sg.check_spawn("task", ["hypothesis:h1"], rules=rules, type_index={})
    assert res.status == sg.UNVERIFIED


# --------------------------------------------------------------------------
# the pre-registered falsifier, as a test
# --------------------------------------------------------------------------

def test_verdict_with_no_parent_is_rejected_naming_rule_and_schema(gate):
    rules, index = gate
    res = sg.check_spawn("verdict", [], rules=rules, type_index=index,
                         node_id="verdict:orphan")
    assert res.status == sg.REJECTED
    assert not res.ok
    assert "min_parents" in res.reason
    assert "[verdict].md" in res.reason          # the schema file, by name
    assert "verdict:orphan" in res.messages[0]   # the node, by name
    assert res.fix                                # and what would fix it


def test_task_with_three_parents_is_rejected(gate):
    rules, index = gate
    res = sg.check_spawn(
        "task", ["hypothesis:h1", "hypothesis:h1", "hypothesis:h1"],
        rules=rules, type_index=index, node_id="task:triple")
    assert res.status == sg.REJECTED
    assert "max_parents" in res.reason
    assert "[task].md" in res.reason
    assert "[shape].md" in res.fix   # raising the budget takes two edits


def test_legal_spawn_is_explicitly_approved(gate):
    rules, index = gate
    res = sg.check_spawn("verdict", ["experiment:e1"], rules=rules,
                         type_index=index, node_id="verdict:ok")
    assert res.status == sg.APPROVED
    assert res.approved and res.ok
    assert "APPROVED" in res.messages[0]
    assert "[verdict].md" in res.messages[0]     # against WHAT it was checked
    assert res.applied == [
        "min_parents>=1", "max_parents<=2",
        "allowed_parents={experiment, hypothesis, verdict}",
    ]


def test_wrong_parent_type_is_rejected(gate):
    rules, index = gate
    res = sg.check_spawn("verdict", ["idea:seed"], rules=rules,
                         type_index=index, node_id="verdict:wrongparent")
    assert res.status == sg.REJECTED
    assert "allowed_parents" in res.reason
    assert "'idea'" in res.reason


# --------------------------------------------------------------------------
# parentless-legal shapes, and the discriminator
# --------------------------------------------------------------------------

def test_idea_may_be_parentless(gate):
    rules, index = gate
    res = sg.check_spawn("idea", [], rules=rules, type_index=index)
    assert res.status == sg.APPROVED
    assert "parentless-legal" in res.messages[0]


@pytest.mark.parametrize("kind", ["long-term", "short-term"])
def test_goal_roots_may_be_parentless(gate, kind):
    rules, index = gate
    res = sg.check_spawn("goal", [], rules=rules, type_index=index,
                         fm={"goal_kind": kind})
    assert res.status == sg.APPROVED


def test_subgoal_may_not_be_parentless(gate):
    rules, index = gate
    res = sg.check_spawn("goal", [], rules=rules, type_index=index,
                         fm={"goal_kind": "subgoal"}, node_id="goal:g7.2")
    assert res.status == sg.REJECTED
    # The whole point of the discriminator: a flat allowed_parents: [] on
    # `goal` would have licensed all 48 subgoals to float free.
    assert "goal:subgoal" in res.reason


def test_subgoal_with_one_goal_parent_is_approved(gate):
    rules, index = gate
    res = sg.check_spawn("goal", ["goal:s17"], rules=rules, type_index=index,
                         fm={"goal_kind": "subgoal"})
    assert res.status == sg.APPROVED


def test_missing_discriminator_is_unverified_not_approved(gate):
    rules, index = gate
    res = sg.check_spawn("goal", [], rules=rules, type_index=index, fm={})
    assert res.status == sg.UNVERIFIED
    assert "goal_kind" in res.reason


# --------------------------------------------------------------------------
# fail-open paths
# --------------------------------------------------------------------------

def test_unknown_type_is_unverified_and_written(gate):
    rules, index = gate
    res = sg.check_spawn("no_such_type", [], rules=rules, type_index=index)
    assert res.status == sg.UNVERIFIED
    assert res.ok


def test_schema_without_spawn_block_is_unverified(gate):
    rules, index = gate
    res = sg.check_spawn("outcome", [], rules=rules, type_index=index)
    assert res.status == sg.UNVERIFIED
    assert "no spawn: block" in res.reason


def test_unresolvable_parent_is_unverified_never_invented(gate):
    rules, index = gate
    res = sg.check_spawn("verdict", ["experiment:does-not-exist"], rules=rules,
                         type_index=index)
    assert res.status == sg.UNVERIFIED
    assert res.ok
    assert "experiment:does-not-exist" in res.reason


def test_no_type_index_declines_to_approve(gate):
    rules, _ = gate
    res = sg.check_spawn("verdict", ["experiment:e1"], rules=rules,
                         type_index=None)
    # Counts still checked; types cannot be, so it does not claim approval.
    assert res.status == sg.UNVERIFIED


def test_bypass_is_loud_and_stamped(gate):
    rules, index = gate
    res = sg.check_spawn("verdict", [], rules=rules, type_index=index,
                         bypass=True)
    assert res.status == sg.BYPASSED
    assert res.ok
    fm = sg.stamp({}, res)
    assert fm == {"spawn_gate": "bypassed"}


def test_approval_is_not_stamped(gate):
    rules, index = gate
    res = sg.check_spawn("idea", [], rules=rules, type_index=index)
    assert sg.stamp({}, res) == {}


def test_unverified_is_stamped_with_a_reason(gate):
    rules, index = gate
    res = sg.check_spawn("verdict", ["experiment:nope"], rules=rules,
                         type_index=index)
    fm = sg.stamp({}, res)
    assert fm["spawn_check"] == "unverified"
    assert "nope" in fm["spawn_check_reason"]


# --------------------------------------------------------------------------
# hyphen/underscore: one type, two spellings, zero renames
# --------------------------------------------------------------------------

def test_both_spellings_resolve_to_one_rule(project):
    sd = project / "context" / "schemas"
    (sd / "[bigger_outcome].md").write_text(
        "---\nname: bigger_outcome\nspawn:\n"
        "  allowed_parents: [outcome, mvp]\n  min_parents: 1\n"
        "  max_parents: 2\n---\nb\n"
    )
    (project / "nodes" / "outcome").mkdir(parents=True, exist_ok=True)
    (project / "nodes" / "outcome" / "o1.md").write_text(
        "---\nid: outcome:o1\ntype: outcome\n---\n\nb\n")
    rules, index = sg.gate_for_root(project)
    for spelling in ("bigger_outcome", "bigger-outcome"):
        res = sg.check_spawn(spelling, ["outcome:o1"], rules=rules,
                             type_index=index)
        assert res.status == sg.APPROVED, spelling


def test_parent_typed_with_a_hyphen_still_validates(project):
    # One real app_purpose node names a parent typed `bigger-outcome` while
    # allowed_parents says `bigger_outcome`. A literal match would reject a
    # correct edge over punctuation.
    sd = project / "context" / "schemas"
    (sd / "[app_purpose].md").write_text(
        "---\nname: app_purpose\nspawn:\n"
        "  allowed_parents: [bigger_outcome, outcome]\n  min_parents: 1\n"
        "  max_parents: 2\n---\na\n"
    )
    d = project / "nodes" / "bigger-outcome"
    d.mkdir(parents=True, exist_ok=True)
    (d / "b1.md").write_text(
        "---\nid: bigger-outcome:b1\ntype: bigger-outcome\n---\n\nb\n")
    rules, index = sg.gate_for_root(project)
    res = sg.check_spawn("app_purpose", ["bigger-outcome:b1"], rules=rules,
                         type_index=index)
    assert res.status == sg.APPROVED


# --------------------------------------------------------------------------
# announce(): BOTH outcomes speak
# --------------------------------------------------------------------------

def test_announce_prints_on_approval_too(gate, capsys):
    rules, index = gate
    sg.announce(sg.check_spawn("idea", [], rules=rules, type_index=index))
    out = capsys.readouterr()
    assert "SPAWN-GATE APPROVED" in out.out   # grep-able marker on stdout
    assert "SPAWN-GATE APPROVED" in out.err   # full explanation on stderr


def test_announce_prints_on_rejection(gate, capsys):
    rules, index = gate
    sg.announce(sg.check_spawn("verdict", [], rules=rules, type_index=index))
    out = capsys.readouterr()
    assert "SPAWN-GATE REJECTED" in out.out
    assert "[verdict].md" in out.err


# --------------------------------------------------------------------------
# writer paths — the whole point is that this is not a linter
# --------------------------------------------------------------------------

def _run_cli(project, *args):
    return subprocess.run(
        [sys.executable, str(BIN / "cli.py"), *args],
        cwd=str(project), capture_output=True, text=True,
    )


@pytest.fixture
def wired_project(project):
    """`project` plus what cli.py needs: an agent record and a goal parent."""
    ad = project / "sessions" / "iter-001" / "a1"
    ad.mkdir(parents=True)
    (ad / "agent.json").write_text(json.dumps({"id": "a1", "status": "run"}))
    return project


def test_cli_scaffold_rejects_a_parentless_verdict(wired_project):
    r = _run_cli(wired_project, "scaffold", "1", "a1",
                 "--type", "verdict", "--slug", "orphan")
    assert r.returncode == 2
    assert "SPAWN-GATE REJECTED" in r.stdout
    assert "[verdict].md" in r.stderr
    assert "min_parents" in r.stderr
    # Rejected means NOTHING is written, same as an evidence taxonomy failure.
    assert not (wired_project / "nodes" / "verdict" / "orphan.md").exists()


def test_cli_scaffold_rejects_a_task_with_three_parents(wired_project):
    r = _run_cli(wired_project, "scaffold", "1", "a1", "--type", "task",
                 "--slug", "triple", "--parent", "hypothesis:h1",
                 "--parent", "hypothesis:h1", "--parent", "hypothesis:h1")
    assert r.returncode == 2
    assert "max_parents" in r.stderr
    assert not (wired_project / "nodes" / "task" / "triple.md").exists()


def test_cli_scaffold_approves_and_says_so(wired_project):
    r = _run_cli(wired_project, "scaffold", "1", "a1", "--type", "verdict",
                 "--slug", "good", "--parent", "experiment:e1")
    assert r.returncode == 0
    assert "SPAWN-GATE APPROVED" in r.stdout
    assert "[verdict].md" in r.stdout
    node = wired_project / "nodes" / "verdict" / "good.md"
    assert node.exists()
    # An approval leaves no frontmatter mark; the terminal line is the feedback.
    assert "spawn_gate" not in node.read_text()
    assert "spawn_check" not in node.read_text()


def test_cli_scaffold_bypass_is_stamped(wired_project):
    r = _run_cli(wired_project, "scaffold", "1", "a1", "--type", "verdict",
                 "--slug", "bypassed", "--no-spawn-gate")
    assert r.returncode == 0
    assert "SPAWN-GATE BYPASSED" in r.stdout
    text = (wired_project / "nodes" / "verdict" / "bypassed.md").read_text()
    assert "spawn_gate: bypassed" in text


def test_cli_scaffold_canonicalises_the_type_spelling(wired_project):
    (wired_project / "context" / "schemas" / "[bigger_outcome].md").write_text(
        "---\nname: bigger_outcome\nspawn:\n  allowed_parents: [outcome, mvp]\n"
        "  min_parents: 1\n  max_parents: 2\n---\nb\n")
    d = wired_project / "nodes" / "outcome"
    d.mkdir(parents=True, exist_ok=True)
    (d / "o1.md").write_text("---\nid: outcome:o1\ntype: outcome\n---\n\nb\n")
    r = _run_cli(wired_project, "scaffold", "1", "a1",
                 "--type", "bigger-outcome", "--slug", "bo",
                 "--parent", "outcome:o1")
    assert r.returncode == 0
    text = (wired_project / "nodes" / "bigger_outcome" / "bo.md").read_text()
    # Hyphen accepted as an alias, underscore written. No node is renamed;
    # the generator simply stops producing new hyphens.
    assert "id: bigger_outcome:bo" in text
    assert "type: bigger_outcome" in text


def test_cli_done_gates_its_fallback_verdict_node(wired_project):
    r = subprocess.run(
        [sys.executable, str(BIN / "cli.py"), "done", "1", "a1",
         "--verdict", "pending", "--node-id", "exp:nonexistent"],
        cwd=str(wired_project), capture_output=True, text=True,
    )
    # No --parent: the fallback path would have written a parentless verdict,
    # which is exactly how 21 of them got into the corpus.
    assert r.returncode == 2
    assert "SPAWN-GATE REJECTED" in r.stdout
    assert not list((wired_project / "nodes" / "verdict").glob("exp_*.md"))


def test_cli_done_fallback_writes_mint_id_when_approved(wired_project):
    r = subprocess.run(
        [sys.executable, str(BIN / "cli.py"), "done", "1", "a1",
         "--verdict", "pending", "--node-id", "exp:nonexistent",
         "--parent", "experiment:e1"],
        cwd=str(wired_project), capture_output=True, text=True,
    )
    assert r.returncode == 0, r.stderr
    text = (wired_project / "nodes" / "verdict" / "exp_nonexistent.md").read_text()
    assert "SPAWN-GATE APPROVED" in r.stdout
    # goal:s14 — without this the node is skipped by `grid.py commit --all`.
    assert "mint_id:" in text


def test_post_wire_reaches_the_gate_through_the_one_writer():
    # Cheap structural check, updated for goal:s17's consolidation: post_wire
    # no longer calls `check_spawn` itself, it calls the one routine that
    # does. Asserting the direct call here would now push a writer BACK to
    # having its own copy — which is the defect, not the fix. The full
    # "every writer routes through node_writer" check lives in
    # tests/test_node_writer.py.
    text = (BIN / "post_wire.py").read_text()
    assert "import node_writer" in text
    assert "node_writer.write_node" in text
    # It still loads the rules once per pass and reports broken schemas.
    assert "spawn_gate.gate_for_root" in text
    assert "spawn_gate.announce_schema_errors" in text


# --------------------------------------------------------------------------
# the real project's own schemas must be self-consistent
# --------------------------------------------------------------------------

def test_shipped_schemas_load_without_error():
    """Guards the two ways the shipped schemas broke while being written.

    Skipped outside the agi-tree checkout — the engine ships no schemas of
    its own, so there is nothing to check in a bare clone.
    """
    here = Path(__file__).resolve()
    candidates = [p / "context" / "schemas"
                  for p in here.parents
                  if (p / "context" / "schemas").is_dir()]
    candidates += [p / "agi-tree" / "context" / "schemas"
                   for p in here.parents
                   if (p / "agi-tree" / "context" / "schemas").is_dir()]
    if not candidates:
        pytest.skip("no context/schemas/ in this checkout")
    sd = candidates[0]
    rules = sg.load_spawn_rules(sd)
    assert rules.schema_errors == [], rules.schema_errors
    # A `---` anywhere inside frontmatter truncates it under the cheap split
    # parser every writer path uses. A comment banner of dashes did exactly
    # that to [shape].md and silently emptied the geometry.
    assert rules.geometry.source.endswith("[shape].md")
    assert rules.geometry.max_parents_ceiling >= 1
    assert "verdict" in rules.schemas
