"""goal:g13.1 — edit mode's verb layer.

The two invariants worth testing are the two the goal states in bold:

- **Edit mode must not become a second way to write.** There is no file write
  in `write.py`; every verb ends in `node_writer.update_node`. Asserted by
  parsing the module, not by grepping it — a `grep` for a concept cannot tell
  prose from code, which this session already learned once.
- **A keystroke an agent cannot spell is a verb that exists only for humans.**
  The named set and the `&&`-serialised form must run the identical
  operations, which is `goal:g9.7`'s argument applied to writing.
"""
from __future__ import annotations

import ast
import sys
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parent.parent / "bin"
SRC = Path(__file__).resolve().parent.parent / "src"
sys.path.insert(0, str(BIN))
sys.path.insert(0, str(SRC))

import write  # noqa: E402
import node_writer  # noqa: E402

THOUGHT = ("<!-- THOUGHT:BEGIN — authored, not derived; carried across "
           "regenerating scans. The reasoning behind THIS version. -->\n"
           "the old reason\n<!-- THOUGHT:END -->")


@pytest.fixture()
def project(tmp_path: Path) -> Path:
    graph = tmp_path / ".agi"
    (graph / "nodes" / "hypothesis").mkdir(parents=True)
    (graph / "config.json").write_text("{}")
    (graph / "nodes" / "hypothesis" / "h1.md").write_text(
        '---\nid: "hypothesis:h1"\ntype: hypothesis\nmint_id: abc123\n'
        'title: "t"\ntestable_claim: "c"\nscaffold_hash: deadbeef\n'
        'status: pending\n---\n\nthe body\n\n' + THOUGHT + "\n")
    return graph


# --------------------------------------------------------------------------
# Not a second way to write
# --------------------------------------------------------------------------

def test_edit_py_contains_no_file_write(project):
    """Every verb ends in `update_node`. If a change can be made here that
    `write.py` cannot make, edit mode is a bypass, not a front end."""
    tree = ast.parse((BIN / "write.py").read_text())
    banned = {"write_text", "write_bytes", "writelines", "replace", "rename"}
    offenders = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            if node.func.attr in banned and node.func.attr != "replace":
                offenders.append((node.lineno, node.func.attr))
            # `str.replace` is fine; `os.replace` is a write.
            if node.func.attr == "replace" and isinstance(node.func.value, ast.Name) \
                    and node.func.value.id == "os":
                offenders.append((node.lineno, "os.replace"))
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) \
                and node.func.id == "open":
            offenders.append((node.lineno, "open"))
    assert offenders == [], f"write.py writes files directly: {offenders}"


def test_identity_and_completion_fields_are_refused(project):
    """A mint id is assigned once (`goal:g2.5`); `scaffold_hash` is how
    completion is detected, and edit mode is not a loophole in the rule the
    kid brief already follows."""
    e = write.Edit("hypothesis:h1")
    for key in ("id", "mint_id", "type", "scaffold_hash"):
        with pytest.raises(write.EditError):
            write.verb_set(e, key, "anything")
        with pytest.raises(write.EditError):
            write.verb_unset(e, key)


# --------------------------------------------------------------------------
# The two callers run the identical operations
# --------------------------------------------------------------------------

def test_the_serialised_form_and_the_verb_calls_produce_the_same_edit():
    """`goal:g9.7`'s argument applied to writing: the human path and the
    agent path are the same operations with the interaction removed."""
    by_hand = write.Edit("hypothesis:h1")
    write.verb_set(by_hand, "status", "active")
    write.verb_link(by_hand, "self")
    write.verb_thought(by_hand, "why")

    scripted = write.Edit("hypothesis:h1")
    for name, args in write.parse_script("set status active && link self && thought why"):
        write.apply_verb(scripted, name, args)

    assert scripted == by_hand


def test_every_verb_is_nameable_from_a_command_line():
    """A keystroke an agent cannot spell is a verb that exists only for
    humans."""
    for name in write.VERBS:
        assert name.isidentifier() or "-" in name
        assert name == name.lower()


