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

TH = argparse.Namespace(warn_avail_mib=2048, crit_avail_mib=1024,
                        warn_psi_some_avg60=10, crit_psi_full_avg60=20,
                        warn_cgroup_max_frac=0.95, clear_margin_frac=0.8)


def sig(avail=8000.0, box=(0.0, 0.0), cg=(0.0, 0.0), cur=None, cap=None):
    def psi(some, full):
        return {"some": {"avg10": some, "avg60": some}, "full": {"avg10": full, "avg60": full}}
    return {"avail_mib": avail, "box_psi": psi(*box), "cg_psi": psi(*cg),
            "cg_current": cur, "cg_max": cap}


def test_quiet_box_is_ok():
    assert m.decide(sig(), TH) == ("ok", [])


def test_low_available_warns_then_crits():
    assert m.decide(sig(avail=1500), TH)[0] == "warn"
    assert m.decide(sig(avail=900), TH)[0] == "crit"


def test_pressure_inside_the_user_cap_is_seen_while_the_box_is_calm():
    assert m.decide(sig(cg=(12.0, 0.0)), TH)[0] == "warn"
    level, reasons = m.decide(sig(cg=(50.0, 25.0)), TH)
    assert level == "crit" and any(r.startswith("user@ PSI full") for r in reasons)


def test_user_cap_fill_warns_only_near_the_hard_cap():
    assert m.decide(sig(cur=5600 << 20, cap=5829 << 20), TH)[0] == "warn"
    assert m.decide(sig(cur=4000 << 20, cap=5829 << 20), TH)[0] == "ok"


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
            "--alerts-log", str(tmp_path / "alerts.log"), "--notify", "belam"]


def test_an_ok_run_writes_and_sends_nothing(tmp_path, capsys, monkeypatch):
    sent = []
    monkeypatch.setattr(m, "_notice", lambda *a: sent.append(a))
    rc = m.main(_args(tmp_path, "--warn-avail-mib", "0", "--crit-avail-mib", "0",
                      "--warn-psi-some-avg60", "1000", "--clear-margin-frac", "1", "--clear-hold-mins", "0", "--crit-psi-full-avg60", "1000",
                      "--warn-cgroup-max-frac", "1000"))
    assert rc == 0 and sent == [] and capsys.readouterr().out == ""
    assert not (tmp_path / "alerts.log").exists() and not (tmp_path / "st.json").exists()


def test_a_raise_logs_once_dms_once_then_stays_quiet(tmp_path, monkeypatch):
    sent = []
    monkeypatch.setattr(m, "_notice", lambda post, body, nb=None: sent.append((post, body)))
    argv = _args(tmp_path, "--warn-avail-mib", "1e12", "--crit-avail-mib", "0",
                 "--warn-psi-some-avg60", "1000", "--clear-margin-frac", "1", "--clear-hold-mins", "0", "--crit-psi-full-avg60", "1000",
                 "--warn-cgroup-max-frac", "1000")
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
    monkeypatch.setattr(m, "_notice", lambda *a: None)
    argv = ["--root", str(root), "--warn-avail-mib", "1e12",
            "--crit-avail-mib", "0", "--warn-psi-some-avg60", "1000", "--clear-margin-frac", "1", "--clear-hold-mins", "0",
            "--crit-psi-full-avg60", "1000", "--warn-cgroup-max-frac", "1000",
            "--repeat-mins", "15", "--cgroup", str(tmp_path / "no-cgroup"),
            "--state", str(tmp_path / "st.json"), "--notify", "belam"]
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
    monkeypatch.setattr(m, "_notice", lambda *a: None)
    argv = ["--root", str(root), "--warn-avail-mib", "1e12",
            "--crit-avail-mib", "0", "--warn-psi-some-avg60", "1000", "--clear-margin-frac", "1", "--clear-hold-mins", "0",
            "--crit-psi-full-avg60", "1000", "--warn-cgroup-max-frac", "1000",
            "--repeat-mins", "15", "--cgroup", str(tmp_path / "no-cgroup")]
    assert m.main(argv) == 0
    state = locations.sessions_dir(root) / m.STATE_FILE
    assert state.is_file() and json.loads(state.read_text())["level"] == "warn"
    src = Path(m.__file__).read_text()
    assert 'STATE_FILE' in src and '"sessions"' not in src.split("def main")[1]


# --- goal:g7.16.1.11.20.2 cut 1: the old inbox mail is OUT of this path -------------------------------

