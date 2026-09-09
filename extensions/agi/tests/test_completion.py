"""Tests for the harness-blind completion check — bin/completion.py.

mvp:unified-spawn-path clause 5: the finish signal is the scaffolded node
acquiring real content — a graph event, observable identically on every
harness. These tests are the falsifiers the hypothesis aimed at:

  F4  a kid that wrote its node and was killed before `cli.py done` is still
      complete, with no pid and no agent.json anywhere;
      the inverse too — a `done` record on an untouched scaffold is not
      completion, because the process state is not the signal.
  F2  no harness-keyed branch in the completion path (AST check over the
      code, docstrings excluded), and `post_wire._gate` reading the node's
      own frontmatter before the agent record.

The scaffold-hash variant is the fallback the hypothesis named in case plain
body comparison proved ambiguous: a template change must not make an
untouched scaffold look filled, so the placeholder's identity is captured at
write time (the `scaffold_hash:` stamp `node_writer` now mints).
"""

import ast
import importlib.util
import json
import sys
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parents[1] / "bin"


def _load(name):
    path = BIN / f"{name}.py"
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


comp = _load("completion")
nw = comp.node_writer
pw = _load("post_wire")

SHAPE = """\
---
name: shape
structural: true
parentless_types:
  - idea
max_parents_ceiling: 2
canonical_type_spelling: underscore
---
shape
"""

SCHEMAS = {
    "[idea].md": "allowed_parents: [goal]\n  min_parents: 0\n  max_parents: 1",
    "[hypothesis].md": "allowed_parents: [idea, hypothesis, experiment]\n  min_parents: 1\n  max_parents: 2",
    "[experiment].md": "allowed_parents: [hypothesis, idea]\n  min_parents: 1\n  max_parents: 2",
}


@pytest.fixture
def project(tmp_path):
    """A throwaway graph repo: schemas plus an idea -> hypothesis -> chain."""
    (tmp_path / "agi-tree.config.json").write_text("{}")
    sd = tmp_path / "context" / "schemas"
    sd.mkdir(parents=True)
    (sd / "[shape].md").write_text(SHAPE)
    for fname, spawn in SCHEMAS.items():
        name = fname[1:-4]
        (sd / fname).write_text(f"---\nname: {name}\nspawn:\n  {spawn}\n---\n{name}\n")
    nd = tmp_path / "nodes"
    for ntype, slug in [("idea", "i1"), ("hypothesis", "h1")]:
        d = nd / ntype
        d.mkdir(parents=True, exist_ok=True)
        (d / f"{slug}.md").write_text(f"---\nid: {ntype}:{slug}\ntype: {ntype}\n---\n\nbody\n")
    return tmp_path


def _scaffold(project, slug="exp1", parent="hypothesis:h1"):
    """One real node through the one writer, so the stamp is real too."""
    res = nw.write_node(project, "experiment", slug, [parent])
    assert res.written, res.reason
    return res


def _fm(path):
    import yaml
    return yaml.safe_load(path.read_text().split("---", 2)[1])


def _fill(path, body):
    """A kid filling its scaffold: the body changes, nothing else does."""
    parts = path.read_text().split("---", 2)
    path.write_text(f"---\n{parts[1]}---\n{body}")


def _agent_done(iter_dir, agent_id, node_id):
    """The pi-process record a kid leaves when it did run `cli.py done`."""
    d = iter_dir / agent_id
    d.mkdir(parents=True, exist_ok=True)
    (d / "agent.json").write_text(json.dumps(
        {"id": agent_id, "status": "done", "node_id": node_id,
         "verdict": "inconclusive_lean_proved:65"}))
    (iter_dir / "manifest.json").write_text(json.dumps(
        {"timeout_seconds": 600,
         "agents": [{"id": agent_id, "status": "done"}]}))


# --------------------------------------------------------------------------
# the stamp
# --------------------------------------------------------------------------

def test_writer_stamps_the_scaffold_identity(project):
    res = _scaffold(project)
    fm = _fm(res.path)
    expected = nw.scaffold_hash(
        nw.BODY_BEGIN + f"\n# {res.node_id}\n\n" + nw.BODY_PROMPTS["experiment"])
    assert fm["scaffold_hash"] == expected


