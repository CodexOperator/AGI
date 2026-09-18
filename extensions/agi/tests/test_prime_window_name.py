"""SM.107 build tests (hypothesis:l4-the-prime-successor-window-name-derives-
from-the-season-and-loop-cells-...): the Prime successor window name derives
the `S<season>` / `L<loop>` token from the LIVE ladder cells, restarts its
numeral at I on a token change and continues it when the token matches; the
after_join belam-chain grep matches the PATTERN, never the literal belam-S1;
and the five-window chain reaps by seniority (token, then numeral) ACROSS
prefixes, so a token change never reaps the newest window.
"""
import re
import sys
from pathlib import Path
from types import SimpleNamespace

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from agi.bin import rotate

_CHAIN_RE = re.compile(r"belam-S[0-9]+-L[0-9]+")


def _ladder(root, season=None, loop=None):
    g = root / "nodes" / ".geometry"
    g.mkdir(parents=True, exist_ok=True)
    fm = ["---", "id: ladder:ladder", "type: ladder"]
    if season is not None:
        fm.append(f"current_season: {season}")
    if loop is not None:
        fm.append(f"current_loop: {loop}")
    fm += ["---", "", "body", ""]
    (g / "ladder.md").write_text("\n".join(fm), encoding="utf-8")


def test_prime_window_name_restarts_on_token_change(tmp_path):
    """season 2 / loop 5 + predecessor belam-S1-L4-XXXI -> belam-S2-L5-I."""
    _ladder(tmp_path, season=2, loop=5)
    assert rotate.prime_window_name(
        tmp_path, "belam-S1-L4-XXXI") == "belam-S2-L5-I"


def test_prime_window_name_continues_same_token(tmp_path):
    """season 2 / loop 5 + predecessor belam-S2-L5-III -> belam-S2-L5-IV."""
    _ladder(tmp_path, season=2, loop=5)
    assert rotate.prime_window_name(
        tmp_path, "belam-S2-L5-III") == "belam-S2-L5-IV"
    assert rotate.prime_window_name(
        tmp_path, "belam-S2-L5") == "belam-S2-L5-II"   # bare base is line 1


def test_prime_window_name_keeps_token_without_cells(tmp_path):
    """A fixture root with no loop cell keeps the predecessor's own token, so
    a pre-cell root stays byte-identical (S1-L4 -> VI)."""
    _ladder(tmp_path, season=2)          # season only, NO current_loop
    assert rotate.prime_window_name(
        tmp_path, "belam-S1-L4-V") == "belam-S1-L4-VI"


def test_belam_chain_grep_matches_the_pattern():
    """The LIVE config:rotations after_join belam-chain entry greps the
    S/L pattern and matches both an old-prefix and a new-prefix window; no
    literal `grep belam-S1` survives (the falsifier)."""
    repo = Path(__file__).resolve().parents[3]
    text = (repo / ".agi" / "nodes" / ".geometry" / "rotations.md").read_text(
        encoding="utf-8")
    assert "grep belam-S1" not in text
    assert "belam-S[0-9]+-L[0-9]+" in text
    assert _CHAIN_RE.search("belam-S1-L4-XXXI")
    assert _CHAIN_RE.search("belam-S2-L5-I")


def test_belam_oldest_reaps_across_prefixes_by_seniority(tmp_path):
    """Six candidates across a token change: the OLDEST prefix is reaped,
    never the newest window belam-S2-L5-II (which a numeral-only sort picks)."""
    live = ["belam-S1-L4-XXIX", "belam-S1-L4-XXX", "belam-S1-L4-XXXI",
            "belam-S2-L5-I", "belam-S2-L5-II"]
    assert rotate._belam_oldest(
        live, "belam-S2-L5-III", "belam") == "belam-S1-L4-XXIX"


def test_rotate_self_step3_names_from_season_and_loop_cells(
        tmp_path, monkeypatch):
    """END TO END: rotate-self step 3, with the live cells at season 2 /
    loop 5 and a predecessor belam-S1-L4-VI, spawns belam-S2-L5-I -- never
    the copied predecessor prefix (the falsifier)."""
    root = tmp_path
    _ladder(root, season=2, loop=5)
    g = root / "nodes" / ".geometry"
    (g / "seats.md").write_text(
        "---\nid: config:seats\ntype: config\nseats:\n"
        '  - {"name": "belam", "role": "prime_director", "model": "x", '
        '"effort": "max", "settings": ""}\n---\n', encoding="utf-8")
    (g / "rotations.md").write_text(
        "---\nid: config:rotations\ntype: config\ntemplates:\n"
        "  prime_director: {brief_file: "
        "extensions/agi/briefs/prime-director-successor.md, "
        "steps: [handoff, spawn], telemetry: [seat]}\n---\n\nbody\n",
        encoding="utf-8")
    (root / "sessions").mkdir(parents=True, exist_ok=True)
    win = root / "windows.txt"
    win.write_text("@8 belam-S1-L4-V\n@9 belam-S1-L4-VI\n", encoding="utf-8")
    monkeypatch.setattr(rotate, "find_project_root", lambda: root)
    seen = {}

    def fake_spawn(**kw):
        seen["name"] = kw["name"]
        return 0, "echo hi"

    monkeypatch.setattr(rotate, "spawn_window", fake_spawn)
    args = SimpleNamespace(
        name="belam", force=True, timeout=5, debug_file=None, model=None,
        effort=None, settings=None, prompt_file=None, tmux_session="t",
        window_path=str(win), dry_run=True, throwaway=False,
        successor_argv=None, role="prime_director")
    rc = rotate.cmd_rotate_self(args, root)
    assert rc == 0
    assert seen["name"] == "belam-S2-L5-I"
