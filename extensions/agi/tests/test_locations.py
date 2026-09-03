"""Tests for bin/locations.py — the one path resolver (goal:g11).

The value of this file is mostly in the *layout* fixtures rather than the
assertions: every one of them is a shape the engine has to survive during the
G11 migration, including the half-migrated ones that only exist for a few
commits and are exactly where a resolver goes wrong.
"""
from __future__ import annotations

import importlib.util
import json
import os
import re
import subprocess
import sys
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parents[1] / "bin"
LIB = Path(__file__).resolve().parents[1] / "lib"
sys.path.insert(0, str(BIN))

import locations  # noqa: E402


# --- fixtures --------------------------------------------------------------


def make_legacy(root: Path, name: str = "agi-tree.config.json", **cfg) -> Path:
    """The layout that exists today: the tree IS the project root."""
    root.mkdir(parents=True, exist_ok=True)
    (root / name).write_text(json.dumps(cfg or {"metric_primary": "outcome_coverage"}))
    (root / "nodes").mkdir(exist_ok=True)
    return root


def make_graph_dir(repo: Path, name: str = "config.json", **cfg) -> Path:
    """The goal:g11 layout: `<repo>/.agi/` beside the source it describes."""
    graph = repo / ".agi"
    graph.mkdir(parents=True, exist_ok=True)
    (graph / name).write_text(json.dumps(cfg or {"metric_primary": "outcome_coverage"}))
    (graph / "nodes").mkdir(exist_ok=True)
    return graph


# --- phase 1: the legacy layout still resolves -----------------------------


def test_legacy_root_from_subdir(tmp_path):
    root = make_legacy(tmp_path / "proj")
    deep = root / "nodes" / "goal"
    deep.mkdir(parents=True)
    assert locations.find_project_root(deep) == root


def test_legacy_name_still_accepted(tmp_path):
    root = make_legacy(tmp_path / "proj", name="autoresearch-tree.config.json")
    assert locations.find_project_root(root) == root


def test_canonical_wins_when_both_names_present(tmp_path):
    root = make_legacy(tmp_path / "proj")
    (root / "autoresearch-tree.config.json").write_text("{}")
    assert locations.config_path(root).name == "agi-tree.config.json"


def test_no_project_returns_none(tmp_path):
    (tmp_path / "empty").mkdir()
    assert locations.find_project_root(tmp_path / "empty") is None


# --- phase 0: the G11 layout -----------------------------------------------


def test_graph_dir_resolves_to_the_dot_agi_itself(tmp_path):
    repo = tmp_path / "fantasia"
    graph = make_graph_dir(repo)
    assert locations.find_project_root(repo) == graph
    assert locations.is_graph_dir(graph)
    assert locations.repo_root(graph) == repo


def test_graph_dir_found_walking_up_from_source(tmp_path):
    repo = tmp_path / "fantasia"
    graph = make_graph_dir(repo)
    deep = repo / "src" / "engine" / "render"
    deep.mkdir(parents=True)
    assert locations.find_project_root(deep) == graph


def test_bare_config_json_is_a_marker_only_inside_dot_agi(tmp_path):
    """A stray config.json must never make an ordinary repo look like a graph."""
    plain = tmp_path / "someone-elses-repo"
    plain.mkdir()
    (plain / "config.json").write_text("{}")
    assert locations.config_path(plain) is None
    assert locations.find_project_root(plain) is None


def test_dot_agi_without_a_config_is_not_a_project(tmp_path):
    repo = tmp_path / "repo"
    (repo / ".agi").mkdir(parents=True)
    assert locations.find_project_root(repo) is None


# --- the case the interleaved walk exists for ------------------------------


def test_nearest_enclosing_wins_between_two_graphs(tmp_path):
    """A project checkout carries two graphs: its own and the engine clone's.

    Neither needs a flag — the answer falls out of where you are standing,
    which is what keeps goal:g8.2's "the engine never knows which project it
    is running" true under G11.
    """
    repo = tmp_path / "fantasia"
    outer = make_graph_dir(repo)
    inner = make_graph_dir(repo / "agi")

    assert locations.find_project_root(repo) == outer
    assert locations.find_project_root(repo / "agi") == inner
    assert locations.find_project_root(repo / "agi" / "extensions") == inner


