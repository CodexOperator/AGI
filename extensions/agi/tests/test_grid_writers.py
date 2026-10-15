"""R1: the REPO-WIDE GRID-WRITER SCANNER (SM's R1; belam's flip depends on 'a new writer is caught'). goal:g7.16.1.11.13, section "refs/grid writers, pushers and fetchers". Re-cut v2 (SM 17:35Z, DG1 17:36Z): the rows compare WITHOUT line numbers. Re-cut v3 (SM, DG1 19:2xZ): the shape row compares the pathspec TOKENS (shlex), not substrings.

The node PINS eight `git grep` commands C1-C8 and their verbatim output at one sha (2e92b6447a); its blocks keep their `path:N:` numbers (informational, at that sha). These rows run the SAME command, as the node prints it, at HEAD of a git repo and compare what it FOUND:
  C1 every ref writer (update-ref | commit-tree | mktree | hash-object -w) · C2 every user of the grid push-spec builders · C3 every user of the fetch-spec builders ·
  C4 every wildcard push (--all | --mirror | refs/*) · C5 every push site, per file (the `path:count` lines) · C6 the `refs/grid` literal outside grid.py ·
  C7 every fetch consumer · C8 every caller of the gated verbs (`grid.py commit | push-changed | sync`, v4 of the list).
C4w (SM: widen C4): the same scan with `refs/grid/\\*` added to the pattern; its extra hits at the pin are the comments and docs in C4W_EXTRA (no hand-spelled `refs/grid/*` push exists).
COMPARE (path, TEXT): every `path:N:text` line becomes `path:text` on BOTH sides and the two lists are compared SORTED (a multiset): a pure line SHIFT or a reorder is GREEN; a changed, added, removed or MOVED-to-another-file matching line is RED. The node's `cut -c1-120` makes the visible text depend on the digit width of N, so each text is cut to the budget of a 5-digit N (120 - len(path) - 7) before comparing: a shift across a digit boundary is GREEN too. C5 is `path:count` and is compared exactly (a shift cannot change a count).
A NEW writer, pusher, fetcher, builder user or literal anywhere under extensions/ src/ .agi/nodes/.geometry changes one of the outputs and the row is RED until a person re-cuts the node (classifying the site); C6 counts comments and docstrings on purpose.

The blocks are READ FROM THE GOAL FILE by their C-heading (`C1 ...` followed by a ``` fence whose first line is `$ <command>`), so a row cannot drift from the node, and a node that loses a block, a command or a scope part is RED.
HERMETIC: only `git grep` on tracked files, `sh`, `cut`, `git archive`/`tar` for the scratch copies; LC_ALL=C. Env: GRID_SCAN_ROOT=<repo> (default: the repo that holds this file) runs a scratch copy of the real tree.
"""
from __future__ import annotations

import difflib
import os
import re
import shlex
import shutil
import subprocess
from pathlib import Path

import pytest

HERE = Path(__file__).resolve()
NODE_REL = ".agi/nodes/goal/g7.16.1.11.13.md"
HEADING = "## refs/grid writers, pushers and fetchers"
IDS = ["C1", "C2", "C3", "C4", "C5", "C6", "C7", "C8"]
#: the scope every command shares, as the pathspec TOKENS the shell hands git (the node prints the four exclusions single-quoted): where a writer can hide, and what is out of it
SCOPE = ["extensions", "src", ".agi/nodes/.geometry", ":!extensions/agi/tests", ":!*.js", ":!*.json", ":!extensions/**/*.md"]


