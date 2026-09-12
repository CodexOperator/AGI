"""Focused tests for the config:seats -> config:posts resolver
(hypothesis:l4-a-seat-is-a-post-everywhere, kid 1 — reader half + flag half).

Proves, on fixture graphs only (never the live tree):
  * a `posts.md` graph resolves post-first with NO deprecated-alias notice;
  * a `seats.md`-only graph resolves via fallback and prints the alias notice
    AT MOST ONCE per process;
  * `--seat <name>` still works on a CLI and `--post <name>` is accepted on
    the SAME CLI (argparse dest unchanged -> no call site breaks);
  * `AGI_POST` wins over `AGI_SEAT` when both are set.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parents[1] / "bin"

SEATS_ROWS = [
    {"name": "seatA", "role": "kid", "tier": 0, "harness": "pi",
     "model": "~deepseek/deepseek-v4-flash-latest"},
    {"name": "seatB", "role": "kid", "tier": 0, "harness": "pi",
     "model": "~deepseek/deepseek-v4-flash-latest"},
]
LADDER = """---
current_season: 2
roles:
  - {"tier": 3, "role": "parent", "harness": "claude-code", "model": "claude-opus-5", "effort": "max", "settings": "ultracode"}
  - {"tier": 1, "role": "parent", "harness": "pi", "model": "~z-ai/glm-flash-latest", "effort": "", "settings": ""}
  - {"tier": 0, "role": "kid", "harness": "pi", "model": "~deepseek/deepseek-v4-flash-latest", "effort": "", "settings": ""}
---

