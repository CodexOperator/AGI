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
import re
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
  - moral
max_parents_ceiling: 2
edge_fields:
  parents:         {role: lineage,    traversable: true}
  next_edges:      {role: lineage,    traversable: true}
  depends_on:      {role: scheduling, traversable: false}
  seeds:           {role: provenance, traversable: false}
  proposes_goals:  {role: proposal,   traversable: false}
  season_parents:  {role: season,     traversable: false}
  grounded_in:     {role: provenance, traversable: false}
  authors:         {role: provenance, traversable: false}
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
  min_parents: 1
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
    long-term:  {allowed_parents: [goal], min_parents: 1, max_parents: 1}
    short-term: {allowed_parents: [goal], min_parents: 1, max_parents: 1}
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
    rules, index, _ = sg.gate_for_root(project)
    return rules, index


# ---------------------------------------------------------------------------
# hypothesis:l3w4-seat-registry — read_seat_registry
# ---------------------------------------------------------------------------

def test_read_seat_registry_none_when_node_absent_fails_open(tmp_path):
    """No .geometry/seats.md -> None, never an exception: dispatch falls back
    to the ladder/config rather than blocking on a missing seat node."""
    nodes_dir = tmp_path / "nodes"
    nodes_dir.mkdir(parents=True)
    assert sg.read_seat_registry(nodes_dir) is None
    assert sg.read_seat_registry(None) is None


def test_read_seat_registry_returns_declared_rows(tmp_path):
    seats_md = tmp_path / "nodes" / ".geometry" / "seats.md"
    seats_md.parent.mkdir(parents=True)
    seats_md.write_text((
        "---\nid: config:seats\ntype: config\n"
        "seats:\n"
        "  - {name: liaison, role: director, tier: 1, harness: claude-code, "
        "model: claude-sonnet-5, effort: high, settings: ''}\n"
        "  - {name: belam, role: prime_director, tier: 3, harness: claude-code, "
        "model: claude-fable-5-1, effort: max, settings: ultracode}\n"
        "---\n"
    ))
    rows = sg.read_seat_registry(tmp_path / "nodes")
    assert isinstance(rows, list) and len(rows) == 2
    names = [r["name"] for r in rows]
    assert names == ["liaison", "belam"]
    assert rows[0]["model"] == "claude-sonnet-5"


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
    assert rules.geometry.parentless_types == frozenset({"moral"})
    assert "idea" not in rules.geometry.parentless_types
    assert "goal:long-term" not in rules.geometry.parentless_types
    assert "goal:short-term" not in rules.geometry.parentless_types


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

def test_idea_may_not_be_parentless_anymore(gate):
    """`goal:g12` — only moral is parentless-legal.

    idea was removed from parentless_types in [shape].md. A parentless idea
    is now REJECTED at the gate. The 42 pre-existing parentless ideas are
    season 1, grandfathered.
    """
    rules, index = gate
    res = sg.check_spawn("idea", [], rules=rules, type_index=index,
                         node_id="idea:new-root")
    assert res.status == sg.REJECTED
    assert "min_parents" in res.reason


@pytest.mark.parametrize("kind", ["long-term", "short-term"])
def test_goal_roots_may_not_be_parentless_anymore(gate, kind):
    """`goal:g12` — only moral is parentless-legal.

    goal:long-term and goal:short-term were removed from parentless_types.
    A root goal is now REJECTED at the gate. The 27 pre-existing roots are
    season 1, grandfathered.
    """
    rules, index = gate
    res = sg.check_spawn("goal", [], rules=rules, type_index=index,
                         fm={"goal_kind": kind}, node_id=f"goal:{kind}-new")
    assert res.status == sg.REJECTED


def test_only_moral_is_parentless_legal(gate):
    """`goal:g12` — only the type 'moral' may be parentless.

    Verifies the gate geometry declares exactly one parentless type and that
    attempting to spawn any other type without a parent is REJECTED or, for
    unregistered types, UNVERIFIED.
    """
    rules, index = gate
    # moral has no schema yet, so it's UNVERIFIED rather than APPROVED;
    # the geometry still declares it as the sole parentless-legal entry.
    assert "moral" in rules.geometry.parentless_types
    assert len(rules.geometry.parentless_types) == 1
    assert "idea" not in rules.geometry.parentless_types
    assert "goal:long-term" not in rules.geometry.parentless_types
    assert "goal:short-term" not in rules.geometry.parentless_types


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
    rules, index, _ = sg.gate_for_root(project)
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
    rules, index, _ = sg.gate_for_root(project)
    res = sg.check_spawn("app_purpose", ["bigger-outcome:b1"], rules=rules,
                         type_index=index)
    assert res.status == sg.APPROVED


