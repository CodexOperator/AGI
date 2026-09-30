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
import re
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


# (8) the installed hook passes --root = the SOURCE (repo) root, while the
# secrets node lives under the GRAPH root (<repo>/.agi/nodes/.geometry). The
# guard must still resolve it and refuse a declared key's env value -- before
# this fix `--root <repo root>` read <repo>/nodes/.geometry/secrets.md, found
# nothing, and checked ZERO secret values (goal:g15.29.16).
SECRETS_NODE_FIXTURE = (
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
    "required_keys: [FIXTURE_GUARD_KEY]\n"
    "---\n\nbody\n"
)


def test_check_from_repo_root_refuses_declared_key_value(tmp_path, monkeypatch):
    """`anonymize.py check --root <repo root>` refuses text carrying a value
    of a key the graph's secrets node declares."""
    root = _graph(tmp_path)                     # <tmp>/.agi graph root
    (root / "nodes" / ".geometry" / "secrets.md").write_text(SECRETS_NODE_FIXTURE)
    env = tmp_path / ".env"                    # <source_root>/.env == <tmp>/.env
    env.write_text("FIXTURE_GUARD_KEY=sk-fake-guard-value\n")
    env.chmod(0o600)
    monkeypatch.delenv("AGI_ANONYMIZE_FIXTURE", raising=False)
    monkeypatch.setattr(anonymize, "_run", lambda argv: "")  # no live `ip`
    # the repo root, exactly as cmd_install_hook writes it
    assert ("secret", "sk-fake-guard-value") in anonymize._secret_tokens(tmp_path)
    text = "diff line carrying sk-fake-guard-value here\n"
    assert "secret" in anonymize.scan(text, anonymize.box_tokens(tmp_path))
    assert anonymize.cmd_check(tmp_path, text, None) == 1


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


# (8) goal:g7.16.1.1.3 · hypothesis:anonymize-check-refuses-the-home-path: the
# box user's home path is one more token, read from HOME in every mode (it is
# not hardware, so the fixture path carries it too). A tmp HOME only. Strict
# xfail on the trunk at 32ef9a785; green since director-general-3's build.
def test_check_refuses_the_home_path(tmp_path, fake_box, monkeypatch, capsys):
    home = str(tmp_path / "home" / "someuser")
    monkeypatch.setenv("HOME", home)
    root = _graph(tmp_path)
    assert anonymize.scan(f"see {home}/x.md", anonymize.box_tokens(root)) == ["home"]
    assert anonymize.cmd_check(root, f"see {home}/x.md\n", None) == 1
    assert home not in capsys.readouterr().err


# (9) the home token rides the LIVE path too (anonymize.py box_tokens tail), not
# only the fixture return (mur wf_a56d005b-d6b row 11). No fixture: the box
# readers are stubbed, so nothing of this box is read; a tmp HOME only.
def test_the_live_path_carries_the_home_token(tmp_path, monkeypatch):
    home = str(tmp_path / "home" / "someuser")
    monkeypatch.setenv("HOME", home)
    monkeypatch.delenv("AGI_ANONYMIZE_FIXTURE", raising=False)
    monkeypatch.setattr(anonymize, "_run", lambda argv: "")
    monkeypatch.setattr(anonymize, "_secret_tokens", lambda root: [])
    monkeypatch.setattr(anonymize, "DMI", tmp_path / "no-dmi")
    monkeypatch.setattr(anonymize.socket, "gethostname", lambda: "stub-host-abc")
    monkeypatch.setattr(anonymize.socket, "getfqdn", lambda: "stub-host-abc")
    toks = anonymize.box_tokens(tmp_path)
    assert ("home", home) in toks
    assert anonymize.scan(f"see {home}/x.md", toks) == ["home"]


# (10) sanctuary-master mur wf_a56d005b-d6b residue 12: a staged diff is judged
# on its ADDED lines only -- a scrub removing the home path must not refuse
# itself -- while an added line carrying it still refuses.
def test_a_diff_is_judged_on_added_lines_only(tmp_path, fake_box, monkeypatch):
    home = str(tmp_path / "home" / "someuser")
    monkeypatch.setenv("HOME", home)
    root = _graph(tmp_path)
    scrub = tmp_path / "scrub.diff"
    scrub.write_text(f"diff --git a/n.md b/n.md\n@@ -1 +1 @@\n-see {home}/x\n+see <home>/x\n")
    assert anonymize.cmd_check(root, None, str(scrub)) == 0
    leak = tmp_path / "leak.diff"
    leak.write_text(f"diff --git a/n.md b/n.md\n@@ -1 +1 @@\n-see <home>/x\n+see {home}/x\n")
    assert anonymize.cmd_check(root, None, str(leak)) == 1


