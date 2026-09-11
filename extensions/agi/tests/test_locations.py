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


def test_env_override_naming_repo_root_descends_into_dot_agi(tmp_path, monkeypatch):
    """hypothesis:l4-env-root-override-descends-never-ascends — case (b).

    `dispatch.py --branch` exports the WORKTREE REPO root into the variable.
    That value names a directory holding `.agi/` with a config, so phase 0's
    rule applies and it must resolve to `<val>/.agi` — this is the dispatched-
    child sense that was previously unreadable.
    """
    repo = tmp_path / "repo"
    graph = make_graph_dir(repo)
    monkeypatch.setenv("AGI_TREE_PROJECT_ROOT", str(repo))
    assert locations.project_root_from_env(repo) == graph


def test_env_override_naming_graph_root_is_unchanged(tmp_path, monkeypatch):
    """hypothesis:l4-env-root-override-descends-never-ascends — case (c).

    `driver.sh` and the session hook export the GRAPH root, already
    `<repo>/.agi`. Naming a graph root must resolve to ITSELF — unchanged —
    or the two working producers regress.
    """
    repo = tmp_path / "repo"
    graph = make_graph_dir(repo)
    monkeypatch.setenv("AGI_TREE_PROJECT_ROOT", str(graph))
    assert locations.project_root_from_env(repo) == graph


def test_env_override_never_ascends_to_an_ancestor(tmp_path, monkeypatch):
    """hypothesis:l4-env-root-override-descends-never-ascends — case (d),
    the never-ascend property asserted directly.

    The override must not walk up. A directory that is neither a graph root
    nor a repo root holding `.agi/`, but whose ANCESTOR holds a config, is
    returned UNCHANGED — it must NOT resolve to that ancestor. An override
    that could ascend would silently defeat the purpose of the env var (a
    caller's explicit root is never overridden for a different project).
    """
    repo = tmp_path / "repo"
    make_legacy(repo)  # the ancestor holds a config (legacy marker)
    deep = repo / "src" / "deep" ; deep.mkdir(parents=True)
    monkeypatch.setenv("AGI_TREE_PROJECT_ROOT", str(deep))
    assert locations.project_root_from_env(repo) == deep


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


# --- dispatch env leak: AGI_LOOP spawn label must not break loop_label ----
# (hypothesis:l3-dispatch-env-leaks-into-tests) ------------------------------

def test_loop_label_ignores_dispatched_agi_loop_spawn_label(tmp_path, monkeypatch):
    """A dispatch spawn env (AGI_LOOP=hypothesis:x@s1) must not raise; it
    falls through to the config 'loop' key instead of crashing on the spawn
    environment."""
    graph = make_graph_dir(tmp_path / "repo", loop="L3")
    monkeypatch.setenv(
        "AGI_LOOP", "hypothesis:l3-dispatch-env-leaks-into-tests@s1")
    monkeypatch.delenv("AGI_TREE_PROJECT_ROOT", raising=False)
    assert locations.loop_label(graph, explicit=None) == "L3"


def test_loop_label_ignores_dispatched_agi_loop_without_config(tmp_path, monkeypatch):
    """No config loop? Still no crash: falls through to DEFAULT_LOOP."""
    graph = make_graph_dir(tmp_path / "repo")
    monkeypatch.setenv("AGI_LOOP", "hypothesis:x@s1")
    monkeypatch.delenv("AGI_TREE_PROJECT_ROOT", raising=False)
    assert locations.loop_label(graph, explicit=None) == locations.DEFAULT_LOOP


def test_loop_label_still_honours_a_real_agi_loop_label(tmp_path, monkeypatch):
    """A genuine bare loop label in AGI_LOOP is still honoured (conductor env)."""
    graph = make_graph_dir(tmp_path / "repo", loop="L3")
    monkeypatch.setenv("AGI_LOOP", "L3")
    monkeypatch.delenv("AGI_TREE_PROJECT_ROOT", raising=False)
    assert locations.loop_label(graph, explicit=None) == "L3"


def test_loop_label_still_raises_on_invalid_explicit_flag(tmp_path):
    """An invalid EXPLICIT flag is a programmer error — still raises."""
    graph = make_graph_dir(tmp_path / "repo")
    with pytest.raises(ValueError):
        locations.loop_label(graph, explicit="hypothesis:x@s1")