def test_values_are_coerced_because_frontmatter_is_typed():
    """A command line hands over strings; a schema's `types:` block will
    reject `confidence: "0.9"`."""
    assert write._coerce("0.9") == 0.9
    assert write._coerce("3") == 3
    assert write._coerce("true") is True
    assert write._coerce("[a, b]") == ["a", "b"]
    assert write._coerce("[]") == []
    assert write._coerce("active") == "active"


# --------------------------------------------------------------------------
# Submit
# --------------------------------------------------------------------------

def test_submit_records_who_made_the_edit(project):
    """Provenance is the payoff. An edit mode that produces an untraceable
    change has delivered the convenience and none of the reason."""
    e = write.Edit("hypothesis:h1")
    write.verb_set(e, "status", "active")
    res = write.submit(project, e, actor="liborum", session="sess-42")

    assert res.status == node_writer.UPDATED
    text = (project / "nodes/hypothesis/h1.md").read_text()
    assert "edited_by: liborum" in text
    assert "thought_session: sess-42" in text


def test_a_thought_verb_replaces_the_region_it_does_not_accumulate(project):
    """The thought says why THIS version differs from the previous one."""
    e = write.Edit("hypothesis:h1")
    write.verb_thought(e, "the new reason")
    write.submit(project, e, actor="t")

    text = (project / "nodes/hypothesis/h1.md").read_text()
    assert "the new reason" in text
    assert "the old reason" not in text
    assert text.count("THOUGHT:BEGIN") == 1


def test_a_frontmatter_only_edit_leaves_the_thought_alone(project):
    """Absent means empty: a caller that passes no thought must not clear one."""
    e = write.Edit("hypothesis:h1")
    write.verb_set(e, "status", "active")
    write.submit(project, e, actor="t")
    assert "the old reason" in (project / "nodes/hypothesis/h1.md").read_text()


def test_a_note_appends_under_the_shared_heading_and_is_idempotent(project):
    for _ in range(2):
        e = write.Edit("hypothesis:h1")
        write.verb_note(e, "an observation")
        write.submit(project, e, actor="t")
    text = (project / "nodes/hypothesis/h1.md").read_text()
    assert text.count("## Agent Notes") == 1
    assert text.count("an observation") == 1


def test_submitting_nothing_is_an_error_not_a_silent_no_op(project):
    with pytest.raises(write.EditError, match="nothing to submit"):
        write.submit(project, write.Edit("hypothesis:h1"), actor="t")


def test_an_unknown_verb_names_the_known_ones(project):
    with pytest.raises(write.EditError) as exc:
        write.apply_verb(write.Edit("hypothesis:h1"), "frobnicate", [])
    assert "set" in str(exc.value) and "link" in str(exc.value)


def test_a_prose_verb_takes_a_whole_sentence(project):
    """Found by dogfooding on the first real use.

    `parse_script` originally split every chunk with `maxsplit=2` — right for
    `set k v`, wrong for everything else: `note some prose here` arrived as
    three arguments to a two-argument verb and errored. A fixed split is a
    parser that assumes every verb has the same shape.
    """
    calls = write.parse_script("note this is a whole sentence, with commas")
    assert calls == [("note", ["this is a whole sentence, with commas"])]

    calls = write.parse_script("set confidence 0.9 && thought why it changed now")
    assert calls == [("set", ["confidence", "0.9"]),
                     ("thought", ["why it changed now"])]


def test_every_verb_declares_its_arity():
    """A verb with no declared arity would silently get 1, which is the right
    default and the wrong thing to rely on."""
    assert set(write.ARITY) == set(write.VERBS)


def test_a_note_appends_under_an_existing_heading_rather_than_adding_a_second(project):
    """Found on the first real use, against a live node.

    `post_wire` and `cli.py done` both already write `## Agent Notes`. The
    first version of the idempotency check tested only whether the TEXT was
    present, so a node that already had the section got a second heading.
    """
    path = project / "nodes" / "hypothesis" / "h1.md"
    path.write_text(path.read_text().rstrip()
                    + "\n\n## Agent Notes\nan earlier note\n")

    e = write.Edit("hypothesis:h1")
    write.verb_note(e, "a later note")
    write.submit(project, e, actor="t")

    text = path.read_text()
    assert text.count("## Agent Notes") == 1, "a second heading was added"
    assert "an earlier note" in text and "a later note" in text


