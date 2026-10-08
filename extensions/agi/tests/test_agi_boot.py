"""G9: the boot piece (engine-root.md ### agi-boot) under sh, fakes on PATH, no real systemd."""
import json, pathlib, re, shutil, subprocess
import pytest

WT = pathlib.Path(__file__).resolve().parents[3]
GEO = ".agi/nodes/.geometry"
ROW = '  - {"name": "%s", %s"engine": {"v": 4, "harness": "claude-code", "model": "m", "effort": "high"}, "role": "director", "tier": 1, "box": "local-town"}\n'


def section(head, f="engine-root.md"):
    text = (WT / GEO / f).read_text()
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
    z = '  - {"name": "z", "boot": true, "role": "director", "tier": 1, "box": "local-town"}\n'  # boot-flagged, no engine row
    (repo / GEO / "posts.md").write_text("---\nposts:\n" + "".join(ROW % (n, '"boot": true, ' if b else "") for n, b in rows) + z)
    cfg = json.loads((WT / ".agi/config.json").read_text())
    cfg["values"]["local_maxxing"]["agi_boot"] = {"poll_s": 0.1, "wait_max_s": 1, "space_s": 0.2}
    (repo / ".agi/config.json").write_text(json.dumps(cfg))
    g = lambda *a: subprocess.run(["git", *a], cwd=repo, check=True, capture_output=True, text=True)
    g("init", "-q"); g("add", "-A"); g("-c", "user.name=t", "-c", "user.email=t.invalid", "commit", "-qm", "x")
    log = tmp_path / "log"
    (fk / "setfacl").write_text('#!/bin/sh\necho "setfacl $*">>%s\n' % log)
    la, io = tmp_path / "loadavg", tmp_path / "io"
    (fk / "systemctl").write_text('#!/bin/sh\necho "systemctl $*">>%s\n[ "$1" = start ]&&{ echo "b $2">>%s;/bin/sleep 0.1;echo "e $2">>%s;[ -e %s/rmload ]&&rm -f %s;[ -e %s/sfail.$2 ]&&exit 1;}\n[ -e %s/drfail ]&&[ "$1" = daemon-reload ]&&exit 1\nexit 0\n' % (log, log, log, fk, la, fk, fk))
    (fk / "sleep").write_text('#!/bin/sh\necho "sleep $*">>%s\n[ -e %s ]&&mv %s %s\nexec /bin/sleep "$@"\n' % (log, tmp_path / "flip", tmp_path / "flip", la))
    for f in fk.iterdir():
        f.chmod(0o755)
    la.write_text("0.50 0.5 0.5 1/1 1\n"); io.write_text("some avg10=0.00 avg60=1.00 avg300=0.00 total=1\nfull avg10=0.00 avg60=0.00 avg300=0.00 total=1\n")
    env = {"PATH": f"{fk}:/usr/bin:/bin", "AGI_TRUNK": g("rev-parse", "HEAD").stdout.strip(), "AGI_RAM": str(tmp_path / "ram"), "AGI_BOOT_OUT": str(tmp_path / "out"),
           "AGI_LOADAVG": str(la), "AGI_PSI_IO": str(io)}
    run = lambda: subprocess.run(["sh", "-s"], input=section("agi-boot"), cwd=repo, env={**env, "AGI_TRUNK": g("rev-parse", "HEAD").stdout.strip()}, capture_output=True, text=True, timeout=60)  # the pin is the sha HEAD has NOW (A1: the unit reads a pinned sha, never HEAD)
    run.env, run.repo = env, repo
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
    r = run(); assert r.returncode == 0
    seq = [l for l in lines(log) if l[:2] in ("b ", "e ")]
    p = lambda n: "agi-post" + "@" + n
    assert seq == [f"b {p('a')}", f"e {p('a')}", f"b {p('b')}", f"e {p('b')}"]  # x is projected, not boot-flagged: stays down
    assert "agi-boot: z not projected (engine v4 row absent), skipped" in r.stderr  # boot-flagged but no projected link


def test_high_reading_delays_next_start(box):
    run, log, la, *_, tp = box
    la.write_text("20.00 1 1 1/1 1\n"); (tp / "flip").write_text("1.00 1 1 1/1 1\n")  # the fake sleep flips it on the first wait
    assert run().returncode == 0
    L = lines(log); assert L.index("sleep 0.1") < next(i for i, l in enumerate(L) if l.startswith("b ")) and sum(l.startswith("b ") for l in L) == 2


