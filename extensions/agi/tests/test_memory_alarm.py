"""memory_alarm.py: the owner's 09-26 memory alarm (raise before the box wedges)."""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "bin"))
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