BIN = Path(m.__file__).resolve()
REPO = BIN.parents[3]
STUB_NOTICE = "#!/bin/sh\n[ \"$1\" = add ] || exit 2\nprintf '%s\\n' \"$2\" >> \"$NOTICE_OUT\"\n"


def test_send_py_is_out_of_memory_alarm_entirely():
    text = BIN.read_text()
    assert "send.py" not in text and "_dm" not in text and "from send" not in text and "import send" not in text, "the old mail path is back"


def _stub(tmp_path, monkeypatch, uid="agi-belam"):
    out = tmp_path / "notices.out"; exe = tmp_path / "agi-notice"
    exe.write_text(STUB_NOTICE); exe.chmod(0o755)
    monkeypatch.setenv("NOTICE_OUT", str(out)); monkeypatch.setattr(m, "_uid_name", lambda: uid)
    return exe, out


def _forbid_send_py(monkeypatch):
    real = m.subprocess.run
    def guard(cmd, *a, **k):
        assert "send.py" not in " ".join(map(str, cmd)), cmd           # a send.py spawn fails the row
        return real(cmd, *a, **k)
    monkeypatch.setattr(m.subprocess, "run", guard)


def _warn_args(tmp_path, *extra, state="st.json", log="alerts.log"):
    return ["--root", str(tmp_path), "--warn-avail-mib", "1e12", "--crit-avail-mib", "0", "--warn-psi-some-avg60", "1000", "--clear-margin-frac", "1", "--clear-hold-mins", "0",
            "--crit-psi-full-avg60", "1000", "--warn-cgroup-max-frac", "1000", "--repeat-mins", "15",
            "--cgroup", str(tmp_path / "no-cgroup"), "--state", str(tmp_path / state), "--alerts-log", str(tmp_path / log), *extra]


def test_the_notice_is_the_posts_own_agi_notice_in_its_own_uid(tmp_path, monkeypatch):
    exe, out = _stub(tmp_path, monkeypatch); _forbid_send_py(monkeypatch)
    assert m.main(_warn_args(tmp_path, "--notify", "belam", "--notice-bin", str(exe))) == 0
    lines = out.read_text().splitlines()
    assert len(lines) == 1, lines
    kind, ev, rest = lines[0].split(" ", 2)
    assert kind == "[memory-alarm-warn]" and len(ev) == 8 and int(ev, 16) > 0 and "WARN memory warn: MemAvailable " in rest, lines[0]
    assert m.main(_warn_args(tmp_path, "--notify", "belam", "--notice-bin", str(exe))) == 0               # inside the repeat window: silent
    assert len(out.read_text().splitlines()) == 1
    # kinds are separate agi-notice keys: a CLEARED is never eaten by an unread ALARM
    assert m.main(["--root", str(tmp_path), "--warn-avail-mib", "0", "--crit-avail-mib", "0", "--warn-psi-some-avg60", "1000", "--clear-margin-frac", "1", "--clear-hold-mins", "0", "--crit-psi-full-avg60", "1000",
                   "--warn-cgroup-max-frac", "1000", "--repeat-mins", "15", "--cgroup", str(tmp_path / "no-cgroup"), "--state", str(tmp_path / "st.json"),
                   "--alerts-log", str(tmp_path / "alerts.log"), "--notify", "belam", "--notice-bin", str(exe)]) == 0
    lines = out.read_text().splitlines()
    assert len(lines) == 2 and lines[1].startswith("[memory-alarm-cleared] "), lines


def test_from_the_wrong_uid_nothing_is_written_it_says_so_and_never_falls_back(tmp_path, monkeypatch, capsys):
    exe, out = _stub(tmp_path, monkeypatch, uid="belam"); _forbid_send_py(monkeypatch)             # the cron job still running as uid belam
    assert m.main(_warn_args(tmp_path, "--notify", "belam", "--notice-bin", str(exe))) == 0
    assert not out.exists(), "a notice was written from the wrong uid"
    err = capsys.readouterr().err
    assert "notice to belam NOT written" in err and "must run as agi-belam" in err, err
    assert "NOTICE to belam NOT written" in (tmp_path / "alerts.log").read_text()                   # and in the log: never a silent failure
    capsys.readouterr()
    exe.write_text("#!/bin/sh\nexit 3\n")                                                          # right uid, agi-notice fails: the same two places say so
    monkeypatch.setattr(m, "_uid_name", lambda: "agi-belam")
    assert m.main(_warn_args(tmp_path, "--notify", "belam", "--notice-bin", str(exe), state="st2.json", log="alerts2.log")) == 0
    assert "exit 3" in capsys.readouterr().err and "exit 3" in (tmp_path / "alerts2.log").read_text()


