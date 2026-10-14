"""memory_alarm.py: the owner's 09-26 memory alarm (raise before the box wedges)."""
import argparse
import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "bin"))
import crons  # noqa: E402
import locations  # noqa: E402
import memory_alarm as m  # noqa: E402

@pytest.fixture(autouse=True)
def _runs_as_the_sending_seat(monkeypatch):
    monkeypatch.setattr(m, "_uid_name", lambda: "agi-sanctuary-master")


TH = argparse.Namespace(warn_avail_mib=2048, crit_avail_mib=1024,
                        warn_psi_some_avg60=10, crit_psi_full_avg60=20,
                        warn_cgroup_max_frac=0.95, warn_slab_mib=1536, clear_margin_frac=0.8)


def sig(avail=8000.0, box=(0.0, 0.0), cg=(0.0, 0.0), cur=None, cap=None, high=None, slab=None, anon=None, rec=None, name="agi.slice", shmem=0, unrec=None):
    def psi(some, full):
        return {"some": {"avg10": some, "avg60": some}, "full": {"avg10": full, "avg60": full}}
    return {"avail_mib": avail, "box_psi": psi(*box), "cg_psi": psi(*cg),
            "cg_current": cur, "cg_max": cap, "cg_high": high,
            "cg_name": name, "cg_slab": slab, "cg_slab_rec": rec, "cg_anon": anon, "cg_shmem": shmem, "cg_slab_unrec": unrec}


def test_quiet_box_is_ok():
    assert m.decide(sig(), TH) == ("ok", [])


def test_low_available_warns_then_crits():
    assert m.decide(sig(avail=1500), TH)[0] == "warn"
    assert m.decide(sig(avail=900), TH)[0] == "crit"


def test_pressure_inside_the_user_cap_is_seen_while_the_box_is_calm():
    assert m.decide(sig(cg=(12.0, 0.0)), TH)[0] == "warn"
    level, reasons = m.decide(sig(cg=(50.0, 25.0)), TH)
    assert level == "crit" and any(r.startswith("agi.slice PSI full") for r in reasons)


def test_user_cap_fill_warns_only_near_the_hard_cap():
    assert m.decide(sig(anon=5600 << 20, unrec=10 << 20, cap=5829 << 20), TH)[0] == "warn"
    assert m.decide(sig(anon=4000 << 20, unrec=10 << 20, cap=5829 << 20), TH)[0] == "ok"


def test_unreadable_signals_never_raise(tmp_path):
    assert m.read_psi(tmp_path / "missing") == {}
    empty = {"avail_mib": None, "box_psi": {}, "cg_psi": {}, "cg_current": None, "cg_max": None}
    assert m.decide(empty, TH) == ("ok", [])


def test_transition_raises_repeats_and_clears():
    assert m.transition({}, "ok", 0, 900) is None
    assert m.transition({}, "warn", 0, 900) == "raise"
    st = {"level": "warn", "last_alert": 0}
    assert m.transition(st, "warn", 100, 900) is None
    assert m.transition(st, "warn", 900, 900) == "repeat"
    assert m.transition(st, "crit", 100, 900) == "raise"
    assert m.transition(st, "ok", 100, 900) == "clear"


def _args(tmp_path, *thresholds):
    return ["--root", str(tmp_path), *thresholds, "--repeat-mins", "15",
            "--cgroup", str(tmp_path / "no-cgroup"), "--state", str(tmp_path / "st.json"),
            "--alerts-log", str(tmp_path / "alerts.log"), "--alarm-seat", "sanctuary-master", "--alarm-to", "belam", "--alarm-job", "memory_alarm_posts", "--alarm-spool-max", "500"]


def test_an_ok_run_writes_and_sends_nothing(tmp_path, capsys, monkeypatch):
    sent = []
    monkeypatch.setattr(m.alarm_spool, "append", lambda *a, **k: sent.append(a))
    rc = m.main(_args(tmp_path, "--warn-avail-mib", "0", "--crit-avail-mib", "0",
                      "--warn-psi-some-avg60", "1000", "--clear-margin-frac", "1", "--clear-hold-mins", "0", "--crit-psi-full-avg60", "1000",
                      "--warn-cgroup-max-frac", "1000", "--warn-slab-mib", "1e12"))
    assert rc == 0 and sent == [] and capsys.readouterr().out == ""
    assert not (tmp_path / "alerts.log").exists() and not (tmp_path / "st.json").exists()


def test_a_raise_logs_once_dms_once_then_stays_quiet(tmp_path, monkeypatch):
    sent = []
    monkeypatch.setattr(m.alarm_spool, "append", lambda job, to, body, **k: sent.append((to, body)))
    argv = _args(tmp_path, "--warn-avail-mib", "1e12", "--crit-avail-mib", "0",
                 "--warn-psi-some-avg60", "1000", "--clear-margin-frac", "1", "--clear-hold-mins", "0", "--crit-psi-full-avg60", "1000",
                 "--warn-cgroup-max-frac", "1000", "--warn-slab-mib", "1e12")
    assert m.main(argv) == 0
    lines = (tmp_path / "alerts.log").read_text().splitlines()
    assert len(lines) == 1 and " WARN memory warn: MemAvailable " in lines[0]
    assert len(sent) == 1 and sent[0][0] == "belam" and sent[0][1].startswith("[memory-alarm-warn] ")
    assert m.main(argv) == 0  # same level inside the repeat window: silent
    assert len((tmp_path / "alerts.log").read_text().splitlines()) == 1 and len(sent) == 1