@pytest.mark.parametrize("which", ["load", "io", "noload", "emptyload"])
def test_bound_gives_up_by_name_and_moves_on(box, which):
    run, log, la, io, _ = box
    {"load": lambda: la.write_text("20.00 1 1 1/1 1\n"), "io": lambda: io.write_text("some avg10=0.00 avg60=60.00 avg300=0.00 total=1\n"),
     "noload": la.unlink, "emptyload": lambda: la.write_text("")}[which]()
    r = run(); assert r.returncode != 0  # a give-up fails the boot unit
    assert "skipping a" in r.stderr and "skipping b" in r.stderr and not any(l.startswith("b ") for l in lines(log))


@pytest.mark.parametrize("which", ["setfacl", "daemon-reload"])
def test_acl_or_reload_failure_is_named_continues_and_exits_nonzero(box, which):
    run, log, *_, tp = box
    if which == "setfacl":
        (tp / "fk/setfacl").write_text("#!/bin/sh\nexit 1\n")
    else:
        (tp / "fk/drfail").write_text("")
    r = run(); assert r.returncode != 0 and f"agi-boot: failed: {which if which == 'setfacl' else 'systemctl daemon-reload'}" in r.stderr
    assert sum(l.startswith("b ") for l in lines(log)) == 2


def test_failed_start_is_named_exits_nonzero_next_row_still_starts(box):
    run, log, *_, tp = box
    (tp / "fk" / ("sfail.agi-post" + "@a")).write_text("")
    r = run(); assert r.returncode != 0 and "start failed a" in r.stderr and "b " + "agi-post" + "@b" in lines(log)


def test_second_load_read_failing_keeps_gate_closed(box):
    run, log, *_, tp = box
    (tp / "fk/rmload").write_text("")  # a's start removes the load file: b's first read finds none, must not reuse a's good value
    r = run(); L = lines(log)
    assert r.returncode != 0 and "skipping b" in r.stderr and "skipping a" not in r.stderr
    assert "b " + "agi-post" + "@a" in L and "b " + "agi-post" + "@b" not in L


@pytest.mark.parametrize("which", ["absent", "noboot"])
def test_unreadable_or_empty_boot_list_is_named_and_fails(box, which):
    run, log, *_ = box
    g = lambda *a: subprocess.run(["git", "-c", "user.name=t", "-c", "user.email=t.invalid", *a], cwd=run.repo, check=True, capture_output=True)
    pm = run.repo / GEO / "posts.md"
    pm.write_text(pm.read_text().replace('"boot": true, ', "")) if which == "noboot" else pm.unlink()
    g("add", "-A"); g("commit", "-qm", "y")
    r = run(); assert r.returncode != 0 and "agi-boot: no boot rows read from " + g("rev-parse", "HEAD").stdout.decode().strip() in r.stderr and not any(l.startswith("b ") for l in lines(log))


def test_unit_execstart_reads_the_pinned_sha_never_head(box):  # g1.41 A1 (was: reads HEAD, no trunk literal)
    run, log, la, io, tp = box
    u = section("agi-boot.service"); assert u.splitlines().count("EnvironmentFile=/etc/agi/carry.env") == 1
    cmd = next(l for l in u.splitlines() if l.startswith("ExecStart=")).split("=", 1)[1]
    assert "HEAD" not in cmd and "$AGI_TRUNK:" in cmd
    assert subprocess.run(cmd, shell=True, cwd=run.repo, env=run.env, capture_output=True, text=True, timeout=60).returncode == 0
    assert sum(l.startswith("b ") for l in lines(log)) == 2


def test_unit_text_one_section():
    u = section("agi-boot.service")
    for need in ("After=agi-ram-main.service", "Requires=agi-ram-main.service", "Type=oneshot", "WantedBy=multi-user.target"):
        assert need in u
    n = sum(f.read_text().count("Requires=agi-ram-main.service") for f in (WT / GEO).glob("*.md"))
    assert n == 1 and "Requires=" not in section("agi-boot")  # F4: one copy, none in the script


