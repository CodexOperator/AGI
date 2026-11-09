"""goal:g7.16.2.1 -- the private-range IPv4 row of anonymize.scan, its ONE allowlist, and both readers.
Rows are judged by the class NAME 'ip', never by emptiness. The VL_ lane: the whole verify-land.sh is too heavy
to run here, so the diff step is the factored `anonymize.mask_diff_ips` (called by verify-land.sh, grep-pinned
below) plus anonymize.ip_allow read from BASE; reds.py _secrets is driven on a real fixture repo."""
import json, os, re, subprocess, sys
from pathlib import Path
import pytest

BIN = Path(__file__).resolve().parents[1] / "bin"
sys.path.insert(0, str(BIN))
import anonymize as a  # noqa: E402
import reds  # noqa: E402

RED = ["10.1.2.3", "172.20.0.1", "100.64.0.1"]
GREEN = ["127.0.0.1", "2.10.1.4", "192.0.2.1", "172.15.0.1", "172.32.0.1", "100.63.0.1", "100.128.0.1",
         "10.52.123.456", "goal:g10.1.2.3", "v10.1.2.3"]
SRC = (BIN / "anonymize.py").read_text()
VL = (BIN.parent / "guard" / "verify-land.sh").read_text()


def ip(x):
    return "ip" in a.scan(x, [])


@pytest.mark.parametrize("x", RED)
def test_red_rows_name_ip(x):
    assert ip(x) and ip("addr " + x + " end")


@pytest.mark.parametrize("x", GREEN)
def test_green_rows_do_not_name_ip(x):
    assert not ip(x)


def test_leading_zero_timestamp_shape_does_not_crash():
    assert not ip("0.00.100.036") and ip("10.00.100.036") is True


def test_no_is_private():
    assert "is_private" not in SRC


# ---- the allowlist helpers
def test_allow_helpers():
    cfg = {"anonymize": {"ip_allow": [{"path": "a/b.py", "why": "x"}, {"path": "d/", "why": "y"}, {"nopath": 1}, "junk"]}}
    al = a.ip_allow(cfg)
    assert al == ["a/b.py", "d/"]
    assert a.path_allowed("a/b.py", al) and a.path_allowed("d/x/y", al)
    assert not a.path_allowed("a/b.pyc", al) and not a.path_allowed("dd/x", al)
    assert a.ip_allow({}) == [] and a.ip_allow({"anonymize": {"ip_allow": "x"}}) == [] and a.ip_allow(None) == []


def _diff(path, line):
    return f"diff --git a/{path} b/{path}\n--- a/{path}\n+++ b/{path}\n@@ -0,0 +1 @@\n+{line}\n"


@pytest.mark.parametrize("x", RED)
def test_diff_reader_allowlisted_green_outside_red(x):
    al = ["t/fix.py", "d/"]
    for path, want in (("t/fix.py", False), ("d/n/f.md", False), ("src/x.py", True), ("t/fix.pyx", True)):
        masked = a.mask_diff_ips(_diff(path, "v = " + x), al)
        assert ("ip" in a.scan(a.added_lines(masked), [])) is want, path


def test_allowlisted_path_still_flags_other_classes():
    masked = a.mask_diff_ips(_diff("t/fix.py", "10.1.2.3 mail " + "me" + "@" + "example-corp.org"), ["t/fix.py"])
    cls = a.scan(a.added_lines(masked), [], email_allow=[])
    assert "ip" not in cls and "email" in cls


def test_verify_land_calls_the_one_helper_and_reads_base():
    assert "anonymize.ip_allow(" in VL and "anonymize.mask_diff_ips(" in VL
    assert 'git show "$B:.agi/config.json"' in VL and "ip_allow(json.load(open(cfg)))" in VL


# ---- reds.py _secrets, on a fixture repo
def _git(repo, *args, env_extra=None):
    env = dict(os.environ, GIT_CONFIG_GLOBAL="/dev/null", GIT_CONFIG_SYSTEM="/dev/null",
               GIT_AUTHOR_NAME="t", GIT_AUTHOR_EMAIL="t@example.com", GIT_COMMITTER_NAME="t", GIT_COMMITTER_EMAIL="t@example.com")
    r = subprocess.run(["git", "-C", str(repo), "-c", "commit.gpgsign=false", *args], capture_output=True, text=True, env=env)
    assert r.returncode == 0, r.stderr
    return r.stdout.strip()


def _repo(tmp_path, base_allow, tip_allow, files):
    repo = tmp_path / "r"
    (repo / ".agi" / "nodes").mkdir(parents=True)
    _git(repo, "init", "-q")
    def cfg(al):
        return json.dumps({"anonymize": {"ip_allow": [{"path": p, "why": "t"} for p in al]}})
    (repo / ".agi" / "config.json").write_text(cfg(base_allow))
    _git(repo, "add", "-A"); _git(repo, "commit", "-q", "-m", "base")
    base = _git(repo, "rev-parse", "HEAD")
    (repo / ".agi" / "config.json").write_text(cfg(tip_allow))
    for p, t in files.items():
        (repo / p).parent.mkdir(parents=True, exist_ok=True)
        (repo / p).write_text(t + "\n")
    _git(repo, "add", "-A"); _git(repo, "commit", "-q", "-m", "tip")
    return repo, base, _git(repo, "rev-parse", "HEAD")


def _secrets(repo, base, tip):
    root = repo  # find_project_root is not needed: _secrets only forwards it
    return reds._secrets(repo, base, tip, root)


@pytest.mark.parametrize("x", RED)
def test_reds_reader(tmp_path, x):
    repo, b, t = _repo(tmp_path, ["ok/f.txt"], ["ok/f.txt"], {"ok/f.txt": "v = " + x, "no/f.txt": "v = " + x})
    got = _secrets(repo, b, t)
    assert got == ["no/f.txt:1"]


