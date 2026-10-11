"""goal:g1.41 lane C, the LEGACY arm -- RETIRED. guard-init.sh runs as root; it used to `.`-source a legacy guard.env
when config:guard was missing. The box's file was set aside on 09-30 and a legacy file predates box-keyed cells
(GUARD_<CELL>_<box key>), so the arm is gone: a stray file is REFUSED BY NAME and never read. A box that still
carries one learns it at the next run instead of having it sourced or silently ignored.
(The node block's own rows live in guard-env.t.sh.)
"""
from __future__ import annotations

import os
import subprocess
from pathlib import Path

GUARD = Path(__file__).resolve().parents[1] / "guard"
FIX = "legacy file predates box-keyed cells (GUARD_<CELL>_<box key>)"


def run(tmp_path: Path, legacy: str | None, node: str | None = None) -> subprocess.CompletedProcess:
    sanct = tmp_path / "sanct"
    (sanct / "guard").mkdir(parents=True)
    if legacy is not None:
        (sanct / "guard" / "guard.env").write_text(legacy)
    nodep = tmp_path / "node.md"
    if node is not None:
        nodep.write_text(node)
    env = {"PATH": os.environ["PATH"], "HOME": str(tmp_path), "GUARD_ENV_NODE": str(nodep), "GUARD_BOX": "t",
           "GUARD_SANCTUARY": str(sanct)}
    return subprocess.run(["bash", str(GUARD / "guard-init.sh"), "--dry-run", "--user", "nobody"], env=env,
                          capture_output=True, text=True, cwd=str(tmp_path))


def test_a_hostile_legacy_guard_env_is_refused_by_name_and_never_run(tmp_path):
    r = run(tmp_path, "GUARD_PSI_FULL_t=60\nGUARD_X_t=$(touch %s)\n" % (tmp_path / "MARK"))
    assert r.returncode != 0 and FIX in r.stderr, (r.stdout, r.stderr)
    assert not (tmp_path / "MARK").exists(), "guard-init.sh sourced the legacy guard.env"


def test_a_clean_legacy_guard_env_is_refused_too_not_silently_read(tmp_path):
    """The retirement is for every legacy file: even a valid-looking one is named, never loaded as settings."""
    r = run(tmp_path, "# a comment\nGUARD_PSI_FULL_t=60\n")
    assert r.returncode != 0 and FIX in r.stderr, (r.stdout, r.stderr)
    assert "settings        legacy" not in r.stdout


def test_a_fenceless_or_half_fenced_legacy_file_is_refused_whole(tmp_path):
    """Plain mode is gone: a bare ``` line in a legacy file cannot load the half above it."""
    r = run(tmp_path, "GUARD_PSI_FULL_t=60\n```\nGUARD_X_t=$(touch %s)\n" % (tmp_path / "MARK"))
    assert r.returncode != 0 and FIX in r.stderr and not (tmp_path / "MARK").exists(), (r.stdout, r.stderr)


def test_no_legacy_file_and_no_node_runs_on_defaults(tmp_path):
    """Control: the retirement refuses a file that exists, not the absence of one."""
    r = run(tmp_path, None)
    assert r.returncode == 0 and "settings        defaults" in r.stdout, (r.stdout, r.stderr)


def test_a_present_node_is_read_and_the_stray_legacy_file_is_not_consulted(tmp_path):
    """Control: with config:guard present the legacy branch is not reached (it was an else arm, still is)."""
    r = run(tmp_path, "GUARD_X_t=$(touch %s)\n" % (tmp_path / "MARK"),
            node="# x\n```sh guard.env\nGUARD_PSI_FULL_t=60\n```\n")
    assert r.returncode == 0 and "settings        config:guard" in r.stdout, (r.stdout, r.stderr)
    assert not (tmp_path / "MARK").exists()
