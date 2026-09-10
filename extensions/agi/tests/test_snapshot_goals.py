"""Tests for bin/snapshot-goals.py — GOALS.md → nodes/goal/ (TODO L15)."""

import importlib.util
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

BIN = Path(__file__).resolve().parents[1] / "bin" / "snapshot-goals.py"
spec = importlib.util.spec_from_file_location("snapshot_goals", BIN)
sg = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sg)


GOALS_DOC = """# GOALS.md — sample

Preamble prose that must be ignored, including a stray G9 mention.

---

## G1 — Playable dungeon crawler (sandbox ladder) — status: active

Upgrade the scene one node at a time.

## G2 — Persistent ideation system — status: active

Adapt the research loop.

## G3 — Marketplace with proof-of-playtime — status: horizon

Design sketch only.

## G5 — Retired experiment — status: mothballed

Status value outside the taxonomy.

## G4 — Movement system

No status clause here.
"""


def run(project: Path, *args):
    """Run the script in-process-ish via subprocess for isolation.

    Defaults to `--from-doc`, the GOALS.md -> nodes import. That was the only
    direction until goal:g6.9 made the nodes authoritative and the bare
    invocation ambiguous; every test below this helper predates the flip and
    is about the import, so the helper supplies it rather than 40 call sites
    growing a flag. Render-direction tests pass `--render` explicitly and the
    helper stays out of their way.
    """
    if "--render" not in args and "--from-doc" not in args:
        args = ("--from-doc", *args)
    return subprocess.run(
        [sys.executable, str(BIN), "--project", str(project), *args],
        capture_output=True, text=True,
    )


@pytest.fixture()
def project(tmp_path):
    (tmp_path / "GOALS.md").write_text(GOALS_DOC, encoding="utf-8")
    (tmp_path / "nodes").mkdir()
    return tmp_path


def fm_of(path: Path) -> dict:
    parts = path.read_text(encoding="utf-8").split("---", 2)
    return yaml.safe_load(parts[1]) or {}


def goal_nodes(project: Path) -> dict:
    out = {}
    for p in sorted((project / "nodes" / "goal").glob("*.md")):
        out[fm_of(p)["id"]] = (p, fm_of(p))
    return out


def write_node(project: Path, rel: str, fm: dict, body: str = "body"):
    path = project / "nodes" / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    sg.write_frontmatter(path, fm, body)
    return path


# --- 1. parsing ------------------------------------------------------------


def test_parses_ids_titles_statuses(project):
    r = run(project)
    assert r.returncode == 0, r.stderr
    nodes = goal_nodes(project)
    assert set(nodes) == {"goal:g1", "goal:g2", "goal:g3", "goal:g4", "goal:g5"}

    path, fm = nodes["goal:g1"]
    assert fm["goal_id"] == "G1"
    assert fm["title"] == "G1: Playable dungeon crawler (sandbox ladder)"
    assert fm["status"] == "active"
    assert fm["type"] == "goal"
    assert fm["origin"] == "goals-doc"
    assert fm["tags"] == ["goal", "root"]
    assert fm["confidence"] == 1.0
    assert path.name.startswith("g1-playable-dungeon-crawler")
    assert "Upgrade the scene one node at a time." in path.read_text()
    # preamble ignored, body stops at the next `## ` heading
    assert "Preamble prose" not in path.read_text()
    assert "Adapt the research loop" not in path.read_text()

    # missing `status:` clause defaults to active
    assert nodes["goal:g4"][1]["status"] == "active"
    assert nodes["goal:g4"][1]["title"] == "G4: Movement system"


def test_no_next_edges_emitted(project):
    run(project)
    for _path, fm in goal_nodes(project).values():
        assert "next_edges" not in fm
        assert "parents" not in fm


# --- 2. unknown status -----------------------------------------------------


def test_unknown_status_preserved_and_warns(project):
    r = run(project)
    assert r.returncode == 0
    assert goal_nodes(project)["goal:g5"][1]["status"] == "mothballed"
    assert "WARN: goal G5 has unrecognized status 'mothballed'" in r.stderr


def test_horizon_is_a_known_status(project):
    # `horizon` is in the taxonomy: a goal declared but not yet being worked.
    r = run(project)
    assert goal_nodes(project)["goal:g3"][1]["status"] == "horizon"
    assert "horizon" not in r.stderr


# --- 3. seeds from parents -------------------------------------------------


def test_seeds_populated_from_parent_pointer(project):
    write_node(project, "idea/seed-a.md",
               {"id": "idea:seed-a", "type": "idea", "parents": ["goal:g1"]})
    write_node(project, "idea/seed-b.md",
               {"id": "idea:seed-b", "type": "idea", "parents": ["goal:g1"]})
    r = run(project)
    assert r.returncode == 0
    nodes = goal_nodes(project)
    assert nodes["goal:g1"][1]["seeds"] == ["idea:seed-a", "idea:seed-b"]
    assert nodes["goal:g2"][1]["seeds"] == []


# --- 4. referential integrity ---------------------------------------------


def test_unknown_goal_ref_warns_but_exits_zero(project):
    write_node(project, "idea/orphan.md",
               {"id": "idea:orphan", "type": "idea", "parents": ["goal:g99"]})
    r = run(project)
    assert r.returncode == 0
    assert "INTEGRITY" in r.stderr
    assert "unknown goal 'goal:g99'" in r.stderr
    assert "orphan.md" in r.stderr


def test_unknown_goal_ref_fails_under_strict(project):
    write_node(project, "idea/orphan.md",
               {"id": "idea:orphan", "type": "idea", "parents": ["goal:g99"]})
    r = run(project, "--strict")
    assert r.returncode == 1
    assert "INTEGRITY" in r.stderr
    # goal nodes are still written even in strict mode
    assert set(goal_nodes(project)) == {"goal:g1", "goal:g2", "goal:g3", "goal:g4", "goal:g5"}


def test_strict_exits_zero_when_all_refs_resolve(project):
    write_node(project, "idea/seed-a.md",
               {"id": "idea:seed-a", "type": "idea", "parents": ["goal:g2"]})
    r = run(project, "--strict")
    assert r.returncode == 0