def test_graph_dir_beats_legacy_marker_in_the_same_directory(tmp_path):
    """Half-migrated: both markers present. The new layout wins."""
    repo = tmp_path / "proj"
    make_legacy(repo)
    graph = make_graph_dir(repo)
    assert locations.find_project_root(repo) == graph


def test_near_legacy_beats_distant_graph_dir(tmp_path):
    """The regression the single interleaved walk prevents.

    Two separate walks — all of phase 0, then all of phase 1 — would return the
    distant `.agi/` here, inverting "nearest enclosing wins" at exactly the
    moment a repo is half migrated.
    """
    outer = tmp_path / "outer"
    make_graph_dir(outer)
    inner = make_legacy(outer / "sub" / "proj")
    assert locations.find_project_root(inner) == inner


# --- phase 2: descend ------------------------------------------------------


def test_descend_prefers_basename_match(tmp_path):
    start = tmp_path / "fantasia"
    start.mkdir()
    tree = make_legacy(start / "fantasia-tree")
    make_legacy(start / "other-tree")
    assert locations.find_project_root(start) == tree


def test_descend_ambiguous_returns_none(tmp_path):
    start = tmp_path / "work"
    start.mkdir()
    make_legacy(start / "a-tree")
    make_legacy(start / "b-tree")
    assert locations.find_project_root(start) is None


def test_descend_skips_a_tree_dir_with_no_config(tmp_path):
    start = tmp_path / "work"
    start.mkdir()
    (start / "decoy-tree").mkdir()
    tree = make_legacy(start / "real-tree")
    assert locations.find_project_root(start) == tree


# --- source_root -----------------------------------------------------------


def test_source_root_defaults_to_repo_under_graph_dir_layout(tmp_path):
    repo = tmp_path / "fantasia"
    graph = make_graph_dir(repo)
    assert locations.source_root(graph) == repo


def test_source_root_defaults_to_engine_beside_a_legacy_tree(tmp_path):
    """Today's `agi-tree/agi` symlink and `fantasia/agi` clone, unchanged."""
    root = make_legacy(tmp_path / "proj")
    engine = root / "agi"
    engine.mkdir()
    assert locations.source_root(root) == engine


def test_source_root_falls_back_to_the_graph_root(tmp_path):
    root = make_legacy(tmp_path / "proj")
    assert locations.source_root(root) == root


def test_source_root_relative_is_resolved_against_the_graph_root(tmp_path):
    """The 'run against a custom source location' dial.

    Relative means relative to the *graph* root, which is what makes `".."` the
    natural spelling of "the repo I live in" and `"../vendor"` the natural
    spelling of a sibling of the graph directory.
    """
    repo = tmp_path / "repo"
    (repo / "vendor").mkdir(parents=True)
    graph = make_graph_dir(repo, locations={"source_root": ".."})
    assert locations.source_root(graph) == repo

    graph2 = make_graph_dir(repo, locations={"source_root": "../vendor"})
    assert locations.source_root(graph2) == repo / "vendor"


def test_source_root_can_climb_out_of_the_repo(tmp_path):
    repo = tmp_path / "repo"
    target = tmp_path / "elsewhere"
    target.mkdir()
    graph = make_graph_dir(repo, locations={"source_root": "../../elsewhere"})
    assert locations.source_root(graph) == target


def test_source_root_explicit_absolute_override(tmp_path):
    target = tmp_path / "somewhere-else"
    target.mkdir()
    root = make_legacy(tmp_path / "proj", locations={"source_root": str(target)})
    assert locations.source_root(root) == target


def test_source_root_override_beats_the_layout_default(tmp_path):
    repo = tmp_path / "repo"
    (repo / "vendor").mkdir(parents=True)
    graph = make_graph_dir(repo, locations={"source_root": "../vendor"})
    assert locations.source_root(graph) == repo / "vendor"


