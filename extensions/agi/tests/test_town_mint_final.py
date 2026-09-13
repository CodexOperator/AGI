"""g15 round I-3b, continuation 3 — THE FINAL DELIVERABLE create lines,
proven by running THE EXACT STRINGS from the node block itself
(hypothesis:l4-a-town-is-a-super-node-whose-cells-derive-its-branch-names).

Two prior kids shipped DELIVERABLE blocks, and both were wrong in exactly the
way their own proof could not see:

  * experiment:a00-061c8dfd-9c6c20 (kid 1) — the RIGHT vision ids but NO
    `AGI_SEASON` control, and a `--dry-run` proof that never reaches the
    stamp.
  * experiment:a00-91c6c811-ffa1f7 (kid 3) — the `AGI_SEASON` control but
    CORELINE placeholder vision ids `vision:a/b/c`, and a fixture built with
    those same placeholders, so the test and the deliverable agreed with each
    other and with nothing else.

This file ships the final block: `AGI_SEASON` per line AND the REAL vision
ids. To make drift impossible, the block lives in the node
``a00-80511a41-c96c9f`` and THIS FILE READS IT — the code fence under
``## Prime create lines (final)`` — and executes each parsed line through a
real subprocess. The only thing injected is ``--root <fixture>``, the one
environmental argument the Prime does not paste (the Prime runs from the repo
root); everything else — the command, the actor, every ``--set`` value, the
vision ids, the ``AGI_SEASON`` env — is byte-for-byte what a Prime reads in
the node and pastes.

Module-level ``DELIVERABLE`` is the one source of the cells the assertions
bind; the test that reconstructs it from the node block is the drift check
(ll: a block line that spells a different vision, season or council fails).

The NEGATIVE corner — the same app line WITHOUT season control landing
``season: 2`` on a ``current_season: 2`` ladder — is the measured reason the
control is load-bearing. It is asserted ONCE in kid 2's
``test_town_mint.py::test_season_set_is_overridden_at_mint_time``
(node_writer.py:770-777) and is cited, not duplicated, here.
"""
from __future__ import annotations

import json
import os
import re
import shlex
import subprocess
import sys
from pathlib import Path

import pytest

import towns

WRITE_PY_REL = "extensions/agi/bin/write.py"
WRITE_PY_ABS = str(Path(__file__).resolve().parents[1] / "bin" / "write.py")
RUNNER = sys.executable or "python3"
NODE_FILE = (Path(__file__).resolve().parents[3]
             / ".agi" / "nodes" / "experiment" / "a00-80511a41-c96c9f.md")
BLOCK_HEADING = "## Prime create lines (final)"

#: The ONE source of the cells the assertions bind: (slug, agi_season,
#: visions-tuple, council, season). The node block and this tuple are
#: cross-checked against each other by test_block_reconstructs_the_deliverable.
DELIVERABLE = (
    ("core", "2", ("vision:alive", "vision:all-is-one",
                   "vision:self-perpetuating"), "council-core", 2),
    ("streaming-suite", "1", ("vision:streaming-suite",),
     "council-streaming-suite", 1),
    ("web-app-suite", "1", ("vision:web-app-suite",),
     "council-web-app-suite", 1),
)


