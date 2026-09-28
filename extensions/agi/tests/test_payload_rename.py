"""A payload_ref change renames the file in the SAME write.

hypothesis:a-payload-ref-change-renames-the-file-in-the-same-write. Before
this, `set payload_ref <new>` rewrote the row and left the file at the old
name: the row dangled until a hand `git mv`. Same directory -> the file moves
with the row, mint_id untouched. Another directory or another `location` base
-> REFUSED, naming both paths, unless the write carries `--confirm-move`. An
existing destination is never overwritten, confirmed or not.

Everything here runs on a temp graph under tmp_path. No user name, home path,
repo path value, host or IP appears in this file.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "bin"))
import node_writer  # noqa: E402
import write  # noqa: E402

ORIG = "# original bytes\n"


def _graph(tmp_path: Path):
    """A temp graph under G11 (graph at `<tmp>/.agi`, source at `<tmp>`), one
    build node whose `payload_ref` is RELATIVE so the `location` base is
    exercised, plus a second declared base for the cross-location case."""
    graph = tmp_path / ".agi"
    (graph / "nodes" / "build").mkdir(parents=True)
    (graph / "config.json").write_text('{"locations": {"vendor": "vendor"}}')
    payload = tmp_path / "lib" / "mod.py"
    payload.parent.mkdir(parents=True, exist_ok=True)
    payload.write_text(ORIG)
    node = graph / "nodes" / "build" / "b1.md"
    node.write_text(
        '---\nid: build:b1\ntype: build\nmint_id: abc123\n'
        'title: "t"\nscaffold_hash: deadbeef\n'
        'payload_ref: lib/mod.py\n---\n\nbody\n\n')
    return graph, payload, node


def _link_graph(tmp_path: Path):
    """The shape `create --payload` actually mints: `link_ref` and NO
    `payload_ref` (write.py:2950). links.py resolves `link_ref` FIRST, so a
    repoint that only writes `payload_ref` moves the file links.py reads and
    leaves the link dangling."""
    graph = tmp_path / ".agi"
    (graph / "nodes" / "build").mkdir(parents=True)
    (graph / "config.json").write_text('{"locations": {"vendor": "vendor"}}')
    payload = tmp_path / "lib" / "mod.py"
    payload.parent.mkdir(parents=True, exist_ok=True)
    payload.write_text(ORIG)
    node = graph / "nodes" / "build" / "b1.md"
    node.write_text(
        '---\nid: build:b1\ntype: build\nmint_id: abc123\n'
        'title: "t"\nscaffold_hash: deadbeef\n'
        'link_ref: lib/mod.py\n---\n\nbody\n\n')
    return graph, payload, node


def _submit_set(graph, node_id, key, value):
    edit = write.Edit(node_id=node_id)
    write.verb_set(edit, key, value)
    return write.submit(graph, edit, actor="kid", session="s1")


def _row_ref(node: Path) -> str:
    from graph_core.persistence import frontmatter as fm_reader
    return str(fm_reader.load_node_file(node, body=False).frontmatter
               .get("payload_ref") or "")


def test_same_directory_rename_moves_the_file_and_keeps_the_mint(tmp_path):
    graph, payload, node = _graph(tmp_path)
    res = _submit_set(graph, "build:b1", "payload_ref", "lib/renamed.py")
    assert res.status != node_writer.REJECTED
    assert not payload.exists(), "the old path must no longer exist"
    renamed = tmp_path / "lib" / "renamed.py"
    assert renamed.is_file() and renamed.read_text() == ORIG
    assert _row_ref(node) == "lib/renamed.py", "the row must resolve to the new file"
    assert node.read_text().count("mint_id: abc123") == 1, \
        "the rename is not a re-mint: mint_id must be unchanged"


def test_cross_directory_rename_is_refused_and_moves_nothing(tmp_path):
    graph, payload, node = _graph(tmp_path)
    with pytest.raises(write.EditError) as refused:
        _submit_set(graph, "build:b1", "payload_ref", "sub/moved.py")
    message = str(refused.value)
    assert "lib/mod.py" in message and "sub/moved.py" in message, \
        "the refusal must name BOTH paths"
    assert payload.is_file() and payload.read_text() == ORIG, \
        "a refused move must not touch the bytes"
    assert not (tmp_path / "sub" / "moved.py").exists()
    assert _row_ref(node) == "lib/mod.py", "a refused move must not touch the row"


def test_cross_location_change_is_refused_unless_confirmed(tmp_path):
    graph, payload, node = _graph(tmp_path)
    with pytest.raises(write.EditError) as refused:
        _submit_set(graph, "build:b1", "location", "vendor")
    assert "lib/mod.py" in str(refused.value) and "vendor" in str(refused.value)
    assert payload.is_file() and _row_ref(node) == "lib/mod.py"

    res = _submit_set(graph, "build:b1", "location", "--confirm-move vendor")
    assert res.status != node_writer.REJECTED
    assert not payload.exists()
    # a declared base is relative to the GRAPH root (locations.payload_base),
    # and the whole ref resolves under it, so the path gains the `lib/` part
    moved = graph / "vendor" / "lib" / "mod.py"
    assert moved.is_file() and moved.read_text() == ORIG
    assert _row_ref(node) == "lib/mod.py" and "location: vendor" in node.read_text()
    import locations as _loc
    assert _loc.resolve_payload_path(graph, _row_ref(node),
                                     "vendor") == moved, \
        "the row must resolve to an existing file after the move"


def test_existing_destination_is_never_overwritten(tmp_path):
    graph, payload, node = _graph(tmp_path)
    other = tmp_path / "lib" / "taken.py"
    other.write_text("# somebody else's bytes\n")
    with pytest.raises(write.EditError) as refused:
        _submit_set(graph, "build:b1", "payload_ref", "lib/taken.py")
    assert "taken.py" in str(refused.value)
    assert other.read_text() == "# somebody else's bytes\n"
    assert payload.read_text() == ORIG and _row_ref(node) == "lib/mod.py"

    # even WITH the confirm flag a same-directory clash is refused
    with pytest.raises(write.EditError):
        _submit_set(graph, "build:b1", "payload_ref", "--confirm-move lib/taken.py")
    assert other.read_text() == "# somebody else's bytes\n"
    assert payload.read_text() == ORIG and _row_ref(node) == "lib/mod.py"


def test_confirm_flag_is_a_prefix_and_only_on_the_two_naming_keys(tmp_path):
    graph, payload, node = _graph(tmp_path)
    edit = write.Edit(node_id="build:b1")
    write.verb_set(edit, "payload_ref", "--confirm-move lib/other.py")
    assert edit.confirm_location_move is True
    assert edit.set_fm["payload_ref"] == "lib/other.py"
    plain = write.Edit(node_id="build:b1")
    write.verb_set(plain, "title", "--confirm-move x")
    assert plain.confirm_location_move is False, \
        "the flag is not a general prefix: on another key it stays part of the value"


def test_mover_is_a_no_op_when_the_path_does_not_change(tmp_path):
    graph, payload, _ = _graph(tmp_path)
    before = payload.read_text()
    res = _submit_set(graph, "build:b1", "title", "still the same file")
    assert res.status != node_writer.REJECTED
    assert payload.is_file() and payload.read_text() == before


def test_a_declared_ref_with_no_file_here_is_not_a_refusal(tmp_path):
    """P4 (experiment:a00-6cb920d2-f30271): a row may name a file that is not
    in this checkout. There is nothing to move, so the write proceeds and the
    ROW is repointed — the mover's contract is 'bytes, when they are here,
    move with the row'."""
    graph, payload, node = _graph(tmp_path)
    payload.unlink()
    res = _submit_set(graph, "build:b1", "payload_ref", "lib/elsewhere.py")
    assert res.status != node_writer.REJECTED
    assert _row_ref(node) == "lib/elsewhere.py", "the row must still be written"
    assert not (tmp_path / "lib" / "elsewhere.py").exists(), \
        "no file is invented where there were none"
    log = (graph / "sessions" / "write-log.jsonl").read_text()
    assert "move_payload" not in log, "nothing moved, so nothing is logged"


