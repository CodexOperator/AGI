"""goal:g7.16.1.5.5.5 -- guard-init.sh reads every memory number from a config:guard
cell, and refuses a bad cell BY NAME before any bash arithmetic reads it.

A fixture run of guard-init's value derivation only: the `# --- cells` block is cut
out of the script and run under bash with a fixed RAM/SWAP, no systemctl, no /proc.
"""
from __future__ import annotations

import os
import re
import subprocess
from pathlib import Path

import pytest

SRC = (Path(__file__).resolve().parents[1] / "guard" / "guard-init.sh").read_text(encoding="utf-8")
BLOCK = SRC[SRC.index("# --- cells (goal:g7.16.1.5.5.5)"):SRC.index("# --- cells end")]
TO_MIB = re.search(r"^to_mib\(\) \{.*?^\}\n", SRC, re.M | re.S).group(0)
HOSTVAR = re.search(r"^hostvar\(\) \{.*\}\n", SRC, re.M).group(0)
OUT = ("RESERVE_M DOCKER_M PSI_FULL OOMD_LIMIT USER_HIGH_PCT GRACE_S USER_MAX_M USER_HIGH_M "
       "USER_SWAP_M AGI_MAX_M AGI_HIGH_M ENGINE_MAX_M ENGINE_HIGH_M WORK_MAX_M WORK_HIGH_M "
       "CLAUDE_LOW_M AGI_OOMD_LIMIT OOMD_SWAP_USED_PCT OOMD_PRESSURE_PCT OOMD_PRESSURE_S "
       "SYSTEM_MIN_M SSH_MIN_M USER_MIN_M DOCKER_CAP_HEADROOM_PCT DEFER_PCT ENGINE_SWAP "
       "RAMDISK_SWAP").split()
# Today's literal for every cell this goal added -- set explicitly, the derivation must not move.
LITERALS = {"USER_SWAP_PCT": "50", "USER_SWAP_CAP": "2048M", "AGI_MAX_PCT": "70",
            "AGI_HIGH_PCT": "90", "ENGINE_HIGH_PCT": "75", "WORK_HIGH_PCT": "90",
            "AGI_OOMD_LIMIT": "40", "OOMD_SWAP_USED_PCT": "90", "OOMD_PRESSURE_PCT": "60",
            "OOMD_PRESSURE_S": "20", "SYSTEM_MIN": "128M", "SSH_MIN": "64M",
            "CLAUDE_LOW_DIV": "6", "CLAUDE_LOW_CAP": "1024M", "ENGINE_SWAP_MAX": "0",
            "RAMDISK_SWAP_MAX": "0", "USER_MIN": "2048M", "DOCKER_CAP_HEADROOM_PCT": "90",
            "DEFER_PCT": "90"}


def derive(tmp_path, **cells):
    """Run the cells block with GUARD_<NAME>_t cells; -> (rc, {var: value}, stderr)."""
    script = "\n".join([
        "die() { printf 'guard-init: %s\\n' \"$*\" >&2; exit 1; }",
        TO_MIB, HOSTVAR,
        "HOSTKEY=t RAM_M=16000 SWAP_M=4095 PEER_CLAUDE=''",
        f"GUARD_RAM_DIR_t={tmp_path / 'no-ram-disk'}",
        *[f"GUARD_{k}_t={_q(v)}" for k, v in cells.items()],
        BLOCK,
        "for _v in %s; do printf '%%s=%%s\\n' \"$_v\" \"${!_v}\"; done" % " ".join(OUT),
    ])
    r = subprocess.run(["bash", "-c", script], capture_output=True, text=True, timeout=30,
                       cwd=tmp_path, env={**os.environ, "LC_ALL": "en_US.UTF-8"})
    return r.returncode, dict(ln.split("=", 1) for ln in r.stdout.splitlines() if "=" in ln), r.stderr


def _q(v):
    return "'" + v.replace("'", "'\\''") + "'"


