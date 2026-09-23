"""hypothesis:write-py-inline-replace-verb -- the `sub` / `sub!` verbs.

`sub <old> => <new>` replaces the ONE literal occurrence of `<old>` anywhere
in the node (frontmatter value or body); `sub payload <old> => <new>` does the
same for the bytes the node points at. 0 or 2+ matches REFUSE and write
nothing; `sub!` replaces every match and prints the count. The write lands
through the ordinary `set_fm` / body / `payload_bytes` paths, so the
schema / ring / written_by gates run exactly as they do for `set`.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parent.parent / "bin"
SRC = Path(__file__).resolve().parent.parent / "src"
sys.path.insert(0, str(BIN))
sys.path.insert(0, str(SRC))

import write  # noqa: E402
import node_writer  # noqa: E402


def _node(project: Path, rel: str, text: str) -> Path:
    path = project / "nodes" / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


@pytest.fixture()
def project(tmp_path: Path) -> Path:
    graph = tmp_path / ".agi"
    (graph / "nodes" / "hypothesis").mkdir(parents=True)
    (graph / "config.json").write_text("{}")
    _node(graph, "hypothesis/h1.md",
          '---\nid: "hypothesis:h1"\ntype: hypothesis\nmint_id: abc123\n'
          'title: "hello world"\ntestable_claim: "c"\nscaffold_hash: deadbeef\n'
          'status: pending\n---\n\nthe body says nothing here\n')
    return graph


def _run(graph: Path, script: str, *extra: str):
    return subprocess.run(
        [sys.executable, str(BIN / "write.py"), "hypothesis:h1", script,
         "--root", str(graph), "--actor", "kid", "--session", "s1", *extra],
        capture_output=True, text=True)


def test_sub_replaces_one_frontmatter_value_and_dry_run_shows_diff(project):
    path = project / "nodes" / "hypothesis" / "h1.md"
    before = path.read_text()
    proc = _run(project, "sub world => WORLD", "--dry-run")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    # conjunct 4: the preview is a diff of the SERIALIZED node the write would
    # land (frontmatter rendered + body), not the raw splice -- unquoted title
    # lines, plus the provenance stamp submit adds.
    assert "-title: hello world" in proc.stdout
    assert "+title: hello WORLD" in proc.stdout
    assert path.read_text() == before, "a dry run writes nothing"
    proc = _run(project, "sub world => WORLD")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "sub: replaced 1 occurrence(s)" in proc.stdout
    assert "hello WORLD" in path.read_text()


def test_sub_refuses_zero_and_two_matches_and_writes_nothing(project):
    path = project / "nodes" / "hypothesis" / "h1.md"
    before = path.read_text()
    proc = _run(project, "sub absent => q")
    assert proc.returncode == 2
    assert "0 occurrences" in proc.stderr
    assert path.read_text() == before
    # `world` in the title AND the body -> two matches, plain sub refuses.
    _node(project, "hypothesis/h1.md",
          '---\nid: "hypothesis:h1"\ntype: hypothesis\nmint_id: abc123\n'
          'title: "hello world"\ntestable_claim: "c"\nscaffold_hash: deadbeef\n'
          'status: pending\n---\n\nthe body says world again\n')
    before = path.read_text()
    proc = _run(project, "sub world => WORLD")
    assert proc.returncode == 2
    assert "2 occurrences" in proc.stderr and "sub!" in proc.stderr
    assert path.read_text() == before


def test_sub_bang_replaces_every_match_and_prints_count(project):
    _node(project, "hypothesis/h1.md",
          '---\nid: "hypothesis:h1"\ntype: hypothesis\nmint_id: abc123\n'
          'title: "hello world"\ntestable_claim: "c"\nscaffold_hash: deadbeef\n'
          'status: pending\n---\n\nthe body says world again\n')
    proc = _run(project, "sub! world => WORLD")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "sub: replaced 2 occurrence(s)" in proc.stdout
    text = (project / "nodes" / "hypothesis" / "h1.md").read_text()
    assert "hello WORLD" in text and "says WORLD again" in text


def test_sub_dry_run_diff_applied_to_disk_is_the_landed_bytes(project):
    """The printed `--dry-run` diff, applied to the on-disk node, is
    byte-for-byte what the real `sub` then writes -- including a body that
    opens with a duplicate frontmatter block the write absorbs and strips.

    Red before the fix: the preview applied `set_fm` BEFORE the absorb, so
    the body block's stale `title` clobbered the edit and the printed diff
    was EMPTY while the real write changed the title
    (hypothesis:sub-dry-run-preview-is-the-bytes-update-node-lands).
    """
    path = project / "nodes" / "hypothesis" / "h1.md"
    path.write_text(
        '---\nid: "hypothesis:h1"\ntype: hypothesis\nmint_id: abc123\n'
        'title: "hello world"\ntestable_claim: "c"\n'
        'scaffold_hash: deadbeef\nstatus: pending\nedited_by: kid\n'
        'thought_session: s1\n---\n\n'
        '---\ntitle: "dupe"\n---\n\nthe body says nothing here\n')
    # canonicalise: the writer's own serializer output is what is on disk, so
    # the printed patch applies to these exact bytes.
    path.write_text(write._baseline_node_text(project, "hypothesis:h1"))
    before = path.read_text()
    proc = _run(project, "sub world => WORLD", "--dry-run")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    lines = proc.stdout.splitlines(True)
    start = next(i for i, l in enumerate(lines) if l.startswith("--- a/"))
    end = next(i for i, l in enumerate(lines) if l.startswith("  sub "))
    diff = "".join(lines[start:end])
    assert diff, "the preview printed no diff for a real change"
    previewed = write.apply_unified_diff(before, diff)
    assert path.read_text() == before, "a dry run writes nothing"
    res = _run(project, "sub world => WORLD")
    assert res.returncode == 0, res.stdout + res.stderr
    landed = path.read_text()
    assert landed == previewed, (
        "applying the printed diff to the on-disk node must yield the landed "
        "bytes\n" + diff)
    assert "hello WORLD" in landed and "dupe" not in landed


def test_sub_body_lands_through_update_node(project):
    res = write.submit(project, _sub_edit("nothing => SOMETHING"),
                       actor="kid", session="s1")
    assert res.status != node_writer.REJECTED
    assert "says SOMETHING here" in write._read_body_text(project, "hypothesis:h1")


def _sub_edit(spec: str) -> write.Edit:
    e = write.Edit(node_id="hypothesis:h1")
    write.verb_sub(e, spec)
    return e


def test_sub_config_node_goes_through_the_written_by_gate(project):
    (project / "context" / "schemas").mkdir(parents=True)
    (project / "context" / "schemas" / "[config].md").write_text(
        "---\nname: config\nwritten_by: [owner]\n---\nconfig\n")
    _node(project, "config/c1.md",
          '---\nid: config:c1\ntype: config\nmint_id: ccc111\n'
          'title: "unique-token here"\n---\n\nbody\n')
    path = project / "nodes" / "config" / "c1.md"
    before = path.read_text()
    edit = write.Edit(node_id="config:c1")
    write.verb_sub(edit, "unique-token => TOKEN")
    with pytest.raises(write.EditError) as ei:
        write.submit(project, edit, actor="kid", session="s1")
    assert "admitted roles owner" in str(ei.value)
    assert path.read_text() == before
    # The admitted role lands the SAME sub.
    res = write.submit(project, edit, actor="owner", session="s1")
    assert res.status != node_writer.REJECTED
    assert "TOKEN here" in path.read_text()


def test_sub_payload_mode(tmp_path):
    graph = tmp_path / ".agi"
    (graph / "nodes" / "build").mkdir(parents=True)
    (graph / "config.json").write_text("{}")
    payload = tmp_path / "lib" / "mod.py"
    payload.parent.mkdir(parents=True)
    payload.write_text("alpha BETA gamma\n")
    _node(graph, "build/b1.md",
          "---\nid: build:b1\ntype: build\nmint_id: bbb111\ntitle: \"t\"\n"
          "scaffold_hash: deadbeef\npayload_ref: lib/mod.py\n---\n\nbody\n")
    proc = subprocess.run(
        [sys.executable, str(BIN / "write.py"), "build:b1",
         "sub payload BETA => DELTA", "--root", str(graph),
         "--actor", "kid", "--session", "s1"],
        capture_output=True, text=True)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert proc.stdout.count("sub: replaced 1 occurrence(s)") == 1
    assert payload.read_text() == "alpha DELTA gamma\n"


def test_sub_ampersand_not_led_by_a_verb_stays_in_argument():
    assert write.parse_script("sub a && b => c") == [("sub", ["a && b => c"])]
    assert write.parse_script("sub x => y && note why") == [
        ("sub", ["x => y"]), ("note", ["why"])]


def test_sub_value_with_open_thought_marker_is_refused_like_set(project):
    """conjunct 2: a `sub` that would land an open THOUGHT marker into a
    frontmatter value is refused by the SAME `_refuse_marker_value` that
    refuses `set` (verb_set)."""
    path = project / "nodes" / "hypothesis" / "h1.md"
    before = path.read_text()
    edit = _sub_edit("world => WORLD <!-- THOUGHT:BEGIN")
    with pytest.raises(write.EditError, match="THOUGHT marker"):
        write.submit(project, edit, actor="kid", session="s1")
    assert path.read_text() == before


def test_second_sub_composes_with_the_first(project):
    """conjunct 3: `sub a => b && sub c => d` applies the second sub to the
    bytes the first produced -- here the second old string only exists after
    the first replacement, so a discarded first sub refuses (0 matches)."""
    path = project / "nodes" / "hypothesis" / "h1.md"
    proc = _run(project, "sub hello => goodbye && sub goodbye => farewell")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "sub: replaced 2 occurrence(s)" in proc.stdout
    assert "farewell world" in path.read_text()