# (11) re-mur wf_aa3f01d4-2aa residue 21: the STAGED branch -- the one
# verification runs, cmd_check(root, None, None) -> `git diff --cached` -- is
# judged on added lines too; _run is stubbed, no real git or index is read.
def test_the_staged_diff_is_judged_on_added_lines_only(tmp_path, fake_box, monkeypatch):
    home = str(tmp_path / "home" / "someuser")
    monkeypatch.setenv("HOME", home)
    root = _graph(tmp_path)
    for staged, rc in ((f"-see {home}/x\n+see <home>/x\n", 0),
                       (f"-see <home>/x\n+see {home}/x\n", 1)):
        diff = f"diff --git a/n.md b/n.md\n@@ -1 +1 @@\n{staged}"
        monkeypatch.setattr(anonymize, "_run",
                            lambda argv, d=diff: d if "--cached" in argv else "")
        assert anonymize.cmd_check(root, None, None) == rc


# (12) re-mur wf_aa3f01d4-2aa residue 22: added-lines-only must not loosen the
# guard. A post-image PATH (new file, '+++ b/', 'rename to') and an added
# content line that starts '++' (shown '+++...') still refuse; a pre-image
# path (the file a scrub renames away) does not.
@pytest.mark.parametrize("diff, want", [
    ("diff --git a/n b/{h}/n\nnew file mode 100644\n--- /dev/null\n+++ b/{h}/n\n@@ -0,0 +1 @@\n+x\n", 1),
    ("diff --git a/n b/m\nsimilarity index 100%\nrename from n\nrename to {h}/m\n", 1),
    ("diff --git a/n b/n\n--- a/n\n+++ b/n\n@@ -1 +1 @@\n-x\n+++{h}\n", 1),
    ("diff --git a/{h}/n b/n\nsimilarity index 100%\nrename from {h}/n\nrename to n\n", 0),
    ("diff --git a/{h}/n b/{h}/n\ndeleted file mode 100644\n--- a/{h}/n\n+++ /dev/null\n@@ -1 +0,0 @@\n-x\n", 0),
    # residue 31, real `git diff --cached -U0` shapes: no '+++' line for these
    ("diff --git a/{h}/.gitkeep b/{h}/.gitkeep\nnew file mode 100644\nindex 0000000..e69de29\n", 1),
    ("diff --git a/{h}/b.bin b/{h}/b.bin\nnew file mode 100644\nindex 0000000..bdc955b\nBinary files /dev/null and b/{h}/b.bin differ\n", 1),
    ("diff --git a/{h}/b.bin b/{h}/b.bin\ndeleted file mode 100644\nindex bdc955b..0000000\nBinary files a/{h}/b.bin and /dev/null differ\n", 0),
])
def test_added_lines_keeps_post_image_paths_and_plus_plus_content(
        tmp_path, fake_box, monkeypatch, diff, want):
    home = str(tmp_path / "home" / "someuser")
    monkeypatch.setenv("HOME", home)
    root = _graph(tmp_path)
    f = tmp_path / "d.diff"
    f.write_text(diff.format(h=home))
    assert anonymize.cmd_check(root, None, str(f)) == want


# (12) goal:g7.16.1.2.3 · hypothesis:anonymize-refuses-any-box-home-by-one-generic-class:
# ANY box's home refuses by one generic class, never a literal list; the
# placeholder forms (`<home>/`, `~/`, `/home/<x>/`) stay allowed. Strict xfail:
# RED on the trunk at ef73dec71 (council bundle 2, director-general-2);
# green since director-general-3's build (scan's generic class).
def test_any_box_home_is_refused_by_one_generic_class(tmp_path, fake_box, monkeypatch):
    monkeypatch.setenv("HOME", str(tmp_path / "h" / "me"))
    root = _graph(tmp_path)
    toks = anonymize.box_tokens(root)
    seg = "someone"  # a made-up segment, joined at runtime so no literal home path is committed
    for other in ("/" + "home/" + seg + "/x.md", "/" + "Users/" + seg + "/x.md"):
        assert anonymize.scan(f"see {other}", toks) == ["home"]
        assert anonymize.cmd_check(root, f"see {other}\n", None) == 1
    assert anonymize.scan("see <home>/x.md, ~/x.md and /home/<x>/y", toks) == []


# bundle 2 residue 46 (sanctuary-master re-mur wf_f6343a9c-419): a BARE home --
# no trailing slash -- is the same class; the rewrite keeps the terminator.
def test_a_bare_home_is_the_same_generic_class(tmp_path, fake_box, monkeypatch):
    monkeypatch.setenv("HOME", str(tmp_path / "h" / "me"))
    toks = anonymize.box_tokens(_graph(tmp_path))
    bare = "/" + "home/" + "zqxwv"  # made up, joined at runtime
    for text in (f"for {bare}", f"pre-set for {bare} at spawn", f'"{bare}"'):
        assert anonymize.scan(text, toks) == ["home"], text
    assert anonymize.home_relative(f"for {bare} at spawn", home="/h/me") == "for <home> at spawn"
    assert anonymize.scan("see /home/<seg> and ~/x", toks) == []


