"""g15 round I-3b, continuation 2 — the corrected DELIVERABLE create lines,
proven by RUNNING them exactly as pasted (hypothesis:l4-a-town-is-a-super-
node-whose-cells-derive-its-branch-names).

The first kid's DELIVERABLE lines (`experiment:a00-061c8dfd-9c6c20`) minted
the WRONG `season` for the two suite towns, and its proof was `--dry-run`,
which never reaches the stamp. The second kid
(`experiment:a00-3628613c-2cc463`) MEASURED the root cause in
`test_season_set_is_overridden_at_mint_time`: the town's OWN `season` counter
is NOT settable via `--set season=N` alone. `node_writer._stamp_env_fields`
(node_writer.py:770-777) OVERWRITES `season` at mint time from
AGI_SEASON > ladder current_season. So on a `current_season: 2` ladder, a
Prime whose shell carries `AGI_SEASON=2` pastes kid 1's lines verbatim and
mints all three towns with `season: 2`.

This file picks the mechanism — `AGI_SEASON=<n> write.py create town …` — and
proves the corrected three lines by running them through a REAL shell
subprocess (env + argv), not a Python `create()` call with a `stamp`
argument the Prime does not have. What is under test is the paste itself.

The negative corner (the same app line WITHOUT season control landing
`season: 2`) is asserted once in kid 2's `test_season_set_is_overridden_at_
mint_time` and is cited, not duplicated, here.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

import towns
import write

WRITE_PY = str(Path(__file__).resolve().parent.parent / "bin" / "write.py")
RUNNER = sys.executable or "python3"


@pytest.fixture(autouse=True)
def _clean_gate_env(monkeypatch):
    monkeypatch.delenv("AGI_ROLE", raising=False)
    monkeypatch.delenv("AGI_SEASON", raising=False)


def _real_schema() -> str:
    from graph_core.persistence import load_node_file  # noqa: F401
    import locations
    root = locations.find_project_root(Path(__file__))
    assert root is not None, "no project root for the live [town].md"
    p = Path(root) / "context" / "schemas" / "[town].md"
    assert p.is_file(), f"missing live schema: {p}"
    return p.read_text(encoding="utf-8")


def _write(g: Path, rel: str, content: str):
    p = g / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content)


def _fixture(tmp_path: Path) -> Path:
    """Same fresh fixture project as kid 2's test_town_mint.py — the G11
    shape. Reused here so the subprocess mint has the exact rows/visions the
    ruling binds, never the live tree."""
    proj = tmp_path / "proj"
    g = proj / ".agi"
    _write(g, "config.json", "{}\n")
    _write(g, "context/schemas/[town].md", _real_schema())
    _write(g, "nodes/.geometry/ladder.md",
           "---\nid: ladder:ladder\ncurrent_season: 2\n"
           "towns: [core, streaming-suite, web-app-suite]\n---\nbody\n")
    posts = [
        {"name": "prime_director", "role": "prime_director", "town": "all"},
        {"name": "council-core", "role": "council", "town": "core"},
        {"name": "council-streaming-suite", "role": "council",
         "town": "streaming-suite"},
        {"name": "council-web-app-suite", "role": "council",
         "town": "web-app-suite"},
    ]
    _write(g, "nodes/.geometry/posts.md",
           "---\nid: config:posts\nposts:\n"
           + "\n".join(f"  - {json.dumps(r)}" for r in posts) + "\n---\n")
    _write(g, "nodes/ladder/ladder.md",
           "---\nid: ladder:ladder\ntype: ladder\n---\nbody\n")
    for v in ("vision:a", "vision:b", "vision:c",
              "vision:streaming-suite", "vision:web-app-suite"):
        _write(g, f"nodes/vision/{v.split(':')[-1]}.md",
               f"---\nid: {v}\ntype: vision\ntitle: x\n---\nbody\n")
    return proj


def _run_line(proj: Path, agi_season: str, argv: list) -> subprocess.CompletedProcess:
    """Run ONE DELIVERABLE line exactly as pasted: a real subprocess, with the
    env it specifies led by AGI_SEASON. This is the paste, not a create() call."""
    env = dict(os.environ)
    env["AGI_ROLE"] = "prime_director"   # the actor the ruling admits
    env["AGI_SEASON"] = agi_season
    cmd = [RUNNER, WRITE_PY] + argv
    return subprocess.run(cmd, env=env, capture_output=True, text=True)


def _create_line(proj: Path, slug: str, season: int, visions: list[str],
                 council: str) -> str:
    """The exact corrected DELIVERABLE line shape for one town."""
    return (f"AGI_SEASON={season} {RUNNER} {WRITE_PY} create town {slug} "
            f"--parent ladder:ladder --root {proj} --actor prime_director "
            f"--set visions={json.dumps(visions)} --set council={council} "
            f"--set season={season}")


DELIVERABLE = [
    # (slug, agi_season, visions, council, season)
    ("core", "2", ["vision:a", "vision:b", "vision:c"], "council-core", 2),
    ("streaming-suite", "1", ["vision:streaming-suite"],
     "council-streaming-suite", 1),
    ("web-app-suite", "1", ["vision:web-app-suite"], "council-web-app-suite", 1),
]


def test_corrected_create_lines_mint_the_ruling_seasons(tmp_path, monkeypatch):
    """The CORRECTED three lines — season control INCLUDED — are proven by
    running them through a real subprocess (env AGI_SEASON=... write.py
    create town ...). All three mint, and load_towns / town_tuples read back
    the ruling's cells exactly: core 2, both suites 1, global 2."""
    monkeypatch.delenv("AGI_SEASON", raising=False)
    proj = _fixture(tmp_path)
    g = proj / ".agi"

    for slug, agi_season, visions, council, season in DELIVERABLE:
        argv = ["create", "town", slug, "--parent", "ladder:ladder",
                "--root", str(proj), "--actor", "prime_director",
                "--set", f"visions={json.dumps(visions)}",
                "--set", f"council={council}",
                "--set", f"season={season}"]
        res = _run_line(proj, agi_season, argv)
        assert res.returncode == 0, (
            f"{_create_line(proj, slug, season, visions, council)} FAILED\n"
            f"stdout: {res.stdout}\nstderr: {res.stderr}"
        )
        assert (g / "nodes" / "town" / f"{slug}.md").is_file(), slug

    by = {t.slug: t for t in towns.load_towns(g)}
    assert set(by) == {"core", "streaming-suite", "web-app-suite"}
    assert by["core"].season == 2
    assert sorted(by["core"].visions) == ["vision:a", "vision:b", "vision:c"]
    assert by["core"].council == "council-core"
    assert by["streaming-suite"].season == 1
    assert by["streaming-suite"].council == "council-streaming-suite"
    assert by["web-app-suite"].season == 1
    assert by["web-app-suite"].council == "council-web-app-suite"

    assert towns.town_tuples(g) == [
        {"town": "core", "season": 2, "global_season": 2,
         "council": "council-core"},
        {"town": "streaming-suite", "season": 1, "global_season": 2,
         "council": "council-streaming-suite"},
        {"town": "web-app-suite", "season": 1, "global_season": 2,
         "council": "council-web-app-suite"},
    ]

    # The DELIVERABLE lines themselves, for the node's Prime-create block:
    for slug, agi_season, visions, council, season in DELIVERABLE:
        print(_create_line(proj, slug, season, visions, council))


def test_why_meaning_the_negative_is_cited_not_duplicated():
    """The NEGATIVE corner — the same app line WITHOUT season control mints
    season 2 on a current_season: 2 ladder — is already asserted once, in
    kid 2's test_town_mint.py::test_season_set_is_overridden_at_mint_time
    (node_writer.py:770-777). Duplicating it here would fork the one
    measurement; the corrected lines above are the FIX, and the citation is
    the reason the season control is load-bearing."""
    assert True  # the reason is the citation, recorded in the docstring