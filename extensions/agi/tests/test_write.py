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


def test_coerce_parses_nested_json_list_and_object():
    """hypothesis:l3-write-set-nested-json — a value that starts with `[` or
    `{` shall be parsed as JSON, so a nested rows table can be written through
    write.py. Comma-splitting a JSON array of objects produced garbage string
    rows (L3.01). The JSON parse runs first; the legacy `[a, b]` comma-split
    survives as a fallback for the non-JSON spelling, which is why `[a, b]`
    still coerces to `["a", "b"]`."""
    rows = ('[{"tier": 3, "role": "prime_director", "harness": '
            '"claude-code"}, {"tier": 1, "role": "parent"}]')
    got = write._coerce(rows)
    assert isinstance(got, list) and len(got) == 2
    assert all(isinstance(r, dict) for r in got)
    assert got[0] == {"tier": 3, "role": "prime_director",
                      "harness": "claude-code"}
    assert got[1] == {"tier": 1, "role": "parent"}
    # a bare JSON object already parses; keep it\.
    assert write._coerce('{"a": 1, "b": [true, null]}') == {
        "a": 1, "b": [True, None]}


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


# --------------------------------------------------------------------------
# `payload` — the bytes behind a build node (goal:g13.1)
# --------------------------------------------------------------------------

def _build_node(project: Path, ref: str = "src/thing.py") -> None:
    (project / "nodes" / "build").mkdir(parents=True, exist_ok=True)
    (project / "nodes" / "build" / "b1.md").write_text(
        '---\nid: "build:b1"\ntype: build\nmint_id: bbb111\n'
        'title: "t"\nbuild_kind: code\norigin: build-scan\n'
        f'payload_ref: {ref}\n---\n\nthe body\n')


def test_payload_verb_replaces_the_bytes_the_node_points_at(project, tmp_path):
    _build_node(project)
    dest = tmp_path / "src" / "thing.py"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text("old\n")
    src = tmp_path / "new.py"
    src.write_text("new\n")

    edit = write.Edit("build:b1")
    write.apply_verb(edit, "payload", [str(src)])
    write.apply_verb(edit, "thought", ["why it changed"])
    write.submit(project, edit, actor="director", session="L1.13")

    assert dest.read_text() == "new\n"
    node = (project / "nodes" / "build" / "b1.md").read_text()
    assert "edited_by: director" in node
    assert "why it changed" in node, "the bytes landed but the reason did not"


def test_payload_preserves_the_destination_mode(project, tmp_path):
    """A dropped exec bit is `goal:s9` again, and the grid reads the real
    mode from lstat -- so replacing a script's bytes must not disarm it."""
    _build_node(project, ref="src/run.sh")
    dest = tmp_path / "src" / "run.sh"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text("#!/bin/sh\necho old\n")
    dest.chmod(0o755)
    src = tmp_path / "new.sh"
    src.write_text("#!/bin/sh\necho new\n")

    edit = write.apply_verb(write.Edit("build:b1"), "payload", [str(src)])
    write.submit(project, edit, actor="director")
    assert dest.read_text().endswith("echo new\n")
    assert dest.stat().st_mode & 0o111, "the exec bit was dropped"


def test_payload_refuses_a_node_that_points_at_nothing(project, tmp_path):
    edit = write.apply_verb(write.Edit("hypothesis:h1"), "payload",
                            [str(tmp_path / "x")])
    with pytest.raises(write.EditError, match="no payload_ref"):
        write.submit(project, edit)


def test_payload_refuses_a_missing_source_rather_than_emptying_the_file(
        project, tmp_path):
    """A typo in the source path must never be a way to blank a payload."""
    _build_node(project)
    dest = tmp_path / "src" / "thing.py"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text("precious\n")
    edit = write.apply_verb(write.Edit("build:b1"), "payload",
                            [str(tmp_path / "typo.py")])
    with pytest.raises(FileNotFoundError):
        write.submit(project, edit)
    assert dest.read_text() == "precious\n"


def test_payload_never_creates_a_file_that_is_not_there(project, tmp_path):
    """Replacing nothing is creating, and creation has its own never-overwrite
    rule in `create --payload`."""
    _build_node(project, ref="src/absent.py")
    src = tmp_path / "new.py"
    src.write_text("x\n")
    edit = write.apply_verb(write.Edit("build:b1"), "payload", [str(src)])
    with pytest.raises(FileNotFoundError, match="never creates"):
        write.submit(project, edit)
    assert not (tmp_path / "src" / "absent.py").exists()


