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

def _open_mode(node) -> str | None:
    """The static mode of an `open(...)` call, or None if undecidable.

    hypothesis:l3-write-partial-diffs-as-writes -- `read` streams a payload
    range with a READ-mode `open(...)`. The invariant this test guards is
    *no file WRITE in this module*; a read-only open is not a write, so the
    guard must flag a write/add/truncate mode (or a mode it cannot prove is
    read-only) and allow a provably read-only one. The default mode is read.
    """
    for kw in node.keywords:
        if kw.arg == "mode":
            if isinstance(kw.value, ast.Constant) and isinstance(kw.value.value, str):
                return kw.value.value
            return None
    if len(node.args) >= 2:
        m = node.args[1]
        if isinstance(m, ast.Constant) and isinstance(m.value, str):
            return m.value
        return None
    return "r"


def _is_read_only_open(mode: str | None) -> bool:
    if mode is None:
        return False          # cannot prove it is a read -> treat as a write
    stripped = mode.replace("b", "").replace("t", "")
    return stripped in ("", "r")


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
        # An `open()` is only the flagged hazard when it can WRITE: a
        # provably read-only open (the `read` verb's payload streamer) is not.
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) \
                and node.func.id == "open" and not _is_read_only_open(_open_mode(node)):
            offenders.append((node.lineno, "open"))
    assert offenders == [], f"write.py writes files directly: {offenders}"