# --------------------------------------------------------------------------
# L1.07 — `create`: the half that was missing when `edit` became `write`
# --------------------------------------------------------------------------

def _schemas(graph: Path):
    """Minimal schema set so the spawn gate has rules to enforce."""
    d = graph / "context" / "schemas"
    d.mkdir(parents=True, exist_ok=True)
    (d / "[hypothesis].md").write_text(
        "---\nname: hypothesis\nvalidation:\n  required: [id, type, mint_id]\n"
        "spawn:\n  allowed_parents: [goal, idea]\n  min_parents: 1\n"
        "  max_parents: 2\n---\n\nbody\n")
    (d / "[experiment].md").write_text(
        "---\nname: experiment\nvalidation:\n  required: [id, type, mint_id]\n"
        "spawn:\n  allowed_parents: [hypothesis]\n  min_parents: 1\n"
        "  max_parents: 1\n---\n\nbody\n")
    (graph / "nodes" / "goal").mkdir(parents=True, exist_ok=True)
    (graph / "nodes" / "goal" / "g1.md").write_text(
        '---\nid: "goal:g1"\ntype: goal\nmint_id: g1mint\ntitle: "G"\n'
        'status: active\n---\n\nbody\n')
    return d


def test_create_mints_a_node_through_the_gate(project):
    _schemas(project)
    res, made = write.create(project, "hypothesis", "new-one", ["goal:g1"])
    assert res.written and not res.rejected
    assert made is None, "no payload was asked for"
    text = Path(res.path).read_text()
    assert "hypothesis:new-one" in text
    assert "mint_id:" in text, "creation must mint an id (goal:s14)"


def test_create_is_refused_by_the_spawn_gate_like_any_other_spawn(project):
    """🔴 A second creation path that skipped the gate would be a bypass
    wearing the name of a front end — the same thing `submit` refuses to be
    on the update side."""
    _schemas(project)
    res, made = write.create(project, "experiment", "bad", ["goal:g1"])
    assert res.rejected, "experiment may not be parented by a goal"
    assert made is None
    assert not (project / "nodes" / "experiment" / "bad.md").exists(), (
        "a rejected spawn must leave no node behind")


def test_create_makes_the_payload_file_and_links_it(project, tmp_path):
    _schemas(project)
    res, made = write.create(project, "hypothesis", "with-payload", ["goal:g1"],
                             payload="src/brand_new.py")
    assert res.written
    assert made is not None and made.exists(), "the source file was not created"
    assert "brand_new.py" in Path(res.path).read_text()


def test_create_never_overwrites_an_existing_payload(project, tmp_path):
    _schemas(project)
    existing = tmp_path / "src" / "already.py"
    existing.parent.mkdir(parents=True, exist_ok=True)
    existing.write_text("# precious\n")
    res, made = write.create(project, "hypothesis", "links-existing", ["goal:g1"],
                             payload="src/already.py")
    assert res.written
    assert made is None, "an existing file is linked, never re-created"
    assert existing.read_text() == "# precious\n"


def test_a_rejected_create_cleans_up_the_file_it_made(project, tmp_path):
    """Otherwise a rejection leaves an empty source file with no node behind
    it — precisely the gitignored staging window `goal:g11` removed."""
    _schemas(project)
    res, made = write.create(project, "experiment", "doomed", ["goal:g1"],
                             payload="src/orphan.py")
    assert res.rejected
    assert made is None
    assert not (tmp_path / "src" / "orphan.py").exists(), (
        "a rejected spawn left an orphaned source file")


def test_a_created_node_carries_the_same_provenance_as_an_edited_one(project):
    _schemas(project)
    res, _ = write.create(project, "hypothesis", "provenanced", ["goal:g1"],
                          actor="director", session="L1.07")
    text = Path(res.path).read_text()
    assert "edited_by: director" in text
    assert "thought_session: L1.07" in text
