"""Tests for bin/inject.py — what the generated map *teaches*.

Renamed from `test_render_context.py` on 2026-09-03 (L1.05) when
`render-context.py` was retired and `inject.py` took over writing
`INJECTION.md` from the viewport's frame stream. **The tests were
retargeted rather than deleted**: what the map teaches is a property of
the map, not of whichever renderer draws it, and a swap of producers is
exactly when that property is most likely to be lost quietly.

`context/INJECTION.md` is read by every agent in every session, so its wording
is engine behaviour, not documentation. It used to say "longest-chain attracts"
and lead with a `longest chain: N hops` headline — the exact target H3 proved
gameable (9 chains x 2000 hops via `hops=2*cycle+8`) and H0c showed to be what
broke the render path. `skills/agi/SKILL.md` says never to optimise chain
length; these tests keep the generated map saying the same thing.

Both injectors take only the first `INJECT_BUDGET` lines (hooks/
cc-session-start.sh `MAX_INJECT_LINES`, agi-bridge/index.ts `INJECTION_LINES`),
so "the map says the right thing" also means "it says it above that line".
"""

import subprocess
import sys
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parents[1] / "bin"
RENDER = BIN / "inject.py"

#: Lines the CC hook and the pi bridge each inject. Anything below is unread.
INJECT_BUDGET = 80


def _node(root, ntype, slug, parents=(), next_edges=()):
    d = root / "nodes" / ntype
    d.mkdir(parents=True, exist_ok=True)
    lines = ["---", f'id: "{ntype}:{slug}"', f"type: {ntype}",
             f'title: "{ntype} {slug}"']
    if parents:
        lines += ["parents:"] + [f"  - {p}" for p in parents]
    if next_edges:
        lines += ["next_edges:"] + [f"  - {n}" for n in next_edges]
    lines += ["---", "", "body", ""]
    (d / f"{slug}.md").write_text("\n".join(lines))


def _render(root) -> str:
    """Run the real entrypoint the way the hook does; return INJECTION.md."""
    proc = subprocess.run(
        [sys.executable, str(RENDER), str(root / "nodes")],
        cwd=root, capture_output=True, text=True,
        env={"PATH": "/usr/bin:/bin", "AGI_TREE_PROJECT_ROOT": str(root)},
    )
    assert proc.returncode == 0, proc.stderr
    return (root / "context" / "INJECTION.md").read_text()


@pytest.fixture()
def project(tmp_path):
    (tmp_path / "agi-tree.config.json").write_text(
        '{"metric_primary": "outcome_coverage"}')
    # Wide enough to fill the top-10 attractor list and push the ASCII block
    # past the injection budget — the shape that hid the old chain rules.
    for i in range(40):
        _node(tmp_path, "idea", f"i{i}", next_edges=[f"hypothesis:h{i}"])
        _node(tmp_path, "hypothesis", f"h{i}", parents=[f"idea:i{i}"])
        _node(tmp_path, "experiment", f"e{i}", parents=[f"hypothesis:h{i}"])
    return tmp_path


def test_chain_length_is_never_presented_as_a_target(project):
    text = _render(project).lower()
    assert "longest-chain attracts" not in text
    assert "chain length is never a target" in text
    # The stat may still be reported — under a heading that disclaims it.
    assert "## chain diagnostics (descriptive — not targets)" in text


def test_longest_chain_stat_sits_under_the_diagnostics_heading(project):
    lines = _render(project).splitlines()
    diagnostics = lines.index("## chain diagnostics (descriptive — not targets)")
    stat = next(i for i, ln in enumerate(lines) if ln.startswith("- longest chain:"))
    snapshot = lines.index("## graph snapshot")
    assert diagnostics < stat, "stat must be inside the diagnostics section"
    # ...and not in the headline block, which is the primary metric's slot.
    assert not any(ln.startswith("- longest chain:")
                   for ln in lines[snapshot:diagnostics])


def test_primary_metric_is_the_headline(project):
    lines = _render(project).splitlines()
    snapshot = lines.index("## graph snapshot")
    head = "\n".join(lines[snapshot:snapshot + 8])
    assert "scored on `outcome_coverage`" in head


def test_gameable_primary_is_flagged_not_endorsed(project):
    (project / "agi-tree.config.json").write_text(
        '{"metric_primary": "longest_chain_length"}')
    text = _render(project)
    assert "not a valid target" in text
    assert "score work on `outcome_coverage`" in text
    # Never advertise the gameable metric as the thing to move.
    assert "scored on `longest_chain_length`" not in text


def test_rules_survive_the_injection_budget(project):
    """The rules are worthless if the 80-line cut drops them (the old bug)."""
    lines = _render(project).splitlines()
    injected = "\n".join(lines[:INJECT_BUDGET])
    for heading in ("## chain diagnostics (descriptive — not targets)",
                    "## chain rules",
                    "## verdict taxonomy",
                    "## big-vs-small decision"):
        assert heading in injected, f"{heading} fell below line {INJECT_BUDGET}"

    # The rules must precede the tree, because both injectors truncate and a
    # rule below the cut is a rule nobody reads. The heading moved from
    # "## ASCII view" to "## the graph" when inject.py replaced the ASCII
    # renderer with the viewport's frame stream (L1.05); the ORDERING is the
    # property, and it is the reason briefing.to_markdown is prepended rather
    # than appended.
    tree_heading = next(h for h in lines if h.startswith("## the graph"))
    assert lines.index("## chain rules") < lines.index(tree_heading)


def test_evidence_gate_rule_is_stated(project):
    """SKILL.md's review gate: decisive verdicts need evidence."""
    text = _render(project)
    assert "evidence_runs >= 1" in text