def test_prose_naming_the_home_dir_is_not_a_home(tmp_path, fake_box, monkeypatch):
    """The segment is a user name: `/home/,` in prose never matches (residue 46 follow-up)."""
    monkeypatch.setenv("HOME", str(tmp_path / "h" / "me"))
    toks = anonymize.box_tokens(_graph(tmp_path))
    assert anonymize.scan("anonymize grep (user name, /home/, IPs)", toks) == []
    assert anonymize.scan("a tmp HOME: <tmp>/home/.npm-global/bin/pi", toks) == []
    assert anonymize.home_relative("for /" + "home/zqxwv, next", home="/h/me") == "for <home>, next"


# SM residue 128: a home OUTSIDE /home and /Users passed the gate (the council's
# home-path row went false green). The roots are derived from the box -- a login
# home from pwd, and the config cell anonymize.home_roots -- never a literal
# list. A fixture user; every path joined at runtime, no real home committed.
def test_a_login_home_outside_home_and_users_is_refused(tmp_path, fake_box, monkeypatch):
    import pwd
    user = "fixtureuser"
    fixture_home = "/" + "data/" + user
    monkeypatch.setattr(pwd, "getpwall", lambda: [pwd.struct_passwd(
        (user, "x", 4242, 4242, "", fixture_home, "/bin/sh"))])
    monkeypatch.setitem(sys.modules, "anonymize", anonymize)  # undo restores it
    mod = _load("anonymize")  # the pattern is derived at import
    monkeypatch.setenv("HOME", str(tmp_path / "h" / "me"))
    root = _graph(tmp_path)
    toks = mod.box_tokens(root)
    assert mod.scan(f"see {fixture_home}/x", toks) == ["home"]
    assert mod.cmd_check(root, f"see {fixture_home}/x\n", None) == 1
    assert mod.home_relative(f"at {fixture_home}/x", home="/h/me") == "at <home>/x"
    # the login home is matched whole, never as a prefix of a sibling
    assert mod.scan(f"see {fixture_home}x/y", toks) == []


def test_the_home_roots_cell_adds_a_root(tmp_path, monkeypatch):
    root = _graph(tmp_path)
    prefix = "/" + "data/home-"
    (root / "config.json").write_text(json.dumps({"anonymize": {"home_roots": [prefix]}}))
    rx = anonymize._home_path_re(root)
    assert rx.search(prefix + "fixtureuser/x")
    assert rx.sub(r"<home>\1", "at " + prefix + "fixtureuser/x") == "at <home>/x"
    assert not rx.search("/" + "data/work/agi/x"), "a non-home sibling stays clear"
    assert not rx.search(prefix), "the bare prefix is not a home"
    (root / "config.json").write_text("{}\n")
    assert not anonymize._home_path_re(root).search(prefix + "fixtureuser/x")


# bundle 3 row H4 b (goal:g7.16.1.3.2.3.1): the generic home class reaches 0
# over the four scrub scopes, read from COMMITTED bytes (`git grep HEAD`)
# through anonymize's ONE pattern -- never a new regex. Only FILE counts per
# scope come back; no matched text is ever printed.
SCRUB_SCOPES = (".agi/sessions/rotations", ".agi/sessions/quorum", "datasets", ".agi/nodes", "skills")


def test_no_committed_home_path_in_the_four_scrub_scopes():
    repo = Path(__file__).resolve().parents[3]
    top = subprocess.run(["git", "-C", str(repo), "rev-parse", "--show-toplevel"],
                         capture_output=True, text=True)
    if top.returncode != 0 or Path(top.stdout.strip()).resolve() != repo:
        pytest.skip("not a git checkout of this repo")
    # council CM1: a scope that no longer exists would count 0 and pass while
    # checking nothing -- every scope must carry tracked files at HEAD first
    for scope in SCRUB_SCOPES:
        tracked = subprocess.run(["git", "-C", str(repo), "ls-tree", "-r", "--name-only", "HEAD", "--", scope],
                                 capture_output=True, text=True).stdout.split()
        assert tracked, f"scrub scope {scope!r} has no tracked file at HEAD: the guard would check nothing"
    p = subprocess.run(["git", "-C", str(repo), "grep", "-lP",
                        anonymize.HOME_PATH_RE.pattern, "HEAD", "--", *SCRUB_SCOPES],
                       capture_output=True, text=True)
    assert p.returncode in (0, 1), p.stderr[-200:]
    per = {s: sum(1 for f in p.stdout.splitlines() if f.startswith(f"HEAD:{s}/"))
           for s in SCRUB_SCOPES}
    assert per == dict.fromkeys(SCRUB_SCOPES, 0)