OWN = ".".join(["10", "9", "8", "7"])   # a fixture box's OWN address (box_tokens class ip), private-range


def _own_box(tmp_path, monkeypatch):
    f = tmp_path / "box.json"
    f.write_text(json.dumps({"ip": [OWN]}))
    monkeypatch.setenv("AGI_ANONYMIZE_FIXTURE", str(f))


def test_reds_allowlist_never_masks_the_boxs_own_address(tmp_path, monkeypatch):
    _own_box(tmp_path, monkeypatch)
    repo, b, t = _repo(tmp_path, ["ok/f.txt"], ["ok/f.txt"], {"ok/f.txt": "v = " + OWN, "ok/g.txt": "x"})
    assert _secrets(repo, b, t) == ["ok/f.txt:1"]
    repo2, b2, t2 = _repo(tmp_path / "2", ["ok/f.txt"], ["ok/f.txt"], {"ok/f.txt": "v = 10.1.2.3"})
    assert _secrets(repo2, b2, t2) == []


def test_diff_reader_allowlist_never_masks_the_boxs_own_address(tmp_path, monkeypatch):
    _own_box(tmp_path, monkeypatch)
    toks = a.box_tokens(None, secrets=False)
    keep = a.own_ips(toks)
    assert keep == {OWN}
    assert "ip" in a.scan(a.added_lines(a.mask_diff_ips(_diff("ok/f.txt", "v = " + OWN), ["ok/f.txt"], keep)), toks)
    assert "ip" not in a.scan(a.added_lines(a.mask_diff_ips(_diff("ok/f.txt", "v = 10.1.2.3"), ["ok/f.txt"], keep)), toks)
    assert "anonymize.own_ips(anonymize.box_tokens(" in VL


def test_mutant_keep_ignored_masks_the_boxs_own_address(tmp_path, monkeypatch):
    # mutant: the allowlist masks every private token, the box's own too -> the own-address row would read green
    _own_box(tmp_path, monkeypatch)
    toks = a.box_tokens(None, secrets=False)
    masked = a.mask_diff_ips(_diff("ok/f.txt", "v = " + OWN), ["ok/f.txt"])   # keep dropped
    assert "ip" not in a.scan(a.added_lines(masked), toks)


def test_reds_base_not_tip(tmp_path):
    repo, b, t = _repo(tmp_path, [], ["no/f.txt"], {"no/f.txt": "v = 10.1.2.3"})
    assert _secrets(repo, b, t) == ["no/f.txt:1"]


def test_diff_reader_base_not_tip():
    # verify-land.sh reads the cell from BASE's copy ($B:), the file it hands anonymize.ip_allow
    assert re.search(r'git show "\$B:\.agi/config\.json" > "\$S/\$N\.cfg"', VL)
    assert 'show "$L:.agi/config.json"' not in VL and '$T:.agi/config.json' not in VL


# ---- mutants: each must make the matching row fail
def _mut_scan(src_edit):
    ns = {"__name__": "mut"}
    code = src_edit(SRC).replace("sys.path.insert(0, str(Path(__file__).resolve().parent))",
                                 f"sys.path.insert(0, {str(BIN)!r})").replace("Path(__file__)", f"Path({str(BIN / 'anonymize.py')!r})")
    exec(compile(code, "mut_anonymize", "exec"), ns)
    return ns


def _rows_ok(ns):
    sc = lambda x: "ip" in ns["scan"](x, [])
    return all(sc(x) for x in RED) and not any(sc(x) for x in GREEN)


def test_unmutated_source_passes_rows():
    assert _rows_ok(_mut_scan(lambda s: s))


def test_mutant_prefix_regex():
    # a leading-octet (prefix) test in place of network membership reads 172.15/172.32/100.63/100.128 RED
    def e(s):
        old = "any(ipaddress.IPv4Address(bytes(o)) in n for n in IP_NETS)"
        assert old in s
        return s.replace(old, "o[0] in (10, 172, 192, 100)")
    assert not _rows_ok(_mut_scan(e))


def test_mutant_lookbehind_digit_or_dot_only():
    def e(s):
        assert "(?<![\\w.])" in s
        return s.replace("(?<![\\w.])", "(?<![\\d.])")
    assert not _rows_ok(_mut_scan(e))


def test_mutant_is_private():
    def e(s):
        return s.replace("any(ipaddress.IPv4Address(bytes(o)) in n for n in IP_NETS)", "ipaddress.IPv4Address(bytes(o)).is_" + "private")
    ns = _mut_scan(e)
    assert not _rows_ok(ns)
    assert "ip" not in ns["scan"]("100.64.0.1", [])


def test_mutant_one_reader_alone(tmp_path, monkeypatch):
    # reds.py reading NO allowlist (as if only verify-land.sh had it): the allowlisted add reads RED there
    repo, b, t = _repo(tmp_path, ["ok/f.txt"], ["ok/f.txt"], {"ok/f.txt": "v = 10.1.2.3"})
    assert _secrets(repo, b, t) == []
    monkeypatch.setattr(a, "ip_allow", lambda cfg: [])
    assert _secrets(repo, b, t) == ["ok/f.txt:1"]
    monkeypatch.undo()
    # and the diff reader with no allowlist reads the same add RED
    assert "ip" in a.scan(a.added_lines(a.mask_diff_ips(_diff("ok/f.txt", "10.1.2.3"), [])), [])
    assert "ip" not in a.scan(a.added_lines(a.mask_diff_ips(_diff("ok/f.txt", "10.1.2.3"), ["ok/f.txt"])), [])