# --- goals_path ------------------------------------------------------------


def test_goals_render_to_the_repo_root_not_inside_dot_agi(tmp_path):
    """The reason `goals_path` exists at all."""
    repo = tmp_path / "fantasia"
    graph = make_graph_dir(repo)
    assert locations.goals_path(graph) == repo / "GOALS.md"


def test_goals_stay_at_the_graph_root_under_the_legacy_layout(tmp_path):
    root = make_legacy(tmp_path / "proj")
    assert locations.goals_path(root) == root / "GOALS.md"


def test_goals_file_override_resolves_the_dropin_collision(tmp_path):
    """A repo that already ships its own GOALS.md keeps both documents."""
    repo = tmp_path / "fantasia"
    graph = make_graph_dir(repo, goals_file="AGI-GOALS.md")
    assert locations.goals_path(graph) == repo / "AGI-GOALS.md"
    assert locations.goals_path(graph).name != "GOALS.md"


def test_goals_file_with_a_separator_is_relative_to_the_graph_root(tmp_path):
    repo = tmp_path / "repo"
    graph = make_graph_dir(repo, goals_file="docs/GOALS.md")
    assert locations.goals_path(graph) == graph / "docs" / "GOALS.md"


def test_goals_file_absolute_is_used_as_is(tmp_path):
    target = tmp_path / "anywhere" / "G.md"
    root = make_legacy(tmp_path / "proj", goals_file=str(target))
    assert locations.goals_path(root) == target


def test_blank_goals_file_falls_back_to_the_default(tmp_path):
    root = make_legacy(tmp_path / "proj", goals_file="   ")
    assert locations.goals_path(root) == root / "GOALS.md"


# --- config loading --------------------------------------------------------


def test_malformed_config_does_not_raise(tmp_path):
    """Half the engine imports this at module scope; it must not die on import."""
    root = tmp_path / "proj"
    root.mkdir()
    (root / "agi-tree.config.json").write_text("{ this is not json")
    assert locations.load_config(root) == {}
    assert locations.find_project_root(root) == root


def test_non_dict_config_is_treated_as_empty(tmp_path):
    root = tmp_path / "proj"
    root.mkdir()
    (root / "agi-tree.config.json").write_text("[1, 2, 3]")
    assert locations.load_config(root) == {}


def test_missing_config_loads_as_empty(tmp_path):
    assert locations.load_config(tmp_path) == {}


# --- env override ----------------------------------------------------------


def test_env_override_wins(tmp_path, monkeypatch):
    root = make_legacy(tmp_path / "proj")
    other = make_legacy(tmp_path / "other")
    monkeypatch.setenv("AGI_TREE_PROJECT_ROOT", str(other))
    assert locations.project_root_from_env(root) == other


def test_legacy_env_spelling_still_read(tmp_path, monkeypatch):
    other = make_legacy(tmp_path / "other")
    monkeypatch.delenv("AGI_TREE_PROJECT_ROOT", raising=False)
    monkeypatch.setenv("AUTORESEARCH_TREE_PROJECT_ROOT", str(other))
    assert locations.project_root_from_env(tmp_path) == other


# --- the two halves agree --------------------------------------------------


def _bash_find_root(start: Path) -> str | None:
    res = subprocess.run(
        ["bash", str(LIB / "find-root.sh"), str(start)],
        capture_output=True, text=True,
    )
    return res.stdout.strip() if res.returncode == 0 else None


@pytest.mark.parametrize("shape", ["legacy", "graph_dir", "nested", "half_migrated",
                                   "descend", "ambiguous", "none"])