def test_payload_text_writes_the_bytes_inline_with_no_scratch_file(project,
                                                                  tmp_path):
    """`note` says the body inline; this says the payload inline. Staging a
    temp file just to hand it over was a step the verb layer imposed."""
    _build_node(project)
    dest = tmp_path / "src" / "thing.py"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text("old\n")

    edit = write.apply_verb(write.Edit("build:b1"), "payload_text",
                            ["print('new')"])
    res = write.submit(project, edit, actor="director")
    assert dest.read_text() == "print('new')\n", "a trailing newline is ensured"
    assert res.payload_changed is True


def test_payload_and_payload_text_are_the_same_operation(project, tmp_path):
    _build_node(project)
    dest = tmp_path / "src" / "thing.py"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text("old\n")
    src = tmp_path / "from_file.py"
    src.write_text("same\n")

    write.submit(project, write.apply_verb(
        write.Edit("build:b1"), "payload", [str(src)]), actor="d")
    from_file = dest.read_bytes()
    dest.write_text("old\n")
    write.submit(project, write.apply_verb(
        write.Edit("build:b1"), "payload_text", ["same"]), actor="d")
    assert dest.read_bytes() == from_file


def test_payload_resolves_against_the_nodes_named_location(project, tmp_path):
    """`goal:g13.1`: the base is a NAME on the node, not a path in the code.

    A node that says `location: docs_root` writes into whatever the config
    calls `docs_root` -- so moving that tree is a config edit, not a sweep
    over every node that points into it.
    """
    (project / "config.json").write_text(
        '{"locations": {"docs_root": "../elsewhere"}}')
    (project / "nodes" / "build").mkdir(parents=True, exist_ok=True)
    (project / "nodes" / "build" / "b2.md").write_text(
        '---\nid: "build:b2"\ntype: build\nmint_id: bbb222\n'
        'title: "t"\nbuild_kind: prose\norigin: build-scan\n'
        'payload_ref: NOTES.md\nlocation: docs_root\n---\n\nbody\n')
    elsewhere = tmp_path / "elsewhere"
    elsewhere.mkdir(parents=True, exist_ok=True)
    (elsewhere / "NOTES.md").write_text("old\n")
    # The default base must NOT be written: same relative ref, wrong tree.
    (tmp_path / "NOTES.md").write_text("untouched\n")

    write.submit(project, write.apply_verb(
        write.Edit("build:b2"), "payload_text", ["new"]), actor="d")
    assert (elsewhere / "NOTES.md").read_text() == "new\n"
    assert (tmp_path / "NOTES.md").read_text() == "untouched\n"


def test_an_unknown_location_is_refused_rather_than_defaulted(project,
                                                              tmp_path):
    """Falling back to the default would write real bytes into the wrong tree
    and report success -- the one failure a payload base can have that nobody
    would notice."""
    (project / "nodes" / "build").mkdir(parents=True, exist_ok=True)
    (project / "nodes" / "build" / "b3.md").write_text(
        '---\nid: "build:b3"\ntype: build\nmint_id: bbb333\n'
        'title: "t"\nbuild_kind: prose\norigin: build-scan\n'
        'payload_ref: NOTES.md\nlocation: nowhere\n---\n\nbody\n')
    (tmp_path / "NOTES.md").write_text("untouched\n")
    with pytest.raises(KeyError, match="unknown payload location"):
        write.submit(project, write.apply_verb(
            write.Edit("build:b3"), "payload_text", ["new"]), actor="d")
    assert (tmp_path / "NOTES.md").read_text() == "untouched\n"


def test_create_stamps_the_location_it_used(project):
    """Auto-assigned, and visible on the node so it can be changed later --
    an implicit default is the hardcoding this replaced, one level up."""
    _schemas(project)
    res, _ = write.create(project, "hypothesis", "located", ["goal:g1"],
                          payload="src/located.py")
    assert res.written
    assert "location: source_root" in Path(res.path).read_text()


def test_a_created_node_carries_the_same_provenance_as_an_edited_one(project):
    _schemas(project)
    res, _ = write.create(project, "hypothesis", "provenanced", ["goal:g1"],
                          actor="director", session="L1.07")
    text = Path(res.path).read_text()
    assert "edited_by: director" in text
    assert "thought_session: L1.07" in text


# --------------------------------------------------------------------------
# L2.08 — owner-only guard for moral nodes (hypothesis:l2w2-write-owner-and-payload-types)
# --------------------------------------------------------------------------

