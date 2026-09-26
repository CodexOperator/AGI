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
                        warn_cgroup_max_frac=0.95)


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
    monkeypatch.setattr(m, "_dm", lambda *a: sent.append(a))
    rc = m.main(_args(tmp_path, "--warn-avail-mib", "0", "--crit-avail-mib", "0",
                      "--warn-psi-some-avg60", "1000", "--crit-psi-full-avg60", "1000",
                      "--warn-cgroup-max-frac", "1000"))
    assert rc == 0 and sent == [] and capsys.readouterr().out == ""
    assert not (tmp_path / "alerts.log").exists() and not (tmp_path / "st.json").exists()


def test_a_raise_logs_once_dms_once_then_stays_quiet(tmp_path, monkeypatch):
    sent = []
    monkeypatch.setattr(m, "_dm", lambda repo, post, body: sent.append((post, body)))
    argv = _args(tmp_path, "--warn-avail-mib", "1e12", "--crit-avail-mib", "0",
                 "--warn-psi-some-avg60", "1000", "--crit-psi-full-avg60", "1000",
                 "--warn-cgroup-max-frac", "1000")
    assert m.main(argv) == 0
    lines = (tmp_path / "alerts.log").read_text().splitlines()
    assert len(lines) == 1 and " WARN memory warn: MemAvailable " in lines[0]
    assert len(sent) == 1 and sent[0][0] == "belam" and sent[0][1].startswith("[red] ")
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
    monkeypatch.setattr(m, "_dm", lambda *a: None)
    argv = ["--root", str(root), "--warn-avail-mib", "1e12",
            "--crit-avail-mib", "0", "--warn-psi-some-avg60", "1000",
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
    monkeypatch.setattr(m, "_dm", lambda *a: None)
    argv = ["--root", str(root), "--warn-avail-mib", "1e12",
            "--crit-avail-mib", "0", "--warn-psi-some-avg60", "1000",
            "--crit-psi-full-avg60", "1000", "--warn-cgroup-max-frac", "1000",
            "--repeat-mins", "15", "--cgroup", str(tmp_path / "no-cgroup")]
    assert m.main(argv) == 0
    state = locations.sessions_dir(root) / m.STATE_FILE
    assert state.is_file() and json.loads(state.read_text())["level"] == "warn"
    src = Path(m.__file__).read_text()
    assert 'STATE_FILE' in src and '"sessions"' not in src.split("def main")[1]
