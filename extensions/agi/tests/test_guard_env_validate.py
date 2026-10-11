"""goal:g1.41 lane C, the LEGACY arm -- RETIRED. guard-init.sh runs as root; it used to `.`-source a legacy guard.env
when config:guard was missing. A legacy file predates box-keyed cells (GUARD_<CELL>_<box key>) and a box may
still carry one until its layer-5 install moves it aside, so the arm is gone: a stray file is REFUSED BY NAME and never read. A box that still
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


NODE = "# x\n```sh guard.env\nGUARD_PSI_FULL_t=60\n```\n"


def test_a_stray_legacy_file_is_refused_when_the_node_is_present_too(tmp_path):
    """The die is above the node test: a legacy file beside a present config:guard is named, never left unmentioned."""
    r = run(tmp_path, "GUARD_X_t=$(touch %s)\n" % (tmp_path / "MARK"), node=NODE)
    assert r.returncode != 0 and FIX in r.stderr, (r.stdout, r.stderr)
    assert not (tmp_path / "MARK").exists()


def test_a_present_node_alone_is_read(tmp_path):
    """Control: with no stray file the node is read and named as the settings source."""
    r = run(tmp_path, None, node=NODE)
    assert r.returncode == 0 and "settings        config:guard" in r.stdout, (r.stdout, r.stderr)


def test_the_header_and_the_node_block_no_longer_say_a_legacy_file_is_read_or_evaluated():
    """The text operators edit under must match the code: nothing is 'evaluated as bash', no legacy file is 'read'."""
    init = (GUARD / "guard-init.sh").read_text()
    node = (GUARD.parents[2] / ".agi" / "nodes" / ".geometry" / "guard.md").read_text()
    assert "is read only when the node is missing" not in init
    assert "evaluated as bash" not in node and "evaluates it as bash" not in node
    assert "read by guard_env_load: validated, never evaluated" in node
