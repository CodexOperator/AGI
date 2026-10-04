"""goal:g7.16.1.11.5 — bootstrap config:engine size bars + Q.2 piece presence.

Falsifier 1: whole engine.md <= 8192 B and engine-post + engine-wrap exist.
F21 (doc:radically-simple-engine §Q): fenced code <= 8192 B and whole <= 12288 B.
Q.2: every named v4c piece still has a ### heading in some engine*.md.
"""
from __future__ import annotations

import re
from pathlib import Path

GEO = Path(__file__).resolve().parents[3] / ".agi" / "nodes" / ".geometry"
ENGINE = GEO / "engine.md"
POST = GEO / "engine-post.md"
WRAP = GEO / "engine-wrap.md"
GROW = GEO / "engine-grow.md"
ROOT = GEO / "engine-root.md"

# Q.2 table live names (signers -> agi-signers already, before this cut).
Q2_HEADINGS = (
    "agi-post@.service", "agi-run", "settings.json", "cccc.ts", "agi-kid",
    "agi-brief", "brief.py", "agi-meter", "agi-turn", "agi-link", "agi-wt",
    "agi-track", "agi-flush", "gitconfig", "agi-signers", "sysusers.conf",
    "agi.rules", "project.sh", "observe.sh", "tick.sh", "agi-project",
    "agi-frontier", "agi-gate", "sect",
)

ZYGOTE_SCRIPTS = ("agi-project", "agi-gate", "sect", "matrix")


def _headings(path: Path) -> set[str]:
    return set(re.findall(r"^### ([^ ]+)", path.read_text(), re.M))


def _fenced_bytes(text: str) -> int:
    n = 0
    inside = False
    for line in text.splitlines(True):
        if line.startswith("~~~"):
            inside = not inside
            continue
        if inside:
            n += len(line.encode())
    return n


def _map_names(text: str) -> list[str]:
    i = text.index("## pieces —")
    j = text.index("\n## ", i + 3)
    inner = text[i:j].split("~~~\n", 1)[1].rsplit("\n~~~", 1)[0]
    return [ln.split()[0] for ln in inner.splitlines() if ln.strip()]


def test_falsifier_1_whole_engine_le_8192_and_expansions_exist():
    assert ENGINE.is_file() and POST.is_file() and WRAP.is_file()
    assert ENGINE.stat().st_size <= 8192, ENGINE.stat().st_size


def test_f21_fenced_code_le_8192_and_whole_le_12288():
    text = ENGINE.read_text()
    assert _fenced_bytes(text) <= 8192
    assert len(text.encode()) <= 12288


def test_q2_v4c_piece_headings_none_gone():
    names: set[str] = set()
    for path in (ENGINE, POST, WRAP, GROW, ROOT):
        assert path.is_file(), path
        names |= _headings(path)
    missing = [n for n in Q2_HEADINGS if n not in names]
    assert missing == [], missing


def test_zygote_script_headings_still_in_engine_md():
    have = _headings(ENGINE)
    assert set(ZYGOTE_SCRIPTS) <= have


def test_map_still_names_38_pieces_and_grow_gate_bytes_parse():
    text = ENGINE.read_text()
    names = _map_names(text)
    assert len(names) == 38
    assert names[0] == "agi-post@.service"
    assert "grow-gate" in names
    m = re.search(r"^grow-gate *([0-9]*) B", text, re.M)
    assert m and int(m.group(1)) == 6335
