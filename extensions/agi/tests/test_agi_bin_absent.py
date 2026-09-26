"""Regression: the <project-root>/bin/ shadow guard bites (goal:s4 / CLAUDE.md rule S1).

driver.sh prefers a project-local script over the engine's own copy
(the `SNAPSHOT_PY=` / `RENDER_PY=` sites in driver.sh):

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

import re
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
#: driver.sh itself, read as BYTES: the override set below is derived from it.
DRIVER = PLUGIN_ROOT / "driver.sh"
sys.path.insert(0, str(BIN))

import locations  # noqa: E402

#: A site of the form `$PROJECT_ROOT/bin/<name>` in driver.sh: that is the whole
#: override rule, written once. No line number anywhere -- those rot on edit.
_OVERRIDE_RE = re.compile(r"\$\{?PROJECT_ROOT\}?/(?:\./)?bin/([A-Za-z0-9_.-]+)")


def driver_override_scripts(driver: Path = DRIVER) -> tuple[str, ...]:
    """The <project-root>/bin/ names driver.sh prefers, read from its bytes.

    DERIVED, never retyped (`inject.py` and the retired `render-context.py` are
    both honoured at the RENDER_PY site). Rename a site in driver.sh and this
    set moves with it -- which is what test_override_set_moves_with_driver_bytes
    asserts on a doctored copy.
    """
    return tuple(dict.fromkeys(_OVERRIDE_RE.findall(driver.read_text())))


#: The scripts driver.sh will prefer from <project-root>/bin/ over the engine's own.
SHADOW_SCRIPTS = driver_override_scripts()


def guard(project_root: Path) -> None:
    """Refuse the DIRECTORY: ANY file under <project-root>/bin is a shadow.

    CLAUDE.md S1 forbids the directory, not a list of three names, so the
    guard cannot be walked around by planting `bin/other.py` (the mur refuter
    did exactly that). The message still names the override set driver.sh
    would prefer, so a reader knows what is at risk.
    """
    bin_dir = project_root / "bin"
    found = sorted(p.name for p in bin_dir.rglob("*") if p.is_file()) if bin_dir.is_dir() else []
    assert found == [], (
        "CLAUDE.md S1 forbids <project-root>/bin/ at all; found "
        + ", ".join(found)
        + ". driver.sh prefers a project-local copy over the engine's own for: "
        + ", ".join(driver_override_scripts())
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


def test_guard_is_red_on_a_file_that_is_not_an_override(tmp_path) -> None:
    """The mur refuter's move: plant bin/other.py, and the guard still bites."""
    project_root, _ = _fixture(tmp_path / "proj")
    guard(project_root)  # green: empty directory
    (project_root / "bin" / "other.py").write_text("# not an override name\n")
    with pytest.raises(AssertionError) as exc:
        guard(project_root)
    assert "other.py" in str(exc.value)


def test_override_set_moves_with_driver_bytes(tmp_path) -> None:
    """Derivation falsifier: drop a name from driver.sh, the set drops it."""
    doctored = tmp_path / "driver.sh"
    doctored.write_text(
        DRIVER.read_text().replace("$PROJECT_ROOT/bin/inject.py", '"$PLUGIN_ROOT/bin/inject.py"')
    )
    assert "inject.py" in driver_override_scripts(DRIVER)
    assert "inject.py" not in driver_override_scripts(doctored)
    assert set(driver_override_scripts(DRIVER)) >= set(driver_override_scripts(doctored))


def test_real_driver_override_set_is_not_empty() -> None:
    """The derivation must actually SEE driver.sh, not vacuously return ().

    Conjunct 1 (refuse the directory) holds even when the regex is blind, so
    an empty set was never caught: the message would name nothing.
    """
    real = driver_override_scripts(DRIVER)
    assert real, "the derived override set is empty -- the regex is blind to driver.sh"
    for name in real:
        # A bare file name, never a path fragment: the regex captures the tail.
        assert name and "/" not in name, f"derived a path, not a name: {name!r}"


def test_braced_and_dotted_override_sites_are_derived(tmp_path) -> None:
    """Blind spot closed: `${PROJECT_ROOT}/bin/x.py` and `$PROJECT_ROOT/./bin/x.py`.

    RED before the widening: the old `\\$PROJECT_ROOT/bin/` literal matched
    neither form, so a site written any other way was invisible to the guard's
    message while the directory refusal still held -- the message listed fewer
    names, or none, with nothing red anywhere.
    """
    for site in ("${PROJECT_ROOT}/bin/braced.py", "$PROJECT_ROOT/./bin/dotted.py"):
        doctored = tmp_path / "driver.sh"
        doctored.write_text(DRIVER.read_text() + f'\nSNAP="{site}"\n')
        assert "braced.py" in driver_override_scripts(doctored) or "dotted.py" in driver_override_scripts(doctored), (
            f"the derivation is blind to the site form {site!r}"
        )
        assert site.rsplit("/", 1)[1] in driver_override_scripts(doctored)


def test_no_driver_line_number_is_cited() -> None:
    """Line numbers rot on every driver.sh edit; the bytes are the citation."""
    assert not re.search(r"line[s]? \d+", Path(__file__).read_text(), re.I)