def test_open_guard_still_flags_a_write_mode_open():
    """The refinement must not gut the guard: a write-mode open is still the
    hazard, and so is an open whose mode cannot be proven read-only."""
    import ast as _ast
    def call(mode_arg):
        src = f"open('x', {mode_arg})" if mode_arg else "open('x')"
        n = _ast.parse(src).body[0].value
        return not _is_read_only_open(_open_mode(n))
    assert call('"w"') is True
    assert call('"a"') is True
    assert call('"r+"') is True
    assert call('mode="wb"') is True
    assert call(None) is False        # default mode is read
    assert call('"r"') is False
    assert call('"rb"') is False
    assert call('opts') is True       # non-literal mode: cannot prove read-only


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
        "---\nname: moral\nwritten_by: owner\nspawn:\n  allowed_parents: []\n"
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
    THE ONE assertion this round is allowed to retarget (L4.40): the refusal
    message no longer contains the phrase `owner only`, so this now asserts
    the NEW message and it asserts MORE — that it names the node TYPE
    (`moral`) and the admitted writer (`owner`), and that the old catch-all
    phrase is gone rather than loosened to `match=""`.
    """
    _moral_schema(project)
    with pytest.raises(write.EditError, match="moral") as ei:
        write.create(project, "moral", "faith", [],
                     actor="director", bypass=True)
    msg = str(ei.value)
    assert "moral" in msg        # the refusal names the node TYPE
    assert "owner" in msg        # and the admitted writer
    assert "owner only" not in msg
    assert not (project / "nodes" / "moral" / "faith.md").exists()


def test_create_moral_with_owner_succeeds(project):
    """Creating a moral node with --actor owner is permitted."""
    _moral_schema(project)
    res, made = write.create(project, "moral", "faith", [],
                              actor="owner", bypass=True)
    assert res.written and not res.rejected
    assert (project / "nodes" / "moral" / "faith.md").exists()


def test_submit_moral_without_owner_is_refused(project):
    """RED FIRST: editing a moral node without --actor owner must be refused."""
    _moral_schema(project)   # L4.32 — the gate is schema-driven; it needs
                             # the [moral].md that declares written_by: owner
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
# hypothesis:l4-written-by-message-and-shape — the refusal message must name
# the node TYPE and its admitted writers, and `written_by` admits a LIST and
# a comma-separated string, matching links.py's report parse.
# --------------------------------------------------------------------------

def _written_by_schema(project, ntype, written_by):
    """Fixture schema for an arbitrary type declaring `written_by`."""
    d = project / "context" / "schemas"
    d.mkdir(parents=True, exist_ok=True)
    (d / f"[{ntype}].md").write_text(
        "---\nname: %s\nwritten_by: %s\n"
        "spawn:\n  allowed_parents: []\n  min_parents: 0\n  max_parents: 0\n"
        "validation:\n  required: [id, type, title]\n---\n\nbody\n"
        % (ntype, written_by))


def _typed_node(project, ntype, slug, node_id):
    (project / "nodes" / ntype).mkdir(parents=True, exist_ok=True)
    (project / "nodes" / ntype / f"{slug}.md").write_text(
        '---\nid: "%s"\ntype: %s\nmint_id: tst001\ntitle: "T"\n---\n\nbody\n'
        % (node_id, ntype))


def test_refusal_message_names_the_types_own_schema_and_its_writers(project):
    """(1) A non-moral type's schema `written_by` refuses with a message that
    names THAT type (not `moral`) and the writers it admits."""
    _written_by_schema(project, "variorum", "scribe")
    with pytest.raises(write.EditError) as ei:
        write.create(project, "variorum", "v1", [],
                     actor="director", bypass=True)
    msg = str(ei.value)
    assert "variorum" in msg      # names the node type being refused
    assert "scribe" in msg        # names the admitted writer
    assert "moral" not in msg     # not the moral catch-all
    assert not (project / "nodes" / "variorum" / "foobar.md").exists()


def test_list_written_by_admits_every_listed_writer(project):
    """(2) A list-valued `written_by` admits EVERY listed writer."""
    _written_by_schema(project, "variorum", "[scribe, corrector]")
    # both listed writers admitted
    write.create(project, "variorum", "foobar", [],
                 actor="scribe", bypass=True)
    write.create(project, "variorum", "baz", [],
                 actor="corrector", bypass=True)
    # an unlisted writer refused
    with pytest.raises(write.EditError) as ei:
        write.create(project, "variorum", "hawk", [],
                     actor="hawk", bypass=True)
    msg = str(ei.value)
    assert "variorum" in msg
    assert "scrib" in msg and "corrector" in msg
    assert not (project / "nodes" / "variorum" / "hawk.md").exists()


def test_comma_string_parses_same_as_list(project):
    """(3) A comma-separated string admits the same writers as the list form.

    The enforcer parses both identically (shared helper with `links.py`), so
    a scalar string and a list never disagree about membership.
    """
    from links import parse_written_by
    assert parse_written_by("scribe, corrector") == \
        parse_written_by(["scribe", "corrector"])
    assert parse_written_by("scribe,  corrector") == {"scribe", "corrector"}
    assert parse_written_by("scribe,corrector") == {"scribe", "corrector"}
    assert parse_written_by(None) is None
    assert parse_written_by("") == set()

    # and through the gate: a comma-string schema admits its writers
    _written_by_schema(project, "variorum", "scribe, corrector")
    write.create(project, "variorum", "foobar", [],
                 actor="scribe", bypass=True)
    with pytest.raises(write.EditError):
        write.create(project, "variorum", "hawk", [],
                     actor="henry", bypass=True)



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


# hypothesis:l3-write-partial-diffs-as-writes
ORIG_MOD = ("def alpha():\n    return 1\n\n"
            "def beta():\n    return 2\n\n"
            "def gamma():\n    return 3\n")
# `def beta():` is original line 4; the hunk moves both cursors to beta's body.
VALID_HUNK = ("--- a/mod.py\n+++ b/mod.py\n"
              "@@ -4,2 +4,2 @@\n"
              " def beta():\n"
              "-    return 2\n"
              "+    return 20\n")


def test_patch_applies_unified_diff_and_refuses_mismatch():
    changed = write.apply_unified_diff(ORIG_MOD, VALID_HUNK)
    assert "    return 20" in changed
    assert "    return 2\n" not in changed

    # A hunk naming a line that is not there must refuse the WHOLE diff,
    # raising, not partially applying.
    bad = VALID_HUNK.replace("-    return 2", "-    return ZZZ-NOT-HERE")
    with pytest.raises(write.EditError):
        write.apply_unified_diff(ORIG_MOD, bad)

    # A malformed hunk header is a refusal too.
    with pytest.raises(write.EditError):
        write.apply_unified_diff(ORIG_MOD, "@@ -x +y @@\n foo\n")


# --------------------------------------------------------------------------
# hypothesis:l3-write-partial-diffs-as-writes, build item 1 — the `read`
# terminal verb (read-only line addressing).
# 🔴 RED FIRST: a ranged read must print the requested lines to stdout and
# leave the node file BYTE-IDENTICAL on disk — no edited_by restamp, no body
# mutation, no trailing-newline loss, no grid version. A read that looks like
# an edit is worse than no read at all.
# --------------------------------------------------------------------------

def _run(argv):
    """Run write.main, capturing stdout/stderr, returning (out, err, rc)."""
    import io
    from contextlib import redirect_stderr, redirect_stdout
    out, err = io.StringIO(), io.StringIO()
    with redirect_stdout(out), redirect_stderr(err):
        rc = write.main(argv)
    return out.getvalue(), err.getvalue(), rc


def test_read_body_prints_range_and_leaves_node_byte_identical(project):
    node = project / "nodes" / "hypothesis" / "h1.md"
    before = node.read_bytes()
    out, err, rc = _run(["hypothesis:h1", "read body 1:3",
                         "--root", str(project)])
    assert rc == 0, err
    assert "the body" in out, f"a body read should print the lines, got {out!r}"
    assert node.read_bytes() == before, (
        "a read must leave the node byte-identical: no edited_by restamp, "
        "no body mutation, no trailing-newline loss, no grid version")


def test_read_payload_prints_the_range_and_writes_nothing(project, tmp_path):
    _build_node(project, ref=str(tmp_path / "mod.py"))
    payload = tmp_path / "mod.py"
    payload.write_text("".join(f"line {i}\n" for i in range(1, 31)))
    node = project / "nodes" / "build" / "b1.md"
    before_file = payload.read_bytes()
    before_node = node.read_bytes()
    out, err, rc = _run(["build:b1", "read payload 10:20",
                         "--root", str(project)])
    assert rc == 0, err
    lines = out.splitlines()
    assert lines and lines[0] == "line 10" and lines[-1] == "line 20"
    assert len(lines) == 11, f"10:20 is 11 lines, got {len(lines)}"
    assert payload.read_bytes() == before_file, "the payload must be untouched"
    assert node.read_bytes() == before_node, "the node must be byte-identical"


def test_read_supports_open_ended_ranges(project, tmp_path):
    _build_node(project, ref=str(tmp_path / "mod.py"))
    payload = tmp_path / "mod.py"
    payload.write_text("".join(f"line {i}\n" for i in range(1, 31)))
    out, err, rc = _run(["build:b1", "read payload 28:",
                         "--root", str(project)])
    assert rc == 0 and out.splitlines() == ["line 28", "line 29", "line 30"]
    out, err, rc = _run(["build:b1", "read payload :3",
                         "--root", str(project)])
    assert rc == 0 and out.splitlines() == ["line 1", "line 2", "line 3"]


def test_read_refuses_a_bad_range(project):
    out, err, rc = _run(["hypothesis:h1", "read body 10:2",
                         "--root", str(project)])
    assert rc == 2 and not out, f"an inverted range must refuse, got {out!r} {rc}"


def test_read_is_terminal_and_cannot_share_a_line_with_write_verbs(project,
                                                                  tmp_path):
    _build_node(project, ref=str(tmp_path / "mod.py"))
    (tmp_path / "mod.py").write_text("x\n")
    node = project / "nodes" / "build" / "b1.md"
    before = node.read_bytes()
    out, err, rc = _run(["build:b1", "read payload 1:1 && set title changed",
                         "--root", str(project)])
    assert rc == 2, "a read mixed with a write verb must refuse, not silently drop the write"
    assert node.read_bytes() == before


def test_patch_verb_fails_closed_and_preserves_exec(tmp_path):
    """Drive the real in-memory patch path against a scratch build node+payload
    with an exec bit set: payload byte-for-byte unchanged on refusal, diff
    landing on success, destination still executable after both."""
    import os
    import stat as _stat
    graph = tmp_path / ".agi"
    (graph / "nodes" / "build").mkdir(parents=True)
    (graph / "config.json").write_text("{}")
    payload = tmp_path / "lib" / "mod.py"
    payload.parent.mkdir(parents=True, exist_ok=True)
    payload.write_text(ORIG_MOD)
    os.chmod(payload, 0o755)
    (graph / "nodes" / "build" / "b1.md").write_text(
        '---\nid: build:b1\ntype: build\nmint_id: abc123\n'
        'title: "t"\nscaffold_hash: deadbeef\n'
        f"payload_ref: {payload}\n---\n\nbody\n\n")

    # Refusal: a mismatched hunk raises and must not have touched the file.
    bad = VALID_HUNK.replace("-    return 2", "-    return ZZZ-NOT-HERE")
    with pytest.raises(write.EditError):
        write.apply_unified_diff(payload.read_text(), bad)
    assert payload.read_text() == ORIG_MOD, "a refused patch must change nothing"
    assert _stat.S_IMODE(payload.stat().st_mode) == 0o755, \
        "exec bit must survive a refused patch"

    # Success: the one-line diff lands through submit; exec is preserved.
    # NB root is the `.agi` DIR (matching the project fixture), not the
    # project dir -- find_node_file resolves under `<root>/nodes`.
    root = graph
    edit = write.Edit(node_id="build:b1")
    write.verb_patch(edit, "-")
    edit.patch_diff = VALID_HUNK
    res = write.submit(root, edit, actor="kid", session="s1")
    text = payload.read_text()
    assert res.status != node_writer.REJECTED
    assert "    return 20" in text and "    return 2\n" not in text
    assert _stat.S_IMODE(payload.stat().st_mode) == 0o755, \
        "the destination must stay executable after a successful patch"


# --------------------------------------------------------------------------
# `replace` — the offset-free partial write (L4, owner 2026-09-09)
# --------------------------------------------------------------------------

REPLACE_TEXT = "\n".join(f"line{i}" for i in range(1, 9))


@pytest.mark.parametrize("rng", ["3:5", "1:1", "6:", ":2", "8:8"])
def test_replace_is_the_exact_inverse_of_read(rng):
    """The property the verb exists for. Overwriting a range with exactly what
    a read of that range returned is the IDENTITY, so `read N:M` then
    `replace N:M` needs no arithmetic between them — which is what removes the
    manual offset step the caller used to have to get right (trap 0ah)."""
    assert write._splice_range(
        REPLACE_TEXT, rng, write._slice_range(REPLACE_TEXT, rng)) == REPLACE_TEXT


def test_replace_overwrites_only_the_named_lines():
    assert write._splice_range(REPLACE_TEXT, "3:5", "X\nY").split("\n") == [
        "line1", "line2", "X", "Y", "line6", "line7", "line8"]


def test_replace_absorbs_one_trailing_newline_so_a_target_does_not_grow():
    """Replacement text from a file or stdin carries a trailing newline;
    inserting it verbatim would add a blank line on every single edit."""
    assert (write._splice_range(REPLACE_TEXT, "3:3", "Z\n")
            == write._splice_range(REPLACE_TEXT, "3:3", "Z"))


def test_replace_with_empty_text_deletes_the_range():
    assert write._splice_range(REPLACE_TEXT, "3:5", "").split("\n") == [
        "line1", "line2", "line6", "line7", "line8"]


def test_replace_refuses_a_range_past_the_end_before_writing():
    with pytest.raises(write.EditError):
        write._splice_range(REPLACE_TEXT, "99:", "x")


def test_replace_refuses_an_unknown_target():
    with pytest.raises(write.EditError):
        write.verb_replace(write.Edit(node_id="x"), "frontmatter", "1:2", "-")


def test_replace_body_uses_the_same_coordinates_as_read(project):
    """End to end on a real node: the range `read` reports is the range
    `replace` writes, with no conversion in between."""
    cur = write._read_body_text(project, "hypothesis:h1")
    n = len(cur.split("\n"))
    whole = f"1:{n}"
    assert write._splice_range(cur, whole, write._slice_range(cur, whole)) == cur

    idx = next(i for i, ln in enumerate(cur.split("\n"), 1)
               if ln.strip() == "the body")
    edit = write.Edit(node_id="hypothesis:h1")
    write.verb_replace(edit, "body", f"{idx}:{idx}", "-")
    edit.replace_text = "REPLACED"
    res = write.submit(project, edit, actor="kid", session="s1")
    assert res.status != node_writer.REJECTED
    after = write._read_body_text(project, "hypothesis:h1")
    assert "REPLACED" in after and "the body" not in after
    assert len(after.split("\n")) == n, \
        "a one-line range replace must not change the line count"


def test_replace_payload_goes_through_the_same_routine_as_a_body(tmp_path):
    """The owner's ask: a payload file is editable by the SAME routine as a
    node body — one reader (`_target_text`), one transform (`_splice_range`),
    one range vocabulary — differing only in where the result lands."""
    graph = tmp_path / ".agi"
    (graph / "nodes" / "build").mkdir(parents=True)
    (graph / "config.json").write_text("{}")
    payload = tmp_path / "lib" / "mod.py"
    payload.parent.mkdir(parents=True, exist_ok=True)
    payload.write_text(ORIG_MOD)
    (graph / "nodes" / "build" / "b1.md").write_text(
        '---\nid: build:b1\ntype: build\nmint_id: abc123\n'
        'title: "t"\nscaffold_hash: deadbeef\n'
        f"payload_ref: {payload}\n---\n\nbody\n\n")

    before = payload.read_text()
    edit = write.Edit(node_id="build:b1")
    write.verb_replace(edit, "payload", "1:1", "-")
    edit.replace_text = "# REPLACED HEADER"
    res = write.submit(graph, edit, actor="kid", session="s1")
    assert res.status != node_writer.REJECTED
    after = payload.read_text()
    assert after.split("\n")[0] == "# REPLACED HEADER"
    assert after.split("\n")[1:] == before.split("\n")[1:], \
        "only the named line may change"


def test_replace_payload_refusal_leaves_the_file_untouched(tmp_path):
    graph = tmp_path / ".agi"
    (graph / "nodes" / "build").mkdir(parents=True)
    (graph / "config.json").write_text("{}")
    payload = tmp_path / "lib" / "mod.py"
    payload.parent.mkdir(parents=True, exist_ok=True)
    payload.write_text(ORIG_MOD)
    (graph / "nodes" / "build" / "b1.md").write_text(
        '---\nid: build:b1\ntype: build\nmint_id: abc123\n'
        'title: "t"\nscaffold_hash: deadbeef\n'
        f"payload_ref: {payload}\n---\n\nbody\n\n")

    edit = write.Edit(node_id="build:b1")
    write.verb_replace(edit, "payload", "9999:", "-")
    edit.replace_text = "nope"
    with pytest.raises(write.EditError):
        write.submit(graph, edit, actor="kid", session="s1")
    assert payload.read_text() == ORIG_MOD, \
        "a refused range must change nothing on disk"


# hypothesis:l4-replace-api-drops-source — the PYTHON API path has no
# coverage, which is exactly why the bug shipped. These tests drive
# write.Edit + write.verb_replace + write.submit with NO argv and NO manual
# replace_text: the replacement source is resolved by the shared resolver,
# exactly as a library caller would.
# --------------------------------------------------------------------------


def _api_replace_payload(tmp_path, src_text):
    """Set up a build node with a payload fixture and a source file, and
    return (graph, payload, payload_node_md, edit) ready for submit."""
    graph = tmp_path / ".agi"
    (graph / "nodes" / "build").mkdir(parents=True)
    (graph / "config.json").write_text("{}")
    payload = tmp_path / "lib" / "mod.py"
    payload.parent.mkdir(parents=True, exist_ok=True)
    payload.write_text(ORIG_MOD)
    (graph / "nodes" / "build" / "b1.md").write_text(
        '---\nid: build:b1\ntype: build\nmint_id: abc123\n'
        'title: "t"\nscaffold_hash: deadbeef\n'
        f"payload_ref: {payload}\n---\n\nbody\n\n")
    src = tmp_path / "src.txt"
    src.write_text(src_text)
    edit = write.Edit(node_id="build:b1")
    write.verb_replace(edit, "payload", "1:1", str(src))
    return graph, payload, edit


def test_api_replace_replaces_the_line_not_deletes_it(tmp_path):
    """The exact bug: an API-driven replace returned `status='updated'` while
    git numstat read `0 1` — the target line was DELETED, nothing inserted.
    Now the same path must produce an insertion+deletion (content equality,
    one line swapped, line count unchanged)."""
    graph, payload, edit = _api_replace_payload(tmp_path, "# REPLACED HEADER")
    before = payload.read_text()
    n_before = len(before.split("\n"))
    res = write.submit(graph, edit, actor="kid", session="s1")
    assert res.status != node_writer.REJECTED
    after = payload.read_text()
    assert after.split("\n")[0] == "# REPLACED HEADER", \
        "the API path must REPLACE the line, not delete it"
    assert after.split("\n")[1:] == before.split("\n")[1:], \
        "only the named line may change"
    assert len(after.split("\n")) == n_before, \
        "a one-line replace must not change the line count (numstat 1 1)"


def test_api_replace_refuses_an_empty_source_and_writes_nothing(tmp_path):
    """An EMPTY source must REFUSE with an EditError naming the source, and
    leave the file byte-identical. Replacing a range with nothing = deleting
    it, and that must never be the silent consequence of an empty file."""
    graph, payload, edit = _api_replace_payload(tmp_path, "")
    before = payload.read_text()
    with pytest.raises(write.EditError) as ei:
        write.submit(graph, edit, actor="kid", session="s1")
    assert "empty" in str(ei.value)
    assert payload.read_text() == before, \
        "an empty source must write NOTHING — file stays byte-identical"


def test_api_replace_refuses_a_missing_source_and_writes_nothing(tmp_path):
    """An ABSENT source must REFUSE naming the source, and write nothing."""
    graph = tmp_path / ".agi"
    (graph / "nodes" / "build").mkdir(parents=True)
    (graph / "config.json").write_text("{}")
    payload = tmp_path / "lib" / "mod.py"
    payload.parent.mkdir(parents=True, exist_ok=True)
    payload.write_text(ORIG_MOD)
    (graph / "nodes" / "build" / "b1.md").write_text(
        '---\nid: build:b1\ntype: build\nmint_id: abc123\n'
        'title: "t"\nscaffold_hash: deadbeef\n'
        f"payload_ref: {payload}\n---\n\nbody\n\n")
    missing = tmp_path / "does-not-exist.txt"
    before = payload.read_text()
    edit = write.Edit(node_id="build:b1")
    write.verb_replace(edit, "payload", "1:1", str(missing))
    with pytest.raises(write.EditError) as ei:
        write.submit(graph, edit, actor="kid", session="s1")
    assert str(missing) in str(ei.value), \
        "the refusal must NAME the unreadable source"
    assert payload.read_text() == before, \
        "a missing source must write NOTHING — file stays byte-identical"


def test_replace_body_is_standalone_like_body_patch(project):
    edit = write.Edit(node_id="hypothesis:h1")
    write.verb_replace(edit, "body", "1:1", "-")
    edit.replace_text = "x"
    write.verb_note(edit, "a note")
    with pytest.raises(write.EditError):
        write.submit(project, edit, actor="kid", session="s1")
