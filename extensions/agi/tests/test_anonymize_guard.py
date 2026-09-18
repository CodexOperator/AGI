"""SM.122 — hypothesis:l4-anonymized-info-shims-and-a-physical-token-guard.

The guard (`bin/anonymize.py`), the sanctioned-facts reader (`bin/agi-boxinfo`),
the raw-tool shims (`shims/`), and the verification quick-level entry. Every
test builds a FAKE box from a fixture; no test reads or prints this box's
physical values.
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
SHIMS = Path(__file__).resolve().parents[1] / "shims"


def _load(name):
    spec = importlib.util.spec_from_file_location(name, BIN / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


anonymize = _load("anonymize")

FIXTURE = {
    "hostname": ["fixture-host-abc"],
    "ip": ["10.9.8.7"],
    "mac": ["aa:bb:cc:dd:ee:ff"],
    "board": ["FIXTURE-BOARD-1"],
    "secret": ["sk-fake-secret-abc"],
}


@pytest.fixture
def fake_box(tmp_path, monkeypatch):
    """A fake-box denylist source; the live box is never consulted."""
    p = tmp_path / "fixture.json"
    p.write_text(json.dumps(FIXTURE))
    monkeypatch.setenv("AGI_ANONYMIZE_FIXTURE", str(p))
    return p


def _graph(tmp_path: Path) -> Path:
    root = tmp_path / ".agi"
    (root / "nodes" / ".geometry").mkdir(parents=True, exist_ok=True)
    (root / "config.json").write_text("{}\n")
    return root


# (1) the denylist is built from the fake box, and only CLASSES come back.
def test_denylist_built_from_fake_box_and_names_classes_only(tmp_path, fake_box):
    toks = anonymize.box_tokens(tmp_path)
    assert dict(toks)  # something was collected
    hits = anonymize.scan("a line with fixture-host-abc and 10.9.8.7 in it", toks)
    assert hits == ["hostname", "ip"]
    # never a value, only class names
    assert all(h in anonymize.CLASSES for h in hits)


# (2) a diff carrying a fixture hostname/IP/MAC/board token is REFUSED BY
# CLASS, and the refused value never reaches the output.
def test_check_refuses_by_class_and_never_prints_value(tmp_path, fake_box, capsys):
    root = _graph(tmp_path)
    text = "diff line aa:bb:cc:dd:ee:ff and FIXTURE-BOARD-1\n"
    rc = anonymize.cmd_check(root, text, None)
    out = capsys.readouterr()
    assert rc == 1
    assert "REFUSED" in out.err
    assert "mac" in out.err and "board" in out.err
    for value in ("aa:bb:cc:dd:ee:ff", "FIXTURE-BOARD-1"):
        assert value not in out.err and value not in out.out


# (3) an alias-only diff passes and is not touched.
def test_alias_only_diff_passes(tmp_path, fake_box, capsys):
    root = _graph(tmp_path)
    rc = anonymize.cmd_check(root, "box: core-town gpu_memory_mib: 8192\n", None)
    out = capsys.readouterr()
    assert rc == 0
    assert "ok" in out.out


# (4) the verification QUICK level runs the guard and it refuses the same way.
def test_verification_quick_level_runs_anonymize(tmp_path, fake_box, monkeypatch):
    import verification
    root = _graph(tmp_path)
    names = []

    def fake_run_check(groot, name, verbose):
        names.append(name)
        return verification.CheckResult(name, "PASS", 0.0)

    monkeypatch.setattr(verification, "run_check", fake_run_check)
    results = verification.run_level(root, "quick", suite=False, verbose=False)
    assert "anonymize" in [r.name for r in results]
    # the same command the check spawns refuses / passes identically
    env = dict(os.environ)
    argv = [sys.executable, str(BIN / "anonymize.py"), "check",
            "--root", str(root)]
    bad = subprocess.run(argv + ["--text", "fixture-host-abc"],
                         capture_output=True, text=True, env=env)
    assert bad.returncode == 1 and "hostname" in bad.stderr
    good = subprocess.run(argv + ["--text", "box: core-town"],
                          capture_output=True, text=True, env=env)
    assert good.returncode == 0


# (5) each shim drops the physical lines and keeps class-level facts, driven
# by a fake raw tool so no real hardware is read.
@pytest.mark.parametrize("tool", ["nvidia-smi", "dmidecode", "lshw",
                                  "hostnamectl", "lspci"])
def test_shim_drops_physical_lines(tmp_path, tool):
    fake = tmp_path / "real"
    fake.mkdir()
    (fake / tool).write_text(
        "#!/usr/bin/env bash\n"
        "echo 'HOSTNAME: fixture-host-abc'\n"
        "echo '  Serial Number: FIXTURE-SERIAL-9'\n"
        "echo '  Product Name: FIXTURE-BOARD-1'\n"
        "echo '  link/ether aa:bb:cc:dd:ee:ff'\n"
        "echo '  inet 10.9.8.7/24'\n"
        "echo '  class: display'\n")
    (fake / tool).chmod(0o755)
    env = dict(os.environ, PATH=os.pathsep.join(
        [str(fake)] + [p for p in os.environ.get("PATH", "").split(os.pathsep)
                       if p]))
    out = subprocess.run([str(SHIMS / tool)], capture_output=True, text=True,
                         env=env).stdout
    for value in ("fixture-host-abc", "FIXTURE-SERIAL-9", "FIXTURE-BOARD-1",
                  "aa:bb:cc:dd:ee:ff", "10.9.8.7"):
        assert value not in out
    if tool != "nvidia-smi":
        assert "class: display" in out
    else:
        assert "gpu: present" in out


# (6) agi-boxinfo prints ONLY sanctioned, class-level facts.
def test_boxinfo_prints_only_sanctioned_facts(tmp_path):
    env = dict(os.environ, AGI_BOX="core-town")
    out = subprocess.run([sys.executable, str(BIN / "agi-boxinfo")],
                         capture_output=True, text=True, env=env).stdout
    allowed = ("box:", "gpu:", "gpu_memory_mib:", "ram_mib:", "disk_free_mib:",
               "load:", "uptime_s:")
    for line in out.splitlines():
        assert line.startswith(allowed), f"unsanctioned fact line: {line!r}"
    assert "box: core-town" in out


# (7) install-hook writes a box-local pre-commit, and refuses a foreign one.
def test_install_hook_writes_box_local_and_refuses_foreign(tmp_path):
    root = _graph(tmp_path)
    hooks = tmp_path / "hooks"
    rc = anonymize.cmd_install_hook(root, str(hooks))
    assert rc == 0
    dest = hooks / "pre-commit"
    body = dest.read_text()
    assert "anonymize" in body and os.access(dest, os.X_OK)
    foreign = tmp_path / "foreign"
    foreign.mkdir()
    (foreign / "pre-commit").write_text("#!/bin/sh\necho hi\n")
    assert anonymize.cmd_install_hook(root, str(foreign)) == 1