# goal:g1.31.3.2 (b) corrective dg6-03: the goal's invariant "no hardware model name,
# no box path, no pi-encoded repo path" certified at the COMMITTED tip. The guard
# above knows only the home class; anonymize.py has no box-path or class-label
# class (a hardware-fragment class belongs to the sibling dg6-04 round). So this
# row reads the round's own in-scope nodes at HEAD and counts hits per class:
# home = anonymize's ONE pattern; box = an absolute path under a mount/data root;
# pi = the pi-encoded (slashes -> dashes, `--` framed) form of such a path;
# hw = the card's bare model digits not carried by the class label GPU2070S.
# Only per-class FILE counts come back -- no matched text is ever printed. The
# round's goal and brief are out of scope: they NAME the patterns by design.
ROUND_NODES = (
    "hypothesis/lm-bonsai2-27b-abc-coding-test-on-the-8gb-box",
    "experiment/a00-797ee7be-e9c742",
    "experiment/a00-600cf080-0cd865-exp",
    "hypothesis/a00-600cf080-0cd865",
    "experiment/a00-2fa1fab0-b7d2a0",
    "experiment/a00-6b761b8c-b6ae8b",
    "experiment/a00-afb177f9-30e4e2",
)
ROUND_CLASSES = {
    "box": r"(?<![\w.<>-])/(?:mnt|data|srv|opt)/[A-Za-z]",
    "pi": r"(?<![\w-])--(?:mnt|data|srv|opt|home|Users)-[A-Za-z]",
    "hw": r"(?<!GPU)20" + r"70",
}


def test_round_nodes_carry_no_box_path_pi_path_or_bare_hardware_token_at_head():
    import re
    repo = Path(__file__).resolve().parents[3]
    top = subprocess.run(["git", "-C", str(repo), "rev-parse", "--show-toplevel"],
                         capture_output=True, text=True)
    if top.returncode != 0 or Path(top.stdout.strip()).resolve() != repo:
        pytest.skip("not a git checkout of this repo")
    classes = dict(ROUND_CLASSES, home=anonymize.HOME_PATH_RE.pattern)
    per = dict.fromkeys(classes, 0)
    for node in ROUND_NODES:
        shown = subprocess.run(["git", "-C", str(repo), "show", f"HEAD:.agi/nodes/{node}.md"],
                               capture_output=True, text=True)
        # a scope that vanished would count 0 and pass while checking nothing
        assert shown.returncode == 0 and shown.stdout, f"{node}: not a tracked node at HEAD"
        for cls, pat in classes.items():
            if re.search(pat, shown.stdout):
                per[cls] += 1
    assert per == dict.fromkeys(classes, 0)


# goal:g1.31.5.1.2: an email address is refused by ONE generic class `email`
# (like `home`: no token source), judged on ADDED lines, class printed never the
# value. The non-personal shapes are the config cell anonymize.email_allow, not
# code. Every address is SYNTHETIC and assembled at run time.
AT = "\x40"
ALLOW = [r"[^@]+@(?:[A-Za-z0-9-]+\.)*example\.(?:com|org|net)",
         r"[^@]+@openssh\.com", r"[^@]+@[0-9]+\.service"]


def _email_graph(tmp_path, allow=ALLOW):
    root = _graph(tmp_path)
    cfg = {"anonymize": {"email_allow": allow}} if allow is not None else {}
    (root / "config.json").write_text(json.dumps(cfg))
    return root


def test_email_a_synthetic_address_is_refused_by_class_never_value(tmp_path, fake_box, capsys):
    root = _email_graph(tmp_path)
    addr = "fixture.person" + AT + "example.invalid"
    assert anonymize.scan(f"reach {addr}", anonymize.box_tokens(root), anonymize._email_allow(root)) == ["email"]
    assert anonymize.cmd_check(root, f"reach {addr}\n", None) == 1
    err = capsys.readouterr().err
    assert "email" in err and addr not in err and "fixture.person" not in err
    assert "email" in anonymize.CLASSES


def test_email_allowed_shapes_pass(tmp_path, fake_box, capsys):
    root = _email_graph(tmp_path)
    toks = anonymize.box_tokens(root)
    allow = anonymize._email_allow(root)
    for shape in ("someone" + AT + "example.com", "someone" + AT + "mail.example.org",
                  "ssh-ed25519-cert-v01" + AT + "openssh.com", "user" + AT + "1000.service"):
        assert anonymize.scan(f"see {shape}", toks, allow) == [], shape
        assert anonymize.cmd_check(root, f"see {shape}\n", None) == 0, shape
    # a lookalike is NOT the allowed shape
    for bad in ("someone" + AT + "example.com.evil.io", "someone" + AT + "notopenssh.com",
                "someone" + AT + "x.service"):
        assert anonymize.scan(bad, toks, allow) == ["email"], bad
    capsys.readouterr()


def test_email_no_cell_allows_nothing_and_placeholders_never_match(tmp_path, fake_box):
    root = _email_graph(tmp_path, allow=None)
    toks = anonymize.box_tokens(root)
    assert anonymize._email_allow(root) == []
    assert anonymize.scan("a" + AT + "example.com", toks, anonymize._email_allow(root)) == ["email"]
    assert anonymize.scan("<user>" + AT + "<host>, <email>, @openssh.com", toks, []) == []