# --- the claim: the alarm's log is UNDER the cap -------------------------
#
# Falsifier, pre-fix: the default was a literal
# `~/logs/sanctuary-guard/alerts.log`, and `crons.enforce_log_caps` globs the
# logs dir NON-recursively, so a 17 MB alert log in that subdirectory drew an
# empty action list and grew without bound.

def test_the_default_alerts_log_lands_where_the_cap_looks(tmp_path, monkeypatch):
    """No `--alerts-log` means: the `logs.alerts_file` cell, a bare NAME in
    `crons.logs_dir()` -- the one dir `enforce_log_caps` bounds. A default that
    re-derives a path (or nests one under a subdir) is a path the cap misses."""
    home = tmp_path / "home"
    (home / "logs").mkdir(parents=True)
    monkeypatch.setenv("HOME", str(home))
    root = tmp_path / "proj"
    root.mkdir()
    (root / "agi-tree.config.json").write_text(json.dumps(
        {"logs": {"cap_mb": 1, "rotations": 3, "mode": "copytruncate",
                  "alerts_file": "memory-alarm-alerts.log"}}))
    monkeypatch.setattr(m.alarm_spool, "append", lambda *a, **k: None)
    argv = ["--root", str(root), "--warn-avail-mib", "1e12",
            "--crit-avail-mib", "0", "--warn-psi-some-avg60", "1000", "--clear-margin-frac", "1", "--clear-hold-mins", "0",
            "--crit-psi-full-avg60", "1000", "--warn-cgroup-max-frac", "1000", "--warn-slab-mib", "1e12",
            "--repeat-mins", "15", "--cgroup", str(tmp_path / "no-cgroup"),
            "--state", str(tmp_path / "st.json"), "--alarm-seat", "sanctuary-master", "--alarm-to", "belam", "--alarm-job", "memory_alarm_posts", "--alarm-spool-max", "500"]
    assert m.main(argv) == 0
    written = crons.alerts_log(root)
    assert written == home / "logs" / "memory-alarm-alerts.log", written
    assert written.is_file() and written.read_text().strip()

    # the falsifier proper: the cap now REACHES that file
    written.write_bytes(b"x" * (2 * 1024 * 1024))   # 2 MB over a 1 MB cap
    out = crons.enforce_log_caps(root, root, dry_run=False)
    assert any("memory-alarm-alerts.log" in line for line in out), out
    assert written.stat().st_size == 0


@pytest.mark.parametrize("bad", [
    "sanctuary/alerts.log",   # a subdirectory: the pre-fix hole, uncapped by the glob
    "/tmp/escape.log",        # absolute: outside the capped dir entirely
    "../escape.log",          # a traversal out of the capped dir
    "sub\\alerts.log",        # a separator the cap's glob cannot see on this box
    "..",                     # the parent dir itself
    "", "   ",                # empty after strip: a dir, not a file
])
def test_the_alerts_log_name_is_a_cell_not_a_path(tmp_path, monkeypatch, bad):
    """The cell carries a NAME, or it is REFUSED BY NAME. A path in it would
    re-open the subdirectory hole the cap's non-recursive glob cannot see, so
    a malformed cell raises `CronsError` exactly as a malformed
    `logs.cap_mb`/`logs.mode` does -- a cap that silently does not apply is
    worse than no cap."""
    monkeypatch.setenv("HOME", str(tmp_path / "home"))
    root = tmp_path / "proj"
    root.mkdir()
    (root / "agi-tree.config.json").write_text(json.dumps({"logs": {"alerts_file": bad}}))
    with pytest.raises(crons.CronsError, match="logs.alerts_file"):
        crons.alerts_log(root)
    assert not (tmp_path / "escape.log").exists()


def test_the_default_alerts_file_name_still_resolves(tmp_path, monkeypatch):
    """The guard is not a ban: the shipped bare NAME resolves into the capped
    dir, and an ABSENT cell falls back to `crons.ALERTS_FILE`."""
    monkeypatch.setenv("HOME", str(tmp_path / "home"))
    (tmp_path / "home" / "logs").mkdir(parents=True)
    for cell in (None, "alerts.log"):
        root = tmp_path / ("p-absent" if cell is None else "p-present")
        root.mkdir()
        (root / "agi-tree.config.json").write_text(json.dumps(
            {} if cell is None else {"logs": {"alerts_file": cell}}))
        assert crons.alerts_log(root).parent == crons.logs_dir()
        assert crons.alerts_log(root).name == (cell or crons.ALERTS_FILE)


# --- the claim, restated: NO path literal is left in memory_alarm.py ------

