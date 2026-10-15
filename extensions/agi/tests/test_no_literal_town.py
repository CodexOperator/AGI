"""hypothesis:l4-towns-each-app-is-a-vision-with-its-own-council (goal:g8.2).

No engine code path may branch on a literal town NAME. A fork that says
`if town == "web-app-suite"` in an engine script has hardcoded a graph value
the ladder owns, and the moment the ladder adds a third app the fork silently
misses it. This test is the falsifier: it derives the town list from the
ladder (never hardcoding an app name), then scans every `bin/*.py` engine
script and fails on any string constant equal to a non-core town.

`core` is excluded on purpose: it is the *default denominator*, the reserved
value every reader falls back to (`vision_town_of` returns it, snapshot-goals
splits on `== "core"`, viewport hides it). Defaulting to core is the designed
behaviour; branching on an APP's name is the defect. The ladder may declare
`core` plus any number of app towns, and each non-core app town is exactly a
name no engine path may hardcode.

Comments and docstrings are excluded because the test walks the **AST**, and
Python's AST does not surface comments, and docstring `Expr`/`Constant` nodes
are skipped deliberately: a docstring that *mentions* an app name in prose is
fine (the hypothesis reference itself names the apps), a runnable literal is
not. Prose is not a code path.
"""
from __future__ import annotations

import ast
import sys
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parents[1] / "bin"

#: Import the shared ladder/frontmatter reader so the town list is DERIVED from
#: the ladder declaration, never copied from this file's line count.
sys.path.insert(0, str(BIN))
import spawn_gate  # noqa: E402
import locations  # noqa: E402


def _ladder_towns(project_root: Path) -> tuple[str, ...]:
    """Non-core town names the ladder declares, ordered and deduplicated.

    Reads `nodes/.geometry/ladder.md`'s `towns:` list through spawn_gate's
    frontmatter reader (the same one the ladder's operational readers use),
    so adding a town to the ladder extends this test's reach for free.
    """
    ladder = Path(locations.find_project_root(Path.cwd())) \
        / "nodes" / ".geometry" / "ladder.md"
    if not ladder.is_file():
        pytest.skip("no ladder node in this graph")
    fm = spawn_gate._read_frontmatter(ladder) or {}
    towns = [str(t).strip() for t in (fm.get("towns") or []) if str(t).strip()]
    return tuple(t for t in towns if t and t != "core")


def _skipped_docstring(node: ast.AST) -> bool:
    """True when `node` is the constant inside a module/class/function docstring.

    A docstring is a bare `Expr` whose value is a string constant at the head
    of a body; prose there is not a code path.
    """
    return (isinstance(node, ast.Expr)
            and isinstance(node.value, ast.Constant)
            and isinstance(node.value.value, str))


def _town_literals_in(src: str, ladder_towns: tuple[str, ...]) -> list[str]:
    """Every non-core town string that appears as a runnable literal in `src`."""
    tree = ast.parse(src, type_comments=True)
    found: list[str] = []
    parents: dict[int, ast.AST] = {}
    for n in ast.walk(tree):
        for child in ast.iter_child_nodes(n):
            parents[id(child)] = n
    for n in ast.walk(tree):
        if not isinstance(n, ast.Constant) or not isinstance(n.value, str):
            continue
        if n.value not in ladder_towns:
            continue
        # A docstring constant is prose; anything else in the AST is code.
        parent = parents.get(id(n))
        if isinstance(parent, ast.Expr):
            continue
        if n.value not in found:
            found.append(n.value)
    return found


@pytest.fixture(scope="session")
def ladder_towns():
    return _ladder_towns(Path.cwd())

def _engine_scripts() -> list[Path]:
    return [f for f in sorted(BIN.iterdir())
            if f.is_file() and f.name.endswith(".py")
            and not f.name.startswith("_") and f.name != "__init__.py"]


def test_no_engine_script_branches_on_a_literal_app_town_name(ladder_towns):
    """goal:g8.2 — no `bin/*.py` may hardcode an app town the ladder owns."""
    if not ladder_towns:
        pytest.skip("ladder declares no non-core towns; nothing to guard")
    offenders: list[str] = []
    for f in _engine_scripts():
        for town in _town_literals_in(f.read_text(encoding="utf-8"), ladder_towns):
            offenders.append(f"{f.name}: literal {town!r} in a runnable AST node")
    assert not offenders, (
        "engine code branches on a literal town NAME (goal:g8.2); derive the "
        "town from the graph through spawn_gate instead:\n" + "\n".join(offenders))