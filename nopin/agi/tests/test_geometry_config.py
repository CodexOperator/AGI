"""Focused tests for the config:seats -> config:posts resolver
(hypothesis:l4-a-seat-is-a-post-everywhere, kid 1 — reader half + flag half).

Proves, on fixture graphs only (never the live tree):
  * a `posts.md` graph resolves post-first with NO deprecated-alias notice;
  * a `seats.md`-only graph resolves via the SILENT fallback with NO
    file-deprecation notice (the notice was a lie on exactly the trees where
    it fired, hypothesis:l4-the-config-posts-note-is-silent-until-posts-md-
    exists);
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
# reader half: posts-first, seats fallback, file notice SILENT             #
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


def test_seats_only_fallback_resolves_silently(tmp_path):
    """Only seats.md exists: resolve() returns the seats rows and prints NO
    file-deprecation notice (hypothesis:l4-the-config-posts-note-is-silent-
    until-posts-md-exists). The notice named a migration target (posts.md)
    that is absent by construction on this branch, so it could only fire
    where its advice was untakeable — it is deleted outright. Resolve twice
    in one process to prove the rows themselves (not just a count) and the
    absence of the notice."""
    g = _graph(tmp_path)
    _write_seats(g)
    r = _resolver(g, (
        "import json\n"
        "print(gc.resolve(ROOT)[0].name)\n"
        "print(json.dumps(gc.load_rows(ROOT)))\n"
        "print(json.dumps(gc.load_rows(ROOT)))\n"
    ))
    assert r.returncode == 0, r.stderr
    lines = r.stdout.splitlines()
    assert lines[0] == "seats.md", lines
    rows = json.loads(lines[1])
    assert rows == SEATS_ROWS, rows     # byte-for-byte identity with today
    assert json.loads(lines[2]) == SEATS_ROWS, lines
    # the file-deprecation notice is SILENT on a seats-only tree
    assert "deprecated" not in r.stderr, r.stderr
    assert "note:" not in r.stderr, r.stderr


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

# --------------------------------------------------------------------------- #
# kid 1 (L4.306) READER-ROUTE fix: the three sites that still hardcoded the   #
# deprecated config:seats / `seats` must route through geometry_config.resolve#
# post-first, with a seats.md-only fallback (hypothesis:l4-a-seat-is-a-post-  #
# everywhere). A residual literal to seats.md/seats: would fail a posts-only  #
# fixture by reading empty/absent.                                            #
# --------------------------------------------------------------------------- #
def test_send_row_write_submit_routes_posts_md_first(tmp_path):
    """send._row_write_submit builds the node id and verb key from
    geometry_config.resolve: on a posts.md-only graph the write targets
    `config:posts` / `posts`, never a literal `config:seats`/`seats`."""
    g = _graph(tmp_path)
    _write_posts(g)
    r = _py(
        "import send\n"
        "import write as _w\n"
        "from pathlib import Path as _P\n"
        f"ROOT=_P({str(g)!r})\n"
        "cap = {}\n"
        "def fake_submit(graph, edit, actor='', role='', **kw):\n"
        "    cap['node'] = edit.node_id\n"
        "    cap['keys'] = list(edit.set_fm)\n"
        "_w.submit = fake_submit\n"
        "ok = send._row_write_submit(ROOT, [{'name':'a'},{'name':'b'}], "
        "actor='x', role='kid')\n"
        "print('ok', ok)\n"
        "print('node', cap.get('node'))\n"
        "print('keys', cap.get('keys'))\n"
    )
    assert r.returncode == 0, r.stderr
    lines = r.stdout.splitlines()
    assert lines[0] == "ok True", lines
    assert lines[1] == "node config:posts", lines
    assert lines[2] == "keys ['posts']", lines


def test_send_row_write_submit_falls_back_to_seats_md(tmp_path):
    """A seats.md-only graph: _row_write_submit still resolves via the alias to
    `config:seats` / `seats` (the one-season fallback must keep working)."""
    g = _graph(tmp_path)
    _write_seats(g)
    r = _py(
        "import send\n"
        "import write as _w\n"
        "from pathlib import Path as _P\n"
        f"ROOT=_P({str(g)!r})\n"
        "cap = {}\n"
        "def fake_submit(graph, edit, actor='', role='', **kw):\n"
        "    cap['node'] = edit.node_id\n"
        "    cap['keys'] = list(edit.set_fm)\n"
        "_w.submit = fake_submit\n"
        "ok = send._row_write_submit(ROOT, [{'name':'a'}], actor='x', role='kid')\n"
        "print('ok', ok)\n"
        "print('node', cap.get('node'))\n"
        "print('keys', cap.get('keys'))\n"
    )
    assert r.returncode == 0, r.stderr
    lines = r.stdout.splitlines()
    assert lines[0] == "ok True", lines
    assert lines[1] == "node config:seats", lines
    assert lines[2] == "keys ['seats']", lines


def test_sensei_load_seats_reads_posts_md(tmp_path):
    """sensei.load_seats resolves posts.md when it is the only geometry config:
    the ~7 callers get the two rows, not the [] a hardcoded config:seats
    lookup would return once posts.md exists."""
    g = _graph(tmp_path)
    _write_posts(g)
    r = _py(
        "import sensei\n"
        "from pathlib import Path as _P\n"
        f"ROOT=_P({str(g)!r})\n"
        "print(len(sensei.load_seats(ROOT)))\n"
        "print(sensei.load_seats(ROOT)[0].get('name'))\n"
    )
    assert r.returncode == 0, r.stderr
    lines = r.stdout.splitlines()
    assert lines[0] == "2", lines
    assert lines[1] == "seatA", lines


def test_sensei_load_seats_falls_back_to_seats_md(tmp_path):
    """A seats.md-only graph: load_seats still returns the rows via the alias."""
    g = _graph(tmp_path)
    _write_seats(g)
    r = _py(
        "import sensei\n"
        "from pathlib import Path as _P\n"
        f"ROOT=_P({str(g)!r})\n"
        "print(len(sensei.load_seats(ROOT)))\n"
    )
    assert r.returncode == 0, r.stderr
    assert r.stdout.strip() == "2", r.stdout


def test_viewport_anchor_index_reads_posts_md(tmp_path):
    """viewport._anchor_index builds the AnchorIndex from posts.md when that is
    the only geometry config file (two rows -> two unanchored anchors), not the
    empty list a literal config:seats lookup would report once posts.md exists."""
    g = _graph(tmp_path)
    _write_posts(g)
    r = _py(
        "import viewport\n"
        "from pathlib import Path as _P\n"
        f"ROOT=_P({str(g)!r})\n"
        "idx = viewport._anchor_index(ROOT, {})\n"
        "print(len(idx.anchored) + len(idx.unanchored))\n"
        "print(len(idx.unanchored))\n"
    )
    assert r.returncode == 0, r.stderr
    lines = r.stdout.splitlines()
    assert lines[0] == "2", lines
    assert lines[1] == "2", lines


def test_viewport_anchor_index_falls_back_to_seats_md(tmp_path):
    """A seats.md-only graph: _anchor_index still reads the rows via the alias."""
    g = _graph(tmp_path)
    _write_seats(g)
    r = _py(
        "import viewport\n"
        "from pathlib import Path as _P\n"
        f"ROOT=_P({str(g)!r})\n"
        "idx = viewport._anchor_index(ROOT, {})\n"
        "print(len(idx.anchored) + len(idx.unanchored))\n"
    )
    assert r.returncode == 0, r.stderr
    assert r.stdout.strip() == "2", r.stdout


# --------------------------------------------------------------------------- #
# GUARD (kid SL7.67, Gap 2): no reader RE-emits the file-deprecation notice  #
# on the seats-only fallback (hypothesis:l4-the-config-posts-note-is-silent- #
# until-posts-md-exists). See the test's docstring for the counterfactual it #
# avoids.                                                                    #
# --------------------------------------------------------------------------- #
def test_no_reader_reemits_file_notice_on_seats_tree(tmp_path):
    """GUARD — an integration assertion across the reader modules that open
    the geometry config. On a seeds-only tree every reader reaches the
    resolver through the SILENT seats fallback (the file-deprecation notice
    was deleted, not silenced: hypothesis:l4-the-config-posts-note-is-silent-
    until-posts-md-exists).

    Chosen over the resolver-only alternative because of the counterfactual:
    a test that only calls `geometry_config.resolve()` directly proves the
    RESOLVER is silent but would still pass if a reader module re-added its
    OWN file-deprecation print — the notice could return through any of the
    ten readers and that guard would not see it. This guard instead drives
    EACH reader's own entry point twice on a seeds-only tree and asserts
    (1) it returns the two seats rows (so a module that never reads the
    geometry config cannot pass trivially: it would report [],absent and
    fail), and (2) the whole subprocess emits NO `note:`/`deprecated`
    file-notice on stderr. A `note: ... is deprecated` file-notice print put
    back on ANY reader's seats path lands on stderr and fails here; a hook-level run
    (option a) is separately covered by test_hook_alias_notice.py's notice-
    family test.
    """
    g = _graph(tmp_path)
    _write_seats(g)
    r = _py(
        "import hierarchy, sensei, seat_status, viewport\n"
        "from pathlib import Path as _P\n"
        f"ROOT=_P({str(g)!r})\n"
        # every reader that opens the geometry config, run TWICE on a
        # seeds-only tree: rows must come back (reaches the fallback) and
        # nothing may reach stderr.
        "print('h1', [x.get('name') for x in hierarchy.load_seats(ROOT)])\n"
        "print('h2', len(hierarchy.load_seats(ROOT)))\n"
        "print('se1', [x.get('name') for x in sensei.load_seats(ROOT)])\n"
        "print('se2', len(sensei.load_seats(ROOT)))\n"
        "_, p = seat_status._load_registry_rows(ROOT); print('ss1', p)\n"
        "_, p2 = seat_status._load_registry_rows(ROOT); print('ss2', p2)\n"
        "v1, pv = viewport.load_seat_rows(ROOT, {}); print('vp', pv, len(v1))\n"
        "v2, pv2 = viewport.load_seat_rows(ROOT, {}); print('vp2', pv2, len(v2))\n"
        "a1 = viewport._anchor_index(ROOT, {})\n"
        "a2 = viewport._anchor_index(ROOT, {})\n"
        "print('an1', len(a1.anchored) + len(a1.unanchored))\n"
        "print('an2', len(a2.anchored) + len(a2.unanchored))\n"
    )
    assert r.returncode == 0, r.stderr
    lines = r.stdout.splitlines()
    expected = [
        "h1 ['seatA', 'seatB']", "h2 2",
        "se1 ['seatA', 'seatB']", "se2 2",
        "ss1 True", "ss2 True",
        "vp True 2", "vp2 True 2",
        "an1 2", "an2 2",
    ]
    assert lines == expected, lines
    # the file-deprecation notice is SILENT through every reader on a
    # seeds-only tree
    assert "note:" not in r.stderr, r.stderr
    assert "deprecated" not in r.stderr, r.stderr