# --- 4b. referential integrity, extended to every parent prefix (G7.1) -----
#
# L15 (later G7.1) only ever validated `goal:`-prefixed parents. On the real
# corpus 89 non-goal parent refs dangled with nothing reporting it — a
# `hypothesis:` vs `hyp:` prefix typo silently disconnected most of the
# `spawns` graph. These tests pin the extension: same mechanism (warn by
# default, exit 0; --strict exits 1), now applied to every prefix, plus a
# distinct message when the dangling ref is a same-slug/different-prefix typo
# of a real id (actionable) versus a genuinely missing node (noise otherwise).


def test_unknown_non_goal_ref_warns_but_exits_zero(project):
    write_node(project, "idea/orphan.md",
               {"id": "idea:orphan", "type": "idea",
                "parents": ["hyp:does-not-exist-anywhere"]})
    r = run(project)
    assert r.returncode == 0
    assert "INTEGRITY" in r.stderr
    assert "unknown parent 'hyp:does-not-exist-anywhere'" in r.stderr
    assert "orphan.md" in r.stderr


def test_unknown_non_goal_ref_fails_under_strict(project):
    write_node(project, "idea/orphan.md",
               {"id": "idea:orphan", "type": "idea",
                "parents": ["hyp:does-not-exist-anywhere"]})
    r = run(project, "--strict")
    assert r.returncode == 1
    assert "INTEGRITY" in r.stderr


def test_known_non_goal_ref_is_not_flagged(project):
    write_node(project, "hyp/real.md",
               {"id": "hyp:real-thing", "type": "hyp"})
    write_node(project, "idea/child.md",
               {"id": "idea:child", "type": "idea", "parents": ["hyp:real-thing"]})
    r = run(project, "--strict")
    assert r.returncode == 0
    assert "INTEGRITY" not in r.stderr


def test_prefix_mismatch_reported_distinctly_with_suggestion(project):
    """`hypothesis:` vs `hyp:` — the real cause found on the live corpus."""
    write_node(project, "hyp/real.md",
               {"id": "hyp:chain-engine-r1", "type": "hyp"})
    write_node(project, "idea/child.md",
               {"id": "idea:child", "type": "idea",
                "parents": ["hypothesis:chain-engine-r1"]})
    r = run(project)
    assert r.returncode == 0
    assert "unknown parent 'hypothesis:chain-engine-r1'" in r.stderr
    assert "prefix typo" in r.stderr
    assert "did you mean 'hyp:chain-engine-r1'" in r.stderr


def test_genuinely_missing_ref_has_no_suggestion(project):
    """No node anywhere shares the slug — must not fabricate a suggestion."""
    write_node(project, "idea/child.md",
               {"id": "idea:child", "type": "idea",
                "parents": ["hyp:totally-unrelated-slug"]})
    r = run(project)
    assert r.returncode == 0
    assert "unknown parent 'hyp:totally-unrelated-slug'" in r.stderr
    assert "prefix typo" not in r.stderr


def test_goal_ref_message_unchanged_by_the_extension(project):
    """Backward compatibility: `goal:` refs keep their original exact wording."""
    write_node(project, "idea/orphan.md",
               {"id": "idea:orphan", "type": "idea", "parents": ["goal:g99"]})
    r = run(project)
    assert r.returncode == 0
    assert "INTEGRITY" in r.stderr
    assert "unknown goal 'goal:g99'" in r.stderr
    assert "unknown parent 'goal:g99'" not in r.stderr


def test_summary_line_splits_prefix_mismatch_from_missing(project):
    write_node(project, "hyp/real.md", {"id": "hyp:chain-engine-r1", "type": "hyp"})
    write_node(project, "idea/a.md",
               {"id": "idea:a", "type": "idea",
                "parents": ["hypothesis:chain-engine-r1"]})  # prefix mismatch
    write_node(project, "idea/b.md",
               {"id": "idea:b", "type": "idea",
                "parents": ["hyp:nothing-like-this-exists"]})  # genuinely missing
    r = run(project)
    assert r.returncode == 0
    assert "unresolved parent references: 2 (1 prefix-mismatch, 1 missing)" in r.stdout


# --- 5. pruning ------------------------------------------------------------


def test_prune_removes_stale_goals_doc_but_spares_agent_nodes(project):
    stale = write_node(project, "goal/g42-obsolete.md",
                       {"id": "goal:g42", "type": "goal", "origin": "goals-doc"})
    agent = write_node(project, "goal/hand-written.md",
                       {"id": "goal:hand-written", "type": "goal"})
    other = write_node(project, "goal/from-build-site.md",
                       {"id": "goal:bs", "type": "goal", "origin": "build-site"})
    r = run(project)
    assert r.returncode == 0
    assert not stale.exists()
    assert agent.exists()
    assert other.exists()


def test_prune_removes_renamed_slug_duplicate(project):
    old = write_node(project, "goal/g1-old-title.md",
                     {"id": "goal:g1", "type": "goal", "origin": "goals-doc"})
    r = run(project)
    assert r.returncode == 0
    assert not old.exists()
    assert len(list((project / "nodes" / "goal").glob("g1-*.md"))) == 1


# --- 6. missing GOALS.md ---------------------------------------------------


def test_missing_goals_md_is_noop_and_prunes_nothing(tmp_path):
    (tmp_path / "nodes").mkdir()
    keep = write_node(tmp_path, "goal/g1-existing.md",
                      {"id": "goal:g1", "type": "goal", "origin": "goals-doc"})
    r = run(tmp_path)
    assert r.returncode == 0
    assert "skipping" in r.stdout
    assert keep.exists()


# --- 7. idempotence --------------------------------------------------------


def test_idempotent_byte_identical(project):
    write_node(project, "idea/seed-a.md",
               {"id": "idea:seed-a", "type": "idea", "parents": ["goal:g1"]})
    assert run(project).returncode == 0
    first = {p.name: p.read_bytes()
             for p in sorted((project / "nodes" / "goal").glob("*.md"))}
    assert run(project).returncode == 0
    second = {p.name: p.read_bytes()
              for p in sorted((project / "nodes" / "goal").glob("*.md"))}
    assert first == second
    assert first  # non-empty


# --- parser unit -----------------------------------------------------------


def test_parse_goals_body_cap():
    """goal:s12 changed this contract deliberately. It used to assert a hard
    `[:4000]` cut; a single 6000-char block has no boundary inside it, so the
    new rule keeps it whole and warns rather than severing it mid-stream. The
    old assertion was encoding the defect."""
    text = "## G1 — Big — status: active\n\n" + ("x" * 6000)
    goals = sg.parse_goals(text)
    assert len(goals[0]["body"]) == 6000