def repo_root() -> Path:
    if os.environ.get("GRID_SCAN_ROOT"):
        return Path(os.environ["GRID_SCAN_ROOT"])
    top = subprocess.run(["git", "-C", str(HERE.parent), "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()
    assert top, "run inside a git repo"
    return Path(top)


ROOT = repo_root()


def read_blocks(root: Path | None = None) -> dict[str, tuple[str, list[str]]]:
    """{C1: (command, [output lines])} from the goal file (of `root`, default the repo), by C-heading."""
    node = (root or ROOT) / NODE_REL
    assert node.exists(), f"{NODE_REL} does not exist in {ROOT}"
    text = node.read_text()
    assert HEADING in text, f"{NODE_REL} has no section {HEADING!r}"
    sec = text[text.index(HEADING):]
    nxt = sec.find("\n## ", 5)
    sec = sec if nxt < 0 else sec[:nxt]
    out = {}
    for m in re.finditer(r"^(C[1-8]) [^\n]*\n```\n(.*?)\n```", sec, re.S | re.M):
        lines = m.group(2).split("\n")
        out[m.group(1)] = (lines[0], lines[1:])
    return out


def pathspec(cmd: str) -> list[str]:
    """The pathspec tokens of a node command: what follows its first bare `--` up to the pipe (`$ ` prefix and `| cut` tail dropped), shell-split like the shell does."""
    toks = shlex.split(cmd[2:])
    if "--" not in toks:
        return []
    after = toks[toks.index("--") + 1:]
    return after[:after.index("|")] if "|" in after else after


def shape_problems(blocks: dict[str, tuple[str, list[str]]]) -> list[str]:
    """What is wrong with the node's C-blocks: a missing / extra block, a non-`git grep` tool, a scope token that is not a WHOLE pathspec token of the command (a substring is not
    enough: `extensions` is also inside `:!extensions/agi/tests`), an empty pinned block."""
    bad = []
    if sorted(blocks) != IDS:
        bad.append(f"the node's C-blocks: {sorted(blocks)}")
    for cid, (cmd, lines) in blocks.items():
        if not cmd.startswith("$ git grep "):
            bad.append(f"{cid}: not a git grep: {cmd[:80]}")
        spec = pathspec(cmd)
        bad += [f"{cid}: the command lost scope {part!r}: {cmd}" for part in SCOPE if part not in spec]
        if not lines:
            bad.append(f"{cid}: an empty pinned block (a scanner that pins nothing)")
    return bad


def run(cmd: str, root: Path | None = None) -> list[str]:
    r = subprocess.run(["sh", "-c", cmd], cwd=root or ROOT, capture_output=True, env={"PATH": "/usr/bin:/bin", "LC_ALL": "C", "HOME": "/nonexistent",
                                                                                      "GIT_CONFIG_GLOBAL": "/dev/null", "GIT_CONFIG_SYSTEM": "/dev/null"})
    assert r.returncode in (0, 1), (cmd, r.returncode, r.stderr[-300:])      # grep: 1 = no match
    return r.stdout.decode("utf-8", "replace").split("\n")[:-1]


#: `path:N:text` (grep -n) -> the key `path:text`, the text cut to the budget of a 5-digit N under the node's `cut -c1-120`
_NUMBERED = re.compile(r"^(?P<path>[^:\n]+):(?P<n>\d+):(?P<text>.*)$")


def norm(lines: list[str]) -> list[str]:
    out = []
    for l in lines:
        m = _NUMBERED.match(l)
        if not m:
            out.append(l)
            continue
        path, text = m.group("path"), m.group("text")
        out.append(f"{path}:{text[:max(0, 120 - len(path) - 7)]}")
    return sorted(out)


#: C4's pattern widened with the hand-spelled grid wildcard; the 5 hits it adds at the pin are comments and docs (a call would be a NEW site, and RED)
C4W_OLD = "(--all|--mirror|refs/\\*)"
C4W_NEW = "(--all|--mirror|refs/\\*|refs/grid/\\*)"
C4W_EXTRA = [
    ".agi/nodes/.geometry/crons.md:162:(every 5 minutes, snapshot + push refs/grid/*) and `branch_push` (hourly).",
    "extensions/agi/bin/grid.py:49:  grid.py sync [REMOTE]             # push refs/grid/* to origin (manual/one-off)",
    "extensions/agi/bin/grid.py:250:    ARE retired. Retired, rotate._push's `refs/grid/*` push and `grid.py sync`",
    "extensions/agi/bin/rotate.py:9624:        # push origin season2/main THEN origin refs/grid/*:refs/grid/*, both",
    "extensions/agi/guard/sanctuary-watch:159:- Never pass --allow-branch to grid.py; never push refs/grid/* wholesale.",
]


def scan_failures(root: Path | None = None) -> list[str]:
    """Every C-id whose scan in `root` (default: the repo) differs from the node's pinned block, compared as (path, text) multisets (C5: path:count, exactly)."""
    bad = []
    blocks = read_blocks()
    for cid in ("C1", "C2", "C3", "C4", "C6", "C7", "C8"):
        cmd, pinned = blocks[cid]
        if norm(run(cmd[2:], root)) != norm(pinned):
            bad.append(cid)
    cmd, pinned = blocks["C5"]
    if run(cmd[2:], root) != pinned:
        bad.append("C5")
    cmd4, pinned4 = blocks["C4"]
    assert C4W_OLD in cmd4, f"C4's pattern is no longer {C4W_OLD}: {cmd4[:200]}"
    if norm(run(cmd4[2:].replace(C4W_OLD, C4W_NEW, 1), root)) != norm(pinned4 + C4W_EXTRA):
        bad.append("C4w")
    return bad


def test_the_node_pins_all_eight_commands_by_c_heading_over_one_shared_scope():
    """C1-C8 are all in the node, each a `$ git grep ...` over the SAME scope (extensions, src, .agi/nodes/.geometry; the tests, js, json and md files excluded), so a node
    that drops a block, swaps the tool, or narrows the scan to hide a site is RED. The scope is compared as whole pathspec TOKENS (shlex), not as substrings."""
    assert shape_problems(read_blocks()) == []


@pytest.mark.parametrize("cid,drop", [("C1", " extensions"), ("C5", " src"), ("C8", " .agi/nodes/.geometry"), ("C2", " ':!extensions/agi/tests'"), ("C7", " ':!extensions/**/*.md'")])
def test_the_shape_row_is_red_when_a_node_command_drops_one_scope_token(tmp_path, cid, drop):
    """SR-1 (DG1 19:2xZ): a scratch copy of the NODE with ONE scope token cut from ONE command is RED. The `extensions` case is the substring trap: with ` extensions` gone from C1 the
    text `extensions` is still inside `':!extensions/agi/tests'` and `':!extensions/**/*.md'`, so `part in cmd` stayed GREEN while the scan silently lost its positive include."""
    text = (ROOT / NODE_REL).read_text()
    at = re.search(rf"^{cid} [^\n]*\n```\n\$ [^\n]*", text, re.M)
    assert at, cid
    line = at.group(0)
    assert line.count(drop) == 1, (cid, drop)
    mutant = tmp_path / NODE_REL
    mutant.parent.mkdir(parents=True)
    mutant.write_text(text.replace(line, line.replace(drop, "", 1), 1))
    bad = shape_problems(read_blocks(tmp_path))
    assert bad and all(b.startswith(f"{cid}: the command lost scope") for b in bad), bad


@pytest.mark.parametrize("cid", ["C1", "C2", "C3", "C4", "C6", "C7", "C8"])
def test_the_scan_output_at_head_equals_the_nodes_pinned_block_without_line_numbers(cid):
    """(a) the SAME command as the node prints it, run at HEAD, finds the SAME (path, text) multiset as the node's block: a new writer (C1), a new user of a push-spec builder (C2)
    or fetch-spec builder (C3), a wildcard push (C4) or a `refs/grid` literal outside grid.py (C6, comments and docstrings included: intended, the node is then re-cut)
    changes it and is RED until the node is re-cut. A line SHIFT does not."""
    cmd, pinned = read_blocks()[cid]
    got = run(cmd[2:])
    diff = "\n".join(list(difflib.unified_diff(norm(pinned), norm(got), "node", "HEAD", lineterm="", n=0))[:30])
    assert norm(got) == norm(pinned), f"{cid}: the scan at HEAD differs from the node's pinned block (re-cut the node, classifying each new site):\n{diff}"


def test_the_push_sites_per_file_at_head_equal_the_nodes_pinned_counts():
    """(b) C5: the per-file push-site counts (`path:N`) at HEAD equal the node's block: one more push in cli.py or rotate.py, or a push in a file that had none, is RED. Counts are shift-proof."""
    cmd, pinned = read_blocks()["C5"]
    got = run(cmd[2:])
    assert all(re.fullmatch(r".+:\d+", l) for l in pinned), f"C5's block must be `path:count` lines: {pinned[:3]}"
    diff = "\n".join(list(difflib.unified_diff(pinned, got, "node", "HEAD", lineterm="", n=0))[:30])
    assert got == pinned, f"C5: the push sites per file differ from the node's block:\n{diff}"


def test_c4_widened_with_refs_grid_wildcard_finds_only_the_pinned_comments():
    """(c) C4w (SM): the node's C4 command with `refs/grid/\\*` added to the pattern finds the node's C4 block plus the 5 comment / doc lines in C4W_EXTRA, nothing else:
    a hand-spelled `git push origin refs/grid/*:refs/grid/*` anywhere in scope is RED here (C4's own `refs/\\*` is the literal `refs/*`, which `refs/grid/*` is not)."""
    cmd, pinned = read_blocks()["C4"]
    assert C4W_OLD in cmd, f"C4's pattern changed: {cmd[:200]}"
    got = run(cmd[2:].replace(C4W_OLD, C4W_NEW, 1))
    diff = "\n".join(list(difflib.unified_diff(norm(pinned + C4W_EXTRA), norm(got), "node+extra", "HEAD", lineterm="", n=0))[:30])
    assert norm(got) == norm(pinned + C4W_EXTRA), f"C4w: the widened scan differs:\n{diff}"


def test_the_scanner_can_see_a_change_at_all(tmp_path):
    """Witness (the rows can fail): in a scratch repo a tracked file under extensions/ that gains a `git push` line changes the C5-shaped output."""
    r = tmp_path / "w"
    (r / "extensions").mkdir(parents=True)
    (r / "extensions" / "a.py").write_text("x = 1\n")
    env = {**os.environ, "GIT_CONFIG_GLOBAL": "/dev/null", "GIT_CONFIG_SYSTEM": "/dev/null"}
    subprocess.run(["git", "-C", str(r), "init", "-q"], env=env, check=True)
    subprocess.run(["git", "-C", str(r), "add", "-A"], env=env, check=True)
    cmd = "git grep -c -E 'git push' -- extensions"
    before = subprocess.run(["sh", "-c", cmd], cwd=r, capture_output=True, text=True, env=env).stdout
    (r / "extensions" / "a.py").write_text("x = 1\nsubprocess.run('git push origin x')\n")
    after = subprocess.run(["sh", "-c", cmd], cwd=r, capture_output=True, text=True, env=env).stdout
    assert before == "" and after == "extensions/a.py:1\n", (before, after)


# ====
# d: SCRATCH COPIES of the real tree: a shift is GREEN, a new / changed / moved site is RED
# ====

GIT_ENV = {"PATH": "/usr/bin:/bin", "HOME": "/nonexistent", "GIT_CONFIG_GLOBAL": "/dev/null", "GIT_CONFIG_SYSTEM": "/dev/null",
           "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t", "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t"}
SCAN_DIRS = ["extensions", "src", ".agi/nodes/.geometry"]


@pytest.fixture(scope="module")
def base_copy(tmp_path_factory) -> Path:
    """A scratch git repo holding the scan's scope (the TRACKED files of ROOT, working-tree bytes) once; each row copies it."""
    dst = tmp_path_factory.mktemp("scan") / "base"
    dst.mkdir()
    ls = subprocess.run(["git", "-C", str(ROOT), "ls-files", "-z", "--", *SCAN_DIRS], capture_output=True, env=GIT_ENV)
    assert ls.returncode == 0, ls.stderr[-300:]
    for rel in [p for p in ls.stdout.decode("utf-8", "replace").split("\0") if p]:
        src = ROOT / rel
        if src.is_file() or src.is_symlink():
            (dst / rel).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst / rel, follow_symlinks=False)
    for cmd in (["init", "-q"], ["add", "-A"], ["commit", "-q", "-m", "base", "--no-gpg-sign"]):
        subprocess.run(["git", "-C", str(dst), *cmd], check=True, capture_output=True, env=GIT_ENV)
    return dst


def scratch(base: Path, tmp_path: Path) -> Path:
    dst = tmp_path / "s"
    shutil.copytree(base, dst, symlinks=True)
    return dst


def edit(root: Path, rel: str, fn) -> None:
    p = root / rel
    p.write_text(fn(p.read_text()))
    subprocess.run(["git", "-C", str(root), "add", "-A"], check=True, capture_output=True, env=GIT_ENV)


def test_d0_the_unmodified_scratch_copy_is_green(base_copy, tmp_path):
    """The control for every d-row: an untouched copy of the tree passes all nine comparisons (C1-C8 and C4w) (so a RED below is the edit, not the copy)."""
    assert scan_failures(scratch(base_copy, tmp_path)) == []


def test_d1_a_comment_line_under_the_shebang_shifts_every_number_and_stays_green(base_copy, tmp_path):
    """SM's measurement: ONE comment line under rotate.py's shebang (no new site) turned 4 of 8 rows RED when the rows pinned numbers. Now: GREEN. Also under grid.py's first line."""
    s = scratch(base_copy, tmp_path)
    edit(s, "extensions/agi/bin/rotate.py", lambda t: t.replace("\n", "\n# a harmless comment\n", 1))
    edit(s, "extensions/agi/bin/grid.py", lambda t: "# a harmless comment\n" + t)
    assert scan_failures(s) == []


def test_d2_a_shift_across_a_digit_boundary_stays_green(base_copy, tmp_path):
    """The node's `cut -c1-120` makes the visible text depend on the width of N: 300 comment lines at the top of grid.py move its sites from 2-3 digits to 3-4 digits (and long lines lose or gain a character at the cut): GREEN."""
    s = scratch(base_copy, tmp_path)
    edit(s, "extensions/agi/bin/grid.py", lambda t: "# pad\n" * 300 + t)
    edit(s, "extensions/agi/bin/cli.py", lambda t: "# pad\n" * 5000 + t)
    assert scan_failures(s) == []


def test_d3_a_pure_reorder_of_two_matching_lines_stays_green(base_copy, tmp_path):
    """The comparison is a multiset: two `refs/grid` comment lines of level3.py swapped (same lines, other order and other numbers) are not a change."""
    s = scratch(base_copy, tmp_path)

    def swap(t: str) -> str:
        ls = t.split("\n")
        ix = [i for i, l in enumerate(ls) if "refs/grid" in l]
        assert len(ix) >= 2, ix
        ls[ix[0]], ls[ix[1]] = ls[ix[1]], ls[ix[0]]
        return "\n".join(ls)
    edit(s, "extensions/agi/bin/level3.py", swap)
    assert scan_failures(s) == []


@pytest.mark.parametrize("rel,line,want", [
    ("extensions/agi/bin/metrics.py", "subprocess.run(['git', 'update-ref', 'refs/grid/x', 'abc'])", ["C1", "C6"]),
    (".agi/nodes/.geometry/engine-wrap.md", "git commit-tree -p HEAD HEAD^{tree}", ["C1"]),
    ("src/w.py", "subprocess.run('git hash-object -w f')", ["C1"]),
])
def test_d4_a_new_update_ref_style_writer_anywhere_in_scope_is_red(base_copy, tmp_path, rel, line, want):
    """A NEW writer line in a file under extensions/, .agi/nodes/.geometry or a NEW file under src/ is RED (C1; the first also names refs/grid: C6)."""
    s = scratch(base_copy, tmp_path)
    p = s / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    edit(s, rel, lambda t, _l=line: t + ("\n" if t and not t.endswith("\n") else "") + _l + "\n") if p.exists() else (p.write_text(line + "\n"), subprocess.run(["git", "-C", str(s), "add", "-A"], check=True, capture_output=True, env=GIT_ENV))
    bad = scan_failures(s)
    for w in want:
        assert w in bad, f"{rel}: a new writer line must be RED on {w}: {bad}"


def test_d5_a_changed_matching_line_is_red(base_copy, tmp_path):
    """The TEXT matters: grid.py's own `update-ref` call gains a trailing word: C1 is RED (same path, same count, different text)."""
    s = scratch(base_copy, tmp_path)
    edit(s, "extensions/agi/bin/grid.py", lambda t: t.replace('res = git_try(root, "update-ref", ref, commit, tip or "")', 'res = git_try(root, "update-ref", ref, commit, tip or "")  # changed', 1))
    assert "C1" in scan_failures(s)


def test_d6_a_site_moved_to_another_file_is_red(base_copy, tmp_path):
    """The PATH matters: the same `update-ref` line deleted from grid.py and added to cli.py is RED (a multiset of (path, text) changes even though the text and the count are the same)."""
    s = scratch(base_copy, tmp_path)
    ln = 'res = git_try(root, "update-ref", ref, commit, tip or "")'
    edit(s, "extensions/agi/bin/grid.py", lambda t: t.replace(ln, "res = None", 1))
    edit(s, "extensions/agi/bin/cli.py", lambda t: t + "\n    " + ln + "\n")
    assert "C1" in scan_failures(s)


def test_d7_a_new_push_a_new_builder_user_and_a_new_literal_are_red(base_copy, tmp_path):
    """C5 (a `git push` in a file that had none), C2 (`grid.PUSH_SPEC`), C3 (`grid.FETCH_SPEC`), C4 (a `--mirror` push), C6 (a `refs/grid` mention in a comment), C7 (a new `git fetch`), C8 (a new caller of `grid.py commit`, and a new `with_name('grid.py')`): one edit each."""
    for i, (rel, line, want) in enumerate([("extensions/agi/bin/sensei.py", "subprocess.run('git push origin x')", "C5"),
                            ("extensions/agi/bin/metrics.py", "x = grid.PUSH_SPEC", "C2"),
                            ("extensions/agi/bin/heal.py", "x = grid.FETCH_SPEC", "C3"),
                            ("extensions/agi/bin/season.py", "subprocess.run('git push --mirror origin')", "C4"),
                            ("extensions/agi/bin/level3.py", "# talks about refs/grid/node/x", "C6"),
                            ("extensions/agi/bin/metrics.py", "subprocess.run([\"git\", \"fetch\", \"origin\"])", "C7"),
                            ("extensions/agi/bin/metrics.py", "os.system(f'python3 {grid_py} commit --all')", "C8"),
                            ("extensions/agi/bin/heal.py", "p = Path(__file__).with_name(\"grid.py\")", "C8")]):
        s = scratch(base_copy, tmp_path / f"{i}{want}")
        edit(s, rel, lambda t, _l=line: t + "\n" + _l + "\n")
        assert want in scan_failures(s), f"{rel}: {line!r} must be RED on {want}"


def test_d8_a_hand_spelled_grid_wildcard_push_is_red_on_the_widened_c4(base_copy, tmp_path):
    """SM's gap: `git push origin 'refs/grid/*:refs/grid/*'` carries no builder name and not `refs/*`: C2 and C4 miss it; C4w catches it, and so does C6 (the `refs/grid` literal outside grid.py); C5 does NOT (its pattern has no `'push', 'origin'` list form) and neither do C2 / C4."""
    s = scratch(base_copy, tmp_path)
    edit(s, "extensions/agi/bin/cli.py", lambda t: t + "\n    subprocess.run(['git', 'push', 'origin', 'refs/grid/*:refs/grid/*'])\n")
    bad = scan_failures(s)
    assert "C4w" in bad and "C6" in bad and "C2" not in bad and "C4" not in bad, bad
