"""hypothesis:a-run-key-is-reserved-atomically-so-concurrent-runs-never-share-one.

8 real PROCESSES mint a run key in one tmp root at the same instant -> 8
distinct keys, and the first still gets the unsuffixed name. A sequential
re-run's key keeps the `-2, -3, ...` shape. No test touches the live
`.agi/sessions/workflows/runs`.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

BIN = Path(__file__).resolve().parents[1] / "bin"
sys.path.insert(0, str(BIN))

import workflow as _wf  # noqa: E402

_CHILD = (
    "import sys;from pathlib import Path;sys.path.insert(0, %r);"
    "import workflow as wf;print(wf._mint_run_key(Path(sys.argv[1]), sys.argv[2], {}))"
    % (str(BIN),)
)


def _mint(root: Path, key: str = "mur-probe") -> str:
    out = subprocess.run([sys.executable, "-c", _CHILD, str(root), key],
                         capture_output=True, text=True, timeout=120)
    assert out.returncode == 0, out.stderr
    return out.stdout.strip()


def test_eight_concurrent_processes_mint_eight_distinct_keys(tmp_path):
    (tmp_path / "sessions" / "workflows").mkdir(parents=True)
    procs = [subprocess.Popen([sys.executable, "-c", _CHILD, str(tmp_path),
                               "mur-probe"], stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE, text=True) for _ in range(8)]
    outs = [p.communicate(timeout=120) for p in procs]
    assert not [e for _o, e in outs if e.strip()], outs
    keys = [o.strip() for o, _e in outs]
    assert len(set(keys)) == 8, keys
    assert "mp" in keys, keys  # a single launch's key is unchanged


def test_sequential_rerun_decollides_and_stale_marker_is_skipped(tmp_path):
    (tmp_path / "sessions" / "workflows").mkdir(parents=True)
    first = _mint(tmp_path)
    second = _mint(tmp_path)
    assert first == "mp" and second == "mp-2", (first, second)
    marker = tmp_path / "run-keys" / f"{first}.lock"
    assert marker.is_file()  # the reservation is on disk
    (tmp_path / "run-keys" / "mp-3.lock").touch()
    assert _mint(tmp_path) == "mp-4"  # crashed holder: skipped, never hung


def test_unwritable_marker_dir_never_raises(tmp_path):
    keys = tmp_path / "run-keys"
    keys.mkdir(parents=True)
    keys.chmod(0o500)
    try:
        got = _wf._mint_run_key(tmp_path, "mur-probe", {})
        assert got.startswith("mp-") and got != "mp", got
    finally:
        keys.chmod(0o700)