def test_parse_goals_truncates_visibly_at_a_block_boundary(monkeypatch):
    """The cap still binds when the body *has* boundaries — and when it binds,
    it says so in the body rather than stopping mid-sentence.

    The cap is pinned here rather than read from a config: agi-tree's own
    config sets `goal_body_cap: 0` (goal:g6.9 — a source of truth cannot be
    capped), so without this the test silently stops testing anything.
    """
    monkeypatch.setattr(sg, "body_cap", lambda: 4000)
    blocks = "\n\n".join(f"para {i} " + "y" * 300 for i in range(30))
    goals = sg.parse_goals(f"## G1 — Big — status: active\n\n{blocks}")
    body = goals[0]["body"]
    assert len(body) < len(blocks)
    assert body.rstrip().endswith("]**")     # the marker, not a severed word
    assert "truncated:" in body


# --------------------------------------------- H0i: re-snapshot must not strip

def test_resnapshot_preserves_fields_the_snapshot_does_not_own(project):
    """Regression: rebuilding frontmatter from GOALS.md dropped everything else.

    The same defect in snapshot-build-site.py severed `next_edges` on 15 nodes
    of the live agi-tree corpus — chain structure deleted by a render pass.
    """
    assert run(project).returncode == 0
    node = next((project / "nodes" / "goal").glob("g1-*.md"))

    text = node.read_text(encoding="utf-8")
    head, body = text.split("---", 2)[1], text.split("---", 2)[2]
    node.write_text(
        f"---{head}next_edges:\n  - idea:seeded\nembedding_coords: [0.1, 0.2]\n"
        f"---{body}",
        encoding="utf-8",
    )

    assert run(project).returncode == 0
    fm = fm_of(node)
    assert fm["next_edges"] == ["idea:seeded"]
    assert "embedding_coords" in fm
    # Snapshot-owned fields still come from GOALS.md, not the old file.
    assert fm["status"] == "active"
    assert fm["goal_id"] == "G1"


# ------------------------------------- sub-goals and standalone short-term goals

NESTED_DOC = """# GOALS.md

## G1 — Long term thing — status: active

Long body.

### G1.2 — A short step inside G1 — status: active

Sub body.

### G1.3 — Another step — status: complete

Sub body two.

## S1 — Standalone short-term item — status: active

Short body.

## G2 — Second long term — status: horizon

Second body.
"""


@pytest.fixture()
def nested(tmp_path):
    (tmp_path / "GOALS.md").write_text(NESTED_DOC, encoding="utf-8")
    (tmp_path / "nodes").mkdir()
    return tmp_path


def _by_id(project: Path) -> dict:
    return {fm_of(p)["id"]: fm_of(p)
            for p in (project / "nodes" / "goal").glob("*.md")}


def test_subgoals_and_short_term_goals_become_nodes(nested):
    assert run(nested).returncode == 0
    nodes = _by_id(nested)
    assert set(nodes) == {"goal:g1", "goal:g1.2", "goal:g1.3", "goal:s1",
                          "goal:g2"}


def test_ingest_keeps_a_build_parent_the_hierarchy_cannot_know_about(nested):
    """A goal may name the build node that produced it (`[goal].md`, 2026-09-05).

    The import direction rebuilds `parents:` from the heading hierarchy, and a
    heading only ever yields the goal parent -- so an unguarded rebuild drops
    the other half silently. It must keep the non-goal parents already on disk
    and still derive the goal parent from the hierarchy, because the hierarchy
    is the authority on that one and only that one.
    """
    # Written at the slug the import will rewrite, so this is the same node
    # coming back rather than a second file with the same id.
    write_node(nested, "goal/g1.2-a-short-step-inside-g1.md", {
        "id": "goal:g1.2", "type": "goal", "goal_id": "G1.2",
        "title": "A short step inside G1", "status": "active", "goal_kind": "subgoal",
        "heading_level": 3, "seeds": [], "tags": ["goal", "subgoal"],
        "confidence": 1.0,
        # The wrong goal parent on purpose: it must be REPLACED from the
        # hierarchy, while the build parent beside it survives.
        "parents": ["goal:g9", "build:COMPLETE.md"],
    })
    run(nested)
    parents = _by_id(nested)["goal:g1.2"]["parents"]
    assert parents[0] == "goal:g1"
    assert "build:COMPLETE.md" in parents
    assert "goal:g9" not in parents


def test_subgoal_parent_points_at_its_long_term_goal(nested):
    run(nested)
    nodes = _by_id(nested)
    assert nodes["goal:g1.2"]["parents"] == ["goal:g1"]
    assert nodes["goal:g1.3"]["parents"] == ["goal:g1"]
    assert nodes["goal:g1.2"]["goal_kind"] == "subgoal"
    # A sub-goal is not a root.
    assert "root" not in nodes["goal:g1.2"]["tags"]


def test_short_term_goal_is_a_root_with_no_parent(nested):
    run(nested)
    s1 = _by_id(nested)["goal:s1"]
    assert s1["goal_kind"] == "short-term"
    assert "parents" not in s1
    assert "root" in s1["tags"]


def test_subgoal_carries_its_own_status(nested):
    run(nested)
    nodes = _by_id(nested)
    assert nodes["goal:g1.2"]["status"] == "active"
    assert nodes["goal:g1.3"]["status"] == "complete"


def test_subgoal_body_is_not_absorbed_into_its_parent(nested):
    run(nested)
    g1 = next((nested / "nodes" / "goal").glob("g1-*.md")).read_text()
    assert "Long body." in g1
    assert "Sub body." not in g1


def test_long_term_goals_are_unchanged_by_the_new_kinds(nested):
    run(nested)
    g2 = _by_id(nested)["goal:g2"]
    assert g2["goal_kind"] == "long-term"
    assert g2["tags"] == ["goal", "root"]
    assert "parents" not in g2


# ------------------------------------------------ --strict-goals (goal:g5)


def _sg_run(project, *extra):
    import subprocess, sys
    # Same default as `run()` above: these tests are about the import
    # direction, which goal:g6.9 moved behind `--from-doc`.
    if "--render" not in extra and "--from-doc" not in extra:
        extra = ("--from-doc", *extra)
    return subprocess.run(
        [sys.executable, str(Path(__file__).resolve().parents[1] / "bin" / "snapshot-goals.py"),
         "--project", str(project), *extra],
        capture_output=True, text=True,
    )


