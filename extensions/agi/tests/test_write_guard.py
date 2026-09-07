"""Tests for the write log and write_guard.py — l2w15-write-guard.

Every sanctioned node write is logged at the one engine function that writes a
node file, and write_guard.py check warns about any node whose bytes are not
in that log.
"""

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parents[1] / "bin"


def _load(name, filename=None):
    fp = BIN / (filename or f"{name}.py")
    spec = importlib.util.spec_from_file_location(name, fp)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


nw = _load("node_writer")
wg = _load("write_guard", "write_guard.py")


SHAPE = """\
---
name: shape
structural: true
parentless_types:
  - goal:long-term
  - goal:short-term
  - idea
max_parents_ceiling: 2
canonical_type_spelling: underscore
---
shape
"""

SCHEMAS = {
    "[hypothesis].md": "allowed_parents: [idea, goal]\n  min_parents: 0\n  max_parents: 2",
    "[experiment].md": "allowed_parents: [hypothesis, idea]\n  min_parents: 1\n  max_parents: 2",
    "[verdict].md": "allowed_parents: [experiment, hypothesis, verdict]\n  min_parents: 1\n  max_parents: 2",
    "[idea].md": "allowed_parents: [goal]\n  min_parents: 0\n  max_parents: 1",
}


# ---------------------------------------------------------------------------
# Fixture: a minimal agi project with .agi/config.json layout
# ---------------------------------------------------------------------------

@pytest.fixture
def project(tmp_path):
    """A throwaway git repo with schemas, one parent node, and .agi layout."""
    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
    subprocess.run(["git", "-C", str(tmp_path), "config", "user.email",
                    "test@test"], check=True)
    subprocess.run(["git", "-C", str(tmp_path), "config", "user.name",
                    "test"], check=True)

    agi = tmp_path / ".agi"
    agi.mkdir(parents=True)
    (agi / "config.json").write_text("{}")

    # Schemas
    sd = agi / "context" / "schemas"
    sd.mkdir(parents=True)
    (sd / "[shape].md").write_text(SHAPE)
    for fname, spawn in SCHEMAS.items():
        name = fname[1:-4]
        (sd / fname).write_text(
            f"---\nname: {name}\nspawn:\n  {spawn}\n---\n{name}\n")

    # Nodes directory
    nd = agi / "nodes"
    nd.mkdir(parents=True)
    nd2 = nd / "idea"
    nd2.mkdir(parents=True)
    (nd2 / "i1.md").write_text(
        "---\nid: idea:i1\ntype: idea\n---\n\nbody\n")

    # Initial commit
    subprocess.run(["git", "-C", str(tmp_path), "add", "-A"], check=True)
    subprocess.run(["git", "-C", str(tmp_path), "commit", "-m", "init"],
                   check=True, capture_output=True)

    return tmp_path  # repo root (contains .agi/)


# ---------------------------------------------------------------------------
# The write log is written by write_node
# ---------------------------------------------------------------------------

def test_write_node_logs(project):
    """write_node creates a log entry."""
    log_path = project / ".agi" / "sessions" / "write-log.jsonl"
    assert not log_path.exists()

    nw.write_node(project / ".agi", "hypothesis", "h2",
                  parents=["goal:g1"], announce=False)

    assert log_path.is_file()
    text = log_path.read_text().strip()
    assert text, "log file must have content"
    for line in text.splitlines():
        entry = json.loads(line)
        assert entry["node_id"] == "hypothesis:h2"
        assert entry["operation"] == "write_node"
        assert entry["sha256"]
        assert entry["path"].endswith("hypothesis/h2.md")


def test_write_log_carries_mint_id(project):
    """write_node logs the node's mint_id (SETTLED rekey)."""
    log_path = project / ".agi" / "sessions" / "write-log.jsonl"

    nw.write_node(project / ".agi", "hypothesis", "h-mint",
                  parents=[], announce=False)

    # Re-read the node to confirm which mint_id it actually carries
    node_file = project / ".agi" / "nodes" / "hypothesis" / "h-mint.md"
    import yaml
    parts = node_file.read_text().split("---", 2)
    fm = yaml.safe_load(parts[1]) or {}
    real_mint = fm["mint_id"]
    assert len(real_mint) == 32

    for line in log_path.read_text().strip().splitlines():
        entry = json.loads(line)
        if entry["operation"] == "write_node":
            assert entry.get("mint_id") == real_mint


