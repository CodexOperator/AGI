"""rotate.py first-decision — the POINT's captive harvest-or-cut
(step 4 of hypothesis:l4-the-window-reply-and-harvest-or-cut-are-captive-steps).

`first-decision --seat S` PRINTS, for each OPEN round of the seat's worktree:
the pre-filled harvest row (branch, parent, kids, verdicts, merge-base,
behind) and then EXACTLY ONE bounded prompt per row —
`harvest <round> | cut <next queued node> | hold`. It NEVER answers the
decision itself: `--answers FILE` replays the LLM's choices into the NAMED
next command per row — the git merge line carrying the EXACT branch name
from `git branch --list` for a harvest, the dispatch line for a cut —
PRINTED and NEVER RUN.

FALSIFIER (tested here): a step that RUNS the merge or the dispatch is
refused — there is no such code path; `first-decision` only reads git and
prints. The test asserts the fixture round branch still exists unmerged
after a `harvest` answer, i.e. nothing was executed.

Hermetic — a real git repo fixture (the same shape dispatch.py produces),
no tmux, no graph, no network.
"""
from __future__ import annotations

import subprocess
import sys
import os
from pathlib import Path
from types import SimpleNamespace

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from agi.bin import rotate  # noqa: E402


#: The fixture repos are FOREIGN git repos. The project's pre-commit guard
#: (hooks/agent-git) would otherwise read AGI_TIER/AGI_PROJECT_ROOT/GIT_*
#: inherited from this kid's own environment and refuse the fixture's own
#: commits. Scrub all of them so a fixture commit is raw git; the guard's
#: first gate (AGI_TIER unset => allow) exits 0 the moment they are gone.
_GIT_SCRUB = (
    "AGI_TIER", "AGI_PROJECT_ROOT", "AGI_AGENT_SESSIONS_ROOT",
    "GIT_DIR", "GIT_COMMON_DIR", "GIT_WORK_TREE",
)


def _git(cwd: Path, *args: str) -> subprocess.CompletedProcess:
    env = {k: v for k, v in os.environ.items() if k not in _GIT_SCRUB}
    env["GIT_OPTIONAL_LOCKS"] = "0"
    return subprocess.run(["git", "-C", str(cwd), *args],
                          capture_output=True, text=True, env=env)


def _seat_sessions(repo: Path) -> Path:
    """The seat worktree's own `.agi/sessions` dir — where the seat's dispatch
    writes iteration manifests. Resolved from the config:seats `worktree`
    field (`.agi/worktrees/seat-sanctuary-director`), the same path
    `_fd_seat_agent_ids` reads to build the manifest-join owned set."""
    return (repo / ".agi" / "worktrees" / "seat-sanctuary-director"
            / ".agi" / "sessions")


def _manifest_agent_ids(repo: Path) -> set[str]:
    """The agent ids currently recorded in the seat's iteration manifests
    (the live manifest shape: `manifest.json` `agents[].id` per iter)."""
    import json as _json
    ids: set[str] = set()
    for path in _seat_sessions(repo).glob("iter-*/manifest.json"):
        try:
            data = _json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        for a in data.get("agents") or []:
            if isinstance(a, dict) and a.get("id"):
                ids.add(str(a["id"]))
    return ids


def _manifest_add(repo: Path, agent_ids) -> None:
    """Record agent id(s) into the seat's iteration manifest, as the seat's
    dispatch does when it spawns a round. Reading the manifests back is the
    manifest-join evidence; a seat-owned round's agent MUST be here or the
    tool treats it as foreign."""
    import json as _json
    d = _seat_sessions(repo) / "iter-L4.1"
    d.mkdir(parents=True, exist_ok=True)
    path = d / "manifest.json"
    data = {"iter": "L4.1", "agents": []}
    if path.exists():
        try:
            data = _json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            data = {"iter": "L4.1", "agents": []}
    have = {a["id"] for a in data.get("agents") or [] if a.get("id")}
    agents = data.setdefault("agents", [])
    for aid in agent_ids:
        if aid not in have:
            agents.append({"id": aid})
    path.write_text(_json.dumps(data), encoding="utf-8")