def _sg_project(tmp_path, goals_md, seed_parent):
    (tmp_path / "agi-tree.config.json").write_text("{}")
    (tmp_path / "GOALS.md").write_text(goals_md)
    d = tmp_path / "nodes" / "idea"
    d.mkdir(parents=True)
    (d / "seed.md").write_text(
        f'---\nid: "idea:seed"\ntype: idea\nparents:\n  - {seed_parent}\n---\n\nbody\n')
    return tmp_path


GOALS = "# GOALS\n\n## G1 — Real goal — status: active\n\nbody\n"


def test_strict_goals_fails_on_a_dangling_goal_reference(tmp_path):
    """goal:g5 — 'fail loudly when a seed node points at a goal id that does
    not exist.' Loudly means non-zero, not a line in a log with 81 others."""
    p = _sg_project(tmp_path, GOALS, "goal:g99")
    r = _sg_run(p, "--strict-goals")
    assert r.returncode == 1
    assert "unresolved goal reference" in r.stderr


def test_strict_goals_ignores_non_goal_dangling_parents(tmp_path):
    """Narrower than --strict on purpose. The live tree carries 81 unresolved
    *parent* refs and 0 unresolved goal refs, so a flag that failed on both
    could never be enabled in driver.sh."""
    p = _sg_project(tmp_path, GOALS, "hypothesis:does-not-exist")
    assert _sg_run(p, "--strict-goals").returncode == 0
    assert _sg_run(p, "--strict").returncode == 1


def test_strict_goals_passes_when_every_goal_ref_resolves(tmp_path):
    p = _sg_project(tmp_path, GOALS, "goal:g1")
    assert _sg_run(p, "--strict-goals").returncode == 0


def test_default_still_only_warns(tmp_path):
    """Enforcement is opt-in; the bare invocation must not start failing."""
    p = _sg_project(tmp_path, GOALS, "goal:g99")
    r = _sg_run(p)
    assert r.returncode == 0
    assert "unknown goal" in r.stderr


# --- write_frontmatter: None must round-trip as null, not the string "None" -
#
# Found live 2026-08-25 backfilling `mint_id` across the agi-tree corpus
# (goal:g2.5): any node carrying a real YAML null (`contrasts:` with nothing
# after it, or a malformed empty `parents:` list entry -- already a known,
# tolerated shape; see `collect_parent_refs`'s empty-entry handling above)
# came back from ONE write_frontmatter round trip as the literal 4-character
# string "None" -- `str(None)` falling through the plain scalar branch. That
# turns a null field into a truthy value, and for `parents: [None]`
# specifically it defeats `collect_parent_refs`'s own empty-entry filter,
# which only special-cases `p is None`, not the string `"None"` -- so a
# malformed-but-recognized entry becomes a phantom dangling reference to a
# node literally named "None".


def test_write_frontmatter_preserves_none_scalar(tmp_path):
    p = write_node(tmp_path, "verdict/x.md", {"id": "verdict:x", "contrasts": None})
    assert fm_of(p)["contrasts"] is None


def test_write_frontmatter_preserves_none_list_entry(tmp_path):
    p = write_node(tmp_path, "hypothesis/x.md", {"id": "hyp:x", "parents": [None]})
    assert fm_of(p)["parents"] == [None]


def test_write_frontmatter_none_survives_a_second_round_trip(tmp_path):
    """The regression was specifically a round-trip: write, re-load, write
    again -- exactly what a generator with `preserve=` does on every run."""
    p = write_node(tmp_path, "verdict/x.md", {"id": "verdict:x", "contrasts": None,
                                              "parents": [None]})
    fm = fm_of(p)
    sg.write_frontmatter(p, fm, "body")
    fm2 = fm_of(p)
    assert fm2["contrasts"] is None
    assert fm2["parents"] == [None]


# --- goal:s12 — a truncated goal body must be visibly truncated --------------


@pytest.fixture()
def capped_project(tmp_path, monkeypatch):
    """A project whose config sets a small `goal_body_cap`, so the cap path is
    exercised without needing a 4000-character fixture."""
    (tmp_path / "agi-tree.config.json").write_text('{"goal_body_cap": 120}')
    monkeypatch.setattr(sg, "PROJECT_ROOT", tmp_path)
    return tmp_path


def test_body_cap_reads_the_project_config(capped_project):
    assert sg.body_cap() == 120


def test_body_cap_falls_back_on_a_broken_config(tmp_path, monkeypatch):
    (tmp_path / "agi-tree.config.json").write_text("{not json")
    monkeypatch.setattr(sg, "PROJECT_ROOT", tmp_path)
    assert sg.body_cap() == sg.BODY_CAP


def test_body_under_the_cap_is_untouched(capped_project):
    body = "short enough\n\nto keep whole"
    assert sg.cap_body(body, "G1") == body


def test_truncation_cuts_at_a_block_boundary_and_says_so(capped_project, capsys):
    """The exact defect goal:s12 records: `goal:g2.5`'s node body ended
    `| Assigned | once, at node creation | derived,` — a markdown table severed
    mid-cell. A block boundary makes that impossible; the marker makes the loss
    legible to a reader who only ever sees the node."""
    table = ("| a | b |\n|---|---|\n| once, at node creation | derived, freely |")
    body = "first paragraph\n\n" + table + "\n\n" + ("tail " * 40).strip()
    out = sg.cap_body(body, "G2.5")

    assert out.startswith("first paragraph")
    assert table in out                      # whole, or not at all
    assert "characters dropped at a block boundary" in out
    assert "GOALS.md" in out and "G2.5" in out
    assert "WARN: goal G2.5" in capsys.readouterr().err


def test_an_unsplittable_first_block_is_kept_whole_not_severed(capped_project, capsys):
    """An honest overrun beats a malformed fragment: there is no boundary
    inside a single over-cap block, so cutting anyway would reintroduce the
    bug in the one case it is least recoverable."""
    body = "x" * 500
    assert sg.cap_body(body, "G9") == body
    assert "unsplittable" in capsys.readouterr().err


def test_zero_cap_disables_capping(tmp_path, monkeypatch):
    (tmp_path / "agi-tree.config.json").write_text('{"goal_body_cap": 0}')
    monkeypatch.setattr(sg, "PROJECT_ROOT", tmp_path)
    body = "para\n\n" + "y" * 10000
    assert sg.cap_body(body, "G1") == body