def test_a_failed_row_write_leaves_the_bytes_where_they_were(tmp_path, monkeypatch):
    """The rename happens AFTER update_node, so a row that refuses to land
    cannot leave the bytes already moved and the row still old."""
    graph, payload, node = _graph(tmp_path)

    def refuse(root, node_id, **kw):
        raise RuntimeError("row refused")
    monkeypatch.setattr(node_writer, "update_node", refuse)
    with pytest.raises(RuntimeError):
        _submit_set(graph, "build:b1", "payload_ref", "lib/renamed.py")
    assert payload.is_file() and payload.read_text() == ORIG
    assert not (tmp_path / "lib" / "renamed.py").exists()
    assert _row_ref(node) == "lib/mod.py"


def test_a_link_ref_only_row_repoints_without_dangling(tmp_path):
    """The inversion: links.py reads `link_ref` FIRST, the mover sourced
    `payload_ref` first. A `create --payload` row names its file in
    `link_ref` alone, so the old mover moved the file links.py reads and left
    `link_ref` pointing at a path that was gone -- `broken_links` 1, a
    standing red with no committed test in the shape."""
    import links as _links
    graph, payload, node = _link_graph(tmp_path)
    assert _links.count_broken_links(graph) == 0
    res = _submit_set(graph, "build:b1", "payload_ref", "lib/new.py")
    assert res.status != node_writer.REJECTED
    assert not payload.exists() and (tmp_path / "lib" / "new.py").is_file()
    assert "link_ref: lib/new.py" in node.read_text(), \
        "the field links.py reads must carry the new path too"
    assert _links.count_broken_links(graph) == 0, \
        "a move must never leave the link broken"


