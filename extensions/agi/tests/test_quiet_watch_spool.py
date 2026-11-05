"""goal:g7.16.1.11.20.2 C2: ROOT NEVER SIGNS. agi-quiet-watch only appends a plain line to the sending seat's spool."""
import json
import os
import re
import stat
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[3]
GUARD = REPO / "extensions" / "agi" / "guard"
SCRIPT = GUARD / "quiet-watch" / "agi-quiet-watch"
SPOOL_PY = REPO / "extensions" / "agi" / "bin" / "alarm_spool.py"

#: the script as it was at 571f300635: root runuser's into the seat and runs `box send` (r1's one hit, quiet-watch:24)
OLD_SEND = ('''if printf '%s\\n' "$m" | runuser -u "agi-$SELF" -- env HOME="/var/lib/agi/$SELF" AGI_POST="$SELF" '''
            '''PATH="/var/lib/agi/$SELF/bin:/opt/agi/bin:/usr/local/bin:/usr/bin:/bin" sh -c 'cd ~/t && box send "$1"' _ "$TO";then''')

#: what r1 forbids in a script a root unit/timer ExecStart's
FORBIDDEN = (re.compile(r"\bbox\s+send\b"), re.compile(r"ssh-keygen\s+-Y\s+sign"))


def _stubs(tmp_path):
    """PATH stubs: one running post 'dg-x' idle for ages, runuser that drops `-u USER --` and runs the rest, logger/box recorders."""
    d = tmp_path / "stubs"; d.mkdir()
    def stub(name, body):
        p = d / name; p.write_text("#!/bin/sh\n" + body); p.chmod(p.stat().st_mode | stat.S_IXUSR)
    stub("systemctl", "echo 'agi-post@dg-x.service loaded active running agi post'\n")
    stub("pgrep", '[ "$1" = -P ] && exit 0\necho 4242\n')
    stub("find", "echo 100.0\n")
    stub("runuser", 'echo "$2" >> "$STUB_LOG.runuser"\nshift 3\nexec "$@"\n')
    stub("logger", 'echo "$*" >> "$STUB_LOG.logger"\n')
    stub("box", 'echo "box $*" >> "$STUB_LOG.box"\n')                        # a root unit that reaches box = the breach
    return d


def _run(tmp_path, script=SCRIPT, extra_env=None):
    if not (tmp_path / "stubs").exists():
        _stubs(tmp_path)
    env = {"PATH": f"{tmp_path / 'stubs'}:/usr/bin:/bin", "HOME": str(tmp_path),
           "S": str(tmp_path / "state"), "STUB_LOG": str(tmp_path / "log"), "AS": str(SPOOL_PY), "STORES": str(tmp_path), **(extra_env or {})}
    return subprocess.run(["sh", str(script)], env=env, capture_output=True, text=True, timeout=60)


def _spool_for(tmp_path):
    """SELF (belam)'s spool is $STORES/belam/alarm.spool: STORES points at tmp, so the real script runs unpatched."""
    (tmp_path / "belam").mkdir(exist_ok=True)
    return SCRIPT, tmp_path / "belam" / "alarm.spool"


def test_a_quiet_town_appends_one_plain_line_to_belams_spool_and_root_touches_no_box(tmp_path):
    script, spool = _spool_for(tmp_path)
    r = _run(tmp_path, script)
    assert r.returncode == 0, r.stderr
    (line,) = spool.read_text().splitlines()
    rec = json.loads(line)
    assert rec["job"] == "quiet-watch" and rec["to"] == "sanctuary-master" and rec["text"].startswith("[quiet] agi-quiet-watch "), rec
    assert (tmp_path / "log.runuser").read_text().strip() == "agi-belam"                   # appended AS the sending seat, a plain line
    assert not (tmp_path / "log.box").exists(), "root reached `box`: it signed"           # r1/r2 at runtime
    assert "spooled for sanctuary-master" in (tmp_path / "log.logger").read_text()
    # at most once per GAP: the second tick adds nothing
    assert _run(tmp_path, script).returncode == 0 and len(spool.read_text().splitlines()) == 1


def test_a_busy_town_spools_nothing(tmp_path):
    script, spool = _spool_for(tmp_path)
    _stubs(tmp_path)
    (tmp_path / "stubs" / "find").write_text(f"#!/bin/sh\necho {10**10}.0\n")             # a transcript from the far future = younger than Q
    assert _run(tmp_path, script).returncode == 0 and not spool.exists()



def test_a_background_shell_is_not_busy(tmp_path):
    """belam 18:2xZ 10-25: the town idled 15 h after L121 and this never fired, because alive and director-goals-1 each held a
    background shell (a claude child), which the old descendant test read as busy for good. A child alone is now quiet."""
    script, spool = _spool_for(tmp_path)
    _stubs(tmp_path)
    (tmp_path / "stubs" / "pgrep").write_text('#!/bin/sh\n[ "$1" = -P ] && { echo 5151; exit 0; }\necho 4242\n')   # a live child
    (tmp_path / "dg-x").mkdir(); o = tmp_path / "dg-x" / "o"; o.write_text("x"); os.utime(o, (1, 1))   # a still screen
    assert _run(tmp_path, script).returncode == 0
    assert len(spool.read_text().splitlines()) == 1


