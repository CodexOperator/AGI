"""hypothesis:l3w4-hierarchy-one-source, body leg — `write.py body_patch`.

The deletion leg of the one-source command-structure hypothesis: a stale
hand-maintained pipe table in a node BODY must be removable as a SANCTIONED
write. `patch` cannot do it — it targets the payload file behind a build node
and refuses a graph node (no `payload_ref`) — so removing the duplicate table
was, for three rounds, only possible as the standing unsanctioned-write
failure class. `body_patch` applies the same fail-closed unified diff to the
node's BODY and lands through `node_writer.update_node`, so the THOUGHT
region is carried across, provenance is stamped, and write_guard sees a
sanctioned write.

Red-first: this file FAILED against pre-change write.py (`apply_verb` raised
"no verb body_patch") before the verb existed, and passes now.
"""
from __future__ import annotations

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

BODY = (
    "# h1\n\n"
    "declared in frontmatter\n\n"
    "| tier | role | harness | model | effort | settings |\n"
    "|---|---|---|---|---|---|\n"
    "| 1 | director (perpetual) | claude-code | fable | max | — |\n"
    "| 0 | kid | pi | ~deepseek/flash | — | — |\n"
    "\n"
    "rest of the body\n\n" + THOUGHT + "\n")


@pytest.fixture()
def project(tmp_path: Path) -> Path:
    graph = tmp_path / ".agi"
    (graph / "nodes" / "hypothesis").mkdir(parents=True)
    (graph / "config.json").write_text("{}")
    (graph / "nodes" / "hypothesis" / "h1.md").write_text(
        '---\nid: "hypothesis:h1"\ntype: hypothesis\nmint_id: abc123\n'
        'title: "t"\ntestable_claim: "c"\nscaffold_hash: deadbeef\n'
        'status: pending\n---\n\n' + BODY)
    return graph


def _remove_table(body: str) -> str:
    """The exact shape of the live deletion: drop the pipe-table block."""
    lines = body.split("\n")
    out, skipping = [], False
    for ln in lines:
        if ln.startswith("| tier | role |"):
            skipping = True
            continue
        if skipping and ln.startswith("| "):
            continue
        if skipping and not ln.startswith("|"):
            skipping = False
        out.append(ln)
    return "\n".join(out).strip("\n")


def _body() -> str:
    # The canonical reader (`frontmatter.load_node_file`) strips the body's
    # trailing newline; the diff must be built against those exact bytes.
    return BODY.rstrip("\n")


def test_body_patch_removes_the_table_and_carries_the_thought(project):
    before = _body()
    expected = _remove_table(before)
    edit = write.Edit("hypothesis:h1")
    write.apply_verb(edit, "body_patch", ["-"])
    edit.body_patch_diff = "\n".join(
        ["--- a/h1.md", "+++ b/h1.md"] +
        _pending_hunks(before, expected))
    res = write.submit(project, edit, actor="kid-a00", session="SD.04")
    assert res.status == node_writer.UPDATED
    new_body = (project / "nodes" / "hypothesis" / "h1.md").read_text()
    assert "director (perpetual)" not in new_body
    assert "| tier | role |" not in new_body
    # The authored region must survive a body rewrite (update_node carries it).
    assert "the old reason" in new_body
    assert "rest of the body" in new_body


def test_body_patch_is_a_sanctioned_write(project):
    """Write_guard keys a sanction on (mint_id, sha256) in write-log.jsonl; a
    body_patch through update_node must land in that log, not be flagged."""
    before = _body()
    expected = _remove_table(before)
    edit = write.Edit("hypothesis:h1")
    write.apply_verb(edit, "body_patch", ["-"])
    edit.body_patch_diff = "\n".join(
        ["--- a/h1.md", "+++ b/h1.md"] +
        _pending_hunks(before, expected))
    write.submit(project, edit, actor="kid-a00", session="SD.04")
    # The write log follows the node's project root (the parent of `nodes/`).
    log = (project.parent / ".agi" / "sessions" / "write-log.jsonl")
    assert log.is_file(), "a sanctioned write must be logged"
    assert "abc123" in log.read_text(), \
        "the log must carry the owning node's mint_id for write_guard"
    assert "update_node" in log.read_text()


def test_body_patch_is_standalone_and_refuses_note_on_the_same_line(project):
    edit = write.Edit("hypothesis:h1")
    write.apply_verb(edit, "body_patch", ["-"])
    edit.body_patch_diff = "@@ -1 +1 @@\n-# h1\n+# h2\n"
    write.apply_verb(edit, "note", ["appended by mistake"])
    with pytest.raises(write.EditError):
        write.submit(project, edit, actor="kid-a00")


def test_body_patch_from_path_applies(project, tmp_path):
    """hypothesis:l3-partial-write-adoption — the path form must APPLY the
    diff, not silently discard it (ordering bug in submit: the path file was
    read AFTER the apply-check, so body_patch_diff was empty at apply time and
    only the file got read into a variable nothing used). Red-first: this
    failed against pre-fix write.py with `unchanged: nothing to change`; the
    diff never landed."""
    before = _body()
    after = before.replace("rest of the body", "rest of the body EDITED")
    assert after != before
    diff = "\n".join(
        ["--- a/h1.md", "+++ b/h1.md"] +
        _pending_hunks(before, after))
    diff_path = tmp_path / "diff.txt"
    diff_path.write_text(diff, encoding="utf-8")

    edit = write.Edit("hypothesis:h1")
    write.apply_verb(edit, "body_patch", [str(diff_path)])
    res = write.submit(project, edit, actor="kid-a00", session="SD.15")
    assert res.status == node_writer.UPDATED, \
        f"path-form body_patch must apply, got {res.status}"
    new_body = (project / "nodes" / "hypothesis" / "h1.md").read_text()
    assert "rest of the body EDITED" in new_body, \
        "the path-form diff must actually land in the body"
    # Every other byte identical: the authored THOUGHT region is carried and
    # the only change is the one intended line.
    assert "the old reason" in new_body
    assert "# h1\n\ndeclared in frontmatter" in new_body


def test_body_patch_from_path_is_standalone(project, tmp_path):
    """hypothesis:l3-partial-write-adoption — the standalone guard must fire
    for the PATH form too. Pre-fix it sat INSIDE `if edit.body_patch_diff:`,
    which a path form never entered, so a chained attempt reported success
    while landing only the thought."""
    diff_path = tmp_path / "diff.txt"
    diff_path.write_text("@@ -1 +1 @@\n-# h1\n+# h2\n", encoding="utf-8")
    edit = write.Edit("hypothesis:h1")
    write.apply_verb(edit, "body_patch", [str(diff_path)])
    write.apply_verb(edit, "note", ["appended by mistake"])
    with pytest.raises(write.EditError):
        write.submit(project, edit, actor="kid-a00")


def test_every_verb_declares_its_arity(project):
    assert set(write.ARITY) == set(write.VERBS)


def _pending_hunks(before: str, after: str) -> list[str]:
    """A minimal fail-closed hunk set: the full deletion as one hunk."""
    import difflib
    return list(difflib.unified_diff(
        before.split("\n"), after.split("\n"),
        lineterm="", n=1))[2:]