def test_an_absent_source_still_asks_for_consent_cross_directory(tmp_path):
    """The consent gate is about the ROW, which outlives the checkout. A
    deleted payload must not turn a cross-directory repoint into a silent
    one: the plan used to return early on the absent source, ahead of the
    refusal (node_writer.plan_move)."""
    graph, payload, node = _graph(tmp_path)
    payload.unlink()
    with pytest.raises(write.EditError) as refused:
        _submit_set(graph, "build:b1", "payload_ref", "sub/moved.py")
    assert "lib/mod.py" in str(refused.value) and "sub/moved.py" in str(refused.value)
    assert _row_ref(node) == "lib/mod.py", "a refused write touches neither"
    # same-directory still lands: nothing to move, and nothing to refuse
    res = _submit_set(graph, "build:b1", "payload_ref", "lib/elsewhere.py")
    assert res.status != node_writer.REJECTED and _row_ref(node) == "lib/elsewhere.py"


def test_an_undeclared_location_is_a_refusal_not_a_traceback(tmp_path):
    """locations.payload_base raises KeyError for an unknown NAME, and neither
    submit nor main caught it -- the write that used to land a row died on a
    stack trace."""
    graph, payload, node = _graph(tmp_path)
    with pytest.raises(write.EditError) as refused:
        _submit_set(graph, "build:b1", "location", "nosuchbase")
    assert "nosuchbase" in str(refused.value)
    assert payload.is_file() and _row_ref(node) == "lib/mod.py"


def test_a_failed_move_rolls_the_row_back_onto_the_bytes(tmp_path, monkeypatch):
    """The rename runs after the row write, guarded only by status. An
    os.replace that raises left the ROW on the new path and the BYTES on the
    old one -- the dangling row conjunct 3 forbids."""
    graph, payload, node = _graph(tmp_path)

    def boom(*a, **kw):
        raise OSError("disk full")
    monkeypatch.setattr(node_writer, "move_payload", boom)
    with pytest.raises(write.EditError) as failed:
        _submit_set(graph, "build:b1", "payload_ref", "lib/renamed.py")
    assert "rolled back" in str(failed.value)
    assert payload.is_file() and payload.read_text() == ORIG, "the bytes stayed"
    assert _row_ref(node) == "lib/mod.py", "the row must resolve to the bytes"