def test_a_freshly_redrawn_screen_is_busy(tmp_path):
    """a turn or a foreground tool redraws its spinner into ~/o: a screen changed inside QUIET s means busy, nothing spooled."""
    script, spool = _spool_for(tmp_path)
    _stubs(tmp_path)
    (tmp_path / "dg-x").mkdir(); (tmp_path / "dg-x" / "o").write_text("x")                 # mtime = now
    assert _run(tmp_path, script).returncode == 0 and not spool.exists()

# --- r1: the scripts every root unit/timer ExecStart's carry no `box send` and no `ssh-keygen -Y sign` -------------

def _root_scripts():
    """The guard scripts a .service in extensions/agi/guard ExecStart's (installed to /usr/local/sbin or /opt/agi/bin)."""
    out = {}
    for svc in sorted(GUARD.rglob("*.service")):
        for m in re.finditer(r"^ExecStart=(\S+)", svc.read_text(), re.M):
            name = Path(m.group(1)).name
            for cand in svc.parent.glob(name):
                out[str(cand.relative_to(REPO))] = cand.read_text()
    return out


def _r1(scripts):
    return sorted(f"{path}:{n}" for path, text in scripts.items() for n, line in enumerate(text.splitlines(), 1)
                  if any(p.search(line) for p in FORBIDDEN))


def test_r1_no_root_execstart_script_signs_or_box_sends():
    scripts = _root_scripts()
    assert "extensions/agi/guard/quiet-watch/agi-quiet-watch" in scripts, scripts.keys()    # the scan sees the unit it exists for
    assert _r1(scripts) == []


def test_r1_the_old_quiet_watch_is_red():
    text = SCRIPT.read_text()
    old = text[: text.index("# ROOT NEVER SIGNS")] + OLD_SEND + "\n echo \"$now\" >\"$S/last\"\nfi\n"
    hits = _r1({"quiet-watch": old})
    assert hits and hits[0].startswith("quiet-watch:"), hits                                  # MUTANT re-adding quiet-watch:24 = RED


def test_r1_a_signing_command_in_any_script_is_red():
    assert _r1({"x": "ssh-keygen -Y sign -f k -n box file\n"}) == ["x:1"]


def test_the_runtime_row_catches_a_root_script_that_reaches_box(tmp_path):
    script, spool = _spool_for(tmp_path)
    text = script.read_text(); assert text.count("# ROOT NEVER SIGNS") == 1
    script = tmp_path / "agi-quiet-watch"
    script.write_text(text.replace("# ROOT NEVER SIGNS", 'box send "$TO" </dev/null\n# ROOT NEVER SIGNS', 1))   # MUTANT: root calls box
    assert _run(tmp_path, script).returncode == 0
    assert (tmp_path / "log.box").exists(), "the stub box was never reached: the runtime row proves nothing"


def test_r2_the_seat_whose_spool_quiet_watch_fills_has_its_own_uid_drain_row():
    sys.path.insert(0, str(REPO / "extensions" / "agi" / "bin"))
    import crons
    seat = re.search(r"SELF=\$\{SELF:-([a-z0-9-]+)\}", SCRIPT.read_text()).group(1)
    fm = crons._parse_frontmatter(crons._node_path(REPO / ".agi"))["cadences"]
    rows = [r for r in fm.values() if isinstance(r, dict) and f"alarm_spool.py drain --seat {seat} " in str(r.get("cmd", "")) + " "]
    assert len(rows) == 1 and rows[0].get("user") == f"agi-{seat}" and rows[0].get("enabled") is True, rows   # belam's spool is signed in belam's uid
    assert "--max-tries" in rows[0]["cmd"]
    assert f"agi-{seat}" in SCRIPT.read_text().replace('"agi-$SELF"', f"agi-{seat}")                              # and the append is runuser'd as that same seat


def test_a_failed_append_is_also_one_notice_line_in_the_seats_own_file_and_is_retried(tmp_path):
    script, spool = _spool_for(tmp_path)
    r = _run(tmp_path, script, {"AS": str(tmp_path / "no-such-alarm_spool.py")})                  # the append fails (python cannot open its script)
    assert r.returncode == 0 and not spool.exists()
    note = (tmp_path / "belam" / ".notice").read_text().splitlines()                              # HOME=$STORES/belam: the seat's own file, no agi-notice there
    assert len(note) == 1 and note[0].startswith("[quiet-watch-unspooled] ") and "NOT spooled" in note[0], note
    assert "spool append for sanctuary-master FAILED" in (tmp_path / "log.logger").read_text()
    assert (tmp_path / "log.runuser").read_text().split() == ["agi-belam", "agi-belam"]           # both the append and the notice ran AS the seat
    assert not (tmp_path / "state" / "last").exists()                                              # no stamp: the next minute tries again, no 30-minute silence
    assert _run(tmp_path, script).returncode == 0 and len(spool.read_text().splitlines()) == 1    # and the retry lands