def test_email_is_judged_on_added_lines_only(tmp_path, fake_box, capsys):
    root = _email_graph(tmp_path)
    addr = "fixture.person" + AT + "example.invalid"
    diff = ("diff --git a/x.md b/x.md\n--- a/x.md\n+++ b/x.md\n@@ -1 +1 @@\n"
            f"-reach {addr}\n+reach <email>\n")
    assert anonymize.cmd_check(root, anonymize.added_lines(diff), None) == 0
    diff2 = diff.replace("-reach", "+reach", 1).replace("+reach <email>", " reach <email>")
    assert anonymize.cmd_check(root, anonymize.added_lines(diff2), None) == 1
    capsys.readouterr()


def test_email_allow_cell_lives_in_the_live_config():
    repo = Path(__file__).resolve().parents[3]
    cell = json.loads((repo / ".agi" / "config.json").read_text())["anonymize"]["email_allow"]
    assert cell and all(isinstance(c, str) for c in cell)




# ---- hypothesis:pb3-anonymize-refuses-a-hardware-model-fragment -------------
# Every value SYNTHETIC: a made-up card, a made-up cpu and a made-up pytest
# user. No row names a real model, no assertion prints a matched value, and no
# row reads this box: every live-path row goes through `_stub_box` (dg6-04
# residue 6 -- this file's own convention, docstring above).
FAKE_HW = "Fixturo Vexel ZX 9990 ULTRA"
FAKE_CPU = "Fixturo Zenix 7700 QX"
FAKE_BOARD = "Fixturo Bords Vexel 9990"
FAKE_USER_PREFIX = "/" + "tmp/pytest-of-"
FAKE_HOME_ROOT = "/" + "home/"


@pytest.fixture(autouse=True)
def _fresh_hw_cache():
    """The source read is cached per process, so every row must start cold --
    AUTOFILE over the whole file, not only the hardware rows: the email and
    home rows read the SAME `anonymize` cell through a tmp project, and one
    row's cached source set leaking into the next is exactly the class of bug
    these rows exist to catch. The clear is a dict clear (2 dict ops, no tool
    run), so the whole-file cost is nil (dg6-04 residue 7)."""
    getattr(anonymize, "_HW_CACHE", {}).clear()
    yield
    getattr(anonymize, "_HW_CACHE", {}).clear()


def _stub_box(tmp_path, monkeypatch, tool_out=None):
    """The LIVE box_tokens path with EVERY reader stubbed: no `ip`, no shim, no
    DMI, no socket name, no $HOME, no secrets env. Returns the list of argv
    `_run` was asked to run; `tool_out` maps a tool's basename to its stdout."""
    monkeypatch.delenv("AGI_ANONYMIZE_FIXTURE", raising=False)
    monkeypatch.setenv("HOME", str(tmp_path / "home" / "someuser"))
    calls = []

    def fake_run(argv):
        calls.append(list(argv))
        return (tool_out or {}).get(Path(argv[0]).name, "")

    monkeypatch.setattr(anonymize, "_run", fake_run)
    monkeypatch.setattr(anonymize, "_secret_tokens", lambda root: [])
    monkeypatch.setattr(anonymize, "DMI", tmp_path / "no-dmi")
    monkeypatch.setattr(anonymize.socket, "gethostname", lambda: "stub-host-abc")
    monkeypatch.setattr(anonymize.socket, "getfqdn", lambda: "stub-host-abc")
    return calls


def _hw_calls(calls):
    """The argv that were NOT the (stubbed) `ip` reader: hardware tools."""
    return [c for c in calls if Path(c[0]).name != "ip"]


def _cell(root, anonymize_cell):
    (root / "config.json").write_text(json.dumps({"anonymize": anonymize_cell}))


def _hw_fixture(tmp_path, monkeypatch, name=FAKE_HW):
    p = tmp_path / "hwbox.json"
    p.write_text(json.dumps({"hardware": [name]}))
    monkeypatch.setenv("AGI_ANONYMIZE_FIXTURE", str(p))
    monkeypatch.setenv("HOME", str(tmp_path / "home" / "someuser"))
    return p


def test_a_hardware_fragment_is_refused_by_class_and_never_printed(
        tmp_path, monkeypatch, capsys):
    """F1 + F2 in one row: the 2-word FRAGMENT goes red by class, the class
    label and the bare numbers that ride the same box stay clean."""
    _hw_fixture(tmp_path, monkeypatch)
    toks = anonymize.box_tokens(tmp_path)
    assert anonymize.scan("loads fully on the 9990 ULTRA: 64/64 layers", toks) \
        == ["hardware"]
    assert anonymize.scan("the card GPU9990U, write.py:29990, 9990 MiB", toks) == []
    rc = anonymize.main(["check", "--root", str(_graph(tmp_path)),
                         "--text", "loads fully on the 9990 ULTRA"])
    err = capsys.readouterr().err
    assert rc == 1
    assert "hardware" in err and FAKE_HW not in err and "9990 ULTRA" not in err