def test_the_state_path_comes_from_the_sessions_resolver(tmp_path, monkeypatch):
    """No `--state` means `locations.sessions_dir(root) / STATE_FILE` -- the
    ONE sessions resolver, so the state file follows the room the graph moved
    it to. A `<root>/"sessions"/...` literal is a path a reader cannot move."""
    monkeypatch.setenv("HOME", str(tmp_path / "home"))
    (tmp_path / "home" / "logs").mkdir(parents=True)
    root = tmp_path / "proj"
    (root / "sessions").mkdir(parents=True)
    (root / "agi-tree.config.json").write_text("{}")
    monkeypatch.setattr(m.alarm_spool, "append", lambda *a, **k: None)
    argv = ["--root", str(root), "--warn-avail-mib", "1e12",
            "--crit-avail-mib", "0", "--warn-psi-some-avg60", "1000", "--clear-margin-frac", "1", "--clear-hold-mins", "0",
            "--crit-psi-full-avg60", "1000", "--warn-cgroup-max-frac", "1000", "--warn-slab-mib", "1e12",
            "--repeat-mins", "15", "--cgroup", str(tmp_path / "no-cgroup")]
    assert m.main(argv) == 0
    state = locations.sessions_dir(root) / m.STATE_FILE
    assert state.is_file() and json.loads(state.read_text())["level"] == "warn"
    src = Path(m.__file__).read_text()
    assert 'STATE_FILE' in src and '"sessions"' not in src.split("def main")[1]


# --- goal:g7.16.1.11.20.2: EVERY alarm is a signed box message, never send.py, never a pane write ----------------

BIN = Path(m.__file__).resolve()
REPO = BIN.parents[3]
def test_send_py_is_out_of_memory_alarm_entirely():
    text = BIN.read_text()
    assert "send.py" not in text and "_dm" not in text and "from send" not in text and "import send" not in text, "the old mail path is back"
    assert "agi-notice" not in text.split("def main")[1] and "--notify" not in text, "the ~/.notice path is back"


def _spool(tmp_path):
    return tmp_path / "alarm.spool"


def _records(tmp_path):
    sp = _spool(tmp_path)
    return [json.loads(l) for l in sp.read_text().splitlines()] if sp.exists() else []


def _stub(tmp_path, monkeypatch, uid="agi-sanctuary-master"):
    monkeypatch.setattr(m, "_uid_name", lambda: uid)


def _forbid_send_py(monkeypatch):
    real = m.subprocess.run
    def guard(cmd, *a, **k):
        assert "send.py" not in " ".join(map(str, cmd)), cmd           # a send.py spawn fails the row
        return real(cmd, *a, **k)
    monkeypatch.setattr(m.subprocess, "run", guard)


def _warn_args(tmp_path, *extra, state="st.json", log="alerts.log"):
    return ["--root", str(tmp_path), "--warn-avail-mib", "1e12", "--crit-avail-mib", "0", "--warn-psi-some-avg60", "1000",
            "--crit-psi-full-avg60", "1000", "--warn-cgroup-max-frac", "1000", "--warn-slab-mib", "1e12", "--repeat-mins", "15",
            "--clear-margin-frac", "1", "--clear-hold-mins", "0",
            "--cgroup", str(tmp_path / "no-cgroup"), "--state", str(tmp_path / state), "--alerts-log", str(tmp_path / log), *extra]


def _alarm(tmp_path):
    return [*(ALARM_FLAGS), "--alarm-spool", str(_spool(tmp_path))]


ALARM_FLAGS = ["--alarm-seat", "sanctuary-master", "--alarm-to", "belam", "--alarm-job", "memory_alarm_posts", "--alarm-spool-max", "500"]


def test_the_alarm_is_one_plain_spool_line_in_the_sending_seats_spool_and_nothing_is_sent(tmp_path, monkeypatch):
    _forbid_send_py(monkeypatch)
    real = m.subprocess.run
    monkeypatch.setattr(m.subprocess, "run", lambda *a, **k: pytest.fail(f"memory_alarm spawned {a}: it only appends"))
    assert m.main(_warn_args(tmp_path, *_alarm(tmp_path))) == 0
    (rec,) = _records(tmp_path)
    assert rec["job"] == "memory_alarm_posts" and rec["to"] == "belam", rec
    assert rec["text"].startswith("[memory-alarm-warn] ") and "WARN memory warn: MemAvailable " in rec["text"], rec
    assert m.main(_warn_args(tmp_path, *_alarm(tmp_path))) == 0                                     # inside the repeat window: silent
    assert len(_records(tmp_path)) == 1
    # kinds are separate lines: a CLEARED is its own alarm, never a repeat of the WARN
    assert m.main(["--root", str(tmp_path), "--warn-avail-mib", "0", "--crit-avail-mib", "0", "--warn-psi-some-avg60", "1000", "--crit-psi-full-avg60", "1000",
                   "--warn-cgroup-max-frac", "1000", "--warn-slab-mib", "1e12", "--repeat-mins", "15", "--clear-margin-frac", "1", "--clear-hold-mins", "0", "--cgroup", str(tmp_path / "no-cgroup"),
                   "--state", str(tmp_path / "st.json"), "--alerts-log", str(tmp_path / "alerts.log"), *_alarm(tmp_path)]) == 0
    recs = _records(tmp_path)
    assert len(recs) == 2 and recs[1]["text"].startswith("[memory-alarm-cleared] "), recs


