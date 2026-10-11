"""goal:g1.41 lane C, the LEGACY arm -- guard-init.sh runs as root and, when config:guard is missing, read a
legacy guard.env by `.`-sourcing it. It now goes through guard_env_load (plain mode): the same grammar and the
same refusal as the node block, BEFORE anything runs. (The node block's own rows live in guard-env.t.sh.)
"""
from __future__ import annotations

import os
import subprocess
from pathlib import Path

GUARD = Path(__file__).resolve().parents[1] / "guard"


def legacy(tmp_path: Path, text: str) -> tuple[subprocess.CompletedProcess, Path]:
    sanct = tmp_path / "sanct"
    (sanct / "guard").mkdir(parents=True)
    (sanct / "guard" / "guard.env").write_text(text)
    env = {"PATH": os.environ["PATH"], "HOME": str(tmp_path), "GUARD_ENV_NODE": str(tmp_path / "absent.md"),
           "GUARD_BOX": "t", "GUARD_SANCTUARY": str(sanct)}
    r = subprocess.run(["bash", str(GUARD / "guard-init.sh"), "--dry-run", "--user", "nobody"], env=env,
                       capture_output=True, text=True, cwd=str(tmp_path))
    return r, tmp_path / "MARK"


def test_a_hostile_legacy_guard_env_is_refused_and_never_run(tmp_path):
    r, marker = legacy(tmp_path, "GUARD_PSI_FULL_t=60\nGUARD_X_t=$(touch %s)\n" % (tmp_path / "MARK"))
    assert r.returncode != 0 and "line 2 refused" in r.stderr, (r.stdout, r.stderr)
    assert not marker.exists(), "guard-init.sh sourced the legacy guard.env before validating it"


def test_a_shell_command_line_in_the_legacy_file_is_refused(tmp_path):
    r, marker = legacy(tmp_path, "touch %s\n" % (tmp_path / "MARK"))
    assert r.returncode != 0 and "line 1 refused" in r.stderr, (r.stdout, r.stderr)
    assert not marker.exists()


def test_a_clean_legacy_guard_env_still_loads(tmp_path):
    """Control: the fallback is kept, so a valid file is read and named as the settings source."""
    r, _ = legacy(tmp_path, "# a comment\n\nGUARD_PSI_FULL_t=60\n")
    assert r.returncode == 0 and "legacy" in r.stdout, (r.stdout, r.stderr)