# --------------------------------------------------------------------------
# announce(): BOTH outcomes speak
# --------------------------------------------------------------------------

def test_announce_prints_on_approval_too(gate, capsys):
    rules, index = gate
    sg.announce(sg.check_spawn("task", ["hypothesis:h1"], rules=rules,
                               type_index=index))
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
    candidates += [p / ".agi" / "context" / "schemas"
                   for p in here.parents
                   if (p / ".agi" / "context" / "schemas").is_dir()]
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


def _shipped_schemas_dir():
    """`context/schemas` for this checkout, under any known layout.

    Bare `context/` (legacy), `.agi/context/` (post-`goal:g11`), and
    `agi-tree/context/` (the pre-migration nested name). None -> no checkout.
    """
    here = Path(__file__).resolve()
    for p in here.parents:
        for rel in (("context", "schemas"),
                    (".agi", "context", "schemas"),
                    ("agi-tree", "context", "schemas")):
            c = p.joinpath(*rel)
            if c.is_dir():
                return c
    return None


def _flat_or_variants(schema):
    """Every Rule a schema enforces — flat or one per variant (build_kind)."""
    if schema.flat:
        return [schema.flat]
    return list(schema.variants.values())


def test_goal_may_not_parent_mvp_or_experiment():
    """`goal:s22` — a goal spawns hypotheses, not designs or runs.

    `goal` is dropped from `[mvp].md` and `[experiment].md`, but kept where it
    is the intended route (`hypothesis`, `idea`) or the only legal parent
    (`cron` — a blanket strip would orphan the type), and kept in `[build].md`
    because level3.py mints builds mechanically, outside the gate.
    """
    sd = _shipped_schemas_dir()
    if sd is None:
        pytest.skip("no context/schemas in this checkout")
    rules = sg.load_spawn_rules(sd)
    assert rules.schema_errors == [], rules.schema_errors
    for ntype in ("mvp", "experiment"):
        for rule in _flat_or_variants(rules.schemas[ntype]):
            assert "goal" not in rule.allowed_parents, (
                f"goal -> {ntype} must be rejected; allows "
                f"{sorted(rule.allowed_parents)}")
    for ntype in ("hypothesis", "idea", "cron", "build"):
        rules_list = _flat_or_variants(rules.schemas[ntype])
        assert rules_list, f"[{ntype}].md has no spawn: rule"
        for rule in rules_list:
            assert "goal" in rule.allowed_parents, (
                f"goal -> {ntype} is the intended (or only) route and was "
                f"over-stripped; allows {sorted(rule.allowed_parents)}")


def test_kid_contract_advertises_only_gate_legal_routes():
    """`goal:s22` — the kid brief in `zoom.py` and the spawn gate agree.

    Before `goal:s22` the contract advertised `mvp from exp` and never told a
    kid the `verdict` step existed: the brief advertised exactly the chain the
    gate closes, which is how `goal:g1.9` says a prose control drifts from the
    code control. So the test reads BOTH: every `X from Y` the contract
    promises must be a spawn the gate would approve, and the two copies of the
    line in `zoom.py` must be the same line.
    """
    zoom_py = Path(__file__).resolve().parents[1] / "bin" / "zoom.py"
    sd = _shipped_schemas_dir()
    if sd is None or not zoom_py.is_file():
        pytest.skip("no checkout to check (schemas + bin/zoom.py)")
    rules = sg.load_spawn_rules(sd)
    text = zoom_py.read_text()
    lines = re.findall(r"Acceptable: spawn one child node \(([^)]*)\)", text)
    assert len(lines) == 2, f"expected two kid-contract lines, found {len(lines)}"
    assert lines[0] == lines[1], "the two kid-contract lines drifted apart"
    assert "mvp from exp" not in lines[0], (
        "the kid contract still advertises the verdict-less shortcut")
    abbr = {"hyp": "hypothesis", "exp": "experiment"}
    for child_abbr, parent_abbr in re.findall(r"(\w+) from (\w+)", lines[0]):
        child = abbr.get(child_abbr, child_abbr)
        parent = abbr.get(parent_abbr, parent_abbr)
        schema = rules.schemas.get(child)
        assert schema is not None, f"no schema for `{child}`"
        rule_list = _flat_or_variants(schema)
        assert rule_list, f"[{child}].md has no spawn: rule"
        assert all(sg.canonical_type(parent) in r.allowed_parents
                   for r in rule_list), (
            f"kid contract advertises `{child_abbr} from {parent_abbr}` but "
            f"{child} allows "
            f"{sorted(set().union(*[r.allowed_parents for r in rule_list]))}")