def _make_repo(tmp_path: Path) -> tuple[Path, Path]:
    """Main checkout on `season/s2` with a committed `.agi/` graph dir, a
    `config:seats` row naming the seat's worktree, and a seat WORKTREE ON
    `seat/sanctuary-director@s2` cut from it and CHECKED OUT AT THE
    config-resolved `.agi/worktrees/seat-sanctuary-director` path. Returns
    (main, worktree)."""
    repo = tmp_path / "main"
    repo.mkdir(parents=True)
    _git(repo, "init", "-b", "master")
    _git(repo, "config", "user.email", "t@t")
    _git(repo, "config", "user.name", "t")
    (repo / "README").write_text("x\n")
    graph = repo / ".agi"
    (graph / "nodes" / ".geometry").mkdir(parents=True)
    (graph / "nodes" / "experiment").mkdir(parents=True)
    (graph / "config.json").write_text('{"metric_primary": "outcome_coverage"}')
    # one seat row: the point director, with its worktree field (the live
    # row shape, e.g. sanctuary-director's ".agi/worktrees/seat-sanctuary-director")
    import json as _json
    _row = {"name": "sanctuary-director", "role": "director",
            "worktree": ".agi/worktrees/seat-sanctuary-director",
            "pin_ref": "", "session_ref": "", "town": "all"}
    (graph / "nodes" / ".geometry" / "seats.md").write_text(
        "---\nid: config:seats\ntype: config\nseats:\n"
        "  - " + _json.dumps(_row) + "\n---\n", encoding="utf-8")
    # make sure the fixture repo is its own sink: no object dir that the real
    # main checkout could leak into (sessions dirs are gitignored like live)
    (repo / ".gitignore").write_text("sessions/\n.agi/sessions/\n",
                                     encoding="utf-8")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-m", "init with graph dir + seat row")
    _git(repo, "branch", "season/s2")
    _git(repo, "checkout", "-q", "season/s2")
    # seat branch + worktree, cut from season/s2, at the config-resolved path
    wt = repo / ".agi" / "worktrees" / "seat-sanctuary-director"
    _git(repo, "worktree", "add", "-b", "seat/sanctuary-director@s2",
         str(wt), "season/s2")
    # one EXCLUSIVE commit ON the seat branch so its lineage is distinguishable
    # from master/season: a sibseat round cut from a DIFFERENT branch must NOT
    # descend from it (without this, master == season/s2 == seat and the two
    # sides of the discriminator are the same branch).
    (wt / "SEAT-EXCLUSIVE").write_text("seat\n", encoding="utf-8")
    _git(wt, "add", "-A")
    _git(wt, "commit", "-m", "seat-exclusive commit")
    return repo, wt


def _make_round(repo: Path, wt: Path, slug: str, agent: str,
                node_id: str, verdict: str = "proved",
                base: str = "seat/sanctuary-director@s2",
                manifest: bool = True) -> str:
    """Cut one OPEN round branch `loop/<slug>-<agent>@s2` from `base` (the
    seat branch by default, or a DIFFERENT branch for a sibseat/foreign round),
    add a kid experiment node file on it, commit. When `manifest` is True the
    round's agent is recorded into the seat's iteration manifest exactly as
    the seat's dispatch would, making it a seat-OWN round under the
    manifest-join discriminator. Returns the branch name."""
    if manifest:
        _manifest_add(repo, [agent])
    branch = f"loop/{slug}-{agent}@s2"
    rwt = repo.parent / f"round-{agent}"
    _git(repo, "worktree", "add", "-b", branch, str(rwt), base)
    kid = rwt / ".agi" / "nodes" / "experiment" / f"{node_id}.md"
    kid.parent.mkdir(parents=True, exist_ok=True)
    fm = ("---\nid: experiment:" + node_id + "\ntype: experiment\n")
    if verdict:
        fm += "verdict: " + verdict + "\n"
    fm += "---\n\nround kid\n"
    kid.write_text(fm, encoding="utf-8")
    _git(rwt, "add", "-A")
    _git(rwt, "commit", "-m", f"kid {agent}")
    return branch


def _args(repo: Path, *, seat="sanctuary-director", answers=None):
    return SimpleNamespace(seat=seat, answers=answers, root=str(repo / ".agi"))