def test_truncation_is_never_silent(capped_project, capsys):
    """The whole of question 1: whatever the cap is, a reader of the graph can
    always tell a complete goal from a clipped one — in the body AND on
    stderr."""
    body = "\n\n".join(["block %d" % i + " " + "z" * 40 for i in range(10)])
    out = sg.cap_body(body, "G7")
    assert len(out) < len(body)
    assert "truncated:" in out
    assert "WARN: goal G7" in capsys.readouterr().err


# --- goal:g6.9 — the nodes are the source; GOALS.md is rendered from them ----


def test_bare_invocation_refuses_to_guess_a_direction(project):
    """Two directions exist and they are not interchangeable: one writes nodes
    and prunes, the other writes a document and cannot. Defaulting to either
    silently would be the H0i shape (a generator input deciding what survives)."""
    r = subprocess.run([sys.executable, str(BIN), "--project", str(project)],
                       capture_output=True, text=True)
    assert r.returncode == 2
    assert "--render" in r.stderr and "--from-doc" in r.stderr


def test_round_trip_is_byte_identical(project):
    """`render(parse(t)) == t` — the migration's own falsifier. A renderer that
    is merely close produces a diff on every run and nobody reads it after the
    third time."""
    run(project)                                  # import: doc -> nodes
    assert run(project, "--render").returncode == 0   # render: nodes -> doc
    assert run(project, "--render", "--check").returncode == 0


def test_heading_level_is_stored_not_inferred(nested):
    """Heading depth is recorded on the node — not derivable, since depth
    would have to be guessed from the id shape. Document position used to be
    a second such field (`order:`); it is retired (this iteration) in favour
    of a natural sort over `goal_id`, so no node should carry it."""
    run(nested)
    nodes = goal_nodes(nested)
    assert nodes["goal:g1"][1]["heading_level"] == 2
    assert nodes["goal:g1.2"][1]["heading_level"] == 3
    assert nodes["goal:s1"][1]["heading_level"] == 2
    for _p, fm in nodes.values():
        assert "order" not in fm


def test_document_order_is_naturally_sorted_by_goal_id_on_render(tmp_path):
    """`order:` is retired: rendering now sorts by a natural read of
    `goal_id` instead of a stored document position. S11..S17 used to sit
    before S1..S10 in the real document (ids are never renumbered and the
    file grew that way) — the render now corrects that once, deliberately,
    rather than preserving the historical, unsorted order."""
    doc = ("# T\n\npre\n\n## S11 — Later — status: active\n\nb11\n\n"
           "## S1 — Earlier — status: active\n\nb1\n")
    (tmp_path / "GOALS.md").write_text(doc)
    (tmp_path / "nodes").mkdir()
    run(tmp_path)
    run(tmp_path, "--render")
    out = (tmp_path / "GOALS.md").read_text()
    assert out.index("## S1 —") < out.index("## S11")


# --- natural_sort_key: order: 's replacement -----------------------------


def test_natural_sort_orders_dotted_subgoals_numerically():
    """A plain lexicographic sort puts `G2.10` between `G2.1` and `G2.2`,
    which is exactly the defect a numeric-aware key exists to avoid."""
    ids = ["G2.10", "G2.1", "G2.11", "G2.9", "G2.2"]
    ordered = sorted(ids, key=sg.natural_sort_key)
    assert ordered == ["G2.1", "G2.2", "G2.9", "G2.10", "G2.11"]


def test_natural_sort_orders_short_term_goals_numerically():
    ids = ["S11", "S1", "S2", "S21", "S9", "S10"]
    ordered = sorted(ids, key=sg.natural_sort_key)
    assert ordered == ["S1", "S2", "S9", "S10", "S11", "S21"]


def test_natural_sort_puts_g_goals_before_s_goals():
    ids = ["S1", "G1", "S2", "G2"]
    ordered = sorted(ids, key=sg.natural_sort_key)
    assert ordered == ["G1", "G2", "S1", "S2"]


def test_natural_sort_full_worked_example():
    """The exact ordering the migration's spec calls out."""
    ids = ["G1", "G1.5", "G2", "G2.5", "G2.7", "G2.10", "G2.11", "G3",
           "G9.6", "G10", "G10.1", "G11", "G11.1", "G12", "G12.2",
           "S1", "S2", "S11", "S21"]
    import random
    shuffled = ids[:]
    random.Random(0).shuffle(shuffled)
    assert sorted(shuffled, key=sg.natural_sort_key) == ids


def test_preamble_becomes_a_doc_node_not_a_goal(project):
    """160 lines of design contract that the parser used to discard. `type: doc`
    so it does not become a phantom entry in every count that reads
    `type == goal`."""
    run(project)
    node = project / "nodes" / "doc" / "goals-preamble.md"
    assert node.exists()
    fm = fm_of(node)
    assert fm["id"] == "doc:goals-preamble" and fm["type"] == "doc"
    assert "Preamble prose" in node.read_text()
    assert "goal:" not in str(sorted(goal_nodes(project))).replace("goal:g", "")


def test_the_banner_does_not_accrete_across_round_trips(project):
    run(project)
    for _ in range(3):
        run(project, "--render")
        run(project)
    assert (project / "GOALS.md").read_text().count("<!-- GENERATED") == 1


def test_deleting_a_heading_does_not_delete_the_node(project):
    """goal:g6.9's pre-registered falsifier. The whole hazard of inverting this
    direction is that `--from-doc` prunes; `--render` must not be able to."""
    run(project)
    doc = project / "GOALS.md"
    before = doc.read_text()
    doc.write_text(before.replace(
        "## G2 — Persistent ideation system — status: active\n\nAdapt the research loop.\n", ""))
    assert "## G2 " not in doc.read_text()

    assert run(project, "--render").returncode == 0
    assert "goal:g2" in goal_nodes(project)                 # node survived
    assert "## G2 " in doc.read_text()                      # heading restored


def test_render_refuses_to_write_an_empty_document(tmp_path):
    """A missing/empty nodes/goal/ must never be read as 'the project has no
    goals' — that is H0's shape with the arrow reversed."""
    (tmp_path / "nodes").mkdir()
    (tmp_path / "GOALS.md").write_text("# real content\n")
    r = run(tmp_path, "--render")
    assert r.returncode == 1
    assert (tmp_path / "GOALS.md").read_text() == "# real content\n"


def test_a_goal_node_missing_heading_level_is_a_hard_error(project):
    run(project)
    path, fm = goal_nodes(project)["goal:g1"]
    del fm["heading_level"]
    sg.write_frontmatter(path, fm, "body", origin="goals-doc")
    r = run(project, "--render")
    assert r.returncode != 0
    assert "heading_level" in r.stderr