# --------------------------------------------------------------------------
# F4 — completion is the node's content, not the process
# --------------------------------------------------------------------------

def test_untouched_scaffold_is_not_complete(project):
    res = _scaffold(project)
    assert comp.is_complete(project, res.node_id) is False


def test_killed_after_writing_is_complete(project):
    """Falsifier 4. Node filled, no `done`, no pid, no session at all."""
    res = _scaffold(project)
    _fill(res.path, "\n# experiment:exp1\n\nRan the thing. It works. See output.\n")
    assert comp.is_complete(project, res.node_id) is True


def test_done_on_untouched_scaffold_is_not_complete(project):
    """The inverse: a report of done does not complete an empty node."""
    res = _scaffold(project)
    _agent_done(project / "sessions" / "iter-001", "kid1", res.node_id)
    assert comp.is_complete(project, res.node_id) is False


def test_completion_does_not_depend_on_which_report_path_existed(project):
    """Same node state, two report histories — the answer is the same."""
    a = _scaffold(project, "expa")
    b = _scaffold(project, "expb", )
    for r in (a, b):
        _fill(r.path, f"\n# {r.node_id}\n\nFilled in for real.\n")
    _agent_done(project / "sessions" / "iter-001", "kid-b", b.node_id)
    assert comp.is_complete(project, a.node_id)
    assert comp.is_complete(project, b.node_id)


def test_missing_node_is_not_complete(project):
    assert comp.is_complete(project, "experiment:never-minted") is False


# --------------------------------------------------------------------------
# the weak joint — template drift
# --------------------------------------------------------------------------

def test_template_drift_keeps_untouched_scaffold_incomplete(project, monkeypatch):
    """BODY_PROMPTS changes after the write; the stamp was captured then."""
    res = _scaffold(project)
    monkeypatch.setitem(nw.BODY_PROMPTS, "experiment", "## New placeholder\n\n")
    assert comp.is_complete(project, res.node_id) is False
    _fill(res.path, "\n# experiment:exp1\n\nReal content.\n")
    assert comp.is_complete(project, res.node_id) is True


def test_legacy_node_without_stamp_uses_current_placeholder(project):
    """Nodes scaffolded before the field existed still resolve, both ways."""
    d = project / "nodes" / "experiment"
    d.mkdir(parents=True, exist_ok=True)
    nid = "experiment:legacy"
    p = d / "legacy.md"
    p.write_text(
        f"---\nid: {nid}\nmint_id: deadbeef\ntype: experiment\n"
        f"parents:\n  - hypothesis:h1\n---\n"
        f"# {nid}\n\n{nw.BODY_PROMPTS['experiment']}")
    assert comp.is_complete(project, nid) is False
    _fill(p, f"\n# {nid}\n\nContent written by a pre-stamp loop.\n")
    assert comp.is_complete(project, nid) is True


# --------------------------------------------------------------------------
# F2 — no harness in the completion path
# --------------------------------------------------------------------------

def _code_tokens(src):
    """Names, attributes and non-docstring strings in `src` — the code, not
    the prose. A docstring may name a harness it is replacing; a branch may
    not."""
    tree = ast.parse(src)
    for node in list(ast.walk(tree)):
        if isinstance(node, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef)):
            if (node.body
                    and isinstance(node.body[0], ast.Expr)
                    and isinstance(node.body[0].value, ast.Constant)
                    and isinstance(node.body[0].value.value, str)):
                node.body = node.body[1:]
    out = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            out.append(node.value)
        elif isinstance(node, ast.Name):
            out.append(node.id)
        elif isinstance(node, ast.Attribute):
            out.append(node.attr)
    return " ".join(out)


def test_completion_code_names_no_harness_and_no_process_state():
    toks = _code_tokens((BIN / "completion.py").read_text(encoding="utf-8")).lower()
    for bad in ("claude", "pi", "agent.json", "manifest", "pid", "heal"):
        assert bad not in toks, f"'{bad}' in completion.py code: {toks}"