def test_bash_and_python_agree(tmp_path, shape):
    """lib/find-root.sh and bin/locations.py implement ONE rule, twice.

    Written as a parametrized cross-check rather than as duplicated assertions
    because the failure this guards against is drift, and drift shows up as
    exactly one shape disagreeing while the rest still pass.
    """
    if shape == "legacy":
        start = make_legacy(tmp_path / "proj")
        expected = start
    elif shape == "graph_dir":
        repo = tmp_path / "repo"
        expected = make_graph_dir(repo)
        start = repo
    elif shape == "nested":
        repo = tmp_path / "fantasia"
        make_graph_dir(repo)
        expected = make_graph_dir(repo / "agi")
        start = repo / "agi"
    elif shape == "half_migrated":
        repo = tmp_path / "proj"
        make_legacy(repo)
        expected = make_graph_dir(repo)
        start = repo
    elif shape == "descend":
        start = tmp_path / "fantasia"
        start.mkdir()
        expected = make_legacy(start / "fantasia-tree")
    elif shape == "ambiguous":
        start = tmp_path / "work"
        start.mkdir()
        make_legacy(start / "a-tree")
        make_legacy(start / "b-tree")
        expected = None
    else:
        start = tmp_path / "empty"
        start.mkdir()
        expected = None

    py = locations.find_project_root(start)
    sh = _bash_find_root(start)

    assert (str(py) if py else None) == (str(expected) if expected else None)
    assert sh == (str(expected) if expected else None), (
        f"bash and python disagree on shape={shape}: bash={sh!r} python={py!r}"
    )


# --- relative start paths --------------------------------------------------
#
# The bash half walked up with `d="$(dirname "$d")"` on whatever it was given.
# `dirname .` is `.`, so a relative argument made `d` stop changing while the
# loop waited for it to reach `/`: an infinite spin, no output, 100% CPU, until
# killed. It survived because every live caller passes `$PWD`, so triggering it
# needs a relative argument AND no project above the cwd. Timeouts below are the
# assertion — a regression hangs rather than fails.


def _bash_find_root_in(cwd: Path, arg: str, timeout: int = 10):
    """Run the bash resolver with `arg`, from `cwd`. Returns (rc, stdout)."""
    res = subprocess.run(
        ["bash", str(LIB / "find-root.sh"), arg],
        capture_output=True, text=True, cwd=str(cwd), timeout=timeout,
    )
    return res.returncode, res.stdout.strip()


@pytest.mark.parametrize("arg", [".", "sub", "./sub", "nope"])
def test_relative_start_with_no_project_terminates(tmp_path, arg):
    """The regression test proper: these used to never return.

    `nope` does not exist and is included deliberately — it has to be made
    absolute too, or `dirname nope` is `.` and the loop is back.
    """
    (tmp_path / "sub").mkdir()
    rc, out = _bash_find_root_in(tmp_path, arg)
    assert rc == 1, f"expected a clean refusal for {arg!r}, got rc={rc} out={out!r}"


@pytest.mark.parametrize("arg", [".", "sub"])
def test_relative_start_resolves_to_an_absolute_root(tmp_path, arg):
    """And it must answer with an absolute path, not `./.agi` — every caller
    treats the result as a root it can hand to another process."""
    graph = make_graph_dir(tmp_path)
    (tmp_path / "sub").mkdir()
    rc, out = _bash_find_root_in(tmp_path, arg)
    assert rc == 0
    assert out == str(graph)
    assert Path(out).is_absolute()


@pytest.mark.parametrize("arg", [".", "sub", "nope"])
def test_relative_start_agrees_with_python(tmp_path, arg):
    """Same cross-check as `test_bash_and_python_agree`, on the input shape it
    never covered — it only ever passed absolute paths."""
    make_graph_dir(tmp_path)
    (tmp_path / "sub").mkdir()
    rc, out = _bash_find_root_in(tmp_path, arg)

    cwd = os.getcwd()
    try:
        os.chdir(tmp_path)
        py = locations.find_project_root(arg)
    finally:
        os.chdir(cwd)

    assert (out if rc == 0 else None) == (str(py) if py else None), (
        f"bash and python disagree on relative start {arg!r}"
    )


def test_symlinked_start_resolves_like_python(tmp_path):
    """`cd -P` must match `Path.resolve()`, or the two halves disagree for any
    project reached through a symlinked directory."""
    repo = tmp_path / "repo"
    graph = make_graph_dir(repo)
    link = tmp_path / "link"
    link.symlink_to(repo)
    assert _bash_find_root(link) == str(graph)
    assert str(locations.find_project_root(link)) == str(graph)