def test_from_the_wrong_uid_or_a_full_spool_nothing_is_spooled_it_says_so_and_never_falls_back(tmp_path, monkeypatch, capsys):
    _stub(tmp_path, monkeypatch, uid="agi-belam"); _forbid_send_py(monkeypatch)                    # the cron job still running as the old uid
    assert m.main(_warn_args(tmp_path, *_alarm(tmp_path))) == 0
    assert not _spool(tmp_path).exists(), "an alarm was spooled from the wrong uid"
    err = capsys.readouterr().err
    assert "alarm to belam NOT spooled" in err and "must run as agi-sanctuary-master" in err, err
    assert "ALARM to belam NOT spooled" in (tmp_path / "alerts.log").read_text()                    # and in the log: never a silent failure
    capsys.readouterr()
    _stub(tmp_path, monkeypatch)                                                                    # right uid, spool at its cap: the same two places say so
    full = ["--alarm-seat", "sanctuary-master", "--alarm-to", "belam", "--alarm-job", "j", "--alarm-spool-max", "0", "--alarm-spool", str(_spool(tmp_path))]
    assert m.main(_warn_args(tmp_path, *full, state="st2.json", log="alerts2.log")) == 0
    assert "max-lines 0" in capsys.readouterr().err and "max-lines 0" in (tmp_path / "alerts2.log").read_text()


def test_the_alarm_flags_go_together(tmp_path):
    with pytest.raises(SystemExit):
        m.main(_warn_args(tmp_path, "--alarm-to", "belam"))


def _real_rows(tmp_path):
    fm = crons._parse_frontmatter(crons._node_path(REPO / ".agi"))["cadences"]
    out = {}
    for name in ("memory_alarm", "memory_alarm_posts"):
        row = fm[name]
        cmd = row["cmd"].replace("{repo_root}", str(REPO)).replace("{root}", str(tmp_path))
        argv = cmd.split()[2:]                                                                       # drop `python3 memory_alarm.py`
        out[name] = (row, argv)
    return out


def _run_rows(tmp_path, monkeypatch, rows, uid):
    _stub(tmp_path, monkeypatch, uid=uid)
    for name, argv in rows.items():
        argv = list(argv)
        argv[argv.index("--warn-avail-mib") + 1] = "1e12"                                             # force a warn on the box-wide signal both jobs read
        argv += ["--alerts-log", str(tmp_path / f"{name}.log")]
        if "--alarm-to" in argv: argv += ["--alarm-spool", str(_spool(tmp_path))]
        if "--state" in argv: argv[argv.index("--state") + 1] = str(tmp_path / f"{name}.state.json")
        else: argv += ["--state", str(tmp_path / f"{name}.state.json")]
        if "--cgroup" in argv: argv[argv.index("--cgroup") + 1] = str(tmp_path / "no-cgroup")
        else: argv += ["--cgroup", str(tmp_path / "no-cgroup")]
        assert m.main(argv) == 0
    return _records(tmp_path)


def _drain_row_problems(fm, seat):
    """r2, structural: the seat whose spool the posts row fills has ONE drain row, run in that seat's own uid."""
    rows = [r for r in fm.values() if isinstance(r, dict) and "alarm_spool.py drain" in str(r.get("cmd", ""))]
    mine = [r for r in rows if f"--seat {seat}" in r["cmd"]]
    out = []
    if len(mine) != 1: out.append(f"{len(mine)} drain rows for {seat}")
    out += [f"drain row user {r.get('user')!r} is not agi-{seat}" for r in mine if r.get("user") != f"agi-{seat}"]
    out += [f"drain row for {seat} is not enabled" for r in mine if r.get("enabled") is not True]
    return out


def test_one_alarm_through_both_real_cron_rows_is_exactly_one_spool_line(tmp_path, monkeypatch):
    _forbid_send_py(monkeypatch)
    rows = _real_rows(tmp_path)
    post = rows["memory_alarm_posts"][1]
    seat, reader = post[post.index("--alarm-seat") + 1], post[post.index("--alarm-to") + 1]
    assert rows["memory_alarm_posts"][0].get("user") == f"agi-{seat}"                                # the owning row runs AS the sending seat: its spool, its uid
    assert all("--alarm-to" not in a and "--alarm-seat" not in a for a in rows["memory_alarm"][1]) and reader == "belam"
    argvs = {k: v[1] for k, v in rows.items()}
    recs = _run_rows(tmp_path, monkeypatch, argvs, f"agi-{seat}")
    assert len(recs) == 1, recs                                                                       # ONE alarm, ONE message (memory_alarm_posts owns it)
    assert (tmp_path / "memory_alarm.log").read_text().count("WARN memory warn") == 1 and (tmp_path / "memory_alarm_posts.log").read_text().count("WARN memory warn") == 1   # the user@ job still logs its own line
    # MUTANT (falsifier b): the user@ job spools too = the alarm arrives twice = this row goes RED
    mut = dict(argvs); mut["memory_alarm"] = argvs["memory_alarm"] + ["--alarm-seat", seat, "--alarm-to", reader, "--alarm-job", "memory_alarm", "--alarm-spool-max", "500"]
    (tmp_path / "m").mkdir()
    assert len(_run_rows(tmp_path / "m", monkeypatch, mut, f"agi-{seat}")) == 2, "the doubled-notify mutant did not double"


def test_r2_the_seat_whose_spool_the_alarm_fills_has_its_own_uid_drain_row():
    fm = crons._parse_frontmatter(crons._node_path(REPO / ".agi"))["cadences"]
    post = fm["memory_alarm_posts"]["cmd"].split()
    seat = post[post.index("--alarm-seat") + 1]
    assert _drain_row_problems(fm, seat) == []
    no_row = {k: v for k, v in fm.items() if k != "alarm_drain"}                                      # MUTANT: the drain row is gone = the spool is never signed
    assert _drain_row_problems(no_row, seat)
    root_row = {**fm, "alarm_drain": {**fm["alarm_drain"], "user": "root"}}                           # MUTANT: a root drain = root signing as the seat
    assert _drain_row_problems(root_row, seat)