def test_post_wire_gate_reads_the_node_before_the_record():
    # The node's own stamp wins over a more aggressive agent-record claim.
    agent = {"verdict": "proved", "evidence_runs": []}
    fm = {"verdict": "inconclusive_lean_proved:65", "evidence_runs": []}
    res = pw._gate(agent, fm, frozenset())
    assert res.verdict == "inconclusive_lean_proved:65"
    # A scaffold carries no verdict key, so an unreported kid still lands
    # where the old path landed: pending, from the record or from neither.
    assert pw._gate({"verdict": "pending"}, {}, frozenset()).verdict == "pending"
    assert pw._gate({}, {}, frozenset()).verdict == "pending"


# --------------------------------------------------------------------------
# F4 at LOOP level — the wiring, not just the function
#
# The function passing is not the claim. `verdict:a00-ad1d7097-fc613c` ratified
# the experiment at 65 precisely because `is_complete` had zero callers, and
# named the one thing that would move it: the loop must count a killed-but-
# filled kid as done end-to-end. These two tests are that.
# --------------------------------------------------------------------------


def _wire_failed_agent(project, agent_id, node_id, status="failed"):
    """The record a kid leaves when the PROCESS model gave up on it.

    `heal.py` stamps exactly this after a pid vanishes with no completion
    signal, and `cmd_wire` used to skip it outright. No `cli.py done` ever ran,
    so there is no verdict anywhere but the node itself.
    """
    iter_dir = project / "sessions" / "iter-001"
    (iter_dir / agent_id).mkdir(parents=True, exist_ok=True)
    (iter_dir / agent_id / "agent.json").write_text(json.dumps(
        {"id": agent_id, "status": status, "node_id": node_id,
         "fail_reason": "pid disappeared without completion signal"}))
    (iter_dir / "manifest.json").write_text(json.dumps(
        {"timeout_seconds": 600,
         "agents": [{"id": agent_id, "status": status, "node_id": node_id,
                     "parent": "hypothesis:h1"}]}))
    import argparse
    return pw.cmd_wire(argparse.Namespace(iter_n=1, project_root=None))


def test_failed_kid_with_a_filled_node_is_wired_anyway(project, monkeypatch):
    """MVP falsifier 4, end to end.

    This is the 2026-09-01 loss reproduced: the kid that wrote `completion.py`
    died on a provider 403 straight after, `heal.py` marked it failed, and
    `post_wire` reported `nodes updated: 0` over a node that was complete on
    disk. The work survived only because it also touched source files.
    """
    res = _scaffold(project)
    _fill(res.path, "\n# experiment:exp1\n\nReal measured content.\n")
    monkeypatch.chdir(project)
    _wire_failed_agent(project, "a00-dead", res.node_id)
    assert _fm(res.path).get("wired_from") == "a00-dead"


def test_failed_kid_with_an_untouched_scaffold_is_not_wired(project, monkeypatch):
    """The inverse, and the reason this is not just `status != failed`.

    A kid that died having written nothing must stay unwired — otherwise the
    check would launder every crash into a finished node.
    """
    res = _scaffold(project)
    monkeypatch.chdir(project)
    _wire_failed_agent(project, "a00-dead", res.node_id)
    assert "wired_from" not in _fm(res.path)


# --------------------------------------------------------------------------
# Agent Notes land ONCE — two writers, one section
#
# `cli.py done` wrote the notes bare and `post_wire` appended them under a
# heading; both run on every kid, so every node carried the text twice. The kid
# contract blamed kids for it by name and by count. No kid was doing it.
# --------------------------------------------------------------------------


def test_notes_land_once_even_when_both_writers_run(project, monkeypatch):
    res = _scaffold(project)
    _fill(res.path, "\n# experiment:exp1\n\nReal content.\n")
    monkeypatch.chdir(project)
    notes = "one line of agent notes"

    # post_wire, twice — re-wiring must not accumulate sections either.
    for _ in range(2):
        iter_dir = project / "sessions" / "iter-001"
        (iter_dir / "a1").mkdir(parents=True, exist_ok=True)
        (iter_dir / "a1" / "agent.json").write_text(json.dumps(
            {"id": "a1", "status": "done", "node_id": res.node_id,
             "notes": notes, "verdict": "pending"}))
        (iter_dir / "manifest.json").write_text(json.dumps(
            {"timeout_seconds": 600, "agents": [
                {"id": "a1", "status": "done", "node_id": res.node_id,
                 "parent": "hypothesis:h1", "notes": notes}]}))
        import argparse
        pw.cmd_wire(argparse.Namespace(iter_n=1, project_root=None))

    text = res.path.read_text()
    assert text.count("## Agent Notes") == 1, text
    assert text.count(notes) == 1, text