def _run(repo, capsys, **kw):
    rc = rotate.cmd_first_decision(_args(repo, **kw), repo / ".agi")
    return rc, capsys.readouterr().out


# --- proof bar 1: one pre-filled row per fixture round + the exact branch ---

def test_one_row_per_open_round_with_exact_branch(tmp_path, capsys):
    repo, wt = _make_repo(tmp_path)
    b1 = _make_round(repo, wt, "l4-x", "a00-aaaa", "a00-aaaa-deadbeef")
    b2 = _make_round(repo, wt, "l4-y", "a00-bbbb", "a00-bbbb-cafebabe",
                     verdict="inconclusive_lean_proved:55")

    rc, out = _run(repo, capsys)

    assert rc == 0
    # one `round:` row per fixture round, each naming the EXACT branch from
    # `git branch --list` (no truncation, no drift).
    assert out.count("round: loop/") == 2
    assert f"round: {b1}" in out
    assert f"round: {b2}" in out
    # parent row names the seat branch the round was cut from.
    assert "parent: seat/sanctuary-director@s2" in out
    # the bounded prompt appears EXACTLY once per row and is never answered.
    for b in (b1, b2):
        assert f"prompt: harvest {b} | cut <next queued node> | hold" in out


# --- proof bar 2: kids + verdicts + merge-base + behind are pre-filled ------

def test_row_prefills_kids_verdicts_mergebase_behind(tmp_path, capsys):
    repo, wt = _make_repo(tmp_path)
    b1 = _make_round(repo, wt, "l4-x", "a00-aaaa", "a00-aaaa-deadbeef",
                     verdict="proved")
    b2 = _make_round(repo, wt, "l4-y", "a00-bbbb", "a00-bbbb-cafebabe",
                     verdict="inconclusive_lean_proved:55")

    rc, out = _run(repo, capsys)

    assert rc == 0
    # each row carries its kid node id and the verdict frontmatter.
    assert "experiment:a00-aaaa-deadbeef (proved)" in out
    assert "experiment:a00-bbbb-cafebabe (inconclusive_lean_proved:55)" in out
    # merge-base is the seat branch's tip (branches cut from it): short sha.
    seat_tip = _git(repo, "rev-parse", "--short",
                    "seat/sanctuary-director@s2").stdout.strip()
    assert f"merge-base: {seat_tip}" in out
    # behind is 0: the rounds were cut from the current seat tip.
    assert "behind: 0" in out


# --- proof bar 3: never runs a merge (falsifier) ----------------------------

def test_harvest_answer_prints_merge_line_and_never_runs_it(tmp_path, capsys):
    repo, wt = _make_repo(tmp_path)
    b1 = _make_round(repo, wt, "l4-x", "a00-aaaa", "a00-aaaa-deadbeef")
    ans = tmp_path / "answers.txt"
    ans.write_text(f"harvest {b1}\n", encoding="utf-8")

    rc, out = _run(repo, capsys, answers=str(ans))

    assert rc == 0
    # the named next command is the git merge line carrying the EXACT branch.
    assert f"git merge --no-ff {b1}" in out
    # the FALSIFIER: nothing was merged. The branch still exists, still not an
    # ancestor of the seat branch, and the seat branch tip did not move.
    assert b1 in _git(repo, "branch", "--list").stdout
    rc_a = _git(repo, "merge-base", "--is-ancestor", b1,
                "seat/sanctuary-director@s2").returncode
    assert rc_a != 0  # still open — the merge was printed, never executed


# --- proof bar 5: the seat's OWN scope — a sibseat round is dropped --------