def test_the_dry_run_preview_refuses_what_the_land_refuses(tmp_path):
    """A dry run simulates (create's schema gate runs PRE-dry-run on
    purpose), so the move plan has to run in the preview too. It did not:
    the preview exited 0 on a write the real submit() refused with exit 2."""
    import subprocess
    import sys as _sys
    graph, payload, _node = _graph(tmp_path)
    bin_dir = Path(__file__).resolve().parents[1] / "bin"
    env = {k: v for k, v in __import__("os").environ.items()
           if k not in ("TMUX", "TMUX_PANE")}
    run = lambda extra: subprocess.run(  # noqa: E731
        [_sys.executable, str(bin_dir / "write.py"), "build:b1",
         "set payload_ref sub/moved.py"] + extra,
        cwd=tmp_path, capture_output=True, text=True, env=env)
    preview = run(["--dry-run"])
    real = run([])
    assert preview.returncode == real.returncode == 2, (
        f"preview exit {preview.returncode}, land exit {real.returncode}")
    assert "MOVE PREVIEW" in preview.stdout
    assert payload.is_file() and _row_ref(Path(str(_node))) == "lib/mod.py"


def test_a_second_repoint_keeps_link_ref_on_the_new_name(tmp_path):
    """P1: the mirror keyed on `payload_ref` being ABSENT, so the SECOND
    `set payload_ref` of a renamed row moved the file and left `link_ref` on
    the first name (`broken_links` 1)."""
    import links as _links
    graph, payload, node = _link_graph(tmp_path)
    _submit_set(graph, "build:b1", "payload_ref", "lib/one.py")
    res = _submit_set(graph, "build:b1", "payload_ref", "lib/two.py")
    assert res.status != node_writer.REJECTED
    assert (tmp_path / "lib" / "two.py").is_file() and not (tmp_path / "lib" / "one.py").exists()
    assert "link_ref: lib/two.py" in node.read_text(), "the field links.py reads must follow EVERY repoint"
    assert _links.count_broken_links(graph) == 0


def test_a_payload_verb_in_the_rename_write_lands_on_the_new_name(tmp_path):
    """P2: the pair was read BEFORE the move, so `replace_payload` aimed at
    the old name and the caller's bytes were written NOWHERE."""
    graph, payload, node = _graph(tmp_path)
    edit = write.Edit(node_id="build:b1")
    write.verb_set(edit, "payload_ref", "lib/renamed.py")
    edit.payload_bytes = "# caller's new bytes\n"
    res = write.submit(graph, edit, actor="kid", session="s1")
    assert res.status != node_writer.REJECTED
    assert not payload.exists()
    assert (tmp_path / "lib" / "renamed.py").read_text() == "# caller's new bytes\n"
    assert _row_ref(node) == "lib/renamed.py"


def test_a_payload_verb_lands_on_the_new_name_when_the_old_file_is_absent(tmp_path):
    """DH.619 P-A': the re-aim was guarded on `_plan.src`, False exactly when the
    declared file is NOT here, so the payload verb aimed at the OLD ref and the
    caller's bytes landed NOWHERE. The effective pair is right either way."""
    graph, payload, node = _graph(tmp_path)
    payload.unlink()  # absent-source shape: lib/mod.py is never created
    (tmp_path / "lib" / "renamed.py").write_text("# already here\n")
    edit = write.Edit(node_id="build:b1")
    write.verb_set(edit, "payload_ref", "lib/renamed.py")
    edit.payload_bytes = "# caller's new bytes\n"
    # DH.643 M1: this half used to PIN the overwrite as intended. It was
    # pinning the hole -- an absent source short-circuited the plan, so the
    # re-aim wrote OVER the file already sitting at the destination.
    with pytest.raises(write.EditError) as onto:
        write.submit(graph, edit, actor="kid", session="s1")
    assert "renamed.py" in str(onto.value), "the refusal names the destination"
    assert (tmp_path / "lib" / "renamed.py").read_text() == "# already here\n"
    assert _row_ref(node) == "lib/mod.py", "a refused write does not touch the row"