def test_the_hardware_cell_source_is_refused_and_its_absence_runs_no_tool(
        tmp_path, monkeypatch):
    """F3: a fragment of a name in the cell's own source file is refused (a
    `@file` source runs no tool); with the cell absent there is NO hardware
    token and `_run` is asked for nothing but the box's own `ip` reader."""
    calls = _stub_box(tmp_path, monkeypatch)
    root = _graph(tmp_path)
    src = tmp_path / "box.txt"
    src.write_text("model_name: %s\nother: x\n" % FAKE_HW)
    _cell(root, {"hardware": {"sources": [["@" + str(src), "model_name"]],
                              "min_words": 2, "core_digits": 3}})
    toks = anonymize.box_tokens(root)
    assert anonymize.scan("runs the 9990 ULTRA here", toks) == ["hardware"]
    assert _hw_calls(calls) == []
    getattr(anonymize, "_HW_CACHE", {}).clear()
    calls.clear()
    _cell(root, {})
    toks = anonymize.box_tokens(root)
    assert not [1 for c, _ in toks if c == "hardware"]
    assert _hw_calls(calls) == [], "no cell: no hardware tool may run"
    assert anonymize.scan("runs the 9990 ULTRA here", toks) == []


def test_hardware_argv_sources_run_their_shim_once_per_process(tmp_path, monkeypatch):
    """Prime SHIM rule + residue: an argv source runs `shims/<tool>`, never the
    raw tool off PATH, and box_tokens() does not respawn it on every call."""
    calls = _stub_box(tmp_path, monkeypatch, {
        "nvidia-smi": FAKE_HW + "\n", "lscpu": "Model name: %s\n" % FAKE_CPU})
    root = _graph(tmp_path)
    _cell(root, {"hardware": {"sources": [
        ["nvidia-smi", "--query-gpu=name", "--format=csv,noheader"], ["lscpu"]],
        "min_words": 2, "core_digits": 3}})
    assert anonymize.SHIMS == SHIMS
    toks = anonymize.box_tokens(root)
    hw = _hw_calls(calls)
    assert sorted(Path(c[0]).name for c in hw) == ["lscpu", "nvidia-smi"]
    assert {Path(c[0]).parent for c in hw} == {SHIMS}, "a raw tool ran off PATH"
    assert hw[0][1:] == ["--query-gpu=name", "--format=csv,noheader"]
    assert anonymize.scan("on the 9990 ULTRA", toks) == ["hardware"]
    assert anonymize.scan("a Zenix 7700 part", toks) == ["hardware"]
    for _ in range(3):
        anonymize.box_tokens(root)
    assert len(_hw_calls(calls)) == 2, "the sources were re-run on a later call"


def test_an_absent_shim_is_an_absent_source_never_the_raw_tool(tmp_path, monkeypatch):
    calls = _stub_box(tmp_path, monkeypatch, {"nvidia-smi": FAKE_HW + "\n"})
    monkeypatch.setattr(anonymize, "SHIMS", tmp_path / "no-shims")
    root = _graph(tmp_path)
    _cell(root, {"hardware": {"sources": [["nvidia-smi", "--query-gpu=name"]],
                              "min_words": 2, "core_digits": 3}})
    toks = anonymize.box_tokens(root)
    assert _hw_calls(calls) == []
    assert not [1 for c, _ in toks if c == "hardware"]


def test_the_lscpu_shim_exists_and_is_executable():
    """The cell names `lscpu`: its shim must exist or the source silently dies."""
    shim = SHIMS / "lscpu"
    assert shim.is_file() and os.access(shim, os.X_OK)
    assert "_shim.py" in shim.read_text() and "lscpu" in shim.read_text()


def test_scan_without_a_root_never_reads_the_cell_of_its_own_module_path(
        tmp_path, monkeypatch):
    """dg6-04 root cause: scan(text, tokens) with no root resolved the project
    from the module's OWN file path, so a caller that never named a project got
    the repo's `user_roots` (and reddened two pre-existing rows under the
    default pytest basetemp). The module is pointed at a tmp project whose cell
    HAS user_roots: only a caller that names the root gets the class."""
    proj = tmp_path / "proj"
    (proj / ".agi").mkdir(parents=True)
    (proj / ".agi" / "config.json").write_text(
        json.dumps({"anonymize": {"user_roots": [FAKE_USER_PREFIX]}}))
    monkeypatch.setattr(anonymize, "__file__",
                        str(proj / "extensions" / "agi" / "bin" / "anonymize.py"))
    text = "basetemp " + FAKE_USER_PREFIX + "fixtureuser/pytest-3"
    assert anonymize.scan(text, []) == []
    assert anonymize.scan(text, [], root=proj) == ["user"]