# --------------------------------------------------------------------------
# min_parents_by_type — per-kind parent floors
#
# `min_parents` counts parents; this counts parents *of a kind*. The type it
# exists for is `bigger_outcome`, where "two outcomes" and "one verdict plus
# one outcome" are the same arity and different shapes — the second is the
# convergence the graph is supposed to force, and arity alone cannot say so.
# --------------------------------------------------------------------------

BIGGER_OUTCOME = """\
---
name: bigger_outcome
spawn:
  allowed_parents: [outcome, verdict]
  min_parents: 2
  max_parents: 2
  min_parents_by_type: {verdict: 1, outcome: 1}
---
bigger_outcome
"""


@pytest.fixture
def converging(project):
    """`project`, plus a bigger_outcome schema and one node of each parent kind."""
    (project / "context" / "schemas" / "[bigger_outcome].md").write_text(BIGGER_OUTCOME)
    for ntype, slug in [("outcome", "o1"), ("outcome", "o2"), ("verdict", "v1")]:
        d = project / "nodes" / ntype
        d.mkdir(parents=True, exist_ok=True)
        (d / f"{slug}.md").write_text(
            f"---\nid: {ntype}:{slug}\ntype: {ntype}\n---\n\nbody\n"
        )
    return project


def _check(project, ntype, parents, **kw):
    rules, index, _ = sg.gate_for_root(project)
    return sg.check_spawn(ntype, parents, rules=rules, type_index=index, **kw)


def test_min_by_type_approves_one_of_each(converging):
    res = _check(converging, "bigger_outcome", ["outcome:o1", "verdict:v1"])
    assert res.status == sg.APPROVED
    assert any("min_parents_by_type" in a for a in res.applied)


def test_min_by_type_rejects_right_arity_wrong_mix(converging):
    """Two outcomes satisfies min_parents: 2 and still misses the point."""
    res = _check(converging, "bigger_outcome", ["outcome:o1", "outcome:o2"])
    assert res.status == sg.REJECTED
    assert "min_parents_by_type" in res.reason
    assert "verdict" in res.reason
    # The rejection has to name the schema file and how to fix it (test #1).
    assert "[bigger_outcome].md" in res.reason
    assert "1 more 'verdict'" in res.fix


def test_min_by_type_shortfall_names_every_missing_kind(converging):
    """One outcome alone is short on verdict; min_parents catches arity first."""
    res = _check(converging, "bigger_outcome", ["outcome:o1"])
    assert res.status == sg.REJECTED
    assert "min_parents" in res.reason


def test_min_by_type_unresolvable_parent_is_unverified_not_rejected(converging):
    """A dangling parent cannot be typed, so the floor cannot be decided."""
    res = _check(converging, "bigger_outcome", ["outcome:o1", "verdict:ghost"])
    assert res.status == sg.UNVERIFIED
    assert "verdict:ghost" in res.reason


def _schema_err(project, body, fname="[bigger_outcome].md"):
    (project / "context" / "schemas" / fname).write_text(body)
    rules = sg.load_spawn_rules(project / "context" / "schemas", root=project)
    return rules, rules.schemas.get("bigger_outcome")


def test_min_by_type_requiring_a_forbidden_type_is_a_schema_error(project):
    """A floor on a type `allowed_parents` forbids can never be satisfied."""
    rules, schema = _schema_err(project, BIGGER_OUTCOME.replace(
        "allowed_parents: [outcome, verdict]", "allowed_parents: [outcome]"))
    assert schema.error
    assert "allowed_parents does not permit" in schema.error
    assert rules.schema_errors