def _moral_schema(project: Path):
    """Write the moral schema so the gate can recognise moral nodes."""
    d = project / "context" / "schemas"
    d.mkdir(parents=True, exist_ok=True)
    (d / "[moral].md").write_text(
        "---\nname: moral\nspawn:\n  allowed_parents: []\n"
        "  min_parents: 0\n  max_parents: 0\n"
        "validation:\n  required: [id, type, mint_id, title]\n---\n\nbody\n")


def _moral_node(project: Path, slug: str = "faith") -> None:
    (project / "nodes" / "moral").mkdir(parents=True, exist_ok=True)
    (project / "nodes" / "moral" / f"{slug}.md").write_text(
        '---\nid: "moral:%s"\ntype: moral\nmint_id: mmm001\n'
        'title: "Faith"\n---\n\nthe body\n' % slug)


def test_create_moral_without_owner_is_refused(project):
    """🔴 RED FIRST: moral node creation without --actor owner must raise EditError.

    goal:g12 — the five moral nodes are hand-edited only by the owner.
    """
    _moral_schema(project)
    with pytest.raises(write.EditError, match="owner only"):
        write.create(project, "moral", "faith", [],
                     actor="director", bypass=True)
    assert not (project / "nodes" / "moral" / "faith.md").exists()


def test_create_moral_with_owner_succeeds(project):
    """Creating a moral node with --actor owner is permitted."""
    _moral_schema(project)
    res, made = write.create(project, "moral", "faith", [],
                              actor="owner", bypass=True)
    assert res.written and not res.rejected
    assert (project / "nodes" / "moral" / "faith.md").exists()


def test_submit_moral_without_owner_is_refused(project):
    """🔴 RED FIRST: editing a moral node without --actor owner must be refused."""
    _moral_node(project, "faith")
    e = write.Edit("moral:faith")
    write.verb_set(e, "title", "New Title")
    with pytest.raises(write.EditError, match="owner"):
        write.submit(project, e, actor="director")


def test_submit_moral_with_owner_succeeds(project):
    """Editing a moral node with --actor owner is permitted."""
    _moral_node(project, "faith")
    e = write.Edit("moral:faith")
    write.verb_set(e, "title", "New Title")
    res = write.submit(project, e, actor="owner")
    assert res.status == node_writer.UPDATED
    text = (project / "nodes" / "moral" / "faith.md").read_text()
    assert "edited_by: owner" in text
    assert "title: New Title" in text


def test_submit_non_moral_without_owner_still_works(project):
    """Non-moral nodes are NOT affected by the owner guard."""
    # The project fixture already has hypothesis:h1
    e = write.Edit("hypothesis:h1")
    write.verb_set(e, "title", "New")
    # This should work even with a non-owner actor
    res = write.submit(project, e, actor="director")
    assert res.status == node_writer.UPDATED


# --------------------------------------------------------------------------
# hypothesis:l3-node-without-mint-id — the `adopt` verb, the parent-facing
# repair that mints a FIRST mint_id on a node written outside node_writer.
# `set mint_id` stays refused; `adopt` is the one sanctioned exception and
# runs through node_writer.repair_mint, which refuses an already-minted node.
# --------------------------------------------------------------------------

def _write_no_mint_kid(project, node_id="experiment:e2"):
    """A kid-written node (valid frontmatter, real content, NO mint_id)."""
    ntype, slug = node_id.split(":", 1)
    p = project / "nodes" / ntype / f"{slug}.md"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(
        f"---\nid: {node_id}\ntype: {ntype}\nparents:\n- hypothesis:h1\n"
        f"---\n\n# {node_id}\n\nThe kid wrote this body directly.\n")
    return p


def test_verb_set_still_refuses_mint_id_even_with_adopt_available():
    """adopt is the exception, not a relaxation: `set mint_id` remains refused."""
    e = write.Edit("experiment:e2")
    with pytest.raises(write.EditError):
        write.verb_set(e, "mint_id", "anything")


def test_adopt_verb_mints_a_missing_mint_id(project):
    _write_no_mint_kid(project)
    rc = write.main(["experiment:e2", "adopt", "--root", str(project)])
    assert rc == 0
    text = (project / "nodes/experiment/e2.md").read_text()
    assert "mint_id:" in text and "scaffold_hash:" in text
    assert "The kid wrote this body directly." in text