def test_the_user_class_is_a_path_context_and_never_a_bare_word(tmp_path, monkeypatch):
    """F6 + the Prime's ruling (n144): a user name counts ONLY after a root
    prefix (`user_roots`, and the home roots), by the SAME segment builder as a
    home; a bare word -- or a token -- never does, and HOME_PATH_RE is
    untouched so the four-scope home test keeps its scope."""
    _stub_box(tmp_path, monkeypatch)
    root = _graph(tmp_path)
    _cell(root, {"user_roots": [FAKE_USER_PREFIX]})
    toks = anonymize.box_tokens(root)
    assert not [1 for _, v in toks if v == "fixtureuser"], "a bare user token"
    assert anonymize.scan("basetemp " + FAKE_USER_PREFIX + "fixtureuser/pytest-3",
                          toks, root=root) == ["user"]
    assert anonymize.scan("basetemp " + FAKE_USER_PREFIX + "<user>/pytest-3",
                          toks, root=root) == []
    assert anonymize.scan("the account fixtureuser, and " + FAKE_USER_PREFIX[5:] + "fixtureuser",
                          toks, root=root) == []
    assert anonymize.scan("see " + FAKE_HOME_ROOT + "fixtureuser/x", toks, root=root) == ["home"]
    assert not anonymize.HOME_PATH_RE.search(FAKE_USER_PREFIX + "fixtureuser/x"), \
        "the user prefix leaked into HOME_PATH_RE and would redden the scope test"


def test_the_refusal_advice_is_what_home_relative_substitutes(
        tmp_path, fake_box, monkeypatch, capsys):
    """dg6-04 missed: the refusal names a remedy, and the remedy must exist.
    home_relative() rewrites `home` and (given the root) `user`; it rewrites
    nothing else, so `hardware` says `by hand`."""
    home = str(tmp_path / "home" / "someuser")
    monkeypatch.setenv("HOME", home)
    root = _graph(tmp_path)
    _cell(root, {"user_roots": [FAKE_USER_PREFIX]})
    text = "see %sfixtureuser/a and %sfixtureuser/b\n" % (FAKE_USER_PREFIX, FAKE_HOME_ROOT)
    assert anonymize.scan(text, [], root=root) == ["home", "user"]
    fixed = anonymize.home_relative(text, home=home, root=root)
    assert FAKE_USER_PREFIX + "<user>/a" in fixed and "<home>/b" in fixed
    assert anonymize.scan(fixed, [], root=root) == []
    assert anonymize.cmd_check(root, text, None) == 1
    err = capsys.readouterr().err
    assert "user" in err and "<user>" in err and "home_relative" in err
    assert "fixtureuser" not in err
    hw = "loads on the 9990 ULTRA\n"
    assert anonymize.home_relative(hw, home=home, root=root) == hw
    assert set(anonymize.ADVICE) == {"home", "user", "hardware", "email"}


def test_a_bare_value_file_source_is_read_in_the_real_on_box_format(
        tmp_path, monkeypatch):
    """dg6-04 residue 2: the cell's `@/sys/class/dmi/id/board_name` source is
    INERT -- that file is ONE bare value line, no colon, so a `field` filter
    matched nothing and the board name went unguarded. The stub is written in
    the real on-box shape (one bare line, no colon) and the row asserts >= 1
    name; the field-filtered shape keeps working beside it."""
    calls = _stub_box(tmp_path, monkeypatch)
    root = _graph(tmp_path)
    bare = tmp_path / "board_name"
    bare.write_text(FAKE_BOARD + "\n")
    _cell(root, {"hardware": {"sources": [["@" + str(bare), "Board Name"]],
                              "min_words": 2, "core_digits": 3}})
    assert len(anonymize._read_hw_sources(
        {"sources": [["@" + str(bare), "Board Name"]]})) >= 1
    toks = anonymize.box_tokens(root)
    assert anonymize.scan("fitted the %s" % FAKE_BOARD, toks) == ["hardware"]
    assert _hw_calls(calls) == [], "a @file source runs no tool"
    keyed = tmp_path / "keyed"
    keyed.write_text("model_name: %s\n" % FAKE_HW)
    assert anonymize._read_hw_sources(
        {"sources": [["@" + str(keyed), "model_name"]]}) == [FAKE_HW]


def test_the_fixture_path_and_the_live_path_expand_one_rule(tmp_path, monkeypatch):
    """dg6-04 residue 8: fixture and live both go through _hw_tokens with the
    SAME cell, so with no `anonymize.hardware` cell a fixture name and a
    source-read name expand identically -- the fixture path expanding nothing
    while the live path expands is what would silently hollow out every row."""
    root = _graph(tmp_path)
    _cell(root, {})
    assert anonymize._hw_tokens([FAKE_HW], {}) == \
        anonymize._hw_tokens([FAKE_HW], {"min_words": 2, "core_digits": 3})
    _stub_box(tmp_path, monkeypatch, {"lscpu": FAKE_CPU + "\n"})
    _cell(root, {"hardware": {"sources": [["lscpu"]]}})
    live = anonymize.box_tokens(root)
    _cell(root, {})
    _hw_fixture(tmp_path, monkeypatch)
    fixture = anonymize.box_tokens(root)
    assert sorted(v for c, v in live if c == "hardware") and \
        sorted(v for c, v in fixture if c == "hardware")
    assert set(v for c, v in live if c == "hardware") <= \
        set(v for _, v in anonymize._hw_tokens([FAKE_CPU], {}))
    assert set(v for c, v in fixture if c == "hardware") <= \
        set(v for _, v in anonymize._hw_tokens([FAKE_HW], {}))