def _fixture(tmp_path: Path) -> Path:
    """Same fresh fixture project as kid 2/3's tests (the G11 shape): live
    [town].md copied byte-for-byte, current_season: 2 ladder, the three
    council rows + a prime_director row, nodes/ladder/ladder.md, and vision
    nodes whose ids are EXACTLY the five REAL ids above — never placeholders.
    """
    from graph_core.persistence import load_node_file  # noqa: F401
    import locations
    root = locations.find_project_root(Path(__file__))
    assert root is not None, "no project root for the live [town].md"
    schema = Path(root) / "context" / "schemas" / "[town].md"
    assert schema.is_file(), f"missing live schema: {schema}"

    proj = tmp_path / "proj"
    g = proj / ".agi"

    def _write(rel, content):
        p = g / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")

    _write("config.json", "{}\n")
    _write("context/schemas/[town].md", schema.read_text(encoding="utf-8"))
    _write("nodes/.geometry/ladder.md",
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
    _write("nodes/.geometry/posts.md",
           "---\nid: config:posts\nposts:\n"
           + "\n".join(f"  - {json.dumps(r)}" for r in posts) + "\n---\n")
    _write("nodes/ladder/ladder.md",
           "---\nid: ladder:ladder\ntype: ladder\n---\nbody\n")
    for vid in ("vision:alive", "vision:all-is-one", "vision:self-perpetuating",
                "vision:streaming-suite", "vision:web-app-suite"):
        _write(f"nodes/vision/{vid.split(':')[-1]}.md",
               f"---\nid: {vid}\ntype: vision\ntitle: x\n---\nbody\n")
    return proj


def _read_node_block_lines() -> list[str]:
    """The three shell lines under ``## Prime create lines (final)`` in the
    node file. One code fence, three lines, AGI_SEASON-led — the paste."""
    text = NODE_FILE.read_text(encoding="utf-8")
    m = re.search(rf"^{re.escape(BLOCK_HEADING)}\s*\n```sh?\s*\n(.*?)\n```",
                  text, re.M | re.S)
    assert m, f"no {BLOCK_HEADING} code fence found in {NODE_FILE}"
    lines = [ln for ln in m.group(1).splitlines() if ln.strip()]
    assert len(lines) == 3, f"expected 3 lines in the block, got {len(lines)}"
    return lines


def _parse_line(line: str) -> tuple[str, str, tuple, str, int]:
    """Split one block line -> (slug, agi_season, visions, council, season)."""
    toks = shlex.split(line)
    env_season = None
    arg_toks = []
    for t in toks:
        if t.startswith("AGI_SEASON=") and env_season is None:
            env_season = t.split("=", 1)[1]
        else:
            arg_toks.append(t)
    # arg_toks: [python, write.py, create, town, SLUG, --parent, ...]
    assert arg_toks[:4] == ["python3", WRITE_PY_REL, "create", "town"] or \
        ("create" in arg_toks and "town" in arg_toks), line
    slug = arg_toks[4]
    sets: dict[str, object] = {}
    for i, t in enumerate(arg_toks):
        if t == "--set" and i + 1 < len(arg_toks):
            k, _, v = arg_toks[i + 1].partition("=")
            sets[k] = v
    visions = tuple(json.loads(sets["visions"]))
    return (slug, env_season, visions, str(sets["council"]),
            int(sets["season"]))


def _run_line(proj: Path, line: str) -> subprocess.CompletedProcess:
    """Run ONE block line exactly, injecting only ``--root <fixture>``. The
    subprocess env is the Prime's dispatch env: AGI_ROLE=prime_director (the
    admitted actor) + AGI_SEASON per line. Everything else — command, actor,
    every --set value, the vision ids — is byte-for-byte the node-block line."""
    toks = shlex.split(line)
    env_season = None
    argv = []
    for t in toks:
        if t.startswith("AGI_SEASON=") and env_season is None:
            env_season = t.split("=", 1)[1]
        else:
            argv.append(t)
    # argv: [python3, write.py, create, town, SLUG, ...]. Drop the literal
    # interpreter token AND the literal script path, substitute the real
    # interpreter + write.py, and inject --root.
    rest = argv[2:]
    cmd = [RUNNER, WRITE_PY_ABS] + rest + ["--root", str(proj)]
    env = dict(os.environ)
    env["AGI_ROLE"] = "prime_director"
    if env_season is not None:
        env["AGI_SEASON"] = env_season
    return subprocess.run(cmd, env=env, capture_output=True, text=True)


def test_block_reconstructs_the_deliverable():
    """The node block and the module DELIVERABLE cannot drift: for every
    line parsed out of the node, its cells equal the tuple. A typo'd vision
    id, a wrong season, a dropped council — all fail here."""
    lines = _read_node_block_lines()
    assert len(lines) == len(DELIVERABLE)
    for line, (slug, season, visions, council, _s) in zip(lines, DELIVERABLE):
        got = _parse_line(line)
        assert got == (slug, season, tuple(visions), council, _s), (
            f"node block line drifted from DELIVERABLE:\n  {line}\n  got "
            f"{got}")


def test_block_lines_carry_seat_actor_and_explicit_role():
    """The corrected lines name the ACTOR as the seat (`belam`) and the ROLE
    explicitly (`--role prime_director`) — never a bare `--actor prime_director`
    that smuggles the role in under the actor flag. A regression back to the
    old spelling fails here, and the fixture mint (below) proves the spelling
    resolves and is admitted."""
    for line in _read_node_block_lines():
        toks = shlex.split(line)
        assert "--actor" in toks and "--role" in toks, line
        actor_i = toks.index("--actor")
        role_i = toks.index("--role")
        assert toks[actor_i + 1] == "belam", (
            f"actor must be the seat (belam), got {toks[actor_i + 1]!r}: "
            f"{line}")
        assert toks[role_i + 1] == "prime_director", (
            f"role must be explicit prime_director, got {toks[role_i + 1]!r}: "
            f"{line}")
        # --role must follow its --actor, never a bare --actor prime_director.
        assert role_i > actor_i, f"--role must follow --actor: {line}"


def test_delivered_lines_mint_the_ruling_cells(tmp_path, monkeypatch):
    """The EXACT node-block strings, run through a real subprocess on a
    fixture whose vision ids are the REAL five, mint the ruling table."""
    monkeypatch.delenv("AGI_ROLE", raising=False)
    monkeypatch.delenv("AGI_SEASON", raising=False)
    proj = _fixture(tmp_path)
    g = proj / ".agi"

    for line in _read_node_block_lines():
        res = _run_line(proj, line)
        assert res.returncode == 0, (
            f"line failed:\n  {line}\n  --root {proj}\n"
            f"stdout: {res.stdout}\nstderr: {res.stderr}")
        slug = _parse_line(line)[0]
        assert (g / "nodes" / "town" / f"{slug}.md").is_file(), slug

    by = {t.slug: t for t in towns.load_towns(g)}
    assert set(by) == {"core", "streaming-suite", "web-app-suite"}

    # FULL visions set for EVERY town (not just core), plus council + season.
    for slug, _season, visions, council, season in DELIVERABLE:
        t = by[slug]
        assert sorted(t.visions) == sorted(visions), slug
        assert t.council == council, slug
        assert t.season == season, slug

    # town_tuples equals the ruling table exactly.
    assert towns.town_tuples(g) == [
        {"town": "core", "season": 2, "global_season": 2,
         "council": "council-core"},
        {"town": "streaming-suite", "season": 1, "global_season": 2,
         "council": "council-streaming-suite"},
        {"town": "web-app-suite", "season": 1, "global_season": 2,
         "council": "council-web-app-suite"},
    ]

    # derive_names on the minted core town's OWN season equals the ruling.
    core = by["core"]
    assert towns.derive_names(
        "core", core.season, post="belam", loop_round="R7",
        agent="a00-1234") == [
            "core/main", "core/season2/main", "core/season2/posts/belam/main",
            "core/season2/posts/belam/loops/R7/a00-1234",
        ]


def test_delivered_vision_ids_resolve_on_the_live_tree():
    """Every vision id in the DELIVERED lines must resolve to a file under the
    LIVE .agi/nodes/vision/. This is the check the placeholder-id block
    (kid 3) was blind to: the fixture could agree with itself while the ids
    resolve to nothing live."""
    import locations
    root = locations.find_project_root(Path(__file__))
    assert root is not None, "no live project root"
    # find_project_root returns the .agi/ dir itself (the graph root).
    live_dir = Path(root) / "nodes" / "vision"
    assert live_dir.is_dir(), f"live vision dir missing: {live_dir}"

    delivered = {vid for (_s, _g, visions, _c, _n) in DELIVERABLE for vid in visions}
    assert delivered, "DELIVERABLE enumerates no vision ids"

    live_ids = {p.stem for p in live_dir.glob("*.md")}
    missing = sorted(delivered - {f"vision:{s}" for s in live_ids})
    assert not missing, (
        f"delivered vision ids with no live node under {live_dir}: {missing} — "
        f"a typo in the node block fails here")


def test_why_meaning_the_negative_is_cited_not_duplicated():
    """The NEGATIVE corner — the same app line WITHOUT season control mints
    season 2 on a current_season: 2 ladder — is already asserted once, in
    kid 2's test_town_mint.py::test_season_set_is_overridden_at_mint_time
    (node_writer.py:770-777). The corrected lines here are the FIX; the
    citation is the reason the season control is load-bearing."""
    # The citation must really resolve to a test that ASSERTS the override —
    # otherwise the FIX above is unreasoned and the season control untested.
    # Read the sibling module's source so the citation cannot drift into a
    # name that asserts nothing (this is the assertion that replaces the
    # old vacuous `assert True`).
    from pathlib import Path as _Path
    src = (_Path(__file__).resolve().parent / "test_town_mint.py").read_text()
    assert "def test_season_set_is_overridden_at_mint_time" in src, (
        "the cited negative-corner test no longer exists in test_town_mint.py")
    body = src.split("def test_season_set_is_overridden_at_mint_time", 1)[1]
    body = body.split("\n\ndef ", 1)[0]
    assert "assert" in body and "== 2" in body and "_mint" in body, (
        "the cited test must really assert the season override (== 2) via a "
        "mint, not merely name it")