def test_known_residual_a_row_may_name_a_file_that_does_not_exist(tmp_path):
    """KNOWN RESIDUAL, not intended behaviour (director-engine item 1): the row
    is repointed at a name with no file, and the payload verb then raises a
    raw FileNotFoundError. Closing it means node_writer.replace_payload
    CREATING -- node_writer.py is OUTSIDE this chain's file scope."""
    graph, payload, node = _graph(tmp_path)
    payload.unlink()
    edit = write.Edit(node_id="build:b1")
    write.verb_set(edit, "payload_ref", "lib/renamed.py")
    edit.payload_bytes = "# caller's new bytes\n"
    with pytest.raises(FileNotFoundError) as refused:
        write.submit(graph, edit, actor="kid", session="s1")
    assert "lib/renamed.py" in str(refused.value)
    assert _row_ref(node) == "lib/renamed.py", "the row dangles -- the residual"


def test_nothing_to_move_does_not_buy_an_overwrite_of_the_destination(tmp_path):
    """DH.643 M1, without the payload verb: the plan was `src=None` on an
    absent source, the mover returned None, and nothing anywhere said the
    destination was taken. The refusal is now unconditional and runs FIRST."""
    graph, payload, node = _graph(tmp_path)
    payload.unlink()  # absent source: nothing to move
    taken = tmp_path / "lib" / "renamed.py"
    taken.write_text("# somebody else's bytes\n")
    with pytest.raises(write.EditError) as refused:
        _submit_set(graph, "build:b1", "payload_ref", "lib/renamed.py")
    assert "renamed.py" in str(refused.value), "the refusal must name the destination"
    assert taken.read_text() == "# somebody else's bytes\n", "never overwritten"
    assert _row_ref(node) == "lib/mod.py", "a refused write does not touch the row"


def test_a_location_only_write_does_not_clobber_the_body_link(tmp_path):
    """DH.619 P-B: the mirror fired on every write naming `payload_ref` OR
    `location` and wrote the `_old_ref` default back over `link_ref`; on a
    BOTH-fields row `_old_ref` is the `payload_ref` value first, so a
    `location` move overwrote the body link's own target."""
    graph, _payload, node = _graph(tmp_path)
    node.write_text(node.read_text().replace(
        "payload_ref: lib/mod.py", "payload_ref: lib/mod.py\nlink_ref: docs/notes.py"))
    res = _submit_set(graph, "build:b1", "location", "--confirm-move vendor")
    assert res.status != node_writer.REJECTED
    assert "link_ref: docs/notes.py" in node.read_text()
    assert _row_ref(node) == "lib/mod.py"
    import locations as _loc
    assert _loc.resolve_payload_path(graph, "lib/mod.py", "vendor").is_file(), \
        "the bytes really moved, they were not copied"
    assert not _loc.resolve_payload_path(graph, "lib/mod.py", None).exists(), \
        "the old path is gone"


def test_a_both_fields_row_keeps_its_hand_written_body_link(tmp_path):
    """DH.643 M2: the mirror fired on every write NAMING `payload_ref` and
    wrote the new name into `link_ref` too, so a hand-written body link was
    repointed as collateral. The mirror maintains ONE name across two fields;
    it is not a licence to rewrite a second, separately declared one."""
    graph, payload, node = _graph(tmp_path)
    node.write_text(node.read_text().replace(
        "payload_ref: lib/mod.py", "payload_ref: lib/mod.py\nlink_ref: docs/notes.py"))
    res = _submit_set(graph, "build:b1", "payload_ref", "lib/renamed.py")
    assert res.status != node_writer.REJECTED
    assert _row_ref(node) == "lib/renamed.py", "the write aimed at payload_ref"
    assert "link_ref: docs/notes.py" in node.read_text(), \
        "a body link the author wrote by hand is not this write's business"
    assert not payload.exists() and (tmp_path / "lib" / "renamed.py").is_file()