def test_sibseat_round_scoped_out_never_copying_seat_parent(tmp_path, capsys):
    """discriminator (b): a round cut by a DIFFERENT seat (a sibseat / parent
    round that forks at the shared season base) must NOT appear under --seat S
    — its agent id lives in ITS OWN seat's manifests, never this one's. It must
    not copy S's parent constant either. Exactly the live defect: 8-14 rows
    all stamped `parent: seat/sanctuary-director@s2` though most were other
    districts' rounds. FALSIFIER (tested here): a sibseat round still printing
    under --seat S with `parent: seat/S@s2`."""
    repo, wt = _make_repo(tmp_path)
    own = _make_round(repo, wt, "l4-own", "a00-ownaa", "a00-ownaa-deadbeef")
    # a round cut from MASTER by ANOTHER seat: its agent is never recorded in
    # THIS seat's manifests (manifest=False), so the manifest join drops it.
    sib = _make_round(repo, wt, "l4-sib", "a00-sibbb", "a00-sibbb-cafebabe",
                      base="master", manifest=False)

    rc, out = _run(repo, capsys)

    assert rc == 0
    # EXACTLY one row: the seat's own round only, never the sibseat round.
    assert out.count("round: loop/") == 1
    assert f"round: {own}" in out
    assert sib not in out
    # the printed parent is the seat branch DERIVED for that round — the branch
    # the manifest-verified round belongs to, never a constant copied from the
    # seat's own HEAD.
    assert "parent: seat/sanctuary-director@s2" in out
    # the sibseat round's kid never leaks into the seat's view either.
    assert "a00-sibbb" not in out


# --- proof bar 6: manifest-join discriminator (b) itself -------------------

def test_manifest_join_owns_exactly_the_recorded_round(tmp_path, capsys):
    """discriminator (b), red-first: a round belongs to seat S iff its agent
    id (parsed from the branch name) appears in ONE of S's own iteration
    manifests' `agents[].id`. Two open rounds cut from the SAME seat branch;
    only ONE is recorded in the seat's manifest. Exactly one row appears,
    with the correct parent — the other is dropped, never shown, never
    stamped with the seat's parent."""
    repo, wt = _make_repo(tmp_path)
    # both descend from the seat branch (identical fork), so ancestry (a)
    # cannot tell them apart — only the manifest join can.
    own = _make_round(repo, wt, "l4-own", "a00-ownaa", "a00-ownaa-deadbeef",
                      manifest=True)
    ghost = _make_round(repo, wt, "l4-ghost", "a00-ghost1", "a00-ghost1-deadbeef",
                        manifest=False)
    # sanity: the ghost really is NOT in the seat's manifests.
    assert "a00-ghost1" not in _manifest_agent_ids(repo)
    assert "a00-ownaa" in _manifest_agent_ids(repo)

    rc, out = _run(repo, capsys)

    assert rc == 0
    assert out.count("round: loop/") == 1
    assert f"round: {own}" in out
    assert f"round: {ghost}" not in out
    assert "a00-ghost1" not in out
    assert "parent: seat/sanctuary-director@s2" in out
    assert "parent: ? " not in out  # no unresolved parent ever printed


# --- proof bar 7: no manifest => no rows (under-count, never mis-attrib) ---

def test_no_matching_manifest_yields_no_rows(tmp_path, capsys):
    """If the seat's manifests do not record the open rounds (fresh / other
    seat's manifests absent), first-decision prints no rows for that seat —
    an under-count — never a row with a copied or guessed parent."""
    repo, wt = _make_repo(tmp_path)
    _make_round(repo, wt, "l4-x", "a00-aaaa", "a00-aaaa-deadbeef",
                manifest=False)

    rc, out = _run(repo, capsys)

    assert rc == 0
    assert "no open rounds for this seat" in out
    assert "round: loop/" not in out


# --- proof bar 4: answers replay yields the dispatch line for a cut ---------

def test_cut_answer_prints_dispatch_line(tmp_path, capsys):
    repo, wt = _make_repo(tmp_path)
    _make_round(repo, wt, "l4-x", "a00-aaaa", "a00-aaaa-deadbeef")
    ans = tmp_path / "answers.txt"
    ans.write_text("cut hypothesis:l4-some-next-node\n", encoding="utf-8")

    rc, out = _run(repo, capsys, answers=str(ans))

    assert rc == 0
    assert "python3 extensions/agi/bin/dispatch.py" in out
    assert "--target hypothesis:l4-some-next-node" in out
    # no merge line was emitted for a cut.
    assert "git merge --no-ff" not in out

