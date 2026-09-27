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
fixture, never retyped, and the fixture tests show the guard going red the
moment the directory exists -- bare, empty, or holding a shadow -- and green
only once the DIRECTORY is gone. CLAUDE.md S1 forbids the directory, so an
empty directory is a violation too, not a clean state.
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


def driver_override_scripts(driver: Path | None = None) -> tuple[str, ...]:
    """The <project-root>/bin/ names driver.sh prefers, read from its bytes.

    DERIVED, never retyped (`inject.py` and the retired `render-context.py` are
    both honoured at the RENDER_PY site). Rename a site in driver.sh and this
    set moves with it -- which is what test_override_set_moves_with_driver_bytes
    asserts on a doctored copy.

    `driver=None` resolves the module global DRIVER at CALL time. A default of
    `driver: Path = DRIVER` freezes the path into `__defaults__` at import, so
    rebinding DRIVER (a monkeypatch, a test harness, a relocated checkout) left
    the refusal message naming the OLD file's sites -- derivation that cannot
    be pointed at another file is half a derivation.
    """
    if driver is None:
        driver = DRIVER
    return tuple(dict.fromkeys(_OVERRIDE_RE.findall(driver.read_text())))


#: The OTHER engine entry points that carry the same override sites (measured
#: 2026-09-27, experiment:a00-7564eae7-402e7f): all three today, byte for byte.
#: Paths are relative to PLUGIN_ROOT, resolved at CALL time, never retyped.
_OVERRIDE_CARRIERS = (
    "hooks/cc-session-start.sh",
    "hooks/cc-session-start.next.sh",
)


#: A driver.sh line citation in ANY form: the prose one (the word "line" then
#: digits) and the path-colon-number one (a dot-sh name, a colon, digits -- see
#: the red-first case in the test below). Both rot on every edit to driver.sh.
_CITATION_RE = re.compile(r"line[s]?\s*\d+|\.sh:\d+", re.I)


def _driver_line_citations(text: str) -> tuple[str, ...]:
    """Every driver.sh line citation in `text`, in every citation form."""
    return tuple(m.group(0) for m in _CITATION_RE.finditer(text))


def guard(project_root: Path) -> None:
    """Refuse the DIRECTORY: if <project-root>/bin is a directory, S1 is broken.

    CLAUDE.md S1 forbids the directory, not a list of three names, so the
    guard cannot be walked around by planting `bin/other.py` (the mur refuter
    did exactly that) -- nor by leaving the directory bare and empty. The
    message states exactly what was checked, in this order: (a) the directory
    that exists, (b) the files found under it, `(empty)` when there are none,
    (c) the override set driver.sh would prefer, derived from driver.sh bytes
    at call time. A reader can tell WHICH check fired from the message alone.
    """
    bin_dir = project_root / "bin"
    if not bin_dir.is_dir():
        return
    found = sorted(p.name for p in bin_dir.rglob("*") if p.is_file())
    raise AssertionError(
        f"CLAUDE.md S1 forbids the directory {bin_dir} at all, and it is a directory. "
        "files found under it: " + (", ".join(found) if found else "(empty)") + ". "
        "driver.sh prefers a project-local copy over the engine's own for: "
        + ", ".join(driver_override_scripts())
    )


def test_agi_bin_directory_does_not_exist() -> None:
    """No project-local shadow of an engine script exists in this project.

    `find_project_root` returns `Path | None`, so `None / "bin"` would raise
    TypeError -- an unnamed failure that reads as a broken test, not as a
    missing project root. Refuse BY NAME instead.
    """
    start = Path(__file__).resolve()
    project_root = locations.find_project_root(start)
    if project_root is None:
        pytest.fail(
            f"no project root resolved from {start}: the guard would raise "
            "TypeError, not refuse the directory"
        )
    guard(project_root)


def test_missing_project_root_is_refused_by_name(monkeypatch) -> None:
    """The fail-closed None branch is EXERCISED, not only asserted in prose."""
    monkeypatch.setattr(locations, "find_project_root", lambda start: None)
    with pytest.raises(pytest.fail.Exception) as exc:
        test_agi_bin_directory_does_not_exist()
    assert "no project root" in str(exc.value), "the refusal must be named"


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
def test_guard_is_red_on_a_shadow_and_green_once_the_directory_is_gone(tmp_path, script) -> None:
    """The biting half: red the moment the directory exists, green without it.

    The fixture creates the directory on every call, so the red starts BARE --
    before any file is planted. Green therefore requires removing the
    directory itself, not just the shadow file.
    """
    project_root, _ = _fixture(tmp_path / "proj")
    with pytest.raises(AssertionError) as exc:
        guard(project_root)
    assert "files found under it: (empty)" in str(exc.value), "a bare directory is already the violation"

    _fixture(tmp_path / "proj", script)  # same fixture, shadow added
    with pytest.raises(AssertionError) as exc:
        guard(project_root)
    assert script in str(exc.value), "the refusal must name the offending script"

    (project_root / "bin" / script).unlink()
    with pytest.raises(AssertionError):
        guard(project_root)  # still red: the directory itself is forbidden
    (project_root / "bin").rmdir()
    guard(project_root)  # green again: the directory is gone