def test_unset_payload_ref_refuses_by_name(tmp_path):
    """DH.643 M3: the mover's trigger keys on `set_fm` and `verb_unset` writes
    `edit.unset_fm`, so `unset payload_ref` repointed nothing, moved nothing,
    and left the row naming nothing."""
    graph, payload, node = _graph(tmp_path)
    edit = write.Edit(node_id="build:b1")
    write.verb_unset(edit, "payload_ref")
    with pytest.raises(write.EditError) as refused:
        write.submit(graph, edit, actor="kid", session="s1")
    assert "set payload_ref" in str(refused.value), "the refusal must name the way out"
    assert _row_ref(node) == "lib/mod.py" and payload.is_file()


def _both_fields_graph(tmp_path: Path):
    """A row naming its bytes in `payload_ref` AND carrying a hand-written body
    link in `link_ref` -- the M2 shape, where the two fields disagree."""
    graph, payload, node = _graph(tmp_path)
    (tmp_path / "docs").mkdir(exist_ok=True)
    target = tmp_path / "docs" / "spec.md"
    target.write_text("the body target\n")
    row = node.read_text().replace("payload_ref: lib/mod.py\n",
                                   "payload_ref: lib/mod.py\nlink_ref: docs/spec.md\n")
    node.write_text(row)
    return graph, payload, node, target


def test_a_body_link_is_unsettable_and_the_payload_refusal_names_its_own_field(
        tmp_path):
    """DH.663 (review probe P7b): the unset guard tested BOTH fields and
    raised ONE message naming `payload_ref`, so a `link_ref` that names a body
    target -- not the payload -- was refused by a message about a field the
    caller never wrote. Only the field the row actually names its FILE by is
    refused, and the refusal names that field."""
    graph, payload, node, target = _both_fields_graph(tmp_path)

    # the body link drops: the file it names is the node's, not the bytes'
    edit = write.Edit(node_id="build:b1")
    write.verb_unset(edit, "link_ref")
    res = write.submit(graph, edit, actor="kid", session="s1")
    assert res.status != node_writer.REJECTED, "dropping a body link is legal"
    assert "link_ref" not in node.read_text().split("---")[1]
    assert target.is_file() and _row_ref(node) == "lib/mod.py" and payload.is_file()

    # the payload field is still refused, by ITS name
    edit = write.Edit(node_id="build:b1")
    write.verb_unset(edit, "payload_ref")
    with pytest.raises(write.EditError) as refused:
        write.submit(graph, edit, actor="kid", session="s1")
    assert "payload_ref" in str(refused.value)
    assert _row_ref(node) == "lib/mod.py" and payload.is_file()


def test_unset_link_ref_on_a_create_payload_row_refuses_by_its_own_name(tmp_path):
    """The `create --payload` shape names the file in `link_ref` ALONE, so
    unsetting it there drops the row's name for bytes that stay on disk -- the
    same hazard, and the refusal must say `link_ref`, not `payload_ref`."""
    graph, payload, node = _link_graph(tmp_path)
    edit = write.Edit(node_id="build:b1")
    write.verb_unset(edit, "link_ref")
    with pytest.raises(write.EditError) as refused:
        write.submit(graph, edit, actor="kid", session="s1")
    assert "link_ref" in str(refused.value)
    assert payload.is_file() and "link_ref: lib/mod.py" in node.read_text()

    # the way out it names IS workable here: taking it moves the file.
    _submit_set(graph, "build:b1", "payload_ref", "lib/renamed.py")
    assert (tmp_path / "lib" / "renamed.py").is_file() and not payload.exists()
    assert _row_ref(node) == "lib/renamed.py"


@pytest.mark.parametrize("unsets,with_payload", [
    ((), False), (("link_ref",), False), ((), True)],
    ids=["plain set", "unset+set", "set+payload"])
