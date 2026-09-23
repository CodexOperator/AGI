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


# (1b) loopback and link-local addresses are skipped; every other address and
# the MAC still come through. The synthetic `ip -o addr` output is the only
# input; the live box is never consulted (the fixture path returns early).
IP_ADDR_OUT = """\
1: lo    inet 127.0.0.1/8 scope host lo
1: lo    inet6 ::1/128 scope host
2: eth0    inet 192.0.2.10/24 brd 192.0.2.255 scope global eth0
2: eth0    inet6 2001:db8::1/64 scope global
2: eth0    inet6 fe80::1/64 scope link
2: eth0    link/ether aa:bb:cc:dd:ee:ff brd ff:ff:ff:ff:ff:ff
3: eth1    inet 169.254.1.1/16 scope link
"""


def test_loopback_and_link_local_skipped_others_kept(tmp_path, monkeypatch):
    monkeypatch.delenv("AGI_ANONYMIZE_FIXTURE", raising=False)
    monkeypatch.setattr(anonymize, "_run",
                        lambda argv: IP_ADDR_OUT if argv[:3] == ["ip", "-o", "addr"] else "")
    monkeypatch.setattr(anonymize, "_secret_tokens", lambda root: [])
    toks = anonymize.box_tokens(tmp_path)
    ip_values = {v for c, v in toks if c == "ip"}
    for gone in ("127.0.0.1", "::1", "169.254.1.1", "fe80::1"):
        assert gone not in ip_values, gone
    for kept in ("192.0.2.10", "2001:db8::1"):
        assert kept in ip_values, kept
    assert ("mac", "aa:bb:cc:dd:ee:ff") in toks
    # a note naming a local server is no longer refused by the ip class
    assert anonymize.scan("llama-server on 127.0.0.1:8080",
                          [t for t in toks if t[0] == "ip"]) == []
    # a real routable address is still refused
    assert anonymize.scan("peer 192.0.2.10",
                          [t for t in toks if t[0] == "ip"]) == ["ip"]


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


# (1c) a key named ONLY under required_any is collected into the physical-token
# denylist; a key the node does not name is not. Fixture values only.
def test_secret_tokens_reads_required_any_groups(tmp_path, fake_box):
    root = _graph(tmp_path)
    (root / "nodes" / ".geometry" / "secrets.md").write_text(
        "---\n"
        'id: "config:secrets"\n'
        "type: config\n"
        "status: active\n"
        "mint_id: 0123456789abcdef0123456789abcdef\n"
        'title: "fixture secrets node"\n'
        "locations:\n"
        "  env_file:\n"
        '    path: "<source_root>/.env"\n'
        "  env_template:\n"
        '    path: "<source_root>/.env.example"\n'
        "required_keys: []\n"
        "required_any:\n"
        '  - ["FIXTURE_ONLY_KEY"]\n'
        "---\n\n"
        "body\n"
    )
    env = tmp_path / ".env"
    env.write_text(
        "FIXTURE_ONLY_KEY=sk-fake-required-any-only\n"
        "UNLISTED_KEY=sk-fake-not-declared\n"
    )
    env.chmod(0o600)
    toks = anonymize._secret_tokens(root)
    assert ("secret", "sk-fake-required-any-only") in toks
    assert ("secret", "sk-fake-not-declared") not in toks


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