body
"""
CONFIG = {
    "harnesses": {
        "pi": {
            "adapter": "pi", "provider": "openrouter",
            "models": {"kid": "deepseek-v4", "parent": "glm-flash"},
            "allowed_models": ["~deepseek/deepseek-v4-flash-latest",
                               "~z-ai/glm-flash-latest"],
        },
    },
    "spawn": {"harness": "pi", "parallel": 1, "max_live": 25},
}


def _rows_fm(key: str) -> str:
    return "".join(f"  - {json.dumps(r, sort_keys=True)}\n" for r in SEATS_ROWS)


def _graph(root: Path) -> Path:
    g = root / ".agi"
    (g / "nodes" / ".geometry").mkdir(parents=True, exist_ok=True)
    return g


def _write_posts(g: Path):
    (g / "nodes" / ".geometry" / "posts.md").write_text(
        "---\nid: config:posts\nposts:\n" + _rows_fm("posts") + "---\n")


def _write_seats(g: Path):
    (g / "nodes" / ".geometry" / "seats.md").write_text(
        "---\nid: config:seats\nseats:\n" + _rows_fm("seats") + "---\n")


def _py(args: str) -> subprocess.CompletedProcess:
    """Run a snippet with bin/ and src/ on sys.path, in a FRESH process (so the
    once-per-process deprecation flag starts clean)."""
    code = (
        "import sys; sys.path.insert(0, "
        f"{str(BIN)!r}); sys.path.insert(0, "
        f"{str(BIN.parent / 'src')!r});\n" + args
    )
    return subprocess.run([sys.executable, "-c", code],
                          capture_output=True, text=True)


def _resolver(root: Path, args: str) -> subprocess.CompletedProcess:
    return _py(f"import geometry_config as gc\nROOT={str(root)!r}\n{args}")


# --------------------------------------------------------------------------- #
# reader half: posts-first, seats fallback, notice ONCE per process            #
# --------------------------------------------------------------------------- #
def test_posts_md_resolves_post_first_no_notice(tmp_path):
    g = _graph(tmp_path)
    _write_posts(g)
    r = _resolver(g, "import json; print(gc.resolve(ROOT)[0].name); print(json.dumps(gc.load_rows(ROOT)))")
    assert r.returncode == 0, r.stderr
    assert r.stdout.splitlines()[0] == "posts.md"
    rows = json.loads(r.stdout.splitlines()[1])
    assert len(rows) == 2 and rows[0].get("name") == "seatA"
    assert "deprecated" not in r.stderr, r.stderr


def test_posts_wins_over_seats_when_both_files(tmp_path):
    g = _graph(tmp_path)
    _write_posts(g)
    _write_seats(g)
    r = _resolver(g, "print(gc.resolve(ROOT)[0].name)")
    assert r.returncode == 0, r.stderr
    assert r.stdout.strip() == "posts.md"
    assert "deprecated" not in r.stderr, r.stderr


def test_seats_only_fallback_resolves_and_notices_exactly_once(tmp_path):
    """Only seats.md exists: resolve twice in one process and the alias notice
    must print exactly ONCE (the once-per-process flag), with rows read."""
    g = _graph(tmp_path)
    _write_seats(g)
    r = _resolver(g, (
        "print(gc.resolve(ROOT)[0].name)\n"
        "print(len(gc.load_rows(ROOT)))\n"
    ))
    assert r.returncode == 0, r.stderr
    assert r.stdout.splitlines()[0] == "seats.md"
    assert r.stdout.splitlines()[1] == "2"
    assert r.stderr.count("deprecated") == 1, r.stderr


def test_missing_geometry_config_returns_empty(tmp_path):
    g = _graph(tmp_path)
    r = _resolver(g, "print(gc.load_rows(ROOT))")
    assert r.returncode == 0, r.stderr
    assert r.stdout.strip() == "[]"
    assert "deprecated" not in r.stderr, r.stderr


# --------------------------------------------------------------------------- #
# flag half: --seat still works, --post accepted, AGI_POST wins               #
# --------------------------------------------------------------------------- #
def test_seat_and_post_accepted_on_same_cli(tmp_path):
    """dispatch.py's --seat parser accepts BOTH `--seat` and `--post` (dest
    unchanged), a --dry-run under either spelling exits 0 and is NOT refused
    as an unrecognized argument."""
    graph = tmp_path / "_cli"
    g = graph / ".agi"
    (g / "nodes" / ".geometry").mkdir(parents=True)
    (g / "config.json").write_text(json.dumps(CONFIG))
    (g / "nodes" / ".geometry" / "ladder.md").write_text(LADDER)
    env = dict(os.environ)
    env.pop("AGI_TIER", None)
    for flag in ("--seat", "--post"):
        r = subprocess.run(
            [sys.executable, str(BIN / "dispatch.py"), str(graph), "1",
             flag, "seatA", "--harness", "pi", "--tier", "kid",
             "--target", "hypothesis:x", "--dry-run"],
            capture_output=True, text=True, env=env)
        assert r.returncode == 0, f"{flag}: {r.stderr}"
        assert "unrecognized arguments" not in r.stderr, f"{flag}: {r.stderr}"


def test_agi_post_wins_over_agi_seat(tmp_path):
    """Both env vars set: AGI_POST wins; the deprecated AGI_SEAT value is not
    returned. Runs in a fresh process so the env deprecation flag is clean."""
    g = _graph(tmp_path)
    code = (
        "import geometry_config as gc\n"
        "import os\n"
        "os.environ['AGI_SEAT']='legacy-seat'\n"
        "os.environ['AGI_POST']='new-post'\n"
        "print(gc.resolved_seat_env())\n"
        "print(gc.resolved_seat_env())\n"
    )
    r = _py(code)
    assert r.returncode == 0, r.stderr
    assert r.stdout.splitlines() == ["new-post", "new-post"]
    # the deprecated AGI_SEAT spelling must not trigger a notice when AGI_POST wins
    assert "AGI_SEAT" not in r.stderr, r.stderr


def test_agi_seat_only_is_legacy_fallback(tmp_path):
    """Only AGI_SEAT set: the legacy value still resolves (deprecated, one
    notice), so existing env never breaks."""
    code = (
        "import geometry_config as gc\n"
        "import os\n"
        "os.environ['AGI_SEAT']='legacy-seat'\n"
        "os.environ.pop('AGI_POST', None)\n"
        "print(gc.resolved_seat_env())\n"
        "print(gc.resolved_seat_env())\n"
    )
    r = _py(code)
    assert r.returncode == 0, r.stderr
    assert r.stdout.splitlines() == ["legacy-seat", "legacy-seat"]
    assert r.stderr.count("AGI_SEAT is deprecated") == 1, r.stderr


# --------------------------------------------------------------------------- #
# kid 2 part A: the FOUR residual readers must route through posts.md, never  #
# a literal seats.md (hypothesis:l4-a-seat-is-a-post-everywhere). Each test   #
# builds ONLY posts.md (no seats.md) and asserts the reader still sees the    #
# posts rows — a reader that stat/reads a literal seats.md would report       #
# absent/empty and FAIL.                                                      #
# --------------------------------------------------------------------------- #
def test_seat_status_presence_and_zoom_read_posts_md(tmp_path):
    """seat_status._load_registry_rows' PRESENCE flag and its zoom fallback
    both resolve posts.md when it is the only geometry config file (no
    seats.md on disk). A residual seats.md literal would report present=False
    and zero rows."""
    g = _graph(tmp_path)
    _write_posts(g)
    r = _py(
        "import seat_status\n"
        "from pathlib import Path as _P\n"
        f"ROOT=_P({str(g)!r})\n"
        "rows, present = seat_status._load_registry_rows(ROOT)\n"
        "print('present', present)\n"
        "print('rows', len(rows))\n"
        "print('zoom', len(seat_status._rows_via_zoom(ROOT)))\n"
    )
    assert r.returncode == 0, r.stderr
    lines = r.stdout.splitlines()
    assert lines[0] == "present True", lines
    assert lines[1] == "rows 2", lines
    assert lines[2] == "zoom 2", lines
    assert "deprecated" not in r.stderr, r.stderr


def test_viewport_load_seat_rows_reads_posts_md(tmp_path):
    """viewport.load_seat_rows reports registry_present=True and two rows from
    posts.md when no seats.md exists. (telemetry first via seat_status.collect
    for this module is allowed to fail open; the posts.md lane is the one under
    test.)"""
    g = _graph(tmp_path)
    _write_posts(g)
    r = _py(
        "import viewport\n"
        "from pathlib import Path as _P\n"
        f"ROOT=_P({str(g)!r})\n"
        "rows, present = viewport.load_seat_rows(ROOT, {})\n"
        "print('present', present)\n"
        "print('rows', len(rows))\n"
    )
    assert r.returncode == 0, r.stderr
    lines = r.stdout.splitlines()
    assert lines[0] == "present True", lines
    assert lines[1] == "rows 2", lines


def test_rotate_ack_seats_path_falls_back_to_posts_md(tmp_path):
    """rotate._ack_seats_path: with a posts.md graph it returns the posts.md
    path; with NO geometry config at all its FALLBACK must spell posts.md, not
    the deprecated seats.md (the kid-2 fix changed the fallback spelling)."""
    g = _graph(tmp_path)
    _write_posts(g)
    r = _py(
        "import rotate\n"
        "from pathlib import Path as _P\n"
        f"G=_P({str(g)!r})\n"
        f"BARE=_P({str(tmp_path)!r})\n"
        "print('post', rotate._ack_seats_path(G).name)\n"
        "print('fallback', rotate._ack_seats_path(BARE).name)\n"
    )
    assert r.returncode == 0, r.stderr
    lines = r.stdout.splitlines()
    assert lines[0] == "post posts.md", lines
    assert lines[1] == "fallback posts.md", lines


def test_send_shared_seats_path_falls_back_to_posts_md(tmp_path):
    """send._shared_seats_path: a posts.md graph resolves the posts.md path;
    with no git/geometry config its FALLBACK spells posts.md, never seats.md.
    Both loops fail if the fallback still names the deprecated seats.md."""
    g = _graph(tmp_path)
    _write_posts(g)
    r = _py(
        "import send\n"
        "from pathlib import Path as _P\n"
        f"G=_P({str(g)!r})\n"
        f"BARE=_P({str(tmp_path)!r})\n"
        "print('post', send._shared_seats_path(G).name)\n"
        "print('fallback', send._shared_seats_path(BARE).name)\n"
    )
    assert r.returncode == 0, r.stderr
    lines = r.stdout.splitlines()
    assert lines[0] == "post posts.md", lines
    assert lines[1] == "fallback posts.md", lines