def test_a_goal_node_missing_order_renders_without_error(tmp_path):
    """`order:` is retired: a goal node need not carry it at all, and its
    absence must render cleanly -- unlike a missing `heading_level`, which is
    still a hard error (see the test above). Natural-sort-by-`goal_id`
    replaces the stored document position this field used to hold."""
    (tmp_path / "nodes").mkdir()
    write_node(tmp_path, "goal/g1-only.md",
               {"id": "goal:g1", "type": "goal", "goal_id": "G1",
                "title": "G1: Only goal", "status": "active",
                "heading_level": 2, "origin": "goals-doc"})
    assert "order" not in fm_of(tmp_path / "nodes" / "goal" / "g1-only.md")
    r = run(tmp_path, "--render")
    assert r.returncode == 0
    assert "G1" in (tmp_path / "GOALS.md").read_text()


def test_integrity_check_runs_in_the_render_direction_too(project):
    """G7.1's sweep has run every iteration since it was built. Making the
    render the default must not retire a live check as a side effect."""
    run(project)
    write_node(project, "idea/orphan.md",
               {"id": "idea:orphan", "type": "idea", "parents": ["goal:g99"]})
    r = run(project, "--render")
    assert "unknown goal 'goal:g99'" in r.stderr
    assert run(project, "--render", "--strict-goals").returncode == 1


def test_write_frontmatter_preserves_embedded_double_quotes(tmp_path):
    """Found by g6.9's round-trip check: S13's own title — `... the string
    "None"` — came back out of its node as `'None'`, because the serializer
    substituted the character instead of escaping it. Silent data loss in the
    one function that touches every node on every run, which is S13's finding
    about a line three below where it was fixed."""
    title = 'S13 — serialized YAML null as the string "None"'
    p = write_node(tmp_path, "goal/x.md", {"id": "goal:x", "title": title})
    assert fm_of(p)["title"] == title


def test_write_frontmatter_preserves_backslashes(tmp_path):
    value = 'a \\ b " c'
    p = write_node(tmp_path, "goal/y.md", {"id": "goal:y", "title": value})
    assert fm_of(p)["title"] == value


def test_prune_only_touches_nodes_this_script_can_produce(project):
    """A generator may delete only what it can produce.

    `origin: goals-doc` alone was the prune predicate, and `doc:goals-preamble`
    carries that origin without being a goal heading. The published engine —
    still running the origin-only rule — deleted it within an hour of it
    existing (loop.log, 2026-08-25T23:04:50Z). Recovered from the grid; the
    rule is narrowed here so the class cannot recur.
    """
    run(project)
    other = write_node(project, "doc/notes.md",
                       {"id": "doc:notes", "type": "doc", "origin": "goals-doc"})
    assert other.exists()
    run(project)                       # a second import must not sweep it
    assert other.exists()
    assert (project / "nodes" / "doc" / "goals-preamble.md").exists()


def test_prune_still_removes_a_goal_the_document_dropped(project):
    """The narrowing must not disable the prune it narrows: a goal heading that
    leaves GOALS.md still takes its node with it under `--from-doc`."""
    run(project)
    assert "goal:g2" in goal_nodes(project)
    doc = project / "GOALS.md"
    doc.write_text(doc.read_text().replace(
        "## G2 — Persistent ideation system — status: active\n\nAdapt the research loop.\n", ""))
    run(project)
    assert "goal:g2" not in goal_nodes(project)


# --- THOUGHT: the authored region of a body (goal:g2.10, goal:g2.11) -------


def test_extract_thought_absent_is_none():
    """Absence is legal and means empty -- that is what made adding the field
    cost zero churn across 786 existing nodes."""
    assert sg.extract_thought("just a body") is None
    assert sg.extract_thought("") is None
    assert sg.extract_thought(None) is None


def test_extract_thought_returns_block_with_markers():
    body = f"derived prose\n\n{sg.THOUGHT_BEGIN}\nwhy I did it\n{sg.THOUGHT_END}"
    got = sg.extract_thought(body)
    assert got is not None
    assert "why I did it" in got
    assert got.startswith("<!--") and got.endswith("-->")


def test_extract_thought_is_multiline_and_non_greedy():
    body = (f"{sg.THOUGHT_BEGIN}\nline one\n\nline two\n{sg.THOUGHT_END}\n"
            f"trailing derived prose")
    got = sg.extract_thought(body)
    assert "line one" in got and "line two" in got
    assert "trailing derived prose" not in got


def test_splice_carries_thought_across_a_regenerating_write():
    """The whole point of g2.10: a scan rewrites the body, the thought lives."""
    old = f"OLD derived\n\n{sg.THOUGHT_BEGIN}\nthe reasoning\n{sg.THOUGHT_END}"
    new = "NEW derived, freshly generated"
    out = sg.splice_thought(new, old)
    assert "NEW derived" in out
    assert "the reasoning" in out
    assert "OLD derived" not in out


def test_splice_prefers_a_thought_authored_this_pass():
    """Clobbering a fresh thought with a stale one is the same defect
    reversed."""
    old = f"x\n{sg.THOUGHT_BEGIN}\nSTALE\n{sg.THOUGHT_END}"
    new = f"y\n{sg.THOUGHT_BEGIN}\nFRESH\n{sg.THOUGHT_END}"
    out = sg.splice_thought(new, old)
    assert "FRESH" in out and "STALE" not in out


def test_splice_is_a_noop_without_a_stored_thought():
    assert sg.splice_thought("body", "no thought here") == "body"
    assert sg.splice_thought("body", None) == "body"


def test_write_frontmatter_preserves_thought_block(tmp_path):
    """End-to-end: the falsifier goal:g2.10 names -- write a thought, let the
    generator rewrite the body, read it back."""
    p = tmp_path / "n.md"
    fm = {"id": "build:x", "type": "build", "title": "x"}
    sg.write_frontmatter(
        p, fm,
        f"v1 derived\n\n{sg.THOUGHT_BEGIN}\nchose X over Y\n{sg.THOUGHT_END}")
    stored = p.read_text()
    assert "chose X over Y" in stored

    old_body = stored.split("---", 2)[2]
    sg.write_frontmatter(p, fm, "v2 derived, wholly regenerated",
                         preserve_body=old_body)
    after = p.read_text()
    assert "v2 derived" in after
    assert "chose X over Y" in after, "the scan wiped the thought (g2.10)"
    assert "v1 derived" not in after