# --- goal:g7.16.1.11.20.2 row 2: the old nudge sweep (send.py wake --all-local) is retired -------------------

def test_the_real_nudge_sweep_cell_is_off_and_renders_no_wake_line_while_the_enabled_mutant_does(tmp_path):
    sys.path.insert(0, str(Path(__file__).parent))
    import test_crons as tc
    cell = crons._parse_frontmatter(crons._node_path(REPO / ".agi"))["cadences"]["nudge_sweep"]
    assert cell.get("enabled") is False, cell
    off = tc.make_project(tmp_path, cadences={"nudge_sweep": cell})
    lines = crons.render_managed_lines(off, off, off, crons.load_crons_node(off), box_name="encryption-town")
    assert not any("wake --all-local" in l or "send.py" in l for l in lines), lines
    on = tc.make_project(tmp_path, name="on", cadences={"nudge_sweep": {**cell, "enabled": True}})
    lines = crons.render_managed_lines(on, on, on, crons.load_crons_node(on), box_name="encryption-town")
    assert any("wake --all-local" in l for l in lines), "the enabled mutant renders nothing: the row proves nothing"


# --- goal:g7.16.1.11.20.2 target 4: the alarm CLEARS only below a clear line, held for a time ----------
# Falsifier, pre-fix: WARN 20:04:02Z (box some avg60 27.5) -> CLEARED 20:06:01Z, and a reading at 10.8 against a line of 10:
# it cleared on the FIRST tick under the line it raised at, so a reading hovering there raised and cleared every few minutes.

import types  # noqa: E402

from_cells = {"warn_avail_mib": 0, "crit_avail_mib": 0, "warn_psi_some_avg60": 10, "crit_psi_full_avg60": 1000,
              "warn_cgroup_max_frac": 1000, "warn_slab_mib": 1e12}


def _flap_argv(tmp_path, margin="0.8", hold="3"):
    return ["--root", str(tmp_path), "--warn-avail-mib", "0", "--crit-avail-mib", "0", "--warn-psi-some-avg60", "10",
            "--crit-psi-full-avg60", "1000", "--warn-cgroup-max-frac", "1000", "--warn-slab-mib", "1e12", "--repeat-mins", "1000",
            "--clear-margin-frac", margin, "--clear-hold-mins", hold, "--cgroup", str(tmp_path / "no-cgroup"),
            "--state", str(tmp_path / "st.json"), "--alerts-log", str(tmp_path / "alerts.log")]


def _drive(mod, tmp_path, ticks, **kw):
    """Run one tick per (minute, box some avg60) against `mod`; return the alerts-log lines."""
    clock = [0.0]; psi = [0.0]
    mod.time = types.SimpleNamespace(time=lambda: clock[0], strftime=__import__("time").strftime, gmtime=__import__("time").gmtime)
    mod.read_signals = lambda cg: {"avail_mib": 8000.0, "box_psi": {"some": {"avg60": psi[0]}, "full": {"avg60": 0.0}},
                                   "cg_psi": {}, "cg_current": None, "cg_max": None}
    mod.alarm_spool = types.SimpleNamespace(append=lambda *a, **k: None)
    for minute, v in ticks:
        clock[0] = 1_000_000.0 + minute * 60; psi[0] = v
        assert mod.main(_flap_argv(tmp_path, **kw)) == 0
    log = tmp_path / "alerts.log"
    return log.read_text().splitlines() if log.exists() else []


def _fresh(src=None):
    text = src if src is not None else Path(m.__file__).read_text()
    mod = types.ModuleType("memory_alarm_probe"); mod.__file__ = m.__file__
    exec(compile(text, m.__file__, "exec"), mod.__dict__)
    return mod


HOVER = [(0, 12.0), (1, 9.0), (2, 9.0), (3, 9.5), (4, 9.0), (5, 9.0), (6, 9.5), (7, 9.0)]   # sits between the clear line (8) and the warn line (10) for 7 minutes, over the hold


def test_a_reading_hovering_at_the_line_never_clears(tmp_path, monkeypatch):
    lines = _drive(_fresh(), tmp_path, HOVER)
    assert [l for l in lines if "CLEARED" in l] == [] and sum("WARN memory warn" in l for l in lines) == 1, lines


def test_it_clears_only_after_the_hold_below_the_clear_line(tmp_path):
    lines = _drive(_fresh(), tmp_path, [(0, 12.0), (1, 7.0), (2, 7.0), (3, 7.0), (3.9, 7.0)])    # below 8 since minute 1: 2.9 min < 3
    assert not any("CLEARED" in l for l in lines), lines
    (tmp_path / "b").mkdir()
    lines = _drive(_fresh(), tmp_path / "b", [(0, 12.0), (1, 7.0), (2, 7.0), (3, 7.0), (4.1, 7.0)])
    assert sum("CLEARED memory back to ok" in l for l in lines) == 1, lines


def test_a_tick_back_over_the_clear_line_restarts_the_hold(tmp_path):
    ticks = BREAK                                                                              # hold restarts at 3.0: 5.9 is 2.9 min on
    assert not any("CLEARED" in l for l in _drive(_fresh(), tmp_path, ticks))
    (tmp_path / "b").mkdir()
    assert any("CLEARED" in l for l in _drive(_fresh(), tmp_path / "b", ticks + [(6.1, 7.0)]))