def test_unset_cells_derive_todays_numbers(tmp_path):
    rc, v, err = derive(tmp_path)
    assert rc == 0, err
    user_max = 16000 - max(768, 16000 * 12 // 100)
    agi_max = user_max * 70 // 100
    assert v["USER_MAX_M"] == str(user_max)
    assert v["USER_SWAP_M"] == str(min(4095 * 50 // 100, 2048))
    assert (v["AGI_MAX_M"], v["AGI_HIGH_M"]) == (str(agi_max), str(agi_max * 90 // 100))
    assert (v["ENGINE_MAX_M"], v["ENGINE_HIGH_M"]) == ("512", "384")
    assert (v["WORK_MAX_M"], v["WORK_HIGH_M"]) == (str(agi_max - 512), str((agi_max - 512) * 90 // 100))
    assert v["CLAUDE_LOW_M"] == str(min(user_max // 6, 1024))
    assert (v["SYSTEM_MIN_M"], v["SSH_MIN_M"], v["ENGINE_SWAP"], v["RAMDISK_SWAP"]) == ("128", "64", "0", "0")


def test_cells_at_todays_literals_derive_the_same_numbers(tmp_path):
    rc0, unset, err0 = derive(tmp_path)
    rc1, lit, err1 = derive(tmp_path, **LITERALS)
    assert (rc0, rc1) == (0, 0), (err0, err1)
    assert lit == unset


def test_a_cell_moves_its_number(tmp_path):
    rc, v, err = derive(tmp_path, AGI_MAX_PCT="60", ENGINE_MAX="3G", ENGINE_SWAP_MAX="1G", CLAUDE_LOW_DIV="20")
    assert rc == 0, err
    user_max = 16000 - 1920
    assert v["AGI_MAX_M"] == str(user_max * 60 // 100)
    assert v["WORK_MAX_M"] == str(user_max * 60 // 100 - 3072)
    assert v["ENGINE_SWAP"] == "1024M"
    assert v["CLAUDE_LOW_M"] == str(user_max // 20)


def test_an_empty_cell_takes_the_default(tmp_path):
    rc, v, err = derive(tmp_path, AGI_MAX_PCT="", SSH_MIN="")
    assert rc == 0, err
    assert (v["AGI_MAX_M"], v["SSH_MIN_M"]) == (str(14080 * 70 // 100), "64")


@pytest.mark.parametrize("name,value", [
    ("WORK_HIGH_PCT", "9x"),
    ("AGI_MAX_PCT", "RAM_M[$(touch pwned)]"),
    ("AGI_HIGH_PCT", "$(touch pwned)"),
    ("CLAUDE_LOW_DIV", "0"),
    ("SSH_MIN", "-64M"),
    ("ENGINE_MAX", "G"),
    ("USER_MIN", "-1M"),
    ("ENGINE_SWAP_MAX", "512m"),
    ("RAMDISK_SWAP_MAX", "1024\nX=1"),
    ("RESERVE", "RAM_M[$(touch pwned)]"),
    ("OOMD_LIMIT", "100"),
    ("SSH_MIN", "\u0663M"),          # an Arabic-Indic 3: [0-9] matches it under en_US.UTF-8
    ("AGI_MAX_PCT", "\uff11\uff12"),  # fullwidth 12
])
def test_a_bad_cell_is_refused_by_name_and_runs_nothing(tmp_path, name, value):
    rc, v, err = derive(tmp_path, **{name: value})
    assert rc != 0
    assert f"GUARD_{name}_t must be" in err, err
    assert not (tmp_path / "pwned").exists()
    assert not v


def test_no_unit_property_carries_a_memory_literal():
    """Falsifier 2: every memory property guard-init writes reads a variable."""
    props = r"(MemoryHigh|MemoryMax|MemorySwapMax|MemoryLow|MemoryMin|ManagedOOMMemoryPressureLimit" \
            r"|SwapUsedLimit|DefaultMemoryPressureLimit|DefaultMemoryPressureDurationSec)"
    hits = [ln for ln in SRC.splitlines() if re.match(props + r"=[0-9]", ln.strip())]
    assert hits == []


@pytest.mark.parametrize("cells,line", [
    ({"ENGINE_MAX": "100G"}, "agi-engine MemoryMax"),        # more than the box's RAM
    ({"ENGINE_MAX": "12000M"}, "agi-work MemoryMax"),        # agi max 9856 - engine max < 0
    ({"ENGINE_MAX": "0.5M"}, "agi-engine MemoryMax"),        # to_mib truncates to 0M
    ({"RESERVE": "20000M"}, "user@ MemoryMax"),               # nothing left for user@
    ({"CLAUDE_LOW_CAP": "0M"}, "Claude MemoryLow"),
])
def test_a_derived_line_out_of_range_is_refused_by_name(tmp_path, cells, line):
    """goal:g7.16.1.5.5.8: a well-formed cell that sizes a unit <= 0 or > RAM."""
    rc, v, err = derive(tmp_path, **cells)
    assert rc != 0 and not v
    assert err.startswith("guard-init: %s would be " % line), err
    assert "(RAM 16000M); check GUARD_" in err, err