def test_write_frontmatter_without_preserve_body_still_wipes(tmp_path):
    """Opt-in, not automatic: a caller that does not pass the old body gets the
    old behaviour, so this change cannot silently resurrect prose elsewhere."""
    p = tmp_path / "n.md"
    fm = {"id": "build:x", "type": "build", "title": "x"}
    sg.write_frontmatter(
        p, fm, f"{sg.THOUGHT_BEGIN}\nSENTINEL_THOUGHT\n{sg.THOUGHT_END}")
    sg.write_frontmatter(p, fm, "regenerated")
    assert "SENTINEL_THOUGHT" not in p.read_text().split("---", 2)[2]


def test_one_serializer_not_two():
    """goal:s14's residual. The two copies had already drifted apart on both
    null round-trip fixes; a third copy must not appear.

    Identity (`is`) is the wrong assertion and was tried first: each file-path
    import builds its own module object, so two `exec_module` calls on the same
    source yield equal-but-distinct functions. The invariant that actually
    matters is where the function is *defined*.
    """
    bsb = Path(__file__).resolve().parents[1] / "bin" / "snapshot-build-site.py"
    assert "def write_frontmatter" not in bsb.read_text(), (
        "snapshot-build-site.py has re-grown its own serializer (goal:s14)")

    bspec = importlib.util.spec_from_file_location("snapshot_build_site", bsb)
    bs = importlib.util.module_from_spec(bspec)
    bspec.loader.exec_module(bs)
    defined_in = Path(bs.write_frontmatter.__code__.co_filename).name
    assert defined_in == "snapshot-goals.py", defined_in


def test_strip_thought_removes_the_block():
    body = f"real prose\n\n{sg.THOUGHT_BEGIN}\nreasoning\n{sg.THOUGHT_END}"
    out = sg.strip_thought(body)
    assert out == "real prose"
    assert "reasoning" not in out


def test_strip_thought_is_a_noop_without_one():
    assert sg.strip_thought("just prose") == "just prose"
    assert sg.strip_thought("") == ""


def test_render_strips_thought_but_the_node_keeps_it():
    """goal:g2.11 — thought is provenance to zoom into, not weight every reader
    carries. The asymmetry (node keeps, renderer strips) is the point."""
    goals = [{"gid": "G1", "title": "T", "status": "active", "order": 0,
              "heading_level": 2,
              "body": f"argument\n\n{sg.THOUGHT_BEGIN}\nSECRET\n{sg.THOUGHT_END}"}]
    out = sg.render_goals("preamble", goals)
    assert "argument" in out
    assert "SECRET" not in out


def test_render_check_round_trip_survives_a_thought():
    """The trap g2.11 names: --check compares render output against a GOALS.md
    that render itself wrote, so both sides are stripped and the round trip
    stays byte-identical. Rendering twice must be a fixed point."""
    goals = [{"gid": "G1", "title": "T", "status": "active", "order": 0,
              "heading_level": 2,
              "body": f"argument\n\n{sg.THOUGHT_BEGIN}\nSECRET\n{sg.THOUGHT_END}"}]
    first = sg.render_goals("preamble", goals)
    assert sg.render_goals("preamble", goals) == first


def test_post_wire_does_not_define_its_own_serializer():
    """goal:s14, third copy. The sweep that de-duplicated `write_frontmatter`
    missed post_wire.py, which kept a private `yaml.dump` until 2026-09-01 --
    so every node it wired was round-tripped into a different YAML style than
    the corpus (list indent lost, `id:` unquoted, `title:` re-quoted, a stray
    blank line). The grid records a version per changed node, so wiring one
    edge minted versions whose content was quote style."""
    pw = Path(__file__).resolve().parents[1] / "bin" / "post_wire.py"
    text = pw.read_text()
    assert "def write_frontmatter" not in text, (
        "post_wire.py has re-grown its own serializer (goal:s14)")
    assert "yaml.dump" not in text, (
        "post_wire.py is serializing frontmatter itself again (goal:s14)")

    spec = importlib.util.spec_from_file_location("agi_post_wire", pw)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    defined_in = Path(mod.write_frontmatter.__code__.co_filename).name
    assert defined_in == "snapshot-goals.py", defined_in


# ------------------------------------- goal_kind: perpetual (hypothesis
# l3w1-goal-kind-perpetual, L3 wave 1) ------------------------------------


def _rebase_goal(project: Path, node_id: str, old: str, new: str) -> None:
    node = goal_nodes(project)[node_id][0]
    node.write_text(node.read_text(encoding="utf-8").replace(old, new),
                    encoding="utf-8")


def test_render_goals_puts_perpetual_under_its_own_section():
    """A `goal_kind: perpetual` goal renders last, under a `## Perpetual`
    section, nested one level, and carries NO `— status:` lifecycle column —
    while legacy `long-term` goals render exactly as before."""
    goals = [
        {"gid": "G1", "title": "Long term thing", "status": "active",
         "heading_level": 2, "goal_kind": "perpetual", "body": "Long body."},
        {"gid": "G2", "title": "Second long term", "status": "horizon",
         "heading_level": 2, "goal_kind": "long-term", "body": "Second body."},
    ]
    out = sg.render_goals("pre", goals)
    assert "## Perpetual" in out
    assert "### G1 — Long term thing" in out           # nested under `## Perpetual`
    assert "## G2 — Second long term — status: horizon" in out   # legacy unchanged
    assert "— status:" not in out.split("## Perpetual", 1)[1]     # no lifecycle column
    assert out.index("## Perpetual") > out.index("## G2")         # rendered last


def test_perpetual_goal_round_trips_via_render(nested):
    """nodes -> GOALS.md for a perpetual goal: the Perpetual section appears,
    renders under it, and `--render --check` stays byte-identical on re-run."""
    assert run(nested).returncode == 0               # import doc -> nodes
    _rebase_goal(nested, "goal:g1", "goal_kind: long-term",
                 "goal_kind: perpetual")
    assert fm_of(goal_nodes(nested)["goal:g1"][0])["goal_kind"] == "perpetual"
    assert run(nested, "--render").returncode == 0
    assert run(nested, "--render", "--check").returncode == 0
    rendered = (nested / "GOALS.md").read_text(encoding="utf-8")
    assert "## Perpetual" in rendered
    assert "### G1 — Long term thing" in rendered
    assert "— status:" not in rendered.split("## Perpetual", 1)[1]
    assert "## G2 — Second long term — status: horizon" in rendered


