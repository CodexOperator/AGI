"""hyp:heal-reaps-only-exited-bg-sessions-in-kid-worktrees.

`heal.py session-reap` lists `claude agents --json --all` rows, one line each
(candidate id, or the SKIP REASON by name), and runs `claude rm <id>` ONLY
with `--live` and ONLY on the candidates.

A FAKE `claude` on PATH is the ONLY path in this file: the real binary is
never exec'd (TMM.202 — a real claude session cannot be ended by any test).
The fake appends its argv to $CLAUDE_FAKE_ARGV so a test can assert EXACTLY
which argv was recorded.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

HEAL = Path(__file__).resolve().parents[1] / "bin" / "heal.py"

FAKE_CLAUDE = """#!{py}
import json, os, sys
argv = sys.argv[1:]
with open(os.environ["CLAUDE_FAKE_ARGV"], "a") as fh:
    fh.write(json.dumps(argv) + "\\n")
if argv[:2] == ["agents", "--json"]:
    print(open(os.environ["CLAUDE_FAKE_FIXTURE"]).read())
    sys.exit(0)
print("removed " + (argv[1] if len(argv) > 1 else ""))
sys.exit(0)
"""


def _fake_claude(tmp_path: Path, rows: list[dict]) -> tuple[str, Path]:
    """Write the fake claude + the fixture; return (PATH dir, argv record)."""
    bindir = tmp_path / "fakebin"
    bindir.mkdir()
    rec = tmp_path / "argv.jsonl"
    fx = tmp_path / "fixture.json"
    fx.write_text(json.dumps(rows))
    script = bindir / "claude"
    script.write_text(FAKE_CLAUDE.format(py=sys.executable))
    script.chmod(0o755)
    return str(bindir), rec


def _project(tmp_path: Path) -> Path:
    """A fake MAIN checkout with one kid worktree under the SHARED graph."""
    main = tmp_path / "main"
    (main / ".agi" / "worktrees" / "a00-4a925479").mkdir(parents=True)
    (main / ".agi" / "config.json").write_text(json.dumps({"box": {"root": "."}}))
    return main


def _rows(main: Path) -> list[dict]:
    wt = str(main / ".agi" / "worktrees" / "a00-4a925479")
    return [
        {"id": "kid-exited", "kind": "background", "state": "done", "cwd": wt},
        {"id": "kid-running", "kind": "background", "state": "running", "cwd": wt},
        {"id": "710907bf", "kind": "background", "state": "done", "cwd": str(main)},
        {"id": "kid-interactive", "kind": "interactive", "state": "done", "cwd": wt},
        {"id": "kid-remote", "kind": "remote-control", "state": "done", "cwd": wt},
    ]


def _run(tmp_path: Path, main: Path, *extra: str) -> tuple[str, list[list[str]]]:
    bindir, rec = _fake_claude(tmp_path, _rows(main))
    env = dict(os.environ, PATH=bindir + os.pathsep + os.environ["PATH"],
               CLAUDE_FAKE_ARGV=str(rec),
               CLAUDE_FAKE_FIXTURE=str(tmp_path / "fixture.json"))
    r = subprocess.run([sys.executable, str(HEAL), "session-reap",
                        "--root", str(main), *extra],
                       capture_output=True, text=True, env=env)
    assert r.returncode == 0, r.stderr
    recorded = ([json.loads(line) for line in rec.read_text().splitlines()]
                if rec.exists() else [])
    return r.stdout, recorded


def test_only_the_exited_kid_worktree_row_is_a_candidate(tmp_path):
    main = _project(tmp_path)
    out, _ = _run(tmp_path, main)
    assert "reap-candidate kid-exited" in out
    for sid in ("kid-running", "710907bf", "kid-interactive", "kid-remote"):
        assert f"reap-candidate {sid}" not in out


def test_every_skip_is_named_by_its_reason(tmp_path):
    main = _project(tmp_path)
    out, _ = _run(tmp_path, main)
    assert "skip 710907bf: repo-root" in out
    assert "skip kid-running: not-exited" in out
    assert "skip kid-interactive: not-interactive" in out
    assert "skip kid-remote: not-interactive" in out


def test_default_is_a_dry_run_and_never_invokes_rm(tmp_path):
    main = _project(tmp_path)
    out, recorded = _run(tmp_path, main)
    assert recorded == [["agents", "--json", "--all"]]
    assert "dry-run: 1 candidate(s)" in out
    assert "rm" not in [a[0] for a in recorded]


def test_live_reaps_exactly_the_candidate_with_a_bare_rm(tmp_path):
    main = _project(tmp_path)
    _, recorded = _run(tmp_path, main, "--live")
    assert recorded[1:] == [["rm", "kid-exited"]]
    blob = json.dumps(recorded)
    for sid in ("710907bf", "kid-running", "kid-interactive", "kid-remote"):
        assert sid not in blob


def test_the_rm_argv_never_carries_the_force_flags():
    sys.path.insert(0, str(HEAL.parent))
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location("heal_under_test", HEAL)
        heal = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(heal)
    finally:
        sys.path.pop(0)
    assert heal._reap_argv("claude", "abc") == ["claude", "rm", "abc"]
    for flag in ("--discard-unpushed", "--force-remove-worktree"):
        assert flag not in heal._reap_argv("claude", "abc")


def test_a_worktree_shaped_but_not_a_kid_name_is_refused(tmp_path):
    main = _project(tmp_path)
    odd = main / ".agi" / "worktrees" / "a00x-nope"
    odd.mkdir(parents=True)
    bindir, rec = _fake_claude(tmp_path, [
        {"id": "odd", "kind": "background", "state": "done", "cwd": str(odd)}])
    env = dict(os.environ, PATH=bindir + os.pathsep + os.environ["PATH"],
               CLAUDE_FAKE_ARGV=str(rec),
               CLAUDE_FAKE_FIXTURE=str(tmp_path / "fixture.json"))
    r = subprocess.run([sys.executable, str(HEAL), "session-reap",
                        "--root", str(main), "--live"],
                       capture_output=True, text=True, env=env)
    assert r.returncode == 0, r.stderr
    assert "skip odd: not-a-kid-worktree" in r.stdout
    assert ["rm", "odd"] not in [json.loads(l) for l in rec.read_text().splitlines()]