def test_min_by_type_exceeding_max_parents_is_a_schema_error(project):
    """Floors summing above max_parents reject the type forever."""
    rules, schema = _schema_err(project, BIGGER_OUTCOME.replace(
        "min_parents_by_type: {verdict: 1, outcome: 1}",
        "min_parents_by_type: {verdict: 2, outcome: 2}"))
    assert schema.error
    assert "no node could satisfy this" in schema.error


def test_min_by_type_zero_is_a_schema_error_not_a_silent_noop(project):
    """`0` reads as a rule but enforces nothing — the exact prose-control trap."""
    rules, schema = _schema_err(project, BIGGER_OUTCOME.replace(
        "{verdict: 1, outcome: 1}", "{verdict: 0, outcome: 1}"))
    assert schema.error
    assert ">= 1" in schema.error


def test_a_broken_min_by_type_schema_is_not_enforced(converging):
    """A schema error makes the type unverified — never half-enforced."""
    (converging / "context" / "schemas" / "[bigger_outcome].md").write_text(
        BIGGER_OUTCOME.replace("min_parents_by_type: {verdict: 1, outcome: 1}",
                               "min_parents_by_type: [verdict, outcome]"))
    res = _check(converging, "bigger_outcome", ["outcome:o1", "outcome:o2"])
    assert res.status == sg.UNVERIFIED


def test_absent_min_by_type_changes_nothing(gate):
    """Every existing schema omits the field; none of them gain a floor."""
    rules, index = gate
    assert rules.schemas["verdict"].flat.min_parents_by_type == ()
    res = sg.check_spawn("verdict", ["experiment:e1"], rules=rules, type_index=index)
    assert res.status == sg.APPROVED


# --------------------------------------------------------------------------
# edge_fields — lineage vs scheduling
#
# `depends_on` orders the build; `parents` is descent. Only the second may be
# walked. The classification lives in `[shape].md` so the guard can be
# mechanical rather than remembered — an undeclared field stays traversable,
# because silently dropping an edge from a walk is the failure mode this is
# meant to prevent, not cause.
# --------------------------------------------------------------------------

SHAPE_WITH_EDGES = """\
---
name: shape
structural: true
parentless_types:
  - moral
max_parents_ceiling: 2
edge_fields:
  parents:    {role: lineage, traversable: true}
  depends_on: {role: scheduling, traversable: false}
---
shape
"""


def test_scheduling_edges_are_not_traversable(project):
    (project / "context" / "schemas" / "[shape].md").write_text(SHAPE_WITH_EDGES)
    geo = sg.load_spawn_rules(project / "context" / "schemas", root=project).geometry
    assert geo.is_traversable("parents") is True
    assert geo.is_traversable("depends_on") is False
    assert geo.scheduling_edges() == frozenset({"depends_on"})


def test_undeclared_edge_field_stays_traversable(project):
    """Fail OPEN: an unclassified edge keeps its behaviour, never loses it."""
    (project / "context" / "schemas" / "[shape].md").write_text(SHAPE_WITH_EDGES)
    geo = sg.load_spawn_rules(project / "context" / "schemas", root=project).geometry
    assert geo.is_traversable("next_edges") is True


def test_absent_edge_fields_leaves_every_edge_traversable():
    """A project with no `edge_fields:` walks exactly what it walked before.

    Uses a shape schema with NO edge_fields declared, so the gate falls back
    to traversable=true for every field.
    """
    shape_no_edges = """\
---
name: shape
structural: true
parentless_types:
  - moral
max_parents_ceiling: 2
---
shape
"""
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        sd = Path(td) / "context" / "schemas"
        sd.mkdir(parents=True)
        (sd / "[shape].md").write_text(shape_no_edges)
        rules = sg.load_spawn_rules(sd)
        assert rules.geometry.edge_fields == {}
        assert rules.geometry.scheduling_edges() == frozenset()
        assert rules.geometry.is_traversable("depends_on") is True
        assert rules.geometry.is_traversable("season_parents") is True


# --------------------------------------------------------------------------
# season_parents gate — L2 wave 2: hypothesis:l2w2-gate-season-parents
# --------------------------------------------------------------------------