def _real_rows(tmp_path):
    fm = crons._parse_frontmatter(crons._node_path(REPO / ".agi"))["cadences"]
    out = {}
    for name in ("memory_alarm", "memory_alarm_posts"):
        row = fm[name]
        cmd = row["cmd"].replace("{repo_root}", str(REPO)).replace("{root}", str(tmp_path))
        argv = cmd.split()[2:]                                                                       # drop `python3 memory_alarm.py`
        out[name] = (row, argv)
    return out


def test_one_alarm_through_both_real_cron_rows_is_exactly_one_notice(tmp_path, monkeypatch):
    exe, out = _stub(tmp_path, monkeypatch); _forbid_send_py(monkeypatch)
    rows = _real_rows(tmp_path)
    for name, (row, argv) in rows.items():
        assert row.get("user") == "agi-belam", (name, row.get("user"))                              # both rows run AS the Prime's own uid
    for name, (row, argv) in rows.items():
        argv = [a for a in argv]
        i = argv.index("--warn-avail-mib"); argv[i + 1] = "1e12"                                      # force a warn on the box-wide signal both jobs read
        argv += ["--alerts-log", str(tmp_path / f"{name}.log"), "--notice-bin", str(exe)]
        if "--state" not in argv: argv += ["--state", str(tmp_path / f"{name}.state.json")]
        else: argv[argv.index("--state") + 1] = str(tmp_path / f"{name}.state.json")
        if "--cgroup" in argv: argv[argv.index("--cgroup") + 1] = str(tmp_path / "no-cgroup")
        else: argv += ["--cgroup", str(tmp_path / "no-cgroup")]
        assert m.main(argv) == 0
    lines = out.read_text().splitlines()
    assert len(lines) == 1, lines                                                                    # ONE alarm, ONE notice (memory_alarm_posts owns it)
    assert all("--notify" not in a for a in rows["memory_alarm"][1]) and "--notify" in rows["memory_alarm_posts"][1]
    assert (tmp_path / "memory_alarm.log").read_text().count("WARN memory warn") == 1 and (tmp_path / "memory_alarm_posts.log").read_text().count("WARN memory warn") == 1      # the user@ job still logs its own line


# --- goal:g7.16.1.11.20.2 target 4: the alarm CLEARS only below a clear line, held for a time ----------
# Falsifier, pre-fix: WARN 20:04:02Z (box some avg60 27.5) -> CLEARED 20:06:01Z, and a reading at 10.8 against a line of 10:
# it cleared on the FIRST tick under the line it raised at, so a reading hovering there raised and cleared every few minutes.

import types  # noqa: E402

from_cells = {"warn_avail_mib": 0, "crit_avail_mib": 0, "warn_psi_some_avg60": 10, "crit_psi_full_avg60": 1000,
              "warn_cgroup_max_frac": 1000}


def _flap_argv(tmp_path, margin="0.8", hold="3"):
    return ["--root", str(tmp_path), "--warn-avail-mib", "0", "--crit-avail-mib", "0", "--warn-psi-some-avg60", "10",
            "--crit-psi-full-avg60", "1000", "--warn-cgroup-max-frac", "1000", "--repeat-mins", "1000",
            "--clear-margin-frac", margin, "--clear-hold-mins", hold, "--cgroup", str(tmp_path / "no-cgroup"),
            "--state", str(tmp_path / "st.json"), "--alerts-log", str(tmp_path / "alerts.log")]


def _drive(mod, tmp_path, ticks, **kw):
    """Run one tick per (minute, box some avg60) against `mod`; return the alerts-log lines."""
    clock = [0.0]; psi = [0.0]
    mod.time = types.SimpleNamespace(time=lambda: clock[0], strftime=__import__("time").strftime, gmtime=__import__("time").gmtime)
    mod.read_signals = lambda cg: {"avail_mib": 8000.0, "box_psi": {"some": {"avg60": psi[0]}, "full": {"avg60": 0.0}},
                                   "cg_psi": {}, "cg_current": None, "cg_max": None}
    mod._notice = lambda *a: None
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