def test_one_submit_reads_the_frontmatter_once(tmp_path, monkeypatch, unsets,
                                              with_payload):
    """Owner 2026-09-28 04:5xZ: `submit` read the node once PER REF HELPER --
    2/3/3 on these shapes, ONE now, every answer derived from that read.
    `unset link_ref` is legal here (the file field is `payload_ref`)."""
    graph, payload, node = _graph(tmp_path)
    seen, real = [], write._node_fm

    def counting(root, node_id):
        fm = real(root, node_id)
        seen.append(fm)
        return fm

    monkeypatch.setattr(write, "_node_fm", counting)
    edit = write.Edit(node_id="build:b1")
    for field in unsets:
        write.verb_unset(edit, field)
    write.verb_set(edit, "payload_ref", "lib/renamed.py")
    if with_payload:
        edit.payload_bytes = "# caller's new bytes\n"
    write.submit(graph, edit, actor="kid", session="s1")
    assert len(seen) == 1, f"{len(seen)} frontmatter reads, want 1"
    assert (tmp_path / "lib" / "renamed.py").is_file()


def test_a_failed_move_rolls_the_location_back_too(tmp_path, monkeypatch):
    """P7: the rollback restored the ref under the NEW `location` the same
    write had rebound -- a row that names nothing."""
    graph, payload, node = _graph(tmp_path)

    def boom(*a, **kw):
        raise OSError("disk full")
    monkeypatch.setattr(node_writer, "move_payload", boom)
    edit = write.Edit(node_id="build:b1")
    write.verb_set(edit, "location", "--confirm-move vendor")
    write.verb_set(edit, "payload_ref", "lib/renamed.py")
    with pytest.raises(write.EditError):
        write.submit(graph, edit, actor="kid", session="s1")
    import locations as _loc
    row = node.read_text()
    assert "location:" not in row, "the base must roll back with the ref"
    assert _loc.resolve_payload_path(graph, "lib/mod.py", None).is_file() \
        and _row_ref(node) == "lib/mod.py"


def _cli(graph, args, tmp_path):
    """write.py as a CALLER runs it: argv, exit code, stdout+stderr."""
    import os
    import subprocess
    import sys as _sys
    env = {k: v for k, v in os.environ.items()
           if k not in ("TMUX", "TMUX_PANE")}
    return subprocess.run(
        [_sys.executable, str(Path(__file__).resolve().parents[1] / "bin"
                              / "write.py")] + list(args),
        cwd=tmp_path, capture_output=True, text=True, env=env)


def test_the_confirm_flag_renames_end_to_end_from_argv(tmp_path):
    """The epilog teaches `set payload_ref --confirm-move <new/dir/f.txt>`;
    nothing ran that sentence through argv. No test line in the repo did."""
    graph, payload, node = _graph(tmp_path)
    run = _cli(graph, ["build:b1", "set payload_ref --confirm-move sub/new.py",
                       "--root", str(graph)], tmp_path)
    assert run.returncode == 0, run.stdout + run.stderr
    assert not payload.exists() and (tmp_path / "sub" / "new.py").is_file()
    assert _row_ref(node) == "sub/new.py"


def test_the_dry_run_refuses_an_outside_ref_the_land_refuses(tmp_path):
    """The outside-repo gate lived only inside submit(), so a `--confirm-move`
    past the MOVE PREVIEW previewed rc 0 for a write the land refuses rc 2."""
    graph, payload, node = _graph(tmp_path)
    args = ["build:b1", "set payload_ref --confirm-move ../escape.py",
            "--root", str(graph)]
    preview = _cli(graph, args + ["--dry-run"], tmp_path)
    land = _cli(graph, args, tmp_path)
    assert preview.returncode == land.returncode == 2, (
        f"preview {preview.returncode}, land {land.returncode}")
    assert "outside the repo tree" in (preview.stdout + preview.stderr)
    assert not Path(str(payload).replace("/lib/mod.py", "/../escape.py")).exists()