def test_space_s_slept_between_starts_never_after_last_gate_read_after_it(box):
    run, log, la, *_, tp = box
    assert run().returncode == 0
    p = lambda n: "agi-post" + "@" + n
    seq = [l for l in lines(log) if l[:2] in ("b ", "e ") or l == "sleep 0.2"]  # poll_s is 0.1: the gate is open, never polled
    assert seq == [f"b {p('a')}", f"e {p('a')}", "sleep 0.2", f"b {p('b')}", f"e {p('b')}"]  # two starts never closer than space_s, no tail after the last
    (tp / "flip").write_text("20.00 1 1 1/1 1\n")  # the space sleep closes the gate: b's re-read, after it, must see that
    log.write_text(""); r = run()
    assert r.returncode != 0 and "skipping b" in r.stderr and "b " + p("a") in lines(log) and "b " + p("b") not in lines(log)


def test_missing_space_cell_is_named_and_fails(box):
    run, log, *_ = box
    p = run.repo / ".agi/config.json"; cfg = json.loads(p.read_text()); del cfg["values"]["local_maxxing"]["agi_boot"]["space_s"]
    p.write_text(json.dumps(cfg)); subprocess.run(["git", "-c", "user.name=t", "-c", "user.email=t.invalid", "commit", "-qam", "y"], cwd=run.repo, check=True, capture_output=True)
    r = run(); assert r.returncode != 0 and "agi-boot: failed: sleep null" in r.stderr


def test_non_boot_row_gets_no_wants_link_boot_rows_do(box):
    run, *_, tp = box
    assert run().returncode == 0
    w = tp / "out" / "multi-user.target.wants"
    assert sorted(x.name for x in w.glob("agi-post@*")) == ["agi-post" + "@a.service", "agi-post" + "@b.service"]  # x: projected unit + h.conf, no wants link
    assert (tp / "out" / ("agi-post" + "@x.service.d") / "h.conf").exists()


def test_gate_checks_projected_dropin_not_wants_links(box):
    run, log, la, io, tp = box
    (tp / "fk" / "sect").write_text("#!/bin/sh\n" + section("sect", "engine.md") + "\n"); (tp / "fk" / "sect").chmod(0o755)
    gate = lambda: subprocess.run(["sh", "-s", "HEAD"], input=section("agi-gate", "engine.md"), cwd=run.repo, env={**run.env, "TMPDIR": str(tp)}, capture_output=True, text=True, timeout=60)
    ci = lambda: subprocess.run(["git", "-c", "user.name=t", "-c", "user.email=t.invalid", "commit", "-qam", "y"], cwd=run.repo, check=True, capture_output=True)
    pf = run.repo / GEO / "posts.md"; rows = pf.read_text()
    assert gate().returncode == 0  # boot rows present
    pf.write_text(rows.replace('"boot": true, ', "")); ci()
    r = gate(); assert r.returncode == 0, r.stderr  # v4 rows, no boot row: no wants link, the drop-ins still pass
    pf.write_text(re.sub(r', "engine": \{.*?\}', "", rows)); ci()
    assert gate().returncode == 1  # no v4 rows at all: refuses


def test_project_service_execstart_checks_dropin_not_wants_links(box):
    run, log, la, io, tp = box
    (tp / "fk" / "systemd-sysusers").write_text("#!/bin/sh\nexit 0\n"); (tp / "fk" / "systemd-sysusers").chmod(0o755)
    ci = lambda: subprocess.run(["git", "-c", "user.name=t", "-c", "user.email=t.invalid", "commit", "-qam", "y"], cwd=run.repo, check=True, capture_output=True)
    pf = run.repo / GEO / "posts.md"; rows = pf.read_text()

    def execstart(n):  # project on the fixture's HEAD, then run the generated unit's whole ExecStart fragment under sh -c
        o = tp / n; o.mkdir()
        assert subprocess.run(["sh", "-s", str(o), "HEAD"], input=section("agi-project", "engine.md"), cwd=run.repo, env=run.env, capture_output=True, text=True, timeout=60).returncode == 0
        frag = re.search(r'^ExecStart=sh -c "(.*)"$', (o / "agi-project.service").read_text(), re.M).group(1)
        assert "ls " in frag and "systemctl daemon-reload" in frag and "systemd-sysusers" in frag
        return subprocess.run(["sh", "-c", frag], cwd=run.repo, env=run.env, capture_output=True, text=True, timeout=60).returncode
    assert execstart("o1") == 0  # boot rows present
    pf.write_text(rows.replace('"boot": true, ', "")); ci()
    assert execstart("o2") == 0  # v4 rows, no boot row: no wants link, h.conf drop-ins exist
    pf.write_text(re.sub(r', "engine": \{.*?\}', "", rows)); ci()
    assert execstart("o3") != 0  # no v4 rows: no h.conf, the check fails the unit