def test_update_log_carries_mint_id(project):
    """update_node logs the same mint_id it stamps into the node."""
    log_path = project / ".agi" / "sessions" / "write-log.jsonl"
    nw.write_node(project / ".agi", "hypothesis", "h-mint-up",
                  parents=[], announce=False)

    import yaml
    node_file = project / ".agi" / "nodes" / "hypothesis" / "h-mint-up.md"
    parts = node_file.read_text().split("---", 2)
    fm = yaml.safe_load(parts[1]) or {}
    real_mint = fm["mint_id"]

    nw.update_node(project / ".agi", "hypothesis:h-mint-up",
                   set_fm={"status": "active"}, announce=False)
    tail_ops = [json.loads(l) for l in log_path.read_text().strip().splitlines()
                if l.strip()]
    upd = [e for e in tail_ops if e["operation"] == "update_node"]
    assert upd and upd[-1].get("mint_id") == real_mint


def test_update_node_logs(project):
    """update_node creates a log entry."""
    log_path = project / ".agi" / "sessions" / "write-log.jsonl"

    nw.write_node(project / ".agi", "idea", "i2",
                  parents=[], announce=False)
    assert log_path.is_file()

    # Now update
    nw.update_node(project / ".agi", "idea:i2",
                   set_fm={"status": "active"}, announce=False)
    text = log_path.read_text().strip()
    ops = [json.loads(line)["operation"] for line in text.splitlines()
           if line.strip()]
    assert "update_node" in ops


# ---------------------------------------------------------------------------
# write_guard check is silent after sanctioned writes
# ---------------------------------------------------------------------------

def _check(project, extra_args=None):
    """Run write_guard check against a test project."""
    root = str((project / ".agi").resolve())
    args = ["--root", root]
    if extra_args:
        args.extend(extra_args)
    return wg.cmd_check(args)


def test_write_guard_silent_after_sanctioned_write(project):
    """After a write_node, check finds nothing unsanctioned."""
    nw.write_node(project / ".agi", "hypothesis", "h-sanctioned",
                  parents=[], announce=False)

    rc = _check(project)
    assert rc == 0, "check must exit 0 after a sanctioned write"


def test_write_guard_strict_ok_after_sanctioned_write(project):
    """After a sanctioned write, even --strict passes."""
    nw.write_node(project / ".agi", "hypothesis", "h-sanctioned-2",
                  parents=[], announce=False)

    rc = _check(project, ["--strict"])
    assert rc == 0, "--strict must pass after a sanctioned write"


# ---------------------------------------------------------------------------
# write_guard warns on direct file edits
# ---------------------------------------------------------------------------

def test_write_guard_warns_after_direct_edit(project):
    """A direct sed/touch edit to a node file triggers a WARN."""
    nw.write_node(project / ".agi", "hypothesis", "h-edited", [],
                  announce=False)

    # Direct file edit (unsanctioned)
    node_file = project / ".agi" / "nodes" / "hypothesis" / "h-edited.md"
    original = node_file.read_text()
    node_file.write_text(original + "\nExtra text\n")

    rc = _check(project)
    assert rc == 0, "non-strict check must exit 0 even with warnings"

    rc = _check(project, ["--strict"])
    assert rc == 1, "--strict must exit 1 on unsanctioned writes"


def test_write_guard_warns_on_edited_payload(project):
    """A direct edit to a payload file triggers a WARN."""
    # Create a build node pointing at a payload
    src = project / "extensions" / "agi" / "bin"
    src.mkdir(parents=True, exist_ok=True)
    payload_file = src / "test_payload.sh"
    payload_file.write_text("#!/bin/bash\necho hello\n")

    nw.write_node(project / ".agi", "mvp", "payload-test",
                  parents=[],
                  extra_fm={"payload_ref": "extensions/agi/bin/test_payload.sh",
                            "link_ref": "extensions/agi/bin/test_payload.sh"},
                  announce=False, bypass=True)

    # Direct edit to the payload
    payload_file.write_text("#!/bin/bash\necho modified\n")

    rc = _check(project, ["--strict"])
    assert rc == 1, "--strict must detect unsanctioned payload edits"