def test_the_clear_line_is_in_the_raise_units(tmp_path):
    up = m.clear_line(argparse.Namespace(**{**from_cells, "warn_avail_mib": 2048, "crit_avail_mib": 1024, "clear_margin_frac": 0.8}))
    assert up.warn_psi_some_avg60 == 8 and up.warn_avail_mib == 2560 and up.crit_avail_mib == 1280, up   # PSI down, MemAvailable up
    th = argparse.Namespace(**{**from_cells, "clear_margin_frac": 0.8})
    assert m.decide(sig(box=(9.0, 0.0)), th, "warn")[0] == "warn" and m.decide(sig(box=(9.0, 0.0)), th, "ok")[0] == "ok"
    assert m.decide(sig(box=(7.0, 0.0)), th, "warn")[0] == "ok"


BREAK = [(0, 12.0), (1, 7.0), (2, 7.0), (2.5, 8.5), (3, 7.0), (5.9, 7.0)]
# HOVER sits in the band for longer than the hold, so only the no-band mutant (M1) shows there; BREAK needs the band AND the hold (all four)
HOVER_MUTANTS = {'th = clear_line(th)'}
BREAK_MUTANTS = {'th = clear_line(th)', 'a.clear_hold_mins * 60', '"clear" if now - float(state.get("ok_since", now)) >= hold_s else None', 'del state["ok_since"]'}


@pytest.mark.parametrize("old,new", [
    ('th = clear_line(th)', 'pass'),                                                    # M1: clear against the raise line again
    ('a.clear_hold_mins * 60', '0'),                                                    # M2: clear on the first tick below the line
    ('"clear" if now - float(state.get("ok_since", now)) >= hold_s else None', '"clear"'),   # M3: transition ignores the hold
    ('del state["ok_since"]', 'pass'),                                                  # M4: a break never restarts the hold
])
def test_each_mutant_of_the_clear_rule_goes_red_on_the_row_meant_for_it(tmp_path, old, new):
    src = Path(m.__file__).read_text()
    assert src.count(old) == 1, old                                                     # anchor: a mutant that matches 0 or 2 places proves nothing
    mut = src.replace(old, new)
    (tmp_path / "h").mkdir(); (tmp_path / "x").mkdir()
    hover = _drive(_fresh(mut), tmp_path / "h", HOVER)
    brk = _drive(_fresh(mut), tmp_path / "x", BREAK)
    assert any("CLEARED" in l for l in hover) == (old in HOVER_MUTANTS), (old, "hover row")      # the row meant for it, and ONLY it
    assert any("CLEARED" in l for l in brk) == (old in BREAK_MUTANTS), (old, "break row")


def test_both_real_rows_declare_the_margin_and_the_hold():
    for name in ("memory_alarm", "memory_alarm_posts"):
        cmd = crons._parse_frontmatter(crons._node_path(REPO / ".agi"))["cadences"][name]["cmd"].split()
        assert cmd[cmd.index("--clear-margin-frac") + 1] == "0.8" and cmd[cmd.index("--clear-hold-mins") + 1] == "3", name


# --- goal:g7.16.1.11.40.1.1 target 4: the cgroup-fill line reads against min(memory.high, memory.max) and names which ----------
# Falsifier, pre-fix: agi.slice is HELD at memory.high 5120 of memory.max 6144 MiB; at 5104 MiB (0.83 of max, 0.997 of high) the line,
# read against max, was silent by construction while the slice thrashed (slab 2713 MiB, 2.2 GB of the posts' anon swapped out).

MIB = 1 << 20


def test_a_slice_at_099_of_memory_high_warns_and_names_the_limit_it_was_read_against():
    level, reasons = m.decide(sig(anon=int(5000 * MIB), shmem=40 * MIB, unrec=29 * MIB, cap=6144 * MIB, high=5120 * MIB), TH)        # 0.99 of high, 0.825 of max
    assert level == "warn" and reasons == ["agi.slice unreclaimable memory at 99% of its memory.high (5069/5120 MiB = anon 5000 + shmem 40 + slab_unreclaimable 29)"], (level, reasons)


def test_a_slice_filled_to_memory_high_by_cache_is_quiet():
    # belam 01:0xZ 10-12, the first real alarm: memory.current 5118/5120 MiB, but anon 2542 + shmem 0 + slab_unreclaimable 14 and PSI full 0.31:
    # the rest is page cache and reclaimable slab that reclaim gives back. The old line (memory.current) fired every 15 minutes, for ever.
    quiet = sig(cur=5118 * MIB, anon=2542 * MIB, unrec=14 * MIB, cap=6144 * MIB, high=5120 * MIB, cg=(0.31, 0.31))
    assert m.decide(quiet, TH) == ("ok", [])
    hot = sig(cur=5118 * MIB, anon=5000 * MIB, shmem=60 * MIB, unrec=14 * MIB, cap=6144 * MIB, high=5120 * MIB)        # 5074/5120 = 0.991
    assert m.decide(hot, TH)[0] == "warn"