# ---------------------------------------------------------------------------
# Linked worktrees resolve shared state to the MAIN checkout (l3w4)
# ---------------------------------------------------------------------------
# `hypothesis:l3w4-parent-branch-merge-up`: a parent dispatched with `--branch`
# runs in its own git worktree, and its kids edit only that worktree. Shared
# state — the spawn budget, the comms root, the meter pins — must stay ONE
# directory across every worktree of a project, or the tree-wide concurrency
# bound silently splits per worktree. These resolve through
# `git rev-parse --git-common-dir` to the main checkout, never per-worktree.


def _git(cwd: Path, *args: str):
    subprocess.run(["git", "-C", str(cwd), *args], check=True,
                   capture_output=True, text=True)


def _make_project_repo(tmp_path: Path) -> Path:
    """A real git repo with a `.agi/` graph dir, on branch `master`."""
    repo = tmp_path / "main"
    repo.mkdir(parents=True)
    _git(repo, "init", "-b", "master")
    _git(repo, "config", "user.email", "t@t")
    _git(repo, "config", "user.name", "t")
    (repo / "README").write_text("x")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-m", "init")
    make_graph_dir(repo)
    return repo


def test_git_common_root_on_main_checkout_is_unchanged(tmp_path):
    """In the main checkout, the common root is the checkout itself."""
    repo = _make_project_repo(tmp_path)
    assert locations.git_common_root(repo) == repo.resolve()
    # A subpath inside the main checkout is unchanged too.
    assert locations.git_common_root(repo / ".agi" / "nodes") == repo.resolve()


def test_git_common_root_inside_linked_worktree_resolves_to_main(tmp_path):
    """A linked worktree's budget/comms/meter root is the MAIN checkout."""
    repo = _make_project_repo(tmp_path)
    wt = tmp_path / "wt"
    _git(repo, "worktree", "add", "-b", "loop/slug@s2", str(wt), "master")
    assert locations.git_common_root(wt) == repo.resolve()
    assert locations.git_common_root(wt / "sub" / "deep") == repo.resolve()


def test_git_common_root_is_identity_outside_a_git_repo(tmp_path):
    """No enclosing git repo: the root is returned unchanged."""
    d = tmp_path / "notgit"
    d.mkdir(parents=True)
    assert locations.git_common_root(d) == d.resolve()


def test_git_common_root_resolves_a_plain_dir_to_enclosing_repo(tmp_path):
    """A plain subdir with no .git of its own resolves to its repo's root."""
    other = _make_project_repo(tmp_path)
    leaf = other / "not_a_submodule"; leaf.mkdir()
    assert locations.git_common_root(leaf) == other.resolve()


def test_shared_project_root_is_identity_in_main_checkout(tmp_path):
    """A caller in the main checkout is unchanged (the usual non-branch case)."""
    repo = _make_project_repo(tmp_path)
    assert locations.shared_project_root(repo) == locations.find_project_root(repo)


def test_shared_project_root_resolves_main_graph_from_worktree(tmp_path):
    """A linked worktree's SHARED graph root is the main checkout's `.agi`.
    This is the primitive the `.env` lookup and any other main-only shared
    state resolve through (`hypothesis:l3w4-branch-shared-state`)."""
    repo = _make_project_repo(tmp_path)
    # `_make_project_repo` commits only README, so the graph dir is NOT in the
    # worktree yet -- real worktrees carry their committed `.agi` (the fork).
    _git(repo, "add", "-A")
    _git(repo, "commit", "-m", "add graph dir")
    wt = tmp_path / "wt"
    _git(repo, "worktree", "add", "-b", "loop/slug@s2", str(wt), "master")
    assert (wt / ".agi" / "config.json").is_file()  # the fork is checked out
    wt_graph = locations.find_project_root(wt)      # the fork a kid edits
    main_graph = locations.find_project_root(repo)  # the one shared body
    assert wt_graph != main_graph                   # the fork is real
    assert locations.shared_project_root(wt) == main_graph
    assert locations.shared_project_root(wt / "deep" / "sub") == main_graph


def test_shared_project_root_is_none_outside_a_project(tmp_path):
    """No project anywhere: None, like find_project_root."""
    d = tmp_path / "notgit"
    d.mkdir(parents=True)
    assert locations.shared_project_root(d) is None