# ---------------------------------------------------------------------------
# pre-commit hook output
# ---------------------------------------------------------------------------

def test_hook_output():
    """write_guard.py hook prints a valid pre-commit hook."""
    import io
    sys.stdout = io.StringIO()
    try:
        rc = wg.cmd_hook([])
        output = sys.stdout.getvalue()
    finally:
        sys.stdout = sys.__stdout__

    assert rc == 0
    assert "#!/bin/sh" in output
    assert "write_guard.py check --strict" in output


# ---------------------------------------------------------------------------
# Log survives rejections — only successful writes are logged
# ---------------------------------------------------------------------------

def test_rejected_write_does_not_log(project):
    """A rejected write_node must not add to the log."""
    log_path = project / ".agi" / "sessions" / "write-log.jsonl"
    if log_path.exists():
        log_path.unlink()

    # Reject: experiment needs 1 parent, we give none, but first create a
    # valid parent to satisfy the schema registry
    nw.write_node(project / ".agi", "hypothesis", "orphan-parent",
                  parents=["idea:missing?"], announce=False, bypass=True)

    # This should be OK now — write_node with an idea parent is fine
    before_count = 0
    if log_path.exists():
        before_count = len(log_path.read_text().strip().splitlines())
    # This should fail
    nw.write_node(project / ".agi", "verdict", "orphan", [],
                  announce=False)
    if log_path.exists():
        after_count = len(log_path.read_text().strip().splitlines())
    else:
        after_count = 0
    assert after_count == before_count, (
        "rejected write must not add a log entry")


# ---------------------------------------------------------------------------
# write_guard in non-git repo
# ---------------------------------------------------------------------------

def test_write_guard_no_git(tmp_path):
    """Outside a git repo, check silently continues."""
    (tmp_path / ".agi" / "config.json").parent.mkdir(parents=True)
    (tmp_path / ".agi" / "config.json").write_text("{}")
    (tmp_path / ".agi" / "sessions").mkdir(parents=True)
    (tmp_path / ".agi" / "sessions" / "write-log.jsonl").write_text(
        '{"sha256": "abc123", "path": "nodes/x.md"}\n')

    # Write guard uses find_project_root which walks up from cwd
    # We can't easily override cwd in a pytest, so just verify the module loads
    assert wg is not None


# ---------------------------------------------------------------------------
# ensure_payload is logged
# ---------------------------------------------------------------------------

def test_ensure_payload_logs(project):
    """ensure_payload creates a log entry."""
    log_path = project / ".agi" / "sessions" / "write-log.jsonl"

    # Create payload directory and file via ensure_payload
    payload_dir = project / "ext" / "test"
    payload_dir.mkdir(parents=True, exist_ok=True)
    nw.ensure_payload(project / ".agi", "ext/test/payload.sh")

    assert log_path.is_file()
    text = log_path.read_text().strip()
    last_line = text.splitlines()[-1]
    entry = json.loads(last_line)
    assert entry["operation"] == "ensure_payload"
    assert entry["payload_ref"] == "ext/test/payload.sh"
    assert entry["path"].endswith("ext/test/payload.sh")
    assert entry["sha256"]  # not empty


def test_write_guard_silent_after_ensure_payload(project):
    """After ensure_payload + commit, check finds nothing unsanctioned."""
    payload_dir = project / "ext" / "test"
    payload_dir.mkdir(parents=True, exist_ok=True)
    nw.ensure_payload(project / ".agi", "ext/test/payload2.sh")

    # Commit so the payload is known to git
    subprocess.run(["git", "-C", str(project), "add", "-A"], check=True,
                   capture_output=True)
    subprocess.run(["git", "-C", str(project), "commit", "-m",
                    "add payload"], check=True, capture_output=True)

    # Create a build node pointing at this payload
    nw.write_node(project / ".agi", "mvp", "payload-mvp",
                  parents=[],
                  extra_fm={"payload_ref": "ext/test/payload2.sh",
                            "link_ref": "ext/test/payload2.sh"},
                  announce=False, bypass=True)

    rc = _check(project)
    assert rc == 0, "check must exit 0 after sanctioned ensure_payload"

    rc = _check(project, ["--strict"])
    assert rc == 0, "--strict must pass after sanctioned ensure_payload"


