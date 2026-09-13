"""Tests for hypothesis:l4-dispatch-exits-non-zero-and-deprecates-the-scaffold-
when-no-agent-record-follows-a-scaffolded-node.

The claim under test: when dispatch.py scaffolds a node for an agent and the
spawn's own registration step (the `Popen` that hands the slot to a pid) fails,
so no agent record exists, dispatch (1) exits a NAMED non-zero code (4,
"scaffolded-but-unregistered") with a JSON issue line naming the node id and
the missing record, (2) DEPRECATES the scaffold the same run — moved to
`nodes/deprecated/<type>/` with `status: deprecated` and a note naming the
failed spawn — and never leaves it live, while (3) a successful spawn's exit
code stays 0 with the scaffold left live, and (4) the stale-base rc-3 path is
untouched.

The registration-seam tests run the REAL live spawn machinery in-process with
`subprocess.Popen` patched (raising to fail registration, or a stub to
succeed); budget / session / manifest live under the scratch tmp_path.
"""
from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parents[1] / "bin"
sys.path.insert(0, str(BIN))


def _load_dispatch():
    spec = importlib.util.spec_from_file_location("agi_dispatch", BIN / "dispatch.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


dispatch = _load_dispatch()


@pytest.fixture()
def project(tmp_path: Path) -> Path:
    """A scratch agi project: `.agi/config.json`, a ladder roles table, a
    secrets geometry pinned to a nonexistent file (so provisioning is absent
    and the live path never mints or touches the network), and the target
    node hypothesis:x the spawn zooms for."""
    graph = tmp_path / ".agi"
    (graph / "nodes" / ".geometry").mkdir(parents=True)
    (graph / "nodes" / "hypothesis").mkdir(parents=True)
    (graph / "nodes" / "goal").mkdir(parents=True)
    (graph / "config.json").write_text(json.dumps({
        "harnesses": {"pi": {"adapter": "pi", "provider": "fake",
                             "models": {"kid": "deepseek-v4"}}},
        "spawn": {"harness": "pi", "parallel": 1, "max_live": 25},
        # keep the live run fast and focused: no inline reaper loop
        "agent_dispatch": {"inline_reaper": False},
    }))
    (graph / "nodes" / ".geometry" / "ladder.md").write_text(
        "---\ncurrent_season: 2\nroles:\n  - {tier: 0, role: kid, "
        "harness: pi, model: deepseek-v4}\n---\nbody")
    # provisioning absent -> the live path never mints a credential
    (graph / "nodes" / ".geometry" / "secrets.md").write_text(
        "---\nenv_file: /tmp/definitely-not-a-real-secrets-file-zzz\n---\n")
    (graph / "nodes" / "goal" / "g15.md").write_text(
        "---\nid: goal:g15\ntype: goal\n---\nbody\n")
    (graph / "nodes" / "hypothesis" / "x.md").write_text(
        "---\nid: hypothesis:x\ntype: hypothesis\nparents:\n  - goal:g15\n"
        "---\nbody\n")
    # keep the live run contained under the scratch project even when the
    # box's own env carries these exports
    for k in ("AGI_TREE_PROJECT_ROOT", "AGI_PROJECT_ROOT", "AGI_AGENT_ID",
              "AGI_ACTOR"):
        os.environ.pop(k, None)
    return tmp_path


def _stub_popen(monkeypatch, *, raise_exc=None):
    """Patch subprocess.Popen. Only the SPAWN call -- the one with
    `start_new_session=True`, which plain `subprocess.run`/git helpers inside
    dispatch never set -- is stubbed (or made to `raise_exc` for the
    fail-to-register seam). Every other Popen delegates to the real one so
    git and subprocess.run helpers keep working under scratch tmp_path."""
    captured = {}

    class _StubProc:
        pid = 7777
        def poll(self): return None
        def wait(self, timeout=None): return 0
        def __enter__(self): return self
        def __exit__(self, *a): return False

    real_popen = subprocess.Popen

    def _patched(argv, **kwargs):
        if kwargs.get("start_new_session"):
            captured["argv"] = argv
            if raise_exc is not None:
                raise raise_exc
            return _StubProc()
        return real_popen(argv, **kwargs)

    monkeypatch.setattr(subprocess, "Popen", _patched)
    return captured


def _argv(tmp_path: Path, *extra):
    import sys as _s
    return [str(BIN / "dispatch.py"), str(tmp_path), "1",
            "--level", "small", "--harness", "pi", "--tier", "kid",
            "--target", "hypothesis:x", *extra]


def _read_fm(path):
    import graph_core.persistence.frontmatter as fm_reader
    return dict(fm_reader.load_node_file(path).frontmatter)


def _deprecated_files(root: Path):
    dep = root / ".agi" / "nodes" / "deprecated"
    return [f for d in dep.glob("*") if d.is_dir() for f in d.glob("*.md")]


def test_popen_failure_returns_4_with_issue_line_and_deprecates(
        project, tmp_path, monkeypatch, capsys):
    """A spawn seam that scaffolds then fails to register: rc 4, a JSON issue
    line naming the node id + 'scaffolded-but-unregistered', and the scaffold
    moved to nodes/deprecated/hypothesis/ with status: deprecated."""
    _stub_popen(monkeypatch, raise_exc=OSError("no such harness binary"))
    monkeypatch.setattr(sys, "argv", _argv(project))

    code = dispatch.main()
    assert code == 4, f"expected rc 4 (scaffolded-but-unregistered), got {code}"

    out = capsys.readouterr().out
    issue = [json.loads(l) for l in out.splitlines()
             if l.lstrip().startswith("{")]
    assert issue, f"no JSON issue line on stdout:\n{out}"
    assert issue[0]["issue"] == "scaffolded-but-unregistered", issue
    node_id = issue[0]["node_id"]
    assert node_id and ":" in node_id, f"issue line must name the node id: {issue}"

    # the scaffold was deprecated the same run: moved under the retired tree
    moved = _deprecated_files(project)
    assert moved, f"scaffold {node_id} not moved under deprecated/"
    fm = _read_fm(moved[0])
    assert fm.get("status") == "deprecated", fm
    assert fm.get("id") == node_id, fm


def test_deprecate_orphan_scaffold_sets_a_note_naming_the_failed_spawn(
        project, tmp_path, monkeypatch, capsys):
    """The deprecation carries a note naming the failed spawn (agent id) so a
    cold reader can trace which spawn left the orphan."""
    from graph_core.persistence import frontmatter as fm_reader
    agent_id = "a00-fail09"

    # scaffold a node directly through the same writer dispatch uses
    info = dispatch._scaffold_node_for_agent(
        project / ".agi", 2, agent_id, "small", "hypothesis:x")
    assert info, "scaffold did not write"
    node_id = info["node_id"]

    # the spawn never registered -> deprecate it by hand through the helper
    assert dispatch._deprecate_orphan_scaffold(
        project / ".agi", node_id, agent_id) is True

    import node_writer
    # find_node_file resolves BOTH live and retired trees by design, so
    # "left live" means: not under the LIVE nodes/type/ dir anymore.
    assert not (project / ".agi" / "nodes" / "experiment" /
                f"{Path(node_id.split(':')[1])}.md").exists(), \
        "scaffold left live"
    moved = _deprecated_files(project)
    assert moved, f"scaffold {node_id} not moved under deprecated/"
    fm = _read_fm(moved[0])
    assert fm.get("status") == "deprecated", fm
    note = fm.get("deprecated_note", "")
    assert agent_id in note, f"note must name the failed spawn: {note!r}"


def test_successful_spawn_stays_0_and_leaves_the_scaffold_live(
        project, tmp_path, monkeypatch, capsys):
    """Success golden: with a working Popen the dispatch exits 0, byte-identical
    exit code to today, and the scaffolded node is left LIVE (not deprecated)."""
    captured = _stub_popen(monkeypatch)
    monkeypatch.setattr(sys, "argv", _argv(project))

    code = dispatch.main()
    assert code == 0, f"success path must stay rc 0, got {code} ({captured})"

    out = capsys.readouterr().out
    assert "scaffolded-but-unregistered" not in out
    assert not _deprecated_files(project), (
        "a successful spawn must not deprecate anything")


def test_stale_base_rc_3_path_is_untouched(project, tmp_path, monkeypatch):
    """The stale-base refusal still exits 3 (before any scaffold); the new
    rc-4 registration logic downstream must not disturb it."""
    monkeypatch.setattr(dispatch, "spawner_base_branch",
                        lambda workdir: "season/s2")
    monkeypatch.setattr(dispatch, "_stale_base_spawn",
                        lambda root, season, town=None: {
                            "status": "behind", "behind": 2, "files": []})
    monkeypatch.setattr(sys, "argv", _argv(project, "--branch"))

    code = dispatch.main()
    assert code == 3, f"stale-base must stay rc 3, got {code}"

def _issue_lines(out: str) -> list:
    return [json.loads(l) for l in out.splitlines()
            if l.lstrip().startswith("{")]


def test_mint_failure_returns_1_with_issue_line_and_deprecates(
        project, tmp_path, monkeypatch, capsys):
    """A spawn that scaffolds then FAILS to mint a credential: rc 1, the SAME
    named JSON issue line the rc-4 seam emits (parseable, names the node id +
    agent id + the missing credential), and the scaffold deprecated the same
    run -- closing the parent's conjunct (2) at the provisioning seam."""
    from provisioning import ProvisioningError
    # force the mint path live, then make the mint itself fail
    monkeypatch.setattr(dispatch.provisioning, "available",
                        lambda root=None: True)

    def _fail_mint(*a, **k):
        raise ProvisioningError("test mint failure")

    monkeypatch.setattr(dispatch.provisioning, "mint", _fail_mint)
    monkeypatch.setattr(sys, "argv", _argv(project))

    code = dispatch.main()
    assert code == 1, f"expected rc 1 (provisioning failure), got {code}"

    issue = _issue_lines(capsys.readouterr().out)
    assert issue, "no JSON issue line on stdout (mint-failure seam)"
    assert issue[0]["issue"] == "scaffolded-but-unregistered", issue
    node_id = issue[0]["node_id"]
    assert node_id and ":" in node_id, \
        f"issue line must name the node id: {issue}"
    assert issue[0]["agent_id"], f"must name the failed agent: {issue}"
    assert "credential" in issue[0]["detail"], issue

    moved = _deprecated_files(project)
    assert moved, f"scaffold {node_id} not moved under deprecated/"
    fm = _read_fm(moved[0])
    assert fm.get("status") == "deprecated", fm
    assert fm.get("id") == node_id, fm


def test_build_command_keyerror_returns_1_with_issue_line_and_deprecates(
        project, tmp_path, monkeypatch, capsys):
    """A config error (adapter build_command raising KeyError for a missing
    model) after scaffolding: rc 1 and the SAME named JSON issue line naming
    the node id -- one shared shape with the rc-4 and mint seams."""
    pi_mod = dispatch.adapters.load("pi")
    monkeypatch.setattr(pi_mod, "build_command",
                        lambda **kw: (_ for _ in ()).throw(
                            KeyError("no model for tier")))
    monkeypatch.setattr(sys, "argv", _argv(project))

    code = dispatch.main()
    assert code == 1, f"expected rc 1 (config error), got {code}"

    issue = _issue_lines(capsys.readouterr().out)
    assert issue, "no JSON issue line on stdout (config-error seam)"
    assert issue[0]["issue"] == "scaffolded-but-unregistered", issue
    node_id = issue[0]["node_id"]
    assert node_id and ":" in node_id, \
        f"issue line must name the node id: {issue}"
    assert issue[0]["agent_id"], f"must name the failed agent: {issue}"

    moved = _deprecated_files(project)
    assert moved, f"scaffold {node_id} not moved under deprecated/"
    fm = _read_fm(moved[0])
    assert fm.get("status") == "deprecated", fm
    assert fm.get("id") == node_id, fm
