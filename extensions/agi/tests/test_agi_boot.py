"""G9: the boot piece (engine-root.md ### agi-boot) under sh, fakes on PATH, no real systemd."""
import json, pathlib, re, shutil, subprocess, threading, time
import pytest

WT = pathlib.Path(__file__).resolve().parents[3]
GEO = ".agi/nodes/.geometry"
ROW = '  - {"name": "%s", %s"engine": {"v": 4, "harness": "claude-code", "model": "m", "effort": "high"}, "role": "director", "tier": 1, "box": "local-town"}\n'


def section(head):
    text = (WT / GEO / "engine-root.md").read_text()
    m = re.search(r"^### %s .*?\n~~~\w*\n(.*?)\n~~~\n" % re.escape(head), text, re.S | re.M)
    assert m, head
    return m.group(1)


@pytest.fixture
def box(tmp_path):
    if not shutil.which("jq"):
        pytest.skip("jq absent")
    repo, fk = tmp_path / "repo", tmp_path / "fk"
    (repo / GEO).mkdir(parents=True), fk.mkdir()
    for f in (WT / GEO).glob("engine*.md"):
        shutil.copy(f, repo / GEO / f.name)
    rows = [("a", True), ("x", False), ("b", True)]
    (repo / GEO / "posts.md").write_text("---\nposts:\n" + "".join(ROW % (n, '"boot": true, ' if b else "") for n, b in rows))
    cfg = json.loads((WT / ".agi/config.json").read_text())
    cfg["values"]["local_maxxing"]["agi_boot"] = {"poll_s": 0.1, "wait_max_s": 1}
    (repo / ".agi/config.json").write_text(json.dumps(cfg))
    g = lambda *a: subprocess.run(["git", *a], cwd=repo, check=True, capture_output=True, text=True)
    g("init", "-q"); g("add", "-A"); g("-c", "user.name=t", "-c", "user.email=t.invalid", "commit", "-qm", "x")
    log = tmp_path / "log"
    (fk / "setfacl").write_text('#!/bin/sh\necho "setfacl $*">>%s\n' % log)
    (fk / "systemctl").write_text('#!/bin/sh\necho "systemctl $*">>%s\n[ "$1" = start ]&&{ echo "b $2">>%s;sleep 0.1;echo "e $2">>%s;}\nexit 0\n' % (log, log, log))
    for f in fk.iterdir():
        f.chmod(0o755)
    la, io = tmp_path / "loadavg", tmp_path / "io"
    la.write_text("0.50 0.5 0.5 1/1 1\n"); io.write_text("some avg10=0.00 avg60=1.00 avg300=0.00 total=1\nfull avg10=0.00 avg60=0.00 avg300=0.00 total=1\n")
    env = {"PATH": f"{fk}:/usr/bin:/bin", "AGI_TRUNK": "HEAD", "AGI_RAM": str(tmp_path / "ram"), "AGI_BOOT_OUT": str(tmp_path / "out"),
           "AGI_LOADAVG": str(la), "AGI_PSI_IO": str(io)}
    run = lambda: subprocess.run(["sh", "-s"], input=section("agi-boot"), cwd=repo, env=env, capture_output=True, text=True, timeout=60)
    return run, log, la, io, tmp_path


def lines(log):
    return log.read_text().splitlines()


def test_acl_pair_and_projection_from_ref(box):
    run, log, _, _, tp = box
    r = run(); assert r.returncode == 0, r.stderr
    L = lines(log)
    assert L.index(f"setfacl -m g:agi:x {tp}/ram") < L.index(f"setfacl -m g:agi:--- {tp}/ram/state")
    assert (tp / "out" / ("agi-post" + "@.service")).exists() and (tp / "out" / ("agi-post" + "@a.service.d") / "h.conf").exists()
    assert "systemctl daemon-reload" in L and L.index("systemctl daemon-reload") < L.index("systemctl start " + "agi-post" + "@a")


def test_only_boot_rows_one_start_each_in_order_no_overlap(box):
    run, log, *_ = box
    assert run().returncode == 0
    seq = [l for l in lines(log) if l[:2] in ("b ", "e ")]
    p = lambda n: "agi-post" + "@" + n
    assert seq == [f"b {p('a')}", f"e {p('a')}", f"b {p('b')}", f"e {p('b')}"]  # x is projected, not boot-flagged: stays down


def test_high_reading_delays_next_start(box):
    run, log, la, *_ = box
    la.write_text("20.00 1 1 1/1 1\n")
    threading.Timer(0.6, lambda: la.write_text("1.00 1 1 1/1 1\n")).start()
    t = time.time(); assert run().returncode == 0
    assert time.time() - t >= 0.6 and sum(l.startswith("b ") for l in lines(log)) == 2


@pytest.mark.parametrize("which", ["load", "io"])
def test_bound_gives_up_by_name_and_moves_on(box, which):
    run, log, la, io, _ = box
    (la if which == "load" else io).write_text("20.00 1 1 1/1 1\n" if which == "load" else "some avg10=0.00 avg60=60.00 avg300=0.00 total=1\n")
    r = run(); assert r.returncode == 0
    assert "skipping a" in r.stderr and "skipping b" in r.stderr and not any(l.startswith("b ") for l in lines(log))


def test_unit_text_one_section():
    u = section("agi-boot.service")
    for need in ("After=agi-ram-main.service", "Requires=agi-ram-main.service", "Type=oneshot", "WantedBy=multi-user.target"):
        assert need in u
    n = sum(f.read_text().count("Requires=agi-ram-main.service") for f in (WT / GEO).glob("*.md"))
    assert n == 1 and "Requires=" not in section("agi-boot")  # F4: one copy, none in the script