# --- cli -------------------------------------------------------------------


def test_cli_what_prints_one_path(tmp_path, capsys):
    repo = tmp_path / "fantasia"
    make_graph_dir(repo)
    assert locations.main([str(repo), "--what", "goals"]) == 0
    assert capsys.readouterr().out.strip() == str(repo / "GOALS.md")


def test_cli_json_reports_the_layout(tmp_path, capsys):
    repo = tmp_path / "fantasia"
    graph = make_graph_dir(repo)
    assert locations.main([str(repo), "--json"]) == 0
    data = json.loads(capsys.readouterr().out)
    assert data["layout"] == "graph_dir"
    assert data["root"] == str(graph)
    assert data["source"] == str(repo)


def test_cli_missing_project_exits_nonzero(tmp_path, capsys):
    (tmp_path / "empty").mkdir()
    assert locations.main([str(tmp_path / "empty")]) == 1
    assert "no agi project found" in capsys.readouterr().out


# --- every entry point calls this module, and only this module -------------
#
# goal:g11.1. `locations.py` existing did not collapse anything by itself: ten
# entry points under `bin/` kept their own copy of "walk up for
# agi-tree.config.json", and when goal:g11 moved the graph into `<repo>/.agi/`
# every one of those copies went wrong at once. The two tests below are the two
# halves of that failure — a structural one that catches a *new* copy being
# added, and a behavioural one that catches a copy that exists but disagrees.


#: Entry points that resolve a project root from the current directory. The
#: expression is carried as source, not as a callable, because these run in
#: separate processes: varying cwd is the whole point and cwd is process state.
CWD_RESOLVERS = {
    "benchmark.py": (
        # Refuses to load without `ollama`, which is not a test dependency. The
        # stub goes in before the import so the resolver is reachable at all.
        'sys.modules.setdefault("ollama", types.ModuleType("ollama"))\n'
        "import benchmark\n"
        "RESOLVED = benchmark._find_root()"
    ),
    "cli.py": "import cli\nRESOLVED = cli._find_root()",
    "metrics.py": "import metrics\nRESOLVED = metrics._find_root(Path.cwd())",
    "post_wire.py": "import post_wire\nRESOLVED = post_wire._find_root()",
    "spawn_gate.py": "import spawn_gate\nRESOLVED = spawn_gate._find_root()",
    # Hyphenated filenames are not importable; these expose the root as a
    # module-level PROJECT_ROOT instead of a function.
    # `render-context.py` was retired 2026-09-03 (L1.05); `inject.py` writes
    # the map now and is importable, so it exposes its resolution as a
    # function rather than a module-level constant.
    "inject.py": "import inject\nRESOLVED = inject.project_root()",
    "snapshot-build-site.py": '_m = _by_path("snapshot-build-site.py")\nRESOLVED = _m.PROJECT_ROOT',
    "snapshot-goals.py": '_m = _by_path("snapshot-goals.py")\nRESOLVED = _m.PROJECT_ROOT',
}

_PROBE = '''
import importlib.util, sys, types
from pathlib import Path
BIN = {bin_dir!r}
sys.path.insert(0, BIN)

def _by_path(fname):
    spec = importlib.util.spec_from_file_location("probe_" + fname, Path(BIN) / fname)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod

{body}
print(RESOLVED)
'''


def _resolve_in(entry: str, cwd: Path) -> str:
    """Run `entry`'s own resolver in a fresh process at `cwd`, return the root."""
    env = dict(os.environ)
    # The walk is what is under test; an inherited override would mask it.
    for var in locations.PROJECT_ROOT_ENV_VARS:
        env.pop(var, None)
    res = subprocess.run(
        [sys.executable, "-c",
         _PROBE.format(bin_dir=str(BIN), body=CWD_RESOLVERS[entry])],
        capture_output=True, text=True, cwd=str(cwd), env=env,
    )
    assert res.returncode == 0, f"{entry} failed at cwd={cwd}:\n{res.stderr}"
    return res.stdout.strip().splitlines()[-1]