def test_a_thrash_with_small_anon_is_seen_by_psi_alone_and_crits_by_the_psi_reason():
    # council alive 01:24Z, SM 02:4xZ: 2026-10-11's thrash (anon 1638 MiB, ~2.2 GB of the posts' anon swapped, high 5120) reads 0.32 under the
    # fill line, so PSI is its ONLY witness. COMBINED row: small anon + PSI full over its line = crit, and the reasons are the PSI one alone.
    thrash = sig(cur=5104 * MIB, anon=1638 * MIB, unrec=15 * MIB, cap=6144 * MIB, high=5120 * MIB, cg=(60.0, 25.0))
    level, reasons = m.decide(thrash, TH)
    assert level == "crit" and reasons == ["agi.slice PSI full avg60 25.0% >= 20"], (level, reasons)
    assert m.decide(sig(cur=5104 * MIB, anon=1638 * MIB, unrec=15 * MIB, cap=6144 * MIB, high=5120 * MIB, cg=(0.31, 0.31)), TH) == ("ok", [])   # the same memory, no pressure


def test_the_mutant_that_drops_the_psi_line_goes_red_on_the_thrash_row():
    old = "if full60 is not None and full60 >= th.crit_psi_full_avg60:"
    src = Path(m.__file__).read_text(); assert src.count(old) == 1, old
    mut = _fresh(src.replace(old, "if False:"))
    thrash = sig(cur=5104 * MIB, anon=1638 * MIB, unrec=15 * MIB, cap=6144 * MIB, high=5120 * MIB, cg=(60.0, 25.0))
    assert m.decide(thrash, TH)[0] == "crit" and mut.decide(thrash, TH)[0] != "crit", "with the PSI line dropped nothing else may see the thrash"


def test_without_memory_stat_the_fill_falls_back_to_memory_current_and_says_so():
    level, reasons = m.decide(sig(cur=5104 * MIB, cap=6144 * MIB, high=5120 * MIB), TH)
    assert level == "warn" and reasons == ["agi.slice memory.current at 100% of its memory.high (5104/5120 MiB; memory.stat unreadable, so cache is counted too)"], reasons


def test_the_mutant_that_reads_memory_current_goes_red_on_the_quiet_row():
    old = "used = anon + (shmem or 0) + unrec"
    src = Path(m.__file__).read_text(); assert src.count(old) == 1, old
    mut = _fresh(src.replace(old, "used = cur"))
    quiet = sig(cur=5118 * MIB, anon=2542 * MIB, unrec=14 * MIB, cap=6144 * MIB, high=5120 * MIB)
    assert m.decide(quiet, TH)[0] == "ok" and mut.decide(quiet, TH)[0] == "warn", "the memory.current reading must warn on the quiet row"


def test_the_alarm_text_names_the_cgroup_it_read_not_user_at():
    reasons = m.decide(sig(anon=5100 * MIB, unrec=10 * MIB, cap=6144 * MIB, high=5120 * MIB, cg=(40.0, 0.0), name="agi.slice"), TH)[1]
    assert reasons and all("user@" not in r and r.startswith("agi.slice") for r in reasons), reasons
    reasons = m.decide(sig(anon=5900 * MIB, unrec=10 * MIB, cap=6144 * MIB, name="user@1000.service"), TH)[1]
    assert reasons and reasons[0].startswith("user@1000.service unreclaimable"), reasons


def test_the_lower_of_the_two_limits_wins_and_an_unset_high_falls_back_to_max():
    assert m.decide(sig(anon=5890 * MIB, unrec=10 * MIB, cap=6144 * MIB, high=7000 * MIB), TH)[1] == ["agi.slice unreclaimable memory at 96% of its memory.max (5900/6144 MiB = anon 5890 + shmem 0 + slab_unreclaimable 10)"]   # high ABOVE max: max is the limit
    assert m.decide(sig(anon=5890 * MIB, unrec=10 * MIB, cap=6144 * MIB, high=None), TH)[0] == "warn"                                                      # memory.high = max (unset)
    assert m.decide(sig(anon=5890 * MIB, unrec=10 * MIB, cap=None, high=None), TH) == ("ok", [])                                                           # no limit at all: no fill line
    assert m.decide(sig(anon=3990 * MIB, unrec=10 * MIB, cap=6144 * MIB, high=5120 * MIB), TH)[0] == "ok"                                                  # 0.78 of high: quiet


def test_read_signals_reads_memory_high_from_the_cgroup(tmp_path):
    cg = tmp_path / "cg"; cg.mkdir()
    (cg / "memory.current").write_text("5352366080\n"); (cg / "memory.max").write_text("6442450944\n"); (cg / "memory.high").write_text("5368709120\n")
    (cg / "memory.pressure").write_text("some avg10=0.00 avg60=0.00 avg300=0.00 total=0\nfull avg10=0.00 avg60=0.00 avg300=0.00 total=0\n")
    got = m.read_signals(cg)
    assert (got["cg_current"], got["cg_max"], got["cg_high"]) == (5352366080, 6442450944, 5368709120)
    (cg / "memory.high").write_text("max\n")
    assert m.read_signals(cg)["cg_high"] is None                                                       # `max` is no limit