VISION_SEASON = """\
---
name: vision
spawn:
  allowed_parents: [moral]
  min_parents: 1
  max_parents: 4
  min_parents_by_type: {moral: 1}
  season_parents_allowed: [overview]
---
vision
"""

OVERVIEW_SCHEMA = """\
---
name: overview
spawn:
  allowed_parents: [bigger_outcome]
  min_parents: 1
  max_parents: 4
---
overview
"""

LADDER_SEASON_1 = """\
---
id: ladder:ladder
type: ladder
current_season: 1
caps: {moral: 5, vision: 3}
tiers: []
director_rotate_at: 0.35
---
ladder
"""

LADDER_SEASON_2 = """\
---
id: ladder:ladder
type: ladder
current_season: 2
caps: {moral: 5, vision: 3}
tiers: []
director_rotate_at: 0.35
---
ladder
"""


@pytest.fixture
def season_project(project, request):
    """`project`, plus a [vision].md schema with season_parents_allowed,
    an [overview].md schema, a ladder node, an overview node, a moral node,
    and a bigger_outcome node. Raises the max_parents_ceiling to 4 so
    vision's max_parents: 4 passes."""
    sd = project / "context" / "schemas"
    (sd / "[vision].md").write_text(VISION_SEASON)
    (sd / "[overview].md").write_text(OVERVIEW_SCHEMA)
    # Raise ceiling to 4 so vision's max_parents: 4 passes
    (sd / "[shape].md").write_text(SHAPE.replace("max_parents_ceiling: 2",
                                                    "max_parents_ceiling: 4"))
    # ladder
    gd = project / "nodes" / ".geometry"
    gd.mkdir(parents=True, exist_ok=True)
    season = getattr(request, "param", 1)
    ladder_body = LADDER_SEASON_2 if season == 2 else LADDER_SEASON_1
    (gd / "ladder.md").write_text(ladder_body)
    # overview node (season 2)
    nd = project / "nodes"
    for ntype, slug, extra in [
        ("overview", "o1", "season: 2"),
        ("bigger_outcome", "bo1", ""),
        ("moral", "faith", ""),
    ]:
        d = nd / ntype
        d.mkdir(parents=True, exist_ok=True)
        body = f"---\nid: {ntype}:{slug}\ntype: {ntype}\n{extra}\n---\n\nb\n"
        (d / f"{slug}.md").write_text(body)
    return project


def test_season_parents_allowed_is_parsed_correctly():
    """season_parents_allowed is parsed from the schema and stored on Rule."""
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        sd = Path(td) / "context" / "schemas"
        sd.mkdir(parents=True)
        (sd / "[shape].md").write_text(SHAPE)
        (sd / "[vision].md").write_text(VISION_SEASON)
        rules = sg.load_spawn_rules(sd, root=Path(td))
        vision = rules.schemas.get("vision")
        assert vision is not None, "vision schema not loaded"
        assert vision.flat is not None, "vision has no flat rule"
        assert vision.flat.season_parents_allowed == frozenset({"overview"})


def test_type_with_no_season_parents_allowed_refuses_entries(season_project):
    """A type that does not declare season_parents_allowed rejects any
    season_parents entries."""
    rules, index, cs = sg.gate_for_root(season_project)
    res = sg.check_spawn(
        "verdict", ["experiment:e1"], rules=rules, type_index=index,
        season_parents=["overview:o1"], current_season=cs,
        fm={"season": 2},
    )
    assert res.status == sg.REJECTED
    assert "season_parents_allowed" in res.reason


def test_vision_valid_season_parents_pass(season_project):
    """Vision with season_parents [overview:x] where x exists passes."""
    rules, index, cs = sg.gate_for_root(season_project)
    res = sg.check_spawn(
        "vision", ["moral:faith"], rules=rules, type_index=index,
        season_parents=["overview:o1"], current_season=cs,
        fm={"season": 2},
    )
    assert res.status == sg.APPROVED, f"failed: {res.reason}"
    assert any("season_parents_allowed" in a for a in res.applied)


def test_vision_wrong_season_parent_type_is_rejected(season_project):
    """Vision with season_parents [bigger_outcome:x] where x exists refuses."""
    rules, index, cs = sg.gate_for_root(season_project)
    res = sg.check_spawn(
        "vision", ["moral:faith"], rules=rules, type_index=index,
        season_parents=["bigger_outcome:bo1"], current_season=cs,
        fm={"season": 2},
    )
    assert res.status == sg.REJECTED
    assert "season_parents_allowed" in res.reason
    assert "bigger_outcome" in res.reason