def test_adopt_verb_refuses_when_a_mint_id_already_exists(project):
    p = _write_no_mint_kid(project)
    # give it a mint_id already
    text = p.read_text().replace(
        "type: experiment", "type: experiment\nmint_id: existing-123")
    p.write_text(text)
    rc = write.main(["experiment:e2", "adopt", "--root", str(project)])
    assert rc != 0
    out = (project / "nodes/experiment/e2.md").read_text()
    assert "existing-123" in out  # untouched


def test_adopt_verb_is_standalone(project):
    _write_no_mint_kid(project)
    rc = write.main(
        ["experiment:e2", "adopt && set status active", "--root", str(project)])
    assert rc == 2
    # nothing was adopted (node still has no mint_id)
    text = (project / "nodes/experiment/e2.md").read_text()
    assert "mint_id:" not in text


def test_adopt_dry_run_writes_nothing(project):
    _write_no_mint_kid(project)
    rc = write.main(
        ["experiment:e2", "adopt", "--dry-run", "--root", str(project)])
    assert rc == 0
    text = (project / "nodes/experiment/e2.md").read_text()
    assert "mint_id:" not in text


# --- a kid in a linked worktree addresses its own node without --root (l3w4)
# `hypothesis:l3w4-branch-shared-state`: the scaffolded node a dispatched kid
# is given lives ONLY in the kid's worktree graph (untracked, created after
# the worktree was cut). `write.py <node-id> "set …"` from the worktree cwd
# must resolve and write THAT node without an explicit `--root`, so a brief
# whose whole body is `write.py … set … && write.py … done` runs as written.


def _write_worktree_repo(tmp_path: Path, node_id: str, body: str) -> tuple[Path, Path]:
    """(repo, worktree): a git repo + linked worktree; the scaffolded node is
    placed ONLY in the worktree's graph, exactly as `dispatch` does."""
    import os
    import subprocess
    repo = tmp_path / "main"
    repo.mkdir(parents=True)
    subprocess.run(["git", "-C", str(repo), "init", "-b", "master"],
                   check=True, capture_output=True, text=True)
    subprocess.run(["git", "-C", str(repo), "config", "user.email", "t@t"],
                   check=True, capture_output=True)
    subprocess.run(["git", "-C", str(repo), "config", "user.name", "t"],
                   check=True, capture_output=True)
    graph = repo / ".agi"
    (graph / "nodes" / "experiment").mkdir(parents=True)
    (graph / "config.json").write_text("{}")
    (repo / "README").write_text("x")
    subprocess.run(["git", "-C", str(repo), "add", "-A"], check=True,
                   capture_output=True, text=True)
    subprocess.run(["git", "-C", str(repo), "commit", "-m", "init"],
                   check=True, capture_output=True, text=True)
    wt = tmp_path / "wt"
    subprocess.run(["git", "-C", str(repo), "worktree", "add",
                    "-b", "loop/x@s2", str(wt), "master"],
                   check=True, capture_output=True, text=True)
    # The kid's scaffold: only in the worktree, untracked (not in the main).
    wt_graph = wt / ".agi"
    (wt_graph / "nodes" / "experiment").mkdir(parents=True, exist_ok=True)
    (wt_graph / "nodes" / "experiment" / "e1.md").write_text(body)
    assert not (repo / ".agi" / "nodes" / "experiment" / "e1.md").exists(), \
        "the scaffolded node must live ONLY in the worktree (the fork)"
    return repo, wt


def test_write_resolves_own_node_from_worktree_without_root(tmp_path):
    """The P2 claim of `hypothesis:l3w4-branch-shared-state`: a kid whose cwd
    is `.agi/worktrees/<agent>` can `write.py <node-id> "set …"` with no
    `--root` and the write lands on its own scaffolded node."""
    import os
    body = ('---\nid: "experiment:e1"\ntype: experiment\nmint_id: abc123\n'
            'title: "t"\nscaffold_hash: deadbeef\nstatus: pending\n'
            'parents: [hypothesis:h1]\n---\n\nbody\n\n')
    _, wt = _write_worktree_repo(tmp_path, "experiment:e1", body)
    old = os.getcwd()
    try:
        os.chdir(wt)                       # the kid's dispatch cwd
        rc = write.main(["experiment:e1", "set verdict proved"])
    finally:
        os.chdir(old)
    assert rc == 0
    text = (wt / ".agi" / "nodes" / "experiment" / "e1.md").read_text()
    assert "verdict: proved" in text