def test_only_locations_declares_the_marker_names():
    """goal:g11.1's falsifier, as a test.

    Structural rather than behavioural on purpose: a newly added copy is
    harmless right up until the layout changes under it, so the thing worth
    catching is the copy appearing, not the day it finally disagrees.
    """
    offenders = sorted(
        p.name for p in BIN.glob("*.py")
        if p.name != "locations.py"
        and re.search(r"^CONFIG_NAMES\s*=", p.read_text(), re.MULTILINE)
    )
    assert offenders == [], (
        "these entry points declare their own copy of the marker names instead "
        f"of importing locations: {offenders}"
    )


@pytest.mark.parametrize("entry", sorted(CWD_RESOLVERS))
def test_entry_point_resolves_the_same_root_from_repo_and_graph_dir(entry, tmp_path):
    """One question, one answer, wherever you are standing.

    Under the goal:g11 layout the graph is `<repo>/.agi` and the repo root
    holds no config at all, so a resolver that only knows the legacy marker
    names either exits (`cli.py`, `metrics.py`, `spawn_gate.py`, `post_wire.py`,
    `benchmark.py`) or — worse — silently answers `os.getcwd()`
    (`inject.py`, `snapshot-build-site.py`). The second shape is the
    one that matters: it aims a generator at `<repo>/nodes` instead of
    `<repo>/.agi/nodes` with nothing raised, which is exactly how level3.py
    minted 3,098 files into its own input set the hour G11 landed.
    """
    repo = tmp_path / "repo"
    graph = make_graph_dir(repo)
    (repo / "src").mkdir()

    from_repo = _resolve_in(entry, repo)
    from_graph = _resolve_in(entry, graph)

    assert from_repo == from_graph == str(graph), (
        f"{entry} resolves differently depending on cwd: "
        f"from repo root {from_repo!r}, from .agi/ {from_graph!r}, "
        f"expected {str(graph)!r}"
    )


@pytest.mark.parametrize("entry", ["dispatch.py", "zoom.py"])
def test_root_taking_entry_points_share_the_config_lookup(entry):
    """`dispatch.py` and `zoom.py` take the root as an argument, not from cwd.

    Their copy of the rule lived in `config_path`, and its blind spot was the
    graph directory's bare `config.json` — so `zoom.py` rejected both the repo
    root and `.agi/` with "not a project root" and was unusable in this repo,
    while `default_runtime` fell through to `pi` and handed every Claude-Code
    kid the wrong completion contract (goal:s8, silently re-broken).
    """
    spec = importlib.util.spec_from_file_location("shared_cfg_" + entry, BIN / entry)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    assert mod.config_path is locations.config_path


def test_zoom_accepts_the_repo_root_and_the_graph_dir(tmp_path):
    """The confirmed live breakage, as a regression test.

    `zoom.py <repo>` is what `dispatch.py` and every human actually type; it
    returned "ERR: not a project root" for every directory in a migrated repo.
    Both spellings must now land on the same context file.
    """
    repo = tmp_path / "repo"
    graph = make_graph_dir(repo)
    (graph / "nodes" / "goal").mkdir(parents=True)
    (graph / "nodes" / "goal" / "g1.md").write_text(
        '---\nid: "goal:g1"\ntype: goal\nstatus: active\n'
        'title: "G1: a goal"\nparents: []\n---\n\nbody\n'
    )

    outs = []
    for start in (repo, graph):
        res = subprocess.run(
            [sys.executable, str(BIN / "zoom.py"), str(start), "1", "kid",
             "--level", "small", "--target", "goal:g1"],
            capture_output=True, text=True,
        )
        assert res.returncode == 0, f"zoom.py {start} failed:\n{res.stderr}"
        outs.append(res.stdout.strip().splitlines()[-1])

    assert outs[0] == outs[1] == str(graph / "sessions" / "iter-001" / "kid" / "context.md")