def test_shared_sessions_dir_is_identity_in_main_checkout(tmp_path):
    """A non-worktree / non-git caller is unchanged (the usual case), and the
    graph-dir form (`root/.agi`) resolves under the graph, not doubled."""
    repo = _make_project_repo(tmp_path)
    _git(repo, "add", "-A")
    _git(repo, "commit", "-m", "add graph dir")
    graph = locations.find_project_root(repo)
    # A REPO-root caller still lands on the graph's sessions (not doubled).
    assert str(locations.shared_sessions_dir(repo)) == str(repo / ".agi" / "sessions")
    assert locations.shared_sessions_dir(graph) == locations.sessions_dir(graph)


def test_shared_sessions_dir_resolves_main_room_from_worktree(tmp_path):
    """FALSIFIER (g4): a linked worktree's SHARED sessions dir is the MAIN
    checkout's room, while the plain per-worktree `sessions_dir` keeps the
    fork (iteration output). `rotate._sessions_dir` delegates here, so one
    implementationare pins/mail/budget/stamp/rotation records all share."""
    repo = _make_project_repo(tmp_path)
    _git(repo, "add", "-A")
    _git(repo, "commit", "-m", "add graph dir")
    wt = tmp_path / "wt"
    _git(repo, "worktree", "add", "-b", "loop/slug@s2", str(wt), "master")
    wt_graph = locations.find_project_root(wt)
    main_graph = locations.find_project_root(repo)
    assert wt_graph != main_graph                       # the fork is real
    assert locations.shared_sessions_dir(wt_graph) == locations.shared_sessions_dir(main_graph)
    assert str(locations.shared_sessions_dir(wt_graph)) == str(main_graph / "sessions")
    # The per-worktree resolver honors the fork (iteration output stays local).
    assert str(locations.sessions_dir(wt_graph)) == str(wt_graph / "sessions")
    assert locations.sessions_dir(wt_graph) != locations.sessions_dir(main_graph)


# --- the lookup is bounded to the given root's own repository (l4-the- ---
# --- management-key-lookup-is-bounded-to-the-given-root) --------------
# A directory with `.git` is the boundary of the repo `start` is inside. An
# `.agi`/config found AT that level (a main checkout or a linked worktree that
# keeps its `.agi` beside its `.git`) is `start`'s own; anything ABOVE that
# boundary lives in a DIFFERENT (ancestral) repository and must never be
# climbed into. This is the primitive that makes a tmp dir under an unrelated
# nested fixture git repo resolve None instead of walking up to the outer
# project's key.


def test_find_project_root_never_crosses_a_git_boundary_into_an_ancestor(tmp_path):
    """A nested git repo with no `.agi` of its own must resolve None, not the
    OUTER project's graph -- the walk stops at the nested repo's `.git`."""
    outer = tmp_path / "project"
    outer.mkdir(parents=True)
    graph = make_graph_dir(outer)
    assert locations.find_project_root(outer) == graph  # sanity: outer findable
    # a real nested repo (no .agi) inside the outer project:
    nested = outer / "vendor" / "dep"
    nested.mkdir(parents=True)
    _git(nested, "init", "-b", "main")
    deep = nested / "sub" / "deep"
    deep.mkdir(parents=True)
    assert locations.find_project_root(deep) is None, (
        "must not cross the nested repo's `.git` boundary into the outer "
        "project's `.agi`")
    # its own repo root, still inside the nested repo, is also None (no .agi):
    assert locations.find_project_root(nested) is None


def test_find_project_root_own_repo_agi_beside_git_still_resolves(tmp_path):
    """A linked worktree whose `.agi` fork sits beside its `.git` still
    resolves its own fork -- the bound must not break worktree provisioning."""
    repo = _make_project_repo(tmp_path)
    _git(repo, "add", "-A")
    _git(repo, "commit", "-m", "add graph dir")
    wt = tmp_path / "wt"
    _git(repo, "worktree", "add", "-b", "loop/slug@s2", str(wt), "master")
    assert (wt / ".agi").is_dir()
    wt_graph = locations.find_project_root(wt)
    assert wt_graph is not None and wt_graph.parent == wt
    # a deep child of the worktree still reaches the fork (bounded to the
    # worktree's own repo, never crossing out):
    assert locations.find_project_root(wt / "deep" / "sub") == wt_graph