def test_guard_is_red_on_a_file_that_is_not_an_override(tmp_path) -> None:
    """The mur refuter's move: plant bin/other.py, and the guard still bites."""
    project_root, _ = _fixture(tmp_path / "proj")
    with pytest.raises(AssertionError) as exc:
        guard(project_root)  # red: the bare directory, before anything is planted
    assert str(project_root / "bin") in str(exc.value), "the refusal must name the directory"

    (project_root / "bin" / "other.py").write_text("# not an override name\n")
    with pytest.raises(AssertionError) as exc:
        guard(project_root)
    assert "other.py" in str(exc.value)


def test_bin_as_a_regular_file_is_green_and_the_words_say_directory(tmp_path) -> None:
    """Falsifier 1: a bin FILE cannot shadow a script, so it stays green.

    The check is `bin_dir.is_dir()`. S1 forbids the directory; a regular file
    named `bin` shadows nothing (driver.sh tests `bin/<script>.py`, and
    `<file>/x.py` is not a path), so green is CORRECT and `exists` in the
    docstring or the message was the real defect -- prose that overstates the
    check. RED before the wording fix: both texts still said "exists".
    """
    project_root = tmp_path / "proj"
    project_root.mkdir()
    (project_root / "bin").write_text("not a directory\n")
    assert not (project_root / "bin").is_dir()
    guard(project_root)  # green: nothing to shadow

    # ...and the refusal text, where a directory IS present, must say so.
    (project_root / "bin").unlink()
    (project_root / "bin").mkdir()
    with pytest.raises(AssertionError) as exc:
        guard(project_root)
    assert "is a directory" in str(exc.value)
    assert "exists" not in str(exc.value), "the message claims more than the check"
    docstring = guard.__doc__ or ""
    assert "is a directory" in docstring
    assert " if <project-root>/bin exists" not in docstring, (
        "the docstring still overstates the check it makes"
    )


def test_guard_message_follows_a_rebound_module_driver(monkeypatch, tmp_path) -> None:
    """Falsifier 2: the message derives from the CURRENT DRIVER, not import.

    RED before the fix: `driver: Path = DRIVER` binds the path into
    `__defaults__` at import, so rebinding the module global left the message
    naming the real driver.sh's sites.
    """
    patched = tmp_path / "driver.sh"
    patched.write_text(DRIVER.read_text() + '\nSNAP="$PROJECT_ROOT/bin/only-in-patch.py"\n')
    monkeypatch.setattr(sys.modules[__name__], "DRIVER", patched)
    assert "only-in-patch.py" in driver_override_scripts()

    project_root, _ = _fixture(tmp_path / "proj")
    with pytest.raises(AssertionError) as exc:
        guard(project_root)
    assert "only-in-patch.py" in str(exc.value), "the refusal ignored the rebound DRIVER"


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


def test_override_set_is_exactly_driver_sh_three_sites() -> None:
    """The PIN: the derived set is exactly driver.sh's three override SITES.

    NOT "the three names S1 names". CLAUDE.md S1, verbatim, is the first of
    "The two rules this project has already paid for":

        **NEVER create `.agi/bin/snapshot-build-site.py` or
        `.agi/bin/render-context.py`.**

    -- so S1 names TWO of the three, plus the ban on the directory itself
    ("Don't recreate a `bin/` directory there (S1)."). The third, `inject.py`,
    is the other half of driver.sh's `RENDER_PY` site (beside
    `render-context.py`); S1 never names it. The pinned SET of three is right;
    the WORDING of this test was the defect, and the wording of the guard
    message is not touched -- "CLAUDE.md S1 forbids the directory" is correct,
    because S1 does forbid the directory.

    A derivation that only ever grows (or shrinks) is unfalsifiable against the
    spec -- `test_override_set_moves_with_driver_bytes` proves it MOVES, not
    that it lands on the right three. An added site in driver.sh and a deleted
    one both go red here; the set is what the refusal message quotes.
    """
    assert set(driver_override_scripts()) == {
        "snapshot-build-site.py", "render-context.py", "inject.py",
    }


def test_override_sites_agree_across_every_engine_entry_point(tmp_path) -> None:
    """The message is only COMPLETE if the sites are the same everywhere.

    driver.sh is not the only file that prefers a project-local copy: the two
    cc-session-start hooks carry the same three sites. A fourth name added to a
    hook only would make the refusal message name one site fewer than the
    engine honours -- and the directory refusal still holds, so nothing else
    goes red. RED before this test: the set was pinned to driver.sh alone.
    """
    real = set(driver_override_scripts())
    for rel in _OVERRIDE_CARRIERS:
        assert set(driver_override_scripts(PLUGIN_ROOT / rel)) == real, (
            f"{rel} prefers a different project-local set than the message names"
        )

    doctored = tmp_path / "cc.sh"
    doctored.write_text(
        (PLUGIN_ROOT / _OVERRIDE_CARRIERS[0]).read_text()
        + '\n[[ -x "$PROJECT_ROOT/bin/fourth.py" ]] && X=1\n'
    )
    assert set(driver_override_scripts(doctored)) != real, "the scan cannot see a new site"


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
    """Line numbers rot on every driver.sh edit; the bytes are the citation.

    RED-FIRST, in the colon form the old prose-only scan was blind to: that
    string is BUILT here, never typed, because a literal of it in this file
    would make the scan below red on its own source.
    """
    colon_citation = "driver" + ".sh:" + "245-246"
    assert _driver_line_citations(colon_citation), "the citation scan is blind to the colon form"

    cited = _driver_line_citations(Path(__file__).read_text())
    assert not cited, f"this file cites a driver.sh line number: {cited}"