def test_from_doc_round_trip_keeps_a_perpetual_goal_perpetual(nested):
    """After a doc -> nodes import of a doc with a Perpetual section, the
    perpetual goal's node still carries `goal_kind: perpetual`, and a fresh
    render reproduces the Perpetual section."""
    assert run(nested).returncode == 0
    _rebase_goal(nested, "goal:g1", "goal_kind: long-term",
                 "goal_kind: perpetual")
    # render the doc (nodes -> GOALS.md), then re-import it (doc -> nodes)
    assert run(nested, "--render").returncode == 0
    assert run(nested).returncode == 0                # --from-doc import
    assert fm_of(goal_nodes(nested)["goal:g1"][0])["goal_kind"] == "perpetual"
    assert run(nested, "--render", "--check").returncode == 0


def test_goal_schema_accepts_perpetual_and_legacy_long_term():
    """The `[goal].md` schema's goal_kind regex accepts both `perpetual`
    (canonical) and `long-term` (legacy, accepted forever like `phasing-out`),
    and both resolve as spawn variants."""
    import re as _re
    schema = Path(__file__).resolve().parents[3] / ".agi" / "context" \
        / "schemas" / "[goal].md"
    text = schema.read_text(encoding="utf-8")
    m = _re.search(r"goal_kind:\s*'(\^[^']+)'", text)
    assert m, "[goal].md goal_kind regex not found"
    rx = _re.compile(m.group(1))
    assert rx.match("perpetual")
    assert rx.match("long-term")
    assert not rx.match("bogus")
    # spawn: block declares a perpetual variant
    assert "perpetual:" in text and "long-term:" in text


# --- hypothesis l4-a-check-that-cries-wolf-gets-waved-through -----------------
# The `--check` false alarm: GOALS.md (a derived artefact) compared against
# goal nodes (its sources) that a concurrent writer can move under the
# comparison. The guard must retry exactly ONCE, report the retry visibly,
# and preserve fail-closed. These tests are NEW — no existing test is edited.

def test_concurrent_source_write_triggers_a_reported_retry(project, monkeypatch, capsys):
    """(a) A source that changes DURING the comparison produces exactly one
    retry, and the retry is REPORTED — asserted on the retry text, not merely
    on the exit code (which is 0 here: the transient race resolves)."""
    run(project)                                   # clean import: doc -> nodes
    assert run(project, "--render").returncode == 0
    path = next((project / "nodes" / "goal").glob("g1-*.md"))
    fm = fm_of(path)
    orig_body = path.read_text(encoding="utf-8").split("---", 2)[2].strip()
    first = {"ran": False}

    def patched(rendered, n_goals):
        if not first["ran"]:
            first["ran"] = True
            # the concurrent write, landed right at the comparison: the node
            # moves AND GOALS.md follows it, so the retry's fresh pass is green
            sg.write_frontmatter(path, fm, orig_body + "\n\n(mutated mid-check)",
                                 preserve_body=orig_body)
            new_doc = sg.render_goals(
                *sg.load_goal_nodes(sg.load_existing_nodes()))
            (project / "GOALS.md").write_text(new_doc, encoding="utf-8")
        return real(rendered, n_goals)

    real = sg._compare_rendered
    monkeypatch.setattr(sg, "_compare_rendered", patched)
    rc = sg.main(["--project", str(project), "--render", "--check"])
    err = capsys.readouterr().err
    assert rc == 0                                  # race resolved cleanly
    assert "changed during comparison" in err, err  # the retry is VISIBLE
    assert "retrying ONCE" in err, err


def test_genuine_divergence_still_fails_on_the_first_comparison(project):
    """(b) Sources stable, artefact wrong: the check FAILS on the FIRST
    comparison and never touches the retry path — a real defect is not masked."""
    run(project)
    assert run(project, "--render").returncode == 0
    doc = project / "GOALS.md"
    doc.write_text(doc.read_text(encoding="utf-8") + "\nSTRAY DEFECT\n",
                   encoding="utf-8")
    r = run(project, "--render", "--check")
    assert r.returncode == 1
    assert "MISMATCH" in r.stderr
    assert "retrying" not in r.stderr, "a no-race divergence must not retry"


def test_race_cannot_launder_a_real_defect(project, monkeypatch, capsys):
    """(c) A genuine divergence that ALSO races still fails AFTER the retry,
    so the race path cannot hide a definite, hand-broken artefact."""
    run(project)
    assert run(project, "--render").returncode == 0
    doc = project / "GOALS.md"
    doc.write_text(doc.read_text(encoding="utf-8") + "\nHAND-BROKEN DEFECT\n",
                   encoding="utf-8")
    path = next((project / "nodes" / "goal").glob("g1-*.md"))
    fm = fm_of(path)
    orig_body = path.read_text(encoding="utf-8").split("---", 2)[2].strip()
    first = {"n": 0}

    def patched(rendered, n_goals):
        if first["n"] == 0:
            first["n"] = 1
            # racing source move, but GOALS.md is NOT made consistent -> the
            # defect must survive the retry
            sg.write_frontmatter(path, fm, orig_body + "\n\n(racing node)",
                                 preserve_body=orig_body)
        return real(rendered, n_goals)

    real = sg._compare_rendered
    monkeypatch.setattr(sg, "_compare_rendered", patched)
    rc = sg.main(["--project", str(project), "--render", "--check"])
    err = capsys.readouterr().err
    assert rc == 1                                  # defect NOT laundered
    assert "retrying ONCE" in err, err              # the race was seen+retried
    assert "MISMATCH" in err, err                   # and it still failed


def test_no_change_case_is_unaffected_and_costs_one_comparison(project, monkeypatch, capsys):
    """(d) The no-change case is unaffected and costs no extra render: exit 0,
    no retry message, and exactly ONE comparison (a retry would re-render and
    call _compare_rendered a second time)."""
    run(project)
    assert run(project, "--render").returncode == 0
    calls = {"n": 0}

    def patched(rendered, n_goals):
        calls["n"] += 1
        return real(rendered, n_goals)

    real = sg._compare_rendered
    monkeypatch.setattr(sg, "_compare_rendered", patched)
    rc = sg.main(["--project", str(project), "--render", "--check"])
    err = capsys.readouterr().err
    assert rc == 0
    assert "retrying" not in err
    assert calls["n"] == 1, calls["n"]   # no second comparison, no extra render