def test_vision_missing_season_parent_is_unverified(season_project):
    """Vision with season_parents pointing to a nonexistent node is UNVERIFIED."""
    rules, index, cs = sg.gate_for_root(season_project)
    res = sg.check_spawn(
        "vision", ["moral:faith"], rules=rules, type_index=index,
        season_parents=["overview:nonexistent"], current_season=cs,
        fm={"season": 2},
    )
    assert res.status == sg.UNVERIFIED
    assert "nonexistent" in res.reason


def test_season_parents_grandfathered_when_season_lower(season_project):
    """A node with season < current_season skips the season_parents check."""
    rules, index, cs = sg.gate_for_root(season_project)
    res = sg.check_spawn(
        "vision", ["moral:faith"], rules=rules, type_index=index,
        season_parents=["overview:nonexistent"], current_season=2,
        fm={"season": 1},
    )
    assert res.status == sg.APPROVED, f"not grandfathered: {res.reason}"
    assert any("grandfathered" in a for a in res.applied)


def test_season_parents_grandfathered_no_season_at_season_1(season_project):
    """A node with no season field at current_season=1 is grandfathered."""
    rules, index, cs = sg.gate_for_root(season_project)
    res = sg.check_spawn(
        "vision", ["moral:faith"], rules=rules, type_index=index,
        season_parents=["overview:nonexistent"], current_season=1,
    )
    assert res.status == sg.APPROVED, f"not grandfathered: {res.reason}"
    assert any("grandfathered" in a for a in res.applied)


def test_no_ladder_skips_season_parents_check(season_project):
    """When the ladder node is missing, current_season is None: no
    grandfathering applies, the type check still runs, and a missing
    season_parent is UNVERIFIED (write, warn) rather than rejected."""
    (season_project / "nodes" / ".geometry" / "ladder.md").unlink()
    rules, index, cs = sg.gate_for_root(season_project)
    assert cs is None, f"expected None, got {cs}"
    res = sg.check_spawn(
        "vision", ["moral:faith"], rules=rules, type_index=index,
        season_parents=["overview:nonexistent"], current_season=cs,
        fm={"season": 2},
    )
    assert res.status == sg.UNVERIFIED
    assert res.ok  # UNVERIFIED still writes


def test_current_season_read_from_ladder(season_project):
    """gate_for_root reads current_season from ladder.md."""
    rules, index, cs = sg.gate_for_root(season_project)
    assert cs == 1, f"expected 1, got {cs}"


def test_season_parents_check_skipped_when_rule_has_none(season_project):
    """If rule has empty season_parents_allowed and season_parents is None,
    no check runs."""
    rules, index, cs = sg.gate_for_root(season_project)
    res = sg.check_spawn(
        "verdict", ["experiment:e1"], rules=rules, type_index=index,
        current_season=cs,
    )
    assert res.status == sg.APPROVED


def test_node_writer_rejects_wrong_season_parent_type(season_project):
    """The creation path enforces season_parents, not just check_spawn.
    Red before node_writer passed season_parents/current_season to
    check_spawn: write_node let a wrong-type season_parent through."""
    import node_writer
    res = node_writer.write_node(
        season_project, "vision", "seasoned-bad", ["moral:faith"],
        extra_fm={"season": 2, "season_parents": ["bigger_outcome:bo1"]},
        body="b\n",
    )
    assert res.rejected, (
        f"expected rejection, gate={getattr(res.gate, 'status', None)}")
    assert "season_parents_allowed" in (res.reason or "")
    assert not (season_project / "nodes" / "vision" / "seasoned-bad.md").exists()


def test_node_writer_accepts_valid_season_parent(season_project):
    """A vision node whose season_parent resolves to an existing overview
    writes through the gate."""
    import node_writer
    res = node_writer.write_node(
        season_project, "vision", "seasoned-good", ["moral:faith"],
        extra_fm={"season": 2, "season_parents": ["overview:o1"]},
        body="b\n",
    )
    assert not res.rejected, res.reason
    assert (season_project / "nodes" / "vision" / "seasoned-good.md").exists()