# --------------------------------------------------------------------------
# `_gate` precedence — the two ways frontmatter-primary went wrong
# --------------------------------------------------------------------------


def test_rewire_does_not_demote_an_earned_proved():
    """`stamp` writes back a COUNT; the gate needs the LIST.

    Second wire sees `evidence_runs: 1`, an int, which goal:g7.3 resolves to
    zero evidence on purpose — so preferring it over the agent's list turned a
    legitimately proved node into `inconclusive_lean_proved:50` on every
    re-wire.
    """
    corpus = frozenset(["experiment:e1"])
    agent = {"verdict": "proved", "evidence_runs": ["experiment:e1"]}
    first = pw._gate(agent, {"verdict": "pending"}, corpus)
    assert first.verdict == "proved", first.verdict
    # what the node looks like after stamp(): verdict set, runs a bare count
    rewire = pw._gate(agent, {"verdict": "proved", "evidence_runs": 1}, corpus)
    assert rewire.verdict == "proved", rewire.verdict
    assert not rewire.demoted


def test_pending_in_the_node_does_not_outrank_a_reported_verdict():
    """`pending` is the absence of a claim, not a claim."""
    corpus = frozenset(["experiment:e1"])
    agent = {"verdict": "proved", "evidence_runs": ["experiment:e1"]}
    assert pw._gate(agent, {"verdict": "pending"}, corpus).verdict == "proved"
    # a real claim in the node still wins over the agent record
    fm = {"verdict": "inconclusive_lean_proved:65", "evidence_runs": []}
    assert pw._gate(agent, fm, corpus).verdict == "inconclusive_lean_proved:65"


def test_malformed_frontmatter_is_not_complete_and_does_not_raise(project):
    """A predicate must answer, not explode.

    `post_wire.cmd_wire` calls `is_complete` inside its agent loop, so a raise
    here loses the whole iteration's wiring rather than one node. Unreachable
    until this module acquired its first caller on 2026-09-01.
    """
    d = project / "nodes" / "experiment"
    d.mkdir(parents=True, exist_ok=True)
    p = d / "bad.md"
    p.write_text("---\nfoo: [unclosed\n---\n\nreal looking body\n")
    assert comp.is_complete(project, "experiment:bad") is False


# --------------------------------------------------------------------------
# Malformed nodes: skip with report, never write back
# --------------------------------------------------------------------------


def test_malformed_node_is_never_rewritten(project, monkeypatch):
    """The corruption case, verified 2026-09-01 and now prevented.

    Reading `{}` + the whole file and writing that back re-headered the node
    with a FRESHLY MINTED `mint_id` and demoted the real one into the body —
    inventing an identity and orphaning the node's grid ref.
    """
    d = project / "nodes" / "experiment"
    d.mkdir(parents=True, exist_ok=True)
    p = d / "e1.md"
    original = "---\nid: experiment:e1\nmint_id: deadbeef\ntype: experiment\nbody\n"
    p.write_text(original)          # frontmatter opened, never closed
    monkeypatch.chdir(project)
    _wire_failed_agent(project, "a1", "experiment:e1", status="done")
    assert p.read_text() == original, "malformed node was rewritten"


def test_both_malformed_shapes_raise_one_catchable_class():
    """`raise` is ONE class — a caller writes a single `except`."""
    for bad in ("---\nfoo: [unclosed\nbody\n",          # never closed
                "---\nfoo: [unclosed\n---\nbody\n",     # closed, bad YAML
                "---\n- a\n- b\n---\nbody\n"):          # parses, not a mapping
        with pytest.raises(pw.MalformedNode):
            pw._read_frontmatter(bad)
    # a file with no frontmatter at all is legitimate, not malformed
    fm, body = pw._read_frontmatter("just text\n")
    assert fm == {} and body == "just text\n"
