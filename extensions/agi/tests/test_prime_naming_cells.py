"""SM.118 build tests (hypothesis:l4-the-prime-successor-name-derives-from-
the-live-ladder-cells-in-every-spelling-belam-s3-l1-i-after-the-rollover).

Parametrized on the ladder cells (2,5) and (3,1): the ONE resolver
`rotate.prime_window_name` derives `belam-S<season>-L<loop>-<numeral>`, and
for a `prime_director` row `_session_label` is None at BOTH settings, so the
window name and the `--remote-control` name are the same derived string
(`spawn_window`'s `rc_name=None` path). `session_name` (the harness join-
resolved ref, goal:g15.25) is a SEPARATE identity axis and is asserted
independent of the cells -- it must never be folded into the belam- pattern.

The three "the literal is gone" falsifiers: 0 `belam-S1` tokens in the
`bin/*.py` CODE (docstrings/comments stripped by tokenize), and 0 in the
RENDERED prime brief (head + brief_file, via `brief.successor_prompt`).
"""
import io
import re
import sys
import tokenize
from pathlib import Path
from types import SimpleNamespace

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from agi.bin import rotate

REPO = Path(__file__).resolve().parents[3]
CELLS = [(2, 5), (3, 1)]


def _ladder(root, season, loop):
    g = root / "nodes" / ".geometry"
    g.mkdir(parents=True, exist_ok=True)
    (g / "ladder.md").write_text(
        "---\nid: ladder:ladder\ntype: ladder\n"
        f"current_season: {season}\ncurrent_loop: {loop}\n---\n\nbody\n",
        encoding="utf-8")


@pytest.mark.parametrize("season,loop", CELLS)
def test_prime_window_name_derives_from_the_cells(tmp_path, season, loop):
    """A predecessor from an OLDER token restarts at I under the live cells."""
    _ladder(tmp_path, season, loop)
    assert rotate.prime_window_name(
        tmp_path, "belam-S1-L4-XXXI") == f"belam-S{season}-L{loop}-I"


@pytest.mark.parametrize("season,loop", CELLS)
def test_prime_window_name_continues_inside_the_same_token(tmp_path, season,
                                                           loop):
    """A predecessor carrying the SAME token continues its numeral."""
    _ladder(tmp_path, season, loop)
    assert rotate.prime_window_name(
        tmp_path, f"belam-S{season}-L{loop}-III"
    ) == f"belam-S{season}-L{loop}-IV"


@pytest.mark.parametrize("season,loop", CELLS)
def test_prime_row_label_is_none_at_every_cell(season, loop):
    """A prime_director row carries NO GUI label, so `rc_name` is None at
    both cell settings and the RC name falls back to the window name."""
    assert rotate._session_label(
        {"name": "belam", "role": "prime_director"}, 31) is None
    # a non-prime row's label comes from its own name -- never a cell token
    assert rotate._session_label(
        {"name": "director-belam", "role": "director"}, 2) == "director-belam"


def _prime_fixture(tmp_path, monkeypatch, season, loop):
    root = tmp_path
    _ladder(root, season, loop)
    g = root / "nodes" / ".geometry"
    (g / "seats.md").write_text(
        "---\nid: config:seats\ntype: config\nseats:\n"
        '  - {"name": "belam", "role": "prime_director", "model": "x", '
        '"effort": "max", "settings": "", "session_name": "agi-0c"}\n---\n',
        encoding="utf-8")
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
    return root, win


@pytest.mark.parametrize("season,loop", CELLS)
def test_one_resolver_feeds_window_and_remote_control(tmp_path, monkeypatch,
                                                      season, loop):
    """END TO END: rotate-self spawns the successor under the derived window
    name AND with `rc_name=None` (the prime row has no label), so the
    `--remote-control` name is the SAME derived string -- one resolver."""
    root, win = _prime_fixture(tmp_path, monkeypatch, season, loop)
    seen = {}

    def fake_spawn(**kw):
        seen.update(kw)
        return 0, "echo hi"

    monkeypatch.setattr(rotate, "spawn_window", fake_spawn)
    args = SimpleNamespace(
        name="belam", force=True, timeout=5, debug_file=None, model=None,
        effort=None, settings=None, prompt_file=None, tmux_session="t",
        window_path=str(win), dry_run=True, throwaway=False,
        successor_argv=None, role="prime_director")
    assert rotate.cmd_rotate_self(args, root) == 0
    assert seen["name"] == f"belam-S{season}-L{loop}-I"
    assert seen["rc_name"] is None  # prime label None -> RC name is `name`


@pytest.mark.parametrize("season,loop", CELLS)
def test_session_name_cell_is_independent_of_the_cells(tmp_path, monkeypatch,
                                                       season, loop):
    """The harness join-resolved `session_name` (`agi-0c`) is a SEPARATE
    identity axis: the successor's chain name derives from the cells and the
    row's `session_name` is neither read nor rewritten by the rotation."""
    root, win = _prime_fixture(tmp_path, monkeypatch, season, loop)
    seen = {}
    monkeypatch.setattr(
        rotate, "spawn_window",
        lambda **kw: (seen.update(kw), (0, "echo hi"))[1])
    args = SimpleNamespace(
        name="belam", force=True, timeout=5, debug_file=None, model=None,
        effort=None, settings=None, prompt_file=None, tmux_session="t",
        window_path=str(win), dry_run=True, throwaway=False,
        successor_argv=None, role="prime_director")
    assert rotate.cmd_rotate_self(args, root) == 0
    assert seen["name"] == f"belam-S{season}-L{loop}-I"
    sheet = (root / "nodes" / ".geometry" / "seats.md").read_text()
    assert '"session_name": "agi-0c"' in sheet  # untouched, never folded in


def _code_tokens(path):
    """Every token of `path` EXCEPT comments and string literals (docstrings
    included), so a `belam-S1` in prose is not read as a code path."""
    src = path.read_text(encoding="utf-8")
    keep = []
    for tok in tokenize.generate_tokens(io.StringIO(src).readline):
        if tok.type in (tokenize.COMMENT, tokenize.STRING,
                        getattr(tokenize, "FSTRING_MIDDLE", -1)):
            continue
        keep.append(tok.string)
    return "".join(keep)


def test_no_belam_s1_in_bin_code_paths():
    """conjunct (2): the literal is gone from every `bin/*.py` CODE path;
    the remaining hits are all docstrings/comments (historical prose)."""
    hits = []
    for py in sorted((REPO / "extensions" / "agi" / "bin").glob("*.py")):
        if "belam-S1" in _code_tokens(py):
            hits.append(py.name)
    assert hits == []


def test_rendered_prime_brief_has_no_literal():
    """conjunct (2): the Prime's actual rendered prompt (constitution head +
    the rotations-declared brief_file) carries the pattern, never belam-S1."""
    import brief
    g = REPO / ".agi" / "nodes" / ".geometry"
    rotations = (g / "rotations.md").read_text(encoding="utf-8")
    m = re.search(r"^\s*prime_director:\s*\n\s*brief_file:\s*(\S+)",
                  rotations, re.M)
    assert m, "config:rotations must declare the prime_director brief_file"
    bfile = REPO / m.group(1).strip()
    assert bfile.exists(), bfile
    rendered = brief.successor_prompt(
        tier="prime_director", body=bfile.read_text(encoding="utf-8"),
        project_root=REPO / ".agi")
    assert "belam-S1" not in rendered
    assert "belam-S<season>-L<loop>" in rendered
