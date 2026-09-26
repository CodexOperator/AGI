"""Regression: the <project-root>/bin/ shadow guard bites (goal:s4 / CLAUDE.md rule S1).

driver.sh prefers a project-local script over the engine's own copy
(`driver.sh:245-246,263-265`):

    SNAPSHOT_PY="$PLUGIN_ROOT/bin/snapshot-build-site.py"
    [[ -x "$PROJECT_ROOT/bin/snapshot-build-site.py" ]] && SNAPSHOT_PY="$PROJECT_ROOT/bin/snapshot-build-site.py"

`PROJECT_ROOT` is what `find_project_root` returns, which under the goal:g11
layout is the GRAPH DIRECTORY `<repo>/.agi` -- so the path that actually shadows
is `<repo>/.agi/bin/<script>.py`. The lone file that lived there
(analyze-chat-structure.py) has been re-homed to extensions/agi/bin/; a stale
shadow silently replaces an engine script and has wiped a node corpus once
(H0/H0b).

This file used to assert `find_project_root(...) / ".agi" / "bin"`, i.e.
`.agi/.agi/bin` -- a path no layout can produce, so the guard could never fail.
The path below is derived by SOURCING the engine's own lib/find-root.sh in a
fixture, never retyped, and the fixture test shows the guard going red on a
real shadow and green once it is gone.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

PLUGIN_ROOT = Path(__file__).resolve().parents[1]
BIN = PLUGIN_ROOT / "bin"
#: The fixture builder, SHIPPED beside this test (tests/fixtures/) so the guard
#: bites in a clean checkout: a fixture living in a per-round session scratch
#: dir is gone next round and 3 of these 4 tests die with ENOENT (measured,
#: experiment:a00-e4a74ff1-789283). It locates the engine from its own path,
#: so no env var and no absolute path is threaded through.
FIXTURE = Path(__file__).resolve().parent / "fixtures" / "make_shadow_fixture.sh"
sys.path.insert(0, str(BIN))

import locations  # noqa: E402

#: The scripts driver.sh will prefer from <project-root>/bin/ over the engine's
#: own. `inject.py` is included because driver.sh consults it at the same site
#: (line 264) -- `render-context.py` is the retired name it still honours.
SHADOW_SCRIPTS = ("snapshot-build-site.py", "render-context.py", "inject.py")


def shadow_scripts(project_root: Path) -> list[Path]:
    """The <project-root>/bin/ scripts that would shadow the engine's own."""
    return [
        p for p in (project_root / "bin" / n for n in SHADOW_SCRIPTS) if p.exists()
    ]


def guard(project_root: Path) -> None:
    """Refuse, by name, on any project-local copy driver.sh would prefer."""
    hits = shadow_scripts(project_root)
    assert hits == [], (
        "driver.sh prefers a project-local copy over the engine's own; remove "
        + ", ".join(str(p) for p in hits)
    )


def test_agi_bin_directory_does_not_exist() -> None:
    """No project-local shadow of an engine script exists in this project."""
    guard(locations.find_project_root(Path(__file__).resolve()))


def _fixture(project: Path, script: str = "") -> tuple[Path, str]:
    """Build the fixture and return (driver.sh's PROJECT_ROOT, bash stdout)."""
    res = subprocess.run(
        ["bash", str(FIXTURE), str(project), script],
        capture_output=True, text=True,
    )
    assert res.returncode == 0, f"fixture build failed:\n{res.stderr}"
    return Path(res.stdout.splitlines()[0]), res.stdout


def test_fixture_resolves_the_graph_dir_as_project_root(tmp_path) -> None:
    """The resolved root IS `<repo>/.agi`, which is why `.agi/.agi/bin` was dead."""
    project_root, _ = _fixture(tmp_path / "proj")
    assert project_root == tmp_path / "proj" / ".agi"
    assert (project_root / "bin").is_dir()


@pytest.mark.parametrize("script", ["snapshot-build-site.py", "render-context.py"])
def test_guard_is_red_on_a_shadow_and_green_once_it_is_gone(tmp_path, script) -> None:
    """The biting half: red on a fixture holding the shadow, green without it.

    Before the shadow exists the same guard is green, so the red below is the
    guard biting and not a fixture that is broken either way.
    """
    project_root, _ = _fixture(tmp_path / "proj")
    guard(project_root)  # green: no shadow yet

    _fixture(tmp_path / "proj", script)  # same fixture, shadow added
    with pytest.raises(AssertionError) as exc:
        guard(project_root)
    assert script in str(exc.value), "the refusal must name the offending script"

    (project_root / "bin" / script).unlink()
    guard(project_root)  # green again