def _make_repo_post(tmp_path: Path) -> tuple[Path, Path]:
    """Same shape as `_make_repo` but the seat is renamed to a POST
    (hypothesis:l4-a-seat-is-a-post-everywhere): the worktree lives at
    `.agi/worktrees/post-sanctuary-director` and the seat branch is
    `post/sanctuary-director@s2`. Returns (main, worktree)."""
    repo = tmp_path / "main"
    repo.mkdir(parents=True)
    _git(repo, "init", "-b", "master")
    _git(repo, "config", "user.email", "t@t")
    _git(repo, "config", "user.name", "t")
    (repo / "README").write_text("x\n")
    graph = repo / ".agi"
    (graph / "nodes" / ".geometry").mkdir(parents=True)
    (graph / "nodes" / "experiment").mkdir(parents=True)
    (graph / "config.json").write_text('{"metric_primary": "outcome_coverage"}')
    import json as _json
    _row = {"name": "sanctuary-director", "role": "director",
            "worktree": ".agi/worktrees/post-sanctuary-director",
            "pin_ref": "", "session_ref": "", "town": "all"}
    (graph / "nodes" / ".geometry" / "seats.md").write_text(
        "---\nid: config:seats\ntype: config\nseats:\n"
        "  - " + _json.dumps(_row) + "\n---\n", encoding="utf-8")
    (repo / ".gitignore").write_text("sessions/\n.agi/sessions/\n",
                                     encoding="utf-8")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-m", "init with graph dir + post row")
    _git(repo, "branch", "season/s2")
    _git(repo, "checkout", "-q", "season/s2")
    wt = repo / ".agi" / "worktrees" / "post-sanctuary-director"
    _git(repo, "worktree", "add", "-b", "post/sanctuary-director@s2",
         str(wt), "season/s2")
    (wt / "POST-EXCLUSIVE").write_text("post\n", encoding="utf-8")
    _git(wt, "add", "-A")
    _git(wt, "commit", "-m", "post-exclusive commit")
    return repo, wt


def test_seat_resolves_under_post_rename_branch_and_worktree(tmp_path, capsys):
    """hypothesis:l4-a-seat-is-a-post-everywhere — the CONVENTION readers
    resolve a post-renamed seat: `_fd_seat_branch` returns the `post/...@s2`
    branch, `_fd_seat_worktree` returns the `post-sanctuary-director` dir, and
    first-decision names the post base branch as the round's parent."""
    repo, wt = _make_repo_post(tmp_path)
    main = repo
    seat = "sanctuary-director"

    root_dir = repo / ".agi"
    # config:seats row points at the post- worktree, so the branch reader
    # should resolve it via the checked-out HEAD first; force the convention
    # fallback by resolving the branch for a name with no worktree row match.
    assert rotate._fd_seat_branch(root_dir, main, seat) == \
        "post/sanctuary-director@s2"
    assert rotate._fd_seat_worktree(root_dir, main, seat) == wt

    # first-decision across a round cut from the post base names post/ parent.
    b1 = _make_round(repo, wt, "l4-x", "a00-aaaa", "a00-aaaa-deadbeef",
                     base="post/sanctuary-director@s2")
    # _make_round writes the owned-manifest into the seat- sessions dir; the
    # post-renamed seat's reader owns FROM `.agi/worktrees/post-<seat>/...`,
    # so mirror the manifest there so the manifest-join sees the round as
    # this post seat's OWN.
    import json as _json
    pm = wt / ".agi" / "sessions" / "iter-L4.1"
    pm.mkdir(parents=True, exist_ok=True)
    (pm / "manifest.json").write_text(
        _json.dumps({"iter": "L4.1", "agents": [{"id": "a00-aaaa"}]}),
        encoding="utf-8")
    rc, out = _run(repo, capsys)
    assert rc == 0
    assert f"parent: post/sanctuary-director@s2" in out
    assert f"round: {b1}" in out


def test_seat_branch_falls_back_to_deprecated_seat_alias(tmp_path):
    """hypothesis:l4-a-seat-is-a-post-everywhere — the seat- spelling is still
    accepted as a one-season alias: a worktree/branch only present under the
    OLD name still resolves through `_fd_seat_branch` / `_fd_seat_worktree`."""
    repo, wt = _make_repo(tmp_path)
    root_dir = repo / ".agi"
    assert rotate._fd_seat_branch(root_dir, repo, "sanctuary-director") == \
        "seat/sanctuary-director@s2"
    assert rotate._fd_seat_worktree(root_dir, repo, "sanctuary-director") == wt