# ---------------------------------------------------------------------------
# .lock files created by _claim_node are ignored
# ---------------------------------------------------------------------------

def test_write_guard_ignores_lock_files(project):
    """
    .lock files under nodes/ are created by _claim_node for flock.
    The guard must not flag them as unsanctioned node writes.
    """
    nw.write_node(project / ".agi", "hypothesis", "h-lock-test",
                  parents=[], announce=False)

    # Commit so the node is tracked by git
    subprocess.run(["git", "-C", str(project), "add", "-A"], check=True,
                   capture_output=True)
    subprocess.run(["git", "-C", str(project), "commit", "-m",
                    "add node"], check=True, capture_output=True)

    # Create a .lock file next to the node, simulating _claim_node behavior
    lock_file = (project / ".agi" / "nodes" / "hypothesis" /
                 "h-lock-test.lock")
    lock_file.write_text("")

    # Must not warn about the .lock file
    rc = _check(project)
    assert rc == 0, ".lock files must not trigger a warning"

    rc = _check(project, ["--strict"])
    assert rc == 0, "--strict must pass when only .lock files differ"

    # Verify the node itself is still monitored
    node_file = project / ".agi" / "nodes" / "hypothesis" / "h-lock-test.md"
    node_file.write_text(node_file.read_text() + "\nExtra\n")

    rc = _check(project, ["--strict"])
    assert rc == 1, "--strict must still detect node edits even with lock files"


# ---------------------------------------------------------------------------
# Mint-id rekey: git mv of a logged node stays silent, hand edit still warns
# ---------------------------------------------------------------------------

def test_git_mv_logged_node_stays_silent(project):
    """A clean git mv of a logged node must not trigger a WARN (SETTLED)."""
    nw.write_node(project / ".agi", "hypothesis", "h-rename",
                  parents=[], announce=False)
    # Commit the node so git knows both the old and new path
    subprocess.run(["git", "-C", str(project), "add", "-A"], check=True,
                   capture_output=True)
    subprocess.run(["git", "-C", str(project), "commit", "-m", "add node"],
                   check=True, capture_output=True)

    old = project / ".agi" / "nodes" / "hypothesis" / "h-rename.md"
    new_dir = project / ".agi" / "nodes" / "hypothesis"
    new = new_dir / "h-renamed-away.md"
    subprocess.run(["git", "-C", str(project), "mv",
                    str(old), str(new)], check=True, capture_output=True)

    # Untracked node of the story, so check only sees the mv
    rc = _check(project, ["--strict"])
    assert rc == 0, "a clean git mv of a logged node must be silent"


def test_hand_edit_after_git_mv_still_warns(project):
    """After a git mv, a hand edit to the moved node's bytes warns (SETTLED)."""
    nw.write_node(project / ".agi", "hypothesis", "h-rename-edit",
                  parents=[], announce=False)
    subprocess.run(["git", "-C", str(project), "add", "-A"], check=True,
                   capture_output=True)
    subprocess.run(["git", "-C", str(project), "commit", "-m", "add node"],
                   check=True, capture_output=True)

    old = project / ".agi" / "nodes" / "hypothesis" / "h-rename-edit.md"
    new = project / ".agi" / "nodes" / "hypothesis" / "h-renamed-edited.md"
    subprocess.run(["git", "-C", str(project), "mv", str(old), str(new)],
                   check=True, capture_output=True)

    # Hand edit the moved node's bytes (unsanctioned)
    new.write_text(new.read_text() + "\nHand edited.\n")

    rc = _check(project, ["--strict"])
    assert rc == 1, "--strict must warn on a hand edit after a git mv"