def test_the_mutant_that_reads_against_max_goes_red_on_the_high_row():
    old = "cap, which = min(limits)"                                                                  # the unreclaimable branch and the memory.current fallback
    src = Path(m.__file__).read_text(); assert src.count(old) == 2, old
    mut = _fresh(src.replace(old, "cap, which = [l for l in limits if l[1] == 'memory.max'][0] if any(l[1] == 'memory.max' for l in limits) else limits[0]"))
    s = sig(anon=int(5040 * MIB), unrec=29 * MIB, cap=6144 * MIB, high=5120 * MIB)
    assert m.decide(s, TH)[0] == "warn" and mut.decide(s, TH)[0] == "ok", "today's /max reading must be silent: the row would prove nothing"


# --- goal:g7.16.1.11.40.1.1 target 3b: a slice held at memory.high by KERNEL SLAB is raised as SLAB, by name; nothing here drops caches ----------
# Falsifier, pre-fix: 2026-10-11 agi.slice sat at 5104/5120 MiB with 1638 MiB anon and 2713 MiB slab; MemAvailable was 4.3 GB free, PSI named no
# cause: the alarm said nothing about the dentry/inode cache that was swapping the posts' anon out.

def test_a_slab_over_the_line_raises_a_slab_named_alarm_while_anon_is_small_and_memory_is_free():
    s = sig(slab=2713 * MIB, rec=2698 * MIB, anon=1638 * MIB, avail=4371.0)                       # tonight's reading
    level, reasons = m.decide(s, TH)
    assert level == "warn" and reasons == ["agi.slice kernel SLAB 2713 MiB >= 1536 (reclaimable 2698, anon 1638 MiB) -- dentry/inode cache; the box owner drops caches, nothing here does"], reasons


def test_a_slab_under_the_line_is_quiet_and_a_missing_stat_is_no_signal():
    assert m.decide(sig(slab=130 * MIB, rec=100 * MIB, anon=1600 * MIB), TH) == ("ok", [])         # after the drop
    assert m.decide(sig(slab=None), TH) == ("ok", [])


def test_a_raised_slab_alarm_is_held_to_the_clear_line_not_the_raise_line():
    th = argparse.Namespace(**{**vars(TH), "warn_slab_mib": 1536})
    assert m.decide(sig(slab=1400 * MIB), th, "warn")[0] == "warn"                                   # 1400 > 1536 * 0.8 = 1229: still raised
    assert m.decide(sig(slab=1100 * MIB), th, "warn")[0] == "ok"
    assert m.decide(sig(slab=1400 * MIB), th, "ok")[0] == "ok"                                       # but 1400 never RAISES it


def test_read_signals_reads_the_slab_and_anon_from_memory_stat(tmp_path):
    cg = tmp_path / "agi.slice"; cg.mkdir()
    (cg / "memory.stat").write_text("anon 1717567488\nfile 100\nslab_reclaimable 2829156352\nslab_unreclaimable 15728640\nslab 2844884992\n")
    got = m.read_signals(cg)
    assert (got["cg_name"], got["cg_slab"], got["cg_slab_rec"], got["cg_anon"]) == ("agi.slice", 2844884992, 2829156352, 1717567488)
    (cg / "memory.stat").write_text("slab_reclaimable 10\nslab_unreclaimable 5\n")                    # no `slab` sum: the two parts
    assert m.read_signals(cg)["cg_slab"] == 15
    (cg / "memory.stat").unlink()
    assert m.read_signals(cg)["cg_slab"] is None


def test_the_slab_alarm_reaches_the_spool_once_and_stays_quiet_inside_the_repeat_window(tmp_path, monkeypatch):
    _stub(tmp_path, monkeypatch)
    monkeypatch.setattr(m, "read_signals", lambda cg: sig(slab=2713 * MIB, rec=2698 * MIB, anon=1638 * MIB, avail=4371.0))
    argv = ["--root", str(tmp_path), "--warn-avail-mib", "0", "--crit-avail-mib", "0", "--warn-psi-some-avg60", "1000", "--crit-psi-full-avg60", "1000",
            "--warn-cgroup-max-frac", "1000", "--warn-slab-mib", "1536", "--repeat-mins", "15", "--clear-margin-frac", "0.8", "--clear-hold-mins", "3",
            "--cgroup", str(tmp_path / "no-cgroup"), "--state", str(tmp_path / "st.json"), "--alerts-log", str(tmp_path / "alerts.log"), *_alarm(tmp_path)]
    assert m.main(argv) == 0 and m.main(argv) == 0
    (rec,) = _records(tmp_path)
    assert rec["text"].startswith("[memory-alarm-warn] ") and "kernel SLAB 2713 MiB" in rec["text"], rec


def test_the_mutant_that_looks_at_anon_only_goes_red_on_the_slab_row():
    old = "if slab is not None and slab / 1048576 >= th.warn_slab_mib:"
    src = Path(m.__file__).read_text(); assert src.count(old) == 1, old
    mut = _fresh(src.replace(old, "if False:"))                                                      # MUTANT: the alarm ignores slab (anon-only, as before)
    s = sig(slab=2713 * MIB, rec=2698 * MIB, anon=1638 * MIB, avail=4371.0)
    assert m.decide(s, TH)[0] == "warn" and mut.decide(s, TH)[0] == "ok"


def test_both_real_rows_carry_the_slab_line():
    for name in ("memory_alarm", "memory_alarm_posts"):
        cmd = crons._parse_frontmatter(crons._node_path(REPO / ".agi"))["cadences"][name]["cmd"].split()
        assert cmd[cmd.index("--warn-slab-mib") + 1] == "1536", name