def test_a_reserved_invalid_tld_is_allowed_and_a_real_shape_is_not(
        tmp_path, fake_box):
    """dg6-04 residue 4: RFC 2606 reserves .invalid (and .test/.example), so
    the cell's allow-list must admit a doc address at example.invalid while a
    real-shaped address at a real domain is still refused. The pattern is a
    CONFIG cell value, not code: this row builds the cell the director lands."""
    root = _email_graph(tmp_path, allow=[
        r"[^@]+@(?:[A-Za-z0-9-]+\.)*example\.(?:com|org|net)",
        r"[^@]+@(?:[A-Za-z0-9-]+\.)*example\.invalid"])
    toks = anonymize.box_tokens(root)
    assert anonymize.scan("reach fixture.person" + AT + "example.invalid", toks,
                          anonymize._email_allow(root)) == []
    assert anonymize.scan("reach fixture.person" + AT + "corp.example", toks,
                          anonymize._email_allow(root)) == ["email"]
    live = json.loads((Path(__file__).resolve().parents[3] / ".agi" /
                       "config.json").read_text())["anonymize"]["email_allow"]
    if r"example\.invalid" not in " ".join(live):
        pytest.skip("the landed cell does not carry the .invalid pattern yet "
                    "(a round cannot commit .agi/config.json; the diff is in "
                    "the round's experiment node)")


def _cell_leaks(node, core_digits=3):
    """One count per string ANYWHERE in the cell (inside a list source or a
    nested dict, keys too) holding a word with a >= core_digits digit core: a
    model name, however spelled. Counts, never the string."""
    if isinstance(node, str):
        return [1 for w in re.findall(r"[A-Za-z0-9]+", node)
                if sum(ch.isdigit() for ch in w) >= core_digits]
    if isinstance(node, dict):
        return [n for k, v in node.items() for n in _cell_leaks(k) + _cell_leaks(v)]
    if isinstance(node, (list, tuple)):
        return [n for v in node for n in _cell_leaks(v)]
    return []


def test_the_no_leak_check_reaches_inside_list_sources_and_nested_values():
    """F4's checker, mutation-tested on FIXTURE cells (no repo read): the
    committed cell's sources are all LISTS, so a str-only walk was vacuous."""
    clean = {"sources": [["nvidia-smi", "--query-gpu=name", "--format=csv,noheader"],
                         ["lscpu"], ["@/sys/class/dmi/id/board_name", "Board Name"]],
             "min_words": 2, "core_digits": 3}
    assert _cell_leaks(clean) == []
    for leaked in (
            {"sources": [["nvidia-smi", FAKE_HW]]},
            {"sources": [["lscpu"], ["cat", "/x", "Model " + FAKE_CPU]]},
            {"sources": [["x"]], "extra": {"deep": [["GTX9990"]]}},
            {"sources": [FAKE_HW]}):
        assert _cell_leaks(leaked), leaked.keys()


def test_the_live_hardware_cell_declares_sources_and_no_model_name():
    """F4 on the repo's own cell -- skipped, never red, where the cell is not
    committed (a worktree branched before it, or the engine in another
    project); the checker itself is proved on fixtures above."""
    repo = Path(__file__).resolve().parents[3]
    cfg = repo / ".agi" / "config.json"
    if not cfg.is_file():
        pytest.skip("no .agi/config.json in this checkout")
    cell = (json.loads(cfg.read_text()).get("anonymize") or {}).get("hardware")
    if not cell:
        pytest.skip("this checkout carries no anonymize.hardware cell")
    assert cell.get("sources") and cell.get("min_words") and cell.get("core_digits")
    assert _cell_leaks(cell) == [], "a digit-core value in the cell is the leak itself"
    for src in cell["sources"]:
        if not src[0].startswith("@"):
            assert (SHIMS / Path(src[0]).name).is_file(), "an argv source with no shim"


def test_a_pre_scrub_shaped_note_is_refused_only_where_the_box_names_the_card(
        tmp_path, monkeypatch, capsys):
    """F5, RESTATED to what the bytes do: the guard refuses a fragment of THIS
    box's own hardware names. A note written about another box's card (the
    pre-scrub #4 node, an 8 GB box's) scores rc 1 on the box that names that
    card and rc 0 on any other box -- measured on the real box: 0 of its
    fragments occur in the node's pre-scrub bytes, so 'refused on the live box'
    was never a property of the guard, only of one box's hardware."""
    diff = tmp_path / "note.diff"
    diff.write_text("diff --git a/n.md b/n.md\n@@ -0,0 +1 @@\n"
                    "+loads on the Fixturo Vexel ZX 9990 ULTRA at 64/64 layers\n")
    root = _graph(tmp_path)
    _hw_fixture(tmp_path, monkeypatch)
    assert anonymize.main(["check", "--root", str(root), "--diff-file", str(diff)]) == 1
    _hw_fixture(tmp_path, monkeypatch, name="Fixturo Other 4410 MAX")
    assert anonymize.main(["check", "--root", str(root), "--diff-file", str(diff)]) == 0
    assert "9990" not in capsys.readouterr().err
